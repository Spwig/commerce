---
title: Configuration de l'autocomplétion
---

L'autocomplétion, également appelée recherche prédictive ou recherche pendant la saisie, affiche les résultats pendant que les clients tapent leurs requêtes. Cela améliore considérablement l'expérience utilisateur en aidant les clients à trouver plus rapidement des produits et en réduisant les recherches sans résultats. Ce guide explique comment configurer le comportement de l'autocomplétion, les paramètres d'affichage et les compromis en matière de performance.

L'autocomplétion est activée par défaut avec des paramètres raisonnables. Ajustez uniquement ces paramètres si vous avez des préoccupations spécifiques liées à la performance ou des préférences d'affichage.

![Paramètres d'autocomplétion](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Activer l'autocomplétion

Accédez à **Recherche > Paramètres de recherche** et cliquez sur l'onglet **Autocomplétion**.

**Activer l'autocomplétion** - Interrupteur principal pour la recherche prédictive. Lorsqu'il est activé, les champs de recherche affichent un menu déroulant de résultats pendant que les clients tapent.

**Max Results Per Type** - Par défaut : 8 éléments. Nombre de résultats à afficher pour chaque type de contenu (produits, catégories, marques, articles de blog). Des valeurs plus basses (5-6) réduisent la taille des payloads API et accélèrent le rendu. Des valeurs plus élevées (10-12) donnent aux clients plus d'options mais ralentissent la réponse.

## Délai de débounced

⚠️ **AVERTISSEMENT DE PERFORMANCE** - Le délai de débounced affecte considérablement la charge du serveur.

**Délai de débounced** - Par défaut : 300 ms. Temps d'attente après la dernière touche de clavier avant de déclencher une requête d'autocomplétion.

Ce paramètre équilibre la réactivité avec la charge du serveur :

| Délai | Expérience utilisateur | Impact sur le serveur |
|-------|----------------|---------------|
| **100 ms** | Très réactif | 3x plus d'appels API que 300 ms - charge élevée |
| **200 ms** | Réactif | 1,5x plus d'appels API que 300 ms |
| **300 ms** | Bon équilibre (recommandé) | Niveau de base |
| **400 ms** | Légèrement lent | Moins d'appels API - charge réduite |
| **500 ms** | Retard notable | 50 % moins d'appels mais semble lent |

**Recommandation** : Gardez entre 250-350 ms. Augmentez uniquement au-delà de 350 ms si votre serveur a du mal avec la charge d'autocomplétion. Ne descendez jamais en dessous de 200 ms sauf si vous avez un serveur très rapide et un catalogue petit.

## Paramètres d'affichage pour les produits

Ces interrupteurs contrôlent les informations affichées dans les résultats d'autocomplétion des produits :

**Afficher la miniature** - Par défaut : ACTIVÉ. Affiche l'image du produit à côté du résultat. **Impact sur la performance** : Ajoute une requête d'image et augmente la taille du payload JSON. Désactivez pour une autocomplétion plus rapide sur les connexions lentes.

**Afficher la description** - Par défaut : DÉSACTIVÉ. Affiche la description courte du produit. **Impact sur la performance** : Ajoute un traitement du texte et augmente considérablement la taille du payload. Gardez désactivé sauf si les descriptions sont essentielles pour la sélection du produit.

**Afficher le prix** - Par défaut : ACTIVÉ. Affiche le prix du produit. **Impact sur la performance** : Faible - les données de prix sont déjà chargées avec le produit. Il est sûr de garder ce paramètre activé.

**Afficher le SKU** - Par défaut : ACTIVÉ. Affiche le SKU du produit. **Impact sur la performance** : Faible - le SKU est déjà indexé. Essentiel pour les magasins B2B.

**Afficher l'état des stocks** - Par défaut : DÉSACTIVÉ. **⚠️ AVERTISSEMENT DE PERFORMANCE Majeur**

Affiche les badges "En stock", "Stock bas" ou "Hors stock". **NE JAMAIS activer cela sur de grands catalogues**.

L'état des stocks nécessite l'agrégation `with_stock_totals()` - calcul des quantités en stock sur tous les entrepôts pour chaque produit dans les résultats d'autocomplétion. Cela ajoute :
- Une charge importante sur la base de données (requêtes d'agrégation)
- 200-500 ms de latence supplémentaire sur les catalogues > 1 000 produits
- Des risques de dépassement de temps sur les catalogues > 10 000 produits

Activez uniquement si c'est absolument critique et que vous avez moins de 500 produits.

## Paramètres d'affichage pour les articles de blog

**Afficher l'image mise en avant** - Par défaut : ACTIVÉ. Miniature de l'article de blog dans les résultats d'autocomplétion.

**Afficher l'extrait** - Par défaut : ACTIVÉ. Texte d'aperçu bref extrait du contenu de l'article.

**Longueur de l'extrait** - Par défaut : 60 caractères. Combien de texte d'aperçu afficher.

Ces paramètres ont un impact minimal sur la performance car les articles de blog sont généralement moins nombreux que les produits.

## Paramètres d'affichage pour les catégories et les marques

**Afficher la miniature/logo** - Par défaut : ACTIVÉ. Image de catégorie ou de marque dans les résultats.

**Afficher le nombre de produits** - Par défaut : DÉSACTIVÉ. **⚠️ AVERTISSEMENT DE PERFORMANCE**

Affiche le nombre de produits dans chaque catégorie ou marque (par exemple, "Électronique (234)").

**NE JAMAIS activer cela sur de grands catalogues**. Les comptes de produits sont recalculés à chaque demande d'autocomplétion :
- Chaque type de contenu avec les comptes activés ajoute 2 requêtes supplémentaires
- Les requêtes comprennent des jointures et des agrégations
- Une latence supplémentaire de 100-300 ms est typique
- Augmente linéairement avec le nombre de catégories/marques

Activez uniquement si vous avez moins de 50 catégories/marques ET moins de 1 000 produits au total.

## Cache

**Durée de vie du cache d'autocomplétion** - Par défaut : 60 secondes (défini dans l'onglet Cache).

Les résultats d'autocomplétion sont mis en cache pour améliorer les performances. La durée de vie de 60 secondes signifie :
- Le premier client recherchant "laptop" déclenche une requête de base de données
- Pendant les 59 secondes suivantes, toutes les recherches "laptop" renvoient les résultats mis en cache
- Après 60 secondes, le cache expire et la prochaine recherche actualise les données

**Recommandation pour la durée de vie du cache** : 
- **45-60 s** : Bon équilibre pour la plupart des magasins (par défaut)
- **90-120 s** : Meilleure performance si le stock des produits change rarement
- **30 s** : Résultats plus récents si vous ajoutez fréquemment des produits

Augmenter la durée de vie du cache est la manière la plus simple d'améliorer les performances de l'autocomplétion.

## Autocomplétion multilingue

Si vous avez plusieurs langues configurées, l'autocomplétion recherche automatiquement le contenu traduit stocké dans les champs JSONField translations.

**Fonctionnement** : 
- Le client recherche en espagnol : "zapatos"
- Le système recherche les traductions des noms de produits en espagnol
- Les résultats affichent les noms de produits en espagnol à partir des données JSONField
- Recourt à la langue de base si la traduction en espagnol est absente

**Performance** : Surcharge minimale pour 1 à 3 langues. Avec 5 langues ou plus, une légère augmentation de la complexité des requêtes.

## Tester l'autocomplétion

Après avoir configuré les paramètres, testez l'expérience d'autocomplétion :

1. **Ouvrez la page d'accueil de votre magasin** dans une fenêtre incognito
2. **Cliquez sur le champ de recherche** pour le mettre en focus
3. **Tapez lentement le nom d'un produit courant** (par exemple, "laptop")
4. **Observez** : 
   - La rapidité avec laquelle les résultats apparaissent après que vous avez arrêté de taper (le débounced fonctionne-t-il ?)
   - Les informations affichées (miniatures, prix, SKUs comme configuré)
   - Si les résultats sont pertinents (vérifiez les poids de pertinence si ce n'est pas le cas)
5. **Testez sur mobile** - Assurez-vous que le menu déroulant est amical au toucher et lisible

## Conseils

- **Désactivez les descriptions des produits pour gagner en vitesse** - Les descriptions augmentent considérablement la taille du payload avec peu de valeur dans le contexte de l'autocomplétion
- **NE JAMAIS activer l'état des stocks sur de grands catalogues** - L'agrégation des stocks ruine les performances de l'autocomplétion
- **Testez sur mobile avec des cibles de toucher** - Les résultats d'autocomplétion doivent être facilement cliquables sur les téléphones
- **Surveillez les temps de réponse hebdomadaires** - Ciblez <200 ms pour les requêtes d'autocomplétion
- **Augmentez la durée de vie du cache si lent** - La mise à jour la plus simple des performances
- **Les comptes de produits sont coûteux - désactivez-les sauf si critiques** - Chaque compte de catégorie/marque ajoute 2 requêtes à chaque demande d'autocomplétion