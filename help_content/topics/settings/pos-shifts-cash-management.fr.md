---
title: Shifts POS et Gestion du Trésor
---

Les shifts POS suivent les périodes de travail des caissiers et assurent une comptabilité précise du trésor. Chaque shift représente le temps d'un caissier sur un terminal, de l'ouverture du tiroir-caisse avec un compte initial de trésor à la fermeture du shift avec un compte final et une conciliation. Le système calcule automatiquement le trésor attendu en fonction des ventes en espèces réelles et le compare au compte physique, mettant en évidence les écarts pour investigation. Les mouvements de trésor pendant les shifts (ajouts de trésor, retraits de trésor de poche) sont suivis avec des raisons pour des traçabilités d'audit complètes.

Accédez à **POS > Shifts** pour consulter tous les shifts, surveiller les shifts actifs, consulter les rapports de conciliation du trésor et auditer l'activité historique.

![Liste des shifts](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Comprendre les shifts POS

Un shift est une période de travail pendant laquelle un caissier utilise un terminal. Les shifts assurent la responsabilité du trésor—chaque caissier est responsable du trésor dans son tiroir pendant son shift.

**Cycle de vie d'un shift**:
1. **Ouverture** - Le caissier commence le shift, compte le trésor initial, enregistre le montant
2. **Pendant le shift** - Traite les ventes, accepte les paiements, émet des remboursements
3. **Fermeture** - Le caissier compte le trésor, enregistre le montant de fermeture, le système calcule l'écart
4. **Concilié** - Le shift est finalisé et verrouillé pour l'audit

**Métriques clés suivies**:
- **Trésor initial** - Montant de trésor dans le tiroir au début du shift
- **Trésor final** - Trésor physique dans le tiroir à la fin du shift
- **Trésor attendu** - Calculé : Trésor initial + ventes en espèces - remboursements en espèces + mouvements de trésor
- **Écart de trésor** - Écart : Trésor final - trésor attendu (positif = excédent, négatif = manque)
- **Total des ventes** - Somme de toutes les transactions de vente pendant le shift
- **Total des remboursements** - Somme de toutes les transactions de remboursement pendant le shift
- **Nombre de transactions** - Nombre de commandes traitées

## Vue de la liste des shifts

La liste des shifts affiche tous les shifts avec des informations clés:

**Statut du shift**:
- **Ouvert** (badge vert) - Shift actif
- **Fermé** (badge gris) - Shift terminé
- **Concilié** (badge bleu) - Finalisé et verrouillé pour l'audit

**Terminal** - Quel terminal POS le shift a été effectué

**Caissier** - Employé qui a travaillé le shift

**Trésor initial** - Montant initial de trésor

**Trésor final** - Montant final de trésor (vide si le shift est toujours ouvert)

**Trésor attendu** - Montant attendu calculé par le système en fonction des transactions

**Écart de trésor** - Écart (mis en surbrillance en rouge si négatif, vert si positif, noir si zéro)

**Durée** - Durée du shift (heure de début à heure de fin)

**Total des ventes** - Chiffre d'affaires généré pendant le shift

Utilisez des filtres pour afficher:
- Seulement les shifts ouverts (surveiller les terminaux actifs)
- Shifts avec des écarts (écart de trésor ≠ 0)
- Shifts par plage de dates (rapports de conciliation quotidienne)
- Shifts par caissier (audit de performance)

## Ouvrir un shift

Les caissiers ouvrent les shifts directement depuis le terminal POS (ne peut pas être ouvert depuis l'admin). Le workflow sur le terminal:

1. **Employé se connecte** - Entrez les identifiants pour accéder au terminal

2. **Compte le trésor initial** - Compte physiquement toutes les espèces dans le tiroir (billets et pièces)

3. **Entrez le montant initial** - Enregistrez le montant compté dans l'application POS

4. **Shift commence** - Le terminal est prêt à traiter les ventes

**Lignes directrices pour le trésor initial**:
- Le trésor initial standard (trésor de change) est généralement de 100 à 300 $ selon la taille du magasin
- Comptez deux fois pour garantir la précision—les erreurs d'ouverture se propagent aux écarts de fermeture
- Si le tiroir est vide, le trésor initial est de 0,00 $ (trésor de change ajouté via un mouvement de trésor)
- Documentez les billets de grande valeur (> 50 $) séparément pour suivre leur mouvement

![Formulaire d'ajout de shift](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Pendant le shift

Pendant que le shift est ouvert, le système suit automatiquement:

**Ventes en espèces** - Toute transaction où le client paie avec de l'argent physique (ajoute au trésor attendu)

**Remboursements en espèces** - Tout remboursement émis en espèces (soustrait du trésor attendu)

**Ventes par carte** - Transactions de carte de crédit/débit (aucun impact sur l'espèce)

**Paiement mixte** - Partie espèce + partie carte (seule la partie espèce affecte le trésor attendu)

**Cartes cadeaux et bons** - Méthodes de paiement non en espèce (aucun impact sur l'espèce)

Les caissiers continuent à traiter les ventes normalement. Le système maintient un calcul en cours du trésor attendu en arrière-plan.

## Mouvements de trésor

Les mouvements de trésor sont des ajustements du tiroir-caisse pendant un shift:

**Ajout de trésor** - Ajout d'espèces au tiroir:
- Raison : "Ajout de monnaie pour les billets de grande valeur"
- Montant : +100,00 $
- Le trésor attendu augmente de 100,00 $

**Retrait de trésor de poche** - Retrait d'espèces pour des dépenses:
- Raison : "Achat de fournitures de bureau"
- Montant : -25,00 $
- Le trésor attendu diminue de 25,00 $

**Dépôts bancaires** - Retrait d'excédent d'espèces pour la sécurité:
- Raison : "Dépôt sécurisé - plus de 500 $ dans le tiroir"
- Montant : -300,00 $
- Le trésor attendu diminue de 300,00 $

**Enregistrer les mouvements de trésor sur le terminal**:
1. Appuyez sur **Menu** > **Mouvement de trésor**
2. Sélectionnez le type : Ajouter ou Retirer
3. Entrez le montant
4. Entrez la raison (obligatoire pour le traçabilité d'audit)
5. Confirmez

Tous les mouvements de trésor apparaissent dans le rapport détaillé du shift avec des horodatages, des montants et des raisons.

## Fermer un shift

Quand un caissier termine sa période de travail, il ferme le shift:

1. **Appuyez sur Fermer le shift** - Dans le menu du terminal

2. **Traiter les transactions restantes** - Terminez les paniers en attente ou les ventes en suspens

3. **Compte le trésor final** - Compte physiquement toutes les espèces dans le tiroir
   - Compte les billets par dénomination (100 $, 50 $, 20 $, 10 $, 5 $, 1 $)
   - Compte les pièces par type (quartiers, dimes, nickels, pennies)
   - Total = montant final du trésor

4. **Entrez le montant final** - Enregistrez le total compté

5. **Le système calcule l'écart**:
   - Trésor attendu = Trésor initial + ventes en espèces - remboursements en espèces + mouvements de trésor
   - Écart de trésor = Trésor final - trésor attendu
   - Exemple : Trésor final 485,00 $ - Trésor attendu 480,00 $ = +5,00 $ excédent

6. **Revue de l'écart** - Le terminal affiche l'écart:
   - **Exact (0,00 $)** - Conciliation parfaite
   - **Petit excédent (+1 $ à +5 $)** - Arrondi acceptable ou pourboire client
   - **Petit manque (-1 $ à -5 $)** - Erreur de comptage mineure, acceptable
   - **Grand écart (> 5 $)** - Recomptage requis

7. **Recomptez si nécessaire** - Si l'écart est important (> 10 $), le caissier doit recompter le trésor final avant de finaliser

8. **Finaliser le shift** - Confirmez le montant final, le statut du shift change en "Fermé"

9. **Imprimer le rapport du shift** - Le terminal imprime un reçu de conciliation du trésor pour les archives du caissier

![Détail du shift](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Formule de conciliation du trésor

Le système calcule le trésor attendu en utilisant cette formule:

```
Trésor attendu = Trésor initial
                + Ventes en espèces
                - Remboursements en espèces
                + Ajouts de trésor (mouvements)
                - Retraits de trésor (mouvements)
```

**Exemple**:
- Trésor initial : 200,00 $
- Ventes en espèces : 450,00 $ (de 15 transactions)
- Remboursements en espèces : -30,00 $ (1 retour)
- Ajout de trésor : +100,00 $ (trésor ajouté pendant le shift)
- Retrait de trésor : -50,00 $ (retrait de trésor de poche)
- **Trésor attendu : 200 + 450 - 30 + 100 - 50 = 670,00 $**

Si le caissier compte 675,00 $ à la fermeture:
- Écart de trésor : 675,00 $ - 670,00 $ = **+5,00 $ excédent**

## Rapports et audit des shifts

Les rapports de shifts fournissent des informations détaillées sur la conciliation:

**Section résumé**:
- Trésor initial et final
- Calcul du trésor attendu
- Écart de trésor (excédent/manque)
- Total des ventes et remboursements
- Nombre de transactions
- Durée du shift

**Détail des transactions**:
- Toutes les ventes pendant le shift (IDs de commandes, montants, méthodes de paiement)
- Tous les remboursements émis
- Horodatage de chaque transaction

**Journal des mouvements de trésor**:
- Tous les ajouts et retraits
- Raisons fournies
- Horodatages

**Cas d'utilisation**:
- **Conciliation quotidienne** - Réviser tous les shifts à la fin de la journée commerciale
- **Performance des caissiers** - Identifier les motifs d'écarts par employé
- **Détection de vols** - Des manques importants et constants peuvent indiquer un vol
- **Besoins de formation** - Des écarts fréquents de petite taille suggèrent des problèmes de précision de comptage
- **Traçabilité d'audit** - Enregistrement complet pour les besoins comptables et fiscaux

## Gestion du trésor avec plusieurs terminaux

Pour les magasins avec plusieurs terminaux en cours de shifts simultanés:

**Tiroirs séparés** : Chaque terminal a son propre tiroir-caisse—les shifts sont indépendants. Le caissier A sur le Terminal 1 et le caissier B sur le Terminal 2 effectuent des shifts séparés avec des conciliations séparées.

**Tiroir partagé** : Certains magasins partagent un seul tiroir-caisse entre plusieurs terminaux (non recommandé). Si c'est le cas:
- Un seul shift peut être ouvert à la fois par tiroir partagé
- Les caissiers doivent fermer le shift lorsqu'ils passent à un autre caissier
- Les mouvements de trésor suivent tous les ajouts/retirs pendant les transferts
- Les écarts sont plus difficiles à attribuer à des caissiers spécifiques

**Meilleure pratique** : Un tiroir-caisse par terminal, un shift par caissier par session. Cela garantit une responsabilité claire et une conciliation simplifiée.

## Gestion des écarts

Lorsque le trésor final ne correspond pas au trésor attendu:

**Petits écarts (< 5 $)**:
- Acceptable en raison d'arrondis, d'erreurs de comptage ou de pourboires clients
- Documentez dans les notes du shift
- Aucune action supplémentaire nécessaire sauf si un motif émerge

**Écarts moyens (5 $ à 20 $)**:
- Recomptez le trésor avant de finaliser le shift
- Révisez le journal des transactions pour les erreurs (monnaie donnée incorrecte, transaction annulée non traitée)
- Documentez les circonstances dans les notes du shift
- Une révision par le manager est recommandée

**Écarts importants (> 20 $)**:
- Recomptage obligatoire
- Approbation du manager requise pour fermer le shift
- Révisez toutes les transactions et mouvements de trésor
- Investiguez les causes potentielles (vols, tap de caisse, montant initial de trésor incorrect)
- Peut nécessiter des sanctions selon les circonstances

**Manques constants**:
- Un motif de manque négatif répétitif du même caissier = problème de formation ou de vol
- Mettez en place une surveillance supplémentaire (vérification aléatoire par le manager pendant le shift)
- Révisez les procédures de formation POS
- Considérez des mises à jour des politiques de gestion du trésor

## Conseils

- **Comptez le trésor initial deux fois** - Les erreurs d'ouverture se propagent aux écarts de fermeture ; la précision au début empêche les problèmes à la fin
- **Enregistrez les mouvements de trésor immédiatement** - Ne tardez pas à documenter les ajouts de trésor ou les retraits de trésor de poche jusqu'à la fermeture
- **Fournissez toujours des raisons pour les mouvements** - "Ajout de 100 $" est inutile pour l'audit ; "Ajout de 100 $ pour la monnaie (manque de billets de 5 $)" est une action possible
- **Recomptez si l'écart > 10 $** - Ne finalisez pas le shift avec un grand écart sans recomptage
- **Imprimez les rapports de shift quotidiennement** - Attachez-les aux documents de conciliation quotidienne pour les comptes
- **Révisez les motifs, pas les écarts individuels** - Un manque de -3,00 $ est acceptable ; cinq manques consécutifs de -3,00 $ sont un problème
- **Fermez les shifts à la fin de la journée** - Ne laissez pas les shifts ouverts toute la nuit ; les écarts sont plus faciles à investiguer lorsqu'ils sont récents
- **Formez les caissiers au comptage par dénomination** - La plupart des erreurs proviennent d'un mauvais comptage des billets (penser qu'un 5 $ est un 10 $)
- **Utilisez des emballages de pièces** - Les pièces pré-emballées réduisent les erreurs de comptage et accélèrent la conciliation

