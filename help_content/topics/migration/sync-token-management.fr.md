---
title: Gestion des jetons de synchronisation
---

Les jetons de synchronisation sont des identifiants sécurisés qui permettent à deux installations Spwig de communiquer entre elles. Avant de pouvoir synchroniser les paramètres ou migrer des données entre des magasins, vous devez générer un jeton sur le magasin **destinataire** et le fournir au magasin **expéditeur**.

## Fonctionnement des jetons de synchronisation

Un jeton de synchronisation est une clé API visible une seule fois qui authentifie les requêtes entre deux installations Spwig. Lorsque vous configurez une connexion, le magasin distant utilise ce jeton pour prouver qu'il a le droit de lire ou d'écrire dans votre magasin.

- Les jetons sont générés sur le magasin qui sera **connecté à** (la cible)
- Chaque jeton ne peut être vu qu'une seule fois, immédiatement après sa génération
- Les jetons peuvent être révoqués à tout moment pour couper immédiatement l'accès
- Un magasin peut avoir plusieurs jetons actifs pour différentes connexions

## Génération d'un jeton

1. Accédez à **Data Migration > Spwig-to-Spwig Sync** dans le menu latéral de l'admin
2. Cliquez sur **Manage Tokens** sur le tableau de bord de synchronisation
3. Entrez un nom descriptif pour le jeton (par exemple, "Staging Server" ou "Production Sync")
4. Cliquez sur **Generate Token**
5. **Copiez immédiatement le jeton** -- il ne sera plus affiché

> **Important :** Conservez le jeton de manière sécurisée. Si vous le perdez, vous devrez en générer un nouveau.

## Utilisation d'un jeton

Une fois que vous avez un jeton du magasin cible :

1. Allez sur le tableau de bord **Spwig-to-Spwig Sync** du magasin qui initiera la connexion
2. Démarrez une nouvelle **Settings Sync** ou **Full Migration**
3. Dans l'étape de connexion, entrez l'URL du magasin cible et collez le jeton
4. Cliquez sur **Test Connection** pour vérifier qu'elle fonctionne
5. La connexion sera enregistrée pour une utilisation future

## Révocation d'un jeton

Si un jeton est compromis ou n'est plus nécessaire :

1. Allez sur **Manage Tokens** sur le tableau de bord de synchronisation
2. Trouvez le jeton que vous souhaitez révoquer
3. Cliquez sur le bouton **Revoke**
4. Confirmez la révocation

La révocation d'un jeton prend effet immédiatement. Toute connexion active utilisant ce jeton cesserait de fonctionner et devrait être reconfigurée avec un nouveau jeton.

## Bonnes pratiques

- **Nommez les jetons de manière descriptive** pour savoir à quelle connexion appartient chaque jeton
- **Révoquez les jetons non utilisés** pour minimiser l'exposition à la sécurité
- **Générez des jetons distincts** pour chaque magasin connecté plutôt que de partager un seul jeton entre plusieurs magasins
- **Régénérez périodiquement les jetons** en tant que partie de votre routine de sécurité, surtout après des changements de personnel

