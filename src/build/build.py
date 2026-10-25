import sys, re, json, os, html as H
BASE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BASE)
from common import CSS, JS as CJS, SEAL, uri, arrow, ico, I, GOLD, G, G2, DEEP, INK, MUTED, LINE, SOFT, TXT, FONT
D=BASE+os.sep
I['heart']='<path d="M12 21s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 8a4.3 4.3 0 0 1 7.5 2.8C19.5 16.4 12 21 12 21Z"></path>'
I['target']='<circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><circle cx="12" cy="12" r="1.5" fill="currentColor"></circle>'
I['pin']='<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"></path><circle cx="12" cy="9.5" r="2.5"></circle>'
I['check']='<path d="m5 12 5 5 9-10"></path>'
I['clock']='<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path>'
I['coin']='<circle cx="12" cy="12" r="9"></circle><path d="M14.5 9c-.5-1-1.5-1.5-2.5-1.5-1.7 0-3 1-3 2.3 0 2.9 6 1.6 6 4.4 0 1.3-1.3 2.3-3 2.3-1.1 0-2.2-.6-2.7-1.6M12 6v1.5M12 16.5V18"></path>'
IM={k:uri(f,m) for k,(f,m) in {'panel':('conference-panel.jpg','image/jpeg'),'sc':('service-civique.jpg','image/jpeg'),'jap':('cooperation-japon.jpg','image/jpeg'),'afd':('cooperation-afd.jpg','image/jpeg'),'min':('ministre.jpg','image/jpeg')}.items()}
IM['seal']=SEAL

# ---------------- Menu (routes) ----------------
MENU=[("Le Ministère","ministere",[("Présentation","a-propos"),("Le Ministre","ministre"),("Cabinet du Ministre","cabinet"),("Le Secrétariat Général","secretariat"),("Directions centrales","directions"),("Établissements sous tutelle","etablissements")]),
("Domaines","domaines","MEGA"),
("Programmes","programmes",[("Programmes","programmes"),("Projets","projets")]),
("Actualités","actualites",[("Toutes les actualités","actualites"),("Photos et vidéos","medias")]),
("Appels d’offres","offres",[("Tout voir","offres"),("Annonces","offres-annonces"),("Appels d’offres","offres-appels"),("Contrats","offres-contrats")]),
("Contact","contact",[])]
MEGA=[("jeunesse","Jeunesse","Autonomisation et participation des jeunes",I['users'],["Autonomisation des jeunes","Renforcement des capacités","Associations et réseaux de jeunesse","Espaces et maisons des jeunes"]),
("emploi","Emploi","Insertion et accompagnement vers l’emploi",I['briefcase'],["Stratégie Nationale de l’Emploi","Coordination de Projets Emploi","Agence TECHGHIL","Permis de travail","Documents"]),
("sports","Sports","Sport de compétition et sport pour tous",I['trophy'],["Sport de compétition","Sport de masse","Fédérations et clubs sportifs","Infrastructures sportives"]),
("service-civique","Service civique","Engagement citoyen et volontariat",I['heart'] if 'heart' in I else I['users'],["Service civique volontaire","Service civique obligatoire"])]
def header():
    items=''
    for t,r,sub in MENU:
        if sub=="MEGA":
            cols=''.join(f'<div class="mc"><a href="#{dr}" class="mc-h"><span class="mc-ic">{ico(ic,22)}</span><span><b>{dn}</b><small>{dt}</small></span></a>'+''.join(f'<a href="#{dr}" class="mc-l">{x}</a>' for x in subs)+'</div>' for dr,dn,dt,ic,subs in MEGA)
            items+=f'<div class="nav-item has-sub mega" data-menu="{r}"><a href="#jeunesse" class="nav-link">{t}<span class="chev">{ico(I["chev"],13,2.4)}</span></a><div class="sub mega-p" role="menu"><div class="mega-cols">{cols}</div><a href="#parcours" class="mega-cta"><span><b>Vous cherchez un service ?</b><small>Trouvez la démarche adaptée à votre besoin.</small></span><span class="mega-go">{arrow(16)}</span></a></div></div>'
        elif sub:
            links=''.join(f'<a href="#{sr}">{st}</a>' for st,sr in sub)
            items+=f'<div class="nav-item has-sub" data-menu="{r}"><a href="#{sub[0][1]}" class="nav-link">{t}<span class="chev">{ico(I["chev"],13,2.4)}</span></a><div class="sub" role="menu">{links}</div></div>'
        else:
            items+=f'<div class="nav-item" data-menu="{r}"><a href="#{r}" class="nav-link">{t}</a></div>'
    return f'''<div class="topbar"><div class="wrap topbar-in"><span>Site officiel · Honneur, Fraternité, Justice</span><span class="tb-right"><a href="#contact">Contact</a><span class="lang"><a href="#accueil" class="on">FR</a><a href="#accueil" lang="ar">عربية</a></span></span></div></div>
<header class="site-header">
  <div class="wrap head-row">
    <a href="#accueil" class="brand"><img data-img="seal" alt="Sceau de la République Islamique de Mauritanie"><span class="brand-txt"><span class="b1">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</span><span class="b2">Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</span></span></a>
    <nav id="menu" class="main-nav" aria-label="Navigation principale"><div class="nav-in"><div class="nav-item" data-menu="accueil"><a href="#accueil" class="nav-link">Accueil</a></div>{items}</div></nav>
    <div class="head-act">
      <button class="s-btn" aria-label="Rechercher" aria-expanded="false" aria-controls="search-panel">{ico(I["search"],19,2.2)}</button>
      <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div id="search-panel" class="search-panel" hidden><div class="wrap"><form class="head-search" role="search" id="hsf"><label for="hs" class="sr">Rechercher sur le portail</label>{ico(I["search"],20,2)}<input id="hs" type="search" placeholder="Que cherchez-vous ? Une page, une actualité, un document…"><button type="submit" class="hs-go">Rechercher</button></form></div></div>
  <div class="stripe" aria-hidden="true"><i style="flex:1;background:#C8102E"></i><i style="flex:13;background:{G2}"></i><i style="flex:1;background:#C8102E"></i></div>
</header>'''
def footer():
    cols=[("Le Ministère",[("Le Ministre","ministre"),("Cabinet du Ministre","cabinet"),("Le Secrétariat Général","secretariat"),("Établissements sous tutelle","etablissements")]),("Offres et appels d’offres",[("Annonces","offres-annonces"),("Appels d’offres","offres-appels"),("Contrats","offres-contrats")]),("Centre des médias",[("Actualités","actualites"),("Photos et vidéos","medias")]),("Programmes et projets",[("Programmes","programmes"),("Projets","projets"),("Agence Techghil","emploi"),("Projets PEJ","projets")])]
    ch=''.join(f'<nav aria-label="{t}"><span class="f-h">{t}</span>'+''.join(f'<a href="#{r}">{l}</a>' for l,r in ls)+'</nav>' for t,ls in cols)
    return f'''<footer class="site-footer">
  <div class="stripe" aria-hidden="true"><i style="flex:1;background:#C8102E"></i><i style="flex:6;background:{G2}"></i><i style="flex:1;background:{GOLD}"></i><i style="flex:6;background:{G2}"></i><i style="flex:1;background:#C8102E"></i></div>
  <span class="glow g1" aria-hidden="true"></span><span class="glow g2" aria-hidden="true"></span>
  <div class="wrap f-in">
    <div class="f-top"><a href="#accueil" class="brand dark"><img data-img="seal" alt=""><span class="brand-txt"><span class="b1">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</span><span class="b2">Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</span></span></a><a href="#parcours" class="btn-gold">Trouver un service {arrow(14)}</a></div>
    <div class="f-cols">{ch}</div>
    <div class="f-bottom"><span>© 2026 Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique · Nouakchott, Mauritanie</span><span class="f-legal"><a href="#contact">Mentions légales</a><a href="#contact">Accessibilité</a><a href="#plan">Plan du site</a></span></div>
  </div>
</footer>
<button class="to-top" aria-label="Revenir en haut de la page">{ico('<path d="M12 19V5M6 11l6-6 6 6"></path>',20,2.2)}</button>'''

# ---------------- Gabarits ----------------
def hero(crumbs,kick,title,intro='',img=None,meta=''):
    cr='<a href="#accueil">Accueil</a>'+''.join(f'<span>›</span><a href="#{r}">{t}</a>' if r else f'<span>›</span><span aria-current="page">{t}</span>' for t,r in crumbs)
    bg=f'<img data-img="{img}" alt="" aria-hidden="true" class="ph-img">' if img else ''
    return f'''<section class="page-hero">{bg}<span class="ph-veil" aria-hidden="true"></span>
  <span class="glow h1g" aria-hidden="true"></span>
  <div class="wrap ph-in">
    <nav class="crumbs" aria-label="Fil d’Ariane">{cr}</nav>
    <span class="kicker gold">{kick}</span>
    <h1>{title}</h1>
    {f'<p>{intro}</p>' if intro else ''}{meta}
  </div>
</section>'''
def side(title,items,cur):
    lis=''.join(f'<a href="#{r}" class="sn{" on" if r==cur else ""}">{t}{arrow(14)}</a>' for t,r in items)
    return f'<aside class="side-nav" data-reveal><span class="box-h">{title}</span>{lis}</aside>'
def card(t,d,icon,href,tag=''):
    return f'<a href="#{href}" class="card" data-stg><span class="card-ic">{ico(icon,24)}</span>{f"<span class=chip>{tag}</span>" if tag else ""}<span class="card-t">{t}</span><span class="card-d">{d}</span><span class="card-go">En savoir plus {arrow(14)}</span></a>'
def route(r,title,body):
    return f'<div class="route" data-route="{r}" data-title="{H.escape(title)}" hidden>\n{body}\n</div>\n'
ABOUT=[("Présentation","a-propos"),("Le Ministre","ministre"),("Cabinet du Ministre","cabinet"),("Le Secrétariat Général","secretariat"),("Directions centrales","directions"),("Établissements sous tutelle","etablissements")]
def cta():
    return f'''<aside class="help" data-reveal><span class="help-ic">{ico(I['mega'],26)}</span><div><b>Une question ? Le ministère vous oriente.</b><span>Information administrative ou demande d’orientation.</span></div><a href="#contact" class="btn btn-green">Nous contacter {arrow(14)}</a></aside>'''

R=''
# ---------- Accueil ----------
home=open(D+'home_main.html').read()
def remap_home(h):
    h=h.replace('href="Actualites.dc.html"','href="#actualites"').replace('href="Main.dc.html"','href="#accueil"')
    h=h.replace('href="offres-et-appels-doffres.html#annonces"','href="#offres-annonces"').replace('href="offres-et-appels-doffres.html"','href="#offres"')
    table=[("Biographie","ministre"),("Missions","a-propos"),("Cabinet","cabinet"),("Secrétariat","secretariat"),("Directions","directions"),("tutelle","etablissements"),
           ("Développer mes compétences","jeunesse"),("Maisons des jeunes","jeunesse"),("Techghil","emploi"),("TECHGHIL","emploi"),("Rokhsa","emploi"),("Permis","emploi"),("Stratégie","emploi"),("Coordination","emploi"),("Documents","emploi"),
           ("Infrastructures","sports"),("Fédérations","sports"),("Service Civique","service-civique"),("volontariat 2025","offres-annonces"),
           ("Lois","offres"),("Décrets","offres"),("Arrêtés","offres"),("Circulaires","offres"),
           ("PAA","document"),("Avis d’appel","document"),("Conférence nationale","article-1"),("Prix du Président","offres-annonces"),("Plan annuel","document"),("Stratégie nationale","document"),
           ("Intitulé","offres"),("Afficher tout","offres-annonces"),("Nous contacter","contact"),("vidéos","medias"),("Mon Projet Futur","medias"),("Bilan du secteur","medias"),("160 jeunes","medias"),
           ("Lire l’article","article-1"),("Voir l’agenda","offres-annonces"),("statistiques","programmes"),("Tekwine","programmes"),("PEJ","programmes"),("Microfinance","programmes")]
    def fix(m):
        seg=m.group(0); txt=re.sub(r'<[^>]+>',' ',h[m.end():m.end()+900].split('</a>')[0])
        for k,r in table:
            if k in txt: return seg.replace('href="#"',f'href="#{r}"')
        return seg
    return re.sub(r'<a (?:class="[^"]*" )?(?:data-stg )?href="#"',fix,h)
