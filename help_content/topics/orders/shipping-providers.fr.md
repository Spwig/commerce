---
title: Fournisseurs de Livraison
---

Les fournisseurs de livraison connectent votre boutique aux API des transporteurs pour obtenir des tarifs d'expédition en temps réel, la génération d'étiquettes et le suivi des colis. Spwig prend en charge les principaux transporteurs dans le monde entier et vous permet également de configurer des grilles tarifaires manuelles pour les transporteurs sans intégration API.

![Shipping providers](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Transporteurs Disponibles

| Transporteur | Régions | Caractéristiques Principales |
|--------------|---------|------------------------------|
| **FedEx** | Mondial | Tarifs en temps réel, impression d'étiquettes, suivi, multi-colis |
| **UPS** | Mondial | Tarifs en temps réel, impression d'étiquettes, suivi, validation d'adresses |
| **USPS** | États-Unis | Tarifs nationaux et internationaux, suivi |
| **NinjaVan** | Asie du Sud-Est | Livraison du dernier kilomètre, prise en charge du contre-remboursement |
| **Canada Post** | Canada | National et international, tarifs colis et courrier |
| **Australia Post** | Australie | National et international, colis et express |

## Connecter un Transporteur

Naviguez vers **Paramètres > Fournisseurs de Livraison** et cliquez sur **Connecter un Fournisseur** pour lancer l'assistant de configuration.

### Étape 1 : Sélectionner le Fournisseur
Choisissez parmi les transporteurs disponibles. Chaque carte affiche les régions et fonctionnalités prises en charge par le transporteur.

### Étape 2 : Instructions de Configuration
Consultez le guide de configuration spécifique au transporteur :
- Comment créer un compte développeur/entreprise auprès du transporteur
- Où trouver vos identifiants API
- Les paramètres de compte requis (ex. : numéro d'expéditeur, numéro de compteur)

### Étape 3 : Saisir les Identifiants
Saisissez les identifiants API de votre compte transporteur. Les champs requis varient selon le transporteur :
- **Clé API / Secret** — Identifiants d'authentification
- **Numéro de Compte** — Votre numéro de compte ou d'expéditeur chez le transporteur
- **Numéro de Compteur** — Requis par certains transporteurs (ex. : FedEx)
- **Mode Sandbox** — Activez-le pour tester avec l'API sandbox du transporteur avant de passer en production

### Étape 4 : Tester la Connexion
Cliquez sur **Tester la Connexion** pour vérifier vos identifiants. L'assistant confirme :
- L'authentification API réussit
- Les permissions du compte sont valides
- Les requêtes de tarifs renvoient les résultats attendus

### Étape 5 : Configurer et Enregistrer
Finalisez les paramètres :
- **Actif** — Activer ou désactiver le transporteur
- **Nom d'Affichage** — Le nom affiché aux clients lors du passage en caisse
- **Adresse d'Origine** — L'adresse de l'entrepôt ou du centre de distribution pour le calcul des tarifs

## Zones de Livraison

Les zones de livraison définissent des zones géographiques pour le calcul des tarifs. Naviguez vers **Paramètres > Zones de Livraison** pour les gérer.

### Créer une Zone
1. Cliquez sur **+ Ajouter une Zone**
2. Donnez un nom à la zone (ex. : "National", "Europe", "Asie-Pacifique")
3. Définissez la couverture de la zone en utilisant un ou plusieurs des critères suivants :
   - **Pays** — Sélectionnez des pays spécifiques
   - **États/Provinces** — Limitez à des régions spécifiques au sein d'un pays
   - **Modèles de Code Postal** — Faites correspondre les codes postaux à l'aide de modèles (ex. : "90*" pour la région de Los Angeles)
4. Définissez la **Priorité** — Lorsque les zones se chevauchent, la zone de priorité la plus élevée est utilisée

### Correspondance des Zones
Lorsqu'un client saisit son adresse de livraison lors du passage en caisse, le système :
1. Vérifie d'abord les modèles de code postal (le plus spécifique)
2. Puis les correspondances d'état/province
3. Puis les correspondances de pays
4. Utilise la zone correspondante de priorité la plus élevée

## Règles de Livraison

Les règles de livraison appliquent des modificateurs conditionnels aux tarifs d'expédition. Naviguez vers **Paramètres > Règles de Livraison** pour les configurer.

### Types de Règles

| Type de Règle | Description |
|---------------|-------------|
| **Remise %** | Réduit le tarif d'expédition d'un pourcentage |
| **Remise Fixe** | Réduit le tarif d'expédition d'un montant fixe |
| **Définir le Coût** | Remplace le tarif par un montant spécifique |
| **Livraison Gratuite** | Met le coût de livraison à zéro |
| **Supplément %** | Ajoute un supplément en pourcentage au tarif |
| **Supplément Fixe** | Ajoute un supplément fixe au tarif |

### Conditions
Chaque règle peut avoir une ou plusieurs conditions qui doivent être remplies :

| Condition | Exemple |
|-----------|---------|
| **Valeur du Panier** | Livraison gratuite pour les commandes supérieures à 100 $ |
| **Poids Total** | Supplément pour les commandes de plus de 30 kg |
| **Nombre d'Articles** | Remise pour les commandes de 5+ articles |
| **Zone de Livraison** | Appliquer la règle uniquement aux envois nationaux |
| **Méthode de Livraison** | Appliquer à des méthodes spécifiques du transporteur |
| **Produits** | Tarifs spéciaux pour des produits spécifiques |
| **Groupe de Clients** | Les clients VIP bénéficient de la livraison gratuite |
| **Plage de Dates** | Promotions de livraison pour les fêtes |

### Priorité des Règles
- Les règles sont évaluées par ordre de priorité (le numéro le plus bas en premier)
- **Arrêter les Règles Suivantes** — Lorsqu'activé, si cette règle correspond, aucune autre règle n'est vérifiée
- Plusieurs règles peuvent se cumuler (ex. : une règle de remise de 10 % plus une règle de seuil de livraison gratuite)

## Grilles Tarifaires

Les grilles tarifaires fournissent une tarification par paliers basée sur les attributs de la commande. Naviguez vers **Paramètres > Grilles Tarifaires de Livraison** pour les configurer.

### Types de Grilles
Créez des paliers tarifaires basés sur :
- **Poids** — Paliers de prix par poids total de la commande (ex. : 0-1 kg = 5 $, 1-5 kg = 10 $)
- **Valeur de la Commande** — Paliers de prix par sous-total du panier
- **Quantité** — Paliers de prix par nombre d'articles

### Créer une Grille Tarifaire
1. Cliquez sur **+ Ajouter une Grille Tarifaire**
2. Nommez la grille et sélectionnez le type de palier
3. Ajoutez des paliers avec des plages min/max et des prix
4. Attribuez la grille tarifaire à une zone de livraison

Les grilles tarifaires sont utiles lorsque vous n'utilisez pas les tarifs API du transporteur et souhaitez définir votre propre structure de prix.

## Colis de Livraison

Définissez des tailles d'emballage standard pour des calculs de tarifs précis. Naviguez vers **Paramètres > Colis de Livraison**.

Pour chaque type de colis, définissez :
- **Nom** — Description (ex. : "Petite Boîte", "Grand Forfait")
- **Dimensions** — Longueur, largeur, hauteur
- **Poids Maximum** — Poids maximum que le colis peut contenir
- **Par Défaut** — Utiliser ce colis lorsqu'aucun emballage spécifique n'est attribué

Les transporteurs utilisent les dimensions des colis pour les calculs de poids dimensionnel, ce qui peut affecter les tarifs d'expédition.

## Transporteurs Manuels (Préréglages de Transporteurs)

Pour les transporteurs sans intégration API, créez des préréglages de transporteurs manuels :
1. Naviguez vers **Paramètres > Préréglages de Transporteurs**
2. Cliquez sur **+ Ajouter un Préréglage**
3. Configurez :
   - **Nom du Transporteur** — Nom affiché lors du passage en caisse
   - **Modèle d'URL de Suivi** — Modèle d'URL avec un espace réservé `{tracking_number}` (ex. : `https://track.transporteur.com/?id={tracking_number}`)
   - **Livraison Estimée** — Plage de délais de livraison à afficher aux clients
4. Associez à une grille tarifaire pour la tarification

Les transporteurs manuels fournissent des liens de suivi et des estimations de livraison sans intégration API en temps réel.

## Expédition Multi-Entrepôts

Si vous avez plusieurs entrepôts, l'expédition peut être calculée depuis différentes origines :
- **Entrepôt par Pays** — Attribuez des entrepôts à des pays spécifiques pour des distances d'expédition plus courtes
- **Chaîne de Repli** — Définissez quel entrepôt expédie lorsque l'entrepôt principal est en rupture de stock
- **Attribution par Produit** — Certains produits ne peuvent être expédiés que depuis des entrepôts spécifiques

Le système sélectionne automatiquement le meilleur entrepôt en fonction de la localisation du client et de la disponibilité du produit.

## Conseils

- Connectez les API des transporteurs pour obtenir des **tarifs en temps réel** chaque fois que possible — ils sont plus précis que les grilles tarifaires forfaitaires et s'ajustent en fonction du poids, des dimensions et de la destination.
- Créez une zone de livraison **"Reste du Monde"** comme solution de repli pour les pays non couverts par des zones spécifiques.
- Utilisez le type de règle **Livraison Gratuite** avec une condition de valeur du panier comme incitatif commercial (ex. : "Livraison gratuite sur les commandes de plus de 75 $").
- Testez les calculs de tarifs d'expédition avec différentes adresses et contenus de panier avant de passer en production.
- Configurez des **Préréglages de Transporteurs** avec des modèles d'URL de suivi pour les transporteurs locaux qui n'ont pas d'intégrations API — les clients recevront quand même des liens de suivi.
- Utilisez les **Colis de Livraison** pour obtenir des prix précis de poids dimensionnel auprès de transporteurs comme FedEx et UPS.
