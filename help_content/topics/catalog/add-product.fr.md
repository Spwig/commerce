---
title: Ajout d'un produit
---

Ce guide vous guide à travers la création d'un nouveau produit dans votre magasin. Le formulaire de produit est organisé en sections couvrant les informations de base, les médias, les prix, l'inventaire, le référencement (SEO), et bien plus encore - vous pouvez remplir l'ensemble en une seule fois ou revenir plus tard pour compléter des sections.

## Premiers pas

Depuis la barre latérale, accédez à **Produits > Tous les produits** pour voir votre catalogue de produits. Cliquez sur le bouton **+ Ajouter un produit** en haut à droite pour ouvrir le formulaire de création de produit.

![Page de liste des produits](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informations de base

La section **Informations de base** est là pour définir l'identité principale de votre produit.

![Formulaire d'ajout de produit](/static/core/admin/img/help/add-product/add-product-form.webp)

### Champs obligatoires

- **Nom** — Le nom du produit affiché aux clients. Cliquez sur l'icône du globe pour ajouter des traductions pour d'autres langues.
- **Slug** — Version convivible pour les URL (généré automatiquement). Personnalisez-le si nécessaire.
- **SKU** — Votre code d'unité de gestion de stock interne.
- **Type de produit** — Choisissez parmi : Simple, Variable, Numérique, Forfait, Chèque-cadeau, Personnalisable, Configurable ou Réservation.
- **Catégorie** — Attribuez le produit à une catégorie pour l'organisation et la navigation sur le site.

### Statut et visibilité

Trouvé dans la section **Statut** en bas du formulaire :

- **Statut** — Défini sur **Brouillon** pendant que vous travaillez, **Publié** lorsque prêt à vendre, ou **Discontinué** pour les produits que vous ne proposez plus.
- **Est-ce une vedette** — Cochez pour mettre en évidence ce produit sur votre site.
- **Est-ce un produit numérique** — Cochez si ce produit inclut des téléchargements numériques (fichiers, licences). Peut être combiné avec n'importe quel type de produit.
- **Cacher du site** — Cache le produit des listes de catalogue tout en le maintenant disponible en tant qu'option de configurateur ou composant de forfait.

### Champs facultatifs

- **Marque** — Associez-le à une marque si applicable.
- **Balises** — Attribuez une ou plusieurs balises dans la carte **Balises** plus bas sur cette onglet. Les balises sont distinctes des Collections — ce sont des étiquettes rapides et libres pour organiser et filtrer les produits plutôt qu'un regroupement de merchandising. Tapez pour rechercher une balise existante, ou tapez un nouveau nom pour la créer en temps réel. Consultez le sujet d'aide **Balises de produit** pour créer, renommer et supprimer en bloc des balises directement.

### Descriptions du produit

- **Description courte** — Apparaît dans les listes de produits et les cartes. Gardez-la brève et percutante.
- **Description complète** — Description détaillée du produit affichée sur la page de détail du produit. Utilisez l'éditeur de texte riche pour ajouter de la mise en forme, des images, des vidéos et des tableaux.

Les deux champs de description prennent en charge la fonction de traduction — cliquez sur l'icône du globe pour fournir du contenu dans d'autres langues.

La section **Détails du produit** contient deux champs de données structurées :

- **Caractéristiques** — Paires clé-valeur pour les points forts du produit (ex. : "Durée de batterie : 20 heures").
- **Spécifications** — Détails techniques pour l'onglet des spécifications sur la page produit (ex. : "Processeur : Intel i7").

## Médias

La section **Médias** vous permet de gérer les images du produit à l'aide de la bibliothèque de médias intégrée.

![Onglet Médias](/static/core/admin/img/help/add-product/media-tab.webp)

1. Cliquez sur **+ Ajouter des images depuis la bibliothèque de médias** pour ouvrir le sélecteur de médias.
2. Sélectionnez des images existantes ou téléversez de nouvelles images directement.
3. Glissez les images pour les réordonner — la **première image** devient l'image principale du produit affichée dans les listes et les cartes.

Le champ **Type de galerie**, dans la carte **Paramètres de la galerie** située sous la liste d'images, détermine comment les images sont affichées sur le magasin : Galerie standard, Carousel, disposition en grille, galerie avec zoom, ou vue 360°.

## Prix

Définissez le prix de votre produit et configurez les ventes.

![Onglet Prix](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Prix régulier

- **Prix régulier** — Le prix de détail standard que les clients verront. La devise est définie avec le montant du prix.
- **Coût** — Votre coût de marchandises, utilisé pour les calculs de bénéfice. Cela n'est jamais affiché aux clients.

### Paramètres de la vente

Configurez des remises temporaires :

- **Type de vente** — Choisissez entre : Aucune vente, Prix de vente fixe, Montant réduit, ou Pourcentage réduit.
- **Valeur de la vente** — Le montant de la remise ou le pourcentage.
- **Date de début de la vente / Date de fin de la vente** — Planifiez quand la vente active et expire. Laissez vide pour un démarrage immédiat ou pas de date de fin.

### Prix multivalute

Si le multivalute est activé sur votre magasin, un champ **Stratégie de prix** apparaît :

- **Prix dynamique** — Les prix dans les autres devises sont calculés automatiquement à l'aide des taux de change configurés.
- **Prix fixe** — Définissez un prix spécifique pour chaque devise indépendamment à l'aide de la section **Prix multivalute** qui apparaît ci-dessous.

## Stock

Gérez les niveaux de stock, le comportement d'expédition et les attributs du produit physique.

![Onglet Stock](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestion du stock

- **Suivi du stock** — Activez pour surveiller les quantités de stock (activé par défaut).
- **Seuil de stock faible** — Recevez des alertes lorsqu'une quantité de stock tombe en dessous de ce nombre (valeur par défaut : 5).
- **Commandes en attente** — Activez pour accepter les commandes même lorsqu'elles sont en rupture de stock.
- **Action en cas de rupture de stock** — Remplacez le comportement du site ou de la catégorie lorsqu'un produit est en rupture de stock : le cacher, l'afficher comme indisponible, afficher un bouton "Soyez informé", ou permettre les commandes en attente.

Les quantités de stock sont gérées par entrepôt. Après avoir enregistré le produit, utilisez la section **Éléments de stock** en bas du formulaire (ou naviguez vers **Produits > Éléments de stock**) pour définir les quantités dans chaque emplacement d'entrepôt.

### Attributs physiques

Entrez le poids du produit (kg) et les dimensions (longueur, largeur, hauteur en cm) pour des calculs d'expédition précis.

### Expédition

- **A-t-il besoin d'expédition** — Si ce produit doit être expédié au client. Activé par défaut pour les produits physiques ; votre magasin et la caisse l'utilisent pour décider si collecter l'adresse d'expédition et établir un devis pour la commande. Spwig le désactive automatiquement pour les produits Numériques, Réservations et Cadeaux, car ceux-ci ne sont jamais envoyés — vous n'avez pas besoin (et ne pouvez pas) de le réactiver pour ces types de produits. Laissez-le coché pour un produit physique qui ressemble à un produit numérique, comme une carte de cadeau imprimée qui est expédiée dans une boîte.
- **Colis d'expédition préféré** — Choisissez optionnellement l'un de vos colis d'expédition configurés. Lorsqu'il est défini, les dimensions propres à ce colis sont utilisées pour les calculs des tarifs d'expédition au lieu du poids et des dimensions du produit ci-dessus — utile lorsqu'un produit est toujours expédié dans la même boîte standard ou enveloppe. Laissez-le vide pour utiliser les attributs physiques du produit. Gérez les colis disponibles sous **Expédition > Colis**.

### Pré-commande

Conservez toutes les formattations markdown, les chemins d'images, les blocs de code et les termes techniques.

Utilisez la carte **Pré-commande** pour vendre un produit avant qu'il n'ait de stock — utile pour les lancements à venir que vous souhaitez commencer à prendre des commandes avant le lancement :

- **Est-ce une pré-commande** — Activez pour permettre aux clients d'acheter ce produit même s'il est en rupture de stock.
- **Date de lancement de la pré-commande** — La date d'arrivée attendue, affichée aux clients.
- **Message de pré-commande** — Un court message personnalisé affiché aux clients, limité à 200 caractères (exemple : « Envoi en mars 2026 »).

### Identifiants de produit

Codes de produit standards pour les listes de marchés et les systèmes de stock :

- **GTIN** — Numéro d'élément de commerce international
- **EAN** — Numéro d'article européen
- **UPC** — Code produit universel (États-Unis)
- **ISBN** — Pour les livres
- **ASIN** — Identifiant Amazon
- **MPN** — Numéro de pièce du fabricant

### Expédition internationale / douane

Obligatoire pour les envois internationaux (développez la section **Expédition internationale / Douane**) :

- **Code HS** — Code de classification du système harmonisé
- **Pays d'origine** — Lieu de fabrication du produit
- **Prix unitaire douanier** — Valeur déclarée par unité pour les douanes
- **Numéro de licence d'exportation** — Nécessaire uniquement pour les articles contrôlés ou restreints
- **Date d'expiration de la licence d'exportation** — Date d'expiration de la licence d'exportation

## SEO

Optimisez la visibilité de votre produit sur les moteurs de recherche.

![onglet SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Titre méta** — Le titre affiché dans les résultats des moteurs de recherche. Cliquez sur l'icône du globe pour traduire.
- **Description méta** — Une brève description pour les résultats de recherche (maximum 160 caractères). Cliquez sur l'icône du globe pour traduire.
- **Génération SEO automatique** — Cochez pour générer automatiquement le contenu SEO lorsque le produit est enregistré.

Une **aperçu de résultat de recherche** en direct montre exactement comment votre produit apparaîtra dans les résultats de recherche de Google.

## Paramètres de la page produit

Sur l'onglet **Avancé**, la carte **Paramètres de la page produit** vous permet de contrôler l'apparence de la page produit sur le site marchand :

- **Modèle de page** — Remplacez le modèle de mise en page du site par défaut pour ce produit unique : Classique, Pleine largeur, Focus sur la galerie, ou Numérique. Laissez-le défini sur **Utiliser le modèle du site** pour hériter de la mise en page spécifiée dans vos paramètres de conception — la plupart des produits devraient rester sur le modèle par défaut afin que les modifications du modèle s'appliquent automatiquement.
- **Afficher les produits associés** — Afficher les produits associés en bas de la page.
- **Afficher les avis** — Afficher les avis clients.
- **Afficher les spécifications** — Afficher l'onglet des spécifications.

Le champ **Type de galerie** — qui contrôle l'affichage des images de produit (Galerie standard, Diapos, disposition en grille, galerie zoom, ou vue 360°) — est défini séparément, sur l'onglet **Médias**.

## Canal de vente

Le champ **Canal de vente** (dans la section Statut) contrôle les endroits où le produit peut être vendu :

- **Tous les canaux** — Disponible en ligne et en magasin (POS).
- **Seulement en ligne** — Non disponible via les terminaux POS.
- **Seulement en magasin** — Non listé en ligne ; uniquement disponible dans votre magasin physique.

Un champ **Code-barres** est également disponible pour la lecture des codes-barres POS.

## Enregistrement de votre produit

Lorsque vous êtes prêt, utilisez les boutons d'enregistrement dans le coin supérieur droit. Votre produit sera visible sur le site marchand une fois que son statut est défini sur **Publié**.

## Conseils

Conservez toutes les formattages markdown, les chemins d'images, les blocs de code et les termes techniques.

- Commencez avec le statut **Brouillon** afin de perfectionner le produit avant que les clients ne le voient.
- Téléversez plusieurs images : les produits avec plusieurs photos ont plus de chances de bien se vendre.
- Remplissez les champs **SEO** pour améliorer la visibilité dans les moteurs de recherche.
- Utilisez les **Catégories**, **Marques** et **Mots-clés** pour aider les clients à naviguer dans votre catalogue.
- Pour les produits variables (par exemple, différentes tailles ou couleurs), choisissez le type **Produit variable** et ajoutez des variantes après avoir enregistré.
- Utilisez les **Caractéristiques** et les **Spécifications** pour ajouter des données structurées sur le produit qui s'affichent dans des onglets dédiés sur la page produit.
- Si **Exige une livraison** ne reste pas coché, vérifiez le **Type de produit** : Spwig désactive automatiquement la livraison pour les produits Numériques, Réservations et Chèques-cadeaux, car aucun de ceux-ci n'est physiquement envoyé.
- Définissez un **Colis de livraison préféré** pour les produits qui sont toujours envoyés dans le même emballage - cela vous évite d'avoir à maintenir les poids et dimensions de ce produit en synchronisation avec la boîte que vous utilisez réellement.