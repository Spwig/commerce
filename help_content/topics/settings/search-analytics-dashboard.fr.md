---
title: Tableau de bord des analytics de recherche
---

Le tableau de bord des analytics de recherche suit chaque requête de recherche sur votre boutique, fournissant des informations sur ce que les clients cherchent, quelles recherches réussissent ou échouent, et à quelle vitesse votre système de recherche répond. Utilisez ces données pour identifier les produits populaires, découvrir les lacunes d'inventaire, créer des synonymes et optimiser les performances de recherche.

La prise en charge des analytics doit être activée dans **Paramètres de recherche > Onglet Analytics** pour que les données s'affichent.

![Tableau de bord des analytics](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Aperçu du tableau de bord

Accédez à **Recherche > Analytics de recherche** pour accéder au tableau de bord. La page affiche :

**Cartes des statistiques** - Métriques rapides pour aujourd'hui et la semaine dernière :
- Total des recherches aujourd'hui
- Total des recherches cette semaine
- Requêtes sans résultats (recherches ne renvoyant aucun produit)
- Temps de réponse moyen en millisecondes

**Tableau des requêtes les plus courantes** - Termes de recherche les plus fréquents avec les comptes de résultats

**Requêtes sans résultats** - Recherches qui n'ont renvoyé aucun résultat (critique pour l'amélioration)

**Liste des requêtes** - Toutes les recherches individuelles avec des filtres

## Statistiques d'aujourd'hui

**Total des recherches d'aujourd'hui** - Nombre total de requêtes de recherche depuis minuit dans le fuseau horaire de votre boutique. Comprend à la fois les requêtes de complétion automatique et les pages de recherche complètes.

**Requêtes uniques d'aujourd'hui** - Nombre de termes de recherche distincts utilisés aujourd'hui. Si 5 clients cherchent tous "laptop", cela compte comme 1 requête unique malgré 5 recherches totales.

**Recherches sans résultats aujourd'hui** - Recherches d'aujourd'hui qui n'ont renvoyé aucun produit. Un nombre élevé de recherches sans résultats indique des produits manquants ou une couverture insuffisante des synonymes.

Les données sont mises à jour en temps réel à mesure que les recherches se produisent.

## Statistiques hebdomadaires

**Total de la semaine** - Total des recherches au cours des 7 derniers jours

**Requêtes uniques** - Termes de recherche distincts utilisés cette semaine

**Croissance par rapport à la semaine précédente** - Pourcentage de changement par rapport à la semaine précédente (si affiché)

Utilisez les données hebdomadaires pour identifier les tendances : une augmentation du volume de recherche est souvent corrélée à une croissance du trafic ou à des campagnes de marketing.

## Temps de réponse moyen

⚠️ **SURVEILLANCE DES PERFORMANCE**

Temps moyen (en millisecondes) pour exécuter les requêtes de recherche. Objectifs de temps de réponse :

| Type de requête | Objectif | Seuil d'alerte |
|----------------|--------|----------------|
| Complétion automatique | < 200 ms | > 300 ms de manière continue |
| Recherche complète | < 500 ms | > 800 ms de manière continue |

Si le temps de réponse moyen dépasse les seuils d'alerte :
1. Vérifiez **Paramètres de recherche > Onglet de mise en cache** - augmentez les durées de mise en cache (TTL)
2. Révisez **Onglet d'indexation approfondie** - désactivez les fonctionnalités coûteuses (indexation des documents, indexation des avis sur de grands catalogues)
3. Consultez le guide [Optimisation des performances de recherche](/en/admin/help/search-performance-optimization/)

## Requêtes les plus courantes

Le tableau des requêtes les plus courantes affiche les termes de recherche les plus fréquents :

**Utilisez ces données pour** :
- **Mettre en avant les produits populaires** - Si "écouteurs sans fil" est une recherche courante, mettez en avant ces produits en évidence sur votre page d'accueil
- **Décisions d'inventaire** - Un volume élevé de recherche pour une catégorie indique une demande
- **Identifier les tendances** - Les recherches saisonnières révèlent ce qui est actuellement populaire
- **Création de contenu** - Rédigez des articles de blog ou des guides sur les sujets fréquemment recherchés

Révisez les requêtes les plus courantes mensuellement pour aligner votre merchandising sur les intérêts des clients.

## Requêtes sans résultats

**CRITIQUE POUR L'AMÉLIORATION** - Les requêtes sans résultats sont une mine d'or pour optimiser votre boutique.

Les requêtes sans résultats surviennent pour trois raisons principales :

### 1. Produits manquants

Les clients cherchent des produits que vous ne vendez pas.

**Exemple** : Recherches répétées pour "tapis de yoga" mais vous ne vendez que du matériel de fitness, pas de fournitures de yoga.

**Action** : Considérez l'ajout de ces produits à votre catalogue si les recherches sont fréquentes.

### 2. Synonymes manquants

Les clients utilisent des termes qui ne correspondent pas à vos descriptions de produits.

**Exemple** : Les clients cherchent "laptop" mais vos produits disent tous "ordinateur portable".

**Action** : Créez une carte des synonymes associant les termes des clients à votre langage de produit. Voir [Gestion des synonymes et redirections](/en/admin/help/managing-synonyms-redirects/).

