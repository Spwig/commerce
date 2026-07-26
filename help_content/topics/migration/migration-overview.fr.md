---
title: Aperçu de la migration des données
---

Si vos produits, clients et commandes se trouvent actuellement dans WooCommerce, Shopify ou Magento — ou simplement dans un petit nombre de fichiers CSV — l'outil de migration transfère ces données vers votre nouvelle boutique Spwig afin que vous n'ayez pas à les saisir à la main. Il gère les catégories, les produits, les clients, les commandes, les avis et les coupons, et pour WooCommerce, il peut également transférer le contenu du blog et, avec un plugin de passerelle, votre programme d'affiliation.

Trouvez-le dans le menu latéral de l'administration sous **Tableau de bord du système > Import/Export de données** (visible uniquement par les superutilisateurs sur les installations auto-hébergées ; si vous ne le voyez pas, demandez à la personne qui gère votre installation). La page, intitulée **Import et export de données**, liste toutes les migrations que vous avez lancées avec des cartes statistiques pour les migrations totales, Terminées, En cours et Échouées, ainsi que les boutons **Démarrer une nouvelle migration**, **Voir les journaux** et **Correspondances des champs**. Les migrations ne peuvent être créées qu'via l'assistant.

## Plateformes prises en charge

Spwig se connecte directement à trois plateformes, ainsi qu'aux fichiers CSV simples :

- **WooCommerce** — la méthode la plus complète ; les données d'extensions (abonnements, groupes, cartes-cadeaux, réservations) et votre programme d'affiliation peuvent également être transférés.
- **Shopify** — se connecte via une application personnalisée que vous créez dans votre tableau de bord de développeur Shopify.
- **Magento 2** — se connecte via un jeton d'intégration depuis votre administration Magento.
- **Fichiers CSV** — cinq fichiers séparés (produits, catégories, clients, commandes, avis), pour d'autres plateformes ou des données préparées manuellement.

> **Remarque :** BigCommerce, PrestaShop, Squarespace et Wix ne sont pas pris en charge en tant que connexions directes. Si vous migrez depuis l'un de ces derniers, exportez votre catalogue et vos données clients vers CSV et utilisez plutôt la méthode CSV — voir [Import depuis des fichiers CSV](csv-import).

## Ce qui est transféré, par plateforme

La couverture varie selon la plateforme — vérifiez ce tableau par rapport à votre propre boutique avant de fixer une date de lancement.

| Données | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Catégories | Oui, avec hiérarchie | Oui, en tant que Collections (plat) | Oui | Oui |
| Produits | Oui | Oui | Oui | Oui (fichier requis) |
| Images de produits | Oui | Oui | Oui | Non |
| Variantes | Oui | Oui | Oui | Non |
| Clients + adresses | Oui | Oui | Oui | Oui |
| Commandes | Oui | Oui, uniquement les 60 derniers jours à moins que l'étendue `read_all_orders` ne soit ajoutée | Oui | Oui |
| Avis | Oui | Pas du tout pris en charge | Généralement indisponibles — Magento Community n'a aucun point de terminaison REST pour les avis | Oui |
| Coupons / réductions | Oui | Oui | Oui | Non |
| Blog / contenu CMS | Oui (articles, catégories, balises, images) | Oui (articles) | Oui (pages CMS) | Non |
| Affiliés, commissions, paiements | Oui, nécessite le plugin Spwig Migration Bridge | Non | Non | Non |
| Détection des champs personnalisés | Oui | Non — les métadonnées Shopify ne sont pas lues | Non | n/a |

Les commerçants Shopify doivent prévoir de saisir manuellement les données des métadonnées (spécifications de produits personnalisées, champs clients supplémentaires) après l'import, car elles ne sont pas détectées ni transférées. Pour tout le reste, consultez [Correspondance des champs de migration](migration-field-mapping) pour voir comment les champs sources correspondent aux champs Spwig.

## Planifier votre migration

- **Migrez avant de lancer votre boutique**, sur une installation Spwig qui n'assure pas encore de trafic réel, avant de pointer le DNS de votre domaine vers elle — ainsi, vous pouvez vérifier et corriger les choses sans que les clients voient un catalogue incomplet.
- **Maintenez votre ancienne boutique en cours d'exécution en mode lecture seule**, jusqu'à ce que vous ayez vérifié que la copie Spwig est correcte.
- **Planifiez du temps pour la configuration des taxes et des frais de port par la suite** — les paramètres de l'assistant pour cela semblent importer vos tarifs et zones, mais ils ne sont pas appliqués (voir [Correspondance des champs de migration](migration-field-mapping)). Configurez vous-même **Paramètres > Taxes et devise** et **Paramètres > Frais de port**.
- **Vérifiez soigneusement plutôt que de survoler** — les données d'extension sont importées sur une base d'effort maximal ; un produit dont les données d'extension ne peuvent pas être lues est tout de même créé, mais sans ces données. Consultez [Après votre migration](after-migration-review) avant d'annoncer quoi que ce soit aux clients.

- **Accès administrateur à votre plateforme source** pour créer des identifiants API — une clé API REST dans WooCommerce, une application personnalisée dans Shopify, ou un jeton d'intégration dans Magento.

Non nécessaire pour le CSV.
- **Portée en lecture seule** là où la plateforme source le propose — Spwig ne lit que depuis votre ancien magasin, jamais en écriture vers celui-ci.
- **Un budget de temps** — chaque exécution a une limite stricte de 4 heures.

