---
title: Migration depuis Shopify
---

Si votre boutique fonctionne actuellement avec Shopify, l'assistant de migration de Spwig peut importer vos produits, clients, commandes et contenu en se connectant à une petite application personnalisée que vous créez via le tableau de bord des partenaires Shopify. La plateforme Shopify est plus verrouillée que la plupart, donc la plupart de ce guide porte sur la création correcte de cette application — la connexion elle-même est une étape de cinq minutes une fois que l'application existe.

## Avant de commencer

Deux limites spécifiques à Shopify sont suffisamment importantes pour être mentionnées ici, et non seulement plus loin dans un tableau :

> **Important :** Shopify n'a pas d'API pour les avis, donc **les avis des clients ne sont pas migrés du tout**, indépendamment des autorisations d'application que vous accordez. Si vous avez besoin de vos avis, exportez-les séparément depuis l'application de commentaires que vous utilisez (Judge.me, Yotpo, Loox, etc.) et importez-les vous-même dans Spwig.

> **Important :** Par défaut, Spwig ne peut lire que **les commandes des 60 derniers jours**. Pour importer votre historique complet de commandes, vous devez ajouter l'autorisation `read_all_orders` lors de la création de votre application — consultez la liste des autorisations ci-dessous. Cela est facile à oublier, car l'application se connecte et importe quand même avec succès sans elle ; elle limite simplement la période d'importation des commandes.

Tout le reste se transfère bien : les catégories (en tant que Collections — voir ci-dessous), les produits, les images, les variantes, les clients et les adresses, les remises, et le contenu du blog. Les champs personnalisés constituent l'autre lacune notable — voir **les métadonnées Shopify** vers la fin de ce guide.

Tenez également compte des points suivants :

- Les options **Importer les paramètres fiscaux** et **Importer les zones et méthodes d'expédition** de l'assistant ne sont pas appliquées aux données importées. Configurez vous-même les taux de TVA et les méthodes d'expédition dans Spwig après l'importation — voir [Après votre migration](after-migration-review).
- L'option **Ajustement des prix** sur la même étape *a bien* effet pour les importations Shopify, modifiant le prix de base de chaque produit lors de sa création. Laissez-la sur **Aucun** sauf si vous souhaitez délibérément modifier chaque prix.
- Vous aurez besoin d'un compte Shopify Partners pour créer l'application. Si vous n'en avez pas déjà un, Shopify vous permet de créer un compte gratuit à [partners.shopify.com](https://partners.shopify.com).

## Création de l'application Shopify

