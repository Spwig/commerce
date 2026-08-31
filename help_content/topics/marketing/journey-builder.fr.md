---
title: Constructeur de parcours
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (ouvrir le constructeur de tout parcours, cliquer sur Modèles)
  filename: journey-builder-templates.webp
  description: Le sélecteur de modèles avec les huit premiers visibles (séries de bienvenue,
    onboarding de commande première, suivi après achat et avis, offre VIP vs. standard, récupération de panier abandonné, rappel de clients désengagés, demande de suivi après livraison,
    alerte de réapprovisionnement) — remplace la capture d'écran existante à la même
    adresse, qui est désormais obsolète.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

Le **Constructeur de parcours** est la toile de dessin visuelle, glissé-déposé, où vous concevez ce que fait réellement un [Parcours](/help/parcours declenches). — les e-mails qui sont envoyés, combien de temps attendre entre eux, et si différents abonnés devraient suivre des chemins différents. Au lieu de remplir un formulaire, vous construisez le flux sous forme de schéma : des boîtes connectées sur une toile que vous pouvez déplacer, diviser et prévisualiser d'un coup d'œil.

## Ouvrir le constructeur

Chaque parcours a sa propre toile de dessin. Vous pouvez y accéder de deux manières :

- Créer un nouveau parcours — remplir son **Nom**, **Déclencheur**, et la cible sur la page des paramètres et cliquer sur **Enregistrer** — vous amène directement dans le constructeur pour commencer à concevoir immédiatement.
- Ouvrir la page des paramètres d'un parcours existant et cliquer sur **Construire le parcours** en haut.

Le constructeur est un espace de travail plein écran avec trois zones : une **palette** de types d'étapes sur la gauche, la **toile** au milieu, et un panneau de **paramètres de l'étape** sur la droite qui s'affiche lorsque vous sélectionnez quelque chose.

