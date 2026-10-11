# CRITERIO V7.13 — Contrato editorial y diagramación

## Objetivo profesional
Presentar a Luis Alberto Sabrera Espinoza como profesional de marketing B2B/B2C, publicidad, marca y comunicación institucional. UX/UI sigue siendo una especialidad complementaria. No atribuir resultados ni campañas no documentados en el CV.

## Causa raíz identificada
El diseño tenía numerosas reglas acumuladas entre versiones. En Chromium con fuentes de respaldo, la palabra «HABLEMOS.» excedía su caja en 1024, 1280 y 1440 px sin producir overflow horizontal de página. A 320 px, el CTA «ESCRÍBEME» excedía el área de contacto. Un HUD flotante cubría contenido del resumen en escritorio.

## Skill adaptada — Editor de retículas, espacio y texto
Fuentes metodológicas: `addyosmani/agent-skills` → `frontend-ui-engineering`, `browser-testing-with-devtools`, `constraint-driven-development`, `code-review-and-quality`. Los principios siguientes son la interpretación específica de CRITERIO, no una copia literal de los upstream.

### 1. Espaciado: intención antes de decoración
- Usar escala de 8, 16, 24, 32 y 48 px para componentes; los capítulos conservan su espaciado expresivo responsivo.
- Alinear títulos, información secundaria y CTA a una retícula común, evitando contenedores que invadan columnas vecinas.
- Evitar paneles flotantes permanentes cuando duplican navegación y cubren texto.

### 2. Tipografía: medidas reales
- Un solo `h1`; `h2` para capítulos y `h3/h4` para la estructura interior.
- Comprobar `scrollWidth > clientWidth` de titulares **además** del ancho total de la página.
- Reducir tamaño tipográfico de forma fluida antes de ocultar, cortar o romper palabras artificialmente.
- Mantener textos de lectura en medida aproximada máxima de 65 caracteres y line-height legible; los titulares cinematográficos pueden ser más grandes, pero no desbordar.
- Validar ancho 320–1920 px con fuentes fallback; pendientes Safari/iOS y fuentes remotas.

### 3. Redacción
- Inicio: ¿qué hace y para quién? Perfil: ¿qué capacidades tiene? Experiencias: ¿qué hizo? Evidencia: ¿qué se puede demostrar? Contacto: ¿cómo escribirle?
- Evitar repetir la misma promesa genérica («acción») en todos los encabezados. Usar «TRES FRENTES. UNA VISIÓN.» en la lectura rápida para orientar, no reiterar la portada.
- Respetar logros existentes (+40 % conversión en 20 Prod.; +25 % engagement y −15 % tiempo de respuesta en SUNAFIL). Evitar atribuir resultados a trabajos no documentados.
- Comunicación para el desarrollo: interés y orientación profesional; no inventar intervenciones C4D.

### 4. Movimiento y accesibilidad
- Los VFX no deben ocultar texto o enlaces. Movimiento activado por defecto salvo preferencia de movimiento reducido, con pausa disponible.
- El scroll por capas mueve decoración, nunca bloques de lectura ni enlaces.

## QA para aceptación
- Script `qa/editorial_contract.py` en Chromium comprueba 13 tamaños (320, 360, 375, 390, 430, 600, 700, 768, 900, 1024, 1280, 1440, 1920), seis familias de titulares, cajas de contacto, ancho total, no invasión del HUD, tres especialidades y sin errores JS.
- `qa/browser_smoke.py`, `qa/navigation_quality.py`, `qa/marketing_positioning.py`, `qa/editorial_depth.py`, `qa/static_checks.py` y `qa/resource_budget.py` complementan estos checks.
- No llamar «sin bugs» a un diseño solo porque GitHub Pages publique correctamente.

## Evidencia
- Fallo original: `audit-before.json`: 4 casos de caja excedida (contacto 320; HABLEMOS 1024/1280/1440).
- Tras corrección: `audit-after.json` y `QA_EDITORIAL_CONTRACT_V7_13.json`: 0 casos en tamaños auditados.
- Entorno: Chromium local, fuentes fallback, HTML/CSS/JS inlined. Pendiente prueba real con Google Fonts y navegadores móviles físicos.
