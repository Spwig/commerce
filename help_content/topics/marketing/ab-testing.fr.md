---
title: Test A/B
---

La fonction **test A/B** de Campaign Studio vous permet d'essayer deux à quatre **variantes** — différentes versions de la même campagne — sur une partie de votre audience avant de procéder à l'envoi complet. Ne modifiez que le sujet, ou créez entièrement du contenu différent pour chaque variante. Spwig divise un échantillon de votre liste de manière égale entre les variantes, surveille les performances de chacune et envoie automatiquement la variante la plus performante à l'ensemble des personnes n'ayant pas participé au test.

## Configuration d'un test

Créez d'abord votre campagne normalement dans le constructeur visuel de Campaign Studio — rédigez un sujet, concevez votre contenu et sélectionnez le **segment** que vous souhaitez atteindre. Cette campagne devient alors le **conteneur** du test. Une fois que vous y attachez un test A/B, le conteneur n'est jamais envoyé directement : son rôle est de contenir les paramètres, et l'audience ciblée est exactement celle sur laquelle le test s'exécute.

Deux endroits ouvrent la boîte de dialogue du test A/B :

- Le bouton **Test A/B** dans la barre d'outils du constructeur visuel.
- L'icône **Test A/B** sur la carte de la campagne dans **Campaign Studio > Campagnes**.

Une fois qu'un test existe sur une campagne, ce même bouton vous amène directement aux résultats du test plutôt qu'au guide, et la carte de la campagne reçoit un petit **A/B** pour que vous puissiez la repérer facilement dans la liste.

## Quoi tester

L'étape suivante du guide demande ce qui doit différer entre les variantes :

| Option | Qu'est-ce qui change | Mesuré par |
|--------|---------------------|-------------|
| **Sujet** | Chaque variante envoie exactement le même contenu — seul le sujet diffère. Le test le plus courant. | Taux d'ouverture |
| **Contenu** | Chaque variante est une conception différente que vous créez vous-même dans le constructeur visuel. | Taux de clic |

