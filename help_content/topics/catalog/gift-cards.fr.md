---
title: Cartes cadeaux
---

Les cartes cadeaux permettent à vos clients d'acheter un crédit de magasin qu'ils peuvent envoyer à quelqu'un comme cadeau ou conserver à leur usage personnel. Les destinataires reçoivent un code unique par e-mail qu'ils peuvent utiliser lors du paiement.

![Gestion des cartes cadeaux](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Types de dénominations

Contrôlez la façon dont les clients choisissent le montant de la carte cadeau:

| Type | Description |
|------|-------------|
| **Dénominations fixes** | Les clients choisissent parmi des montants prédéfinis (par exemple, 25 $, 50 $, 100 $) |
| **Montant personnalisé** | Les clients entrent tout montant compris entre un minimum et un maximum |
| **Les deux** | Proposez des dénominations prédéfinies ainsi qu'une option de montant personnalisé |

## Création d'un produit de carte cadeau

### Étape 1: Créer le produit

1. Accédez à **Produits > Tous les produits** et cliquez sur **+ Ajouter un produit**
2. Définissez le **Type de produit** sur **Carte cadeau**
3. Remplissez le nom et la description du produit
4. Configurez les paramètres de dénomination:
   - Choisissez un **Type de dénomination** (Fixe, Personnalisé ou Les deux)
   - Pour Fixe: définissez les montants de dénomination disponibles
   - Pour Personnalisé: définissez le **Minimum** et le **Maximum** des montants autorisés
5. Définissez le **Nombre de jours avant expiration** (0 = ne jamais expirer) — cela détermine la durée de validité des cartes cadeaux après l'achat
6. Enregistrez et publiez le produit

### Étape 2: Publier et vendre

Une fois publié, la carte cadeau apparaît dans votre boutique en ligne comme tout autre produit. Les clients peuvent la consulter, choisir un montant et l'ajouter à leur panier.

## Cycle de vie d'une carte cadeau

Une carte cadeau suit ce cycle de vie:

1. **Achat** — Le client achète le produit de carte cadeau et fournit les détails du destinataire
2. **Livraison** — Un e-mail contenant le code de la carte cadeau est envoyé automatiquement au destinataire
3. **Utilisation** — Le destinataire entre le code lors du paiement pour appliquer le solde
4. **Suivi du solde** — Chaque utilisation déduit du solde jusqu'à ce qu'il atteigne zéro

## Flux d'achat du client

Lorsqu'un client achète une carte cadeau:

1. **Choisir le montant** — Choisir une dénomination ou entrer un montant personnalisé
2. **Détails du destinataire** — Entrer l'adresse e-mail et le nom du destinataire
3. **Message personnel** — Ajouter un message optionnel à inclure dans l'e-mail de livraison
4. **Nom de l'expéditeur** — Fournir le nom de l'expéditeur pour l'e-mail
5. **Livraison planifiée** — Planifier optionnellement l'e-mail pour une date ultérieure (par exemple, un anniversaire)
6. **Paiement** — Terminer l'achat comme tout autre produit

## Livraison automatique

Après l'achat, la carte cadeau est livrée automatiquement:

- Un e-mail stylisé est envoyé au destinataire avec:
  - Le code unique de la carte cadeau
  - La valeur de la carte cadeau
  - Le message personnel de l'expéditeur
  - Un lien pour vérifier le solde restant
- Si une livraison planifiée a été définie, l'e-mail est envoyé à la date et à l'heure spécifiées
- L'expéditeur reçoit une confirmation de commande avec les détails de la carte cadeau

## Gestion des cartes cadeaux dans l'administration

Accédez à **Produits > Cartes cadeaux** pour gérer toutes les cartes cadeaux:

### Tableau de bord des statistiques

En haut de la page, quatre cartes affichent des indicateurs clés:

- **Total des cartes cadeaux** — Nombre total de cartes cadeaux émises
- **Actives** — Cartes actives avec un solde disponible
- **Total du solde** — Solde restant combiné de toutes les cartes
- **Utilisées partiellement** — Cartes qui ont été partiellement utilisées

### Filtres

Filtrez les cartes cadeaux par:

- **Recherche** — Trouver par code, e-mail ou nom du destinataire
- **Statut** — Actives, Inactives, Expirées, Totalement utilisées ou Utilisées partiellement
- **Solde** — Avec solde ou Solde nul
- **Créé** — Période de temps (Aujourd'hui, Cette semaine, Ce mois, Cette année)

### Détails de la carte cadeau

Chaque carte cadeau affiche:

- **Code** — Le code unique de rédemption (par exemple, GC-XXXX-XXXX-XXXX)
- **Destinataire** — E-mail et nom
- **Badges de statut** — Statut actuel avec une coloration
- **Solde / Initial / Utilisé** — Résumé financier avec le pourcentage utilisé
- **Dates importantes** — Créé, émis, première utilisation
- **Expéditeur** — Qui a acheté la carte cadeau

### Actions

Pour chaque carte cadeau, vous pouvez:

- **Modifier** — Voir et modifier les détails de la carte cadeau
- **Voir les transactions** — Voir l'historique complet des transactions
- **Renvoyer l'e-mail** — Renvoyer l'e-mail de livraison au destinataire
- **Désactiver** — Désactiver la carte (le solde est préservé mais la carte ne peut plus être utilisée)

## Utilisation à la caisse

Lorsqu'un client entre un code de carte cadeau à la caisse:

1. Le code est validé (actif, non expiré, avec solde)
2. Le solde disponible est affiché
3. Le solde est appliqué au total de la commande
4. Si le solde couvre l'ensemble de la commande, aucun paiement supplémentaire n'est nécessaire
5. Si le solde est inférieur au total de la commande, le client paie le reste
6. La transaction est enregistrée et le solde est mis à jour

## Gestion des remboursements

Lorsque vous remboursez des commandes qui ont utilisé une carte cadeau:

- **Cartes cadeaux non utilisées** — Désactiver complètement la carte cadeau
- **Cartes partiellement utilisées** — Le solde doit être ajusté manuellement via une transaction
- **Remboursement total** — Créditer le montant sur le solde de la carte cadeau via une transaction de remboursement

## Conseils

- Fixez des périodes d'expiration raisonnables (par exemple, 365 jours) pour respecter les réglementations locales sur les cartes cadeaux — certaines juridictions exigent des durées minimales de validité.
- Utilisez le type de dénomination "Les deux" pour offrir commodité (montants prédéfinis) et flexibilité (montants personnalisés).
- Surveillez régulièrement le métrique Total du solde — il représente une dette restante sur vos livres comptables.
- Utilisez la livraison planifiée pour les promotions saisonnières — les clients peuvent acheter des cartes cadeaux en avance et les avoir livrées à la date exacte.
- Testez le flux complet (achat, livraison par e-mail, utilisation) avec une commande de test avant de lancer.
- Si vous vendez à des clients dans plusieurs pays, vous pouvez émettre des cartes cadeaux en devises spécifiques — consultez le sujet d'aide **Cartes cadeaux multidevises** pour plus de détails.