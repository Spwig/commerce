---
title: Guide de livraison des courriels
---

Obtenir un courriel *envoyé* est facile. L'obtention d'un courriel dans la boîte de réception au lieu du dossier spam est le vrai travail - et les fournisseurs de boîtes de réception comme Gmail et Yahoo appliquent désormais des exigences techniques strictes avant de considérer même un courriel. Ce guide explique ce qu'il faut configurer, dans quel ordre, afin que vos confirmations de commande et campagnes atterrissent là où les clients peuvent les voir.

Rien ici n'est une tâche unique. La livrabilité est un statut que vous construisez au fil du temps et que vous pouvez perdre rapidement - la liste de vérification à la fin mérite d'être révisée chaque fois que quelque chose semble défectueux.

## Pourquoi c'est important

Chaque fournisseur de boîte de réception important évalue les courriels entrants sur la réputation de l'expéditeur avant de décider s'ils doivent les livrer, les plier dans un dossier spam ou les rejeter directement. Depuis 2024, Gmail et Yahoo ont formalisé cela en exigences explicites **pour les expéditeurs en vrac** pour quiconque envoie un volume significatif :

- **Authentifiez votre domaine** - des enregistrements SPF, DKIM et DMARC valides.
- **Rendez-le facile à se désabonner** - un moyen de désactivation fonctionnel, peu encombrant, dans chaque courriel marketing.
- **Maintenez les plaintes pour spam faibles** - les expéditeurs en vrac qui dépassent environ 0,3 % de plaintes risquent d'avoir leurs courriels rejetés ou placés dans un dossier de masse ; le meilleur objectif est bien en dessous de 0,1 %.

Échouer à ces exigences n'affecte pas seulement les campagnes marketing - une réputation de domaine endommagée peut entraîner des courriels transactionnels (confirmations de commande, réinitialisations de mot de passe) dans le spam également, car Gmail et Yahoo jugent de plus en plus la réputation au niveau du domaine d'expédition, et non seulement par type de message. Les étapes ci-dessous sont comment vous répondez à ces trois.

## Étape 1 : Authentifier votre domaine d'expédition

SPF, DKIM et DMARC sont des enregistrements TXT DNS qui prouvent aux serveurs de messagerie réceveurs que le courriel prétendant provenir de votre domaine a bien été envoyé par vous. Comment vous les configurez dépend du mode d'expédition que votre magasin utilise - les trois sont configurés sous **Configuration e-mail** dans la barre latérale de l'administrateur (cela ouvre la liste des comptes e-mail ; voir [Configuration e-mail](email-configuration) pour la procédure complète de configuration du compte).

| Mode d'expédition | Comment l'authentification fonctionne |
|---|---|
| **SMTP intégré** (le serveur e-mail de Spwig lui-même) | Spwig génère un couple de clés DKIM pour votre domaine automatiquement. Ajoutez un compte e-mail, et **étape 4** de la procédure de configuration affiche l'état SPF, DKIM et DMARC ainsi que l'enregistrement exact à ajouter, avec un bouton de copie dans le presse-papier et des instructions spécifiques au fournisseur pour Cloudflare, GoDaddy, Namecheap et AWS Route 53. Le même enregistrement DKIM DNS est également affiché sur la page admin du compte ultérieurement, sous **Clés DKIM configurées**, si vous avez besoin de le retrouver plus tard. |
| **SMTP générique** (un fournisseur que vous apportez vous-même comme SendGrid, Mailgun, Amazon SES ou Google Workspace, connecté via des identifiens SMTP) | L'authentification se fait partiellement dans le tableau de bord de ce fournisseur lui-même. L'étape DNS de la procédure de configuration inclut des instructions à onglets pour Gmail, Outlook, SendGrid, Mailgun et Amazon SES spécifiquement - chacune explique ce qu'il faut configurer dans la console du fournisseur (par exemple, vérifier un domaine d'expédition dans SendGrid) et quels enregistrements DNS ajouter à votre hébergeur DNS. |
| **Passerelle e-mail hébergée par Spwig** | Disponible sur les forfaits hébergés par Spwig en tant qu'option d'expédition gérée. Elle signe les courriels sortants avec DKIM automatiquement et définit par défaut l'envoi à partir d'une adresse sur le domaine vérifié de Spwig lui-même, donc cela fonctionne avec zéro configuration. Si vous souhaitez envoyer à partir de votre propre domaine via la passerelle, parlez à votre hébergeur pour vérifier qu'il est configuré - c'est un service géré, pas un flux DNS autonome.

