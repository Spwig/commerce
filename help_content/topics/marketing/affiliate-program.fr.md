---
title: Programme de parrainage
---

Le programme de parrainage vous permet de recruter des partenaires qui promeuvent vos produits et gagnent des commissions sur les ventes qu'ils génèrent. Les affiliés partagent des liens de parrainage uniques, et Spwig suit automatiquement les clics, attribue les commandes et calcule les commissions.

![Programmes de parrainage](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Comment ça fonctionne

1. Vous créez un ou plusieurs **programmes de parrainage** avec des taux de commission et des règles
2. Les affiliés **s'inscrivent** via un portail public ou sont ajoutés manuellement
3. Chaque affilié obtient un **lien de parrainage unique** avec un code de suivi
4. Lorsqu'un client clique sur le lien et effectue un achat, une **commission** est enregistrée
5. Vous examinez et approuvez les commissions, puis traitez les **versements**

## Création d'un programme

Accédez à **Marketing > Programmes de parrainage** et cliquez sur **Ajouter un programme**.

### Paramètres du programme

| Paramètre | Description |
|---------|-------------|
| **Nom** | Nom du programme visible aux affiliés (ex. : "Programme Partenaire") |
| **Type de commission** | **Pourcentage** du montant total de la commande ou **Montant fixe** par achat |
| **Taux de commission** | Le pourcentage ou le montant fixe que gagnent les affiliés |
| **Durée de vie du cookie** | Nombre de jours pendant lesquels le cookie de suivi du parrainage est valide (par défaut : 30 jours) |
| **Montant minimum de versement** | Montant minimum gagné avant qu'un affilié ne puisse demander un versement |
| **Approuver automatiquement les affiliés** | Accepter automatiquement les nouvelles demandes d'inscription des affiliés, ou demander une approbation manuelle |
| **Statut** | Actif, en pause ou fermé |

### Types de commissions

- **Pourcentage** — Les affiliés gagnent un pourcentage du sous-total de chaque commande qu'ils ont générée (ex. : 10 % d'une commande de 100 $ = 10 $ de commission)
- **Montant fixe** — Les affiliés gagnent un montant fixe par achat, indépendamment de la valeur de la commande (ex. : 5 $ par achat)

## Gestion des affiliés

Accédez à **Marketing > Affiliés** pour consulter et gérer les comptes affiliés.

### Détails de l'afillie

Chaque affilié a :
- **Code affilié** — Un code unique utilisé dans les URLs de parrainage (généré automatiquement ou personnalisé)
- **Lien de parrainage** — L'URL complète que l'afillie partage (ex. : `yourstore.com/?ref=CODE`)
- **Statut** — En attente, approuvé ou rejeté
- **Méthode de paiement** — La manière dont l'afillie reçoit les versements (PayPal ou virement bancaire)
- **Appartenance au programme** — Quels programmes l'afillie appartient

### Ajout d'affiliés manuellement

1. Cliquez sur **Ajouter un affilié**
2. Sélectionnez un compte client existant ou créez un nouveau compte
3. Affectez l'afillie à un ou plusieurs programmes
4. Définissez le code affilié (ou laissez-le vide pour générer automatiquement)

### Portail affilié

Les affiliés accèdent à un portail public où ils peuvent :
- Voir leur tableau de bord avec leurs revenus et statistiques de clics
- Copier leurs liens de parrainage
- Suivre l'historique des commissions
- Demander des versements

L'URL du portail est automatiquement disponible à `/affiliate/` sur votre boutique.

## Suivi et commissions

### Comment fonctionne le suivi

1. Un client clique sur un lien de parrainage d'un affilié
2. Un cookie de suivi est défini dans le navigateur du client (valide pendant la durée de vie du cookie configurée)
3. Si le client passe une commande pendant la durée de vie du cookie, la commande est attribuée à l'afillie
4. Un enregistrement de commission est créé avec le statut **En attente**

### États des commissions

| État | Description |
|--------|-------------|
| **En attente** | Commission enregistrée, en attente de vérification |
| **Approuvée** | Vérifiée et prête pour le versement |
| **Rejetée** | Commission refusée (ex. : commande frauduleuse ou article retourné) |
| **Payée** | Commission incluse dans un versement terminé |

### Vérification des commissions

Accédez à **Marketing > Commissions** pour vérifier les commissions en attente :

1. Vérifiez les détails de la commande pour confirmer que la vente est légitime
2. Cliquez sur **Approuver** pour confirmer, ou **Rejeter** avec une raison
3. Les commissions approuvées s'accumulent vers le solde de versement de l'afillie

## Versements

Lorsque le solde de commission approuvé d'un affilié atteint le seuil minimum de versement, vous pouvez traiter un versement.

### Traitement des versements

1. Accédez à **Marketing > Versements**
2. Sélectionnez les affiliés avec des soldes disponibles
3. Choisissez le mode de paiement : 
   - **PayPal** — Envoyez les fonds directement à l'adresse e-mail PayPal de l'afillie
   - **Virement bancaire** — Enregistrez un virement bancaire manuel
4. Confirmez et traitez le versement
5. Le statut du versement passe à **Terminé** et les commissions sont marquées comme **Payées**

### Fournisseurs de versements

Spwig s'intègre avec des fournisseurs de paiement pour des versements automatisés : 
- **PayPal** — Versements de masse automatisés via l'API PayPal
- **Airwallex** — Versements internationaux avec des taux de change compétitifs
- **Manuel** — Enregistrez les versements traités en dehors de Spwig

## Liens de parrainage

Chaque lien de parrainage d'un affilié suit ce modèle : 

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Les affiliés peuvent également créer des liens vers des produits ou des catégories spécifiques : 

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

Le paramètre `ref` fonctionne sur toutes les pages — le cookie de suivi est défini indépendamment de la page d'atterrissage.

## Analytique du programme

Le tableau de bord du programme de parrainage affiche : 
- **Total des clics** — Le nombre de fois où les liens de parrainage ont été cliqués
- **Total des commandes** — Les commandes attribuées aux affiliés
- **Total des commissions** — Somme de toutes les commissions (en attente, approuvées et payées)
- **Affiliés actifs** — Nombre d'affiliés approuvés qui génèrent actuellement des parrainages

## Conseils

- Commencez avec une **commission basée sur un pourcentage** (5–15 %) — elle s'adapte naturellement à la valeur de la commande et est facile à comprendre pour les affiliés.
- Fixez une **durée de vie du cookie de 30 jours** comme base — cela donne aux clients le temps de revenir et de terminer leur achat tout en attribuant toujours la vente à l'afillie.
- Activez l'**approbation automatique** pour les programmes publics afin de réduire les frictions, ou utilisez l'approbation manuelle pour les programmes invités où vous souhaitez vérifier chaque affilié.
- Fixez un **montant minimum de versement** raisonnable (ex. : 25 $–50 $) pour éviter de traiter de nombreuses transactions petites.
- Personnalisez le **portail affilié** pour correspondre à votre marque — les affiliés sont plus enclins à promouvoir votre boutique lorsque l'expérience semble professionnelle.
- Surveillez régulièrement les commissions pour des **patterns frauduleux** tels que les auto-parrainages, des taux de retour anormalement élevés ou des volumes de clics suspects.