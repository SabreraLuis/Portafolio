/* INK / IMPACT V5 — integrated progressive-enhancement controller.
 * Motion never owns layout, focus or scroll. Page is fully readable without JS.
 */
(() => {
  'use strict';
  const doc = document.documentElement;
  const nav = document.getElementById('nav');
  const toggle = document.getElementById('menu-toggle');
  const progress = document.getElementById('read-progress-bar');
  const motionButton = document.getElementById('motion-toggle');
  const announcer = document.getElementById('announcer');
  const chapterNumber = document.getElementById('chapter-number');
  const sections = [...document.querySelectorAll('[data-chapter]')];
  const reduceQuery = matchMedia('(prefers-reduced-motion: reduce)');
  let userMotion = true;
  try { userMotion = sessionStorage.getItem('ink-v5-motion') !== 'off'; } catch(_) {}
  const canMove = () => userMotion && !reduceQuery.matches;
  const announce = message => { announcer.textContent = ''; requestAnimationFrame(() => announcer.textContent = message); };

  const closeMenu = () => { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); };
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); toggle.focus(); }
  });
  document.addEventListener('pointerdown', event => {
    if (!toggle.contains(event.target) && !nav.contains(event.target)) closeMenu();
  });

  const revealed = [...document.querySelectorAll('[data-reveal]')];
  let revealObserver;
  function syncMotion() {
    const enabled = canMove();
    doc.classList.toggle('motion-off', !enabled);
    doc.classList.toggle('motion-ready', enabled);
    motionButton.textContent = enabled ? 'MOTION: ON' : 'MOTION: OFF';
    motionButton.setAttribute('aria-pressed', String(enabled));
    motionButton.setAttribute('aria-label', enabled ? 'Desactivar animaciones' : 'Activar animaciones');
    if (revealObserver) revealObserver.disconnect();
    // Keep essential content visible on each preference change.
    if (!enabled) { revealed.forEach(el => el.classList.add('is-visible')); return; }
    if (!('IntersectionObserver' in window)) { revealed.forEach(el => el.classList.add('is-visible')); return; }
    revealObserver = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        entry.target.classList.add('is-visible'); revealObserver.unobserve(entry.target);
      }
    }, {rootMargin:'0px 0px -40px 0px', threshold:0.08});
    revealed.forEach(el => {
      if (el.getBoundingClientRect().top < innerHeight - 35) el.classList.add('is-visible');
      else if (!el.classList.contains('is-visible')) revealObserver.observe(el);
    });
  }
  motionButton.addEventListener('click', () => {
    userMotion = !userMotion;
    try {sessionStorage.setItem('ink-v5-motion', userMotion ? 'on':'off');} catch(_) {}
    syncMotion();
    announce(canMove() ? 'Animaciones activadas' : 'Animaciones desactivadas');
  });
  if (reduceQuery.addEventListener) reduceQuery.addEventListener('change', syncMotion);
  syncMotion();

  let ticking = false;
  const updateProgress = () => {
    ticking = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    const fraction = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
    progress.style.width = (fraction * 100).toFixed(2) + '%';
  };
  addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(updateProgress); }
  }, {passive:true});
  addEventListener('resize', updateProgress, {passive:true});
  updateProgress();

  function updateChapter() {
    let chapter = '00';
    const anchor = innerHeight * .36;
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= anchor) chapter = section.dataset.chapter || chapter;
    }
    chapterNumber.textContent = chapter;
  }
  addEventListener('scroll', () => requestAnimationFrame(updateChapter), {passive:true});
  addEventListener('resize', updateChapter, {passive:true});
  updateChapter();
  document.getElementById('print-cv').addEventListener('click', () => window.print());
})();
