---
title: Attribution des revenus
---

L'attribution des revenus vous montre d'où vos ventes proviennent réellement, pas seulement du dernier lien cliqué par le client avant l'achat, mais de chaque canal qui a joué un rôle dans son arrivée. Si un client lit un article de blog que vous avez partagé sur les réseaux sociaux, puis revient une semaine plus tard via une recherche Google, puis finalement achète après avoir cliqué sur un lien dans une newsletter, ces trois touches ont toutes contribué à cette vente. Ce tableau de bord leur attribue toutes, en utilisant un modèle que vous choisissez, afin que vous puissiez voir votre marketing comme il fonctionne réellement, plutôt que comme le prétend "le dernier clic gagne".

![Le tableau de bord d'attribution des revenus : le sélecteur de modèle d'attribution, la bande de KPI avec le badge "Reconciles to net revenue", les revenus par canal, les revenus dans le temps, le parcours du client et le tableau des campagnes](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Où le trouver

Accédez à **Insights > Attribution des revenus** dans la barre latérale. Insights est un groupe de menu dédié au-dessus de Products, donc l'attribution des revenus a sa propre page, séparée de vos rapports sur les commandes et les clients.

Insights est protégé par la catégorie de permission **Insights & Analytics**. Si vous ne le voyez pas dans votre barre latérale, demandez à un administrateur de magasin de vous accorder cette permission - voir [Rôles et autorisations du personnel](/help/staff-roles) pour savoir comment gérer l'accès du personnel.

## Comprendre l'attribution multi-touches

La plupart des magasins s'habituent à penser en termes de "d'où vient cette commande ?" comme s'il n'y avait qu'une seule réponse. En réalité, les clients achètent rarement lors de leur première visite. Ils découvrent votre site de manière différente, reviennent d'une autre manière, et convertissent d'une troisième manière - parfois sur plusieurs visites réparties sur plusieurs jours ou semaines. Chacune de ces visites est une **touche** : une arrivée enregistrée sur votre site portant une information sur d'où elle vient (un lien de courriel, un résultat de recherche, un post de réseaux sociaux, un lien affilié, etc.).

**L'attribution multi-touches** signifie reconnaître chaque touche dans ce parcours et décider de la quantité de crédit que chaque touche mérite pour la vente finale, plutôt que de donner 100 % du crédit au canal qui a été cliqué en dernier. Cela est important car le rapport sur le dernier clic sous-évalue systématiquement les canaux qui effectuent le travail d'identification précoce - votre blog, votre présence organique dans les moteurs de recherche, vos publications sur les réseaux sociaux - car ils rarement être le dernier clic avant la caisse.

## Choix d'un modèle d'attribution

Le sélecteur de modèle en haut du tableau de bord en est le contrôle le plus important de la page. Cliquez sur n'importe quel modèle et chaque chiffre du tableau de bord - la bande de KPI, les barres de canal, le graphique, le tableau des campagnes - mettra instantanément à jour ses crédits pour correspondre. C'est une aperçu en direct : le changement de modèle ici modifie la manière dont vous regardez vos revenus existants, il ne réécrit pas les enregistrements ou ne change pas le modèle par défaut sauvegardé de votre magasin.

![Le sélecteur de modèle d'attribution - Dernière touche, Première touche, Linéaire, Décroissance temporelle et Position 40/20/40 - avec l'indicateur "Réattribue en direct · pas de traitement"](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | Ce qu'il fait | Idéal pour |
|-------|---------------|----------|
| **Dernière touche** | Accorde la pleine reconnaissance à la dernière canal avant la commande, en ignorant les contacts précédents (sauf les visites "directes" purement, qui sont ignorées en faveur de la dernière source réelle) | Une vue rapide et familière - comment la plupart des outils d'analyse basiques rapportent les revenus |
| **Première touche** | Accorde la pleine reconnaissance à n'importe quel canal qui a amené le client dans votre magasin | Comprendre ce qui motive la découverte des nouveaux clients et la croissance en haut du robinet |
| **Linéaire** | Répartit la reconnaissance de manière égale sur chaque touche du parcours | Une vue équilibrée, sans opinion, lorsque vous ne voulez pas favoriser un seul canal |
| **Décroissance temporelle** | Accorde plus de reconnaissance aux touches plus proches de la commande, moins aux touches plus anciennes | Des campagnes avec une fenêtre de prise de décision courte, où les rappels récents comptent le plus |
| **Position 40/20/40** | Accorde 40 % de reconnaissance à la première touche, 40 % à la dernière touche, et répartit les 20 % restants sur tout ce qui se situe entre | Reconnaître à la fois "qui nous a trouvés" et "qui a clos la vente", tout en créditant toujours le milieu du parcours |

Il n'y a pas de modèle "correct" unique — chacun répond à une question différente. Une approche courante consiste à vérifier **Première touche** pour voir ce qui motive la découverte, puis **Dernière touche** ou **Position 40/20/40** pour voir ce qui motive les conversions, et à utiliser les deux vues ensemble plutôt qu'à choisir l'une et d'ignorer les autres.

## Lire la bande de KPI

Juste en dessous du sélecteur de modèle, quatre chiffres résument la période sélectionnée et le modèle :

- **Revenus attribués** — le revenu total crédité à l'ensemble des canaux pour le modèle en cours. Il porte un badge **Reconciles à la recette nette** lorsquels les chiffres s'additionnent correctement à la recette nette réelle de votre magasin pour la période — en d'autres termes, le modèle partage la recette réelle entre les canaux, sans en inventer ou en perdre.
- **Commandes** — combien de commandes tombent dans la plage de dates sélectionnée.
- **Nombre moyen de touches par commande** — le nombre moyen de touches enregistrées par commande. Un chiffre supérieur à 1 confirme que la plupart des parcours de vos clients impliquent plus qu'une simple visite, c'est exactement pourquoi l'attribution multi-touche est importante pour votre magasin.
- **Canal principal** — le canal qui détient actuellement la plus grande part de revenus attribués selon le modèle sélectionné, avec son pourcentage de part et son revenu.

## Recette par canal

La carte **Recette par canal** affiche une barre horizontale pour chaque canal, dont la taille dépend de la recette attribuée. Changez le modèle d'attribution et regardez les barres se réorganiser progressivement par classement — c'est la même recette sous-jacente, mais répartie selon un ensemble différent de règles, donc un canal qui semble fort sous **Dernière touche** peut descendre de plusieurs rangs sous **Première touche** s'il joue principalement un rôle secondaire.

## Recette au fil du temps

Le graphique **Recette au fil du temps** empile la recette attribuée par canal sur chaque jour de la plage sélectionnée, afin que vous puissiez voir non seulement combien chaque canal vaut, mais aussi à quel moment il contribue. Utilisez-le pour repérer des modèles saisonniers, confirmer l'impact d'une campagne est tombé le jour que vous attendiez, ou vérifier si la contribution d'un canal croît ou diminue sur la période.

## Comment les clients arrivent réellement

Le panneau **Comment les clients arrivent réellement** est un schéma de flux de parcours reliant le canal qui a d'abord amené un client (à gauche) au canal présent lors de la conversion (à droite). Des rubans plus épais signifient plus de revenus qui passent par ce chemin. C'est le moyen le plus clair de voir des parcours à plusieurs étapes d'un coup — par exemple, un ruban épais d'Organic Search vers Email vous dit que la recherche apporte des gens, mais que votre marketing par courriel est ce qui les ramène acheter.

![Le schéma de flux du parcours client, avec la lentille "Influenced" sélectionnée, montrant les canaux de première touche à gauche qui coulent vers le canal sur lequel chaque commande s'est faite](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Utilisez le basculement **Attribué** / **Influencé** au-dessus du graphique pour changer de lentille :

- **Attribué** répartit chaque revenu de commande selon le modèle que vous avez sélectionné, de sorte que les totaux totalisent 100 % des revenus attribués — les mêmes chiffres affichés ailleurs sur le tableau de bord.
- **Influencé** attribue *chaque* canal ayant touché une commande avec la *valeur complète* de cette commande, compté une fois par commande.

Cela ne totalise pas délibérément à 100 % — un canal peut être « influencé » par des revenus qui sont également entièrement comptabilisés pour un autre canal.

Il existe pour mettre en évidence l'étendue d'un canal qui est cachée par le rapport de clic final, par exemple un article de blog ou un partage sur les réseaux sociaux qui ont intéressé quelqu'un, même s'il n'a pas cliqué dessus lors de sa visite finale.

## Campagnes

Le tableau **Campagnes** décompose les revenus, les commandes et la valeur moyenne des commandes (AOV) pour chacune de vos campagnes étiquetées — des liens ou codes que vous avez marqués d'un nom de campagne, y compris les codes de bons de réduction étiquetés par une campagne (voir [Idées de campagnes de bons](/help/voucher-campaign-ideas)). Utilisez-le pour comparer les performances de promotions individuelles, de codes d'influenceurs ou de campagnes marketing les unes par rapport aux autres, indépendamment du canal qui les a portées.

## Plage de dates et export de vos données

Utilisez le sélecteur de plage de dates en haut à droite pour passer entre **Derniers 7 jours**, **Derniers 14 jours**, **Derniers 30 jours**, **Derniers 90 jours** et **Mois à ce jour**. L'ensemble du tableau de bord se recharge pour la nouvelle période.

Cliquez sur **Exporter au format CSV** pour télécharger la répartition par canal pour le modèle et la plage de dates actuellement sélectionnés — utile pour importer des chiffres dans une feuille de calcul ou partager avec une agence partenaire.

## Comment les touches sont enregistrées

Spwig enregistre automatiquement une touche à chaque fois qu'un visiteur arrive sur votre magasin en portant une source reconnaissable, et uniquement lorsque le visiteur a donné la **permission d'analyse** dans le bannière de cookies de votre magasin (si vous ne faites pas fonctionner de bannière de consentement, le suivi est activé par défaut, conformément à la politique de votre magasin). Cela maintient l'attribution des revenus sur le même pied d'égalité en matière de confidentialité que le reste de l'analyse de votre site marchand.

Plusieurs sources sont automatiquement étiquetées, sans nécessiter de configuration :

| Canal | Comment il est identifié |
|---------|----------------------|
| **Email** | Liens dans vos courriels marketing (pas de courriels de commande ou d'expédition) |
| **Recherche organique / payante** | Référants des moteurs de recherche, ou des valeurs `utm_medium` indiquant une campagne de recherche payante |
| **Réseaux sociaux organiques / payants** | Référants des réseaux sociaux, ou des valeurs `utm_medium` sociales |
| **Partenariat** | Liens générés via votre programme de partenariat |
| **Inviter un ami** | Liens générés via votre programme de recommandation client |
| **Campagne** | Tout lien ou code portant une étiquette de campagne, y compris les codes de bons de réduction étiquetés par une campagne |
| **Lien externe** | Un lien entrant provenant d'un autre site web qui n'est pas autrement catégorisé |
| **Direct** | Aucun signal de source n'était présent — le visiteur a tapé l'adresse, a utilisé un signet, ou est arrivé depuis une application sans référant |

Les articles de blog qui ont été automatiquement partagés sur vos comptes de réseaux sociaux connectés sont automatiquement étiquetés, de sorte que le trafic qu'ils génèrent s'affiche sous le bon canal social plutôt que d'être perdu vers Direct ou Lien externe.

Vous pouvez également étiqueter vos propres liens manuellement en utilisant les paramètres standard `utm_source`, `utm_medium` et `utm_campaign` sur n'importe quelle URL menant à votre magasin — utile pour des matériaux imprimés, des newsletters de partenaires, ou tout canal que Spwig ne met pas automatiquement en évidence.

## Limites à garder à l'esprit

- **L'attribution suit un navigateur, pas une personne.** Si un client recherche sur son téléphone et achète sur son ordinateur portable, ce sont deux trajets distincts en ce qui concerne le suivi — il n'y a aucun moyen de relier les activités sur différents appareils.


Cela signifie que certaines ventes qui « devraient » être attribuées à un contact antérieur sur un autre appareil atterrissent sur Direct.
- **Direct est l endroit où les revenus non suivis atterrissent.** Une part élevée de Direct ne signifie pas nécessairement que les gens tapent votre URL en mémoire — cela peut également vouloir dire qu une touche antérieure d un client s est produite sur un autre appareil, ou qu un lien qu ils ont utilisé n était pas tagué.
- **Le refus de consentement signifie qu aucun contact n est enregistré.** Les visiteurs qui refusent le consentement pour les analyses dans votre bannière de cookies ne sont pas suivis, donc leurs commandes s affichent comme Direct même s ils sont arrivés par un canal que vous reconnaîtriez normalement.

## Conseils

- Vérifiez plus d un modèle avant de tirer des conclusions — un canal qui semble faible sous **Dernier contact** peut être votre principal moteur de découverte sous **Premier contact**.
- Si **Direct** représente une part importante de vos revenus, examinez si davantage de vos liens marketing pourraient être étiquetés avec `utm_source`/`utm_medium`/`utm_campaign` — le trafic non étiqueté n a nulle part où atterir.
- Utilisez la vue **Influencé** sur le graphique de parcours lorsque vous décidez si vous devez continuer à investir dans un canal comme la recherche organique ou le contenu de blog qui reçoit rarement le dernier clic mais qui commence constamment des parcours.
- Comparez la **Moyenne de contacts par commande** au fil du temps — un nombre croissant indique généralement que les clients prennent plus de temps pour décider, ce qui est un signal utile lors de la planification des emails de suivi ou du retargeting.
- Exportez le fichier CSV pour le modèle et la période sur lesquels vous effectuez votre rapport avant de changer à nouveau de modèle, car l exportation reflète celui qui est sélectionné à l instant où vous cliquez sur **Exporter en CSV**.