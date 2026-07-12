---
title: Fournisseurs de livraison
---

Les fournisseurs de livraison connectent votre magasin aux API des transporteurs pour obtenir des tarifs de livraison en temps réel, générer des étiquettes et suivre les colis. Spwig prend en charge les principaux transporteurs du monde entier et vous permet également de configurer des tableaux de tarifs manuels pour les transporteurs sans intégration API.

![Fournisseurs de livraison](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Fournisseurs disponibles

| Fournisseur | Régions | Fonctionnalités clés |
|-----------|-------|------------------|
| **FedEx** | Mondial | Tarifs en temps réel, impression d'étiquettes, suivi, multiples colis |
| **UPS** | Mondial | Tarifs en temps réel, impression d'étiquettes, suivi, validation d'adresses |
| **USPS** | États-Unis | Tarifs nationaux et internationaux, suivi |
| **NinjaVan** | Asie du Sud-Est | Dernier mile, paiement à la livraison |
| **Canada Post** | Canada | Nationaux et internationaux, tarifs pour colis et lettres |
| **Australia Post** | Australie | Nationaux et internationaux, colis et express |

## Connexion à un fournisseur

Accédez à **Paramètres > Fournisseurs de livraison** et cliquez sur **Connecter un fournisseur** pour lancer l'assistant d'installation.

### Étape 1 : Sélectionner le fournisseur

Choisissez parmi les fournisseurs de livraison disponibles. Chaque carte affiche les régions et les fonctionnalités prises en charge par le transporteur.

### Étape 2 : Instructions de configuration

Consultez le guide de configuration spécifique au transporteur :
- Comment créer un compte développeur/entreprise avec le transporteur
- Où trouver vos identifiants API
- Paramètres du compte requis (par exemple, numéro de transporteur, numéro de mètre)

### Étape 3 : Entrer les identifiants

Entrez les identifiants API de votre compte de transporteur. Les champs requis varient selon le transporteur :

- **Clé API / Secret** — Identifiants d'authentification
- **Numéro de compte** — Votre numéro de compte ou de transporteur
- **Numéro de mètre** — Requis par certains transporteurs (par exemple, FedEx)
- **Mode de test** — Activez-le pour tester avec l'API de test du transporteur avant de passer en production

### Étape 4 : Tester la connexion

Cliquez sur **Tester la connexion** pour vérifier vos identifiants. L'assistant confirme :
- L'authentification API réussit
- Les autorisations du compte sont valides
- Les requêtes de tarif renvoient les résultats attendus

### Étape 5 : Configurer et enregistrer

Finalisez les paramètres :
- **Actif** — Activer ou désactiver le transporteur
- **Nom d'affichage** — Le nom affiché aux clients lors du paiement
- **Adresse d'origine** — L'adresse du entrepôt ou de livraison utilisée pour le calcul des tarifs

## Zones de livraison

Les zones de livraison définissent des zones géographiques pour le calcul des tarifs. Accédez à **Paramètres > Zones de livraison** pour les gérer.

### Créer une zone

1. Cliquez sur **+ Ajouter une zone**
2. Donnez un nom à la zone (par exemple, "Domestique", "Europe", "Asie-Pacifique")
3. Définissez la couverture de la zone à l'aide d'un ou plusieurs des éléments suivants :
   - **Pays** — Sélectionnez des pays spécifiques
   - **États/Provinces** — Restreignez à des régions spécifiques dans un pays
   - **Modèles de codes postaux** — Correspondre aux codes postaux/ZIP en utilisant des modèles (par exemple, "90*" pour la région de Los Angeles)
4. Définissez la **Priorité** — Lorsque les zones se chevauchent, la zone avec la priorité la plus élevée est utilisée

### Correspondance des zones

Lorsqu'un client entre son adresse de livraison lors du paiement, le système :
1. Vérifie d'abord les modèles de codes postaux (plus spécifique)
2. Puis les correspondances d'états/provinces
3. Puis les correspondances de pays
4. Utilise la zone correspondante avec la priorité la plus élevée

## Promotions de livraison

Les promotions de livraison appliquent des modificateurs conditionnels aux tarifs de livraison. Accédez à **Paramètres > Promotions de livraison** pour les configurer.

### Types de promotion

| Type de promotion | Description |
|----------------|-------------|
| **Réduction en pourcentage** | Réduire le tarif de livraison d'un pourcentage |
| **Réduction fixe** | Réduire le tarif de livraison d'un montant fixe |
| **Remplacement du coût** | Remplacer le tarif par un montant spécifique |
| **Livraison gratuite** | Définir le coût de livraison à zéro |
| **Majoration en pourcentage** | Ajouter une majoration en pourcentage au tarif |
| **Majoration fixe** | Ajouter une majoration fixe au tarif |

### Conditions

Chaque promotion peut avoir une ou plusieurs conditions à remplir :

| Condition | Exemple |
|-----------|---------|
| **Valeur du panier** | Livraison gratuite pour les commandes de plus de 100 $ |
| **Poids total** | Majoration pour les commandes de plus de 30 kg |
| **Nombre d'articles** | Réduction pour les commandes avec 5 articles ou plus |
| **Zone de livraison** | Appliquer la promotion uniquement aux livraisons nationales |
| **Méthode de livraison** | Appliquer à des méthodes spécifiques de transporteur |
| **Produits** | Tarifs spéciaux pour des produits spécifiques |
| **Groupe de clients** | Les clients VIP bénéficient de la livraison gratuite |
| **Plage de dates** | Promotions de livraison de Noël |

### Priorité des promotions

- Les promotions sont évaluées dans l'ordre de priorité (le plus petit nombre en premier)
- **Arrêter les autres promotions** — Lorsqu'elle est activée, si cette promotion correspond, aucune autre promotion n'est vérifiée
- Plusieurs promotions peuvent s'appliquer (par exemple, une promotion de 10 % de réduction plus une promotion de livraison gratuite sur un seuil de commande)

## Tableaux de tarifs

Les tableaux de tarifs permettent de définir des tarifs échelonnés en fonction des attributs de commande. Accédez à **Paramètres > Tableaux de tarifs de livraison** pour les configurer.

### Types de tableaux

Créez des échelons de tarifs en fonction de :
- **Poids** — Échelons de prix en fonction du poids total de la commande (par exemple, 0-1 kg = 5 $, 1-5 kg = 10 $)
- **Valeur de commande** — Échelons de prix en fonction du sous-total du panier
- **Quantité** — Échelons de prix en fonction du nombre d'articles

### Créer un tableau de tarifs

1. Cliquez sur **+ Ajouter un tableau de tarifs**
2. Donnez un nom au tableau et sélectionnez le type d'échelon
3. Ajoutez des échelons avec des plages minimales/maximales et des prix
4. Attribuez le tableau de tarifs à une zone de livraison

Les tableaux de tarifs sont utiles lorsque vous n'utilisez pas les tarifs API des transporteurs et que vous souhaitez définir votre propre structure de tarification.

## Emballages de livraison

Définissez des tailles d'emballage standard pour des calculs de tarif précis. Accédez à **Paramètres > Emballages de livraison**.

Pour chaque type d'emballage, définissez :
- **Nom** — Description (par exemple, "Petite boîte", "Grand colis plat")
- **Dimensions** — Longueur, largeur, hauteur
- **Poids maximal** — Poids maximal que l'emballage peut contenir
- **Par défaut** — Utiliser cet emballage lorsque aucun emballage spécifique n'est assigné

Les transporteurs utilisent les dimensions de l'emballage pour calculer le poids dimensionnel, ce qui peut affecter les tarifs de livraison.

## Transporteurs manuels (Préférences de transporteur)

Pour les transporteurs sans intégration API, créez des préférences de transporteur manuelles :

1. Accédez à **Paramètres > Préférences de transporteur**
2. Cliquez sur **+ Ajouter une préférence**
3. Configurez :
   - **Nom du transporteur** — Nom affiché lors du paiement
   - **Modèle d'URL de suivi** — Modèle d'URL avec un espace réservé {tracking_number} (par exemple, `https://track.carrier.com/?id={tracking_number}`)
   - **Délai estimé de livraison** — Plage de temps de livraison à afficher aux clients
4. Associez un tableau de tarifs pour les prix

Les transporteurs manuels fournissent des liens de suivi et des estimations de livraison sans intégration API en temps réel.

## Livraison multi-entrepôts

Si vous avez plusieurs entrepôts, la livraison peut être calculée à partir de différentes origines :

- **Entrepôt spécifique au pays** — Attribuez des entrepôts à des pays spécifiques pour des distances de livraison plus courtes
- **Chaîne de secours** — Définissez quel entrepôt livrera lorsque l'entrepôt principal est en rupture de stock
- **Affectation par produit** — Certains produits ne peuvent être livrés qu'à partir d'entrepôts spécifiques

Le système sélectionne automatiquement le meilleur entrepôt en fonction de l'emplacement du client et de la disponibilité du produit.

## Conseils

- Connectez les API des transporteurs pour obtenir des **tarifs en temps réel** dès que possible — ils sont plus précis que les tableaux de tarifs fixes et tiennent compte du poids, des dimensions et de la destination.
- Créez une **zone de livraison "Reste du monde"** comme zone de secours pour les pays non couverts par des zones spécifiques.
- Utilisez le type de promotion **Livraison gratuite** avec une condition de valeur du panier comme incitation à l'achat (par exemple, "Livraison gratuite pour les commandes de plus de 75 $")
- Testez les calculs des tarifs de livraison avec différentes adresses et contenus de panier avant de mettre en ligne.
- Configurez des **Préférences de transporteur** avec des modèles d'URL de suivi pour tout transporteur local qui n'a pas d'intégration API — les clients obtiennent toujours des liens de suivi.
- Utilisez les **Emballages de livraison** pour obtenir des tarifs précis de poids dimensionnel auprès de transporteurs comme FedEx et UPS.