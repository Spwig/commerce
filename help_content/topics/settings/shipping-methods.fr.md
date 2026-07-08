---
title: Méthodes d'expédition
---

Les méthodes d'expédition sont les options d'expédition affichées aux clients lors de la validation de leur commande — chaque méthode calcule les coûts d'expédition en utilisant différentes stratégies de tarification. Spwig prend en charge 7 types de méthodes allant des tarifs plafonds simples à des tarifs en temps réel complexes calculés par les transporteurs. Les méthodes peuvent être restreintes par valeur minimale/maximale de commande, poids et zones géographiques. Les clients sélectionnent leur méthode préférée lors de la validation, et le coût calculé est ajouté au total de leur commande.

Utilisez ce guide pour configurer des méthodes d'expédition correspondant à votre modèle d'entreprise, allant des tarifs plafonds basiques à des tarifs hiérarchisés basés sur des zones sophistiqués.

## Types de méthodes d'expédition

Spwig propose 7 types de méthodes d'expédition, chacun avec une logique de calcul de coût différente:

### Expédition au tarif fixe

**Qu'est-ce que c'est** : Coût fixe indépendamment du contenu du panier, de la destination ou du poids.

**Quand l'utiliser**:
- Magasins simples avec des coûts d'expédition prévisibles
- Un seul type de produit (taille/poids similaires)
- Expédition nationale uniquement avec des tarifs standard des transporteurs
- Promotions de gratuité de l'expédition (utiliser avec les règles d'expédition)

**Configuration**:
- Définir **Type de méthode** = Tarif fixe
- Entrer **Coût fixe** (ex. $9.99)
- Optionnel : Définir des restrictions de valeur minimale/maximale de commande

**Exemple** : "Expédition standard - $9.99" pour toutes les commandes nationales.

---

### Expédition gratuite

**Qu'est-ce que c'est** : Option d'expédition gratuite (aucun coût pour le client).

**Quand l'utiliser**:
- Promotions d'expédition gratuite
- Commandes de haute valeur (combiner avec la valeur minimale de commande)
- Alternative de retrait local
- Avantages des programmes de fidélité

**Configuration**:
- Définir **Type de méthode** = Expédition gratuite
- Optionnel : Définir **Valeur minimale de commande** (ex. gratuite au-delà de $50)
- Fonctionne bien avec les règles d'expédition pour une expédition gratuite conditionnelle

**Exemple** : "Expédition gratuite pour les commandes de plus de $50" avec min_order_value = $50.

---

### Expédition basée sur le poids

**Qu'est-ce que c'est** : Coût calculé à partir d'une table de tarif hiérarchique basée sur le poids total du panier.

**Quand l'utiliser**:
- Produits avec des poids variables (livres, matériel, épicerie)
- Modèles de tarification des transporteurs basés sur le poids
- Rapport prévisible poids-coût

**Configuration**:
1. Définir **Type de méthode** = Basé sur le poids
2. Créer **Table de tarif d'expédition** avec basis_type = "weight"
3. Ajouter **Échelons de tarif d'expédition** (ex. 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Optionnel : Restreindre à des zones spécifiques

**Exemple**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Fonctionnement** : Le panier calcule le poids total → trouve l'échelon correspondant → retourne le taux de l'échelon.

---

### Expédition basée sur le prix

**Qu'est-ce que c'est** : Coût calculé à partir d'une table de tarif hiérarchique basée sur le sous-total du panier.

**Quand l'utiliser**:
- Coût d'expédition corrélé à la valeur de la commande
- Encourager des valeurs de panier plus élevées (taux plus bas par dollar aux échelons supérieurs)
- Alternative simple à l'expédition basée sur le poids pour des articles de prix similaire

