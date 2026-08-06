---
title: Cartes cadeaux
---

Les cartes cadeaux sont un crédit magasin que les clients peuvent acheter pour quelqu'un d'autre — ou pour eux-mêmes — envoyé par e-mail sous forme de code de rédemption unique. Vous pouvez également émettre une carte cadeau directement depuis l'admin sans achat client.

La vente de cartes cadeaux est active. Lorsqu'un client en achète une, la carte est créée et envoyée par e-mail automatiquement une fois que leur paiement est validé — jamais avant, afin qu'aucun client ne reçoive un code pour un paiement qui échouera plus tard.

Quelques choses à savoir avant d'activer un produit de carte cadeau :

- **Une carte cadeau est de l'argent, pas un rabais.** Elle est déduite du montant final après les taxes et les frais d'expédition, et elle ne réduit pas les impôts que vous devez. Cela est contraire à un bon de réduction, qui réduit le prix des marchandises.
- **Les cartes sont uniques en devise.** Une carte achetée en euros ne peut être utilisée que pour un achat en euros. Si vous vendez en plusieurs devises, créez un produit de carte cadeau distinct pour chacune. Cela vous protège des fluctuations des taux de change sur un solde qui pourrait ne pas être utilisé pendant un an.
- **Les cartes cadeaux ne peuvent pas être rabattues.** Un bon de réduction ne s'appliquera pas à une ligne de carte cadeau, car vendre 100 £ de crédit pour 80 £ vous coûte 20 £ chaque fois.
- **Une carte cadeau ne peut pas acheter une autre carte cadeau.** Cela ferme une voie que les gens utilisent pour blanchir des détails de carte volée.
- **Acheter une carte cadeau n'octroie pas de points de fidélité.** Les points sont gagnés lorsque la carte est utilisée pour acheter des marchandises, donc personne ne gagne deux fois sur le même argent.