home=remap_home(home)
home=home.replace('<a href="#annonces" style="height: 50px','<a href="#offres-annonces" style="height: 50px')
R+=route('accueil','Accueil',home)

# ---------- À propos ----------
def about_page(r,title,kick,intro,body):
    return route(r,title,hero([("À propos","a-propos"),(title,None)] if r!='a-propos' else [("À propos",None)],kick,title,intro)+f'''<div class="wrap with-side">{side("À propos du Ministère",ABOUT,r)}<div class="main-col" data-reveal>{body}</div></div><div class="wrap">{cta()}</div><div class="spacer"></div>''')
R+=about_page('a-propos','À propos du Ministère','Le Ministère','Une institution au service des jeunes et de l’avenir.',f'''
<div class="lead-block" data-stg><h2>Missions</h2><p class="big">Le Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique a pour mission générale de <b>concevoir, de mettre en œuvre, de suivre et d’évaluer</b> les politiques nationales en matière d’autonomisation des jeunes, d’emploi, des sports et du service civique.</p></div>
<div class="minister" data-stg><img data-img="min" alt="Mohamed Abdallahi Louly"><div><span class="kicker">Le Ministre</span><h3>Mohamed Abdallahi Louly</h3><p>Ministre de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service civique</p><a href="#ministre" class="btn btn-green">Biographie {arrow(14)}</a></div></div>
<h2 class="h2s" data-stg>Organisation</h2>
<div class="cards">{card("Cabinet du Ministre","Chargés de mission, conseillers techniques, inspecteur général et attachés de cabinet.",I['users'],"cabinet")}{card("Le Secrétariat Général","Dirigé par un Secrétaire Général, il coordonne les services du ministère.",I['folder'],"secretariat")}{card("Directions centrales","Les huit (08) directions centrales du ministère.",I['doc'],"directions")}{card("Établissements sous tutelle","Les établissements placés sous la tutelle du Ministre.",I['link'],"etablissements")}</div>''')
MIN_POSTES=[("6 août 2024","Ministre de l’Autonomisation de la Jeunesse, des Sports et du Service civique","Nomination"),
("4 juillet 2023","Ministre de la Transition numérique, de l’Innovation et de la Modernisation de l’Administration","Nomination"),
("Juillet 2022","Membre du Conseil Supérieur de l’Investissement en Mauritanie",""),
("2021","Chef adjoint du Département de la Transformation numérique et Innovation à l’Union Nationale du Patronat Mauritanien","")]
MIN_AUTRES=["Fondateur et Directeur Général du Groupe GTI International.","Chercheur académique dans le domaine du commerce et du management, notamment en stratégies de la transformation numérique et écosystème PME.","Membre du Bureau du Club des entrepreneurs."]
MIN_FORM=[("2020 – 2022","Master of Business Administration (MBA)","« Leadership of Innovation and Change », British University York St. John.",""),
("2001 – 2004","Master de l’École Polytechnique de Tunisie (BAC+5)","Ingénieur d’État. Premier de sa promotion.","Lauréat du prix présidentiel « Meilleur ingénieur diplômé de Tunisie 2004 »"),
("1999 – 2001","Institut Préparatoire de Sfax","Premier au concours national d’entrée aux grandes écoles d’ingénieurs de Tunisie.",""),
("1998 – 1999","Lycée National de Nouakchott","Baccalauréat en mathématiques, deuxième au niveau national.","")]
def tl(items,kind):
    out=''
    for i,it in enumerate(items):
        if kind=='p':
            d,t,tag=it; extra=f'<span class="tl-tag">{tag}</span>' if tag else ''
            body=f'<span class="tl-t">{t}</span>{extra}'
        else:
            d,t,sub,award=it
            aw=f'<span class="tl-award">{ico(I["trophy"],16)} {award}</span>' if award else ''
            body=f'<span class="tl-t">{t}</span><span class="tl-s">{sub}</span>{aw}'
        out+=f'<li class="tl-i{" first" if i==0 else ""}" data-stg><span class="tl-d">{d}</span><span class="tl-dot" aria-hidden="true"></span><div class="tl-c">{body}</div></li>'
    return f'<ol class="tl">{out}</ol>'
abnav=''.join(f'<a href="#{r}" class="ab{" on" if r=="ministre" else ""}">{t}</a>' for t,r in ABOUT)
R+=route('ministre','Le Ministre',f'''
<section class="min-hero">
  <span class="glow h1g" aria-hidden="true"></span>
  <div class="wrap mh-in">
    <div class="mh-txt">
      <nav class="crumbs" aria-label="Fil d’Ariane"><a href="#accueil">Accueil</a><span>›</span><a href="#a-propos">À propos du ministère</a><span>›</span><span aria-current="page">Le Ministre</span></nav>
      <span class="kicker gold">Le Ministre</span>
      <h1>Mohamed Abdallahi Louly</h1>
      <p class="mh-role">Ministre de l’Autonomisation de la Jeunesse, de l’Emploi, des Sports et du Service civique</p>
      <div class="mh-facts">
        <span>{ico(I['cal'],18)}<b>Né le</b> 21 mai 1980</span>
        <span>{ico(I['users'],18)}<b>Situation familiale</b> Marié</span>
        <span>{ico('<circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"></path>',18)}<b>Langues</b> Arabe, français, anglais</span>
      </div>
      <div class="mh-act"><a href="#min-parcours" class="btn-gold">Parcours professionnel {arrow(14)}</a><a href="#min-formation" class="btn btn-ghost">Formation</a></div>
    </div>
    <div class="mh-photo">
      <span class="mh-frame" aria-hidden="true"></span>
      <img data-img="min" alt="Portrait officiel de Mohamed Abdallahi Louly">
      <span class="mh-badge"><small>En fonction depuis le</small><b>6 août 2024</b></span>
    </div>
  </div>
</section>
<div class="wrap sec" data-reveal>
  <div class="hl">
    <div class="hl-c" data-stg><span class="hl-y">2024</span><span>Ministre de l’Autonomisation de la Jeunesse, des Sports et du Service civique</span></div>
    <div class="hl-c" data-stg><span class="hl-y">2023</span><span>Ministre de la Transition numérique, de l’Innovation et de la Modernisation de l’Administration</span></div>
    <div class="hl-c gold" data-stg><span class="hl-y">2004</span><span>Prix présidentiel « Meilleur ingénieur diplômé de Tunisie »</span></div>
    <div class="hl-c" data-stg><span class="hl-y">MBA</span><span>Leadership of Innovation and Change, York St. John University</span></div>
  </div>
</div>
<section id="min-parcours" class="wrap sec min-sec" data-reveal aria-labelledby="mp-h">
  <div class="ms-h"><span class="kicker">Postes occupés</span><h2 id="mp-h">Parcours professionnel</h2></div>
  <div class="ms-body">
    {tl(MIN_POSTES,'p')}
    <div class="other" data-stg><span class="box-h">Autres responsabilités</span>{''.join(f'<p>{x}</p>' for x in MIN_AUTRES)}<div class="quote">{ico(I['mega'],20)}<span>Il a présenté plusieurs conférences sur les thèmes de l’entrepreneuriat, de la gestion du changement et des nouvelles techniques expérimentales.</span></div></div>
  </div>
</section>
<section id="min-formation" class="min-band" data-reveal aria-labelledby="mf-h">
  <div class="wrap min-sec">
    <div class="ms-h"><span class="kicker gold">Qualifications académiques</span><h2 id="mf-h">Formation</h2></div>
    <div class="ms-body">{tl(MIN_FORM,'f')}</div>
  </div>
</section>
<section id="min-langues" class="wrap sec" data-reveal aria-labelledby="ml-h">
  <div class="sec-h"><span class="kicker">Compétences linguistiques</span><h2 id="ml-h">Il parle trois langues</h2></div>
  <div class="langs">{''.join(f'<div class="lg" data-stg><span class="lg-c"{" lang=ar" if c=="ع" else ""}>{c}</span><b>{n}</b></div>' for c,n in [("ع","Arabe"),("Fr","Français"),("En","Anglais")])}</div>
</section>
<div class="wrap">{cta()}</div><div class="spacer"></div>''')
R+=about_page('cabinet','Cabinet du Ministre','À propos','La composition du Cabinet du Ministre.',f'''
<div class="prose" data-stg><p class="big">Le Cabinet du Ministre comprend des chargés de mission, huit (08) conseillers techniques, un (1) inspecteur général, trois (3) attachés de cabinet dont un chargé du secrétariat du Ministre, et un (1) secrétaire particulier.</p></div>
<div class="stats" data-stg><div><b>08</b><span>conseillers techniques</span></div><div><b>01</b><span>inspecteur général</span></div><div><b>03</b><span>attachés de cabinet</span></div><div><b>01</b><span>secrétaire particulier</span></div></div>''')
R+=about_page('secretariat','Le Secrétariat Général','À propos','Le Secrétariat Général est dirigé par un Secrétaire Général.',f'''
<div class="prose" data-stg><p class="big">Le Secrétariat Général est dirigé par un Secrétaire Général et comprend les services suivants :</p><ul><li>[Service 1]</li><li>[Service 2]</li><li>[Service 3]</li></ul></div>''')
R+=about_page('directions','Directions centrales','À propos','Les directions centrales du ministère sont au nombre de huit (08).',f'''
<div class="prose" data-stg><p class="big">Les Directions Centrales du Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique sont au nombre de huit (08) :</p></div>
<div class="num-list" data-stg>{''.join(f'<div><b>0{i}</b><span>[Nom de la direction centrale]</span></div>' for i in range(1,9))}</div>''')
R+=about_page('etablissements','Établissements sous tutelle','À propos','Le Ministre exerce le pouvoir de tutelle sur les établissements suivants.',f'''
<div class="cards">{card("Agence nationale de l’emploi TECHGHIL","Accompagnement des demandeurs d’emploi et intermédiation.",I['briefcase'],"emploi")}{card("[Établissement]","[Description de l’établissement]",I['link'],"etablissements")}{card("[Établissement]","[Description de l’établissement]",I['link'],"etablissements")}</div>''')

