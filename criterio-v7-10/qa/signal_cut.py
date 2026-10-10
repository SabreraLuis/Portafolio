#!/usr/bin/env python3
"""CRITERIO V7.10: visual, motion, content and keyboard smoke through Chromium file:// local source."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,shutil,sys
root=Path(__file__).resolve().parents[1]
raw=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>', '', raw)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>', '', html)
html=html.replace('<link rel="stylesheet" href="./styles.css">', '<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>', '')
html=html.replace('</body>', '<script>'+js+'</script></body>')
assert (root/'cv-luis-sabrera.pdf').read_bytes().startswith(b'%PDF')
report={'widths':[],'interactions':{},'accessibility':{},'source':'chromium-inlined-exact-src-no-external-fonts'}
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox','--disable-background-networking'])
    for w in [320,360,375,390,430,650,700,768,900,1024,1280,1440,1920]:
        page=browser.new_page(viewport={'width':w,'height':850 if w<768 else 900},reduced_motion='no-preference')
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        page.wait_for_timeout(180)
        d=page.evaluate('''() => {const headings=[...document.querySelectorAll('h1,h2,h3,h4')];return {scrollWidth:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),badHeadings:headings.filter(e=>{let r=e.getBoundingClientRect();return r.left<-2||r.right>innerWidth+2}).map(e=>e.innerText.slice(0,45)),motion:document.documentElement.dataset.motion,glitchCount:document.querySelectorAll('[data-fx-burst] .fx-glitch-ghost[aria-hidden=true]').length,links:[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash&&!document.getElementById(a.hash.slice(1))).length}}''')
        report['widths'].append({'width':w,'overflow':max(0,d['scrollWidth']-w),'clippedHeadings':d['badHeadings'],'errors':errors, 'glitchClones':d['glitchCount'],'brokenAnchors':d['links']})
        if w in (390,1440):
            (root/'previews').mkdir(exist_ok=True)
            page.screenshot(path=str(root/'previews'/f'hero-{w}.png'))
            page.locator('#archivo').scroll_into_view_if_needed()
            page.wait_for_timeout(150)
            page.screenshot(path=str(root/'previews'/f'archive-{w}.png'))
        page.close()
    p=browser.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
    errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
    p.set_content(html,wait_until='domcontentloaded')
    p.locator('#menu-btn').click()
    report['interactions']['menu_opens']=p.locator('#menu-btn').get_attribute('aria-expanded')=='true'
    p.keyboard.press('Escape')
    report['interactions']['menu_esc_closes']=p.locator('#menu-btn').get_attribute('aria-expanded')=='false'
    report['interactions']['hero_text_real']=p.locator('.fx-glitch-base').inner_text()=='ACCIÓN.'
    report['interactions']['decorative_only']=p.locator('.fx-glitch-ghost[aria-hidden=true]').count()==2
    p.locator('#replay').click()
    p.wait_for_timeout(220)
    report['interactions']['glitch_animation_running']=p.evaluate("""()=>[...document.querySelectorAll('.fx-glitch-ghost')].some(e=>getComputedStyle(e).animationName.includes('signal-glitch')&&e.getAnimations().some(a=>a.playState==='running'))""")
    report['interactions']['razor_animation_running']=p.evaluate("""()=>document.querySelector('.hero-visual .fx-razor')?.getAnimations().some(a=>a.playState==='running')""")
    p.locator('#motion-toggle').click()
    report['interactions']['motion_off']=p.evaluate('document.documentElement.dataset.motion')=='off'
    report['interactions']['glitch_stopped']=p.evaluate("""()=>[...document.querySelectorAll('.fx-glitch-ghost')].every(e=>getComputedStyle(e).animationName==='none')""")
    p.locator('#motion-toggle').click()
    report['interactions']['motion_on']=p.evaluate('document.documentElement.dataset.motion')=='on'
    p.locator('#dossier-prod').scroll_into_view_if_needed()
    p.wait_for_timeout(250)
    report['interactions']['evidence_case_visible']=p.locator('#dossier-prod').is_visible()
    p.locator('#contacto').scroll_into_view_if_needed()
    report['interactions']['email_link']=p.locator('a[href="mailto:lpumsm@gmail.com"]').count()>0
    report['interactions']['pdf_link']=p.locator('a[href$="cv-luis-sabrera.pdf"]').count()>0
    report['accessibility']['unique_h1']=p.locator('h1').count()==1
    report['accessibility']['no_extra_ghosts_announced']=p.locator('.fx-glitch-ghost:not([aria-hidden])').count()==0
    report['accessibility']['src_content']=all(t in p.content() for t in ['AMAZON','20 PROD','SUNAFIL','STUDIOS'])
    report['interactions']['no_js_error']=len(errors)==0
    p.close()
    reduced=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    reduced.set_content(html,wait_until='domcontentloaded')
    report['accessibility']['reduced_motion_off_initially']=reduced.evaluate("document.documentElement.dataset.motion==='off'")
    report['accessibility']['reduced_motion_content_visible']=reduced.locator('.fx-glitch-base').is_visible()
    reduced.locator('#replay').click()
    reduced.wait_for_timeout(220)
    report['accessibility']['reduced_opt_in_works']=reduced.evaluate("document.documentElement.dataset.motion==='on'")
    reduced.locator('#motion-toggle').click()
    report['accessibility']['reduced_opt_out_works']=reduced.evaluate("document.documentElement.dataset.motion==='off'")
    reduced.close()
    nojs=browser.new_page(viewport={'width':390,'height':844},java_script_enabled=False)
    nojs.set_content(html,wait_until='domcontentloaded')
    report['accessibility']['no_js_menu']=nojs.locator('.mobile-nav-cv').is_visible()
    report['accessibility']['no_js_glitch_base']=nojs.locator('.fx-glitch-base').is_visible()
    nojs.close()
    browser.close()
(root/'QA_SIGNAL_V7_10.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
failed=[row for row in report['widths'] if row['overflow'] or row['clippedHeadings'] or row['errors'] or row['brokenAnchors'] or row['glitchClones']!=2]
assert not failed,('responsive',failed)
assert all(report['interactions'].values()),('interactions',report['interactions'])
assert all(report['accessibility'].values()),('accessibility',report['accessibility'])
print(json.dumps({'widths':len(report['widths']),'interactions':report['interactions'],'accessibility':report['accessibility'],'status':'PASS'},ensure_ascii=False,indent=2))
