---
title: Travaux de traduction
---

Travaux de traduction automatisent la traduction en masse de grands volumes de contenu. Au lieu de traduire manuellement les produits un par un, créez un travail qui traduit tout votre catalogue - ou des sous-ensembles spécifiques - en arrière-plan. Les travaux s'exécutent de manière asynchrone, donc vous pouvez continuer à travailler pendant que des centaines ou des milliers de champs sont traduits automatiquement.

Utilisez les travaux de traduction lorsqu'il s'agit d'activer de nouvelles langues, d'importer de nouveaux produits ou de rattraper le contenu non traduit.

## Qu'est-ce qu'un travail de traduction ?

Un travail de traduction est une tâche en arrière-plan qui :

1. **Scanne le contenu** pour les champs traduisibles (produits, pages, publications de blog, etc.)
2. **Identifie les champs non traduits ou obsolètes** en fonction de l'étendue de votre travail
3. **Envoie les champs à l'engine de traduction** (modèle d'IA local ou fournisseur externe)
4. **Enregistre les traductions** dans votre contenu
5. **Signale la fin** avec des statistiques sur les champs traduits

Les travaux s'exécutent via la file d'attente Celery, donc ils ne bloquent pas votre interface d'administration.

## Quand utiliser les travaux de traduction

**Lancement d'une nouvelle langue**:
- Activez le allemand comme nouvelle langue
- Créez un travail : Traduire tous les produits en allemand
- Résultat : Tout le catalogue disponible en allemand dans les minutes/heures (selon la taille)

**Importation de nouveaux produits**:
- Importez 500 nouveaux produits en anglais
- Créez un travail : Traduire les nouveaux produits vers toutes les langues actives
- Résultat : Nouvelle gamme immédiatement disponible dans tous les marchés

**Rattraper les lacunes**:
- Le rapport de couverture montre que les Produits ne sont que 60% traduits en français
- Créez un travail : Traduire uniquement les champs manquants en français
- Résultat : La couverture française augmente à ~100%

**Mettre à jour les traductions obsolètes**:
- Le modèle de traduction s'est amélioré ou un nouveau fournisseur est disponible
- Créez un travail : Ré-traduire tous les produits en espagnol
- Résultat : Une meilleure qualité des traductions espagnoles dans tout le catalogue

## Création d'un travail de traduction

Accédez à **Paramètres > Travaux de traduction** et cliquez sur **+ Créer un travail**.

### Configuration du travail

**Nom du travail** - Étiquette descriptive (ex. : "Traduire les produits en allemand", "Nouvelles publications de blog - toutes les langues")

**Type de contenu** - Ce que vous souhaitez traduire :
- Produits
- Catégories de produits
- Pages
- Publications de blog
- Métadonnées SEO
- Modèles d'e-mails
- Tous les types de contenu

**Langue source** - La langue depuis laquelle vous traduisez (généralement votre langue par défaut)

**Langue(s) cible(s)** - Une ou plusieurs langues vers lesquelles traduire (sélectionnez plusieurs pour une traduction parallèle)

**Étendue** - Quel sous-ensemble de contenu :
- **Tous les éléments** - Traduire tout, indépendamment des traductions existantes
- **Seulement les non traduits** - Ignorer les champs qui ont déjà des traductions
- **Créés/mis à jour depuis une date** - Seulement le contenu nouveau ou récemment modifié
- **Éléments spécifiques** - Sélectionnez des produits/pages individuels (filtrage avancé)

**Engine de traduction** - Quel service utiliser :
- Modèle d'IA local (par défaut, sans coûts d'API)
- Fournisseur externe spécifique (DeepL, Google, Azure, AWS)
- Auto-sélection (utilise la préférence configurée)

**Verrouiller les traductions** - Si les champs traduits sont verrouillés contre les surécritures futures automatiques (utile pour les traductions revues)

### Options avancées

**Ignorer les champs verrouillés** - Si activé, respecte les traductions verrouillées existantes (recommandé)

**Écraser les existantes** - Ré-traduire même si des traductions existent (utiliser pour les améliorations de qualité)

**Filtres de champ** - Traduire uniquement des champs spécifiques (ex. : noms et descriptions de produits, ignorer les attributs)

**Taille du lot** - Combien d'éléments traiter à la fois (par défaut : 50, augmenter pour un traitement plus rapide si le serveur peut le gérer)

**Priorité** - Les travaux de haute priorité s'exécutent avant les travaux de priorité normale (utiliser avec modération)

## Cycle de vie et statut des travaux

Les travaux progressent à travers ces états :

**En file d'attente** - Travail créé, en attente qu'un worker le prenne

**En cours de traitement** - Worker traduisant activement le contenu

**Terminé** - Toutes les traductions terminées avec succès

