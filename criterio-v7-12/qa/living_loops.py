#!/usr/bin/env python3
"""Real Chromium repeated animation regression for V7.11."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, shutil
r=Path(__file__).resolve().parents[1]
s=(r/'index.html').read_text()
s=re.sub(r'<link[^>]+fonts.googleapis.com[^>]*>','',s)
s=re.sub(r'<link[^>]+fonts.gstatic.com[^>]*>','',s)
s=s.replace('<link rel="stylesheet" href="./styles.css">','<style>'+(r/'styles.css').read_text()+'</style>')
s=s.replace('<script src="./app.js" defer></script>','').replace('</body>','<script>'+(r/'app.js').read_text()+'</script></body>')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox'])
 for width in (390,1440):
  p=b.new_page(viewport={'width':width,'height':900},reduced_motion='no-preference')
  errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
  p.set_content(s,wait_until='domcontentloaded')
  assert p.evaluate("document.documentElement.dataset.motion==='on'")
  e=p.locator('.metric').first
  e.evaluate("x=>x.scrollIntoView({behavior:'instant',block:'center'})")
  p.wait_for_timeout(850)
  a=int(e.get_attribute('data-fx-cycles') or 0)
  assert a>=1,'first scene activation missing'
  assert e.evaluate("x=>x.classList.contains('fx-ambient-visible')")
  p.wait_for_timeout(7700)
  z=int(e.get_attribute('data-fx-cycles') or 0)
  assert z>a,'scene did not repeat'
  p.evaluate("document.getElementById('motion-toggle').click()")
  assert p.evaluate("document.documentElement.dataset.motion==='off'")
  assert e.evaluate("x=>getComputedStyle(x,'::after').animationName==='none'")
  last=int(e.get_attribute('data-fx-cycles') or 0)
  p.wait_for_timeout(1350)
  assert int(e.get_attribute('data-fx-cycles') or 0)==last
  p.evaluate("document.getElementById('motion-toggle').click()")
  assert p.evaluate("document.documentElement.dataset.motion==='on'")
  assert max(p.evaluate("document.body.scrollWidth"),p.evaluate("document.documentElement.scrollWidth"))<=width
  assert not errs,errs
  print('PASS',width,'cycles',a,z)
  p.close()
 red=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 red.set_content(s,wait_until='domcontentloaded')
 assert red.evaluate("document.documentElement.dataset.motion==='off'")
 red.locator('#motion-toggle').click()
 assert red.evaluate("document.documentElement.dataset.motion==='on'")
 print('PASS reduced-motion opt-in')
 b.close()
