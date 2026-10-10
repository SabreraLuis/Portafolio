#!/usr/bin/env python3
"""Browser QA. Requires Playwright + system Chromium (or Playwright Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json, os
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>','')
html=html.replace('</body>','<script>'+js+'</script></body>')
report={'widths':[],'interactions':{},'browser_errors':[],'limits':['inline-local resources; not a live CDN test','Google Fonts network disabled','Safari and physical devices not covered','sessionStorage persistence not verifiable in about:blank sandbox']}
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-background-networking'])
    for width in [320,360,375,390,430,650,768,900,1024,1280,1440,1920]:
        p=browser.new_page(viewport={'width':width,'height':844 if width<700 else 900})
        errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
        p.set_content(html,wait_until='domcontentloaded');p.wait_for_timeout(50)
        vals=p.evaluate('''() => ({w:innerWidth,scroll:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),clipped:[...document.querySelectorAll('h1,h2,h3')].filter(x=>{let r=x.getBoundingClientRect(),s=getComputedStyle(x);return r.right>innerWidth+2||r.left<-2}).length})''')
        report['widths'].append({'width':width,'overflow':max(0,vals['scroll']-width),'js_errors':errs,'headings_outside_viewport':vals['clipped']})
        p.close()
    p=browser.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    p.set_content(html,wait_until='domcontentloaded')
    p.locator('#menu-btn').click()
    report['interactions']['menu_opens']=p.locator('#menu-btn').get_attribute('aria-expanded')=='true'
    report['interactions']['pdf_visible_in_menu']=p.locator('.navigation.is-open .mobile-nav-cv').is_visible()
    p.keyboard.press('Escape')
    report['interactions']['menu_escape']=p.locator('#menu-btn').get_attribute('aria-expanded')=='false'
    report['interactions']['pdf_visible_in_hero']=p.locator('.action-pdf').is_visible()
    p.locator('#motion-toggle').click()
    report['interactions']['fx_pauses']=p.evaluate('document.documentElement.dataset.motion')=='off'
    p.locator('#motion-toggle').click()
    report['interactions']['fx_resumes']=p.evaluate('document.documentElement.dataset.motion')=='on'
    p.locator('#replay').click();x=p.locator('.hero .name-line:first-child>span').evaluate('el=>getComputedStyle(el).transform');p.wait_for_timeout(200)
    report['interactions']['replay_moves']=x!=p.locator('.hero .name-line:first-child>span').evaluate('el=>getComputedStyle(el).transform')
    p.locator('#archivo').scroll_into_view_if_needed();p.wait_for_timeout(170)
    report['interactions']['scroll_reveals']=p.locator('.dossier').first.evaluate("x=>x.classList.contains('is-visible')")
    p.locator('.dossier-jump a[href="#dossier-prod"]').click()
    report['interactions']['case_index_anchor']=p.evaluate("location.hash === '#dossier-prod'")
    p.locator('.decision-interlude').scroll_into_view_if_needed()
    report['interactions']['interlude_visible']=p.locator('.decision-interlude').is_visible()
    p.wait_for_timeout(160)
    report['interactions']['interlude_motion_measurable']=p.locator('.decision-interlude .fx-razor').evaluate("e=>e.getAnimations().some(a=>a.playState==='running')")
    p.set_viewport_size({'width':1440,'height':900})
    report['interactions']['menu_reset_on_resize']=p.locator('#menu-btn').get_attribute('aria-expanded')=='false'
    p.close()
    red=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    red.set_content(html,wait_until='domcontentloaded')
    report['interactions']['reduced_default_off']=red.evaluate('document.documentElement.dataset.motion')=='off'
    red.locator('#replay').click();report['interactions']['reduced_explicit_opt_in']=red.evaluate('document.documentElement.dataset.motion')=='on'
    red.locator('#motion-toggle').click();report['interactions']['reduced_explicit_opt_out']=red.evaluate('document.documentElement.dataset.motion')=='off'
    red.close()
    nojs=browser.new_page(viewport={'width':390,'height':844},java_script_enabled=False)
    nojs.set_content(html,wait_until='domcontentloaded')
    report['interactions']['nojs_navigation']=nojs.locator('#navigation a[href="#archivo"]').is_visible()
    report['interactions']['nojs_pdf']=nojs.locator('.mobile-nav-cv').is_visible()
    nojs.close();browser.close()
    report['browser_errors']=errs
print(json.dumps(report,ensure_ascii=False,indent=2))
(root/'QA_POLISH.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if not all(x['overflow']==0 and not x['js_errors'] and x['headings_outside_viewport']==0 for x in report['widths']) or not all(report['interactions'].values()) or errs:
    raise SystemExit('QA FAILED')
