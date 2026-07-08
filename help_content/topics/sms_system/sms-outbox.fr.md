---
title: Boîte de sortie SMS
---

La boîte de sortie SMS est un registre complet de chaque message texte que votre magasin a tenté d'envoyer. Utilisez-la pour confirmer que les notifications ont atteint les clients, enquêter sur les échecs d'envoi, et comprendre votre activité globale de messagerie.

Accédez à **Système SMS > Boîte de sortie SMS** pour consulter le journal des messages.

![Liste de la boîte de sortie SMS avec des badges d'état](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Lire la boîte de sortie

Chaque ligne de la boîte de sortie représente un tentative de message et affiche :

- **Téléphone** — le numéro de téléphone du destinataire
- **Type de message** — SMS ou WhatsApp
- **Statut** — le statut actuel de livraison (voir ci-dessous)
- **Créé le** — quand le message a été créé
- **Envoyé le** — quand le message a été envoyé au fournisseur

La barre de résumé en haut affiche des compteurs agrégés pour les statuts les plus importants à vue d'œil.

## États des messages

| Statut | Signification |
|--------|---------|
| En attente | Le message attend d'être pris en charge par la file d'attente d'envoi |
| En file d'attente | Le message a été mis en file d'attente et sera envoyé bientôt |
| Envoyé | Le fournisseur a accepté le message pour livraison |
| Livré | Le fournisseur a confirmé que le message a atteint l'appareil du destinataire |
| Échoué | Le fournisseur a refusé ou n'a pas pu livrer le message |
| Ignoré | L'envoi a été ignoré intentionnellement (voir les raisons d'ignorance ci-dessous) |
| Enregistré en sandbox | Le message a été enregistré uniquement (le magasin est en mode test/sandbox) |

> **Envoyé vs Livré :** Un statut **Envoyé** signifie que le message a quitté votre magasin et a été accepté par le fournisseur. Un statut **Livré** signifie que le fournisseur a reçu un reçu de livraison du transporteur. Tous les fournisseurs ne prennent pas en charge les reçus de livraison — si votre fournisseur ne le fait pas, les messages peuvent afficher **Envoyé** mais ne progresseront jamais vers **Livré**, ce qui est normal.

## Voir les détails du message

Cliquez sur n'importe quelle ligne de la boîte de sortie pour voir les détails complets de ce message :

- Le texte complet du **Message** envoyé
- L'**ID du message du fournisseur** — le numéro de référence du fournisseur SMS (utile lors de la communication avec le support du fournisseur)
- Le **Message d'erreur** (pour les messages échoués) — l'erreur exacte retournée par le fournisseur
- Le **Compteur de réessais** — le nombre de fois que Spwig a tenté d'envoyer le message
- Toutes les timestamps (créé, en file d'attente, envoyé, livré)

## Filtre de la boîte de sortie

Utilisez les filtres à droite pour affiner la liste :

- **Statut** — afficher uniquement les messages avec un statut particulier
- **Type de message** — afficher uniquement les SMS ou uniquement les messages WhatsApp
- **Date** — filtrer par la journée où le message a été créé

La barre de recherche en haut vous permet de rechercher par numéro de téléphone, contenu du message ou ID du message du fournisseur.

## Comprendre les raisons d'ignorance

Les messages ignorés n'ont pas été envoyés car Spwig a déterminé que l'envoi était inapproprié ou inutile. Raisons d'ignorance courantes :

| Raison d'ignorance | Ce que cela signifie |
|-------------|---------------|
| `user_preference_disabled` | Le client a désactivé les notifications SMS dans ses paramètres de compte |
| `unsubscribed` | Le client s'est désinscrit des messages SMS |
| `no_provider` | Aucun compte par défaut actif de fournisseur SMS n'est configuré |
| `template_inactive` | Le modèle pour ce type de notification est inactif |

Un message ignoré n'est pas un échec — cela signifie que le système a fonctionné comme prévu. Cependant, un nombre élevé de sauts `no_provider` indique que vous devez configurer et activer un compte de fournisseur SMS.

## Dépannage des livraisons échouées

Si les messages affichent un statut **Échoué**, suivez ces étapes :

1. Cliquez sur le message échoué pour voir son **Message d'erreur**
2. Causes courantes d'erreur :

   | Erreur | Cause probable |
   |-------|-------------|
   | Numéro de téléphone invalide | Le numéro de téléphone du client est manquant ou n'est pas au format E.164 |
   | Authentification échouée | Vos identifiants du fournisseur sont invalides ou expirés — mettez-les à jour dans **SMS Provider Accounts** |
   | Compte suspendu | Votre compte du fournisseur a été suspendu — connectez-vous au tableau de bord du fournisseur |
   | Solde insuffisant | Le solde de votre compte du fournisseur est trop bas — rechargez-le |
   | Rejet par le fournisseur | Le fournisseur de destination a bloqué le message (souvent en raison du filtrage du contenu) |

3. Après avoir résolu le problème sous-jacent, les messages futurs seront envoyés normalement — le dossier de sortie est un journal en lecture seule et les messages individuels ne peuvent pas être envoyés manuellement

## Le dossier de sortie est en lecture seule

Le dossier de sortie SMS est un enregistrement uniquement. Vous ne pouvez pas ajouter de messages au dossier de sortie manuellement, et vous ne pouvez pas renvoyer individuellement des messages depuis ici. Les messages sont envoyés automatiquement par Spwig lorsqu'événements pertinents se produisent (par exemple, un ordre est passé).

## Conseils

- Vérifiez le dossier de sortie après une période chargée pour confirmer que tous les messages de confirmation des commandes ont été envoyés avec succès
- Si un client dit qu'il n'a pas reçu un SMS, recherchez dans le dossier de sortie par son numéro de téléphone pour voir si le message a été envoyé, a échoué ou a été ignoré
- Une augmentation soudaine de messages **Échoués** indique généralement un problème avec vos identifiants ou le solde de votre compte fournisseur — vérifiez-les immédiatement
- Si vous voyez de nombreux messages **Ignorés** avec la raison `no_provider`, allez dans **SMS System > SMS Provider Accounts** et assurez-vous qu'un compte par défaut actif est configuré
- La hiérarchie de dates en haut de la liste vous permet de naviguer rapidement par jour, mois ou année pour consulter les messages historiques