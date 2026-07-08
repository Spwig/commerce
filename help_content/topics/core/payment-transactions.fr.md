---
title: Transactions de paiement
---

Les transactions de paiement constituent le registre complet de chaque événement de paiement traité par votre magasin — paiements, remboursements, autorisations et plus encore. Cette section inclut également les journaux de webhooks provenant de vos fournisseurs de paiement et les intentions de paiement créées lors du passage à la caisse.

## Transactions de paiement

Accédez à **Paiements > Transactions de paiement** pour voir toutes les transactions traitées par votre magasin.

### Types de transactions

| Type | Ce que cela signifie |
|------|--------------|
| **Paiement** | Un paiement immédiat — les fonds sont collectés au moment de la transaction |
| **Autorisation** | Les fonds sont bloqués sur la carte du client mais ne sont pas encore collectés |
| **Capture** | Collecte les fonds d'une autorisation précédente |
| **Annulation** | Annule une autorisation avant sa capture |
| **Remboursement** | Restitue le paiement au client |

### États des transactions

| État | Ce que cela signifie |
|--------|--------------|
| **En attente** | La transaction a été initiée mais n'a pas encore été traitée |
| **En cours de traitement** | En cours de traitement par le fournisseur de paiement |
| **Autorisé** | Les fonds sont bloqués — en attente de capture |
| **Complété** | Le paiement a été réussi |
| **Échoué** | Le paiement a été refusé ou une erreur s'est produite |
| **Annulé** | L'autorisation a été annulée avant la capture |
| **Remboursé** | Un remboursement complet a été émis |
| **Partiellement remboursé** | Une partie du paiement a été restituée |

### Ce que vous pouvez voir dans un enregistrement de transaction

