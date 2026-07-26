---
title: Migration depuis Magento
---

Spwig peut importer directement votre catalogue, clients, commandes, coupons et pages CMS à partir d'un magasin Magento 2 ou Adobe Commerce en cours d'utilisation, en utilisant l'API REST de Magento. Ce guide vous guide à travers la génération des informations d'intégration requises par Magento, l'exécution de l'assistant de migration et l'une des lacunes majeures que les commerçants venant de Magento doivent planifier : les avis de produits.

Seuls **Magento 2 et Adobe Commerce** sont pris en charge. Magento 1 a atteint la fin de sa durée de vie il y a plusieurs années et ne propose pas l'API REST sur laquelle cette migration repose — si vous utilisez toujours Magento 1, utilisez plutôt [Importation à partir de fichiers CSV](csv-import).

## Avant de commencer

Consultez [Aperçu de la migration des données](migration-overview) pour obtenir des conseils généraux sur la planification. Pour Magento en particulier :

- **Catégories** — importées avec leur hiérarchie intacte.
- **Produits** — importés, y compris les images.
- **Clients et adresses** — importés.
- **Commandes** — importées.
- **Coupons** — importés sous forme de bons Spwig, issus des règles de vente de Magento.
- **Pages CMS** — importées sous forme de pages Spwig.
- **Avis** — généralement **non** importés. Consultez la section suivante avant de vous y fier.
- Les variantes sont prises en charge pour les produits configurables.

> **Remarque :** Les migrations Magento ne transfèrent pas les programmes d'affiliation, les commissions ou les paiements — l'intégration du pont d'affiliation de Spwig n'est disponible que pour les magasins WooCommerce.

### La limitation des avis

L'édition communautaire de Magento ne propose pas de point de terminaison REST pour les avis de produits — la route `/reviews` n'existe simplement pas sur une installation communautaire standard. Spwig vérifie sa présence avant l'importation et, si elle n'est pas trouvée, affiche un message et continue avec le reste de votre migration plutôt que d'échouer l'ensemble de la tâche. Vos catégories, produits, clients, commandes, coupons et pages sont toujours transférés ; seuls les avis sont ignorés.

Les avis **seront** importés si votre magasin utilise **Adobe Commerce** (qui expose ce point de terminaison) ou si votre installation Magento dispose d'un module personnalisé ajoutant une route compatible pour les avis.

