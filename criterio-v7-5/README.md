# CRITERIO — INK / IMPACT V7.5 (Production Polish)

Portafolio/CV profesional de Luis Alberto Sabrera Espinoza, en la identidad original **CRITERIO: El archivo de las decisiones**.

**URL** https://sabreraluis.github.io/Portafolio/criterio-v7-5/

## Release

- Mantiene la identidad editorial de V7.4: corte carmín, cuatro expedientes profesionales, narrativa Entender → Decidir → Demostrar, dos puentes cinematográficos y navegación de capítulos.
- El PDF original se incorpora en la propia carpeta; ninguna descarga depende de una ruta de versión anterior.
- Añade pausado de animaciones cuando la página queda en segundo plano, restauración con `pageshow` y fallback de revelados sin transiciones innecesarias.
- Ajusta área táctil, foco, texto largo, scroll a anclas, impresión y safe areas de móvil.
- Los datos profesionales y las cifras se mantienen fieles al CV entregado. No se introduce un backend innecesario.
- El portafolio principal y V7.4 permanecen sin modificar.

## Stack

HTML semántico, CSS nativo, JavaScript vanilla, sin frameworks ni librerías JS de terceros. Fuentes externas con fallback. Todos los controles son de progresive enhancement; sin JavaScript, los enlaces y el CV siguen disponibles.

## Validación reproducible

```bash
python qa/static_checks.py
node --check app.js
python qa/resource_budget.py
python qa/browser_smoke.py
python qa/dossier_motion.py
python qa/cinematic_bridges.py
python qa/production_gate.py
```

Los tests de navegador usan Chromium local con CSS/JS inlined para que las pruebas sean deterministas en entornos sin internet. **Esta técnica no valida la carga CDN pública**.

Los artefactos de evidencia son `QA_POLISH.json`, `QA_DOSSIER_MOTION.json` (cuando se genere), `QA_PRODUCTION_V7_5.json`, `QA_RESOURCE_BUDGET.json`, y `QA_RELEASE_V7_5.json`. El despliegue se verifica aparte en GitHub Actions.

## Definición de terminado

- Pruebas estáticas y navegador automáticas en verde.
- QA visual desktop/mobile con capturas disponibles.
- GitHub Pages desplegado, archivos leídos de vuelta desde GitHub.
- PDF incluido en directorio y descargable.
- Pruebas externas aún no realizadas: Safari iOS, hardware Android, Google Fonts cargadas en producción, Lighthouse/Core Web Vitals de usuarios reales. Estas limitaciones se declaran abiertamente; no se promete “cero errores absolutos”.

## Rollback

1. Mantener el acceso a `criterio-v7-4/`, que no fue modificado.
2. Si un problema real se detecta en V7.5, dirigir de nuevo a `criterio-v7-4/` mientras se corrige la carpeta de V7.5 en una rama segura.
3. El historial Git conserva todos los archivos de ambas versiones.

## Conocimiento aplicado

Adaptación de `web-experience-engineering@0.1.0` (A.P.U. staging), basada en skills de frontend UI, pruebas en navegador, CI/CD, rendimiento y seguridad de https://github.com/addyosmani/agent-skills .
