# Luis Sabrera — INK / IMPACT VI

**A portfolio that behaves like an editorial CV, not a generic AI landing page.**

**Public URL (when GitHub Pages publishes `main`):** https://sabreraluis.github.io/Portafolio/cv-ink-impact-v6/

Designed from the real CV provided by Luis Alberto Sabrera Espinoza, October 2026. The production content is in Spanish. All names, companies, role descriptions and metrics are traceable to the original CV. The typography and illustrations are original; this is not an official anime theme, or a reproduction of any protected Bleach assets.

## Files

- `index.html`: semantic document, SEO/social tags, experience cases and contacts.
- `styles.css`: visual system, chapter artwork, responsiveness, motion and print rules.
- `app.js`: accessible mobile menu, disclosure-ready interaction, chapter HUD, reading mode, reduced motion preference and print button.
- `DESIGN_SYSTEM.md`: design canon, research and decisions.
- `QA_RESULTS.json`: local Chromium test matrix and limitations.

## Verify locally

```sh
python -m http.server 8080
# visit http://localhost:8080/
node --check app.js
```

This page does not need a bundler, framework, GSAP, analytics or an external JavaScript library. Google Fonts are loaded from a CDN if available, with browser/system fallbacks.

## User modes

- **VISTA EDITORIAL**: full original typography and bespoke artwork.
- **MODO LECTURA**: compact recruiter-friendly layout, all CV information retained.
- **MOVIMIENTO ON/OFF**: motion control; OS `prefers-reduced-motion` always takes precedence.
- **GUARDAR CV EN PDF**: invokes native print dialog; choose Save as PDF. No nonexistent PDF link.

## Privacy and safety

Contact information is published because it was explicitly shared in the user's CV. This is public on GitHub Pages. No cookies, third-party analytics, advertising scripts, email forms, sensitive data submission, or API tokens exist in this codebase.

## Preservation

Lives in a completely separate `cv-ink-impact-v6` directory on the existing `SabreraLuis/Portafolio` repository. Previous editions and main portfolio remain unchanged. To review this candidate, use the URL above. Do not point the main portfolio's entry page to this edition before user acceptance.

## Printed CV QA

The browser's print dialog expands all professional disclosures for printing, then restores their original state afterwards. Local Chromium PDF QA verified a two-page A4 CV with the detailed duties, contact information and all four employers. The PDF uses system-font fallbacks in this offline environment; browser-hosted fonts may differ subtly.
