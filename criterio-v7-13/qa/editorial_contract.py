#!/usr/bin/env python3
"""CRITERIO V7.13 — geometry, typographic measures and editorial integrity.
Screenshot-independent regression checks for bugs that horizontal-overflow tests miss.
"""
from pathlib import Path
import json, re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
h=(ROOT/'index.html').read_text(); css=(ROOT/'styles.css').read_text();js=(ROOT/'app.js').read_text()
h=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',h)
h=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">',f'<style>{css}</style>').replace('<script src="./app.js" defer></script>','').replace('</body>',f'<script>{js}</script></body>')
report={'widths':[],'checks':{},'console_errors':[]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-background-networking'])
 for width,wide_fallback in [(w, False) for w in (320,360,375,390,430,600,700,768,900,1024,1280,1440,1920)] + [(w, True) for w in (320,360,375,390,430,600,700,768,900,1024,1280,1440,1920)]:
  page=b.new_page(viewport={'width':width,'height':850 if width<701 else 900},reduced_motion='reduce')
  page.on('pageerror',lambda e:report['console_errors'].append(str(e)))
  page.set_content(h,wait_until='domcontentloaded')
  if wide_fallback: page.add_style_tag(content=':root{--display:Arial,sans-serif!important}')
  result=page.evaluate('''() => {
   let bad=[];
   const sels=['.contact-head','.contact-cta','.contact-base','.contact-address','.brief-head h2','.brief-card strong','.manifesto-content h2','.discipline-card h4','.archive-header h2','.dossier-title h3','.evidence-intro h2','.method-head h2','.method-stages h3','.training h3'];
   for (const selector of sels) for (const el of document.querySelectorAll(selector)) {
    const r=el.getBoundingClientRect(),content=el.scrollWidth,viewport=innerWidth;
    if(r.width>0&&(r.left < -2 || r.right>viewport+2 || content>el.clientWidth+4))
      bad.push({selector,scroll:content,client:el.clientWidth,left:Math.round(r.left),right:Math.round(r.right)});
   }
   return {page_width:document.documentElement.scrollWidth,bad,
    hud:getComputedStyle(document.querySelector('.chapter-hud')).display,
    brief:document.querySelectorAll('.brief-card').length,
    nav:document.querySelectorAll('nav.navigation a[href^="#"]').length};
  }''')
  report['widths'].append({'width':width,'font_case':'wide_sans_fallback' if wide_fallback else 'native_fallback',**result})
  page.close()
 b.close()
report['checks']={
 'no_horizontal_overflow':all(x['page_width']<=x['width'] for x in report['widths']),
 'no_text_box_clipping':all(not x['bad'] for x in report['widths']),
 'no_floating_hud_occlusion':all(x['hud']=='none' for x in report['widths']),
 'all_three_professional_pillars':all(x['brief']==3 for x in report['widths']),
 'five_navigation_chapters':all(x['nav']==5 for x in report['widths']),
 'copy_realistic':all(t.lower() in (ROOT/'index.html').read_text().lower() for t in ('Amazon Magic Park','20 Prod.','SUNAFIL','Studios TKOH')),
 'hero_marketing_not_ux': 'MARKETING · PUBLICIDAD · COMUNICACIÓN' in (ROOT/'index.html').read_text(),
 'no_font_based_clipping':not bool(re.search(r'\.manifesto\s*\{\s*overflow-x\s*:\s*clip\s*\}',css[-4000:])),
 'vfx_pause_preserved':'id="motion-toggle"' in (ROOT/'index.html').read_text(),
 'no_page_errors':not report['console_errors']
}
(ROOT/'QA_EDITORIAL_CONTRACT_V7_13.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['checks'],indent=2,ensure_ascii=False))
if not all(report['checks'].values()):
 print(json.dumps([x for x in report['widths'] if x['bad']],ensure_ascii=False,indent=2));raise SystemExit('V7.13 editorial contract failed')
