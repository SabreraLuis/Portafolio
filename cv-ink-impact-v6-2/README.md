# INK / IMPACT VI.2 — Responsive Stable Candidate

Independent, source-grounded version of Luis Alberto Sabrera Espinoza's CV, refining the VI.1 direction without replacing the main portfolio or previous editions.

## Updates

- Smaller mobile artwork and less empty vertical spacing, with first-screen legibility preserved.
- PDF download above the fold and from the primary navigation, as well as at the contact section.
- Collapsible utility menu (reading mode, motion control), no full-width persistent bar obstructing content.
- Accessible Escape/outside-click closure, keyboard operability, native reduced-motion respect, responsive menu for short viewports.
- Clear focus states and high-contrast treatment, no scroll hijacking and no scroll-pinned scenes.
- Professionally grounded CV content, metrics, tools and chronology retained.

## Hosting

https://sabreraluis.github.io/Portafolio/cv-ink-impact-v6-2/

## Files

- `index.html`, `styles.css`, `app.js` — standalone static website.
- `cv-luis-sabrera.pdf` — original PDF resume supplied by the user.
- `DESIGN_SYSTEM.md`, `QA_RESULTS.json` — implementation and QA report.

Run locally via `python -m http.server 8000` inside this directory. On the test runner, headless Chromium browser networking was blocked; tests used equivalent inline HTML+CSS+JS with the same source content and fonts unavailable. Live browser font/render tests remain separate from this local QA.

Contacts are public because this is a public GitHub Pages CV website.
