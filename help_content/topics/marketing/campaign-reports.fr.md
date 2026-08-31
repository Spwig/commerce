---
title: Rapports de campagne
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Chaque campagne envoyée via Campaign Studio dispose de sa propre page **Rapport** — un résumé sur une seule page du nombre de personnes atteintes, du nombre d'e-mails réellement arrivés et de la réaction des destinataires. Utilisez-la pour vérifier qu'un envoi s'est bien déroulé, détecter un problème de délivrabilité à un stade précoce, ou comparer la performance de différentes campagnes au fil du temps.

## Ouvrir un rapport

Depuis **Campaign Studio > Campagnes**, trouvez la campagne que vous souhaitez vérifier et cliquez sur l'icône graphique (**Rapport**) de sa carte.

![La grille de cartes statistiques de la page de rapport de campagne, affichant les destinataires, les livraisons, le taux d'ouverture, le taux de clic, le taux de rebond et les signalements de spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Un rapport ne contient des chiffres à afficher qu'une fois que la campagne a réellement été envoyée — une campagne encore en **Brouillon** affiche toutes les statistiques à zéro, car il n'y a encore rien à mesurer.

## Les cartes statistiques

| Carte | Ce qu'elle affiche |
|------|---------------|
| **Destinataires** | Le nombre d'abonnés ciblés par cette campagne, accompagné d'une sous-ligne indiquant combien ont été ignorés et, parmi ceux-ci, combien l'ont été spécifiquement parce que l'adresse figure sur votre [liste de suppression](list-hygiene). Un ignore n'est pas toujours une suppression — Spwig ignore également un abonné qui n'a pas d'adresse e-mail utilisable, par exemple — c'est pourquoi les deux compteurs sont affichés séparément. |
| **Livré** | Le nombre d'e-mails réellement acceptés par le serveur de messagerie destinataire et jamais renvoyés, ainsi que le **taux de livraison** — les livraisons en proportion de chaque envoi *tenté* par Spwig (accepté par votre serveur de messagerie ou votre fournisseur, qu'il ait rebondi ou non par la suite). |
| **Taux d'ouverture** | La proportion d'e-mails *livrés* qui ont été ouverts, ainsi que le nombre brut d'**ouvertures**. |
| **Taux de clic** | La proportion d'e-mails *livrés* qui ont été cliqués, ainsi que le nombre brut de **clics** et le **taux de clic par ouverture** — les clics en proportion des ouvertures, un indicateur de la pertinence de votre contenu pour les personnes qui l'ont déjà ouvert. |
| **Taux de rebond** | La proportion d'envois *tentés* qui ont rebondi, répartis en rebonds **durs** et **mous**. |
| **Signalements de spam** | Le nombre de destinataires ayant marqué l'e-mail comme spam ou courrier indésirable, ainsi que le **taux de signalement** — les signalements en proportion des e-mails *livrés*. |
| **Revenu attribué** | Le revenu des commandes que Spwig peut retracer jusqu'à cette campagne, ainsi que le nombre de commandes, la valeur moyenne de la commande (**AOV**), le revenu par e-mail livré et — une fois que vous avez saisi le coût de la campagne — son **ROAS**. Voir [Revenu attribué](#attributed-revenue) ci-dessous. |

## Pourquoi les taux utilisent des dénominateurs différents

Le taux d'ouverture, le taux de clic et le taux de signalement sont tous mesurés par rapport aux e-mails **livrés** — les destinataires qui pouvaient réellement voir l'e-mail — tandis que le taux de livraison et le taux de rebond sont mesurés par rapport aux envois **tentés**. C'est une pratique standard dans l'industrie de l'e-mail, et c'est pourquoi aucun de ces taux ne peut dépasser 100 % : un e-mail qui a rebondi n'a jamais été livré, il ne peut donc pas être compté dans votre taux d'ouverture ou de clic, et un e-mail qui n'a même pas été tenté (un ignore) ne compte pour aucun d'entre eux.

## Rebonds durs et rebonds mous

- **Rebond dur** — l'adresse est définitivement non livrable. Elle n'existe pas, ou le domaine refuse d'accepter le courrier pour elle.
- **Rebond mou** — un problème temporaire : une boîte aux lettres pleine, un serveur destinataire brièvement indisponible, et similaires. Les rebonds mous se résolvent souvent d'eux-mêmes.

