---
title: Parcours déclenchés
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Les **Parcours** de Campaign Studio sont des séquences d'e-mails automatisées et multi-étapes qui démarrent automatiquement lorsqu'un client effectue une action spécifique — s'inscrit, passe une commande, laisse des articles dans son panier, reste inactif pendant un certain temps, ou a une commande livrée. Au lieu de vous souvenir d'envoyer manuellement un e-mail de bienvenue, une relance de panier ou une demande d'avis, vous créez la séquence une seule fois et Spwig l'exécute pour chaque client éligible, tant que le parcours reste actif.

## Trois façons d'envoyer des e-mails

Campaign Studio couvre désormais trois modèles d'envoi distincts :

| Type | Comportement |
|------|-----------|
| **Diffusion** | Envoyé une seule fois — immédiatement ou à une date et une heure planifiées. À utiliser pour une annonce ou une vente ponctuelle. |
| **Récurrent** | Un modèle qui s'envoie selon un calendrier répété (voir [Campagnes récurrentes](/help/recurring-campaigns)). |
| **Parcours** | Une séquence multi-étapes qui démarre automatiquement pour un client lorsqu'un événement du cycle de vie se produit, puis diffuse ses étapes sur des heures ou des jours. |

Un parcours n'a pas de bouton « Envoyer » propre et aucun calendrier à configurer — il réagit aux événements plutôt qu'à l'horloge.

## Déclencheurs

Chaque parcours écoute exactement un événement, défini comme le **Déclencheur** du parcours :

| Déclencheur | Se déclenche lorsque |
|---------|-----------|
| **Un client s'inscrit** | Un nouveau compte client est créé. |
| **Une commande est passée** | Toute commande est passée, par un nouveau ou un client existant. |
| **La première commande est passée** | Spécifiquement la toute première commande d'un client. |
| **Panier abandonné** | Un acheteur ajoute quelque chose à son panier, puis reste inactif sans finaliser l'achat. |
| **Client inactif (récupération)** | Un client n'a pas passé de commande depuis un certain temps. |
| **Commande livrée** | Le statut d'une commande passe à Livrée. |
| **Produit de nouveau en stock** | Un produit pour lequel un client a demandé à être notifié est de nouveau disponible. |

## Les déclencheurs de récupération et de réengagement, en détail

**Commande livrée** et **Produit de nouveau en stock** se déclenchent immédiatement, de la même manière que **Une commande est passée**. **Panier abandonné** et **Client inactif (récupération)** fonctionnent différemment : au lieu de réagir à un moment précis, Spwig vérifie périodiquement les acheteurs et les clients qui correspondent aux critères, il peut donc y avoir un court délai entre l'inactivité d'un panier (ou l'inactivité d'un client) et l'inscription au parcours.

**Panier abandonné** — inscrit un acheteur qui a ajouté quelque chose à son panier puis est resté inactif sans finaliser l'achat. Par défaut, cela se produit après environ une heure d'inactivité ; la fenêtre d'inactivité exacte (et la période de recul sur laquelle Spwig effectuera toujours la recherche) est un seuil que votre hébergeur peut ajuster pour votre boutique. Cela fonctionne pour les acheteurs connectés et les invités — pour un invité, Spwig utilise l'adresse e-mail capturée lors de l'achat. Si l'acheteur revient et finalise sa commande, il est automatiquement retiré du parcours, afin qu'un achat finalisé ne reçoive jamais un e-mail « avez-vous oublié quelque chose ? ». Ajoutez un bloc de contenu **Panier abandonné** à l'e-mail de récupération pour afficher exactement ce qui a été laissé derrière, avec des prix en direct, des images et un lien vers le panier — ou utilisez un bloc **Produit vedette** pour mettre en avant un article en particulier.

**Client inactif (récupération)** — inscrit un client qui n'a pas passé de commande depuis un certain temps, pour lui donner une raison de revenir.

