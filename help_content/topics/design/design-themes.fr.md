---
title: Conception et Thèmes
---

Le système de conception et de thèmes vous permet de contrôler l'apparence de votre magasin — des couleurs et de la typographie aux en-têtes, pieds de page et mises en page de page. Accédez à **Paramètres > Conception et Thèmes** pour ouvrir le tableau de bord de conception.

![Tableau de bord de conception](/static/core/admin/img/help/design-themes/theme-dashboard.webp)

## Tableau de bord de conception

Le tableau de bord vous donne un aperçu de l'état de la conception de votre magasin :

- **Thème actif** — Affiche quel thème est actuellement appliqué, avec un aperçu et des boutons d'accès rapide
- **Statistiques de conception** — Nombre de thèmes installés, d'en-têtes personnalisés, de pieds de page et de menus
- **Cartes de section** — Accédez aux Thèmes, Constructeur d'en-tête, Constructeur de pied de page, Menus ou Annonces

## Thèmes

### Navigation dans les thèmes

Cliquez sur la carte de section **Thèmes** pour voir tous les thèmes installés. Chaque carte de thème affiche :
- Nom du thème et image de prévisualisation
- Auteur et version
- Statut actif/inactif

### Activation d'un thème

1. Cliquez sur **Activer** sur le thème que vous souhaitez utiliser
2. Le thème est appliqué immédiatement à votre magasin
3. Un seul thème peut être actif à la fois

### Personnalisation du thème

Chaque thème propose un ensemble de **tokens de conception** — valeurs configurables qui contrôlent l'apparence visuelle sans modifier le code.

Cliquez sur **Personnaliser** sur votre thème actif pour accéder à l'éditeur de tokens. Les catégories de tokens disponibles comprennent :

| Catégorie | Ce qu'elle contrôle |
|----------|--------------------|
| **Couleurs** | Couleurs principales, secondaires, accent, arrière-plan, couleurs du texte |
| **Typographie** | Familles de polices, tailles, poids, hauteurs de ligne |
| **Espaces** | Marges, espacement, écarts entre les éléments |
| **Bords** | Largeurs des bords, rayons, couleurs |
| **Ombres** | Ombres de cases, boutons, boîtes modales |
| **Boutons** | Styles de bouton, tailles, effets de survol |
| **Mise en page** | Largeurs des conteneurs, écarts de grille, points de rupture |

Les modifications sont visibles en temps réel avant que vous ne les enregistriez.

## Constructeur d'en-tête

Le Constructeur d'en-tête vous permet de concevoir l'en-tête de votre magasin à l'aide d'une interface glisser-déposer.

### Création d'un en-tête

1. Accédez à **Conception > Constructeur d'en-tête**
2. Cliquez sur **Créer un en-tête** ou éditez-en un existant
3. Le constructeur dispose de trois lignes : **Barre supérieure**, **En-tête principal** et **Barre inférieure**
4. Glissez les widgets de la boîte d'outils dans n'importe quelle ligne

### Widgets d'en-tête disponibles

- **Logo** — Votre logo de magasin avec une taille et un lien configurables
- **Menu de navigation** — Menu déroulant provenant de vos menus définis
- **Champ de recherche** — Recherche de produits avec des résultats instantanés
- **Icône du panier** — Mini-panier avec un badge de nombre d'articles
- **Icône du compte** — Menu déroulant de connexion/comppte
- **Sélecteur de langue** — Sélecteur de langue pour les magasins multilingues
- **Sélecteur de devise** — Sélecteur de devise pour les magasins multidevise
- **Sélecteur de livraison** — Permet aux clients de choisir leur pays de livraison, modifiant ainsi leur région de vente (et leur devise, pour les magasins multidevise). Consultez le guide **Disponibilité des régions** pour plus de détails
- **HTML personnalisé** — Ajoutez n'importe quel contenu personnalisé
- **Icônes sociales** — Lien vers vos profils médias sociaux
- **Bandeau d'annonce** — Messages promotionnels et offres

### Paramètres d'en-tête

Chaque modèle d'en-tête dispose de paramètres globaux :
- **En-tête collant** — L'en-tête reste visible lors du défilement
- **Mode transparent** — Superposition sur les images d'héros
- **Point de rupture mobile** — Quand passer au layout mobile

## Constructeur de pied de page

Le Constructeur de pied de page fonctionne de la même manière que le Constructeur d'en-tête.

### Création d'un pied de page

1. Accédez à **Conception > Constructeur de pied de page**
2. Cliquez sur **Créer un pied de page** ou éditez-en un existant
3. Le constructeur prend en charge plusieurs colonnes et lignes
4. Glissez les widgets dans la position souhaitée

### Widgets de pied de page disponibles

- **Menu de navigation** — Liens de navigation du pied de page
- **Inscription à la newsletter** — Formulaire de souscription par courriel
- **Icônes sociales** — Liens vers vos réseaux sociaux
- **HTML personnalisé** — Contenu personnalisé, badges, certifications
- **Icônes de paiement** — Affichage des méthodes de paiement acceptées
- **Copyright** — Texte dynamique de copyright avec l'année
- **Logo** — Variante du logo du pied de page

## Menus de navigation

Les menus définissent les liens de navigation dans votre en-tête et pied de page.

### Création d'un menu

1.

Accédez à **Conception > Menus**
2.

Cliquez sur **Ajouter un menu**
3.

Donnez au menu un nom (par exemple, "Navigation principale")
4.

Ajoutez des éléments de menu:
   - **Lien vers une page** — Lien vers une page du constructeur de pages
   - **Lien vers une catégorie** — Lien vers une catégorie de produit
   - **URL personnalisée** — N'importe quelle URL externe ou interne
   - **Menu déroulant** — Éléments de sous-menu imbriqués
5.

Glissez les éléments pour les réordonner
6.

Enregistrez et attribuez le menu à un widget d'en-tête ou de pied de page

## Annonces

Créez des bannières promotionnelles qui s'affichent en haut de votre magasin.

### Création d'une annonce

1. Accédez à **Conception > Annonces** (ou utilisez la carte du tableau de bord)
2. Cliquez sur **Ajouter une annonce**
3. Configurez:
   - **Message** — Le texte de l'annonce (prend en charge les traductions)
   - **Lien** — URL facultative lors du clic
   - **Style** — Couleur d'arrière-plan, couleur du texte, icône
   - **Calendrier** — Dates de début et de fin
   - **Fermable** — Si les clients peuvent la fermer
4. Enregistrer et activer

Plusieurs annonces peuvent être actives en même temps — elles tournent automatiquement.

## Conseils

- Commencez par le customizer du thème actif pour correspondre à vos couleurs de marque avant de créer les en-têtes et pieds de page.
- Utilisez la fonction **aperçu** dans les outils de création d'en-tête et de pied de page pour voir les changements avant la publication.
- Créez des en-têtes séparés pour ordinateurs et appareils mobiles si vous avez besoin de conceptions très différentes.
- Gardez la navigation simple - 5 à 7 éléments de menu de niveau supérieur est idéal pour l'usabilité.
- Utilisez les annonces pour les promotions à durée limitée plutôt que des messages permanents.
- L'éditeur de jetons de thème prend en charge l'aperçu en temps réel — expérimentez librement et enregistrez lorsque vous êtes satisfait.