# ---------- Domaines ----------
NEWS=[("Grand angle","26 octobre 2025","La jeunesse au cœur du dialogue national.","La Conférence nationale de l’autonomisation des jeunes, un espace pour faire entendre les ambitions.","panel","Jeunesse"),
("Coopération","14 novembre 2025","Le Ministre reçoit l’ambassadeur de l’Empire du Japon en Mauritanie","Le ministère a reçu l’ambassadeur de l’Empire du Japon accrédité en Mauritanie.","jap","Coopération"),
("Coopération","14 novembre 2025","Le Ministre reçoit le Directeur de l’Agence française de Développement (AFD) en Mauritanie","Une rencontre avec le Directeur de l’Agence française de Développement en Mauritanie.","afd","Coopération"),
("Service civique","Septembre 2025","300 volontaires : une nouvelle promotion engagée","Cérémonie de sortie d’une promotion de 300 volontaires du service civique, supervisée par les ministres concernés.","sc","Service civique"),
("Coopération","[Date]","Le Ministre reçoit l’ambassadeur de Chine","[Résumé de l’actualité]",None,"Coopération")]
def newscard(i):
    c,d,t,desc,img,_=NEWS[i]
    media=f'<span class="nc-img"><img data-img="{img}" alt=""></span>' if img else f'<span class="nc-img ph">{ico(I["mega"],34)}</span>'
    return f'<a href="#article-{i+1}" class="ncard" data-stg data-cat="{c}">{media}<span class="nc-b"><span class="nc-meta"><span class="chip">{c}</span>{d}</span><span class="nc-t">{t}</span><span class="nc-go">Lire l’article {arrow(14)}</span></span></a>'
DOM={
'jeunesse':("Jeunesse","Autonomisation des jeunes","Donner à chaque jeune les moyens d’agir.","Renforcer les capacités des jeunes en offrant des opportunités d’éducation, de formation et d’emploi, ainsi qu’en soutenant l’innovation et l’entrepreneuriat.","panel",
  [("Autonomisation des jeunes","Accompagner les jeunes vers l’autonomie et l’entrepreneuriat.",I['users']),("Renforcement des capacités","Formations et ressources pour développer les compétences.",I['doc']),("Associations et réseaux de jeunesse","Soutien et accompagnement de la vie associative.",I['users']),("Espaces et maisons des jeunes","Lieux dédiés aux activités et à la participation des jeunes.",I['home'])],[0,3]),
'emploi':("Emploi","Emploi et insertion","Construire son parcours professionnel.","Un point d’entrée vers les ressources de l’emploi, l’accompagnement de TECHGHIL et les informations administratives.","afd",
  [("Stratégie Nationale de l’Emploi","Le cadre national des politiques de l’emploi.",I['doc']),("Coordination de Projets Emploi","Le suivi et la coordination des projets en faveur de l’emploi.",I['folder']),("Agence nationale de l’emploi TECHGHIL","L’accompagnement des demandeurs d’emploi.",I['briefcase']),("Permis de travail","Les informations administratives sur le permis de travail.",I['pen']),("Documents","Les documents du département de l’emploi.",I['doc'])],[2,1]),
'sports':("Sports","Développement du sport","Le sport, une énergie qui nous rassemble.","Améliorer les infrastructures sportives et renforcer la participation sportive aux niveaux local et national, avec le soutien aux athlètes et l’organisation d’événements sportifs.",None,
  [("Sport de compétition","Soutien aux athlètes et aux compétitions.",I['trophy']),("Sport de masse","Le sport pour tous, pour la santé et la communauté.",I['users']),("Fédérations et clubs sportifs","Les structures du sport national.",I['folder']),("Infrastructures sportives","Équipements et espaces sportifs.",I['home'])],[]),
'service-civique':("Service civique","Service civique et intégration communautaire","S’engager aujourd’hui. Être utile à tous.","Encourager la participation sociale des jeunes à travers le bénévolat et les initiatives communautaires, et promouvoir la coexistence et la coopération entre les différentes couches de la société.","sc",
  [("Service civique volontaire","S’engager volontairement au service de la nation.",I['users']),("Service civique obligatoire","Les informations sur le service civique obligatoire.",I['doc']),("Prix du volontariat 2025","Prix du Président de la République pour les meilleures actions de volontariat.",I['trophy'])],[3])}
for r,(name,axis,title,desc,img,subs,news) in DOM.items():
    sc=''.join(f'<div class="rub" data-stg><span class="rub-ic">{ico(ic,24)}</span><div><b>{t}</b><span>{d}</span></div></div>' for t,d,ic in subs)
    nh=''.join(newscard(i) for i in news) or '<p class="muted" data-stg>Les actualités de ce domaine seront publiées ici.</p>'
    body=hero([(name,None)],axis,title,desc,img)+f'''
<div class="wrap sec" data-reveal><div class="sec-h"><span class="kicker">Nos rubriques</span><h2>{name} : ce que fait le ministère</h2></div><div class="rubs">{sc}</div></div>
<div class="band" data-reveal><div class="wrap band-in"><div><span class="kicker gold">Services en ligne</span><h2>Accéder aux démarches</h2><p>Les démarches officielles se poursuivent sur les plateformes concernées.</p></div><div class="band-act"><a href="#offres-annonces" class="btn-gold">Annonces et candidatures {arrow(14)}</a><a href="#contact" class="btn btn-ghost">Besoin d’orientation ?</a></div></div></div>
<div class="wrap sec" data-reveal><div class="sec-h row"><div><span class="kicker">Actualités</span><h2>Dernières actualités</h2></div><a href="#actualites" class="tlink">Toutes les actualités {arrow(14)}</a></div><div class="ncards">{nh}</div></div>
<div class="wrap">{cta()}</div><div class="spacer"></div>'''
    R+=route(r,name,body)

# ---------- Programmes ----------
# ---------- Programmes ----------
MEH_OBJ=["Créer un cadre de concertation actif entre les opérateurs de l’emploi, de la formation professionnelle et le secteur privé pour garantir une meilleure adéquation formation-emploi et faciliter l’intégration des jeunes au milieu du travail.",
"Suivre l’évolution de la demande du marché du travail et orienter l’offre de formation en fonction de ses besoins.",
"Organiser des campagnes de sensibilisation pour la vulgarisation et la valorisation des emplois demandés par le marché du travail, et orienter les jeunes vers l’appropriation des métiers afférents.",
"Appuyer les opérateurs de la formation et les entreprises pour l’identification et la sélection des bénéficiaires des formations qualifiantes et en apprentissage.",
"Coordonner avec les services de l’emploi concernés pour accompagner les bénéficiaires des formations vers l’intégration en entreprise ou l’auto-emploi.",
"Développer les stages en entreprise et promouvoir l’apprentissage et les formations par alternance.",
"Participer aux études de prospection et d’identification des besoins en formation dans les secteurs porteurs d’emplois.",
"Améliorer la perception des métiers peu pratiqués par les nationaux."]
def objlist(L): return '<ul class="obj">'+''.join(f'<li data-stg><span class="ok">{ico(I["check"],14,2.6)}</span><span>{x}</span></li>' for x in L)+'</ul>'
def subnav(cur):
    return f'<div class="pp-switch"><a href="#programmes" class="{"on" if cur=="programmes" else ""}">{ico(I["target"],18)}Programmes</a><a href="#projets" class="{"on" if cur=="projets" else ""}">{ico(I["folder"],18)}Projets</a></div>'
prog_hero=hero([("Programmes et projets","programmes"),("Programmes",None)],"Programmes et projets","Nos programmes","Des dispositifs pour accompagner les jeunes vers l’entrepreneuriat, la formation et l’emploi.",None,'<div class="ph-meta"><span>'+ico(I['cal'],17)+' Mis à jour le 24 août 2024</span></div>')
R+=route('programmes','Programmes',prog_hero+f'''
<div class="wrap pp-top">{subnav("programmes")}<nav class="pp-index" aria-label="Sur cette page"><a href="#prog-mpma"><b>01</b>Mon Projet, Mon Avenir</a><a href="#prog-mehenti"><b>02</b>MEHENTI</a></nav></div>
<article id="prog-mpma" class="wrap prog" data-reveal>
  <header class="prog-h" data-stg><span class="prog-n">01</span><div><span class="kicker">Entrepreneuriat · Auto-emploi</span><h2>Mon Projet, Mon Avenir</h2><p class="prog-ar">« Mechroui Moustaqbeli »</p></div></header>
  <div class="prog-grid">
    <section class="pg-box" data-stg><span class="pg-k">{ico(I['doc'],18)} Contexte</span><p>Le gouvernement a mis en place des dispositifs et des mesures afin d’encourager et soutenir les auto-entrepreneurs à travers le programme <b>« Mechroui Moustaqbeli »</b>, « Mon Projet, Mon Avenir », pour l’accompagnement et le financement de micro et petites entreprises rentables dans les secteurs productifs, sur l’étendue du territoire national.</p></section>
    <section class="pg-box green" data-stg><span class="pg-k">{ico(I['target'],18)} Objectif</span><p>Contribuer à la lutte contre le chômage des jeunes à travers le financement et l’accompagnement d’un tissu de MPE productives de richesses, en partenariat avec les acteurs professionnels d’un écosystème entrepreneurial travaillant en synergie.</p>
      <div class="pg-tags"><span>Financement</span><span>Accompagnement</span><span>Micro et petites entreprises</span><span>Tout le territoire</span></div></section>
  </div>
</article>
<article id="prog-mehenti" class="prog-band" data-reveal>
  <div class="wrap prog">
  <header class="prog-h" data-stg><span class="prog-n">02</span><div><span class="kicker">Orientation · Métiers</span><h2>MEHENTI</h2><p class="prog-ar">Programme de valorisation des métiers et des professions</p></div><span class="prog-badge">{ico(I['doc'],16)} Arrêté N° 352 du 19 mai 2020</span></header>
  <div class="prog-grid">
    <section class="pg-box white" data-stg><span class="pg-k">{ico(I['doc'],18)} Contexte</span>
      <p class="pg-quote">Pour réussir un métier, il faut le pratiquer avec passion. Son choix doit être réfléchi, travaillé et mûri.</p>
      <p>Le choix du métier doit bénéficier du plus grand intérêt et des conseils de services spécialisés ou de personnes de confiance, souvent insuffisants voire absents pour nos jeunes.</p>
      <p>Il en résulte une auto-orientation vers des formations et des métiers peu sollicités par le marché de l’emploi, et l’abandon de professions réellement porteuses d’emplois : BTP, pêche, restauration, hôtellerie, artisanat, agriculture, élevage…</p>
      <p>Pour pallier ce déséquilibre, le Ministère a mis en place le programme de valorisation des métiers et des professions <b>« MEHENTI »</b>, créé par l’arrêté N° 352 du 19 mai 2020.</p>
      <div class="pg-tags">{''.join(f'<span>{x}</span>' for x in ["BTP","Pêche","Restauration","Hôtellerie","Artisanat","Agriculture","Élevage"])}</div>
    </section>
    <section class="pg-box" data-stg><span class="pg-k">{ico(I['target'],18)} Objectifs du programme</span>{objlist(MEH_OBJ)}</section>
  </div>
  </div>
</article>
<div class="wrap">{cta()}</div><div class="spacer"></div>''')

