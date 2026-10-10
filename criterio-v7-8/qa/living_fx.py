#!/usr/bin/env python3
"""CRITERIO V7.6 LIVING FX acceptance; local file:// browser, direct assets, no external fonts."""
import json, shutil, time, re, base64
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'previews';PREV.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text(encoding='utf-8')
css=(ROOT/'styles.css').read_text(encoding='utf-8')
js=(ROOT/'app.js').read_text(encoding='utf-8')
grain=base64.b64encode((ROOT/'grain.png').read_bytes()).decode('ascii')
css=css.replace("url('./grain.png')", "url('data:image/png;base64,"+grain+"')")
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>', '',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>', '',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>','')
html=html.replace('</body>','<script>'+js+'</script></body>')
report={'sizes':[],'checks':{},'measurements':{},'browser_errors':[],'limitations':['Local Chromium with inlined CSS/JS and raster grain, external Google Fonts blocked','Field INP/LCP/CLS and physical Safari/Android pending']}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox','--disable-background-networking'])
 for w in [320,360,390,430,650,768,1024,1440,1920]:
  page=browser.new_page(viewport={'width':w,'height':844 if w<650 else 900},reduced_motion='reduce',device_scale_factor=1)
  err=[];page.on('pageerror',lambda e:err.append(str(e)))
  page.route('https://fonts.googleapis.com/**',lambda r:r.abort());page.route('https://fonts.gstatic.com/**',lambda r:r.abort())
  page.set_content(html,wait_until='domcontentloaded');page.wait_for_timeout(120)
  d=page.evaluate('''() => ({overflow:Math.max(0,document.body.scrollWidth-innerWidth,document.documentElement.scrollWidth-innerWidth),headings:[...document.querySelectorAll('h1,h2,h3')].filter(e=>{const r=e.getBoundingClientRect();return r.left<-3||r.right>innerWidth+3}).length,fxOff:document.documentElement.dataset.motion==='off',source:document.querySelector("style")?.sheet?.cssRules?.length||0,caseScans:document.querySelectorAll('.fx-case-scan').length,proofRules:document.querySelectorAll('.fx-proof-rule').length,heroScan:!!document.querySelector('.fx-scanline')})''')
  report['sizes'].append({'width':w,**d,'errors':err});page.close()
 for width in [390,1440]:
  page=browser.new_page(viewport={'width':width,'height':844 if width==390 else 900},reduced_motion='no-preference',device_scale_factor=1)
  page.route('https://fonts.googleapis.com/**',lambda r:r.abort());page.route('https://fonts.gstatic.com/**',lambda r:r.abort())
  err=[];page.on('pageerror',lambda e:err.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded')
  page.wait_for_timeout(900)
  page.screenshot(path=str(PREV/f'hero-living-{width}.png'),animations='disabled')
  def state():return page.locator('.fx-scanline').evaluate('e=>({top:getComputedStyle(e).transform,opacity:getComputedStyle(e).opacity,animation:getComputedStyle(e).animationName})')
  a=state();page.wait_for_timeout(500);b=state()
  report['measurements'][str(width)]={'scan_first':a,'scan_second':b,'movement_observable':(a['top']!=b['top'] or a['opacity']!=b['opacity']) and a['animation']!='none'}
  if width==1440:
   r=page.locator('.hero-visual').bounding_box()
   page.mouse.move(r['x']+r['width']*.15,r['y']+r['height']*.15);page.wait_for_timeout(100)
   p1=page.locator('.visual-stage').evaluate("e=>e.style.getPropertyValue('--fx-px')")
   page.mouse.move(r['x']+r['width']*.85,r['y']+r['height']*.85);page.wait_for_timeout(100)
   p2=page.locator('.visual-stage').evaluate("e=>e.style.getPropertyValue('--fx-px')")
   report['checks']['pointer_response']=p1!=p2 and bool(p1) and bool(p2)
  page.locator('#motion-toggle').click()
  page.wait_for_timeout(100)
  paused=page.locator('.fx-scanline').evaluate("e=>getComputedStyle(e).animationName")
  report['checks'][f'pause_{width}']=paused=='none' and page.locator('html').get_attribute('data-motion')=='off'
  page.locator('#motion-toggle').click()
  page.wait_for_timeout(100)
  resumed=page.locator('.fx-scanline').evaluate("e=>getComputedStyle(e).animationName")
  report['checks'][f'resume_{width}']=resumed!='none' and page.locator('html').get_attribute('data-motion')=='on'
  page.locator('#dossier-prod').scroll_into_view_if_needed();page.wait_for_timeout(200)
  sc=page.locator('#dossier-prod .fx-case-scan').evaluate("e=>getComputedStyle(e).animationName")
  report['checks'][f'case_scan_{width}']=sc!='none'
  page.locator('#evidencia').scroll_into_view_if_needed();page.wait_for_timeout(900)
  report['checks'][f'proof_activated_{width}']=page.locator('.metric.fx-proof-on').count()>0
  page.screenshot(path=str(PREV/f'evidence-{width}.png'),animations='disabled')
  report['browser_errors'].extend(err);page.close()
 page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 page.route('https://fonts.googleapis.com/**',lambda r:r.abort());page.route('https://fonts.gstatic.com/**',lambda r:r.abort())
 page.set_content(html,wait_until='domcontentloaded')
 report['checks']['reduced_motion_off']=page.locator('html').get_attribute('data-motion')=='off' and page.locator('.fx-scanline').evaluate("e=>getComputedStyle(e).animationName")=='none'
 page.locator('#motion-toggle').click()
 report['checks']['reduced_explicit_optin']=page.locator('html').get_attribute('data-motion')=='on' and page.locator('.fx-scanline').evaluate("e=>getComputedStyle(e).animationName")!='none'
 page.close()
 browser.close()
report['success']=all(r['overflow']==0 and r['headings']==0 and r['fxOff'] and r['source']>0 and r['caseScans']==4 and r['proofRules']==3 and r['heroScan'] and not r['errors'] for r in report['sizes']) and all(report['checks'].values()) and all(v['movement_observable'] for v in report['measurements'].values()) and not report['browser_errors']
(ROOT/'QA_LIVING_V7_6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,indent=2,ensure_ascii=False))
if not report['success']:raise SystemExit('Living FX QA failed')
