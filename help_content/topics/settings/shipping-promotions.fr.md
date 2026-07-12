---
title: Promotions d'expédition
---

Les règles d'expédition appliquent des ajustements de coûts conditionnels aux méthodes d'expédition en fonction du contenu du panier, des attributs du client et des zones de livraison – offrir automatiquement une expédition gratuite au-delà de 50 $, ajouter des majorations pour les zones reculées ou réduire les frais d'expédition pour les clients VIP. Les règles utilisent une exécution basée sur la priorité (priorité plus élevée en premier) avec des drapeaux d'arrêt optionnels pour empêcher un traitement ultérieur. Chaque règle évalue plusieurs conditions (valeur du panier, poids, zones, produits, groupes de clients) et exécute l'une des 6 types d'ajustements lorsque toutes les conditions correspondent.

Utilisez les promotions d'expédition lorsque vous avez besoin de coûts d'expédition dynamiques qui changent en fonction du contexte de la commande, et non seulement des taux statiques provenant des méthodes d'expédition.

## Types de promotions d'expédition

Les règles d'expédition appliquent 6 types d'ajustements de coûts :

### Réduction en pourcentage

**Ce que cela fait** : Réduit le coût d'expédition en pourcentage (ex. : 25 % de réduction).

**Formule** : `nouveau_coût = coût_de_base × (1 - pourcentage/100)`

**Exemple** : 
```
Coût de base : 20 $
Réduction : 25 %
Résultat : 15 $
```

**Cas d'utilisation** : 
- Réduction pour clients VIP (20 % de réduction sur toutes les expéditions)
- Promotions saisonnières (15 % de réduction sur les expéditions en décembre)
- Réduction pour commandes en gros (10 % de réduction sur les expéditions pour 5+ articles)

---

### Réduction fixe

**Ce que cela fait** : Soustrait un montant fixe du coût d'expédition.

**Formule** : `nouveau_coût = coût_de_base - montant` (minimum 0 $)

**Exemple** : 
```
Coût de base : 15 $
Réduction : 5 $
Résultat : 10 $
```

