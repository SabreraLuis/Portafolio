#!/usr/bin/env python3
"""V7.5 release gates: keyboard, real motion state, pageshow, print, responsive & source integrity.
Uses inlined local assets because external networking is not available in this QA runtime.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,re,shutil
root=Path(__file__).resolve().parents[1]
h=(root/'index.html').read_text(encoding='utf-8')
c=(root/'styles.css').read_text(encoding='utf-8')
j=(root/'app.js').read_text(encoding='utf-8')
h=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',h)
h=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">','<style>'+c+'</style>').replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+j+'</script></body>')
report={'responsive':[],'interaction':{},'limits':['Chromium local with fallback fonts, not actual GitHub Pages CDN','Safari/iOS and physical Android device still require manual validation','Synthetic behavior gates are not field Core Web Vitals']}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox','--disable-background-networking'])
 for width in [320,375,390,430,768,1024,1440,1920]:
  page=b.new_page(viewport={'width':width,'height':844 if width<650 else 900},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(h,wait_until='domcontentloaded')
  result=page.evaluate('''() => ({
   overflow:Math.max(0,document.body.scrollWidth-innerWidth,document.documentElement.scrollWidth-innerWidth),
   h1:document.querySelectorAll('h1').length,
   pdfLocal:[...document.querySelectorAll('a[href$=".pdf"]')].every(a=>a.getAttribute('href')==='./cv-luis-sabrera.pdf'),
   contentVisible:[...document.querySelectorAll('h1,h2,h3')].every(e=>getComputedStyle(e).visibility!=='hidden'),
   chapterIndex:!!document.querySelector('#chapter-count'),
   skipLink:!!document.querySelector('.skip[href="#contenido"]'),
   motionOff:document.documentElement.dataset.motion==='off'
  })''')
  report['responsive'].append({'width':width,**result,'errors':errors})
  page.close()
 page=b.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(h,wait_until='domcontentloaded')
 page.locator('#menu-btn').click()
 report['interaction']['mobile_open']=page.locator('#menu-btn').get_attribute('aria-expanded')=='true'
 page.keyboard.press('Escape')
 report['interaction']['mobile_escape']=page.locator('#menu-btn').get_attribute('aria-expanded')=='false'
 page.locator('#motion-toggle').click()
 report['interaction']['manual_pause']=page.evaluate('document.documentElement.dataset.motion')=='off'
 page.locator('#motion-toggle').click()
 report['interaction']['manual_resume']=page.evaluate('document.documentElement.dataset.motion')=='on'
 page.evaluate("document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('pagehide'))")
 report['interaction']['tab_hidden_pause']=page.locator('html').evaluate("e=>e.classList.contains('visibility-paused')")
 page.evaluate("window.dispatchEvent(new Event('pageshow'))")
 report['interaction']['tab_return_resumes']=page.locator('html').evaluate("e=>!e.classList.contains('visibility-paused')")
 page.emulate_media(media='print')
 report['interaction']['print_hides_fx']=page.locator('#motion-toggle').evaluate("e=>getComputedStyle(e).display==='none'")
 report['interaction']['print_displays_details']=page.locator('.dossier').first.evaluate("e=>getComputedStyle(e).display!=='none'")
 page.emulate_media(media='screen')
 report['interaction']['screen_restored']=page.locator('.dossier').first.evaluate("e=>getComputedStyle(e).display!=='none'")
 report['interaction']['js_no_errors']=not errors
 page.close()
 b.close()
(root/'QA_PRODUCTION_V7_5.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not all(x['overflow']==0 and x['h1']==1 and x['pdfLocal'] and x['contentVisible'] and x['chapterIndex'] and x['skipLink'] and x['motionOff'] and not x['errors'] for x in report['responsive']) or not all(report['interaction'].values()):
 raise SystemExit('Production gate failed')
