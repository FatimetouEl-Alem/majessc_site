import base64, re, os
IMG=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','images')+os.sep
def uri(fn,mime): return f'data:{mime};base64,'+base64.b64encode(open(IMG+fn,'rb').read()).decode()
SEAL=uri('seal.svg','image/svg+xml')
GOLD='#E3A008'; G='#063B2C'; G2='#0B6B45'; DEEP='#052E22'; INK='#0B1F18'; MUTED='#56665F'; LINE='#E2E8E5'; SOFT='#F5F8F6'; TXT='#33443D'
def arrow(s=15,w=2.2): return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
def ico(p,s=22,w=1.8): return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
I=dict(search='<circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.5-3.5"></path>',
 doc='<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z"></path><path d="M14 3v5h5M9 13h6M9 17h4"></path>',
 mega='<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1Z"></path><path d="M15 9a4 4 0 0 1 0 6"></path>',
 folder='<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"></path>',
 pen='<path d="M4 20h4L19 9l-4-4L4 16v4Z"></path><path d="m13 7 4 4"></path>',
 users='<circle cx="8" cy="9" r="3"></circle><circle cx="16" cy="9" r="3"></circle><path d="M2 20c.8-3 3.2-5 6-5s5.2 2 6 5M14 15.2c.6-.1 1.3-.2 2-.2 2.8 0 5.2 2 6 5"></path>',
 cal='<rect x="3" y="5" width="18" height="16" rx="2.5"></rect><path d="M16 3v4M8 3v4M3 10h18"></path>',
 down='<path d="M12 4v11M7 10l5 5 5-5M5 20h14"></path>',
 eye='<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"></path><circle cx="12" cy="12" r="3"></circle>',
 chev='<path d="m6 9 6 6 6-6"></path>',
 home='<path d="M4 21V10l8-6 8 6v11"></path><path d="M9 21v-6h6v6"></path>',
 link='<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"></path><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"></path>',
 trophy='<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4ZM7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"></path>',
 briefcase='<rect x="3" y="7" width="18" height="13" rx="2.5"></rect><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"></path>')

MENU=[("À propos","accueil-majessc.html#ministere",[("Le Ministre","accueil-majessc.html#ministere"),("Cabinet du Ministre","accueil-majessc.html#ministere"),("Le Secrétariat Général","accueil-majessc.html#ministere"),("Directions centrales","accueil-majessc.html#ministere"),("Établissements sous tutelle","accueil-majessc.html#ministere")]),
("Jeunesse","#",[("Autonomisation des jeunes","#"),("Renforcement des capacités","#"),("Associations et réseaux de jeunesse","#"),("Espaces et maisons des jeunes","#")]),
("Emploi","#",[("Stratégie Nationale de l’Emploi","#"),("Coordination de Projets Emploi","#"),("Agence TECHGHIL","#"),("Permis de travail","#"),("Documents","#")]),
("Sports","#",[("Sport de compétition","#"),("Sport de masse","#"),("Fédérations et clubs sportifs","#"),("Infrastructures sportives","#")]),
("Service civique","#",[("Service civique volontaire","#"),("Service civique obligatoire","#")]),
("Programmes / Projets","#",[]),
("Centre des médias","#",[("Actualités","#"),("Photos et vidéos","accueil-majessc.html#medias")]),
("Offres et appels d’offres","offres-et-appels-doffres.html",[("Annonces","offres-et-appels-doffres.html#annonces"),("Appels d’offres","offres-et-appels-doffres.html#appels"),("Contrats","offres-et-appels-doffres.html#contrats")]),
("Contact","#contact",[])]

def header(active):
    items=''
    for t,h,sub in MENU:
        on=t==active
        cur=' aria-current="page"' if on else ''
        if sub:
            links=''.join(f'<a href="{sh}">{st}</a>' for st,sh in sub)
            items+=f'<div class="nav-item has-sub{" is-active" if on else ""}"><a href="{h}"{cur} class="nav-link">{t}<span class="chev">{ico(I["chev"],13,2.4)}</span></a><div class="sub" role="menu">{links}</div></div>'
        else:
            items+=f'<div class="nav-item{" is-active" if on else ""}"><a href="{h}"{cur} class="nav-link">{t}</a></div>'
    return f'''<div class="topbar"><div class="wrap topbar-in"><span>Site officiel · Honneur, Fraternité, Justice</span><span class="tb-right"><a href="#contact">Contact</a><span class="lang"><a href="#" class="on">FR</a><a href="#" lang="ar">عربية</a></span></span></div></div>
<header class="site-header">
  <div class="wrap head-row">
    <a href="accueil-majessc.html" class="brand"><img src="{SEAL}" alt="Sceau de la République Islamique de Mauritanie"><span class="brand-txt"><span class="b1">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</span><span class="b2">Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</span></span></a>
    <form class="head-search" role="search"><label for="hs" class="sr">Rechercher</label>{ico(I["search"],18,2)}<input id="hs" type="search" placeholder="Rechercher sur le portail…"></form>
    <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
  <nav id="menu" class="main-nav" aria-label="Navigation principale"><div class="wrap nav-in">{items}</div></nav>
  <div class="stripe" aria-hidden="true"><i style="flex:1;background:#C8102E"></i><i style="flex:13;background:{G2}"></i><i style="flex:1;background:#C8102E"></i></div>
</header>'''

