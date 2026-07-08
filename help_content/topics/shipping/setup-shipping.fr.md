---
title: Configuration de la Livraison
---

Ce guide explique comment configurer la livraison pour votre boutique, de la mise en place de méthodes d'expédition de base à la connexion d'intégrations avec des transporteurs pour obtenir des tarifs en temps réel.

## Aperçu de la Livraison

Spwig propose deux approches pour la livraison :

- **Méthodes d'Expédition Manuelles** — Méthodes à tarif fixe que vous définissez (par exemple, "Livraison Standard — 5,99 EUR")
- **Intégrations avec les Transporteurs** — Tarifs en temps réel de fournisseurs comme FedEx, UPS et DHL

Vous pouvez utiliser l'une ou l'autre approche, ou combiner les deux.

## Méthodes d'Expédition

Les méthodes d'expédition sont les options que vos clients voient lors du paiement. Accédez à **Commandes > Expéditions** dans la barre latérale pour les gérer.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Créer une Méthode d'Expédition

1. Cliquez sur **Ajouter une Méthode d'Expédition**
2. Remplissez les informations :
   - **Nom** — Nom affiché aux clients (par exemple, "Livraison Express")
   - **Description** — Brève description du service
   - **Prix** — Coût d'expédition fixe
   - **Délai de Livraison Estimé** — Estimation du délai de livraison (par exemple, "3-5 jours ouvrés")
3. Cliquez sur **Enregistrer**

## Zones de Livraison

Les zones de livraison définissent les régions géographiques où vos méthodes d'expédition s'appliquent. Accédez à la section **Zones de Livraison** pour les gérer.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Créer une Zone

1. Cliquez sur **Ajouter une Zone de Livraison**
2. Configurez la zone :
   - **Nom de la Zone** — Nom interne (par exemple, "France Métropolitaine", "Europe")
   - **Pays** — Sélectionnez les pays appartenant à cette zone
   - **États/Régions** — Réduisez éventuellement à des régions spécifiques
   - **Codes Postaux** — Utilisez des modèles comme "9*" pour cibler des zones spécifiques
3. Assignez des méthodes d'expédition à cette zone
4. Cliquez sur **Enregistrer**

### Priorité des Zones

Lorsque l'adresse d'un client correspond à plusieurs zones, la zone la plus spécifique est prioritaire. Une zone ciblant au niveau régional a la priorité sur une zone au niveau du pays.

## Intégrations avec les Transporteurs

Connectez-vous aux transporteurs pour proposer des tarifs calculés en temps réel lors du paiement.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Fournisseurs Disponibles

Parcourez et installez des fournisseurs de livraison depuis le marketplace.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Les transporteurs pris en charge incluent :

- **FedEx** — Terrestre, Express, International
- **UPS** — Terrestre, 2 Jours, Express, Mondial
- **DHL** — Express, eCommerce
- **USPS** — Priority, First Class, Media Mail
- Et d'autres disponibles via le Marketplace

### Configurer un Transporteur

1. Rendez-vous sur la page des fournisseurs de livraison et cliquez sur **Installer** pour le transporteur de votre choix
2. Suivez l'assistant de configuration :
   - **Étape 1** — Consulter les détails du fournisseur
   - **Étape 2** — Configurer les paramètres généraux
   - **Étape 3** — Saisir vos identifiants API (numéro de compte, clé API, etc.)
   - **Étape 4** — Activer les services spécifiques (Terrestre, Express, etc.)
   - **Étape 5** — Tester la connexion
3. Une fois connecté, les tarifs du transporteur apparaissent automatiquement lors du paiement

### Identifiants API

Chaque transporteur nécessite un compte API :

- **FedEx** — Inscrivez-vous sur le Portail Développeur FedEx, créez une application et copiez votre clé API et votre secret
- **UPS** — Inscrivez-vous sur le Kit Développeur UPS, demandez une clé d'accès
- **DHL** — Contactez DHL pour obtenir les identifiants API via leur portail professionnel

## Règles d'Expédition

Créez des règles avancées pour contrôler quand et comment les méthodes d'expédition sont proposées.

### Règles Courantes

- **Livraison gratuite à partir de 50 EUR** — Définissez un minimum de panier pour la livraison gratuite
- **Tarif fixe pour les commandes légères** — Tarif fixe lorsque le poids de la commande est inférieur à un seuil
- **Désactiver l'express pour les zones éloignées** — Masquer les options express selon les codes postaux
- **Majoration en pourcentage** — Ajouter des frais de manutention en pourcentage des tarifs du transporteur

### Créer une Règle

1. Accédez à la section des règles d'expédition
2. Cliquez sur **Ajouter une Règle**
3. Définissez les conditions (total du panier, poids, zone, etc.)
4. Définissez l'action (ajuster le tarif, masquer la méthode, activer la livraison gratuite)
5. Enregistrez la règle

Les règles sont évaluées dans l'ordre ; la première règle correspondante s'applique.

## Livraison Gratuite

### Livraison Gratuite pour Toute la Boutique

Activez la livraison gratuite globalement dans **Paramètres > Paramètres de la Boutique** :

- Activez **Livraison Gratuite**
- Définissez éventuellement un montant minimum de commande
- Choisissez les régions éligibles

### Livraison Gratuite Promotionnelle

Créez des offres de livraison gratuite à durée limitée :

1. Allez dans **Marketing > Ventes et Promotions**
2. Créez une nouvelle promotion
3. Définissez la condition : "Total du panier supérieur à X"
4. Définissez l'action : "Livraison gratuite"
5. Configurez les dates de début et de fin

## Livraison Internationale

Pour les commandes internationales, assurez-vous que vos produits disposent de :

- **Code SH** — Classification tarifaire du Système Harmonisé
- **Pays d'Origine** — Pays de fabrication
- **Valeur en Douane** — Valeur déclarée pour les douanes

Ces champs se trouvent dans l'onglet **Inventaire** de chaque produit. Les transporteurs utilisent ces informations pour générer automatiquement la documentation douanière.

## Conseils

- Commencez par des méthodes d'expédition manuelles pour lancer rapidement votre boutique, puis ajoutez les intégrations avec les transporteurs par la suite.
- Créez d'abord les zones de livraison pour vos destinations les plus fréquentes.
- Testez toujours votre configuration d'expédition en passant des commandes de test avec différentes adresses.
- Utilisez la fonctionnalité de majoration des tarifs pour couvrir les frais de manutention et d'emballage.
- Mettez en place des seuils de livraison gratuite pour augmenter la valeur moyenne des commandes.
