---
title: Actions en vrac sur les produits
---

La liste **Produits** vous permet d'agir sur plusieurs produits à la fois, sans ouvrir chacun individuellement. À partir de la case **Actions en vrac** dans la barre d'outils au-dessus de la grille de produits, vous pouvez publier ou ne pas publier des produits, les mettre en avant ou les retirer de la mise en avant, exporter les données vers un CSV, vérifier lesquels des produits sont prêts pour l'expédition internationale ou les supprimer - tout cela en une seule étape.

Accédez à **Produits > Tous les produits** pour utiliser ces actions.

![La barre d'outils de la liste des produits avec trois cartes de produits sélectionnées et la case **Actions en vrac** affichant toutes les options, y compris **Exporter les données douanières (CSV)** et **Vérifier la préparation pour l'expédition internationale**](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Exécution d'une action en vrac

1. Utilisez le panneau de filtre ou la case **Rechercher** pour réduire le nombre de produits que vous souhaitez, si nécessaire
2. Cochez la case en haut à gauche de chaque carte de produit que vous souhaitez inclure - la barre **Actions en vrac** affiche un comptage en temps réel du nombre de produits sélectionnés
3. Choisissez une action dans la case **Actions en vrac**
4. Cliquez sur **Appliquer**

Les actions qui modifient ou exportent des données s'exécutent immédiatement ; **Supprimer les produits sélectionnés** demande une confirmation d'abord, car c'est la seule action ici qui ne puisse pas être annulée facilement depuis la liste elle-même.

## Actions disponibles

| Action | Ce qu'elle fait |
|--------|------------------|
| **Marquer comme publié** | Définit le statut des produits sélectionnés sur **Publié**, afin qu'ils soient visibles sur le magasin. |
| **Marquer comme brouillon** | Définit le statut des produits sélectionnés sur **Brouillon**, les cachant du magasin pendant que vous continuez à les éditer. |
| **Marquer comme mis en avant** | Active **Est mis en avant** sur les produits sélectionnés. |
| **Supprimer la mise en avant** | Désactive **Est mis en avant** sur les produits sélectionnés. |
| **Exporter vers CSV** | Télécharge un CSV des ID, du nom, du SKU, du statut, du drapeau mis en avant et du prix des produits sélectionnés. |
| **Exporter les données douanières (CSV)** | Télécharge un CSV des informations douanières pour les produits sélectionnés. Voir ci-dessous. |
| **Vérifier la préparation pour l'expédition internationale** | Affiche un résumé de ceux des produits sélectionnés qui disposent des données douanières nécessaires pour les envois internationaux. Voir ci-dessous. |
| **Supprimer les produits sélectionnés** | Déplace les produits sélectionnés vers la corbeille, après une boîte de dialogue de confirmation. |

## Export des données douanières (CSV)

Utilisez-le lorsque vous avez besoin d'une feuille de déclaration douanière à remettre à un transporteur, à un coursier ou à un agent douanier - par exemple, avant un envoi international important, ou lors de la mise en place d'un nouveau transporteur qui demande les codes HS et les données d'origine en amont.

Sélectionnez les produits, choisissez **Exporter les données douanières (CSV)** depuis la case, puis cliquez sur **Appliquer**. Spwig télécharge un fichier nommé `product_customs_data.csv` avec une ligne par produit et les colonnes suivantes :

| Colonne | Source |
|--------|--------|
| **SKU** | Le SKU du produit |
| **Nom** | Le nom du produit |
| **Code HS** | Le code de classification du système harmonisé |
| **Pays d'origine** | Lieu de fabrication du produit |
| **Prix unitaire douanier** | La valeur déclarée par unité pour les douanes |
| **Autorisation d'exportation** | Le numéro d'autorisation d'exportation, si le produit en a besoin |
| **Date d'expiration de l'autorisation** | La date d'expiration de l'autorisation d'exportation, si elle est définie |
| **Prêt pour l'expédition internationale** | `Oui` ou `Non` - indique si le produit dispose des données minimales nécessaires pour l'expédition internationale (voir ci-dessous) |

Ces champs proviennent de la section **Expédition internationale / Douane** du formulaire de produit. Si un produit manque l'une de ces informations, la colonne correspondante reste vide dans l'exportation - remplissez les données manquantes sur le produit avant de vous fier à ce fichier pour un envoi réel.

## Vérifier la préparation pour l'expédition internationale

Utilisez-le pour auditer un lot de produits avant de commencer à les expédier à l'international, sans ouvrir chaque produit individuellement ou en attendant une exportation CSV complète.

Sélectionnez les produits, choisissez **Vérifier la préparation pour l'expédition internationale**, puis cliquez sur **Appliquer**. Spwig vérifie chaque produit sélectionné par rapport aux trois champs requis - **Code HS**, **Pays d'origine** et **Prix unitaire douanier** - et affiche une notification résumant le résultat :

- Si chaque produit sélectionné a les trois champs remplis, vous verrez une confirmation indiquant qu'ils sont tous prêts.
- Si certains manquent des données, la notification indique combien sont prêts et combien ne le sont pas, et liste chaque produit qui n'est pas prêt ainsi que les champs qu'il manque (par exemple, "Tasse en céramique bleue (manquant : hs_code, country_of_origin)").

Si plus de 10 produits manquent de données, la notification liste les 10 premiers et indique combien d'autres il y a.

Cette action ne lit que des données — elle ne modifie rien sur les produits, donc c'est sûr de l'exécuter aussi souvent que souhaité pendant que vous remplissez les informations douanières sur votre catalogue.

**Numéro de licence d'export** et **Date d'expiration de la licence d'export** ne font pas partie de la vérification de la prétention. Ils ne s'appliquent qu'aux articles contrôlés ou restreints, donc un produit peut être "prêt" pour l'expédition internationale sans eux.

## Conseils

- Exécutez **Vérifier la prétention à l'expédition internationale** sur l'ensemble de votre catalogue (ou une catégorie à la fois) avant votre première commande internationale — c'est beaucoup plus rapide que de découvrir un code HS manquant alors qu'un envoi est déjà à la frontière.
- Conservez **Exporter les données douanières (CSV)** pour les remettre aux courtiers et transporteurs, et **Vérifier la prétention à l'expédition internationale** pour votre propre liste de vérification — le CSV est un enregistrement, la vérification de la prétention est une liste de tâches.
- Remplissez les **Code HS**, **Pays d'origine** et **Prix unitaire douanier** sur le formulaire du produit (sous **Expédition internationale / Douane**) lorsque vous ajoutez de nouveaux produits, afin de ne pas devoir le faire en masse plus tard.
- La grille de produits charge plus de produits automatiquement lorsque vous faites défiler (défilement infini), et vos sélections de cases à cocher sont conservées lorsque de nouveaux produits s'affichent — vous pouvez donc faire défiler pour construire une sélection importante avant d'appliquer une action. Cependant, modifier un filtre ou recharger la page efface vos sélections, donc appliquez l'action avant d'ajuster les filtres.
- **Marquer comme brouillon** est un moyen rapide de retirer plusieurs produits du site en même temps — par exemple, avant un comptage de stock — sans modifier le reste de ceux-ci.
