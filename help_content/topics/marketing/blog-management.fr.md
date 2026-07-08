---
title: Gestion du blog
---

Le blog vous permet de publier des articles, des guides et des actualités afin d'attirer du trafic et d'engager votre audience. Le blog de Spwig inclut un éditeur de texte enrichi, une publication planifiée, des notifications aux abonnés, une partage automatique sur les réseaux sociaux et des outils SEO.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Création d’un article de blog

Accédez à **Marketing > Articles de blog** et cliquez sur **Ajouter un article**.

### Contenu de l’article

Rédigez votre article à l’aide de l’éditeur de texte enrichi **CKEditor 5**, qui prend en charge :
- Le formatage du texte (titres, gras, italique, listes, citations)
- Les images et médias (téléchargés via la bibliothèque multimédia)
- Les vidéos intégrées (YouTube, Vimeo)
- Les tableaux et blocs de code
- Les liens vers des produits, des catégories et des URLs externes

Pour des dispositions plus complexes, activez l’interrupteur **Page Builder** pour utiliser le constructeur de pages glisser-déposer au lieu de l’éditeur de texte.

### Paramètres de l’article

| Paramètre | Description |
|---------|-------------|
| **Titre** | Le titre principal affiché sur le blog et dans les résultats de recherche |
| **Slug** | Identifiant convivial pour l’URL (généré automatiquement à partir du titre, modifiable) |
| **Extrait** | Résumé court affiché sur les cartes de liste du blog et les flux RSS |
| **Image mise en avant** | Image principale affichée en haut de l’article et sur les cartes de liste |
| **Catégorie** | Catégorie principale de l’article |
| **Tags** | Mots-clés pour le filtrage et le contenu lié |
| **Auteur** | Membre du personnel crédité comme auteur |
| **Statut** | Brouillon, Planifié, Publié ou Archivé |
| **Mettre en avant** | Fixer l’article en haut de la liste du blog |

### Paramètres SEO

Chaque article inclut des champs SEO :
- **Titre meta** — Titre personnalisé pour les résultats des moteurs de recherche (par défaut, le titre de l’article)
- **Description meta** — Résumé affiché dans les résultats des moteurs de recherche
- **Image Open Graph** — Image utilisée lors du partage de l’article sur les réseaux sociaux

## États des articles

| État | Description |
|--------|-------------|
| **Brouillon** | Travail en cours, non visible au public |
| **Planifié** | Sera publié automatiquement à une date et heure définies |
| **Publié** | En ligne et visible pour les visiteurs |
| **Archivé** | Caché dans la liste du blog mais toujours accessible via l’URL directe |

### Planification des articles

Pour planifier la publication d’un article à un moment futur :
1. Définissez le statut sur **Planifié**
2. Choisissez la **date et l’heure de publication**
3. Enregistrez l’article

Une tâche en arrière-plan publie automatiquement l’article à l’heure planifiée et déclenche les notifications aux abonnés.

## Catégories

Accédez à **Marketing > Catégories de blog** pour organiser votre contenu.

Les catégories prennent en charge :
- **Hiérarchie** — Créez des catégories parentes et enfants (par exemple, « Guides » > « Getting Started »)
- **URLs personnalisées** — Chaque catégorie a son propre slug pour des URLs propres
- **Descriptions** — Ajoutez des descriptions de catégories affichées sur la page d’archives de la catégorie
- **Tri** — Contrôlez l’ordre d’affichage des catégories dans la navigation

## Tags

Les tags offrent un moyen secondaire de classer le contenu. Contrairement aux catégories (qui sont hiérarchiques), les tags sont des étiquettes plates. Les visiteurs peuvent cliquer sur un tag pour voir tous les articles associés à ce tag.

## Abonnés

Accédez à **Marketing > Abonnés du blog** pour gérer votre liste d’abonnés.

### Fonctionnement des abonnements

1. Les visiteurs s’abonnent via un formulaire sur le blog (adresse e-mail obligatoire)
2. Un e-mail de **confirmation double opt-in** est envoyé
3. Une fois confirmé, l’abonné reçoit des notifications lors de la publication d’articles nouveaux

