---
title: Règles d'expédition
---

Les règles d'expédition appliquent des ajustements de coûts conditionnels aux méthodes d'expédition en fonction du contenu du panier, des attributs du client et des zones de livraison — offrir automatiquement une livraison gratuite au-delà de 50 $, ajouter des majorations pour les zones éloignées, ou réduire les frais d'expédition pour les clients VIP. Les règles utilisent une exécution basée sur la priorité (priorité plus élevée en premier) avec des drapeaux d'arrêt optionnels pour empêcher un traitement ultérieur. Chaque règle évalue plusieurs conditions (valeur du panier, poids, zones, produits, groupes de clients) et exécute l'un des 6 types d'ajustements lorsque toutes les conditions correspondent.

Utilisez les règles d'expédition lorsque vous avez besoin de coûts d'expédition dynamiques qui changent en fonction du contexte de la commande, et non seulement des taux statiques provenant des méthodes d'expédition.

## Types de règles d'expédition

Les règles d'expédition appliquent 6 types d'ajustements de coûts :

### Réduction en pourcentage

**Ce que cela fait** : Réduit le coût d'expédition en pourcentage (ex. 25 % de réduction).

**Formule** : `nouveau_coût = coût_de_base × (1 - pourcentage/100)`

**Exemple** :
```
Coût de base : 20 $
Réduction : 25 %
Résultat : 15 $
```

**Cas d'utilisation** :
- Réduction pour clients VIP (20 % de réduction sur toutes les expéditions)
- Promotions saisonnières (15 % de réduction sur les expéditions en décembre)
- Réduction sur les commandes en lots (10 % de réduction sur les expéditions pour 5+ articles)

---

### Réduction fixe

**Ce que cela fait** : Soustrait un montant fixe du coût d'expédition.

**Formule** : `nouveau_coût = coût_de_base - montant` (minimum 0 $)

**Exemple** :
```
Coût de base : 15 $
Réduction : 5 $
Résultat : 10 $
```

