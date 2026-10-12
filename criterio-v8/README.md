# CRITERIO V8 — High Impact Editorial

CV web de Luis Alberto Sabrera Espinoza, desarrollado como **versión independiente** de las versiones V7 y del portafolio principal.

## Intención de diseño

Comunicación que genera acción: identidad editorial negra/crema/carmín, tipografía condensada de alta intensidad, carteles asimétricos, cortes diagonales, expedientes con ilustraciones CSS originales y un cierre de contacto directo. Construida como HTML/CSS/JavaScript funcional; no se está publicando una imagen del mockup.

## Contenido y veracidad

Datos profesionales y métricas proceden del CV de origen: 20 Prod. (+40 % de conversión a la que contribuyó), SUNAFIL (+25 % engagement, −15 % tiempo de respuesta), Amazon Magic Park (campañas, leads y CRM), Studios TKOH (UX/UI complementario). No se incorporaron cifras especulativas del mockup (+5M, +40 campañas, +12 marcas, +10 años), fotografías ficticias ni casos inventados. Los paneles visuales son **abstracciones gráficas originales**, no fotografías documentales de clientes ni muestras reales de campañas.

## Tecnología

- HTML semántico, CSS nativo, JavaScript sin dependencias ni backend.
- Navegación por anclas, menú móvil con Escape, progreso de lectura, control FX on/off, scroll nativo, elementos visuales con parallax moderado, preferencia de movimiento reducido y navegación sin JS.
- Imágenes de proyectos hechas con formas CSS, por motivos de licencia y veracidad.
- Fuentes de Google Fonts con respaldo local; el diseño se prueba sin acceso a Google Fonts.
- A.P.U. no modificó la raíz ni versiones anteriores del repositorio.

## Pruebas

`python qa/smoke.py` con Playwright + Chromium instalado: 13 anchos 320–1920 px, clipping de títulos y CTA, overflow, enlaces, menú, Escape, efectos, reduced-motion y navegación sin JavaScript. Capturas locales están en `previews/` (no garantizan equivalencia exacta con Safari ni con fuentes remotas). CI separado para la carpeta V8.

## Pendiente antes de promoción como CV principal

Verificación pública HTTP/CDN y Google Fonts, Lighthouse/Core Web Vitals, Safari/iPhone y Android físico. Sustituir las ilustraciones de casos por **activos profesionales reales autorizados** cuando estén disponibles. Confirmar lenguaje de comunicaciones para desarrollo en entrevista/currículum antes de afirmar proyectos C4D.

## Reversibilidad

Último baseline V7.13: `https://sabreraluis.github.io/Portafolio/criterio-v7-13/`. La V8 se sirve desde su propia carpeta, sin redirección de raíz.