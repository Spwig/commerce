---
title: Gestion des Commandes
---

Ce guide couvre tout ce dont vous avez besoin pour gérer les commandes de vos clients, de l'examen des nouvelles commandes au traitement des expéditions et à la gestion des remboursements.

## Liste des Commandes

Accédez à **Commandes > Toutes les Commandes** dans la barre latérale pour voir toutes les commandes. La liste affiche le numéro, le statut, le client, le total et la date de chaque commande.

![Order list](/static/core/admin/img/help/manage-orders/order-list.webp)

Utilisez les filtres en haut pour affiner les commandes par statut, plage de dates, ou recherchez par numéro de commande ou nom du client.

## Détail de la Commande

Cliquez sur n'importe quelle commande pour ouvrir sa page de détail. Vous y trouverez toutes les informations sur la commande organisées en sections claires.

![Order detail](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Informations de la Commande

La section supérieure affiche :

- **Numéro de Commande** — L'identifiant unique de cette commande
- **Statut** — Statut actuel de la commande (En attente, En cours, Expédiée, Livrée, Terminée, Annulée)
- **Client** — Nom et adresse e-mail du client qui a passé la commande
- **Créée** — Date de la commande

### Articles de la Commande

La section des articles répertorie tout ce que le client a commandé :

- Nom du produit et SKU
- Quantité commandée
- Prix unitaire et total de la ligne
- Toute remise appliquée

### Détails du Paiement

Affiche le mode de paiement utilisé, l'ID de transaction et le statut du paiement. Pour les commandes en attente de paiement, vous pouvez suivre l'état de la passerelle de paiement ici.

### Adresse de Livraison

L'adresse de livraison du client. Si l'adresse de facturation est différente, les deux sont affichées.

## Cycle de Vie de la Commande

Les commandes passent généralement par ces statuts :

1. **En attente** — Nouvelle commande reçue, en attente de confirmation de paiement
2. **En cours** — Paiement confirmé, préparation de l'expédition
3. **Expédiée** — Commande envoyée avec informations de suivi
4. **Livrée** — Le client a reçu la commande
5. **Terminée** — Commande finalisée

## Traitement d'une Commande

### 1. Examiner la Commande

Vérifiez que :

- Les articles et les quantités sont corrects
- L'adresse de livraison est complète
- Le paiement a été reçu
- Toutes les notes du client ont été prises en compte

### 2. Créer une Expédition

Pour expédier la commande :

1. Cliquez sur **Créer une Expédition** sur la page de détail de la commande
2. Sélectionnez les articles à inclure (pour les expéditions partielles, sélectionnez uniquement certains articles)
3. Choisissez le transporteur et le service d'expédition
4. Saisissez le numéro de suivi
5. Cliquez sur **Enregistrer l'Expédition**

Le statut de la commande est automatiquement mis à jour à **Expédiée** et le client reçoit un e-mail de notification d'expédition avec les informations de suivi.

### 3. Marquer comme Livrée

Une fois que le client confirme la livraison ou que le suivi indique la livraison, mettez à jour le statut à **Livrée** puis à **Terminée**.

## Actions sur la Commande

### Ajouter des Notes

Ajoutez des notes internes ou des messages visibles par le client :

1. Faites défiler jusqu'à la section **Notes** sur la page de détail de la commande
2. Tapez votre message
3. Choisissez s'il s'agit d'une note interne (personnel uniquement) ou d'une notification au client
4. Cliquez sur **Ajouter une Note**

Les notes visibles par le client déclenchent une notification par e-mail.

### Traiter un Remboursement

Pour émettre un remboursement :

1. Cliquez sur **Remboursement** sur la page de détail de la commande
2. Sélectionnez les articles à rembourser (ou saisissez un montant personnalisé)
3. Choisissez un motif de remboursement
4. Confirmez le remboursement

Les remboursements sont traités via la passerelle de paiement d'origine. Le client reçoit un e-mail de confirmation.

### Annuler une Commande

Pour annuler :

1. Cliquez sur **Annuler la Commande**
2. Sélectionnez un motif d'annulation
3. Choisissez si vous souhaitez remettre les articles en stock
4. Confirmez

Le client est notifié automatiquement et un remboursement est initié si le paiement a déjà été effectué.

## Actions Groupées

Depuis la liste des commandes, vous pouvez sélectionner plusieurs commandes et appliquer des actions groupées :

- **Mettre à jour le statut** — Déplacer plusieurs commandes vers le même statut
- **Exporter** — Télécharger les commandes sélectionnées au format CSV
- **Imprimer** — Générer des bons de livraison ou des factures

## Notifications de Commande

Les clients reçoivent automatiquement des e-mails aux étapes clés :

- **Confirmation de commande** — Immédiatement après avoir passé la commande
- **Paiement reçu** — Lorsque le paiement est confirmé
- **Notification d'expédition** — Lorsqu'une expédition est créée (inclut le lien de suivi)
- **Confirmation de livraison** — Lorsque la commande est marquée comme livrée

Configurez les modèles d'e-mails dans **Paramètres > Configuration des E-mails**.

## Conseils

- Traitez les commandes quotidiennement pour maintenir des délais d'expédition rapides.
- Utilisez les filtres de statut pour vous concentrer sur les commandes nécessitant une attention particulière (En attente et En cours).
- Ajoutez des notes internes pour suivre toute exigence de traitement spéciale.
- Pour les périodes de forte activité, utilisez les actions groupées pour mettre à jour plusieurs commandes en une fois.
- Mettez en place des règles d'expédition pour automatiser la sélection du transporteur en fonction du poids de la commande et de la destination.
