---
title: Service de traduction
---

Le service de traduction fournit des traductions alimentées par l'intelligence artificielle pour les descriptions de produits, le contenu des pages, les publications de blog, les champs SEO et d'autres contenus du commerçant. Les traductions s'exécutent localement sur votre serveur ou via des fournisseurs externes, donc votre contenu reste privé et les traductions ont lieu en quelques secondes.

![Gestion des langues](/static/core/admin/img/help/translation-service/language-management.webp)

## Comment ça marche

1. Vous **activez les langues** pour votre magasin (par exemple, anglais, allemand, japonais)
2. Lorsque vous créez ou modifiez du contenu (produits, pages, publications de blog), vous rédigez dans votre langue par défaut
3. Cliquez sur **Traduire** sur tout champ traduisible pour générer des traductions en IA vers vos langues activées
4. Les traductions sont stockées avec le contenu original et sont servies automatiquement en fonction de la langue du visiteur

## Gestion des langues

Accédez à **Paramètres > Langues** pour gérer les langues de votre magasin.

### Tableau de bord des langues

Le tableau de bord affiche :
- **Total des langues** — Toutes les langues disponibles dans le système (100+)
- **Langues activées** — Langues actuellement activées pour votre magasin
- **Couverture du modèle** — Le nombre de langues prises en charge par le modèle de traduction installé

### Activation des langues

1. Trouvez la langue dans la colonne **Langues disponibles**
2. Cliquez sur la langue pour la déplacer vers la colonne **Langues activées**
3. La langue est immédiatement disponible pour les traductions et apparaît dans le commutateur de langues de votre magasin

### Langue par défaut

Une langue est marquée comme **langue par défaut**. Il s'agit de :
- La langue dans laquelle vous rédigez du contenu
- La langue de secours lorsqu'une traduction n'existe pas
- La langue affichée lorsque les visiteurs n'ont pas sélectionné de préférence

## Modèles de traduction

Spwig inclut un moteur de traduction en IA local qui s'exécute entièrement sur votre serveur — aucun données n'est envoyée vers des services externes.

### Modèles disponibles

| Modèle | Langues | Vitesse | Qualité |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Rapide | Bon pour les paires de langues courantes |
| **M2M100-1.2B** | 100 | Modérée | Meilleure qualité, utilisation plus élevée des ressources |
| **NLLB-200** | 200+ | Modérée | Meilleure couverture, y compris les langues rares |

### Sélection du modèle

La page de gestion des langues indique quel modèle est installé et sa couverture linguistique. Le modèle s'exécute comme un service local en utilisant CTranslate2 pour une inférence efficace.

## Fournisseurs externes

Pour les magasins qui préfèrent la traduction basée sur le cloud ou qui ont besoin d'une qualité linguistique spécifique, Spwig prend en charge les fournisseurs de traduction externes.

| Fournisseur | Description |
|----------|-------------|
| **DeepL** | Qualité de traduction premium pour les langues européennes et asiatiques |
| **Google Translate** | Couverture linguistique étendue avec la traduction par machine neuronale |
| **Azure Translator** | Service de traduction neuronal de Microsoft |
| **AWS Translate** | Traduction par machine d'Amazon avec prise en charge des termes personnalisés |

### Connexion à un fournisseur

1. Accédez à **Paramètres > Fournisseurs de traduction**
2. Sélectionnez le fournisseur et entrez votre clé API
3. Définissez le fournisseur comme moteur de traduction préféré
4. Les traductions utiliseront le fournisseur externe au lieu du modèle local

Vous pouvez utiliser des fournisseurs externes en parallèle avec le modèle local — par exemple, utilisez DeepL pour les langues européennes et le modèle local pour tout le reste.

## Traduction du contenu

### Traduction au niveau des champs

Les champs traduisibles (noms de produits, descriptions, titres SEO, etc.) affichent un **bouton de traduction** à côté du champ. Cliquez dessus pour :

1. **Traduire vers toutes les langues activées** — Génère des traductions pour chaque langue active en une seule fois
2. **Traduire vers une langue spécifique** — Sélectionnez des langues individuelles à traduire

