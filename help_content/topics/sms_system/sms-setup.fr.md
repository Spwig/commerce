---
title: Configuration du fournisseur SMS
---

Les notifications SMS permettent d'informer vos clients à chaque étape de leur commande — de la confirmation jusqu'à la livraison. Pour envoyer des SMS ou des messages WhatsApp depuis votre boutique, vous devez connecter un compte de fournisseur SMS avec vos identifiants. Une fois connecté, Spwig utilise ce compte pour envoyer tous les messages texte sortants.

Accédez à **Système SMS > Comptes de fournisseurs SMS** pour gérer vos fournisseurs SMS.

![Liste des comptes de fournisseurs SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Ajout d'un fournisseur SMS

Vous pouvez ajouter un fournisseur en utilisant soit le **Assistant d'installation** (recommandé pour la première configuration) soit le formulaire manuel.

### Utilisation de l'assistant d'installation

1. Accédez à **Système SMS > Comptes de fournisseurs SMS**
2. Cliquez sur **Assistant d'installation** dans la barre d'outils
3. Suivez les étapes guidées :
   - **Étape 1** : Choisissez votre fournisseur dans la liste des fournisseurs disponibles
   - **Étape 2** : Entrez vos identifiants du fournisseur (clés API, SID de compte, etc.)
   - **Étape 3** : Définissez le nom d'affichage et les paramètres par défaut, puis enregistrez
4. L'assistant teste automatiquement la connexion avant l'enregistrement

### Ajout d'un fournisseur manuellement

1. Accédez à **Système SMS > Comptes de fournisseurs SMS**
2. Cliquez sur **Parcourir les fournisseurs** pour explorer les fournisseurs SMS disponibles, ou cliquez directement sur **+ Ajouter un compte de fournisseur SMS**
3. Dans le champ **Fournisseur**, sélectionnez votre fournisseur SMS dans le menu déroulant
4. Une fois que vous avez sélectionné un fournisseur, les champs d'identifiants apparaissent automatiquement en fonction des exigences de ce fournisseur
5. Remplissez les champs d'identifiants requis (ces champs varient selon le fournisseur — consultez les sections ci-dessous pour les fournisseurs courants)
6. Entrez un **Nom d'affichage** pour identifier ce compte (ex. `Twilio — Principal`)
7. Définissez les **Paramètres par défaut** (voir ci-dessous)
8. Cliquez sur **Enregistrer**

## Identifiants du fournisseur

### Twilio

| Champ | Où le trouver |
|-------|-----------------|
| SID de compte | Console Twilio → Tableau de bord |
| Jeton d'authentification | Console Twilio → Tableau de bord |
| Numéro d'appel | Votre numéro de téléphone Twilio au format E.164 (ex. `+15551234567`) |

### Autres fournisseurs

D'autres composants de fournisseurs SMS installés afficheront leurs propres champs d'identifiants spécifiques lorsqu'ils sont sélectionnés. Référez-vous à la documentation de votre fournisseur pour les valeurs exactes nécessaires — généralement une clé API ou un jeton d'accès et un identifiant d'expéditeur.

## Paramètres par défaut

Après avoir entré les identifiants, configurez la manière dont ce compte sera utilisé :

- **Actif** — activez ou désactivez ce compte. Les comptes inactifs ne sont pas utilisés pour l'envoi, même s'ils sont définis comme par défaut
- **Compte SMS par défaut** — lorsqu'il est coché, tous les notifications SMS de votre boutique utiliseront ce compte. Un seul compte peut être le compte SMS par défaut à la fois
- **Compte WhatsApp par défaut** — si ce fournisseur prend en charge WhatsApp (ex. Twilio via l'API WhatsApp Business), cochez cette case pour l'utiliser comme compte par défaut pour les messages WhatsApp

## Test de la connexion

Après avoir enregistré un compte de fournisseur, testez que les identifiants fonctionnent :

1. Accédez à **Système SMS > Comptes de fournisseurs SMS**
2. Cliquez sur votre compte de fournisseur pour l'ouvrir
3. Cliquez sur le bouton **Tester la connexion**
4. Spwig envoie une demande de test au fournisseur et met à jour le champ **Statut de la connexion**

| Statut | Signification |
|--------|---------|
| Connecté | Les identifiants sont valides et le fournisseur est accessible |
| Échec de la connexion | Les identifiants sont incorrects ou le fournisseur n'est pas accessible |
| Non testé | La connexion n'a pas encore été testée |

Si le test échoue, vérifiez à nouveau vos identifiants et assurez-vous que votre compte dispose des autorisations nécessaires sur le tableau de bord du fournisseur.

## Colonne du statut de connexion

La liste des comptes de fournisseurs SMS affiche un badge **Connexion** coloré pour chaque compte :

- **Connecté** (vert) — le compte fonctionne
- **Échec de la connexion** (rouge) — les identifiants ont échoué — mettez-les à jour
- **Non testé** (gris) — le compte n'a pas encore été testé

## Conseils

- Utilisez l'Assistant d'installation pour votre premier fournisseur — il vous guide à travers chaque champ et teste la connexion avant l'enregistrement
- Un seul compte peut être le Compte SMS par défaut à la fois.

Si vous ajoutez un deuxième compte et que vous le marquez comme par défaut, le compte par défaut précédent est automatiquement désactivé
- Notez vos identifiants API du fournisseur dans un endroit sécurisé.

Si les identifiants changent, mettez-les à jour ici immédiatement pour éviter les notifications échouées
- Les comptes inactifs restent dans la liste mais ne sont pas utilisés pour l'envoi — utile pour conserver des identifiants de secours sans les activer
- La plupart des fournisseurs facturent par message envoyé — surveillez l'utilisation dans le tableau de bord de votre fournisseur pour éviter des factures inattendues