![Étape "Qu'est-ce que vous voulez tester ?", avec le sujet sélectionné](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Choix de vos variantes

Ce que vous entrez ensuite dépend de ce que vous avez choisi :

- **Sujet** — tapez un sujet pour chaque variante (2 à 4). Deux lignes sont affichées au départ ; cliquez sur **Ajouter un autre sujet** pour une troisième ou quatrième variante.
- **Contenu** — sélectionnez simplement le nombre de variantes souhaité (2 à 4). Chaque variante commence comme une copie exacte de la conception actuelle du conteneur, donc vous n'avez qu'à modifier ce que vous testez.

Dans les deux cas, Spwig étiquette les variantes **A**, **B**, **C** et **D** dans l_ordre d'entrée — vous les verrez comme "Variante A", "Variante B", etc., à partir de là.

![Étape des variantes avec trois sujets entrés pour les variantes A, B et C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Pour un test de contenu, vous ne concevez pas les variantes dans la boîte de dialogue elle-même — après avoir créé le test, chaque carte de variante sur le tableau de bord des résultats dispose d'une petite icône de crayon qui l'ouvre dans le même constructeur visuel que celui utilisé pour le conteneur. Cela n'est disponible que tant que le test est toujours en **Brouillon** ; une fois que vous lancez le test, les conceptions sont verrouillées afin que ce que vous mesurez ne change pas pendant le test.

## Paramètres du test

La dernière étape du guide traite de la manière dont le test est exécuté et décidé :

| Paramètre | Ce que cela fait |
|---------|--------------|
| **Échantillon de test** | La part de votre audience utilisée pour le test, divisée équitablement entre les variantes : 20 %, 30 %, 50 % ou 100 %. Le reste — le **groupe témoin** — reçoit le gagnant par la suite. En choisissant 100 %, vous testez l'ensemble de votre liste en même temps, donc il n'y a plus de groupe témoin pour envoyer le gagnant. |
| **Décision du gagnant par** | **Taux d'ouverture** ou **Taux de clic**. Par défaut, le taux d'ouverture pour un test de sujet et le taux de clic pour un test de contenu, puisque ce sont les mesures réelles de chaque test — mais vous pouvez les changer.
| **Période de test (heures)** | Durée pendant laquelle les ouvertures et les clics sont recueillis avant de choisir un gagnant, de 1 à 168 heures (une semaine entière). |
| **Envoi automatique du gagnant à l'ensemble de l'audience** | Activé par défaut. Lorsqu'il est coché, Spwig envoie la variante gagnante au groupe témoin dès la fin de la période, sans action supplémentaire de votre part. |

Une carte de révision courte en bas résume vos choix avant que vous ne confirmiez.

![Étape Paramètres avec les options échantillon, métrique, fenêtre et envoi automatique configurées, ainsi qu'une carte de récapitulatif](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Démarrage du test

Cliquez sur **Créer le test** pour enregistrer la configuration — cela n'envoie encore rien. Vous arrivez sur le centre de résultats du test avec le statut **Brouillon**, affichant chaque variante avec zéro destinataire pour l'instant et deux boutons : **Démarrer le test** et **Annuler le test**.

![Un test nouvellement créé avec le statut Brouillon, affichant trois variantes prêtes à démarrer](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Cliquez sur **Démarrer le test** lorsque vous êtes prêt. Spwig répartit votre échantillon de test également entre les variantes et envoie un e-mail à chacune immédiatement — vous n'avez rien d'autre à faire ; une tâche en arrière-plan vérifie une fois la fenêtre du test écoulée et décide du gagnant tout seul. Le statut de la campagne conteneur reste **Brouillon** tout au long de ce processus — c'est normal, car ce sont les variantes (et plus tard le gagnant) qui sont réellement envoyées, jamais le conteneur.

Votre audience doit être suffisamment grande pour que chaque variante reçoive un nombre significatif de destinataires. Spwig bloque le démarrage d'un test si une variante se retrouverait avec zéro personne, mais un test réellement exploitable nécessite plus qu'un minimum absolu — visez quelques centaines de destinataires ou plus avant de vous fier au résultat.

## Pendant le test

Une fois démarré, le centre bascule en **Test en cours** et affiche « Test en cours — le gagnant est déterminé automatiquement autour de » la date et l'heure de fin de la fenêtre. Les nombres de destinataires et les taux d'ouverture/clic en direct se mettent à jour à chaque visite, accompagnés d'un graphique en barres comparant le taux d'ouverture et le taux de clic de chaque variante côte à côte — pas seulement la métrique que vous avez choisie pour déterminer le gagnant.

![Un test en cours affichant les nombres de destinataires en direct, les taux d'ouverture/clic et un graphique de comparaison](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Vous pouvez également surveiller chaque test depuis le **tableau de bord du Studio de campagnes** : son panneau *Tests A/B récents* liste vos tests en cours et récemment décidés — chacun avec son niveau de confiance en un coup d'œil — et renvoie directement vers les résultats, aux côtés de cartes comptant le nombre de tests en cours et le nombre de tests décidés au cours des 30 derniers jours.

## Lecture des résultats

Lorsque la fenêtre du test se termine, Spwig choisit la variante avec le taux le plus élevé sur votre métrique choisie, marque le test **Terminé** et — si **Envoyer automatiquement le gagnant** était coché et qu'il y a un groupe témoin à qui envoyer — envoie cette variante à tous ceux qui n'ont pas fait partie du test. La carte de la variante gagnante est mise en évidence et porte un badge **Gagnant** ; le graphique de comparaison reste en place pour que vous puissiez voir comment les variantes se sont comparées.

![Un test terminé avec la variante gagnante mise en évidence et un badge Gagnant](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Gardez à l'esprit que les chiffres sur cette page sont toujours pour l'échantillon de test, pas pour toute votre liste — avec un échantillon de 20 %, vous lisez comment un cinquième de votre audience a réagi, pas tout le monde.

## Quelle est la fiabilité du résultat ?

Un taux d'ouverture ou de clic plus élevé ne signifie pas toujours qu'une variante est réellement meilleure — avec une petite audience, une variante peut prendre la tête purement par hasard. C'est pourquoi, aux côtés du gagnant, Spwig affiche **à quel point il est confiant que le résultat est réel**, basé sur la taille de l'écart et le nombre de destinataires. Vous verrez l'une des trois lectures suivantes :

- **Un résultat clair** — Spwig est au moins à 95 % confiant que la variante en tête bat réellement les autres. C'est un résultat sur lequel vous pouvez agir.
- **Trop serré pour trancher** — il y a un leader, mais l'écart est suffisamment petit pour qu'il puisse s'agir d'un hasard. Le pourcentage affiché indique le niveau de confiance de Spwig, en dessous du seuil de 95 %. Envisagez de relancer avec une audience plus grande ou une fenêtre de test plus longue avant de tirer des conclusions.
- **Pas encore assez de données** — trop peu de destinataires (ou trop peu d'ouvertures et de clics) pour distinguer les variantes. C'est courant sur les petites listes ; agrandissez l'audience ou laissez le test se dérouler plus longtemps.

![Test terminé affichant un résultat clair — la variante gagnante porte un badge de confiance et le résumé indique « statistiquement clair »](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

Le même affichage apparaît pendant qu'un test est encore en cours, ce qui vous permet de voir un résultat se préciser — ou non — avant la fermeture de la fenêtre. Étant donné que la confiance dépend fortement de la taille de l'audience, c'est la raison pratique pour viser plusieurs centaines de destinataires ou plus par test : sur une liste très petite, même une différence apparemment importante sera généralement lue comme « trop serré pour trancher ».

Notez que lorsque l'envoi automatique est activé, Spwig envoie toujours la variante au taux le plus élevé au reste de votre audience, même si le résultat est inconclusif — l'indicateur de confiance sert à vous dire dans quelle mesure vous pouvez faire confiance au résultat, et non à retarder l'envoi.

## Annuler un test

**Annuler le test** est disponible pendant qu'un test est en **Brouillon** ou **En test**, et l'arrête sans jamais envoyer de gagnant. Il est prévu pour les cas où vous avez changé d'avis ou commis une erreur dans la configuration — ce n'est pas une action à prendre à la légère, car une fois un test annulé (ou terminé normalement), il n'y a pas de bouton pour en configurer un nouveau sur cette même campagne. Si vous souhaitez effectuer une autre comparaison plus tard, créez une nouvelle campagne à cet effet.

## Conseils

- Commencez par un test de **Ligne d'objet** — c'est le plus simple à configurer et la raison la plus courante de faire un test A/B.
- Utilisez un test de **Contenu** lorsque vous souhaitez comparer des designs ou des offres réellement différents, et pas seulement le libellé de l'objet.
- Terminez la conception de chaque variante d'un test de contenu — en utilisant l'icône crayon sur chaque carte — avant de cliquer sur **Démarrer le test**. Vous ne pouvez pas modifier le design d'une variante une fois le test en cours.
- Laissez **Échantillon de test** en dessous de 100 % si vous souhaitez que Spwig envoie automatiquement le gagnant au reste de votre liste par la suite — à 100 %, il ne reste aucun groupe témoin pour y parvenir.
- Donnez à la fenêtre de test suffisamment de temps pour couvrir les habitudes de lecture normales de vos abonnés (24 heures couvrent confortablement une journée complète de fuseaux horaires et de boîtes de réception) plutôt que de désigner un gagnant sur la base des premières heures seulement.