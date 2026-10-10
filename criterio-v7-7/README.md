# CRITERIO V7.7 — Navigation & Reliability

CV editorial de Luis Alberto Sabrera Espinoza, versión independiente basada en CRITERIO V7.6. Mantiene dirección INK / IMPACT (corte carmín, expedientes diferenciados, capítulos cinematográficos, Living Systems y todas las cifras originales).

## Objetivo del incremento

La versión anterior perdía el acceso a la navegación al desplazarse: la cabecera tenía `position:relative`. En recorridos largos esto obligaba a volver al inicio. La versión V7.7 introduce una cabecera **sticky** que permanece accesible sin agregar barras flotantes sobre el contenido. El menú móvil muestra el capítulo actual, el enlace seleccionado tiene `aria-current="location"`, y los saltos a capítulos y expedientes transfieren el foco al contenido de destino mediante cambios de hash nativos, sin interceptar scroll ni manipular el historial.

### Correcciones y mejoras

- Cabecera persistente en PC y móvil. Estado de desplazamiento con sombra discreta.
- Navegación de sección activa sincronizada con el progreso de lectura.
- Estado de capítulo `00` a `05` en el botón MENÚ del móvil.
- Destinos semánticos de navegación con `tabindex="-1"` y gestión de foco tras `hashchange` para teclado/lectores de pantalla.
- Menú accesible, tecla Escape, cierre al escoger destino, ancho variable, altura máxima y scroll dentro del menú cuando se reduce la altura disponible.
- Desplazamiento con márgenes adecuados según la altura real de la cabecera en desktop, tablet y móvil.
- PDF local sin redirecciones entre versiones, CTA y navegación sin JS.
- Mantener un solo director JS y todos los efectos existentes con control FX ON/OFF, movimiento reducido y pausa al ocultar pestaña.
- Canonical, metadatos y nombre de versión actualizados.

## Validación

- `python qa/static_checks.py`
- `node --check app.js`
- `python qa/navigation_quality.py`: 9 tamaños desde 320 hasta 1920 px; menú, navegación mediante fragmento, foco, estado activo, sticky, reduced motion, PDF, navegación sin JavaScript.
- `python qa/browser_smoke.py`, `qa/production_gate.py`, `qa/dossier_motion.py`, `qa/cinematic_bridges.py`, `qa/living_fx.py`: pruebas de regresión de V7.6.
- `python qa/resource_budget.py`: recursos dentro del presupuesto existente.

QA: `QA_OPERABILITY_V7_7.json`. Las pruebas fueron locales usando Chromium, sin fuentes públicas cargadas. **CI y despliegue se verifican por separado**. No hay evidencia concluyente de Safari/iOS real ni de métricas de campo LCP/INP/CLS. No se proclaman “cero errores universales”.

## Arquitectura y rollback

Alojamiento estático en GitHub Pages, sin backend ni APIs necesarias. Fuentes y activos externos se mantienen como en V7.6; sin analítica ni cookies añadidas. Las experiencias, textos, estadísticas y email permanecen sin alteración. Fuente profesional: PDF original del CV.

- Nueva web: https://sabreraluis.github.io/Portafolio/criterio-v7-7/
- Rollback: https://sabreraluis.github.io/Portafolio/criterio-v7-6/
- Repositorio: `SabreraLuis/Portafolio`, sin tocar el portafolio principal de la raíz.
