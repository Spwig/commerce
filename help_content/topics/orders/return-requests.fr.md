---
title: Demandes de retour & Traitement
---

Les demandes de retour suivent les retours des clients depuis l'initiation jusqu'à la fin du remboursement — les clients sélectionnent des articles à retourner avec des raisons, les vendeurs approuvent ou rejettent les demandes, génèrent des étiquettes de retour, inspectent les articles retournés et traitent les remboursements. Le workflow progresse à travers 9 étapes d'état (en attente → approuvé → étiquette_envoyée → en_transit → reçu → inspecté → terminé/rejeté/annulé) avec des raisons de retour au niveau des articles, des notes d'inspection et des frais de réapprovisionnement optionnels.

Utilisez cette page d'administration pour revoir, approuver et traiter efficacement les demandes de retour des clients.

## Workflow des demandes de retour

**Processus à 9 étapes**:

### 1. En attente (Client initie)

Client soumet la demande de retour:
- Sélectionne des articles depuis la commande
- Fournit une raison de retour par article
- Notes client optionnelles
- Statut : `en attente`

### 2. Approuvé/Rejeté (Vendeur examine)

Vendeur examine la demande:
- **Approuver** : Retour autorisé, passer à la génération de l'étiquette
- **Rejeter** : Retour refusé avec raison de rejet
- Statut : `approuvé` ou `rejeté`

### 3. Étiquette envoyée (Expédition de retour)

Étiquette de retour générée:
- Vendeur crée l'expédition de retour (optionnel)
- Étiquette de retour envoyée par e-mail au client
- Client renvoie les articles
- Statut : `étiquette_envoyée`

### 4. En transit (Client expédie)

Client expédie les articles:
- Suivi montre le mouvement
- Mise à jour automatique de l'état depuis le webhook du transporteur
- Statut : `en_transit`

### 5. Réçu (Arrivé au entrepôt)

Articles arrivés:
- Entreposage scanne l'expédition
- Articles vérifiés
- Statut : `réçu`

### 6. Inspection (Contrôle de qualité)

Vendeur inspecte les articles:
- Enregistre l'état de l'article (excellent/bon/acceptable/endommagé/defectueux)
- Ajoute des notes d'inspection
- Applique les frais de réapprovisionnement si applicable
- Statut : `inspecté`

### 7. Terminé (Remboursement traité)

Remboursement émis:
- Créez le remboursement associé
- Paiement traité
- Retour fermé
- Statut : `terminé`

**Résultats alternatifs**:
- **Annulé** : Client annule avant l'expédition
- **Rejeté** : Vendeur refuse après examen

---

## Traitement des demandes de retour

**Étapes à suivre**:

**Étape 1 : Examiné les demandes en attente**
- Accédez à Ordres > Demandes de retour
- Filtrez par statut = "En attente"
- Cliquez sur la demande pour voir les détails

**Étape 2 : Évaluer la demande**
- Examinez les détails de la commande
- Vérifiez les raisons de retour
- Vérifiez la conformité avec la politique de retour (dans la période de retour, articles éligibles)

**Étape 3 : Approuver ou Rejeter**
- Cliquez sur "Approuver" pour accepter le retour
- OU cliquez sur "Rejeter" et entrez la raison de rejet
- Enregistrez votre décision

**Étape 4 : Générer l'étiquette de retour** (si approuvé)
- Cliquez sur "Créer l'expédition de retour"
- Sélectionnez le transporteur/service
- Le système génère l'étiquette de retour
- L'étiquette est automatiquement envoyée par e-mail au client
- Statut → `étiquette_envoyée`

**Étape 5 : Suivre le transit**
- Les mises à jour de suivi sont automatiquement synchronisées depuis les webhooks du transporteur
- Le statut avance automatiquement à `en_transit` lorsque le transporteur scanne le colis

**Étape 6 : Réception des articles**
- Lorsque les articles arrivent, cliquez sur "Marquer comme reçu"
- Statut → `réçu`

**Étape 7 : Inspecter les articles**
- Ouvrez la demande de retour
- Sélectionnez l'état de l'article dans le menu déroulant:
  - Excellent (neuf, reventable)
  - Bon (usure mineure, reventable)
  - Acceptable (usure visible, reventable avec remise)
  - Endommagé (non reventable)
  - Défectueux (défaut de fabrication)
- Ajoutez des notes d'inspection
- Optionnel : Appliquez des frais de réapprovisionnement (pourcentage ou fixe)
- Statut → `inspecté`

