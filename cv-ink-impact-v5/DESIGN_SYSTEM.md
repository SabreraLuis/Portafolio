# INK / IMPACT 005 — Dirección de arte, UX y motion (2026-10-09)

**Estatus:** prototipo independiente. Inspiración: principios de composición del equipo artístico de *Bleach: Thousand-Year Blood War*, retícula editorial, jerarquía tipográfica y diseño digital contemporáneo. No se reproduce propiedad intelectual de la serie. **No se cambian el CV profesional de origen, otros repositorios ni el sitio de la carpeta principal.**

## Evidencia estudiada

1. **Dirección artística real de TYBW:** https://bleach-anime.com/special/interview/08.html — grandes masas visuales, contraste figura/fondo y reducción de trazos innecesarios. Aplicación: un foco principal por escena, no sobreproducción de FX.
2. **NN/g, jerarquía visual:** https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — escala, agrupación y contraste sirven a un orden de lectura. Aplicación: nombre→rol→experiencia→evidencia→CTA.
3. **NN/g, homepage:** https://www.nngroup.com/articles/homepage-design-principles/ — comunicar con claridad quién es el profesional y qué hace antes de presentar elementos espectaculares.
4. **CSS Color OKLCH:** https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch — útil para graduar escalas perceptuales. Aplicación: tokens semánticos con valores de respaldo hexadecimales; no añadir colores sin rol.
5. **web.dev, animaciones de alto rendimiento:** https://web.dev/articles/animations-guide — preferir transform/opacity; no animar propiedades de layout ni asumir rendimiento sin perf-trace.
6. **MDN, View Transitions:** https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API — futuro posible para páginas independientes; no necesario para la landing actual.
7. **W3C WCAG 2.2:** https://www.w3.org/TR/WCAG22/ — contraste, navegación y movimiento reducido.
8. **GSAP ScrollTrigger:** https://gsap.com/docs/v3/Plugins/ScrollTrigger/ — posible herramienta para casos futuros; no se añade dependencia sin justificar el rendimiento.
9. **web.dev Core Web Vitals:** https://web.dev/articles/vitals — LCP ≤2.5 s, INP ≤200 ms y CLS ≤0.1 medidos en percentil 75.

## 1. Sistema cromático (roles, no arbitrariedad)

- `paper #F0ECE5` — portada, contenidos informativos, lectura larga.
- `ink #111112` — escenario cinematográfico, legibilidad y profundidad.
- `red #E54B3C` — tensión, formas decorativas, titulares grandes y escena de evidencia.
- `red-dark #AC3027` — etiqueta pequeña sobre papel claro (ratio aproximado 5.56:1).
- `cobalt #2347BB` — escena única de contraste que separa habilidades de formación.
- `bone #FAF6ED` — texto sobre tinta oscura y azul.

**Contrato:** no más de un acento dominante por escena. Texto normal con contraste WCAG AA (4.5:1), texto grande 3:1. La escena roja usa principalmente texto negro, no blanco sobre rojo. Verificar tokens al cambiar.

## 2. Composición editorial

- Retícula fluid-responsive: gutter `clamp(20px,4.5vw,86px)`, dos superficies en portada desktop y portada secuencial en móvil.
- Titulares condensados sin introducir quiebres que colapsen la línea. Cada contenedor tiene `min-width:0` y reglas de adaptación reales, no `overflow:hidden` aplicado como parche al texto.
- Jerarquía: 1 gran sujeto por sección → metadato pequeño → cuerpo legible → acción explícita.
- Contrastes narrativos: papel → negro → rojo (interludio) → papel → rojo (resultados) → papel → azul (formación) → negro (contacto).
- Sin tarjetas flotantes genéricas, sombras de UI estándar, degradados cosméticos ni partículas.

## 3. Gramática de movimiento

- Entrada hero: máscara de título `~810ms`; iconografía geométrica `~880ms` sin bloquear interacción.
- Reveal de titulares de sección: `640ms`, transform/opacity, una sola activación; no animar cada renglón de párrafo.
- FX: corte diagonal en poster, retícula editorial y acentos de alto contraste como elementos estáticos. No animar blur/filter masivos.
- Progreso de lectura con `requestAnimationFrame` y listener pasivo; UI de capítulos informativa, no fijaciones que atrapen scroll.
- `prefers-reduced-motion` y toggle manual de motion (sesión); contenido siempre visible sin JS.

## 4. Sistema UX y arquitectura integrada

- Fuente única de contenido profesional: CV aportado por el usuario. Toda métrica asociada a empresa y atribución correcta.
- CTA claro en portada y contacto; teléfono y correo nativos. Impresión con diseño A4 y sin FX.
- Navegación con anclas y menú móvil, foco visible, Escape y etiquetas ARIA. JSON-LD Person para datos estructurados. No tracking sin consentimiento explícito.
- HTML semántico + CSS tokens + JS de enhancement; un sitio estático no requiere SPA, API ni servidor backend para este alcance.

## 5. QA antes de GO

1. Capturas 320, 375, 390, 768, 1024, 1440 y 1920 px; sin desbordamiento horizontal.
2. Comprobar título y rol legibles con fuentes cargadas y con fallback; reproducir con/sin animaciones.
3. Pruebas teclado, menú, anclas, CTA, impresión y enlace mailto; JS sin excepciones.
4. Auditoría de contraste para todos los roles y textos pequeños, incluida la escena roja.
5. Lighthouse / Playwright cuando entorno disponible; CWV reales solo si hay mediciones de campo, no inferirlas del screenshot.
6. GO requiere revisión visual en al menos Chrome móvil, Firefox desktop y Safari/WebKit cuando sean accesibles.

## Hipótesis de producto

Un CV-landing más claro y legible, con narrativa de alto impacto y evidencia profesional, podría aumentar contactos pertinentes. **No es una afirmación de conversión**. Validar con pruebas breves de comprensión, visitas y tasa de contacto, sin recoger datos personales sin autorización.

### Contrastes calculados entre tokens (sRGB, WCAG 2.x)

- Ink / paper: **16.03:1**.
- Ink / red: **4.86:1**.
- Bone / ink: **17.50:1**.
- Bone / cobalt: **7.24:1**.
- Red-dark / paper: **5.56:1**.
- Red / paper: **3.30:1** → restringir a gran tipografía o decoración, nunca párrafos o etiquetas pequeñas.

Son cálculos cromáticos del sistema, no una auditoría automática de todos los píxeles de cada componente.
