---
title: Optimisation des performances de recherche
---

Les performances de recherche influencent directement l'expérience client et les conversions. Les recherches lentes frustrent les clients et augmentent les taux de rebond. Ce guide complet identifie les goulots d'étranglement courants du système de recherche natif à la base de données de Spwig, fournit des stratégies d'optimisation et établit des objectifs de performance. Utilisez ce guide lorsque les temps de réponse de recherche dépassent les seuils acceptables ou si vous prévoyez une croissance du catalogue.

Temps de réponse cibles : <200ms pour l'autocomplétion, <500ms pour la recherche complète. Suivez le checklist d'optimisation ci-dessous pour atteindre ces objectifs.

## Compréhension des métriques de performance

Suivez ces métriques dans **Search > Search Analytics** :

**Temps de réponse** - Millisecondes pour exécuter une requête de recherche (uniquement côté serveur, exclut la latence réseau)

**Taux de cache hit** - Pourcentage de recherches servies à partir du cache par rapport à la base de données

**Nombre de requêtes** - Nombre de requêtes à la base de données par recherche (moins est mieux)

**Temps de requête de base de données** - Temps passé dans la base de données par rapport au code d'application

## Objectifs de performance

| Type de requête | Cible | Acceptable | Nécessite une optimisation |
|----------------|-------|------------|--------------------------|
| Autocomplétion | <200ms | 200-300ms | >300ms de manière constante |
| Recherche complète | <500ms | 500-800ms | >800ms de manière constante |
| Recherche d'administrateur | <1000ms | 1000-1500ms | >1500ms de manière constante |

Si vos temps de réponse moyens dépassent les seuils "Nécessite une optimisation", mettez en œuvre les stratégies ci-dessous.

## Surveillance des performances

**Temps de réponse moyen du tableau de bord d'analyse**

Accédez à **Search > Search Analytics** pour consulter le temps de réponse moyen pour toutes les recherches. C'est votre métrique principale de surveillance des performances.

**Quand investiguer** : Temps de réponse moyen >300ms pour l'autocomplétion ou >800ms pour la recherche complète de manière constante sur plusieurs jours.

**Surveillance hebdomadaire** : Révisez les analyses chaque lundi pour détecter tôt la dégradation des performances.

## Goulots d'étranglement connus

La recherche native à la base de données de Spwig présente plusieurs goulots d'étranglement documentés à éviter :

### Calcul des taux de clic (CTR) avec N+1 requêtes

**Qu'est-ce que c'est** : Le calcul du taux de clic dans AnalyticsService exécute des requêtes séparées pour chaque élément de résultat agrégé.

**Impact** : Très important pour les magasins à fort trafic avec de nombreuses requêtes suivies.

**Emplacement du code** : `search/services/analytics_service.py` - méthode `get_click_through_rate()`

**Atténuation** : Évitez d'appeler les calculs de CTR en production. C'est principalement une fonctionnalité d'analyse d'administrateur qui devrait être calculée de manière asynchrone, et non pendant les requêtes orientées client.

### Agrégation des stocks

**Qu'est-ce que c'est** : `with_stock_totals()` calcule les quantités en stock sur tous les entrepôts par produit.

**Impact** : Coûteux pour les catalogues >1 000 produits. Appelé lors de l'utilisation du filtre `in_stock` ou de l'affichage de l'état des stocks dans l'autocomplétion.

**Déclencheur** : **Search Settings > Autocomplete** - option "Show Stock Status"

**Recommandation** : NE JAMAIS activer l'état des stocks dans l'autocomplétion pour les catalogues volumineux. Ajoute 200-500ms par demande.

### Rejoindre les variantes

**Qu'est-ce que c'est** : Les recherches SKU déclenchent un JOIN sur la table des variantes pour rechercher les SKU de variantes.

**Impact** : 2 à 3 fois plus lent sur les produits avec de nombreuses variantes (10+ variantes par produit).

**Atténuation** : Utilise `.distinct()` pour éviter les doublons, ce qui ajoute un surcoût. Nécessaire pour la fonctionnalité SKU - ne désactivez pas à moins que les SKU ne soient inutilisés.

### Comptes de produits dans l'autocomplétion

**Qu'est-ce que c'est** : Les résultats d'autocomplétion de catégorie/marque affichent les comptes de produits ("Électronique (234)")

**Impact** : Chaque type de contenu avec des comptes activés ajoute 2 requêtes supplémentaires. Les requêtes comprennent des joints et des agrégations.

**Déclencheur** : **Search Settings > Autocomplete** - "Show Product Count" pour les catégories/marques

**Recommandation** : Désactiver les comptes de produits. Économise 2-4 requêtes par demande d'autocomplétion. Plus grande optimisation d'autocomplétion.

### Indexation de documents

**Qu'est-ce que c'est** : Extraction de texte à partir de fichiers PDF/DOCX/XLSX pendant les requêtes de recherche.

**Impact** : Très coûteux (I/O de fichiers + extraction de texte). Opérations bloquantes synchrones.

**Déclencheur** : **Search Settings > Deep Indexing** - "Index Documents"

