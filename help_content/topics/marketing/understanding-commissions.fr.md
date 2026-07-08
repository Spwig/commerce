---
title: Comprendre les commissions
---

Les commissions sont des enregistrements de revenus créés lorsque l'un de vos affiliés parvient à générer un achat sur votre boutique. Chaque commission est liée à un ordre spécifique, à un affilié et à un programme, et traverse un cycle de vie allant du statut en attente au statut payé. Ce guide explique comment fonctionnent les commissions, comment elles sont calculées et comment les gérer efficacement.

## Qu'est-ce qu'une commission ?

Une commission représente le montant dû à un affilié pour avoir fait référence à un client qui a effectué un achat. Lorsqu'un client clique sur le lien de référence d'un affilié et passe une commande dans la fenêtre de validité du cookie, Spwig crée automatiquement un enregistrement de commission.

Chaque commission contient :
- **Affilié** — Le partenaire qui a fait référence au client
- **Programme** — Le programme d'affiliation qui définit les règles des commissions
- **Ordre** — L'ordre qui a généré la commission
- **Montant** — La valeur de la commission calculée
- **Statut** — L'étape actuelle dans le cycle de vie de la commission
- **Dates** — Date de création, date d'approbation/refus et date de paiement

## Calcul des commissions

Les commissions sont calculées automatiquement en fonction du type de commission et du taux du programme.

| Type de commission | Calcul | Exemple |
|-------------------|--------|---------|
| **Pourcentage** | Total de la commande × pourcentage de commission ÷ 100 | Commande : 200 $, Taux : 10 % → **Commission de 20 $** |
| **Fixe** | Montant fixe par commande | Taux : 15 $ → **Commission de 15 $** (indépendamment de la valeur de la commande) |

### Exemples de calcul

**Commission en pourcentage (10 %)** : 
- Client passe une commande de 50 $ → 5 $ de commission
- Client passe une commande de 150 $ → 15 $ de commission
- Client passe une commande de 300 $ → 30 $ de commission

**Commission fixe (20 $)** : 
- Client passe une commande de 50 $ → 20 $ de commission
- Client passe une commande de 150 $ → 20 $ de commission
- Client passe une commande de 300 $ → 20 $ de commission

La commission est calculée sur le **sous-total de la commande** (avant les frais de livraison et les taxes) et est créée immédiatement lors de la passation de la commande.

## Cycle de vie des commissions

Chaque commission traverse une série de statuts de la création au paiement : 

```
En attente → Approuvée → Payée
   ↓
Refusée
```

### Définitions des statuts

| Statut | Description | Ce qui se passe |
|--------|-------------|------------------|
| **En attente** | Commande passée, commission en attente de vérification | La commission est créée mais pas encore confirmée. L'affilié peut la voir mais ne peut pas retirer d'argent. |
| **Approuvée** | Le commerçant confirme que la vente est valide | La commission est vérifiée et ajoutée au solde disponible de l'affilié. Éligible au paiement. |
| **Refusée** | Le commerçant refuse la commission | La commission est refusée (par exemple, commande remboursée, fraude ou violation des conditions). Non éligible au paiement. |
| **Payée** | La commission a été incluse dans un paiement terminé | L'affilié a été payé. La commission est finalisée et ne peut plus être modifiée. |

![Liste des commissions](/static/core/admin/img/help/commission-management/commission-list.webp)

## Quand les commissions sont créées

Les commissions sont créées automatiquement selon cette séquence : 

1. **Le client clique sur le lien de l'affilié** — L'URL de référence contient le code de suivi unique de l'affilié (par exemple, `?ref=JOHNSMITH`)
2. **Un cookie est défini** — Un cookie de suivi est stocké dans le navigateur du client avec le code de l'affilié
3. **Achat dans la période de validité du cookie** — Le client termine une commande avant l'expiration du cookie (par défaut : 30 jours)
4. **Le système attribue l'ordre** — Spwig vérifie la présence d'un cookie de suivi actif et identifie l'affilié qui a fait référence au client
5. **Commission créée automatiquement** — Un enregistrement de commission est généré avec le statut **En attente**

La commission est créée **immédiatement** lors de la passation de la commande, même avant la confirmation du paiement. Cela permet aux commerçants de vérifier les commissions pendant le traitement des commandes.

