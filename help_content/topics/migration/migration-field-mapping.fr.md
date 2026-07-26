---
title: Mappage des champs de migration
---

Chaque plateforme nomme les choses un peu différemment — le `regular_price` de WooCommerce n'est pas le `price` de Shopify, et une colonne CSV nommée `barcode` pourrait être exactement la même chose que ce à quoi Spwig s'attend, à savoir `sku`. L'étape 4 de l'assistant de migration, **Configurer le mappage des champs**, est l'endroit où vous vérifiez comment vos données sources s'inscriront dans Spwig avant que l'import ne commence réellement. Ce sujet aborde chaque bloc de cette page et s'applique aux migrations WooCommerce, Shopify, Magento et CSV, avec des différences de plateforme mentionnées là où elles comptent. Pour les informations d'identification et les étapes précédentes de l'assistant, consultez [Migrer depuis WooCommerce](migrate-from-woocommerce) ou le guide équivalent pour votre plateforme.

## Mappages automatiques

Ce bloc affiche, pour chaque type de données que vous avez sélectionné à l'étape 3, une liste en lecture seule des champs sources et du champ Spwig correspondant — par exemple, le `name` d'un produit qui correspond au titre du produit Spwig, ou l'`email` d'un client qui correspond à l'adresse e-mail du compte. Seuls les types de données que vous importez réellement apparaissent ici ; si vous n'avez pas sélectionné les Avis à l'étape 3, il n'y a pas de section Avis sur cette page.

Comme ces lignes sont en lecture seule, il n'y a rien à configurer — elles existent pour que vous puissiez vérifier le mappage avant de confirmer l'import. Si un mappage semble incorrect pour vos données, il n'y a aucun moyen de le modifier à partir de cette interface ; vos options sont de corriger les données sources avant la migration, ou de corriger les enregistrements concernés dans Spwig après la fin de l'import.

## Mappage des colonnes CSV

Ce bloc n'apparaît que pour les migrations CSV, avec un tableau par fichier que vous avez téléchargé. Spwig détecte automatiquement les correspondances probables à partir des en-têtes de vos colonnes — par exemple, un mappage `sku` reconnaît également des en-têtes comme `barcode`, `part_number` ou `item_number` — donc dans la plupart des cas, vous n'avez rien à modifier ici.

Chaque colonne CSV obtient un menu déroulant listant les champs que Spwig attend pour ce type de fichier :

- **produits** — `id, name, slug, description, price, sku, stock_quantity, category`
- **catégories** — `id, name, slug, description, parent_id`
- **clients** — `id, email, first_name, last_name, phone`
- **commandes** — `id, customer_email, order_date, status, total, currency`
- **avis** — `id, product_id, customer_email, rating, comment, date`

Chaque menu déroulant inclut également **— Ignorer cette colonne —**, ce qui exclut cette colonne de l'importation entièrement. Remplacez le mappage détecté automatiquement lorsque votre en-tête utilise une convention de nommage que Spwig n'a pas reconnue, ou lorsque la colonne ne correspond vraiment à rien que Spwig importe (un champ de note interne, par exemple) — choisissez Ignorer plutôt que de l'assigner au champ disponible le plus proche.

## Champs personnalisés

Ce bloc est spécifique à WooCommerce. Spwig extrait 10 produits, clients et commandes de votre boutique et liste tout champ de métadonnées personnalisé qu'il détecte au-delà des champs standard de WooCommerce, ainsi que le type détecté et une valeur d'exemple.

Pour chaque champ, choisissez où il doit être mappé :

- **Mapper à** — Champ personnalisé 1, 2 ou 3 pour les produits (Champ personnalisé 1 ou 2 pour les clients et les commandes), ou **Métadonnées (JSON)** comme solution de secours si vous avez plus de champs personnalisés que les emplacements numérotés, ou laissez-le comme **— Ignorer ce champ —**.
- **Transformer** — comment la valeur doit être convertie lors de l'importation : En texte, En nombre (entier), En décimal, En vrai/faux (booléen), En JSON, En date, En URL, ou En e-mail.

> **Remarque :** Les métadonnées Shopify ne sont pas détectées par cette fonctionnalité du tout — les migrations Shopify ne montrent jamais de bloc de champs personnalisés, peu importe la quantité de données de métadonnées que votre boutique possède. Si vous dépendez des métadonnées Shopify pour les spécifications des produits, les attributs des clients ou des éléments similaires, prévoyez de réentrer ces données manuellement dans Spwig après l'importation.

Si Spwig ne détecte aucun champ personnalisé dans votre échantillon, vous verrez un message de confirmation à la place de ce bloc, et il n'y a rien de plus à configurer.

