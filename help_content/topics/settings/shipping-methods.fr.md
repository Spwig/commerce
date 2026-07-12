---
title: Méthodes d'expédition
---

Les méthodes d'expédition sont les options d'expédition affichées aux clients lors du passage à la caisse — chaque méthode calcule les coûts d'expédition en utilisant différentes stratégies de tarification. Spwig prend en charge 7 types de méthodes, allant des tarifs plats simples à des tarifs en temps réel calculés par les transporteurs. Les méthodes peuvent être restreintes en fonction de la valeur minimale/maximale de la commande, du poids et des zones géographiques. Les clients sélectionnent leur méthode préférée lors du passage à la caisse, et le coût calculé est ajouté au total de leur commande.

Utilisez ce guide pour configurer des méthodes d'expédition correspondant à votre modèle d'entreprise, allant des tarifs plats de base à des tarifs hiérarchisés basés sur des zones complexes.

## Types de méthodes d'expédition

Spwig propose 7 types de méthodes d'expédition, chacun avec une logique de calcul des coûts différente:

### Expédition au tarif fixe

**Qu'est-ce que c'est** : Coût fixe, indépendamment du contenu du panier, de la destination ou du poids.

**Quand l'utiliser**:
- Magasins simples avec des coûts d'expédition prévisibles
- Un seul type de produit (taille/poids similaires)
- Expédition nationale uniquement avec des tarifs standard des transporteurs
- Promotions de livraison gratuite (à utiliser avec des promotions d'expédition)

**Configuration**:
- Définir **Type de méthode** = Tarif fixe
- Entrer **Coût fixe** (ex. 9,99 $)
- Optionnel : Définir des restrictions de valeur minimale/maximale de commande

**Exemple** : « Expédition standard - 9,99 $ » pour toutes les commandes nationales.

---

### Expédition gratuite

**Qu'est-ce que c'est** : Option d'expédition gratuite (aucun frais pour le client).

**Quand l'utiliser**:
- Promotions d'expédition gratuites
- Commandes de haute valeur (à combiner avec une valeur minimale de commande)
- Alternative de retrait local
- Avantages des programmes de fidélité

**Configuration**:
- Définir **Type de méthode** = Expédition gratuite
- Optionnel : Définir **Valeur minimale de commande** (ex. gratuite au-delà de 50 $)
- Fonctionne bien avec des promotions d'expédition pour une expédition gratuite conditionnelle

**Exemple** : « Expédition gratuite pour les commandes de plus de 50 $ » avec min_order_value = 50 $.

---

### Expédition basée sur le poids

**Qu'est-ce que c'est** : Coût calculé à partir d'une table de tarifs hiérarchique basée sur le poids total du panier.

**Quand l'utiliser**:
- Produits avec des poids variables (livres, matériel, épicerie)
- Modèles de tarification des transporteurs basés sur le poids
- Rapport prévisible poids-coût

**Configuration**:
1. Définir **Type de méthode** = Basé sur le poids
2. Créer **Table de tarifs d'expédition** avec basis_type = "weight"
3. Ajouter **Échelons de tarifs d'expédition** (ex. 0-5 kg = 10 $, 5-10 kg = 15 $, 10-20 kg = 25 $)
4. Optionnel : Restreindre à des zones spécifiques

**Exemple**:
```
0-2 kg : 8 $
2-5 kg : 12 $
5-10 kg : 18 $
10 kg+ : 25 $
```

**Fonctionnement** : Le panier calcule le poids total → trouve l'échelon correspondant → renvoie le taux de l'échelon.

---

### Expédition basée sur le prix

**Qu'est-ce que c'est** : Coût calculé à partir d'une table de tarifs hiérarchique basée sur le sous-total du panier.

**Quand l'utiliser**:
- Coût d'expédition corrélé à la valeur de la commande
- Encourager des valeurs de panier plus élevées (taux plus bas par dollar aux échelons supérieurs)
- Alternative simple à l'expédition basée sur le poids pour des articles de prix similaire

**Configuration**:
1. Définir **Type de méthode** = Basé sur le prix
2. Créer **Table de tarifs d'expédition** avec basis_type = "price"
3. Ajouter **Échelons de tarifs d'expédition** (ex. 0-50 $ = 9,99 $, 50-100 $ = 14,99 $, 100+ $ = 19,99 $)

**Exemple**:
```
0-25 $ : 6,99 $
25-75 $ : 9,99 $
75-150 $ : 12,99 $
150+ $ : Gratuit
```

**Fonctionnement** : Le panier calcule le sous-total → trouve l'échelon correspondant → renvoie le taux de l'échelon.

---

### Tarifs en temps réel des transporteurs

**Qu'est-ce que c'est** : Tarifs en direct extraits des API des transporteurs (FedEx, UPS, DHL) lors du passage à la caisse.

**Quand l'utiliser**:
- Coûts d'expédition variables selon la destination
- Plusieurs options de transporteurs pour les clients
- Tarification précise des transporteurs sans tables de tarifs manuelles
- Expédition internationale avec des tarifs complexes

**Configuration**:
1. Définir **Type de méthode** = En temps réel
2. Créer **Compte fournisseur** (Paramètres > Expédition > Comptes fournisseur)
3. Entrer les identifiants API du transporteur (numéro de compte, clé API, secret)
4. Lier le compte fournisseur à la méthode d'expédition
5. Optionnel : Ajouter un pourcentage de marge ou une marge fixe

**Exigences**:
- Compte actif chez le transporteur (FedEx, UPS, DHL, etc.)
- Identifiants API fournis par le transporteur
- Packages d'expédition définis (pour le calcul du poids dimensionnel)



**Exemple** : La méthode "FedEx Ground" récupère les tarifs FedEx en temps réel en fonction du poids du panier, des dimensions et de la destination à la caisse.

**Fonctionnement** : 
1. Le client entre son adresse à la caisse
2. Le système appelle l'API du transporteur avec l'origine, la destination, les dimensions du colis et le poids
3. Le transporteur renvoie une estimation du prix
4. Application éventuelle d'une marge
5. Le prix est affiché au client

---

### Retrait en magasin

**Qu'est-ce que c'est** : Le client récupère son commande en personne à un emplacement physique (aucun coût de livraison).

**Quand l'utiliser** : 
- Magasins de détail proposant le retrait en magasin
- Options de retrait en entrepôt
- Événements ou marchés
- Éliminer les frais de livraison pour les clients locaux

**Configuration** : 
1. Définir **Type de méthode** = Retrait en magasin
2. Créer **Emplacement** (Paramètres > Livraison > Emplacements)
   - Définir l'adresse, les heures d'ouverture, la capacité de retrait
3. Lier l'emplacement(s) à la méthode
4. Optionnel : Définir le temps de préparation du retrait (ex. : "Prêt dans 2 heures")

**Expérience client** : 
- Sélectionne "Retrait en magasin" à la caisse
- Choisis l'emplacement de retrait (si plusieurs)
- Sélectionne la date/heure de retrait selon la disponibilité
- Recevra une notification lorsque la commande sera prête

**Exemple** : "Retrait en magasin - Gratuit" avec 3 emplacements de vente au détail, prêt dans les 24 heures.

---

### Livraison par tarif de tableau

**Qu'est-ce que c'est** : Tarification flexible par paliers basée sur le poids, le prix ou la quantité avec une ciblage avancé des zones.

**Quand l'utiliser** : 
- Tarification complexe (différents tarifs par zone ET poids)
- Besoin d'un contrôle plus important que la tarification basée sur le poids ou le prix seul
- Plusieurs facteurs de tarification (ex. : poids + destination + quantité)

**Configuration** : 
1. Définir **Type de méthode** = Tarif de tableau
2. Créer **Tableau de tarif de livraison**
3. Définir **basis_type** : poids, prix ou quantité
4. Ajouter **Paliers de tarif de livraison** avec des valeurs min/max
5. Optionnel : Restreindre les paliers à des zones ou pays spécifiques

**Différence par rapport à la tarification basée sur le poids/prix** : Le tarif de tableau prend en charge les restrictions géographiques par palier, permettant des tarifs différents pour le même poids/prix dans différentes zones.

**Exemple** : 
```
Zone A (Domestique) : 
  0-5kg : $10
  5-10kg : $15

Zone B (Région éloignée) : 
  0-5kg : $18
  5-10kg : $25
```

**Fonctionnement** : Le panier calcule la valeur de base (poids/prix/quantité) → trouve le palier correspondant à la zone du client → renvoie le tarif du palier.

---

## Configuration des méthodes de livraison

Toutes les méthodes de livraison partagent ces paramètres communs : 

### Paramètres de base

- **Nom** : Identifiant interne (non affiché aux clients)
- **Nom d'affichage** : Nom affiché aux clients à la caisse (ex. : "Livraison standard", "Livraison express")
- **Description** : Texte d'aide optionnel affiché à la caisse (ex. : "Livraison en 3 à 5 jours ouvrés")
- **Type de méthode** : Un des 7 types ci-dessus
- **Actif** : Basculer pour activer/désactiver la méthode sans la supprimer

### Paramètres de coût

- **Coût fixe** : Pour les méthodes à tarif fixe uniquement
- **Tableau de tarif** : Pour les méthodes basées sur le poids, le prix ou le tarif de tableau
- **Compte fournisseur** : Pour les méthodes de livraison en temps réel avec les transporteurs
- **Classe de taxe** : Appliquer la taxe sur le coût de livraison (si applicable)

### Restrictions

**Restrictions liées à la valeur de la commande** : 
- **Valeur minimale de la commande** : La méthode n'est disponible que si le sous-total du panier est ≥ à un montant (ex. : livraison gratuite au-delà de 50 $)
- **Valeur maximale de la commande** : La méthode est cachée si le sous-total du panier > à un montant (ex. : tarif fixe uniquement pour les commandes inférieures à 100 $)

**Restrictions liées au poids** : 
- **Poids minimum** : La méthode n'est disponible que si le poids du panier ≥ à un montant
- **Poids maximum** : La méthode est cachée si le poids du panier > à un montant (fréquent pour les options de livraison léger)

**Restrictions géographiques** : 
- **Zones de livraison** : Lier la méthode à des zones spécifiques (nationale, internationale, régionale)
- Zones vides = disponible pour toutes les adresses
- Plusieurs zones = disponible pour toute zone correspondante

### Paramètres avancés

- **Priorité** : Ordre d'affichage à la caisse (un nombre plus bas = plus haut dans la liste)
- **Frais de manutention** : Frais supplémentaires ajoutés au coût calculé
- **Seuil de livraison gratuite** : Met automatiquement le coût à $0 si le sous-total du panier ≥ seuil (alternative à min_order_value)

---

## Créer une méthode de livraison

**Workflow étape par étape** : 

1. **Naviguer vers les méthodes de livraison**
   - Aller à Paramètres > Panier > Méthodes de livraison
   - Cliquez sur "Ajouter une méthode de livraison"


2. **Choisir le type de méthode**
   - Sélectionnez le type approprié en fonction de votre stratégie tarifaire
   - Le type détermine les champs de configuration des coûts disponibles

3. **Configurer les informations de base**
   - Nom : Référence interne (ex. : "domestic_ground")
   - Nom d'affichage : Destiné aux clients (ex. : "Livraison standard")
   - Description : Délai de livraison (ex. : "5 à 7 jours ouvrés")

4. **Définir le calcul des coûts**
   - **Tarif fixe** : Entrez un coût fixe
   - **Poids/Prix/Tableau des tarifs** : Créez un tableau de tarifs (voir ci-dessous)
   - **En temps réel** : Liez le compte du prestataire
   - **Gratuit/Retrait en magasin** : Aucune configuration de coût nécessaire

5. **Ajouter des restrictions (facultatif)**
   - Valeur minimale/maximale de commande
   - Poids minimal/maximal
   - Zones de livraison

6. **Définir la priorité**
   - Les nombres plus bas apparaissent en premier lors du paiement
   - Ordre recommandé : Gratuit (1), Retrait local (2), Standard (3), Express (4)

7. **Activer la méthode**
   - Basculer "Actif" = Oui
   - Enregistrer

---

## Créer des tableaux de tarifs

Pour les méthodes basées sur le poids, le prix et les tableaux de tarifs :

**Étape 1 : Créer un tableau de tarifs**
- Allez dans Paramètres > Livraison > Tableaux de tarifs
- Cliquez sur "Ajouter un tableau de tarifs"
- Définissez **Nom** (ex. : "Tranches de poids nationales")
- Définissez **Type de base** : poids, prix ou quantité

**Étape 2 : Ajouter des tranches**
- Cliquez sur "Ajouter une tranche"
- Définissez **Valeur minimale** et **Valeur maximale** (plage pour correspondre)
- Définissez **Tarif** (coût pour cette tranche)
- Optionnel : Restreindre à des zones ou des pays spécifiques
- Enregistrer la tranche

**Étape 3 : Répéter pour toutes les tranches**
- Couvrir toute la plage (0 à la valeur maximale attendue)
- Assurer qu'il n'y a pas de lacunes (ex. : 0-5, 5-10, 10-20, 20+)
- Utilisez `null` pour la valeur maximale dans la dernière tranche (illimité)

**Étape 4 : Lier à la méthode de livraison**
- Modifier la méthode de livraison
- Sélectionner le tableau de tarifs dans le menu déroulant
- Enregistrer

**Exemple de tableau basé sur le poids**:
```
Nom : Tranches de poids nationales
Base : Poids

Tranches :
1. Min : 0g, Max : 2000g, Tarif : $8
2. Min : 2000g, Max : 5000g, Tarif : $12
3. Min : 5000g, Max : 10000g, Tarif : $18
4. Min : 10000g, Max : null, Tarif : $25
```

---

## Scénarios de livraison courants

### Scénario 1 : Livraison nationale de base

**Objectif** : Tarif fixe de 9,99 $ pour toutes les commandes nationales.

**Solution**:
- Type de méthode : Tarif fixe
- Coût fixe : 9,99 $
- Zone de livraison : "Nationale" (votre pays uniquement)

---

### Scénario 2 : Livraison gratuite au-delà de 50 $ 

**Objectif** : Encourager des valeurs de panier plus élevées avec un seuil de livraison gratuite.

**Solution Option A** (Recommandée) : 
- Type de méthode : Livraison gratuite
- Valeur minimale de commande : 50 $
- Nom d'affichage : "Livraison gratuite (commandes de 50 $ +)"

**Solution Option B** (En utilisant des règles) : 
- Type de méthode : Tarif fixe
- Coût fixe : 9,99 $
- Créer une promotion de livraison : 
  - Condition : Valeur du panier ≥ 50 $
  - Action : Définir le coût à 0 $

---

### Scénario 3 : Livraison nationale et internationale basée sur le poids

**Objectif** : Différents tarifs pour les livraisons nationales et internationales basés sur le poids.

**Solution**:
1. Créer 2 zones : "Nationale", "Internationale"
2. Créer 2 tableaux de tarifs : "Poids nationaux", "Poids internationaux"
3. Créer 2 méthodes : 
   - "Livraison nationale" → liée à la zone nationale + tableau de tarifs nationaux
   - "Livraison internationale" → liée à la zone internationale + tableau de tarifs internationaux

---

### Scénario 4 : Plusieurs options de transport

**Objectif** : Permettre aux clients de choisir entre FedEx Ground, FedEx Express, UPS Ground.

**Solution**:
1. Créer un compte fournisseur pour l'API FedEx
2. Créer un compte fournisseur pour l'API UPS
3. Créer 3 méthodes en temps réel : 
   - "FedEx Ground" → fournisseur FedEx, code de service = "FEDEX_GROUND"
   - "FedEx Express" → fournisseur FedEx, code de service = "FEDEX_EXPRESS"
   - "UPS Ground" → fournisseur UPS, code de service = "UPS_GROUND"
4. Toutes les 3 méthodes interrogent les API des transporteurs lors du paiement et affichent les tarifs en temps réel

---

### Scénario 5 : Retrait local + livraison

**Objectif** : Un magasin de détail propose à la fois des options de retrait et de livraison.

**Solution**:
1. Créer un emplacement : "Magasin principal" avec adresse, horaires et temps de préparation
2. Créer 2 méthodes : 
   - "Retrait local" → type de retrait local, lié à l'emplacement du magasin principal
   - "Livraison standard" → tarif fixe de 9,99 $
3. Les clients voient les deux options lors du paiement

---

## Tester les méthodes de livraison

Avant de lancer, testez toutes les méthodes :

1. **Créer un panier de test**
   - Ajouter des produits avec des poids/prix variés
   - Passer à la caisse

2. **Tester chaque méthode**
   - Entrer des adresses dans différentes zones
   - Vérifier que les méthodes correctes apparaissent
   - Vérifier que les coûts calculés correspondent aux attentes

3. **Tester les restrictions**
   - Ajouter des articles jusqu'à ce que la valeur minimale de commande soit atteinte → vérifier que l'expédition gratuite apparaît
   - Ajouter des articles lourds → vérifier que les paliers basés sur le poids fonctionnent
   - Tester les restrictions de zone → vérifier que les méthodes sont masquées pour les zones exclues

4. **Tester les méthodes en temps réel** (si applicable)
   - Utiliser les identifiants de test du transporteur
   - Vérifier que les tarifs sont retournés avec succès
   - Vérifier la précision des tarifs par rapport au site du transporteur

---

## Dépannage

**Problème 1 : Méthode non affichée à la caisse**

**Causes**:
- Méthode inactive
- Panier ne respecte pas la valeur minimale/maximale de commande
- Panier ne respecte pas le poids minimal/maximal
- Adresse client ne correspond à aucune zone liée
- Aucun palier de tableau de tarifs ne couvre le poids/prix du panier

**Solution** : Vérifier les restrictions, vérifier le statut actif, s'assurer que les zones/paliers couvrent le scénario du client.

---

**Problème 2 : Échec des tarifs en temps réel**

**Causes**:
- Identifiants API invalides
- Compte fournisseur inactif
- Aucun colis d'expédition défini (le transporteur a besoin des dimensions)
- Adresse d'origine non définie
- API du transporteur hors service

**Solution** : Tester la connexion au fournisseur, vérifier les identifiants, s'assurer que les colis sont configurés, vérifier l'adresse d'origine dans les paramètres.

---

**Problème 3 : Coût calculé incorrect**

**Causes**:
- Paliers de tableau de tarifs avec des écarts ou des chevauchements
- Valeurs min/max des paliers dans les unités incorrectes (grammes vs kg)
- Frais de manutention ajoutés de façon inattendue
- Règle d'expédition modifiant le coût

**Solution** : Vérifier les paliers du tableau de tarifs, vérifier les unités, vérifier la priorité des promotions d'expédition.

---

## Conseils

- **Commencer simple** - Utiliser un tarif plat pour la première méthode, ajouter la complexité si nécessaire
- **Tester en détail** - Vérifier que toutes les méthodes fonctionnent en environnement de test avant d'activer en production
- **Utiliser des noms descriptifs** - « Livraison standard (5-7 jours) » est préférable à « Méthode 1 »
- **Fixer des délais de livraison réalistes** - Sous-estimer, surperformer pour la satisfaction client
- **Proposer le retrait si possible** - Réduit les coûts d'expédition, améliore la commodité du client
- **Surveiller la fiabilité de l'API du transporteur** - Avoir un tarif plat en cas d'échec des tarifs en temps réel
- **Utiliser des zones pour l'international** - Des tarifs différents par région évitent les pertes sur les destinations coûteuses
- **Combiner avec des promotions d'expédition** - Les règles ajoutent une logique conditionnelle (promotions de livraison gratuites, majorations pour les zones reculées)
- **Garder les méthodes limitées** - 2 à 4 options à la caisse évitent la paralysie de la décision
- **Mettre à jour les tableaux de tarifs saisonnièrement** - Les tarifs des transporteurs changent, vérifier annuellement
- **Utiliser la priorité avec soin** - Placer les options gratuites/abordables en premier, les options coûteuses en dernier