## Suivi et attribution

Spwig utilise le **modèle d'attribution sur le dernier clic** pour déterminer quel affilié doit recevoir le crédit pour une vente.

### Fonctionnement de l'attribution

- **Modèle du dernier clic** — Le dernier lien d'affiliation cliqué obtient le crédit (même si plusieurs affiliés ont fait référence au client)
- **Suivi basé sur les cookies** — Un cookie stocke le code de l'affilié dans le navigateur du client
- **Durée de validité du cookie** — Détermine la fenêtre pendant laquelle une vente peut être attribuée (configurée par programme, généralement 30 jours)
- **Suivi de l'IP et des sessions** — Des données supplémentaires aident à identifier les schémas frauduleux

### Exemple d'attribution

- Jour 1 : Le client clique sur le lien de l'affilié A → Cookie défini pour l'affilié A
- Jour 5 : Le client clique sur le lien de l'affilié B → Cookie **mis à jour** pour l'affilié B (le dernier clic l'emporte)
- Jour 7 : Le client passe une commande → La commission revient à **l'affilié B**

Si le client revient le Jour 35 (après l'expiration du cookie de 30 jours) et passe une commande, **aucune commission** n'est créée car la fenêtre de suivi est fermée.

## Détails des commissions

Accédez à **Marketing > Commissions** pour consulter tous les enregistrements de commissions.

### Champs des commissions

Chaque commission affiche : 

| Champ | Description |
|-------|-------------|
| **Affilié** | Le nom et le code de l'affilié |
| **Programme** | Le nom du programme d'affiliation |
| **Ordre** | Numéro de commande (lien cliquable pour consulter les détails complets de la commande) |
| **Montant** | Valeur de la commission calculée |
| **Statut** | Étape actuelle (En attente, Approuvée, Refusée, Payée) |
| **Créé le** | Quand la commission a été générée |
| **Date d'approbation/refus** | Quand le statut a été mis à jour |
| **Date de paiement** | Quand le paiement a été traité |
| **Notes** | Notes internes concernant la commission |

### Voir les détails de la commande

Cliquez sur le **numéro de commande** dans l'enregistrement de la commission pour consulter la commande originale. Cela vous permet de vérifier : 
- Total de la commande et articles achetés
- Informations sur le client
- Statut du paiement
- Statut de livraison
- Toute remise ou retour

Ce contexte vous aide à décider si vous souhaitez approuver ou refuser la commission.

## Gestion des commissions

Bien que ce guide se concentre sur la compréhension des commissions, les étapes pratiques pour approuver, refuser et payer les commissions sont détaillées dans le sujet d'aide **Gestion des commissions**.

### Aperçu rapide

- **Approbation** — Vérifiez que l'ordre est légitime et confirmez que la commission est valide
- **Refus** — Refusez les commissions pour les commandes frauduleuses, les remboursements ou les violations des politiques
- **Ajout de notes** — Documentez les raisons de l'approbation ou du refus pour référence ultérieure
- **Traitement des paiements** — Groupez les commissions approuvées en paiements par lots

Consultez les sujets d'aide connexes pour obtenir des instructions étape par étape pour chaque tâche de gestion.

## Conseils

- Examinez les commissions en attente **quotidiennement** pendant votre premier mois pour établir un rythme et détecter tout problème de suivi dès le début
- Configurez des **notifications par e-mail** pour être alerté lors de la création de nouvelles commissions afin de les vérifier pendant que les détails de la commande sont encore frais
- Approuvez les commissions **après la livraison de la commande** (et non immédiatement après la passation de la commande) pour tenir compte des annulations et des retours
- Utilisez le **champ de notes** pour documenter vos décisions, en particulier pour les commissions refusées, afin d'avoir un enregistrement si les affiliés posent des questions
- Recherchez **les motifs de refus** — si un affilié a beaucoup de commissions refusées, cela peut indiquer une fraude ou une malcompréhension des termes du programme
- Pensez à créer une **politique d'approbation des commissions** (par exemple, « approuvée après la fenêtre de retour de 14 jours ») et communiquez-la aux affiliés pour fixer des attentes claires

