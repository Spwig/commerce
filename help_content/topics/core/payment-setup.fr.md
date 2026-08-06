---
title: Configuration des paiements
---

Les fournisseurs de paiement connectent votre boutique aux passerelles de paiement afin que vous puissiez accepter les cartes de crédit, les portefeuilles numériques et d'autres méthodes de paiement lors du passage à la caisse. Spwig prend en charge plusieurs fournisseurs simultanément, offrant ainsi à vos clients des options de paiement flexibles.

![Fournisseurs de paiement](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Fournisseurs disponibles

| Fournisseur | Description |
|----------|-------------|
| **Stripe** | Cartes de crédit, Apple Pay, Google Pay et 135+ devises |
| **PayPal** | Solde PayPal, cartes de crédit/débit et options de paiement différé |
| **Airwallex** | Paiements multi-devise optimisés pour le commerce transfrontalier |
| **Square** | Paiements en personne et en ligne avec un support POS intégré |
| **Revolut** | Paiements européens rapides avec des taux de change compétitifs |

## Connexion à un fournisseur

Accédez à **Paramètres > Fournisseurs de paiement** et cliquez sur **Connecter un fournisseur** pour lancer l'assistant d'installation.

### Étape 1 : Sélectionner un fournisseur

Choisissez parmi les fournisseurs de paiement disponibles. Chaque carte affiche les fonctionnalités et les régions pris en charge par le fournisseur.

### Étape 2 : Instructions d'installation

Consultez le guide d'installation spécifique au fournisseur. Cela inclut :
- La manière de créer un compte avec le fournisseur (si vous n'en avez pas un)
- L'endroit où trouver vos identifiants API dans le tableau de bord du fournisseur
- Toutes les prérequis (par exemple, la vérification de l'entreprise)

### Étape 3 : Entrer les identifiants

Entrez vos identifiants API :
- **Clé API / Clé secrète** — Vos identifiants d'authentification provenant du tableau de bord du fournisseur
- **Mode de paiement** — Choisissez comment les clients interagissent avec le formulaire de paiement :

| Mode | Description |
|------|-------------|
| **Hébergé** | Les clients sont redirigés vers la page de paiement du fournisseur (par exemple, Stripe Checkout). Configuration la plus simple, la conformité PCI est gérée par le fournisseur. |
| **Intégré** | Le formulaire de paiement est intégré directement sur votre page de passage à la caisse. Expérience fluide, mais nécessite le SDK JavaScript du fournisseur. |

- **Mode test / mode live** — Commencez en mode test pour les tests, puis passez en mode live lorsque vous êtes prêt

### Étape 4 : Tester la connexion

Cliquez sur **Tester la connexion** pour vérifier que vos identifiants sont valides. L'assistant vérifie :
- L'authentification de la clé API
- Les autorisations du compte
- L'accessibilité du point de terminaison Webhook

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
- **Métriques de performance** — Revenus totaux, taux de réussite, valeur moyenne des transactions et taux de remboursement
- **Comparaison des fournisseurs** — Cartes de performance côte à côte pour chaque fournisseur connecté

### Détail des transactions

- **Répartition des statuts** — Comptes de transactions terminées, en attente, échouées et remboursées
- **Mélange des méthodes de paiement** — Les méthodes de paiement les plus utilisées par les clients (cartes de crédit, PayPal, portefeuilles numériques)

## Gestion des méthodes de paiement

Chaque fournisseur prend en charge différentes méthodes de paiement. Vous pouvez activer ou désactiver des méthodes spécifiques par pays :

1. Accédez à la page de configuration d'un fournisseur
2. Faites défiler jusqu'à la section **Méthodes de paiement**
3. Activez ou désactivez les méthodes individuelles
4. Utilisez les contrôles au niveau du pays pour restreindre les méthodes à des marchés spécifiques

Cela est utile lorsque une méthode de paiement est populaire dans une région mais pas dans une autre (par exemple, iDEAL aux Pays-Bas, Bancontact en Belgique).

## Webhooks

Les webhooks permettent de synchroniser votre magasin en temps réel avec le prestataire de paiement.

Ils gèrent des événements tels que :
- Paiement terminé ou échoué
- Remboursements traités
- Disputes et recours bancaires ouverts
- Renouvellements d'abonnement

### Configuration automatique

Lorsque vous connectez un prestataire, Spwig enregistre automatiquement un point de terminaison de webhook auprès du prestataire. L'URL du webhook est affichée sur la page de configuration du prestataire pour référence.

### Surveillance des webhooks

Chaque webhook entrant est enregistré avec :
- **Type d'événement** (par exemple, payment_intent.succeeded)
- **Horodatage** et statut de traitement
- **Charge utile** pour le débogage

Si un webhook échoue lors du traitement, il est enregistré en tant qu'erreur afin que vous puissiez enquêter.

## Utilisation de plusieurs prestataires

Vous pouvez connecter simultanément plusieurs prestataires de paiement :

- **Prestataire par défaut** — Le prestataire sélectionné par défaut lors du paiement. Sélectionnez un prestataire comme par défaut dans sa configuration.
- **Ordre de tri** — Contrôle l'ordre d'affichage lors du paiement. Les clients voient tous les prestataires actifs et peuvent choisir leur préféré.
- **Fonction de secours** — Si un prestataire connaît un temps d'arrêt, les clients peuvent toujours payer en utilisant un autre prestataire.

## Conseils

- Commencez par **Stripe** ou **PayPal** — ils couvrent la plus large gamme de méthodes de paiement et de régions.
- Utilisez le **mode test/sandbox** pour traiter des transactions de test avant de passer en production. Chaque prestataire dispose de numéros de carte de test dans sa documentation.
- Activez **plusieurs prestataires** afin que les clients aient une option de paiement de secours si un prestataire rencontre des problèmes.
- Affectez un **ordre de tri bas** à votre prestataire préféré afin qu'il s'affiche en premier lors du paiement.
- Surveillez le tableau de bord des paiements hebdomadairement pour détecter les transactions échouées et les problèmes de connexion tôt.
- Gardez vos **identifiants API** sécurisés — ils sont stockés chiffrés dans la base de données, mais ne devraient jamais être partagés.