# INK / IMPACT VI — Design Direction, Systems & Motion Canon

**Project:** Luis Alberto Sabrera Espinoza — personal editorial CV.  
**Edition:** VI — 2026-10-09.  
**Design objective:** An original, high-end editorial web presence that makes a professional marketing CV both memorable and credible. Inspired by compositional principles observed in *Bleach: Thousand-Year Blood War*, independent fashion editorial design and modern creative web craft. The system does **not** copy characters, posters, trademarks or exact compositions from any third party.

## Evidence and research foundations

- Codrops, *1820 Productions — Minimal Design, Maximal Motion* (2026-02-13): expressive movement can coexist with a small typographic and monochrome system. https://tympanus.net/codrops/2026/02/13/1820-productions-minimal-design-maximal-motion/
- Codrops, *Inside Bisous* (2026-06-29): a stable grid lets cinematic transitions and varied content formats coexist. https://tympanus.net/codrops/2026/06/29/inside-bisous-designing-an-editorial-experience-for-cinematic-cgi/
- Codrops, *House of Yellow* (2026-09-16): motion should be authored as part of brand identity, not added as decorative afterthought. https://tympanus.net/codrops/2026/09/16/house-of-yellow/
- Codrops, *Stefan Vitasović Portfolio* (2025-03-05): offset structures and a few repeatable typographic motion motifs add personality. https://tympanus.net/codrops/2025/03/05/case-study-stefan-vitasovic-portfolio-2025/
- MDN, Scroll-driven Animation Timelines: animations must honor `prefers-reduced-motion` and degrade safely. https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines
- W3C, WCAG 2.2 1.4.3 contrast: 4.5:1 small text, 3:1 large text. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- Official Bleach TYBW material (a formal composition reference, not an asset repository): https://bleach-anime.com/

## Why V6 is structurally different from V5

The weakness of the earlier iterations was repetition of strong headings without accompanying storytelling, and generic decorative movement. V6 instead presents a professional document as a coherent sequence:

1. **Cover / personal identity:** name, profession, contact entry point, original typographic study.
2. **Positioning / profile:** one dramatic statement supported by CV facts.
3. **Four professional case studies:** differentiated graphic panels that correspond to the facts of each job; native `<details>` expand the full duties.
4. **Proof:** three metrics tied explicitly to their named roles, never extrapolated.
5. **Capabilities and education:** structured lists that can be skimmed quickly.
6. **Contact:** clear email, telephone and a print-as-PDF option.

No fake case study imagery or made-up portfolio screenshots. The CRM mockup is openly labeled **conceptual**. Funnel flow is qualitative, not quantitative. No fabricated claims or certifications.

## Visual grammar

| Token | Value | Use |
|---|---|---|
| paper | `#edeae2` | reading and portfolio background |
| light-paper | `#f9f7f1` | education and whitespace |
| ink | `#111113` | typography, full-black scenes |
| scarlet | `#e1464b` | graphic accents, full-size impact panel |
| dark-scarlet | `#c92234` | small semantic text on paper |
| off-white | `#f7f4ed` | text on ink |
| muted | `#67635c` | metadata on paper |

Measured WCAG 2 relative contrast in sRGB: ink/paper **15.69:1**; off-white/ink **17.17:1**; ink/scarlet **4.65:1**; dark-scarlet/paper **4.64:1**; muted/paper **4.97:1**. Off-white/scarlet is **3.69:1** and is therefore **not** used as essential body-sized text. Decorative type in this combination must remain large.

### Typography

- `Barlow Condensed 800/900` for display; fallback `Arial Narrow` / `Impact`.
- `DM Sans` for professional body copy and descriptions.
- `IBM Plex Mono` for orientation, annotation and metadata.
- Maximum two main text emphases per viewport. One obvious focal point. Short paragraphs and unbroken reading routes.

### Composition

- Master grid: two-column cover 64/36; case study text/art 58/42; small viewport becomes a single column.
- Rare full-bleed color interruption. No pointless UI cards or shadow stacks.
- Edge-to-edge chapter bands and thin structural strokes, not ornamental frames.
- Every case art panel has a grounded reason: capture flow; 40% performance; conceptual CRM wireframe; institutional communication KPIs.

### Motion contract

**Motion is a component of rhythm, never a requirement for comprehension.**

- Entrance: headline word mask, staggered by 120ms.
- Page sections: IntersectionObserver reveals that never alter document layout.
- Artwork: initial ring transform and micro-elevation on hover.
- Scroll orientation: progress line and chapter counter, using a single `requestAnimationFrame` per scroll frame.
- No scroll hijacking, full-screen blocking loaders, continuous WebGL, heavy filters or parallax affecting text readability.
- Manual motion control plus OS `prefers-reduced-motion`; the system fails open if IntersectionObserver is unsupported, and has a 13s all-content reveal watchdog.
- Native semantic interactivity. `details` elements remain functional with JS disabled.

### UX provisions

- Clear above-the-fold career description and one task-focused CTA.
- Recruiter mode: **MODO LECTURA**, hiding only visual art and tightening spacing while preserving professional data. State kept only in sessionStorage.
- Keyboard-operable mobile menu with Esc and outside click closing.
- Contact via real `mailto:` and `tel:`; print button uses browser printing, with an A4 CSS stylesheet.
- Semantically structured headings, nav, sections and job cases. No private or premium APIs required.

## QA gate and known limits

Local automated Chromium QA using offline fonts fallback, at 320/375/390/430/768/1024/1440/1920px: zero viewport horizontal overflow, zero JavaScript page errors, all 4 experiences present, all anchors grounded, 4 functional disclosure panels, H1 unique, reduced motion visible, mobile menu opens/closes on Esc, and manual reading/motion controls function. See `QA_RESULTS.json`.

Important limitations: browser QA is local and uses local system font fallbacks because this runtime cannot reach Google Fonts. It is *not* a verified render of the public GitHub Pages origin. Lighthouse and actual Core Web Vitals remain **unmeasured**; don't claim a production LCP/INP/CLS pass without production data. Nor have real-user usability tests been conducted.

### Acceptance for next iteration

- No unexpected horizontal scroll at 320, 375, 390, 430, 768, 1024, 1440, 1920px.
- No empty/unreadable information in motion-off or reduced-motion modes.
- Every metric sourced to a single employer, and all CV dates exact.
- Remote typography and line breaks visually checked before choosing V6 as replacement for earlier versions.
- A11y audit (axe), Lighthouse and at least one mobile-device review when a live browser is available.

## Preservation contract

- This new edition lives under `cv-ink-impact-v6/` and **does not replace** the existing website root or the V1–V5 experiments.
- No new photo assets or remote marketing imagery have been included. If the user supplies a real portrait, adapt it with their explicit approval.
