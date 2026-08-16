---
title: Vendre des produits en tant que abonnements
---

Tout produit Simple, Variable ou Numérique peut désormais être vendu de manière récurrente, à côté ou à la place d'un achat unique. Ce guide couvre l'activation des abonnements pour un produit, le choix des forfaits parmi lesquels les clients peuvent en choisir, et ce que vos clients voient réellement lorsqu'ils achètent.

## Quels types de produits peuvent être vendus en tant qu'abonnements

Les abonnements ne sont disponibles que pour ces types de produits :

| Éligible | Non éligible |
|----------|---------------|
| Produit Simple | Produit Forfait |
| Produit Variable | Carte Cadeau |
| Produit Numérique | Produit personnalisable |
| | Produit Configurable |
| | Produit de Réservation |

La raison en est la livraison, pas le prix : un abonnement facture à nouveau votre client à chaque cycle et lui réexpédie le produit via une nouvelle commande à chaque fois. Spwig sait comment réexpédier un produit Simple ou Variable et réattribuer un produit Numérique son téléchargement ou sa licence à chaque renouvellement - mais il ne peut pas s'assurer de réexécuter à nouveau l'émission d'une carte cadeau, un forfait à composants multiples, une personnalisation sauvegardée par le client, une construction de configurateur, ou une plage de réservation à un rythme récurrent. Permettre la vente de ces types en tant qu'abonnements risquerait de prendre l'argent du client au cycle 2 sans pouvoir lui fournir quoi que ce soit.

La case à cocher **Activer l'abonnement** n'est pas cachée ou grisé pour les types non éligibles - vous pouvez techniquement la cocher sur n'importe quel produit. Si vous essayez de sauvegarder un produit Carte Cadeau, Forfait, Personnalisable, Configurable ou Réservation avec les abonnements activés, Spwig refusera la sauvegarde avec une erreur de validation expliquant que ce type de produit ne peut pas être vendu en tant qu'abonnement. Changez d'abord le **Type de produit** (onglet Informations de base), ou désactivez les abonnements pour ce produit.

## Activer les abonnements sur un produit

1. Accédez à **Produits > Tous les produits** et ouvrez le produit que vous souhaitez vendre en tant qu'abonnement (ou créez-en un nouveau).
2. Vérifiez que le **Type de produit** sur l'onglet Informations de base est Simple, Variable ou Numérique.
3. Cliquez sur l'onglet **Abonnements**.
4. Cochez **Activer l'abonnement**.
5. Dans le champ **Forfaits d'abonnement**, sélectionnez un ou plusieurs forfaits que ce produit devrait proposer. Vous ne pouvez choisir que des forfaits qui existent déjà - si vous n'avez pas encore créé de forfaits, consultez d'abord [Forfaits d'abonnement](/help/subscription-plans).
6. Configurez les deux cases à cocher de mode d'achat (ci-dessous).
7. Cliquez sur **Enregistrer**.

