---
title: Comprendre les paramètres de recherche
---

L'interface SearchSettings contrôle le comportement de recherche global dans votre boutique Spwig. Cette seule page de configuration utilise une interface à 8 onglets pour organiser les options de recherche, des paramètres de base à l'ajustement des performances avancées. Les modifications apportées ici s'appliquent à tous les moteurs de recherche sauf si elles sont remplacées au niveau du moteur.

Ce guide parcourt chaque onglet, expliquant ce que fait chaque paramètre et quand l'ajuster.

![Onglet Général des paramètres de recherche](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## L'interface à 8 onglets

SearchSettings est un modèle singleton - un seul enregistrement de configuration existe (pk=1) pour votre boutique entière. L'interface est divisée en huit onglets:

| Onglet | Objectif |
|--------|---------|
| **Général** | Activer/désactiver la recherche, définir les paramètres de base |
| **Autocomplete** | Configurer le comportement du menu déroulant de recherche prédictive |
| **Types de contenu** | Choisir les types de contenu pouvant être recherchés |
| **Indexation approfondie** | Contrôler les données du produit indexées (impact sur les performances) |
| **Correspondance floue** | Tolérance aux fautes de frappe et seuils de similarité |
| **Poids** | Multiplicateurs de pertinence pour le classement des résultats |
| **Caching** | Compromis entre temps de réponse et fraîcheur |
| **Analytique** | Suivi des requêtes et paramètres de confidentialité |

Chaque onglet se concentre sur un aspect spécifique de la configuration de recherche.

## Onglet Général

L'onglet Général contient les paramètres fondamentaux qui affectent toutes les recherches:

**Activer la recherche** - Interrupteur principal pour le système de recherche. Lorsqu'il est désactivé, toutes les fonctionnalités de recherche sont inactives dans votre boutique, y compris l'autocomplete et la page des résultats de recherche.

**Longueur minimale de la requête** - Par défaut: 2 caractères. Les requêtes plus courtes que cela sont refusées. En la fixant à 1, les recherches à un seul caractère (ex: "A") sont autorisées, mais cela augmente la charge du serveur.

**Résultats par page** - Par défaut: 20 éléments. Contrôle la pagination pour les pages de résultats de recherche. Des valeurs plus élevées (30-50) réduisent les clics de pagination mais augmentent le temps de chargement de la page.

## Onglet Types de contenu

![Paramètres des types de contenu](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Basculer les types de contenu qui apparaissent dans les résultats de recherche:

- **Produits** - Produits physiques, numériques et abonnements
- **Catégories** - Catégories de produits
- **Marques** - Marques de produits
- **Articles de blog** - Contenu de blog

**Remarque sur les performances**: Moins de types de contenu = des recherches plus rapides. Chaque type activé ajoute des requêtes supplémentaires à la base de données. Si vous n'avez pas de blog, désactivez les Articles de blog pour améliorer les temps de réponse.

## Onglet Indexation approfondie

⚠️ **AVERTISSEMENT DE PERFORMANCE** - Ces paramètres ont des implications significatives sur les performances.

![Paramètres d'indexation approfondie](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

L'indexation approfondie contrôle les données liées aux produits inclus dans les recherches:

**Indexer les références** - Par défaut: ACTIF, faible impact. Inclut les références des produits et des variantes dans la recherche. Essentiel pour les magasins B2B où les clients cherchent par codes de produits.

**Indexer les attributs** - Par défaut: ACTIF, impact moyen. Inclut les attributs des produits (couleur, taille, matériau) dans la recherche. Ajoute une jointure à la table des attributs. Important pour les vêtements et les produits configurables.

**Indexer les champs personnalisés** - Par défaut: ACTIF, impact moyen. Inclut les champs personnalisés définis par le vendeur dans les résultats de recherche. Nécessite le parcours JSONField.

**Indexer les avis** - Par défaut: ACTIF, impact moyen-élevé ⚠️

L'indexation des documents extrait le texte à partir des fichiers PDF, DOCX et XLSX joints aux produits numériques. Cette fonctionnalité:

- Nécessite une indexation initiale très coûteuse
- Ajoute un surcoût important à chaque recherche
- Peut provoquer des temps d'attente sur de grands fichiers
- **Ne doit être activée que pour les magasins de produits numériques avec des documents recherchables**
- **Ne l'activez jamais de façon aléatoire** - testez soigneusement l'impact sur les performances

## Onglet Correspondance floue

![Paramètres de correspondance floue](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

La correspondance floue utilise la distance de Levenshtein pour gérer les fautes de frappe:

**Activer la correspondance floue** - Permet aux recherches de correspondre à des termes similaires (ex: "laptop" correspond à "labtop")

**Seuil de similarité** - Par défaut: 0,80 (80 % de similarité). Plage: 0,0-1,0. Des valeurs plus élevées exigent des correspondances plus proches et s'exécutent plus rapidement. Des valeurs plus basses capturent plus de fautes de frappe mais peuvent renvoyer des résultats non pertinents.

**Distance d'édition maximale** - Par défaut: 2 changements de caractères. Nombre maximal d'insertions, de suppressions ou de substitutions autorisées. Des valeurs plus basses (1) améliorent les performances mais capturent moins de fautes de frappe.

## Onglet Poids

Les poids contrôlent le classement de la pertinence - comment les résultats sont classés. L'onglet Poids affiche les multiplicateurs par défaut pour chaque champ pouvant être recherché:

- weight_name: 1,50 (les noms de produits sont les plus importants)
- weight_sku: 1,20
- weight_description: 0,80
- weight_categories: 0,80
- weight_attributes: 0,70
- weight_brands: 0,70
- weight_blog_posts: 0,60
- weight_reviews: 0,50

Ces paramètres par défaut fonctionnent bien pour la plupart des magasins e-commerce. Pour des informations détaillées sur l'ajustement des poids et leur impact, consultez le sujet [Poids de pertinence et indexation approfondie](/en/admin/help/relevance-weights-deep-indexing/).

## Onglet Caching

![Paramètres de mise en cache](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Le caching améliore considérablement les performances de recherche en stockant les résultats récents:

**Durée de vie du cache d'autocomplete** - Par défaut: 60 secondes. Durée pendant laquelle les résultats d'autocomplete sont mis en cache. Une durée de vie plus courte (30-45 s) = résultats plus récents mais plus de requêtes à la base de données. Une durée de vie plus longue (90-120 s) = plus rapide mais des résultats potentiellement obsolètes.

**Durée de vie du cache des résultats** - Par défaut: 300 secondes (5 minutes). Durée de mise en cache de la page complète des résultats de recherche. Une durée de vie plus longue améliore considérablement les performances mais retarde la visibilité des nouveaux produits.

**Compromis**: Le caching est l'optimisation de performance la plus efficace. Si les recherches sont lentes, augmentez ces valeurs avant de désactiver des fonctionnalités.

## Onglet Analytique

![Paramètres analytiques](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Suivre les requêtes de recherche** - Active le tableau de bord d'analyse de recherche. Enregistre le texte de la requête, le nombre de résultats, le temps de réponse et la date-heure.

**Suivre les informations utilisateur** - Associe les recherches aux utilisateurs connectés. Désactivez pour la conformité à la protection de la vie privée (RGPD, CCPA).

**Suivre les informations de session** - Utilise les identifiants de session pour suivre les recherches des utilisateurs anonymes. Utile pour identifier les schémas de recherche sans données personnelles.

## Modèle singleton

SearchSettings utilise un modèle singleton - un seul enregistrement de paramètres existe dans votre base de données (pk=1). Lorsque vous accédez aux paramètres de recherche dans l'administration, vous modifiez toujours le même enregistrement.

Il n'y a pas d'option "Ajouter" ou "Supprimer" - juste "Modifier". Tous les moteurs de recherche héritent de ces paramètres sauf s'ils spécifient des remplacements par moteur (rare).

## Conseils

- **Gardez les paramètres par défaut sauf si vous avez un besoin spécifique** - Les paramètres par défaut sont optimisés pour les magasins e-commerce typiques
- **NE JAMAIS activer l'indexation des documents de façon aléatoire** - Seulement pour les magasins de produits numériques avec des documents recherchables, et testez d'abord l'impact sur les performances
- **Surveillez les temps de réponse dans les analyses** - Ciblez <200 ms pour l'autocomplete, <500 ms pour la recherche complète
- **Augmentez la durée de vie du cache si les performances sont lentes** - Le caching est la plus facile optimisation de performance
- **Révisez les requêtes sans résultats hebdomadairement** - Elles révèlent des produits manquants ou des synonymes nécessaires
- **Désactivez les types de contenu non utilisés** - Si vous n'avez pas de blog, désactivez les Articles de blog pour accélérer les recherches

Souvenez-vous: Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.