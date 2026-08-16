---
title: Disponibilité par région
---

La disponibilité par région détermine lesquelles de vos régions de vente un produit peut être vendu, et comment les acheteurs en dehors de ces régions expérimentent votre catalogue. Utilisez-le lorsque qu'un produit n'est autorisé que pour certains pays, lorsque le stock est réservé à un marché local, ou lorsque vous lancez un nouveau produit région par région.

Cela s'appuie sur les **régions de vente**, qui regroupent les pays en marchés nommés (voir le guide des régions de vente pour les configurer). Une fois que vos régions existent, vous pouvez limiter les produits individuels à celles-ci et décider comment les produits restreints s'affichent aux acheteurs qui ne peuvent pas les acheter.

## Limiter un produit à des régions spécifiques

Chaque produit dispose d'un paramètre **Disponibilité par région** sur sa page de modification. Ouvrez **Produits > Tous les produits**, sélectionnez un produit, puis trouvez-le dans la section **Statut** à côté de **Statut**, **Mis en avant** et **Masquer du magasin**.

![La section Statut du formulaire de modification du produit, avec la case de sélection de la disponibilité par région définie sur "Seulement dans les régions sélectionnées" à côté de Mis en avant et Masquer du magasin](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Option | Ce que cela signifie |
|--------|--------------------|
| **Disponible dans toutes les régions** | Aucune restriction. Le produit est vendu partout. C'est la valeur par défaut pour chaque produit. |
| **Seulement dans les régions sélectionnées** | Une liste d'autorisation. Le produit n'est vendu que dans les régions que vous sélectionnez ci-dessous - partout ailleurs, il est considéré comme non disponible. |
| **Toutes les régions sauf les régions sélectionnées** | Une liste de blocage. Le produit est vendu partout *sauf* les régions que vous sélectionnez ci-dessous. |

### Sélectionner les régions

Sous la section Statut, une table intitulée **Disponibilité par région (régions sélectionnées)** liste les régions auxquelles le mode ci-dessus s'applique.

1. Définissez **Disponibilité par région** sur **Seulement dans les régions sélectionnées** ou **Toutes les régions sauf les régions sélectionnées**.
2. Dans la table **Disponibilité par région (régions sélectionnées)**, cliquez sur **Ajouter une autre région** et sélectionnez une région de vente.
3. Répétez pour chaque région que vous souhaitez ajouter.
4. Cliquez sur **Enregistrer**.

![La table en ligne "Disponibilité par région (régions sélectionnées)" avec les lignes Amérique du Nord et Europe ajoutées](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Si **Disponibilité par région** est définie sur **Disponible dans toutes les régions**, tout ce qui se trouve dans cette table est ignoré - effacez d'abord le menu déroulant si vous souhaitez supprimer une restriction sans supprimer les lignes.

Pour une vue globale du catalogue de chaque produit sur les règles de région dans une seule liste (utile lorsque vous auditez plusieurs produits à la fois), rendez-vous sur **Visibilité des produits par région** à `/admin/catalog/productregionvisibility/`.

## Affichage aux acheteurs pour lesquels le produit ne livre pas

Lorsqu'une région d'acheteur ne correspond pas aux règles de disponibilité d'un produit, vous contrôlez ce qu'ils voient dans **Paramètres d'affichage du stock**, sous la section **Disponibilité par région**. Cette page n'a pas encore de raccourci de barre latérale - ouvrez-la directement à `/admin/catalog/stockdisplaysettings/`.

![Paramètres d'affichage du stock, section Disponibilité par région - la case de sélection de l'affichage par région, définie sur "Afficher, marqué comme non disponible"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Option | Ce que les acheteurs voient |
|--------|---------------------------|
| **Afficher, marqué comme non disponible** (par défaut) | Le produit s'affiche toujours dans les listes, avec un badge "Indisponible" et un avertissement "Ne livre pas vers [région]" à la place du bouton "Ajouter au panier". Un bandeau s'affiche également en haut des pages de liste ("Certains produits ne livrent pas vers [destination]) avec un lien pour filtrer uniquement les articles qui y livrent. |
| **Masquer des la liste** | Le produit est supprimé des listes et résultats de recherche pour les acheteurs de cette région. |

![Liste de produits du magasin livrant vers l'Europe - le bandeau "Certains produits ne livrent pas vers l'Europe" au-dessus de la grille, et une carte de produit marquée "Indisponible" avec un avertissement "Ne livre pas vers l'Europe"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

La page d'un produit restreint affiche toujours un avertissement « Ce produit n'est pas livrable en [région] » lorsqu'un acheteur y accède directement (par exemple, à partir d'un lien partagé ou d'un résultat de moteur de recherche) — cela s'applique indépendamment du choix de la liste que vous effectuez ci-dessus, car un lien direct contourne entièrement la liste.

## Permettre aux acheteurs de choisir ou de découvrir leur région

Spwig peut détecter la région d'un acheteur automatiquement et proposer un changement, et vous pouvez ajouter un sélecteur afin que les acheteurs puissent le modifier à tout moment.

### Avant de commencer

Vous avez besoin de deux éléments configurés correctement pour que la détection et le changement de région fonctionnent :

1. **Zones de vente** — les pays de chaque région et la devise par défaut de chaque région. Si vous ne voyez pas **Zones de vente** sous **Inventaire** dans la barre latérale, activez **Activer le stockage multiple** sous **Paramètres > Paramètres de la boutique > Commerce électronique** pour afficher le lien du menu (vous n'avez pas besoin d'utiliser réellement plusieurs entrepôts — ce paramètre n'ouvre que l'élément de menu). Vous pouvez également accéder directement à `/admin/catalog/salesregion/`.
2. **Pays de livraison** — les pays vers lesquels votre magasin effectue des livraisons. Ceux-ci sont généralement déjà en place : chaque pays que vous ajoutez à une zone de livraison est automatiquement ajouté ici également. Pour consulter ou ajuster manuellement la liste, ouvrez directement `/admin/shipping/shippingcountry/` (il n'a toujours pas de lien dans la barre latérale).

### La confirmation automatique de la région

Spwig détecte la région d'un acheteur à partir de leur emplacement et l'applique automatiquement. Lorsque cela les place dans une région *autre que* le marché principal (par défaut) de votre magasin — et que vous avez deux ou plusieurs zones de vente actives — Spwig affiche une confirmation lors de leur première visite afin qu'ils sachent dans quelle région ils se trouvent et puissent la changer :

> **Nous avons défini votre région sur [Région]**
> Nous avons choisi celle-ci en fonction de votre localisation afin que vous voyiez les bons produits et prix. Ce n'est pas correct ? Choisissez votre pays.
> Livrer à : [sélecteur de pays]  **[Continuer les achats]**

![La fenêtre de confirmation « Nous avons défini votre région sur l'Amérique du Nord » sur le site, avec un sélecteur de pays « Livrer à » et un bouton « Continuer les achats »](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Choisir un autre pays dans le sélecteur les fait immédiatement basculer. Fermer la fenêtre ou cliquer sur **Continuer les achats** conserve leur région actuelle, et ils ne seront plus interrogés sur ce navigateur. Les visiteurs déjà dans leur région par défaut ne reçoivent pas du tout la confirmation.

### Ajouter un sélecteur de livraison à votre en-tête ou pied de page

Si vous préférez permettre aux acheteurs de changer de région eux-mêmes à tout moment (au lieu de ne compter que sur l'invitation automatique), ajoutez le widget **Sélecteur de livraison** à votre en-tête ou pied de page.

1. Accédez à **Conception > Constructeur d'en-tête** (ou **Constructeur de pied de page**).
2. Glissez le widget **Sélecteur de livraison** depuis la bibliothèque de widgets dans une rangée.
3. Cliquez sur **Enregistrer**.

![La bibliothèque de widgets du Constructeur d'en-tête avec le groupe Shop sélectionné, montrant le widget Sélecteur de livraison à côté du Panier d'achat, du Menu de compte et du Sélecteur de langue](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Le widget n'a pas besoin de configuration — il affiche automatiquement vos pays de livraison actifs, et affiche la sélection actuelle d'un acheteur (ou le pays détecté par GeoIP, s'ils n'ont pas encore choisi). Sélectionner un autre pays met immédiatement à jour leur région et recharge les disponibilités et prix des produits.

Le Sélecteur de livraison n'a pas encore de formulaire de paramètres dédié. Si vous souhaitez modifier le style du bouton (contour, plein ou fantôme) ou cacher l'étiquette « Livrer à », ouvrez les paramètres du widget dans le constructeur et éditez directement le champ **Configuration personnalisée (JSON)**, en utilisant `button_style` et `show_label`.

### La devise suit la région

Si votre magasin prend en charge plus d'une devise (définie sous **Paramètres > Multidevises**), le changement de région — qu'il soit effectué via l'invitation ou le Sélecteur de livraison — change également la devise affichée en celle par défaut de la région.

Si votre magasin n'utilise qu'une seule devise, ou n'a pas activé explicitement une deuxième, la devise reste inchangée lorsqu'un client change de région.

## Conseils

- Laissez **Disponibilité des régions** sur **Disponible dans toutes les régions** à moins d'avoir une raison spécifique de restreindre un produit : c'est l'option la plus simple et ne nécessite aucun entretien lorsque vous ajoutez des régions ultérieurement.
- Utilisez **Seulement dans certaines régions** pour un petit liste blanche (par exemple, un produit lancé dans un seul pays d'abord) et **Toutes les régions sauf les régions sélectionnées** pour un petit liste noire (par exemple, partout sauf un pays où l'objet n'est pas autorisé) - choisissez celui qui nécessite moins de lignes pour la configuration.
- Si les clients signalent qu'un produit manque alors qu'il devrait être visible, vérifiez à la fois le paramètre **Disponibilité des régions** du produit et si leur pays est couvert par un **Région de vente** actif et un **Pays de livraison** actif.
- **Cacher des listes** maintient votre catalogue propre pour les clients qui ne peuvent pas acheter certains articles, mais cela signifie également que la promotion et la recherche seront plus minces dans ces régions - **Afficher, marqué comme indisponible** est généralement plus pertinent si vous souhaitez toujours que les clients parcourent l'ensemble de votre catalogue, même là où ils ne peuvent pas passer commande.
- Testez le comportement des régions en ajoutant le sélecteur de livraison à votre en-tête et en passant d'un pays à un autre vous-même avant de vous reposer sur la détection GeoIP lors d'un lancement.
- Définissez vos valeurs de priorité des régions (sur la page Régions de vente) de manière délibérée - la région la plus prioritaire active est la sauvegarde pour les clients dont le pays ne peut pas être détecté ou ne correspond à aucune région.