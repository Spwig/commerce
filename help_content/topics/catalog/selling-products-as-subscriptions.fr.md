---
title: Vendre des produits en tant que abonnements
---

Tout produit Simple, Variable ou Numérique peut désormais être vendu de manière récurrente, à côté ou à la place d'un achat unique. Ce guide couvre l'activation des abonnements pour un produit, le choix des forfaits parmi lesquels les clients peuvent s'abonner, et ce que vos clients voient réellement lorsqu'ils achètent.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: La forme de modification du produit avec l'onglet Abonnements actif, montrant
    Cocher Activer l'abonnement, un ou plusieurs forfaits sélectionnés dans le champ Forfaits d'abonnement, et les cases à cocher Autoriser l'achat unique / Défaut vers l'abonnement visibles.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (magasin) page de détail du produit pour un produit compatible abonnement
  filename: subscribe-and-save-selector.webp
  description: Le sélecteur "Acheter une fois" vs "S'abonner et économiser" déroulé, montrant une liste de niveaux de fréquence de livraison avec un badge "Économisez X%" sur les niveaux discount.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Exige un produit compatible abonnement réel avec au moins un forfait actif public et des tranches de tarification, consulté depuis le magasin (pas l'administration).
-->

## Quels types de produits peuvent être vendus en tant qu'abonnements

Les abonnements ne sont disponibles que pour ces types de produits :

| Éligible | Non éligible |
|----------|---------------|
| Produit simple | Produit en vrac |
| Produit variable | Carte cadeau |
| Produit numérique | Produit personnalisable |
| | Produit configurable |
| | Produit de réservation |

La raison en est la livraison, pas le prix : un abonnement facture à nouveau votre client à chaque cycle et lui réexpédie le produit à travers une nouvelle commande à chaque fois. Spwig sait comment réexpédier un produit simple ou variable et réattribuer un produit numérique sa téléchargement ou sa licence à chaque renouvellement - mais il ne peut pas s'assurer de réexécuter une émission de carte cadeau, un ensemble à composants multiples, une personnalisation sauvegardée du client, une construction d'un configurateur, ou une case de réservation sur un planning récurrent. Permettre à ces types de produits d'être vendus en tant qu'abonnements risquerait de prendre l'argent du client au cycle 2 sans pouvoir lui fournir quoi que ce soit.

La case à cocher **Activer l'abonnement** n'est pas masquée ou grise pour les types non éligibles - vous pouvez techniquement la cocher sur n'importe quel produit. Si vous essayez de sauvegarder un produit de carte cadeau, de produit en vrac, de produit personnalisable, de produit configurable ou de produit de réservation avec les abonnements activés, Spwig refusera la sauvegarde avec une erreur de validation expliquant que ce type de produit ne peut pas être vendu en tant qu'abonnement. Changez d'abord le **Type de produit** (onglet Informations de base), ou laissez les abonnements désactivés pour ce produit.

## Activation des abonnements sur un produit

1. Accédez à **Produits > Tous les produits** et ouvrez le produit que vous souhaitez vendre en tant qu'abonnement (ou créez-en un nouveau).
2. Vérifiez que le **Type de produit** sur l'onglet Informations de base est Simple, Variable ou Numérique.
3. Cliquez sur l'onglet **Abonnements**.
4. Cochez **Activer l'abonnement**.
5. Dans le champ **Forfaits d'abonnement**, sélectionnez un ou plusieurs forfaits que ce produit devrait proposer. Vous ne pouvez choisir que des forfaits qui existent déjà - si vous n'avez pas encore créé de forfaits, consultez d'abord [Forfaits d'abonnement](/help/subscription-plans).
6. Configurez les deux cases à cocher de mode d'achat (ci-dessous).
7. Cliquez sur **Enregistrer**.

## Attacher des forfaits d'abonnement

Un **Forfait d'abonnement** est un modèle réutilisable - options de fréquence de facturation, essai, frais d'ouverture, règles de désistement - que vous créez une fois et pouvez attacher à n'importe quel nombre de produits éligibles. Le champ **Forfaits d'abonnement** sur l'onglet Abonnements du produit est l'endroit où vous reliez le produit aux forfaits qu'il devrait être vendu.

Vous pouvez attacher plus d'un forfait au même produit.

Cela est utile lorsqu'on souhaite proposer un niveau récurrent "Standard" et "Premium" pour le même article - chaque forfait peut avoir ses propres tranches de prix, son essai et sa politique de désistement.

