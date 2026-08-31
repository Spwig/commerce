---
title: Guide d'exploitation de la délivrabilité des e-mails
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Envoyer un e-mail est facile. Le faire arriver dans la boîte de réception plutôt que dans le dossier de spam est le vrai défi — et les fournisseurs de messagerie comme Gmail et Yahoo imposent désormais des exigences techniques strictes avant même de le prendre en considération. Ce guide d'exploitation détaille ce qu'il faut configurer, dans quel ordre, pour que vos confirmations de commande et vos campagnes arrivent là où vos clients peuvent les voir.

Rien ici n'est une tâche à faire une seule fois. La délivrabilité est une réputation que vous construisez au fil du temps et qui peut se perdre rapidement — la liste de contrôle en fin de document mérite d'être réexaminée chaque fois que quelque chose semble anormal.

## Pourquoi c'est important

Chaque grand fournisseur de boîte de réception évalue les e-mails entrants sur la base de la réputation de l'expéditeur avant de décider de les livrer, de les classer dans le dossier de spam ou de les rejeter purement et simplement. Depuis 2024, Gmail et Yahoo ont formalisé cela en **exigences pour les expéditeurs en volume** pour quiconque envoie un volume significatif :

- **Authentifiez votre domaine** — enregistrements SPF, DKIM et DMARC valides.
- **Facilitez le désabonnement** — un mécanisme de désinscription fonctionnel et sans friction dans chaque e-mail marketing.
- **Gardez le taux de signalement de spam bas** — les expéditeurs en volume qui dépassent environ 0,3 % de plaintes risquent d'avoir leurs e-mails rejetés ou classés en masse dans le dossier de spam ; l'objectif le plus sûr est bien en dessous de 0,1 %.

En cas d'échec, ce ne sont pas seulement les campagnes marketing qui en souffrent — une réputation de domaine endommagée peut entraîner les e-mails transactionnels (confirmations de commande, réinitialisations de mot de passe) dans le spam également, car Gmail et Yahoo évaluent de plus en plus la réputation au niveau du domaine d'envoi, et non seulement par type de message. Les étapes ci-dessous sont la manière de répondre aux trois exigences.

## Étape 1 : Authentifiez votre domaine d'envoi

SPF, DKIM et DMARC sont des enregistrements TXT DNS qui prouvent aux serveurs de messagerie destinataires que les e-mails prétendant provenir de votre domaine ont réellement été envoyés par vous. La manière de les configurer dépend du mode d'envoi utilisé par votre boutique — les trois sont configurés sous **Configuration des e-mails** dans la barre latérale d'administration (cela ouvre la liste des comptes e-mail ; voir [Configuration des e-mails](email-configuration) pour le guide complet de configuration des comptes).

| Mode d'envoi | Fonctionnement de l'authentification |
|---|---|
| **SMTP intégré** (serveur de messagerie propre à Spwig) | Spwig génère automatiquement une paire de clés DKIM pour votre domaine. Ajoutez un compte e-mail, et l'**étape 4** de l'assistant de configuration affiche votre statut SPF, DKIM et DMARC, ainsi que l'enregistrement exact à ajouter, avec une option de copie dans le presse-papiers et des instructions spécifiques aux fournisseurs Cloudflare, GoDaddy, Namecheap et AWS Route 53. Le même enregistrement DNS DKIM est également affiché sur la page d'administration du compte, sous **Clés DKIM configurées**, si vous avez besoin de le retrouver. |
| **SMTP générique** (un fournisseur apporté par vous-même, comme SendGrid, Mailgun, Amazon SES ou Google Workspace, connecté via des identifiants SMTP) | L'authentification se fait en partie dans le tableau de bord de ce fournisseur. L'étape DNS de l'assistant de configuration inclut des instructions en onglets spécifiquement pour Gmail, Outlook, SendGrid, Mailgun et Amazon SES — chacune explique quoi configurer dans la console du fournisseur (par exemple, la vérification d'un domaine d'envoi dans SendGrid) et quels enregistrements DNS résultants ajouter chez votre hébergeur DNS. |
| **Passerelle de messagerie hébergée par Spwig** | Disponible sur les plans hébergés par Spwig en tant qu'option d'envoi gérée. Elle signe automatiquement les e-mails sortants avec DKIM et envoie par défaut depuis une adresse sur le domaine vérifié de Spwig, ce qui fonctionne sans aucune configuration. Si vous souhaitez envoyer depuis votre propre domaine via la passerelle, parlez-en à votre fournisseur d'hébergement pour le faire vérifier — il s'agit d'un service géré, et non d'un flux DNS en libre-service. |