![Étape 4 de la procédure de configuration du compte e-mail, montrant la validation SPF/DKIM/DMARC, les onglets de fournisseur DNS et un enregistrement DKIM étendu prêt à copier](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Un panneau de clés DKIM configurées d'un compte e-mail SMTP intégré existant, avec l'enregistrement TXT DNS et un bouton Copier l'enregistrement DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Quel que soit le mode utilisé, **l'ajout de l'enregistrement DNS lui-même est toujours une étape externe** — vous le faites chez votre registrar de domaine ou votre hébergeur DNS (Cloudflare, GoDaddy, Namecheap, Route 53, ou là où pointent les serveurs de noms de votre domaine), et non à l'intérieur de Spwig.

Spwig peut vous indiquer exactement quoi ajouter et valider qu'il est en ligne, mais il ne peut pas accéder à votre registrar pour l'ajouter à votre place.

Quelques points importants à connaître avant de commencer :

- **Les modifications DNS ne sont pas instantanées.** La propagation peut prendre de quelques minutes à 48 heures. L'étape de validation de l'assistant affichera l'enregistrement comme en échec ou manquant tant qu'il n'a pas réellement propagé — c'est normal, ce n'est pas un signe que quelque chose ne va pas.
- **Un seul enregistrement SPF est autorisé par domaine.** Si vous en avez déjà un (depuis Google Workspace, un autre service de messagerie, etc.), ajoutez votre nouvel expéditeur à l'enregistrement existant avec `include:` plutôt que de créer un second enregistrement TXT SPF — deux enregistrements SPF casseront l'authentification pour tout le monde.
- **DMARC nécessite que SPF ou DKIM soit déjà validé.** Configurez-le en dernier, une fois que SPF et DKIM sont tous deux vérifiés.

## Étape 2 : Utiliser une identité d'envoi réelle

Une fois votre domaine authentifié, assurez-vous que ce que les destinataires voient réellement le soutient :

- **Adresse d'expéditeur** — utilisez une adresse sur votre propre domaine authentifié (`orders@yourstore.com`), jamais une adresse d'un fournisseur gratuit (`yourstore@gmail.com`). Une adresse d'expéditeur d'un fournisseur gratuit ne peut tout simplement pas être authentifiée par vos enregistrements SPF/DKIM/DMARC, et les fournisseurs de boîte de réception la traitent comme un fort signal de spam provenant d'une boutique.
- **Nom d'expéditeur** — utilisez le nom reconnaissable de votre boutique, et non une étiquette générique comme "Notifications" ou "Sans réponse".
- **Répondre à** — définissez une adresse surveillée. Une adresse `noreply@` non surveillée qui rebondit ou qui supprime silencieusement les réponses est en elle-même un léger signal de réputation, et elle bloque le seul canal que les clients ont pour vous signaler qu'il y a eu un problème.

Définissez les trois sous **Configuration des e-mails > (votre compte) > Configuration de l'expéditeur** — voir [Configuration des e-mails](email-configuration) pour le guide complet des champs.

## Étape 3 : Échauffez avant de passer à l'échelle

Un domaine ou une IP sans historique d'envoi n'a pas encore de réputation — bonne ou mauvaise — et les fournisseurs de boîte de réception sont prudents avec l'inconnu. Envoyer une première vague massive depuis un tout nouveau domaine ressemble statistiquement à un spammeur qui lance une nouvelle campagne, et cela peut se retrouver dans le dossier de courrier indésirable même si toutes les cases techniques sont cochées.

- Commencez petit. Envoyez vos premières campagnes à votre audience la plus engagée, la plus susceptible d'ouvrir, plutôt qu'à votre liste entière d'un coup — voir [Audiences](audiences) pour créer un segment de démarrage ciblé.
- Augmentez le volume progressivement au cours des premières semaines plutôt que de passer directement aux envois sur la liste complète.
- Si vous migrez une liste existante depuis une autre plateforme, considérez-la comme le premier jour pour les besoins de réputation également — l'historique d'envoi de votre ancienne plateforme ne se transfère pas avec le domaine.

## Étape 4 : Gardez votre liste propre

Chaque réclamation ou rebond vous coûte en réputation, et les deux sont largement fonction de qui est sur votre liste et de la manière dont ils y sont arrivés :

- **N'envoyez des e-mails qu'à des personnes qui ont consenti.** Les contacts importés, les listes achetées et les adresses collectées sont le moyen le plus rapide de faire exploser les réclamations de spam et les rebonds durs.
- **Utilisez la double confirmation d'inscription.** Le flux de consentement marketing de Spwig vérifie l'adresse e-mail d'un abonné avant de lui envoyer des e-mails marketing — voir [Préférences de communication](communication-preferences) pour voir comment cela est configuré.
- **Laissez la suppression automatique de Spwig faire son travail.** Spwig surveille les rebonds durs, les réclamations de spam et les rebonds doux répétés et cesse d'envoyer des e-mails à ces adresses automatiquement, sans configuration requise — voir [Hygiène de liste et suppressions](list-hygiene) pour voir exactement comment cela fonctionne et quand (rarement) le contourner.
- **Éliminez périodiquement les abonnés inactifs** plutôt que d'envoyer des e-mails indéfiniment aux mêmes adresses non engagées — une liste qui diminue mais qui ouvre et clique vaut plus pour votre réputation qu'une grande liste qui ne le fait pas.

## Étape 5 : Surveiller

Les problèmes de délivrabilité apparaissent dans les statistiques avant même qu'un client ne vous signale qu'un e-mail n'est pas arrivé.

Ouvrez le [Rapport](campaign-reports) d'une campagne après chaque envoi et surveillez :

| Indicateur | Points de vigilance |
|---|---|
| **Taux de rebond** | La prédominance des rebonds doux est normale ; une part croissante de **rebonds durs** signifie que votre liste accumule des adresses obsolètes ou invalides. |
| **Signalements de spam** | Devrait rester proche de zéro à chaque envoi. Maintenez-le bien en dessous du seuil d'environ 0,3 % qui déclenche les mesures d'application pour les expéditeurs en volume chez Gmail et Yahoo — considérez même une petite hausse comme nécessitant une investigation immédiate. |
| **Taux d'ouverture / taux de clics par ouverture** | Une baisse soudaine et inexpliquée entre les envois vers la même liste (et non pour une seule campagne) peut être un signe précoce que les e-mails atterrissent dans les spams plutôt que dans la boîte de réception, et ce avant même que les chiffres de rebond ou de signalements ne bougent. |

Vérifiez également périodiquement la carte **Adresses supprimées** du tableau de bord de Campaign Studio — un flux constant est une usure normale de la liste, mais une hausse soudaine mérite d'être investiguée avant votre prochain envoi (voir [Hygiène de liste](list-hygiene)).

![La carte de statistiques des adresses supprimées sur le tableau de bord de Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Si quelque chose augmente brusquement : mettez en pause et vérifiez d'abord que vos enregistrements DNS sont toujours valides (un renouvellement de domaine expiré ou une modification accidentnelle du DNS peut casser silencieusement SPF/DKIM), puis examinez ce qui a changé dans le contenu ou l'audience de l'envoi qui a déclenché le problème.

## Étape 6 : Hygiène du contenu

L'authentification et la qualité de la liste vous ouvrent la porte ; le contenu influence toujours la façon dont vous êtes traité une fois à l'intérieur.

- **Évitez les motifs déclencheurs de spam** dans les objets — MAJUSCULES, ponctuation excessive (« !!! ») et des phrases comme « agissez maintenant » ou « argent gratuit » pèsent encore contre vous auprès des filtres anti-spam, même depuis un domaine authentifié.
- **N'envoyez pas d'e-mails contenant uniquement des images.** Un e-mail qui n'est qu'une seule image sans texte réel est un motif de spam classique ; conservez une quantité significative de contenu textuel réel aux côtés des images.
- **Aperçu avant envoi.** Vérifiez comment l'e-mail s'affiche réellement — y compris sur mobile — avant qu'il ne soit envoyé à votre liste complète.
- **Le lien de désinscription est déjà géré.** Spwig ajoute automatiquement un lien de désinscription fonctionnel, sans connexion requise, au pied de chaque e-mail marketing — vous n'avez pas besoin d'en ajouter un vous-même (voir [Préférences de communication](communication-preferences) pour savoir exactement comment ce flux fonctionne). Ne le supprimez pas et ne le masquez pas ; un lien de désinscription manquant ou cassé constitue en soi une violation des règles des expéditeurs en volume de Gmail et Yahoo, quel que soit vos autres indicateurs.

## « Mes e-mails vont dans les spams » — liste de contrôle de dépannage

Parcourez ces étapes dans l'ordre :

1. **Revérifiez vos enregistrements DNS.** Ouvrez l'étape DNS de l'assistant de configuration du compte (ou le panneau DKIM sur la page d'administration du compte pour le SMTP intégré) et confirmez que SPF, DKIM et DMARC sont toujours valides.

Un renouvellement de domaine, une migration de fournisseur DNS ou une modification non liée à votre fichier de zone peut casser silencieusement l'un de ces éléments.
2. **Vérifiez les chiffres de rebond et de signalements du rapport de campagne** pour les envois concernés — voir [Rapports de campagne](campaign-reports).


Une augmentation de l'un ou l'autre indique un problème de qualité de la liste ou de contenu plutôt qu'un problème d'authentification.
3. **Vérifiez la liste des suppressions** ([Hygiène de la liste](list-hygiene)) pour détecter une hausse soudaine — si une grande partie de votre liste échoue depuis un certain temps, la délivrabilité vers le reste se dégrade également.
4. **Confirmez que votre adresse d'expéditeur est sur votre domaine authentifié**, et non une adresse de fournisseur gratuit ou un domaine qui ne correspond pas à celui pour lequel SPF/DKIM/DMARC ont été configurés.
5. **Envoyez un e-mail de test à une adresse Gmail et à une adresse Yahoo/Outlook que vous contrôlez** et vérifiez le dossier réel dans lequel il atterrit, pas seulement s'il est arrivé.
6. **Si vous avez récemment modifié brutalement le volume d'envoi ou l'audience,** traitez-le comme une nouvelle phase de mise en route — réduisez le volume et augmentez-le plus progressivement.
7. **Si tout ce qui précède est correct et que le problème persiste,** il peut s'agir d'une limitation spécifique au fournisseur plutôt que d'un défaut dans votre configuration — cela peut prendre un certain temps à se résoudre de lui-même une fois la cause sous-jacente (généralement les plaintes ou les rebonds) corrigée.

## Conseils

- Corrigez l'authentification DNS avant toute autre chose — tous les autres leviers de délivrabilité (contenu, hygiène de la liste, mise en route) comptent moins si SPF/DKIM/DMARC ne passent pas.
- Considérez la validation DNS de l'assistant de configuration comme une vérification ponctuelle, et non comme une opération unique — relancez-la chaque fois que vous migrez de fournisseur DNS ou renouvelez un domaine auprès d'un registraire différent.
- Une liste propre qui ouvre et clique surpassera toujours une liste plus grande qui ne le fait pas — résistez à l'envie d'importer une liste ancienne et non vérifiée « au cas où ».
- Surveillez vos chiffres par rapport à vos propres envois passés, et non à un benchmark sectoriel générique — votre propre historique est le signal le plus fiable d'un problème réel.
- Si vous êtes sur un plan hébergé par Spwig, la signature DKIM et la gestion de la réputation de la passerelle e-mail hébergée sont gérées pour vous — votre responsabilité restante est la qualité de la liste et le contenu, et non le DNS.