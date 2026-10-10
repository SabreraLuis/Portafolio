# INK / IMPACT — Visual Systems Playbook (V4)
**Status:** working canon for Luis Sabrera's CV website. **Owner:** Luis S. **Date:** 2026-10-09.

## Thesis
Build a professional editorial website where typography is the image, negative space defines hierarchy, and each animation communicates *entry, orientation, transition or feedback*. Reference Bleach: TYBW graphic principles without reproducing protected title cards, character art, logos or exact compositions.

## Research distilled
1. Bleach TYBW production team's published discussion: use broad dark color masses; simplify line detail where it competes with composition. Source: https://bleach-anime.com/special/interview/08.html
2. Scroll-driven animations should be progressive enhancements, not dependencies: MDN notes optional view progress timelines and reduced-motion considerations. Source: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines
3. The View Transition API can help communicate state between distinct views, but does not justify transitions between simple document sections. Source: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
4. GSAP ScrollTrigger provides advanced timelines when truly required. Its pin/scrub features were reviewed but intentionally NOT integrated into this simple CV because they would increase implementation and QA cost. Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/

## Layout grammar
- **12-column mental model** with breakpoints; 68:32 hero, 17:83 about, 32:68 work with sticky index, three-column evidence, asymmetric two-column skills and education, monochrome contact.
- **One hero element per section.** Subordinates use mono labels; body copy stays readable at 14-16px rather than inheriting oversized condensed display type.
- **Hard palette**: warm paper `#eae7e0`, near-black `#111110`, warm white `#f7f5ef`, vermilion `#db4b3c`. No AI-style gradients or scattered colored UI pills.
- **Type**: Barlow Condensed for display, DM Sans for reading, IBM Plex Mono for archival indexes.
- Section cadence: light cover → paper chapter → vermilion punctuation → black work chapters → vermilion evidence → light skills & education → black contact. Different section structures prevent monotony.

## Motion grammar
| Motion | Purpose | Trigger | Safety |
| --- | --- | --- | --- |
| Intro title masked reveal | Establish hierarchy | Initial page load | CSS off on reduced motion |
| Slash/04 cover | Original graphic accent | Initial page load | Decorative only |
| Reveal once | Guide sequential reading | IntersectionObserver | Content present without JS; timeout fail-open |
| Sticky case index 01-04 | Orientation through career | Scroll (rAF) | Pure text fallback if JS absent |
| Reading rail | Orientation | Scroll | Passive listener; lightweight |
| Typographic interlude | Express chapter shift | CSS view timeline when supported | static fallback |
| Poster pointer shift (±4 px) | Desktop microfeedback | Fine-pointer hover | No layout reflow; disabled by preference |
| Motion toggle | User control | Click | Session-only state; respects OS |
| Contact/print | Practical action | Click | Native links and print CSS |

## Interaction and FX constraints
- Animations should only use compositor-friendly `transform` and `opacity` where possible.
- No persistent spinner, custom cursor, uncontrolled video, image overload, scroll hijacking, scroll-smoothing dependency, or false performance claims.
- No client-side analytics, trackers or network APIs apart from optional Google Fonts.
- Preserve browser back, anchor navigation, `Escape`, keyboard focus and page reading order.
- No fabricated projects, case studies or metrics: every career claim remains anchored to the supplied CV.

## Acceptance criteria before replacing V3
1. Test 320/390/768/1440/1920 px in a real browser (not only static inspection).
2. Inspect hero, chapter transitions, all four career cases, interactive controls and print preview.
3. Test `prefers-reduced-motion`, reduced motion toggle, keyboard, zoom at 200%, menu, copied email, and error console.
4. Check no clipped *essential* typography at narrow widths and no horizontal body overflow.
5. Measure Lighthouse performance, accessibility and Web Vitals under repeatable serving conditions.
6. Obtain user sign-off after side-by-side V3 / V4 comparison.

## Delivery
Keep `cv-ink-impact/` (V3) unchanged while testing `cv-ink-impact-v4/` (V4) as a separate GitHub Pages URL. Promotion is a deliberate later decision; a successful GitHub Pages build alone is not visual QA.
