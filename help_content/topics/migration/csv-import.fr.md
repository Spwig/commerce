---
title: Importation à partir de fichiers CSV
---

L'importation CSV est le moyen de migration par défaut pour tout magasin que Spwig ne connecte pas directement. Si vous venez de BigCommerce, PrestaShop, Squarespace, Wix, d'une feuille de calcul que vous avez maintenue à la main, ou d'un système personnalisé sans API que Spwig comprend, c'est ici que vous arrivez — exportez vos données vers des fichiers CSV et chargez-les ici au lieu de vous connecter en direct.

Ce guide couvre quand utiliser le CSV, ce qu'il ne peut pas transférer, les cinq fichiers impliqués, comment les préparer, et comment fonctionne le mappage des colonnes.

## Quand utiliser le CSV au lieu d'une connexion API

Spwig se connecte directement à WooCommerce, Shopify et Magento 2/Adobe Commerce — voir [Aperçu de la migration des données](migration-overview) pour ces derniers. Pour tout autre plateforme, le CSV est votre seule option ; il n'y a aucune intégration directe pour BigCommerce, PrestaShop, Squarespace ou Wix. C'est également le bon choix si vous consolidez des données à partir d'une feuille de calcul, si vous retirez un magasin personnalisé, ou si vous souhaitez contrôler exactement ce qui est importé en curant vous-même les fichiers.

## Ce que le CSV ne peut pas faire

Avant de préparer quoi que ce soit, sachez ce que ce mode d'importation laisse de côté — c'est la source la plus grande de surprise pour les commerçants utilisant l'importation CSV :

- **Aucune image de produit.** Les produits s'importent sans images attachées ; téléchargez-les ultérieurement.
- **Aucune variante.** Chaque produit est créé comme un produit simple. Reconstruisez les structures de taille/couleur/stylesheet dans Spwig après l'importation.
- **Aucun coupon.** Les codes de réduction et les promotions ne font pas partie du format CSV.
- **Aucun contenu de blog.** Il n'y a aucun fichier CSV pour les publications ou articles.

Aucun de cela ne bloque l'importation — cela signifie simplement que les produits nécessiteront un suivi après leur importation dans Spwig. Voir [Après votre migration](after-migration-review) pour la liste complète des vérifications post-importation.

## Les cinq fichiers

L'étape CSV du wizard propose cinq entrées de fichiers, chacune avec un bouton **Télécharger le modèle**. Commencez à partir de ces modèles plutôt que de construire des fichiers à partir de zéro — ils garantissent les bons noms de colonnes et permettent à la détection automatique de faire plus du travail à l'étape 4.

| Fichier | Obligatoire ? |
|---|---|
| Produits | **Obligatoire** |
| Catégories | Facultatif |
| Clients | Facultatif |
| Commandes | Facultatif |
| Avis | Facultatif |

Le seul fichier que Spwig exige est **Produits** — les autres peuvent être laissés vides si vous n'avez pas encore ces données.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Étape 2 avec CSV sélectionné, montrant les cinq entrées de fichiers et leurs boutons Télécharger le modèle
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Produits (Obligatoire)

| Colonne | Description |
|---|---|
| `id` | Identifiant unique dans vos données source ; non affiché aux clients. |
| `name` | Le titre du produit. **Essentiel.** |
| `slug` | Version amicale des URL du nom ; généré automatiquement à partir de `name` si vide. |
| `description` | La description affichée sur le point de vente. |
| `price` | Le prix régulier du produit. **Essentiel.** |
| `sku` | Unité de gestion des stocks — utilisé pour correspondre lorsque **Ignorer les éléments existants** est activé. |
| `stock_quantity` | Unités actuellement en stock. |
| `category` | Nom de la catégorie à laquelle appartient ce produit. Doit correspondre à un `name` dans votre fichier de catégories. |

### Catégories

| Colonne | Description |
|---|---|
| `id` | Identifiant unique dans vos données source. |
| `name` | Le nom de la catégorie. **Essentiel.** |
| `slug` | Version amiciale des URL du nom ; généré automatiquement si vide. |
| `description` | Texte de description de la catégorie. |
| `parent_id` | L'`id` de la catégorie parente. Vide signifie niveau supérieur. |

### Clients

| Colonne | Description |
|---|---|
| `id` | Identifiant unique dans vos données source. |
| `email` | Adresse e-mail du client. **Essentiel** — relie les commandes et les avis au client correct. |
| `first_name` | Prénom du client. |
| `last_name` | Nom de famille du client. |
| `phone` | Numéro de téléphone du client. |

### Commandes

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Colonne | Description |
|---|---|
| `id` | Identifiant unique dans vos données source. |
| `customer_email` | Adresse e-mail du client ayant passé la commande. **Essentiel** — relie la commande à un enregistrement client. |
| `order_date` | La date à laquelle la commande a été passée. |
| `status` | L'état de la commande (par exemple, terminée, en traitement). |
| `total` | Le montant total de la commande. **Essentiel.** |
| `currency` | Code de la devise du montant total de la commande. |

### Avis (Optionnel)

