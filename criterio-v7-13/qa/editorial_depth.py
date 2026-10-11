#!/usr/bin/env python3
"""V7.12: verify native scroll, decorative-only layered parallax, recruiter scan, and user motion settings."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, os, json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
css=(root/'styles.css').read_text()
js=(root/'app.js').read_text()
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">',f'<style>{css}</style>')
html=html.replace('<script src="./app.js" defer></script>','')
html=html.replace('</body>',f'<script>{js}</script></body>')
result={'widths':[],'checks':{},'issues':[]}
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-background-networking'])
    for width in [320,360,390,430,650,768,900,1024,1440,1920]:
        page=browser.new_page(viewport={'width':width,'height':820 if width<700 else 900})
        page.on('pageerror',lambda e:result['issues'].append(f'{width}: {e}'))
        page.set_content(html, wait_until='domcontentloaded')
        size=page.evaluate('''() => ({w:document.documentElement.scrollWidth, h:document.body.scrollHeight,
            snap:document.querySelectorAll('.brief-card').length,
            clipped:[...document.querySelectorAll('.recruiter-brief h2,.brief-card strong')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+2 || r.left< -2}).length})''')
        result['widths'].append({'width':width,'overflow':max(0,size['w']-width),'brief_cards':size['snap'],'brief_head_clipped':size['clipped']})
        page.close()
    for width in [390,1440]:
        page=browser.new_page(viewport={'width':width,'height':850 if width<700 else 900},reduced_motion='no-preference')
        page.on('pageerror',lambda e:result['issues'].append(f'{width}: {e}'))
        page.set_content(html,wait_until='domcontentloaded')
        result['checks'][f'fx_default_on_{width}']=page.evaluate('document.documentElement.dataset.motion')=='on'
        page.evaluate('document.querySelector(".hero-visual").scrollIntoView({behavior:"instant",block:"center"})')
        page.wait_for_timeout(150)
        element=page.locator('.stage-disc')
        a=element.evaluate('e=>getComputedStyle(e).translate')
        page.evaluate('window.scrollTo({top: 420,behavior:"instant"})')
        page.wait_for_timeout(450)
        b=element.evaluate('e=>getComputedStyle(e).translate')
        result['checks'][f'parallax_changes_{width}']=a!=b
        result['checks'][f'native_scroll_{width}']=page.evaluate('scrollY')>=400
        page.locator('#motion-toggle').click()
        result['checks'][f'pause_resets_depth_{width}']=element.evaluate('e=>getComputedStyle(e).translate') in ['0px 0px','0px','none','0px 0px 0px']
        page.locator('#motion-toggle').click()
        result['checks'][f'reactivate_{width}']=page.evaluate('document.documentElement.dataset.motion')=='on'
        page.close()
    page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    page.set_content(html,wait_until='domcontentloaded')
    result['checks']['reduced_default_off']=page.evaluate('document.documentElement.dataset.motion')=='off'
    result['checks']['reduced_scroll_instant']=page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
    page.close();browser.close()
print(json.dumps(result,indent=2,ensure_ascii=False))
(root/'QA_EDITORIAL_DEPTH_V7_12.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
if any(r['overflow'] or r['brief_cards']!=3 or r['brief_head_clipped'] for r in result['widths']) or not all(result['checks'].values()) or result['issues']:
    raise SystemExit('Editorial depth QA failed')
