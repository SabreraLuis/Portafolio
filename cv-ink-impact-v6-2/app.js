/** INK / IMPACT VI — Interaction director.
 * Progressive enhancement, no scroll hijacking, no synthetic inertia, no hidden content without fallback.
 */
(() => {
  'use strict';
  const root = document.documentElement;
  const $ = (id) => document.getElementById(id);
  const menu = $('site-nav');
  const menuButton = $('menu-toggle');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const motionButton = $('motion-toggle');
  const readingButton = $('reading-toggle');
  const announcer = $('announcer');
  const viewToggle = $('view-toggle');
  const viewPanel = $('view-panel');
  const closeViewPanel = (returnFocus = false) => {
    if (viewPanel.hidden) return;
    viewPanel.hidden = true;
    viewToggle.setAttribute('aria-expanded', 'false');
    viewToggle.setAttribute('aria-label', 'Abrir opciones de visualización');
    if (returnFocus) viewToggle.focus();
  };
  viewToggle.addEventListener('click', () => {
    const opening = viewPanel.hidden;
    viewPanel.hidden = !opening;
    viewToggle.setAttribute('aria-expanded', String(opening));
    viewToggle.setAttribute('aria-label', opening ? 'Cerrar opciones de visualización' : 'Abrir opciones de visualización');
  });
  document.addEventListener('pointerdown', (event) => {
    if (!viewPanel.hidden && !event.composedPath().includes(viewToggle) && !event.composedPath().includes(viewPanel)) closeViewPanel();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !viewPanel.hidden) { event.stopPropagation(); closeViewPanel(true); }
  });

  const allScenes = [...document.querySelectorAll('[data-scene]')];
  const allReveals = [...document.querySelectorAll('[data-enter]')];
  const navAnchors = [...menu.querySelectorAll('a[href^="#"]')];
  let motionPref = 'on';
  let readingPref = 'off';
  try {
    motionPref = sessionStorage.getItem('ink-impact-v6-motion') ?? 'on';
    readingPref = sessionStorage.getItem('ink-impact-v6-reading') ?? 'off';
  } catch (_) { /* session storage may be unavailable */ }
  const activeMotion = () => motionPref === 'on' && !reduce.matches;
  const announce = (message) => { announcer.textContent = message; };
  const savePref = (key, value) => { try { sessionStorage.setItem(key, value); } catch (_) {} };
  const closeMenu = () => {
    menu.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
  };
  menuButton.addEventListener('click', () => {
    closeViewPanel();
    const isOpen = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.classList.contains('is-open')) {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener('pointerdown', event => {
    if (!menuButton.contains(event.target) && !menu.contains(event.target)) closeMenu();
  });

  let revealObserver;
  function syncMotion() {
    const moving = activeMotion();
    root.classList.toggle('motion-disabled', !moving);
    root.classList.toggle('motion-enabled', moving);
    motionButton.textContent = reduce.matches ? 'MOVIMIENTO: SISTEMA' : (moving ? 'MOVIMIENTO: ON' : 'MOVIMIENTO: OFF');
    motionButton.disabled = reduce.matches;
    motionButton.setAttribute('aria-pressed', String(moving));
    motionButton.setAttribute('aria-label', moving ? 'Desactivar efectos de movimiento' : 'Activar efectos de movimiento');
    if (revealObserver) revealObserver.disconnect();
    if (!moving || !('IntersectionObserver' in window)) {
      allReveals.forEach(el => el.classList.add('is-in'));
      return;
    }
    // Set initial visible elements before enabling the animation class.
    allReveals.forEach(el => {
      if (el.getBoundingClientRect().top <= innerHeight * .98) el.classList.add('is-in');
    });
    revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {threshold:0.07,rootMargin:'0px 0px -22px 0px'});
    allReveals.filter(el => !el.classList.contains('is-in')).forEach(el => revealObserver.observe(el));
    // Fails open for observers that never fire (e.g. backgrounded browser).
    window.setTimeout(() => { allReveals.forEach(el => el.classList.add('is-in')); revealObserver?.disconnect(); }, 13000);
  }
  motionButton.addEventListener('click', () => {
    if (reduce.matches) return;
    motionPref = motionPref === 'on' ? 'off' : 'on';
    savePref('ink-impact-v6-motion', motionPref);
    syncMotion();
    announce(activeMotion() ? 'Movimiento activado' : 'Movimiento desactivado');
  });
  if (reduce.addEventListener) reduce.addEventListener('change', syncMotion);
  syncMotion();

  function syncReading() {
    const enabled = readingPref === 'on';
    root.classList.toggle('reading-mode', enabled);
    readingButton.setAttribute('aria-pressed', String(enabled));
    readingButton.textContent = enabled ? 'VISTA EDITORIAL' : 'MODO LECTURA';
    readingButton.setAttribute('aria-label', enabled ? 'Volver a la vista editorial' : 'Mostrar vista compacta de lectura');
    // Don't pre-reveal every section on startup: this previously disabled
    // all scroll-triggered entrance motion across the entire site.
    if (enabled) allReveals.forEach(el => el.classList.add('is-in'));
    else if (activeMotion()) syncMotion();
  }
  readingButton.addEventListener('click', () => {
    readingPref = readingPref === 'on' ? 'off' : 'on';
    savePref('ink-impact-v6-reading', readingPref);
    syncReading();
    announce(readingPref === 'on' ? 'Modo lectura activado' : 'Vista editorial activada');
    scheduleHUD();
  });
  syncReading();

  const progress = $('progress-bar');
  const sceneLabel = $('scene-index');
  let scheduled = false;
  function updateHUD() {
    scheduled = false;
    const remaining = Math.max(0, document.documentElement.scrollHeight - innerHeight);
    progress.style.width = ((remaining ? scrollY / remaining : 0) * 100).toFixed(2) + '%';
    const readLine = innerHeight * .32;
    let scene = '00';
    for (const section of allScenes) {
      if (section.getBoundingClientRect().top <= readLine) scene = section.dataset.scene || scene;
    }
    sceneLabel.textContent = scene;
    document.querySelector('.header')?.classList.toggle('is-scrolled', scrollY > 24);
    navAnchors.forEach(anchor => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target && target.dataset.scene === scene) anchor.setAttribute('aria-current', 'location');
      else anchor.removeAttribute('aria-current');
    });
  }
  const scheduleHUD = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(updateHUD);
  };
  addEventListener('scroll', scheduleHUD, {passive:true});
  addEventListener('resize', scheduleHUD, {passive:true});
  scheduleHUD();

  $('print-button').addEventListener('click', () => window.print());
  const closedForPrint = [];
  window.addEventListener('beforeprint', () => {
    allReveals.forEach(el => el.classList.add('is-in'));
    document.querySelectorAll('.case-more').forEach(detail => {
      if (!detail.open) { closedForPrint.push(detail); detail.open = true; }
    });
  });
  window.addEventListener('afterprint', () => {
    closedForPrint.splice(0).forEach(detail => { detail.open = false; });
  });
})();
