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

(function(){
  var tabs=[].slice.call(document.querySelectorAll('.sub-tab')), panels=[].slice.call(document.querySelectorAll('.panel')), f=document.getElementById('filter');
  window.openOffre=function(k){
    var all=!k||!document.querySelector('.panel[data-panel="'+k+'"]');
    tabs.forEach(function(t){var on=t.dataset.tab===k;t.classList.toggle('on',on);t.setAttribute('aria-selected',on?'true':'false');});
    panels.forEach(function(p){p.hidden=!all&&p.dataset.panel!==k; if(!p.hidden){var d=p.querySelector('[data-reveal]'); if(d) d.classList.add('is-in');}});
    if(f){f.value='';filter();}
  };
  function filter(){
    var q=f.value.trim().toLowerCase();
    panels.forEach(function(p){ if(p.hidden) return; var n=0;
      p.querySelectorAll('.doc').forEach(function(d){var ok=!q||d.dataset.text.indexOf(q)>-1; d.style.display=ok?'':'none'; if(ok)n++;});
      p.querySelector('.empty').hidden=n>0; var pg=p.querySelector('.pager'); if(pg) pg.style.display=q?'none':''; });
  }
  if(f) f.addEventListener('input',filter);
})();

(function(){
  var IMG={"panel": "assets/img/conference-nationale.jpg", "sc": "assets/img/service-civique.jpg", "jap": "assets/img/cooperation-japon.jpg", "afd": "assets/img/cooperation-afd.jpg", "min": "assets/img/ministre.jpg", "seal": "assets/img/sceau-mauritanie.svg"}, INDEX=[{"t": "Le Ministère", "r": "a-propos", "c": "Rubrique"}, {"t": "Présentation", "r": "a-propos", "c": "Le Ministère"}, {"t": "Le Ministre", "r": "ministre", "c": "Le Ministère"}, {"t": "Cabinet du Ministre", "r": "cabinet", "c": "Le Ministère"}, {"t": "Le Secrétariat Général", "r": "secretariat", "c": "Le Ministère"}, {"t": "Directions centrales", "r": "directions", "c": "Le Ministère"}, {"t": "Établissements sous tutelle", "r": "etablissements", "c": "Le Ministère"}, {"t": "Jeunesse", "r": "jeunesse", "c": "Domaine"}, {"t": "Autonomisation des jeunes", "r": "jeunesse", "c": "Jeunesse"}, {"t": "Renforcement des capacités", "r": "jeunesse", "c": "Jeunesse"}, {"t": "Associations et réseaux de jeunesse", "r": "jeunesse", "c": "Jeunesse"}, {"t": "Espaces et maisons des jeunes", "r": "jeunesse", "c": "Jeunesse"}, {"t": "Emploi", "r": "emploi", "c": "Domaine"}, {"t": "Stratégie Nationale de l’Emploi", "r": "emploi", "c": "Emploi"}, {"t": "Coordination de Projets Emploi", "r": "emploi", "c": "Emploi"}, {"t": "Agence TECHGHIL", "r": "emploi", "c": "Emploi"}, {"t": "Permis de travail", "r": "emploi", "c": "Emploi"}, {"t": "Documents", "r": "emploi", "c": "Emploi"}, {"t": "Sports", "r": "sports", "c": "Domaine"}, {"t": "Sport de compétition", "r": "sports", "c": "Sports"}, {"t": "Sport de masse", "r": "sports", "c": "Sports"}, {"t": "Fédérations et clubs sportifs", "r": "sports", "c": "Sports"}, {"t": "Infrastructures sportives", "r": "sports", "c": "Sports"}, {"t": "Service civique", "r": "service-civique", "c": "Domaine"}, {"t": "Service civique volontaire", "r": "service-civique", "c": "Service civique"}, {"t": "Service civique obligatoire", "r": "service-civique", "c": "Service civique"}, {"t": "Programmes", "r": "programmes", "c": "Rubrique"}, {"t": "Programmes", "r": "programmes", "c": "Programmes"}, {"t": "Projets", "r": "projets", "c": "Programmes"}, {"t": "Actualités", "r": "actualites", "c": "Rubrique"}, {"t": "Toutes les actualités", "r": "actualites", "c": "Actualités"}, {"t": "Photos et vidéos", "r": "medias", "c": "Actualités"}, {"t": "Appels d’offres", "r": "offres", "c": "Rubrique"}, {"t": "Tout voir", "r": "offres", "c": "Appels d’offres"}, {"t": "Annonces", "r": "offres-annonces", "c": "Appels d’offres"}, {"t": "Appels d’offres", "r": "offres-appels", "c": "Appels d’offres"}, {"t": "Contrats", "r": "offres-contrats", "c": "Appels d’offres"}, {"t": "Contact", "r": "contact", "c": "Rubrique"}, {"t": "La jeunesse au cœur du dialogue national.", "r": "article-1", "c": "Actualité"}, {"t": "Le Ministre reçoit l’ambassadeur de l’Empire du Japon en Mauritanie", "r": "article-2", "c": "Actualité"}, {"t": "Le Ministre reçoit le Directeur de l’Agence française de Développement (AFD) en Mauritanie", "r": "article-3", "c": "Actualité"}, {"t": "300 volontaires : une nouvelle promotion engagée", "r": "article-4", "c": "Actualité"}, {"t": "Le Ministre reçoit l’ambassadeur de Chine", "r": "article-5", "c": "Actualité"}, {"t": "PAA 2025", "r": "document", "c": "Document"}, {"t": "Avis d’appel à candidature interne", "r": "document", "c": "Document"}, {"t": "La phase nationale de la Conférence nationale de l’autonomisation des jeunes", "r": "document", "c": "Document"}, {"t": "Lancement d’un appel à candidatures pour le Prix du Président de la République pour les meilleures actions de volontariat au titre de l’année 2025", "r": "document", "c": "Document"}, {"t": "Avis à toutes les associations de jeunesse", "r": "document", "c": "Document"}, {"t": "Mobilisation de 50 bénévoles pour la caravane de Bénévolat et de Citoyenneté", "r": "document", "c": "Document"}, {"t": "Appel à candidature pour la mobilisation d’un volontaire national technicien en élevage", "r": "document", "c": "Document"}, {"t": "Appel à candidature pour la mobilisation de 02 volontaires nationaux assistants en gestion et suivi des projets", "r": "document", "c": "Document"}, {"t": "Appel à candidature pour la mobilisation d’un volontaire national technicien en agriculture", "r": "document", "c": "Document"}, {"t": "Lancement d’un appel à candidature pour la mobilisation de 06 volontaires nationaux en qualité d’agents de développement local", "r": "document", "c": "Document"}, {"t": "Plan Annuel d’Achats 2026", "r": "document", "c": "Document"}, {"t": "Avis d’appel à candidature", "r": "document", "c": "Document"}, {"t": "Marché d’acquisition de matériels d’équipement des espaces et maisons des jeunes", "r": "document", "c": "Document"}, {"t": "Avis d’appel d’offres", "r": "document", "c": "Document"}, {"t": "Plan de Passation des Marchés 2025", "r": "document", "c": "Document"}, {"t": "Appel d’offres pour la réalisation de travaux d’aménagement de dix (10) terrains de football", "r": "document", "c": "Document"}, {"t": "Avis à manifestation d’intérêt", "r": "document", "c": "Document"}, {"t": "Avis d’appel d’offres pour l’acquisition de quatre (04) véhicules 4x4 double cabine, en un lot unique et indivisible", "r": "document", "c": "Document"}, {"t": "Marché de développement de la plateforme tripartite Techghil", "r": "document", "c": "Document"}, {"t": "Marché d’élaboration du référentiel des métiers", "r": "document", "c": "Document"}, {"t": "Marché d’acquisition de véhicules Techghil", "r": "document", "c": "Document"}, {"t": "Consultant pour la création et l’aménagement PNDJSL", "r": "document", "c": "Document"}, {"t": "Contrat N° 1911 PNDJSL 2024", "r": "document", "c": "Document"}, {"t": "Mon Projet, Mon Avenir", "r": "programmes", "c": "Programme"}, {"t": "MEHENTI", "r": "programmes", "c": "Programme"}, {"t": "Projet d’appui à l’employabilité des jeunes vulnérables en Mauritanie", "r": "projets", "c": "Projet"}, {"t": "Projet d’appui à l’employabilité et à l’insertion socio-économique des jeunes vulnérables dans la wilaya du Brakna", "r": "projets", "c": "Projet"}, {"t": "Promouvoir des emplois et d’autres moyens de subsistance respectueux de l’environnement", "r": "projets", "c": "Projet"}];
  document.querySelectorAll('img[data-img]').forEach(function(im){ if(IMG[im.dataset.img]) im.src=IMG[im.dataset.img]; });
  var icon=document.querySelector('link[rel=icon]'); if(icon) icon.href=IMG.seal;
  var routes={}; document.querySelectorAll('.route').forEach(function(s){routes[s.dataset.route]=s;});
  var MENUMAP={'accueil':'accueil','a-propos':'ministere','ministre':'ministere','cabinet':'ministere','secretariat':'ministere','directions':'ministere','etablissements':'ministere','jeunesse':'domaines','emploi':'domaines','sports':'domaines','service-civique':'domaines','programmes':'programmes','projets':'programmes','actualites':'actualites','medias':'actualites','offres':'offres','document':'offres','contact':'contact'};
  var header=document.querySelector('.site-header'), burger=document.querySelector('.burger'), current=null;
  document.querySelectorAll('.main-nav a').forEach(function(a){a.addEventListener('click',function(){ if(window.innerWidth>1240){ header.classList.add('nav-closing'); if(document.activeElement) document.activeElement.blur(); } });});
  document.querySelectorAll('.nav-link').forEach(function(l){ l.addEventListener('mouseenter',function(){ header.classList.remove('nav-closing'); }); l.addEventListener('focus',function(){ header.classList.remove('nav-closing'); }); });
  function show(name, anchor){
    var r=name; if(/^article-/.test(r)) r=r; 
    var tab=null; var m=/^offres-(annonces|appels|contrats)$/.exec(r); if(m){tab=m[1]; r='offres';}
    if(!routes[r]){ var el=document.getElementById(name); var host=el&&el.closest('.route'); if(host){ r=host.dataset.route; anchor=el; } else r='accueil'; }
    if(current!==r){
      Object.keys(routes).forEach(function(k){routes[k].hidden=k!==r;});
      current=r;
      routes[r].querySelectorAll('[data-reveal]').forEach(function(x){ x.classList.remove('is-in'); });
      requestAnimationFrame(function(){ routes[r].querySelectorAll('[data-reveal]').forEach(function(x){ var b=x.getBoundingClientRect(); if(b.top<innerHeight) x.classList.add('is-in'); else revealIO.observe(x); }); });
    }
    var mk=/^article-/.test(r)?'actualites':(MENUMAP[r]||'');
    document.querySelectorAll('.nav-item').forEach(function(n){n.classList.toggle('is-active',n.dataset.menu===mk);});
    document.title=(routes[r].dataset.title||'')+' – Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique';
    if(r==='offres' && window.openOffre) window.openOffre(tab);
    header.classList.remove('menu-open'); burger.setAttribute('aria-expanded','false');
    if(anchor){ setTimeout(function(){anchor.scrollIntoView({behavior:'smooth'});},60); }
    else window.scrollTo({top:0});
  }
  var revealIO=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');revealIO.unobserve(e.target);}});},{threshold:.08});
  function route(){ var h=decodeURIComponent(location.hash.slice(1))||'accueil'; show(h); }
  window.addEventListener('hashchange',route);
  route();
  // filtres actualités
  document.querySelectorAll('.cf').forEach(function(b){b.addEventListener('click',function(){var c=b.dataset.cat;document.querySelectorAll('.cf').forEach(function(x){x.classList.toggle('on',x===b);});document.querySelectorAll('#newsgrid .ncard').forEach(function(n){n.style.display=(c==='Toutes'||n.dataset.cat===c)?'':'none';});});});
  // copier le lien
  document.querySelectorAll('.sh.copy').forEach(function(b){b.addEventListener('click',function(){try{navigator.clipboard.writeText(location.href);}catch(e){} b.classList.add('done');setTimeout(function(){b.classList.remove('done');},1600);});});
  document.querySelectorAll('a.sh[href="#"], a[href="#"]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();});});
  // galerie
  var lb=document.querySelector('.lightbox');
  document.querySelectorAll('.ph').forEach(function(p){p.addEventListener('click',function(){lb.querySelector('img').src=IMG[p.dataset.full];lb.querySelector('p').textContent=p.querySelector('span').textContent;lb.hidden=false;lb.querySelector('.lb-x').focus();});});
  lb.querySelector('.lb-x').addEventListener('click',function(){lb.hidden=true;});
  lb.addEventListener('click',function(e){if(e.target===lb)lb.hidden=true;});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.hidden=true;});
  // recherche
  function search(q){
    q=(q||'').trim(); var box=document.getElementById('results'); document.getElementById('sq').value=q;
    document.getElementById('q-label').textContent=q?('« '+q+' »'):'';
    var ql=q.toLowerCase(), res=INDEX.filter(function(x){return ql && (x.t.toLowerCase().indexOf(ql)>-1 || x.c.toLowerCase().indexOf(ql)>-1);});
    box.innerHTML=res.length?res.map(function(x){return '<a class="res" href="#'+x.r+'"><span><small>'+x.c+'</small><b>'+x.t+'</b></span><span aria-hidden="true">→</span></a>';}).join(''):'<p class="muted">'+(q?'Aucun résultat pour cette recherche.':'Saisissez un mot-clé.')+'</p>';
  }
  function goSearch(q){ if(location.hash!=='#recherche') location.hash='recherche'; setTimeout(function(){search(q);},30); }
  var sb=document.querySelector('.s-btn'), sp=document.getElementById('search-panel');
  sb.addEventListener('click',function(){ var o=sp.hidden; sp.hidden=!o; sb.setAttribute('aria-expanded',o?'true':'false'); if(o) setTimeout(function(){document.getElementById('hs').focus();},50); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && !sp.hidden){ sp.hidden=true; sb.setAttribute('aria-expanded','false'); sb.focus(); } });
  document.getElementById('hsf').addEventListener('submit',function(){ sp.hidden=true; sb.setAttribute('aria-expanded','false'); });
  document.getElementById('hsf').addEventListener('submit',function(e){e.preventDefault();goSearch(document.getElementById('hs').value);});
  document.getElementById('sf').addEventListener('submit',function(e){e.preventDefault();search(document.getElementById('sq').value);});
  document.getElementById('sq').addEventListener('input',function(){search(this.value);});
  var heroForm=document.querySelector('.hero form'); if(heroForm) heroForm.addEventListener('submit',function(e){e.preventDefault();goSearch(heroForm.querySelector('input').value);});
})();
