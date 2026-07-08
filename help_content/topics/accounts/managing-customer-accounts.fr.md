---
title: Gestion des comptes clients
---

Les comptes clients permettent aux commerçants de suivre les informations clients, l'historique des commandes et les préférences. Accédez à **Clients > Tous les clients** dans le menu latéral de l'administration pour gérer les comptes clients.

![Ajouter un client](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Comprendre les comptes clients vs les profils clients

**Comptes clients** sont les identifiants de connexion (e-mail/mot de passe) stockés dans le modèle Utilisateur. **Profils clients** stockent des informations supplémentaires sur les clients comme le numéro de téléphone, la date de naissance, les préférences et les analyses. Chaque compte client a un profil correspondant qui stocke ces données étendues.

Lorsque vous gérez des clients dans l'administration, vous travaillez avec des profils clients qui se lient aux comptes utilisateurs en arrière-plan.

## Afficher tous les clients

La liste des clients affiche tous les clients enregistrés avec des métriques clés:

| Colonne | Description |
|--------|-------------|
| **Utilisateur** | Nom et adresse e-mail du client |
| **Statut d'affiliate** | Indique si le client est également un partenaire d'affiliate |
| **Valeur client** | Montant total dépensé par le client (codé en couleur) |
| **Segment client** | Segment RFM (Champion, Fidèle, En risque, etc.) |
| **Total des commandes** | Nombre de commandes terminées |
| **Jours depuis la dernière commande** | Récence de la dernière commande |
| **Client VIP** | Badge si le client est marqué comme VIP |

### Filtrer les clients

Utilisez le menu latéral de filtrage pour affiner la liste:
- **Statut d'affiliate** — Est affilié, Non affilié, Affilié en attente, Actif, Suspendu, Rejeté
- **Disposition du tableau de bord** — Disposition du tableau de bord préférée par le client
- **Abonné au bulletin d'information** — Indique si le client a souscrit au bulletin d'information
- **E-mails de marketing** — Indique si le client a souscrit aux e-mails de marketing
- **Créé le** — Filtre par date d'enregistrement

### Rechercher des clients

Utilisez la barre de recherche pour trouver des clients par:
- Nom d'utilisateur
- Adresse e-mail
- Prénom
- Nom de famille
- Numéro de téléphone

## Afficher les détails du client

Cliquez sur le nom d'un client pour afficher son profil complet. La page de détails du client affiche:

![Détails du client](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Section Informations client

Détails de contact de base et statut du compte:
- **Utilisateur** — Lien vers le compte utilisateur sous-jacent
- **Téléphone** — Numéro de téléphone du client
- **Date de naissance** — Pour la vérification d'âge et les campagnes d'anniversaire

### Préférences du tableau de bord

La manière dont le client a personnalisé son tableau de bord de compte:
- **Disposition du tableau de bord** — Vue en grille, en liste ou compacte
- **Afficher l'historique des commandes** — Indique si l'historique des commandes apparaît sur le tableau de bord
- **Afficher la liste de souhaits** — Indique si la liste de souhaits apparaît sur le tableau de bord
- **Afficher les produits récents** — Indique si les produits récemment consultés apparaissent
- **Afficher les recommandations** — Indique si les recommandations de produits apparaissent

### Préférences de communication

Statut d'abonnement du client pour diverses communications:
- **Abonné au bulletin d'information** — Abonné aux bulletins d'information généraux
- **E-mails de marketing** — Abonné aux e-mails promotionnels
- **Mises à jour de statut de commande** — Abonné aux mises à jour du statut de commande

### Analyse client

Résumés en lecture seule du comportement et de la valeur du client:
- **Résumé de l'analyse client** — Scores RFM, segment, valeur à vie
- **Résumé du comportement d'achat** — Fréquence d'achat, valeur moyenne de commande, catégories préférées
- **Résumé de l'engagement** — Dernière connexion, taux d'ouverture des e-mails, activité sur le site

Ces champs d'analyse sont calculés automatiquement et ne peuvent pas être modifiés manuellement. Voir [Comprendre l'analyse client](customer-analytics.md) pour plus de détails.

## Créer un compte client

Les commerçants peuvent créer manuellement des comptes clients pour les commandes par téléphone, les retraits en magasin ou pour les clients wholesale à pré-enregistrer.

1. Cliquez sur **+ Ajouter un profil client** en haut à droite
2. Remplissez les champs requis et optionnels:

| Champ | Obligatoire | Description |
|-------|-------------|-------------|
| **Utilisateur** | Oui | Sélectionnez un compte utilisateur existant ou créez un nouveau compte |
| **Téléphone** | Non | Numéro de téléphone du client |
| **Date de naissance** | Non | Pour la vérification d'âge et les campagnes d'anniversaire |
| **Abonné au bulletin d'information** | Non | Abonnez le client aux bulletins d'information |
| **E-mails de marketing** | Non | Abonnez le client aux e-mails de marketing |

### Créer un nouveau compte utilisateur en ajoutant un profil

Si le client n'a pas encore de compte utilisateur:
1. Cliquez sur l'icône **+** à côté du champ Utilisateur
2. Entrez l'**adresse e-mail** du client (cela devient son nom d'utilisateur)
3. Entrez optionnellement le **prénom** et le **nom de famille**
4. Entrez optionnellement un **mot de passe**
5. Cochez **Envoyer un e-mail de réinitialisation du mot de passe** si vous n'avez pas défini de mot de passe
6. Enregistrez le compte utilisateur
7. Terminez les champs du profil client
8. Cliquez sur **Enregistrer**

