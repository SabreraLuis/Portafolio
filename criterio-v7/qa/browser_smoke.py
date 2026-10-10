#!/usr/bin/env python3
"""CRITERIO CV: real Chromium interactions with locally inlined assets."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,re,shutil,json

root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>','')
html=html.replace('</body>','<script>'+js+'</script></body>')
result={'viewports':[],'interactions':{},'errors':[]}
executable=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser')
with sync_playwright() as pw:
    kwargs={'executable_path':executable} if executable else {}
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-background-networking'],**kwargs)
    for width in [320,360,375,390,430,650,768,900,1024,1280,1440,1920]:
        p=browser.new_page(viewport={'width':width,'height':844 if width<700 else 900})
        errors=[];p.on('pageerror',lambda error:errors.append(str(error)))
        p.set_content(html,wait_until='domcontentloaded')
        data=p.evaluate("""() => ({
          documentWidth: Math.max(document.body.scrollWidth,document.documentElement.scrollWidth),
          clippedTitles:[...document.querySelectorAll('h1,h2,h3')].filter(el=>{
            const r=el.getBoundingClientRect();return r.left<-2||r.right>innerWidth+2
          }).length
        })""")
        result['viewports'].append({'width':width,'overflow':max(0,data['documentWidth']-width),'clippedTitles':data['clippedTitles'],'errors':errors})
        p.close()
    p=browser.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    p.set_content(html,wait_until='domcontentloaded')
    p.locator('#menu-btn').click()
    result['interactions']['menu']=p.locator('#menu-btn').get_attribute('aria-expanded')=='true'
    result['interactions']['pdf_in_menu']=p.locator('.navigation.is-open .mobile-nav-cv').is_visible()
    p.keyboard.press('Escape')
    result['interactions']['menu_escape']=p.locator('#menu-btn').get_attribute('aria-expanded')=='false'
    result['interactions']['pdf_in_hero']=p.locator('.action-pdf').is_visible()
    p.locator('#motion-toggle').click()
    result['interactions']['motion_off']=p.evaluate('document.documentElement.dataset.motion')=='off'
    p.locator('#motion-toggle').click()
    result['interactions']['motion_on']=p.evaluate('document.documentElement.dataset.motion')=='on'
    p.locator('#replay').click()
    frame_a=p.locator('.hero .name-line:first-child>span').evaluate('e=>getComputedStyle(e).transform')
    p.wait_for_timeout(220)
    frame_b=p.locator('.hero .name-line:first-child>span').evaluate('e=>getComputedStyle(e).transform')
    result['interactions']['replay_motion_observed']=frame_a!=frame_b
    p.locator('#archivo').scroll_into_view_if_needed()
    p.wait_for_timeout(220)
    result['interactions']['scroll_reveal']=p.locator('.dossier').first.evaluate("e=>e.classList.contains('is-visible')")
    p.set_viewport_size({'width':1440,'height':900})
    result['interactions']['desktop_resize']=p.locator('#menu-btn').get_attribute('aria-expanded')=='false'
    p.close()
    red=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    red.set_content(html,wait_until='domcontentloaded')
    result['interactions']['reduced_default_off']=red.evaluate('document.documentElement.dataset.motion')=='off'
    red.locator('#replay').click()
    result['interactions']['reduced_user_opt_in']=red.evaluate('document.documentElement.dataset.motion')=='on'
    red.locator('#motion-toggle').click()
    result['interactions']['reduced_user_opt_out']=red.evaluate('document.documentElement.dataset.motion')=='off'
    red.close()
    nojs=browser.new_page(viewport={'width':390,'height':844},java_script_enabled=False)
    nojs.set_content(html,wait_until='domcontentloaded')
    result['interactions']['no_js_nav']=nojs.locator('#navigation a[href="#archivo"]').is_visible()
    result['interactions']['no_js_pdf']=nojs.locator('.mobile-nav-cv').is_visible()
    nojs.close();browser.close()
    result['errors']=errs
print(json.dumps(result,indent=2,ensure_ascii=False))
if any(row['overflow']>0 or row['clippedTitles'] or row['errors'] for row in result['viewports']) or not all(result['interactions'].values()) or result['errors']:
    raise SystemExit('Browser QA failed')
