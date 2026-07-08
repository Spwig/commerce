---
title: Aperçu des webhooks
---

Les webhooks permettent à votre magasin d'informer automatiquement des systèmes externes — tels que des outils de gestion des stocks, des ERP, des services de livraison ou des applications personnalisées — dès qu'un événement se produit dans votre magasin. Au lieu de ce que ces systèmes demandent répétitivement « quelque chose a-t-il changé ? », votre magasin envoie une notification dès qu'un événement se produit.

## Ce que font les webhooks

Lorsqu'un événement se produit dans votre magasin (une commande est passée, un paiement est reçu, un produit est en rupture de stock), Spwig envoie une demande HTTP POST contenant les données de l'événement à l'URL que vous configurez. Le système récepteur peut alors agir immédiatement sur ces données — par exemple, mettre à jour les stocks, déclencher un étiquette de livraison ou envoyer une notification personnalisée.

Les usages courants des webhooks incluent :

- Synchroniser en temps réel les commandes avec un partenaire de livraison
- Mettre à jour les stocks dans un ERP lors d'une modification de stock
- Déclencher des notifications SMS ou push en cas de changement d'état de commande
- Enregistrer des événements dans un entrepôt de données pour la reporting
- Se connecter à des outils d'automatisation tels que Zapier ou Make

## Afficher et gérer les points de terminaison

Accédez à **Intégrations > Webhooks** pour voir tous vos points de terminaison de webhook configurés.