**Configuration**:
1. Définir **Type de méthode** = Basé sur le prix
2. Créer **Table de tarif d'expédition** avec basis_type = "price"
3. Ajouter **Échelons de tarif d'expédition** (ex. $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Exemple**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratuit
```

**Fonctionnement** : Le panier calcule le sous-total → trouve l'échelon correspondant → retourne le taux de l'échelon.

---

### Tarifs en temps réel des transporteurs

**Qu'est-ce que c'est** : Tarifs en direct extraits des API des transporteurs (FedEx, UPS, DHL) lors de la validation.

**Quand l'utiliser**:
- Coûts d'expédition variables selon la destination
- Plusieurs options de transporteurs pour les clients
- Tarification précise des transporteurs sans tables de tarif manuelles
- Expédition internationale avec des tarifs complexes

**Configuration**:
1. Définir **Type de méthode** = En temps réel
2. Créer **Compte fournisseur** (Paramètres > Expédition > Comptes fournisseur)
3. Entrer les identifiants API du transporteur (numéro de compte, clé API, secret)
4. Lier le compte fournisseur à la méthode d'expédition
5. Optionnel : Ajouter un pourcentage de marge ou une marge fixe

**Exigences**:
- Compte actif du transporteur (FedEx, UPS, DHL, etc.)
- Identifiants API fournis par le transporteur
- Packages d'expédition définis (pour le calcul du poids dimensionnel)

**Exemple** : Méthode "FedEx Ground" qui récupère les tarifs en direct de FedEx basés sur le poids du panier, les dimensions et la destination lors de la validation.

**Fonctionnement**:
1. Le client entre son adresse lors de la validation
2. Le système appelle l'API du transporteur avec l'origine, la destination, les dimensions du colis et le poids
3. Le transporteur retourne une estimation de tarif
4. Marge optionnelle appliquée
5. Tarif affiché au client

---

### Retrait local

**Qu'est-ce que c'est** : Le client récupère sa commande à un emplacement physique (aucun coût d'expédition).

**Quand l'utiliser**:
- Magasins physiques proposant le retrait
- Options de retrait en entrepôt
- Événements ou marchés
- Éliminer les coûts d'expédition pour les clients locaux

**Configuration**:
1. Définir **Type de méthode** = Retrait local
2. Créer **Emplacement** (Paramètres > Expédition > Emplacements)
   - Définir l'adresse, les heures d'ouverture, la capacité de retrait
3. Lier l'emplacement(s) à la méthode
4. Optionnel : Définir le temps de préparation du retrait (ex. "Prêt en 2 heures")

**Expérience client**:
- Sélectionne "Retrait local" lors de la validation
- Choisis l'emplacement de retrait (si plusieurs)
- Choisis la date/heure de retrait en fonction de la disponibilité
- Recevra une notification lorsque la commande sera prête

**Exemple** : "Retrait au magasin - Gratuit" avec 3 emplacements de vente au détail, prêts dans les 24 heures.

---

### Expédition par tableau de tarifs

**Qu'est-ce que c'est** : Tarification hiérarchique flexible basée sur le poids, le prix ou la quantité avec une ciblage de zone avancé.

**Quand l'utiliser**:
- Tarification complexe (différents taux par zone ET poids)
- Besoin d'un contrôle plus important que les méthodes basées sur le poids ou le prix seules
- Plusieurs facteurs de tarification (ex. poids + destination + quantité)

**Configuration**:
1. Définir **Type de méthode** = Tableau de tarifs
2. Créer **Table de tarif d'expédition**
3. Définir **basis_type** : poids, prix ou quantité
4. Ajouter **Échelons de tarif d'expédition** avec des valeurs minimales/maximales
5. Optionnel : Restreindre les échelons à des zones ou pays spécifiques

**Différence par rapport aux méthodes basées sur le poids/prix** : Le tableau de tarifs prend en charge les restrictions géographiques par échelon, permettant des taux différents pour le même poids/prix dans différentes zones.

**Exemple**:
```
Zone A (Domestique):
  0-5kg: $10
  5-10kg: $15

Zone B (Zone éloignée):
  0-5kg: $18
  5-10kg: $25
