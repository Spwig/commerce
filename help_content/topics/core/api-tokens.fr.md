---
title: Jeton API
---

Les jetons API sont des clés sécurisées qui permettent aux services externes et aux intégrations de communiquer avec votre magasin. Lorsqu'un service tiers ou un outil a besoin d'accéder aux données de votre magasin ou d'activer des actions, il envoie un jeton API avec chaque demande afin que votre magasin puisse vérifier que la demande est autorisée. Vous créez et gérez tous les jetons, y compris exactement les parties de votre magasin auxquelles ils peuvent accéder, depuis la section Jetons API de votre administration.

## Lorsque vous avez besoin d'un jeton API

Vous devrez généralement créer un jeton API lorsque :

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

## Portée API : contrôler ce à quoi un jeton peut accéder

Chaque jeton dispose également d'une section **Portée API** qui détermine exactement les parties de votre magasin qu'il est autorisé à appeler. Au lieu qu'un jeton ait un accès général à tout, vous accordez l'accès une zone à la fois — et au niveau que l'intégration en a réellement besoin.

**Un jeton sans portée sélectionnée ne peut accéder à aucun API**, même s'il est autrement actif et valide. C'est la valeur par défaut pour un nouveau jeton, donc une intégration ne fonctionnera pas jusqu'à ce que vous lui accordiez délibérément l'accès.

Pour chaque portée, vous choisissez l'un des trois niveaux d'accès suivants :

| Niveau d'accès | Ce à quoi il permet |
|--------------|-----------------|
| **Aucun accès** | Le jeton ne peut appeler aucun point de terminaison dans cette zone |
| **Lecture** | Le jeton peut récupérer des données de cette zone, mais ne peut pas apporter de modifications |
| **Lecture & Écriture** | Le jeton peut récupérer des données et également les créer, les mettre à jour ou les supprimer |

Les portées sont regroupées pour correspondre aux zones de votre administration :

| Groupe | Portée | Lecture & Écriture disponible ? | Accorde l'accès à |
|-------|-------|:---:|-------------------|
| Analytics | **Analyse des ventes** | Seulement lecture | Tableaux de bord des ventes, KPI, analyses des produits/client/catégories, comparaisons et exports |
| Analytics | **Analyse web** | Seulement lecture | Analyse des visiteurs et du trafic : aperçu, tendances, pages populaires, géographie et sources de trafic |
| Catalogue | **Produits** | Oui | Produits, variantes, images, ajustements de stock et affectation d'attributs |
| Catalogue | **Catégories** | Oui | Catégories de produits, y compris les images et les bannières |
| Catalogue | **Marques** | Oui | Marques de produits |
| Catalogue | **Attributs** | Oui | Définitions d'attributs de produits |
| Catalogue | **Stock** | Oui | Tableaux de bord du stock, vitesse de stock, mouvements, suggestions de réapprovisionnement et paramètres de stock |
| Commandes | **Commandes** | Oui | Commandes, notes de commande, mises à jour d'état/traçabilité, annulations, remboursements et documents de commande |
| Clients | **Messages clients** | Oui | Messages clients provenant de formulaires de contact et de notes de commande, y compris les mises à jour d'état et les réponses |
| Magasin & Paramètres | **Paramètres du magasin** | Oui | Paramètres du magasin, langues disponibles et branding (nom, couleurs, logo) |
| Utilisateurs & Accès | **Personnel & Rôles** | Oui | Comptes de personnel, invitations, rôles et catalogue des autorisations |

Les deux portées **Analytics** sont toujours en lecture seule — les données de reporting n'ont aucun concept de « écriture », donc le menu ne propose que **Aucun accès** ou **Lecture** pour elles.

