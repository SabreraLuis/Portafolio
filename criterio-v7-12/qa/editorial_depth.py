#!/usr/bin/env python3
"""Editorial depth: Chromium local rendering, motion preference and native navigation."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,os
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
css=(root/'styles.css').read_text()
js=(root/'app.js').read_text()
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>').replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+js+'</script></body>')
result={'widths':[],'checks':{},'issues':[]}
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-background-networking'])
    for width in [320,360,390,430,650,768,900,1024,1440,1920]:
        page=browser.new_page(viewport={'width':width,'height':820 if width<700 else 900})
        page.on('pageerror',lambda e:result['issues'].append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        val=page.evaluate("""() => ({width: document.documentElement.scrollWidth,
          cards:document.querySelectorAll('.brief-card').length,
          clipped:[...document.querySelectorAll('.recruiter-brief h2,.brief-card strong')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+2||r.left< -2}).length})""")
        result['widths'].append({'width':width,'overflow':max(0,val['width']-width),'cards':val['cards'],'clipped':val['clipped']})
        page.close()
    for width in [390,1440]:
        p=browser.new_page(viewport={'width':width,'height':850 if width<700 else 900},reduced_motion='no-preference')
        p.set_content(html,wait_until='domcontentloaded')
        result['checks'][f'fx_default_{width}']=p.evaluate("document.documentElement.dataset.motion")=='on'
        p.evaluate('scrollTo({top:0,behavior:"instant"})');p.wait_for_timeout(150)
        el=p.locator('.stage-disc')
        a=el.evaluate('e=>getComputedStyle(e).translate')
        p.evaluate('scrollTo({top:420,behavior:"instant"})');p.wait_for_timeout(450)
        b=el.evaluate('e=>getComputedStyle(e).translate')
        result['checks'][f'layer_moved_{width}']=a!=b
        result['checks'][f'native_scroll_{width}']=p.evaluate('scrollY')>=400
        p.locator('#motion-toggle').click()
        result['checks'][f'paused_{width}']=el.evaluate('e=>getComputedStyle(e).translate') in ('0px 0px','0px','none','0px 0px 0px')
        p.locator('#motion-toggle').click()
        result['checks'][f'reactivated_{width}']=p.evaluate('document.documentElement.dataset.motion')=='on'
        p.close()
    p=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    p.set_content(html,wait_until='domcontentloaded')
    result['checks']['reduced_default_off']=p.evaluate('document.documentElement.dataset.motion')=='off'
    result['checks']['reduced_scroll_instant']=p.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
    p.close();browser.close()
print(json.dumps(result,indent=2,ensure_ascii=False))
if any(row['overflow'] or row['cards']!=3 or row['clipped'] for row in result['widths']) or not all(result['checks'].values()) or result['issues']:
    raise SystemExit('Editorial depth QA failed')
