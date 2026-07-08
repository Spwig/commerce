---
title: Comptes vs. Clients
---

Les commerçants se demandent souvent : "Quelle est la différence entre un compte et un client ?" Cette confusion est courante car chaque client est un compte, mais pas chaque compte est un client. Ce guide clarifie cette distinction et explique quand utiliser chaque interface d'administration.

![Liste d'utilisateurs](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Qu'est-ce qu'un compte ?

Un **compte** est l'objet principal d'authentification dans Spwig. Toute personne capable de se connecter à votre plateforme — membre du personnel ou client — possède un compte. Les comptes sont gérés par le système d'authentification Spwig et sont stockés dans le modèle `User`.

Tous les comptes ont :
- **Adresse e-mail** — L'identifiant principal et le mot de passe de connexion
- **Nom d'utilisateur** — Un nom d'utilisateur unique (généré automatiquement à partir de l'e-mail par défaut)
- **Mot de passe** — Haché et stocké en toute sécurité
- **Drapeau is_staff** — Détermine si le compte peut accéder à l'arrière-plan d'administration

Les comptes peuvent également s'authentifier via des fournisseurs OAuth (Google, Facebook, etc.) configurés à **Paramètres > Authentification**.

## Qu'est-ce qu'un client ?

Un **client** est un type particulier de compte avec `is_staff=False`. Les clients achètent sur votre boutique en ligne, passent des commandes et gèrent leurs profils. Chaque compte client est automatiquement étendu avec :

- **CustomerProfile** — Stocke les préférences, le statut d'abonnement à la newsletter et les valeurs des champs personnalisés
- **CustomerMetrics** — Suit la valeur à vie (LTV), les scores RFM, l'historique des commandes et les données de segmentation
- **OrderHistory** — Liens vers toutes les commandes passées par ce client

Les clients peuvent être :
- **Clients enregistrés** — Créés via l'enregistrement sur la boutique en ligne ou l'administration
- **Utilisateurs invités** — Comptes temporaires créés lors du paiement invité (le nom d'utilisateur commence par `guest_`)
- **Clients importés** — Migrés depuis d'autres plateformes via l'import CSV

## La différence clé

| Attribut | Compte | Client |
|-----------|---------|----------|
| **Objectif** | Authentification et autorisation | Achat, commandes et analyse |
| **Portée** | Membres du personnel ET clients | Uniquement les clients |
| **Drapeau is_staff** | Vrai OU Faux | Toujours Faux |
| **Données étendues** | Aucune (uniquement les champs principaux) | CustomerProfile + CustomerMetrics |
| **Emplacement de l'administration** | Paramètres > Utilisateurs | Clients > Profils clients |
| **Peut se connecter** | Oui | Oui |
| **Peut passer des commandes** | Uniquement s'il a un CustomerProfile | Oui |
| **Peut accéder à l'administration** | Uniquement si is_staff=True | Non |

En bref : 
- Un **compte** est toute personne capable de se connecter
- Un **client** est un compte qui achète et passe des commandes

## Les membres du personnel sont également des comptes

Les membres du personnel sont des comptes avec `is_staff=True`. Ils peuvent se connecter à l'arrière-plan d'administration et effectuer des actions en fonction de leurs permissions **StaffRole** attribuées.

Les membres du personnel peuvent avoir optionnellement un **CustomerProfile** s'ils achètent également sur la boutique en ligne. Par exemple, si vous (le commerçant) placez une commande de test sur votre propre boutique, un CustomerProfile est créé pour votre compte de personnel. Cela n'affecte pas votre accès à l'administration.

Les permissions des membres du personnel sont contrôlées par : 
- **StaffRole** — Définit les sections et actions d'administration auxquelles le membre du personnel a accès
- **Drapeau is_superuser** — Accorde un accès complet sans restriction (utilisez-le avec parcimonie)

Gérez les membres du personnel à **Paramètres > Gestion du personnel**.

## Les utilisateurs invités

Le paiement invité crée des comptes temporaires avec des noms d'utilisateur générés automatiquement commençant par `guest_`. Ces comptes : 
- Ont `is_staff=False` (ils sont des clients)
- Ont un CustomerProfile (pour l'association des commandes)
- Ont un mot de passe aléatoire (l'invité ne peut pas se connecter sauf s'il se convertit en client enregistré)
- Sont exclusivement exclus des analyses clients par défaut

Les invités peuvent se convertir en clients enregistrés en : 
1. Créant un compte sur la boutique en ligne avec la même adresse e-mail
2. En vérifiant leur adresse e-mail
3. Le système fusionne l'historique des commandes invité avec le nouveau compte enregistré

Gérez les paramètres de conversion des invités à **Paramètres > Paiement > Paiement invité**.

## Où trouver chacun

| Emplacement de l'administration | Ce que vous gérez | Cas d'utilisation clés |
|----------------|-----------------|---------------|
| **Paramètres > Utilisateurs** | Tous les comptes (personnel + clients) | Réinitialiser les mots de passe, activer/désactiver les comptes, attribuer les permissions de personnel |
| **Paramètres > Gestion du personnel** | Seulement les comptes de personnel (is_staff=True) | Attribuer des rôles, gérer l'accès des membres de l'équipe, configurer les permissions |
| **Clients > Profils clients** | Seulement les comptes clients (is_staff=False) | Voir les préférences des clients, l'historique des commandes, LTV, scores RFM, segments |
| **Clients > Analyse** | Métriques et segments clients | Analyser le comportement des clients, créer des segments marketing, suivre la fidélisation |

![Liste des profils clients](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Quand utiliser chaque interface

Utilisez **Paramètres > Utilisateurs** lorsque vous avez besoin de : 
- Réinitialiser le mot de passe d'un client
- Désactiver un compte compromis
- Créer manuellement un compte client
- Voir les connexions de login OAuth
- Voir tous les comptes (personnel + clients) dans une seule liste

Utilisez **Paramètres > Gestion du personnel** lorsque vous avez besoin de : 
- Ajouter un nouveau membre d'équipe
- Attribuer ou modifier le rôle d'un membre du personnel
- Configurer des permissions détaillées
- Auditer les journaux d'activité des membres du personnel

Utilisez **Clients > Profils clients** lorsque vous avez besoin de : 
- Voir l'historique des commandes d'un client
- Voir les préférences du client et les valeurs des champs personnalisés
- Vérifier le statut d'abonnement à la newsletter
- Réviser la valeur à vie (LTV) et les scores RFM du client
- Gérer les segments clients

Utilisez **Clients > Analyse** lorsque vous avez besoin de : 
- Identifier les clients à haute valeur
- Créer des segments marketing (par exemple, "clients qui n'ont pas commandé en 90 jours")
- Analyser les tendances de la valeur à vie des clients
- Exporter des listes de clients pour des campagnes

## Conseils

- **Les profils clients sont créés automatiquement** — Lorsqu'un client passe sa première commande (invité ou enregistré), Spwig crée un enregistrement CustomerProfile et CustomerMetrics pour l'analyse.
- **Les membres du personnel peuvent également être des clients** — Si un membre du personnel passe une commande sur la boutique en ligne, il obtient un CustomerProfile. Cela est normal et n'affecte pas son accès à l'administration.
- **Les comptes invités encombrent la liste des utilisateurs** — Utilisez l'interface de profil client pour vous concentrer sur les clients réels et engagés. La liste des utilisateurs inclut tous les comptes invités.
- **Segmentez par is_staff=False** — Lors de l'exportation de listes de clients pour des campagnes par e-mail, filtrez toujours pour `is_staff=False` pour exclure les membres de l'équipe.
- **Les comptes OAuth sont également des comptes** — Lorsqu'un client se connecte via Google ou Facebook, Spwig crée un compte et le relie à son profil OAuth. Le champ e-mail est rempli à partir du fournisseur OAuth.