### Fréquence des notifications

Les abonnés choisissent la fréquence à laquelle ils reçoivent les notifications :

| Fréquence | Description |
|-----------|-------------|
| **Immédiat** | E-mail envoyé dès qu’un nouvel article est publié |
| **Résumé hebdomadaire** | Un résumé hebdomadaire de tous les nouveaux articles |
| **Résumé mensuel** | Un résumé mensuel de tous les nouveaux articles |

Les tâches en arrière-plan gèrent automatiquement la compilation et la livraison des résumés.

### Gestion des abonnés

- Affichez le nombre d’abonnés, le statut de confirmation et la date d’inscription
- Exportez les listes d’abonnés pour les utiliser dans des outils de marketing par e-mail externes
- Supprimez ou désabonnez des adresses individuelles
- Chaque e-mail de notification inclut un lien de **désabonnement** en un clic

## Partage automatique sur les réseaux sociaux

Spwig peut partager automatiquement de nouveaux articles sur vos comptes de réseaux sociaux lorsqu’ils sont publiés.

### Connexion aux comptes sociaux

Accédez à **Marketing > Connecteurs sociaux** pour connecter vos comptes :

| Plateforme | Authentification |
|----------|---------------|
| **Facebook** | OAuth — connectez votre Page Facebook |
| **Instagram** | OAuth — connectez votre compte professionnel |
| **LinkedIn** | OAuth — connectez votre page entreprise |

### Fonctionnement du partage automatique

1. Connectez un ou plusieurs comptes sociaux
2. Lors de la création d’un article, activez **Partage automatique** pour chaque compte connecté
3. Personnalisez le message de partage (par défaut, le titre de l’article et l’extrait)
4. Lorsque l’article est publié (ou atteint l’heure planifiée), il est automatiquement partagé

Le partage automatique fonctionne également avec les articles planifiés — le partage sur les réseaux sociaux est envoyé au même moment que la publication de l’article.

## Flux RSS

Le blog génère automatiquement un flux RSS à l’adresse `/blog/feed/`. Cela permet aux visiteurs et aux agrégateurs de s’abonner à votre contenu. Le flux inclut :
- Le titre et l’extrait de l’article
- La date de publication
- Les informations sur l’auteur
- Le lien direct vers l’article complet

## Paramètres du blog

Accédez à **Marketing > Paramètres du blog** pour configurer les options globales du blog :

- **Nombre d’articles par page** — Nombre d’articles affichés par page dans la liste
- **Permettre les commentaires** — Activer ou désactiver les commentaires sur les articles
- **Catégorie par défaut** — Catégorie de secours pour les articles sans catégorie assignée
- **Boutons de partage sociaux** — Afficher les boutons de partage sur les pages d’articles individuels

## Conseils

- Rédigez des articles en pensant à l’**optimisation pour les moteurs de recherche** — utilisez des titres descriptifs, remplissez les descriptions meta et incluez naturellement des mots-clés pertinents dans le contenu.
- Utilisez la **publication planifiée** pour maintenir un rythme de publication régulier sans effort manuel.
- Activez le **partage automatique** pour maximiser votre portée — les articles partagés sur les réseaux sociaux peu de temps après leur publication obtiennent le plus d’engagement.
- Encouragez les visiteurs à **s’abonner** en plaçant le formulaire d’abonnement en évidence sur votre blog et en utilisant un appel à l’action percutant.
- Utilisez les **catégories** pour regrouper le contenu de manière large et les **tags** pour des sujets spécifiques — cela aide les visiteurs à trouver du contenu lié.
- Ajoutez une **image mise en avant** à chaque article — les articles avec des images obtiennent de meilleures performances dans les résultats de recherche et les partages sur les réseaux sociaux.
- Utilisez l’option de **résumé hebdomadaire ou mensuel** pour les abonnés qui ne souhaitent pas recevoir des e-mails fréquents — cela réduit les taux de désabonnement.