```

**Fonctionnement** : Le panier calcule la valeur de base (poids/prix/quantité) → trouve l'échelon correspondant à la zone du client → retourne le taux de l'échelon.

---

## Configuration des méthodes d'expédition

Toutes les méthodes d'expédition partagent ces paramètres communs:

### Paramètres de base

- **Nom** : Identifiant interne (non affiché aux clients)
- **Nom d'affichage** : Nom affiché aux clients lors de la validation (ex. "Expédition standard", "Livraison express")
- **Description** : Texte d'aide optionnel affiché lors de la validation (ex. "Livraison en 3-5 jours ouvrés")
- **Type de méthode** : Un des 7 types ci-dessus
- **Actif** : Basculer pour activer/désactiver la méthode sans la supprimer

### Paramètres de coût

- **Coût fixe** : Uniquement pour les méthodes au tarif fixe
- **Table de tarif** : Pour les méthodes basées sur le poids, le prix ou le tableau de tarifs
- **Compte fournisseur** : Pour les méthodes en temps réel des transporteurs
- **Classe de taxe** : Appliquer la taxe sur le coût d'expédition (si applicable)

### Restrictions

**Restrictions de valeur de commande**:
- **Valeur minimale de commande** : Méthode uniquement disponible si le sous-total du panier ≥ montant (ex. expédition gratuite au-delà de $50)
- **Valeur maximale de commande** : Méthode cachée si le sous-total du panier > montant (ex. tarif fixe uniquement pour les commandes inférieures à $100)

**Restrictions de poids**:
- **Poids minimal** : Méthode uniquement disponible si le poids du panier ≥ montant
- **Poids maximal** : Méthode cachée si le poids du panier > montant (commun pour les options d'expédition léger)

**Restrictions géographiques**:
- **Zones d'expédition** : Lier la méthode à des zones spécifiques (domestique, internationale, régionale)
- Zones vides = disponible pour toutes les adresses
- Plusieurs zones = disponible pour toute zone correspondante

### Paramètres avancés

- **Priorité** : Ordre d'affichage lors de la validation (un nombre plus bas = plus haut dans la liste)
- **Frais de manutention** : Frais supplémentaires fixes ajoutés au coût calculé
- **Seuil d'expédition gratuite** : Coût automatiquement défini à $0 si le sous-total du panier ≥ seuil (alternative à min_order_value)

---

## Créer une méthode d'expédition

**Workflow étape par étape**:

1. **Naviguer vers les méthodes d'expédition**
   - Aller à Paramètres > Panier > Méthodes d'expédition
   - Cliquez sur "Ajouter une méthode d'expédition"

2. **Choisir le type de méthode**
   - Sélectionner le type approprié selon votre stratégie de tarification
   - Le type détermine les champs de configuration de coût disponibles

3. **Configurer les informations de base**
   - Nom : Référence interne (ex. "domestic_ground")
   - Nom d'affichage : Affiché aux clients (ex. "Expédition standard")
   - Description : Période de livraison (ex. "5-7 jours ouvrés")

4. **Définir le calcul des coûts**
   - **Tarif fixe** : Entrer le coût fixe
   - **Poids/Prix/Tableau de tarifs** : Créer une table de tarif (voir ci-dessous)
   - **En temps réel** : Lier le compte fournisseur
   - **Gratuit/Retrait** : Aucun paramètre de coût nécessaire

5. **Ajouter des restrictions (optionnel)**
   - Valeur minimale/maximale de commande
   - Poids minimal/maximal
   - Zones d'expédition

6. **Définir la priorité**
   - Les nombres plus bas apparaissent en premier lors de la validation
   - Ordre recommandé : Gratuit (1), Retrait local (2), Standard (3), Express (4)

7. **Activer la méthode**
   - Basculer "Actif" = Oui
   - Enregistrer

---

## Créer des tables de tarifs

Pour les méthodes basées sur le poids, le prix et le tableau de tarifs:

**Étape 1 : Créer une table de tarifs**
- Aller à Paramètres > Expédition > Tables de tarifs
- Cliquez sur "Ajouter une table de tarifs"
- Définir **Nom** (ex. "Échelons de poids domestiques")
- Définir **Type de base** : poids, prix ou quantité

**Étape 2 : Ajouter des échelons**
- Cliquez sur "Ajouter un échelon"
- Définir **Valeur minimale** et **Valeur maximale** (plage pour correspondre)
- Définir **Taux** (coût pour cet échelon)
- Optionnel : Restreindre à des zones ou pays spécifiques
- Enregistrer l'échelon

**Étape 3 : Répéter pour tous les échelons**
- Couvrir toute la plage (0 à la valeur maximale attendue)
- Assurer qu'il n'y a pas de lacunes (ex. 0-5, 5-10, 10-20, 20+)
- Utiliser `null` pour la valeur maximale dans l'échelon final (illimité)

**Étape 4 : Lier à la méthode d'expédition**
- Éditer la méthode d'expédition
- Sélectionner la table de tarif depuis le menu déroulant
- Enregistrer

**Exemple de table basée sur le poids**:
```
Nom : Échelons de poids domestiques
Type de base : Poids