Chaque transaction affiche :
- **ID de transaction** — Référence interne de Spwig
- **ID de transaction du fournisseur** — La référence de votre fournisseur de paiement (par exemple, l'ID de paiement Stripe)
- **Montant** — Le montant de la transaction et la devise
- **État** et **Type**
- **Email du client** et **Nom du client**
- **Méthode de paiement** — Type (carte de crédit, virement bancaire, etc.) et derniers 4 chiffres
- **Commande** — La commande à laquelle appartient cette transaction
- **Compte du fournisseur** — Le fournisseur de paiement qui l'a traitée
- **Réponse du fournisseur** — La réponse technique brute du fournisseur de paiement
- **Message d'erreur** — Si la transaction a échoué, la raison donnée par le fournisseur
- Horodatages pour la création, la dernière mise à jour et la complétion

### Filtre des transactions

Utilisez les filtres d'administration pour affiner les transactions selon :
- État (par exemple, afficher uniquement les transactions échouées)
- Type (par exemple, afficher uniquement les remboursements)
- Compte du fournisseur
- Plage de dates

Cela est utile pour la conciliation à la fin de la journée ou pour enquêter sur l'historique des paiements d'un client spécifique.

### Quand une transaction peut-elle être remboursée ?

Une transaction peut être remboursée lorsque :
- Son état est **Complété**
- Son type est **Paiement** ou **Capture**

Pour émettre un remboursement, utilisez l'action **Remboursement** depuis la page des détails de la commande. Les remboursements traités via la commande créent un nouvel enregistrement de transaction du type **Remboursement**.

### Flux d'autorisation et de capture

Certaines méthodes de paiement (ainsi que certains fournisseurs de paiement) prennent en charge une autorisation et une capture séparées. Cela est utile si vous souhaitez vérifier le paiement avant l'expédition :

1. **Autorisation** — Les fonds sont bloqués sur la carte du client (état : `Autorisé`)
2. **Capture** — Déclenchée lors de l'expédition de la commande ou de sa livraison
3. Si la capture n'est pas effectuée dans la fenêtre d'autorisation, le blocage **expire** automatiquement

Le champ **Expire à** sur la transaction indique à quel moment une autorisation va expirer.

## Webhooks de paiement

Les fournisseurs de paiement envoient des événements webhook pour informer votre magasin des changements d'état des paiements — par exemple, lorsqu'un paiement réussit, échoue ou qu'une contestation est soulevée. Spwig enregistre tous les webhooks entrants.

Accédez à **Paiements > Webhooks de paiement** pour consulter le journal.

### Ce que les enregistrements de webhook montrent

| Champ | Description |
|-------|-------------|
| **Fournisseur** | Le fournisseur de paiement qui a envoyé le webhook |
| **ID de l'événement** | L'identifiant unique de l'événement du fournisseur |
| **Type d'événement** | Le type d'événement (par exemple, `payment_intent.succeeded`, `charge.refunded`) |
| **Traité** | Indique si Spwig a agi sur ce webhook |
| **Signature vérifiée** | Indique si la signature de sécurité du webhook était valide |
| **Charge utile** | Les données complètes envoyées par le fournisseur |
| **Résultat du traitement** | Ce que Spwig a fait en réponse |
| **Erreur de traitement** | Toute erreur survenue lors du traitement |
| **Reçu à** | Lorsque le webhook est arrivé |

### Utilisation des journaux de webhooks pour le dépannage

Si un paiement semble bloqué ou que le statut de la commande n'a pas été mis à jour après le paiement :

1. Accédez à **Paiements > Webhooks de paiement**
2. Filtrez par le fournisseur et cherchez des événements récents
3. Vérifiez la colonne **Traité** — un webhook non traité peut indiquer un problème de livraison
4. Vérifiez **Signature vérifiée** — une signature échouée peut signifier que votre secret de webhook est mal configuré
5. Examinez **Erreur de traitement** pour toute message d'erreur

Les événements en double sont gérés automatiquement — la combinaison de `ID de l'événement` et du fournisseur est unique, donc le même webhook ne peut pas être traité deux fois.

## Intents de paiement

Un intent de paiement suit le cycle de vie d'un paiement de checkout depuis le moment où un client commence le processus de paiement jusqu'au résultat final. Les intents de paiement sont créés automatiquement lorsque le client atteint l'étape de paiement au checkout.

Accédez à **Paiements > Intents de paiement** pour consulter la liste.

### États des intents de paiement

| État | Signification |
|--------|---------|
| **Créé** | L'intent a été créé, en attente de la méthode de paiement |
| **Requiert une méthode de paiement** | En attente que le client entre ses détails de carte |
| **Requiert une confirmation** | Les détails de paiement ont été entrés, en attente de confirmation |
| **Requiert une action** | Le client doit accomplir une action (par exemple, une authentification 3D Secure) |
| **En cours de traitement** | Le paiement est en cours de traitement |
| **Réussi** | Le paiement a été terminé avec succès |
| **Annulé** | Le paiement a été abandonné ou annulé |
| **Échoué** | L'essai de paiement a échoué |

### Flux d'intent de paiement vers la commande

1. Le client atteint l'étape de paiement du checkout → Spwig crée un **Intent de paiement** et une **Commande** brouillon (non payée)
2. Le client entre les détails de paiement et confirme
3. Le fournisseur de paiement traite le paiement
4. En cas de succès, la commande est mise à jour en **Payée** et l'Intent de paiement passe à **Réussi**
5. Un **Enregistrement de transaction de paiement** est créé avec les détails de la charge finale

L'intent de paiement relie la session de checkout, le compte du fournisseur et la commande — vous donnant une image complète du parcours de checkout du client.

### Utilisation des intents de paiement pour le support

Si un client signale qu'il a payé mais que sa commande apparaît comme non payée :

1. Trouvez la commande du client dans **Commandes**
2. Accédez à **Paiements > Intents de paiement** et recherchez les intents liés à cette commande
3. Vérifiez le statut de l'intent — si c'est **Réussi**, vérifiez la transaction liée
4. Si l'intent est **Requiert une action**, le client n'a peut-être pas terminé l'authentification 3D Secure
5. Si l'intent est **Échoué**, les détails de l'erreur expliquent pourquoi le paiement a été refusé

## Conseils

- Vérifiez quotidiennement les transactions échouées — des modèles d'échecs (par exemple, une méthode de paiement ou un pays spécifique) peuvent indiquer un problème de configuration ou une tentative de fraude.
- Les journaux de webhooks sont inestimables lors de l'enquête sur les écarts de paiement.

Si une commande a été payée mais non confirmée, le journal de webhook vous indiquera généralement ce qui s'est mal passé.
- Les blocs d'autorisation expirent automatiquement — si vous utilisez autorisez-puis-capturer, assurez-vous que votre processus de livraison capture les fonds avant la fin de la fenêtre d'expiration (généralement 7 jours pour la plupart des fournisseurs).
- Le champ **Réponse du fournisseur** sur les transactions contient les données brutes du fournisseur de paiement.

Partagez cela avec l'équipe de support de votre fournisseur si vous avez besoin d'aide pour résoudre un problème de transaction spécifique.
- Les échecs de vérification de la signature sur les webhooks doivent être investigués immédiatement — ils peuvent indiquer un secret de webhook mal configuré ou un tentative d'envoyer des événements webhook frauduleux à votre magasin.