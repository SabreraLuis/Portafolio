# CRITERIO — INK / IMPACT V7 (candidate)

Web CV profesional de Luis Alberto Sabrera Espinoza, versión **independiente** en `criterio-v7/`.

## Una idea gráfica propia

**El archivo de las decisiones.** Tres acciones conectan carrera, método, movimiento e identidad: **Entender → Decidir → Demostrar**. Un corte carmín atraviesa la retícula editorial y revela el contenido.

No contiene personajes, logos o composiciones copiadas de *Bleach*. No contiene retrato ficticio ni imágenes ajenas utilizadas como si fueran evidencia. Toda experiencia y cifra proviene del CV facilitado por el usuario. El sitio es público y muestra email/teléfono.

## Arquitectura

HTML5 semántico + un CSS de diseño y movimiento + **un solo controlador JavaScript**. No se usa scroll hijacking ni se oculta información cuando no hay JS. No depende de librerías JS.

## Interacción y rendimiento

- Portada animada con reproducción explícita.
- Motion reducido por defecto cuando el SO lo solicita; reproducción manual permite *opt-in* del usuario.
- Cambio de capítulo y progreso de lectura mediante `requestAnimationFrame`.
- Reveal progresivo con IntersectionObserver y fail-open temporizado.
- Foco visible, navegación teclado/Escape, CTA PDF, email, teléfono e impresión `@media print`.
- Animaciones continuas pausadas cuando la portada no está visible.

## Publicación

URL candidata: https://sabreraluis.github.io/Portafolio/criterio-v7/

La V6.2 y el portafolio principal NO se sustituyen. **QA local con fuentes fallback no garantiza la apariencia final con Google Fonts en Android/iOS**. Ver `QA_REPORT.json` para pruebas realmente ejecutadas.

## Procedencia

Método derivado de la habilidad A.P.U `web-experience-engineering@0.1.0` staging, con fuentes primarias `addyosmani/agent-skills`. Véase: https://github.com/SabreraLuis/A.P.U-AUTOMATIZACI-N-PROGRESIVA-UNIVERSAL-/blob/main/skills/web-experience-engineering/SKILL.md