Quel que soit le mode utilisé, **l'ajout de l'enregistrement DNS lui-même est toujours une étape externe** — vous le faites chez votre registrar de domaine ou votre hébergeur DNS (Cloudflare, GoDaddy, Namecheap, Route 53, ou là où pointent les serveurs de noms de votre domaine), et non à l'intérieur de Spwig. Spwig peut vous dire exactement quoi ajouter et valider qu'il est actif, mais il ne peut pas accéder à votre registrar pour l'ajouter à votre place.

Quelques points à connaître avant de commencer :

- **Les modifications DNS ne sont pas instantanées.** La propagation peut prendre de quelques minutes à 48 heures. L'étape de validation de l'assistant affichera un enregistrement comme échoué ou manquant jusqu'à ce qu'il ait réellement propagé — c'est normal, ce n'est pas un signe que quelque chose ne va pas.
- **Un seul enregistrement SPF est autorisé par domaine.** Si vous en avez déjà un (depuis Google Workspace, un autre outil de messagerie, etc.), ajoutez votre nouvel expéditeur à l'enregistrement existant avec `include:` plutôt que de créer un second enregistrement TXT SPF — deux enregistrements SPF casseront l'authentification pour tout le monde.
- **DMARC nécessite que SPF ou DKIM soit déjà validé.** Configurez-le en dernier, une fois que SPF et DKIM sont tous deux vérifiés.

## Étape 2 : Utiliser une identité d'envoi réelle

Une fois votre domaine authentifié, assurez-vous que ce que les destinataires voient réellement le soutient :

- **Adresse d'expéditeur** — utilisez une adresse sur votre propre domaine authentifié (`orders@yourstore.com`), jamais une adresse de fournisseur gratuit (`yourstore@gmail.com`). Une adresse d'expéditeur de fournisseur gratuit ne peut tout simplement pas être authentifiée par vos enregistrements SPF/DKIM/DMARC, et les fournisseurs de boîte de réception la traitent comme un fort signal de spam provenant d'une boutique.
- **Nom d'expéditeur** — utilisez le nom reconnaissable de votre boutique, et non un libellé générique comme "Notifications" ou "No Reply".
- **Répondre à** — définissez une adresse surveillée. Une adresse `noreply@` non surveillée qui rebondit ou qui supprime silencieusement les réponses est en elle-même un léger signal de réputation, et elle bloque le seul canal que les clients ont pour vous dire que quelque chose s'est mal passé.

Définissez les trois sous **Configuration e-mail > (votre compte) > Configuration de l'expéditeur** — voir [Configuration e-mail](email-configuration) pour le parcours complet des champs.

## Étape 3 : Faire chauffer avant de passer à l'échelle

Un domaine ou une IP sans historique d'envoi n'a pas encore de réputation — bonne ou mauvaise — et les fournisseurs de boîte de réception sont prudents avec l'inconnu. Envoyer une première vague massive depuis un tout nouveau domaine ressemble statistiquement à un spammeur qui lance une nouvelle campagne, et cela peut être classé dans le dossier de courrier indésirable même si toutes les cases techniques sont cochées.

- Commencez plus petit.

Envoyez vos premières campagnes à votre audience la plus impliquée et la plus susceptible d'ouvrir vos courriels, plutôt qu'à l'ensemble de votre liste d'un coup — consultez [Publics] (publics) pour créer un segment ciblé initial.
- Augmentez progressivement le volume au cours des premières semaines plutôt que de passer directement à l'envoi à l'ensemble de la liste.
- Si vous migrez une liste existante depuis un autre service, considérez cela comme le jour 1 pour des raisons de réputation également — l'historique d'envoi de votre ancien service ne transfère pas avec le domaine.

