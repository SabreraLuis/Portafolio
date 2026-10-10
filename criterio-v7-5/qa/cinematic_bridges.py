#!/usr/bin/env python3
"""V7.4 focused QA: cinematic bridges, next dossier links, reduced motion, mobile graphics."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os, re, shutil
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
css=(root/'styles.css').read_text()
js=(root/'app.js').read_text()
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>','')
html=html.replace('</body>','<script>'+js+'</script></body>')
exe=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser')
result={'bridges':{},'next_links':{},'reduced_motion':{},'console_errors':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-background-networking'],**({'executable_path':exe} if exe else {}))
 for width in (320,390,768,1440,1920):
  p=b.new_page(viewport={'width':width,'height':844 if width<700 else 900},reduced_motion='no-preference')
  errors=[];p.on('pageerror', lambda e:errors.append(str(e)))
  p.set_default_timeout(8000)
  p.set_content(html,wait_until='domcontentloaded')
  checks=[]
  for idx in range(2):
   item=p.locator('.scene-bridge').nth(idx)
   item.scroll_into_view_if_needed();p.wait_for_timeout(120)
   # The animated cut must visibly travel after entering the viewport
   start=item.locator('.bridge-slash').evaluate('e=>getComputedStyle(e).transform')
   p.wait_for_timeout(300)
   end=item.locator('.bridge-slash').evaluate('e=>getComputedStyle(e).transform')
   rect=item.bounding_box()
   sizes=p.evaluate('({body:document.body.scrollWidth,doc:document.documentElement.scrollWidth,view:innerWidth})')
   checks.append({'inViewport':rect['width']<=width+1,'visible':item.is_visible(),'activated':item.evaluate('e=>e.classList.contains("is-cut-in")'),'motionMeasured':start!=end,'overflow':max(0,sizes['body']-width,sizes['doc']-width)})
   if os.environ.get('CAPTURE_QA_SCREENSHOTS') == '1' and width in (390,1440): item.screenshot(path=str(root/f'bridge-{idx+1}-{width}.png'),animations='disabled',timeout=8000)
  result['bridges'][str(width)]=checks
  if width==390:
   checks=[]
   for current,expected in [('amp','#dossier-prod'),('prod','#dossier-tkoh'),('tkoh','#dossier-sunafil'),('sunafil','#evidencia')]:
    a=p.locator(f'#dossier-{current} .case-next')
    a.scroll_into_view_if_needed()
    box=a.bounding_box()
    checks.append({'source':current,'target':a.get_attribute('href'),'expected':expected,'touchHeight':round(box['height'],1),'tabbable':a.evaluate('e=>e.tabIndex>=0')})
   result['next_links']['390']=checks
  result['console_errors']+=errors
  p.close()
 p=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 p.set_content(html,wait_until='domcontentloaded')
 a=p.locator('.scene-bridge').first;a.scroll_into_view_if_needed();p.wait_for_timeout(100)
 result['reduced_motion']['default_off']=p.evaluate('document.documentElement.dataset.motion')=='off'
 result['reduced_motion']['no_animation']=a.locator('.bridge-slash').evaluate('e=>getComputedStyle(e).animationName')=='none'
 result['reduced_motion']['text_visible']=a.locator('.bridge-body p').is_visible()
 p.locator('#motion-toggle').click()
 a.scroll_into_view_if_needed();p.wait_for_timeout(100)
 result['reduced_motion']['explicit_optin']=p.evaluate('document.documentElement.dataset.motion')=='on'
 result['reduced_motion']['activated']=a.evaluate('e=>e.classList.contains("is-cut-in")')
 result['reduced_motion']['optin_animation']=a.locator('.bridge-slash').evaluate('e=>getComputedStyle(e).animationName')=='bridge-cut-slide'
 p.close();b.close()
print(json.dumps(result,indent=2,ensure_ascii=False))
assert not result['console_errors'],result['console_errors']
assert all(all(all(v for k,v in t.items() if k in ('inViewport','visible','activated','motionMeasured')) and t['overflow']==0 for t in row) for row in result['bridges'].values()),'bridge failure'
assert all(x['target']==x['expected'] and x['touchHeight']>=44 and x['tabbable'] for x in result['next_links']['390'])
assert all(result['reduced_motion'].values())