Observez la répartition, pas seulement le total. Une augmentation du nombre de **rebonds durs** signifie généralement que votre liste contient des adresse obsolètes ou mal orthographiées ; une augmentation du nombre de **rebonds mous** est plus souvent un incident temporaire côté destinataire. Tout rebond dur, tout signalement de spam, et une adresse qui accumule des rebonds mous répétés alimentent tous la [liste de suppression](list-hygiene) automatique de Spwig — vous n'avez pas besoin d'agir vous-même, mais le rapport est l'endroit où vous remarquerez en premier un pic méritant investigation.

## Revenu attribué

Comme votre boutique et Campaign Studio vivent dans le même système, Spwig n'a pas besoin d'une plateforme d'analyse externe ou d'un pixel de suivi pour vous dire si une campagne a réellement généré des ventes. Lorsqu'un client clique sur un lien dans l'e-mail de cette campagne et atterrit sur votre boutique, Spwig peut suivre cette visite jusqu'à la caisse et créditer le revenu de la commande résultante à la campagne — c'est ce que montre la carte **Revenu attribué**.

La sous-ligne de la carte détaille davantage le chiffre :

- **Commandes** — le nombre de commandes créditées à cette campagne.
- **AOV** — la valeur moyenne de la commande sur ces commandes.
- **Revenu par e-mail** — le revenu attribué divisé par le nombre d'e-mails *livrés*, le même dénominateur que le rapport utilise pour le taux d'ouverture et le taux de clic.
- **ROAS** — retour sur investissement publicitaire, affiché uniquement une fois que vous avez saisi un montant de **Dépense** sur la campagne elle-même.

Il est calculé comme le revenu attribué divisé par la dépense.

Si les dépenses ont été enregistrées dans une devise différente de la devise par défaut de votre boutique, Spwig masque le ROAS plutôt que d'afficher un chiffre qui ne permet pas une comparaison directe — saisissez les dépenses dans la devise de base de votre boutique pour le voir.

Quelques points à connaître sur la manière dont ce chiffre est calculé :

