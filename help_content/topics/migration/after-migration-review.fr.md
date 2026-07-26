---
title: Après votre migration
---

Une migration terminée marque le début de votre revue, pas la fin. L'étape 6 de l'assistant vous fournit un résumé de ce qui a été transféré, un outil pour corriger les liens qui pointent toujours vers votre ancien site, ainsi qu'un rapport que vous pouvez télécharger pour vos archives. Ce sujet vous guide à travers ce que vous devez vérifier avant de considérer le transfert comme terminé, y compris les tâches liées aux taxes, aux livraisons et à la mise en production que l'assistant ne fait pas à votre place.

## Lire vos résultats

En haut de la page de fin de migration, vous verrez une rangée de cartes statistiques — une par type de données (Produits, Catégories, Clients, Commandes, etc.) — suivie d'un tableau **Résumé d'importation** avec des colonnes pour les éléments Importés, Ignorés, Échoués et Total pour chaque étape exécutée.

- **Importés** — éléments créés avec succès dans Spwig.
- **Ignorés** — éléments que votre plateforme source avait, mais que Spwig n'a pas créés. Cela arrive presque toujours de manière attendue : avec **Ignorer les éléments existants** activé à l'étape 3, tout élément correspondant à un élément déjà existant dans Spwig (par SKU, e-mail, etc.) est laissé tel quel plutôt que dupliqué. Un nombre élevé d'éléments ignorés après un nouvel essai signifie simplement que la première tentative a déjà créé ces enregistrements.
- **Échoués** — éléments que Spwig a tenté de créer mais n'a pas pu, en raison d'un problème de données, d'une dépendance manquante ou d'une erreur côté source. Un nombre non nul d'éléments échoués mérite d'être investigué ; consultez [Résolution des problèmes de migration](migration-troubleshooting) pour savoir comment lire les journaux et quelles sont vos options de nettoyage.

> **Remarque :** Si une étape affiche des échecs, ne supposez pas que le magasin a annulé quoi que ce soit pour compenser — il ne le fait pas. Tout ce qui a été importé avant l'échec se trouve dans votre magasin à côté de tout ce qui a réussi. Vérifiez-le de la même manière que vous le feriez pour un résultat partiel normal.

## Réécriture des liens

Les produits, pages et articles de blog importés depuis votre ancienne plateforme contiennent souvent des liens vers leur domaine d'origine — une URL d'image, un lien vers un « produit similaire », une référence interne. Si Spwig détecte l'un de ces éléments dans le contenu qu'il vient d'importer, un panneau **Réécriture des liens** apparaît sur la page de fin.

Chaque lien détecté est regroupé par la page ou le produit d'où il provient, et affiché avec :

- **URL originale** — le lien tel qu'il apparaissait exactement dans le contenu importé.
- **URL suggérée** — la meilleure estimation de Spwig pour la page correspondante sur votre nouveau magasin, si une telle page a été trouvée.
- **Correspondance** — un pourcentage de confiance pour cette suggestion. Les liens sans correspondance raisonnable s'affichent comme **Aucune** et n'ont aucune URL suggérée à approuver.

Pour chaque lien, vous pouvez **Approuver** la suggestion ou **Ignorer** celle-ci, un par un. **Approuver automatiquement les suggestions à forte confiance** approuve toutes les suggestions à 85 % ou plus d'un seul clic — un gain de temps, mais toujours utile de vérifier quelques-unes après. Les suggestions en dessous de ce seuil sont celles qui méritent d'être ouvertes manuellement : une correspondance de 50 à 70 % pourrait être le bon produit sous le mauvais nom, ou elle pourrait être très éloignée, et seul un coup d'œil humain peut le dire.

Approuver ou ignorer un lien ne modifie que le statut du lien — rien dans votre contenu ne change jusqu'à ce que vous cliquiez sur **Appliquer les liens approuvés**, qui réécrit tous les liens approuvés en une seule fois. Cela signifie qu'il est sûr de parcourir la liste sur plusieurs séances avant de valider.

> **Conseil :** Laissez tout lien dont vous n'êtes pas sûr comme **Ignorer** plutôt que d'approuver une supposition. Vous pouvez toujours corriger manuellement un lien orphelin vers l'ancien domaine plus tard ; une réécriture incorrecte appliquée à une douzaine de produits est plus de travail à annuler.

## Vérification de vos données

Traitez les cartes statistiques comme un point de départ, pas comme une preuve que tout est correct. Prenez quelques minutes pour vérifier à l'œil :

- **Produits** — Ouvrez une poignée de produits, en particulier ceux qui ont des variantes (taille, couleur, etc.), et confirmez que les options de variantes et les prix ont été transférés correctement, et que les images sont attachées et affichées sur le site de vente, et non seulement dans l'administration.
- **Catégories** — Vérifiez que la hiérarchie des catégories semble correcte, en particulier si vous avez migré depuis Shopify, où les collections s'importent comme une liste plate plutôt que comme un arbre hiérarchique.
- **Comptes clients** — Vérifiez quelques enregistrements pour confirmer les e-mails et les adresses.

Les clients migrés ne conservent pas leur ancien mot de passe — Spwig n'a aucun moyen de le lire depuis la plateforme d'origine — donc **les clients devront réinitialiser leur mot de passe** lors de leur première connexion.

Pensez à envoyer un courriel d'avertissement une fois que vous êtes en ligne.
- **Commandes** — Vérifiez que les totaux, les statuts et les éléments de commande d'un échantillon de commandes correspondent à ce que vous avez vu sur l'ancienne plateforme.
- **Produits dérivés d'une extension** — Si vous avez migré depuis WooCommerce avec des extensions comme Subscriptions, Bundles, Gift Cards, Composite Products ou Bookings, vérifiez quelques produits qui en ont utilisé.