def footer():
    cols=[("Le Ministère",["Le Ministre","Cabinet du Ministre","Le Secrétariat Général","Établissements sous tutelle"]),("Offres et appels d’offres",["Annonces","Appels d’offres","Contrats"]),("Centre des médias",["Actualités","Photos et vidéos"]),("Liens utiles",["Techghil","Tekwine","PEJ","Portail de la Microfinance"])]
    hrefs={"Annonces":"offres-et-appels-doffres.html#annonces","Appels d’offres":"offres-et-appels-doffres.html#appels","Contrats":"offres-et-appels-doffres.html#contrats"}
    ch=''.join(f'<nav data-stg aria-label="{t}"><span class="f-h">{t}</span>'+''.join(f'<a href="{hrefs.get(l,"#")}">{l}</a>' for l in ls)+'</nav>' for t,ls in cols)
    return f'''<footer class="site-footer" data-reveal>
  <div class="stripe" aria-hidden="true"><i style="flex:1;background:#C8102E"></i><i style="flex:6;background:{G2}"></i><i style="flex:1;background:{GOLD}"></i><i style="flex:6;background:{G2}"></i><i style="flex:1;background:#C8102E"></i></div>
  <span class="glow g1" aria-hidden="true"></span><span class="glow g2" aria-hidden="true"></span>
  <div class="wrap f-in">
    <div class="f-top"><a href="accueil-majessc.html" class="brand dark"><img src="{SEAL}" alt=""><span class="brand-txt"><span class="b1">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</span><span class="b2">Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</span></span></a><a href="accueil-majessc.html#parcours" class="btn-gold">Trouver un service {arrow(14)}</a></div>
    <div class="f-cols">{ch}</div>
    <div class="f-bottom"><span>© 2026 Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique · Nouakchott, Mauritanie</span><span class="f-legal"><a href="#">Mentions légales</a><a href="#">Accessibilité</a><a href="#">Plan du site</a></span></div>
  </div>
</footer>
<button class="to-top" aria-label="Revenir en haut de la page">{ico('<path d="M12 19V5M6 11l6-6 6 6"></path>',20,2.2)}</button>'''

