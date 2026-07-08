---
title: Configuration de l'authentification OAuth et des connexions sociales
---

OAuth et les connexions sociales permettent aux clients de se connecter à votre magasin en utilisant leurs comptes Google, Apple ou Microsoft existants — aucun besoin de créer et de se souvenir d'un autre mot de passe.

![Paramètres OAuth](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## Qu'est-ce que l'OAuth / la connexion sociale ?

L'OAuth est un standard d'authentification sécurisé qui permet aux clients de se connecter en utilisant des identifiants provenant de fournisseurs de confiance tels que Google, Apple ou Microsoft.

### Avantages

- **Paiement plus rapide** — Les clients sautent le formulaire d'inscription et se connectent avec un seul clic
- **Réduction des frottements** — Aucun création de mot de passe, de courriels de vérification ou de flux de mot de passe oublié
- **Meilleure conversion** — Des études montrent que la connexion sociale peut augmenter les taux de conversion de 20 à 40 %
- **Sécurité renforcée** — Les identifiants ne passent jamais par votre magasin ; l'authentification est gérée par le fournisseur
- **Confiance des clients** — Les clients font confiance aux fournisseurs établis pour leurs identifiants de connexion

### Fonctionnement

1. Le client clique sur "Se connecter avec Google" (ou Apple/Microsoft) sur votre page de connexion
2. Ils sont redirigés vers la page de connexion sécurisée du fournisseur
3. Le client s'authentifie avec ses identifiants du fournisseur
4. Le fournisseur envoie des informations d'identité vérifiées de retour à votre magasin
5. Le client est connecté automatiquement

À la première connexion, un nouveau compte client est créé automatiquement à l'aide de son adresse e-mail et des informations de profil provenant du fournisseur.

## Fournisseurs pris en charge

Spwig prend en charge trois grands fournisseurs OAuth :

| Fournisseur | Cas d'utilisation | Exigences des identifiants |
|-------------|------------------|--------------------------|
| **Google** | Le plus populaire, le plus facile à configurer | ID client, Secret client |
| **Apple** | Requis pour les applications iOS, axé sur la confidentialité | ID client, ID d'équipe, ID de clé, Clé privée |
| **Microsoft** | Clients d'entreprise, utilisateurs de Office 365 | ID client, Secret client, ID de locataire |

Vous pouvez activer un, deux ou les trois fournisseurs. Chacun fonctionne de manière indépendante.

## Configuration de l'OAuth Google

L'OAuth Google est l'option la plus populaire et la plus facile à configurer.

### Prérequis

- Un compte Google
- Accès au Google Cloud Console

### Étapes de configuration

1. **Accédez aux paramètres OAuth**
   - Allez à **Paramètres > Paramètres du magasin** dans votre panneau d'administration
   - Faites défiler jusqu'à la section **Fournisseurs OAuth**
   - Cliquez sur **Configurer Google**

2. **Créez un projet Google Cloud**
   - Visitez [Google Cloud Console](https://console.cloud.google.com/)
   - Cliquez sur **Créer un projet**
   - Entrez un nom de projet (par exemple, "Mon magasin OAuth")
   - Cliquez sur **Créer**

3. **Activez l'API Google+**
   - Dans le menu de gauche, allez à **APIs & Services > Bibliothèque**
   - Recherchez "Google+ API"
   - Cliquez sur **Activer**

4. **Créez des identifiants OAuth**
   - Allez à **APIs & Services > Identifiants**
   - Cliquez sur **Créer des identifiants > ID client OAuth**
   - Sélectionnez le type d'application : **Application web**
   - Entrez un nom (par exemple, "Connexion au magasin")

5. **Configurez l'URI de redirection**
   - Sous **URI de redirection autorisés**, ajoutez :
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Remplacez `yourdomain.com` par votre domaine réel
   - Cliquez sur **Créer**

6. **Copiez les identifiants**
   - Copiez l'**ID client** et le **Secret client** depuis la fenêtre contextuelle

7. **Entrez les identifiants dans Spwig**
   - Retournez aux paramètres OAuth de votre administration Spwig
   - Collez l'ID client et le secret client
   - Cliquez sur **Enregistrer**
   - Activez **Activer l'OAuth Google** en basculant l'interrupteur

### Tests

- Visitez la page de connexion de votre magasin en ligne
- Cherchez le bouton "Se connecter avec Google"
- Cliquez dessus et authentifiez-vous avec votre compte Google
- Vous devriez être connecté et redirigé vers votre tableau de bord client

## Configuration de l'OAuth Apple

L'OAuth Apple est plus complexe que Google en raison de son système d'authentification basé sur les clés.

### Prérequis

- Un compte développeur Apple (adhésion payante requise)
- Accès au portail du développeur Apple

### Étapes de configuration

1. **Accédez aux paramètres OAuth**
   - Allez à **Paramètres > Paramètres du magasin > Fournisseurs OAuth**
   - Cliquez sur **Configurer Apple**

2. **Créez un ID de service**
   - Connectez-vous à [Apple Developer](https://developer.apple.com/account/)
   - Allez à **Certificats, Identifiants & Profils**
   - Cliquez sur **Identifiants** puis sur le bouton **+**
   - Sélectionnez **IDs de service** puis cliquez sur **Continuer**
   - Entrez une description (par exemple, "Connexion au magasin")
   - Entrez un identifiant (par exemple, `com.yourstore.login`)
   - Cliquez sur **Continuer** puis sur **Enregistrer**

3. **Configurez l'ID de service**
   - Cliquez sur votre nouvel ID de service
   - Cochez **Se connecter avec Apple**
   - Cliquez sur **Configurer**
   - Ajoutez votre domaine et l'URL de retour :
     - **Domaines** : `yourdomain.com`
     - **URLS de retour** : `https://yourdomain.com/accounts/apple/login/callback/`
   - Cliquez sur **Enregistrer** puis sur **Continuer** et **Enregistrer** à nouveau

4. **Créez une clé**
   - Dans le menu de gauche, cliquez sur **Clés** puis sur le bouton **+**
   - Entrez un nom de clé (par exemple, "Clé OAuth du magasin")
   - Cochez **Se connecter avec Apple**
   - Cliquez sur **Configurer** et sélectionnez votre ID d'application principal
   - Cliquez sur **Enregistrer**, puis sur **Continuer** et **Enregistrer** à nouveau
   - **Téléchargez le fichier de clé** (.p8) — vous ne pouvez pas le télécharger à nouveau

5. **Collectez les informations nécessaires**
   Vous avez besoin de :
   - **ID client** (ID de service) : L'identifiant que vous avez créé (par exemple, `com.yourstore.login`)
   - **ID d'équipe** : Trouvé en haut à droite du portail du développeur Apple
   - **ID de clé** : Affiché lors de la création de la clé
   - **Clé privée** : Le contenu du fichier .p8 que vous avez téléchargé

6. **Entrez les identifiants dans Spwig**
   - Retournez aux paramètres OAuth de Spwig
   - Collez l'ID client, l'ID d'équipe et l'ID de clé
   - Ouvrez le fichier .p8 dans un éditeur de texte et copiez son contenu
   - Collez l'ensemble de la clé (y compris les en-têtes) dans le champ Clé privée
   - Cliquez sur **Enregistrer**
   - Activez **Activer l'OAuth Apple** en basculant l'interrupteur

### Tests

- Visitez la page de connexion de votre magasin en ligne sur un appareil avec un ID Apple
- Cliquez sur "Se connecter avec Apple"
- Authentifiez-vous avec votre ID Apple
- Vous devriez être connecté avec succès

## Configuration de l'OAuth Microsoft

L'OAuth Microsoft est idéal pour les magasins ciblant des clients d'entreprise qui utilisent Office 365 ou Azure AD.

### Prérequis

- Un compte Microsoft
- Accès au portail Azure

### Étapes de configuration

1. **Accédez aux paramètres OAuth**
   - Allez à **Paramètres > Paramètres du magasin > Fournisseurs OAuth**
   - Cliquez sur **Configurer Microsoft**

2. **Enregistrez une application dans Azure**
   - Visitez [Azure Portal](https://portal.azure.com/)
   - Allez à **Azure Active Directory > Inscriptions des applications**
   - Cliquez sur **Nouvelle inscription**
   - Entrez un nom (par exemple, "OAuth du magasin")
   - Sélectionnez **Comptes dans tout les répertoires organisationnels et comptes Microsoft personnels**
   - Sous **URI de redirection**, sélectionnez **Web** et entrez :
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Cliquez sur **Enregistrer**

3. **Copiez l'ID de l'application**
   - Sur la page d'aperçu de l'application, copiez l'**ID de l'application (client)**

4. **Créez un secret client**
   - Dans le menu de gauche, cliquez sur **Certificats & secrets**
   - Cliquez sur **Nouveau secret client**
   - Entrez une description (par exemple, "Secret OAuth")
   - Sélectionnez une période d'expiration (recommandé : 24 mois)
   - Cliquez sur **Ajouter**
   - **Copiez immédiatement la valeur du secret** — elle ne sera plus affichée

5. **Entrez les identifiants dans Spwig**
   - Retournez aux paramètres OAuth de Spwig
   - Collez l'ID de l'application (client) comme ID client
   - Collez la valeur du secret comme Secret client
   - Entrez éventuellement un ID de locataire (pour les applications à un seul locataire ; laissez vide pour les applications à plusieurs locataires)
   - Cliquez sur **Enregistrer**
   - Activez **Activer l'OAuth Microsoft** en basculant l'interrupteur

### Tests

- Visitez la page de connexion de votre magasin en ligne
- Cliquez sur "Se connecter avec Microsoft"
- Authentifiez-vous avec votre compte Microsoft
- Vous devriez être connecté avec succès

## Gestion des connexions OAuth

### Vue client

Les clients peuvent consulter et gérer leurs fournisseurs OAuth connectés depuis leur tableau de bord du compte :

- Accédez à **Mon compte > Comptes connectés**
- Voyez quels fournisseurs sont liés (Google, Apple, Microsoft)
- Désactivez un fournisseur en cliquant sur **Désactiver**
- Réactivez en vous connectant à nouveau avec ce fournisseur

### Plusieurs fournisseurs

Un seul compte client peut être lié à plusieurs fournisseurs OAuth. Par exemple, un client peut connecter à la fois Google et Apple au même compte.

Si un client tente de se connecter avec un autre fournisseur OAuth en utilisant la même adresse e-mail, Spwig relie automatiquement cela à leur compte existant.

### Gestion par l'administrateur

En tant qu'administrateur, vous pouvez consulter les connexions OAuth des clients :

- Allez à **Clients > Clients**
- Ouvrez le dossier client
- Faites défiler jusqu'à la section **Comptes connectés**
- Consultez quels fournisseurs sont liés et quand ils ont été connectés

Vous ne pouvez pas désactiver les fournisseurs à la place des clients — ils doivent le faire eux-mêmes pour des raisons de sécurité.

## Dépannage

### Mismatch de l'URI de redirection

**Erreur** : "Mismatch de l'URI de redirection" ou "URI de redirection non valide"

**Solution** : 
- Assurez-vous que l'URI de redirection dans vos paramètres du fournisseur correspond exactement à celle dans Spwig
- Vérifiez les barres obliques de fin — elles doivent correspondre
- Vérifiez que vous utilisez `https://` (et non `http://`)
- Videz le cache de votre navigateur et réessayez

### Identifiants invalides

**Erreur** : "ID client invalide" ou "Authentification échouée"

**Solution** : 
- Vérifiez à nouveau que vous avez correctement copié l'ID client et le secret client
- Assurez-vous qu'il n'y a pas d'espaces supplémentaires ou de sauts de ligne
- Vérifiez que les identifiants proviennent du bon projet/appli
- Pour Apple, assurez-vous que la clé privée inclut le contenu complet du fichier .p8

### API du fournisseur non activée

**Erreur** : "API non activée" ou "Accès non configuré"

**Solution** : 
- Pour Google : Assurez-vous que vous avez activé l'API Google+ dans votre projet Google Cloud
- Pour Microsoft : Vérifiez que votre inscription d'application est approuvée et active
- Pour Apple : Vérifiez que "Se connecter avec Apple" est activé pour votre ID de service

### SSL requis

**Erreur** : "L'OAuth nécessite HTTPS" ou "URI de redirection non sécurisée"

**Solution** : 
- Les fournisseurs OAuth exigent SSL/TLS (HTTPS) pour la sécurité
- Assurez-vous que votre magasin a un certificat SSL valide installé
- Mettez à jour vos URI de redirection pour utiliser `https://` au lieu de `http://`
- Si vous testez localement, utilisez un service comme ngrok pour créer un tunnel HTTPS

### Bouton non apparu

**Problème** : Le bouton "Se connecter avec Google/Apple/Microsoft" n'apparaît pas sur la page de connexion

**Solution** : 
- Vérifiez que le fournisseur est activé dans les paramètres OAuth
- Videz le cache de votre navigateur et actualisez la page
- Vérifiez que votre thème inclut le modèle de connexion sociale
- Vérifiez le console du navigateur pour les erreurs JavaScript

## Conseils et bonnes pratiques

### Sécurité

- **Renouvelez les secrets régulièrement** — Mettez à jour les secrets client toutes les 12 à 24 mois
- **Surveillez les tentatives de connexion échouées** — Surveillez les schémas d'authentification inhabituels
- **Utilisez des identifiants séparés par environnement** — Des identifiants différents pour les environnements de test et de production
- **Restreignez les URI de redirection** — Ajoutez uniquement les URI exactement nécessaires

### Expérience utilisateur

- **Activez les trois fournisseurs** — Donnez aux clients un choix ; différentes démographies préfèrent différents fournisseurs
- **Placez les boutons en évidence** — Les boutons de connexion sociale doivent être placés au-dessus du formulaire e-mail/mot de passe
- **Utilisez une marque reconnaissable** — Gardez les styles standard des boutons Google/Apple/Microsoft
- **Testez sur mobile** — Les flux OAuth fonctionnent différemment sur les navigateurs mobiles

### Conformité

- **Politique de confidentialité** — Indiquez que vous utilisez des fournisseurs OAuth et les données que vous recevez
- **Conditions d'utilisation** — Respectez les conditions des fournisseurs (Google, Apple, Microsoft chacun a des exigences)
- **Minimisation des données** — N'appelez que les informations de profil que vous avez réellement besoin

### Liste de vérification des tests

Avant de mettre en ligne, testez :

- [ ] Connexion avec chaque fournisseur sur ordinateur
- [ ] Connexion avec chaque fournisseur sur mobile
- [ ] Connexion pour la première fois (création de compte)
- [ ] Connexions ultérieures (liaison de compte)
- [ ] Connexion avec la même adresse e-mail via différents fournisseurs
- [ ] Désactiver et réactiver un fournisseur
- [ ] Le flux de réinitialisation de mot de passe fonctionne toujours pour les utilisateurs non OAuth

