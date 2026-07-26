---
title: Dépannage des migrations
---

La plupart des migrations se déroulent sans incident, mais les connexions peuvent échouer, les importations peuvent expirer, et parfois un processus s'arrête avant d'être terminé. Ce sujet aborde le diagnostic d'une connexion échouée, la lecture du journal de progression pendant une importation, et — ce qui est le plus important — les options réelles dont vous disposez une fois qu'une erreur survient, y compris ce que Retry, Cancel et Rollback font réellement.

## Échecs de connexion à l'étape 2

Le **Test de connexion avant de continuer** est activé par défaut et constitue votre premier diagnostic — il valide les identifiants contre la plateforme source avant que vous ne confirmez le reste de l'assistant. Si le test échoue, le message d'erreur indique généralement l'un des éléments suivants :

- **WooCommerce** — URL du magasin manquant `https://` ou avec un segment de chemin en fin de chaîne ; une clé/secret de consommateur mal orthographié ou régénéré ; ou une clé d'API REST créée sans autorisation **Read** à **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** — Domaine du magasin n'étant pas au format `yourstore.myshopify.com` ; ID/secret du client provenant d'une application différente ; ou, le plus souvent, une application créée dans le tableau de bord de développement mais jamais **installée** — créer une version d'application n'est pas suffisant, vous avez besoin du lien de distribution personnalisé et d'un clic sur **Install**. Spwig avertit également si `read_products`, `read_customers` ou `read_orders` n'ont pas été inclus dans les autorisations de l'application.
- **Magento 2** — URL du magasin pointant vers le site de vente au lieu de la racine de l'API, ou un jeton d'intégration créé mais jamais activé (**Save > Activate > Allow**).
- **Problèmes SSL** — un certificat expiré, auto-signé ou mal configuré échoue la connexion avant même la vérification des identifiants, affichant un message d'erreur général plutôt qu'une erreur d'authentification. Si les identifiants semblent corrects, vérifiez ensuite le certificat.

Réexécuter le test de connexion après chaque correction plutôt que de modifier plusieurs identifiants à la fois — cela isole celui qui était incorrect.

## Lire le journal en temps réel à l'étape 5

Pendant qu'une importation se déroule, l'étape 5 affiche un journal des activités en cours. Cliquez sur **Show Details** pour l'élargir en entrées individuelles — niveau et message — au lieu de simplement afficher un résumé de l'étape actuelle. C'est la méthode la plus rapide pour voir ce qui se passe si le progrès semble bloqué : une série d'entrées "skipped" pour un type de données indique généralement que l'option "Skip existing items" fonctionne comme prévu, et non que quelque chose est bloqué.

L'affichage du journal ne montre que les **500 dernières entrées**, donc sur une migration importante, les entrées les plus anciennes sortent de l'écran pendant que l'importation se poursuit. Si vous avez besoin du journal complet une fois qu'un type de données a terminé, utilisez **Download Logs** sur la page des résultats à la place — il n'a aucune limite.

## Ce qu'un échec de migration signifie réellement

C'est la chose la plus importante à comprendre si une migration échoue.

Lorsqu'une migration échoue, la page de fin vous indique clairement ce qui s'est produit : les éléments importés avant l'erreur restent dans votre magasin, rien n'a été supprimé automatiquement, et corriger le problème et relancer l'importation sautera ce qui a déjà été importé la première fois. Prenez cela à la lettre. Aucune étape de l'importation ne s'exécute dans une transaction de base de données pouvant être annulée en unité — ce qui a été importé avec succès avant le point d'échec, produits, catégories, clients, commandes, ce que le travail a réussi à traiter, reste dans votre magasin exactement comme il a été créé. Une migration échouée est une **migration partielle**, et non une migration annulée.

L'échec marque également le travail comme non réversible, donc le bouton **Rollback** ne sera pas disponible sur une **importation** échouée — il n'apparaît qu'une fois qu'une migration a été terminée, ou si un rollback d'une migration terminée a lui-même échoué partiellement, auquel cas Spwig propose à nouveau le bouton afin que vous puissiez réessayer. La seule situation où vous voudriez le plus un annulation automatique — une importation échouée — est exactement la situation où le bouton n'est pas proposé.

