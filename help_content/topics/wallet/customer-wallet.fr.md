---
title: Portefeuille client
---

Le portefeuille client est un registre de crédit de magasin qui suit un solde en cours pour chaque client. Le crédit de magasin peut être ajouté en raison de remboursements, de récompenses par parrainage, de campagnes promotionnelles ou d'ajustements manuels effectués par votre équipe.

> **Les soldes de portefeuille peuvent être utilisés à la caisse.** Un client connecté possédant un crédit de magasin le voit à l'étape de paiement et peut l'appliquer d'un clic. Le crédit est déduit du montant final de la facture — après les taxes et les frais de livraison — et tout solde restant est facturé à sa carte comme d'habitude. Si le crédit couvre l'ensemble de la commande, aucune carte n'est nécessaire du tout. Le crédit est réservé lorsqu'il est appliqué et n'est effectivement déduit qu'une fois le paiement confirmé, donc un abandon de panier ne coûte rien au client.

Accédez à **Clients > Portefeuilles clients** pour consulter et gérer les portefeuilles.

## Comprendre les soldes de portefeuille

Chaque portefeuille client affiche quatre figures de solde :

| Solde | Description |
|---|---|
| **Solde disponible** | Le crédit actuel et utilisable du client — ce sera le solde utilisable à la caisse une fois que cette fonctionnalité est disponible |
| **Solde en attente** | Crédits qui ne sont pas encore inclus dans le solde disponible — par exemple, un remboursement qui est toujours dans la période de confirmation |
| **Crédit total jamais** | Le montant total jamais crédité à ce portefeuille, y compris tous les crédits passés |
| **Débit total jamais** | Le montant total jamais débité de ce portefeuille |

Le solde disponible est la figure qui aura de l'importance une fois que le paiement via le portefeuille sera disponible. Les crédits en attente passent dans ce solde une fois que la période d'attente expire.

## Consulter le portefeuille d'un client

1. Accédez à **Clients > Portefeuilles clients**
2. Utilisez le champ de recherche pour trouver le client par nom ou par e-mail
3. Cliquez sur l'entrée du portefeuille pour ouvrir la vue détaillée

La vue détaillée affiche les soldes actuels en haut et l'historique complet des transactions en dessous. Les timestamps **Dernier crédit** et **Dernier débit** indiquent quand le portefeuille a été utilisé pour la dernière fois.

### Filtre de la liste des portefeuilles

Utilisez le filtre **Actif** pour séparer les portefeuilles actifs des portefeuilles gelés. Un portefeuille marqué comme inactif est gelé — aucun crédit ou débit ne peut être enregistré contre lui, même s'il conserve son solde.

## Lire l'historique des transactions

Chaque modification du solde d'un portefeuille est enregistrée comme une transaction individuelle. L'historique des transactions est un registre complet et permanent — les transactions ne sont jamais modifiées ou supprimées. Si une erreur doit être corrigée, une nouvelle transaction compensatrice est ajoutée à la place.

Chaque transaction affiche :

| Champ | Description |
|---|---|
| **Type** | Crédit, Débit, Remboursement, Ajustement ou Annulation |
| **Montant** | La valeur de cette transaction (toujours affichée comme un nombre positif) |
| **Solde après** | Le solde du portefeuille immédiatement après que cette transaction ait été appliquée |
| **Source** | L'origine du crédit ou du débit |
| **Statut** | Terminé, En attente ou Annulé |
| **Description** | Une courte explication de la transaction |
| **ID de référence** | Un lien vers l'enregistrement d'origine (par exemple, un numéro de commande ou un ID de récompense) |
| **Créé le** | Quand la transaction a été enregistrée |

### Explication des types de transactions

