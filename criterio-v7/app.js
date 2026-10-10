/** CRITERIO / INK IMPACT 001 — one motion director, no libraries. */
(() => {
  'use strict';
  const root = document.documentElement;
  const menu = document.getElementById('navigation');
  const toggle = document.getElementById('menu-btn');
  const replay = document.getElementById('replay');
  const motionStatus = document.getElementById('motion-status');
  const progress = document.getElementById('reading-progress');
  const hero = document.querySelector('.hero');
  const visual = document.querySelector('.hero-visual');
  const band = document.querySelector('.transition-band');
  const entries = [...document.querySelectorAll('[data-reveal]')];
  const chapters = [...document.querySelectorAll('[data-chapter]')];
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)');
  let userOptIn = false;
  let active = !prefersReduced.matches;
  let observer;
  let rafPending = false;
  let manualAnimations = [];
  try { userOptIn = sessionStorage.getItem('criterio-motion-opt-in') === 'yes'; } catch (_) {}
  if (userOptIn) active = true;

  const closeMenu = () => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Abrir navegación');
  };
  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar navegación' : 'Abrir navegación');
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('is-open')) { closeMenu(); toggle.focus(); } });
  document.addEventListener('pointerdown', e => { if (!menu.contains(e.target) && !toggle.contains(e.target)) closeMenu(); });

  function refreshMotion() {
    root.dataset.motion = active ? 'on' : 'off';
    motionStatus.textContent = active ? 'FX EN MOVIMIENTO' : 'FX EN PAUSA · PULSA REPRODUCIR';
    entries.forEach(entry => {
      if (!active) entry.classList.add('is-visible');
      else if (!entry.classList.contains('is-visible')) {
        const box = entry.getBoundingClientRect();
        if (box.top < innerHeight * .92 && box.bottom >= 0) entry.classList.add('is-visible');
      }
    });
    if (observer) observer.disconnect();
    if (active && 'IntersectionObserver' in window) {
      observer = new IntersectionObserver(changes => {
        changes.forEach(change => { if (change.isIntersecting) { change.target.classList.add('is-visible'); observer.unobserve(change.target); } });
      }, { rootMargin:'0px 0px -45px 0px', threshold:0 });
      entries.filter(x=>!x.classList.contains('is-visible')).forEach(x=>observer.observe(x));
    } else entries.forEach(x => x.classList.add('is-visible'));
    // Fail open: content must not remain hidden when browsers suspend observers.
    window.setTimeout(() => entries.forEach(x => x.classList.add('is-visible')), 6500);
  }
  refreshMotion();

  function cancelManual() { manualAnimations.forEach(animation => animation.cancel()); manualAnimations = []; }
  function runReplay() {
    if (prefersReduced.matches && !userOptIn) {
      userOptIn = true;
      try { sessionStorage.setItem('criterio-motion-opt-in', 'yes'); } catch (_) {}
    }
    active = true;
    refreshMotion();
    cancelManual();
    if (!Element.prototype.animate) return;
    const actions = [
      ['.hero .name-line:first-child>span', [{transform:'translateY(120%)'}, {transform:'translateY(0)'}], 1050, 0],
      ['.hero .name-line:nth-child(2)>span', [{transform:'translateY(120%)'}, {transform:'translateY(0)'}], 1000, 140],
      ['.hero-sub', [{opacity:0,transform:'translateY(19px)'},{opacity:1,transform:'translateY(0)'}], 760, 420],
      ['.hero-visual', [{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0 0 0)'}], 1350, 90]
    ];
    for (const [selector,frames,duration,delay] of actions) {
      const element = document.querySelector(selector);
      if (!element) continue;
      const animation = element.animate(frames, {duration, delay, easing:'cubic-bezier(.16,.82,.2,1)', fill:'both'});
      manualAnimations.push(animation);
      animation.finished.then(() => {animation.cancel(); manualAnimations = manualAnimations.filter(a=>a!==animation)}).catch(() => {});
    }
  }
  replay.addEventListener('click', runReplay);
  if (prefersReduced.addEventListener) prefersReduced.addEventListener('change', () => {
    if (!userOptIn) { active = !prefersReduced.matches; refreshMotion(); }
  });

  const observeHero = 'IntersectionObserver' in window ? new IntersectionObserver(changes => {
    changes.forEach(c => {visual.classList.toggle('is-paused', !c.isIntersecting);band.classList.toggle('is-paused', !c.isIntersecting);});
  },{threshold:0}) : null;
  if(observeHero) observeHero.observe(hero);

  const update = () => {
    rafPending = false;
    const length = Math.max(0, document.documentElement.scrollHeight - innerHeight);
    progress.style.width = (length ? Math.min(100, (scrollY / length) * 100) : 0) + '%';
    let chapter = '00';
    for (const section of chapters) if (section.getBoundingClientRect().top < innerHeight * .35) chapter = section.dataset.chapter;
    menu.querySelectorAll('a[href^="#"]').forEach(anchor => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target?.dataset.chapter === chapter) anchor.setAttribute('aria-current','location');
      else anchor.removeAttribute('aria-current');
    });
  };
  const scheduleUpdate = () => {if (!rafPending) {rafPending = true;requestAnimationFrame(update);}};
  addEventListener('scroll', scheduleUpdate,{passive:true});addEventListener('resize',scheduleUpdate,{passive:true});scheduleUpdate();
  window.addEventListener('beforeprint', () => { cancelManual();entries.forEach(x=>x.classList.add('is-visible')); });
})();
