---
title: Boîte de sortie des e-mails
---

La boîte de sortie des e-mails est un journal complet de chaque e-mail que votre magasin a envoyé ou tenté d'envoyer — confirmations de commande, mises à jour de livraison, rapports d'administration et tous autres messages transactionnels. Utilisez-la pour confirmer les livraisons, enquêter sur les échecs et gérer la file d'attente des e-mails.

Accédez à **Système de messagerie > Boîte de sortie des e-mails** pour consulter le journal des e-mails.

![Liste de la boîte de sortie des e-mails avec des badges d'état](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Lire la boîte de sortie

La barre de résumé en haut affiche les comptes pour chaque catégorie d'état. La liste ci-dessous affiche les e-mails individuels avec :

- **Sujet** — le sujet de l'e-mail
- **À** — l'adresse e-mail du destinataire
- **De** — l'adresse utilisée pour l'expéditeur
- **Statut** — l'état actuel de livraison
- **Enfilement à** — moment où l'e-mail a été ajouté à la file d'attente
- **Envoyé à** — moment où l'e-mail a été envoyé au fournisseur
- **Nombre de tentatives** — combien de fois l'envoi a été tenté

## États des e-mails

| État | Signification |
|------|-------------|
| Enfilement | L'e-mail est en attente dans la file d'attente pour être envoyé |
| En cours d'envoi | L'e-mail est actuellement envoyé au fournisseur |
| Envoyé | Le fournisseur a accepté l'e-mail |
| En attente | L'e-mail est suspendu et ne sera pas envoyé jusqu'à ce qu'il soit libéré |
| Enregistré | L'e-mail a été enregistré mais n'a pas été envoyé (mode test ou configuration uniquement enregistrée) |
| Échoué | Le fournisseur a refusé ou n'a pas pu livrer l'e-mail |
| Rejeté | L'e-mail a été envoyé mais a été renvoyé par le serveur de messagerie du destinataire |
| Ignoré | L'envoi a été ignoré pour une raison liée au système |

## Voir les détails des e-mails

Cliquez sur n'importe quel e-mail dans la liste pour voir les détails complets :

- Le **corps HTML** et le **corps texte** complets de l'e-mail
- **ID de message du fournisseur** — la référence de votre fournisseur d'e-mails (utilisez-la lors de la communication avec le support du fournisseur)
- **Message d'erreur** — le message d'erreur exact pour les e-mails échoués ou rejetés
- **Nombre de tentatives** et **Nombre maximum de tentatives** — combien de fois l'envoi a été tenté
- Toutes les timestamps : créée, enfilement, envoyée et échouée

## Filtre de la boîte de sortie

Utilisez les filtres à droite pour affiner votre vue :

- **Statut** — afficher les e-mails d'un statut de livraison spécifique
- **Date** — filtrer par la date à laquelle les e-mails ont été créés ou envoyés
- **Type de modèle** — afficher uniquement les e-mails d'un type spécifique de notification (par exemple, uniquement les confirmations de commande)

La barre de recherche en haut recherche par sujet, adresse du destinataire, adresse de l'expéditeur ou ID de message du fournisseur.

## Libérer les e-mails en attente

Les e-mails en **attente** sont suspendus — ils ne seront pas envoyés jusqu'à ce que vous les libériez. Un e-mail peut être en attente si votre magasin était en mode maintenance lorsqu'il a été généré, ou si une action d'administrateur l'a mis en attente.

Pour libérer les e-mails en attente :
1. Sélectionnez les e-mails que vous souhaitez libérer (cochez les cases à gauche)
2. Choisissez **Libérer les e-mails en attente pour l'envoi** dans le menu déroulant **Actions**
3. Cliquez sur **Aller**

Les e-mails libérés passent à l'état **Enfilement** et sont envoyés lors du prochain cycle de traitement de la file d'attente.

## E-mails planifiés

Certains e-mails sont planifiés pour être envoyés à un moment futur — par exemple, les rapports hebdomadaires sont planifiés pour être envoyés à une date et à une heure spécifiques. Accédez à **Système de messagerie > E-mails planifiés** pour consulter les envois planifiés à venir.

La liste des e-mails planifiés affiche :

- **Type de modèle** — le type d'e-mail planifié
- **Adresse e-mail du destinataire** — l'adresse à laquelle il sera envoyé
- **Planifié pour** — la date et l'heure à laquelle l'e-mail doit être envoyé
- **Statut** — En attente (non encore envoyé), Envoyé ou Échoué

Les e-mails planifiés sont traités automatiquement lors de l'heure planifiée — aucune action manuelle n'est nécessaire.

## Dépannage des livraisons échouées

Si des e-mails affichent un statut **Échoué**, cliquez pour voir le message d'erreur et suivez ces étapes :

### Causes courantes et solutions

| Symptôme | Cause probable | À faire |
|---------|-------------|------------|
| "Authentication failed" | Les identifiants du fournisseur de courriel sont invalides | Mettez à jour les identifiants dans **Email System > Email Accounts** |
| "Connection refused" / "Timeout" | Votre serveur de courriel est inatteignable | Vérifiez la page d'état du fournisseur de courriel ; testez la connexion dans **Email Accounts** |
| "Invalid recipient" | L'adresse courriel du client est mal formée | Vérifiez le compte du client et corrigez leur courriel |
| Courriels rejetés | Le serveur de courriel du destinataire a rejeté le courriel | L'adresse n'existe pas ou leur boîte de réception est pleine ; ne réessayez pas trop souvent |
| Taux de défaillance élevé soudain | Problème du fournisseur ou identifiants expirés | Vérifiez l'état du fournisseur ; ré-testez la connexion dans **Email Accounts** |

### Vérification de la connexion de votre compte de courriel

Si plusieurs courriels échouent, testez votre compte de courriel :

1. Accédez à **Email System > Email Accounts**
2. Trouvez votre compte actif et vérifiez son statut de **Connection**
3. Si la connexion affiche une erreur, cliquez sur le compte et utilisez l'option **Test Connection** pour diagnostiquer le problème

### Comportement des réessais

Spwig réessaie automatiquement les courriels échoués jusqu'au limite **Max Retries**. Le nombre de réessais affiché sur chaque courriel vous indique combien d'essais ont été effectués. Une fois la limite de réessai atteinte, le courriel reste en statut **Failed** et aucun autre réessai automatique ne se produit.

## Courriels rejetés

Un courriel **Bounced** a été envoyé mais a été renvoyé par le serveur de courriel du destinataire. Il existe deux types de rejets :

- **Hard bounce** — l'adresse courriel n'existe pas ou le domaine n'accepte pas les courriels. Ne réessayez pas les rejets durs ; l'adresse est invalide
- **Soft bounce** — un problème temporaire (boîte de réception pleine, serveur temporairement indisponible). Peut réussir sur réessai

Des rejets répétés vers la même adresse peuvent nuire à votre réputation d'expéditeur auprès des fournisseurs de courriel. Si vous constatez des rejets répétés vers la même adresse client, mettez à jour ou supprimez cette adresse du compte du client.

## Conseils

- Vérifiez la boîte de sortie après des événements majeurs tels qu'une vente flash ou un lancement de produit important pour confirmer que tous les courriels de confirmation des commandes ont été envoyés avec succès
- Si un client affirme n'avoir pas reçu un courriel, recherchez la boîte de sortie par son adresse courriel pour voir s'il a été envoyé, échoué ou ignoré
- Une augmentation soudaine des échecs indique généralement un problème d'identifiants ou de compte — vérifiez **Email Accounts** immédiatement
- Le statut **Held** n'est pas un échec — cela signifie simplement que le courriel est en attente. Libérez les courriels en attente lorsque vous êtes prêt à les envoyer
- Utilisez le filtre **Template Type** pour vérifier rapidement tous les courriels d'un type spécifique — par exemple, vérifiez que tous les confirmations de commande des 7 derniers jours ont un statut **Sent**
- La navigation hiérarchique des dates (jour / mois / année) en haut de la liste est utile pour consulter la boîte de sortie pour une période spécifique