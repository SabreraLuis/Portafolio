# CRITERIO — INK / IMPACT V7.4 (Cinematic Experience)

**Scope:** isolated, responsive static CV experience. Based on the user-approved V7.3. The main portfolio and V7.3 remain unchanged.

## Art direction

The 'corte carmín' is now a narrative transition with two editorial passages. The first connects the manifesto with the professional archive (**Del contexto a la acción**); the second bridges methodology and contact (**Una forma de hacer**). Transitions retain the same color grammar and identity as the dossier series. They are visually striking without blocking content or scroll, adding a video or creating synthetic metrics.

## What changed

- Two dedicated, original cinematic bridges using typographic hierarchy, ghost numerals and animated diagonal cut; reduced-height mobile variants.
- Four 48–56px contextual **Siguiente** links to advance through every dossier (last leads to evidence), using normal anchors, usable by touch, keyboard and without JavaScript.
- A single observer in the existing JS motion director activates the bridge when visible and respects **PAUSAR FX**, reduced-motion and user opt-in. No additional JS library or second animation controller.
- Brief red chapter-activation stroke to unify transitions between sections; with print and reduced-motion fallbacks.
- Fixes to the mobile diagonal's position to preserve legibility.

## Validation

- `python qa/static_checks.py` — semantic anchors, sources, links and assets.
- `python qa/browser_smoke.py` — 12 viewports 320–1920 px; navigation, PDF access, controls, existing intro and interlude, no-JS, reduced motion.
- `python qa/dossier_motion.py` — case active state, movement, width and links at 390/768/1440 px.
- `python qa/cinematic_bridges.py` — two transitions at 320/390/768/1440/1920 px (temporal computed-transform differences), four mobile next actions, absence of overflow, reduced-motion default and manual explicit opt-in.
- `node --check app.js` — syntax.

See `QA_V7_4.json` for captured results. Local Chromium tests inline CSS/JS to avoid sandbox network restrictions and use font fallbacks. They are **not** Lighthouse measurements, real phone measurements or proof that the live GitHub Pages endpoint was visually examined in Safari. GitHub Actions deploy success is tracked separately.

## Technical and privacy constraints

- Only HTML/CSS/vanilla JavaScript. There is no backend or API, because the CV does not need one.
- All professional facts, dates and metrics remain from the user-provided CV: 20 Prod +40%; SUNAFIL +25% and -15%.
- A real photo of Luis was not supplied, so the work uses original graphic compositions, not generated persons represented as him.
- PDF download links use the preserved original source in `../criterio-v7/cv-luis-sabrera.pdf`. Keep that folder when deploying.
- Pause/reduced-motion modes avoid animation. No scroll hijacking, no intrusive modals, no tracking and no new external JS dependencies.
- Rollback: use https://sabreraluis.github.io/Portafolio/criterio-v7-3/ (unchanged).

## Attribution

The QA and release method is informed by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), recorded in A.P.U. as staging `web-experience-engineering`. All new visual details are original CRITERIO compositions, not franchise artwork.
