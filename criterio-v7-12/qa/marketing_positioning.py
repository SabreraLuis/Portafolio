#!/usr/bin/env python3
"""Contract: market-facing positioning, truthful dossier order and mobile usability."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,json
root=Path(__file__).resolve().parents[1]
h=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
terms=['marketing','publicidad','comunicación','comunicación para el desarrollo','comunicación institucional','ux/ui']
assert all(t in h.lower() for t in terms),[x for x in terms if x not in h.lower()]
caseorder=['amp','prod','sunafil','tkoh'];assert sorted(caseorder)==sorted(re.findall(r'data-case="([a-z]+)"',h))
assert [m.group(1) for m in re.finditer(r'data-case="([a-z]+)"',h)]==caseorder
assert [m.group(1) for m in re.finditer(r'data-case-link="([a-z]+)"',h)]==caseorder
assert '/Portafolio/' in h and 'VER PORTAFOLIO UX/UI' in h
assert all(f'href="#{target}"' in re.search(rf'<article[^>]*class="dossier"[^>]*id="dossier-{case}".*?</article>',h,re.S).group(0) for case,target in [('amp','dossier-prod'),('prod','dossier-sunafil'),('sunafil','dossier-tkoh'),('tkoh','evidencia')])
assert len(re.findall(r'class="discipline-card"',h))==3
for proof in ('+40','+25','−15'):
 assert proof in h
assert 'participación comunitaria ejecutada' not in h.lower()
h=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',h)
h=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
h=h.replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+js+'</script></body>')
checks=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-background-networking'])
 for width in (320,360,390,430,768,1024,1440,1920):
  p=b.new_page(viewport={'width':width,'height':844 if width<700 else 900},reduced_motion='reduce');p.set_default_timeout(6000)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.set_content(h,wait_until='domcontentloaded');p.wait_for_timeout(120)
  data=p.evaluate('''() => ({overflow: Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth, cards:document.querySelectorAll('.discipline-card').length, role: !!document.querySelector('.hero-role'),ux:document.querySelector('.ux-secondary a').href})''')
  assert data['overflow']==0 and data['cards']==3 and data['role'] and not errors,(width,data,errors)
  checks.append({'width':width,'overflow':data['overflow'],'errors':errors})
  if width in (390,1440):
   folder=root/'previews';folder.mkdir(exist_ok=True)
   p.screenshot(path=str(folder/f'hero-{width}.png'))
   p.locator('.discipline-heading').scroll_into_view_if_needed();p.wait_for_timeout(100)
   p.screenshot(path=str(folder/f'pillars-{width}.png'))
   p.locator('#dossier-sunafil').scroll_into_view_if_needed();p.wait_for_timeout(100)
   p.screenshot(path=str(folder/f'public-comms-{width}.png'))
  p.close()
 b.close()
report={'case_order':caseorder,'marketing_pillars':3,'views':checks,'notes':['Chromium fallback fonts, no real public CDN validation','Communication for development is a professional direction, not a claimed completed C4D program.']}
(root/'QA_MARKETING_V7_9.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
