---
title: Services hébergés Spwig
---

Spwig inclut trois services cloud optionnels que votre boutique peut utiliser sans avoir à les configurer ou les héberger vous-même : **GeoIP** détecte l'emplacement de vos visiteurs, **Geocoder** convertit les adresses des clients en coordonnées de carte, et **Push** envoie des notifications instantanées à votre application mobile Spwig admin. Dans l'édition Communauté (gratuite), chaque service vient avec une limite mensuelle généreuse. Lorsque l'un des services approche sa limite, Spwig vous alerte dans l'admin afin que vous puissiez décider s'il faut effectuer une mise à niveau avant que vos clients ne remarquent quoi que ce soit.

## Les trois services hébergés

### GeoIP — détection du pays du visiteur

GeoIP recherche le pays de chaque visiteur en se basant sur son adresse IP. Votre boutique utilise cette information pour afficher automatiquement la bonne devise lorsqu'un client arrive, et pour remplir automatiquement le champ pays lors du paiement. Par exemple, un visiteur allemand verra les prix en euros, et un visiteur japonais verra les prix en yens — sans avoir à choisir manuellement.

Chaque chargement de page où GeoIP effectue une recherche compte pour votre quota mensuel. Les visites répétées depuis la même session de navigateur ne consomment pas chacune une recherche ; le résultat est mis en cache pour la session. Les recherches GeoIP ne se produisent qu'à l'interface de vente, pas dans votre panneau d'administration.

### Geocoder — adresse aux coordonnées

Geocoder convertit les adresses tapées par les clients en coordonnées géographiques (latitude et longitude). Votre boutique utilise ces coordonnées à deux fins : calculer les coûts d'expédition basés sur la distance lorsqu'il y a des points de retrait ou des règles d'expédition basées sur un rayon, et alimenter les suggestions d'autocomplétion d'adresses sur la page de paiement afin que les clients puissent trouver leur adresse rapidement.

Une recherche Geocoder est déclenchée lorsque le client sélectionne ou confirme une adresse lors du paiement. Comme GeoIP, les résultats sont mis en cache afin qu'une même adresse ne soit recherchée qu'une seule fois par session.

### Push — notifications de l'application admin

Push envoie des notifications en temps réel à votre application mobile Spwig merchant. Lorsqu'une nouvelle commande arrive, lorsqu'il y a un manque de stock en dessous d'un seuil, ou lorsque le client envoie un message, Push envoie une notification instantanée à votre appareil afin que vous puissiez y répondre sans avoir à garder le panneau d'administration ouvert.

Chaque notification envoyée à votre appareil compte comme une demande de push contre votre quota mensuel.

## Le niveau gratuit Communauté

Dans l'édition Communauté de Spwig, chaque service est inclus sans coût jusqu'à une limite mensuelle de requêtes. Les limites exactes sont définies par Spwig et peuvent varier ; votre tableau de bord admin affiche toujours les chiffres actuels pour votre installation. Les plans payants (Débutant, Croissance, Pro, Pro Plus) et les installations auto-hébergées avec un licence payante ont des limites plus élevées pour chaque service.

Lorsqu'un service atteint 100 % de sa limite Communauté, les requêtes vers ce service s'arrêtent jusqu'au mois suivant, qui réinitialise le compteur. L'impact sur votre boutique dépend du service concerné :

| Service | Ce qui se produit à 100 % |
|---------|----------------------|
| GeoIP | La détection automatique de la devise revient à la devise par défaut de votre boutique. Les clients peuvent toujours changer manuellement de devise. |
| Geocoder | L'autocomplétion d'adresses cesse de proposer des suggestions. Les clients peuvent toujours taper manuellement leur adresse. Le calcul des tarifs d'expédition continue d'utiliser les coordonnées connues précédemment. |
| Push | Les nouvelles notifications de l'application admin sont mises en file d'attente mais ne sont pas envoyées jusqu'au mois suivant ou une mise à niveau. |

