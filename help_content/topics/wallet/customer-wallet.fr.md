---
title: Portefeuille client
---

Le portefeuille client est un système de crédit de magasin qui permet aux clients d'avoir un solde qu'ils peuvent utiliser pour des commandes futures. Le crédit de magasin peut être ajouté en raison de remboursements, de récompenses de parrainage, de campagnes promotionnelles ou d'ajustements manuels effectués par votre équipe. Les clients peuvent ensuite appliquer leur solde de portefeuille à la caisse pour réduire le montant qu'ils paient.

Accédez à **Clients > Portefeuilles clients** pour consulter et gérer les portefeuilles.

## Comprendre les soldes de portefeuille

Chaque portefeuille client affiche quatre figures de solde :

| Solde | Description |
|---|---|
| **Solde disponible** | Le montant que le client peut dépenser dès maintenant à la caisse |
| **Solde en attente** | Crédits non encore utilisables — par exemple, un remboursement qui se trouve encore dans la période de confirmation |
| **Crédit total au cours de la vie** | Le montant total jamais crédité à ce portefeuille, y compris tous les crédits passés |
| **Utilisation totale** | Le montant total que le client a dépensé depuis son portefeuille sur toutes les commandes |

Le solde disponible est la seule figure qui compte à la caisse. Les crédits en attente deviennent disponibles une fois que la période d'attente est expirée.

## Consulter le portefeuille d'un client

1. Accédez à **Clients > Portefeuilles clients**
2. Utilisez le champ de recherche pour trouver le client par nom ou par e-mail
3. Cliquez sur l'entrée du portefeuille pour ouvrir la vue détaillée

La vue détaillée affiche les soldes actuels en haut et un historique complet des transactions en dessous. Les timestamps **Dernier crédit** et **Dernière utilisation** indiquent quand le portefeuille a été utilisé pour la dernière fois.

### Filtre de la liste des portefeuilles

Utilisez le filtre **Actif** pour séparer les portefeuilles actifs des portefeuilles gelés. Un portefeuille marqué comme inactif ne peut pas être utilisé à la caisse, même s'il a un solde positif.

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
- **Débit** — fonds dépensés à la caisse
- **Remboursement** — crédit ajouté spécifiquement en raison d'une commande retournée ou annulée
- **Ajustement** — correction manuelle effectuée par votre équipe
- **Annulation** — transaction qui annule une entrée antérieure

### Explication des sources de transactions

- **Remboursement de commande** — crédit octroyé lorsqu'une commande a été remboursée vers le portefeuille
- **Récompense de parrainage** — crédit gagné via le programme de parrainage
- **Promotion** — crédit octroyé en tant que partie d'une campagne de marketing
- **Ajustement manuel** — crédit ajouté ou retiré directement par un membre du personnel
- **Paiement de commande** — fonds dépensés à la caisse pour payer une commande

## Ajustements manuels du portefeuille

Vous ne pouvez pas ajouter ou retirer directement des fonds depuis la vue détaillée du portefeuille — les transactions de portefeuille sont créées via les processus pertinents (remboursements, récompenses, promotions). Cependant, les membres du personnel ayant les autorisations appropriées peuvent créer des transactions d'ajustement manuel via la section **Transactions de portefeuille**.

Accédez à **Clients > Transactions de portefeuille** et utilisez **+ Ajouter une transaction de portefeuille** si vous avez besoin d'appliquer un crédit qui ne correspond à aucune autre source — par exemple, un crédit de bonne volonté suite à une plainte sur un service.

Lors de la création d'un ajustement manuel :

1.

Sélectionnez le **Portefeuille** que vous ajustez (recherchez par e-mail du client)
2.


Définissez **Type de transaction** sur `Adjustment`
3.

Définissez **Source** sur `Manual Adjustment`
4.

Entrez le **Montant** — toujours un nombre positif, indépendamment de la direction
5.

Définissez le **Statut** sur `Completed` pour un crédit immédiat
6.

Ajoutez une **Description** claire expliquant la raison — cela est visible dans l'historique des transactions
7.

Cliquez sur **Enregistrer**

> **Note :** Puisque les transactions de portefeuille sont immuables, vérifiez soigneusement le montant et le portefeuille avant d'enregistrer. Si vous faites une erreur, vous devrez créer une transaction de réversal pour la corriger.

## Gel d'un portefeuille

Si vous avez besoin d'empêcher un client d'utiliser son solde de portefeuille — par exemple, lors d'une enquête sur la fraude — vous pouvez le désactiver sans le supprimer ou enlever le solde.

1. Ouvrez la vue détaillée du portefeuille du client
2. Désactivez le curseur **Actif**
3. Cliquez sur **Enregistrer**

Le solde est conservé et le portefeuille peut être réactivé à tout moment. Pendant qu'il est inactif, le client ne peut pas utiliser le solde du portefeuille lors du paiement.

## Affichage de toutes les transactions

Pour obtenir une vue globale de l'activité des portefeuilles, accédez à **Customers > Wallet Transactions**. Cette liste affiche toutes les transactions de tous les portefeuilles de clients, avec des filtres pour :

- **Type de transaction** — filtrez par crédit, débit, ajustement, etc.
- **Source** — filtrez par l'origine des transactions
- **Statut** — filtrez par terminé, en attente ou annulé
- **Date** — utilisez la hiérarchie de dates en haut pour explorer un jour, un mois ou une année spécifique

La liste des transactions est en lecture seule — les transactions ne peuvent pas être modifiées ou supprimées depuis cette vue.

## Conseils

- Vérifiez **Crédit total** versus **Utilisation totale** pour comprendre à quel point un client utilise activement son crédit de magasin — un grand solde non utilisé peut indiquer que le client a oublié son existence
- Si un client signale que son solde semble incorrect, examinez l'historique complet des transactions pour retracer exactement comment le solde a changé au fil du temps ; la colonne **Solde après** de chaque entrée facilite cela
- Utilisez les crédits de portefeuille comme outil de fidélisation des clients — un crédit de bonne volonté après une expérience d'achat difficile peut coûter moins qu'un remboursement tout en maintenant le client à dépenser dans votre magasin
- Les portefeuilles gelés conservent leur solde de manière permanente ; il n'y a pas d'expiration — si vous désactivez temporairement un portefeuille, n'oubliez pas de le réactiver une fois que le problème est résolu
- L'**ID de référence** sur chaque transaction renvoie au registre d'origine, ce qui permet de vérifier facilement pourquoi un crédit ou un débit a été appliqué, sans avoir à chercher ailleurs