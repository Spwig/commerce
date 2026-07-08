---
title: Gestion des Catégories
---

Les catégories vous aident à organiser votre catalogue de produits afin que les clients puissent parcourir et trouver facilement les produits. Accédez à **Produits > Catégories** dans la barre latérale d'administration.

![Liste des catégories](/static/core/admin/img/help/manage-categories/category-list.webp)

## Liste des Catégories

La page de gestion des catégories affiche toutes vos catégories sous forme de cartes avec :

- **Image miniature** — Identifiant visuel de la catégorie
- **Nom et slug** — Nom d'affichage et identifiant compatible avec les URLs
- **Nombre de produits** — Nombre de produits assignés à cette catégorie
- **Statut** — Publiée ou brouillon

Utilisez les **onglets de filtre** en haut pour afficher rapidement Toutes, Publiées ou Brouillon. La **barre de recherche** vous permet de trouver des catégories par nom.

## Créer une Catégorie

1. Cliquez sur **+ Ajouter une Catégorie** en haut à droite
2. Remplissez les détails de la catégorie :
   - **Nom** — Le nom d'affichage que les clients verront
   - **Slug** — Généré automatiquement à partir du nom, utilisé dans les URLs
   - **Catégorie parente** — Laissez vide pour une catégorie de premier niveau, ou sélectionnez une catégorie parente pour créer une sous-catégorie
   - **Description** — Description en texte enrichi affichée sur la page de la catégorie
3. Téléchargez une **image de catégorie** — affichée dans les menus de navigation et les listes de catégories
4. Configurez les **champs SEO** (méta-titre, description) dans l'onglet SEO
5. Cliquez sur **Enregistrer**

## Hiérarchie des Catégories

Les catégories prennent en charge une imbrication illimitée pour créer une structure arborescente :

- **Catégories de premier niveau** — Éléments principaux de navigation (ex. : "Vêtements", "Électronique")
- **Sous-catégories** — Imbriquées sous une catégorie parente (ex. : "Vêtements > Homme > T-Shirts")

La liste déroulante de catégorie parente affiche le chemin complet de la hiérarchie pour vous aider à choisir le bon niveau.

## Paramètres des Catégories

### Visibilité

- **Publiée** — La catégorie apparaît sur la boutique et dans la navigation
- **Brouillon** — La catégorie est masquée pour les clients mais accessible dans l'administration

### Catégories Mises en Avant

Marquez des catégories comme **mises en avant** pour les mettre en valeur sur votre page d'accueil ou dans des sections de navigation spéciales. Les catégories mises en avant peuvent être affichées à l'aide de l'élément grille de catégories du Constructeur de Pages.

### Ordre de Tri

Contrôlez l'apparence des catégories dans les menus de navigation en définissant une valeur d'**ordre de tri**. Les nombres les plus bas apparaissent en premier.

## Assigner des Produits aux Catégories

Il existe deux façons d'assigner des produits :

1. **Depuis le formulaire d'édition du produit** — Sélectionnez une catégorie dans le menu déroulant Catégorie de l'onglet Informations de Base
2. **Assignation groupée** — Sélectionnez plusieurs produits dans la liste des produits et utilisez l'action groupée pour les assigner à une catégorie

Chaque produit peut appartenir à une catégorie principale. Utilisez des étiquettes ou des collections pour des regroupements supplémentaires.

## Pages de Catégorie sur la Boutique

Chaque catégorie publiée obtient automatiquement une page dédiée affichant :
- Nom et description de la catégorie
- Image de bannière (si définie)
- Grille de produits avec tous les produits assignés
- Options de filtrage et de tri

L'URL de la page de catégorie suit le modèle : `votreboutique.com/category/slug-de-categorie/`

## Conseils

- Gardez votre arborescence de catégories peu profonde — 2 à 3 niveaux de profondeur est idéal pour l'ergonomie de la navigation.
- Utilisez des noms de catégorie descriptifs qui correspondent à ce que recherchent les clients.
- Ajoutez des images de catégorie pour une expérience de navigation plus visuelle.
- Mettez en place votre structure de catégories avant d'ajouter des produits pour rester organisé.
- Utilisez la description de la catégorie pour le SEO — incluez des mots-clés pertinents de manière naturelle.
