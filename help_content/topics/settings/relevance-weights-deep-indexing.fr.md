---
title: Poids de pertinence et indexation approfondie
---

Les poids de pertinence et l'indexation approfondie contrôlent la manière dont les résultats de recherche sont classés et les données du produit qui sont indexées. Les poids sont des multiplicateurs d'importance - un poids de 2,0 signifie que les correspondances dans ce champ sont deux fois plus importantes qu'un poids de 1,0. L'indexation approfondie détermine si la recherche va au-delà des noms de produits de base vers les références, les attributs, les avis et même le contenu des documents. Ce guide explique les deux systèmes, quand les ajuster et les implications critiques sur les performances.

Les paramètres par défaut fonctionnent bien pour la plupart des magasins e-commerce. Ajustez uniquement si vous avez des besoins spécifiques en classement ou en indexation.

![Onglet Poids](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Comprendre les poids

Les poids sont des multiplicateurs (échelle 0,0-2,0) appliqués lorsqu'il y a des correspondances de texte dans différents champs. Des poids plus élevés signifient que les correspondances dans ce champ obtiennent un classement plus élevé dans les résultats.

**Exemple** : Si un produit a « laptop » à la fois dans son nom (poids 1,50) et dans sa description (poids 0,80) :
- La correspondance du nom contribue 1,50 au score de pertinence
- La correspondance de la description contribue 0,80
- Le score combiné détermine le classement par rapport aux autres produits

Les poids vous permettent de prioriser certains champs par rapport à d'autres lors du classement des résultats de recherche.

## Catégories de poids et paramètres par défaut

Accédez à **Paramètres de recherche > Onglet Poids** pour consulter toutes les configurations de poids :

| Champ | Poids par défaut | Rationale |
|-------|---------------|-----------|
| **weight_name** | 1,50 | Les noms de produits sont les plus importants - les clients s'attendent à ce que les correspondances exactes de nom soient en tête |
| **weight_sku** | 1,20 | Les références sont des identifiants spécifiques - importantes pour les entreprises B2B et les clients existants |
| **weight_description** | 0,80 | Les descriptions fournissent un contexte mais sont moins importantes que les correspondances exactes de nom |
| **weight_categories** | 0,80 | Les correspondances de catégories sont utiles pour la navigation mais moins spécifiques que le nom/référence |
| **weight_attributes** | 0,70 | Les recherches par couleur, taille, matériau - utiles mais informations secondaires |
| **weight_brands** | 0,70 | Le filtrage par marque est important mais pas le critère principal de recherche pour la plupart des magasins |
| **weight_blog_posts** | 0,60 | Le contenu du blog est moins important dans une recherche axée sur le commerce électronique (priorité la plus basse) |
| **weight_reviews** | 0,50 | Le contenu généré par les utilisateurs est le moins contrôlé - poids le plus bas |

Ces paramètres par défaut supposent un magasin e-commerce typique où la découverte de produits est l'objectif principal de la recherche.

## Quand ajuster les poids

Ajustez les poids lorsque les priorités de votre magasin diffèrent des schémas typiques de commerce électronique :

**Magasins axés sur les références (B2B, Grossiste)** - Augmentez `weight_sku` à 1,8-2,0 pour que les recherches par code de produit dominent les résultats. Les clients B2B cherchent souvent par référence exacte.

**Magasins axés sur les marques** - Augmentez `weight_brands` à 1,2-1,5 lorsque les clients achètent principalement par marque (vêtements de designer, produits de luxe).

**Magasins axés sur le contenu** - Augmentez `weight_blog_posts` à 0,9-1,2 si vous êtes un éditeur de contenu ou un détaillant éducatif où les articles de blog sont aussi importants que les produits.

**Magasins axés sur les attributs (Mode)** - Augmentez `weight_attributes` à 1,0-1,2 lorsque les clients recherchent fréquemment par couleur, taille, style.

## Exemples d'ajustement des poids

| Type de magasin | Ajustements recommandés |
|-----------|------------------------|
| **B2B Grossiste** | weight_sku: 2,0, weight_name: 1,3, weight_description: 0,6 - Prioriser les codes de produit |
| **Boutique de mode** | weight_attributes: 1,2, weight_brands: 1,2, weight_name: 1,4 - Couleur/Style/Marque importantes |
| **Éditeur de contenu** | weight_blog_posts: 1,2, weight_name: 1,3, weight_reviews: 0,7 - Contenu aussi important que les produits |
| **Commerce électronique général** | Utiliser les paramètres par défaut - Équilibré pour les magasins en ligne typiques |

Ajustez un seul poids à la fois et testez avant de faire d'autres modifications.

## Aperçu de l'indexation approfondie

⚠️ **AVERTISSEMENT DE PERFORMANCE** - Chaque option d'indexation approfondie ajoute de la complexité et des coûts supplémentaires aux requêtes.

L'indexation approfondie étend la recherche au-delà du nom et de la description du produit vers d'autres données : 

![Onglet Indexation approfondie](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Accédez à **Paramètres de recherche > Onglet Indexation approfondie** pour configurer.

## Indexer les références

**Par défaut** : ACTIF, **Impact sur les performances** : Faible

Inclut les références et les variantes de produits dans l'index de recherche. Active la jointure de variantes (coût mineur).

**Quand garder ACTIF** : Essentiel pour les magasins B2B où les clients connaissent les codes de produits. Utile également pour les clients existants qui se souviennent des références de leurs commandes précédentes.

**Quand désactiver** : Jamais, sauf si vous n'avez absolument aucune référence attribuée. L'impact sur les performances est négligeable.

## Indexer les attributs

**Par défaut** : ACTIF, **Impact sur les performances** : Moyen

Inclut les attributs du produit (couleur, taille, matériau, attributs personnalisés) dans l'index de recherche. Jointure vers la table des attributs.

**Quand garder ACTIF** : Important pour les vêtements, les produits configurables ou tout magasin où les clients recherchent par caractéristiques du produit (« robe rouge », « t-shirt large »).

**Quand désactiver** : Les catalogues avec plus de 20 000 produits et de nombreux attributs par produit peuvent voir un surcoût de 50 à 100 ms. Désactivez uniquement si les performances sont critiques et que les clients ne recherchent pas par attributs.

## Indexer les champs personnalisés

**Par défaut** : ACTIF, **Impact sur les performances** : Moyen

Inclut les champs personnalisés définis par le vendeur à partir du JSONField dans l'index. Nécessite la navigation dans le JSONField.

**Quand garder ACTIF** : Si vous utilisez des champs personnalisés pour des données de produit recherchables (informations sur la garantie, spécifications, détails de compatibilité).

**Quand désactiver** : Si vous n'utilisez pas de champs personnalisés, ou si les champs personnalisés contiennent des données non recherchables (notes internes, codes comptables). Désactiver économise le surcoût de traitement du JSONField.

## Indexer les avis

**Par défaut** : ACTIF, **Impact sur les performances** : Moyen-Élevé

Inclut les titres et commentaires des avis approuvés dans la recherche. Jointure vers la table des avis et ajout de surcoût de recherche de texte.

**Quand garder ACTIF** : Catalogues à avis nombreux où les clients recherchent des produits basés sur le contenu des avis (« sac à dos étanche pour ordinateur » pourrait apparaître dans le texte des avis).

**Quand désactiver** : Catalogues avec plus de 20 000 produits ou magasins avec de nombreux avis par produit. Ajoute un surcoût de 100 à 200 ms sur les catalogues importants.

## Indexer les documents

**Par défaut** : DÉSACTIF, **Impact sur les performances** : TRÈS ÉLEVÉ 🚨

**NE JAMAIS ACTIVER AVEC LÉGÈRETÉ** - La fonctionnalité de recherche la plus coûteuse.

L'indexation des documents extrait le texte des fichiers PDF, DOCX et XLSX joints aux produits numériques, rendant le contenu des fichiers recherchable.

**Détails techniques** : 
- Utilise les bibliothèques PyPDF2, python-docx et openpyxl
- I/O de fichiers et extraction de texte synchrones lors de la recherche
- Suivi des fichiers via le hachage MD5 (re-indexage uniquement lorsqu'un fichier change)
- Risque de dépassement de temps sur les grands fichiers (>10 Mo de PDF)

**Impact sur les performances** : 
- Coût d'indexation initial très élevé (minutes à heures pour les bibliothèques importantes)
- Surcoût important des requêtes (latence supplémentaire de 100 à 500 ms)
- Utilisation intensive de la mémoire pour les grands documents

**Activez uniquement si** : 
- Vous vendez des produits numériques avec des documents recherchables (livres électroniques, rapports, manuels)
- Le catalogue est petit (<500 produits numériques)
- Le serveur dispose de ressources suffisantes
- Vous avez testé l'impact de manière approfondie

**Pour les magasins de produits numériques** : Réfléchissez à savoir si les clients ont vraiment besoin de rechercher le contenu des documents, ou si la recherche du nom/description du produit est suffisante.

## Tableau d'impact des performances

| Fonctionnalité | Défaut | Impact | Utiliser quand |
|---------|---------|--------|----------|
| Indexer les références | ACTIF | Faible | Toujours (essentiel pour B2B) |
| Indexer les attributs | ACTIF | Moyen | Produits configurables |
| Indexer les champs personnalisés | ACTIF | Moyen | Utilisation des champs personnalisés |
| Indexer les avis | ACTIF | Moyen-Élevé | Magasin à avis nombreux |
| Indexer les documents | DÉSACTIF | Très Élevé | Produits numériques uniquement (testez d'abord) |

L'impact suppose des catalogues typiques. Les catalogues importants (>50 000 produits) subissent un surcoût proportionnellement plus élevé.

## Test des modifications des poids

Lorsque vous ajustez les poids, suivez ce workflow de test : 

1. **Changez un seul poids à la fois** - Ne modifiez pas plusieurs poids en même temps ; vous ne saurez pas laquelle a causé les résultats
2. **Petites augmentations** - Ajustez par paliers de ±0,2 (par exemple, 1,0 → 1,2, pas 1,0 → 1,8)
3. **Testez avec des requêtes réelles** - Utilisez des termes de recherche réels des clients provenant des analyses, pas des tests aléatoires
4. **Surveillez les analyses** - Comparez la pertinence des résultats avant/après en utilisant les requêtes les plus courantes
5. **Attendez 1 à 2 semaines** - Donnez aux clients le temps d'interagir avec les nouveaux classements
6. **Mesurez les taux de clics** - Les clients cliquent-ils plus/moins que par le passé ?

## Compromis entre performance et précision

Plus d'indexation = meilleurs résultats de recherche mais moins de performance : 

**Cas d'utilisation : Catalogue petit (<1 000 produits)**
- Activez toutes les options d'indexation (références, attributs, champs personnalisés, avis)
- Impact sur les performances minimal
- Capacités de recherche approfondie

**Cas d'utilisation : Catalogue moyen (1 000-10 000 produits)**
- Gardez les références, attributs, champs personnalisés ACTIFS
- Envisagez de désactiver les avis si la moyenne est >10 avis par produit
- Surveillez les temps de réponse

**Cas d'utilisation : Catalogue important (>10 000 produits)**
- Gardez les références ACTIVES (impact faible)
- Désactivez l'indexation des avis (impact élevé)
- Désactivez les champs personnalisés si inutilisés
- **NE JAMAIS activer l'indexation des documents**
- Envisagez Elasticsearch à partir de >50 000 produits

Équilibrez en fonction de la taille de votre catalogue et des ressources du serveur.

## Surcharge de poids spécifique au moteur

Lors de la création d'un moteur de recherche via l'assistant (Étape 3), vous pouvez remplacer les poids globaux pour ce moteur spécifique.

**Cas d'utilisation** : Moteur axé sur les blogs
- Créez le moteur « blog »
- Remplacez `weight_blog_posts` à 1,5 (au lieu de 0,60 globalement)
- Le contenu du blog obtient maintenant un rang plus élevé dans les recherches du moteur de blog

La plupart des moteurs ne devraient PAS remplacer les poids - laissez vide pour hériter des paramètres globaux.

## Conseils

- **NE JAMAIS activer l'indexation des documents sauf si absolument nécessaire** - Coût de performance le plus élevé de toute fonctionnalité de recherche
- **Magasins B2B : Augmentez weight_sku à 2,0** - Les codes de produit sont la méthode principale de recherche
- **Testez les modifications des poids pendant les heures à faible trafic** - Observez l'impact sur les performances avant les pics d'activité
- **Surveillez les temps de réponse après l'activation de l'indexation** - Vérifiez le tableau de bord des analyses pour détecter les ralentissements
- **Désactivez l'indexation des avis sur les catalogues >20K produits** - Impact de performance significatif
- **Une modification de poids à la fois pour les tests** - Impossible de déterminer cause/effet avec des modifications simultanées
- **L'extraction de documents nécessite PyPDF2/docx/openpyxl** - Vérifiez que ces bibliothèques sont installées avant d'activer l'indexation des documents

Souvenez-vous : Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.