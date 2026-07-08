---
title: Authentification unique (SSO) pour l'administration
---

L'authentification unique (SSO) permet à votre personnel de se connecter au panneau d'administration en utilisant votre fournisseur d'identité organisationnel au lieu d'un nom d'utilisateur et d'un mot de passe distincts. Spwig prend en charge tout fournisseur d'identité utilisant le protocole OpenID Connect (OIDC), notamment Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak et d'autres.

## Qu'est-ce que l'authentification unique d'entreprise ?

L'authentification unique d'entreprise diffère de la connexion sociale (connexion avec un compte Google ou Facebook personnel). Avec l'authentification unique d'entreprise :

- Le personnel s'authentifie via votre **fournisseur d'identité organisationnel** — le même système qu'il utilise pour le courriel, les outils internes et d'autres applications professionnelles
- Votre équipe informatique contrôle l'accès de manière centralisée — lorsqu'une personne quitte l'organisation, désactiver son compte sur le fournisseur d'identité révoque immédiatement son accès à Spwig
- L'authentification à deux facteurs (MFA) est appliquée par le fournisseur d'identité, vous offrant une politique de sécurité cohérente pour toutes les applications
- Le personnel n'a pas besoin de se souvenir d'un mot de passe distinct pour Spwig

## Fonctionnement

Lorsque l'authentification unique est activée, la page de connexion administrateur affiche un bouton **Se connecter avec [Fournisseur]**. Le flux d'authentification fonctionne comme suit :

1. Le membre du personnel clique sur le bouton SSO sur la page de connexion Spwig
2. Il est redirigé vers la page de connexion de votre fournisseur d'identité (par exemple, connexion Microsoft)
3. Il s'authentifie auprès du fournisseur d'identité (y compris tout MFA requis par le fournisseur)
4. Le fournisseur d'identité le redirige vers Spwig avec un code d'autorisation sécurisé
5. Spwig échange le code contre les informations utilisateur et crée une session
6. Le membre du personnel arrive sur le tableau de bord administrateur, pleinement authentifié

Cela utilise le protocole **OpenID Connect (OIDC)** standard de l'industrie, qui est pris en charge par la plupart des fournisseurs d'identité d'entreprise.

## Activation de l'authentification unique

L'authentification unique est configurée dans deux endroits :

1. **Paramètres du site > onglet Sécurité** — Activer ou désactiver l'authentification unique et contrôler la visibilité de la connexion par mot de passe
2. **Configuration du fournisseur SSO** — Entrer les détails OIDC de votre fournisseur d'identité

### Étape 1 : Configurer votre fournisseur d'identité

Avant d'activer l'authentification unique dans Spwig, vous devez enregistrer Spwig comme application dans votre fournisseur d'identité. Consultez les guides spécifiques au fournisseur :

- **Microsoft Entra ID** — consultez le guide d'installation Microsoft Entra ID
- **Google Workspace** — consultez le guide d'installation Google Workspace
- **Okta** — consultez le guide d'installation Okta
- **Autres fournisseurs** — tout fournisseur OIDC compatible fonctionne. Enregistrez une application web avec l'URI de redirection `https://your-store.com/oidc/callback/` et consultez la documentation de votre fournisseur pour l'URL de découverte OIDC, l'ID client et le secret client.

### Étape 2 : Configurer le fournisseur SSO dans Spwig

