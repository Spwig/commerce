---
title: Étiquettes des abonnés
---

Les étiquettes sont vos propres étiquettes pour organiser votre audience Studio de campagnes — des repères courts comme `VIP`, `grossiste` ou `événement-2026` que vous définissez et que vous appliquez à n'importe quel abonné qui convient. Une fois qu'une étiquette existe, vous pouvez filtrer votre liste d'abonnés par celle-ci, lui appliquer ou la supprimer à partir de n'importe quel nombre de personnes en même temps, et — le plus utilement — l'utiliser comme condition lors de la création d'un segment, afin que vos campagnes et parcours ciblent exactement les personnes que vous avez étiquetées.

## Qu'est-ce qu'une étiquette

Une étiquette n'est rien de plus qu'un nom que vous choisissez. Spwig ne dispose d'aucune étiquette prédéfinie, et il ne lui applique jamais automatiquement — vous décidez de leur nom et de qui en a. Cela convient bien à tout ce qui est spécifique à votre propre entreprise et qui ne correspond pas à un statut que Spwig suit déjà : un niveau de fidélité, un compte de gros, l'ensemble des personnes s'étant inscrites à un salon professionnel, ou une liste d'événement unique comme `événement-2026`.

Chaque étiquette reçoit également un **Slug** — une version simplifiée, compatible URL de son nom — généré automatiquement lorsque vous la créez. Les segments et les filtres utilisent le slug en interne ; en tant que commerçant, vous n'aurez presque jamais besoin de le regarder.

## Création d'une étiquette

Les étiquettes ont leur propre section d'administration. Ouvrez **Studio de campagne > Abonnés**, puis cliquez sur **Studio de campagne** en haut de la page pour voir la liste complète des sections de Studio de campagne, et choisissez **Étiquettes des abonnés**.

1. Cliquez sur **Ajouter une étiquette d'abonné**.
2. Entrez un **Nom** — un nom court et précis est le plus lisible, par exemple `VIP`, `Gros` ou `Événement 2026`.
3. Spwig remplit un **Slug** correspondant pendant que vous tapez. Vous pouvez le laisser tel quel.
4. Un champ **Couleur** optionnel est également disponible si vous souhaitez enregistrer une couleur hexadécimale (par exemple `#2563eb`) associée à l'étiquette pour votre propre référence.
5. Cliquez sur **Enregistrer**.

Vous n'avez pas besoin de quitter ce que vous êtes en train de faire pour en créer une non plus — un **+** vert à côté du champ **Étiquettes** sur la page d'édition d'un abonné ouvre le même formulaire "ajouter une étiquette" dans une fenêtre contextuelle. Et si vous essayez de marquer plusieurs abonnés avant d'avoir créé des étiquettes du tout, le sélecteur d'étiquettes propose un raccourci **Créer une étiquette** qui vous y amène directement.

## Attribution d'étiquettes aux abonnés

La façon la plus courante d'appliquer une étiquette est en vrac, depuis la liste des abonnés :

1. Ouvrez **Studio de campagne > Abonnés**.
2. Cochez la case de chaque abonné que vous souhaitez étiqueter (ou **Sélectionner tous sur cette page**).
3. Dans le menu déroulant **Actions en vrac**, choisissez **Ajouter une étiquette aux sélections…** (ou **Supprimer une étiquette des sélections…** pour désétiqueter des personnes).
4. Cliquez sur **Exécuter**.
5. Choisissez l'étiquette dans la liste et cliquez sur **Ajouter une étiquette** (ou **Supprimer une étiquette**).

![Le sélecteur d'étiquettes en vrac après avoir choisi "Ajouter une étiquette aux sélections" pour quatre abonnés](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Une fois appliquée, une étiquette s'affiche sous forme de petit élément sur la carte de l'abonné dans la liste, à côté de leurs badges de statut et de source. Un filtre **Étiquette** apparaît également dans le panneau de filtre de la liste des abonnés une fois que vous avez au moins une étiquette, afin que vous puissiez réduire la liste à tous ceux qui portent une étiquette spécifique — pratique pour vérifier qui est dans une audience avant de créer une campagne autour.

![La liste des abonnés filtrée sur l'étiquette VIP, avec le bouton Importer CSV et les puces d'étiquettes visibles](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Vous pouvez également ajouter ou supprimer les étiquettes d'un seul abonné directement depuis leur propre page d'édition, en utilisant le même champ **Étiquettes** que gère l'action en vrac.

## Utilisation des étiquettes dans les segments

Les segments sont les audiences basées sur des règles que vous pointez vers vos campagnes et parcours. Une fois que vous avez créé au moins une étiquette, une condition **A une étiquette** devient disponible dans le constructeur de règles de segment — elle n'apparaît pas sur une installation fraîche sans étiquette définie, donc vous ne verrez pas d'option inutile avant qu'elle ne soit utile pour vous.

Pour l'utiliser, ouvrez **Studio de campagne > Segments**, ajoutez (ou modifiez) un segment dynamique, puis cliquez sur **+ Ajouter une condition** : 

1. Définissez le champ de la condition sur **A une étiquette**.
2. Choisissez un opérateur — **est** pour une seule étiquette, ou **est l'une des** lorsqu'on veut l'exprimer ainsi.
3. Choisissez l'étiquette dans le menu déroulant.

![Une condition « A un tag » définie sur VIP, affichant un comptage en direct des abonnés correspondants](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

Le comptage en haut à droite se met à jour à mesure que vous construisez la règle, ce qui vous permet de voir exactement combien d'abonnés sont actuellement éligibles avant d'enregistrer. Chaque condition **A un tag** correspond actuellement à un tag à la fois — si vous souhaitez une audience qui correspond à *n'importe lequel* de plusieurs tags (par exemple, `VIP` ou `Wholesale`), ajoutez une condition **A un tag** par tag et définissez **Correspondance** sur **n'importe lequel**.

C'est ce qui rend les tags utiles au-delà de l'organisation : un segment construit sur **A un tag** devient une audience que vous pouvez sélectionner en tant que **Segment** sur une diffusion ou une campagne récurrente, ou en tant que paramètre **Uniquement pour le segment** d'un parcours — ainsi, « tout le monde tagué VIP » peut avoir sa propre série de bienvenue, son propre bulletin récurrent, ou simplement être celui que vous sélectionnez la prochaine fois que vous envoyez une annonce ponctuelle.

## Conseils

- Gardez les noms de tags courts et spécifiques — ils s'affichent sous forme de puces compactes sur les cartes d'abonnés, donc `VIP` se lit mieux que `Very Important Person - Tier 1`.
- Utilisez le filtre **Tag** pour vérifier qui est réellement tagué avant de construire un segment ou d'envoyer une campagne à ce sujet.
- Le tagage est additif — la suppression d'un tag d'un abonné n'affecte jamais aucun autre tag qu'il possède, et ne touche jamais à son statut, sa source ou son consentement.
- Combinez les tags avec d'autres conditions du constructeur de règles (comme **A opté pour le marketing** ou **Total dépensé**) sur le même segment pour une audience plus précise, pas seulement un tag à lui seul.
- Un abonné peut porter autant de tags que vous le souhaitez — il n'y a pas de limite, donc il est tout à fait acceptable de les utiliser à plusieurs fins superposées (un niveau de fidélité *et* une liste d'événements *et* une note de source).
- Si un tag cesse d'être utile, sa suppression depuis **Tags d'abonnés** le retire de tous les abonnés auxquels il était appliqué et de toutes les règles de segment qui y faisaient référence — les segments l'utilisant cesseront simplement de correspondre à cette condition.