![La toile du Constructeur de parcours montrant une série de bienvenue avec une branche Oui/Non](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

En haut de la toile, un en-tête répète le **Déclencheur** du parcours et la **cible** (ou "Tous les abonnés" s'il n'y a pas de segment défini) afin que vous sachiez toujours à qui vous concevez sans quitter le constructeur. Utilisez le **Retour** pour revenir à la page des paramètres du parcours.

## Les types d'étapes

Glissez une étape de la palette de gauche vers la toile, ou cliquez sur un élément de la palette pour le déposer automatiquement. Quatre types d'étapes sont disponibles :

| Étape | Ce qu'elle fait |
|------|----------------|
| **Envoyer un e-mail** | Envoie l'une de vos campagnes à l'abonné. |
| **Attente** | Met en pause pendant un nombre défini d'heures ou de jours avant de continuer. |
| **Branche** | Divise le chemin en deux — **Oui** ou **Non** — en fonction de si l'abonné appartient à un segment que vous choisissez. |
| **Sortie** | Met fin au parcours pour l'abonné. |

Chaque parcours commence par une seule étape **Entrée**, créée automatiquement la première fois que vous ouvrez le constructeur. Elle affiche le déclencheur du parcours et ne peut pas être supprimée — c'est simplement l'endroit où les abonnés entrent dans le flux.

## Connexion des étapes

Chaque étape a un petit **port** circulaire : un sur le haut (entrée) et un ou plusieurs sur le bas (sortie). Pour connecter deux étapes, faites glisser depuis le port du bas d'une étape vers le port du haut d'une autre — une ligne courbe apparaît reliant les deux.

Une étape **Branche** a deux ports de sortie au lieu d'un seul : un **Oui** vert et un **Non** rouge. Connectez chacun vers l'endroit où ce chemin doit mener — ils peuvent se rejoindre plus tard au même endroit (comme dans l'exemple ci-dessus, où les deux chemins reviennent vers la même **Sortie**) ou prendre leur propre chemin.

Pour modifier la disposition, faites glisser une étape par son corps pour la repositionner — les lignes connectées suivent automatiquement. Faites glisser une partie vide de l'arrière-plan de la toile pour faire défiler, et utilisez la molette de défilement pour agrandir ou réduire. Si vous perdez le fil du flux, cliquez sur **Ajuster** dans la barre d'outils pour recentrer et zoomer pour afficher l'ensemble de l'écran.

## Configuration d'une étape

Cliquez sur n'importe quelle étape pour ouvrir ses paramètres dans le panneau de droite :

| Étape | Paramètre |
|------|---------|
| **Envoyer un e-mail** | Choisissez le **E-mail à envoyer** dans la liste déroulante de vos campagnes. |
| **Attente** | Définissez **Attendre** — un nombre suivi de **heures** ou **jours**. |
| **Branche** | Choisissez **Si l'abonné est dans le segment** — le segment qui détermine Oui ou Non. |
| **Sortie** | Aucun paramètre — c'est simplement un point de terminaison. |

![Panneau de droite configurant une étape de Branche, avec le canevas assombri en arrière-plan](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Les modifications sont enregistrées automatiquement dès que vous choisissez une valeur — il n'y a pas de bouton **Enregistrer** séparé sur le canevas. Chaque étape, sauf **Entrée**, possède un bouton **Supprimer l'étape** en bas de son panneau de paramètres.

Les e-mails que vous choisissez pour les étapes **Envoyer un e-mail** sont des campagnes ordinaires que vous concevez dans le créateur visuel standard de Campaign Studio — objet, blocs de contenu, tout est inclus. Laissez-les en **Brouillon** et sélectionnez-les simplement depuis la liste déroulante ici ; le parcours les envoie pour vous, vous ne cliquez jamais sur Envoyer vous-même.

## Démarrer à partir d'un modèle

Construire un flux depuis un canevas vierge n'est pas toujours nécessaire — cliquez sur **Modèles** dans la barre d'outils (ou **Parcourir les modèles** sur un canevas vide) pour ouvrir un sélecteur avec huit modèles prêts à l'emploi :

| Modèle | Ce qu'il construit |
|----------|-----------------|
| **Série de bienvenue** | Accueillir les nouveaux abonnés, partager ce que vous proposez, puis un rappel pour la première commande. |
| **Intégration première commande** | Transformer un premier acheteur en client fidèle avec une séquence d'intégration douce. |
| **Post-achat et avis** | Remercier après toute commande, puis demander un avis une fois celle-ci livrée. |
| **Offre VIP vs. standard** | Après une commande, branche sur votre segment VIP pour envoyer l'offre de suivi appropriée à chaque groupe. |
| **Récupération panier abandonné** | Rappeler à un acheteur qui a laissé des articles derrière, puis un rappel de suivi un jour plus tard. |
| **Réactivation clients inactifs** | Réengager un client qui n'a pas acheté depuis un moment avec une raison de revenir. |
| **Demande d'avis post-livraison** | Demander un avis quelques jours après qu'une commande est marquée comme Livrée. |
| **Alerte retour en stock** | Informer un acheteur en attente dès qu'un produit qu'il souhaitait est à nouveau disponible. |

Chaque modèle est préconfiguré avec le déclencheur correspondant — par exemple, appliquer **Réactivation clients inactifs** à un nouveau parcours suppose également que le **Déclencheur** de ce parcours soit **Client inactif (réactivation)**. Consultez [Parcours déclenchés](/help/triggered-journeys) pour savoir ce qui déclenche chacun de ces événements et comment fonctionnent ceux axés sur la récupération (fenêtres d'inactivité, commande invité, demandes d'avis une fois par commande, et comment un parcours de retour en stock prend le relais de l'alerte ponctuelle standard).

![Le sélecteur de modèles montrant les parcours de démarrage prêts à l'emploi](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

L'application d'un modèle **remplace le flux actuel** sur le canevas, utilisez-le donc au début de la conception d'un parcours plutôt qu'en cours de route. Spwig relie chaque étape à un e-mail ou un segment réel lorsque les noms correspondent à quelque chose que vous avez déjà ; partout où il ne trouve pas de correspondance, l'en-tête indique combien d'étapes ont encore besoin d'un e-mail ou d'un segment choisi, afin que vous sachiez exactement quoi finaliser avant la mise en ligne.

## Partage des parcours

Deux boutons de la barre d'outils vous permettent de déplacer la conception d'un parcours entre les étapes ou entre les magasins :

- **Exporter** télécharge le parcours sous forme de fichier `.journey.json` — une description portable de la forme du flux (ses étapes, attentes, branches et chemins Oui/Non) ainsi que les *noms* des e-mails et des segments utilisés par chaque étape. Il n'inclut pas les conceptions des e-mails eux-mêmes ni aucune donnée d'abonné.
- **Importer** charge un fichier `.journey.json` dans le parcours actuel, remplaçant ce qui se trouve sur le canevas.

Cela est utile pour sauvegarder un flux dont vous êtes fier, transmettre une série de bienvenue éprouvée à un autre magasin Spwig, ou reconstruire un parcours après avoir cloné votre magasin vers une nouvelle installation.

Comme pour les modèles, Spwig réinitialise les e-mails et les segments par nom lorsqu'il y a une correspondance sur le magasin cible, et signale tout élément qui ne peut pas être mis en correspondance afin que vous puissiez terminer la configuration.

## Activation de votre parcours

Lorsque le parcours est prêt, utilisez le contrôle de statut en haut à droite du constructeur. Une pastille affiche l'état actuel du parcours — **Brouillon**, **Actif** ou **En pause** — à côté d'un bouton **Activer**.

Cliquez sur **Activer** **vérifie d'abord le parcours**. Si quelque chose empêche son fonctionnement, l'activation est bloquée et une bannière liste les problèmes — par exemple, un étape **Envoyer un e-mail** sans e-mail sélectionné, une **Branche** sans segment ou sans chemin Oui/Non, un e-mail ou un segment supprimé depuis, ou une boucle qui tournerait indéfiniment. Chaque problème est cliquable : en le sélectionnant, vous accédez à l'étape concernée, qui est entourée de rouge jusqu'à ce que vous la corrigiez. Des avertissements (tels qu'une étape inatteignable ou une **Attente** sans délai défini) sont également listés, mais ils n'empêchent pas l'activation.

![Activation bloquée, avec le problème listé dans une bannière et l'étape défectueuse entourée de rouge](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Une fois que le parcours est opérationnel, la pastille passe à **Actif** et le parcours commence à inscrire les abonnés dès que son déclencheur s'active. Le bouton devient **En pause**, ce qui arrête les nouvelles inscriptions — les abonnés déjà en cours de parcours continuent de recevoir leurs étapes restantes. Consultez [Parcours déclenchés](/help/triggered-journeys) pour comprendre comment l'inscription, les périodes de repos et le statut interagissent.

## Voir qui est dans le parcours

Dès qu'un parcours est en ligne, chaque étape affiche un petit **badge de compteur** dans son coin : le nombre d'abonnés se trouvant actuellement à cette étape. C'est un moyen rapide de voir où les gens circulent et où ils s'accumulent — un grand nombre sur une étape **Attente** est normal, tandis qu'une accumulation juste avant un e-mail particulier pourrait mériter une vérification. Les comptes sont actualisés à chaque retour sur l'onglet du constructeur.

![Le canevas avec des badges de compteur actifs sur les étapes et le bouton Activer dans la barre d'outils](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Conseils

- Concevez le parcours pendant qu'il est encore **Brouillon** — personne n'est inscrit tant que vous **Activez** le parcours. Activer depuis le constructeur effectue d'abord une vérification rapide et n'autorise pas un parcours défectueux à être en ligne, donc il n'y a aucun risque qu'un parcours à moitié construit inscrive les abonnés.
- Commencez à partir d'un **Modèle** même si vous prévoyez de le personnaliser fortement — c'est plus rapide d'éditer un parcours existant que de le construire pas à pas, et cela démontre le schéma de branche si vous n'avez pas encore utilisé ce type de schéma.
- Après avoir appliqué un modèle ou importé un fichier, vérifiez l'en-tête pour un message indiquant des étapes non correspondantes et remplissez les étapes **Envoyer un e-mail** ou **Branche** qu'il ne peut pas faire correspondre avant d'activer.
- Cliquez sur **Ajuster** à chaque fois qu'un parcours devient trop large (les branches en particulier) — c'est le moyen le plus rapide de revoir la forme complète après un zoom ou un déplacement.
- Gardez les noms d'étapes faciles à repérer en plaçant chaque étape **Attente** immédiatement avant l'e-mail qu'elle reporte, plutôt que de regrouper plusieurs attentes ensemble.
- **Exporter** un parcours fonctionnel avant d'apporter des modifications importantes — c'est un moyen rapide de conserver une copie de secours que vous pouvez réimporter si vous n'êtes pas satisfait du résultat.