Les données d'extension qui ne peuvent pas être lues n'empêchent pas l'importation du produit — il est toujours importé, mais sans cette configuration supplémentaire — donc ces produits auront le plus besoin d'une correction manuelle.

## Configuration des taxes et des frais d'expédition

Les options du pas 4 du assistant pour importer les paramètres de taxes et les zones d'expédition enregistrent vos préférences, mais elles ne sont pas appliquées à l'importation — aucune taux de taxe ou zone d'expédition n'est créée à partir d'elles. C'est prévu : **la configuration des taxes et des frais d'expédition est une étape normale et distincte que vous effectuez directement dans Spwig** après la fin de l'importation des données, de la même manière que vous le feriez lors de la configuration d'une nouvelle boutique.

Le contrôle **Ajustement des prix** sur la même étape est l'exception — il prend effet pour les importations WooCommerce, CSV et Shopify, déplaçant le prix de base de chaque produit lors de sa création. Si vous en avez défini un et que vos prix semblent incorrects, c'est là que vient le changement. Voir [Migration Field Mapping](migration-field-mapping) pour les détails.

Avant de mettre en ligne, configurez :

- Vos taux de taxes — voir [Tax Configuration](tax-configuration) pour configurer les taux par pays, état ou région, y compris les exemptions nécessaires à vos produits.
- Vos zones et méthodes d'expédition — voir [Setting Up Shipping](setup-shipping) pour recréer les options d'expédition que vos clients avaient sur votre ancienne plateforme.

Faites cela avant de tester le paiement, afin que votre commande de test reflète les totaux réels.

## Télécharger votre rapport

La page de fin d'importation propose trois téléchargements :

- **Télécharger en PDF** — un résumé formaté avec les métadonnées de la tâche, les comptes par étape et une liste d'erreurs, limitée aux **premières 20 erreurs**.
- **Télécharger en CSV** — le même résumé sous forme de feuille de calcul, limité aux **premières 50 erreurs**.
- **Télécharger les journaux** — toutes les entrées de journal de la tâche, sans limite.

Si le nombre d'erreurs est faible, le PDF ou le CSV suffit. Pour une migration avec un grand nombre d'échecs, téléchargez les journaux à la place — c'est le seul des trois qui contient l'enregistrement complet plutôt qu'un échantillon tronqué.

> **Conseil :** Les enregistrements des tâches de migration — y compris leurs journaux et rapports — restent dans Spwig indéfiniment ; rien ne les supprime selon un calendrier. Téléchargez quand même une copie si vous souhaitez l'utiliser pour des archives hors ligne ou pour la partager avec quelqu'un qui n'a pas d'accès administrateur, mais il n'y a aucun compte à rebours qui vous force à le faire aujourd'hui.

## Mettre en ligne

Une fois que vous êtes satisfait de votre configuration des données, des taxes et des frais d'expédition :

1. **Testez le paiement de bout en bout.** Ajoutez un produit au panier, finalisez le paiement et confirmez que les taxes, les frais d'expédition et le paiement sont tous calculés et traités correctement, idéalement avec une méthode de paiement réelle en mode test.
2. **Mettez à jour votre DNS** pour pointer votre domaine vers Spwig uniquement après que ce test ait réussi. Ne changez pas le DNS en premier et ne déboguez pas après — les clients pourraient tomber sur un paiement cassé en attendant.
3. **Gardez votre ancienne boutique disponible, en mode lecture seule ou "fermée"**, jusqu'à ce que vous soyez sûr que la nouvelle gère correctement les commandes. Cela vous donne un recours sans risquer que des commandes soient passées sur l'ancienne plateforme après le changement.

## Révoquer les identifiants de la plateforme d'origine

Une fois que vous avez vérifié que la migration est terminée et que vous ne prévoyez pas de la relancer, retournez sur votre plateforme d'origine et révoquez ou supprimez la clé API, l'application ou l'intégration que vous avez créée pour elle (voir [Migrating from WooCommerce](migrate-from-woocommerce) ou le guide de la plateforme équivalente pour savoir où se trouve ce paramètre).


Spwig n'a pas besoin d'un accès permanent à votre ancien magasin après la fin de l'importation, donc le supprimer ferme un accès que vous n'utilisez plus.

## Conseils

- **Skipped est généralement acceptable, failed n'est pas** — un grand nombre de skipped après un nouvel essai avec Skip existing items on est attendu ; un nombre non nul de failed mérite une vérification des journaux.
- **Ne vous précipitez pas pour appliquer les liens approuvés** — les approbations et les sauts peuvent changer librement jusqu'à ce que vous cliquiez sur Appliquer, donc prenez votre temps avec ceux qui ont une faible confiance.
- **Configurez les taxes et les frais de livraison avant votre première vente en direct**, et non après — l'importation ne le fait pas pour vous, et un taux de taxe non configuré est facile à ignorer jusqu'à ce qu'un client se plaint.
- **Avertissez les clients concernant les réinitialisations de mot de passe** si vous envoyez un courriel à votre liste de clients concernant le changement, afin que la première connexion ne soit pas une surprise.
- **Téléchargez votre rapport avant la marque des 90 jours** si vous en avez besoin pour les enregistrements comptables ou de conformité.
- **Gardez l'ancien magasin disponible en lecture seule pendant un certain temps** — cela coûte peu et vous donne un filet de sécurité pendant vos premiers jours en direct sur Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Page de complétion de migration affichant les cartes de statistiques et le tableau de résumé Imported/Skipped/Failed/Total
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Panel de réécriture des liens avec des suggestions groupées, des pourcentages de confiance et les contrôles Approve/Skip/Apply Approved Links
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->