/* INK / IMPACT — restrained editorial motion. Native browser APIs, no dependencies. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduceQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const button = document.getElementById('motion-switch');
  const switchLabel = document.getElementById('motion-switch-label');
  const hudCount = document.getElementById('hud-number');
  const hudTitle = document.getElementById('hud-title');
  const hero = document.getElementById('inicio');
  const art = document.getElementById('hero-art');
  const toast = document.getElementById('toast');
  let manualOff = false;
  try { manualOff = sessionStorage.getItem('ink-impact-no-motion') === '1'; } catch (_) {}
  let active = !reduceQuery.matches && !manualOff;
  let toastTimer = 0;
  let activeAnimations = [];
  const observed = new WeakSet();
  const sections = [
    [hero, '00', 'PORTADA'],
    [document.getElementById('perfil'), '01', 'PERFIL'],
    [document.getElementById('trayectoria'), '02', 'TRAYECTORIA'],
    [document.querySelector('.proof'), '03', 'RESULTADOS'],
    [document.getElementById('especialidades'), '04', 'EXPERTISE'],
    [document.getElementById('formacion'), '05', 'FORMACIÓN'],
    [document.getElementById('contacto'), '06', 'CONTACTO']
  ];
  const setMotionUI = () => {
    active = !reduceQuery.matches && !manualOff;
    root.classList.toggle('motion-active', active);
    root.classList.toggle('manual-reduced', !active);
    button.setAttribute('aria-pressed', String(active));
    button.setAttribute('aria-label', reduceQuery.matches ? 'Animaciones reducidas por configuración del sistema' : (active ? 'Desactivar las animaciones' : 'Activar las animaciones'));
    button.disabled = reduceQuery.matches;
    switchLabel.textContent = reduceQuery.matches ? 'MOVIMIENTO / SISTEMA' : (active ? 'MOVIMIENTO / ON' : 'MOVIMIENTO / OFF');
    if (!active) { activeAnimations.forEach(a=>a.cancel()); activeAnimations=[];art.style.setProperty('--art-x','0px');art.style.setProperty('--art-y','0px'); }
  };
  const say = message => {
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(()=>toast.classList.remove('is-visible'), 2200);
  };
  button.addEventListener('click', () => {
    if(reduceQuery.matches) return;
    manualOff = !manualOff;
    try { sessionStorage.setItem('ink-impact-no-motion', manualOff?'1':'0'); } catch (_) {}
    setMotionUI();
    say(manualOff ? 'ANIMACIONES DESACTIVADAS' : 'ANIMACIONES ACTIVADAS');
  });
  reduceQuery.addEventListener?.('change', setMotionUI);
  setMotionUI();
  // Keep main navigation current without scroll hijacking.
  const navLinks=[...document.querySelectorAll('.nav a[href^="#"]')];
  let raf=0;
  const updateSection=()=>{
    let current=sections[0];
    const cutoff=innerHeight*.38;
    for(const s of sections){if(s[0] && s[0].getBoundingClientRect().top <= cutoff)current=s;}
    hudCount.textContent=current[1]+'—06';hudTitle.textContent=current[2];
    for(const a of navLinks){const isCurrent=a.hash==='#'+current[0].id;a.classList.toggle('is-current',isCurrent);if(isCurrent)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');}
    cancelAnimationFrame(raf);raf=0;
  };
  addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(updateSection)},{passive:true});
  addEventListener('resize',()=>{if(!raf)raf=requestAnimationFrame(updateSection)},{passive:true});
  updateSection();
  // Choreographed entrance. Never hide the content; API animates transient compositor-only layers.
  if ('IntersectionObserver' in window){
    const targets=[
      ...document.querySelectorAll('.chapter,.intro-statement,.intro-detail,.work-head,.role,.proof-intro h2,.proof-primary,.proof-secondary>div,.skills-lead,.skill-item,.edu-item,.contact-above,.contact h2,.contact-bottom,.break-lines>span,.outro-index>span:nth-child(2)')
    ];
    const io=new IntersectionObserver(entries=>{
      for(const entry of entries){
        if(!entry.isIntersecting)continue;
        io.unobserve(entry.target);
        if(observed.has(entry.target))continue;
        observed.add(entry.target);
        if(!active || document.visibilityState==='hidden')continue;
        const el=entry.target;
        let from={opacity:.35,transform:'translateY(23px)'};
        let duration=650;
        if(el.closest('.break-lines')){from={opacity:0,transform:'translateX(-46px)'};duration=820;}
        else if(el.classList.contains('role')){from={opacity:.46,transform:'translateY(36px)'};duration=740;}
        else if(el.matches('.intro-statement,.work-head,.contact h2')){from={opacity:.25,transform:'translateY(31px)'};duration=840;}
        const a=el.animate([from,{opacity:1,transform:'none'}],{duration,easing:'cubic-bezier(.18,.78,.24,1)'});
        activeAnimations.push(a);
        a.addEventListener('finish',()=>{activeAnimations=activeAnimations.filter(x=>x!==a)},{once:true});
      }
    },{threshold:.12,rootMargin:'0px 0px -8% 0px'});
    targets.forEach(el=>io.observe(el));
    // Metrics retain a complete and accessible fallback until animated.
    const metrics=[...document.querySelectorAll('[data-count]')];
    const counted=new Set();
    const numberIO=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        if(!entry.isIntersecting)return;
        numberIO.unobserve(entry.target);
        if(counted.has(entry.target))return;
        counted.add(entry.target);
        if(!active || document.visibilityState==='hidden')return;
        const target=entry.target;
        const total=Number(target.dataset.count);
        const prefix=target.dataset.prefix||'';
        const t0=performance.now();
        const duration=1100;
        const tick=t=>{
          if(!active){target.textContent=prefix+total;return;}
          const p=Math.min(1,(t-t0)/duration), eased=1-Math.pow(1-p,3);
          target.textContent=prefix+Math.round(total*eased);
          if(p<1)requestAnimationFrame(tick);else target.textContent=prefix+total;
        };
        requestAnimationFrame(tick);
      });
    },{threshold:.6});
    metrics.forEach(el=>numberIO.observe(el));
  }
  if(active){requestAnimationFrame(()=>hero.classList.add('has-entered'));}
  // Tiny editorial parallax. Pointer fine only; no scroll parallax or scroll locking.
  if(matchMedia('(hover: hover) and (pointer: fine)').matches){
    let artRaf=0;
    art.addEventListener('pointermove',event=>{
      if(!active || artRaf)return;
      const {left,top,width,height}=art.getBoundingClientRect();
      const x=Math.max(-4,Math.min(4,((event.clientX-left)/width-.5)*8));
      const y=Math.max(-4,Math.min(4,((event.clientY-top)/height-.5)*8));
      artRaf=requestAnimationFrame(()=>{art.style.setProperty('--art-x',x+'px');art.style.setProperty('--art-y',y+'px');artRaf=0;});
    },{passive:true});
    art.addEventListener('pointerleave',()=>{art.style.setProperty('--art-x','0px');art.style.setProperty('--art-y','0px');});
  }
  const copy=document.getElementById('copy-email');
  copy?.addEventListener('click',async()=>{
    try{
      await navigator.clipboard.writeText('lpumsm@gmail.com');
      say('EMAIL COPIADO AL PORTAPAPELES');
    }catch(_){say('COPIA: LPUMSM@GMAIL.COM');}
  });
})();