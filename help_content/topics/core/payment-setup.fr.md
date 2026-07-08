---
title: Configuration des paiements
---

Les fournisseurs de paiement connectent votre boutique aux passerelles de paiement afin que vous puissiez accepter les cartes de crédit, les portefeuilles numériques et d'autres méthodes de paiement lors du passage à la caisse. Spwig prend en charge plusieurs fournisseurs simultanément, offrant à vos clients des options de paiement flexibles.

![Fournisseurs de paiement](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Fournisseurs disponibles

| Fournisseur | Description |
|----------|-------------|
| **Stripe** | Cartes de crédit, Apple Pay, Google Pay et 135+ devises |
| **PayPal** | Solde PayPal, cartes de crédit/débit et options de paiement ultérieur |
| **Airwallex** | Paiements en devises multiples optimisés pour le commerce transfrontalier |
| **Adyen** | Paiements de niveau entreprise avec plus de 250 méthodes de paiement à l'échelle mondiale |
| **Square** | Paiements en personne et en ligne avec un support POS intégré |
| **Revolut** | Paiements européens rapides avec des taux de change compétitifs |

## Connexion à un fournisseur

Accédez à **Paramètres > Fournisseurs de paiement** et cliquez sur **Connecter un fournisseur** pour lancer le assistant d'installation.

### Étape 1 : Sélectionner un fournisseur

Choisissez parmi les fournisseurs de paiement disponibles. Chaque carte affiche les fonctionnalités et les régions pris en charge par le fournisseur.

### Étape 2 : Instructions d'installation

Consultez le guide d'installation spécifique au fournisseur. Cela inclut : 
- La manière de créer un compte avec le fournisseur (si vous n'en avez pas déjà un)
- L'endroit où trouver vos identifiants API dans le tableau de bord du fournisseur
- Toutes les prérequis (par exemple, la vérification de l'entreprise)

### Étape 3 : Entrer les identifiants

Entrez vos identifiants API : 
- **Clé API / Clé secrète** — Vos identifiants d'authentification provenant du tableau de bord du fournisseur
- **Mode de paiement** — Choisissez la manière dont les clients interagissent avec le formulaire de paiement : 

| Mode | Description |
|------|-------------|
| **Hébergé** | Les clients sont redirigés vers la page de paiement du fournisseur (par exemple, Stripe Checkout). Installation la plus simple, la conformité PCI est gérée par le fournisseur. |
| **Intégré** | Le formulaire de paiement est intégré directement sur votre page de passage à la caisse. Expérience fluide, mais nécessite le SDK JavaScript du fournisseur. |

- **Mode de test / Mode réel** — Commencez en mode de test pour les tests, puis basculez vers le mode réel lorsque vous êtes prêt

### Étape 4 : Tester la connexion

Cliquez sur **Tester la connexion** pour vérifier que vos identifiants sont valides. L'assistant vérifie : 
- L'authentification de la clé API
- Les permissions du compte
- L'accessibilité du point de terminaison de webhook

### Étape 5 : Configurer et enregistrer

Finalisez les paramètres du fournisseur : 
- **Actif** — Activer ou désactiver le fournisseur
- **Fournisseur par défaut** — Définir comme méthode de paiement principale lors du passage à la caisse
- **Nom d'affichage** — Le nom affiché aux clients lors du passage à la caisse
- **Ordre de tri** — Contrôle l'ordre d'apparition des fournisseurs lors du passage à la caisse (les numéros plus bas apparaissent en premier)

## Tableau de bord des paiements

Accédez à **Paramètres > Tableau de bord des paiements** pour obtenir un aperçu de votre activité de paiement : 

### Actions requises

Les cartes d'alerte en haut mettent en évidence les problèmes nécessitant une attention : 
- **Transactions échouées** — Paiements qui n'ont pas pu être traités
- **Captures en attente** — Paiements approuvés en attente de capture
- **Erreurs de connexion** — Fournisseurs avec des problèmes de connectivité

### Analyse des revenus

- **Graphique des revenus** — Décomposition visuelle du volume de paiement au fil du temps, groupé par jour, semaine ou mois
- **Métriques de performance** — Chiffre d'affaires total, taux de réussite, valeur moyenne des transactions et taux de remboursement
- **Comparaison des fournisseurs** — Cartes de performance côte à côte pour chaque fournisseur connecté

### Détail des transactions

- **Répartition des statuts** — Comptes des transactions terminées, en attente, échouées et remboursées
- **Mélange des méthodes de paiement** — Les méthodes de paiement les plus utilisées par les clients (cartes de crédit, PayPal, portefeuilles numériques)

## Gestion des méthodes de paiement

Chaque fournisseur prend en charge différentes méthodes de paiement. Vous pouvez activer ou désactiver des méthodes spécifiques par pays : 

1. Accédez à la page de configuration d'un fournisseur
2. Faites défiler jusqu'à la section **Méthodes de paiement**
3. Activez ou désactivez les méthodes individuelles
4. Utilisez les contrôles au niveau du pays pour restreindre les méthodes à certains marchés

Cela est utile lorsque une méthode de paiement est populaire dans une région mais pas dans une autre (par exemple, iDEAL aux Pays-Bas, Bancontact en Belgique).

## Webhooks

Les webhooks maintiennent votre boutique synchronisée avec le fournisseur de paiement en temps réel. Ils gèrent des événements tels que : 
- Paiement terminé ou échoué
- Remboursements traités
- Ouvertures de litiges et de recours
- Renouvellements d'abonnements

### Configuration automatique

Lorsque vous connectez un fournisseur, Spwig enregistre automatiquement un point de terminaison de webhook auprès du fournisseur. L'URL du webhook est affichée sur la page de configuration du fournisseur pour référence.

### Surveillance des webhooks

Chaque webhook entrant est enregistré avec : 
- **Type d'événement** (par exemple, payment_intent.succeeded)
- **Horodatage** et statut de traitement
- **Charge utile** pour le débogage

Si un webhook échoue à être traité, il est enregistré comme une erreur afin que vous puissiez enquêter.

## Utilisation de plusieurs fournisseurs

Vous pouvez connecter simultanément plusieurs fournisseurs de paiement : 

- **Fournisseur par défaut** — Le fournisseur sélectionné par défaut lors du passage à la caisse. Marquez un fournisseur comme fournisseur par défaut dans sa configuration.
- **Ordre de tri** — Contrôle l'ordre d'affichage lors du passage à la caisse. Les clients voient tous les fournisseurs actifs et peuvent choisir leur préféré.
- **Redondance** — Si un fournisseur connaît un temps d'arrêt, les clients peuvent toujours payer en utilisant un autre fournisseur.

## Conseils

- Commencez par **Stripe** ou **PayPal** — ils couvrent la plus large gamme de méthodes de paiement et de régions.
- Utilisez **le mode test / mode de test** pour traiter des transactions de test avant de passer en production. Chaque fournisseur a des numéros de carte de test dans leur documentation.
- Activez **plusieurs fournisseurs** afin que les clients aient une option de paiement de secours si un fournisseur a des problèmes.
- Définissez un **ordre de tri bas** pour votre fournisseur préféré afin qu'il s'affiche en premier lors du passage à la caisse.
- Surveillez le Tableau de bord des paiements hebdomadairement pour détecter les transactions échouées et les problèmes de connexion tôt.
- Gardez vos identifiants API sécurisés — ils sont stockés chiffrés dans la base de données mais ne devraient jamais être partagés.

