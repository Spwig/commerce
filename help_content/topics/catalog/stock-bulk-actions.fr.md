---
title: Actions de stock en vrac
---

Au-delà des ajustements individuels, Spwig vous propose trois actions en vrac sur la liste des **Articles de stock** pour les opérations de gestion des stocks qui concernent plusieurs produits à la fois : déplacer le stock entre les entrepôts, comptabiliser les unités endommagées ou perdues, et régler le stock après un inventaire physique. Les trois actions s'exécutent à partir du même menu déroulant **Actions**, appliquent la même quantité à chaque article de stock que vous sélectionnez, et sont pleinement enregistrées dans le journal de suivi des mouvements de stock.

Accédez à **Produits > Articles de stock** pour les utiliser.

## Exécution d'une action de stock en vrac

1. Sur la liste des **Articles de stock**, utilisez les filtres ou la recherche pour trouver les articles que vous souhaitez mettre à jour
2. Cochez la case à côté de chaque article de stock pour l'inclure (ou utilisez la case de la tête de liste pour sélectionner tous les articles de la page)
3. Choisissez l'une des trois actions dans le menu déroulant **Actions** : 
   - **Transférer le stock vers un entrepôt** 
   - **Enregistrer le stock endommagé/perdu** 
   - **Recompter le stock (inventaire physique)** 
4. Cliquez sur **Aller**
5. Consultez la page de confirmation — elle liste chaque article de stock sélectionné avec ses quantités **en stock**, **allouées** et **disponibles** actuelles afin que vous puissiez vérifier que vous avez sélectionné les bons articles
6. Remplissez les champs de l'action (voir ci-dessous) et cliquez sur le bouton de soumission pour appliquer

