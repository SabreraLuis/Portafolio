#!/usr/bin/env python3
"""V8 QA: responsive, text clipping, navigation, motion, reduced-motion."""
import json, os, re, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
h=(root/'index.html').read_text()
css=(root/'styles.css').read_text()
js=(root/'app.js').read_text()
h=re.sub(r'<link[^>]*fonts.googleapis.com[^>]*>','',h)
h=re.sub(r'<link[^>]*fonts.gstatic.com[^>]*>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
h=h.replace('<script defer src="./app.js"></script>','')
h=h.replace('</body>','<script>'+js+'</script></body>')
res={'widths':[],'interactions':{},'errors':[]}
executable=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox','--disable-background-networking'])
 for w in [320,360,375,390,430,600,768,900,1024,1110,1280,1440,1920]:
  page=browser.new_page(viewport={'width':w,'height':844 if w<700 else 900},reduced_motion='no-preference')
  errors=[];page.on('pageerror',lambda exc:errors.append(str(exc)))
  page.set_content(h,wait_until='domcontentloaded')
  page.wait_for_timeout(950)
  r=page.evaluate('''() => {let ww=innerWidth; let els=[...document.querySelectorAll('h1,h2,h3,.btn,.case-cta,.brand-copy,.contact-phone,.contact-pdf')]; let bad=els.filter(el=>{let r=el.getBoundingClientRect();return r.right>ww+2||r.left < -2|| (el.scrollWidth>el.clientWidth+3 && getComputedStyle(el).overflowX!=='visible')});return {overflow:Math.max(0,document.documentElement.scrollWidth-ww,document.body.scrollWidth-ww),bad:bad.map(el=>({tag:el.tagName,className:el.className,txt:el.textContent.trim().slice(0,35),scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,rect:[Math.round(el.getBoundingClientRect().left),Math.round(el.getBoundingClientRect().right)]})).slice(0,12)};}''')
  if r['overflow']:
   r['suspects']=page.evaluate("""() => [...document.querySelectorAll('body *')].filter(el=>{
     const b=el.getBoundingClientRect(); if(b.right<=innerWidth+.15)return false;
     let p=el.parentElement; while(p&&p!==document.body){let o=getComputedStyle(p).overflowX;if(o==='hidden'||o==='clip')return false;p=p.parentElement}return true;
   }).slice(0,18).map(el=>({tag:el.tagName,cls:String(el.className).slice(0,60),text:el.textContent.trim().slice(0,35),right:Math.round(el.getBoundingClientRect().right*10)/10,scrollWidth:el.scrollWidth,parent:el.parentElement?.className,parentText:el.parentElement?.textContent.trim().slice(0,90)}))""")
  res['widths'].append({'width':w,**r,'jsErrors':errors})
  if w in [390,1440]:
   page.screenshot(path=str(root/'previews'/f'v8-hero-{w}.png'),full_page=False)
   page.locator('#experiencia').scroll_into_view_if_needed();page.wait_for_timeout(920)
   page.screenshot(path=str(root/'previews'/f'v8-work-{w}.png'),full_page=False)
   page.screenshot(path=str(root/'previews'/f'v8-full-{w}.png'),full_page=True)
  page.close()
 mobile=browser.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
 mobile.on('pageerror',lambda exc:res['errors'].append(str(exc)))
 mobile.set_content(h,wait_until='domcontentloaded')
 res['interactions']['motion_default_on']=mobile.evaluate("document.documentElement.dataset.motion==='on'")
 res['interactions']['pdf_local']=(root/'cv-luis-sabrera.pdf').is_file()
 res['interactions']['menu_hidden']=not mobile.locator('#site-nav').is_visible()
 mobile.locator('#menu-toggle').click()
 res['interactions']['menu_opens']=mobile.locator('#site-nav').is_visible()
 res['interactions']['menu_aria']=mobile.locator('#menu-toggle').get_attribute('aria-expanded')=='true'
 mobile.keyboard.press('Escape')
 res['interactions']['menu_escape']=not mobile.locator('#site-nav').is_visible()
 mobile.locator('#motion-toggle').click()
 res['interactions']['motion_pauses']=mobile.evaluate("document.documentElement.dataset.motion==='off'")
 mobile.locator('#motion-toggle').click()
 res['interactions']['motion_reactivates']=mobile.evaluate("document.documentElement.dataset.motion==='on'")
 mobile.locator('#experiencia').scroll_into_view_if_needed();mobile.wait_for_timeout(220)
 res['interactions']['case_visible']=mobile.locator('#caso-amp').is_visible()
 res['interactions']['active_navigation']=mobile.locator('a[href="#experiencia"][data-nav]').get_attribute('aria-current')=='location'
 mobile.close()
 reduce=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 reduce.set_content(h,wait_until='domcontentloaded')
 res['interactions']['reduced_default_off']=reduce.evaluate("document.documentElement.dataset.motion==='off'")
 reduce.locator('#motion-toggle').click()
 res['interactions']['reduced_explicit_optin']=reduce.evaluate("document.documentElement.dataset.motion==='on'")
 reduce.close()
 nojs=browser.new_page(viewport={'width':390,'height':844},java_script_enabled=False)
 nojs.set_content(h,wait_until='domcontentloaded')
 res['interactions']['no_js_content']=nojs.locator('#resultados').is_visible() and nojs.locator('#caso-sunafil').count()==1
 res['interactions']['no_js_mobile_nav']=nojs.locator('a[href="#experiencia"][data-nav]').is_visible()
 nojs.close();browser.close()
print(json.dumps(res,ensure_ascii=False,indent=2))
(root/'QA_REPORT.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
if any(x['overflow']>0 or x['bad'] or x['jsErrors'] for x in res['widths']) or not all(res['interactions'].values()) or res['errors']:
 raise SystemExit('QA FAILURE')