# INK / IMPACT VI.1 — Refinement Record

## Protected decisions

- Editorial split cover; warm paper `#edeae2`, black `#111113`, carmine `#e1464b`.
- Barlow Condensed / DM Sans / IBM Plex Mono as a hierarchy, not interchangeable display typography.
- Four original typographic/diagrammatic representations of employment history, grounded in the supplied CV.
- No imitation of specific Bleach posters/characters/logo; only principles of contrast, scale, and composition.

## VI.1 priorities

1. **Reading order:** stabilize sticky chapter access and keep focus visible.
2. **Mobile compactness:** remove decorative empty height from opening while preserving hierarchy.
3. **Reader utilities:** controls sized for touch and placed above safe-area; preserve native scrolling.
4. **Motion:** animations only on short, predictable transitions; comply with system reduced-motion settings.
5. **Recruiter workflow:** direct PDF download from original CV, alongside native print.
6. **Reversible release:** separate URL; original V6 untouched.

## Reference guidance

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- web.dev high performance animations: https://web.dev/articles/animations-guide
- MDN reduced motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

## QA gate

Run local Chromium across eight viewport widths, normal and reduced motion, mobile nav + Escape, read mode, section focus, PDF download link, print and uncaught browser errors. Commit QA_RESULTS.json to the candidate directory after test execution.


## VI.2 — Mobile/Desktop Stability Contract

- Composition first. The hero balances title, introduction and artwork; mobile artwork ≤214px (≤199px at 355px).
- Recruiter-first entry: direct original-PDF download from hero and navigation; no gated download.
- Utility actions are progressive enhancement: an unobtrusive VIEW toggle opens a controlled panel for reading and motion.
- No locked scroll, no intrusive persistent menu, no full-width floating bar.
- Keyboard: Escape closes the open view panel; toggles use `aria-expanded`/`aria-controls`; focus returns to the trigger.
- Layout: viewport test matrix 320, 360, 375, 390, 430, 650, 651, 768, 950, 951, 1024, 1280, 1440, 1920px. No overflow permitted.
- Progressive enhancement and user OS motion preference are preserved. Print and source PDF remain two separate workflows.
- Source fact integrity: never add fictional sales, campaigns, metrics, awards or products. No proprietary Bleach IP or direct composition copies.
