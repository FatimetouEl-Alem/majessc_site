# Portail MAJESSC

Site du **Ministère de l’Autonomisation des Jeunes, de l’Emploi, des Sports et du Service Civique** – République Islamique de Mauritanie.

Site statique (HTML, CSS, JavaScript) : aucune base de données ni serveur applicatif n’est nécessaire.

## Structure du dépôt

```
majessc-portail/
├── public/                    ← SITE À DÉPLOYER
│   ├── index.html             toutes les pages du site
│   └── assets/
│       ├── css/style.css      design, animations, responsive
│       ├── js/main.js         navigation, menu, recherche, filtres, animations
│       └── img/               photos et sceau national
├── src/                       ← SOURCES DE CONCEPTION
│   ├── build/                 scripts de génération du site
│   │   ├── build.py           contenu des pages, menu, styles → dist/site-majessc.html
│   │   ├── export.py          découpe en site statique → public/
│   │   ├── common.py          en-tête, pied de page, couleurs, icônes
│   │   └── *.html / *.css / *.js   blocs de la page d’accueil et des pages Offres
│   └── images/                images sources
├── design/maquettes-html/     maquettes autonomes (un seul fichier chacune)
│   ├── site-majessc.html      site complet en un fichier
│   ├── accueil-majessc.html   page d’accueil seule
│   ├── offres-et-appels-doffres.html
│   └── publication.html
├── netlify.toml               configuration Netlify
└── .github/workflows/         déploiement automatique GitHub Pages
```

## Pages

| Rubrique | Adresse |
| --- | --- |
| Accueil | `#accueil` |
| Le Ministère | `#a-propos`, `#ministre`, `#cabinet`, `#secretariat`, `#directions`, `#etablissements` |
| Domaines | `#jeunesse`, `#emploi`, `#sports`, `#service-civique` |
| Programmes et projets | `#programmes`, `#projets` |
| Actualités | `#actualites`, `#article-1` à `#article-5`, `#medias` |
| Appels d’offres | `#offres`, `#offres-annonces`, `#offres-appels`, `#offres-contrats`, `#document` |
| Autres | `#contact`, `#recherche`, `#plan` |

## Mettre le projet sur Git

```bash
cd majessc-portail
git init
git add .
git commit -m "Portail MAJESSC : première version"
git branch -M main
git remote add origin <URL_DU_DEPOT>
git push -u origin main
```

## Déployer

Le dossier à publier est **`public/`**.

- **Serveur web (Apache, Nginx, IIS)** : copier le contenu de `public/` à la racine du site.
- **GitHub Pages** : dans *Settings → Pages*, choisir la source *GitHub Actions*. Chaque `git push` sur `main` déploie automatiquement.
- **Netlify** : importer le dépôt ; `netlify.toml` indique déjà le dossier `public`.
- **Test local** : `cd public && python3 -m http.server 8000`, puis ouvrir http://localhost:8000.

Les polices (Plus Jakarta Sans, Noto Kufi Arabic) sont chargées depuis Google Fonts.

## Modifier le site

Deux possibilités :

1. **Directement** dans `public/index.html`, `public/assets/css/style.css` et `public/assets/js/main.js`.
2. **Avec les sources** (Python 3, sans dépendance externe) :
   ```bash
   python3 src/build/build.py    # génère dist/site-majessc.html
   python3 src/build/export.py   # met à jour public/
   ```
   Attention : cette méthode régénère `public/` et remplace les modifications faites directement dans ce dossier.

## Charte graphique

| Élément | Valeur |
| --- | --- |
| Vert profond | `#063B2C` · `#052E22` |
| Vert | `#0B6B45` |
| Doré | `#E3A008` |
| Fond clair | `#F5F8F6` · traits `#E2E8E5` |
| Texte | `#0B1F18` · secondaire `#56665F` |
| Police | Plus Jakarta Sans (arabe : Noto Kufi Arabic) |

## À compléter avant la mise en production

- Les textes entre crochets `[ … ]` : coordonnées, directions centrales, établissements sous tutelle, textes d’articles, miniatures vidéo.
- Les liens vers les PDF officiels et les plateformes partenaires.
- La photo officielle du Ministre en haute définition.
- La version arabe du site.

## Intégration Drupal

Chaque bloc `<div class="route" data-route="…">` de `public/index.html` correspond à une page ou à un type de contenu à reproduire dans un thème Drupal ; `style.css` et `main.js` peuvent être repris comme bibliothèques du thème.
