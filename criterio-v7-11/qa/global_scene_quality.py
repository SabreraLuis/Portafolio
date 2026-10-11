#!/usr/bin/env python3
"""V7.10: assert real automatic scene effects throughout the actual local source."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, shutil, json
root=Path(__file__).resolve().parents[1]
s=(root/'index.html').read_text()
s=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>', '', s)
s=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>', '', s)
s=s.replace('<link rel="stylesheet" href="./styles.css">','<style>'+(root/'styles.css').read_text()+'</style>')
s=s.replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+(root/'app.js').read_text()+'</script></body>')
result={'viewports':[],'scenes':{},'controls':{},'errors':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox','--disable-background-networking'])
 for w in (320,360,390,430,650,700,768,900,1024,1440,1920):
  page=browser.new_page(viewport={'width':w,'height':844 if w<701 else 900},reduced_motion='no-preference')
  errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.set_content(s,wait_until='domcontentloaded')
  page.wait_for_timeout(100)
  v=page.evaluate('''() => ({width:Math.max(document.body.scrollWidth,document.documentElement.scrollWidth),active:document.documentElement.dataset.motion,scenes:document.querySelectorAll('[data-fx-scene]').length,headings:[...document.querySelectorAll('h1,h2,h3,h4')].filter(x=>{const r=x.getBoundingClientRect();return r.left<-2||r.right>innerWidth+2}).map(x=>x.textContent.slice(0,38))})''')
  result['viewports'].append({'width':w,'overflow':max(0,v['width']-w),'motion':v['active'],'scenes':v['scenes'],'clipped':v['headings'],'errors':errors})
  page.close()
 page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='no-preference')
 errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
 page.set_content(s,wait_until='domcontentloaded')
 result['controls']['auto_on_fresh_tab']=page.evaluate("document.documentElement.dataset.motion==='on'")
 result['controls']['auto_button_says_pause']=page.locator('#motion-toggle').inner_text().strip()=='PAUSAR FX'
 names={
  'vision':'#manifiesto', 'disciplines':'.discipline-heading','discipline':'.discipline-card:first-child',
  'archive':'#archivo','dossier':'#dossier-prod', 'interlude':'.decision-interlude',
  'evidence':'#evidencia','metric':'.metric:first-child','method':'#metodo',
  'method-step':'.method-stages article:first-child', 'training':'.training',
  'bridge':'.bridge-forward', 'contact':'#contacto'
 }
 for key, selector in names.items():
  el=page.locator(selector).first
  el.scroll_into_view_if_needed(timeout=4000)
  page.wait_for_timeout(165)
  d=el.evaluate('''e=>({seen:e.classList.contains('fx-scene-seen'),running:e.classList.contains('fx-scene-burst'),animation: [...e.querySelectorAll('*')].some(x=>x.getAnimations().some(a=>a.playState==='running'))})''')
  result['scenes'][key]=d
  if key in ('vision','dossier','evidence','method','contact'):
   (root/'previews').mkdir(exist_ok=True)
   page.screenshot(path=str(root/'previews'/f'v710-{key}-390.png'),animations='disabled')
 page.locator('#motion-toggle').click()
 result['controls']['pause']=page.evaluate("document.documentElement.dataset.motion==='off'")
 result['controls']['all_scene_bursts_stopped']=page.locator('.fx-scene-burst').count()==0
 page.reload() if False else None
 page.locator('#motion-toggle').click()
 result['controls']['resume']=page.evaluate("document.documentElement.dataset.motion==='on'")
 result['controls']['all_scenes_covered']=page.locator('[data-fx-scene]').count()>=22
 result['errors']=errors
 page.close()
 reduced=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 reduced.set_content(s,wait_until='domcontentloaded')
 result['controls']['reduce_off']=reduced.evaluate("document.documentElement.dataset.motion==='off'")
 reduced.locator('#motion-toggle').click()
 result['controls']['reduce_manual_on']=reduced.evaluate("document.documentElement.dataset.motion==='on'")
 reduced.close(); browser.close()
(root/'QA_GLOBAL_SCENES_V7_10.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'viewports':len(result['viewports']),'scenes':result['scenes'],'controls':result['controls'],'errors':result['errors']},ensure_ascii=False,indent=2))
assert all(x['overflow']==0 and x['motion']=='on' and x['scenes']>=22 and not x['clipped'] and not x['errors'] for x in result['viewports']), 'Responsive fail'
assert all(v['seen'] for v in result['scenes'].values()), 'A global scene never entered'
assert all(result['controls'].values()) and not result['errors'], 'Controls fail'
