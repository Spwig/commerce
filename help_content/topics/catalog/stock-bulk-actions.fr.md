---
title: Actions de stock en vrac
---

Au-delà des ajustements individuels, Spwig vous propose trois actions en vrac sur la liste des **Articles de stock** pour les tâches de gestion du stock qui concernent plusieurs produits à la fois : déplacer le stock entre les entrepôts, comptabiliser les unités endommagées ou perdues, et reconcilier le stock après un inventaire physique. Les trois actions s'exécutent à partir du même menu déroulant **Actions**, appliquent la même quantité à chaque article de stock que vous sélectionnez, et sont pleinement enregistrées dans le journal de suivi des mouvements de stock.

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

![La liste des articles de stock avec la liste déroulante des actions en vrac ouverte, affichant le transfert de stock vers un entrepôt, l'enregistrement du stock endommagé/perdu et le recompte de stock (inventaire physique) aux côtés des autres actions](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

La même quantité que vous entrez est appliquée à **chaque** article sélectionné — ceci est conçu pour déplacer, écrire ou recompter le même nombre d'unités sur plusieurs références simultanément (par exemple, transférer 10 unités de plusieurs produits vers une nouvelle localisation de magasin). Pour un seul article avec une quantité différente, exécutez à nouveau l'action avec juste cet article sélectionné, ou utilisez **Ajuster les niveaux de stock** à la place.

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

**Seul le stock non réservé peut être transféré.** Spwig transfère à partir du *stock disponible* (en stock moins les unités allouées aux commandes ouvertes) — les unités déjà promises à une commande client restent dans l'entrepôt source afin que cette commande puisse toujours être exécutée. Si un article sélectionné n'a pas assez de stock disponible pour couvrir la quantité que vous avez entrée, cet article est ignoré et une erreur explique pourquoi ; le reste de la sélection est toujours transféré.

Si un article sélectionné est déjà stocké à l'entrepôt de destination que vous avez choisi, il est automatiquement ignoré (il n'y a rien à transférer vers soi-même), et vous verrez un message vous indiquant combien d'articles ont été ignorés pour cette raison.

Chaque transfert écrit un ensemble pair de mouvements dans le journal de suivi — une entrée négative **Transfert d'entrepôt** au point de départ et une entrée positive correspondante au point d'arrivée — ainsi, l'historique complet montre exactement d'où le stock vient et où il est allé.

## Enregistrer le stock endommagé/perdu

Utilisez-le pour écrire des unités qui sont cassées, abîmées ou manquantes — par exemple, après avoir trouvé des marchandises endommagées dans une livraison ou après avoir enquêté sur une incohérence.

Sur la page de confirmation, remplissez :

| Field | Description |
|-------|-------------|
| **Quantité à déduire (par article)** | Unités à retirer du stock en main propre pour chaque article sélectionné. |
| **Raison** | Note optionnelle, ex. "Dommage dû à l'eau pendant le stockage". |

Cliquez sur **Enregistrer la déduction** pour appliquer.

**Le stock réservé ne peut pas être déduit.** Le stock en main propre ne peut jamais descendre en dessous de la quantité actuellement allouée aux commandes ouvertes — Spwig bloque la déduction pour tout article dont la quantité que vous avez entrée risquerait de réduire le stock non réservé, vous empêchant ainsi de laisser accidentellement une commande payée sans stock pour la remplir. Si cela se produit pour un article, vous verrez un message d'erreur indiquant l'article et le nombre d'unités non réservées qu'il possède réellement disponibles pour déduire.

Chaque déduction est enregistrée en tant que mouvement **Dommage/Perte** pour cet article de stock, avec une quantité négative.

## Recompte du stock (compte physique)

Utilisez-le après un comptage physique du stock pour corriger les quantités en main propre afin qu'elles correspondent à celles que vous avez physiquement comptées — le moyen le plus rapide de reconcilier de nombreux articles après une vérification de stock ou un comptage cyclique.

Sur la page de confirmation, remplissez les éléments suivants :

| Field | Description |
|-------|-------------|
| **Quantité en stock comptée (par article)** | La quantité que vous avez physiquement comptée. Le stock en main propre est défini à ce nombre exact pour chaque article sélectionné — pas ajouté ou soustrait. |
| **Raison** | Note optionnelle, ex. "Comptage du stock du troisième trimestre". |

Cliquez sur **Appliquer le recompte** pour appliquer.

![Page de confirmation du recompte du stock : la carte des articles de stock sélectionnés et un formulaire des détails du recompte avec la quantité en stock comptée et une raison renseignées](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Contrairement aux deux autres actions, le recompte peut déplacer le stock dans les deux sens — vers le haut si vous avez compté plus que ce que le système s'attendait, vers le bas si vous avez compté moins. Si le compte que vous entrez est inférieur à la quantité actuellement allouée aux commandes ouvertes, Spwig l'applique tout de même (un compte est un fait, pas quelque chose à contester), mais la valeur **Disponible** de cet article affichera `0` sur la liste des stocks et son icône de statut passera à "En rupture de stock" — traitez cela comme un signal pour vérifier si les commandes affectées peuvent toujours être exécutées.

Chaque recompte est enregistré en tant que mouvement **Recompte physique**, avec la quantité montrant la correction (positive ou négative) entre les anciennes et nouvelles valeurs en main propre.

## Revoyez ce qui a changé

Chaque transfert, déduction et recompte est enregistré de la même manière qu'une autre modification du stock :

- Ouvrez un article de stock et faites défiler vers la section **Historique des mouvements de stock** pour voir son historique complet
- Ou naviguez vers **Produits > Historique des mouvements de stock** pour parcourir les mouvements sur tous les articles, filtrables par type

Chaque entrée enregistre le type de mouvement, la variation de quantité, les anciennes et nouvelles valeurs en main propre, la personne ayant effectué le changement, et la raison que vous avez entrée (le cas échéant) — ainsi, un transfert ou une déduction par lots est aussi traçable qu'une modification manuelle individuelle.

## Conseils

- Exécutez le **Recompte du stock** juste après un comptage physique du stock tandis que les chiffres comptés sont frais — c'est plus facile de repérer une erreur sur la page de confirmation que de s'y retrouver plus tard dans l'historique des mouvements.
- Remplissez toujours **Raison** pour les déductions et les recomptes. Six mois plus tard, "Dommage dû à l'eau pendant le stockage" est bien plus utile dans la traçabilité des audits qu'un champ vide.
- Avant de transférer du stock, vérifiez la colonne **Disponible** sur la page de confirmation — elle tient déjà compte des unités allouées, vous saurez donc immédiatement si une quantité est trop élevée pour l'un des articles que vous avez sélectionnés.
- Ces actions appliquent la même quantité à chaque article sélectionné. Regroupez vos sélections par des articles qui ont besoin de la même quantité déplacée, déduite ou recomptée, et traitez les exceptions un article à la fois.
- Si vous utilisez un point de vente dans un magasin de détail, n'oubliez pas que le stock tampon du entrepôt n'en fait pas partie de "disponible" pour les commandes en ligne — mais les transferts en vrac et les déductions fonctionnent toujours contre le total réel du stock en main propre de l'entrepôt.