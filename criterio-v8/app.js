/** CRITERIO V8 — accessible motion director, native scroll, no dependencies. */
(()=>{'use strict';
 const root=document.documentElement,nav=document.querySelector('#site-nav'),menuBtn=document.querySelector('#menu-toggle'),fxBtn=document.querySelector('#motion-toggle'),progress=document.querySelector('#progress-bar');
 root.classList.add('has-js');
 const media=matchMedia('(prefers-reduced-motion: reduce)');
 let manual=null;try{manual=sessionStorage.getItem('criterio-v8-motion');}catch(_){}
 let active=manual==='off'?false:manual==='on'?true:!media.matches;
 let framePending=false;
 const moving=[document.querySelector('.hero-composition'),document.querySelector('.contact-slash')];
 const targets=[...document.querySelectorAll('.scene-target')];targets.forEach(x=>x.setAttribute('data-reveal',''));
 function stopMenu(){nav.classList.remove('is-open');menuBtn.setAttribute('aria-expanded','false');menuBtn.setAttribute('aria-label','Abrir menú de navegación');}
 function setMotion(){root.dataset.motion=active?'on':'off';fxBtn.textContent=active?'FX ON':'FX OFF';fxBtn.setAttribute('aria-pressed',String(active));fxBtn.setAttribute('aria-label',active?'Pausar efectos visuales':'Activar efectos visuales');if(!active){moving[0]?.style.setProperty('--layer','0px');moving[1]?.style.setProperty('--contact-depth','0px');targets.forEach(el=>el.classList.add('is-visible'));}else updateScroll();}
 fxBtn.addEventListener('click',()=>{active=!active;manual=active?'on':'off';try{sessionStorage.setItem('criterio-v8-motion',manual);}catch(_){}setMotion()});
 const matchChange=()=>{if(manual===null){active=!media.matches;setMotion()}};
 if(media.addEventListener)media.addEventListener('change',matchChange);
 menuBtn.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');menuBtn.setAttribute('aria-expanded',String(open));menuBtn.setAttribute('aria-label',open?'Cerrar menú de navegación':'Abrir menú de navegación')});
 nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',stopMenu));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('is-open')){stopMenu();menuBtn.focus()}});
 document.addEventListener('pointerdown',e=>{if(!nav.contains(e.target)&&!menuBtn.contains(e.target))stopMenu()});
 addEventListener('resize',()=>{if(innerWidth>1110)stopMenu();scheduleUpdate()},{passive:true});
 const reveal='IntersectionObserver'in window?new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');reveal.unobserve(e.target)}})},{rootMargin:'0px 0px -40px 0px',threshold:.03}):null;
 targets.forEach(el=>{if(reveal)reveal.observe(el);else el.classList.add('is-visible')});setTimeout(()=>targets.forEach(el=>el.classList.add('is-visible')),8000);
 const sections=[...document.querySelectorAll('[data-section]')];
 function updateScroll(){framePending=false;const max=Math.max(0,document.documentElement.scrollHeight-innerHeight);progress.style.width=(max?Math.min(100,Math.max(0,scrollY/max*100)):0)+'%';let chapter='';for(const s of sections)if(s.getBoundingClientRect().top<innerHeight*.36)chapter=s.dataset.section;
 nav.querySelectorAll('a').forEach(a=>{let target=document.querySelector(a.getAttribute('href'));if(target?.dataset.section===chapter)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
 if(active&&!document.hidden&&!media.matches||active&&!document.hidden&&manual==='on'){const hero=document.querySelector('.hero').getBoundingClientRect(),contact=document.querySelector('.contact').getBoundingClientRect();if(hero.bottom>0&&hero.top<innerHeight){const t=Math.max(-35,Math.min(35,-hero.top*.07));moving[0]?.style.setProperty('--layer',t+'px')}if(contact.bottom>0&&contact.top<innerHeight){moving[1]?.style.setProperty('--contact-depth',Math.max(-30,Math.min(30,(innerHeight-contact.top)*.06))+'px')}}
 }
 function scheduleUpdate(){if(!framePending){framePending=true;requestAnimationFrame(updateScroll)}};
 addEventListener('scroll',scheduleUpdate,{passive:true});addEventListener('resize',scheduleUpdate,{passive:true});document.addEventListener('visibilitychange',()=>{root.classList.toggle('tab-hidden',document.hidden)});
 document.addEventListener('click',e=>{const anchor=e.target.closest('a[href^="#"]');if(!anchor)return;const id=anchor.getAttribute('href');if(id.length<2)return;const target=document.querySelector(id);if(!target)return;target.setAttribute('tabindex','-1');const focusIt=()=>{try{target.focus({preventScroll:true})}catch(_){target.focus()}};setTimeout(focusIt,420)});
 root.classList.toggle('tab-hidden',document.hidden);setMotion();scheduleUpdate();window.addEventListener('beforeprint',()=>targets.forEach(x=>x.classList.add('is-visible')));
})();