**Étape 8 : Processus de remboursement**
- Cliquez sur "Créer un remboursement"
- Le système calcule le montant du remboursement:
  - Prix original de l'article
  - Moins les frais de réapprovisionnement (si appliqués)
  - Moins les frais d'expédition (si non remboursables)
- Créez le remboursement (lié à la demande de retour)
- Statut → `terminé`

---

## Raisons de retour au niveau des articles

Les clients sélectionnent une raison par article:

**Raisons courantes**:
- Article erroné reçu
- Article endommagé/défectueux
- Changement d'avis/plus nécessaire
- Article ne correspond pas à la description
- Meilleur prix trouvé
- Commandé par erreur
- Qualité non conforme aux attentes

**Utiliser des raisons pour**:
- Analyse (suivre les causes courantes de retour)
- Contrôle de qualité (identifier les produits défectueux)
- Amélioration du processus (réduire les retours évitables)

---

## Frais de réapprovisionnement

Appliquez des frais pour compenser les coûts de traitement des retours:

**Configuration**:
- **Type** : Pourcentage (ex., 15%) ou Fixe (ex., $5)
- **Quand appliquer** : Retours non défectueux, articles ouverts, commandes spéciales

**Exemple**:
```
Achat original : $100
Frais de réapprovisionnement : 15%
Montant du remboursement : $85
```

**Meilleures pratiques**:
- Communiquez clairement la politique de frais de réapprovisionnement
- Ne les appliquez pas aux articles défectueux
- Pensez à les annuler pour les clients VIP

---

## Lignes directrices d'inspection des retours

Établissez des critères d'inspection cohérents:

**Excellent**:
- Emballage d'origine non ouvert
- Aucune usure visible
- Tous les accessoires inclus
- Entièrement reventable au prix plein

**Bon**:
- Ouvré mais utilisation minimale
- Usure légère de l'emballage
- Tous les composants présents
- Reventable au prix plein

**Acceptable**:
- Usure visible
- Emballage endommagé
- Manque d'accessoires non essentiels
- Reventable avec remise

**Endommagé**:
- Endommagement physique
- Pièces manquantes
- Non reventable
- Déchet ou réparation nécessaire

**Défectueux**:
- Défaut de fabrication
- Échec fonctionnel
- Réclamation de garantie
- Retour au fabricant

---

## Options de livraison de retour

**Option 1 : Le client paie les frais de retour**
- Aucune étiquette de retour fournie
- Le client sélectionne son propre transporteur
- Enregistrement manuel du numéro de suivi

**Option 2 : Le vendeur fournit une étiquette prépayée**
- Générez l'étiquette de retour via le compte du fournisseur
- Coût déduit du remboursement OU le vendeur l'absorbe
- Suivi automatiquement synchronisé

**Option 3 : Retour gratuit**
- Le vendeur absorbe les frais de retour
- Améliore la satisfaction client
- Augmente le taux de retour (considérez le compromis)

---

## Filtrage et rapports

**Filtres utiles**:
- Statut : En attente (action requise)
- Plage de dates : Les 30 derniers jours
- Commande : Recherche d'une commande spécifique
- Raison : Suivre les causes des retours

**Analyse des retours**:
- Taux de retour par produit
- Raisons de retour les plus courantes
- Temps de traitement moyen (en attente → terminé)
- Revenus des frais de réapprovisionnement

---

## Conseils

- **Fixez une politique de retour claire** - Communiquez la fenêtre (30 jours), les conditions, les frais
- **Traitez les demandes rapidement** - Répondez aux demandes en attente dans les 24 heures
- **Inspectez soigneusement** - Documentez l'état pour éviter les litiges
- **Suivez les raisons des retours** - Utilisez les données pour améliorer les produits/descriptions
- **Automatisez là où possible** - Les webhooks des transporteurs mettent à jour automatiquement l'état de transit
- **Communiquez avec les clients** - Envoyez des mises à jour par e-mail à chaque changement d'état
- **Soyez juste avec les frais de réapprovisionnement** - Appliquez de manière cohérente, annulez pour les défectueux
- **Surveillez les fraudes de retour** - Signalez les clients avec de nombreux retours
- **Améliorez l'emballage** - Réduisez les retours liés aux dommages
- **Mettez à jour l'inventaire rapidement** - Restaurez l'inventaire après l'inspection
- **Apprenez des tendances** - Un taux élevé de retour pour un produit spécifique peut indiquer un problème de qualité
