---
title: Migration depuis WooCommerce
---

Si votre boutique fonctionne actuellement avec WooCommerce, l'assistant de migration de Spwig peut importer directement vos produits, clients, commandes et contenus via l'API REST de WooCommerce. Ce guide couvre l'obtention des identifiants API, l'exécution de l'importation, ainsi que deux fonctionnalités spécifiques à WooCommerce à connaître en premier : le plugin optionnel Spwig Migration Bridge pour les données d'affiliation, et le support intégré de plusieurs extensions populaires de WooCommerce.

## Avant de commencer

WooCommerce dispose du plus large support parmi toutes les plateformes sources dans l'assistant de migration. L'importation suivante est nette : catégories (avec hiérarchie), produits, images et variantes, clients et adresses, commandes, avis, coupons, et articles de blog avec leurs catégories, balises et images.

Les profils d'affiliation, les enregistrements de commission et l'historique des paiements peuvent également être importés, mais uniquement si vous installez d'abord le plugin Spwig Migration Bridge — voir ci-dessous. Sans celui-ci, ces données sont simplement ignorées.

Tenez également compte des points suivants :

- Les produits issus de certaines extensions WooCommerce (abonnements, groupes, réservations, cartes-cadeaux) sont transférés vers la fonctionnalité correspondante de Spwig, mais pas tous les détails ne sont pas transférés — voir **Support des extensions WooCommerce** ci-dessous.
- Les champs personnalisés sur vos produits, clients et commandes sont détectés automatiquement et nécessitent un mapping lors d'une étape ultérieure. Voir [Mapping des champs de migration](migration-field-mapping).
- Les options **Importer les paramètres fiscaux** et **Importer les zones et méthodes d'expédition** de l'assistant ne sont pas appliquées aux données importées. Configurez vous-même les taux fiscaux et les méthodes d'expédition dans Spwig après l'importation — voir [Après votre migration](after-migration-review).
- L'option **Ajustement des prix** sur la même étape *a bien* effet pour les importations WooCommerce, modifiant le prix de base de chaque produit lors de sa création. Laissez-la sur **Aucun** sauf si vous souhaitez délibérément décaler tous les prix.

Ayez à portée de main votre connexion administrateur WordPress, et sachez approximativement combien de produits, clients et commandes vous importez afin de vérifier les chiffres affichés par l'assistant.

## Obtenir les identifiants de l'API REST

Spwig se connecte à WooCommerce via une clé API REST générée depuis votre administration WordPress. Cette clé n'a besoin que d'un accès **Lecture** — Spwig ne lit que depuis votre boutique pendant la migration, il n'écrit rien en retour.

1. Dans WordPress, allez à **WooCommerce > Paramètres > Avancé > API REST**
2. Cliquez sur **Ajouter une clé**
3. Donnez-lui une description (par exemple, `Spwig Migration`) et définissez **Permissions** sur **Lecture**
4. Cliquez sur **Générer la clé API**
5. Copiez la **Clé du consommateur** (`ck_...`) et le **Secret du consommateur** (`cs_...`) dans un endroit sûr

> **Important :** WooCommerce affiche le Secret du consommateur uniquement une fois, au moment de sa génération. Si vous quittez avant de l'avoir copié, vous devrez générer une nouvelle clé.

## Connecter votre boutique

Allez dans **Importation et exportation de données > Démarrer une nouvelle migration** dans l'administration Spwig et choisissez **WooCommerce** à l'étape 1. À l'étape 2, entrez :

- **URL du magasin** — l'adresse web complète de votre boutique, par exemple `https://mystore.com`
- **Clé du consommateur** et **Secret du consommateur** — les valeurs que vous venez de copier

Laissez **Tester la connexion avant de continuer** cochée (par défaut activée) afin que Spwig confirme qu'il peut atteindre votre boutique et s'authentifier avant de continuer — cela détecte immédiatement les fautes de frappe et les problèmes de permissions plutôt que partiellement pendant l'importation. Cliquez sur **Suivant** une fois que cela a réussi.

## Révision et sélection des données

L'étape 3 extrait les comptes en temps réel de votre boutique — catégories, produits, clients, commandes, avis et coupons — ainsi qu'un échantillon des cinq premiers produits afin que vous puissiez confirmer qu'il lit bien le bon site. La case à cocher de chaque type de données est automatiquement cochée lorsque son compte est supérieur à zéro, et désactivée à zéro.

**Options d'importation :**

- **Ignorer les éléments existants** (activé) — correspond les enregistrements entrants à ce qui est déjà présent dans Spwig (SKU pour les produits, e-mail pour les clients) et ignore les doublons.

Laissez-le actif sauf si vous démarrez à partir d'un magasin vide.
- **Importer les images des produits** (activé) — plus lent, mais utile.
- **Conserver les ID originaux autant que possible** (désactivé) — le wizard lui-même le désigne comme "non recommandé". Laissez-le désactivé sauf si vous avez une raison technique spécifique pour conserver les ID numériques de WooCommerce.
- **Taille des lots** — 10, 25 (par défaut), 50 ou 100 enregistrements à la fois.

Les lots plus petits conviennent aux connexions instables ; les lots plus grands terminent plus rapidement sur une connexion stable.

## Le plugin Spwig Migration Bridge

WooCommerce n'a pas de concept intégré de programme d'affiliation, donc si vous en faites fonctionner un via une extension d'affiliation WooCommerce, ces données résident dans des tables que l'API REST standard ne peut pas voir. Le **Spwig Migration Bridge** est un petit plugin complémentaire que vous installez sur votre site WordPress pour les rendre accessibles.

Le plugin Bridge permet d'accéder à :