Donc, lorsque une migration échoue :

1. **Vérifiez ce qui a réellement été importé**, en utilisant les compteurs Imported/Skipped/Failed et les journaux téléchargés pour avoir une idée de ce qui se trouve dans votre magasin par rapport à ce qui n’a pas réussi.

2. **Décidez comment nettoyer.** Pour une petite quantité de données partielles, examinez-les manuellement et supprimez ce que vous ne souhaitez pas via les vues de liste administratives normales.

Pour une importation partielle plus importante ou plus désordonnée, il est souvent plus rapide de supprimer vous-même les données importées avant de recommencer à partir de zéro que de les réconcilier une par une.

3. **Réexécuter avec l'option 'Ignorer les éléments existants' activée**, quel que soit le chemin de nettoyage choisi — c'est ce qui empêche les données qui ont survécu de se dupliquer lors de la prochaine tentative.

## Réessayer

**Réessayer** relance l'importation à partir du début. Il efface les compteurs et les journaux précédents de la tâche et réimporte tout à partir du début — il ne reprend pas là où l'essai échoué s'était arrêté. Gardez **Ignorer les éléments existants** activé afin que les éléments qui ont déjà été importés ne soient pas dupliqués lors du deuxième passage.

Si une migration s'arrête car elle a atteint la **limite de 4 heures**, le message que vous verrez est exact : relancer l'importation à partir du début et ignorer les éléments déjà importés, et non un reprise à partir du point où elle s'était arrêtée. Pour un magasin suffisamment grand pour atteindre la limite de temps, réessayer l'ensemble plusieurs fois ne finit rarement ; au lieu de cela, réduisez l'étendue de chaque exécution en sélectionnant moins de types de données à l'étape 3 (les produits dans une exécution, les commandes dans une autre) et faites plusieurs passes plus petits.

## Annuler

**Annuler** est disponible sur une migration en cours, et il marque immédiatement la tâche comme échouée dans le tableau de bord. Il **n'arrête pas** la tâche d'importation en arrière-plan, qui continue de s'exécuter et d'écrire des données jusqu'à ce qu'elle atteigne un point d'arrêt naturel. Prêtez-vous à ce que les compteurs d'importation continuent d'augmenter pendant un certain temps après avoir annulé — laissez-les se stabiliser avant de décider ce que vous allez nettoyer, plutôt que d'agir sur les compteurs capturés au moment où vous avez cliqué sur Annuler.

## Il n'y a pas de pause ou de reprise

Spwig ne prend pas en charge le fait de suspendre une migration en cours et de la reprendre plus tard. Le bouton **Reprendre** du tableau de bord est destiné à un cas différent : une migration configurée via l'assistant mais jamais lancée. Il rouvre l'assistant là où vous l'aviez laissé lors de la configuration — sans lien avec une exécution déjà en cours.

## Rollback

> **Avertissement :** Le rollback est une action permanente et destructrice. Lisez entièrement cette section avant de l'utiliser.

Le rollback est proposé sur une **migration terminée**, et à nouveau sur une migration dont le rollback a précédemment échoué partiellement (statut **Rollback échoué**), donc un rollback bloqué peut être réessayé. Il supprime uniquement ce que l'importation elle-même a créé, et garde tout ce sur quoi votre magasin dépend maintenant :

- Un client migré qui a passé une commande réelle depuis l'importation est **gardé** — son compte, ses adresses, son historique de fidélité et son crédit en magasin restent avec lui, et cette commande réelle reste intacte. Seules les commandes créées par l'importation sont supprimées.

- Un produit migré qui est toujours référencé par toute commande, ensemble, carte-cadeau ou emplacement de configuration est **gardé**. Les commandes appartenant à d'autres clients ne sont jamais modifiées — le rollback ne peut plus retirer des éléments de commande non liés ou laisser une commande avec un total incorrect.

