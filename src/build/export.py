"""Découpe dist/site-majessc.html en site statique : public/index.html + assets/."""
import re, base64, json, os
BASE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(BASE,'..','..')
h=open(os.path.join(ROOT,'dist','site-majessc.html'),encoding='utf-8').read()
P=os.path.join(ROOT,'public')
for d in ['assets/css','assets/js','assets/img']: os.makedirs(os.path.join(P,d),exist_ok=True)
css=h[h.index('<style>')+7:h.index('</style>')]
js=h[h.rindex('<script>')+8:h.rindex('</script>')]
m=re.search(r'var IMG=(\{.*?\}), INDEX=',js,re.S); IMG=json.loads(m.group(1))
names={'panel':'conference-nationale.jpg','sc':'service-civique.jpg','jap':'cooperation-japon.jpg','afd':'cooperation-afd.jpg','min':'ministre.jpg','seal':'sceau-mauritanie.svg'}
paths={}
for k,v in IMG.items():
    fn=names.get(k,k); open(os.path.join(P,'assets/img',fn),'wb').write(base64.b64decode(v.split(',',1)[1])); paths[k]='assets/img/'+fn
js=js[:m.start(1)]+json.dumps(paths)+js[m.end(1):]
open(os.path.join(P,'assets/css/style.css'),'w',encoding='utf-8').write(css.strip()+'\n')
open(os.path.join(P,'assets/js/main.js'),'w',encoding='utf-8').write(js.strip()+'\n')
body=h[h.index('<body>')+6:h.rindex('<script>')]
head=h[:h.index('<style>')].replace('<link rel="icon" href="data:,">','<link rel="icon" href="assets/img/sceau-mauritanie.svg" type="image/svg+xml">')
head=head.replace('<meta name="viewport"','<meta name="description" content="Portail officiel du Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique – République Islamique de Mauritanie.">\n<meta name="viewport"')
open(os.path.join(P,'index.html'),'w',encoding='utf-8').write(head+'<link rel="stylesheet" href="assets/css/style.css">\n</head>\n<body>'+body+'<script src="assets/js/main.js"></script>\n</body>\n</html>\n')
print('Site statique généré dans', os.path.abspath(P))
