---
title: Ajouter un produit
---

Ce guide vous guide à travers la création d'un nouveau produit dans votre magasin. Le formulaire de produit est organisé en sections couvrant les informations de base, les médias, les prix, le stock, le référencement (SEO), et bien plus encore - vous pouvez remplir l'ensemble en une seule fois ou revenir pour compléter des sections ultérieurement.

## Premiers pas

Depuis la barre latérale, accédez à **Produits > Tous les produits** pour voir votre catalogue de produits. Cliquez sur le bouton **+ Ajouter un produit** en haut à droite pour ouvrir le formulaire de création de produit.

![Page de liste des produits](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informations de base

La section **Informations de base** est là pour définir l'identité principale de votre produit.

![Formulaire d'ajout de produit](/static/core/admin/img/help/add-product/add-product-form.webp)

### Champs obligatoires

- **Nom** — Le nom du produit affiché aux clients. Cliquez sur l'icône du globe pour ajouter des traductions pour d'autres langues.
- **Slug** — Version convivible pour les URL (générée automatiquement). Personnalisez-la si nécessaire.
- **SKU** — Votre code d'unité de gestion de stock interne.
- **Type de produit** — Choisissez parmi : Simple, Variable, Numérique, Forfait, Carte-cadeau, Personnalisable, Configurable ou Réservation.
- **Catégorie** — Attribuez le produit à une catégorie pour l'organisation et la navigation sur le site.

### Statut et visibilité

Trouvé dans la section **Statut** en bas du formulaire :

- **Statut** — Défini sur **Brouillon** pendant que vous travaillez, **Publié** lorsque prêt à vendre, ou **Discontinué** pour les produits que vous ne proposez plus.
- **Est-ce une vedette** — Cochez pour mettre en évidence ce produit sur votre site.
- **Est-ce un produit numérique** — Cochez si ce produit inclut des téléchargements numériques (fichiers, licences). Peut être combiné avec n'importe quel type de produit.
- **Cacher du site** — Cache le produit des listes de catalogue tout en le maintenant disponible en tant qu'option de configurateur ou composant de forfait.

### Champs optionnels

- **Marque** — Associez-le à une marque si applicable.
- **Mots-clés** — Attribuez un ou plusieurs mots-clés dans la carte **Mots-clés** plus bas sur cette onglet. Les mots-clés sont distincts des collections — ce sont des étiquettes rapides et libres pour organiser et filtrer les produits plutôt qu'un regroupement de vente. Tapez pour rechercher un mot-clé existant, ou tapez un nouveau nom pour le créer en temps réel. Consultez le sujet d'aide **Mots-clés de produit** pour créer, renommer et supprimer en bloc des mots-clés directement.

![La carte Mots-clés sur l'onglet Informations de base, avec deux mots-clés appliqués dans le sélecteur de mots-clés](/static/core/admin/img/help/add-product/tags-card.webp)

### Descriptions du produit

- **Description courte** — Apparaît dans les listes de produits et les cartes. Gardez-la brève et percutante.
- **Description complète** — Description détaillée du produit affichée sur la page de détail du produit. Utilisez l'éditeur de texte enrichi pour ajouter de la mise en forme, des images, des vidéos et des tableaux.

Les deux champs de description prennent en charge la fonction de traduction — cliquez sur l'icône du globe pour fournir du contenu dans d'autres langues.

### Fonctionnalités et spécifications

La section **Détails du produit** contient deux champs de données structurées :

- **Fonctionnalités** — Paires clé-valeur pour les points forts du produit (ex. : "Durée de batterie : 20 heures").
- **Spécifications** — Détails techniques pour l'onglet de spécifications sur la page du produit (ex. : "Processeur : Intel i7").

## Médias

La section **Médias** vous permet de gérer les images du produit à l'aide de la bibliothèque de médias intégrée.

![Onglet Médias](/static/core/admin/img/help/add-product/media-tab.webp)

1. Cliquez sur **+ Ajouter des images depuis la bibliothèque de médias** pour ouvrir le sélecteur d'images.
2. Sélectionnez des images existantes ou téléversez de nouvelles images directement.
3. Glissez les images pour les réordonner — la **première image** devient l'image principale du produit affichée dans les listes et les cartes.

Le champ **Type de galerie**, dans la carte **Paramètres de galerie** ci-dessous la liste d'images, contrôle l'affichage des images sur le site : Galerie standard, Carousel, disposition en grille, galerie zoom, ou vue 360°.

## Prix

Définissez le prix de votre produit et configurez les ventes.

![Onglet Prix](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Prix régulier

- **Prix régulier** — Le prix de détail standard que les clients verront.

La devise est définie en même temps que le montant du prix.
- **Coût** — Vos coûts de marchandises, utilisés pour les calculs de bénéfice.

Cela n'est jamais affiché aux clients.

### Paramètres de vente

Configurez des remises temporaires :

- **Type de vente** — Choisissez entre : Aucune vente, Prix de vente fixe, Montant réduit, ou Pourcentage réduit.
- **Valeur de la vente** — Le montant de la remise ou le pourcentage.
- **Date de début de la vente / Date de fin de la vente** — Planifiez la date de mise en service et d'expiration de la vente. Laissez vide pour un démarrage immédiat ou pas de date de fin.

### Tarification multivalute

Si la multivalute est activée sur votre magasin, un champ **Stratégie de tarification** apparaît : 

- **Tarification dynamique** — Les prix dans les autres devises sont calculés automatiquement en utilisant vos taux de change configurés.
- **Tarification fixe** — Définissez un prix spécifique pour chaque devise indépendamment à l'aide de la section **Tarification multivalute** qui s'affiche ci-dessous.

## Inventaire

Gérez les niveaux de stock, le comportement d'expédition et les attributs des produits physiques.

![onglet Inventaire](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestion du stock

- **Suivi de l'inventaire** — Activez pour surveiller les quantités de stock (activé par défaut).
- **Seuil de stock faible** — Recevez des alertes lorsque le stock tombe en dessous de ce nombre (valeur par défaut : 5).
- **Commandes en attente** — Activez pour accepter les commandes même lorsqu'il n'y a plus de stock. Les nouveaux produits commencent avec la valeur **Autoriser les commandes en attente par défaut** depuis **Paramètres > Paramètres du magasin > Commerce**, mais vous pouvez le modifier par produit ici à tout moment.
- **Action en cas de rupture de stock** — Remplacez le comportement du site ou de la catégorie lorsqu'un produit est en rupture de stock : le cacher, l'afficher comme indisponible, afficher un bouton « Avertissez-moi », ou autoriser les commandes en attente.

Les quantités de stock sont gérées par entrepôt. Après avoir enregistré le produit, utilisez la section **Éléments de stock** en bas du formulaire (ou naviguez vers **Produits > Éléments de stock**) pour définir les quantités dans chaque emplacement d'entrepôt.

### Attributs physiques

Entrez le poids du produit (kg) et les dimensions (longueur, largeur, hauteur en cm) pour des calculs d'expédition précis.

### Expédition

- **Expédition requise** — Si ce produit doit être expédié au client. Activé par défaut pour les produits physiques ; votre interface client et la caisse l'utilisent pour décider si elle doit collecter une adresse d'expédition et établir une estimation de frais de port pour la commande. Spwig désactive automatiquement cette option pour les produits numériques, de réservation et de carte-cadeau, car ceux-ci ne sont jamais envoyés — vous n'avez pas besoin (et ne pouvez pas) de la réactiver pour ces types de produits. Laissez-la cochée pour un produit physique qui ressemble à un produit numérique, comme une carte-cadeau imprimée qui est expédiée dans une boîte.
- **Colis d'expédition préféré** — Choisissez optionnellement l'un de vos colis d'expédition configurés. Lorsqu'elle est définie, les dimensions propres à ce colis sont utilisées pour les calculs des tarifs d'expédition au lieu du poids et des dimensions du produit ci-dessus — utile lorsqu'un produit est toujours expédié dans la même boîte standard ou enveloppe. Laissez-la vide pour utiliser les attributs physiques du produit. Gérez les colis disponibles sous **Expédition > Colis**.

### Acompte

Utilisez la carte **Acompte** pour vendre un produit avant qu'il n'ait du stock — utile pour les lancements futurs que vous souhaitez commencer à prendre des commandes avant le lancement : 

- **Est-ce un acompte** — Activez pour permettre aux clients d'acheter ce produit même s'il est en rupture de stock.
- **Date de lancement de l'acompte** — La date d'availability attendue, affichée aux clients.
- **Message d'acompte** — Un court message personnalisé affiché aux clients, limité à 200 caractères (exemple : « Expédié en mars 2026 »).

### Identifiants de produit

Codes de produit standards pour les listes de marchés et les systèmes de gestion de stock : 

- **GTIN** — Numéro de produit de la chaîne d'approvisionnement mondiale
- **EAN** — Numéro d'article européen
- **UPC** — Code de produit universel (États-Unis)
- **ISBN** — Pour les livres
- **ASIN** — Identifiant Amazon
- **MPN** — Numéro de pièce du fabricant

### Expédition internationale / douane

Obligatoire pour les envois internationaux (développez la section **Expédition internationale / Douane**) :

- **Code HS** — Code de classification du Système harmonisé
- **Pays d'origine** — Lieu de fabrication du produit
- **Prix unitaire en douane** — Valeur déclarée par unité pour les douanes
- **Numéro de licence d'exportation** — Requis uniquement pour les articles contrôlés ou restreints
- **Expiration de la licence d'exportation** — Date d'expiration de la licence d'exportation

## SEO

Optimisez la visibilité de votre produit dans les moteurs de recherche.

![Onglet SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Titre Meta** — Le titre affiché dans les résultats des moteurs de recherche. Cliquez sur l'icône de globe pour traduire.
- **Description Meta** — Une brève description pour les résultats de recherche (160 caractères max). Cliquez sur l'icône de globe pour traduire.
- **Génération automatique du SEO** — Cochez pour générer automatiquement le contenu SEO lorsque le produit est enregistré.

Un **Aperçu des résultats de recherche** en direct montre exactement comment votre produit apparaîtra dans les résultats de recherche Google.

## Paramètres de la page produit

Sur l'onglet **Avancé**, la carte **Paramètres de la page produit** vous permet de contrôler l'apparence de la page boutique de ce produit :

- **Modèle de page** — Remplacez la mise en page par défaut de la page produit du site pour ce produit uniquement : Classique, Pleine largeur, Focus galerie, ou Numérique. Laissez-le sur **Utiliser le défaut du site** pour hériter de la mise en page spécifiée dans vos paramètres de Design — la plupart des produits doivent rester sur le défaut afin que les changements de modèle appliqués là-bas soient appliqués automatiquement.
- **Afficher les produits liés** — Affichez les produits liés en bas de la page.
- **Afficher les avis** — Affichez les avis des clients.
- **Afficher les spécifications** — Affichez l'onglet des spécifications.

Le champ **Type de galerie** — qui contrôle l'affichage des images du produit (Galerie standard, Carrousel, Disposition en grille, Galerie avec zoom, ou Vue 360°) — est défini séparément, sur l'onglet **Médias**.

![Onglet Avancé montrant la carte Paramètres de la page produit avec un menu déroulant Modèle de page, et la carte Détails techniques en dessous](/static/core/admin/img/help/add-product/advanced-tab.webp)

## Canal de vente

Le champ **Canal de vente** (dans la section Statut) contrôle où le produit peut être vendu :

- **Tous les canaux** — Disponible en ligne et en magasin (POS).
- **En ligne uniquement** — Non disponible via les terminaux POS.
- **En magasin uniquement** — Non listé en ligne ; disponible uniquement dans votre magasin physique.

Un champ **Code-barres** est également disponible pour le scan de code-barres POS.

## Enregistrement de votre produit

Lorsque vous êtes prêt, utilisez les boutons d'enregistrement dans le coin supérieur droit. Votre produit sera visible sur la boutique une fois son statut défini sur **Publié**.

## Conseils

- Commencez avec le statut **Brouillon** pour que vous puissiez perfectionner le produit avant que les clients ne le voient.
- Téléchargez plusieurs images — les produits avec plusieurs photos convertissent mieux.
- Remplissez les champs **SEO** pour améliorer la découvrabilité dans les moteurs de recherche.
- Utilisez les **Catégories**, les **Marques** et les **Étiquettes** pour aider les clients à naviguer dans votre catalogue.
- Pour les produits variables (par exemple, différentes tailles ou couleurs), choisissez le type **Produit variable** et ajoutez des variantes après l'enregistrement.
- Utilisez les **Caractéristiques** et les **Spécifications** pour ajouter des données produit structurées qui s'affichent dans des onglets dédiés sur la page produit.
- Si **Exige une expédition** ne reste pas coché, regardez le **Type de produit** — Spwig désactive automatiquement l'expédition pour les produits Numériques, Réservation et Carte Cadeau, car aucun de ceux-ci n'est physiquement expédié.
- Définissez un **Colis d'expédition préféré** pour les produits qui sont toujours expédiés dans la même boîte — cela vous évite de devoir garder le poids et les dimensions propres au produit synchronisés avec la boîte que vous utilisez réellement.