**Cas d'utilisation** :
- Bonus pour les premiers clients (5 $ de réduction sur les frais d'expédition de la première commande)
- Récompense pour l'inscription à la newsletter (3 $ de réduction sur l'expédition)
- Avantage du programme de fidélité (10 $ de réduction sur l'expédition par mois)

---

### Coût fixe

**Ce que cela fait** : Remplace le coût d'expédition par un montant spécifique.

**Formule** : `nouveau_coût = montant_fixe`

**Exemple** :
```
Coût de base : 25 $
Fixé à : 9,99 $
Résultat : 9,99 $
```

**Cas d'utilisation** :
- Vente flash (expédition plate de 5 $ pour toutes les commandes aujourd'hui)
- Expédition spécifique à la catégorie (les livres ont toujours une expédition de 3,99 $)
- Promotions basées sur le temps (expédition plafonnée à 9,99 $ cette semaine)

---

### Expédition gratuite

**Ce que cela fait** : Fixe le coût d'expédition à 0 $.

**Formule** : `nouveau_coût = 0 $`

**Exemple** :
```
Coût de base : 18 $
Règle s'applique
Résultat : 0 $
```

**Cas d'utilisation** :
- Expédition gratuite au-delà de 50 $
- Expédition gratuite pour des produits spécifiques (articles promotionnels)
- Expédition gratuite pour les clients VIP
- Expédition gratuite pour les commandes avec 3+ articles

---

### Majoration (fixe)

**Ce que cela fait** : Ajoute un montant fixe au coût d'expédition.

**Formule** : `nouveau_coût = coût_de_base + montant`

**Exemple** :
```
Coût de base : 12 $
Majoration : 5 $
Résultat : 17 $
```

**Cas d'utilisation** :
- Frais de livraison pour les zones éloignées
- Frais de manipulation des articles de grande taille
- Majoration pour la livraison le samedi
- Frais d'emballage pour les articles fragiles

---

### Majoration (en pourcentage)

**Ce que cela fait** : Augmente le coût d'expédition en pourcentage.

**Formule** : `nouveau_coût = coût_de_base × (1 + pourcentage/100)`

**Exemple** :
```
Coût de base : 20 $
Majoration : 15 %
Résultat : 23 $
```

**Cas d'utilisation** :
- Majoration de saison (20 % pendant les vacances)
- Prime d'expédition express (majoration de 50 %)
- Majoration pour le carburant (variable selon les taux actuels)

---

## Conditions de règle

Les règles évaluent **Toutes les conditions doivent être remplies** pour que la règle s'applique :

### Validité temporelle

- **Date de début** : La règle n'est active que après cette date
- **Date de fin** : La règle n'est active que avant cette date
- **Cas d'utilisation** : Promotions saisonnières, offres limitées dans le temps

**Exemple** : Expédition gratuite uniquement le week-end de Black Friday
```
Date de début : 2026-11-27 00:00
Date de fin : 2026-11-30 23:59
```

---

### Plage de valeur du panier

- **Valeur minimale du panier** : Le sous-total du panier doit être ≥ montant
- **Valeur maximale du panier** : Le sous-total du panier doit être ≤ montant
- **Cas d'utilisation** : Seuil d'expédition gratuite, réductions en escalier

**Exemple** : Expédition gratuite pour les commandes de 50 $ à 200 $
```
Min : 50 $
Max : 200 $
```

---

### Plage de poids du panier

- **Poids minimum** : Le poids total du panier doit être ≥ montant
- **Poids maximum** : Le poids total du panier doit être ≤ montant
- **Cas d'utilisation** : Réductions pour les envois légers, majorations pour les articles lourds

**Exemple** : Majoration de 5 $ pour les commandes supérieures à 20 kg
```
Poids minimum : 20 kg
Poids maximum : null (illimité)
```

---

### Plage du nombre d'articles

- **Nombre minimum d'articles** : Le panier doit avoir ≥ quantité d'articles
- **Nombre maximum d'articles** : Le panier doit avoir ≤ quantité d'articles
- **Cas d'utilisation** : Réductions pour les commandes en lots, frais pour un seul article

**Exemple** : Expédition gratuite pour 5+ articles
```
Nombre minimum d'articles : 5
Nombre maximum d'articles : null
```

---

### Zone d'expédition

- **Zones** : La règle s'applique uniquement si l'adresse du client correspond à au moins une zone sélectionnée
- **Sélection vide** : La règle s'applique à toutes les zones
- **Cas d'utilisation** : Majorations ou réductions spécifiques à la zone

**Exemple** : Expédition gratuite uniquement pour la zone nationale
```
Zones : ["Domestic USA"]
```

---

### Méthode d'expédition

- **Méthodes** : La règle s'applique uniquement à des méthodes d'expédition spécifiques
- **Sélection vide** : La règle s'applique à toutes les méthodes
- **Cas d'utilisation** : Promotions spécifiques à la méthode

**Exemple** : 25 % de réduction sur l'expédition Express
```
Méthodes : ["Express Delivery"]
```

---

### Produits requis

**Produits requis** : Le panier doit contenir au moins un de ces produits

**Catégories requises** : Le panier doit contenir au moins un produit de ces catégories

**Cas d'utilisation** : Expédition gratuite spécifique aux produits, bundles promotionnels

**Exemple** : Expédition gratuite lorsque le panier contient « Article promotionnel A »
```
Produits requis : [ID de produit 123]
```

---

### Exclusions de produits

**Produits exclus** : La règle ne s'applique pas si le panier contient l'un de ces produits

**Catégories excluses** : La règle ne s'applique pas si le panier contient des produits de ces catégories

**Cas d'utilisation** : Exclure les articles lourds/à grande taille de l'expédition gratuite

**Exemple** : Expédition gratuite sauf pour la catégorie meubles
```
Catégories excluses : [Meubles]
```

---

### Groupe de clients

- **Groupes de clients** : La règle s'applique uniquement aux clients appartenant aux groupes sélectionnés (VIP, Grossiste, etc.)
- **Sélection vide** : La règle s'applique à tous les groupes de clients
- **Cas d'utilisation** : Avantages VIP, réductions pour les grossistes

**Exemple** : Réduction de 15 % sur l'expédition pour les membres VIP
```
Groupes de clients : ["VIP"]
```

---

### Client novice

- **Client novice** : Interrupteur pour restreindre la règle aux clients sans commandes précédentes
- **Cas d'utilisation** : Offres de bienvenue pour les nouveaux clients

**Exemple** : 5 $ de réduction sur l'expédition pour la première commande
```
Client novice : Oui
```

---

## Priorité et exécution des règles

Les règles s'exécutent dans **l'ordre de priorité** (numéro plus élevé = exécution plus tôt) :

### Mécanique de priorité

**Exécution d'exemple** :
```
Règle A (Priorité 100) : Expédition gratuite si le panier > 50 $
Règle B (Priorité 50) : Réduction de 10 % sur toutes les expéditions
Règle C (Priorité 1) : Majoration de 2 $ pour les zones éloignées

Panier : 60 $, zone éloignée
Coût d'expédition de base : 15 $

Étape 1 : Règle A évalue (Priorité 100)
  Panier > 50 $? OUI
  Appliquer : Fixer le coût à 0 $
  Coût maintenant : 0 $

Étape 2 : Règle B évalue (Priorité 50)
  Appliquer une réduction de 10 % à 0 $
  Coût maintenant : 0 $ (toujours gratuit)

Étape 3 : Règle C évalue (Priorité 1)
  Ajouter une majoration de 2 $ à 0 $
  Coût maintenant : 2 $

Coût final : 2 $
```

**Drapeau d'arrêt des règles supplémentaires** :

Si la Règle A a `stop_further_rules = True` :
```
Règle A (Priorité 100, stop_further_rules=True) : Expédition gratuite si le panier > 50 $
Règle B (Priorité 50) : Réduction de 10 %
Règle C (Priorité 1) : Majoration de 2 $ pour les zones éloignées

Panier : 60 $
Coût de base : 15 $

Étape 1 : Règle A s'applique, fixe le coût à 0 $
        stop_further_rules = True → STOP

Coût final : 0 $ (les règles B et C ne s'exécutent jamais)
```

---

## Création de règles d'expédition

**Workflow étape par étape** :

1. **Naviguez vers les règles**
   - Paramètres > Expédition > Règles d'expédition
   - Cliquez sur « Ajouter une règle d'expédition »

2. **Configuration de base**
   - **Nom** : Identifiant interne (ex. « Expédition gratuite au-delà de 50 $ »)
   - **Description** : Notes optionnelles (non affichées aux clients)
   - **Actif** : Interrupteur pour activer/désactiver
   - **Priorité** : Définir l'ordre d'exécution (100 pour une priorité élevée, 1 pour une priorité basse)

3. **Choisir le type de règle**
   - Sélectionner le type d'ajustement (réduction %, réduction fixe, coût fixe, gratuite, majoration %, majoration fixe)
   - Entrer le montant ou le pourcentage

4. **Définir le drapeau d'arrêt** (optionnel)
   - Cocher « Arrêter les règles supplémentaires » si cette règle doit empêcher l'exécution des règles de priorité plus basse
   - Utiliser pour les règles finales/absolues (ex. l'expédition gratuite ne devrait pas avoir de majorations ajoutées après)

5. **Définir les conditions** (optionnel - laisser vide pour « s'appliquer toujours »)
   - Validité temporelle : Dates de début/fin
   - Valeur du panier : Min/max
   - Poids du panier : Min/max
   - Nombre d'articles : Min/max
   - Zones : Sélectionner les zones applicables
   - Méthodes : Sélectionner les méthodes applicables
   - Produits : Produits requis ou exclus
   - Client : Groupes ou uniquement pour les clients nouveaux

6. **Enregistrer la règle**
   - Cliquez sur Enregistrer
   - La règle devient active immédiatement (si le commutateur Actif est sur Oui)

---

## Scénarios courants de règles d'expédition

### Scénario 1 : Expédition gratuite au-delà de 50 $

**Objectif** : Offrir une expédition gratuite lorsque le sous-total du panier ≥ 50 $.

**Configuration** :
```
Nom : Expédition gratuite au-delà de 50 $
Type : Expédition gratuite
Priorité : 100
Conditions :
  Valeur minimale du panier : 50 $
Arrêter les règles supplémentaires : Oui
```

---

### Scénario 2 : Majoration pour les zones éloignées

**Objectif** : Ajouter une majoration de 10 $ pour les livraisons vers les zones éloignées.

**Configuration** :
```
Nom : Majoration pour les zones éloignées
Type : Majoration (fixe)
Montant : 10 $
Priorité : 50
Conditions :
  Zones : ["Zones éloignées"]
Arrêter les règles supplémentaires : Non
```

---

### Scénario 3 : Réduction de 20 % pour les clients VIP

**Objectif** : Les clients VIP obtiennent 20 % de réduction sur toutes les expéditions.

**Configuration** :
```
Nom : Réduction d'expédition VIP
Type : Réduction (en pourcentage)
Pourcentage : 20
Priorité : 75
Conditions :
  Groupes de clients : ["VIP"]
Arrêter les règles supplémentaires : Non
```

---

### Scénario 4 : Tarif plat de décembre

**Objectif** : Toutes les expéditions plafonnées à 9,99 $ pendant le mois de décembre.

**Configuration** :
```
Nom : Promotion tarif plat décembre
Type : Coût fixe
Montant : 9,99 $
Priorité : 100
Conditions :
  Date de début : 2026-12-01
  Date de fin : 2026-12-31
Arrêter les règles supplémentaires : Oui
```

---

### Scénario 5 : Majoration pour les articles lourds

**Objectif** : Ajouter un frais de 15 $ pour les commandes supérieures à 25 kg.

**Configuration** :
```
Nom : Majoration pour les commandes lourdes
Type : Majoration (fixe)
Montant : 15 $
Priorité : 50
Conditions :
  Poids minimum : 25 kg
Arrêter les règles supplémentaires : Non
```

---

### Scénario 6 : Expédition gratuite pour la première commande

**Objectif** : Les nouveaux clients obtiennent une expédition gratuite pour leur première commande.

**Configuration** :
```
Nom : Expédition gratuite pour la première commande
Type : Expédition gratuite
Priorité : 100
Conditions :
  Client novice : Oui
Arrêter les règles supplémentaires : Oui
```

---

### Scénario 7 : Expédition gratuite pour les catégories promotionnelles

**Objectif** : Expédition gratuite pour les commandes contenant des articles de la catégorie promotionnelle.

**Configuration** :
```
Nom : Expédition gratuite pour la catégorie promotionnelle
Type : Expédition gratuite
Priorité : 90
Conditions :
  Catégories requises : ["Promotions"]
Arrêter les règles supplémentaires : Oui
```

---

### Scénario 8 : Exclure les meubles de l'expédition gratuite

**Objectif** : Expédition gratuite au-delà de 50 $, sauf si le panier contient des meubles.

**Solution** : Deux règles

**Règle 1** :
```
Nom : Expédition gratuite générale
Type : Expédition gratuite
Priorité : 50
Conditions :
  Valeur minimale du panier : 50 $
  Catégories excluses : ["Meubles"]
Arrêter les règles supplémentaires : Non
```

**Règle 2** :
```
Nom : Réduction de 5 $ pour les commandes de meubles
Type : Réduction (fixe)
Montant : 5 $
Priorité : 40
Conditions :
  Catégories requises : ["Meubles"]
  Valeur minimale du panier : 50 $
Arrêter les règles supplémentaires : Non
```

---

## Stratégies de combinaison de règles

### Stratégie 1 : Empiler les réductions

**Permettre à plusieurs réductions de s'empiler** :
```
Règle A (Priorité 100) : 10 % de réduction pour les VIP → stop_further_rules=Non
Règle B (Priorité 50) : 15 % de réduction sur les commandes > 100 $ → stop_further_rules=Non

Client VIP avec commande de 120 $ :
Coût de base : 15 $
Après la Règle A : 13,50 $ (10 % de réduction)
Après la Règle B : 11,48 $ (15 % de réduction sur 13,50 $)
```

### Stratégie 2 : Règles exclusives

**Seule une règle s'applique** (priorité la plus élevée) :
```
Règle A (Priorité 100) : Expédition gratuite > 50 $ → stop_further_rules=Oui
Règle B (Priorité 50) : 20 % de réduction sur toutes les expéditions → stop_further_rules=Oui

Panier > 50 $ :
Règle A s'applique → Expédition gratuite → STOP
Règle B ne s'exécute jamais
```

### Stratégie 3 : Majorations conditionnelles

**Réductions en premier, majorations en dernier** :
```
Règle A (Priorité 100) : Expédition gratuite > 75 $
Règle B (Priorité 75) : Réduction de 15 % pour les VIP
Règle C (Priorité 50) : Réduction de 10 % générale
Règle D (Priorité 25) : Majoration de 5 $ pour les zones éloignées
Règle E (Priorité 1) : Majoration de 10 % pour le carburant

Commande : 80 $, zone éloignée, client VIP
Coût de base : 20 $
A : 80 $ > 75 $ → Gratuit (0 $)
B : VIP → 15 % de réduction sur 0 $ = 0 $
C : 10 % de réduction sur 0 $ = 0 $
D : Zone éloignée +5 $ = 5 $
E : Carburant +10 % de 5 $ = 5,50 $

Résultat final : 5,50 $ (non gratuit en raison des majorations)
```

**Pour éviter cela, utilisez stop_further_rules=Oui** :
```
Règle A (Priorité 100, stop=Oui) : Expédition gratuite > 75 $

Même commande :
A : 80 $ > 75 $ → Gratuit (0 $) → STOP
Résultat final : 0 $ (vraiment gratuit)
```

---

## Test des règles d'expédition

**Avant de mettre en ligne** :

1. **Créer des paniers de test**
   - Panier A : 25 $ (en dessous du seuil)
   - Panier B : 55 $ (au dessus du seuil)
   - Panier C : 200 $ + zone éloignée
   - Panier D : client VIP

2. **Tester chaque règle**
   - Passer à la caisse
   - Vérifier le coût d'expédition affiché
   - Vérifier l'ordre d'exécution des règles

3. **Tester la résolution des priorités**
   - Plusieurs règles correspondantes
   - Vérifier que la règle de priorité la plus élevée s'exécute en premier
   - Vérifier le comportement de stop_further_rules

4. **Tester les cas limites**
   - Valeur du panier exactement au seuil
   - Plusieurs conditions correspondantes
   - Règles en conflit

---

## Dépannage

**Problème 1 : La règle ne s'applique pas**

**Causes** :
- La règle est inactive
- Une ou plusieurs conditions non remplies
- Une règle de priorité plus élevée a stop_further_rules=Oui
- Validité temporelle en dehors de la date actuelle

**Solution** : Vérifier toutes les conditions, vérifier la priorité, vérifier l'état actif.

---

**Problème 2 : Montant de réduction inattendu**

**Causes** :
- Plusieurs règles s'empilent
- Pourcentage appliqué à un coût déjà réduit
- Priorité de règle incorrecte

**Solution** : Vérifier l'ordre de priorité, vérifier les drapeaux stop_further_rules, tracer manuellement l'exécution.

---

**Problème 3 : Expédition gratuite ne fonctionne pas**

**Causes** :
- Une règle de majoration de priorité plus basse ajoute un coût après la règle d'expédition gratuite
- Le panier ne répond pas au seuil de valeur minimale
- Produits exclus dans le panier

**Solution** : Utiliser stop_further_rules=Oui sur la règle d'expédition gratuite, vérifier les conditions, vérifier les exclusions.

---

## Conseils

- **Utilisez une priorité élevée pour l'expédition gratuite** - Priorité 100 assure qu'elle s'exécute avant d'autres ajustements
- **Définissez stop_further_rules pour les règles absolues** - L'expédition gratuite doit arrêter le traitement ultérieur
- **Testez les combinaisons de règles** - Plusieurs règles peuvent interagir de manière inattendue
- **Utilisez des noms descriptifs** - « Réduction VIP de 20 % (Priorité 75) » est meilleur que « Règle 3 »
- **Documentez la logique complexe** - Ajoutez des notes dans le champ de description
- **Commencez par des règles simples** - Ajoutez progressivement de la complexité
- **Surveillez la performance des règles** - Vérifiez si les règles sont utilisées ou causent de la confusion
- **Évitez un nombre excessif de règles** - Trop de règles ralentissent le processus de paiement, utilisez 5 à 10 maximum
- **Utilisez les zones pour la géographie** - Meilleur que plusieurs règles similaires par pays
- **Combiner avec des méthodes** - Les règles + méthodes fonctionnent ensemble pour un tarif sophistiqué
- **Définissez des fenêtres temporelles claires** - Incluez toujours une date de fin pour les promotions
- **Testez les cas limites** - Exactement 50 $, exactement 5 articles, etc.