# ---------- Projets ----------
PJ=[("pej-bm","Banque mondiale","Projet d’appui à l’employabilité des jeunes vulnérables en Mauritanie","PEJ Banque mondiale","42 millions USD","5 ans","Jeunes de 15 à 24 ans",
     [("Objectif de développement","Promouvoir l’employabilité des jeunes vulnérables dans les zones sélectionnées."),("Indicateur","Amélioration des résultats de l’emploi pour les jeunes.")],
     ["Nouakchott","Hodh Gharbi","Hodh Echargui","Assaba","Trarza","Guidimagha"],"Personnes âgées de 15 à 24 ans ayant au plus le niveau de l’enseignement secondaire (sans le baccalauréat), au chômage, inactives ou travaillant dans des conditions précaires.",None),
    ("pej-brakna","BAD","Projet d’appui à l’employabilité et à l’insertion socio-économique des jeunes vulnérables dans la wilaya du Brakna","PEJ Brakna / BAD","3,3 millions USD","5 ans","Jeunes de 15 à 24 ans",
     [("Objectif global","Améliorer la qualité de vie des populations à travers une meilleure employabilité des jeunes vulnérables dans la région du Brakna."),("Objectif spécifique","Promouvoir l’employabilité des jeunes vulnérables de 15 à 24 ans qui ne sont ni en formation ni en emploi, notamment les femmes.")],
     ["Brakna"],"Personnes âgées de 15 à 24 ans ayant au plus le niveau de l’enseignement secondaire (sans le baccalauréat), au chômage, inactives ou travaillant dans des conditions précaires.",None),
    ("pnud","PNUD","Promouvoir des emplois et d’autres moyens de subsistance respectueux de l’environnement","PNUD","1,5 million USD","12 mois","2 000 jeunes hommes et femmes",
     [("Objectif global","Contribuer directement au plan de riposte socio-économique contre les effets de la COVID-19.")],
     ["Guidimakha","Assaba"],"2 000 jeunes hommes et femmes, dont 1 700 femmes et 300 jeunes.",
     ["Des moyens de subsistance alternatifs, résilients, respectueux de l’environnement et rentables sont renforcés et développés au profit des groupes de femmes et des jeunes.","Les capacités nationales d’exécution, de coordination et de suivi des opportunités d’emploi des femmes et des jeunes sont renforcées."])]
def pj_card(i,p):
    pid,partner,title,short,fin,dur,ben_s,objs,zones,ben,res=p
    o=''.join(f'<div class="pj-o"><span class="pg-k">{ico(I["target"],16)} {k}</span><p>{v}</p></div>' for k,v in objs)
    r=('<div class="pj-o"><span class="pg-k">'+ico(I['check'],16,2.4)+' Résultats attendus</span>'+objlist(res)+'</div>') if res else ''
    split='<div class="pj-split"><span><b>1 700</b>femmes</span><span><b>300</b>jeunes</span></div>' if pid=='pnud' else ''
    return f'''<article id="{pid}" class="pj" data-reveal>
  <div class="pj-side" data-stg>
    <span class="pj-partner">{partner}</span>
    <span class="pj-n">0{i+1}</span>
    <h2>{title}</h2>
    <span class="pj-short">{short}</span>
    <div class="pj-facts">
      <div><span class="f-ic">{ico(I['coin'],20)}</span><small>Financement global</small><b>{fin}</b></div>
      <div><span class="f-ic">{ico(I['clock'],20)}</span><small>Durée</small><b>{dur}</b></div>
      <div><span class="f-ic">{ico(I['users'],20)}</span><small>Bénéficiaires</small><b>{ben_s}</b></div>
    </div>
  </div>
  <div class="pj-main" data-stg>
    {o}
    <div class="pj-o"><span class="pg-k">{ico(I['users'],16)} Bénéficiaires</span><p>{ben}</p>{split}</div>
    {r}
    <div class="pj-o"><span class="pg-k">{ico(I['pin'],16)} Zones d’intervention</span><div class="zones">{''.join(f'<span>{ico(I["pin"],14)}{z}</span>' for z in zones)}</div></div>
  </div>
</article>'''
proj_hero=hero([("Programmes et projets","programmes"),("Projets",None)],"Programmes et projets","Nos projets","Des projets menés avec les partenaires techniques et financiers pour l’employabilité des jeunes.",None,'<div class="ph-meta"><span>'+ico(I['cal'],17)+' Mis à jour le 24 août 2024</span></div>')
R+=route('projets','Projets',proj_hero+f'''
<div class="wrap pp-top">{subnav("projets")}<nav class="pp-index" aria-label="Sur cette page">{''.join(f'<a href="#{p[0]}"><b>0{i+1}</b>{p[3]}</a>' for i,p in enumerate(PJ))}</nav></div>
<div class="wrap" data-reveal><div class="pj-sum">
  <div data-stg><b>3</b><span>projets avec des partenaires</span></div>
  <div data-stg><b>46,8 M USD</b><span>de financement cumulé</span></div>
  <div data-stg><b>15 – 24 ans</b><span>tranche d’âge principale</span></div>
  <div data-stg><b>7</b><span>wilayas d’intervention</span></div>
</div></div>
<div class="wrap pjs">{''.join(pj_card(i,p) for i,p in enumerate(PJ))}</div>
<div class="wrap">{cta()}</div><div class="spacer"></div>''')
PR=[("Mon Projet, Mon Avenir","programmes"),("MEHENTI","programmes")]+[(p[2],"projets") for p in PJ]
# ---------- Actualités ----------
cats=["Toutes","Grand angle","Coopération","Service civique"]
R+=route('actualites','Actualités',hero([("Centre des médias","actualites"),("Actualités",None)],"Centre des médias","Actualités","Rencontres, initiatives et temps forts du ministère.")+f'''
<div class="wrap sec" data-reveal><div class="sec-h row"><div class="chips-f" role="tablist">{''.join(f'<button class="cf{" on" if i==0 else ""}" data-cat="{c}">{c}</button>' for i,c in enumerate(cats))}</div><a href="#medias" class="tlink">Photos et vidéos {arrow(14)}</a></div>
<div class="ncards big" id="newsgrid">{''.join(newscard(i) for i in range(len(NEWS)))}</div></div><div class="spacer"></div>''')
# Articles
JAP_TXT='''<p>Le Ministre de l’Autonomisation des Jeunes, de l’Emploi et du Service civique, M. Mohamed Abdellahi Louly, a reçu, ce vendredi 14 novembre 2025, en audience, Son Excellence M. Uchida Tatsukuni, ambassadeur de l’Empire du Japon accrédité en Mauritanie.</p><p>Cette rencontre a été l’occasion d’échanger sur l’état des relations de coopération entre les deux pays et d’explorer de nouvelles perspectives de partenariat.</p><p>L’audience s’est déroulée en présence du Secrétaire général du ministère, M. Naji Khattri.</p>'''
share=f'<div class="share" data-stg><span>Partager</span><div class="sh-row">'+''.join(f'<a href="#" class="sh" aria-label="Partager sur {n}">{n[0]}</a>' for n in ["Facebook","X","WhatsApp","LinkedIn"])+f'<button class="sh copy" aria-label="Copier le lien">{ico(I["link"],17,2)}</button></div></div>'
for i,(c,d,t,desc,img,cat) in enumerate(NEWS):
    txt=JAP_TXT if i==1 else f'<p>{desc}</p><p>[Texte complet de l’article.]</p>'
    others=[j for j in range(len(NEWS)) if j!=i][:3]
    fig=f'<figure class="art-fig" data-stg><img data-img="{img}" alt=""></figure>' if img else ''
    R+=route(f'article-{i+1}',t,hero([("Actualités","actualites"),(t if len(t)<40 else t[:38]+'…',None)],c,t,'',None,f'<div class="ph-meta"><span>{ico(I["cal"],17)} {d}</span></div>')+f'''
<div class="wrap with-side art"><div class="main-col" data-reveal>{fig}<div class="prose" data-stg>{txt}</div>{share}
<nav class="prevnext" data-stg><a href="#article-{(i-1)%len(NEWS)+1}" class="pn"><span><small>Précédent</small>{NEWS[(i-1)%len(NEWS)][2]}</span></a><a href="#article-{(i+1)%len(NEWS)+1}" class="pn next"><span><small>Suivant</small>{NEWS[(i+1)%len(NEWS)][2]}</span>{arrow(16)}</a></nav></div>
<aside class="side-nav" data-reveal><span class="box-h">À lire aussi</span>{''.join(f'<a href="#article-{j+1}" class="rec"><span class="rec-meta">{NEWS[j][0]} · {NEWS[j][1]}</span><span class="rec-t">{NEWS[j][2]}</span></a>' for j in others)}<a href="#actualites" class="box-link">Toutes les actualités {arrow(14)}</a></aside></div><div class="spacer"></div>''')

# ---------- Photos et vidéos ----------
gal=[("panel","Concertation autour de l’autonomisation des jeunes"),("sc","Cérémonie de sortie des volontaires du service civique"),("jap","Rencontre avec l’ambassadeur du Japon"),("afd","Échanges avec l’Agence française de Développement")]
vids=["Une histoire de réussite d’une bénéficiaire du programme Mon Projet Futur.","Bilan du secteur de l’emploi et de la formation professionnelle : lancement du programme de formation dans les établissements privés.","Cérémonie de lancement de la formation au profit de 160 jeunes, Programme National Intégré de Soutien aux Petites Entreprises."]
R+=route('medias','Photos et vidéos',hero([("Centre des médias","actualites"),("Photos et vidéos",None)],"Centre des médias","Photos et vidéos","Les temps forts du ministère en images.")+f'''
<div class="wrap sec" data-reveal><div class="sec-h"><span class="kicker">Vidéos</span><h2>Les vidéos</h2></div><div class="vids">{''.join(f'<a href="#" class="vid" data-stg><span class="vid-p"><span class="play"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7L8 5Z"></path></svg></span><span class="vid-n">[Miniature de la vidéo]</span></span><span class="vid-t">{v}</span></a>' for v in vids)}</div></div>
<div class="wrap sec" data-reveal><div class="sec-h"><span class="kicker">Photos</span><h2>Galerie photos</h2></div><div class="gal">{''.join(f'<button class="ph" data-stg data-full="{k}" aria-label="Agrandir : {c}"><img data-img="{k}" alt="{c}"><span>{c}</span></button>' for k,c in gal)}</div></div>
<div class="lightbox" hidden><button class="lb-x" aria-label="Fermer">×</button><img alt=""><p></p></div><div class="spacer"></div>''')

# ---------- Offres + document ----------
off=open(D+'off_main.html').read()
off=off.replace('href="accueil-majessc.html"','href="#accueil"').replace('href="publication.html"','href="#document"').replace('href="#contact"','href="#contact"')
off=re.sub(r'<a href="#(annonces|appels|contrats)" class="sub-tab',r'<a href="#offres-\1" class="sub-tab',off)
off=off.replace('id="annonces" class="panel"','id="p-annonces" class="panel"').replace('id="appels" class="panel"','id="p-appels" class="panel"').replace('id="contrats" class="panel"','id="p-contrats" class="panel"')
off=re.sub(r'<div class="tabs-bar">.*?</div></div>','',off,count=1,flags=re.S)
R+=route('offres','Offres et appels d’offres',off+'<div class="spacer"></div>')
pub=open(D+'pub_main.html').read()
pub=pub.replace('href="accueil-majessc.html"','href="#accueil"').replace('href="offres-et-appels-doffres.html#contrats"','href="#offres-contrats"').replace('href="offres-et-appels-doffres.html"','href="#offres"').replace('id="copy"','class="sh copy"').replace('class="sh" class="sh copy"','class="sh copy"')
pub=re.sub(r'<a href="#" class="same"','<a href="#document" class="same"',pub); pub=re.sub(r'<a href="#" class="rec"','<a href="#article-2" class="rec"',pub,count=0)
R+=route('document','Marché de développement de la plateforme tripartite Techghil',pub)

