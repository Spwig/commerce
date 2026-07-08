---
title: Moteurs de recherche expliqués
---

Les moteurs de recherche dans Spwig ne sont pas des services externes comme Elasticsearch ou Algolia - ils sont des contextes de configuration au sein du système de recherche natif de votre base de données de magasin. Chaque moteur définit quels types de contenus rechercher, ce qu'il faut exclure et comment classer les résultats. Ce guide explique ce qu'ils sont, quand créer plusieurs moteurs et comment les configurer.

La plupart des commerçants utilisent un seul moteur par défaut "shop". Créez plusieurs moteurs uniquement si vous avez besoin de mélanges de contenus ou d'exclusions différents pour différents cas d'utilisation.

![Liste des moteurs de recherche](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## Qu'est-ce qu'un moteur de recherche ?

Un moteur de recherche dans Spwig est une configuration nommée qui spécifie :

- **Quels types de contenus rechercher** (produits, catégories, marques, articles de blog)
- **Ce qu'exclure** (des catégories ou des marques spécifiques que vous souhaitez cacher dans la recherche)
- **Poids de pertinence personnalisés** (surcharge de poids par moteur, optionnel)
- **Statut actif** (les moteurs peuvent être désactivés temporairement)

Chaque moteur a un slug unique utilisé dans les appels API et le code frontend pour spécifier quel moteur doit gérer une requête de recherche.

## Quand créer plusieurs moteurs

La plupart des magasins n'ont besoin que d'un seul moteur. Créez des moteurs supplémentaires pour ces scénarios :

| Cas d'utilisation | Exemple |
|------------------|---------|
| **Mélanges de contenus différents** | Le moteur de magasin recherche uniquement les produits ; le moteur de blog recherche uniquement les articles de blog |
| **Exclusions sélectives** | Le moteur principal du magasin cache la catégorie "solde" ; le moteur de solde affiche uniquement les articles en solde |
| **Recherche par département** | Le moteur d'électronique exclut les catégories de vêtements ; le moteur de vêtements exclut l'électronique |
| **Séparation B2B vs B2C** | Le moteur de gros affiche uniquement les produits en gros ; le moteur de détail affiche les produits destinés aux consommateurs |

Si vous n'êtes pas sûr de savoir si vous avez besoin de plusieurs moteurs, restez avec un seul. Ajouter des moteurs crée de la complexité sans bénéfice à moins que vous n'ayez un cas d'utilisation spécifique.

## Le guide en 4 étapes

![Étape 1 du guide - Informations de base](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Accédez à **Recherche > Guide d'installation** pour créer un nouveau moteur via un processus guidé en 4 étapes :

### Étape 1 : Informations de base

**Nom du moteur** - Nom convivial affiché (ex. "Recherche de magasin", "Recherche de blog"). Utilisé uniquement dans l'interface d'administration.

**Slug** - Identifiant sécurisé pour les URL (ex. "shop-search", "blog-search"). Utilisé dans les appels API et le code frontend. Généré automatiquement à partir du nom s'il est laissé vide.

**Actif** - Indique si ce moteur est disponible pour les recherches. Les moteurs inactifs ne renvoient aucun résultat.

### Étape 2 : Types de contenus

Sélectionnez les types de contenus que ce moteur recherchera :

- Produits (inclut tous les types de produits : physiques, numériques, abonnements)
- Catégories
- Marques
- Articles de blog

**Conseil** : Sélectionnez uniquement les types de contenus pertinents pour le but de ce moteur. Un moteur axé sur le blog n'a pas besoin d'avoir les produits activés.

### Étape 3 : Poids (optionnel)

![Étape 3 du guide - Poids](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Personnalisez optionnellement les poids de pertinence pour ce moteur spécifique. Si cette étape est ignorée, le moteur hérite des poids globaux définis dans SearchSettings.

La plupart des moteurs devraient ignorer cette étape et utiliser les paramètres globaux par défaut. Personnalisez uniquement les poids si ce moteur a des besoins de classement uniques (ex. un moteur de blog pourrait augmenter weight_blog_posts à 1,2).

### Étape 4 : Révision et création

Révisez votre configuration et cliquez sur **Créer le moteur** pour enregistrer.

## Champs de configuration des moteurs

Si vous modifiez un moteur directement (en contournant le guide), vous verrez ces champs :

**Nom et Slug** - Nom d'affichage et identifiant URL

**Statut actif** - Interrupteur pour activer/désactiver

**Types de contenus** - Tableau JSON comme `['product', 'category']`

**Surcharge des poids** - Objet JSON comme `{'weight_name': 1.8}` (vide si les poids globaux sont utilisés)

**Catégories exclues** - Relation M2M avec le modèle Category. Les produits de ces catégories ne s'afficheront pas dans les résultats de recherche.

**Marques exclues** - Relation M2M avec le modèle Brand. Les produits avec ces marques ne s'afficheront pas dans les résultats de recherche.

## Utilisation des exclusions

Les exclusions cachent un contenu spécifique des résultats de recherche pour ce moteur :

**Exemple : Cacher les articles en solde**

1. Créez un moteur "Main Shop"
2. Dans le champ Catégories exclues, sélectionnez votre catégorie "Clearance"
3. Dans le champ Marques exclues, sélectionnez toute marque de budget que vous souhaitez cacher
4. Enregistrez

Maintenant, les recherches via le moteur "Main Shop" ne renverront pas les produits en solde, même s'ils sont visibles sur votre site. Vous pouvez créer un moteur séparé "Clearance" qui recherche UNIQUEMENT les articles en solde.

## Utilisation des moteurs côté frontend

Votre code frontend spécifie quel moteur utiliser via des appels API :

```javascript
// Utilisez le moteur "shop" (le plus courant)
fetch('/api/search/?q=laptop&engine=shop')

// Utilisez le moteur "blog"
fetch('/api/search/?q=ecommerce tips&engine=blog')

// Moteur par défaut si aucun paramètre engine n'est spécifié
fetch('/api/search/?q=laptop')
```

Le slug du moteur devient un paramètre de requête. Si aucun moteur n'est spécifié, Spwig utilise le premier moteur actif dans l'ordre alphabétique.

## Synonymes et redirections spécifiques aux moteurs

Les modèles Synonym et SearchRedirect ont une clé étrangère optionnelle `engine`. Si elle est définie, ce synonyme ou cette redirection s'applique UNIQUEMENT aux recherches effectuées via ce moteur spécifique.

**Exemple** : Un moteur de blog pourrait avoir des synonymes comme "tutorial" → "guide" qui ne s'appliquent pas aux recherches de produits.

La plupart des synonymes et redirections ne devraient PAS être spécifiques à un moteur - laissez le champ engine vide pour les appliquer globalement.

## Conseils

- **Commencez par un seul moteur** - Créez le moteur par défaut "shop" et utilisez-le pour tout jusqu'à ce que vous ayez un besoin clair de plusieurs moteurs
- **Utilisez des slugs descriptifs** - Choisissez des slugs comme "shop", "blog", "wholesale" qui indiquent clairement le but du moteur
- **Testez les moteurs avant d'activer** - Créez des moteurs en mode inactif, testez via l'API, puis activez-les
- **Ne créez pas de moteurs à moins d'en avoir besoin** - Plus de moteurs = plus de complexité de configuration sans bénéfice si tous font la même chose
- **Analysez les performances par moteur** - Le tableau de bord des statistiques de recherche peut filtrer par moteur pour voir lesquels sont les plus utilisés

