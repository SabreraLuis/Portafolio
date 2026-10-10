#!/usr/bin/env python3
"""V7.3: empirically verify dossier active state, motion, links and mobile accessibility."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,os
root=Path(__file__).resolve().parents[1]
s=(root/'index.html').read_text();s=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',s);s=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',s)
s=s.replace('<link rel="stylesheet" href="./styles.css">','<style>'+(root/'styles.css').read_text()+'</style>')
s=s.replace('<script src="./app.js" defer></script>','')
s=s.replace('</body>','<script>'+(root/'app.js').read_text()+'</script></body>')
report={'cases':{},'checks':{},'errors':[],'notes':['Chromium with inline JS and CSS, fallback fonts; not mobile physical nor public HTTP test']}
with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-background-networking'])
  for width in [390,768,1440]:
    p=browser.new_page(viewport={'width':width,'height':850 if width<700 else 900},reduced_motion='no-preference')
    err=[];p.on('pageerror',lambda e:err.append(str(e)))
    p.set_content(s,wait_until='domcontentloaded');p.wait_for_timeout(350)
    # Each dossier should become active, have its own visible label and context jump.
    results={}
    for id in ['amp','prod','tkoh','sunafil']:
      item=p.locator('#dossier-'+id)
      p.evaluate('(id) => document.getElementById(id).scrollIntoView({block:"center",behavior:"instant"})', 'dossier-'+id);p.wait_for_timeout(450)
      nav=p.locator(f'[data-case-link="{id}"]')
      active=nav.get_attribute('aria-current')=='location'
      inFocus=item.evaluate('(e)=>e.classList.contains("in-focus")')
      jump=item.locator('.dossier-actions a').get_attribute('href')
      graphic=item.locator('.case-graphic-header').is_visible()
      visualRatio=item.evaluate('(e)=>e.querySelector(".dossier-visual").getBoundingClientRect().width/e.getBoundingClientRect().width')
      first=item.locator('.case-graphic-cut').evaluate('(e)=>getComputedStyle(e).transform')
      p.wait_for_timeout(410)
      second=item.locator('.case-graphic-cut').evaluate('(e)=>getComputedStyle(e).transform')
      vals=p.evaluate('''()=>({w:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),width:innerWidth})''')
      results[id]={'activeLink':active,'inFocus':inFocus,'jump':jump,'graphicVisible':graphic,'visualWidthRatio':round(visualRatio,3),'graphicMoving':first!=second,'overflow':max(0,vals['w']-vals['width'])}
    report['cases'][str(width)]=results
    if width==390:
      p.locator('#motion-toggle').click()
      p.locator('#dossier-prod').scroll_into_view_if_needed();p.wait_for_timeout(250)
      off=p.locator('#dossier-prod .case-graphic-cut').evaluate('(e)=>getComputedStyle(e).animationName')
      report['checks']['paused_motion']=off=='none'
      p.locator('#motion-toggle').click()
      p.locator('.dossier-jump [data-case-link="tkoh"]').click()
      report['checks']['index_navigation']=p.evaluate('location.hash === "#dossier-tkoh"')
      report['checks']['case_actions_factual']=all(p.locator(f'#dossier-{id} .dossier-actions a').get_attribute('href') in ('#metodo','#evidencia') for id in ['amp','prod','tkoh','sunafil'])
      report['checks']['minimum_touch_target']=all(p.locator(f'#dossier-{id} .dossier-actions a').evaluate('(e)=>e.getBoundingClientRect().height>=40') for id in ['amp','prod','tkoh','sunafil'])
    report['errors'].extend(err);p.close()
  browser.close()
(root/'QA_DOSSIERS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
if report['errors'] or not all(report['checks'].values()) or not all(all(v['activeLink'] and v['inFocus'] and v['graphicVisible'] and v['visualWidthRatio'] >= (.95 if width=='390' else .2) and v['graphicMoving'] and v['overflow']==0 for v in d.values()) for d in report['cases'].values()):
  raise SystemExit('Dossier QA FAILED')