# ---------- Contact ----------
R+=route('contact','Contact',hero([("Contact",None)],"Contact","Une question ? Le ministère vous oriente.","Pour une information administrative ou une demande d’orientation, contactez le ministère.")+f'''
<div class="wrap sec contact" data-reveal>
  <div class="ct-cards">
    <div class="ct" data-stg><span class="ct-ic">{ico(I['home'],24)}</span><b>Adresse</b><span>[Adresse du ministère]<br>Nouakchott, Mauritanie</span></div>
    <div class="ct" data-stg><span class="ct-ic">{ico('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"></path>',24)}</span><b>Téléphone</b><span>[Numéro de téléphone]</span></div>
    <div class="ct" data-stg><span class="ct-ic">{ico('<rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="m3 7 9 6 9-6"></path>',24)}</span><b>E-mail</b><span>[Adresse e-mail]</span></div>
    <div class="ct" data-stg><span class="ct-ic">{ico(I['cal'],24)}</span><b>Horaires</b><span>[Jours et heures d’ouverture]</span></div>
  </div>
  <div class="ct-map" data-stg><span>[Carte d’accès au ministère]</span></div>
  <div class="ct-links" data-stg><span class="box-h">Liens utiles</span><div>{''.join(f'<a href="#{r}" class="pill">{t}</a>' for t,r in [("Agence Techghil","emploi"),("Tekwine","programmes"),("PEJ","programmes"),("Portail de la Microfinance","programmes"),("Annonces et appels d’offres","offres")])}</div></div>
</div><div class="spacer"></div>''')

# ---------- Recherche et plan du site ----------
R+=route('recherche','Recherche',hero([("Recherche",None)],"Recherche","Résultats de recherche",'<span id="q-label"></span>')+'<div class="wrap sec"><form class="filter big-f" id="sf"><label for="sq" class="sr">Rechercher</label>'+ico(I['search'],18,2)+'<input id="sq" type="search" placeholder="Rechercher sur le portail…"></form><div id="results" class="results"></div></div><div class="spacer"></div>')
plan=''.join(f'<div class="pl" data-stg><a href="#{(sub[0][1] if isinstance(sub,list) and sub else r) if sub!="MEGA" else "jeunesse"}" class="pl-h">{t}</a>'+(''.join(f'<a href="#{sr}">{st}</a>' for st,sr in sub) if sub!='MEGA' else ''.join(f'<a href="#{dr}">{dn}</a>' for dr,dn,dt,ic,subs in MEGA))+'</div>' for t,r,sub in MENU)
R+=route('plan','Plan du site',hero([("Plan du site",None)],"Navigation","Plan du site","Toutes les pages du portail.")+f'<div class="wrap sec" data-reveal><div class="plan"><div class="pl" data-stg><a href="#accueil" class="pl-h">Accueil</a></div>{plan}</div></div><div class="spacer"></div>')

