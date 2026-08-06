---
title: Règles d'expédition
---

Les règles d'expédition appliquent des ajustements de coûts conditionnels aux méthodes d'expédition en fonction du contenu du panier, des attributs du client et des zones de livraison : offrez automatiquement une livraison gratuite au-delà de 50 $, ajoutez des frais supplémentaires pour les zones éloignées ou réduisez les frais d'expédition pour les clients VIP. Les règles utilisent une exécution basée sur la priorité (priorité élevée d'abord) avec des drapeaux de fin optionnels pour empêcher tout traitement ultérieur. Chaque règle évalue plusieurs conditions (valeur du panier, poids, zones, produits, groupes de clients) et exécute l'une des 6 sortes d'ajustements lorsqu'toutes les conditions correspondent.

Utilisez les règles d'expédition lorsque vous avez besoin de coûts d'expédition dynamiques qui changent en fonction du contexte de la commande, et non seulement des tarifs statiques provenant des méthodes d'expédition.

## Types de règles d'expédition

Les règles d'expédition appliquent 6 types d'ajustements de coûts :

### Réduction en pourcentage

**Ce qu'elle fait** : Réduit le coût d'expédition en pourcentage (par exemple, 25 % de réduction).

**Formule** : `nouveau_prix = prix_de_base × (1 - pourcentage/100)`

**Exemple** : 
```
Coût de base : 20 $ 
Remise : 25 % 
Résultat : 15 $ 
```