- **Crédit** — fonds ajoutés au portefeuille (à partir d'un remboursement, d'une promotion ou d'un ajustement manuel)
- **Débit** — fonds retirés du portefeuille. Une fois que le paiement via le portefeuille est disponible, cela signifiera "dépensé sur une commande" — pour l'instant, la seule façon dont un débit se produit est un ajustement manuel
- **Remboursement** — crédit ajouté spécifiquement en raison d'une commande retournée ou annulée
- **Ajustement** — une correction manuelle effectuée par votre équipe
- **Annulation** — une transaction qui annule une entrée antérieure

### Explication des sources de transactions

- **Remboursement de commande** — crédit octroyé lorsqu'une commande a été remboursée vers le portefeuille
- **Récompense de parrainage** — crédit gagné via le programme de parrainage
- **Promotion** — crédit octroyé en tant que partie d'une campagne de marketing
- **Ajustement manuel** — crédit ajouté ou retiré directement par un membre du personnel
- **Paiement de commande** — fonds dépensés à la caisse pour payer une commande. Pas encore utilisé — réservé pour lorsqu'un paiement via le portefeuille sera disponible

## Ajustements manuels du portefeuille

Vous ne pouvez pas ajouter ou retirer des fonds depuis le panneau d'administration — les transactions de portefeuille sont créées uniquement par les processus qui les possèdent : remboursements de commandes, récompenses de fidélité et récompenses de parrainage. Cela est délibéré. Chaque mouvement porte une référence indiquant ce qui l'a provoqué, et une vérification nocturne vérifie le solde de chaque portefeuille par rapport à son propre historique ; les lignes saisies à la main sont ce qui brisent cette chaîne.

Pour un crédit de bonne volonté — un problème de service, un geste après un problème — émettez une **carte cadeau** manuellement à la place (voir le sujet d'aide **Cartes cadeaux**). Une carte cadeau a été conçue exactement pour cela : vous contrôlez la valeur, le client reçoit un code par e-mail, et elle se utilise à la caisse de la même manière que le crédit magasin.

## Bloquer un portefeuille

Si vous avez besoin d'empêcher un client d'utiliser son solde de portefeuille — par exemple, lors d'une enquête sur la fraude — vous pouvez le désactiver sans le supprimer ou enlever le solde.

1. Ouvrez la vue détaillée du portefeuille du client
2. Désactivez le curseur **Actif**
3. Cliquez sur **Enregistrer**

Le solde est conservé et le portefeuille peut être réactivé à tout moment. Pendant qu'il est inactif, aucun nouveau crédit ou débit — manuel ou autre — ne peut être enregistré sur le portefeuille.

## Voir toutes les transactions

Pour obtenir une vue globale de l'activité des portefeuilles, accédez à **Clients > Transactions de portefeuille**. Cette liste affiche toutes les transactions de tous les portefeuilles de clients, avec des filtres pour :

- **Type de transaction** — filtrez par crédit, débit, ajustement, etc.
- **Source** — filtrez par l'endroit d'où proviennent les transactions
- **Statut** — filtrez par terminé, en attente ou annulé
- **Date** — utilisez la hiérarchie de dates en haut pour explorer un jour, un mois ou une année spécifique

La liste des transactions est en lecture seule — les transactions ne peuvent pas être modifiées ou supprimées depuis cette vue.

## Conseils

- Vérifiez **Crédités au cours de la vie** versus **Utilisés au cours de la vie** pour comprendre à quel point un client utilise activement son crédit magasin — un solde non utilisé important peut indiquer que le client a oublié son existence
- Si un client signale que son solde semble incorrect, examinez l'historique complet des transactions pour retracer exactement comment le solde a changé au fil du temps ; la colonne **Solde après** sur chaque entrée rend cela facile
- Un solde non dépensé important vaut une petite poussée — les clients voient leur crédit magasin sur le tableau de bord du compte et à l'étape de paiement à la caisse, mais un e-mail court le signalant souvent le convertit en commande
- Les portefeuilles gelés conservent leur solde de manière permanente ; il n'y a pas d'expiration — si vous désactivez temporairement un portefeuille, n'oubliez pas de le réactiver une fois que le problème est résolu
- L'**ID de référence** sur chaque transaction renvoie au record d'origine, ce qui permet de vérifier facilement pourquoi un crédit ou un débit a été appliqué sans avoir à chercher ailleurs