# CRITERIO V7.9 — SIGNAL CUT

**Luis Alberto Sabrera Espinoza · Marketing, publicidad y comunicación estratégica**

## Dirección

V7.9 reescribe el texto del CV web para presentarlo como una trayectoria profesional de marketing B2B/B2C, publicidad, construcción de marca y comunicación institucional. La comunicación para el desarrollo permanece señalada como área de interés y aprendizaje, no como campaña implementada. UX/UI queda como una capacidad secundaria vinculada al otro portafolio.

La dirección VFX cambia del movimiento decorativo continuo a **señales breves, intencionales y visibles**:

- Signal Cut: dos duplicados decorativos de una palabra, con `aria-hidden`, recorte parcial y desplazamiento carmín/cian en un burst de 820 ms. El texto auténtico permanece siempre visible.
- Razor Pass: una sola línea que cruza las composiciones principales en 920 ms al entrar en pantalla o mediante replay.
- Evidence Hit: movimiento puntual para valores ya documentados, sin animar cifras hacia números inventados.
- Retiradas las oscilaciones y barridos continuos anticuados que superponían el contenido.

Sin dependencias JavaScript externas, sin scroll hijacking, sin fotografías ficticias ni cambios a las métricas CV. Un solo coordinador de movimiento en `app.js`. El botón `PAUSAR FX` cancela los efectos; `ACTIVAR SIGNAL CUT` ofrece replay explícito. Se respeta `prefers-reduced-motion` por defecto y solo se reactiva tras una interacción voluntaria. Los flashes de pantalla no se utilizan.

## Publicación

- Preview independiente: https://sabreraluis.github.io/Portafolio/criterio-v7-9/
- La V7.8, V7.7 y el portafolio UX raíz siguen intactos.
- Assets binarios preservados por su SHA exacto desde V7.8: PDF original, favicon, grain.

## Pruebas

`python qa/static_checks.py && python qa/resource_budget.py && python qa/marketing_positioning.py && python qa/signal_cut.py`

Además se ejecutaron localmente browser_smoke, navigation_quality, production_gate, cinematic_bridges y dossier_motion (ajustadas a los efectos de una sola ejecución). QA local usa Chromium con CSS y JS inlinados porque el entorno de prueba bloquea servidores locales y Google Fonts. Esto no valida Safari iOS ni Core Web Vitals reales. `QA_SIGNAL_V7_9.json` documenta 13 anchuras, errores, interacciones, reduced motion y fallback sin JavaScript. Verificar publicación HTTP por separado cuando el entorno lo permita.

## Referencias técnicas

- Google Chrome Motion: https://github.com/GoogleChrome/modern-web-guidance-src/blob/main/guides/ui-behaviors/motion/guide.md
- Glitch clip-path con duplicados decorativos: https://animationpatterns.art/animations/glitch-text-clip-path-slice-bands/

Diseño y copy son adaptaciones propias de CRITERIO; no se han copiado layouts ni assets protegidos.
