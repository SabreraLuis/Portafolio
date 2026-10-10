/** INK / IMPACT — V6.2.1 Motion Director.
 * Adds observable page motion without a library. All scene content is visible before JS.
 */
(() => {
  'use strict';
  const root = document.documentElement;
  const hero = document.querySelector('.hero');
  const scenes = [...document.querySelectorAll('.scene[data-scene]')];
  const cases = [...document.querySelectorAll('.case')];
  const button = document.getElementById('replay-intro');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const enabled = () => root.classList.contains('motion-enabled') && !root.classList.contains('reading-mode');

  // The legacy build marked every reveal as "in" on startup: this is intentionally
  // corrected in app.js. This director provides distinctive choreography, not just fades.
  const sceneObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting && enabled()) {
      entry.target.classList.add('is-motion-seen');
      sceneObserver.unobserve(entry.target);
    }
  }, {threshold:0, rootMargin:'0px 0px -90px 0px'}) : null;
  const caseObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting && enabled()) {
      entry.target.classList.add('is-motion-seen');
      caseObserver.unobserve(entry.target);
    }
  }, {threshold:0, rootMargin:'0px 0px -90px 0px'}) : null;
  const heroObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    for (const entry of entries) hero.classList.toggle('is-motion-paused',!entry.isIntersecting);
  }, {threshold:0}) : null;
  if (heroObserver && hero) heroObserver.observe(hero);
  if (sceneObserver) scenes.forEach(scene => sceneObserver.observe(scene));
  if (caseObserver) cases.forEach(item => caseObserver.observe(item));

  let replayAnimations=[];
  function cancelReplay() { replayAnimations.forEach(animation=>animation.cancel()); replayAnimations=[]; }
  function sync() {
    const status = document.getElementById('motion-state');
    if (status) status.textContent = enabled() ? 'FX EN MOVIMIENTO' : (reduce.matches ? 'EFECTOS PAUSADOS · PULSA REPRODUCIR' : 'FX PAUSADOS · PULSA REPRODUCIR');
    if (!enabled()) {
      cancelReplay();
      // Never conceal content, don't run intro with reduced-motion setting.
      button.disabled = false;
      button.title = 'Reproducir secuencia; activará el movimiento solo si lo solicitas';
    } else {
      button.disabled = false;
      button.title = 'Repetir la secuencia de entrada';
      if (!sceneObserver) scenes.forEach(scene=>scene.classList.add('is-motion-seen'));
      if (!caseObserver) cases.forEach(item=>item.classList.add('is-motion-seen'));
      // If motion was re-enabled mid-scroll, trigger the currently visible chapters.
      for (const item of [...scenes, ...cases]) {
        const r=item.getBoundingClientRect();
        if (r.top < innerHeight*.86 && r.bottom > innerHeight*.10) item.classList.add('is-motion-seen');
      }
    }
  }
  const stateObserver = new MutationObserver(sync);
  stateObserver.observe(root,{attributes:true,attributeFilter:['class']});
  if(reduce.addEventListener)reduce.addEventListener('change',sync);
  sync();
  button.addEventListener('click',() => {
    if (!enabled()) {
      if (root.classList.contains('reading-mode')) document.getElementById('reading-toggle')?.click();
      if (!enabled()) document.getElementById('motion-toggle')?.click();
    }
    if (!enabled() || typeof Element.prototype.animate !== 'function') return;
    cancelReplay();
    const sequence=[
      ['.hero-pretitle', [{opacity:0,transform:'translateY(15px)'},{opacity:1,transform:'translateY(0)'}],650,0],
      ['.hero-title .mask:nth-child(1)>span',[{transform:'translateY(120%)'},{transform:'translateY(0)'}],1100,70],
      ['.hero-title .mask:nth-child(2)>span',[{transform:'translateY(120%)'},{transform:'translateY(0)'}],1100,230],
      ['.hero-tagline',[{opacity:0,transform:'translateX(-25px)'},{opacity:1,transform:'translateX(0)'}],750,670],
      ['.hero-intro',[{opacity:0,transform:'translateY(25px)'},{opacity:1,transform:'translateY(0)'}],750,780],
      ['.hero-right',[{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0 0 0)'}],1300,150]
    ];
    for (const [selector,frames,duration,delay] of sequence){
      const element=document.querySelector(selector);
      if (!element) continue;
      const animation=element.animate(frames,{duration,delay,fill:'both',easing:'cubic-bezier(.22,1,.36,1)'});
      replayAnimations.push(animation);
      animation.onfinish=()=>{ animation.cancel(); replayAnimations=replayAnimations.filter(a=>a!==animation); };
    }
  });
})();