Les traductions apparaissent dans les onglets de langue de l'éditeur. Vous pouvez les réviser et modifier manuellement toute traduction générée par la machine.

### Tâches de traduction en masse

Pour de grandes quantités de contenu, utilisez **les tâches de traduction** :

1. Accédez à **Paramètres > Tâches de traduction**
2. Créez un nouveau travail en sélectionnant :
   - **Type de contenu** — Produits, pages, publications de blog, catégories, etc.
   - **Langue source** — La langue à partir de laquelle traduire
   - **Langues cibles** — Une ou plusieurs langues vers lesquelles traduire
   - **Étendue** — Tous les contenus, ou uniquement les champs non traduits
3. Soumettez la tâche — elle s'exécute en arrière-plan via une file d'attente de tâches
4. Suivez la progression dans la liste des tâches (en attente → en cours de traitement → terminée)

Les tâches en masse sont utiles lorsque vous activez une nouvelle langue et que vous souhaitez traduire tout votre catalogue en une seule fois.

## Gestion des traductions

### Révision des traductions

Champ traduit suit : 
- **Statut de traduction** — Si le champ a été traduit automatiquement, modifié manuellement ou manquant
- **Statut de verrouillage** — Les traductions verrouillées ne seront pas remplacées par les futures traductions automatiques
- **Dernière traduction** — Quand la traduction a été générée ou modifiée pour la dernière fois

### Verrouiller les traductions

Si vous modifiez manuellement une traduction générée par la machine pour l'améliorer, **verrouillez** le champ pour empêcher qu'il soit remplacé la prochaine fois qu'une traduction en masse s'exécutera. Les champs verrouillés sont ignorés lors des traductions automatiques.

### Couverture des traductions

Le suivi de la couverture indique quel pourcentage de votre contenu est traduit pour chaque langue. Accédez à **Paramètres > Langues** pour voir : 
- Les pourcentages de complétion par langue
- Quels types de contenu ont des lacunes
- Les champs qui nécessitent encore une traduction

## Surcharge des traductions de l'interface utilisateur

Au-delà du contenu des produits et des pages, vous pouvez personnaliser les traductions des **chaînes d'interface utilisateur du frontend** — boutons, étiquettes, messages et autres textes d'interface affichés aux visiteurs.

Accédez à **Paramètres > Surcharges de l'interface utilisateur** pour : 
1. Rechercher une chaîne spécifique (par exemple, "Ajouter au panier")
2. Entrez votre traduction préférée pour chaque langue
3. Enregistrer — la surcharge prend effet immédiatement

Il y a environ 300 chaînes d'interface utilisateur disponibles pour la personnalisation. Les surcharges prennent le pas sur les traductions par défaut.

## Conseils

- Commencez par activer uniquement les langues que vos clients utilisent vraiment — vous pouvez toujours en ajouter plus plus tard.
- Utilisez le **modèle d'IA local** pour les traductions quotidiennes — il est rapide, privé et n'a aucun coût par traduction.
- Pensez à **DeepL** si vous avez besoin de la meilleure qualité pour les langues européennes clés — il produit régulièrement des traductions plus naturelles que les modèles généraux.
- Vérifiez toujours les **traductions générées par la machine** pour les noms de produits, les termes de marque et les copies de marketing — l'IA gère bien le contenu technique mais peut manquer de nuances dans le texte créatif.
- **Verrouillez** toute traduction que vous avez améliquée manuellement pour la protéger contre l'être remplacée lors des exécutions de traduction en masse.
- Utilisez **les tâches de traduction en masse** lors de l'activation d'une nouvelle langue pour traduire tout votre catalogue en une seule passe plutôt que de traduire les produits un par un.
- Personnalisez les **surcharges de l'interface utilisateur** pour correspondre à la voix de votre marque — par exemple, changez "Ajouter au panier" en "Acheter maintenant" si cela convient mieux à votre magasin.

Souvenez-vous : Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.