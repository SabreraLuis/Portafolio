# CRITERIO / INK IMPACT — V7.3 (Dossier Edition)

CV web profesional de **Luis Alberto Sabrera Espinoza**, en la dirección editorial propia *CRITERIO — El archivo de las decisiones*. La versión V7.3 es una candidata independiente: conserva intactas V7.2, V7.1 y la raíz de Portafolio.

## Qué cambia

- Los cuatro expedientes profesionales reciben tratamientos gráficos **diferenciados pero coherentes**: adquisición/funnel, branding +40 %, CRM SaaS/UX y comunicación +25 % / −15 %.
- Se añade una gramática de marca original: líneas de corte, leyendas editoriales de cada expediente, jerarquía tipográfica y enfoque cromático por caso.
- Navegación contextual entre expedientes: índice con `aria-current`, indicador de progreso editorial y accesos a método/evidencia con hechos reales del CV.
- Movimiento visual comprobado: cada expediente activo utiliza transformaciones CSS ligeras; la preferencia de movimiento reducido se respeta y la reproducción manual requiere gesto explícito. Sigue habiendo un único JS y un único CSS.
- Corrección crítica en móvil: el breakpoint de tablet dejaba `.dossier-text` en `grid-column: 2/-1`, creando una segunda columna implícita de 58px y comprimiendo los gráficos. Ahora el diseño de teléfono usa un ancho completo en todos los elementos del expediente.

## Contenido y ética

No se atribuyen números inventados: +40 % pertenece a 20 Prod.; +25 % y −15 % pertenecen a SUNAFIL. AMP y Studios TKOH presentan responsabilidades reales, sin métricas ficticias. No se usan retratos inventados, marcas copiadas ni imágenes de terceros como evidencia.

El PDF original se descarga desde `../criterio-v7/cv-luis-sabrera.pdf`, preservando el binario canónico ya publicado. **Esa carpeta debe seguir accesible**.

## QA

`python qa/static_checks.py`, `python qa/browser_smoke.py`, `python qa/dossier_motion.py`.

- 12 anchuras generales 320–1920px sin errores JavaScript ni overflow horizontal.
- 17 interacciones previas de V7.2 siguen aprobadas.
- 4 expedientes × 3 resoluciones 390/768/1440 = 12 escenarios de activación, gráfica visible, movimiento medible y navegación contextual.
- Test explícito de movimiento pausado, enlaces de evidencia/método y área táctil contextual.
- Inspección visual local de las cuatro composiciones en 390 y 1440px.

`QA_V7_3.json` conserva los resultados. Pruebas basadas en Chromium local con assets inlined, sin carga externa de Google Fonts. No se ha certificado rendimiento de producción, Safari real ni Chrome Android físico. No equivale a Lighthouse.

## Reversión

URL anterior estable: https://sabreraluis.github.io/Portafolio/criterio-v7-2/ ; no se sobrescribe ni redirecciona.

## Enfoque técnico

Frontend estático, GitHub Pages, HTML semántico, una hoja de estilos, un controlador JS. Sin backend ni nuevas dependencias. Método basado en A.P.U `web-experience-engineering@0.1.0` staging y el repositorio `addyosmani/agent-skills`, incluyendo frontend, QA real del navegador e implementación incremental.
