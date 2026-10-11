#!/usr/bin/env python3
"""Regression: 320px remains within viewport with uncondensed system font fallbacks."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,os,json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
css=(root/'styles.css').read_text()
js=(root/'app.js').read_text()
html=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
html=html.replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+js+'</script></body>')
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
    for font in ['Arial','DejaVu Sans','Liberation Sans']:
        page=browser.new_page(viewport={'width':320,'height':844},reduced_motion='reduce')
        page.set_content(html,wait_until='domcontentloaded')
        page.add_style_tag(content=':root{--display:"'+font+'"!important}')
        value=page.evaluate('''() => Math.max(document.body.scrollWidth,document.documentElement.scrollWidth)-innerWidth''')
        results.append({'font':font,'overflow':value})
        page.close()
    browser.close()
print(json.dumps(results,ensure_ascii=False))
if any(x['overflow']>0 for x in results):raise SystemExit('font fallback overflow')