Par défaut, cela correspond à 90 jours sans achat (également un seuil ajustable par l'hébergeur).

Un client n'est réintégré dans un parcours de réactivation qu'une seule fois par fenêtre, de sorte qu'une personne qui reste inactive ne soit pas réinscrite immédiatement.

**Commande livrée** — inscrit un client dès que le statut de sa commande passe à **Livrée**, ce qui est un moment naturel pour demander un avis quelques jours plus tard. Il se déclenche une fois par commande, lors de la transition vers Livrée — les modifications ultérieures d'une commande déjà livrée ne le déclenchent pas à nouveau. Notez que l'action en masse **Marquer les commandes sélectionnées comme Livrées** de la liste des commandes met à jour les commandes directement et ne déclenche pas ce déclencheur (ni l'e-mail de confirmation de livraison) ; mettez à jour les commandes une par une, ou via l'application mobile Spwig, pour qu'il se déclenche.

**Produit de nouveau en stock** — lorsqu'un produit pour lequel un client a demandé à être notifié revient en stock, Spwig vérifie si vous avez un parcours actif à l'écoute de ce déclencheur. Si c'est le cas, le client est inscrit dans ce parcours au lieu de l'alerte ponctuelle simple — vous pouvez ainsi ajouter un délai, un bloc **Produit en vedette** montrant l'article réapprovisionné, ou un e-mail de suivi. Si aucun parcours de réapprovisionnement n'est actif, les clients reçoivent toujours l'e-mail de notification ponctuelle standard comme avant, de sorte qu'activer un parcours pour ce déclencheur est entièrement optionnel.

## Créer un parcours

Accédez à **Studio de campagnes > Parcours** et cliquez sur **Ajouter un parcours**.

1. Donnez au parcours un **Nom** — cela est uniquement pour votre référence ; les clients ne le voient jamais.
2. Choisissez l'événement **Déclencheur**.
3. Définissez éventuellement **Uniquement pour le segment** sur un Segment — lorsqu'il est défini, seuls les abonnés appartenant à ce segment sont inscrits. Laissez-le vide pour inscrire tous les abonnés éligibles.
4. Définissez **Une fois par abonné** et **Délai de réinscription (jours)** — voir [Prévenir les sur-inscriptions](#guarding-against-over-enrollment) ci-dessous.
5. Définissez **Statut** sur **Actif** pour activer le parcours. Laissez-le sur **Brouillon** tant que vous êtes encore en train de le concevoir, ou définissez-le sur **En pause** pour arrêter les nouvelles inscriptions sans perdre votre configuration.
6. Cliquez sur **Enregistrer** — Spwig vous emmène directement dans le [Créateur de parcours](/help/journey-builder), le canevas visuel où vous concevez la séquence réelle : quels e-mails sont envoyés, combien de temps attendre entre eux, et si différents abonnés doivent suivre des chemins différents.

Une simple série d'accueil en trois étapes, une fois conçue sur le canevas, pourrait ressembler à ceci :

| Étape | Attend | Envoie |
|------|-------|-------|
| 1 | Immédiatement | E-mail de bienvenue |
| 2 | 3 jours plus tard | Conseils de démarrage |
| 3 | 7 jours après cela | Remise sur la première commande |

Les e-mails eux-mêmes sont des Campagnes ordinaires que vous concevez dans le même créateur visuel que vous utiliseriez pour une Diffusion — objet, blocs de contenu, tout. Il n'est pas nécessaire de planifier ou d'envoyer vous-même ; laissez-le en **Brouillon** et sélectionnez-le simplement depuis le menu déroulant de l'étape dans le créateur. Le parcours l'envoie pour vous, une fois par abonné qui atteint cette étape.

Voir [Créateur de parcours](/help/journey-builder) pour le guide complet de la conception d'étapes sur le canevas, du branchement d'un parcours avec une condition **Oui/Non**, et du démarrage à partir d'un modèle prêt à l'emploi au lieu d'un canevas vierge.

## Test A/B d'une étape

Toute étape **Envoyer un e-mail** peut être transformée en test A/B, de sorte qu'un parcours découvre automatiquement — et continue ensuite d'utiliser — l'e-mail qui performe le mieux. Parce qu'un parcours fonctionne en continu (les abonnés arrivent au fil du temps), Spwig ne teste pas un lot fixe et s'arrête ; au lieu de cela, il **divise les inscrits uniformément entre les variantes au fur et à mesure qu'ils arrivent, observe comment chacune performe, et dès qu'une est un vainqueur statistique clair, il verrouille cette variante pour tous les inscrits futurs.** Les abonnés déjà en cours de parcours conservent la version qui leur a été envoyée en premier.

Ouvrez une étape Envoyer un e-mail dans le [Créateur de parcours](/help/journey-builder) et définissez **Type d'étape** :

- **Email unique** — comportement normal : chaque personne reçoit le même e-mail que vous choisissez.
- **A/B : e-mails différents** — sélectionnez **deux à quatre** e-mails (différents dans leur conception, leurs offres ou leur mise en page) ; chaque inscrit reçoit l'un d'eux.
- **A/B : sujets d'e-mails différents** — sélectionnez un e-mail et saisissez **deux à quatre** sujets ; chaque inscrit reçoit cet e-mail avec un sujet différent.

Ensuite, choisissez **Choisir le gagnant par** — **Taux d'ouverture** (généralement le meilleur pour un test de sujet) ou **Taux de clic** — et c'est terminé. Configurez le parcours **Actif** et les inscrits commencent à être répartis entre les variantes.

Le panneau de l'étape affiche un **tableau de score en temps réel** alors que les données arrivent — chaque variante, le nombre de destinataires, le taux d'ouverture et le taux de clic, ainsi que le degré de confiance de Spwig dans le leader (« En tête à 92 % de confiance »). Un gagnant n'est verrouillé que lorsqu'il y a au moins **95 % de confiance** *et* suffisamment de données pour y croire, donc un parcours à faible trafic ne tire pas de conclusions hâtives. Une fois verrouillé, l'étape affiche **« Gagnant verrouillé : Variante B »** et chaque nouvel inscrit reçoit cette variante ; sur le canevas, la carte affiche **« A/B · N e-mails »** pendant le test, puis **« Gagnant A/B : B »** une fois décidé.

Quelques éléments à noter :

- **Donnez-lui du trafic.** La confiance dépend du volume — un étape atteint par quelques personnes ne restera peut-être qu'à « Pas assez de données pour l'instant » pendant un moment. Le test A/B fonctionne bien sur des parcours avec un nombre constant d'inscrits.
- **Modifier les variantes ou le critère de victoire démarre un nouveau test** — un gagnant verrouillé précédemment est effacé afin que le nouveau paramétrage puisse obtenir ses propres résultats.
- Un étape A/B avec moins de deux variantes **bloque le parcours jusqu'à ce qu'il soit activé** jusqu'à ce que vous l'ayez terminé (ou que vous le passiez à un e-mail unique).

Voyez [Test A/B](ab-testing) pour plus d'informations sur la manière dont Spwig lit la confiance et la signification.

## Comment fonctionne l'inscription

Lorsqu'un événement déclencheur se produit pour un client, Spwig vérifie chaque parcours actif qui écoute cet événement et, pour chaque parcours pour lequel le client est éligible, **l'inscrit** au point de départ du flux. À partir de là, Spwig fait avancer le souscripteur à travers tout ce que vous avez conçu sur le canevas — attendre chaque étape **Attente**, envoyer l'e-mail de chaque étape **Envoi d'e-mail**, et suivre le bon chemin **Oui**/**Non** à tout **Bras** — jusqu'à ce qu'ils atteignent une étape **Sortie**, auquel cas le parcours est marqué **Terminé** pour ce souscripteur.

**La consentement est toujours respecté.** Un souscripteur qui n'a pas opté pour les e-mails marketing, ou qui s'est désabonné depuis, est simplement ignoré — le parcours ne s'arrête pas pour les autres souscripteurs, et les désabonnements intermédiaires stoppent automatiquement les envois restants de ce souscripteur. Vous n'avez jamais besoin de filtrer vos parcours par rapport à leur statut de consentement vous-même.

## Protection contre l'inscription excessive

Deux paramètres sur le parcours contrôlent combien de fois un souscripteur peut y passer :

| Paramètre | Ce qu'il fait | Utilisation typique |
|---------|--------------|-------------|
| **Une fois par souscripteur** *(activé par défaut)* | Chaque souscripteur n'est inscrit qu'une seule fois, peu importe le nombre de fois où l'événement déclencheur se produit à nouveau pour lui. | Une série de bienvenue — un client ne devrait jamais recevoir cela plus d'une fois. |
| **Délai de réinscription (jours)** | Lorsque **Une fois par souscripteur** est désactivé, il définit un nombre minimum de jours à passer depuis la dernière inscription d'un souscripteur avant qu'il puisse être inscrit à nouveau. Définissez sur `0` pour aucun délai. | Une série déclenchée par une commande qui devrait s'exécuter à nouveau pour une nouvelle commande, mais pas s'exécuter à nouveau pour chaque commande passée la même semaine. |

Désactivez **Une fois par souscripteur** pour un parcours que vous souhaitez exécuter par commande (comme un remerciement après achat), et associez-le à un délai de réinscription afin qu'un client qui passe deux commandes le même jour n'ait qu'une seule inscription. Un souscripteur en train de travailler sur un parcours n'est jamais inscrit dans un deuxième parcours qui se chevauche, peu importe ces paramètres.

## Surveillance des parcours

Préservez toutes les formattages markdown, les chemins d'images, les blocs de code et les termes techniques.

La liste **Campaign Studio > Journeys** affiche le **Déclencheur**, le **Statut**, le nombre d'**Emails** envoyés et les totaux en cours d'**Inscrits** / **Terminés** pour chaque parcours, afin de voir d'un coup d'œil si un parcours atteint réellement les personnes.

![La liste des parcours montrant deux parcours actifs avec les nombres d'inscriptions et de complétions](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Pour voir les abonnés individuels plutôt que les totaux, ouvrez la liste **Journey Enrollments** à `/admin/email_marketing/journeyenrollment/`. Chaque ligne montre la progression d'un abonné à travers un parcours : le **Parcours** dans lequel il se trouve, son **Étape actuelle**, son **Statut** (Actif, Terminé ou Annulé) et quand son **Prochaine étape** est due. Utilisez les filtres pour restreindre à un parcours ou à un statut — par exemple, filtrer sur **Actif** montre tous ceux qui sont actuellement en cours de séquence.

![La liste des inscriptions aux parcours montrant la progression des abonnés à travers deux parcours](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Rapport de parcours

Chaque parcours a sa propre page **Rapport**, ouverte en cliquant sur le bouton **Rapport** sur la carte du parcours dans **Campaign Studio > Journeys**, ou sur la page de paramètres du parcours lui-même. C'est un résumé sur une seule page de la distance parcourue par les inscrits dans la séquence et, lorsque vos e-mails contiennent des liens suivis, du chiffre d'affaires généré par le parcours.

![La page de rapport du parcours montrant l'entonnoir d'inscription, la carte du chiffre d'affaires attribué et le tableau du chiffre d'affaires par étape](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Entonnoir d'inscription

Quatre cartes montrent où en sont actuellement les inscrits :

| Carte | Ce qu'elle montre |
|------|---------------|
| **Inscrits** | Le nombre total d'abonnés qui ont déjà rejoint ce parcours. |
| **Actifs actuellement** | Les inscrits actuellement en cours de séquence, en attente ou en train de traiter leur prochaine étape. |
| **Terminés** | Les inscrits qui ont atteint l'étape **Sortie** du parcours. |
| **Sortis** | Les inscrits retirés du parcours avant sa complétion — par exemple, un acheteur qui a terminé le paiement en cours d'une séquence d'abandon de panier, ou un abonné qui s'est désabonné. |

Si le parcours n'a pas encore d'inscriptions, les quatre cartes affichent zéro et une note vous rappelle que les métriques apparaissent dès que les clients commencent à rejoindre le parcours.

### Chiffre d'affaires attribué

La carte **Chiffre d'affaires attribué** fonctionne de la même manière qu'un [rapport de campagne](campaign-reports) — Spwig trace les commandes jusqu'aux clics sur les liens dans les e-mails du parcours, avec la même attribution par clic, soumise au consentement, décrite dans [Chiffre d'affaires attribué](campaign-reports#attributed-revenue) sur cette page. Les mêmes réserves s'appliquent ici : l'attribution est uniquement par clic (une simple ouverture n'attribue jamais de chiffre d'affaires), elle suit le modèle d'attribution actif et la fenêtre de rétroactivité de votre boutique, elle respecte le consentement analytique, et elle n'est pas rétroactive — un parcours n'affiche que le chiffre d'affaires des e-mails envoyés après l'activation du suivi d'attribution pour votre boutique.

La sous-ligne de la carte détaille le total en :

- **Commandes** — le nombre de commandes créditées à ce parcours, sur l'ensemble des e-mails de toutes les étapes combinées.
- **Panier moyen** — la valeur moyenne des commandes parmi ces commandes.
- **Revenu par inscrit** — le chiffre d'affaires attribué divisé par le total des **Inscrits**. Un parcours n'a pas de « dépense » unique comme une campagne — il fonctionne en continu plutôt que de coûter quelque chose une seule fois — donc il n'y a pas de figure ROAS ici. Le **Revenu par inscrit** est l'équivalent le plus proche : une mesure stable et comparable de l'efficacité avec laquelle le parcours transforme une inscription en vente, que vous pouvez suivre dans le temps ou comparer à un autre parcours.

### Chiffre d'affaires par étape

Lorsque le parcours a au moins une étape **Envoyer un e-mail**, un tableau **Chiffre d'affaires par étape** détaille davantage le total, une ligne par étape, afin que vous puissiez voir quel e-mail de la séquence est réellement rentable :


| Colonne | Ce qu'elle affiche |
|--------|---------------|
| **Étape** | L'e-mail de l'étape, avec un badge **A/B** si cette étape exécute un [test A/B](ab-testing). |
| **Revenu** | Le revenu attribué aux commandes retracées jusqu'à l'e-mail de cette étape. |
| **Commandes** | Le nombre de commandes derrière ce chiffre de revenu. |
| **Envoyés** | Le nombre de fois où l'e-mail de cette étape a été envoyé. |
| **Ouvertures** / **Clics** | Le nombre de ces envois qui ont été ouverts, et le nombre de clics. Spwig suit les ouvertures et les clics pour les envois de chaque étape, qu'ils soient simples ou A/B. |

Utilisez ce tableau pour repérer un maillon faible dans un parcours globalement sain — par exemple, une série de bienvenue où le premier e-mail génère la majeure partie du revenu et une étape ultérieure contribue peu pourrait être un candidat pour une offre plus forte ou une réécriture, plutôt que de supposer que toute la séquence doit être repensée.

## Conseils

- La façon la plus rapide de démarrer un parcours d'abandon de panier, de réactivation, d'avis après livraison ou de retour en stock est un modèle de démarrage — lorsque vous enregistrez un nouveau parcours avec l'un de ces déclencheurs, le sélecteur **Modèles** du [Journey Builder](/help/journey-builder) propose un flux prêt à l'emploi (**Récupération du panier abandonné**, **Réactivation des clients inactifs**, **Demande d'avis après livraison** ou **Alerte de retour en stock**) que vous pouvez ajuster plutôt que de construire à partir de zéro.
- Commencez chaque parcours en **Brouillon** pendant que vous construisez ses étapes, puis passez le **Statut** à **Actif** une fois que vous avez vérifié les e-mails et les délais — aucun abonné n'est inscrit tant que le parcours n'est pas Actif.
- Gardez **Une fois par abonné** activé pour tout ce qui est lié à un jalon unique (inscription, première commande) ; désactivez-le avec un délai de refroidissement raisonnable pour tout ce qui doit se répéter, comme une série après achat.
- Utilisez **Uniquement pour le segment** pour exécuter une série de bienvenue différente pour un public spécifique — par exemple, un segment VIP reçoit une séquence plus riche que tout le monde.
- Réglez l'attente de la première étape sur `0` si vous souhaitez que le premier e-mail soit envoyé immédiatement après le déclenchement, plutôt que d'attendre.
- Vérifiez la liste des **Inscriptions au parcours** après l'activation d'un nouveau parcours pour confirmer que les abonnés sont effectivement inscrits et progressent à travers leurs étapes comme prévu.
- La mise en pause d'un parcours (**Statut : En pause**) arrête les nouvelles inscriptions mais n'annule pas les abonnés déjà en cours de route — ils continuent de recevoir leurs étapes restantes.