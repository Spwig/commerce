---
title: Combining Discounts
---

La plateforme propose quatre types de remises qui peuvent fonctionner ensemble : les ventes de produits, les promotions, les codes-cadeaux et les cartes-cadeaux. Comprendre comment elles interagissent vous aide à mener des campagnes efficaces sans résultats inattendus ou des remises doubles non souhaitées.

## Les Quatre Couches de Remises

Chaque type de remise fonctionne à un niveau différent et est visible par les clients de manière différente.

| Couche | Où l'appliquer | Comment l'appliquer | Visible par le client |
|-------|---------------|-----------------|-------------------|
| **Vente de produit** | Formulaire d'édition du produit > Section Vente | Modifie automatiquement le prix affiché | Oui — affiché comme un prix d'origine barré |
| **Promotion** | Marketing > Ventes et promotions | Appliquée automatiquement aux produits correspondants | Oui — affichée comme un prix de vente sur les cartes de produit |
| **Code-cadeaux** | Marketing > Codes-cadeaux | Le client entre un code à la caisse | Uniquement à la caisse après avoir entré le code |
| **Carte-cadeaux** | Appliquée à la caisse à partir du solde d'une carte-cadeaux | Réduit le montant total du paiement | Uniquement à la caisse |

## Comment Fonctionne la Priorité

Les promotions ont un champ **Priorité** qui accepte des valeurs de 0 et plus. Des nombres plus élevés signifient une priorité plus élevée.

Lorsque plusieurs promotions correspondent au même produit, celle avec la **priorité la plus élevée gagne**. Elles ne s'accumulent pas — seule une promotion s'applique par produit.

**Exemple :** « Vente flash 50 % de réduction » (priorité 10) et « Vente d'été 20 % de réduction » (priorité 5) ciblent tous les produits. Un client voit le prix de la vente flash de 50 %, et non 70 % combiné.

Au sein du même niveau de priorité, le système sélectionne la promotion qui offre la plus grande remise au client.

## Règles d'Empilement

Le tableau suivant montre les combinaisons de remises autorisées et comment les contrôler.

| Combinaison | Autorisé ? | Comment le contrôler |
|-------------|----------|-------------------|
| Vente de produit + Promotion | Seulement si activé | Cochez **« Empilable avec les ventes de produits »** dans les Paramètres avancés de la promotion |
| Promotion + Promotion | Non — la priorité la plus élevée gagne | Définissez des valeurs de priorité pour contrôler laquelle s'applique |
| Promotion + Code-cadeaux | Oui | La promotion réduit le prix du produit, le code-cadeaux réduit le total du panier séparément |
| Code-cadeaux + Code-cadeaux | Configurable | Le drapeau **« Ne peut pas être combiné avec d'autres codes-cadeaux »** du code-cadeaux contrôle cela (activé par défaut) |
| Code-cadeaux + Articles en promotion | Configurable | Le drapeau **« Exclure les articles en promotion »** du code-cadeaux contrôle cela |
| Carte-cadeaux + Toute remise | Oui — toujours | Les cartes-cadeaux sont appliquées en dernier, réduisant le montant final du paiement après toutes les autres remises |

## Scénarios Courants

### Scénario A : Promotion globale + code-cadeaux

- **Configuration :** 20 % de réduction sur tout (promotion) + le client a un code-cadeaux de 10 $
- **Résultat :** Un produit de 100 $ devient 80 $ (promotion), puis le code-cadeaux de 10 $ s'applique au total du panier. Le client paie **70 $**.

### Scénario B : Produit en promotion + promotion globale

- **Configuration :** Le produit a une vente de 30 % au niveau du produit + une promotion globale de 20 % existe
- **Résultat (empilement désactivé) :** Seule la vente du produit s'applique. Le client paie **70 $**.
- **Résultat (empilement activé) :** Les deux s'appliquent. 30 % de réduction en premier = 70 $, puis 20 % de réduction = **56 $**.

### Scénario C : Deux promotions sur le même produit

- **Configuration :** « Vente flash 40 % de réduction » (priorité 10) + « Vente d'été 20 % de réduction » (priorité 5), toutes deux ciblent tous les produits
- **Résultat :** La vente flash gagne car elle a une priorité plus élevée. Le client paie **60 $** sur un produit de 100 $.

### Scénario D : Code-cadeaux sur un article en promotion

- **Configuration :** Le produit est en promotion à 25 % de réduction. Le client entre un code-cadeaux de 10 % qui a l'option « Exclure les articles en promotion » activée.
- **Résultat :** Le code-cadeaux ne s'applique pas à ce produit. Si le panier contient des articles non en promotion, le code-cadeaux s'applique uniquement à ceux-ci.

## Quel Type de Remise Utiliser

| Objectif | Approche Recommandée | Pourquoi |
|------|---------------------|-----|
| Éliminer l'inventaire saisonnier | **Promotion** (ciblage par catégorie ou collection) | Automatique, aucun action du client nécessaire, visible sur les cartes de produit |
| Récompenser un client spécifique | **Code-cadeaux** (utilisation unique, limite par client) | Ciblé, traçable, semble personnel |
| Offre rapide pour un seul produit | **Vente de produit** (sur le formulaire d'édition du produit) | Le plus rapide à configurer, aucun besoin du wizard de promotion |
| Crédit ou cadeau | **Carte-cadeaux** | Basé sur le solde, le client gère son propre crédit |
| Événement global | **Promotion** (ciblage de tous les produits) | Portée maximale, une configuration couvre tout |
| Campagne de rachat | **Code-cadeaux** (restrictions pour clients nouveaux ou revenants) | Peut cibler des segments de clients spécifiques |

## Conseils

- **Testez avec un panier réel** — après avoir configuré les promotions et les codes-cadeaux, ajoutez des produits à un panier et passez à la caisse pour vérifier que les remises s'appliquent comme prévu.
- **Vérifiez le nombre de produits concernés** — dans l'étape de révision de la promotion, vérifiez que le nombre de produits concernés correspond à votre intention.
- **Utilisez la priorité de manière délibérée** — si vous exécutez plusieurs promotions en même temps, définissez toujours des valeurs de priorité différentes afin de contrôler laquelle gagne.
- **Désactivez l'empilement par défaut** — activez uniquement « Empilable avec les ventes de produits » lorsque vous souhaitez spécifiquement des remises doubles.
- **Documentez votre stratégie** — utilisez le champ Description de la promotion pour noter pourquoi une promotion existe et comment elle se rapporte aux autres promotions actives.