![L'onglet Abonnements du formulaire d'édition du produit : la case **Activer l'abonnement** cochée, un forfait sélectionné dans la liste des forfaits d'abonnement, et les cases **Autoriser l'achat unique** et **Pré-sélectionner l'abonnement**](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Attacher des forfaits d'abonnement

Un **Forfait d'abonnement** est un modèle réutilisable - options de fréquence de facturation, essai, frais d'ouverture, règles de désistement - que vous créez une fois et pouvez attacher à n'importe quel nombre de produits éligibles. Le champ **Forfaits d'abonnement** sur l'onglet Abonnements du produit est l'endroit où vous reliez le produit aux forfaits qu'il devrait proposer.

Vous pouvez attacher plus d'un forfait au même produit. Cela est utile lorsque, par exemple, vous souhaitez proposer un niveau "Standard" et "Premium" récurrent pour le même article - chaque forfait peut avoir ses propres tranches de prix, son essai et sa politique de désistement. Lorsqu'un produit a plus d'un forfait attaché, les clients voient un sélecteur de forfait sur la page produit avant de choisir la fréquence de facturation.

## Contrôler les achats uniques vs. abonnements

Deux cases à cocher sur l'onglet Abonnements contrôlent comment les clients peuvent acheter le produit :

- **Autoriser l'achat unique** — activé par défaut.

Lorsqu'elle est cochée, les clients choisissent entre un achat unique régulier et un abonnement.

Décochez-la pour rendre le produit exclusif aux abonnements - chaque achat devient une commande récurrente, et aucun achat unique n'est affiché du tout.

Cela n'a d'effet que si **Autoriser l'achat unique** est également coché — si l'achat unique est désactivé, le produit n'est disponible que sous forme d'abonnement, indépendamment de ce paramètre.

Utilisez **Passer à l'abonnement par défaut** pour les produits où la livraison récurrente est l'attente naturelle (café, compléments alimentaires, produits consommables) : cela réduit un clic et pousse les clients vers l'option qui les incite à revenir, sans leur retirer la possibilité d'acheter une fois.

## Ce que les clients voient

### Sur la page produit

Lorsqu'un produit a les abonnements activés et qu'au moins un plan actif et public est attaché, un sélecteur de mode d'achat apparaît sur la page produit :

![Le sélecteur d'achat du magasin avec "Abonnement et économies" sélectionné : un achat unique par rapport à un commutateur Abonnement et économies au-dessus d'une liste de fréquence de livraison montrant des catégories Annuelle (Économisez 20 %), Mensuelle et Trimestrielle (Économisez 10 %) avec des prix, ainsi que des notes de période d'essai, de résiliation et de paiement](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Si l'achat unique est autorisé, les clients voient un choix **"Achat unique"** vs **"Abonnement et économies"**, par défaut sur le mode que vous avez configuré.
- Si le produit comporte plus d'un plan attaché, un sélecteur de plan apparaît une fois que "Abonnement et économies" est sélectionné.
- Pour le plan choisi, les clients voient une liste de **fréquence de livraison** construite à partir des tranches de prix de ce plan (par exemple, Mensuelle, Trimestrielle, Annuelle), chacune montrant son prix et un **sigle "Économisez X%"** lorsqu'une tranche comporte une remise.
- La durée d'essai, la frais de mise en service, et la politique de résiliation du plan (par exemple, "Résiliez à tout moment") sont affichés à côté de la liste des tranches, ainsi qu'une note indiquant qu'une méthode de paiement est ajoutée lors de la caisse.

### Dans le panier et lors de la caisse

Les articles d'abonnement dans le panier portent une **étiquette Abonnement**, la périodicité de facturation (par exemple, "Tous les mois") et une note d'essai si applicable, afin que le client sache clairement quels articles sont récurrents. Lors de la caisse, le client choisit un fournisseur de paiement comme d'habitude — c'est la méthode de paiement qui sera facturée lors des renouvellements futurs.

> **Limitation connue :** Le fait de stocker automatiquement la carte du client pour les renouvellements d'abonnement lors de la caisse est toujours en cours de mise en place pour certains fournisseurs de paiement. Jusqu'à ce qu'un fournisseur spécifique prenne en charge cela, les abonnements passés via celui-ci peuvent nécessiter un suivi supplémentaire (par exemple, contacter le client pour obtenir des coordonnées de paiement mises à jour avant un renouvellement) plutôt que d'être entièrement automatisés dès le premier jour. Consultez votre configuration de fournisseur de paiement si vous constatez que les renouvellements ne s'effectuent pas automatiquement pour un abonnement.

## Conseils

- Créez et testez d'abord le plan d'abonnement (tranches de prix, période d'essai, politique de résiliation), puis attachez-le aux produits - il est plus facile d'obtenir le bon plan dès le début que de le corriger sur plusieurs produits plus tard.
- Laissez **Autoriser l'achat unique** coché pour la plupart des produits. Réservez les produits exclusivement en abonnement pour les cas où un achat unique ne convient vraiment pas à votre entreprise.
- Si vous transformez un produit phare existant en option d'abonnement, désactivez d'abord **Passer à l'abonnement par défaut** afin de ne pas perturber les clients habitués à l'acheter une fois - activez-le plus tard une fois avoir vu comment les abonnés réagissent.
- Les produits numériques sont un excellent choix pour les abonnements (licences logicielles, abonnements à du contenu) car le renouvellement restaure automatiquement l'accès sans livraison impliquée.
- Si vous avez besoin d'un type de produit qui n'est pas éligible (un ensemble ou un article personnalisable, par exemple) pour être vendu de manière récurrente, réfléchissez à l'idée d'utiliser une version simplifiée ou numérique équivalente pour l'abonnement à la place.