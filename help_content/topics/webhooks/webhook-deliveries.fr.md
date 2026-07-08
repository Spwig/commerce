---
title: Journal de livraison des webhooks
---

Chaque fois que votre magasin tente d'envoyer un webhook, une entrée de journal de livraison est créée. Ces journaux vous permettent de voir exactement ce qui a été envoyé, si cela a réussi, et ce qui s'est produit lors des tentatives de réessai. Ce guide explique comment consulter les journaux de livraison et dépanner les problèmes lorsque les livraisons échouent.

## Consultation des journaux de livraison

Accédez à **Intégrations > Livraisons de webhooks** pour voir l'historique complet de toutes les tentatives de livraison de webhook sur tous vos points de terminaison.

![Journal de livraison des webhooks](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

La liste affiche le nom du point de terminaison, le type d'événement, le statut, le code de réponse HTTP, le temps de réponse et le nombre d'essais effectués pour chaque livraison.

Les journaux de livraison sont en lecture seule — ils sont créés automatiquement lors de la survenue d'événements et ne peuvent pas être modifiés.

## Statuts de livraison

Chaque livraison a l'un des statuts suivants :

| Statut | Ce que cela signifie |
|--------|---------------------|
| **En attente** | La livraison est en file d'attente et n'a pas encore été tentée |
| **Succès** | Le serveur récepteur a répondu avec un code d'état HTTP 2xx — livraison confirmée |
| **Échec** | Toutes les tentatives de livraison ont été épuisées — la livraison ne sera plus réessayée |
| **Réessai** | La dernière tentative a échoué, mais le système tentera à nouveau à l'heure de réessai planifiée |
| **Bloqué en sandbox** | La livraison a été bloquée car l'URL du point de terminaison n'est pas accessible dans l'environnement actuel |

Une livraison est considérée comme réussie lorsque le serveur récepteur renvoie tout code de réponse HTTP 2xx (200, 201, 202, etc.). Toute autre réponse — y compris les redirections 3xx ou les erreurs 4xx/5xx — est considérée comme un échec.

## Filtre des livraisons

Utilisez le panneau de filtre à droite pour affiner la liste :

- **Statut** — Afficher uniquement les livraisons échouées, en cours de réessai ou réussies
- **Type d'événement** — Voir toutes les livraisons pour un événement spécifique (par exemple, toutes les livraisons `order.created`)
- **Point de terminaison** — Afficher les livraisons pour un point de terminaison spécifique
- **Créé le** — Filtre par plage de dates

Utilisez la barre de recherche pour rechercher par type d'événement ou par nom de point de terminaison, ou pour trouver une livraison spécifique par son ID.

## Consultation des détails d'une livraison

Cliquez sur n'importe quelle livraison pour voir ses détails complets. Les enregistrements de livraison sont en lecture seule.

### Résumé

- **ID** — L'identifiant unique de cette tentative de livraison
- **Point de terminaison** — Le webhook vers lequel cette livraison a été envoyée (lien vers l'enregistrement du point de terminaison)
- **Type d'événement** — L'événement qui a déclenché cette livraison (par exemple, `order.paid`)
- **Statut** — Statut actuel de la livraison

### Charge utile

La section **Charge utile** affiche les données JSON exactes qui ont été envoyées à votre point de terminaison. Cela inclut le type d'événement, une horodatage et les données d'événement complètes. Utilisez cela pour vérifier que votre serveur récepteur reçoit la structure de données correcte.

### Réponse

La section **Réponse** affiche ce que votre serveur a répondu :

- **Code de statut de réponse** — Le code d'état HTTP renvoyé par votre serveur. Coloré : vert pour 2xx (succès), jaune pour 4xx (erreur client), rouge pour 5xx (erreur serveur).
- **Temps de réponse** — Le temps que votre serveur a pris pour répondre en millisecondes. Coloré : vert en dessous de 500 ms, jaune jusqu'à 2 secondes, rouge au-delà de 2 secondes.
- **Corps de la réponse** — Le corps de la réponse de votre serveur (tronqué à 1 000 caractères). Cela peut aider à identifier pourquoi votre serveur a rejeté le webhook.
- **En-têtes de réponse** — Les en-têtes renvoyés par votre serveur.

### Détails de l'erreur

Si la livraison a échoué, la section **Détails de l'erreur** affiche le message d'erreur — par exemple, `Connection refused`, `Timeout after 30s`, ou l'erreur HTTP de votre serveur.

### Informations sur le réessai

- **Nombre d'essais** — Le nombre de tentatives de livraison effectuées (y compris la première tentative)
- **Prochain réessai à** — Lors de laquelle le prochain réessai sera tenté (affiché uniquement pour les livraisons en statut **Réessai**)

Les réessais suivent un plan de réessai avec un écart exponentiel — l'intervalle entre les réessais augmente à chaque tentative pour éviter de surcharger un serveur temporairement indisponible. Avec un maximum de 5 réessais (par défaut), le plan de réessai s'étale sur plusieurs heures.

## Réessayer manuellement les livraisons échouées

Si vous souhaitez réessayer immédiatement une livraison sans attendre le planificateur automatique :

1. Cochez les cases à côté des livraisons que vous souhaitez réessayer
2. Dans le menu déroulant **Action**, choisissez **Réessayer les livraisons sélectionnées**
3. Cliquez sur **Go**

Seules les livraisons qui ne sont pas déjà en statut **Success** seront mises en file d'attente pour être réessayées. Les livraisons réussies sont ignorées.

Cela est utile lorsque vous avez corrigé un problème avec votre serveur de réception et que vous souhaitez retraiter les événements échoués sans attendre.

## Diagnostiquer les échecs courants

### Codes de réponse HTTP 4xx

Une réponse 4xx de votre serveur indique généralement qu'il y a un problème avec la demande — l'authentification a échoué, l'URL de l'endpoint a changé, ou votre serveur a refusé le format de la charge utile. Vérifiez :

- L'URL de l'endpoint est-elle correcte ?
- Votre serveur vérifie-t-il correctement la signature HMAC ? Une incohérence provoque souvent des retours 401 ou 403 sur de nombreux serveurs.
- La structure de la charge utile a-t-elle changé ? Comparez la charge utile dans le journal de livraison avec ce que votre serveur attend.

### Codes de réponse HTTP 5xx

Une réponse 5xx signifie que votre serveur a rencontré une erreur interne lors du traitement du webhook. Vérifiez les journaux d'erreurs de votre propre serveur pour diagnostiquer le problème.

### Connexion refusée / Timeout

Ces erreurs signifient que Spwig n'a pas pu atteindre votre serveur du tout :

- Le serveur est-il en cours d'exécution et publiquement accessible ?
- L'URL est-elle correcte (y compris le protocole correct — http ou https) ?
- Un pare-feu bloque-t-il les requêtes entrantes ?
- Le temps de réponse du serveur dépasse-t-il le délai de temporisation configuré ? Si oui, augmentez le paramètre **Timeout** sur l'endpoint ou optimisez votre gestionnaire de webhook pour répondre rapidement (idéalement en moins de 5 secondes).

### Sandbox Bloqué

Les livraisons sont bloquées vers les URLs localhost ou les adresses réseau internes. Les endpoints de webhook doivent être publiquement accessibles. Utilisez un outil comme ngrok pendant le développement pour rendre publiquement accessible un serveur local.

## Conseils

- Traitez rapidement les livraisons **Failed** — les données de l'événement sont toujours dans la charge utile, et vous pouvez les réessayer manuellement une fois que le problème est résolu.
- Si vous voyez de nombreuses livraisons **Retrying** pour un seul endpoint, ouvrez le dossier de l'endpoint et vérifiez la section **Health** — l'endpoint risque d'être désactivé automatiquement.
- Le temps de réponse compte : configurez votre gestionnaire de webhook pour répondre rapidement (en quelques secondes) et traitez la charge utile de manière asynchrone en arrière-plan. Un gestionnaire lent provoque des échecs de temporisation même si votre logique est correcte.
- Utilisez le filtre **Type d'événement** pour vérifier l'historique des livraisons pour un type d'événement spécifique lors de l'enquête sur le fait que votre intégration reçoit les bons événements.
- Les journaux de livraison s'accumulent au fil du temps. Utilisez le filtre de date pour vous concentrer sur les livraisons récentes et éviter de naviguer dans l'historique ancien.