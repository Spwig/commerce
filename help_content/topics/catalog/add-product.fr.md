---
title: Ajouter un Produit
---

Ce guide vous accompagne dans la creation d'un nouveau produit dans votre boutique. Les produits sont organises en plusieurs onglets — Informations de base, Medias, Tarification, Inventaire et SEO — vous pouvez tout remplir en une seule fois ou revenir completer les sections plus tard.

## Pour Commencer

Depuis le menu lateral, accedez a **Produits > Tous les Produits** pour afficher votre catalogue de produits. Cliquez sur le bouton **+ Ajouter un Produit** dans le coin superieur droit pour ouvrir le formulaire de creation de produit.

![Page de liste des produits](/static/core/admin/img/help/add-product/product-list-page.webp)

## Onglet Informations de Base

L'onglet **Informations de base** est l'endroit ou vous definissez les details essentiels de votre produit.

![Formulaire d'ajout de produit](/static/core/admin/img/help/add-product/add-product-form.webp)

### Champs Obligatoires

- **Nom** — Le nom du produit affiche aux clients. Cliquez sur l'icone globe pour ajouter des traductions dans d'autres langues.
- **Slug** — Version du nom adaptee aux URL (generee automatiquement). Desactivez « Auto » pour le personnaliser.
- **SKU** — Votre code interne de reference produit.
- **Type de Produit** — Choisissez parmi : Simple, Variable, Numerique, Lot, Carte Cadeau, Personnalisable ou Configurable.
- **Statut** — Definissez sur Brouillon pendant la preparation, puis passez a Publie lorsque le produit est pret.

### Champs Facultatifs

- **Categorie** — Attribuez le produit a une categorie pour l'organisation et la navigation en vitrine.
- **Marque** — Associez a une marque si applicable.
- **Produit Vedette** — Cochez pour mettre ce produit en avant sur votre vitrine.
- **Produit Numerique** — Cochez si ce produit comprend des telechargements numeriques (fichiers, licences).
- **Masquer de la Vitrine** — Masque le produit des listings du catalogue tout en le gardant disponible en tant qu'option de configurateur ou composant de lot.

### Descriptions du Produit

- **Description Courte** — Apparait dans les listings et les fiches produit. Gardez-la breve et percutante.
- **Description Complete** — Description detaillee du produit affichee sur la page de detail du produit. Utilisez l'editeur de texte enrichi pour ajouter de la mise en forme, des images, des videos et des tableaux.

Les deux champs de description prennent en charge la fonctionnalite de traduction — cliquez sur l'icone globe pour fournir du contenu dans d'autres langues.

## Onglet Medias

L'onglet **Medias** vous permet de gerer les images de vos produits a l'aide de la Mediatheque integree.

![Onglet Medias](/static/core/admin/img/help/add-product/media-tab.webp)

1. Cliquez sur **+ Ajouter des Images depuis la Mediatheque** pour ouvrir le selecteur de medias.
2. Selectionnez des images existantes ou telechargez-en de nouvelles directement.
3. Faites glisser les images pour les reordonner — la **premiere image** devient l'image principale du produit affichee dans les listings et les fiches.
4. Choisissez un **Type de Galerie** pour controler l'affichage des images sur la page produit : Galerie Standard, Carrousel, Disposition en Grille, Galerie Zoom ou Vue a 360°.

## Onglet Tarification

Definissez les prix de votre produit et configurez les promotions.

![Onglet Tarification](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Tarification Standard

- **Prix Normal** — Le prix de vente standard que les clients verront.
- **Devise** — Selectionnez la devise (la devise par defaut de votre boutique est preselectionnee).
- **Cout** — Votre cout d'achat, utilise pour les calculs de rentabilite. Ce montant n'est jamais affiche aux clients.

### Parametres de Promotion

Configurez des remises temporaires :

- **Type de Promotion** — Choisissez parmi : Aucune Promotion, Prix de Vente Fixe, Reduction en Montant ou Reduction en Pourcentage.
- **Valeur de la Promotion** — Le montant ou le pourcentage de la remise.
- **Dates de Debut/Fin** — Planifiez l'activation et l'expiration de la promotion. Laissez vide pour un debut immediat ou sans date de fin.

## Onglet Inventaire

Gerez les niveaux de stock et les attributs physiques du produit.

![Onglet Inventaire](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestion des Stocks

- **Suivre l'Inventaire** — Activez pour suivre les quantites en stock (active par defaut).
- **Seuil de Stock Bas** — Recevez des alertes lorsque le stock descend en dessous de ce nombre (par defaut : 5).
- **Quantite en Stock** — Nombre total d'unites disponibles.
- **Autoriser les Precommandes** — Activez pour accepter les commandes meme en rupture de stock.

### Attributs Physiques

Saisissez le poids du produit (kg) et ses dimensions (longueur, largeur, hauteur en cm) pour des calculs d'expedition precis.

### Identifiants Produit

Codes produit standards pour les places de marche et les systemes de gestion des stocks :

- **GTIN** — Numero Global d'Article Commercial
- **EAN** — Numero d'Article Europeen
- **UPC** — Code Produit Universel (US)
- **ISBN** — Pour les livres
- **ASIN** — Identifiant Amazon
- **MPN** — Reference Fabricant

### Expedition Internationale / Douanes

Requis pour les envois internationaux :

- **Code SH** — Code de classification du Systeme Harmonise
- **Pays d'Origine** — Pays de fabrication du produit
- **Prix Unitaire Douanier** — Valeur declaree par unite pour les douanes

## Onglet SEO

Optimisez la visibilite de votre produit dans les moteurs de recherche.

![Onglet SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Titre Meta** — Le titre affiche dans les resultats des moteurs de recherche. Cliquez sur l'icone globe pour traduire.
- **Description Meta** — Une breve description pour les resultats de recherche (160 caracteres maximum). Cliquez sur l'icone globe pour traduire.
- **Generer le SEO automatiquement** — Cochez pour generer automatiquement le contenu SEO lors de l'enregistrement du produit.

Un **Apercu du Resultat de Recherche** en direct montre exactement comment votre produit apparaitra dans les resultats de recherche Google.

## Enregistrer Votre Produit

Lorsque vous etes pret, utilisez les boutons d'enregistrement dans le coin superieur droit :

- **Enregistrer** (coche) — Enregistre et reste sur la page du produit.
- **Enregistrer et continuer la modification** — Enregistre et reste sur le formulaire pour continuer a travailler.

Votre produit sera visible sur la vitrine une fois son statut defini sur **Publie**.

## Conseils

- Commencez avec le statut **Brouillon** pour perfectionner le produit avant que les clients ne le voient.
- Telechargez plusieurs images — les produits avec plusieurs photos se vendent mieux.
- Remplissez les champs **SEO** pour ameliorer la visibilite dans les moteurs de recherche.
- Utilisez les **Categories** et les **Marques** pour aider les clients a naviguer dans votre catalogue.
- Pour les produits variables (par exemple, differentes tailles ou couleurs), choisissez le type **Produit Variable** et ajoutez des variantes apres l'enregistrement.
