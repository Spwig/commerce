---
title: Bibliothèque multimédia
---

La Bibliothèque multimédia est le centre de gestion de toutes les images, vidéos, modèles 3D et fichiers utilisés dans votre magasin. Téléchargez des fichiers en les glissant-déposant, organisez-les avec des dossiers et des balises, et laissez le système optimiser automatiquement les images pour un chargement rapide.

![Galerie multimédia](/static/core/admin/img/help/media-library/media-gallery.webp)

## Interface de la galerie

Accédez à **Bibliothèque multimédia** dans le menu latéral pour ouvrir la galerie. L'interface comporte trois zones :

| Zone | Emplacement | Objectif |
|------|----------|---------|
| **Zone de téléchargement** | En haut du menu latéral gauche | Glisser-déposer des fichiers pour les télécharger (images, vidéos, modèles 3D jusqu'à 100 Mo) |
| **Dossiers & Balises** | En dessous dans le menu latéral gauche | Parcourir les dossiers, filtrer par balises, accéder à la corbeille |
| **Grille multimédia** | Zone principale | Rechercher, filtrer, parcourir et gérer tous vos actifs |

### Contrôles de la barre d'outils

La barre d'outils au-dessus de la grille multimédia fournit :

- **Recherche** — trouver des actifs par titre, texte alternatif, description ou nom de balise
- **Filtre par type** — afficher uniquement les Images, Vidéos ou Modèles 3D
- **Filtre par taille** — filtrer par taille de fichier (Petit, Moyen, Grand)
- **Actions en masse** — Sélectionner des éléments, Modifier les détails, Supprimer les éléments sélectionnés
- **Modes d'affichage** — Grille (grande), Grille petite ou Vue en liste (persistante entre les sessions)

## Téléchargement de fichiers

Glissez un ou plusieurs fichiers dans la zone **Télécharger** du menu latéral gauche, ou cliquez sur la zone pour ouvrir un explorateur de fichiers.

### Formats pris en charge

| Type | Formats |
|------|---------|
| **Images** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Vidéos** | MP4, WebM, MOV, MKV, AVI |
| **Modèles 3D** | GLB, glTF |

### File Upload Queue

Lors du téléchargement de plusieurs fichiers, un gestionnaire de file d'attente apparaît affichant :

- Le nom de chaque fichier et la barre de progression de téléchargement
- Les téléchargements simultanés (jusqu'à 2 à la fois pour des performances optimales)
- L'état de traitement des fichiers après leur optimisation
- L'option d'annuler des téléchargements individuels ou de supprimer les éléments terminés

La file d'attente est déplaçable et peut être minimisée afin que vous puissiez continuer à travailler pendant que les téléchargements se terminent.

## Optimisation automatique des images

Toutes les images que vous téléchargez sont optimisées automatiquement :

- **Conversion en WebP** — une version WebP est générée à côté de l'originale (qualité 85%) pour un chargement plus rapide
- **Génération de miniature** — plusieurs versions de tailles sont créées en fonction de vos paramètres d'image prédéfinis
- **Orientation EXIF** — les images sont automatiquement tournées dans la bonne orientation

### Paramètres d'image système

La plateforme inclut 21 paramètres prédéfinis intégrés qui couvrent les cas d'utilisation courants :

| Paramètre | Dimensions | Recadrage | Utilisé pour |
|--------|-----------|------|---------|
| **Miniature** | 150 x 150 | Couvrir | Listes d'administration, aperçus rapides |
| **Petit** | 300 x 300 | Couvrir | Cartes de produit petites |
| **Moyen** | 600 x 600 | Contenir | Cartes de produit, miniatures de blog |
| **Grand** | 1200 x 1200 | Contenir | Pages détaillées des produits |
| **Galerie** | 800 x 800 | Contenir | Galeries d'images |
| **Héro** | 1920 x 1080 | Couvrir | Sections héro, bannières de page |
| **Bannière** | 1200 x 400 | Couvrir | Bannières de promotion |
| **Carte** | 400 x 300 | Couvrir | Cartes de fonctionnalités, cartes de contenu |
| **Avatar** | 200 x 200 | Recadrer | Avatars de clients et de personnel |
| **Liste de produits** | 400 x 400 | Couvrir | Cartes de grille de produits |
| **Détail du produit** | 1200 x 1200 | Couvrir | Images de produits complètes |
| **Miniature du produit** | 100 x 100 | Couvrir | Sélecteurs de variantes, paniers miniatures |
| **Bannière de catégorie** | 1920 x 480 | Couvrir | En-têtes de pages de catégories |
| **Miniature de catégorie** | 300 x 200 | Couvrir | Cartes de catégories |
| **Logo en-tête** | 300 x 80 | Paver | Logo de l'en-tête du site |
| **Logo pied de page** | 200 x 60 | Paver | Logo du pied de page du site |
| **Logo e-mail** | 400 x 100 | Paver | Logos de modèles d'e-mail |
| **Logo carré** | 160 x 160 | Paver | Emplacements de logos carrés |
| **Logo de marque** | 200 x 100 | Paver | Logos de marques/partners |
| **Bannière d'annonce** | 800 x 300 | Couvrir | Images d'annonces |
| **Arrière-plan d'annonce** | 1200 x 800 | Couvrir | Arrière-plans d'annonces |

Les paramètres système ne peuvent pas être renommés ou supprimés. Vous pouvez créer des paramètres personnalisés supplémentaires sous **Bibliothèque multimédia > Paramètres de taille d'image** si vous avez besoin de tailles non couvertes par les paramètres par défaut.

### Modes de recadrage

| Mode | Comportement |
|------|----------|
| **Couvrir** | Remplit toute la zone, recadrant les bords si nécessaire — idéal pour les cartes et les bannières |
| **Contenir** | Ajuste l'image entière dans la zone, ajoutant de l'espace transparent si nécessaire — idéal pour les images de produits |
| **Recadrer** | Recadre au centre pour les dimensions exactes |
| **Paver** | Ajuste l'image et ajoute du padding (transparent, blanc ou noir) — idéal pour les logos |

## Organisation des fichiers

### Dossiers

Créez des dossiers pour organiser vos médias en groupes logiques. Les dossiers peuvent être imbriqués à n'importe quelle profondeur. Cliquez sur un dossier dans le menu latéral gauche pour afficher uniquement les actifs qu'il contient. Le lien **Tous les fichiers** affiche tout.

### Balises

Ajoutez des balises aux actifs pour une organisation flexible à travers les dossiers. Les balises apparaissent dans un nuage dans le menu latéral gauche. Cliquez sur une balise pour filtrer les actifs par cette balise. Les actifs peuvent avoir plusieurs balises.

### Recherche

La barre de recherche trouve des actifs par titre, texte alternatif, description ou nom de balise. Combinez la recherche avec les filtres de type et de taille pour obtenir des résultats précis.

## Détail de l'actif

Cliquez sur un actif pour ouvrir sa vue détaillée avec un aperçu agrandi et une métadonnée complète.

![Détail de l'actif](/static/core/admin/img/help/media-library/media-detail.webp)

La vue détaillée affiche :

- **Aperçu** — aperçu d'image agrandi avec les dimensions d'origine
- **Informations sur le fichier** — type, dimensions, taille du fichier, date de téléchargement
- **Onglets** pour l'édition :

| Onglet | Champs |
|-----|--------|
| **Général** | Titre, Texte alternatif, Description (tous traduisibles pour les magasins multilingues) |
| **Technique** | Type MIME, hachage du fichier, nom de fichier original, statut de la version WebP |
| **Organisation** | Affectation de dossier, balises, bascule public/privé |
| **Avancé** | Coordonnées du point focal, ID externe, métadonnées JSON |

### Champs traduisibles

Le titre, le texte alternatif et la description prennent en charge les traductions. Cliquez sur l'icône de traduction à côté de chaque champ pour ajouter des traductions pour vos langues activées. Cela garantit que les images ont un texte alternatif et des descriptions correctement localisés pour le référencement et l'accessibilité.

### Suivi des usages

Le système suit où chaque actif est utilisé à travers la plateforme. La section **Usages des médias** en bas affiche chaque modèle et champ qui fait référence à cet actif, vous aidant à comprendre l'impact avant de faire des modifications ou de supprimer.

## Support des vidéos

Les vidéos téléchargées dans la bibliothèque multimédia sont analysées automatiquement :

- **Extraction des métadonnées** — durée, résolution, taux de trame, débit, et codecs sont capturés
- **Image de présentation** — une miniature est générée à partir de la vidéo pour l'aperçu
- **Streaming** — les vidéos prennent en charge les requêtes de plage pour le déplacement sans télécharger le fichier complet
- **Conversion optionnelle** — les vidéos peuvent être converties en format WebM/AV1 optimisé pour une livraison plus rapide

## Corbeille

La suppression d'un actif le déplace vers la **Corbeille** plutôt que de l'enlever définitivement. Cela protège contre la suppression accidentelle.

| Action | Ce qu'elle fait |
|--------|-------------|
| **Supprimer** | Déplace l'actif vers la corbeille (suppression douce) |
| **Restaurer** | Renvoie un actif supprimé à son emplacement d'origine |
| **Suppression permanente** | Supprime l'actif et toutes ses miniatures du stockage de manière permanente |
| **Vider la corbeille** | Supprime définitivement tous les éléments de la corbeille |

Cliquez sur **Corbeille** dans le menu latéral gauche pour consulter et gérer les actifs supprimés.

## Où la bibliothèque multimédia est utilisée

La bibliothèque multimédia est intégrée à travers toute la plateforme :

| Fonctionnalité | Comment elle utilise les médias |
|---------|------------------|
| **Catalogue de produits** | Images de produits, images de variantes, bannières de catégories |
| **Blog** | Images mises en avant, images dans le contenu via CKEditor |
| **Construire une page** | Éléments d'image, arrière-plans héro, composants de galerie |
| **Construire l'en-tête/pied de page** | Images de logo, images d'arrière-plan |
| **Paramètres du site** | Logo du site et favicon |
| **Annonces** | Images d'annonces et arrière-plans |
| **CKEditor** | Tous les téléchargements d'images dans le texte enrichi passent par la bibliothèque multimédia |
| **Programme de fidélité** | Images de récompenses et de niveaux |

Lorsque vous sélectionnez une image dans l'une de ces fonctionnalités, la galerie de la bibliothèque multimédia s'ouvre en tant que modal pour un parcours et une sélection faciles.

## Conseils

- **Utilisez des titres et des textes alternatifs descriptifs** — de bons métadonnées améliorent le référencement et l'accessibilité. Le système utilise le texte alternatif dans les balises d'images à travers le magasin.
- **Organisez avec des dossiers dès le début** — créez une structure de dossiers (par exemple, Produits, Blog, Bannières, Logos) avant de télécharger de nombreux fichiers. Il est beaucoup plus facile d'organiser au fur et à mesure que de reorganiser plus tard.
- **Utilisez des balises pour des catégories transversales** — des balises comme "saisonnier", "vente" ou "mode de vie" vous aident à trouver des actifs qui couvrent plusieurs dossiers.
- **Vérifiez l'utilisation avant de supprimer** — la section de suivi des usages affiche où un actif est référencé. La suppression d'un actif utilisé peut laisser des images cassées sur votre magasin.
- **Laissez WebP faire le travail** — la conversion automatique en WebP réduit généralement les tailles de fichiers de 25 à 35 % par rapport au JPEG sans perte visible de qualité. Vous n'avez pas besoin de convertir manuellement les images avant de les télécharger.
- **Créez des paramètres personnalisés** — si vous avez un layout unique qui nécessite une taille d'image spécifique, créez un paramètre personnalisé plutôt que de redimensionner manuellement les images.