Lorsqu'un produit possède plusieurs forfaits associés, les clients voient un sélecteur de forfait sur la page produit avant de choisir la fréquence de facturation.

## Contrôler les achats uniques et les abonnements

Deux cases à cocher sur l'onglet Abonnements contrôlent comment les clients peuvent acheter le produit :

- **Autoriser l'achat unique** — Coché par défaut. Lorsqu'il est coché, les clients choisissent entre un achat unique régulier et un abonnement. Décochez-le pour rendre le produit uniquement abonné - chaque achat devient une commande récurrente, et aucune option d'achat unique n'est affichée du tout.
- **Sélectionner par défaut l'abonnement** — Sélectionne l'option d'abonnement (et son forfait/tarif par défaut) lors du chargement de la page produit, plutôt que de demander aux clients de le choisir activement. Cela n'a d'effet que lorsqu'**Autoriser l'achat unique** est également coché - si l'achat unique est désactivé, le produit est uniquement abonné, indépendamment de ce paramètre.

Utilisez **Sélectionner par défaut l'abonnement** pour les produits où la livraison récurrente est l'attente naturelle (café, compléments nutritionnels, produits consommables) - cela élimine un clic et pousse les clients vers l'option qui les fait revenir, sans leur retirer la possibilité d'acheter une fois.

## Ce que les clients voient

### Sur la page produit

Lorsqu'un produit a les abonnements activés et qu'au moins un forfait actif, public est associé, un sélecteur de mode d'achat apparaît sur la page produit :

- Si l'achat unique est autorisé, les clients voient un choix entre **"Acheter une fois"** et **"S'abonner et économiser"**, par défaut selon le mode que vous avez configuré.
- Si le produit possède plus d'un forfait associé, un sélecteur de forfait apparaît une fois que **"S'abonner et économiser"** est sélectionné.
- Pour le forfait choisi, les clients voient une liste de **fréquence de livraison** construite à partir des tranches de prix de ce forfait (par exemple : Mensuel, Trimestriel, Annuel), chacune montrant son prix et un **badge "Économisez X%"** lorsqu'une tranche comporte une remise.
- La durée d'essai, la frais de mise en service et la politique de résiliation du forfait (par exemple : "Résiliez à tout moment") sont affichés avec la liste des tranches, ainsi qu'une note indiquant qu'une méthode de paiement est ajoutée lors de la caisse.

### Dans le panier et lors de la caisse

Les articles d'abonnement dans le panier portent une **étiquette Abonnement**, la périodicité de facturation (par exemple : "Tous les mois") et une note d'essai si applicable, afin que le client sache clairement quels articles sont récurrents. Lors de la caisse, le client choisit un fournisseur de paiement comme d'habitude - c'est la méthode de paiement qui sera facturée lors des renouvellements futurs.

> **Limiter connue :** Enregistrer automatiquement la carte du client pour les renouvellements d'abonnement lors de la caisse est toujours en cours de connexion pour certains fournisseurs de paiement. Jusqu'à ce qu'un fournisseur spécifique prenne en charge cela, les abonnements passés via celui-ci peuvent avoir besoin d'une vérification supplémentaire (par exemple, contacter le client pour obtenir des coordonnées de paiement mises à jour avant un renouvellement) plutôt que d'être entièrement sans intervention dès le premier jour. Vérifiez avec votre configuration de fournisseur de paiement si vous constatez que les renouvellements ne se font pas automatiquement pour un abonnement.

## Conseils

- Créez et testez d'abord le forfait d'abonnement (tranches de prix, essai, politique de résiliation), puis attachez-le aux produits - il est plus facile d'obtenir le bon forfait dès le début que de le corriger sur plusieurs produits plus tard.
- Laissez **Autoriser l'achat unique** coché pour la plupart des produits. Réservez les produits uniquement abonnés pour les cas où un achat unique ne convient vraiment pas à votre entreprise.
- Si vous transformez un produit phare existant en option d'abonnement, laissez **Sélectionner par défaut l'abonnement** désactivé au départ afin de ne pas perturber les clients habitués à l'acheter une fois - activez-le plus tard une fois avoir vu comment les abonnés réagissent.
- Les produits numériques sont un excellent choix pour les abonnements (licences logicielles, abonnements contenus) car le renouvellement restaure automatiquement l'accès sans livraison impliquée.
- Si vous avez besoin d'un type de produit qui n'est pas éligible (un ensemble ou un article personnalisable, par exemple) pour être vendu de manière récurrente, envisagez si un équivalent simplifié ou numérique pourrait porter l'abonnement à la place.