Échelons:
1. Min : 0g, Max : 2000g, Taux : $8
2. Min : 2000g, Max : 5000g, Taux : $12
3. Min : 5000g, Max : 10000g, Taux : $18
4. Min : 10000g, Max : null, Taux : $25
```

---

## Scénarios d'expédition courants

### Scénario 1 : Expédition domestique de base

**Objectif** : Tarif fixe simple de $9.99 pour toutes les commandes domestiques.

**Solution**:
- Type de méthode : Tarif fixe
- Coût fixe : $9.99
- Zone d'expédition : "Domestique" (seulement votre pays)

---

### Scénario 2 : Expédition gratuite au-delà de $50

**Objectif** : Encourager des valeurs de panier plus élevées avec un seuil d'expédition gratuite.

**Solution Option A** (Recommandé):
- Type de méthode : Expédition gratuite
- Valeur minimale de commande : $50
- Nom d'affichage : "Expédition gratuite (Commandes $50+)")

**Solution Option B** (En utilisant des règles):
- Type de méthode : Tarif fixe
- Coût fixe : $9.99
- Créer une règle d'expédition:
  - Condition : Valeur du panier ≥ $50
  - Action : Définir le coût à $0

---

### Scénario 3 : Expédition basée sur le poids domestique + internationale

**Objectif** : Différents tarifs pour le domestique vs international basés sur le poids.

**Solution**:
1. Créer 2 zones : "Domestique", "International"
2. Créer 2 tables de tarifs : "Tarifs de poids domestique", "Tarifs de poids internationaux"
3. Créer 2 méthodes:
   - "Expédition domestique" → liée à la zone domestique + table de tarifs domestique
   - "Expédition internationale" → liée à la zone internationale + table de tarifs internationale

---

### Scénario 4 : Plusieurs options de transporteurs

**Objectif** : Permettre aux clients de choisir entre FedEx Ground, FedEx Express, UPS Ground.

**Solution**:
1. Créer un compte fournisseur pour l'API FedEx
2. Créer un compte fournisseur pour l'API UPS
3. Créer 3 méthodes en temps réel:
   - "FedEx Ground" → fournisseur FedEx, code de service = "FEDEX_GROUND"
   - "FedEx Express" → fournisseur FedEx, code de service = "FEDEX_EXPRESS"
   - "UPS Ground" → fournisseur UPS, code de service = "UPS_GROUND"
4. Les 3 méthodes interrogent les API des transporteurs lors de la validation et affichent les tarifs en direct

---

### Scénario 5 : Retrait local + livraison

**Objectif** : Un magasin de détail propose à la fois des options de retrait et de livraison.

**Solution**:
1. Créer un emplacement : "Magasin principal" avec adresse, heures, temps de préparation
2. Créer 2 méthodes:
   - "Retrait local" → type Retrait local, liée à l'emplacement principal
   - "Livraison standard" → tarif fixe $9.99
3. Les clients voient les deux options lors de la validation

---

## Tester les méthodes d'expédition

Avant de mettre en ligne, testez toutes les méthodes:

1. **Créer un panier de test**
   - Ajouter des produits avec différents poids/prix
   - Procéder à la validation

2. **Tester chaque méthode**
   - Entrer des adresses dans différentes zones
   - Vérifier que les méthodes correctes apparaissent
   - Vérifier que les coûts calculés correspondent aux attentes

3. **Tester les restrictions**
   - Ajouter des articles jusqu'à ce que la valeur minimale de commande soit atteinte → vérifier que l'expédition gratuite apparaît
   - Ajouter des articles lourds → vérifier que les échelons basés sur le poids fonctionnent
   - Tester les restrictions de zone → vérifier que les méthodes sont cachées pour les zones exclues

4. **Tester les méthodes en temps réel** (si applicable)
   - Utiliser les identifiants de test du fournisseur
   - Vérifier que les tarifs sont retournés avec succès
   - Vérifier la précision des tarifs par rapport au site web du transporteur

---

## Dépannage

**Problème 1 : Méthode non apparaissant lors de la validation**

**Causes**:
- Méthode inactive
- Panier ne répond pas aux restrictions de valeur minimale/maximale de commande
- Panier ne répond pas aux restrictions de poids minimal/maximal
- Adresse du client ne correspond à aucune zone liée
- Aucun échelon de table de tarif ne couvre le poids/prix du panier

**Solution** : Vérifier les restrictions, vérifier l'état actif, s'assurer que les zones/échelons couvrent le scénario du client.

---

**Problème 2 : Échec des tarifs en temps réel**

**Causes**:
- Identifiants API invalides
- Compte fournisseur inactif
- Aucun package d'expédition défini (le transporteur a besoin des dimensions)
- Adresse d'origine non définie
- API du transporteur hors service

**Solution** : Tester la connexion du fournisseur, vérifier les identifiants, s'assurer que les packages sont configurés, vérifier l'adresse d'origine dans les paramètres.

---

**Problème 3 : Coût calculé incorrect**

**Causes**:
- Échelons de table de tarif avec des lacunes ou des chevauchements
- Valeurs minimales/maximales des échelons dans les mauvaises unités (grammes vs kg)
- Frais de manutention ajoutés inattendument
- Règle d'expédition modifiant le coût

**Solution** : Vérifier les échelons de table de tarif, vérifier les unités, vérifier la priorité des règles d'expédition.

---

## Conseils

- **Commencez simple** - Utilisez un tarif fixe pour la première méthode, ajoutez la complexité si nécessaire
- **Testez en détail** - Vérifiez que toutes les méthodes fonctionnent en environnement de test avant d'activer en production
- **Utilisez des noms descriptifs** - "Expédition standard (5-7 jours)" est meilleur que "Méthode 1"
- **Fixez des délais de livraison réalistes** - Sous-estimez, surperformez pour la satisfaction client
- **Proposez le retrait si possible** - Réduit les coûts d'expédition, améliore la commodité client
- **Surveillez la fiabilité des API des transporteurs** - Ayez un tarif fixe en cas d'échec des tarifs en temps réel
- **Utilisez des zones pour l'international** - Différents taux par région évitent les pertes sur les destinations coûteuses
- **Combinez avec des règles d'expédition** - Les règles ajoutent une logique conditionnelle (promotions d'expédition gratuite, majorations pour les zones éloignées)
- **Limitez les méthodes** - 2-4 options à la validation évitent la paralysie de décision
- **Mettez à jour les tables de tarif saisonnièrement** - Les tarifs des transporteurs changent, vérifiez annuellement
- **Utilisez la priorité avec soin** - Placez les options gratuites/abordables en premier, les options coûteuses en dernier

Souvenez-vous : Conserver tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.