### E-mails de bienvenue

Après avoir créé un compte client:
- Si vous avez défini un mot de passe, le client peut se connecter immédiatement avec ce mot de passe
- Si vous n'avez pas défini de mot de passe, le système envoie un e-mail de réinitialisation du mot de passe afin que le client puisse définir son propre mot de passe
- Vous pouvez déclencher manuellement un e-mail de bienvenue via le système d'e-mail à **Marketing > Campagnes d'e-mail**

## Modifier les informations client

Pour mettre à jour les détails du client:
1. Accédez à **Clients > Tous les clients**
2. Cliquez sur le nom du client
3. Modifiez les champs que vous souhaitez mettre à jour
4. Cliquez sur **Enregistrer**

### Ce que vous pouvez modifier

**Détails de contact**:
- Nom (via le compte utilisateur)
- Adresse e-mail (via le compte utilisateur)
- Numéro de téléphone
- Date de naissance

**Préférences**:
- Statut d'abonnement au bulletin d'information
- Abonnement aux e-mails de marketing
- Préférences de notification de commande
- Disposition du tableau de bord et paramètres de visibilité

### Ce que vous ne pouvez pas modifier

Ces champs sont calculés automatiquement en fonction du comportement du client:
- Montant total dépensé / Valeur client
- Nombre de commandes
- Segment client (Champion, Fidèle, En risque, etc.)
- Scores RFM
- Prédictions de valeur à vie
- Date de dernière commande
- Résumés d'analyse

Si ces champs semblent incorrects, vérifiez les données de commande sous-jacentes ou déclenchez un recalcul manuel à **Clients > Analyse** → **Recalculer les métriques**.

## Notes clients

Ajoutez des notes internes sur les clients pour suivre les problèmes de support, les demandes VIP ou les tâches de suivi.

### Ajouter une note

1. Ouvrez le profil du client
2. Faites défiler jusqu'à la section **Notes clients** (peut être un onglet séparé)
3. Cliquez sur **+ Ajouter une note**
4. Remplissez les détails de la note:

| Champ | Description |
|-------|-------------|
| **Type de note** | Générale, Problème de support, Plainte, Éloges, Service VIP, Suivi nécessaire, Problème de paiement, Problème d'expédition |
| **Titre** | Résumé court de la note |
| **Contenu** | Contenu détaillé de la note |
| **Nécessite un suivi** | Cochez si cela nécessite une action |
| **Date de suivi** | Date de suivi |
| **Terminé** | Cochez quand le suivi est terminé |

### Types de notes

| Type | Cas d'utilisation |
|------|------------------|
| **Note générale** | Toute observation générale sur le client |
| **Problème de support** | Enregistrement d'un ticket de support ou d'un problème |
| **Plainte** | Plainte client pour suivi et résolution |
| **Éloges** | Feedback positif sur le client ou son feedback sur vous |
| **Service VIP** | Demandes de traitement spécial pour les clients VIP |
| **Suivi nécessaire** | Tâches nécessitant une action d'ici une date spécifique |
| **Problème de paiement** | Notes sur les problèmes de paiement ou les litiges |
| **Problème d'expédition** | Notes sur les problèmes d'expédition ou les demandes d'expédition spéciales |

### Historique des notes

Toutes les notes apparaissent dans l'ordre chronologique sur le profil du client. Chaque note affiche:
- Date et heure de création
- Créé par (nom du membre du personnel)
- Badge de type de note
- Titre et contenu
- Statut de suivi si applicable

### Notes internes vs notes visibles par le client

Toutes les notes client sont **internes uniquement** par défaut — les clients ne voient jamais ces notes. Elles sont destinées uniquement à la communication au sein de l'équipe commerciale.

