---
title: Publics
---

Un **Segment** est un public enregistré que vous pouvez cibler avec une campagne, un parcours ou un test A/B — la liste des segments de Studio de campagne appelle cela « publics ciblés », et ce guide utilise les deux termes pour la même chose. Chaque segment est soit **dynamique**, défini par des règles que Spwig réévalue à chaque utilisation, soit **statique**, une liste explicite de souscripteurs que vous choisissez manuellement.

Ce guide traite de la création des règles d'un segment dynamique — y compris les nouveaux champs qui ciblent vos propres tranches de valeur client, votre programme de fidélité et vos partenaires affiliés — et le bouton **Ajouter des publics de base** qui crée un ensemble de segments prêts à l'emploi à partir des données dont votre magasin dispose déjà.

## Segments dynamiques vs. statiques

| Type | Comment ça fonctionne | Idéal pour |
|---|---|---|
| **Dynamique (règles)** | Vous définissez des conditions — par exemple, « Total dépensé est d'au moins 500 $ ». Spwig recalcule qui correspond à chaque fois que le segment est utilisé, donc l'appartenance change automatiquement au fur et à mesure que vos souscripteurs évoluent. | Des publics en continu qui doivent toujours être à jour, comme « clients VIP » ou « n'a pas commandé depuis 90 jours ».
| **Statique (liste fixe)** | Une liste explicite de souscripteurs que vous ajoutez ou supprimez manuellement. L'appartenance ne change jamais à moins que vous ne la modifiiez. | Une liste unique — tous provenant d'un événement spécifique, ou un groupe sélectionné manuellement pour un envoi unique. |

Choisissez le type avec le champ **Type** lorsque vous créez un segment. Le reste de ce guide concerne les segments dynamiques — les segments statiques ne sont qu'une liste de membres sans règles à configurer.

## Création d'un segment dynamique

Ouvrez **Studio de campagne > Segments**, puis cliquez sur **+ Nouveau segment** (ou ouvrez un segment dynamique existant) pour accéder au **Constructeur de règles de public**. Cliquez sur **+ Ajouter une condition** pour ajouter une règle, choisissez ce à vérifier et comment, puis définissez si un souscripteur doit correspondre à **toutes** ou à **n'importe laquelle** de vos conditions. Un compteur en temps réel en haut à droite — par exemple, « 8 souscripteurs correspondants » — s'actualise quelques instants après chaque modification, afin que vous puissiez voir exactement qui convient avant de sauvegarder.