Spwig se connecte à Shopify via une application personnalisée que vous créez et installez sur votre propre boutique. Cela correspond au guide **Shopify API Setup Guide** (ouvert via **Ouvrir le guide d'installation** à l'étape 2 de l'assistant), donc les étapes ci-dessous correspondent exactement à ce que vous verrez là-bas — vous pouvez suivre l'une ou l'autre.

### Étape 1 : Créer l'application

1. Allez sur votre [tableau de bord de développement Shopify Partners](https://dev.shopify.com/dashboard) et ouvrez **Apps**
2. Cliquez sur **Créer une application**
3. Choisissez **Commencer depuis le tableau de bord de développement**
4. Entrez le nom de l'application : `Spwig Migration`
5. Cliquez sur **Créer**

![Création de l'application Spwig Migration dans le tableau de bord de développement Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Étape 2 : Définir l'URL de l'application et les autorisations

Sur la page de configuration de l'application nouvelle, sous **Versions**, définissez :

- **App URL** : `https://shopify.dev/apps/default-app-home`
- **Scopes** : `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Définition de l'URL de l'application et des autorisations requises](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Scope | Donne à Spwig l'accès à |
|---|---|
| `read_products` | Produits, variantes, images, collections |
| `read_customers` | Noms de clients, emails, adresses |
| `read_orders` | Commandes des 60 derniers jours |
| `read_content` | Articles de blog et pages |
| `read_discounts` | Codes de réduction et règles |
| `read_files` | Fichiers multimédias téléchargés |

> **Note :** Souhaitez-vous l'ensemble de votre historique de commandes au lieu des 60 derniers jours seulement ? Ajoutez `read_all_orders` à la liste des autorisations ci-dessus.

### Étape 3 : Copier votre ID Client et votre Secret

Allez à **Paramètres > Informations d'identification** et copiez l'**ID Client** et le **Secret** affichés là — vous les collerez dans l'assistant Spwig dans un instant.

![Copie de l'ID Client et du Secret depuis la page Paramètres de l'application](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Étape 4 : Générer un lien de distribution personnalisé

1.

Accédez à **Distribution** et sélectionnez **Distribution personnalisée**
2.

Entrez votre domaine de magasin (par exemple, `yourstore.myshopify.com`)
3.

Cliquez sur **Générer le lien**, puis **Copier** le lien d'installation qu'il génère

![Copiant le lien d'installation de distribution personnalisée généré](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Étape 5 : Installer l'application sur votre magasin

Ouvrez le lien d'installation que vous venez de copier dans votre navigateur (veillez à être connecté à l'administration de votre magasin Shopify), examinez les autorisations qu'il demande, puis cliquez sur **Installer**.

![Installer l'application sur le magasin Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Important :** Cette dernière étape est facile à oublier. La génération du lien d'installation n'installe pas l'application — vous devez ouvrir le lien et cliquer sur Installer, sinon Spwig ne pourra pas se connecter. Si le test de connexion échoue dans la section suivante, c'est la première chose à vérifier.

## Copier vos identifiants dans Spwig

Dans l'administration Spwig, allez à **Importation et exportation des données > Démarrer une nouvelle migration**, choisissez **Shopify** à l'étape 1, et à l'étape 2, entrez :

- **Domaine du magasin** — `yourstore.myshopify.com`
- **ID client** — depuis Paramètres > Identifiants
- **Secret client** — depuis Paramètres > Identifiants

Si vous préférez suivre le tutoriel en ligne plutôt que ce guide, cliquez sur **Ouvrir le guide d'installation** à cette étape — il couvre les mêmes cinq étapes ci-dessus avec les mêmes captures d'écran, et prend environ 10 minutes en tout.

Laissez **Tester la connexion avant de continuer** cochée. Si `read_products`, `read_customers` ou `read_orders` est absent des autorisations de votre application, Spwig vous avertit avant de continuer — retournez à la page Versions de l'application dans le tableau de bord Shopify, ajoutez l'autorisation manquante, enregistrez une nouvelle version, puis réessayez.

## Révision et sélection des données

L'étape 3 extrait les comptes en direct de votre magasin et affiche un exemple des cinq premiers produits. Quelques éléments sont différents des autres plateformes :

- **Collections, pas des catégories** — Shopify organise les produits en Collections plutôt que des catégories, et les Collections ne prennent pas en charge l'imbrication, donc la hiérarchie s'importe de manière plate. Si votre magasin Shopify utilisait des collections pour représenter un arbre de catégories, prévoyez de reconstruire cette structure dans le gestionnaire de catégories de Spwig après l'importation.
- **Remises, pas des coupons** — Les codes et règles de remise de Shopify s'importent comme des remises Spwig.
- **Aucune ligne de commentaires** — puisque Shopify n'a pas d'API de commentaires, ce type de données n'apparaît pas sur cette étape du tout, contrairement à WooCommerce ou aux imports CSV.

Les **Options d'importation** fonctionnent de la même manière que sur d'autres plateformes : **Ignorer les éléments existants** (activé) correspond sur l'identifiant SKU et l'adresse e-mail pour éviter les doublons ; **Importer les images des produits** (activé) est plus lent mais recommandé ; **Conserver les identifiants d'origine autant que possible** (désactivé) doit rester désactivé sauf si vous avez une raison spécifique de le changer ; **Taille des lots** est par défaut de 25.

## Metafields Shopify

Si vous utilisez des metafields Shopify pour stocker des données supplémentaires sur les produits, les clients ou les commandes, sachez que Spwig ne les détecte ni ne les lit — contrairement à WooCommerce, il n'y a pas d'étape de mappage des champs personnalisés pour les imports Shopify. Toute donnée que vous avez stockée dans des metafields devra être réintroduite manuellement dans Spwig à l'aide des [champs personnalisés](migration-field-mapping) après l'importation, donc il est utile d'exporter une liste de vos metafields et de leurs valeurs depuis Shopify avant de commencer.

## Exécuter l'importation

Une fois que vous avez révisé l'étape 3, démarrez l'importation. Elle s'exécute en arrière-plan — vous pouvez fermer la fenêtre du navigateur et elle continue. L'étape 5 affiche le progrès en temps réel avec une ligne par type de données et un journal d'activité expansible.

L'étape 6 affiche vos résultats : ce qui a été importé, ignoré ou échoué, ainsi qu'un outil de **Réécriture des liens** si des liens internes vers votre ancien domaine `myshopify.com` ont été trouvés dans le contenu importé.

Vérifiez soigneusement le résumé, puis suivez la checklist dans [Après votre migration](after-migration-review) — elle couvre la vérification de vos données, la reconstruction de toute hiérarchie de collections, la configuration des taux de taxes et de livraison (que le wizard ne configure pas pour vous), ainsi que la réintroduction de tout ce qui était stocké dans les métadonnées.

## Supprimez l'application de Shopify

Une fois que vous avez confirmé que la migration s'est terminée avec succès, retournez sur la page **Apps** de votre administration Shopify, ou sur le tableau de bord des partenaires, et supprimez l'application de migration Spwig (ou au minimum, désinstallez-la de votre boutique). Il n'y a aucune raison de laisser l'accès en lecture à vos données de boutique actif une fois la migration terminée.

## Conseils

- **L'historique des commandes est limité par défaut** — si vous avez besoin de plus de 60 jours de commandes, ajoutez `read_all_orders` à la liste des portées avant de générer votre lien d'installation, et non après.
- **Les avis nécessitent une exportation séparée** — planifiez cela avant de migrer, car il n'y a aucun moyen de transférer les avis via le wizard.
- **Générer le lien n'est pas la même chose que d'installer l'application** — assurez-vous toujours de terminer l'étape 5 et de cliquer sur Installer, sinon le test de connexion dans Spwig échouera.
- **Les collections arrivent en format plat** — si votre structure de catégories avait de l'importance pour la navigation ou le référencement, prévoyez du temps pour reconstruire la hiérarchie dans Spwig après l'import.
- **Exportez vos métadonnées en premier** — Spwig ne peut pas les lire, donc capturez ces données depuis Shopify avant de commencer si vous en aurez besoin plus tard.
- **Supprimez l'application une fois que vous êtes vérifié** — ne laissez pas une intégration active pointant vers votre ancienne boutique après que vous avez terminé la migration.