Votre boutique continue à fonctionner normalement dans tous les cas — aucune commande n'est perdue et les clients peuvent toujours effectuer un achat. Les effets sont limités aux fonctionnalités de commodité.

## Lire le tile du tableau de bord

Le tile **Utilisation des services Spwig** apparaît sur la page d'accueil de votre tableau de bord admin. Il affiche une barre de progression pour chacun des trois services.

Chaque ligne du tile suit le même layout :

- **Nom du service** (à gauche) — GeoIP, Recherche d'adresse (Geocoder), ou Notifications Push.
- **Barre de progression** (au centre) — s'emplie de gauche à droite à mesure que l'utilisation augmente.

La couleur de la barre change à mesure que les limites approchent :
  - **Vert** — l'utilisation est inférieure à 80 %.

Tout fonctionne normalement.
  - **Amber** — l'utilisation est comprise entre 80 % et 99 %.

Le service fonctionne toujours mais se rapproche de la limite.
  - **Rouge** — l'utilisation a atteint 100 %.

Le service est maintenant limité pour ce mois.
- **Compteur d'utilisation** (à droite) — le nombre exact de requêtes utilisées sur le total autorisé, par exemple `3 241 / 10 000`.

L'étiquette entre parenthèses indique la fenêtre de temps, généralement `(ce mois)`.

Si le tile ne peut pas atteindre le serveur de mise à jour Spwig pour récupérer votre utilisation actuelle (par exemple, si votre serveur n'a pas d'accès Internet sortant), la colonne des compteurs affiche un tiret (`—`) pour ce service. Cela ne signifie pas que le service est cassé ; cela signifie simplement que l'affichage de l'utilisation est temporairement indisponible.

### Le bouton **Mettre à niveau**

Lorsque tout service atteint 80 % ou plus, un bouton **Mettre à niveau** apparaît dans le coin supérieur droit du tile. En cliquant dessus, cela ouvre la page de mise à niveau Spwig où vous pouvez comparer les plans et augmenter vos limites de service. Le bouton disparaît une fois que l'utilisation redescend en dessous de 80 % au début du mois suivant.

## Le bandeau d'avertissement de quota

En plus du tile du tableau de bord, un bandeau apparaît en haut de chaque page d'administration lorsque tout service dépasse le seuil de 80 %. Ce bandeau n'apparaît que sur les installations Communautaires.

**Bandeau Amber — proche de la limite (80–99 %)**

> **Proche de la limite des services hébergés :** L'un de vos services Spwig dépasse les 80 % de la limite de votre plan Communautaire. Mettez à niveau pour augmenter la limite avant qu'elle ne soit atteinte.

Ce bandeau est un avertissement précoce. Vos services continuent de fonctionner, et vous avez le temps de décider si vous souhaitez mettre à niveau avant la fin du mois.

**Bandeau Rouge — limite atteinte (100 %)**

> **Limite des services Spwig atteinte :** L'un de vos services hébergés a atteint la limite de votre plan Communautaire. Mettez à niveau pour les faire fonctionner sans interruption.

Ce bandeau apparaît lorsque tout service a atteint 100 % et est maintenant limité. En cliquant sur **Mettre à niveau** sur l'un ou l'autre des bandeaux, cela ouvre la même page de mise à niveau que le bouton du tile.

Le bandeau disparaît automatiquement au début du mois calendaire suivant lorsque les compteurs sont réinitialisés, ou immédiatement après que vous avez mis à niveau vers un plan payant.

## Avertissement par e-mail à 90 %

Lorsque tout service dépasse 90 % de sa limite, Spwig envoie également un avertissement par e-mail unique à l'adresse configurée dans les paramètres de votre magasin (**Paramètres > Paramètres du magasin > Contact > E-mail administrateur**). L'e-mail est envoyé au maximum une fois par service par mois calendaire, donc vous ne serez pas inondé de messages. Aucun e-mail n'est envoyé à 100 % car à ce moment-là, le bandeau dans l'administration rend déjà la situation claire.