### 3. Mauvaise correspondance floue

Les fautes de frappe ou les orthographes incorrectes ne correspondent même pas avec la recherche floue activée.

**Exemple** : La recherche "accomodate" ne trouve pas les produits "accommodate".

**Action** : 
- Réduisez le seuil de similarité dans **Paramètres de recherche > Onglet de correspondance floue** (de 0,80 à 0,75)
- Ajoutez des synonymes unidirectionnels pour les fautes d'orthographe courantes

**Workflow hebdomadaire** : 
1. Révisez les requêtes sans résultats chaque lundi
2. Catégorisez : Produits manquants, synonymes manquants ou fautes d'orthographe
3. Ajoutez des synonymes pour les termes fréquemment recherchés
4. Notez les lacunes de produits pour la planification de l'inventaire

## Détails de la requête

Cliquez sur n'importe quelle requête dans la liste pour afficher les détails complets : 

**Champs suivis** : 
- **Texte de la requête** - Ce que le client a cherché
- **Horodatage** - Quand la recherche s'est produite
- **Nombre de résultats** - Combien de résultats ont été renvoyés
- **Temps de réponse** - Millisecondes pour exécuter (surveillance des performances)
- **Utilisateur** - Client connecté (si la prise en charge utilisateur est activée)
- **ID de session** - Identifiant d'une session anonyme
- **Langue** - Langue du magasin pendant la recherche
- **Moteur** - Le moteur de recherche qui a traité la requête

## Filtres et recherche

Utilisez des filtres pour analyser des segments spécifiques : 

**Hiérarchie de dates** - Filtrez par date, mois ou année

**Filtre de langue** - Voir les recherches par langue (utile pour les magasins multilingues)

**Filtre du moteur** - Comparez le comportement de recherche entre différents moteurs

**Commutateur de requêtes sans résultats** - Affichez uniquement les requêtes qui n'ont renvoyé aucun résultat

**Boîte de recherche** - Trouvez un texte de requête spécifique

## Exportation des données

Cliquez sur **Exporter** pour télécharger les données des requêtes au format CSV pour une analyse approfondie dans Excel ou des outils de données.

**Le CSV inclut** : 
- Tous les textes de requête
- Horodatages
- Comptes de résultats
- Temps de réponse
- Données de langue et de moteur

Utilisez les exports pour : 
- Analyse des tendances au fil du temps
- Identifier les motifs de recherche saisonniers
- Audit des performances
- Présentation aux parties prenantes

## Considérations de confidentialité

La prise en charge des analytics de recherche respecte la confidentialité : 

**Suivi des utilisateurs** (optionnel) - Relie les recherches aux comptes de clients connectés. Désactivez pour la conformité RGPD/CCPA dans **Paramètres de recherche > Onglet Analytics**.

**Suivi des sessions** (par défaut) - Utilise des identifiants de sessions anonymes pour suivre les motifs de recherche sans identifier les clients. Respectueux de la confidentialité.

**Gestion des données** - Les requêtes de recherche restent dans la base de données indéfiniment. Mettez en œuvre une politique de conservation personnalisée si nécessaire pour la conformité.

## Utilisation des analytics pour améliorer la recherche

Insights actionnables à partir des analytics de recherche : 

**Tâches hebdomadaires** : 
- Révisez les résultats nuls et ajoutez des synonymes pour les termes courants
- Surveillez les temps de réponse et optimisez si lent constamment
- Identifiez les recherches principales et assurez-vous que ces produits sont bien approvisionnés

**Tâches mensuelles** : 
- Analysez les requêtes principales pour orienter le choix des produits
- Exportez les données pour identifier les tendances saisonnières
- Révisez les motifs de recherche spécifiques à la langue
- Suivez les comptes de redirection pour optimiser les raccourcis de navigation

**Tâches trimestrielles** : 
- Audit des synonymes (les résultats nuls ont-ils diminué ?)
- Comparez la croissance du volume de recherche par rapport au trafic global
- Test A/B des changements de pondération et mesurez la pertinence des résultats
- Révisez si de nouvelles catégories de produits devraient être ajoutées en fonction de la demande de recherche

## Conseils

- **Les requêtes sans résultats sont des mines d'or pour l'amélioration** - Elles vous indiquent directement ce que les clients veulent et que vous ne fournissez pas
- **Révisez les analytics le matin du lundi** - Commencez votre semaine en optimisant en fonction des données de la semaine précédente
- **Temps de réponse >300 ms de manière continue = investigatez** - Vérifiez d'abord les paramètres de mise en cache, puis les fonctionnalités d'indexation approfondie
- **Exportez CSV pour l'analyse des tendances** - L'analyse en feuille de calcul révèle des motifs non évidents dans l'interface d'administration
- **Créez des synonymes avant d'ajouter des produits** - Si les clients cherchent "étuis pour tablettes" mais que vous les appelez "couvertures de protection", ajoutez d'abord le synonyme
- **Suivez les motifs de recherche saisonnières** - "Chaussures d'hiver" en octobre, "maillot de bain" en mars - approvisionnez votre inventaire en conséquence