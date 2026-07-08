---
title: Jeton API
---

Les jetons API sont des clés sécurisées qui permettent aux services externes et aux intégrations de communiquer avec votre magasin. Lorsqu'un service tiers ou un outil a besoin d'accéder aux données de votre magasin ou d'activer des actions, il envoie un jeton API avec chaque demande afin que votre magasin puisse vérifier que la demande est autorisée. Vous créez et gérez tous les jetons dans la section Jetons API de votre administration.

## Lorsque vous avez besoin d'un jeton API

Vous aurez généralement besoin de créer un jeton API lorsque :

- Vous connectez un service externe ou un outil d'automatisation qui doit lire ou écrire dans votre magasin
- Vous configurez un récepteur de webhook qui doit authentifier les appels entrants
- Vous configurez le système d'aide Spwig pour votre installation
- Vous créez une intégration personnalisée à l'aide de l'API Spwig
- Vous synchronisez des données entre votre magasin Spwig et un autre système

Chaque intégration devrait avoir son propre jeton afin que vous puissiez révoquer l'accès à un service sans affecter les autres.

## Types de jetons

Lors de la création d'un jeton, vous choisissez un type qui décrit son objectif. Le type est à votre disposition et vous aide à garder une trace de ce que chaque jeton fait.

| Type | Objectif |
|------|---------|
| **Système d'aide** | Utilisé par le système de documentation d'aide Spwig |
| **Intégration externe** | Services tiers, outils d'automatisation (ex. Zapier), ou outils de synchronisation de données |
| **Webhook** | Authentification pour les récepteurs de webhook ou les points de terminaison |
| **Personnalisé** | Tout autre objectif qui ne correspond pas aux catégories ci-dessus |
| **Synchronisation d'instance** | Synchronisation entre les installations Spwig ou les services externes Spwig |

## Création d'un jeton API

1. Accédez à **Paramètres > Jetons API**
2. Cliquez sur **+ Ajouter un jeton API**
3. Entrez un **Nom** qui décrit clairement à quoi le jeton sert (ex. `Synchronisation des produits Zapier` ou `API du système d'aide`)
4. Sélectionnez le type de jeton approprié
5. Ajoutez éventuellement une **Description** avec plus de détails sur l'intégration
6. Configurez l'état **Actif**, la **Date d'expiration** et les **Adresses IP autorisées** selon vos besoins (voir ci-dessous)
7. Cliquez sur **Enregistrer**

Après l'enregistrement, la valeur complète du jeton est affichée sur la page de détails. **Copiez-la immédiatement** — le jeton est masqué dans la vue de liste pour des raisons de sécurité et ne peut plus être récupéré en totalité après avoir quitté cette page.

![Détail du jeton API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sécurité de la valeur du jeton

Spwig affiche la valeur complète du jeton une seule fois : immédiatement après avoir enregistré un nouveau jeton. Après cela, la vue de liste affiche uniquement une version masquée (ex. `spw_••••••••••••••••••••3f8a`).

Si vous perdez la valeur d'un jeton, vous ne pouvez pas la récupérer. Vous devrez supprimer le jeton ancien et en créer un nouveau, puis mettre à jour l'intégration qui l'utilisait.

**Ne partagez jamais les valeurs des jetons par e-mail, message de chat ou dans le code source.** Traitez-les comme des mots de passe.

## Définition d'une date d'expiration

Le champ **Expire à** définit une date et une heure après lesquelles le jeton cesserait de fonctionner automatiquement. Laissez-le vide pour les jetons qui ne devraient pas expirer.

Les dates d'expiration sont utiles pour :

- Des intégrations temporaires avec une date de fin fixe
- Des jetons donnés à des tiers où vous souhaitez supprimer automatiquement l'accès
- Ajouter une couche supplémentaire de sécurité aux intégrations à privilèges élevés

Lorsqu'un jeton expire, les demandes qui l'utilisent sont refusées. Vous pouvez prolonger l'accès en mettant à jour la date **Expire à** ou en créant un jeton de remplacement.

## Restriction aux adresses IP spécifiques

Le champ **Adresses IP autorisées** accepte une liste d'adresses IP. Lorsque la liste n'est pas vide, le jeton ne fonctionne que si la demande provient de l'une de ces adresses.

Par exemple, si votre outil d'analyse fonctionne sur un serveur à `203.0.113.42`, l'ajout de cette adresse IP signifie que le jeton ne peut pas être mal utilisé depuis tout autre emplacement, même s'il est fuité.

Laissez **Adresses IP autorisées** vide pour permettre les demandes provenant de toute adresse IP.

## Surveillance de l'utilisation des jetons

La liste des jetons affiche :

- **Compteur d'utilisation** — nombre total de fois où le jeton a été utilisé
- **Dernière utilisation** — moment où le jeton a été utilisé pour effectuer une demande

Ces champs vous aident à identifier les jetons non utilisés (candidats à la révocation) et à détecter une activité inattendue.

Une augmentation soudaine du nombre d'utilisations peut indiquer que le jeton est utilisé par quelqu'un d'autre que l'intégration prévue.

## Révoquer un jeton

Pour arrêter immédiatement un jeton sans le supprimer :

1. Cliquez sur le nom du jeton
2. Désactivez **Active**
3. Enregistrez

Le jeton reste dans votre liste à titre de référence mais est refusé lors des demandes ultérieures. Cela est utile lorsque vous devez suspendre temporairement une intégration pendant une enquête sur un problème.

Pour supprimer définitivement un jeton :

1. Cochez sa case dans la liste
2. Choisissez **Supprimer les jetons API sélectionnés** dans le menu d'action
3. Confirmez la suppression

Une fois supprimé, un jeton ne peut pas être récupéré. Si l'intégration a toujours besoin d'accès, créez un nouveau jeton et mettez à jour la configuration de l'intégration.

## Exemple : configuration d'une intégration Zapier

**Scénario :** Vous souhaitez connecter votre magasin à Zapier pour automatiser les notifications de commandes.

| Champ | Valeur |
|-------|-------|
| Nom | `Zapier Order Automation` |
| Type de jeton | Intégration externe |
| Description | Utilisé par Zapier pour lire les nouvelles commandes et déclencher des notifications |
| Actif | Oui |
| Expire le | *(laissez vide)* |
| IPs autorisés | *(laissez vide — Zapier utilise des IPs dynamiques)* |

Après l'enregistrement, copiez la valeur complète du jeton et collez-la dans les paramètres d'intégration Spwig de Zapier.

## Conseils

- Donnez à chaque jeton un nom clair et spécifique — `Shopify Sync v2` est bien plus utile que `Token 3` lors de la résolution de problèmes plusieurs mois plus tard
- Créez un jeton par intégration — si une intégration est compromise, vous pouvez révoquer uniquement ce jeton sans perturber les autres
- Fixez une date d'expiration pour les jetons utilisés dans des projets ponctuels ou des intégrations temporaires — cela réduit le risque que des jetons oubliés restent actifs indéfiniment
- Révisez votre liste de jetons toutes les quelques mois et désactivez tout jeton dont la date **Dernière utilisation** est inattendument ancienne, car ceux-ci peuvent appartenir à des intégrations qui ne sont plus en cours d'exécution
- Si vous soupçonnez qu'un jeton a été exposé, désactivez-le immédiatement, créez un remplacement et mettez à jour l'intégration concernée avant de réactiver l'accès