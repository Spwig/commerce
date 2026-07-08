---
title: Exemples de promotions
---

Ce guide montre des exemples concrets de la manière dont configurer différents types de promotions. Chaque exemple inclut les valeurs exactes à entrer dans l'assistant de création de promotion afin que vous puissiez suivre ou les adapter à votre magasin.

![Carte de promotion](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Exemple : Pourcentage de réduction sur une catégorie

**Scénario :** 30 % de réduction sur toutes les chaussures pour la liquidation d'hiver.

Accédez à **Marketing > Ventes et promotions** et cliquez sur **+ Créer une promotion**. Entrez les valeurs suivantes à chaque étape de l'assistant :

| Étape | Champ | Valeur |
|-------|-------|-------|
| Basics | Nom | Liquidation d'hiver — 30 % de réduction sur les chaussures |
| Basics | Description | Liquidation de fin de saison pour tous les articles de chaussure |
| Basics | Actif | Coché |
| Réduction | Type | Pourcentage de réduction |
| Réduction | Valeur | 30 |
| Planification | Date de début | 15 janv. 2026 |
| Planification | Date de fin | 28 févr. 2026 |
| Produits | Appliquer à | Catégories |
| Produits | Sélectionné | Chaussures, Bottes, Sandales |

Cela crée une vente limitée dans le temps qui réduit automatiquement chaque produit des catégories sélectionnées. Un paire de bottes à 120 $ devient 84 $, et une paire de sandales à 60 $ devient 42 $.

## Exemple : Réduction fixe sur une collection

**Scénario :** 15 $ de réduction sur les articles de la collection Essentials d'été.

| Étape | Champ | Valeur |
|-------|-------|-------|
| Basics | Nom | Essentials d'été — 15 $ de réduction |
| Basics | Actif | Coché |
| Réduction | Type | Montant de réduction |
| Réduction | Valeur | 15,00 |
| Planification | Date de début | 1 juin 2026 |
| Planification | Date de fin | (vide — sans expiration) |
| Produits | Appliquer à | Collections |
| Produits | Sélectionné | Essentials d'été |

> **Note :** La réduction de 15 $ s'applique à chaque produit éligible individuellement. Un produit à 50 $ devient 35 $, un produit à 30 $ devient 15 $. Laisser la Date de fin vide signifie que la promotion fonctionne indéfiniment jusqu'à ce que vous la désactivez manuellement.

## Exemple : Prix de vente fixe pour la liquidation

**Scénario :** Fixer tous les articles de liquidation à 9,99 $.

| Étape | Champ | Valeur |
|-------|-------|-------|
| Basics | Nom | Liquidation finale — Tout à 9,99 $ |
| Basics | Actif | Coché |
| Réduction | Type | Prix de vente fixe |
| Réduction | Valeur | 9,99 |
| Planification | Date de début | (aujourd'hui) |
| Produits | Appliquer à | Collections |
| Produits | Sélectionné | Liquidation finale |

> **Note :** Le prix de vente fixe fixe le prix de vente exact, indépendamment du prix d'origine. Un article à 75 $ et un article à 25 $ deviennent tous les deux 9,99 $. Utilisez cela pour les rayons de liquidation ou les prix uniformes où vous souhaitez que chaque article soit au même point de prix.

![Promotion de catégorie](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Choisir le bon type de réduction

| Type | Fonctionnement | Meilleur pour | Exemple |
|------|-------------|----------|---------|
| **Pourcentage de réduction** | Réduit le prix d'un pourcentage | Ventes généralisées où les produits ont des prix variables | 20 % de réduction — 100 $ devient 80 $, 50 $ devient 40 $ |
| **Montant de réduction** | Soustrait un montant fixe en dollars | Promotions avec un message de réduction spécifique en dollars | 15 $ de réduction — 100 $ devient 85 $, 50 $ devient 35 $ |
| **Prix de vente fixe** | Fixe le prix de vente exact | Liquidation, prix uniformes, "tous à X $" | 9,99 $ — tous les articles deviennent 9,99 $ indépendamment du prix d'origine |

## Choisir la bonne cible

| Cible | Fonctionnement | Meilleur pour |
|--------|-------------|----------|
| **Tous les produits** | S'applique à tous les produits de votre magasin | Ventes généralisées, événements généralisés |
| **Catégories** | S'applique à tous les produits des catégories sélectionnées | Ventes par département, liquidations saisonnières par type |
| **Marques** | S'applique à tous les produits des marques sélectionnées | Partenariats de marque, événements spécifiques à une marque |
| **Collections** | S'applique à tous les produits des collections sélectionnées | Promotions ciblées, ventes thématiques |
| **Produits** | S'applique aux produits sélectionnés individuellement | Offres sélectionnées à la main, sélections limitées |

## Schémas de planification

Trois schémas courants pour configurer les plans de promotion :

| Schéma | Date de début | Date de fin | Cas d'utilisation |
|---------|-----------|----------|----------|
| **Immédiat, en cours** | Aujourd'hui | (vide) | Réductions de prix permanentes, ventes à long terme |
| **Plage de dates** | Date future | Date future | Événements saisonniers, ventes de fêtes |
| **Début futur, pas de fin** | Date future | (vide) | Nouveaux prix permanents qui commencent à une date spécifique |

Définir une Date de début à l'avenir crée une promotion planifiée. Elle apparaîtra dans l'onglet **Planifié** du tableau de bord des promotions et s'activera automatiquement lorsque la date arrivera. Laisser la Date de fin vide signifie que la promotion reste active jusqu'à ce que vous la désactiviez manuellement.

## Conseils

- **Utilisez des noms descriptifs** — Incluez la valeur de la réduction et la cible dans le nom (par exemple, "Été 20 % de réduction sur les chaussures") afin que vous puissiez rapidement identifier les promotions sur le tableau de bord.
- **Vérifiez le nombre de produits concernés** — L'étape Revue affiche combien de produits seront réduits. Si le nombre semble incorrect, revenez en arrière et vérifiez votre ciblage.
- **Commencez petit** — Si vous n'êtes pas sûr d'une réduction, commencez avec un pourcentage plus petit et augmentez-le si nécessaire.
- **Utilisez la réduction en montant pour le marketing** — "15 $ de réduction" est une économie concrète qui est facile à communiquer dans les publicités et les campagnes par courriel.
- **Utilisez la réduction en pourcentage pour l'équité** — Une réduction en pourcentage s'adapte au prix, offrant des économies proportionnelles à différents points de prix.