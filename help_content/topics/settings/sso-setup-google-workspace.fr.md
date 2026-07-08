---
title: 'Configuration de l''authentification unique (SSO) : Google Workspace'
---

Ce guide vous guide à travers la connexion de Spwig à Google Workspace pour l'authentification unique (SSO) des administrateurs. Une fois configuré, votre personnel pourra se connecter au panneau d'administration Spwig à l'aide de leur compte Google Workspace.

**Remarque :** Google peut mettre à jour l'interface du Cloud Console au fil du temps. Ces instructions ont été rédigées sur la base de l'interface telle qu'elle était en début d'année 2026. Si certaines étapes diffèrent de ce que vous voyez, faites référence à la documentation officielle de Google sur [la configuration d'OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Prérequis

- Un abonnement Google Workspace (Google Workspace Business, Enterprise ou Education)
- Un accès administrateur au [Google Cloud Console](https://console.cloud.google.com)
- L'URL de votre boutique Spwig (par exemple, `https://your-store.com`)
- Les membres du personnel doivent avoir des adresses e-mail dans Spwig correspondant à leurs comptes Google Workspace

## Étape 1 : Créer ou sélectionner un projet Google Cloud

1. Accédez au [Google Cloud Console](https://console.cloud.google.com)
2. Cliquez sur le sélecteur de projet dans la barre supérieure
3. Cliquez sur **Nouveau projet** (ou sélectionnez un projet existant si vous le souhaitez)
4. Entrez un nom de projet (par exemple, `Spwig SSO`)
5. Sélectionnez votre organisation
6. Cliquez sur **Créer**

## Étape 2 : Configurer l'écran de consentement OAuth

1. Dans le Cloud Console, accédez à **APIs & Services > OAuth consent screen**
2. Sélectionnez **Internal** comme type d'utilisateur — cela restreint la connexion aux utilisateurs de votre organisation Google Workspace
3. Cliquez sur **Créer**
4. Remplissez les champs requis :

| Champ | Valeur |
|-------|-------|
| **Nom de l'application** | `Spwig Admin` (ou le nom de votre boutique) |
| **E-mail du support utilisateur** | Votre adresse e-mail d'administrateur |
| **Domaines autorisés** | `your-store.com` (le domaine de votre boutique, sans `https://`) |
| **E-mail de contact du développeur** | Votre adresse e-mail d'administrateur |

5. Cliquez sur **Enregistrer et continuer**
6. Sur la page **Scopes**, cliquez sur **Ajouter ou supprimer des scopes** et ajoutez :
   - `openid`
   - `email`
   - `profile`
7. Cliquez sur **Enregistrer et continuer**
8. Vérifiez le résumé et cliquez sur **Retour au tableau de bord**

## Étape 3 : Créer des identifiants OAuth

1. Accédez à **APIs & Services > Credentials**
2. Cliquez sur **Créer des identifiants > OAuth client ID**
3. Configurez le client :

| Champ | Valeur |
|-------|-------|
| **Type d'application** | Application web |
| **Nom** | `Spwig SSO` |
| **URLs de redirection autorisées** | `https://your-store.com/oidc/callback/` |

4. Cliquez sur **Créer**
5. Une fenêtre affiche votre **Client ID** et **Client Secret** — copiez les deux valeurs. Vous pouvez également les télécharger au format JSON pour les conserver en toute sécurité.

**Important :** L'URL de redirection doit correspondre exactement à `https://your-store.com/oidc/callback/` — y compris la barre oblique finale et le schéma `https://`. Remplacez `your-store.com` par le domaine réel de votre boutique.

## Étape 4 : Obtenir l'URL de découverte

Google utilise une seule URL de découverte standard pour tous les locataires Workspace :

```
https://accounts.google.com/.well-known/openid-configuration
```

Cette URL est la même pour toutes les organisations Google Workspace — vous n'avez pas besoin de la personnaliser avec un locataire ou un domaine.

## Étape 5 : Configurer dans Spwig

1. Dans l'administration Spwig, accédez à **Enterprise SSO > Configuration du fournisseur SSO**
2. Définissez **Nom du fournisseur** sur `Google Workspace`
3. Entrez l'URL de découverte : `https://accounts.google.com/.well-known/openid-configuration`
4. Cliquez sur **Découvrir automatiquement** — cela remplira automatiquement tous les champs d'extrémité
5. Entrez le **Client ID** de l'étape 3
6. Entrez le **Client Secret** de l'étape 3
7. Cliquez sur **Enregistrer**

### Mappage des revendications

Google utilise des noms de revendications OIDC standard, donc la configuration par défaut de Spwig fonctionne directement :

| Paramètre Spwig | Revendication Google | Valeur par défaut |
|---------------|-------------|---------------|
| Revendication e-mail | `email` | `email` |
| Revendication prénom | `given_name` | `given_name` |
| Revendication nom de famille | `family_name` | `family_name` |

Aucun changement au mappage des revendications n'est nécessaire.

## Étape 6 : Activer et tester

1.

Accédez à **Paramètres du site > Onglet Sécurité**
2.

Cochez **Activer le SSO pour la connexion administrateur**
3.

Cliquez sur **Enregistrer**
4.

Conservez tous les formats de mise en forme Markdown, les chemins d'image, les blocs de code et les termes techniques.

Ouvrez la page de connexion de l'admin dans une **fenêtre privée/incognito**
5.

Vous devriez voir un bouton **Se connecter avec Google Workspace**
6.

Cliquez dessus — vous devriez être redirigé vers la page de connexion de Google
7.

Connectez-vous avec un compte Google Workspace dont l'adresse e-mail correspond à un utilisateur du personnel dans Spwig
8.

Vous devriez être redirigé vers le tableau de bord d'administration de Spwig

## Cartographie des rôles basée sur les groupes

Contrairement à Microsoft Entra ID ou Okta, Google ne comprend pas par défaut l'appartenance aux groupes dans les jetons OIDC standard. L'implémentation des revendications de groupe avec Google nécessite l'API de répertoire Google Workspace et une configuration supplémentaire au-delà de l'OIDC basique.

Pour la plupart des déploiements Google Workspace, nous recommandons de gérer directement le statut de personnel et de superutilisateur dans Spwig plutôt que par le biais d'une cartographie automatique des rôles :

1. Créez des comptes de personnel dans Spwig avec les autorisations appropriées
2. Utilisez le système de rôles de personnel de Spwig pour contrôler les niveaux d'accès
3. Le personnel se connecte via SSO, et Spwig utilise leurs autorisations existantes

Si vous avez besoin d'une cartographie automatique des rôles basée sur les groupes, consultez la [documentation de l'API de répertoire Admin SDK de Google Workspace](https://developers.google.com/admin-sdk/directory) pour configurer des revendications personnalisées.

## Problèmes courants

| Problème | Cause | Solution |
|---------|-------|----------|
| **Erreur 400 : redirect_uri_mismatch** | L'URI de redirection dans Google Cloud ne correspond pas exactement | Vérifiez que l'URI de redirection est `https://your-store.com/oidc/callback/` avec la barre oblique finale. Vérifiez HTTP contre HTTPS. |
| **Erreur 403 : access_denied** | L'utilisateur n'appartient pas à l'organisation Google Workspace | Avec le type d'utilisateur "Internal", seuls les utilisateurs de votre organisation peuvent se connecter. Vérifiez que le compte de l'utilisateur fait partie de votre domaine Workspace. |
| **L'écran de consentement OAuth affiche "Cette application n'est pas vérifiée"** | Normal pour les applications internes | Ce avertissement est attendu pour les applications internes et n'affecte pas le fonctionnement. Les utilisateurs de votre organisation peuvent toujours se connecter. |
| **La connexion réussit chez Google mais échoue chez Spwig** | Aucun utilisateur correspondant dans Spwig | Assurez-vous qu'un compte de personnel existe dans Spwig avec la même adresse e-mail que le compte Google Workspace. Vérifiez que "Restreindre aux employés" est configuré correctement. |
| **"Accès bloqué : Cette demande de l'application est invalide"** | Les portées ne sont pas correctement configurées | Vérifiez que les portées `openid`, `email` et `profile` ont été ajoutées à l'écran de consentement OAuth. |

## Conseils

- **Utilisez le type d'utilisateur "Internal"** — cela restreint la connexion à votre organisation Google Workspace et n'exige pas le processus de vérification de l'application de Google.
- **Les secrets client Google ne expirent pas** — contrairement à Microsoft Entra ID, les secrets client OAuth de Google n'ont pas de date d'expiration. Cependant, vous pouvez les renouveler à tout moment depuis la page des informations d'identification.
- **Un projet pour plusieurs applications** — vous pouvez créer plusieurs ID client OAuth dans le même projet Google Cloud si vous avez plusieurs installations de Spwig.
- **Testez avec un compte non administrateur** — créez un compte de test de personnel dans Spwig et utilisez un utilisateur Google Workspace normal (non administrateur) pour vérifier que le SSO fonctionne comme prévu.