# ---------------- CSS ----------------
home_css=open(D+'home_css.css').read()
for blk in [r'\.wrap\{max-width:1280px;margin:0 auto;padding:0 32px\}\n\.sr\{[^}]*\}\n']: home_css=re.sub(blk,'',home_css)
SITE_CSS=f'''
:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}
.site-header{{top:env(safe-area-inset-top,0px)!important}}
.route[hidden]{{display:none!important}}
.route{{animation:pageIn .5s cubic-bezier(.2,.7,.2,1) both}}
@keyframes pageIn{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.spacer{{height:72px}}
.page-hero{{position:relative;overflow:hidden;background:linear-gradient(120deg,{DEEP} 0%,{G} 60%,#0B5A3D 100%);color:#fff}}
.ph-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.32;filter:grayscale(.3)}}
.ph-veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,46,34,.95) 0%,rgba(5,46,34,.75) 55%,rgba(5,46,34,.4) 100%)}}
.h1g{{right:-160px;top:-220px;width:620px;height:620px;background:radial-gradient(closest-side,rgba(227,160,8,.22),rgba(0,0,0,0))}}
.h2g{{left:-200px;bottom:-300px;width:600px;height:600px;background:radial-gradient(closest-side,rgba(11,107,69,.7),rgba(0,0,0,0))}}
.ph-in{{position:relative;padding-top:48px;padding-bottom:54px;display:flex;flex-direction:column;gap:14px}}
.ph-in>*{{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}} .ph-in>*:nth-child(2){{animation-delay:.08s}} .ph-in>*:nth-child(3){{animation-delay:.16s}} .ph-in>*:nth-child(4){{animation-delay:.24s}}
.crumbs{{display:flex;flex-wrap:wrap;gap:8px 10px;font-size:13.5px;color:#9DB8AC}} .crumbs a{{color:#C7D8D0;text-decoration:none}} .crumbs a:hover{{color:#fff}} .crumbs [aria-current]{{color:#fff;font-weight:700}}
.kicker.gold{{color:{GOLD}}}
.page-hero h1{{margin:0;max-width:22em;font-size:clamp(30px,4vw,54px);line-height:1.05;font-weight:800;letter-spacing:-.045em}}
.page-hero p{{margin:0;max-width:42em;font-size:17px;line-height:1.6;color:#D6E4DD}}
.ph-meta{{display:flex;flex-wrap:wrap;gap:10px 24px;font-size:14px;color:#D6E4DD}} .ph-meta span{{display:inline-flex;align-items:center;gap:8px}} .ph-meta svg{{color:{GOLD}}}
.with-side{{display:flex;flex-wrap:wrap;gap:32px 48px;padding-top:40px;align-items:flex-start}}
.with-side .side-nav{{order:-1}}
.with-side.art .side-nav{{order:2}}
.side-nav{{flex:0 1 300px;min-width:240px;display:flex;flex-direction:column;padding:20px;border-radius:24px;border:1px solid {LINE};position:sticky;top:160px}}
.box-h{{font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:{MUTED};padding-bottom:12px}}
.sn{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 12px;border-radius:12px;color:{INK};text-decoration:none;font-weight:700;font-size:14.5px;transition:background .2s,color .2s}}
.sn:hover{{background:{SOFT};color:{G}}} .sn.on{{background:{G};color:#fff}} .sn.on svg{{color:{GOLD}}} .sn svg{{color:{G2}}}
.main-col{{flex:1 1 560px;min-width:0;display:flex;flex-direction:column;gap:28px}}
.lead-block h2,.prose h2,.h2s{{margin:0 0 12px;font-size:clamp(24px,2.4vw,32px);font-weight:800;letter-spacing:-.03em}}
.big{{font-size:clamp(18px,1.7vw,22px);line-height:1.6;color:{INK};margin:0}} .big b{{color:{G2}}}
.prose p,.prose li{{font-size:16.5px;line-height:1.8;color:{TXT}}} .prose p{{margin:0 0 16px}} .prose ul{{padding-left:20px}}
.minister{{display:flex;flex-wrap:wrap;gap:24px;align-items:center;padding:20px;border-radius:26px;background:{SOFT}}}
.minister img{{width:140px;height:160px;object-fit:cover;object-position:50% 20%;border-radius:20px}}
.minister.big img{{width:220px;height:260px}}
.minister div{{flex:1 1 260px;display:flex;flex-direction:column;gap:8px;align-items:flex-start}} .minister h3{{margin:0;font-size:26px;letter-spacing:-.03em}} .minister p{{margin:0;color:{MUTED}}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:16px}}
.cards.three{{grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));margin-top:24px}}
.card{{display:flex;flex-direction:column;gap:10px;padding:24px;border-radius:24px;border:1px solid {LINE};background:#fff;text-decoration:none;color:{INK};transition:transform .3s,box-shadow .3s,border-color .3s}}
.card:hover{{transform:translateY(-4px);box-shadow:0 18px 40px rgba(5,46,34,.10);border-color:#CFE0D7}}
.card-ic{{width:50px;height:50px;border-radius:15px;background:#E8F3EE;color:{G2};display:grid;place-items:center;transition:background .3s,color .3s}} .card:hover .card-ic{{background:{G};color:{GOLD}}}
.card .chip{{align-self:flex-start}} .card-t{{font-weight:800;font-size:18px;letter-spacing:-.015em;line-height:1.3}} .card-d{{font-size:14.5px;line-height:1.55;color:{MUTED}}}
.card-go{{margin-top:auto;padding-top:8px;display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:14px;color:{G2}}}
.chip{{padding:3px 10px;border-radius:999px;background:#FDF5E1;color:#6B4E05;font-weight:800;font-size:11.5px}}
.stats{{display:flex;flex-wrap:wrap;border-radius:24px;border:1px solid {LINE};overflow:hidden}}
.stats div{{flex:1 1 160px;padding:22px 24px;display:flex;flex-direction:column;gap:4px;border-left:1px solid {LINE}}} .stats div:first-child{{border-left:0}}
.stats b{{font-size:36px;font-weight:800;letter-spacing:-.04em;color:{G}}} .stats span{{font-size:14px;color:{MUTED}}}
.stats.wide b{{font-size:clamp(34px,4vw,52px)}}
.num-list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:10px}}
.num-list div{{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:16px;background:{SOFT}}} .num-list b{{color:{G2};font-size:14px}}
.sec{{padding-top:56px}}
.sec-h{{display:flex;flex-direction:column;gap:10px;margin-bottom:24px}} .sec-h.row{{flex-direction:row;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px 24px}}
.sec-h h2,.band h2{{margin:0;font-size:clamp(26px,2.8vw,40px);font-weight:800;letter-spacing:-.04em}}
.tlink{{display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:14.5px;color:{G2};text-decoration:none}}
.rubs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,270px),1fr));gap:14px}}
.rub{{display:flex;gap:16px;padding:22px;border-radius:22px;background:{SOFT}}} .rub div{{display:flex;flex-direction:column;gap:4px}} .rub b{{font-size:17px}} .rub span:not(.rub-ic){{font-size:14.5px;color:{MUTED};line-height:1.5}}
.rub-ic{{width:48px;height:48px;flex:none;border-radius:14px;background:{G};color:{GOLD};display:grid;place-items:center}}
.band{{margin-top:56px;background:{G};color:#fff;position:relative;overflow:hidden}}
.band-in{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:24px;padding-top:44px;padding-bottom:44px}} .band p{{margin:8px 0 0;color:#C7D8D0}}
.band-act{{display:flex;flex-wrap:wrap;gap:10px}} .btn-ghost{{border:1.5px solid rgba(255,255,255,.3);color:#fff;height:48px;border-radius:999px}}
.ncards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:20px}}
.ncard{{display:flex;flex-direction:column;border-radius:24px;overflow:hidden;border:1px solid {LINE};background:#fff;text-decoration:none;color:{INK};transition:transform .3s,box-shadow .3s}}
.ncard:hover{{transform:translateY(-4px);box-shadow:0 18px 40px rgba(5,46,34,.12)}}
.nc-img{{display:block;aspect-ratio:16/10;overflow:hidden;background:{G}}} .nc-img img{{width:100%;height:100%;object-fit:cover;transition:transform .8s ease}} .ncard:hover .nc-img img{{transform:scale(1.06)}}
.nc-img.ph{{display:grid;place-items:center;color:{GOLD}}}
.nc-b{{padding:20px 22px 24px;display:flex;flex-direction:column;gap:10px;flex:1}} .nc-meta{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12.5px;color:{MUTED}}}
.nc-t{{font-weight:800;font-size:18px;line-height:1.3;letter-spacing:-.015em}} .nc-go{{margin-top:auto;display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:14px;color:{G2}}}
.chips-f{{display:flex;flex-wrap:wrap;gap:6px;padding:5px;border-radius:16px;background:{SOFT};border:1px solid {LINE}}}
.cf{{height:40px;padding:0 16px;border-radius:12px;border:0;background:transparent;font:inherit;font-size:14px;font-weight:600;color:{MUTED};cursor:pointer;transition:background .2s,color .2s}} .cf.on{{background:{G};color:#fff;font-weight:800}}
.art-fig{{margin:0;border-radius:26px;overflow:hidden}} .art-fig img{{width:100%;display:block}}
.share{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;padding:18px 22px;border-radius:20px;background:{SOFT}}} .share>span{{font-weight:800}}
.sh-row{{display:flex;gap:8px}} .sh{{width:42px;height:42px;border-radius:50%;border:1px solid {LINE};background:#fff;color:{G};display:grid;place-items:center;cursor:pointer;font-weight:800;text-decoration:none;font-size:14px;transition:background .2s,color .2s}} .sh:hover{{background:{G};color:#fff}} .sh.done{{background:{GOLD};color:{DEEP}}}
.prevnext{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:12px}}
.pn{{display:flex;align-items:center;gap:14px;padding:18px 20px;border-radius:20px;border:1px solid {LINE};text-decoration:none;color:{INK};font-weight:700;font-size:15px;line-height:1.35;transition:border-color .2s}} .pn:hover{{border-color:{G2}}}
.pn small{{display:block;font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:{G2};margin-bottom:4px}} .pn.next{{justify-content:space-between;text-align:right}}
.rec{{display:flex;flex-direction:column;gap:5px;padding:14px 4px;border-top:1px solid {LINE};text-decoration:none;color:{INK}}} .rec-meta{{font-size:12px;font-weight:800;color:{G2}}} .rec-t{{font-weight:700;font-size:14.5px;line-height:1.45}}
.box-link{{margin-top:8px;padding-top:14px;border-top:1px solid {LINE};display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:14px;color:{G2};text-decoration:none}}
.vids{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:20px}}
.vid{{display:flex;flex-direction:column;gap:14px;text-decoration:none;color:{INK}}} .vid-p{{position:relative;aspect-ratio:16/9;border-radius:22px;background:linear-gradient(135deg,{G},{G2});display:grid;place-items:center}}
.play{{width:64px;height:64px;border-radius:50%;background:{GOLD};color:{DEEP};display:grid;place-items:center;padding-left:4px;transition:transform .3s;box-shadow:0 0 0 10px rgba(227,160,8,.18)}} .vid:hover .play{{transform:scale(1.1)}}
.vid-n{{position:absolute;right:14px;bottom:10px;font-size:11px;color:#9DB8AC}} .vid-t{{font-weight:700;font-size:16px;line-height:1.45}}
.gal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));gap:14px}}
.ph{{position:relative;padding:0;border:0;border-radius:20px;overflow:hidden;aspect-ratio:4/3;cursor:zoom-in;background:{G}}} .ph img{{width:100%;height:100%;object-fit:cover;transition:transform .6s}} .ph:hover img{{transform:scale(1.06)}}
.ph span{{position:absolute;left:0;right:0;bottom:0;padding:30px 16px 14px;background:linear-gradient(to top,rgba(5,46,34,.9),rgba(5,46,34,0));color:#fff;font:700 13.5px/1.35 inherit;text-align:left}}
.lightbox{{position:fixed;inset:0;z-index:90;background:rgba(3,30,23,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:24px;animation:pageIn .3s both}} .lightbox[hidden]{{display:none}}
.lightbox img{{max-width:min(1100px,100%);max-height:78vh;border-radius:16px}} .lightbox p{{color:#fff;margin:0;font-weight:700;text-align:center}}
.lb-x{{position:absolute;top:18px;right:18px;width:48px;height:48px;border-radius:50%;border:0;background:#fff;color:{DEEP};font-size:28px;cursor:pointer}}
.ct-cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));gap:14px}}
.ct{{display:flex;flex-direction:column;gap:8px;padding:24px;border-radius:22px;background:{SOFT}}} .ct b{{font-size:17px}} .ct span:not(.ct-ic){{color:{MUTED};line-height:1.5}}
.ct-ic{{width:50px;height:50px;border-radius:15px;background:{G};color:{GOLD};display:grid;place-items:center;margin-bottom:6px}}
.ct-map{{margin-top:16px;height:320px;border-radius:24px;background:linear-gradient(135deg,#E8F3EE,#DCEBE3);display:grid;place-items:center;color:{MUTED};font-weight:700}}
.ct-links{{margin-top:16px;padding:22px;border-radius:22px;border:1px solid {LINE}}} .ct-links div{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{padding:10px 16px;border-radius:999px;background:{SOFT};color:{G};font-weight:800;font-size:14px;text-decoration:none;transition:background .2s,color .2s}} .pill:hover{{background:{G};color:#fff}}
.help{{margin-top:56px;display:flex;flex-wrap:wrap;align-items:center;gap:18px 24px;padding:24px 28px;border-radius:24px;background:{SOFT};border:1px solid {LINE}}}
.help-ic{{width:56px;height:56px;border-radius:18px;background:{G};color:{GOLD};display:grid;place-items:center;flex:none}} .help div{{flex:1 1 300px;display:flex;flex-direction:column;gap:4px}} .help b{{font-size:18px}} .help span{{color:{MUTED};font-size:14.5px}}
.filter{{display:flex;align-items:center;gap:10px;height:54px;padding:0 18px;border-radius:14px;border:1px solid {LINE};background:{SOFT};color:{MUTED}}} .filter input{{flex:1;min-width:0;border:0;outline:0;background:transparent;font:inherit;font-size:16px;color:{INK}}}
.results{{margin-top:24px;display:flex;flex-direction:column;gap:10px}}
.res{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:18px 20px;border-radius:18px;border:1px solid {LINE};text-decoration:none;color:{INK};transition:border-color .2s}} .res:hover{{border-color:{G2}}} .res small{{display:block;font-size:12px;font-weight:800;color:{G2};margin-bottom:4px}} .res b{{font-size:16px}}
.muted{{color:{MUTED}}}
.plan{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));gap:16px}}
.pl{{display:flex;flex-direction:column;gap:8px;padding:22px;border-radius:22px;background:{SOFT}}} .pl a{{color:{TXT};text-decoration:none;font-size:14.5px}} .pl a:hover{{color:{G2}}} .pl-h{{font-weight:800;font-size:17px!important;color:{G}!important;margin-bottom:4px}}
.nav-item.is-active .nav-link{{color:{G};font-weight:800}} .nav-item.is-active .nav-link::after{{transform:scaleX(1)}}

.min-hero{{position:relative;overflow:hidden;background:linear-gradient(120deg,{DEEP} 0%,{G} 62%,#0B5A3D 100%);color:#fff}}
.mh-in{{position:relative;display:flex;flex-wrap:wrap;align-items:center;gap:40px 64px;padding-top:44px;padding-bottom:56px}}
.mh-txt{{flex:1.3 1 480px;min-width:0;display:flex;flex-direction:column;gap:16px}}
.mh-txt>*{{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}} .mh-txt>*:nth-child(2){{animation-delay:.06s}} .mh-txt>*:nth-child(3){{animation-delay:.12s}} .mh-txt>*:nth-child(4){{animation-delay:.18s}} .mh-txt>*:nth-child(5){{animation-delay:.24s}} .mh-txt>*:nth-child(6){{animation-delay:.3s}}
.min-hero h1{{margin:0;font-size:clamp(36px,4.6vw,62px);line-height:1;font-weight:800;letter-spacing:-.045em}}
.mh-role{{margin:0;max-width:30em;font-size:clamp(17px,1.6vw,20px);line-height:1.5;color:#D6E4DD;font-weight:600}}
.mh-facts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}}
.mh-facts span{{display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border-radius:14px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);font-size:14px;color:#fff}}
.mh-facts svg{{color:{GOLD};flex:none}} .mh-facts b{{color:#9DB8AC;font-weight:600}}
.mh-act{{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}}
.mh-photo{{flex:0 1 380px;position:relative;animation:rise 1s .2s cubic-bezier(.2,.7,.2,1) both}}
.mh-photo img{{position:relative;display:block;width:100%;aspect-ratio:4/4.4;object-fit:cover;object-position:50% 25%;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.35)}}
.mh-frame{{position:absolute;inset:18px -18px -18px 18px;border-radius:30px;border:2px solid {GOLD};opacity:.7}}
.mh-badge{{position:absolute;left:-22px;bottom:28px;display:flex;flex-direction:column;gap:2px;padding:14px 18px;border-radius:18px;background:#fff;color:{INK};box-shadow:0 18px 40px rgba(0,0,0,.25);animation:rise .8s .6s both, float 6s 1.4s ease-in-out infinite}}
.mh-badge small{{font-size:11.5px;font-weight:700;color:{MUTED}}} .mh-badge b{{font-size:18px;color:{G}}}
@keyframes float{{0%,100%{{translate:0 0}}50%{{translate:0 -8px}}}}
.ab-bar{{border-bottom:1px solid {LINE};background:#fff}}
.ab-in{{display:flex;gap:6px;overflow-x:auto;padding-top:12px;padding-bottom:12px;scrollbar-width:none}}
.ab{{flex:none;padding:10px 16px;border-radius:999px;font-size:14px;font-weight:700;color:{MUTED};text-decoration:none;transition:background .2s,color .2s}} .ab:hover{{color:{G}}} .ab.on{{background:{G};color:#fff}}
.hl{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:14px}}
.hl-c{{display:flex;flex-direction:column;gap:10px;padding:22px;border-radius:22px;background:{SOFT};font-size:14.5px;line-height:1.5;color:{TXT};font-weight:600}}
.hl-y{{font-size:30px;font-weight:800;letter-spacing:-.04em;color:{G}}} .hl-c.gold{{background:#FDF5E1}} .hl-c.gold .hl-y{{color:#8A6508}}
.min-sec{{display:flex;flex-wrap:wrap;gap:24px 64px;align-items:flex-start}}
.ms-h{{flex:0 1 300px;display:flex;flex-direction:column;gap:12px;position:sticky;top:170px}}
.ms-h h2{{margin:0;font-size:clamp(28px,3vw,42px);font-weight:800;letter-spacing:-.04em}}
.ms-body{{flex:1 1 560px;min-width:0;display:flex;flex-direction:column;gap:24px}}
.tl{{list-style:none;margin:0;padding:0;position:relative}}
.tl::before{{content:"";position:absolute;left:150px;top:10px;bottom:10px;width:2px;background:{LINE}}}
.tl-i{{position:relative;display:grid;grid-template-columns:130px 40px 1fr;align-items:start;padding:0 0 22px}}
.tl-d{{padding-top:16px;font-size:14px;font-weight:800;color:{G2};text-align:right}}
.tl-dot{{justify-self:center;margin-top:20px;width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid {G2};position:relative;z-index:1}}
.tl-i.first .tl-dot{{background:{GOLD};border-color:{GOLD};box-shadow:0 0 0 6px rgba(227,160,8,.2)}}
.tl-c{{display:flex;flex-direction:column;gap:8px;padding:16px 20px;border-radius:18px;border:1px solid {LINE};background:#fff;transition:transform .3s,box-shadow .3s}}
.tl-c:hover{{transform:translateX(4px);box-shadow:0 14px 30px rgba(5,46,34,.08)}}
.tl-t{{font-weight:800;font-size:16.5px;line-height:1.4}} .tl-s{{font-size:14.5px;line-height:1.55;color:{MUTED}}}
.tl-tag{{align-self:flex-start;padding:3px 10px;border-radius:999px;background:#E8F3EE;color:{G};font-size:11.5px;font-weight:800}}
.tl-award{{align-self:flex-start;display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:12px;background:#FDF5E1;color:#6B4E05;font-size:13px;font-weight:800}}
.other{{padding:22px 24px;border-radius:22px;background:{SOFT}}} .other p{{margin:0;padding:12px 0;border-top:1px solid {LINE};font-size:15px;line-height:1.6;color:{TXT}}}
.quote{{display:flex;gap:12px;margin-top:10px;padding:16px;border-radius:16px;background:#fff;color:{TXT};font-size:14.5px;line-height:1.6}} .quote svg{{color:{G2};flex:none;margin-top:2px}}
.min-band{{margin-top:64px;padding:64px 0;background:{SOFT};border-top:1px solid {LINE};border-bottom:1px solid {LINE}}}
.min-band .tl-c{{background:#fff}}
.langs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,200px),1fr));gap:14px}}
.lg{{display:flex;align-items:center;gap:16px;padding:20px;border-radius:22px;border:1px solid {LINE}}}
.lg-c{{width:56px;height:56px;border-radius:18px;background:{G};color:{GOLD};display:grid;place-items:center;font-size:20px;font-weight:800}} .lg b{{font-size:18px}}
@media (max-width:900px){{ .ms-h{{position:static}} .mh-photo{{flex:1 1 100%;max-width:420px}} }}
@media (max-width:760px){{
  .tl::before{{left:7px}} .tl-i{{grid-template-columns:28px 1fr;grid-template-areas:"dot date" ". card"}}
  .tl-d{{grid-area:date;text-align:left;padding-top:14px}} .tl-dot{{grid-area:dot;justify-self:start;margin-top:16px}} .tl-c{{grid-area:card;margin-top:8px}}
  .mh-badge{{left:12px}} .mh-frame{{inset:12px -10px -10px 12px}}
  .min-band{{padding:44px 0;margin-top:44px}}
}}

.main-nav{{position:relative}}
.site-header.nav-closing .sub{{opacity:0!important;visibility:hidden!important;pointer-events:none!important}}
.nav-in{{justify-content:flex-start!important;gap:0 30px!important}}
.nav-link{{font-size:15px!important}}
.home-l{{padding:0 2px!important;color:{G}!important}}
.nav-item.mega{{position:static}}
.sub.mega-p{{left:max(32px,calc(50% - 608px));right:max(32px,calc(50% - 608px));top:100%;min-width:0;padding:18px;border-radius:24px}}
.mega-cols{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}}
.mc{{display:flex;flex-direction:column;gap:2px;padding:8px;border-radius:18px;transition:background .2s}} .mc:hover{{background:{SOFT}}}
.sub .mc-h{{display:flex;align-items:flex-start;gap:12px;padding:10px;border-radius:14px;margin-bottom:4px}} .sub .mc-h::after{{display:none}}
.mc-ic{{width:44px;height:44px;flex:none;border-radius:14px;background:{G};color:{GOLD};display:grid;place-items:center}}
.mc-h b{{display:block;font-size:16px;color:{INK}}} .mc-h small{{display:block;font-size:12.5px;font-weight:500;color:{MUTED};margin-top:2px;line-height:1.4}}
.sub .mc-l{{padding:8px 10px;font-size:13.5px;font-weight:600;color:{TXT}}}
.sub .mega-cta{{margin-top:12px;display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-radius:16px;background:{G};color:#fff}} .sub .mega-cta::after{{display:none}}
.sub .mega-cta:hover{{background:{DEEP};color:#fff}} .mega-cta b{{display:block;font-size:15px}} .mega-cta small{{display:block;font-size:13px;color:#C7D8D0;font-weight:500}}
.mega-go{{width:40px;height:40px;border-radius:50%;background:{GOLD};color:{DEEP};display:grid;place-items:center}}
/* Programmes et projets */
.pp-top{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px 24px;padding-top:28px}}
.pp-switch{{display:inline-flex;gap:4px;padding:5px;border-radius:16px;background:{SOFT};border:1px solid {LINE}}}
.pp-switch a{{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 18px;border-radius:12px;font-weight:700;font-size:14.5px;color:{MUTED};text-decoration:none;transition:background .2s,color .2s}} .pp-switch a.on{{background:{G};color:#fff}} .pp-switch a.on svg{{color:{GOLD}}}
.pp-index{{display:flex;flex-wrap:wrap;gap:8px}} .pp-index a{{display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:999px;border:1px solid {LINE};font-size:13.5px;font-weight:700;color:{INK};text-decoration:none;transition:border-color .2s}} .pp-index a:hover{{border-color:{G2}}} .pp-index b{{color:{G2}}}
.prog{{padding-top:48px}}
.prog-h{{display:flex;flex-wrap:wrap;align-items:flex-start;gap:16px 24px;margin-bottom:24px}}
.prog-n{{font-size:clamp(56px,6vw,88px);line-height:.85;font-weight:800;letter-spacing:-.06em;color:{GOLD}}}
.prog-h>div{{flex:1 1 320px;display:flex;flex-direction:column;gap:8px}}
.prog-h h2{{margin:0;font-size:clamp(30px,3.4vw,48px);font-weight:800;letter-spacing:-.045em;line-height:1}}
.prog-ar{{margin:0;font-size:17px;color:{MUTED};font-weight:600}}
.prog-badge{{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:12px;background:#FDF5E1;color:#6B4E05;font-size:13.5px;font-weight:800}}
.prog-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px}}
.pg-box{{padding:26px 28px;border-radius:24px;background:{SOFT};display:flex;flex-direction:column;gap:12px}}
.pg-box p{{margin:0;font-size:16px;line-height:1.75;color:{TXT}}} .pg-box b{{color:{INK}}}
.pg-box.green{{background:{G};color:#fff}} .pg-box.green p{{color:#D6E4DD}} .pg-box.green .pg-k{{color:{GOLD}}}
.pg-box.white{{background:#fff;border:1px solid {LINE}}}
.pg-k{{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:{G2}}}
.pg-quote{{font-size:clamp(19px,1.8vw,23px)!important;line-height:1.45!important;font-weight:700;color:{G}!important;padding-left:16px;border-left:3px solid {GOLD}}}
.pg-tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}} .pg-tags span{{padding:6px 12px;border-radius:999px;background:rgba(227,160,8,.16);color:#8A6508;font-size:13px;font-weight:800}} .pg-box.green .pg-tags span{{background:rgba(255,255,255,.1);color:#fff}}
.obj{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}} .obj li{{display:flex;gap:12px;font-size:15px;line-height:1.6;color:{TXT}}}
.ok{{width:24px;height:24px;flex:none;border-radius:50%;background:{G};color:{GOLD};display:grid;place-items:center;margin-top:1px}}
.prog-band{{margin-top:56px;padding-bottom:56px;background:{SOFT};border-top:1px solid {LINE};border-bottom:1px solid {LINE}}}
.prog-band .pg-box:not(.white){{background:#fff;border:1px solid {LINE}}}
.pj-sum{{margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));border-radius:24px;border:1px solid {LINE};overflow:hidden}}
.pj-sum div{{padding:22px 24px;display:flex;flex-direction:column;gap:4px;border-left:1px solid {LINE}}} .pj-sum div:first-child{{border-left:0}}
.pj-sum b{{font-size:clamp(26px,2.6vw,36px);font-weight:800;letter-spacing:-.04em;color:{G}}} .pj-sum span{{font-size:14px;color:{MUTED}}}
.pjs{{display:flex;flex-direction:column;gap:24px;margin-top:28px}}
.pj{{display:flex;flex-wrap:wrap;border-radius:28px;border:1px solid {LINE};overflow:hidden;background:#fff;scroll-margin-top:150px}}
.pj-side{{flex:1 1 360px;min-width:0;position:relative;padding:30px;background:linear-gradient(150deg,{G} 0%,{DEEP} 100%);color:#fff;display:flex;flex-direction:column;gap:12px}}
.pj-partner{{align-self:flex-start;padding:7px 14px;border-radius:999px;background:{GOLD};color:{DEEP};font-size:12.5px;font-weight:800}}
.pj-n{{position:absolute;right:24px;top:18px;font-size:64px;font-weight:800;letter-spacing:-.06em;color:rgba(255,255,255,.08);line-height:1}}
.pj-side h2{{margin:4px 0 0;font-size:clamp(21px,2vw,26px);line-height:1.25;font-weight:800;letter-spacing:-.025em}}
.pj-short{{font-size:14px;color:#9DB8AC;font-weight:700}}
.pj-facts{{margin-top:auto;padding-top:14px;display:grid;gap:10px}}
.pj-facts div{{display:grid;grid-template-columns:40px 1fr;grid-template-rows:auto auto;column-gap:12px;align-items:center;padding:12px 14px;border-radius:16px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12)}}
.f-ic{{grid-row:span 2;width:40px;height:40px;border-radius:12px;background:rgba(227,160,8,.18);color:{GOLD};display:grid;place-items:center}}
.pj-facts small{{font-size:12px;color:#9DB8AC}} .pj-facts b{{font-size:17px}}
.pj-main{{flex:1.6 1 480px;min-width:0;padding:28px 30px;display:flex;flex-direction:column;gap:20px}}
.pj-o{{display:flex;flex-direction:column;gap:8px}} .pj-o p{{margin:0;font-size:15.5px;line-height:1.7;color:{TXT}}}
.pj-split{{display:flex;gap:10px;margin-top:4px}} .pj-split span{{display:flex;align-items:baseline;gap:6px;padding:10px 14px;border-radius:14px;background:{SOFT};font-size:14px;color:{MUTED}}} .pj-split b{{font-size:22px;color:{G}}}
.zones{{display:flex;flex-wrap:wrap;gap:8px}} .zones span{{display:inline-flex;align-items:center;gap:6px;padding:8px 13px;border-radius:999px;background:#E8F3EE;color:{G};font-size:13.5px;font-weight:700}}
@media (max-width:1279px){{
  .nav-in{{gap:0!important}} .home-l{{display:none!important}}
  .nav-item.mega{{position:relative}} .sub.mega-p{{padding:4px 0 8px 14px}}
  .mega-cols{{grid-template-columns:1fr}} .mc{{padding:0}} .sub .mc-h{{padding:8px 0}} .mc-ic{{width:34px;height:34px;border-radius:10px}} .mc-h small{{display:none}}
  .sub .mega-cta{{display:none}}
}}
@media (max-width:760px){{ .pj-sum div{{border-left:0;border-top:1px solid {LINE}}} .pj-sum div:first-child{{border-top:0}} .pg-box,.pj-main,.pj-side{{padding:22px}} .prog-band{{margin-top:40px}} }}

/* En-tête sur une ligne */
.head-row{{min-height:84px!important;gap:12px 24px!important;flex-wrap:nowrap}}
.head-row .brand{{flex:none}} .head-row .brand .b2{{max-width:300px!important;font-size:13px!important}}
.main-nav{{border-top:0!important;position:static!important;margin-left:auto}}
.main-nav .nav-in{{display:flex;flex-wrap:nowrap;align-items:stretch;gap:0 20px!important;padding:0;justify-content:flex-end!important}}
.main-nav .nav-link{{min-height:84px;font-size:15px!important;padding:0 1px}}
.head-act{{display:flex;align-items:center;gap:8px;flex:none}}
.s-btn{{width:44px;height:44px;border-radius:50%;border:1px solid {LINE};background:#fff;color:{G};display:grid;place-items:center;cursor:pointer;transition:background .2s,color .2s}}
.s-btn:hover,.s-btn[aria-expanded="true"]{{background:{G};color:#fff}}
.search-panel{{border-top:1px solid {LINE};background:#fff}}
.search-panel:not([hidden]){{animation:rise .3s ease both}}
.search-panel .wrap{{padding-top:14px;padding-bottom:16px}}
.head-search{{display:flex!important;flex:1 1 auto!important;max-width:none!important;height:56px!important;padding:0 8px 0 18px!important;border-radius:16px!important}}
.hs-go{{height:42px;padding:0 18px;border:0;border-radius:12px;background:{G};color:#fff;font:inherit;font-weight:800;font-size:14px;cursor:pointer}}
.sub.mega-p{{top:calc(100% - 3px)!important}}
@media (max-width:1320px){{ .main-nav .nav-in{{gap:0 16px!important}} .main-nav .nav-link{{font-size:14.5px!important}} }}
@media (max-width:1279px){{
  .head-row{{flex-wrap:wrap;min-height:76px!important}}
  .head-row .brand{{flex:1 1 0;min-width:0}} .head-row .brand .b2{{max-width:420px!important}}
  .main-nav{{display:none;order:3;width:100%;margin-left:0}}
  .site-header.menu-open .main-nav{{display:block;max-height:calc(100vh - 110px);overflow:auto;padding-bottom:12px}}
  .main-nav .nav-in{{flex-direction:column;gap:0!important;justify-content:flex-start!important}}
  .main-nav .nav-link{{min-height:52px;border-bottom:1px solid {SOFT}}}
  .main-nav .nav-link::after{{display:none}}
  .burger{{display:flex}}
}}
@media (max-width:480px){{
  .head-row{{gap:10px!important}}
  .brand{{gap:10px}} .brand img{{width:40px!important;height:40px!important}} .brand-txt{{padding-left:10px}}
  .head-row .brand .b2{{font-size:11px!important;line-height:1.25!important;max-width:none!important}}
  .s-btn,.burger{{width:42px;height:42px}}
  .topbar-in>span:first-child{{display:none}} .topbar-in{{justify-content:flex-end}}
  .head-search{{height:50px!important}} .hs-go{{padding:0 12px}}
}}

/* Responsive renforcé */
@media (max-width:1279px){{
  .hero [aria-label="Chiffres clés du secteur"]{{flex-direction:row!important;flex-wrap:wrap;flex-basis:100%!important}}
  .hero .badge{{align-self:auto!important;margin-right:0!important;flex:1 1 190px;min-width:0}}
  .hero .badge span{{white-space:normal!important}}
}}
@media (max-width:1000px){{
  [style*="max-width: 440px"]{{max-width:none!important;min-height:380px!important}}
}}
@media (max-width:760px){{
  [role="tablist"]:has(.tab){{flex-wrap:nowrap!important;overflow-x:auto;max-width:100%;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
  [role="tablist"]:has(.tab)::-webkit-scrollbar{{display:none}}
  .tab{{flex:none;white-space:nowrap}}
  .hero .badge{{flex-basis:100%}}
  .pp-index{{flex-wrap:nowrap;overflow-x:auto;max-width:100%;scrollbar-width:none}} .pp-index a{{flex:none}}
  .pp-switch{{width:100%}} .pp-switch a{{flex:1;justify-content:center}}
  .hl{{grid-template-columns:repeat(2,minmax(0,1fr))}} .hl-c{{padding:16px}} .hl-y{{font-size:24px}}
  .page-hero h1,.min-hero h1{{font-size:clamp(28px,8vw,40px)}}
  .doc-title{{font-size:15px}}
  .help{{padding:20px}} .help .btn{{width:100%;justify-content:center}}
}}
@media (max-width:420px){{
  .hero form button{{font-size:0!important;padding:0 14px!important}}
  .hero form button::before{{content:"OK";font-size:15px}}
  .hl{{grid-template-columns:1fr}}
  .wrap{{padding-left:16px!important;padding-right:16px!important}}
}}

/* v3 : en-tête avec Accueil, sans bandes tricolores */
.stripe{{display:none!important}}
.site-header{{border-bottom:1px solid {LINE}}}
.main-nav .nav-in{{gap:0 18px!important}}
@media (min-width:1280px){{ .head-row .brand .b2{{max-width:240px!important;font-size:12.5px!important}} .main-nav .nav-in{{gap:0 12px!important}} .main-nav .nav-link{{font-size:14.5px!important}} .head-row{{gap:12px 18px!important}} }}
.site-footer{{border-top:3px solid {GOLD}}}
@media (max-width:1340px) and (min-width:1280px){{ .main-nav .nav-in{{gap:0 12px!important}} .main-nav .nav-link{{font-size:14px!important}} .head-row .brand .b2{{max-width:235px!important;font-size:12px!important}} .head-row{{gap:12px 16px!important}} }}
/* v3 : photos 100 % responsives sur mobile */
img{{max-width:100%}}
@media (max-width:760px){{
  .hero{{flex-direction:column!important;align-items:stretch!important;min-height:0!important}}
  .hero>img{{position:relative!important;inset:auto!important;width:100%!important;height:auto!important;aspect-ratio:16/10;object-position:50% 35%!important;order:-1;translate:none!important;animation:none!important;transform:none!important}}
  .hero>[aria-hidden="true"]:not(img){{display:none!important}}
  .hero>div:not([aria-hidden]){{padding-top:28px!important}}
  .page-hero{{display:flex;flex-direction:column}}
  .page-hero .ph-img{{position:relative;inset:auto;order:-1;width:100%;height:auto;aspect-ratio:16/9;opacity:1;filter:none}}
  .page-hero .ph-veil{{display:none}}
  .np.is-open{{height:auto!important;display:flex;flex-direction:column;align-items:stretch}}
  .np.is-open .np-img{{position:relative;inset:auto;width:100%;height:auto;aspect-ratio:16/10;transform:none}}
  .np.is-open .np-veil{{display:none}}
  .np.is-open .np-open{{background:{G}}}
  .np-prog{{z-index:3}}
  .mh-photo{{flex:1 1 100%!important;max-width:100%!important}}
  .mh-frame{{display:none}}
  .mh-photo img{{aspect-ratio:1/1}}
  .mh-badge{{left:12px;bottom:12px}}
  .minister img{{width:100%;height:auto;aspect-ratio:4/3.4}}
  .art-fig img{{width:100%;height:auto}}
  .nc-img,.ph,.vid-p{{width:100%}}
}}

/* v4 : pied de page responsive */
.f-top .brand{{min-width:0;flex:1 1 320px}}
.f-top .brand-txt{{min-width:0}}
.f-top .brand .b2{{overflow-wrap:break-word}}
@media (max-width:760px){{
  .site-footer .f-top{{flex-direction:column!important;align-items:stretch!important;gap:18px!important;padding:20px!important}}
  .site-footer .f-top .brand{{flex:none!important;width:100%;gap:12px}}
  .site-footer .f-top .brand img{{width:48px!important;height:48px!important}}
  .site-footer .f-top .brand-txt{{padding-left:12px;flex:1;min-width:0}}
  .site-footer .f-top .brand .b2{{max-width:none!important;font-size:13.5px!important;line-height:1.35!important}}
  .site-footer .f-top .btn-gold{{width:100%;justify-content:center}}
  .site-footer .f-cols{{gap:28px 24px!important;padding:32px 0 28px!important}}
  .site-footer .f-cols nav{{flex:1 1 140px!important}}
  .site-footer .f-bottom{{flex-direction:column;align-items:flex-start;padding:18px 0!important}}
  .site-footer .f-legal{{gap:10px 16px}}
}}
@media (max-width:380px){{ .site-footer .f-cols nav{{flex-basis:100%!important}} }}
@media (max-width:1000px){{ .side-nav{{position:static;flex:1 1 100%}} .with-side .side-nav{{order:-1}} }}
@media (max-width:760px){{ .spacer{{height:48px}} .ph-in{{padding-top:34px;padding-bottom:38px}} .sec{{padding-top:40px}} .stats div{{border-left:0;border-top:1px solid {LINE}}} .stats div:first-child{{border-top:0}} .minister.big img{{width:100%;height:280px}} }}
'''
oc=open(D+'off_css.css').read(); pc=open(D+'pub_css.css').read()
# éviter les doublons de règles des gabarits de page
for c in ['.page-hero{','.h1g{','.h2g{','.ph-in{','.ph-in>*{','.crumbs{','.kicker.gold{','.page-hero h1{','.page-hero p{','.ph-meta{','.help{','.help-ic{','.help div{','.share{','.share>span{','.sh-row{','.sh{','.sh:hover{','.sh.done{','.prevnext{','.pn{','.pn:hover{','.pn small{','.pn.next{','.box-link{','.rec{','.rec-meta{','.rec-t{','.rec:hover']:
    pass
