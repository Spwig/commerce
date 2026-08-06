---
title: Disponibilité par région
---

La disponibilité par région détermine lesquelles de vos régions de vente un produit peut être vendu, et comment les acheteurs en dehors de ces régions expérimentent votre catalogue. Utilisez-la lorsque qu'un produit n'est autorisé que pour certains pays, lorsqu'un stock est réservé à un marché local, ou lorsque vous lancez un nouveau produit région par région.

Cela s'appuie sur les **régions de vente**, qui regroupent les pays en marchés nommés (voir le guide des régions de vente pour les configurer). Une fois que vos régions existent, vous pouvez restreindre les produits individuels à celles-ci et décider de la manière dont les produits restreints s'affichent aux acheteurs qui ne peuvent pas les acheter.

## Restreindre un produit à des régions spécifiques

Chaque produit dispose d'un paramètre **Disponibilité par région** sur sa page de modification. Ouvrez **Produits > Tous les produits**, sélectionnez un produit, puis trouvez-le dans la section **Statut** à côté de **Statut**, **Mis en avant** et **Masquer du storefront**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Page de modification du produit défilée vers la section Statut, avec la case de sélection de la disponibilité par région visible et définie sur « Uniquement dans les régions sélectionnées »
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Utilisez un produit avec au moins 2 régions déjà sélectionnées ci-dessous, si possible, afin que le tableau intérieur ait des lignes visibles dans la deuxième image.
-->

| Option | Ce que cela signifie |
|--------|--------------------|
| **Disponible dans toutes les régions** | Aucune restriction. Le produit est vendu partout. C'est la valeur par défaut pour chaque produit. |
| **Uniquement dans les régions sélectionnées** | Une liste autorisée. Le produit n'est vendu que dans les régions que vous sélectionnez ci-dessous - ailleurs, il est considéré comme non disponible. |
| **Toutes les régions sauf les régions sélectionnées** | Une liste de blocage. Le produit est vendu partout *sauf* les régions que vous sélectionnez ci-dessous. |

### Sélectionner les régions

Sous la section Statut, un tableau intitulé **Disponibilité par région (régions sélectionnées)** liste les régions auxquelles le mode ci-dessus s'applique.

1. Définissez **Disponibilité par région** sur **Uniquement dans les régions sélectionnées** ou **Toutes les régions sauf les régions sélectionnées**.
2. Dans le tableau **Disponibilité par région (régions sélectionnées)**, cliquez sur **Ajouter une autre région** et sélectionnez une région de vente.
3. Répétez pour chaque région que vous souhaitez ajouter.
4. Cliquez sur **Enregistrer**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: Le tableau intitulé « Disponibilité par région (régions sélectionnées) » avec deux ou trois lignes de région ajoutées
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Si **Disponibilité par région** est définie sur **Disponible dans toutes les régions**, tout ce qui se trouve dans ce tableau est ignoré - effacez d'abord le menu déroulant de mode si vous souhaitez supprimer une restriction sans supprimer les lignes.

Pour une vue globale du catalogue de chaque règle de région d'un produit dans une seule liste (utile lorsque vous auditez plusieurs produits à la fois), rendez-vous sur **Visibilité des produits par région** à l'adresse `/admin/catalog/productregionvisibility/`.

## Affichage aux acheteurs pour lesquels le produit ne livre pas

Lorsqu'une région d'acheteur ne correspond pas aux règles de disponibilité d'un produit, vous contrôlez ce qu'ils voient dans **Paramètres d'affichage du stock**, sous la section **Disponibilité par région**. Cette page n'a pas encore de raccourci de barre latérale - ouvrez-la directement à l'adresse `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Formulaire de modification des paramètres d'affichage du stock défilé vers le champ **Disponibilité par région**, montrant la case de sélection de l'affichage restreint par région
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

| Option | Ce que les clients voient |
|--------|-------------------|
| **Afficher, marqué comme indisponible** (par défaut) | Le produit apparaît toujours dans les listes, avec un badge "Indisponible" et une notice "Ne livre pas vers [région]" à la place du bouton "Ajouter au panier". Un bandeau s'affiche également en haut des pages de liste ("Certains produits ne sont pas livrables vers [destination]") avec un lien pour filtrer uniquement les articles qui y sont livrables. |
| **Cacher des listes** | Le produit est supprimé des listes et des résultats de recherche pour les clients de cette région. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Liste de produits du magasin avec le bandeau de région en haut et au moins une carte de produit montrant le badge "Indisponible" et la notice "Ne livre pas vers [région]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Nécessite une sélection de destination en direct (ou détection GeoIP) qui aboutit à une région restreinte par un produit démonstration.
-->

Un produit restreint affiche toujours une notice "Ce produit ne livre pas vers [région]" lorsqu'un client y accède directement (par exemple, à partir d'un lien partagé ou d'un résultat de moteur de recherche) — cela s'applique quel que soit le paramètre de liste que vous choisissez ci-dessus, car un lien direct contourne entièrement la liste.

## Permettre aux clients de choisir ou de découvrir leur région

Spwig peut détecter la région d'un client automatiquement et proposer un changement, et vous pouvez ajouter un sélecteur pour permettre aux clients de le modifier à tout moment.

### Avant de commencer

Vous avez besoin de deux éléments configurés pour que la détection et le changement de région fonctionnent correctement :

