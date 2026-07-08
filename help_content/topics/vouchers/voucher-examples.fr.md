---
title: Exemples de bons de réduction
---

Ce guide fournit des exemples concrets, champ par champ, pour les types de bons de réduction les plus courants. Chaque exemple montre exactement ce qu'il faut entrer lors de la création d'un bon de réduction à **Marketing > Vouchers** → **+ Ajouter un bon de réduction**.

![Voucher Card](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Exemple 1 : Pourcentage de réduction avec plafond

**Scénario :** Offrir 20 % de réduction sur l'ensemble du panier, mais limiter la réduction à 50 $ afin que les commandes de grande valeur restent rentables. Aucune date d'expiration.

| Champ | Valeur |
|-------|-------|
| Code | `SAVE20` |
| Nom | 20 % de réduction — Max 50 $ |
| Type de réduction | Pourcentage |
| Valeur de réduction | 20 |
| Montant maximum de réduction | 50 |
| Portée de l'application | Ensemble du panier |
| Nombre maximum d'utilisations total | *(vide — illimité)* |
| Nombre maximum d'utilisations par client | 1 |
| Valeur minimale de commande | *(vide — pas de minimum)* |

**Fonctionnement du plafond :** Pour un panier de 200 $, la réduction est de 40 $. Pour un panier de 300 $, elle serait de 60 $, mais le plafond la limite à 50 $. Pour un panier de 500 $, la réduction reste à 50 $. Cela vous permet de lancer une promotion qui semble généreuse tout en maintenant la réduction réelle prévisible.

## Exemple 2 : Réduction fixe avec minimum

**Scénario :** Donner 10 $ de réduction sur toute commande supérieure à 75 $ pour encourager des commandes plus importantes.

| Champ | Valeur |
|-------|-------|
| Code | `TAKE10` |
| Nom | 10 $ de réduction sur les commandes supérieures à 75 $ |
| Type de réduction | Montant fixe |
| Valeur de réduction | 10 |
| Portée de l'application | Ensemble du panier |
| Valeur minimale de commande | 75 |
| Nombre maximum d'utilisations par client | 0 *(illimité)* |
| Date de fin | *(vide — pas d'expiration)* |

> **Remarque :** Définir une valeur minimale de commande protège vos marges. Sans cela, un client pourrait utiliser ce code sur une commande de 12 $ et annuler ainsi votre profit. Associez toujours les bons de réduction à montant fixe à un minimum raisonnable.

## Exemple 3 : Livraison gratuite

**Scénario :** Offrir une livraison gratuite sur toute commande, sans minimum de dépense.

| Champ | Valeur |
|-------|-------|
| Code | `FREESHIP` |
| Nom | Livraison gratuite |
| Type de réduction | Livraison gratuite |
| Portée de l'application | Ensemble du panier |
| Nombre maximum d'utilisations total | *(vide — illimité)* |
| Nombre maximum d'utilisations par client | 1 |
| Valeur minimale de commande | *(vide — pas de minimum)* |

> **Remarque :** Sélectionnez le type de réduction **Livraison gratuite**, qui supprime automatiquement les frais de livraison de la commande. C'est l'approche la plus propre et fonctionne indépendamment de la méthode de livraison choisie par le client.

## Exemple 4 : Code de bienvenue pour les nouveaux clients

**Scénario :** Donner 15 % de réduction sur la première commande des nouveaux clients pour encourager la conversion.

| Champ | Valeur |
|-------|-------|
| Code | `WELCOME15` |
| Nom | Bienvenue — 15 % de réduction sur la première commande |
| Type de réduction | Pourcentage |
| Valeur de réduction | 15 |
| Portée de l'application | Ensemble du panier |
| Nombre maximum d'utilisations par client | 1 |
| Uniquement pour les nouveaux clients | Coché |

Le système vérifie le statut de nouveau client en vérifiant si le client a des commandes précédentes terminées. Si un client avec un historique de commandes tente d'appliquer ce code, il voit un message d'erreur clair à la caisse.

## Exemple 5 : Bon de réduction spécifique à un produit

**Scénario :** Offrir 5 $ de réduction sur des produits sélectionnés — par exemple, pour écouler des stocks lents.

| Champ | Valeur |
|-------|-------|
| Code | `PICK5` |
| Nom | 5 $ de réduction sur des articles sélectionnés |
| Type de réduction | Montant fixe |
| Valeur de réduction | 5 |
| Portée de l'application | Produits spécifiques |
| Produits éligibles | *(sélectionner les produits ciblés)* |
| Nombre maximum d'utilisations par client | 1 |

> **Remarque :** Utilisez la portée produit lorsque vous souhaitez réduire des SKU individuels. Utilisez la portée catégorie (exemple suivant) lorsque vous souhaitez réduire tout un département. La portée produit vous donne un contrôle précis ; la portée catégorie est plus facile à maintenir lorsque votre catalogue change fréquemment.

## Exemple 6 : Bon de réduction par catégorie

**Scénario :** Organiser une promotion de 25 % de réduction sur tous les articles de la catégorie Électronique.

| Champ | Valeur |
|-------|-------|
| Code | `ELEC25` |
| Nom | 25 % de réduction sur les produits électroniques |
| Type de réduction | Pourcentage |
| Valeur de réduction | 25 |
| Portée de l'application | Catégories spécifiques |
| Catégories éligibles | Électronique |
| Nombre maximum d'utilisations total | *(vide — illimité)* |
| Nombre maximum d'utilisations par client | 1 |


Lorsqu'elle est appliquée à une catégorie, la remise ne s'applique qu'aux articles éligibles du panier.

Les articles non électroniques sont facturés au prix plein.

## Comparaison des types de remise

| Type | Fonctionnement | Meilleur pour | Exemple |
|------|-------------|----------|---------|
| **Pourcentage** | Soustrait un pourcentage du total éligible | Des remises qui augmentent avec la taille de la commande | 20 % de réduction sur l'ensemble du panier |
| **Montant fixe** | Soustrait un montant fixe en dollars | Des promotions simples et prévisibles | 10 $ de réduction sur les commandes de plus de 75 $ |
| **Livraison gratuite** | Supprime les frais de livraison de la commande | Réduire l'abandon de panier à la caisse | Livraison gratuite, sans minimum |

## Comparaison des portées

| Portée | Fonctionnement | Meilleur pour |
|-------|-------------|----------|
| **Tout le panier** | La remise s'applique au total de la commande complète | Des promotions à l'échelle de l'ensemble du magasin et des codes de bienvenue |
| **Produits spécifiques** | La remise s'applique uniquement aux produits sélectionnés dans le panier | Pour vider un inventaire spécifique ou mettre en avant des offres |
| **Catégories spécifiques** | La remise s'applique uniquement aux articles des catégories sélectionnées | Des ventes par département et des promotions saisonnières |

## Conseils

- **Utilisez des codes mémorables** — `SUMMER20` est plus facile à retenir que `COUPONX1600406498`. Réservez les codes générés automatiquement pour les campagnes en masse.
- **Testez avant de distribuer** — Placez une commande de test avec le code promo pour vérifier qu'il s'applique correctement et respecte toutes les limites.
- **Suivez l'utilisation** — Vérifiez le compteur de rédemptions sur chaque carte de code promo pour suivre les performances des campagnes en temps réel.
- **Combinez avec la barre d'annonce** — Promouvez votre code promo dans une annonce sur l'ensemble du site pour que les clients le voient avant de commencer à acheter.