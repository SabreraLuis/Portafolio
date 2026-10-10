/** CRITERIO / INK IMPACT 001 — one motion director, no libraries. */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('has-js');
  const menu = document.getElementById('navigation');
  const toggle = document.getElementById('menu-btn');
  const replay = document.getElementById('replay');
  const motionStatus = document.getElementById('motion-status');
  const motionToggle = document.getElementById('motion-toggle');
  const progress = document.getElementById('reading-progress');
  const hero = document.querySelector('.hero');
  const visual = document.querySelector('.hero-visual');
  const band = document.querySelector('.transition-band');
  const entries = [...document.querySelectorAll('[data-reveal]')];
  const chapters = [...document.querySelectorAll('[data-chapter]')];
  const cinematicBridges = [...document.querySelectorAll('[data-cinematic]')];
  let cinematicObserver;
  const hudChapter = document.getElementById('chapter-count');
  const mobileChapter = document.getElementById('menu-chapter');
  const header = document.querySelector('.masthead');
  const interlude = document.querySelector('.decision-interlude');
  const dossierItems = [...document.querySelectorAll('.dossier[data-case]')];
  const dossierLinks = [...document.querySelectorAll('[data-case-link]')];
  const caseCurrent = document.getElementById('case-current');
  const caseProgress = document.getElementById('case-progress');
  const archiveSection = document.getElementById('archivo');
  let selectedDossier = '';
  const caseLabels = {amp:'AMAZON MAGIC PARK',prod:'20 PROD.',tkoh:'STUDIOS TKOH',sunafil:'SUNAFIL'};
  const chapterLabels = {'00':'INICIO','01':'PERFIL','02':'ARCHIVO','03':'EVIDENCIA','04':'MÉTODO','05':'CONTACTO'};
  function selectDossier(next) {
    if (!next || selectedDossier === next) return;
    selectedDossier = next;
    const index = dossierItems.findIndex(item => item.dataset.case === next);
    if (index < 0) return;
    dossierItems.forEach(item => item.classList.toggle('in-focus', item.dataset.case === next));
    dossierLinks.forEach(link => {
      if (link.dataset.caseLink === next) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    if (caseCurrent) caseCurrent.textContent = String(index + 1).padStart(2,'0') + ' / 04 — ' + caseLabels[next];
    if (caseProgress) caseProgress.style.width = (index + 1) * 25 + '%';
  }
  dossierLinks.forEach(link => link.addEventListener('click', () => selectDossier(link.dataset.caseLink)));

  // Living Systems: one controller, additive decorative layers, no scroll interception.
  const finePointer = matchMedia('(hover:hover) and (pointer:fine)');
  const stage = document.querySelector('.visual-stage');
  const lightScenes = [...document.querySelectorAll('.dossier-visual')];
  const metrics = [...document.querySelectorAll('.metric')];
  let metricsObserver;
  let pointerPending = false;
  let queuedPointer = null;
  let lastVisualPointer = null;
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)');
  let userOptIn = false;
  let manualPreference = null;
  let active = !prefersReduced.matches;
  let observer;
  let rafPending = false;
  let manualAnimations = [];
  let revealTimer;
  try {
    userOptIn = sessionStorage.getItem('criterio-motion-opt-in') === 'yes';
    const saved = sessionStorage.getItem('criterio-motion-setting');
    if (saved === 'on' || saved === 'off') manualPreference = saved;
  } catch (_) {}
  if (manualPreference) active = manualPreference === 'on';
  else if (userOptIn) active = true;

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

  // Native fragments own scrolling/history; after the hash settles, place screen-reader focus on the destination.
  // Do not hijack normal scrolling or overwrite browser history.
  const focusFragment = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) { scheduleUpdate(); return; }
    const target = document.getElementById(id);
    if (target && (target.matches('section,article') || target.id === 'contenido')) {
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({preventScroll:true});
    }
    scheduleUpdate();
  };
  addEventListener('hashchange', focusFragment);
  addEventListener('resize', () => { if (innerWidth > 900 && menu.classList.contains('is-open')) closeMenu(); }, {passive:true});
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('is-open')) { closeMenu(); toggle.focus(); } });
  document.addEventListener('pointerdown', e => { if (menu.classList.contains('is-open') && !menu.contains(e.target) && !toggle.contains(e.target)) closeMenu(); });

  function syncCinematic() {
    // No content depends on these transitions: effects are decoration only.
    if (cinematicObserver) cinematicObserver.disconnect();
    if (!active || !('IntersectionObserver' in window)) {
      cinematicBridges.forEach(bridge => bridge.classList.toggle('is-cut-in',active));
      return;
    }
    cinematicObserver = new IntersectionObserver(changes => {
      for (const change of changes) {
        if (change.isIntersecting) {
          change.target.classList.add('is-cut-in');
          cinematicObserver.unobserve(change.target);
        }
      }
    }, {rootMargin: '0px 0px -45px 0px', threshold:0});
    cinematicBridges.forEach(bridge => {
      const r=bridge.getBoundingClientRect();
      if (r.top < innerHeight*.88 && r.bottom > 0) bridge.classList.add('is-cut-in');
      else cinematicObserver.observe(bridge);
    });
  }

  function syncEvidence() {
    if (metricsObserver) metricsObserver.disconnect();
    if (!active || !('IntersectionObserver' in window)) {
      metrics.forEach(metric => metric.classList.add('fx-proof-on'));
      return;
    }
    metricsObserver = new IntersectionObserver(changes => {
      changes.forEach(change => {
        if (change.isIntersecting) {
          change.target.classList.add('fx-proof-on');
          metricsObserver.unobserve(change.target);
        }
      });
    }, {threshold:0.18});
    metrics.forEach(metric => {
      const rect = metric.getBoundingClientRect();
      if (rect.top < innerHeight*.9 && rect.bottom > 0) metric.classList.add('fx-proof-on');
      else metricsObserver.observe(metric);
    });
  }

  function refreshMotion() {
    root.dataset.motion = active ? 'on' : 'off';
    root.classList.toggle('living-active', active);
    motionStatus.textContent = active ? 'FX EN MOVIMIENTO' : 'FX EN PAUSA';
    motionToggle.textContent = active ? 'PAUSAR FX' : 'ACTIVAR FX';
    motionToggle.setAttribute('aria-pressed', String(active));
    motionToggle.setAttribute('aria-label', active ? 'Pausar los efectos visuales' : 'Activar los efectos visuales');
    if (!active) {
      cancelManual();
      if (stage) {
        stage.style.setProperty('--fx-px','0px');
        stage.style.setProperty('--fx-py','0px');
      }
    }
    syncCinematic();
    syncEvidence();
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
    clearTimeout(revealTimer);
    revealTimer = window.setTimeout(() => {
      entries.forEach(x => {
        if (!x.classList.contains('is-visible')) {
          x.classList.add('reveal-fallback');
          x.classList.add('is-visible');
        }
      });
    }, 6500);
  }
  refreshMotion();

  function cancelManual() { manualAnimations.forEach(animation => animation.cancel()); manualAnimations = []; }
  function runReplay() {
    if (prefersReduced.matches && !userOptIn) {
      userOptIn = true;
      try { sessionStorage.setItem('criterio-motion-opt-in', 'yes'); } catch (_) {}
    }
    active = true;
    manualPreference = 'on';
    try { sessionStorage.setItem('criterio-motion-setting','on'); } catch (_) {}
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
  motionToggle.addEventListener('click', () => {
    active = !active;
    manualPreference = active ? 'on' : 'off';
    userOptIn = active && prefersReduced.matches;
    try {
      sessionStorage.setItem('criterio-motion-opt-in', userOptIn ? 'yes' : 'no');
      sessionStorage.setItem('criterio-motion-setting', manualPreference);
    } catch (_) {}
    refreshMotion();
  });
  replay.addEventListener('click', runReplay);
  if (prefersReduced.addEventListener) prefersReduced.addEventListener('change', () => {
    if (!manualPreference && !userOptIn) { active = !prefersReduced.matches; refreshMotion(); }
  });

  // Visibility handling is independent from motion preference; no extra animation controller.
  const syncPageVisibility = () => {
    root.classList.toggle('visibility-paused', document.hidden);
  };
  document.addEventListener('visibilitychange', syncPageVisibility);
  addEventListener('pagehide', () => root.classList.add('visibility-paused'));
  addEventListener('pageshow', syncPageVisibility);
  syncPageVisibility();

  // Fine pointer: bounded parallax on decorative hero geometry (never paragraphs).
  // Touch has native :active feedback; no pointer tracking on coarse input.
  if (stage) {
    const commitPointer = () => {
      pointerPending = false;
      if (!queuedPointer || !active || !finePointer.matches || document.hidden) return;
      stage.style.setProperty('--fx-px', queuedPointer.x.toFixed(2) + 'px');
      stage.style.setProperty('--fx-py', queuedPointer.y.toFixed(2) + 'px');
    };
    visual.addEventListener('pointermove', event => {
      if (!active || !finePointer.matches || document.hidden) return;
      const r=visual.getBoundingClientRect();
      queuedPointer = {x:((event.clientX-r.left)/r.width-.5)*24, y:((event.clientY-r.top)/r.height-.5)*20};
      if (!pointerPending) {pointerPending = true; requestAnimationFrame(commitPointer);}
    },{passive:true});
    visual.addEventListener('pointerleave', () => {
      queuedPointer = null;
      stage.style.setProperty('--fx-px','0px');
      stage.style.setProperty('--fx-py','0px');
    });
    // Weak motion on mobile is still visible via timed CSS, not pointer tracking.
  }
  function syncVisualProgress() {
    if (!active || document.hidden) return;
    // Clamp 0..1 and only update an active artwork. No DOM writes to layout dimensions.
    const h=innerHeight||1;
    const sections=[visual,...lightScenes];
    sections.forEach((el)=>{
      const rect=el.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > h) return;
      const progress=Math.max(-1,Math.min(1,((rect.top+rect.height/2)-h/2)/h));
      el.style.setProperty('--fx-depth', progress.toFixed(3));
    });
  }
  const observeHero = 'IntersectionObserver' in window ? new IntersectionObserver(changes => {
    changes.forEach(c => {visual.classList.toggle('is-paused', !c.isIntersecting);band.classList.toggle('is-paused', !c.isIntersecting);});
  },{threshold:0}) : null;
  if(observeHero) observeHero.observe(hero);

  const update = () => {
    rafPending = false;
    syncVisualProgress();
    const length = Math.max(0, document.documentElement.scrollHeight - innerHeight);
    progress.style.width = (length ? Math.min(100, (scrollY / length) * 100) : 0) + '%';
    if (header) header.classList.toggle('is-scrolled', scrollY > 18);
    let chapter = '00';
    for (const section of chapters) if (section.getBoundingClientRect().top < innerHeight * .35) chapter = section.dataset.chapter;
    if (hudChapter) hudChapter.textContent = chapter;
    if (mobileChapter) mobileChapter.textContent = chapter;
    toggle.setAttribute('aria-label', (menu.classList.contains('is-open') ? 'Cerrar navegación' : 'Abrir navegación') + ', capítulo ' + chapter + ' ' + (chapterLabels[chapter] || '')); 
    chapters.forEach(section => section.classList.toggle('chapter-active',section.dataset.chapter === chapter));
    if (interlude) { const rect=interlude.getBoundingClientRect(); interlude.classList.toggle('is-paused', rect.bottom<0 || rect.top>innerHeight); }
    if (archiveSection && dossierItems.length) {
      const archiveRect = archiveSection.getBoundingClientRect();
      if (archiveRect.top < innerHeight * .72 && archiveRect.bottom > innerHeight * .18) {
        const line = innerHeight * .46;
        let best = null;
        let distance = Infinity;
        for (const item of dossierItems) {
          const rect = item.getBoundingClientRect();
          const d = rect.top <= line && rect.bottom >= line ? 0 : Math.min(Math.abs(rect.top-line),Math.abs(rect.bottom-line));
          if (d < distance) { best=item; distance=d; }
        }
        if (best) selectDossier(best.dataset.case);
      }
    }

    menu.querySelectorAll('a[href^="#"]').forEach(anchor => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target?.dataset.chapter === chapter) anchor.setAttribute('aria-current','location');
      else anchor.removeAttribute('aria-current');
    });
  };
  const scheduleUpdate = () => {if (!rafPending) {rafPending = true;requestAnimationFrame(update);}};
  addEventListener('scroll', scheduleUpdate,{passive:true});addEventListener('resize',scheduleUpdate,{passive:true});scheduleUpdate();
  addEventListener('pageshow', scheduleUpdate);
  addEventListener('load', scheduleUpdate);
  window.addEventListener('beforeprint', () => { cancelManual();entries.forEach(x=>x.classList.add('is-visible')); });
})();
