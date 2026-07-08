---
title: Paniers abandonnés
---

Un panier abandonné est créé lorsqu'un client connecté ajoute des articles à son panier mais ne termine pas le processus de paiement dans les 24 heures. Spwig suit automatiquement ces paniers afin que vous puissiez comprendre les pertes de revenus, identifier les motifs pour lesquels les clients partent et prendre des mesures pour récupérer des ventes.

Accédez à **Clients > Paniers abandonnés** pour consulter toutes les abandonnements enregistrés.

## Ce que vous pouvez voir dans la liste des paniers abandonnés

La vue en liste affiche chaque panier abandonné avec les informations suivantes à un coup d'œil :

| Colonne | Description |
|---|---|
| **Client** | Le nom et l'adresse e-mail du client |
| **Abandonné le** | Date et heure à laquelle le panier a été signalé comme abandonné |
| **Valeur totale** | Valeur monétaire des articles dans le panier au moment de l'abandon |
| **Nombre total d'articles** | Nombre d'articles dans le panier |
| **Motif estimé** | Meilleure estimation de Spwig sur la raison de l'abandon |
| **Statut de récupération** | Indique si ce panier a été récupéré (transformé en commande terminée) |
| **Jours depuis l'abandon** | Indique depuis combien de temps le panier a été abandonné |

### Filtre des paniers abandonnés

Utilisez les filtres à droite pour affiner la liste :

- **Motif estimé** — filtrez par motif d'abandon (par exemple, affichez uniquement les paniers pour lesquels le motif estimé était un coût de livraison élevé)
- **Récupéré** — filtrez pour afficher uniquement les paniers récupérés ou non récupérés
- **Abandonné le** — filtrez par plage de dates pour vous concentrer sur les abandonnements récents ou une période de campagne spécifique

## Comprendre les motifs d'abandon

Spwig enregistre un motif estimé pour chaque abandon. Ces motifs sont basés sur des signaux captés lors du processus de paiement et ne sont pas garantis être exacts, mais ils constituent un point de départ utile pour diagnostiquer les motifs de désistement.

| Motif | Ce que cela peut indiquer |
|---|---|
| **Inconnu** | Aucun signal spécifique n'a été capté — la raison la plus courante |
| **Coût de livraison élevé** | Le client a peut-être été découragé par le coût de livraison affiché lors du paiement |
| **Total trop élevé** | Le montant total de la commande peut avoir été plus élevé que prévu |
| **Problèmes de paiement** | Le client a rencontré un problème lors du processus de paiement |
| **Échec du paiement** | Un paiement a été tenté mais a échoué |
| **Comparaison des prix** | Le client a probablement visité pour comparer les prix |
| **Enregistré pour plus tard** | Le client a intentionnellement enregistré des articles pour une visite ultérieure |

Si vous constatez une proportion importante de paniers avec la même raison — par exemple, un grand regroupement de motifs d'abandon « Coût de livraison élevé » — cela est un signal à investiguer dans vos paramètres de livraison ou dans l'affichage du processus de paiement.

## Afficher un panier abandonné individuel

Cliquez sur n'importe quelle ligne de la liste pour ouvrir la vue détaillée. Vous verrez :

- **Détails de l'abandon** — le client, la référence du panier, la date à laquelle il a été abandonné et le motif estimé
- **Résumé du panier** — le nombre d'articles et la valeur totale au moment de l'abandon
- **Suivi de la récupération** — indique si le panier a été récupéré, quand il a été récupéré et quelle commande il a générée

Le champ **Panier** fait directement référence au record du panier sous-jacent, donc vous pouvez voir exactement quels produits étaient dans le panier.

## Workflow de récupération

Spwig suit si chaque panier abandonné se convertit finalement en commande terminée. Lorsqu'un client revient et termine un achat à partir d'un panier abandonné, le record est automatiquement marqué comme **Récupéré** et la commande résultante est liée.

Le compteur **E-mails de récupération envoyés** indique combien d'e-mails de récupération automatisés ont été envoyés au client pour ce panier. Cela vous aide à comprendre si vos campagnes d'e-mail incitent les clients à revenir.

### Actions de récupération manuelle

La vue des paniers abandonnés est en lecture seule — c'est un enregistrement de ce qui s'est produit, pas un outil pour modifier le contenu du panier. Pour agir sur les paniers abandonnés :

1.

Notez l'adresse e-mail du client à partir du record du panier abandonné
2.

Utilisez votre système de messagerie ou vos outils de marketing pour envoyer un message personnalisé
3.

Considérez l'ajout d'un code promo pour donner au client un incitant à terminer l'achat
4.

Conservez tous les formats de markdown, les chemins d'image, les blocs de code et les termes techniques.

Suivez le statut **Recovered** au cours des jours suivants pour voir si l'initiative a fonctionné

## Analyse des tendances d'abandon de panier

Examinez régulièrement la liste des paniers abandonnés comme un indicateur de santé de votre processus de paiement :

- Une augmentation soudaine des abandons peut indiquer un problème technique lors du paiement
- Des valeurs de panier élevées et persistantes dans les paniers non récupérés représentent votre segment de récupération le plus prometteur
- Comparez le ratio de paniers récupérés par rapport aux paniers non récupérés au fil du temps pour mesurer l'efficacité de vos e-mails de récupération

La section **Customer Analytics** du profil de chaque client affiche également leur taux personnel d'abandon de panier, ce qui vous permet d'identifier les clients qui ajoutent fréquemment des articles au panier mais qui achètent rarement.

## Conseils

- Triez par **Total Value** (du plus élevé au plus bas) pour identifier les paniers les plus onéreux à prioriser pour une approche personnalisée
- Utilisez le filtre **Abandoned At** pour consulter les abandons d'une campagne ou d'une période promotionnelle spécifique — une augmentation pendant une vente flash peut signifier que votre promotion a attiré des visiteurs plutôt que des acheteurs
- Associez les données des paniers abandonnés aux campagnes de coupons : envoyez un code de réduction limité dans le temps aux clients ayant des paniers non récupérés de haute valeur pour créer de l'urgence
- Un panier abandonné depuis plus de 7 jours a peu de chances de se récupérer seul — si les e-mails de récupération sont activés, ce sont ces paniers qui nécessitent le plus d'attention
- Les clients invités ne figurent pas dans les paniers abandonnés — ce suivi s'applique uniquement aux clients ayant un compte enregistré