Si vous utilisez Magento Community et que vous avez besoin de vos avis dans Spwig, exportez-les séparément (la plupart des extensions d'avis offrent une exportation CSV) et importez-les ultérieurement à l'aide du fichier d'avis dans [Importation à partir de fichiers CSV](csv-import), associé à vos produits via `product_id`.

## Étape 1 : Choisir Magento

À partir du tableau de bord de migration à **Importation et exportation des données**, cliquez sur **Démarrer une nouvelle migration** et sélectionnez **Magento** comme plateforme.

## Étape 2 : Se connecter à votre magasin

Vous aurez besoin de l'URL de votre magasin Magento et d'un jeton d'accès d'intégration. L'admin Magento ne fournit pas simplement un jeton API comme le font certaines plateformes — vous créez une **Intégration**, qui est une information d'accès limitée que Magento traite comme une application connectée.

### Création d'un jeton d'accès d'intégration

1. Dans votre admin Magento, allez à **Système > Intégrations**.
2. Cliquez sur **Ajouter une nouvelle intégration**.
3. Définissez le nom sur `Spwig Migration` pour faciliter son identification ultérieure.
4. Ouvrez l'onglet **API** et définissez **Accès aux ressources** sur **Tout**.
5. Cliquez sur **Enregistrer**, puis sur **Activer**.
6. Confirmez en cliquant sur **Autoriser** dans la fenêtre contextuelle qui liste les autorisations accordées.
7. Copiez le jeton d'accès affiché après l'activation — Magento ne l'affiche qu'une seule fois.

> **Remarque :** L'accès aux ressources est défini sur **Tout** car l'arborescence des ressources de Magento est très granulaire — des centaines de permissions individuelles couvrant le catalogue, les ventes, les clients et le CMS — sans aucun interrupteur "lire tout" à moins de sélectionner toutes les permissions. La migration n'écrit jamais dans votre magasin ; elle ne lit que depuis, et vous pouvez révoquer l'intégration une fois que votre migration a été vérifiée (abordée à la fin de ce guide).

Revenez à l'assistant Spwig et entrez votre **URL du magasin** et le **Jeton d'accès** que vous avez copié. Laissez **Tester la connexion avant de continuer** cochée (activée par défaut) afin que Spwig vérifie qu'elle peut atteindre et s'authentifier auprès de votre magasin avant de continuer. Si le test échoue, vérifiez à nouveau l'URL et assurez-vous que l'intégration est toujours active dans Magento. Cliquez sur **Suivant**.

screenshots-needed

heading

## Étape 3 : Révision de ce qui sera importé

paragraph

Spwig interroge votre boutique Magento et affiche des comptages en temps réel pour chaque type de données qu'il a trouvées : catégories, produits, clients, commandes, coupons (provenant des règles de vente) et pages CMS. Chaque type a une case à cocher, automatiquement cochée lorsque Spwig a trouvé des éléments à importer et désactivée lorsque le comptage est à zéro.

paragraph

Vous verrez également un exemple des cinq premiers produits afin que vous puissiez vérifier que les titres, les prix et les images semblent corrects avant de confirmer l'importation complète.

paragraph

En dessous des comptages, **Options d'importation** vous permettent de contrôler le comportement de l'importation :

list

paragraph

Si vous avez besoin de modifier la manière dont les champs spécifiques sont mappés — attributs personnalisés, correspondance des catégories, traitement des taxes ou des frais d'expédition — cela se fait à l'étape 4, abordée dans [Migration Field Mapping](migration-field-mapping). Cliquez sur **Suivant** pour passer au mappage, puis sur **Démarrer la migration** une fois que vous avez vérifié.

heading

## Exécution de l'importation

paragraph

L'importation s'exécute en arrière-plan — vous pouvez fermer la fenêtre et elle continuera. La page de progression affiche l'état en temps réel pour chaque type de données (catégories, produits, clients, commandes, avis, coupons) avec un journal que vous pouvez développer pour plus de détails.

paragraph

Une fois qu'elle est terminée, vous atterrirez sur la page de résumé des résultats. Parcourez [Après votre migration](after-migration-review) pour vérifier ce qui a été transféré, gérer toute réécriture de liens pour le contenu qui faisait référence aux anciens URLs de votre boutique Magento, et prendre en charge la configuration des taxes et des frais d'expédition que le wizard collecte mais n'applique pas automatiquement.

screenshots-needed

heading

## Date limite de remboursement

paragraph

Magento est la seule plateforme où le remboursement a une limite de temps. Une fois que votre migration est terminée, le bouton **Remboursement** apparaît sur la page de résumé de l'opération — mais pour Magento spécifiquement, ce bouton peut cesser d'être proposé après une période suivant la fin. Les autres types de migration (WooCommerce, Shopify, CSV) n'ont pas cette date limite, mais Magento en a une, donc ne reportez pas la vérification.

blockquote

paragraph

Vérifiez vos données importées rapidement, tant que le remboursement est encore disponible, au cas où vous en auriez besoin.

heading

## Révoquer l'intégration

paragraph

Une fois que vous avez vérifié vos données dans Spwig — les produits, les prix, les images, les clients, les commandes, les coupons et les pages semblent corrects — retournez à **Système > Intégrations** dans Magento, trouvez `Spwig Migration`, et désactivez-le ou supprimez-le.

Le jeton n'est plus nécessaire à moins que vous ne planifiiez de relancer la migration, et son suppression ferme un accès en lecture ouvert que vous n'avez plus besoin d'avoir actif.

## Conseils

- **Les avis sont la plus grande surprise pour les commerçants Magento** — prévoyez une exportation/importation séparée si vous utilisez la version Communautaire et que les avis sont importants pour votre magasin.
- **Copiez immédiatement le jeton d'accès** — Magento ne l'affiche qu'une seule fois lors de l'activation de l'intégration ; si vous le perdez, vous devrez désactiver et recréer l'intégration.
- **Ne repoussez pas la vérification** — le bouton Annuler est disponible pendant un temps limité pour Magento, contrairement aux autres plateformes.
- **Utilisez la prévisualisation d'exemple à l'étape 3** pour détecter les problèmes de mappage évidents (prix incorrects, images manquantes) avant d'exécuter l'import complet.
- **Les coupons proviennent des règles de vente** — si un coupon Magento repose sur des conditions complexes, vérifiez-le dans Spwig par la suite, car tous les types de règles n'ont pas de contrepartie directe.
- **Configurez les taux de taxe et les zones de livraison dans Spwig après l'import** — les options de taxe et de livraison du wizard sont enregistrées mais ne sont pas appliquées automatiquement à votre magasin.