**Cas d'utilisation** : 
- Réduction pour les clients VIP (20 % de réduction sur l'expédition)
- Promotions saisonnières (15 % de réduction sur l'expédition en décembre)
- Réduction pour les commandes en vrac (10 % de réduction sur l'expédition pour 5+ articles)

---

### Remise fixe

**Ce qu'elle fait** : Soustrait un montant fixe du coût d'expédition.

**Formule** : `nouveau_prix = prix_de_base - montant` (minimum 0 $)

**Exemple** : 
```
Coût de base : 15 $ 
Remise : 5 $ 
Résultat : 10 $ 
```

**Cas d'utilisation** : 
- Bonus pour les nouveaux clients (5 $ de réduction sur l'expédition de la première commande)
- Récompense pour l'inscription à la newsletter (3 $ de réduction sur l'expédition)
- Avantage du programme de fidélité (10 $ de réduction sur l'expédition par mois)

---

### Coût fixe

**Ce qu'elle fait** : Remplace le coût d'expédition par un montant spécifique.

**Formule** : `nouveau_prix = montant_fixe`

**Exemple** : 
```
Coût de base : 25 $ 
Fixer à : 9,99 $ 
Résultat : 9,99 $ 
```

**Cas d'utilisation** : 
- Vente flash (frais d'expédition fixes de 5 $ pour toutes les commandes aujourd'hui)
- Frais d'expédition spécifiques aux catégories (toujours 3,99 $ d'expédition pour les livres)
- Promotions basées sur le temps (frais d'expédition plafonnés à 9,99 $ cette semaine)

---

### Expédition gratuite

**Ce qu'elle fait** : Fixe le coût d'expédition à 0 $.

**Formule** : `nouveau_prix = 0 $`

**Exemple** : 
```
Coût de base : 18 $ 
La règle s'applique 
Résultat : 0 $ 
```

**Cas d'utilisation** : 
- Expédition gratuite au-delà de 50 $
- Expédition gratuite pour des produits spécifiques (articles promotionnels)
- Expédition gratuite pour les clients VIP
- Expédition gratuite pour les commandes comprenant 3+ articles

---

### Surcharge (montant fixe)

**Ce qu'elle fait** : Ajoute un montant fixe au coût d'expédition.

**Formule** : `nouveau_prix = prix_de_base + montant`

**Exemple** : 
```
Coût de base : 12 $ 
Surcharge : 5 $ 
Résultat : 17 $ 
```

**Cas d'utilisation** : 
- Frais d'expédition pour les zones éloignées
- Frais de traitement pour articles volumineux
- Surcharge pour livraison le samedi
- Frais de conditionnement pour articles fragiles

---

### Surcharge (pourcentage)

**Ce qu'elle fait** : Augmente le coût d'expédition en pourcentage.

**Formule** : `nouveau_prix = prix_de_base × (1 + pourcentage/100)`

**Exemple** : 
```
Coût de base : 20 $ 
Surcharge : 15 % 
Résultat : 23 $ 
```

**Cas d'utilisation** : 
- Surcharge saisonnière (20 % pendant les fêtes)
- Prime pour livraison express (surcharge de 50 %)
- Frais de carburant (variable selon les taux en vigueur)

---

## Conditions des règles

Les règles évaluent **toutes les conditions doivent être remplies** pour que la règle s'applique : 

### Validité temporelle

- **Date de début** : La règle n'est active que après cette date
- **Date de fin** : La règle n'est active que avant cette date
- **Cas d'utilisation** : Promotions saisonnières, offres limitées

**Exemple** : Livraison gratuite le week-end de la Saint-Valentin uniquement
```
Début : 2026-11-27 00:00
Fin : 2026-11-30 23:59
```

---

### Plage de valeur du panier

- **Valeur minimale du panier** : Le montant total du panier doit être ≥ montant
- **Valeur maximale du panier** : Le montant total du panier doit être ≤ montant
- **Cas d'utilisation** : Seuils de livraison gratuite, remises par tranches

**Exemple** : Livraison gratuite pour les commandes de 50 $ à 200 $
```
Min : 50 $ 
Max : 200 $
```

---

### Plage de poids du panier

- **Poids minimal** : Le poids total du panier doit être ≥ montant
- **Poids maximal** : Le poids total du panier doit être ≤ montant
- **Cas d'utilisation** : Réduction pour envoi léger, surcharge pour articles lourds

**Exemple** : Surcharge de 5 $ pour les commandes de plus de 20 kg
```
Poids minimal : 20 kg 
Poids maximal : null (illimité)
```

---

### Plage de nombre d'articles


- **Min Item Count** : Le panier doit contenir ≥ quantité d'articles
- **Max Item Count** : Le panier doit contenir ≤ quantité d'articles
- **Cas d'utilisation** : Remises pour commandes en vrac, frais pour articles individuels

**Exemple** : Livraison gratuite pour 5+ articles
```
Min Items: 5
Max Items: null
```


### Zone de livraison

- **Zones** : La règle s'applique uniquement si l'adresse du client correspond à au moins une zone sélectionnée
- **Sélections vides** : La règle s'applique à TOUTES les zones
- **Cas d'utilisation** : Surcoûts ou remises spécifiques aux zones

**Exemple** : Livraison gratuite uniquement pour la zone locale
```
Zones: ["Domestic USA"]
```


### Mode de livraison

- **Méthodes** : La règle s'applique uniquement aux méthodes de livraison spécifiques
- **Sélections vides** : La règle s'applique à TOUTES les méthodes
- **Cas d'utilisation** : Promotions spécifiques aux méthodes

**Exemple** : -25 % sur la livraison express
```
Méthodes: ["Livraison express"]
```


### Exigences produits

**Produits requis** : Le panier doit contenir au moins l'un de ces produits

**Catégories requises** : Le panier doit contenir au moins un produit de ces catégories

**Cas d'utilisation** : Livraison gratuite spécifique aux produits, ensembles promotionnels

**Exemple** : Livraison gratuite si le panier contient "Produit promotionnel A"
```
Produits requis: [ID produit 123]
```


### Exclusions produits

**Produits exclus** : La règle ne s'applique pas si le panier contient l'un de ces produits

**Catégories exclues** : La règle ne s'applique pas si le panier contient des produits de ces catégories

**Cas d'utilisation** : Exclure les articles lourds/oversized de la livraison gratuite

**Exemple** : Livraison gratuite sauf pour la catégorie meubles
```
Catégories exclues: [Meubles]
```


### Groupe client

- **Groupes clients** : La règle s'applique uniquement aux clients appartenant aux groupes sélectionnés (VIP, Détail, etc.)
- **Sélections vides** : La règle s'applique à TOUTS les groupes clients
- **Cas d'utilisation** : Avantages VIP, remises en détail

**Exemple** : -15 % de réduction sur la livraison pour les membres VIP
```
Groupes clients: ["VIP"]
```


### Client pour la première fois

- **Client pour la première fois** : Activer le basculement pour restreindre la règle aux clients n'ayant pas de commandes précédentes
- **Cas d'utilisation** : Offres d'accueil pour nouveaux clients

**Exemple** : -5 $ sur la livraison pour la première commande
```
Client pour la première fois: Oui
```


## Priorité des règles et exécution

Les règles s'exécutent dans l'ordre de **priorité** (nombre plus élevé = exécution plus tôt) : 

### Mécanique de priorité

**Exécution exemple** : 
```
Règle A (Priorité 100) : Livraison gratuite si le panier > 50 $ 
Règle B (Priorité 50) : Réduction de 10 % sur l'ensemble des frais de livraison 
Règle C (Priorité 1) : Surcoût de 2 $ pour les zones éloignées 

Panier : 60 $, Zone éloignée 
Frais de livraison de base : 15 $ 

Étape 1 : Évaluation de la Règle A (Priorité 100) 
  Le panier > 50 $? OUI 
  Appliquer : Définir le coût sur 0 $ 
  Coût maintenant : 0 $ 

Étape 2 : Évaluation de la Règle B (Priorité 50) 
  Appliquer une réduction de 10 % sur 0 $ 
  Coût maintenant : 0 $ (toujours gratuit) 

Étape 3 : Évaluation de la Règle C (Priorité 1) 
  Ajouter un surcoût de 2 $ sur 0 $ 
  Coût maintenant : 2 $ 

Coût final : 2 $
```

**Drapeau pour arrêter les règles suivantes** : 

Si la Règle A a `stop_further_rules = True` : 
```
Règle A (Priorité 100, stop_further_rules=True) : Livraison gratuite si le panier > 50 $ 
Règle B (Priorité 50) : Réduction de 10 % sur l'ensemble des frais de livraison 
Règle C (Priorité 1) : Surcoût de 2 $ pour les zones éloignées 

Panier : 60 $ 
Base : 15 $ 

Étape 1 : Règle A s'applique, définit le coût à 0 $ 
        stop_further_rules = True → ARRET 

Coût final : 0 $ (Règles B et C ne s'exécutent jamais)
```


## Création des règles de livraison

**Processus étape par étape** : 

1. **Naviguer vers les règles** 
   - Paramètres > Livraison > Règles de livraison 
   - Cliquer sur "Ajouter une règle de livraison"

2. **Configuration de base** 
   - **Nom** : identifiant interne (ex. : "Livraison gratuite au-dessus de 50 $") 
   - **Description** : notes optionnelles (non visibles par les clients) 
   - **Actif** : basculer pour activer/désactiver 
   - **Priorité** : définir l'ordre d'exécution (100 pour une priorité élevée, 1 pour une priorité faible) 

3. **Choisir le type de règle** 
   - Sélectionner le type de modification (pourcentage de remise, montant fixe, coût fixe, gratuit, pourcentage de surcoût, montant fixe de surcoût) 
   - Entrer le montant ou le pourcentage 

4. **Définir le drapeau d'arrêt** (optionnel) 
   - Cocher "Arrêter les règles suivantes" si cette règle doit empêcher les règles à faible priorité de s'exécuter 
   - Utiliser pour les règles finales/absolues (ex. : la livraison gratuite ne devrait pas avoir de surcoûts ajoutés après)


5. **Définir les conditions** (Facultatif - laisser vide pour "appliquer toujours")
  - Validité temporelle : Dates de début et de fin
  - Valeur du panier : Min/Max
  - Poids du panier : Min/Max
  - Nombre d'articles : Min/Max
  - Zones : Sélectionner les zones applicables
  - Méthodes : Sélectionner les méthodes applicables
  - Produits : Requis ou exclus
  - Clients : Groupes ou uniquement les premières commandes

6. **Enregistrer la règle**
  - Cliquer sur Enregistrer
  - La règle devient active immédiatement (si le basculement actif est Oui)


## Cas courants de règles de livraison

### Cas 1 : Livraison gratuite au-dessus de 50 $ 

**Objectif** : Offrir la livraison gratuite lorsque le sous-total du panier est ≥ 50 $.

**Configuration** : 
```
Nom : Livraison gratuite au-dessus de 50 $ 
Type : Livraison gratuite 
Priorité : 100 
Conditions : 
  Valeur minimale du panier : 50 $ 
Arrêter les autres règles : Oui 
```


### Cas 2 : Surcharge pour zones reculées

**Objectif** : Ajouter une surcharge de 10 $ pour les livraisons vers les zones reculées.

**Configuration** : 
```
Nom : Surcharge pour zones reculées 
Type : Surcharge (Montant fixe) 
Montant : 10 $ 
Priorité : 50 
Conditions : 
  Zones : ["Zones reculées"] 
Arrêter les autres règles : Non 
```


### Cas 3 : Remise de 20 % pour les clients VIP

**Objectif** : Les clients VIP reçoivent une remise de 20 % sur toutes les livraisons.

**Configuration** : 
```
Nom : Remise de 20 % sur la livraison VIP 
Type : Remise (Pourcentage) 
Pourcentage : 20 
Priorité : 75 
Conditions : 
  Groupes de clients : ["VIP"] 
Arrêter les autres règles : Non 
```


### Cas 4 : Forfait de Noël

**Objectif** : Toutes les livraisons sont limitées à 9,99 $ pendant décembre.

**Configuration** : 
```
Nom : Offre Forfait de décembre 
Type : Coût fixe 
Montant : 9,99 $ 
Priorité : 100 
Conditions : 
  Date de début : 2026-12-01 
  Date de fin : 2026-12-31 
Arrêter les autres règles : Oui 
```


### Cas 5 : Surcharge pour articles lourds

**Objectif** : Ajouter une surcharge de 15 $ pour les commandes supérieures à 25 kg.

**Configuration** : 
```
Nom : Surcharge pour commande lourde 
Type : Surcharge (Montant fixe) 
Montant : 15 $ 
Priorité : 50 
Conditions : 
  Poids minimal : 25 kg 
Arrêter les autres règles : Non 
```


### Cas 6 : Livraison gratuite pour la première commande

**Objectif** : Les nouveaux clients reçoivent la livraison gratuite pour leur première commande.

**Configuration** : 
```
Nom : Livraison gratuite pour la première commande 
Type : Livraison gratuite 
Priorité : 100 
Conditions : 
  Client pour la première fois : Oui 
Arrêter les autres règles : Oui 
```


### Cas 7 : Livraison gratuite spécifique aux catégories

**Objectif** : Livraison gratuite pour les commandes contenant des articles de la catégorie promotionnelle.

**Configuration** : 
```
Nom : Livraison gratuite pour les catégories promotionnelles 
Type : Livraison gratuite 
Priorité : 90 
Conditions : 
  Catégories requises : ["Promotions"] 
Arrêter les autres règles : Oui 
```


### Cas 8 : Exclure les meubles de la livraison gratuite

**Objectif** : Livraison gratuite au-dessus de 50 $, sauf si le panier contient des meubles.

**Solution** : Deux règles

**Règle 1** : 
```
Nom : Livraison gratuite générale 
Type : Livraison gratuite 
Priorité : 50 
Conditions : 
  Valeur minimale du panier : 50 $ 
  Catégories exclues : ["Meubles"] 
Arrêter les autres règles : Non 
```

**Règle 2** : 
```
Nom : Remise de 5 $ pour les commandes de meubles 
Type : Remise (Montant fixe) 
Montant : 5 $ 
Priorité : 40 
Conditions : 
  Catégories requises : ["Meubles"] 
  Valeur minimale du panier : 50 $ 
Arrêter les autres règles : Non 
```


## Stratégies de combinaison de règles

### Stratégie 1 : Remises cumulatives

**Autoriser plusieurs remises à s'additionner** : 
```
Règle A (Priorité 100) : 10 % de réduction pour les VIP → stop_further_rules=Non 
Règle B (Priorité 50) : 15 % de réduction pour les commandes > 100 $ → stop_further_rules=Non 

Client VIP avec commande de 120 $ : 
Base : 15 $ 
Après Règle A : 13,50 $ (10 % de réduction) 
Après Règle B : 11,48 $ (15 % de réduction sur 13,50 $) 
```


### Stratégie 2 : Règles exclusives

**Une seule règle s'applique** (la plus haute priorité) : 
```
Règle A (Priorité 100) : Livraison gratuite > 50 $ → stop_further_rules=Oui 
Règle B (Priorité 50) : 20 % de réduction sur toutes les livraisons → stop_further_rules=Oui 

Panier > 50 $ : 
Règle A s'applique → Livraison gratuite → ARRÊT 
Règle B ne s'exécute jamais 
```


### Stratégie 3 : Surcharges conditionnelles

**Remises d'abord, surcharges en dernier** : 
```
Règle A (Priorité 100) : Livraison gratuite > 75 $ 
Règle B (Priorité 75) : 15 % de réduction VIP 
Règle C (Priorité 50) : 10 % de réduction générale 
Règle D (Priorité 25) : Surcharge de 5 $ pour zones reculées 
Règle E (Priorité 1) : Surcharge de 10 % pour carburant 

Commande : 80 $, zone reculée, client VIP 
Base : 20 $ 
A : 80 $ > 75 $ → Gratuit ($0) 
B : VIP → 15 % de réduction sur $0 = $0 
C : 10 % de réduction sur $0 = $0 
D : Zone reculée +5 $ = $5 
E : Carburant +10 % de $5 = $5,50 
```


Preserve all markdown formatting, image paths, code blocks, and technical terms.

Final : 5,50 $ (non gratuit en raison des frais supplémentaires)
```

**Pour éviter cela, utilisez stop_further_rules=Oui** : 
```
Règle A (Priorité 100, stop=Oui) : Livraison gratuite >75 $ 

Même commande : 
A : 80 $ > 75 $ → Gratuit (0 $) → ARRÊT 
Final : 0 $ (vraiment gratuit) 
```


## Tests des règles de livraison

**Avant de passer en production** : 

1. **Créer des paniers de test** 
   - Panier A : 25 $ (en dessous du seuil) 
   - Panier B : 55 $ (au-dessus du seuil) 
   - Panier C : 200 $ + zone reculée 
   - Panier D : Client VIP 

2. **Tester chaque règle** 
   - Passer à la caisse 
   - Vérifier que le coût de livraison correct s'affiche 
   - Vérifier l'ordre d'exécution des règles 

3. **Tester la résolution de priorité** 
   - Plusieurs règles correspondantes 
   - Vérifier que la priorité la plus élevée s'exécute d'abord 
   - Vérifier le comportement de stop_further_rules 

4. **Tester les cas limites** 
   - Valeur du panier exactement au seuil 
   - Plusieurs conditions correspondantes 
   - Règles en conflit 


## Dépannage

**Problème 1 : La règle n'est pas appliquée** 

**Causes** : 
- La règle est inactive 
- Une ou plusieurs conditions non remplies 
- Une règle de priorité plus élevée a défini stop_further_rules=Oui 
- La validité temporelle est en dehors de la date actuelle 

**Solution** : Réexaminez toutes les conditions, vérifiez la priorité, vérifiez l'état actif.


**Problème 2 : Montant de remise inattendu** 

**Causes** : 
- Plusieurs règles qui s'additionnent 
- Pourcentage appliqué à un coût déjà remis 
- Priorité de la règle incorrecte 

**Solution** : Vérifiez l-ordre des priorités, vérifiez les indicateurs stop_further_rules, effectuez un suivi manuel de l'exécution.


**Problème 3 : La livraison gratuite ne fonctionne pas** 

**Causes** : 
- Une règle de frais inférieure a ajouté un coût après la règle de livraison gratuite 
- Le panier ne répond pas au seuil minimum 
- Des produits exclus sont dans le panier 

**Solution** : Utilisez stop_further_rules=Oui sur la règle de livraison gratuite, vérifiez les conditions, vérifiez les exclusions.


## Conseils 

- **Utilisez une priorité élevée pour la livraison gratuite** - Une priorité de 100 assure qu'elle s'exécute avant les autres ajustements 
- **Définissez stop_further_rules pour les règles absolues** - La livraison gratuite devrait arrêter le traitement ultérieur 
- **Testez les combinaisons de règles** - Plusieurs règles peuvent interagir de manière inattendue 
- **Utilisez des noms explicites** - « Réduction VIP 20 % (Priorité 75) » est plus clair que « Règle 3 » 
- **Documentez la logique complexe** - Ajoutez des notes dans le champ de description 
- **Commencez par des règles simples** - Ajoutez de la complexité progressivement 
- **Surveillez les performances des règles** - Vérifiez si les règles sont utilisées ou causent de la confusion 
- **Évitez d'avoir trop de règles** - Trop de règles ralentissent la caisse, utilisez un maximum de 5 à 10 
- **Utilisez des zones pour la géographie** - Cela vaut mieux que plusieurs règles similaires par pays 
- **Combiner avec des méthodes** - Les règles + les méthodes fonctionnent ensemble pour des prix sophistiqués 
- **Fixez des plages horaires claires** - Ajoutez toujours des dates de fin pour les promotions 
- **Testez les cas limites** - Exactement 50 $, exactement 5 articles, etc.