**Échoué** - Le travail a rencontré des erreurs (vérifiez le journal d'erreurs)

**Annulé** - Arrêté manuellement par l'administrateur

**En pause** - Suspens temporaire (peut être reprise)

## Surveillance de la progression du travail

La page détaillée du travail affiche :

**Barre de progression** - Pourcentage terminé

**Statistiques** : 
- Nombre total d'éléments à traduire
- Éléments terminés
- Éléments restants
- Temps estimé restant

**Journal en temps réel** - Flux d'activité de traduction (utile pour le dépannage)

**Compteur d'erreurs** - Combien de champs ont échoué à traduire (avec les raisons)

## Résultats et statistiques des travaux

Lorsqu'un travail est terminé, la page des résultats affiche :

**Résumé** : 
- Champs traités au total
- Traduits avec succès
- Traductions échouées
- Passés (déjà traduits, verrouillés ou exclus par les filtres)

**Détail par élément** : 
- Quels produits/pages ont été traduits
- Combien de champs par élément
- Toute erreur rencontrée

**Métriques de performance** : 
- Temps total écoulé
- Moyenne de traductions par seconde
- Engine de traduction utilisé

## Gestion des traductions échouées

Si certaines traductions échouent :

**Vérifiez le journal d'erreurs** - Identifie les champs qui ont échoué et pourquoi

**Causes courantes d'échec** : 
- Limite de taux d'API atteinte (fournisseur externe)
- Timeout de l'engine de traduction (texte très long)
- Format de champ invalide (erreur de parsing JSON)
- Le modèle ne prend pas en charge le couple de langues

**Options de nouvelle tentative** : 
- Corrigez le problème sous-jacent
- Créez un nouveau travail pour les éléments ayant échoué
- Utilisez un autre engine de traduction

## Annulation et mise en pause des travaux

**Annuler** - Arrête le travail immédiatement, abandonne toutes les traductions en cours (les traductions terminées sont enregistrées)

**Mettre en pause** - Arrête temporairement le travail, peut reprendre plus tard à partir de là où il s'était arrêté

**Reprendre** - Continue un travail mis en pause

Utilisez la mise en pause/reprise lorsque vous avez besoin de libérer temporairement les ressources du serveur.

## Stratégies de travaux en masse

**Stratégie 1 : Langue par langue** : 
- Créez des travaux séparés pour chaque langue cible
- Plus facile de surveiller la progression par langue
- Peut prioriser les langues importantes
- Répartit la charge au fil du temps

**Stratégie 2 : Tout en une fois** : 
- Un seul travail traduisant vers toutes les langues actives
- Termination globale plus rapide
- Charge du serveur plus élevée pendant le traitement
- Gestion des travaux plus simple

**Stratégie 3 : Type de contenu par type de contenu** : 
- Traduisez d'abord les produits (priorité la plus élevée)
- Ensuite les catégories, pages, publications de blog
- Permet un déploiement progressif
- Plus facile de tester et vérifier les traductions

Choisissez en fonction de votre capacité du serveur, de l'urgence et de la taille du catalogue.

## Planification des travaux

Planifiez des travaux récurrents pour gérer automatiquement le nouveau contenu : 

**Travaux quotidiens** - Traduire tout produit créé/mis à jour au cours des 24 dernières heures

**Travaux hebdomadaires** - Rattraper les lacunes de traduction hebdomadaires

**Après l'importation** - Démarrer automatiquement un travail après l'importation en masse de produits

**À l'activation d'une langue** - Créer automatiquement un travail lors de l'activation d'une nouvelle langue

Les travaux planifiés maintiennent les traductions à jour sans intervention manuelle.

## Considérations de performance

**Modèle d'IA local** : 
- ~100-500 traductions/second (dépend du serveur)
- Intensif en CPU pendant le traitement
- Aucune limite de taux d'API
- Gratuit (aucun coût par traduction)

**Fournisseurs externes** : 
- Les limites de taux varient (DeepL : 500k caractères/mois sur le niveau gratuit)
- La latence API ajoute un surcoût
- Meilleure qualité mais coûte de l'argent
- Limites de requêtes simultanées

**Travaux volumineux** (>10 000 champs) : 
- Exécuter pendant les heures creuses
- Surveiller les ressources du serveur
- Considérer de diviser en lots plus petits
- Tester avec un sous-ensemble d'abord

## Conseils

- **Commencez petit** - Testez les travaux sur un sous-ensemble (ex. : 10 produits) avant de lancer la traduction du catalogue complet
- **Utilisez l'étendue "Seulement les non traduits"** - Plus rapide et évite de ré-traduire du contenu déjà bon
- **Surveillez votre premier travail de près** - Vérifiez les erreurs ou les problèmes de qualité avant de lancer des travaux plus importants
- **Planifiez les travaux pendant les périodes à faible trafic** - La traduction est intensive en CPU/API
- **Verrouillez les traductions revues** - Empêche les travaux en masse de surécrire vos modifications manuelles
- **Gardez les travaux ciblés** - Les travaux plus petits et ciblés sont plus faciles à dépanner que les travaux massifs "traduire tout"
- **Vérifiez des échantillons après la fin** - Vérifiez quelques traductions aléatoires pour la qualité avant de considérer le travail comme réussi
- **Exportez/backup avant les grands travaux** - Au cas où vous devriez revenir en arrière sur les modifications en masse

Souvenez-vous : Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.