- Ce qui est gardé vous est signalé par nom et par nombre, avec la raison — par exemple « 1 Produit gardé, toujours référencé par un élément de commande » — afin que vous sachiez exactement ce qui reste et pourquoi.

- Les affiliés, commissions et paiements créés par l'importation **sont** supprimés, ainsi que tout compte affilié que l'importation a créé. Un affilié attaché à un client qui existait déjà garde son compte ; seul l'enregistrement affilié est supprimé.

- L'historique de fidélité et le crédit en magasin suivent le client : supprimés si le client est supprimé, gardés si le client est gardé.

Il ne supprime toujours pas les plans d'abonnement, les niveaux tarifaires ou les ressources de réservation créés par les extensions du magasin — ceux-ci survivent à un rollback et doivent être nettoyés manuellement si vous ne souhaitez pas les garder.

Avant de confirmer, la page de confirmation affiche un aperçu de ce qui sera exactement supprimé et ce qui sera conservé, calculé par rapport à vos données en temps réel — lisez-la avant de cliquer sur **Oui, Annuler la migration**.

L'annulation s'exécute ensuite en arrière-plan plutôt qu'à l'intérieur de votre navigateur, donc il est sûr de fermer l'onglet ; vérifiez l'état de la migration pour obtenir le rapport sur ce qui a réellement été supprimé et conservé une fois qu'elle est terminée.

Puisque l'annulation ne dépasse plus ce qui a été créé par l'import, elle n'est plus un outil à usage limité au même jour — les commandes réelles d'un client migré et les ventes réelles d'un produit migré sont protégées, indépendamment du temps écoulé depuis la migration. Il s'agit toujours d'une action permanente et destructrice sur les lignes qu'elle supprime, donc utilisez-la de manière réfléchie plutôt que de façon légère, et nettoyez à la main tout ce que Spwig conserve si vous ne le souhaitez pas réellement.

Concernant la disponibilité : le bouton Annuler reste disponible sur le résumé d'une migration terminée aussi longtemps que le record de la tâche existe — pour la plupart des plateformes, il n'y a pas de délai fixe. Magento est l'exception et perd la disponibilité d'annulation après une fenêtre prédéfinie, donc décidez rapidement si vous utilisez Magento. Les records de tâche ne sont pas supprimés selon un calendrier, donc une migration reste annulable indéfiniment à moins que vous ne supprimiez vous-même son record.

## Stratégie pour les grandes boutiques et imports lents

Pour une boutique suffisamment grande pour que l'exécution unique risque la limite de 4 heures :

- **Augmentez la taille du lot** à l'étape 3 (jusqu'à 100) — des lots plus importants signifient généralement moins de trajets aller-retour et une meilleure vitesse de traitement.
- **Séparez la migration en plusieurs exécutions par type de données** — les catégories et les produits dans une première exécution, les clients et les commandes dans une suivante, plutôt que tout en même temps.
- **Gardez l'option "Ignorer les éléments existants" activée** pour chaque exécution après la première, afin que les exécutions répétées ne dupliquent pas ce qui a déjà réussi.
- **Désactivez l'import des images des produits.** Le téléchargement et le traitement de chaque image sont généralement le facteur principal d'une exécution lente. Vous pouvez ajouter des images aux produits individuellement, ou via un import CSV séparé, une fois que le reste des données est en place.

## Conseils

- **Testez la connexion après chaque modification des identifiants**, et non seulement une fois à la fin — cela isole la valeur incorrecte.
- **Ne supposez jamais qu'une tâche échouée a nettoyé elle-même** — vérifiez ce qui est réellement présent dans votre boutique avant de décider d'un nettoyage ou d'une nouvelle tentative.
- **L'option "Ignorer les éléments existants" doit rester activée pour chaque tentative** — c'est la seule chose qui empêche les duplications lors d'une deuxième passe.
- **Ne luttez pas contre la limite de 4 heures avec plus de tentatives** — séparez plutôt par type de données.
- **Lisez l'aperçu d'annulation avant de confirmer** — elle indique exactement ce qui sera supprimé et ce qui sera conservé, calculé par rapport à vos données en temps réel, afin qu'il n'y ait aucune surprise.