| Colonne | Description |
|---|---|
| `id` | Identifiant unique dans vos données source. |
| `product_id` | L'`id` du produit sur lequel porte l'avis, correspondant à votre fichier de produits. **Essentiel** — relie l'avis au produit approprié. |
| `customer_email` | Adresse e-mail du client ayant rédigé l'avis. |
| `rating` | La note attribuée en étoiles. |
| `comment` | Le texte de l'avis. |
| `date` | La date à laquelle l'avis a été publié. |

## Préparation de vos fichiers

- **Enregistrez en UTF-8** pour éviter les caractères accentués corrompus, en particulier provenant d'une encodage source différent.
- **Citez les champs contenant des virgules** — entourez une description ou un nom contenant une virgule de guillemets doubles afin qu'il ne soit pas mal interprété comme une rupture de colonne.
- **Incluez une ligne d'en-tête.** La première ligne doit contenir vos noms de colonnes — un fichier sans ligne d'en-tête est refusé.
- **Construisez la hiérarchie des catégories avec `parent_id`.** Donnez à chaque catégorie un `id` unique, puis définissez le `parent_id` d'une sous-catégorie à l'`id` de sa catégorie parente. Laissez vide pour indiquer un niveau supérieur.
- **Reliez les commandes aux clients via `customer_email`**, correspondant à la colonne `email` de votre fichier clients (ou un enregistrement invité est créé), plutôt que de dépendre des numéros d'identification internes, qui correspondent rarement entre les plateformes.
- **Reliez les avis aux produits via `product_id`**, correspondant à une valeur de la colonne `id` de votre fichier de produits, ou cet avis sera ignoré.

## Mappage des colonnes à l'étape 4

L'étape 4 affiche un panneau de mappage des colonnes CSV. Spwig scanne vos en-têtes et détecte automatiquement les correspondances probables par rapport à une liste d'alias courants — par exemple, un champ `sku` correspond également à `barcode`, `part_number` ou `item_number`. Les en-têtes exportés directement d'une autre plateforme correspondent souvent correctement sans aucun travail manuel.

Pour chaque colonne, vous pouvez accepter la devinette détectée automatiquement, la remplacer en choisissant un autre champ de destination, ou choisir «— Ignorer cette colonne —» pour l'exclure. Les mappages sont enregistrés et réutilisés lors des futures migrations CSV. Consultez [Migration Field Mapping](migration-field-mapping) pour obtenir une vue d'ensemble de l'étape 4, y compris les mappages automatiques des champs, le mappage des catégories et les options d'impôt/expédition.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Panel de mappage des colonnes CSV de l'étape 4 montrant les mappages détectés automatiquement avec des menus déroulants de remplacement
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Erreurs courantes et ce qu'elles signifient

| Erreur | Signification |
|---|---|
| `Products CSV is required.` | Vous avez tenté de continuer sans avoir téléchargé un fichier de produits. C'est le seul fichier que Spwig exige — téléchargez-en un pour continuer. |
| `{Type} CSV has no headers.` | La première ligne du fichier nommé est vide ou manquante. Ajoutez une ligne d'en-tête avec les noms des colonnes et rétéléchargez-le. |
| `{Type} CSV could not be read: ...` | Spwig n'a pas pu analyser le fichier nommé — cela se produit généralement avec un fichier corrompu, une encodage incorrecte ou un fichier qui n'est pas réellement CSV malgré son extension. Réexportez-le et vérifiez qu'il s'ouvre correctement avant de le télécharger à nouveau. |

## Exécution de l'import

Une fois le mappage confirmé, démarrez la migration à partir de l'étape 5. Elle s'exécute en arrière-plan, donc vous pouvez fermer la fenêtre — le progrès et un journal en direct sont disponibles si vous revenez avant la fin. Consultez [After Your Migration](after-migration-review) pour vérifier les résultats.

Souvenez-vous que l'import CSV laisse spécifiquement **les images de produit** et **les variantes** pour que vous les finissiez à la main — aucune de ces deux choses ne transmet automatiquement, peu importe à quel point vos fichiers étaient complets.

## Conseils

Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Commencez par le bouton Télécharger le modèle** pour chaque fichier — cela vous évite de perdre du temps à corriger les fautes de frappe dans les noms des colonnes qui autrement passeraient inaperçues et nécessiteraient un mappage manuel.
- **Corrigez les incohérences de `product_id` avant de charger les avis** — un avis dont le `product_id` ne correspond à aucun produit `id` n'a rien à quoi s'attacher et est ignoré.
- **Ne renommez pas les en-têtes provenant d'une exportation d'un autre système** — la détection automatique les reconnaît souvent tels quels via des alias, donc le mappage n'aura peut-être aucun travail manuel à effectuer.
- **Réservez du temps pour les images et les variantes juste après l'importation** — ce sont les deux choses que le CSV n'apporte jamais, et elles sont faciles à oublier jusqu'à ce qu'un client remarque une page de produit vide.
- **Utilisez `parent_id` pour modéliser des catégories à plusieurs niveaux** — faites pointer le `parent_id` d'une sous-catégorie vers l'`id` de sa catégorie parente pour la hiérarchiser ; laissez-le vide pour les catégories de niveau supérieur.
- **Ré-exportez et vérifiez à nouveau en cas d'erreur "could not be read"** — il s'agit presque toujours d'un problème d'encodage ou de corruption dans le fichier source, et non d'une erreur à corriger dans Spwig.