Lorsque certaines de vos catégories sources n'ont pas de correspondance évidente dans Spwig, ce bloc propose trois options : **Créer de nouvelles catégories**, **Attribuer à la catégorie par défaut** (une catégorie de tout ce qui n'est pas classé), ou **Ignorer les éléments dont les catégories ne sont pas mappées**.

> **Remarque :** Quelle que soit l'option que vous choisissez ici, Spwig crée automatiquement une catégorie correspondante pour tout produit qui possède des données de catégorie source, et ne recourt qu'aux catégories "Non classé" pour les produits qui n'ont aucune information de catégorie. Vous n'avez pas besoin de vous torturer l'esprit avec ce choix — si vous finissez par avoir des catégories que vous ne souhaitez pas, il est plus rapide de les fusionner ou de les supprimer dans **Catalogue > Catégories** après l'importation que de dépendre de ce paramètre.

## Paramètres de taxe, d'expédition et de prix

Le dernier bloc, **Paramètres de taxe et d'expédition**, comporte trois contrôles : **Importer les paramètres de taxe**, **Importer les zones et méthodes d'expédition**, et un type et une valeur d'**Ajustement de prix**.

Les deux cases à cocher n'ont actuellement aucun effet sur l'importation — aucune taux de taxe ou zone d'expédition ne provient de votre ancienne plateforme, quel que soit le paramétrage. Configurez-les directement dans Spwig une fois l'importation terminée : les taux de taxe sous **Paramètres > Taxe et devise**, les zones et méthodes d'expédition sous **Paramètres > Expédition**.

L'**Ajustement de prix** se comporte différemment selon votre plateforme source :

- **Migrations WooCommerce, CSV et Shopify** — ce contrôle fonctionne comme décrit. Choisissez **Pourcentage** ou **Montant fixe**, saisissez une valeur (par exemple `10` pour une augmentation de 10 %, ou `-5` pour une diminution de 5 $), et le prix de base de chaque produit est ajusté de cette quantité lors de l'importation. Cela s'applique uniquement au prix de base — les prix de vente ou de comparaison sont importés sans ajustement.
- **Migrations Magento** — le même contrôle apparaît sur la page, mais il n'a aucun effet ; les prix Magento sont importés tels quels, indépendamment de ce que vous saisissez. Si vous avez besoin d'un changement global de prix pour une migration Magento, appliquez-le ultérieurement à l'aide des outils de mise à jour de prix en masse de Spwig plutôt que via ce champ.

> **Avertissement :** Si vous migrez depuis WooCommerce, CSV ou Shopify et ne souhaitez pas modifier les prix, laissez **Ajustement de prix** défini sur **Aucun**. C'est le seul contrôle de cette page qui modifie réellement vos données, et il est facile de supposer — de manière incorrecte — qu'il se comporte de la même manière que les cases à cocher de taxe et d'expédition juste au-dessus.

## Les mappages sont sauvegardés pour la prochaine fois

Quel que soit le paramétrage que vous configurez sur cette page, il est enregistré avec le travail de migration, et Spwig l'utilise à nouveau comme point de départ pour les futures migrations depuis la même plateforme — utile si vous effectuez une migration progressive (catégories et produits en premier, commandes plus tard) ou si vous avez besoin de réimporter après avoir corrigé un problème de données. Vous pouvez également revenir et ajuster les mappages enregistrés après la fin d'une migration via le bouton **Mappages des champs** sur le tableau de bord de migration, sans avoir à relancer l'ensemble du guide.

## Conseils

- **Vérifiez le bloc des mappages automatiques même si vous ne pouvez pas l'éditer** — détecter un mauvais mappage avant de cliquer sur Démarrer l'importation est bien plus économique que de corriger des centaines d'enregistrements importés par la suite.
- **Renommez les en-têtes CSV ambigus avant de les charger** si la détection automatique ne les a pas reconnus, plutôt que de tenter de forcer un champ mal correspondant via le menu déroulant.
- **Utilisez les Métadonnées (JSON) comme zone de dépassement pour vos champs personnalisés** — c'est le seul objectif de mappage qui ne se limite pas après deux ou trois champs.
- **Ne comptez pas sur cette page pour la taxe, l'expédition ou (pour Magento) le prix** — traitez-les comme une tâche de configuration manuelle à effectuer juste après l'importation, et non comme quelque chose que le guide gère pour vous.
- **Laissez l'ajustement de prix sur Aucun lors de votre première exécution d'une nouvelle migration**, puis utilisez un petit lot de test pour confirmer les calculs avant d'appliquer l'ajustement à votre catalogue complet.