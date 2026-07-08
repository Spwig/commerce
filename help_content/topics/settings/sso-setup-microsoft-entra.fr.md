---
title: 'Configuration de SSO : Microsoft Entra ID'
---

Ce guide vous guide à travers la connexion de Spwig à Microsoft Entra ID (anciennement Azure Active Directory) pour le single sign-on des administrateurs. Une fois configuré, votre personnel pourra se connecter au panneau d'administration Spwig à l'aide de leur compte de travail Microsoft.

**Remarque :** Microsoft peut mettre à jour l'interface du centre d'administration Entra au fil du temps. Ces instructions ont été rédigées sur la base de l'interface telle qu'elle était en début d'année 2026. Si certaines étapes diffèrent de ce que vous voyez, faites référence à la documentation officielle de Microsoft sur [l'enregistrement d'une application avec la plateforme d'identité Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Prérequis

- Un abonnement Azure avec accès à Microsoft Entra ID
- Rôle **Administrateur d'application** ou **Administrateur global** dans votre locataire Entra ID
- Votre URL de magasin Spwig (ex. : `https://your-store.com`)
- Les membres du personnel doivent avoir des adresses e-mail dans Spwig correspondant à leurs comptes Microsoft

## Étape 1 : Enregistrer une application

1. Connectez-vous au [centre d'administration Microsoft Entra](https://entra.microsoft.com)
2. Accédez à **Identity > Applications > App registrations**
3. Cliquez sur **New registration**
4. Configurez l'enregistrement :

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO` (ou tout autre nom que vous préférez) |
| **Supported account types** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Cliquez sur **Register**

**Important :** L'URI de redirection doit correspondre exactement à `https://your-store.com/oidc/callback/` — y compris la barre oblique finale. Remplacez `your-store.com` par votre domaine de magasin réel.

## Étape 2 : Noter les identifiants de l'application

Après l'enregistrement, vous verrez la page **Overview** de l'application. Notez ces deux valeurs — vous en aurez besoin plus tard :

| Value | Where to Find It | What It's For |
|-------|-----------------|---------------|
| **Application (client) ID** | Overview page, top section | Entrez-le comme **Client ID** dans Spwig |
| **Directory (tenant) ID** | Overview page, top section | Utilisé pour construire l'URL de découverte |

## Étape 3 : Créer un secret client

1. Dans l'enregistrement de l'application, accédez à **Certificates & secrets**
2. Cliquez sur **New client secret**
3. Entrez une description (ex. : `Spwig SSO`) et choisissez une période d'expiration
4. Cliquez sur **Add**
5. **Copiez immédiatement la valeur** — elle n'est affichée qu'une seule fois. C'est le secret client que vous entrerez dans Spwig.

**Ne copiez pas l'ID du secret** — vous avez besoin de la **colonne Valeur**, pas de la colonne ID.

**Fixez un rappel** pour renouveler le secret avant son expiration. Lorsqu'un secret expire, le SSO cesser de fonctionner jusqu'à ce que vous en créez un nouveau et que vous le mettiez à jour dans Spwig.

## Étape 4 : Configurer les autorisations API

1. Accédez à **API permissions**
2. Vérifiez que **Microsoft Graph > User.Read** (délégué) est listé. Cela est ajouté par défaut.
3. Si les autorisations `openid`, `email` et `profile` ne sont pas listées, cliquez sur **Add a permission > Microsoft Graph > Delegated permissions** et ajoutez-les.
4. Cliquez sur **Grant admin consent for [your organization]** si cela vous est demandé.

## Étape 5 : Construire l'URL de découverte

L'URL de découverte OIDC suit ce format :

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Remplacez `{tenant-id}` par l'**ID de répertoire (locataire)** de l'étape 2.

Exemple : si votre ID de locataire est `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, l'URL de découverte est :

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Étape 6 : Configurer les revendications de groupe (facultatif)

Si vous souhaitez que Spwig attribue automatiquement le statut de personnel ou de superutilisateur en fonction de l'appartenance à un groupe Entra ID :

1. Dans l'enregistrement de l'application, accédez à **Token configuration**
2. Cliquez sur **Add groups claim**
3. Sélectionnez les types de groupes à inclure (généralement **Security groups**)
4. Sous **Customize token properties by type**, pour le **ID** token, sélectionnez **Group ID**
5. Cliquez sur **Add**

**Important:** Entra ID envoie les **Object IDs** (UUIDs comme `a1b2c3d4-...`) des groupes, et non les noms d'affichage des groupes.

Lors de la configuration de la carte des rôles dans Spwig, vous devez utiliser ces Object IDs.

Pour trouver l'Object ID d'un groupe :
1. Dans le centre d'administration Entra, allez à **Identity > Groups > All groups**
2. Cliquez sur le groupe
3. Copiez le **Object ID** depuis la page d'aperçu du groupe

### Limitation des groupes

Microsoft Entra ID inclut un maximum de **200 groupes** dans le jeton. Si un utilisateur appartient à plus de 200 groupes, l'affirmation de groupe est remplacée par un lien vers l'API Microsoft Graph. Pour les organisations avec de nombreux groupes, envisagez de créer un groupe de sécurité dédié pour l'accès à Spwig et d'utiliser [le filtrage des groupes](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) pour limiter les groupes inclus.

## Étape 7 : Configurer dans Spwig

1. Dans l'administration Spwig, accédez à **Enterprise SSO > Configuration du fournisseur SSO**
2. Définissez **Nom du fournisseur** sur `Microsoft Entra ID`
3. Collez l'URL de découverte depuis l'étape 5 dans **URL de découverte OIDC**
4. Cliquez sur **Découvrir automatiquement** — cela remplira automatiquement tous les champs de point de terminaison
5. Entrez l'**ID client** de l'étape 2
6. Entrez le **Secret client** (la valeur) de l'étape 3
7. Si vous avez configuré des affirmations de groupe dans l'étape 6 :
   - Définissez **Affirmation de groupe** sur `groups`
   - Dans **Groupes du personnel**, entrez les Object IDs des groupes dont les membres doivent être des employés (séparés par des virgules)
   - Dans **Groupes administrateurs**, entrez les Object IDs des groupes dont les membres doivent être des administrateurs (séparés par des virgules)
8. Cliquez sur **Enregistrer**

## Étape 8 : Activer et tester

1. Accédez à **Paramètres du site > Onglet Sécurité**
2. Cochez **Activer le SSO pour la connexion administrateur**
3. Cliquez sur **Enregistrer**
4. Ouvrez la page de connexion administrateur dans une **fenêtre privée/incognito**
5. Vous devriez voir un bouton **Se connecter avec Microsoft Entra ID**
6. Cliquez dessus — vous devriez être redirigé vers la page de connexion Microsoft
7. Connectez-vous avec un compte Microsoft dont l'adresse e-mail correspond à un utilisateur employé dans Spwig
8. Vous devriez être redirigé vers le tableau de bord administrateur de Spwig

## Problèmes courants

| Problème | Cause | Solution |
|---------|-------|----------|
| **AADSTS50011 : L'URI de redirection ne correspond pas** | L'URI de redirection dans Entra ne correspond pas exactement | Vérifiez que l'URI de redirection est `https://your-store.com/oidc/callback/` avec la barre oblique finale. Vérifiez les écarts entre HTTP et HTTPS. |
| **AADSTS700016 : Application non trouvée** | ID client incorrect ou locataire | Vérifiez à nouveau l'ID client et que l'URL de découverte utilise l'ID de locataire correct |
| **La connexion réussit chez Microsoft mais échoue chez Spwig** | Aucun utilisateur correspondant dans Spwig | Assurez-vous qu'un compte employé existe dans Spwig avec la même adresse e-mail que le compte Microsoft. Vérifiez que l'utilisateur a le statut employé si l'option « Restreindre aux employés » est activée. |
| **L'affirmation de groupe est vide** | Les affirmations de groupe ne sont pas configurées | Suivez l'étape 6 pour ajouter une affirmation de groupe à la configuration du jeton |
| **L'affirmation de groupe renvoie une URL au lieu des IDs** | L'utilisateur appartient à plus de 200 groupes | Utilisez le filtrage des groupes pour limiter les groupes dans le jeton, ou affectez des groupes spécifiques |
| **Le SSO cesse de fonctionner après quelques mois** | Le secret client a expiré | Créez un nouveau secret client dans Entra et mettez-le à jour dans la configuration du fournisseur SSO de Spwig |

## Conseils

- **Utilisez des groupes de sécurité** pour la carte des rôles, et non les groupes Microsoft 365 ou les listes de distribution.

Les groupes de sécurité sont conçus pour le contrôle d'accès et fonctionnent le plus efficacement avec les affirmations OIDC.
- **Un seul locataire est recommandé** — en sélectionnant « Comptes de ce seul répertoire organisationnel » vous restreignez le SSO aux utilisateurs de votre organisation.

Les configurations multilocataires nécessitent une validation supplémentaire.
- **Définissez une expiration longue du secret** — choisissez 24 mois lors de la création du secret client, et configurez un rappel de calendrier à 22 mois pour le renouveler.
- **Accès conditionnel** — vous pouvez créer des politiques d'accès conditionnel dans Entra ID qui s'appliquent spécifiquement à l'enregistrement de l'application Spwig.


Par exemple, exiger la MFA, bloquer la connexion depuis des emplacements non fiables ou exiger des appareils conformes.
- **Tester avec un compte non administrateur** — créer un compte personnel de test dans Spwig pour vérifier que la SSO fonctionne avant de le déployer auprès de toute votre équipe.