Si vous ne recevez pas l'e-mail, vérifiez que l'adresse e-mail administrateur est correctement configurée sous **Paramètres > Paramètres du magasin**.

## Mise à niveau de votre plan

Lorsque vous mettez à niveau du plan Communautaire à tout plan payant, les limites supérieures prennent effet immédiatement — aucune redémarrage du magasin ou modification de configuration n'est nécessaire. Le tile du tableau de bord affichera la nouvelle limite plus élevée la prochaine fois qu'il se rafraîchira (dans les cinq minutes).

Pour mettre à niveau, cliquez sur le bouton **Mettre à niveau** sur le tile du tableau de bord ou le bandeau de quota, ou visitez directement la page de mise à niveau Spwig. Les plans payants incluent les mêmes trois services hébergés (GeoIP, Geocoder, Push) avec des limites mensuelles augmentées, ainsi qu'un accès à la livraison d'e-mails hébergée par Spwig et un support prioritaire.

## Hébergement autonome et licences Pro

Si vous utilisez une installation Spwig auto-hébergée avec une licence payante, votre niveau de licence détermine vos limites de service, de la même manière que le plan hébergé équivalent. Votre magasin a toujours besoin d'un accès Internet sortant pour atteindre `updates.spwig.com` afin que la plateforme puisse récupérer et vérifier votre configuration de niveau. Les compteurs d'utilisation affichés dans le tile du tableau de bord sont extraits des points de terminaison des services hébergés à `geoip.spwig.com`, `geocoder.spwig.com` et `push.spwig.com`.

Il n'y a actuellement aucune option pour remplacer GeoIP, Geocoder ou Push par des alternatives auto-hébergées — ces services sont fournis exclusivement par l'infrastructure Spwig et sont inclus dans toutes les éditions.

## Conseils

Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Vérifiez régulièrement le carreau à la fin des mois chargés** — un événement de vente ou une promotion peut augmenter significativement les requêtes GeoIP et Geocoder.

Le carreau vous prévient à l'avance, avant que les clients ne soient affectés.
- **Le recours à la devise par défaut est invisible pour la plupart des clients** — si GeoIP atteint sa limite, les clients verront la devise par défaut de votre magasin.

Cela n'est rarement un problème sérieux pour les magasins qui servent principalement un seul marché ; cela importe davantage pour les magasins véritablement internationaux.
- **L'autocomplétion des adresses est un confort, pas un obstacle** — lorsque Geocoder est limité, les clients peuvent toujours taper et soumettre leur adresse normalement.

Si vous organisez fréquemment des promotions qui génèrent un trafic de paiement élevé, envisagez de passer à un niveau supérieur avant les périodes chargées.
- **Le ralentissement des notifications ne perd pas les notifications de manière permanente** — les notifications en attente de la période de ralentissement ne sont pas envoyées en arrière lors du réinitialisation du mois ou après une mise à niveau.

Si vous dépendez fortement des notifications push pour des alertes de commandes à caractère temporel, passer à un niveau supérieur avant d'atteindre la limite vous assure de ne rien manquer.
- **Le cache de 5 minutes signifie que le carreau n'est pas parfaitement en temps réel** — les statistiques d'utilisation sont rafraîchies approximativement toutes les cinq minutes en arrière-plan.

Pendant des périodes de trafic inhabituellement élevé, l'utilisation réelle peut être légèrement supérieure à ce que montre le carreau.
- **Définissez votre adresse e-mail d'administration** — le courriel d'avertissement à 90 % ne fonctionne que si **Paramètres > Paramètres du magasin > E-mail d'administration** est renseigné.

Il est utile de vérifier que cela est correctement configuré afin de recevoir l'avertissement avant que les problèmes ne surviennent.