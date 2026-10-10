# CRITERIO — Plan de evolución para el CV INK / IMPACT

**Estatus:** diagnóstico y especificación, NO implementación. Fecha: 2026-10-09.
**Origen del método:** habilidad staging A.P.U `web-experience-engineering`, derivada de `addyosmani/agent-skills` (commit 1401c8b8030e023baeebb31781a6653fe8e93026).
**Página baseline:** https://sabreraluis.github.io/Portafolio/cv-ink-impact-v6-2/
**Alcance:** exclusivamente CV personal en Portafolio. No modificar la portada raíz ni CHAKA, CRM u otros proyectos.

## Hallazgos objetivos de la versión actual
- La UI funciona como página estática HTML/CSS/JS y contiene navegación, PDF, identidad editorial, experiencias, cifras y movimiento.
- Hay **tres capas CSS** (`styles.css`, `motion-director.css`, `motion-boost.css`) y **dos directores JS** (`app.js`, `motion-director.js`). Diferentes capas controlan efectos en la misma portada; hay reglas `!important` en la capa correctiva. Riesgo real de conflicto y mantenimiento; requiere inventario de selectores antes de simplificar.
- `MOTION_QA.json` describe comportamientos de la iteración VI.2.1 y debe actualizarse frente a las correcciones VI.2.2, especialmente el opt-in del usuario con reduced-motion. No usarlo como prueba de VI.2.2 sin nuevas mediciones.
- `DESIGN_SYSTEM.md` termina en VI.2.1; documentar estados de motion actuales.
- No existe, en la documentación examinada, evidencia actual de Lighthouse/INP/LCP/CLS ni validación Safari iOS de la versión pública. **PENDIENTE**, no FAIL probado.
- En el estado editorial actual, las secciones siguen una gramática recurrente de titulares enormes + rectángulos: propuesta de identidad CRITERIO busca composición y secuencia más distintivas.

## Propuesta creativa original (no es doctrina de Addy Osmani)
**INK / IMPACT: CRITERIO — El archivo de las decisiones**.
Una línea de corte como elemento de marca: ENTENDER → DECIDIR → DEMOSTRAR. Más precisión editorial que decoración. Negro #101113, papel #EEE9E0, carmín #E3453E, cian tenue #91CADB usado solo para datos/estado. No usar logos/personajes ni composición literal de Bleach TYBW; inspirarse en contraste, tensión y economía gráfica. No usar retratos generados presentados como Luis.

## Slices para implementar
### P0 — Gate técnico y baseline (sin cambios visuales)
- Auditar carga real de CSS/JS y PDF desde Pages, errores de consola, controles de motion, preferencias almacenadas, tamaño de imágenes/fuentes, h1/alt/aria, contraste, foco.
- Capturas **reales** en PC (1440/1920) y móvil (320/390/430), con y sin movimiento reducido.
- Capturar trayectoria temporal para poster/motion en 0/800/1600 ms, demostrar cambios visibles.
- Medir Core Web Vitals reales o sinteticos; registrar equipo, navegador, hora y condiciones.
- Criterio: baseline trazado, bugs reproducibles con pasos.

### P1 — Sistema visual CRITERIO (prototipo design-only)
- Componer tres escenas maestras: portada, caso de experiencia, contacto/cierre en 390px y 1440px.
- Retícula 12 col desktop / 4 col móvil con subgrid/fluidez donde aplique; no copiar como preset ciego.
- Sistema de escala tipográfica, márgenes, densidad, contrastes, diagramas originales y jerarquía de lectura a 5 segundos.
- Criterio: nombre, profesión, enfoque, CTA y prueba profesional distinguibles sin scrollear excesivamente; sin overflow.

### P2 — Narrativa de CV, sin inventar
- Organizar: portada / entender / decisiones en 4 experiencias / evidencia de resultados / método y herramientas / contacto.
- Cada caso presenta problema/contexto conocido, trabajo efectuado y resultado verificable; no atribuir resultados a empresas sin sustento.
- +40% corresponde a 20 Prod.; +25% y -15% a SUNAFIL. Los otros trabajos se cuentan sin porcentajes inventados.
- CTA principal "Ver experiencias"; secundario PDF real. Email y teléfono funcionales.
- Criterio: lectura reclutador de 90 segundos y recorrido visual largo coherente.

### P3 — Motion como gramática de tres actos
- CORTE: revela transición de contenido por máscara gráfica; sin ocultación persistente.
- ALINEACIÓN: retícula se ordena al entrar en cada capítulo; sin mover el párrafo de lectura.
- EVIDENCIA: datos aparecen después del enunciado y con respaldo contextual, sin animaciones numéricas engañosas.
- Reemplazar dos directores JS + tres CSS superpuestos por un coordinador de estados pequeño, con tokens y contrato de triggers; no agregar bibliotecas por moda.
- Estado reducido accesible y activación manual explícita; nunca imponer animación intensa a preferencias del dispositivo.
- Criterio: dos frames reproducibles y cambio de transform/opacity verificable, zero jank crítico, contenido legible sin JS.

### P4 — UX PC/Móvil + accesibilidad
- Móvil 320/360/390/430, tablet 768/1024, desktop 1440/1920. Alternar retrícula acorde al contenido, no apilar todo sin criterio.
- Botones táctiles ≥44×44 CSS px como meta interna de diseño; menú, Escape, focus visible, target, texto, CTA, estados de loading, enlaces y lectura sin JS.
- WCAG AA para texto normal/expandido y pruebas automatizadas+manuales (contraste, semántica, foco, lector de pantalla).
- Probar print PDF, descarga original, 200s de assets y navegación Safari/Chrome real cuando disponible.
- Criterio: 0 overflow, 0 interacciones inertes y 0 contenido oculto por efectos.

### P5 — Performance, review y ship
- Definir budgets desde baseline; prioridades LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, previa comprobación de trazas/percentiles.
- No optimizar a ciegas; identificar cuello de botella, corregirlo y comparar bajo las mismas condiciones.
- 5-axis review (corrección, simplicidad, arquitectura, seguridad/procedencia, rendimiento) + dirección artística.
- Publicar como variante aislada, medir Pages real, verificar recursos, registrar rollback y comparación visual.
- **GO** únicamente con pruebas observadas; no confundir Actions verde con UI auditada.

## Evidencia mínima a adjuntar al PR
1. Screenshots comparativas (baseline y candidata) en 390 y 1440.
2. Registro de animación t0/t1, preferencia de movimiento y resultado visible.
3. Matriz de navegación, errores, overflow, focus y JS.
4. Lighthouse / Web Vitals si disponible; pendientes marcados de forma explícita.
5. Resultado de revisión de derechos y verificación del CV.
6. Procedimiento de rollback a la V6.2 anterior.

## Fuente primaria del método
https://github.com/addyosmani/agent-skills
Basado especialmente en frontend-ui-engineering, browser-testing-with-devtools, spec-driven-development, constraint-driven-development, performance-optimization, incremental-implementation, code-review-and-quality, debugging-and-error-recovery y shipping-and-launch.
