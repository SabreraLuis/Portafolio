#!/usr/bin/env python3
"""Dependency-free sanity checks for static CRITERIO CV. Run: python qa/static_checks.py"""
from pathlib import Path
from html.parser import HTMLParser
import re
root = Path(__file__).resolve().parents[1]
html = (root/'index.html').read_text(encoding='utf-8')
css = (root/'styles.css').read_text(encoding='utf-8')
js = (root/'app.js').read_text(encoding='utf-8')

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[];self.local=[];self.anchors=[];self.h1=[];self.buttons=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1.append(a)
        if tag=='button': self.buttons.append(a)
        for attr in ('href','src'):
            val=a.get(attr, '')
            if val.startswith('#'): self.anchors.append(val[1:])
            elif val.startswith('./'): self.local.append(val[2:].split('?')[0])

d=Scan();d.feed(html)
checks={
    'one_h1':len(d.h1)==1,
    'unique_ids':len(d.ids)==len(set(d.ids)),
    'anchors_resolve':all(a in d.ids for a in d.anchors),
    'assets_exist':all((root/p).is_file() for p in d.local),
    'pdf_exists':(root/'cv-luis-sabrera.pdf').is_file() and (root/'cv-luis-sabrera.pdf').read_bytes().startswith(b'%PDF-'),
    'mobile_pdf_navigation':'mobile-nav-cv' in html,
    'index_of_experiences':'dossier-jump' in html,
    'original_interlude':'decision-interlude' in html,
    'chapter_hud':'chapter-count' in html,
    'motion_pause_control':'id="motion-toggle"' in html and 'motionToggle.addEventListener' in js,
    'no_eval_or_innerHTML':not re.search(r'\beval\s*\(|\.innerHTML\b',js),
    'reduced_motion_support':'prefers-reduced-motion:reduce' in css,
    'focus_visible':'focus-visible' in css,
    'no_js_navigation_fallback':'html:not(.has-js) .navigation' in css,
    'no_external_js_dependencies':not bool(re.search(r'<script[^>]+src="https?://',html)),
    'no_dead_control':all(b.get('type')=='button' for b in d.buttons),
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
if not all(checks.values()):raise SystemExit(1)