![La liste des articles de stock avec la liste déroulante des actions en vrac ouverte, affichant le transfert de stock vers un entrepôt, l'enregistrement du stock endommagé/perdu et le recompte de stock (inventaire physique) côte à côte avec les autres actions](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

La même quantité que vous entrez est appliquée à **chaque** article sélectionné — ceci est conçu pour déplacer, écrire ou recompter le même nombre d'unités sur plusieurs références à la fois (par exemple, transférer 10 unités de plusieurs produits vers une nouvelle localisation de magasin). Pour un seul article avec une quantité différente, exécutez à nouveau l'action avec juste cet article sélectionné, ou utilisez plutôt **Ajuster les niveaux de stock**.

## Transférer le stock vers un entrepôt

Utilisez-le pour déplacer le stock disponible de chaque article sélectionné de son entrepôt vers un autre entrepôt — par exemple, réapprovisionner un nouveau magasin de détail à partir de votre entrepôt principal, ou rééquilibrer le stock entre les centres de traitement régionaux.

Sur la page de confirmation, remplissez : 

| Champ | Description |
|-------|-------------|
| **Entrepôt de destination** | Où le stock doit être transféré. Seuls les entrepôts actifs apparaissent dans cette liste. |
| **Quantité par article** | Unités à transférer de l'entrepôt actuel de chaque article sélectionné. |
| **Raison** | Note optionnelle, par exemple « Réapprovisionnement du nouveau magasin d'Auckland ». |

Cliquez sur **Transférer le stock** pour appliquer.

![La page de confirmation du transfert de stock : une carte des articles de stock sélectionnés listant trois articles avec leurs chiffres en stock/attribués/disponibles, et un formulaire de détails de transfert avec un entrepôt de destination, une quantité et une raison remplis](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Seul le stock non réservé peut être transféré.** Spwig transfère à partir du **stock disponible** (en stock moins les unités allouées aux commandes ouvertes) — les unités déjà promises à une commande client restent dans l'entrepôt source afin que cette commande puisse toujours être exécutée. Si un article sélectionné n'a pas assez de stock disponible pour couvrir la quantité que vous avez entrée, cet article est ignoré et une erreur explique pourquoi ; le reste de la sélection est toujours transféré.

Si un article sélectionné est déjà stocké à l'entrepôt de destination que vous avez choisi, il est automatiquement ignoré (il n'y a rien à transférer vers soi-même), et vous verrez un message vous indiquant combien d'articles ont été ignorés pour cette raison.

Chaque transfert écrit un ensemble pair de mouvements dans le journal de suivi — une entrée négative **Transfert d'entrepôt** au point de départ et une entrée positive correspondante au point d'arrivée — ainsi, l'intégralité du journal montre exactement d'où le stock vient et où il est allé.

## Enregistrer le stock endommagé/perdu

Utilisez-le pour écrire des unités qui sont cassées, abîmées ou manquantes — par exemple, après avoir trouvé des marchandises endommagées dans une livraison ou après avoir enquêté sur une incohérence.

Sur la page de confirmation, remplissez :

| Champ | Description |
|-------|-------------|
| **Quantité à écrire (par article)** | Unités à retirer du stock disponible pour chaque article sélectionné. |
| **Raison** | Note facultative, par exemple « Dégâts des eaux pendant le stockage ». |

Cliquez sur **Enregistrer l'écriture** pour appliquer.

**Le stock réservé ne peut pas être écrit.** Le stock disponible ne peut jamais descendre en dessous de la quantité actuellement allouée aux commandes ouvertes — Spwig bloque l'écriture pour tout article où la quantité saisie empiéterait sur le stock alloué, afin d'éviter de laisser une commande payée sans le stock nécessaire pour l'expédier. Si cela se produit pour un article, vous verrez une erreur indiquant le nom de l'article et le nombre d'unités non réservées réellement disponibles pour l'écriture.

Chaque écriture est enregistrée comme un mouvement **Endommagé/Perdu** sur cet article de stock, avec une quantité négative.

## Recensement du stock (comptage physique)

Utilisez cette fonction après un comptage physique du stock pour corriger les quantités disponibles afin qu'elles correspondent à ce que vous avez réellement compté — c'est la méthode la plus rapide pour réconcilier de nombreux articles après un audit d'entrepôt ou un comptage cyclique.

Sur la page de confirmation, remplissez :

| Champ | Description |
|-------|-------------|
| **Quantité comptée disponible (par article)** | La quantité que vous avez comptée physiquement. Le stock disponible est fixé à ce nombre exact pour chaque article sélectionné — il n'est ni ajouté ni soustrait. |
| **Raison** | Note facultative, par exemple « Comptage de stock de l'entrepôt T3 ». |

Cliquez sur **Appliquer le recensement** pour appliquer.

![La page de confirmation du Recensement du stock : la carte Articles de stock sélectionnés et un formulaire Détails du recensement avec la quantité comptée disponible et une raison remplies](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Contrairement aux deux autres actions, le recensement peut faire varier le stock dans les deux sens — à la hausse si vous avez compté plus que ce que le système prévoyait, à la baisse si vous avez compté moins. Si le comptage saisi est inférieur à la quantité actuellement allouée aux commandes ouvertes, Spwig l'applique tout de même (un comptage est un fait, pas quelque chose avec lequel on peut discuter), mais la valeur **Disponible** de cet article s'affichera comme `0` dans la liste des stocks et son icône de statut passera à Rupture de stock — considérez cela comme un signal pour vérifier si les commandes affectées peuvent encore être expédiées.

Chaque recensement est enregistré comme un mouvement **Recensement physique**, avec la quantité indiquant la correction (positive ou négative) entre les anciennes et nouvelles valeurs du stock disponible.

## Examiner les modifications

Chaque transfert, écriture et recensement est journalisé de la même manière que tout autre changement de stock :

- Ouvrez un article de stock et faites défiler jusqu'à la section **Mouvements de stock** pour voir son historique complet
- Ou naviguez vers **Produits > Mouvements de stock** pour parcourir les mouvements de tous les articles, filtrables par type

Chaque entrée enregistre le type de mouvement, le changement de quantité, les valeurs précédentes et nouvelles du stock disponible, qui a effectué le changement, et la raison saisie (le cas échéant) — ainsi, un transfert ou une écriture en masse est aussi traçable qu'un ajustement manuel unique.

## Conseils

- Exécutez **Recensement du stock** juste après un comptage physique du stock, pendant que les chiffres comptés sont encore frais — il est plus facile de repérer une erreur de frappe sur la page de confirmation que de la démêler plus tard dans l'historique des mouvements.
- Remplissez toujours le champ **Raison** pour les écritures et les recensements. Dans six mois, « Dégâts des eaux pendant le stockage » sera bien plus utile dans la piste d'audit qu'un champ vide.
- Avant de transférer du stock, vérifiez la colonne **Disponible** sur la page de confirmation — elle tient déjà compte des unités allouées, vous saurez donc immédiatement si une quantité est trop élevée pour l'un des articles sélectionnés.

- Ces actions appliquent la même quantité à chaque article sélectionné. Regroupez votre sélection par articles qui ont réellement besoin de la même quantité déplacée, écrite ou recensée, et gérez les exceptions un article à la fois.
- Si vous utilisez un POS dans un point de vente au détail, rappelez-vous que le tampon de stock de l'entrepôt ne fait pas partie du « disponible » pour les commandes en ligne — mais les transferts et écritures en masse fonctionnent toujours sur la base du total réel du stock disponible de l'entrepôt.