- **Profils d'affiliation** — les détails de vos affiliés et leurs codes de parrainage
- **Historique des commissions** — l'historique des commissions liées à chaque affilié
- **Historique des paiements** — les paiements effectués aux affiliés

C'est entièrement optionnel — sautez-le si vous n'avez pas de programme d'affiliation ou si vous n'avez pas besoin de cet historique dans Spwig.

> **Note :** Les données d'affiliation ne peuvent être importées que si les commandes et les clients sont également importés dans la même migration, car les commissions et les paiements sont liés à des commandes et des clients spécifiques.

Pour l'installer :

1. À l'étape 3, si le plugin n'est pas déjà détecté sur votre site, vous verrez un bouton **Télécharger le plugin Bridge** avec des instructions d'installation
2. Téléchargez le fichier ZIP du plugin
3. Dans WordPress, allez à **Plugins > Ajouter un nouveau > Télécharger un plugin**, sélectionnez le ZIP, cliquez sur **Installer maintenant**, puis **Activer**
4. Retournez au wizard Spwig et actualisez la page — une case à cocher **Affiliés** et un bloc **Données du programme d'affiliation** apparaîtront, affichant les comptages trouvés

Vous pouvez désactiver et supprimer le plugin Bridge de WordPress une fois que votre migration est terminée.

## Prise en charge des extensions WooCommerce

Si votre magasin utilise certaines extensions populaires, les produits qu'elles créent sont reconnus lors de l'importation et mappés vers la fonctionnalité correspondante de Spwig plutôt que d'être importés comme des produits normaux :

| Extension WooCommerce | Atterrissent dans |
|---|---|
| Abonnements | Plans d'abonnement Spwig |
| Add-Ons de produit | Add-Ons de produit Spwig |
| Bundles de produit | Bundles de produit Spwig |
| Cartes cadeaux (variantes WooCommerce, YITH et PW) | Cartes cadeaux Spwig |
| Produits composites | Produits composites Spwig |
| Réservations et Réservations d'hébergement | Réservations Spwig |

> **Note :** L'importation des données d'extension ne bloque jamais la création du produit sous-jacent. Si les données spécifiques à l'extension d'un produit ne peuvent pas être lues, le produit est tout de même importé — simplement comme un produit normal, sans sa configuration d'abonnement, de bundle, de réservation ou de carte cadeau.

Vérifiez quelques produits d'abonnement, de bundle, de réservation et de carte cadeau après l'importation pour confirmer que leurs paramètres spécifiques à l'extension ont été transférés, plutôt que d'assumer qu'une importation réussie a transféré tous les détails.

## Champs personnalisés

Si vous avez ajouté des champs métadonnées personnalisés à vos produits, clients ou commandes WooCommerce, Spwig en extrait environ dix enregistrements de chaque type pour détecter quels champs existent. Vous allez mapper chacun d'eux à un emplacement de champ personnalisé Spwig ou à un champ de métadonnées général à l'étape 4. Consultez [Migration Field Mapping](migration-field-mapping) pour le tutoriel complet, y compris la manière dont les mappages sont sauvegardés pour les futures migrations.

## Exécuter l'importation

Une fois que vous avez revu l'étape 3 et confirmé vos mappages à l'étape 4, commencez l'importation. Elle s'exécute en arrière-plan — vous pouvez fermer la fenêtre du navigateur et elle continue. L'étape 5 affiche un suivi en temps réel avec une ligne par type de données (catégories, produits, clients, commandes, avis, coupons, articles de blog et affiliés/commissions/paiements si le plugin Bridge a été utilisé) plus un journal d'activité expansible.

L'étape 6 affiche vos résultats : ce qui a été importé, ignoré ou échoué, plus un outil **Réécriture des liens** si des liens internes vers votre ancien domaine WooCommerce ont été trouvés dans le contenu importé.

Vérifiez soigneusement le résumé, puis suivez la liste de vérification dans [Après votre migration](after-migration-review) — elle couvre la vérification de vos données, la configuration des taux de taxe et de l'expédition (que le assistant ne configure pas pour vous), ainsi que la réécriture des liens internes.

## Révoquer votre clé API

Une fois que vous avez confirmé que la migration s'est terminée avec succès, retournez dans **WooCommerce > Paramètres > Avancé > API REST** dans WordPress et révoquez ou supprimez la clé que vous avez créée pour Spwig. Il n'y a aucune raison de laisser une clé API active sur votre ancien magasin une fois que vous avez terminé.

## Conseils

- **Générez la clé API juste avant de l'avoir besoin** — puisque le Secret du Consommateur n'est affiché qu'une seule fois, créez-la immédiatement avant de commencer l'étape 2 plutôt que d'avance.
- **Un accès en lecture seule est vraiment suffisant** — ne conférez jamais les autorisations Écriture ou Lecture/Écriture ; Spwig n'accède jamais qu'en lecture à votre magasin WooCommerce.
- **Installez le plugin Bridge avant de commencer l'import** — vous devrez l'ajouter et actualiser l'assistant avant l'import, donc vérifiez-le dès le début plutôt que plus tard.
- **Vérifiez partiellement les produits basés sur des extensions** — les abonnements, les groupes de produits, les réservations et les cartes-cadeaux sont les produits les plus susceptibles de nécessiter une vérification manuelle après l'import.
- **Un import partiel n'est pas nettoyé automatiquement** — consultez [Dépannage de la migration](migration-troubleshooting) avant de réessayer un import échoué.
- **Révoquez la clé API une fois que vous avez terminé** — ne laissez pas les anciennes intégrations actives sur un magasin duquel vous avez migré.