ALLCSS=CSS+home_css.replace(CSS[CSS.index('/* Bandeau du haut */'):CSS.index('/* Commun */')],'')+oc+pc+SITE_CSS

# ---------------- JS ----------------
home_js=open(D+'home_js.js').read()
off_js=r'''
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
'''
INDEX=[]
for t,r,sub in MENU:
    if sub=='MEGA':
        for dr,dn,dt,ic,subs in MEGA:
            INDEX.append(dict(t=dn,r=dr,c='Domaine'))
            for x in subs: INDEX.append(dict(t=x,r=dr,c=dn))
        continue
    INDEX.append(dict(t=t,r=(sub[0][1] if sub else r),c='Rubrique'))
    for st,sr in sub: INDEX.append(dict(t=st,r=sr,c=t))
for i,n in enumerate(NEWS): INDEX.append(dict(t=n[2],r=f'article-{i+1}',c='Actualité'))
for m in re.finditer(r'class="doc-title">([^<]+)</span>',off): INDEX.append(dict(t=H.unescape(m.group(1)),r='document',c='Document'))
for t,r in PR: INDEX.append(dict(t=t,r=r,c='Programme' if r=='programmes' else 'Projet'))
router=r'''
(function(){
  var IMG=__IMG__, INDEX=__INDEX__;
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
'''.replace('__IMG__',json.dumps(IM)).replace('__INDEX__',json.dumps(INDEX,ensure_ascii=False))

