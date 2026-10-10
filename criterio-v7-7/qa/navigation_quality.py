#!/usr/bin/env python3
"""V7.7: persistent navigation, fragment focus, keyboard use and performance-safe controls.
Tests local source in Chromium with inline dependencies; not field telemetry.
"""
from pathlib import Path
import json,re,shutil,os
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
h=(root/'index.html').read_text(encoding='utf-8');c=(root/'styles.css').read_text(encoding='utf-8');j=(root/'app.js').read_text(encoding='utf-8')
h=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',h);h=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">','<style>'+c+'</style>').replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+j+'</script></body>')
report={'viewport_checks':[],'interactions':{},'errors':[],'coverage_note':'local Chromium, inline CSS/JS, fallback fonts, not live Pages or mobile Safari'}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),headless=True,args=['--no-sandbox','--disable-background-networking'])
 for width in [320,360,390,430,768,900,1024,1440,1920]:
  page=b.new_page(viewport={'width':width,'height':844 if width<650 else 900},reduced_motion='reduce')
  page.set_default_timeout(4500); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(h,wait_until='domcontentloaded')
  page.evaluate('document.querySelector("#evidencia").scrollIntoView({behavior:"instant", block:"start"})');page.wait_for_timeout(120)
  data=page.evaluate('''() => ({
   sticky:getComputedStyle(document.querySelector('.masthead')).position==='sticky',
   top:Math.round(document.querySelector('.masthead').getBoundingClientRect().top),
   overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth,document.body.scrollWidth-innerWidth),
   menuChapter:document.querySelector('#menu-chapter').textContent.trim(),
   current:[...document.querySelectorAll('.navigation a[aria-current="location"]')].map(e=>e.getAttribute('href')),
   pdfLocal:[...document.querySelectorAll('a[href$=".pdf"]')].every(x=>x.getAttribute('href')==='./cv-luis-sabrera.pdf')})''')
  report['viewport_checks'].append({'width':width,**data,'errors':errors});page.close()
 page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');page.set_default_timeout(5000)
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.set_content(h,wait_until='domcontentloaded')
 page.locator('#menu-btn').click()
 report['interactions']['menu_opens']=page.locator('#menu-btn').get_attribute('aria-expanded')=='true'
 page.locator('#navigation a[href="#archivo"]').click()
 page.wait_for_timeout(450)
 report['interactions']['menu_closes_after_navigation']=page.locator('#menu-btn').get_attribute('aria-expanded')=='false'
 report['interactions']['navigation_sets_hash']=page.evaluate('location.hash')=='#archivo'
 report['interactions']['destination_receives_focus']=page.evaluate('document.activeElement.id')=='archivo'
 report['interactions']['header_remains_accessible']=page.locator('.masthead').evaluate('e=>{let r=e.getBoundingClientRect();return r.top===0&&r.bottom>0}')
 report['interactions']['active_chapter_updates']=page.locator('#menu-chapter').inner_text().strip()=='02'
 report['interactions']['aria_current_matches']=page.locator('a[href="#archivo"][aria-current="location"]').count()==1
 page.locator('#menu-btn').click();page.keyboard.press('Escape')
 report['interactions']['escape_returns_focus']=page.evaluate('document.activeElement.id')=='menu-btn'
 report['interactions']['escape_closes_menu']=page.locator('#menu-btn').get_attribute('aria-expanded')=='false'
 page.locator('#motion-toggle').click()
 report['interactions']['voluntary_fx_optin']=page.evaluate('document.documentElement.dataset.motion')=='on'
 page.locator('#motion-toggle').click()
 report['interactions']['pause_fx']=page.evaluate('document.documentElement.dataset.motion')=='off'
 page.close()
 # no-JS fallback menu and CV stay navigable
 nojs=b.new_page(viewport={'width':390,'height':844},java_script_enabled=False)
 nojs.set_content(h,wait_until='domcontentloaded')
 report['interactions']['nojs_menu_visible']=nojs.locator('#navigation a[href="#archivo"]').is_visible()
 report['interactions']['nojs_pdf_visible']=nojs.locator('.mobile-nav-cv').is_visible()
 nojs.close();b.close()
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not report['errors']
for row in report['viewport_checks']:
 assert row['sticky'] and abs(row['top'])<=1 and row['overflow']==0 and row['pdfLocal'] and not row['errors'],row
 assert row['menuChapter']=='03' and row['current']==['#evidencia'],row
assert all(report['interactions'].values()),report['interactions']