Accédez à la page **Configuration du fournisseur SSO** (liée depuis l'onglet Sécurité ou accessible à **Authentification unique d'entreprise > Configuration du fournisseur SSO** dans le menu latéral de l'administration). Entrez :

1. **Nom du fournisseur** — affiché sur le bouton de connexion (par exemple, "Microsoft Entra ID")
2. **URL de découverte OIDC** — l'URL `.well-known/openid-configuration` de votre fournisseur. Cliquez sur **Découvrir automatiquement** pour remplir automatiquement les champs de point de terminaison.
3. **ID client** et **secret client** — provenant de l'enregistrement de l'application de votre fournisseur d'identité

Le secret client est stocké chiffré et n'est jamais affiché après l'enregistrement.

### Étape 3 : Activer l'authentification unique dans les paramètres du site

Accédez à **Paramètres du site > onglet Sécurité** et cochez **Activer l'authentification unique pour la connexion administrateur**. Le bouton SSO apparaîtra immédiatement sur la page de connexion administrateur.

## Paramètres SSO

| Paramètre | Description |
|---------|-------------|
| **Activer l'authentification unique pour la connexion administrateur** | Affiche le bouton SSO sur la page de connexion administrateur. N'affecte pas la connexion par mot de passe sauf si vous le désactivez également. |
| **Permettre la connexion par mot de passe sur la page administrateur** | Lorsque cette option est décochée, le formulaire de mot de passe est caché derrière un bouton déroulant. Le personnel ne voit que le bouton SSO par défaut. Le formulaire de mot de passe peut toujours être accédé en cliquant sur "Se connecter avec un compte local" ou en ajoutant `?password=1` à l'URL de connexion. |

### Comportement de la page de connexion


| SSO activé | Connexion par mot de passe | Résultat |
|-------------|---------------|--------|
| Off | On | Page de connexion standard avec un formulaire de nom d'utilisateur/mot de passe uniquement |
| On | On | Bouton SSO en haut, séparateur "ou", puis formulaire de mot de passe en dessous |
| On | Off | Bouton SSO uniquement. Le formulaire de mot de passe est derrière un interrupteur "Se connecter avec un compte local" |
| Off | Off | Impossible — la connexion par mot de passe est automatiquement réactivée si SSO est désactivé ou non configuré |

## Correspondance utilisateur

Lorsqu'un membre du personnel se connecte via SSO, Spwig le fait correspondre à un compte utilisateur existant par **adresse e-mail** (insensible à la casse). L'e-mail provenant des revendications du fournisseur d'identité doit correspondre à l'e-mail du compte Spwig du membre du personnel.

Si aucun utilisateur correspondant n'est trouvé :

- **Création automatique des utilisateurs désactivée** (par défaut) — la connexion est refusée. Vous devez créer le compte du personnel dans Spwig en premier avec une adresse e-mail correspondante.
- **Création automatique des utilisateurs activée** — un nouveau compte utilisateur est créé automatiquement avec le nom et l'e-mail provenant des revendications du fournisseur d'identité.

Le paramètre **Restreindre aux membres du personnel** (activé par défaut) ajoute un contrôle supplémentaire : même si un compte utilisateur existe, la connexion est refusée sauf si l'utilisateur a le statut de membre du personnel. Cela empêche les comptes non membres du personnel d'accéder au panneau d'administration via SSO.

## Mappage des rôles

Si votre fournisseur d'identité envoie des informations sur l'appartenance aux groupes dans les revendications OIDC, Spwig peut automatiquement définir le statut de membre du personnel et de superutilisateur en fonction de l'appartenance aux groupes.

Pour configurer le mappage des rôles :

1. Dans la configuration du fournisseur SSO, définissez le champ **Revendication de groupe** sur le nom de revendication utilisé par votre fournisseur (par défaut : `groups`)
2. Dans **Groupes de membres du personnel**, saisissez des noms ou des identifiants de groupes séparés par des virgules. Les utilisateurs appartenant à l'un de ces groupes obtiennent le statut de membre du personnel.
3. Dans **Groupes de superutilisateurs**, saisissez des noms ou des identifiants de groupes séparés par des virgules. Les utilisateurs appartenant à l'un de ces groupes obtiennent le statut de superutilisateur.

Le mappage des rôles est évalué chaque fois qu'un utilisateur se connecte via SSO. Si un utilisateur est retiré d'un groupe par le fournisseur d'identité, son statut de membre du personnel ou de superutilisateur est mis à jour lors de sa prochaine connexion SSO.

**Important** : Microsoft Entra ID envoie par défaut les **identifiants d'objet** (UUID) des groupes, et non les noms de groupes. Copiez l'identifiant d'objet depuis le portail Azure lors de la configuration du mappage des rôles. D'autres fournisseurs comme Okta envoient généralement les noms de groupes.

## Mappage des revendications

Spwig lit les informations utilisateur à partir des revendications OIDC standard. Les paramètres par défaut fonctionnent avec la plupart des fournisseurs, mais vous pouvez personnaliser les noms des champs de revendications dans la configuration du fournisseur SSO :

| Paramètre | Défaut | Description |
|---------|---------|-------------|
| **Revendication e-mail** | `email` | La revendication contenant l'adresse e-mail de l'utilisateur |
| **Revendication prénom** | `given_name` | La revendication contenant le prénom de l'utilisateur |
| **Revendication nom de famille** | `family_name` | La revendication contenant le nom de famille de l'utilisateur |
| **Revendication groupe** | `groups` | La revendication contenant les adhésions aux groupes (laissez vide pour désactiver le mappage des rôles) |

## Comportement MFA

Lorsqu'un membre du personnel se connecte via SSO, la exigence d'authentification à deux facteurs (2FA) intégrée de Spwig est automatiquement contournée. Cela est dû au fait que le fournisseur d'identité est responsable de l'application de l'MFA comme partie du flux de connexion SSO.

Si votre organisation exige l'MFA, configurez-la dans les politiques d'accès conditionnel de votre fournisseur d'identité plutôt que dans les paramètres de 2FA de Spwig. Cela vous permet une gestion centralisée de l'MFA pour toutes vos applications.

## Accès de secours

Si votre fournisseur d'identité rencontre un incident ou une configuration incorrecte, vous pouvez toujours accéder au formulaire de connexion administrateur :

- **Cliquez sur l'interrupteur** — Si la connexion par mot de passe est désactivée, cliquez sur "Se connecter avec un compte local" sur la page de connexion pour afficher le formulaire de mot de passe
- **Paramètre URL** — Ajoutez `?password=1` à l'URL de connexion administrateur (par exemple, `https://your-store.com/en/admin/login/?password=1`) pour afficher directement le formulaire de mot de passe
- **La connexion par mot de passe est toujours disponible** — Même lorsqu'elle est masquée dans l'interface utilisateur, le backend d'authentification par mot de passe reste actif. Seule la visibilité du formulaire est affectée.

Spwig vous empêche également de désactiver l'authentification par mot de passe sauf si l'authentification unique (SSO) est à la fois activée et correctement configurée — vous ne pouvez pas vous bloquer accidentellement vous-même.

## Fournisseurs pris en charge

Spwig fonctionne avec tout fournisseur d'identité qui prend en charge le protocole OpenID Connect (OIDC). Des guides de configuration détaillés sont disponibles pour :

- **Microsoft Entra ID** (anciennement Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Pour d'autres fournisseurs conformes à OIDC (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, etc.), les étapes de configuration de Spwig sont les mêmes — vous avez besoin de l'URL de découverte OIDC du fournisseur, de l'ID client et du secret client. Consultez la documentation de votre fournisseur pour savoir comment enregistrer une application web et obtenir ces identifiants. L'URI de redirection à utiliser est toujours `https://your-store.com/oidc/callback/`.

## Conseils

- **Commencez avec l'authentification par mot de passe activée** — Activez l'authentification unique (SSO) en même temps que l'authentification par mot de passe. Une fois que vous avez confirmé que l'authentification unique fonctionne pour votre équipe, vous pouvez éventuellement désactiver l'authentification par mot de passe.
- **Testez dans une fenêtre incognito** — Utilisez une fenêtre de navigateur privée/incognito pour tester l'authentification unique sans être affecté par votre session d'administrateur actuelle.
- **Créez des comptes d'employés en premier** — À moins que vous n'activiez la création automatique des utilisateurs, les employés ont besoin d'un compte Spwig existant avec une adresse e-mail correspondante avant de pouvoir se connecter via l'authentification unique.
- **Utilisez le bouton Auto-Découvrir** — Entrez l'URL de découverte OIDC de votre fournisseur et cliquez sur Auto-Découvrir pour remplir automatiquement tous les champs d'extrémité. Cela est plus rapide et moins sujette à erreur que d'entrer manuellement les extrémités.
- **Conservez un compte administrateur local** — Maintenez toujours au moins un compte administrateur local avec un mot de passe en tant qu'option de récupération en cas de problème avec le fournisseur d'identité.
- **Surveillez l'expiration du secret client** — Certains fournisseurs (notamment Microsoft Entra ID) émettent des secrets client avec des dates d'expiration. Configurez un rappel dans votre calendrier pour renouveler le secret avant son expiration.