body=header()+'\n<main id="contenu">\n'+R+'</main>\n'+footer()
body=re.sub(r'<div class="stripe" aria-hidden="true">.*?</div>','',body)
body=re.sub(r'<div aria-hidden="true" style="(?:position: absolute; left: 0; right: 0; bottom: 0; )?height: [356]px; display: flex">(?:<div style="flex: \d+; background: [^"]+"></div>)+</div>','',body)
body=body.replace('<path d="M12 21s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 8a4.3 4.3 0 0 1 7.5 2.8C19.5 16.4 12 21 12 21Z"></path>','<path d="M5 21V4"></path><path d="M5 4h12.5l-2.5 4.5L17.5 13H5"></path>')
# remplacer toute image intégrée restante par une référence
rev={v:k for k,v in IM.items()}
def rep(m):
    k=rev.get(m.group(1)); return f'data-img="{k}"' if k else m.group(0)
body=re.sub(r'src="(data:image/[^"]+)"',rep,body)
assert 'base64' not in body, 'image encore intégrée'
JSALL=home_js+off_js+router
page=f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique</title>
<link rel="icon" href="data:,">
{FONT}
<style>{ALLCSS}</style>
</head>
<body>
{body}
<script>{JSALL}</script>
</body>
</html>'''
OUT=os.path.join(BASE,'..','..','dist'); os.makedirs(OUT,exist_ok=True)
open(os.path.join(OUT,'site-majessc.html'),'w').write(page)
print('Fichier unique :',os.path.join(OUT,'site-majessc.html'))
print(len(page)//1024,'Ko', len(re.findall('class="route"',page)),'pages')