## Étape 4 : Maintenez votre liste propre

Chaque réclamation ou échec d'envoi coûte de la réputation, et les deux sont principalement fonction de qui se trouve sur votre liste et de la manière dont ils y sont parvenus :

- **Ne faites par parvenir de courriels qu'aux personnes ayant donné leur accord.** Les contacts importés, les listes achetées et les adresses récupérées de manière non autorisée sont le moyen le plus rapide d'augmenter les réclamations de spam et les échecs permanents.
- **Utilisez une inscription double.** Le processus de consentement marketing de Spwig vérifie l'adresse e-mail d'un abonné avant d'envoyer un courriel marketing — consultez [Préférences de communication] (préférences-de-communication) pour savoir comment cela est configuré.
- **Laissez le processus automatique de suppression de Spwig faire son travail.** Spwig surveille les échecs permanents, les réclamations de spam et les échecs temporaires répétés et arrête automatiquement l'envoi à ces adresses, sans configuration nécessaire — consultez [Hygiène de la liste et suppressions] (hygiène-de-liste) pour comprendre exactement comment cela fonctionne et quand (rarement) le contourner.
- **Supprimez régulièrement les abonnés inactifs** plutôt que d'envoyer indéfiniment à des adresses non impliquées — une liste qui se réduit mais qui s'ouvre et clique vaut plus pour votre réputation qu'une grande liste qui ne le fait pas.

## Étape 5 : Surveiller

Les problèmes de livrabilité apparaissent dans les chiffres avant qu'un client ne vous dise qu'un courriel n'est pas arrivé.

Ouvrez le [Rapport] (rapports-de-campagne) d'une campagne après chaque envoi et surveillez :

| Indicateur | À surveiller |
|---|---|
| **Taux d'échec** | Un taux majoritairement d'échecs temporaires est normal ; une part croissante d'**échec permanent** signifie que votre liste contient des adresses obsolètes ou invalides qui s'accumulent. |
| **Réclamations de spam** | Devrait être proche de zéro pour chaque envoi. Gardez-le bien en dessous de la limite d'environ 0,3 % qui déclenche l'application des règles pour les expéditeurs en vrac chez Gmail et Yahoo — traitez même une petite augmentation comme valant la peine d'être investiguée immédiatement. |
| **Taux d'ouverture / taux de clics** | Une baisse soudaine et non expliquée sur les envois à la même liste (pas seulement une campagne) peut être un signe précoce que les courriels atterrissent dans le spam plutôt que dans la boîte de réception, même avant que les chiffres d'échec ou de réclamation ne bougent. |

Vérifiez également la carte **Adresses supprimées** du tableau de bord du Studio de Campagne périodiquement — un flux constant est une dégradation normale de la liste, mais une augmentation soudaine vaut la peine d'être investiguée avant votre prochain envoi (voir [Hygiène de la liste] (hygiène-de-liste)).

Si quelque chose augmente : arrêtez et vérifiez d'abord que vos enregistrements DNS sont toujours valides (une annulation de renouvellement de domaine ou un changement DNS accidentel peut briser silencieusement SPF/DKIM), puis regardez ce qui a changé concernant le contenu ou le public de l'envoi qui l'a déclenché.

## Étape 6 : Hygiène du contenu

L'authentification et la qualité de la liste vous ouvrent la porte ; le contenu affecte toujours comment vous êtes traité une fois que vous y êtes.

