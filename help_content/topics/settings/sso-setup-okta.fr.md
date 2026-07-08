---
title: 'Configuration de SSO : Okta'
---

Ce guide vous guide à travers la connexion de Spwig à Okta pour le single sign-on administrateur. Une fois configuré, votre personnel peut se connecter au panneau d'administration Spwig en utilisant leur compte Okta.

**Remarque :** Okta peut mettre à jour leur interface de console d'administration au fil du temps. Ces instructions ont été rédigées en se basant sur la console d'administration Okta telle qu'elle était en début d'année 2026. Si certaines étapes diffèrent de ce que vous voyez, faites référence à la documentation officielle d'Okta sur [la création d'une intégration d'application OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Prérequis

- Une organisation Okta (n'importe quel niveau — les comptes développeurs gratuits fonctionnent pour les tests)
- Le rôle **Super Administrateur** ou **Administrateur d'application** dans Okta
- Votre URL de magasin Spwig (par exemple, `https://your-store.com`)
- Les membres du personnel doivent avoir des adresses e-mail dans Spwig correspondant à leurs comptes Okta

## Étape 1 : Créer une application

1. Connectez-vous à la [console d'administration Okta](https://your-org-admin.okta.com)
2. Accédez à **Applications > Applications**
3. Cliquez sur **Créer une intégration d'application**
4. Sélectionnez :

| Champ | Valeur |
|-------|-------|
| **Méthode de connexion** | OIDC - OpenID Connect |
| **Type d'application** | Application Web |

5. Cliquez sur **Suivant**

## Étape 2 : Configurer l'application

Remplissez les paramètres de l'application :

| Champ | Valeur |
|-------|-------|
| **Nom de l'intégration d'application** | `Spwig Admin SSO` (ou tout autre nom que vous préférez) |
| **Type de concesssion** | Code d'autorisation (devrait être sélectionné par défaut) |
| **URL de redirection de connexion** | `https://your-store.com/oidc/callback/` |
| **URL de redirection de déconnexion** | `https://your-store.com/en/admin/login/` |
| **Accès contrôlé** | Choisissez selon vos besoins (voir ci-dessous) |

Pour **Accès contrôlé**, choisissez l'une des options suivantes :

- **Permettre à tout le monde dans votre organisation d'accéder** — tous les utilisateurs Okta peuvent se connecter (vous pouvez toujours contrôler l'accès Spwig avec le paramètre Restrict to Staff)
- **Limiter l'accès aux groupes sélectionnés** — uniquement les utilisateurs dans des groupes Okta spécifiques peuvent se connecter
- **Ignorer l'affectation de groupe pour le moment** — vous affecterez manuellement les utilisateurs ou les groupes plus tard

Cliquez sur **Enregistrer**.

**Important :** L'URL de redirection de connexion doit correspondre exactement à `https://your-store.com/oidc/callback/` — y compris la barre oblique finale.

## Étape 3 : Obtenir les identifiants client

Après avoir enregistré, l'onglet **Général** de l'application affiche vos identifiants :

| Valeur | Où le trouver |
|-------|-----------------|
| **Client ID** | Onglet Général, section Identifiants client |
| **Client Secret** | Onglet Général, section Identifiants client (cliquez sur l'icône œil pour l'afficher) |

Copiez les deux valeurs — vous en aurez besoin pour Spwig.

## Étape 4 : Construire l'URL de découverte

L'URL de découverte dépend de votre organisation Okta et de votre serveur d'autorisation :

**Serveur d'autorisation par défaut (le plus courant) :**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**Serveur d'autorisation personnalisé (si configuré) :**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

Remplacez `your-org.okta.com` par votre domaine Okta réel. Vous pouvez trouver votre domaine Okta dans la barre d'URL de la console d'administration ou sous **Settings > Account**.

**Conseil :** La plupart des organisations utilisent le Serveur d'autorisation d'organisation (le par défaut). Utilisez uniquement une URL de serveur d'autorisation personnalisé si votre administrateur Okta en a configuré une spécifiquement.

## Étape 5 : Affecter des utilisateurs ou des groupes

Si vous avez choisi "Ignorer l'affectation de groupe" à l'étape 2, vous devez affecter des utilisateurs avant qu'ils puissent se connecter :

1. Dans l'onglet **Affectations** de l'application, cliquez sur **Affecter**
2. Choisissez **Affecter à des personnes** ou **Affecter à des groupes**
3. Sélectionnez les utilisateurs ou les groupes et cliquez sur **Affecter**
4. Cliquez sur **Terminer**

Les utilisateurs non affectés à l'application verront une erreur lorsqu'ils tenteront de se connecter via SSO.

## Étape 6 : Configurer les revendications de groupe (facultatif)

Si vous souhaitez que Spwig définisse automatiquement le statut de personnel ou de superutilisateur en fonction de l'appartenance aux groupes Okta :

1.

Accédez à **Security > API** dans la console d'administration
2.

Sélectionnez votre **Authorization Server** (utilisez "default" si vous n'avez pas créé un serveur d'autorisation personnalisé, ou le Serveur d'autorisation d'organisation)
3.

Allez à l'onglet **Claims**
4.

Conservez tous les formats de markdown, les chemins d'image, les blocs de code et les termes techniques.

Cliquez sur **Ajouter une revendication**
5.

Configurez la revendication :

| Champ | Valeur |
|-------|-------|
| **Nom** | `groups` |
| **Inclure dans le type de jeton** | ID Token, Always |
| **Type de valeur** | Groups |
| **Filtre** | Correspond à l'expression régulière : `.*` (pour inclure toutes les groupes) |
| **Inclure dans** | Tout scope (ou `openid` si vous souhaitez le limiter) |

6. Cliquez sur **Créer**

**Conseil :** Contrairement à Microsoft Entra ID qui envoie les ID d'objet, Okta envoie par défaut **les noms de groupe**. Cela rend la cartographie des rôles plus intuitive — vous pouvez utiliser directement les noms d'affichage de vos groupes Okta dans les champs Groupes du personnel et Groupes des superutilisateurs de Spwig.

### Filtre des groupes

Si vos utilisateurs appartiennent à de nombreux groupes Okta et que vous souhaitez uniquement inclure certains d'entre eux dans le jeton :

- Modifiez le filtre de `.*` vers une expression régulière plus spécifique, par exemple `^Spwig.*` pour inclure uniquement les groupes commençant par « Spwig »
- Ou utilisez les filtres **Commence par**, **Égal à** ou **Contient** au lieu des expressions régulières

## Étape 7 : Configurer dans Spwig

1. Dans l'administration Spwig, accédez à **Enterprise SSO > Configuration du fournisseur SSO**
2. Définissez **Nom du fournisseur** sur `Okta`
3. Entrez l'URL de découverte provenant de l'étape 4
4. Cliquez sur **Découvrir automatiquement** — cela remplira automatiquement tous les champs d'extrémité
5. Entrez l'**ID client** provenant de l'étape 3
6. Entrez le **Secret client** provenant de l'étape 3
7. Si vous avez configuré des revendications de groupe à l'étape 6 :
   - Définissez **Revendication de groupe** sur `groups`
   - Dans **Groupes du personnel**, entrez les noms des groupes Okta dont les membres doivent être des employés (séparés par des virgules)
   - Dans **Groupes des superutilisateurs**, entrez les noms des groupes Okta dont les membres doivent être des superutilisateurs (séparés par des virgules)
8. Cliquez sur **Enregistrer**

## Étape 8 : Activer et tester

1. Accédez à **Paramètres du site > Onglet Sécurité**
2. Cochez **Activer le SSO pour la connexion administrateur**
3. Cliquez sur **Enregistrer**
4. Ouvrez la page de connexion administrateur dans une **fenêtre privée/incognito**
5. Vous devriez voir un bouton **Se connecter avec Okta**
6. Cliquez dessus — vous devriez être redirigé vers la page de connexion Okta
7. Connectez-vous avec un compte Okta qui est assigné à l'application et dont l'adresse e-mail correspond à un utilisateur du personnel dans Spwig
8. Vous devriez être redirigé vers le tableau de bord administrateur de Spwig

## Problèmes courants

| Problème | Cause | Solution |
|---------|-------|----------|
| **L'URI de redirection n'est pas autorisée** | L'URI de redirection ne correspond pas à la configuration de l'application | Vérifiez que l'URI de redirection vers laquelle on redirige est exactement `https://your-store.com/oidc/callback/` avec la barre oblique finale |
| **L'utilisateur n'est pas assigné à l'application client** | L'utilisateur n'est pas assigné à l'application Okta | Assignez l'utilisateur ou son groupe à l'application dans l'onglet Assignments |
| **La connexion réussit sur Okta mais échoue sur Spwig** | Aucun utilisateur correspondant dans Spwig | Assurez-vous qu'un compte employé existe dans Spwig avec la même adresse e-mail. Vérifiez le paramètre Restrict to Staff. |
| **La revendication de groupe est vide** | La revendication de groupe n'est pas configurée sur le serveur d'autorisation | Suivez l'étape 6 pour ajouter une revendication de groupe. Assurez-vous d'ajouter celle-ci au serveur d'autorisation correct. |
| **Mauvais serveur d'autorisation** | L'URL de découverte utilise un serveur d'autorisation différent de celui où la revendication de groupe est configurée | Vérifiez que l'URL de découverte correspond au serveur d'autorisation sur lequel vous avez configuré la revendication de groupe |
| **« L'ID client fourni est invalide »** | L'ID client ne correspond pas ou l'application est inactive | Vérifiez que l'ID client est correct et que l'état de l'application est Actif dans Okta |

## Conseils

- **Okta envoie les noms de groupe, pas les ID** — cela rend la cartographie des rôles directe.

Entrez exactement le nom d'affichage du groupe (par exemple, `Spwig Admins`) dans les champs Groupes du personnel ou Groupes des superutilisateurs de Spwig.
- **Utilisez l'attribution de groupe pour le contrôle d'accès** — attribuez des groupes Okta spécifiques à l'application Spwig plutôt que d'autoriser tous les utilisateurs.

# Sécuriser l'accès avec Okta

De cette façon, seul le personnel concerné peut se connecter.
- **Les secrets client Okta ne expirent pas par défaut** — mais vous pouvez les renouveler à tout moment depuis l'onglet Général de l'application pour suivre les bonnes pratiques en matière de sécurité.
- **Testez avec un compte non administrateur** — utilisez un utilisateur Okta normal (non super administrateur) affecté à l'application pour vérifier que le SSO fonctionne comme prévu.
- **MFA dans Okta** — configurez la politique de session globale d'Okta ou les politiques d'authentification pour exiger le MFA.

Cela s'appliquera à toutes les connexions SSO vers Spwig sans avoir besoin de configurer le MFA séparément dans Spwig.