**Recommandation** : Presque jamais justifié par le coût de performance. ACTIVEZ UNIQUEMENT pour de petits catalogues de produits numériques (<500 produits) après des tests approfondis.

## Configuration du cache

Le cache est la mesure d'optimisation de performance la plus efficace.

**Cache d'autocomplétion** - Défaut : 60s
- **Plage recommandée** : 45-90s
- **TTL plus élevé (90-120s)** : Meilleures performances si les changements d'inventaire sont rares
- **TTL plus bas (30-45s)** : Résultats plus récents si vous ajoutez des produits toutes les heures

**Cache de résultats** - Défaut : 300s (5 minutes)
- **Plage recommandée** : 180-600s
- **TTL plus élevé (600s/10min)** : Amélioration significative des performances pour les catalogues statiques
- **TTL plus bas (180s)** : Résultats plus récents si les données du produit sont fréquemment mises à jour

**Stratégie d'optimisation** : Si les recherches sont lentes, doublez le TTL du cache avant de désactiver des fonctionnalités. Passer du cache d'autocomplétion de 60s à 120s réduit la charge de la base de données de moitié.

## Checklist d'optimisation de l'autocomplétion

Appliquez ces modifications aux paramètres d'autocomplétion pour une performance maximale :

**1. Augmenter le délai de débounced à 300-400ms**
- Emplacement : **Search Settings > Autocomplete** - "Debounce Delay"
- Impact : Réduit les appels API en attendant plus longtemps entre les frappes de clavier
- Compromis : Légèrement moins réactif (imperceptible pour la plupart des utilisateurs)

**2. Réduire le nombre maximal de résultats de 8 à 5-6**
- Emplacement : **Search Settings > Autocomplete** - "Max Results Per Type"
- Impact : Ensembles de résultats plus petits = requêtes plus rapides et payloads JSON plus petits
- Compromis : Moins d'options affichées (souvent suffisant)

**3. Désactiver les comptes de produits (PLUS GRANDE GAGNE)**
- Emplacement : **Search Settings > Autocomplete** - décocher "Show Product Count" pour les catégories/marques
- Impact : Économise 2-4 requêtes par demande d'autocomplétion
- Compromis : Aucun compte de produit dans le menu déroulant (rarement nécessaire)

**4. Désactiver l'état des stocks**
- Emplacement : **Search Settings > Autocomplete** - décocher "Show Stock Status"
- Impact : Élimine l'agrégation coûteuse des stocks
- Compromis : Aucun badge de stock (non critique dans le contexte d'autocomplétion)

**5. Désactiver les descriptions des produits**
- Emplacement : **Search Settings > Autocomplete** - décocher "Show Description"
- Impact : Réduit le traitement du texte et la taille du payload
- Compromis : Moins de texte d'aperçu (le nom du produit est généralement suffisant)

**6. Augmenter le TTL du cache à 90s**
- Emplacement : **Search Settings > Caching** - "Autocomplete Cache TTL"
- Impact : Plus de requêtes servies à partir du cache
- Compromis : Les résultats peuvent être obsolètes jusqu'à 90 secondes (acceptable pour la plupart des magasins)

**Amélioration attendue** : L'application de toutes les 6 optimisations réduit généralement le temps de réponse d'autocomplétion de 50 à 70 %.

## Optimisation de l'indexation approfondie

Chaque option d'indexation approfondie ajoute un surcoût. Désactivez-la en fonction de la taille du catalogue :

| Taille du catalogue | Indexation approfondie recommandée |
|--------------------|-------------------------------|
| **<1 000 produits** | TOUT ACTIF (impact minimal) |
| **1 000-10 000** | Gardez les SKU, les attributs, les champs personnalisés ACTIFS ; Désactivez les avis |
| **10 000-20 000** | Gardez les SKU, les attributs ACTIFS ; Désactivez les champs personnalisés, les avis |
| **20 000-50 000** | Gardez les SKU ACTIFS uniquement ; Désactivez tout le reste |
| **>50 000** | Gardez les SKU ACTIFS ; Considérez la migration vers Elasticsearch |

**Indexation de documents** : TOUJOURS DÉSACTIVÉE sauf si critique (produits numériques avec documents recherchables ET <500 produits au total).

## Optimisation des types de contenu

Désactivez les types de contenu non utilisés dans **Search Settings > Content Types** :

- **Aucun blog ?** Désactivez "Blog Posts" - économise des requêtes
- **Aucun filtre de marque ?** Désactivez "Brands" - économise des requêtes
- **Magasin uniquement pour le commerce ?** Désactivez "Categories" et "Blog Posts"

Chaque type de contenu désactivé retire des requêtes de base de données de chaque recherche.

## Optimisation de la base de données

Spwig crée les index nécessaires via des migrations. Faites confiance à cela - ne créez pas d'index supplémentaires sans profilage.

**Maintenance PostgreSQL** (si vous utilisez PostgreSQL) :
- Exécuter `VACUUM ANALYZE` hebdomadairement pour mettre à jour les statistiques du planificateur de requêtes
- Les catalogues volumineux bénéficient d'un `VACUUM FULL` mensuel (nécessite un temps d'arrêt)