- **Évitez les modèles déclencheurs de spam** dans les sujets — tout en majuscules, une ponctuation excessive ("!!!"), et des phrases comme "agissez maintenant" ou "argent gratuit" pèsent toujours contre vous avec les filtres de spam, même depuis un domaine authentifié.
- **Ne faites pas parvenir d'e-mails ne comportant qu'une image.** Un courriel n'ayant qu'une seule image sans texte réel est un modèle classique de spam ; gardez une quantité significative de contenu textuel réel à côté de toute image.
- **Prévisualisez avant d'envoyer.** Vérifiez comment le courriel s'affiche réellement — y compris sur mobile — avant qu'il ne soit envoyé à l'ensemble de votre liste.
- **Le lien de désabonnement est déjà géré.** Spwig ajoute automatiquement un lien de désabonnement fonctionnel, sans nécessiter de connexion, au pied de chaque courriel marketing — vous n'avez pas besoin d'ajouter le vôtre (voir [Préférences de communication] (préférences-de-communication) pour savoir exactement comment ce processus fonctionne). Ne le supprimez pas ou ne le cachez pas ; un lien de désabonnement manquant ou cassé constitue à lui seul une violation de politique avec les règles d'expéditeur en vrac de Gmail et Yahoo, indépendamment de vos autres chiffres.

Conservez toutes les formattages markdown, les chemins d'images, les blocs de code et les termes techniques.

## « Mes e-mails vont dans les courriers indésirables » — liste de contrôle de dépannage

Suivez ces étapes dans l'ordre :

1. **Vérifiez à nouveau vos enregistrements DNS.** Ouvrez l'étape DNS de l'assistant de configuration du compte (ou le panneau DKIM sur la page d'administration du compte pour le SMTP intégré) et confirmez que SPF, DKIM et DMARC passent toujours. Un renouvellement de domaine, une migration de fournisseur DNS ou une modification non liée à votre fichier de zone peut casser l'un de ces éléments sans avertissement.
2. **Vérifiez les nombres de rebonds et de plaintes dans le rapport de campagne** pour les envois concernés — voir [Rapports de campagne](campaign-reports). Une augmentation de l'un ou l'autre indique un problème de qualité de liste ou de contenu plutôt qu'un problème d'authentification.
3. **Vérifiez la liste des suppressions** ([Hygiène de liste](list-hygiene)) pour une augmentation soudaine — si une grande partie de votre liste échoue depuis un certain temps, la délivrabilité vers le reste se dégrade également.
4. **Confirmez que votre adresse Expéditeur est sur votre domaine authentifié**, et non sur une adresse de fournisseur gratuit ou un domaine qui ne correspond pas à celui pour lequel SPF/DKIM/DMARC ont été configurés.
5. **Envoyez un e-mail de test à une adresse Gmail et à une adresse Yahoo/Outlook que vous contrôlez** et vérifiez le dossier réel dans lequel il atterrit, et pas seulement s'il est arrivé.
6. **Si vous avez récemment modifié brutalement le volume d'envoi ou l'audience,** traitez-le comme un nouveau réchauffage — réduisez le volume et augmentez-le plus progressivement.
7. **Si tout ce qui précède est correct et que le problème persiste,** il peut s'agir d'une limitation spécifique au fournisseur plutôt que d'un défaut dans votre configuration — cela peut prendre un certain temps à se résoudre de lui-même une fois la cause sous-jacente (généralement les plaintes ou les rebonds) corrigée.

## Conseils

- Corrigez l'authentification DNS avant tout le reste — tous les autres leviers de délivrabilité (contenu, hygiène de liste, réchauffage) comptent moins si SPF/DKIM/DMARC ne passent pas.
- Traitez la validation DNS de l'assistant de configuration comme une vérification ponctuelle, et non comme une opération unique — relancez-la chaque fois que vous migrez de fournisseur DNS ou renouvelez un domaine auprès d'un registrant différent.
- Une liste propre qui ouvre et clique surpassera toujours une liste plus grande qui ne le fait pas — résistez à l'envie d'importer une liste ancienne et non vérifiée « au cas où ».
- Surveillez vos chiffres par rapport à vos propres envois passés, et non à un benchmark sectoriel générique — votre propre historique est le signal le plus fiable d'un problème réel.
- Si vous êtes sur un plan hébergé par Spwig, la signature DKIM et la gestion de la réputation de la passerelle de messagerie hébergée sont gérées pour vous — votre responsabilité restante est la qualité de la liste et le contenu, et non le DNS.