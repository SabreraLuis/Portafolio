# CRITERIO V7.6 — Living Systems

Versión **experimental publicada en carpeta independiente** del CV profesional de Luis Alberto Sabrera Espinoza. Conserva el lenguaje visual **CRITERIO / INK IMPACT** y los contenidos reales de V7.5.

## Identidad

**Entender → Decidir → Demostrar**. Una línea de corte carmín, tipografía editorial, papel, tinta, cian y señales de negocio como vocabulario gráfico. Sin fotos sintéticas presentadas como Luis, sin piezas de terceros ni cifras inventadas.

## VFX añadidos

- **Pulso ambiental**: aurora radial, retícula y barrido de lectura en el cartel original. Microinteracción de punto orbital y señal **LIVE**. Textura raster pequeña local; no WebGL ni SVG turbulence en cada fotograma.
- **Profundidad**: respuesta acotada del cartel al cursor *solo en escritorio y puntero fino*; contraste y animaciones de ritmo independiente en móvil. Solo modifica formas decorativas, nunca párrafos.
- **Expedientes**: barrido cian, marcas de esquina y microetiquetas de producción (decorativas, no datos externos). Movimiento distinto en captación, 40 %, interfaz SaaS y resultados institucionales.
- **Evidencia**: línea que se revela y tipografía con entrada breve. Las cifras literales no se cuentan ni se alteran.
- **Interludios**: pulso adicional en el corte y la retícula, subordinados a la transición existente.
- **Interacción**: feedback de botones para hover/puntero fino y estados táctiles sin navegación capturada ni scroll bloqueado.

## Estado del movimiento

- Un solo director en `app.js`, con `requestAnimationFrame` compartido para scroll y `requestAnimationFrame` coalescido para puntero.
- FX presentes solo cuando el usuario no ha pausado (`data-motion=on`). En `prefers-reduced-motion: reduce`, se apagan inicialmente; el usuario puede encenderlos explícitamente.
- Animación ambiental pausada fuera de escena y cuando la pestaña está en segundo plano.
- Contenido esencial visible cuando JavaScript falla o las animaciones están apagadas. `@media print` oculta todos los FX.

## Arquitectura

HTML, CSS y JavaScript vanilla, sin paquetes adicionales. Recursos propios: `favicon.svg`, `grain.png` y CV PDF original. Las fuentes desde Google Fonts tienen fallback local. Un cambio en la página raíz del repositorio no es necesario.

- URL: https://sabreraluis.github.io/Portafolio/criterio-v7-6/
- Rollback: https://sabreraluis.github.io/Portafolio/criterio-v7-5/

## QA observado

- `qa/static_checks.py` — semántica/anchors/resources.
- `qa/browser_smoke.py`, `qa/dossier_motion.py`, `qa/cinematic_bridges.py`, `qa/production_gate.py` — regresiones previas.
- `qa/living_fx.py` — 9 anchos entre 320 y 1920, 4 barridos, 3 reglas de evidencia, movimiento real t0/t1, hover, pausa/reanudación, reducción y opt-in.
- `qa/resource_budget.py` — límites de HTML/CSS/JS/PDF/íconos y nuevo grain raster.
- `QA_RELEASE_V7_6.json` — síntesis de QA y límites explícitos.

**Pendiente:** inspección del CDN público con Google Fonts, pruebas en teléfonos físicos (Android e iOS) y Core Web Vitals de campo; el despliegue verde de GitHub Actions no sustituye esos controles.

## Referencias metodológicas

A.P.U `web-experience-engineering@0.1.0` (staging) y [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), especialmente `frontend-ui-engineering`, `browser-testing-with-devtools`, `performance-optimization` y `code-review-and-quality`. La estética CRITERIO es un desarrollo original del proyecto.
