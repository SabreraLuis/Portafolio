#!/usr/bin/env python3
"""V7.8 static byte budgets; no network-dependent marketing claims."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
files={'html':root/'index.html','css':root/'styles.css','javascript':root/'app.js','pdf':root/'cv-luis-sabrera.pdf','favicon':root/'favicon.svg','grain':root/'grain.png'}
limits={'html':36000,'css':100000,'javascript':25000,'pdf':100000,'favicon':12000,'grain':16000}
sizes={k:v.stat().st_size for k,v in files.items()}
html=files['html'].read_text(encoding='utf-8'); js=files['javascript'].read_text(encoding='utf-8')
flags={
 'budget':all(sizes[k]<=limits[k] for k in files),
 'no_remote_scripts':not re.search(r'<script[^>]+src="https?://',html),
 'no_unsafe_eval':not re.search(r'\beval\s*\(|new\s+Function\s*\(',js),
 'pdf_magic':files['pdf'].read_bytes().startswith(b'%PDF-'),
 'canonical_v712':'/criterio-v7-12/' in html and '/criterio-v7-8/' not in html,
 'pdf_self_contained':'../criterio-v7/' not in html and 'href="./cv-luis-sabrera.pdf"' in html,
 'privacy_no_analytics':not any(term in html.lower() for term in ['googletagmanager.com/gtm.js','google-analytics.com','facebook.net/en_us/fbevents.js'])
}
report={'files':sizes,'limits':limits,'checks':flags,'total_asset_bytes':sum(sizes.values()),'note':'Only first-party static bytes; fonts from Google Fonts are not included. This is not Lighthouse or field performance data.'}
(root/'QA_RESOURCE_BUDGET.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not all(flags.values()):raise SystemExit('Resource/contract budget failed')
