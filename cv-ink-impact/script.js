(() => {
  'use strict';
  const nav = document.getElementById('nav');
  const toggle = document.getElementById('menu-toggle');
  const progress = document.getElementById('progress');
  const closeMenu = () => {nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');};
  toggle.addEventListener('click',() => { const open = nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open)); });
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('keydown',e=>{if(e.key==='Escape' && nav.classList.contains('open')){closeMenu();toggle.focus();}});
  document.addEventListener('click',e=>{if(!nav.contains(e.target)&&!toggle.contains(e.target))closeMenu();});
  const updateProgress = () => {const d=document.documentElement.scrollHeight-innerHeight;progress.style.width = (d>0?Math.min(100,scrollY/d*100):0)+'%';};
  addEventListener('scroll',updateProgress,{passive:true});addEventListener('resize',updateProgress,{passive:true});updateProgress();
  document.getElementById('print-btn').addEventListener('click',()=>print());
})();
