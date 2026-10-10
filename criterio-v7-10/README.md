# CRITERIO V7.10 — Global Signal

**Luis Alberto Sabrera Espinoza — marketing, publicidad y comunicación institucional.**

## Qué cambió respecto a V7.9

- La animación aparece automáticamente al abrir la web y entrar en cada escena en navegadores con movimiento normal. El botón **PAUSAR FX** detiene inmediatamente los efectos; **REPETIR APERTURA** permite reproducir la portada sin ser requisito para ver animación.
- El nuevo controlador en `app.js` dirige 24 puntos de escena: perfil, tres especialidades, perspectiva de comunicación para el desarrollo, puente editorial, encabezado de trayectoria, cuatro experiencias, interludio, bloque de resultados, tres resultados, método, tres etapas, formación, segundo puente y contacto.
- Cada capítulo usa un lenguaje de movimiento diferente: máscaras editoriales, líneas de precisión, señales sobre casos, cortes en métricas, barras del método y salida cinematográfica en contacto.
- Los efectos se activan por `IntersectionObserver`, pueden volver a ejecutarse al reentrar con 2,8 s de cooldown, y desaparecen tras 980 ms. No hay intervalos globales, scroll hijacking, librerías JS, números inventados ni superposición permanente sobre textos importantes.
- Se respeta `prefers-reduced-motion`: empieza **off** si el sistema lo pide, salvo activación voluntaria. Los ajustes manuales se mantienen durante la sesión usando una clave nueva exclusiva de V7.10, por lo que un antiguo estado de pausa de V7.9 no apaga la nueva versión de manera inesperada.
- Los contenidos profesionales, datos de contacto, resultados y portafolio UX complementario permanecen sin cambios.

## Pruebas locales

- `node --check app.js`
- `python qa/static_checks.py && python qa/resource_budget.py`
- `python qa/marketing_positioning.py && python qa/browser_smoke.py`
- `python qa/navigation_quality.py && python qa/dossier_motion.py`
- `python qa/cinematic_bridges.py && python qa/production_gate.py`
- `python qa/signal_cut.py && python qa/global_scene_quality.py`

La suite Global Signal cubre 11 anchos entre 320–1920 px, 13 tipos de escenas representativas y controles de activación/pausa/reduced-motion; 24 targets existen en DOM. Local Chromium usa fuentes fallback y assets inline para CSS/JS por restricciones de red del entorno. La ruta pública, dispositivos iOS/Android físicos y Core Web Vitals reales requieren validación independiente.

## Sitio de esta versión

https://sabreraluis.github.io/Portafolio/criterio-v7-10/

V7.9 y el portafolio principal no se reemplazan. Los tres assets binarios (CV PDF, favicon y grain) se conservan exactamente de la versión GitHub V7.9 publicada; no son nuevos.