1. **Zones de vente** — les pays de chaque région et la devise par défaut de chaque région. Si vous ne voyez pas **Zones de vente** sous **Inventaire** dans la barre latérale, activez **Activer plusieurs entrepôts** sous **Paramètres > Paramètres de la boutique > Commerce électronique** pour afficher le lien du menu (vous n'avez pas besoin d'utiliser réellement plusieurs entrepôts — ce paramètre n'ouvre que l'élément de menu). Vous pouvez également accéder directement à `/admin/catalog/salesregion/`.
2. **Pays de livraison** — les pays vers lesquels votre magasin livre effectivement. Ceux-ci sont généralement déjà en place : chaque pays que vous ajoutez à une zone de livraison est automatiquement ajouté ici. Pour consulter ou ajuster manuellement la liste, ouvrez directement `/admin/shipping/shippingcountry/` (il n'a toujours pas de lien dans la barre latérale).

### La confirmation automatique de la région

Spwig détecte la région d'un client à partir de leur emplacement et l'applique automatiquement. Lorsque cela les place dans une région *autre que* le marché principal (par défaut) de votre magasin — et que vous avez deux ou plusieurs Zones de vente actives — Spwig affiche une confirmation lors de leur première visite afin qu'ils sachent quelle région ils ont choisie et puissent la modifier :

> **Nous avons défini votre région sur [Région]**
> Nous avons choisi cela en fonction de votre localisation afin que vous voyiez les bons produits et prix. Ce n'est pas correct ? Choisissez votre pays.
> Livrer vers : [sélecteur de pays]  **[Continuer les achats]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: La fenêtre modale "Nous avons défini votre région sur [Région]" sur la page d'accueil du magasin, avec le sélecteur de pays et le bouton Continuer les achats
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Nécessite une résolution GeoIP vers une région non par défaut et au moins 2 Zones de vente actives pour déclencher. Localement, définissez un cookie "geo_country" sur un pays non par défaut pour le simuler.
-->

Choisir un autre pays dans le sélecteur les change immédiatement. Fermer la fenêtre ou cliquer sur **Continuer les achats** conserve leur région actuelle, et ils ne seront plus interrogés sur ce navigateur. Les visiteurs déjà dans leur région par défaut ne reçoivent pas du tout la confirmation.

### Ajouter un sélecteur de livraison à votre en-tête ou pied de page

Si vous préférez permettre aux clients de modifier la région eux-mêmes à tout moment (au lieu de ne compter que sur l'invitation automatique), ajoutez le widget **Sélecteur de livraison** à votre en-tête ou pied de page.

1.

Accédez à **Conception > Constructeur d'en-tête** (ou **Constructeur de pied de page**).
2.

Glissez le widget **Sélecteur de livraison** depuis la bibliothèque de widgets dans une ligne.
3.

Cliquez sur **Enregistrer**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Constructeur d'en-tête avec la barre latérale de la bibliothèque de widgets ouverte et le widget Sélecteur de livraison visible/en évidence
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Le widget n'a pas besoin de configuration — il affiche automatiquement vos pays de livraison actifs, et affiche la sélection actuelle d'un client (ou le pays détecté par GeoIP, s'ils n'ont pas encore choisi de pays). Choisir un autre pays met à jour immédiatement leur région et recharge la disponibilité et les prix des produits de la page.

Le Sélecteur de livraison n'a pas encore de formulaire de paramètres dédié. Si vous souhaitez modifier le style du bouton (contour, plein ou fantôme) ou cacher l'étiquette "Livrer à", ouvrez les paramètres du widget dans le constructeur et éditez directement le champ **Configuration personnalisée (JSON)**, en utilisant `button_style` et `show_label`.

### Devise selon la région

Si votre magasin prend en charge plus d'une devise (définie sous **Paramètres > Multidevise**), le passage de région — qu'il s'agisse de la fenêtre d'invite ou du Sélecteur de livraison — change également la devise affichée par celle par défaut de la région. Si votre magasin n'a qu'une seule devise, ou n'a pas activé explicitement une seconde, la devise reste inchangée lorsqu'un client change de région.

## Conseils

- Laissez **Disponibilité par région** sur **Disponible dans toutes les régions** à moins d'avoir une raison spécifique de restreindre un produit - c'est l'option la plus simple et ne nécessite aucun entretien lorsque vous ajoutez des régions ultérieurement.
- Utilisez **Uniquement dans les régions sélectionnées** pour un petit liste blanche (par exemple, un produit lancé dans un seul pays d'abord) et **Toutes les régions sauf les régions sélectionnées** pour un petit liste noire (par exemple, partout sauf un pays où l'article n'est pas autorisé) - choisissez celui qui nécessite moins de lignes pour la configuration.
- Si les clients signalent qu'un produit manque alors qu'il devrait être visible, vérifiez à la fois le paramètre **Disponibilité par région** du produit et si leur pays est couvert par un **Pays de vente** actif et un **Pays de livraison** actif.
- **Cacher des listes** permet de garder votre catalogue propre pour les clients qui ne peuvent pas acheter certains articles, mais cela signifie également que la commercialisation et la recherche seront plus minces dans ces régions - **Afficher, marqué comme indisponible** est généralement plus pertinent si vous souhaitez toujours que les clients parcourent l'ensemble de votre catalogue, même s'ils ne peuvent pas passer commande.
- Testez le comportement des régions en ajoutant le Sélecteur de livraison à votre en-tête et en passant d'un pays à l'autre vous-même avant de vous reposer sur la détection GeoIP lors d'une mise en ligne.
- Définissez vos valeurs de priorité des régions (sur la page des régions de vente) de manière délibérée - la région la plus prioritaire active est la sauvegarde pour les clients dont le pays ne peut pas être détecté ou ne correspond à aucune région.