Pour un grand magasin, planifiez une approche par phases (catégories et produits en premier, commandes plus tard) plutôt qu'une seule passe.

> **Important :** Spwig ne chiffre pas les identifiants API que vous entrez dans l'assistant. Une fois la migration vérifiée comme terminée, révoquez ou supprimez l'identifiant sur la plateforme source.

## L'assistant de migration, étape par étape

L'assistant comporte six étapes, avec un suivi des progrès entre elles :

1. **Plateforme** — choisissez WooCommerce, Shopify, Magento ou Import CSV.
2. **Connexion** — entrez les identifiants, avec l'option (activée par défaut) de tester la connexion en premier. Les guides spécifiques à la plateforme indiquent exactement ce que vous devez générer.
3. **Aperçu** — des comptes en temps réel depuis votre magasin source, un échantillon des 5 premiers produits, et des cases à cocher pour les types de données à inclure, ainsi que des options comme la taille des lots.
4. **Mappage** — la manière dont les champs source se cartographient sur les champs Spwig, tout champ personnalisé WooCommerce, et les catégories sans correspondance évidente. Détails complets dans [Migration Field Mapping](migration-field-mapping).
5. **Import** — s'exécute en arrière-plan ; vous pouvez fermer l'onglet et il continue, avec un journal en temps réel.
6. **Terminé** — un résumé des résultats, un outil de réécriture des liens pour le contenu qui fait référence à votre ancien domaine, et des téléchargements de rapports PDF/CSV.

## Après votre migration

Un import réussi n'est pas la fin de la course — consultez [After Your Migration](after-migration-review) pour obtenir une liste de vérification complète couvrant la vérification des données, la correction des liens internes qui pointent toujours vers votre ancien domaine, et la configuration des taxes et des frais d'expédition que l'assistant ne gère pas pour vous.

## Le rollback n'est pas un filet de sécurité

Comprenez cela avant de commencer, et non après un problème. Le rollback existe, mais ce n'est pas le bouton annuler qu'il pourrait sembler être :

- Il n'y a aucun rollback automatique si l'import échoue partiellement. Ce qui a été importé avant l'échec reste dans votre magasin, et un import échoué ne peut pas être annulé depuis l'administration — vous devrez vérifier et nettoyer les données partielles manuellement.
- Une migration terminée peut être annulée, et le rollback supprime uniquement ce que l'import lui-même a créé — jamais plus. Un client migré qui a passé une commande réelle depuis l'import garde son compte, ses adresses, son historique de fidélité et son crédit en magasin, et cette commande réelle reste intacte ; seules les commandes créées par l'import sont supprimées. Un produit migré qui est toujours référencé par une commande, un ensemble, une carte cadeau ou un emplacement de configuration est également conservé, et les commandes appartenant à d'autres clients ne sont jamais modifiées.
- Les affiliés, les commissions et les paiements créés par l'import sont supprimés, ainsi que tout compte affilié que l'import a créé — un affilié rattaché à un client qui existait déjà garde son compte, et seul l'enregistrement d'affiliation est supprimé. Les plans d'abonnement, les niveaux tarifaires et les ressources de réservation créés par des extensions de la boutique ne sont toujours pas supprimés — nettoyez-les manuellement.
- Avant de confirmer, Spwig affiche un aperçu exact de ce qui sera supprimé et de ce qui sera conservé, par nom et nombre, avec la raison — calculé par rapport à vos données en temps réel. Lisez-le avant de confirmer. Le rollback s'exécute ensuite en arrière-plan, donc il est sûr de fermer l'onglet ; vérifiez le résumé de la migration pour le rapport une fois qu'il est terminé.
- Le rollback reste une action permanente et destructrice sur les lignes qu'il supprime, donc utilisez-le délibérément — et nettoyez manuellement tout ce que Spwig conserve si vous ne le souhaitez pas vraiment. Mais comme il ne dépasse plus ce qui a été créé par l'import, il n'est plus un outil à usage limité au même jour comme autrefois.
- Le bouton Rollback reste disponible sur le résumé d'une migration terminée tant que l'enregistrement de la tâche existe, et il est à nouveau proposé si une tentative de rollback échoue elle-même partiellement, afin que vous puissiez la relancer. Les enregistrements ne sont pas supprimés selon un calendrier, donc cela n'expire pas tout seul.

Si vous rencontrez une migration échouée ou bloquée, [Migration Troubleshooting](migration-troubleshooting) aborde la relance, l'annulation et la lecture des journaux.

## Conseils

- **Commencez par un test avec un petit échantillon** — les catégories plus une poignée de produits confirment que la correspondance des champs semble correcte avant le catalogue complet.
- **Lisez d'abord le guide spécifique à la plateforme** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify), et [Migrating from Magento](migrate-from-magento) couvrent exactement les identifiants et les étendues dont vous avez besoin.
- **Ne sautez pas la matrice des fonctionnalités ci-dessus** — connaître les avis de Shopify ou les variantes CSV évite les surprises après avoir changé le DNS.
- **Gardez l'administration de votre plateforme source ouverte dans un autre onglet** pour générer ou copier les identifiants au fur et à mesure.
- **Traitez littéralement les cases à cocher du assistant** — si un paramètre n'est pas décrit comme fonctionnel ici, configurez-le directement dans Spwig plutôt que de faire confiance à l'assistant.