**Cas d'utilisation** : 
- Bonus pour les premiers clients (5 $ de réduction sur la première commande d'expédition)
- Récompense pour l'inscription à la newsletter (3 $ de réduction sur l'expédition)
- Avantage du programme de fidélité (10 $ de réduction sur l'expédition par mois)

---

### Coût personnalisé

**Ce que cela fait** : Remplace le coût d'expédition par un montant spécifique.

**Formule** : `nouveau_coût = montant_fixe`

**Exemple** : 
```
Coût de base : 25 $
Défini à : 9,99 $
Résultat : 9,99 $
```

**Cas d'utilisation** : 
- Vente flash (expédition à 5 $ pour toutes les commandes aujourd'hui)
- Expédition spécifique à une catégorie (les livres ont toujours une expédition de 3,99 $)
- Promotions basées sur le temps (expédition limitée à 9,99 $ cette semaine)

---

### Expédition gratuite

**Ce que cela fait** : Fixe le coût d'expédition à 0 $.

**Formule** : `nouveau_coût = 0 $`

**Exemple** : 
```
Coût de base : 18 $
Règle s'applique
Résultat : 0 $
```

**Cas d'utilisation** : 
- Expédition gratuite au-delà de 50 $
- Expédition gratuite pour des produits spécifiques (articles promotionnels)
- Expédition gratuite pour les clients VIP
- Expédition gratuite pour les commandes avec 3+ articles

---

### Majoration (fixe)

**Ce que cela fait** : Ajoute un montant fixe au coût d'expédition.

**Formule** : `nouveau_coût = coût_de_base + montant`

**Exemple** : 
```
Coût de base : 12 $
Majoration : 5 $
Résultat : 17 $
```

**Cas d'utilisation** : 
- Frais de livraison pour des zones reculées
- Frais de manipulation pour des articles de grande taille
- Majoration pour la livraison le samedi
- Frais d'emballage pour des articles fragiles

---

### Majoration (en pourcentage)

**Ce que cela fait** : Augmente le coût d'expédition en pourcentage.

**Formule** : `nouveau_coût = coût_de_base × (1 + pourcentage/100)`

**Exemple** : 
```
Coût de base : 20 $
Majoration : 15 %
Résultat : 23 $
```

**Cas d'utilisation** : 
- Majoration de saison (20 % pendant les vacances)
- Majoration pour livraison express (majoration de 50 %)
- Majoration pour le carburant (variable selon les taux actuels)

---

## Conditions de promotion

Les promotions évaluent **Toutes les conditions doivent être remplies** pour que la règle s'applique :

### Validité temporelle

- **Date de début** : La règle est active uniquement après cette date
- **Date de fin** : La règle est active uniquement avant cette date
- **Cas d'utilisation** : Promotions saisonnières, offres limitées dans le temps

**Exemple** : Expédition gratuite uniquement le week-end de Black Friday
```
Début : 2026-11-27 00:00
Fin : 2026-11-30 23:59
```

---

### Plage de valeur du panier

- **Valeur minimale du panier** : La valeur totale du panier doit être ≥ montant
- **Valeur maximale du panier** : La valeur totale du panier doit être ≤ montant
- **Cas d'utilisation** : Seuils d'expédition gratuite, réductions en escalier

**Exemple** : Expédition gratuite pour les commandes de 50 $ à 200 $
```
Min : 50 $
Max : 200 $
```

---

### Plage de poids du panier

- **Poids minimum** : Le poids total du panier doit être ≥ montant
- **Poids maximum** : Le poids total du panier doit être ≤ montant
- **Cas d'utilisation** : Réductions pour les envois légers, majorations pour les articles lourds

**Exemple** : Majoration de 5 $ pour les commandes supérieures à 20 kg
```
Poids minimum : 20 kg
Poids maximum : null (illimité)
```

---

### Plage du nombre d'articles


- **Min Item Count** : Le panier doit contenir ≥ quantité d'articles
- **Max Item Count** : Le panier doit contenir ≤ quantité d'articles
- **Use Case** : Réductions pour commandes en lots, frais par article unique

**Exemple** : Livraison gratuite pour 5+ articles
```
Min Items: 5
Max Items: null
```

---

### Zone de livraison

- **Zones** : La règle s'applique uniquement si l'adresse du client correspond à au moins une zone sélectionnée
- **Empty selection** : La règle s'applique à TOUTES les zones
- **Use Case** : Surcoûts ou réductions spécifiques à une zone

**Exemple** : Livraison gratuite uniquement pour la zone nationale
```
Zones: ["Domestic USA"]
```

---

### Méthode de livraison

- **Methods** : La règle s'applique uniquement à des méthodes de livraison spécifiques
- **Empty selection** : La règle s'applique à TOUTES les méthodes
- **Use Case** : Promotions spécifiques à une méthode

**Exemple** : 25 % de réduction sur la livraison express
```
Methods: ["Express Delivery"]
```

---

### Exigences de produit

**Requires Products** : Le panier doit contenir au moins un de ces produits

**Requires Categories** : Le panier doit contenir au moins un produit de ces catégories

**Use Case** : Livraison gratuite spécifique à un produit, bundles promotionnels

**Exemple** : Livraison gratuite lorsque le panier contient « Item de promotion A »
```
Requires Products: [Product ID 123]
```

---

### Exclusions de produit

**Excludes Products** : La règle ne s'applique pas si le panier contient l'un de ces produits

**Excludes Categories** : La règle ne s'applique pas si le panier contient des produits de ces catégories

**Use Case** : Exclure les articles lourds/à grande dimension de la livraison gratuite

**Exemple** : Livraison gratuite sauf pour la catégorie meubles
```
Excludes Categories: [Furniture]
```

---

### Groupe de client

- **Customer Groups** : La règle s'applique uniquement aux clients appartenant aux groupes sélectionnés (VIP, Grossiste, etc.)
- **Empty selection** : La règle s'applique à TOUS les groupes de clients
- **Use Case** : Avantages VIP, réductions pour les grossistes

**Exemple** : Réduction de 15 % sur la livraison pour les membres VIP
```
Customer Groups: ["VIP"]
```

---

### Client novice

- **First Time Customer** : Basculer pour restreindre la règle aux clients sans commandes précédentes
- **Use Case** : Offres de bienvenue pour les nouveaux clients

**Exemple** : Réduction de 5 $ sur la livraison pour la première commande
```
First Time Customer: Yes
```

---

## Priorité et exécution des promotions

Les promotions s'exécutent dans l'**ordre de priorité** (numéro plus élevé = exécution plus tôt) :

### Mécanique de priorité

**Exécution d'exemple** : 
```
Promotion A (Priority 100) : Livraison gratuite si le panier > 50 $ 
Promotion B (Priority 50) : Réduction de 10 % sur toutes les livraisons 
Promotion C (Priority 1) : Surcoût de 2 $ pour les zones éloignées 

Panier : 60 $, zone éloignée 
Coût de livraison de base : 15 $ 

Étape 1 : Promotion A évalue (Priority 100) 
  Panier > 50 $? OUI 
  Appliquer : Définir le coût à 0 $ 
  Coût maintenant : 0 $ 

Étape 2 : Promotion B évalue (Priority 50) 
  Appliquer une réduction de 10 % sur 0 $ 
  Coût maintenant : 0 $ (toujours gratuit) 

Étape 3 : Promotion C évalue (Priority 1) 
  Ajouter un surcoût de 2 $ à 0 $ 
  Coût maintenant : 2 $ 

Coût final : 2 $ 
```

**Drapeau Arrêter les promotions suivantes** : 

Si la Promotion A a `stop_further_promotions = True` : 
```
Promotion A (Priority 100, stop_further_promotions=True) : Livraison gratuite si le panier > 50 $ 
Promotion B (Priority 50) : Réduction de 10 % 
Promotion C (Priority 1) : Surcoût de 2 $ 

Panier : 60 $ 
Coût de base : 15 $ 

Étape 1 : Promotion A s'applique, définit le coût à 0 $ 
        stop_further_promotions = True → STOP 

Coût final : 0 $ (les règles B et C ne s'exécutent jamais) 
```

---

## Créer des promotions de livraison

**Workflow étape par étape** : 

1. **Naviguez vers les règles** 
   - Paramètres > Livraison > Promotions de livraison 
   - Cliquez sur « Ajouter une promotion de livraison » 

2. **Configuration de base** 
   - **Name** : Identifiant interne (ex. : « Livraison gratuite au-delà de 50 $ ») 
   - **Description** : Notes facultatives (non affichées aux clients) 
   - **Active** : Basculer pour activer/désactiver 
   - **Priority** : Définir l'ordre d'exécution (100 pour une priorité élevée, 1 pour une priorité basse) 

3. **Choisir le type de promotion** 
   - Sélectionner le type d'ajustement (réduction %, réduction fixe, définir le coût, gratuit, surcoût %, surcoût fixe) 
   - Entrer le montant ou le pourcentage 


- Cochez "Stop Further Promotions" si cette règle doit empêcher les promotions de priorité inférieure d'être exécutées
- Utilisez pour les règles finales/absolues (par exemple, le livraison gratuite ne devrait pas avoir de frais supplémentaires ajoutés après)

paragraph

- Validité horaire : dates de début/fin
- Valeur du panier : min/max
- Poids du panier : min/max
- Nombre d'articles : min/max
- Zones : sélectionnez les zones applicables
- Méthodes : sélectionnez les méthodes applicables
- Produits : requis ou exclus
- Client : groupes ou uniquement pour les nouveaux clients

paragraph

- Cliquez sur Enregistrer
- La règle devient active immédiatement (si le commutateur Actif est sur Oui)

paragraph

## Scénarios courants de promotion d'expédition

heading

### Scénario 1 : Livraison gratuite au-delà de 50 $

heading

**Objectif** : Offrir une livraison gratuite lorsque le sous-total du panier est ≥ 50 $.

paragraph

**Configuration**

paragraph

```
Nom : Livraison gratuite au-delà de 50 $
Type : Livraison gratuite
Priorité : 100
Conditions : 
  Valeur minimale du panier : 50 $
Arrêter les promotions suivantes : Oui
```

code

### Scénario 2 : Surcoût pour zones reculées

heading

**Objectif** : Ajouter un surcoût de 10 $ pour les livraisons vers les zones reculées.

paragraph

```
Nom : Surcoût pour zones reculées
Type : Surcoût (Fixe)
Montant : 10 $
Priorité : 50
Conditions : 
  Zones : ["Zones reculées"]
Arrêter les promotions suivantes : Non
```

code

### Scénario 3 : Réduction de 20 % pour les clients VIP

heading

**Objectif** : Les clients VIP obtiennent une réduction de 20 % sur toutes les expéditions.

paragraph

```
Nom : Réduction d'expédition VIP
Type : Réduction (Pourcentage)
Pourcentage : 20
Priorité : 75
Conditions : 
  Groupes de clients : ["VIP"]
Arrêter les promotions suivantes : Non
```

code

### Scénario 4 : Tarif plat de Noël

heading

**Objectif** : Toutes les expéditions plafonnées à 9,99 $ pendant le mois de décembre.

paragraph

```
Nom : Promotion tarif plat décembre
Type : Remplacement du coût
Montant : 9,99 $
Priorité : 100
Conditions : 
  Date de début : 2026-12-01
  Date de fin : 2026-12-31
Arrêter les promotions suivantes : Oui
```

code

### Scénario 5 : Surcoût pour articles lourds

heading

**Objectif** : Ajouter un frais de 15 $ pour les commandes supérieures à 25 kg.

paragraph

```
Nom : Surcoût pour commandes lourdes
Type : Surcoût (Fixe)
Montant : 15 $
Priorité : 50
Conditions : 
  Poids minimum : 25 kg
Arrêter les promotions suivantes : Non
```

code

### Scénario 6 : Livraison gratuite pour la première commande

heading

**Objectif** : Les nouveaux clients obtiennent une livraison gratuite pour leur première commande.

paragraph

```
Nom : Livraison gratuite pour première commande
Type : Livraison gratuite
Priorité : 100
Conditions : 
  Client novice : Oui
Arrêter les promotions suivantes : Oui
```

code

### Scénario 7 : Livraison gratuite spécifique à une catégorie

heading

**Objectif** : Livraison gratuite pour les commandes contenant des articles de la catégorie promotionnelle.

paragraph

```
Nom : Livraison gratuite catégorie promotionnelle
Type : Livraison gratuite
Priorité : 90
Conditions : 
  Catégories requises : ["Promotions"]
Arrêter les promotions suivantes : Oui
```

code

### Scénario 8 : Exclure le mobilier de la livraison gratuite

heading

**Objectif** : Livraison gratuite au-delà de 50 $, sauf si le panier contient du mobilier.

paragraph

**Solution** : Deux règles

paragraph

**Promotion 1**

paragraph

```
Nom : Livraison gratuite générale
Type : Livraison gratuite
Priorité : 50
Conditions : 
  Valeur minimale du panier : 50 $
Exclut les catégories : ["Mobilier"]
Arrêter les promotions suivantes : Non
```

code

**Promotion 2**

paragraph

```
Nom : Réduction de 5 $ pour commandes de mobilier
Type : Réduction (Fixe)
Montant : 5 $
Priorité : 40
Conditions : 
  Catégories requises : ["Mobilier"]
Valeur minimale du panier : 50 $
Arrêter les promotions suivantes : Non
```

code

## Stratégies de combinaison de promotions

heading

### Stratégie 1 : Empiler les réductions

heading

**Permettre à plusieurs réductions de s'empiler**

paragraph

```
Promotion A (Priorité 100) : 10 % de réduction pour VIP → stop_further_promotions=Non
Promotion B (Priorité 50) : 15 % de réduction pour les commandes > 100 $ → stop_further_promotions=Non

Client VIP avec commande de 120 $ : 
Base : 15 $
Après la Promotion A : 13,50 $ (10 % de réduction)
Après la Promotion B : 11,48 $ (15 % de réduction sur 13,50 $)
```

code

### Stratégie 2 : Règles exclusives

heading

**Seule une règle s'applique** (priorité la plus élevée)

paragraph

```
Promotion A (Priorité 100) : Livraison gratuite > 50 $ → stop_further_promotions=Oui
Promotion B (Priorité 50) : 20 % de réduction sur toutes les expéditions → stop_further_promotions=Oui

Panier > 50 $ : 
Promotion A s'applique → Livraison gratuite → STOP
Promotion B ne s'exécute jamais
```

code

### Stratégie 3 : Surcoûts conditionnels

heading

**Remises en premier, majorations en dernier**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**Pour éviter cela, utilisez stop_further_promotions=Yes**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Promotions

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.