![Le constructeur de règles de public avec les critères de segment client, niveau de fidélité, valeur de vie, et partenaire affilié définis, et un compteur de souscripteurs correspondants en temps réel](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Une condition avec une vérification de type **est vrai** — **A commandé**, **A opté pour la publicité**, **Membre de fidélité**, **Partenaire affilié** — n'a besoin que de sélectionner le champ lui-même ; il n'y a pas d'opérateur ou de valeur à définir.

## Ce que vous pouvez cibler

| Champ | Ce qu'il vérifie |
|---|---|
| **Dépense totale** | Total des commandes sur la durée. |
| **Nombre de commandes** | Nombre d'achats effectués. |
| **Valeur de vie** | Valeur de vie calculée du client. |
| **Valeur moyenne des commandes** | Montant moyen par commande effectuée. |
| **Jours depuis la dernière commande** | Le temps écoulé depuis la dernière commande du client — ciblez 90 jours ou plus pour un public de retour. |
| **A commandé** | Si le client a au moins une commande effectuée. |
| **A opté pour la publicité** | Si le souscripteur a consenti à recevoir des courriels de marketing. |
| **Langue** | La langue stockée du souscripteur. |
| **Source** | Comment le souscripteur s'est-il inscrit — inscription sur le site, import, commande, ajout manuel ou API. |
| **S'inscrit après** | Les souscripteurs qui se sont inscrits à partir d'une date choisie. |
| **A une étiquette** | Si le souscripteur possède une [étiquette](/help/subscriber-tags) que vous avez créée. |
| **Segment client** | Si le client appartient à l'une des [segments clients](/help/customer-segments) nommés de votre magasin — Client invité, Nouveau client, Client régulier, Acheteur fréquent, Client à haute valeur, Client VIP, Chasseur de bonnes affaires, Client à risque, ou Inactif. |
| **Membre de fidélité** | Si le client est un membre actif de votre programme de fidélité. |
| **Points de fidélité** | Solde de points disponibles actuel du membre. |
| **Niveau de fidélité** | Quel niveau de fidélité le membre occupe-t-il actuellement. |
| **Partenaire affilié** | Si le client est l'un de vos partenaires affiliés actifs. |

**Segment client**, les deux champs de valeur **Fidélité**, **Niveau de fidélité**, et **Partenaire affilié** sont des ajouts récents, et n'apparaissent chacun que dans le sélecteur de conditions une fois que votre magasin possède effectivement ce type de données : les champs de fidélité apparaissent une fois que votre programme de fidélité a des membres et au moins un niveau actif, **Partenaire affilié** apparaît une fois que vous avez au moins un partenaire affilié, et **Segment client** apparaît une fois que vous avez au moins un segment client actif configuré.

Vous ne verrez pas d'option sur un magasin frais qui ne pourrait pas correspondre à quelqu'un.

Une limite actuelle à connaître : pour toute condition avec une liste déroulante de choix — **Langue**, **Source**, **Avec un mot-clé**, **Segment client**, **Niveau de fidélité** — l'opérateur **est l'un de** ne vous permet toujours que de sélectionner une seule valeur à la fois. Si vous souhaitez correspondre à plusieurs (par exemple, les clients situés dans le segment VIP ou le segment à haut valeur), ajoutez une condition par valeur et définissez **Match** sur **n'importe lequel**.

## Ajouter des segments de base

Créer une règle à partir de zéro pour chaque public évident — vos VIP, vos membres de fidélité, tout le monde qui est devenu silencieux — est fastidieux lorsque Spwig peut déjà voir qui est éligible. Sur la liste des Segments, cliquez sur **Ajouter des segments de base** et Spwig crée un ensemble de segments dynamiques prêts à l'emploi à partir des données clients, de fidélité et d'affiliation que votre magasin possède déjà.

![La liste des Segments avec les boutons Nouveau segment et Ajouter des segments de base](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Segments de base | Cibles | Besoins |
|---|---|---|
| **Clients VIP** | Votre segment de clients VIP | Un segment de clients VIP actif |
| **Clients à haut valeur** | Vos segments de clients VIP et de clients à haut valeur | Un segment de clients VIP ou à haut valeur actif |
| **Clients fidèles** | Vos segments de clients fréquents et réguliers | Un segment de clients fréquents ou réguliers actif |
| **Nouveaux clients** | Votre segment de nouveaux clients | Un segment de nouveaux clients actif |
| **Clients qui ont déserté** | Les clients ayant commandé avant mais pas au cours des 90 derniers jours | Une historique de commande client |
| **Membres de fidélité** | Tous les participants actifs de votre programme de fidélité | Un programme de fidélité actif avec des membres |
| **Niveau de fidélité le plus élevé** | Les membres de votre niveau de fidélité le plus élevé | Au moins un niveau de fidélité actif |
| **Partenaires affiliés** | Vos partenaires affiliés actifs | Au moins un partenaire affilié |

Spwig n'utilise que les segments de base pour lesquels il dispose effectivement de données : un magasin sans programme de fidélité n'obtiendra pas de segment **Membres de fidélité**, mais plutôt un vide qui ne pourrait jamais correspondre à quelqu'un. Spwig confirme exactement ce qu'il a ajouté, par exemple : « Ajouté 7 segments de base : clients à haut valeur, clients fidèles, nouveaux clients, clients qui ont déserté, membres de fidélité, niveau de fidélité le plus élevé, partenaires affiliés ».

![Message de succès confirmant quels segments de base viennent d'être ajoutés](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

Il est sécurisé de cliquer sur **Ajouter des segments de base** plus d'une fois. Spwig ne crée jamais de doublon d'un segment de base qui existe déjà, donc cliquer à nouveau après avoir configuré (par exemple) votre programme de fidélité n'ajoute que ce qui est désormais disponible — si tout est déjà configuré, il le dit simplement.

![Message d'information montrant que tous les segments de base existent déjà](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Si vous supprimez un segment de base que vous ne voulez pas, cliquer à nouveau sur **Ajouter des segments de base** ne le fera pas revenir — Spwig le traite comme un segment que vous avez supprimé intentionnellement, et non un à recréer.

Une fois créé, un segment de base est un segment dynamique ordinaire : ouvrez-le depuis la liste pour le revérifier ou le modifier, le renommer ou le supprimer, exactement comme vous le feriez pour n'importe quel segment que vous avez créé vous-même.

## Qui ces segments atteignent réellement

Les conditions clients, fidélité et partenaire ci-dessus ne correspondent qu'aux abonnés dont l'e-mail est lié à un compte client - une inscription à la newsletter anonyme ne correspondra pas à une condition **membre fidèle** ou **VIP**, même correctement, car Spwig n'a pas d'historique de commande ou de fidélité à vérifier.

Si beaucoup de vos clients possèdent un compte mais n'ont pas encore souscrit, demandez à celui qui gère votre installation Spwig de lancer une synchronisation des abonnés - cela crée un enregistrement d'abonné pour chaque compte client existant en une seule étape, afin que ces publics aient des personnes réelles à comparer.

Quel que soit le nombre d'abonnés d'un segment, ce nombre décrit qui *pourrait* recevoir une campagne, et non pas qui le fera. Chaque envoi vérifie d'abord la volonté marketing de chaque abonné, donc un segment n'est jamais un moyen d'y échapper.

## Conseils

- Commencez par un public de base et ajustez-le plutôt que de tout créer à la main - une fois créé, un public de base n'est pas différent d'un segment que vous avez vous-même construit.
- Les conditions booléennes comme **membre fidèle**, **partenaire** et **a commandé** n'ont pas besoin d'opérateur ou de valeur - ajoutez simplement la condition et c'est terminé.
- Combiner les nouveaux champs avec les anciens pour une ciblage plus précis, par exemple **membre fidèle** plus **a opté pour le marketing**, plutôt que de s'appuyer uniquement sur une seule condition.
- Si les règles d'un segment font référence à quelque chose qui a depuis été supprimé - un segment client supprimé, une étiquette vidée, etc. - Spwig le traite comme correspondant à personne plutôt que de revenir à l'ensemble de votre liste d'abonnés. Une ciblage défaillant envoie moins de personnes ; il ne diffuse jamais par accident l'ensemble.
- Si le nombre de membres d'un segment semble obsolète, ouvrez-le et enregistrez-le à nouveau, ou utilisez l'action de masse **Reconstruire les nombres de membres** depuis la liste des Segments, pour le recalculer immédiatement.
- Regardez le compteur en temps réel "abonnés correspondants" pendant que vous créez une règle - c'est le moyen le plus rapide de repérer une condition qui est plus étroite (ou plus large) que prévu avant de l'enregistrer.