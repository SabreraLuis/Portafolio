# CRITERIO / INK IMPACT V7.2 — Editorial Refinement

[Live candidate](https://sabreraluis.github.io/Portafolio/criterio-v7-2/) · [Previous baseline V7.1](https://sabreraluis.github.io/Portafolio/criterio-v7/)

## Objective

Art-direct the existing professional CV without sacrificing the V7.1 functionality, accessibility and content integrity. This is a self-contained **candidate** published separately from the approved V7.1 and the root portfolio.

## V7.2 changes

- Added an **index of four professional dossiers**, keyboard-accessible with native anchor navigation, placed where a reader needs it.
- Added a strong editorial **decision interlude** between career and evidence, with an original typography-based composition, cutting red stroke and time-controlled motion; not copied from Bleach IP.
- Added a subtle desktop-only **live chapter HUD**, synced to the existing single JS motion director.
- Added independent art-directed transformations, red rules and transitions for experience panels; no new JavaScript dependencies and no second competing motion director.
- Reduced empty first-screen space on mobile, enhanced touch links and refined monochrome/carmine/cyan accents without introducing unlicensed imagery.
- Reused the **original CV PDF** at `../criterio-v7/cv-luis-sabrera.pdf` to avoid duplicating an existing binary; available from hero/nav/contact. The previous version must remain hosted.

## Implementation

Vanilla semantic HTML5, a single CSS bundle, one JS controller, no backend, no build step, no third-party JS libraries. External Google Fonts are optional thanks to fallbacks. Root portfolio and previous editions remain unchanged.

## Local QA

- `python qa/static_checks.py` checks IDs, links, accessible inputs, asset paths, PDF reference, no-script menu and single JS controller.
- `python qa/browser_smoke.py` tests 12 viewports, browser errors, scroll reveals, keyboard menu, PDF links, motion replay/toggle, reduced-motion opt in/out, interlude animation t0/t1, dossier jump and no-JS navigation in Chromium.
- `QA_V7_2.json` captures execution evidence. Tests run with **CSS/JS inlined** and fallback fonts because the test browser's network is restricted; therefore they do not establish live production load success or Safari / Android behavior.
- `hero-390.png`, `hero-1440.png`, `interlude-390.png`, `interlude-1440.png` are local previews, not production evidence. They are retained in this working session, not published to GitHub to avoid unnecessary binary assets.

## Explicit pending release verification

- Real HTTP requests for deployed CSS, JS, and PDF with correct 200 responses.
- Mobile Android Chrome / iOS Safari and actual Google Font rendering.
- Lighthouse / field Core Web Vitals baseline + candidate under comparable conditions.
- Independent manual screen reader walkthrough.

## Data ethics

CV facts and all reported metrics are unchanged from the user's supplied CV: +40% belongs to 20 Prod.; +25% and -15% belong to SUNAFIL. No invented professional portraits, employers, social profiles or verified external case studies.

## Rollback

Original site at `/criterio-v7/` remains intact; point the user back to that URL if V7.2 needs reversal. No production rewrites or redirects have been made.