![Gestion des cartes cadeaux](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Types de dénominations

Ces paramètres contrôlent la manière dont un client choisit le montant lors de l'achat d'une carte cadeau :

| Type | Description |
|------|-------------|
| **Dénominations fixes** | Les clients choisissent parmi des montants prédéfinis (ex. 25 $, 50 $, 100 $) |
| **Montant personnalisé** | Les clients entrent tout montant compris entre un minimum et un maximum |
| **Les deux** | Proposer des dénominations prédéfinies ainsi qu'une option de montant personnalisé |

## Créer un produit de carte cadeau

Toute carte cadeau — qu'elle soit finalement vendue ou émise manuellement aujourd'hui — a besoin d'un produit de type carte cadeau derrière elle.

### Étape 1 : Configurer le produit

1. Accédez à **Produits > Tous les produits** et cliquez sur **+ Ajouter un produit**
2. Définissez **Type de produit** sur **Carte cadeau**
3. Remplissez le nom et la description du produit
4. Configurez les paramètres de dénomination :
   - Choisissez un **Type de dénomination** (Fixe, Personnalisé ou Les deux)
   - Pour Fixe : définissez les montants de dénomination disponibles
   - Pour Personnalisé : définissez le **Minimum** et le **Maximum** autorisés
5. Définissez **Jours d'expiration** (0 = ne jamais expirer) — cela détermine combien de temps les cartes cadeaux sont valides après l'achat
6. Enregistrez et publiez le produit

### Étape 2 : Publication

Publiez le produit lorsque vous êtes prêt à le vendre. Les clients peuvent l'acheter directement depuis votre boutique en ligne dès maintenant, et la carte est envoyée par e-mail automatiquement une fois que leur paiement est validé.

Ce produit est également celui que vous sélectionnez lors de l'émission manuelle d'une carte — donc il vaut la peine de l'en créer même si vous prévoyez uniquement de donner des cartes cadeaux.

## Créer une carte cadeau manuellement

C'est la seule façon de créer une carte cadeau financée pour le moment, et elle fonctionne pleinement aujourd'hui.

1. Accédez à **Produits > Cartes cadeaux** et cliquez sur **+ Ajouter une carte cadeau**
2. Choisissez le **Produit** — cela doit être un produit de type carte cadeau existant (voir ci-dessus)
3. Entrez la **Valeur initiale** — le solde de départ, dans le montant que vous choisissez. Contrairement à un achat client, cela n'est pas limité aux paramètres de dénomination du produit
4. Définissez optionnellement une date **Expire à**, et laissez **Actif** coché afin que la carte puisse être réclamée
5. Remplissez la section **Destinataire**, plus bas sur la même page :
   - **E-mail du destinataire** — obligatoire ; l'endroit où l'e-mail de livraison sera envoyé
   - **Nom du destinataire**, **Nom de l'expéditeur** et **Message personnel** — tous optionnels
   - **Date d'envoi planifiée** — optionnel ; laissez vide et envoyez quand vous êtes prêt, ou définissez une date/heure future (ex. un anniversaire)
6. Cliquez sur **Enregistrer**

Le code de réclamation est généré automatiquement et le solde initial est défini à partir de la Valeur initiale — vous ne remplissez ni l'un ni l'autre vous-même.

**Enregistrement de la carte ne l'envoie pas par courriel.** Pour l'envoyer, retournez à la liste des cartes-cadeaux, sélectionnez la case à cocher de la carte, choisissez **Envoyer les courriels de carte-cadeaux** dans le menu déroulant Actions, puis cliquez sur **Aller**.

La même action permet de renvoyer le courriel si vous avez besoin de le faire plus tard.

## Gestion des cartes-cadeaux dans l'administration

Accédez à **Produits > Cartes-cadeaux** pour gérer toutes les cartes-cadeaux :

### Tableau de bord des statistiques

En haut de la page, quatre cartes affichent des indicateurs clés :

- **Total des cartes-cadeaux** — Nombre total de cartes-cadeaux émises
- **Actives** — Cartes actives avec un solde disponible
- **Solde total** — Solde restant combiné de toutes les cartes
- **Partiellement utilisées** — Cartes qui ont été partiellement réclamées

### Filtres

Filtrez les cartes-cadeaux par :

- **Recherche** — Trouver par code, courriel ou nom du destinataire
- **Statut** — Actives, Inactives, Expirées, Totalement Réclamées ou Partiellement Utilisées
- **Solde** — Avec solde ou sans solde
- **Créé** — Période de temps (Aujourd'hui, Cette semaine, Ce mois, Cette année)

### Détails de la carte-cadeaux

Chaque carte-cadeaux affiche :

- **Code** — Le code unique de réclamation (ex. GC-XXXX-XXXX-XXXX)
- **Destinataire** — Courriel et nom
- **Badges de statut** — Statut actuel avec une coloration
- **Solde / Initial / Réclamé** — Résumé financier avec le pourcentage utilisé
- **Dates importantes** — Créé, émis, première utilisation
- **Expéditeur** — Qui a acheté (ou qui a émis) la carte-cadeaux

### Actions

- Cliquez sur une carte-cadeaux pour **éditer** ses détails et consulter son **historique complet de transactions**, affiché en ligne sur la même page
- Sélectionnez une ou plusieurs cartes et utilisez le menu déroulant **Actions** pour **Envoyer les courriels de carte-cadeaux** (envoie ou renvoie le courriel d'envoi) ou **Marquer les cartes-cadeaux sélectionnées comme inactives** (désactive — le solde est préservé mais la carte ne peut plus être réclamée)

## Réclamation aujourd'hui

**En magasin**, à votre terminal de caisse :

1. Le caissier prend le code à l'étape du paiement
2. Le code est validé — actif, non expiré, avec un solde, et dans la même devise que la vente
3. Le solde est appliqué au montant total dû, y compris les taxes et les frais de livraison
4. Si le solde ne couvre pas l'ensemble de la vente, le client paie le reste d'une autre manière
5. Le solde est déduit et la transaction est enregistrée

Notez que le caissier prend le code à l'**étape du paiement**, et non lors de la création du panier. Une carte-cadeaux est de l'argent que le client a déjà donné, donc elle règle la facture plutôt que de réduire les marchandises.

**En ligne**, le processus de paiement inclut un champ pour la carte-cadeaux à l'étape du paiement. Le client entre son code, le solde est déduit du montant dû — après les taxes et les frais de livraison — et le reste est facturé à sa carte comme d'habitude. Si la carte couvre l'ensemble de la commande, aucun autre paiement n'est nécessaire. Le solde n'est déduit qu'une fois le paiement confirmé, donc un panier abandonné ne touche jamais la carte.

Les destinataires peuvent également vérifier leur solde restant à tout moment via le lien dans leur courriel d'envoi.

## Gestion des remboursements

Lors du remboursement de commandes ou de ventes qui ont utilisé une carte-cadeaux :

- **Une carte-cadeaux achetée par le client et encore inutilisée** — la carte est désactivée et son solde est annulé, donc le crédit disparaît avec le remboursement.
- **Une carte-cadeaux achetée par le client et partiellement utilisée** — cela nécessite votre jugement. Désactiver la carte retirerait le crédit déjà utilisé, donc le solde reste intact et est marqué pour que vous l'ajustez manuellement.
- **Une carte-cadeaux utilisée pour payer la commande remboursée** — le remboursement est d'abord retourné sur la carte, avant tout paiement par carte ou par banque. Rembourser de l'argent à une banque dont le commerçant n'a jamais réellement collecté est une erreur plus grave, et le fait de rendre la valeur là d'où elle vient ferme également une voie connue de fraude. Si la carte originale a depuis expiré ou a été désactivée, une nouvelle carte est émise au même destinataire sans date d'expiration.
- **Remboursement total** — Créditez le montant sur le solde de la carte-cadeaux via une transaction de remboursement

## Conseils

Conservez tous les formats de mise en forme markdown, les chemins d'image, les blocs de code et les termes techniques.

- Utilisez l'émission manuelle pour les crédits de bonne volonté, les résolutions liées au service client ou tout cas où vous souhaitez accorder un crédit de magasin à un client sans achat via le site.
- Fixez des durées d'expiration raisonnables (par exemple, 365 jours) afin de respecter les réglementations locales sur les cartes-cadeaux — certaines juridictions exigent des durées minimales de validité.
- Utilisez le type de désignation "Both" pour offrir à la fois commodité (montants prédéfinis) et flexibilité (un montant personnalisé).
- Surveillez régulièrement le métrique Solde total — il représente une dette impayée sur vos livres comptables.
- Une carte s'utilise de la même manière en ligne et en personne — lors du paiement à l'étape de paiement lors du passage à la caisse en ligne, ou au comptoir.

L'e-mail de livraison inclut un lien permettant de vérifier le solde, que les destinataires peuvent utiliser à tout moment.
- Si vous vendez à des clients dans plusieurs pays, vous pouvez émettre des cartes-cadeaux dans des devises spécifiques — consultez le sujet d'aide **Multi-Currency Gift Cards** pour plus de détails.