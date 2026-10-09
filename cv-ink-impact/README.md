# CV — INK / IMPACT (Luis Sabrera)

Micrositio de CV profesional para Luis Alberto Sabrera Espinoza, basado en su CV compartido el 09/10/2026. Diseño original **INK / IMPACT**, bajo el lenguaje *Bold Cinematic Editorial*: tipografía de gran escala, alto contraste, composición de moda y espacios negativos. Inspiración conceptual en recursos compositivos del anime **Bleach: Thousand-Year Blood War**; sin utilizar material o diseños protegidos de la obra.

## URL prevista en GitHub Pages

Si GitHub Pages publica la rama main desde la raíz del repositorio Portafolio:

https://sabreraluis.github.io/Portafolio/cv-ink-impact/

La carpeta es completamente autónoma y **no altera el portafolio principal** alojado en la raíz.

## Stack

HTML, CSS, JavaScript puro. Sin frameworks, build ni dependencias JavaScript externas. Utiliza fuentes de Google Fonts con alternativas locales.

## Uso local

Abrir index.html o ejecutar desde la raíz de este directorio:

    python -m http.server 8000

Visitar http://localhost:8000

## Contenido y trazabilidad

Todo el contenido factual proviene del CV profesional compartido por el usuario. Los titulares editoriales son copy conceptual, no nuevas declaraciones de resultados. Resultados: +40% conversión clientes potenciales (20 Prod.; contribución), +25% engagement y −15% tiempo de respuesta (SUNAFIL). Se incluyen herramientas y fechas informadas en el CV. No se han inventado nuevos indicadores, formación o certificaciones.

El botón «GUARDAR CV EN PDF» usa la función de impresión del navegador: selecciona «Guardar como PDF». No apunta a un archivo inexistente.

## Accesibilidad y QA

- Navegación por teclado y enlace para saltar al contenido.
- Menú móvil con aria-expanded, cierre al navegar, clic exterior o Escape.
- Contenido disponible sin JavaScript; reveal con fallback.
- Animación desactivada con prefers-reduced-motion.
- Diseño adaptable a dispositivos móviles y formato de impresión A4.
- Acentos de rojo sobre fondos no se utilizan para texto pequeño esencial.
- No hay tracking, cookies, formularios externos ni envío de datos.

## Personalización

- Textos y experiencia: index.html
- Estética y puntos de quiebre: styles.css
- Navegación/impresión/motion: script.js

**Privacidad:** al estar publicado en GitHub Pages, el correo y teléfono declarados en el CV son públicos. Para ocultarlos, modifica la sección de contacto antes de difundir la URL.