[![Le sélecteur de portée API, avec une note d'accès au-dessus des groupes de portée Analytics et Catalog](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

En dessous du sélecteur de portée, un résumé en lecture seule **"Ce jeton peut accéder à :"** liste toutes les portées que vous avez accordées et leur niveau, afin que vous puissiez vérifier rapidement l'accès d'un jeton sans avoir à décoder le sélecteur.

![Le résumé "Ce jeton peut accéder à" listant chaque portée accordée et son niveau Lecture ou Lecture & Écriture](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Quelles sont les autorisations réellement utilisées par un jeton

Les portées d'un jeton décrivent le *plafond* de ce qu'il peut faire — mais le jeton hérite également des autorisations réelles du membre du personnel qui l'a créé :

- Le jeton ne peut jamais agir avec des pouvoirs **superutilisateur**, même si le membre du personnel créateur est un superutilisateur.
- **Lecture & Écriture** sur une portée ne fonctionne que si le rôle du membre du personnel créateur permet également l'accès en écriture à cette zone. Si leur rôle est en lecture seule pour, disons, les Produits, un jeton qu'ils créent avec "Produits : Lecture & Écriture" ne pourra toujours que lire — le rôle agit comme une deuxième porte au-dessus de la portée.
- Si le membre du personnel qui a créé un jeton est supprimé ou si son compte est désactivé, le jeton perd immédiatement l'accès API, indépendamment de ses portées — il n'y a plus d'utilisateur autorisé pour qu'il agisse.

Cela signifie que la manière la plus sûre de limiter les portées d'un jeton est de le créer en vous connectant en tant que membre du personnel dont le rôle correspond déjà à l'accès que vous souhaitez que le jeton ait.

## Créer un jeton API

1. Accédez à **Paramètres > Jetons API**
2. Cliquez sur **+ Ajouter un jeton API**
3. Entrez un **Nom** qui décrit clairement à quoi le jeton sert (par exemple, `Zapier Product Sync` ou `Help System API`)
4. Sélectionnez le **Type de jeton** approprié
5. Ajoutez éventuellement une **Description** avec plus de détails sur l'intégration
6. Dans **Portées API**, choisissez **Aucun accès**, **Lecture** ou **Lecture & Écriture** pour chaque zone dont l'intégration a besoin — laissez toutes les autres portées sur **Aucun accès**
7. Configurez le statut **Actif**, la **Date d'expiration** et les **Adresses IP autorisées** selon vos besoins (voir ci-dessous)
8. Cliquez sur **Enregistrer**

Après l'enregistrement, la valeur complète du jeton est affichée sur la page de détails. **Copiez-la immédiatement** — le jeton est masqué dans la vue en liste pour des raisons de sécurité et ne peut plus être récupéré en totalité après avoir quitté cette page.

![Détail du jeton API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sécurité de la valeur du jeton

Spwig affiche la valeur complète du jeton une seule fois : immédiatement après avoir enregistré un nouveau jeton. Après cela, la vue en liste affiche uniquement une version masquée (par exemple, `spw_••••••••••••••••••••3f8a`).

Si vous perdez la valeur d'un jeton, vous ne pouvez pas la récupérer. Vous devrez supprimer l'ancien jeton et en créer un nouveau, puis mettre à jour l'intégration qui l'utilisait.

**Ne partagez jamais les valeurs des jetons par e-mail, message de chat ou code source.** Traitez-les comme des mots de passe.

## Définir une date d'expiration

Le champ **Expire à** définit une date et une heure après lesquelles le jeton cesserait de fonctionner automatiquement. Laissez-le vide pour les jetons qui ne devraient pas expirer.

Les dates d'expiration sont utiles pour :

- Des intégrations temporaires avec une date de fin fixe
- Des jetons donnés à des tiers où vous souhaitez un retrait automatique de l'accès
- Ajouter une couche supplémentaire de sécurité aux intégrations à privilèges élevés

Lorsqu'un jeton expire, les requêtes utilisant ce jeton sont refusées. Vous pouvez prolonger l'accès en mettant à jour la date **Expire à** ou en créant un jeton de remplacement.

## Limiter aux adresses IP spécifiques

Le champ **Adresses IP autorisées** accepte une liste d'adresses IP. Lorsque la liste n'est pas vide, le jeton ne fonctionne que si la requête provient de l'une de ces adresses.

Par exemple, si votre outil d'analyse fonctionne sur un serveur à `203.0.113.42`, l'ajout de cette adresse IP signifie que le jeton ne peut pas être mal utilisé depuis tout autre emplacement, même s'il est fuité.

Laissez **Adresses IP autorisées** vide pour permettre les requêtes provenant de toute adresse IP.

**La vérification des dates d'expiration et des restrictions d'IP se fait indépendamment des portées.** Un jeton expiré ou non autorisé est refusé avant même que ses portées ne soient prises en compte, et un jeton avec des portées étendues est tout de même refusé dès qu'il expire ou est utilisé depuis une adresse IP non listée.

## Appel de l'API avec un jeton

Les intégrations s'authentifient auprès de l'API admin de Spwig en envoyant le jeton dans un en-tête `Authorization` :

```
Authorization: Bearer <valeur-de-votre-jeton>
```

Chaque point de terminaison de l'API admin se trouve sous `/api/admin/...`. Le développeur qui crée votre intégration décide quels points de terminaison appeler — votre rôle en tant que commerçant est de vous assurer que les **Portées API** du jeton couvrent ces points de terminaison. Si une demande est refusée avec une erreur de permissions, la première chose à vérifier est si le jeton a été accordé la bonne portée au bon niveau d'accès.

### Exemple : lecture des statistiques de trafic web

Spwig expose un point de terminaison `GET /api/admin/analytics/traffic/` qui renvoie des statistiques de visiteurs et de trafic pour votre magasin — un aperçu des visites et des visiteurs uniques, des tendances au fil du temps, des pages les plus populaires, de la géographie des visiteurs et des sources de référencement. Pour permettre à un outil de reporting ou à un tableau de bord de lire ces données :

1. Créez un jeton (ou modifiez-en un existant) pour cette intégration
2. Dans **Portées API**, définissez **Analyse Web** sur **Lecture**
3. Enregistrez le jeton et fournissez-le à l'intégration

Puisque **Analyse Web** est une portée en lecture seule, il n'y a pas d'option **Lecture & Écriture** à choisir — l'intégration ne peut récupérer que les données d'analyse, jamais modifier la configuration de votre magasin.

## Surveillance de l'utilisation des jetons

La liste des jetons affiche :

- **Compteur d'utilisation** — nombre total de fois où le jeton a été utilisé
- **Dernière utilisation** — moment où le jeton a été utilisé pour faire une demande

Ces champs vous aident à identifier les jetons non utilisés (candidats à la révocation) et à détecter une activité inattendue. Une augmentation soudaine du compteur d'utilisation peut indiquer que le jeton est utilisé par quelqu'un d'autre que l'intégration prévue.

## Révocation d'un jeton

Pour arrêter immédiatement un jeton sans le supprimer :

1. Cliquez sur le nom du jeton
2. Désactivez **Actif**
3. Enregistrez

Le jeton reste dans votre liste à titre de référence mais est refusé lors de toute demande ultérieure. Cela est utile lorsque vous devez temporairement suspendre une intégration pendant une enquête sur un problème.

Pour supprimer définitivement un jeton :

1. Cochez sa case dans la liste
2. Choisissez **Supprimer les jetons API sélectionnés** dans le menu d'action
3. Confirmez la suppression

Une fois supprimé, un jeton ne peut plus être récupéré. Si l'intégration a toujours besoin d'accès, créez un nouveau jeton et mettez à jour la configuration de l'intégration.

## Exemple : configuration d'une intégration Zapier

**Scénario :** Vous souhaitez connecter votre magasin à Zapier pour automatiser les notifications de commandes.

| Champ | Valeur |
|-------|-------|
| Nom | `Zapier Order Automation` |
| Type de jeton | Intégration externe |
| Description | Utilisé par Zapier pour lire les nouvelles commandes et déclencher des notifications |
| Portées API | **Commandes** : Lecture & Écriture |
| Actif | Oui |
| Expire à | *(laissez vide)* |
| IPs autorisés | *(laissez vide — Zapier utilise des IPs dynamiques)* |

Seule la portée **Commandes** est accordée, donc même si ce jeton était exposé, il ne pourrait pas toucher les produits, les messages clients, les comptes du personnel ou toute autre partie de votre magasin. Après l'enregistrement, copiez la valeur complète du jeton et collez-la dans les paramètres d'intégration Spwig de Zapier.

## Conseils

Conservez tous les formats de mise en forme markdown, les chemins d'image, les blocs de code et les termes techniques.

- Donnez à chaque jeton un nom clair et spécifique — `Shopify Sync v2` est bien plus utile que `Token 3` lorsque vous effectuez un débogage plusieurs mois plus tard
- Créez un jeton par intégration — si une intégration est compromise, vous pouvez révoquer uniquement ce jeton sans perturber les autres
- **Accordez uniquement les étendues nécessaires à l'intégration** — un outil de reporting n'a besoin que d'un accès en lecture aux Analyses des Ventes ou aux Analyses Web, et non en lecture et écriture sur les Produits ou les Employés & Rôles
- Vérifiez le résumé **"Ce jeton peut accéder à :"** sur le formulaire de modification avant de transmettre un jeton à un tiers — c'est la manière la plus rapide de confirmer que vous n'avez pas accordé plus que prévu
- Souvenez-vous que l'accès en écriture dépend également du rôle du membre du personnel qui l'a créé — si une étendue affiche Lecture & Écriture mais que les écritures échouent tout de même, vérifiez également les autorisations du rôle de cet utilisateur
- Fixez une date d'expiration pour les jetons utilisés dans des projets ponctuels ou des intégrations temporaires — cela réduit le risque que des jetons oubliés restent actifs indéfiniment
- Revoyez votre liste de jetons toutes les quelques mois et désactivez tout jeton dont la date **Dernière Utilisation** est inattendamment ancienne, car ceux-ci pourraient appartenir à des intégrations qui ne sont plus en cours d'exécution
- Si vous soupçonnez qu'un jeton a été exposé, désactivez-le immédiatement, créez un remplacement, mettez à jour l'intégration concernée, puis réactivez l'accès