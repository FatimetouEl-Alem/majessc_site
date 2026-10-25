
(function(){
  // Révélation au défilement
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{threshold:.12});
  document.querySelectorAll('[data-reveal]').forEach(function(el){io.observe(el);});

  // Compteurs animés
  function countUp(el){
    var target=parseInt(el.dataset.count,10),start=null,dur=1600;
    function fmt(n){return n.toLocaleString('fr-FR').replace(/\u202f|\u00a0/g,' ');}
    function step(t){if(!start)start=t;var p=Math.min((t-start)/dur,1);var e=1-Math.pow(1-p,3);el.textContent=fmt(Math.round(target*e));if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  }
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-count]').forEach(function(el){ if(!reduce) setTimeout(function(){countUp(el);},700); });

  // Onglets
  document.querySelectorAll('.tab').forEach(function(b){
    b.addEventListener('click',function(){
      var g=b.dataset.group,i=b.dataset.i;
      document.querySelectorAll('.tab[data-group="'+g+'"]').forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false');});
      document.querySelectorAll('.tabpanel[data-group="'+g+'"]').forEach(function(p){p.hidden=p.dataset.i!==i;});
    });
  });

  // Accordéon
  document.querySelectorAll('.acc-head').forEach(function(h){
    h.addEventListener('click',function(){
      var a=h.parentNode,open=!a.classList.contains('is-open');
      document.querySelectorAll('.acc[data-acc="'+a.dataset.acc+'"]').forEach(function(x){x.classList.remove('is-open');x.querySelector('.acc-head').setAttribute('aria-expanded','false');});
      if(open){a.classList.add('is-open');h.setAttribute('aria-expanded','true');}
    });
  });
})();
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header=document.querySelector('.site-header'), top=document.querySelector('.to-top'), heroImg=document.querySelector('.hero img[aria-hidden]');
  var ticking=false;
  function onScroll(){
    var y=window.scrollY;
    header.classList.toggle('is-scrolled',y>40);
    top.classList.toggle('show',y>700);
    if(heroImg && !reduce && y<900){ heroImg.style.translate='0 '+(y*0.25)+'px'; }
    ticking=false;
  }
  window.addEventListener('scroll',function(){ if(!ticking){requestAnimationFrame(onScroll);ticking=true;} },{passive:true});
  top.addEventListener('click',function(){window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});});
  var burger=document.querySelector('.burger');
  burger.addEventListener('click',function(){var o=header.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o?'true':'false');burger.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');});
  document.querySelectorAll('.main-nav a').forEach(function(a){a.addEventListener('click',function(){header.classList.remove('menu-open');burger.setAttribute('aria-expanded','false');});});
  document.querySelectorAll('[data-reveal]').forEach(function(sec){
    sec.querySelectorAll('[data-stg]').forEach(function(el,i){el.style.transitionDelay=(Math.min(i,10)*70+150)+'ms';});
  });
  var row=document.querySelector('.np-row'); if(!row) return;
  var panels=[].slice.call(row.querySelectorAll('.np')), DUR=6000, timer=null, paused=reduce, idx=0, hover=false;
  var btn=document.querySelector('.nc-play');
  row.style.setProperty('--dur',DUR+'ms');
  function run(){ var p=panels[idx]; p.classList.remove('is-running'); void p.offsetWidth; if(!paused) p.classList.add('is-running'); }
  function schedule(){ clearTimeout(timer); if(!paused && !hover) timer=setTimeout(function(){show(idx+1);},DUR); }
  function show(i){
    idx=(i+panels.length)%panels.length;
    panels.forEach(function(p,k){var on=k===idx;p.classList.toggle('is-open',on);if(!on)p.classList.remove('is-running');p.setAttribute('aria-expanded',on?'true':'false');});
    run(); schedule();
  }
  function setPaused(p){
    paused=p; btn.setAttribute('aria-pressed',p?'true':'false'); btn.setAttribute('aria-label',p?'Reprendre le défilement':'Mettre en pause le défilement');
    row.classList.toggle('is-paused',p);
    if(p){clearTimeout(timer);} else {run(); schedule();}
  }
  panels.forEach(function(p,k){
    p.addEventListener('click',function(){ if(k!==idx) show(k); });
    p.addEventListener('keydown',function(e){ if((e.key==='Enter'||e.key===' ')&&k!==idx){e.preventDefault();show(k);} });
  });
  document.querySelector('.nc[data-act="prev"]').addEventListener('click',function(){show(idx-1);});
  document.querySelector('.nc[data-act="next"]').addEventListener('click',function(){show(idx+1);});
  btn.addEventListener('click',function(){setPaused(!paused);});
  row.addEventListener('mouseenter',function(){hover=true; if(!paused){clearTimeout(timer);row.classList.add('is-paused');}});
  row.addEventListener('mouseleave',function(){hover=false; if(!paused){row.classList.remove('is-paused');run();schedule();}});
  document.addEventListener('visibilitychange',function(){ if(document.hidden) clearTimeout(timer); else schedule(); });
  if(reduce){ setPaused(true); } else { show(0); }
})();
