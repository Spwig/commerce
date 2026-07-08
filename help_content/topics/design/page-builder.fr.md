---
title: Page Builder
---

Le Page Builder est un éditeur visuel de type glisser-déposer pour créer des pages riches et réactives sans écrire de code. Ajoutez des éléments à partir d'une bibliothèque de 39 composants, stylez-les avec des outils puissants, configurez des animations et des règles de visibilité, puis publiez-les avec un historique complet des versions.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## L'Interface du Builder

Le builder comporte quatre zones principales:

| Zone | Emplacement | Objectif |
|------|----------|---------|
| **Barre d'outils** | Barre supérieure | Aperçu du dispositif (ordinateur, tablette, mobile), annuler/refaire, paramètres de la page, sauvegarder un brouillon, publier |
| **Bibliothèque d'éléments** | Barre latérale gauche | Parcourir et glisser 39 éléments organisés en 9 catégories |
| **Canvas** | Centre | Zone d'édition WYSIWYG en direct — voir les modifications au fur et à mesure |
| **Panneau des propriétés** | Barre latérale droite | Modifier le contenu, le style, les animations et les paramètres avancés de l'élément sélectionné |

## Bibliothèque d'Éléments

Les éléments sont organisés en catégories. Glissez n'importe quel élément depuis la bibliothèque sur le canvas pour l'ajouter à votre page.

| Catégorie | Éléments |
|----------|----------|
| **Mise en page** | Conteneur, Séparateur, Section Héro, Pop-up Modal, Menu de navigation, Espacement |
| **Basique** | Titre, Texte, Bouton, Icône |
| **Contenu** | Carrousel de publications de blog, Grille de publications de blog, Accordeon FAQ, Publications liées, Témoignages |
| **Médias** | Image, Galerie d'images, Accordeon d'images, Incrustation de vidéo |
| **Formulaires** | Formulaire de contact, Formulaire, Inscription à la newsletter |
| **Marketing** | Compteur à l'envers, Bannière CTA, Bannière de publication mise en avant, Bannière de fidélité, Bannière de promotion, Badges de confiance, Affichage du code-cadeau |
| **E-commerce** | Mise en avant de catégorie, Promotion de carte-cadeau, Carrousel de produits, Grille de produits, Liste de produits, Affichage des avis, Produits en promotion, Localisateur de magasin |
| **Social** | Liens sociaux |
| **Navigation** | Barre de recherche |

### Conteneurs et Nesting

L'élément **Conteneur** est la base des mises en page complexes. Les conteneurs peuvent contenir d'autres éléments — y compris d'autres conteneurs — vous permettant de créer des grilles à plusieurs colonnes et des structures imbriquées. Utilisez les paramètres de mise en page du conteneur pour configurer rapidement des arrangements de colonnes courants (50/50, 33/33/33, 25/75, etc.).

## Ajout d'Éléments

1. Trouvez l'élément que vous souhaitez dans la barre latérale gauche
2. **Glissez**-le sur le canvas et déposez-le là où vous le souhaitez
3. Les éléments peuvent être déposés entre des éléments existants, ou à l'intérieur des conteneurs
4. La ligne d'insertion bleue indique où l'élément sera placé
5. Après le dépôt, l'élément est automatiquement sélectionné et le panneau des propriétés s'ouvre

Vous pouvez également réordonner les éléments en les glissant vers le haut ou vers le bas sur le canvas.

## Édition du Contenu

Sélectionnez n'importe quel élément sur le canvas pour ouvrir ses propriétés dans le panneau de droite. L'onglet **Contenu** affiche des champs spécifiques à ce type d'élément.

![Panneau des Propriétés](/static/core/admin/img/help/page-builder/properties-panel.webp)

Par exemple:
- **Titre** — texte, balise HTML (H1–H6), alignement, ID d'ancre
- **Image** — source d'image (bibliothèque média), texte alternatif, lien, mise en page
- **Bouton** — étiquette, URL, variante de style, icône
- **Grille de produits** — source de données, nombre de colonnes, produits par page, ordre de tri
- **Section Héro** — titre, sous-titre, description, arrière-plan, boutons d'appel à l'action

Les champs de contenu traduisibles affichent une icône de traduction — cliquez-y pour ajouter des traductions pour les magasins multilingues.

## Style des Éléments

L'onglet **Style** fournit des contrôles visuels pour chaque élément. Chaque section ouvre un éditeur d'utilitaire dédié.

![Onglet Style](/static/core/admin/img/help/page-builder/style-tab.webp)

| Section | Ce qu'elle contrôle | Utilitaire |
|---------|-----------------|---------|
| **Typographie** | Famille de police, taille, poids, hauteur de ligne, espacement entre les lettres, style du texte | Éditeur de typographie |
| **Couleurs** | Couleur du texte avec entrée hex/RGB/HSL et jetons de thème | Sélecteur de couleur |
| **Arrière-plan** | Couleur solide, dégradé, image ou arrière-plan vidéo avec états de survol | Éditeur d'arrière-plan |
| **Bordure** | Largeur, style, couleur et rayon de bordure par côté | Éditeur de bordure |
| **Espacement** | Marge et padding avec éditeur de modèle de boîte visuel | Éditeur d'espacement |
| **Effets** | Ombre de boîte avec préférences et support multi-couches, curseur d'opacité | Éditeur d'ombre |

Chaque utilitaire est documenté dans son propre sujet d'aide — recherchez "sélecteur de couleur", "éditeur d'arrière-plan", etc. pour en savoir plus.

## Animations

L'onglet **Animations** vous permet d'ajouter du mouvement aux éléments.

### Animations d'Entrée

Déclenchées lorsque l'élément roule dans le champ de vision:

| Animation | Description |
|-----------|-------------|
| Apparition en Fad | Apparaît progressivement |
| Glisser en (Haut/Bas/Gauche/Droite) | Glisse depuis une direction |
| Zoom In | Grandit depuis une petite taille jusqu'à la taille complète |
| Bounce In | Bascule en place |
| Pulse / Shake / Bounce / Flash / Spin | Effets attirant l'attention |

Configurez **durée** (0,3s–1,5s), **délai** (0–1s), **fonction de temporisation** (ease, ease-in, ease-out, linéaire), et **répétition** (une fois ou infinie).

### Animations de survol

Déclenchées lorsque les visiteurs survolent l'élément:

| Effet | Description |
|--------|-------------|
| Agrandir / Réduire | Grossit ou réduit |
| Lever | Flotte vers le haut |
| Rotation (sens horaire / anti-horaire) | Tourne dans le sens horaire ou anti-horaire |
| Assombrir / Faire disparaître | Modifie la luminosité ou l'opacité |
| Ombre qui s'élargit | L'ombre s'élargit |
| Lever avec ombre | Montre avec une ombre qui s'élargit |
| Pulse Scale / Skew / Border Glow | Effets spéciaux |

Configurez **durée**, **temporisation** et **intensité** (subtile, normale, forte).

## Paramètres Avancés

L'onglet **Avancé** fournit un contrôle fin:

### Règles de Visibilité

Contrôlez quand un élément est affiché ou masqué en fonction de conditions:

- **Statut de l'utilisateur** — connecté, déconnecté, nouveau client, client existant
- **Appareil** — ordinateur, tablette, mobile
- **Heure** — plage de dates, heure de la journée, jour de la semaine
- **Groupe de clients** — VIP, gros client, etc.
- **Valeur du panier** — total minimum ou maximum du panier
- **Géographie** — pays, région
- Et 20+ autres types de règles

Les règles peuvent être combinées avec une logique ET/OU pour des ciblages complexes.

### CSS personnalisé

| Champ | Objectif |
|-------|---------|
| **ID de l'élément** | ID unique pour les liens d'ancre ou la ciblage CSS |
| **Classes CSS personnalisées** | Classes supplémentaires à appliquer |
| **Styles CSS personnalisés** | CSS inline pour des surcharges ponctuelles |
| **Attributs de données** | Attributs de données personnalisés comme paires clé-valeur |
| **Z-Index** | Ordre de superposition pour les éléments superposés |

## Workflow de publication

Les pages utilisent un système de brouillon/publier avec un historique complet des versions:

| Statut | Signification |
|--------|---------|
| **Brouillon** | Travail en cours — pas visible pour les visiteurs |
| **Publié** | En ligne sur votre magasin |
| **Archivé** | Supprimé du site mais conservé |

### Fonctionnement

1. Apportez des modifications dans le builder — elles sont enregistrées comme un **brouillon**
2. Cliquez sur **Enregistrer le brouillon** pour enregistrer sans publier
3. Cliquez sur **Publier** pour rendre le brouillon actuel en ligne
4. Chaque publication crée un **instantané de version**
5. Vous pouvez **restaurer** toute version précédente à partir de l'historique des versions (icône d'horloge dans la barre d'outils)

Cela signifie que vous pouvez expérimenter librement — votre page en ligne reste inchangée jusqu'à ce que vous publiiez explicitement.

## Modèles de Pages

Gagnez du temps en travaillant avec des modèles:

- **Enregistrer en tant que modèle** — enregistrez la conception de toute page comme un modèle réutilisable
- **Créer à partir d'un modèle** — commencez une nouvelle page à partir d'un modèle existant
- **Catégories de modèles** — organisez les modèles par objectif (page d'accueil, à propos, mise en avant de produit, etc.)

Les modèles capturent la structure complète de la page, y compris tous les éléments, le contenu et le style.

## Conception Réactive

Utilisez les boutons d'aperçu des appareils dans la barre d'outils pour voir comment votre page se présente sur différentes tailles d'écran:

- **Ordinateur** — mise en page à large bande
- **Tablette** — fenêtre de visualisation moyenne
- **Mobile** — fenêtre de visualisation étroite

Les éléments se réorganisent automatiquement en fonction des paramètres de leur conteneur. Vous pouvez également utiliser des règles de visibilité pour afficher ou cacher des éléments spécifiques sur certains appareils.

## Conseils

- **Commencez par un conteneur** — la plupart des mises en page commencent par un conteneur pour créer des colonnes et une structure. Utilisez les paramètres de mise en page pour les arrangements courants.
- **Utilisez les sections Héro pour les en-têtes de page** — l'élément Héro fournit un titre, un sous-titre, une image d'arrière-plan et des boutons CTA dans un seul composant.
- **Prévisualisez avant de publier** — cliquez sur Prévisualiser pour voir exactement ce que verront les visiteurs, puis publiez lorsque vous êtes satisfait.
- **Utilisez les règles de visibilité pour la personnalisation** — affichez du contenu différent aux visiteurs connectés vs. déconnectés, ou ciblez des groupes de clients spécifiques.
- **Gardez les animations subtilles** — une ou deux animations d'entrée par section de page donnent un aspect professionnel. Trop d'animations peuvent sembler écrasantes.
- **Nommez vos conteneurs** — utilisez le champ ID de l'élément pour étiqueter les conteneurs (par exemple, "hero-section", "features") afin qu'ils soient faciles à trouver dans les pages complexes.
- **Testez sur tous les appareils** — utilisez l'aperçu des appareils pour vérifier votre mise en page sur ordinateur, tablette et mobile avant de publier.
- **Exploitez les modèles** — enregistrez vos meilleures conceptions de page comme modèles pour accélérer la création de pages futures.