- **C'est basé sur les clics, pas sur les ouvertures.** Un client doit cliquer sur un lien suivi dans l'e-mail et arriver sur votre boutique — une simple ouverture n'attribue jamais de revenus. C'est volontaire : le suivi des ouvertures est de plus en plus peu fiable maintenant que des services comme Apple Mail Privacy Protection préchargent les images pour presque tous les messages, gonflant les nombres d'ouvertures indépendamment du fait que quelqu'un ait réellement lu l'e-mail.
- **Il suit le modèle d'attribution de votre boutique.** Par défaut, c'est le **dernier point de contact non direct** avec une fenêtre de retour de 90 jours — le même clic doit mener à une commande dans cette fenêtre pour être compté, et une visite directe ultérieure n'efface pas le crédit déjà acquis par le clic de cette campagne.
- **Il respecte le consentement analytique.** Seuls les visiteurs qui ont accepté le consentement analytique dans le bandeau de cookies de votre boutique sont suivis (si vous n'utilisez pas de bandeau de consentement, le suivi suit la politique par défaut de votre boutique). Un client qui a refusé le consentement peut toujours acheter — sa commande simplement ne sera pas attribuée à aucun canal, y compris celui-ci.
- **Ce n'est pas rétroactif.** Le suivi des revenus ne couvre que les campagnes envoyées après l'activation du suivi d'attribution pour votre boutique. Une campagne envoyée avant cela n'affichera aucun revenu attribué ici, même si elle a généré de vraies ventes, simplement parce que Spwig n'a pas de données de clics enregistrées pour elle.
- **Les tests A/B et les campagnes récurrentes agrègent également leurs revenus attribués** — voir [Rapports sur un test A/B](#rapports-sur-un-test-ab) ci-dessous.

Vous trouverez également une carte **Revenus attribués (30j)** sur le tableau de bord de Campaign Studio lui-même, additionnant les revenus attribués par e-mail sur toutes les campagnes sur les 30 derniers jours — un contrôle rapide sans ouvrir un rapport individuel. Pour une vue à l'échelle de la boutique qui inclut tous les canaux, pas seulement l'e-mail — recherche organique, réseaux sociaux, affiliés, et plus — voir le tableau de bord [Attribution des revenus](/help/revenue-attribution) sous **Insights**.

## Engagement au fil du temps

Sous les cartes de statistiques, le graphique **Engagement au fil du temps** trace trois lignes — **Envoyés**, **Ouverts** et **Cliqués** — un point par jour, couvrant les 30 jours précédant aujourd'hui (ou moins, si la campagne n'a pas été envoyée aussi longtemps — le graphique ne commence jamais avant le jour du premier envoi de la campagne).

Quelques points à connaître sur la manière dont les lignes sont comptées :

- **Ouverts** et **Cliqués** comptent chaque destinataire une seule fois — le jour de leur *première* ouverture ou de leur *premier* clic — et non à chaque fois qu'ils rouvrent l'e-mail ou cliquent à nouveau sur un lien. Cela empêche le graphique d'être faussé par une poignée de personnes qui ouvrent le même e-mail à plusieurs reprises.
- Les totaux derrière ce graphique correspondent aux cartes de statistiques ci-dessus : **Envoyés** reflète le courrier que Spwig a tenté de livrer, tandis que **Ouverts** et **Cliqués** sont tous deux mesurés par rapport au courrier livré, tout comme les cartes **Taux d'ouverture** et **Taux de clic**.
- Le graphique n'apparaît que lorsque la campagne a au moins un envoi enregistré — une campagne encore en **Brouillon** affiche le message « Aucun envoi pour le moment » à la place, tout comme les cartes de statistiques.

Utilisez ce graphique pour voir la *forme* d'un envoi, et pas seulement ses chiffres finaux — une campagne envoyée à une grande liste montre souvent une forte augmentation des ouvertures les premier ou deuxième jour, puis diminue ensuite. Une deuxième hausse quelques jours plus tard peut indiquer que le serveur de messagerie d'un destinataire a mis votre message en file d'attente, ou que votre objet a été remarqué plus tard que d'habitude.

## Liens les plus populaires

Si votre e-mail contient des liens et qu'au moins un destinataire en a cliqué sur un, un tableau **Liens les plus populaires** apparaît sous le graphique, listant tous les liens suivis classés par popularité.

| Column | What it shows |
|--------|---------------|
| **Lien** | L'URL de destination telle qu'elle apparaissait dans votre e-mail. |
| **Clics** | Le nombre total de fois où ce lien a été cliqué, y compris les clics répétés du même destinataire. |
| **Uniques** | Le nombre de destinataires distincts ayant cliqué sur ce lien au moins une fois. |
| **Taux de clic** | Le **taux de clic** de ce lien — le **Nombre unique** divisé par le nombre de courriels envoyés. Cela utilise le même dénominateur que la carte **Taux de clic** en haut du rapport, vous pouvez donc comparer directement les performances d'un seul lien par rapport à l'ensemble de la campagne. |

Si votre courriel contient plusieurs produits ou un mélange de boutons d'appel à l'action, ce tableau est le moyen le plus rapide de savoir lequel a réellement généré des clics — utile pour décider ce que vous souhaitez mettre en avant davantage la prochaine fois.

## Destinataires

Cliquez sur **Destinataires** en haut du rapport pour ouvrir une liste complète et recherchable de toutes les personnes à qui cette campagne a été envoyée, avec leur statut de livraison et leur engagement.

Deux façons de réduire la liste :

- **Recherche** — filtre par adresse e-mail (une correspondance partielle fonctionne, donc taper une partie d'un domaine ou d'un nom suffit).
- **Engagement** — filtre pour un seul état à la fois : **Ouvert**, **Clic**, **Livré, mais non ouvert**, ou **Échec de livraison**. Laissez-le sur **Tous** pour voir la liste complète.

La liste affiche les 100 derniers destinataires correspondants à la fois, du plus récent au plus ancien — le compteur au-dessus de la liste reflète toujours le nombre total exact qui correspond à vos filtres actuels, même s'il est plus grand que ce qui est affiché. Pour une grande diffusion, réduisez d'abord la liste avec la recherche ou l'engagement plutôt que de défiler à travers tous les destinataires.

### Affichage de la chronologie des activités d'un destinataire

Cliquez sur l'icône d'activité sur la ligne d'un destinataire pour ouvrir la **Chronologie des activités du destinataire** — chaque événement suivi pour la copie de courriel de cette personne, dans l'ordre : livré, ouvert, cliqué (en indiquant quel lien), échec de livraison (avec la raison de l'échec), signalé comme spam, ou désabonné, chacun avec sa propre horodatage.

C'est le moyen le plus rapide pour répondre à une question spécifique concernant un client — par exemple, confirmer qu'un abonné particulier a bien reçu une campagne avant de le contacter à nouveau par un autre canal, ou vérifier quel lien un client a cliqué avant qu'il ne passe commande.

## Rapports d'un test A/B

Si la campagne que vous consultez est le conteneur d'un [test A/B](ab-testing), son rapport regroupe **toutes les variantes** — l'ensemble du test, combiné, y compris **Revenu attribué** — et non pas une seule variante seule. Pour voir comment chaque variante individuelle s'est comportée, ouvrez la page des résultats de ce test au lieu du rapport. Une [campagne récurrente](recurring-campaigns) fonctionne de la même manière : son rapport regroupe chaque envoi qu'elle a effectué.

## À quoi cela ressemble lorsqu'une campagne est bonne

Il n'y a pas de nombre sain unique qui convient à toutes les boutiques ou listes — l'audience, le secteur d'activité et le contenu modifient tous la base — mais quelques schémas sont à surveiller sur n'importe quelle campagne :

- Un **taux d'échec** principalement composé d'échecs temporaires, avec des échecs permanents rares, indique une liste propre, bien entretenue. Une augmentation soudaine des échecs permanents mérite d'être investiguée avant votre prochain envoi.
- Les **plaintes pour spam** proches de zéro sont l'objectif de chaque envoi. Les plaintes affectent plus votre réputation d'expéditeur que presque tout autre élément — voir [L'hygiène des listes](list-hygiene) pour comprendre pourquoi elles sont importantes au-delà de cette seule campagne.
- Un **taux de clic par ouverture** sain par rapport à votre taux d'ouverture indique que les personnes ayant ouvert ont trouvé le contenu suffisamment pertinent pour y agir — un faible taux de clic par ouverture accompagné d'un bon taux d'ouverture indique généralement que le sujet a fonctionné mieux que le contenu à l'intérieur.

## Conseils

Conservez tous les formats markdown, les chemins d'images, les blocs de code et les termes techniques.

- Vérifiez le rapport quelques instants après l'envoi, pas immédiatement : les ouvertures et les clics (ainsi que certains rapports de rebond) peuvent prendre du temps pour arriver depuis votre fournisseur de messagerie.
- Si **Livré** semble inférieur à la moyenne, vérifiez d'abord la répartition des **Destinataires** — un lot de sauts dus à une suppression est souvent l'histoire réelle, et non un problème de livraison.
- Utilisez le rapport pour comparer une campagne à vos envois précédents plutôt qu'à un chiffre générique du secteur : votre liste, votre contenu et votre audience déterminent votre base réaliste.
- Une augmentation soudaine des plaintes pour un envoi particulier mérite une analyse plus approfondie du contenu ou de la ciblage de cette campagne, et non simplement une note pour passer à autre chose.
- Pour une campagne testée en A/B, lisez ce rapport pour obtenir le résultat global et la page [résultats du test A/B](ab-testing) pour connaître la version qui a gagné et de combien.
- Utilisez le tableau **Liens les plus cliqués** pour trouver le lien le plus cliqué, puis vérifiez s'il correspond à ce que vous avez *souhaité* que les destinataires cliquent — si un lien secondaire dépasse votre appel à l'action principal, il pourrait être utile de le placer plus haut dans le courriel la prochaine fois.
- Les filtres **Ouverts** et **Cliqués** de la page **Destinataires** sont un moyen rapide de constituer un public pour un suivi — par exemple, vérifier qui a ouvert mais n'a pas cliqué avant de planifier un rappel à l'ensemble de la liste.
- Si vous avez payé une promotion autour d'un envoi — un post social boosté, une mention d'influenceur, un location de liste payante — indiquez-le en tant que **Dépense** de la campagne pour déverrouiller le **ROAS** sur le rapport.

C'est le moyen le plus rapide pour voir quels types d'envois sont réellement à répéter.