![Liste des points de terminaison de webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

La liste affiche le nom de chaque point de terminaison, son URL, son statut actif, le nombre d'événements auxquels il s'abonne, son statut de santé et la date de la dernière livraison reçue.

### Indicateurs de santé

La colonne **Santé** indique à vue d'œil à quel point chaque point de terminaison fonctionne bien :

- **Santé** — Toutes les dernières livraisons ont réussi
- **Dégradé** — Certaines échecs récents, mais le point de terminaison est toujours actif
- **Non fonctionnel / Désactivé** — Le point de terminaison a été désactivé automatiquement après trop de défaillances consécutives (10 par défaut). Vous devez le réactiver manuellement une fois que le problème sous-jacent est résolu.

## Créer un point de terminaison de webhook

Cliquez sur **+ Ajouter un point de terminaison de webhook** pour ouvrir l'assistant de configuration. L'assistant vous guide à travers quatre étapes.

### Étape 1 : Informations de base

- **Nom** — Un étiquette amicale pour identifier ce point de terminaison (par exemple, `Service de livraison des commandes` ou `Synchronisation des stocks`).
- **URL** — L'URL complète du serveur qui recevra les demandes POST de webhook. Cela doit être publiquement accessible (pas une URL localhost).
- **Description** — Notes optionnelles sur l'utilisation de ce point de terminaison.
- **Actif** — Indique si ce point de terminaison doit recevoir des livraisons. Désactivez-le pour suspendre temporairement sans supprimer le point de terminaison.

### Étape 2 : Abonnements aux événements

Choisissez quels événements doivent déclencher une livraison vers ce point de terminaison. Les événements sont regroupés par catégorie :

### Événements de commande

| Événement | Lorsqu'il se déclenche |
|-----------|----------------------|
| `order.created` | Une nouvelle commande est passée |
| `order.paid` | Le paiement d'une commande est confirmé |
| `order.cancelled` | Une commande est annulée |
| `order.fulfilled` | Tous les articles d'une commande sont expédiés |
| `order.partially_fulfilled` | Certains articles d'une commande sont expédiés |
| `order.status_changed` | L'état de la commande change |
| `order.note_added` | Une note est ajoutée à une commande |

### Événements de paiement

| Événement | Lorsqu'il se déclenche |
|-----------|----------------------|
| `payment.received` | Un paiement est reçu |
| `payment.failed` | Un tentative de paiement échoue |
| `payment.pending` | Un paiement attend la confirmation |

### Événements de livraison

| Événement | Lorsqu'il se déclenche |
|-----------|----------------------|
| `shipment.created` | Une livraison est créée |
| `shipment.shipped` | Une livraison est expédiée |
| `shipment.delivered` | Une livraison est livrée |
| `shipment.returned` | Une livraison est retournée |
| `shipment.tracking_updated` | Les informations de suivi sont mises à jour |

### Événements de stock

| Événement | Lorsqu'il se déclenche |
|-----------|----------------------|
| `inventory.low_stock` | Le stock tombe en dessous du seuil |
| `inventory.out_of_stock` | Un produit est en rupture de stock |
| `inventory.restocked` | Un produit est réapprovisionné |
| `inventory.adjusted` | Le stock est ajusté manuellement |

### Événements de produit

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

### Événements client


`customer.created`, `customer.updated`, `customer.deleted`

#### Événements de souscription

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Autres événements

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Pour recevoir tous les événements, abonnez-vous à `*` (joker). Cela est utile pour les points de terminaison de journalisation généralistes, mais génère plus de trafic — abonnez-vous uniquement aux événements dont vous avez vraiment besoin pour les intégrations en production.

### Étape 3 : Configuration

- **Max Retries** — Combien de fois Spwig doit réessayer une livraison échouée avant d'abandonner (par défaut : 5). Chaque réessai utilise un espacement avec un recul exponentiel.
- **Timeout (Seconds)** — Combien de temps attendre que le serveur récepteur réponde avant de marquer la livraison comme échouée (par défaut : 30 secondes). Augmentez uniquement cela si votre serveur est connu pour être lent.

### Étape 4 : Sécurité

Chaque point de terminaison de webhook obtient un **secret de signature** généré automatiquement — une clé aléatoire de 64 caractères. Spwig utilise ce secret pour signer chaque charge utile de webhook avec une signature HMAC-SHA256.

La signature est incluse dans l'en-tête de requête `X-Webhook-Signature`. Votre serveur récepteur doit vérifier cette signature pour confirmer que la requête provient effectivement de votre magasin et n'a pas été altérée.

Le secret est affiché masqué dans l'administration. Pour voir ou renouveler le secret, utilisez l'API Spwig. Renouvelez immédiatement votre secret si vous soupçonnez qu'il a été compromis.

## Activer et désactiver les points de terminaison

Pour activer ou désactiver rapidement un ou plusieurs points de terminaison sans ouvrir chacun :

1. Cochez les cases à côté des points de terminaison que vous souhaitez modifier
2. Utilisez le menu déroulant **Action** pour choisir **Activer les points de terminaison sélectionnés** ou **Désactiver les points de terminaison sélectionnés**
3. Cliquez sur **Go**

Pour réactiver un point de terminaison qui a été désactivé automatiquement en raison d'échecs, sélectionnez-le et utilisez l'action **Réinitialiser le compteur d'échecs**, puis réactivez-le. Corrigez d'abord ce qui a causé les échecs, sinon il sera à nouveau désactivé rapidement.

## Conseils

- Abonnez-vous uniquement aux événements dont vous avez vraiment besoin — les événements inutiles créent du bruit dans vos journaux et augmentent la charge de livraison.
- Vérifiez toujours la signature du webhook sur votre serveur récepteur avant de traiter la charge utile. Cela vous protège contre les requêtes falsifiées.
- Utilisez le champ **Description** pour enregistrer quel système ou intégration ce point de terminaison connecte. Cela aide lors de la résolution de problèmes plusieurs mois plus tard.
- Fixez un **Timeout** légèrement supérieur au temps de réponse typique de votre serveur. Un timeout de 10 à 15 secondes est suffisant pour la plupart des intégrations.
- Si un point de terminaison devient **Mauvais**, vérifiez d'abord les journaux de livraison (voir **Livraisons de webhook**) pour comprendre le motif d'échec avant de le réactiver.
- Pour le test, pointez les webhooks vers un outil comme [webhook.site](https://webhook.site) pour inspecter les charges utiles brutes sans avoir besoin d'un serveur en direct.