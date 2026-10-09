# Luis Sabrera — CV editorial (INK / IMPACT v2)

CV web profesional de **Luis Alberto Sabrera Espinoza**.

## Dirección de arte

Rediseño desde cero del primer CV INK / IMPACT. Inspirado en principios formales de las tarjetas de título y la dirección visual de *Bleach: Thousand-Year Blood War*: jerarquía tipográfica fuerte, color plano, masas negras, blanco negativo, composiciones asimétricas. Se han traducido a un lenguaje de diseño web **original**, con tratamiento editorial de moda y comunicación comercial. No utiliza ilustraciones, personajes, logotipos ni composiciones exactas de la franquicia.

### Qué cambia respecto a v1

- Se retiraron gradientes, slogans genéricos, sombras y chips repetitivos.
- Hero de dos superficies y placa tipográfica compuesta a medida.
- Tipografía Barlow Condensed en titulares, DM Sans en cuerpo e IBM Plex Mono en señalética.
- Retícula editorial, capítulos y jerarquía de lectura pensados para reclutadores.
- Resultados vinculados a experiencias concretas; sin atribuciones exageradas.
- CSS reconstruido y JavaScript reducido a navegación, progreso e impresión.

## Publicación

https://sabreraluis.github.io/Portafolio/cv-ink-impact/

La carpeta `cv-ink-impact/` es independiente; el portafolio principal en la raíz del repositorio permanece intacto.

## Uso local

Abrir `index.html` en el navegador o servir la carpeta con `python -m http.server 8000`.

## Implementación

- HTML5, CSS3, JavaScript vanilla.
- Responsive para móvil, tablet y desktop; comprobación local de ancho 320, 390, 768, 960 y 1440 px.
- Menú con aria-expanded, Escape y clic exterior.
- Respeto de prefers-reduced-motion; sin paralaje ni intercepción de scroll.
- «Guardar CV en PDF» usa la impresión nativa con layout @media print.
- Sin cookies, trackers, formularios externos ni credenciales.

**Fuente profesional:** CV_Luis_Sabrera_Coordinador_Marketing_B2B_B2C.pdf, proporcionado por el usuario. Correo y teléfono del CV son visibles públicamente en GitHub Pages.

## Referencia investigada

Entrevista oficial del equipo de color y diseño de TYBW: https://bleach-anime.com/special/interview/08.html


## V3 — Kinetic Editorial Motion

Fecha: 2026-10-09. Rediseño incremental sobre INK / IMPACT V2.

### Dirección visual
Inspiración conceptual contrastada con el sitio oficial de Bleach TYBW: https://bleach-anime.com/keyword/ y entrevista con dirección de color: https://bleach-anime.com/special/interview/08.html. Combinación original de masas negras, titulares recortados, retículas editoriales, contraste carmín/negro/papel, y alternancia de pausas visuales y composición tipográfica. Sin copiar logos, personajes, animaciones ni láminas originales.

### Cambios
- `motion.css`: gramática de animación, cubierta cinética, trama editorial, transiciones de capítulos, línea de lectura, tipografía intermedia PENSAR/HACER/MEDIR, señalización HUD y microinteracciones.
- `motion.js`: animaciones de entrada con Web Animations API y IntersectionObserver, contador de métricas que conserva sus valores accesibles, respuesta fina al puntero limitada a ±4px, HUD de capítulo activo, desactivación manual de movimiento por sesión, y botón copiar correo con fallback.
- `index.html`: semántica de nuevas secciones editoriales, botones y ayudas accesibles.
- La información factual y las experiencias del CV permanecen sin cambios, y el portafolio principal en la raíz no se modifica.
- Sin dependencias JS externas, sin scroll hijacking ni animaciones infinitas.
- Reducción de movimiento a nivel OS (`prefers-reduced-motion`), control manual de movimiento y tratamiento de impresión.

### QA local
Inspección automatizada en Chromium a 320, 390, 768, 1440 y 1920 px (desktop, móvil y tablet), con y sin reducción de movimiento. Verificados los enlaces internos, H1 único, ausencia de errores JavaScript, ausencia de desplazamiento horizontal, menú móvil (abrir/cerrar/Escape), control de movimiento ON/OFF y presencia de 4 experiencias. Se observaron elementos decorativos desbordados dentro de sus contenedores con `overflow:hidden` intencionalmente, sin aumentar el scroll horizontal.
