# CRITERIO V7.13 — Editorial Quality

Versión reversible sobre V7.12. Enfatiza la legibilidad de marketing, publicidad y comunicación institucional sin abandonar el diseño cinematográfico y los VFX existentes.

## Correcciones
- Título HABLEMOS sin recorte tipográfico de escritorio y CTA ESCRÍBEME válido a 320 px.
- HUD redundante retirado para que no cubra tarjetas ni texto de lectura rápida.
- Escala editorial explícita, medida de párrafos, mejor ritmo de lectura y mínimos de ancho de retícula.
- Textos de portada, resumen, perfil, carrera y evidencia más concretos, sin alterar las métricas documentadas.
- Eliminadas reglas de `overflow:clip` como solución superficial de titulares estrechos.

## Evidencia
`EDITORIAL_SYSTEM_V7_13.md`, `QA_EDITORIAL_CONTRACT_V7_13.json` y `qa/editorial_contract.py`. Chromium local y fallback fonts; no implica validación física iOS/Android ni Core Web Vitals de campo.

## Rollback
Versión anterior intacta: `https://sabreraluis.github.io/Portafolio/criterio-v7-12/`.
