# CRITERIO V7.11 — Continuous Signal

Portafolio profesional de Luis Alberto Sabrera Espinoza: marketing, publicidad, comunicación institucional y UX como especialidad complementaria.

## VFX
- 24 escenas heredadas de Global Signal V7.10, conservando identidad gráfica y contenidos.
- Dos capas: movimiento ambiental continuo mientras la escena está visible e impactos que regresan aproximadamente cada 6,5 segundos.
- Un temporizador compartido comprueba escenas visibles cada 1,1 s; máximo dos impactos simultáneos y cada clase de impacto se limpia a los 1,85 s.
- VFX **encendidos por defecto** en dispositivos que no solicitan movimiento reducido. PAUSAR FX y ACTIVAR FX funcionan sin activar scroll automático. El ajuste se conserva en la sesión; cuando el sistema solicita movimiento reducido, el usuario debe optar expresamente por activarlos.
- Todo el movimiento se pausa al salir de la pestaña o al imprimir; las animaciones fuera de la vista se suspenden.
- No se modifica ningún dato profesional o cifra y la V7.10 permanece intacta.

## Calidad
`qa/living_loops.py` verifica bucles reales en Chromium junto con las pruebas ya existentes de contenido, navegación, expedientes, escenas y responsive. El control CI solo verifica Chromium; rendimiento de campo, Safari/iOS y Android físico siguen pendientes.

Sitio: https://sabreraluis.github.io/Portafolio/criterio-v7-11/