CSS=f'''
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:#fff;color:{INK};font-family:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
img{{max-width:100%}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.wrap{{max-width:1280px;margin:0 auto;padding:0 32px}}
:focus-visible{{outline:2px solid {GOLD};outline-offset:3px;border-radius:6px}}
a svg{{transition:transform .25s ease}} a:hover>svg{{transform:translateX(3px)}}
section[id]{{scroll-margin-top:150px}}
/* Bandeau du haut */
.topbar{{background:{DEEP};color:#C7D8D0;font-size:12.5px}}
.topbar-in{{min-height:34px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 24px}}
.tb-right{{display:flex;align-items:center;gap:18px}} .tb-right a{{color:#C7D8D0;text-decoration:none}}
.lang{{display:flex;gap:2px;padding:2px;border-radius:7px;background:rgba(255,255,255,.08)}}
.lang a{{padding:2px 9px;border-radius:5px;color:#fff!important;font-weight:600;font-size:11.5px}}
.lang a.on{{background:#fff;color:{DEEP}!important;font-weight:800}}
.lang a[lang=ar]{{font-family:'Noto Kufi Arabic',sans-serif}}
/* En-tête */
.site-header{{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.97);backdrop-filter:blur(10px);transition:box-shadow .3s}}
.site-header.is-scrolled{{box-shadow:0 10px 30px rgba(5,46,34,.10)}}
.head-row{{display:flex;align-items:center;justify-content:space-between;gap:16px 32px;min-height:78px}}
.brand{{display:flex;align-items:center;gap:14px;text-decoration:none}}
.brand img{{width:52px;height:52px;flex:none}}
.brand-txt{{display:flex;flex-direction:column;gap:3px;padding-left:14px;border-left:1px solid {LINE}}}
.brand .b1{{font-size:10.5px;font-weight:800;letter-spacing:.12em;color:{MUTED}}}
.brand .b2{{font-size:13.5px;line-height:1.3;font-weight:800;color:{INK};max-width:380px}}
.brand.dark img{{width:64px;height:64px}} .brand.dark .brand-txt{{border-color:rgba(255,255,255,.18)}} .brand.dark .b1{{color:#9DB8AC}} .brand.dark .b2{{color:#fff;font-size:15px;max-width:440px}}
.head-search{{flex:0 1 340px;display:flex;align-items:center;gap:10px;height:46px;padding:0 16px;border-radius:999px;border:1px solid {LINE};background:{SOFT};color:{MUTED};transition:border-color .2s,background .2s}}
.head-search:focus-within{{border-color:{G2};background:#fff}}
.head-search input{{flex:1;min-width:0;border:0;outline:0;background:transparent;font:inherit;font-size:14.5px;color:{INK}}}
.main-nav{{border-top:1px solid {LINE}}}
.nav-in{{display:flex;flex-wrap:nowrap;justify-content:space-between;gap:0 6px}}
.nav-item{{position:relative}}
.nav-link{{display:flex;align-items:center;gap:4px;min-height:54px;padding:0 2px;font-size:14px;font-weight:650;color:#1B2B25;text-decoration:none;position:relative;white-space:nowrap}}
.nav-link::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;border-radius:3px 3px 0 0;background:{GOLD};transform:scaleX(0);transform-origin:left;transition:transform .3s ease}}
.nav-item:hover .nav-link::after,.nav-item:focus-within .nav-link::after,.nav-item.is-active .nav-link::after{{transform:scaleX(1)}}
.nav-item.is-active .nav-link{{color:{G};font-weight:800}}
.chev{{display:inline-flex;color:{MUTED};transition:transform .3s}}
.nav-item:hover .chev,.nav-item:focus-within .chev{{transform:rotate(180deg)}}
.sub{{position:absolute;top:100%;left:-14px;min-width:250px;padding:10px;border-radius:18px;background:#fff;box-shadow:0 24px 60px rgba(5,46,34,.18);border:1px solid {LINE};opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .25s,transform .25s,visibility .25s;z-index:60}}
.nav-item:last-child .sub,.nav-item:nth-last-child(2) .sub{{left:auto;right:-14px}}
.nav-item:hover .sub,.nav-item:focus-within .sub{{opacity:1;visibility:visible;transform:none}}
.sub a{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:11px 14px;border-radius:12px;font-size:14px;font-weight:600;color:{INK};text-decoration:none;transition:background .2s,color .2s}}
.sub a::after{{content:"→";color:{GOLD};opacity:0;transform:translateX(-6px);transition:all .2s}}
.sub a:hover{{background:{SOFT};color:{G}}} .sub a:hover::after{{opacity:1;transform:none}}
.stripe{{height:3px;display:flex}} .stripe i{{display:block}}
.burger{{display:none;width:46px;height:46px;border-radius:12px;border:1px solid {LINE};background:#fff;cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:5px;flex:none}}
.burger span{{display:block;width:20px;height:2px;border-radius:2px;background:{G};transition:transform .3s,opacity .3s}}
.site-header.menu-open .burger span:nth-child(1){{transform:translateY(7px) rotate(45deg)}}
.site-header.menu-open .burger span:nth-child(2){{opacity:0}}
.site-header.menu-open .burger span:nth-child(3){{transform:translateY(-7px) rotate(-45deg)}}
/* Commun */
.kicker{{display:inline-flex;align-items:center;gap:10px;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:{G2}}}
.kicker::before{{content:"";width:24px;height:2px;background:currentColor;transition:width .8s .2s ease}}
.btn-gold{{height:48px;padding:0 20px;border-radius:999px;background:{GOLD};color:{DEEP};font-weight:800;font-size:14px;display:inline-flex;align-items:center;gap:8px;text-decoration:none;transition:filter .2s,transform .2s}}
.btn-gold:hover{{filter:brightness(1.06);transform:translateY(-2px)}}
.btn{{height:46px;padding:0 18px;border-radius:14px;font-weight:800;font-size:14px;display:inline-flex;align-items:center;gap:8px;text-decoration:none;transition:transform .2s,background .2s,color .2s;cursor:pointer;border:0;font-family:inherit}}
.btn-green{{background:{G};color:#fff}} .btn-green:hover{{transform:translateY(-2px)}}
.btn-line{{background:#fff;color:{G};border:1.5px solid {LINE}}} .btn-line:hover{{border-color:{G2}}}
/* Pied de page */
.site-footer{{position:relative;overflow:hidden;color:#C7D8D0;background:linear-gradient(160deg,{G} 0%,{DEEP} 55%,#031E17 100%)}}
.glow{{position:absolute;border-radius:50%;pointer-events:none}}
.g1{{left:-200px;top:-260px;width:640px;height:640px;background:radial-gradient(closest-side,rgba(11,107,69,.55),rgba(0,0,0,0))}}
.g2{{right:-120px;bottom:-200px;width:520px;height:520px;background:radial-gradient(closest-side,rgba(227,160,8,.14),rgba(0,0,0,0))}}
.f-in{{position:relative;padding-top:56px}}
.f-top{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:24px 40px;padding:26px 28px;border-radius:26px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1)}}
.f-cols{{display:flex;flex-wrap:wrap;gap:32px 40px;padding:44px 4px 40px}}
.f-cols nav{{flex:1 1 180px;min-width:0;display:flex;flex-direction:column;gap:12px;font-size:14.5px}}
.f-cols a{{color:#C7D8D0;text-decoration:none;transition:color .2s}} .f-cols a:hover{{color:#fff}}
.f-h{{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:{GOLD};margin-bottom:4px}}
.f-bottom{{padding:20px 4px;border-top:1px solid rgba(255,255,255,.1);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;font-size:13px;color:#9DB8AC}}
.f-legal{{display:flex;flex-wrap:wrap;gap:18px}} .f-legal a{{color:#9DB8AC;text-decoration:none}}
/* Animations */
[data-reveal]{{opacity:0;transform:translateY(32px);transition:opacity .8s ease,transform .8s cubic-bezier(.2,.7,.2,1)}}
[data-reveal].is-in{{opacity:1;transform:none}}
[data-reveal] [data-stg]{{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}}
[data-reveal].is-in [data-stg]{{opacity:1;transform:none}}
@keyframes rise{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
.to-top{{position:fixed;right:22px;bottom:22px;width:50px;height:50px;border-radius:50%;border:0;background:{G};color:#fff;display:grid;place-items:center;cursor:pointer;box-shadow:0 12px 30px rgba(5,46,34,.3);opacity:0;transform:translateY(20px);pointer-events:none;transition:opacity .3s,transform .3s;z-index:60}}
.to-top.show{{opacity:1;transform:none;pointer-events:auto}} .to-top:hover{{background:{GOLD};color:{DEEP}}}
/* Responsive */
@media (max-width:1279px){{
  .burger{{display:flex}}
  .head-search{{display:none}}
  .main-nav{{display:none}}
  .site-header.menu-open .main-nav{{display:block;max-height:calc(100vh - 120px);overflow:auto;animation:rise .35s ease both}}
  .nav-in{{flex-direction:column;padding-top:8px;padding-bottom:16px}}
  .nav-link{{min-height:50px;border-bottom:1px solid {SOFT}}}
  .nav-link::after{{display:none}}
  .nav-item.is-active .nav-link{{box-shadow:inset 4px 0 0 {GOLD};padding-left:14px}}
  .chev{{display:none}}
  .sub{{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:0;padding:4px 0 8px 14px;min-width:0;background:transparent}}
  .sub a{{padding:9px 10px;font-weight:500;color:{MUTED}}}
}}
@media (max-width:760px){{
  .wrap{{padding:0 18px}}
  .brand .b1{{display:none}}
  .brand .b2{{font-size:12px;max-width:230px}}
  .head-row{{min-height:70px}}
  .brand img{{width:44px;height:44px}}
  .f-top{{padding:20px}}
  .to-top{{right:14px;bottom:14px;width:44px;height:44px}}
}}
@media (prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important;scroll-behavior:auto!important}}[data-reveal],[data-reveal] [data-stg]{{opacity:1;transform:none}}}}
'''
JS=r'''
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{threshold:.08});
  document.querySelectorAll('[data-reveal]').forEach(function(el){io.observe(el);el.querySelectorAll('[data-stg]').forEach(function(s,i){s.style.transitionDelay=(Math.min(i,12)*60+120)+'ms';});});
  var header=document.querySelector('.site-header'),top=document.querySelector('.to-top');
  window.addEventListener('scroll',function(){var y=window.scrollY;header.classList.toggle('is-scrolled',y>30);top.classList.toggle('show',y>600);},{passive:true});
  top.addEventListener('click',function(){window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});});
  var burger=document.querySelector('.burger');
  burger.addEventListener('click',function(){var o=header.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o?'true':'false');burger.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');});
})();
'''
FONT='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@600&display=swap" rel="stylesheet">'
def page(title,active,main,extra_css='',extra_js=''):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</title>
<link rel="icon" href="{SEAL}">
{FONT}
<style>{CSS}{extra_css}</style>
</head>
<body>
{header(active)}
<main>
{main}
</main>
{footer()}
<script>{JS}{extra_js}</script>
</body>
</html>
'''