**Surveillez le temps de requête de base de données** : Pendant le développement, identifiez les requêtes lentes à l'aide d'outils de profilage. La plupart de l'optimisation des requêtes est déjà implémentée :
- `.select_related('brand', 'category')` sur les produits
- `.prefetch_related('images')` pour les miniatures
- `.distinct()` pour les recherches de variantes

## Performance du matching flou

La distance de Levenshtein est coûteuse en calcul (complexité O(m*n)) :

**Optimisation du seuil** :
- **Seuil plus élevé (0,85 vs 0,80)** : Plus rapide mais capture moins de fautes de frappe
- **Seuil plus bas (0,75 vs 0,80)** : Plus lent mais plus tolérant

**Optimisation du nombre maximal d'éditions** :
- **Nombre maximal d'éditions plus bas (1 vs 2)** : Plus rapide mais manque plus de fautes d'orthographe
- **Nombre maximal d'éditions plus haut (2 vs 3)** : Plus lent mais capture plus de fautes de frappe

**Performance de la bibliothèque** : Spwig utilise `rapidfuzz` si disponible (10 fois plus rapide que le Python pur). Assurez-vous qu'il est installé : `pip install rapidfuzz`

## Performance des synonymes et redirections

**Expansion de requête par synonymes** : Chaque synonyme ajoute des clauses OR à la requête de recherche. Limitez à 10-20 synonymes par terme maximum.

**Type de correspondance Regex** : Les redirections Regex sont plus lentes que exact/contains/starts_with. Évitez les motifs complexes.

**Recommandation** : Utilisez les types de correspondance simples autant que possible. Réservez le regex aux cas où d'autres types de correspondance ne fonctionnent pas.

## Optimisation pour les catalogues volumineux (>10 000 produits)

Stratégies spécifiques pour les catalogues volumineux :

**1. Cache agressif**
- Autocomplétion : TTL de 90-120s
- Résultats : TTL de 600s (10 min)
- Accepter l'obsolescence pour la performance

**2. Indexation approfondie minimale**
- Seulement les SKU (désactiver les attributs, les champs personnalisés, les avis)
- Tester la performance avec et sans attributs

**3. Résultats d'autocomplétion réduits**
- Max 5 résultats par type (contre 8)
- Réduit le surcoût des requêtes

**4. Désactiver l'état des stocks partout**
- Dans l'autocomplétion
- Dans les résultats de recherche s'ils sont affichés

**5. Considérer Elasticsearch à partir de 50 000 produits**
- La recherche native à la base de données est adaptée jusqu'à environ 50 000 produits
- Au-delà, Elasticsearch est recommandé pour :
  - Recherche facetée complexe
  - Charge de recherche simultanée élevée (>100 recherches/sec)
  - Temps de réponse constants >500ms malgré l'optimisation

## Performance multilingue

L'indexation JSONField JSONB (PostgreSQL) rend la multilingue efficace :

- **1-3 langues** : Surcoût minimal (5-10ms)
- **5+ langues** : Augmentation mineure de la complexité des requêtes (20-40ms)
- **10+ langues** : Surcoût notable (50-100ms)

Le surcoût augmente linéairement avec le nombre de langues.

## Réparations de performance d'urgence

Si les recherches sont extrêmement lentes (>2s de temps de réponse), appliquez ces réparations immédiates dans l'ordre suivant :

**Immédiat** (appliquer maintenant) :
1. Désactiver l'indexation de documents
2. Désactiver les comptes de produits dans l'autocomplétion
3. Augmenter les TTL du cache à 120s d'autocomplétion / 600s de résultats

**Rapide** (appliquer dans les 24 heures) :
4. Désactiver l'état des stocks dans l'autocomplétion
5. Réduire le nombre maximal de résultats d'autocomplétion à 5
6. Désactiver les descriptions des produits dans l'autocomplétion

**Moyen** (appliquer dans la semaine) :
7. Désactiver l'indexation des avis si >20K produits
8. Réviser et désactiver les types de contenu non utilisés
9. Augmenter le délai de débounced à 400ms

**Amélioration attendue** : Ces 9 réparations réduisent généralement les temps de réponse de 60 à 80 % sur les catalogues volumineux.

## Conseils

- **Surveillez les temps de réponse hebdomadairement** - Détectez tôt la dégradation des performances
- **Les augmentations de cache sont la première optimisation** - Doubler le TTL du cache est la plus facile gagne
- **Les comptes de produits dans l'autocomplétion = coûteux** - Plus grand tueur de performance d'autocomplétion
- **L'indexation de documents presque jamais justifiée** - Coût de performance rarement justifie le bénéfice
- **Testez un changement à la fois** - Ne pouvez pas identifier cause/effet avec des changements simultanés
- **Benchmarkez avec des volumes de données réalistiques** - Testez avec des catalogues de production
- **L'agrégation des stocks tue les performances sur les catalogues volumineux** - Évitez d'afficher les stocks dans l'autocomplétion
- **Considérez Elasticsearch à partir de 50 000+ produits** - La recherche native à la base de données a des limites