Si vous avez besoin de communiquer avec le client, utilisez le système d'e-mail à **Marketing > Campagnes d'e-mail** ou ajoutez un commentaire à l'ordre spécifique.

## Conversion d'un client invité en client enregistré

Les clients invités sont créés automatiquement lorsqu'une personne termine le paiement sans créer de compte. Leur nom d'utilisateur suit le modèle `guest_10374` où le nombre est un identifiant unique.

Pour convertir un client invité en client enregistré:

1. Accédez à **Clients > Tous les clients**
2. Recherchez l'invité par son adresse e-mail de commande
3. Cliquez sur le profil du client invité
4. Cliquez sur le lien **Utilisateur** pour modifier le compte utilisateur sous-jacent
5. Changez le **nom d'utilisateur** de `guest_10374` en l'adresse e-mail réelle du client
6. Changez l'**e-mail** pour correspondre
7. Ajoutez optionnellement le **prénom** et le **nom de famille**
8. Cochez **Envoyer un e-mail de réinitialisation du mot de passe** afin que le client puisse définir un mot de passe
9. Cliquez sur **Enregistrer**

Le client peut maintenant se connecter avec son adresse e-mail et verra ses anciennes commandes en tant qu'invité dans son historique de commandes.

### Pourquoi convertir les clients invités ?

- Les commandes d'invités ne comptent pas dans les analyses client ou les segments
- Les invités ne peuvent pas suivre les commandes ou accéder à l'historique des commandes
- La conversion d'invités augmente le nombre de clients enregistrés et améliore la précision des analyses
- Les clients enregistrés sont plus enclins à effectuer des achats répétés

## Désactivation vs suppression de comptes

### Désactiver un compte client

La désactivation empêche la connexion tout en préservant toutes les données:

1. Ouvrez le profil du client
2. Cliquez sur le lien **Utilisateur** pour modifier le compte utilisateur
3. **Décochez "Actif"**
4. Cliquez sur **Enregistrer**

**Ce qui se produit :**
- Le client ne peut pas se connecter
- L'historique des commandes est préservé
- Le client peut être réactivé ultérieurement en cochant à nouveau "Actif"
- Les analyses et les métriques restent intactes

**Utilisez la désactivation pour :**
- Suspendre temporairement des comptes en raison de litiges de paiement
- Bloquer les clients abusifs
- Clients qui ont demandé d'arrêter de recevoir l'accès sans supprimer les données

### Supprimer un compte client

La suppression supprime le compte et peut orphéiner l'historique des commandes:

1. Ouvrez le profil du client
2. Faites défiler jusqu'en bas et cliquez sur **Supprimer**
3. Confirmez la suppression

**Ce qui se produit :**
- Le compte client est définitivement supprimé
- Le profil client est supprimé
- L'historique des commandes peut être orphelin (les commandes existent mais ne sont pas liées à un client)
- Ne peut pas être annulé

**Utilisez la suppression pour :**
- Demandes de suppression de données GDPR/CCPA (exportez les données en premier)
- Comptes de test qui ne devaient jamais exister
- Comptes dupliqués créés par erreur

### Conformité au RGPD

Avant de supprimer un compte client en réponse à une demande RGPD:

1. Accédez à **Clients > Tous les clients**
2. Sélectionnez le client
3. Utilisez l'action **Exporter les données** pour générer une exportation complète des données
4. Envoyez l'export au client s'il l'a demandé
5. Puis procédez à la suppression

L'export inclut : profil client, historique des commandes, adresses, notes et données d'analyse.

## Conseils

- **Utilisez les filtres pour identifier les clients à haute valeur** — Filtrez par Valeur client pour trouver vos Champions et VIP
- **Révisez régulièrement les notes clients** — Vérifiez les tâches de suivi ouvertes au moins une fois par semaine
- **Ne modifiez pas manuellement les analyses** — Laissez le système calculer automatiquement les scores RFM et les segments
- **Convertissez proactivement les clients invités** — Après qu'un client invité effectue un deuxième achat, contactez-le et proposez de créer un compte correct
- **Utilisez la désactivation plutôt que la suppression** — La désactivation préserve les données et peut être inversée si nécessaire
- **Ajoutez des notes pendant les appels de support** — Documentez les interactions de support pour que les autres membres de l'équipe aient le contexte
- **Définissez des dates de suivi** — Utilisez le système de tâches de suivi dans les notes pour garantir qu'aucune tâche ne se perde
- **Respectez les préférences de communication** — Ne jamais envoyer d'e-mails de marketing aux clients qui ont opté pour l'abandon

