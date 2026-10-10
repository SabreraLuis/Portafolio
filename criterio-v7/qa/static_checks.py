#!/usr/bin/env python3
"""CRITERIO CV: dependency-free structural QA. Run python criterio-v7/qa/static_checks.py."""
from pathlib import Path
from html.parser import HTMLParser
import re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.local=[];self.anchors=[];self.h1=[];self.buttons=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1.append(a)
        if tag=='button':self.buttons.append(a)
        for key in ('href','src'):
            v=a.get(key,'')
            if v.startswith('#'):self.anchors.append(v[1:])
            elif v.startswith('./'):self.local.append(v[2:].split('?')[0])
scan=Scan();scan.feed(html)
checks={
    'one_h1':len(scan.h1)==1,
    'unique_ids':len(scan.ids)==len(set(scan.ids)),
    'anchors_resolve':all(i in scan.ids for i in scan.anchors),
    'local_assets_exist':all((root/x).is_file() for x in scan.local),
    'pdf_exists':(root/'cv-luis-sabrera.pdf').is_file(),
    'mobile_pdf_navigation':'mobile-nav-cv' in html,
    'motion_pause_control':'id="motion-toggle"' in html and 'motionToggle.addEventListener' in js,
    'no_eval_or_innerHTML':not bool(re.search(r'\beval\s*\(|\.innerHTML\b',js)),
    'reduced_motion_support':'prefers-reduced-motion:reduce' in css,
    'focus_visible':'focus-visible' in css,
    'no_js_navigation_fallback':'html:not(.has-js) .navigation' in css,
    'no_external_js_dependencies':not bool(re.search(r'<script[^>]+src="https?://',html)),
    'buttons_have_type':all(x.get('type')=='button' for x in scan.buttons),
}
for label,ok in checks.items():print(('PASS' if ok else 'FAIL'),label)
if not all(checks.values()):raise SystemExit('Static QA failed')
