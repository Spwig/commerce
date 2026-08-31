---
title: Hygiène de la liste et suppressions
---

Chaque adresse e-mail qui génère un rebond définitif, marque vos messages comme indésirables ou échoue de manière répétée à recevoir vos messages met le reste de votre liste en danger — les fournisseurs de messagerie évaluent la réputation de votre expéditeur en fonction de la propreté de vos envois, et une liste sale signifie qu'une plus grande partie de *chaque* campagne atterrit dans les courriers indésirables. Campaign Studio vous protège automatiquement contre cela grâce à l'**hygiène de la liste** : il surveille les adresses non livrables et les adresses ayant signalé des plaintes, et cesse d'envoyer des e-mails marketing à ces adresses, sans aucune configuration de votre part.

Ceci est distinct des désinscriptions. Une adresse désinscrite a retiré son consentement ; une adresse **supprimée** est une adresse que Spwig a apprise comme étant non sûre ou impossible à continuer de recevoir des e-mails, quel que soit le consentement.

## Comment les adresses sont supprimées

Spwig ajoute une adresse à la **liste de suppression** automatiquement lorsque :

| Déclencheur | Ce que cela signifie |
|---------|---------------|
| **Rebond définitif** | L'adresse n'existe pas, ou le domaine a refusé d'accepter le courrier pour elle — non livrable de manière permanente. |
| **Plainte pour spam** | Un destinataire a marqué votre e-mail comme spam ou courrier indésirable. |
| **Rebonds temporaires répétés** | L'adresse a généré un rebond temporaire (boîte aux lettres pleine, serveur temporairement indisponible) 5 fois dans une fenêtre glissante de 30 jours. Un seul rebond temporaire est traité comme un incident passager et ignoré — seul un schéma d'échecs répétés déclenche la suppression. |
| **Blocage manuel** | Vous avez ajouté l'adresse vous-même. |

Une fois qu'une adresse est supprimée, Spwig cesse immédiatement de lui envoyer tout e-mail de **campagne** ou de **parcours** — aucune autre action n'est requise de votre part.

## D'où vient le signal

Spwig peut apprendre un rebond ou une plainte à partir de plusieurs endroits différents, affichés comme la **Source** sur chaque adresse supprimée :

- **Rejet à l'envoi** — votre serveur de messagerie a refusé l'adresse immédiatement lorsque Spwig a tenté de lui envoyer un e-mail.
| **Webhook du fournisseur** — si vous avez connecté un fournisseur de messagerie (tel que SendGrid, Amazon SES, Mailgun ou Postmark), ce fournisseur signale les rebonds et les plaintes à Spwig au fur et à mesure qu'ils se produisent.
- **Passerelle de messagerie** — si votre boutique envoie via la passerelle de messagerie hébergée par Spwig, Spwig récupère les rapports de rebonds de la passerelle en votre nom.
- **Ajout manuel** — vous avez saisi l'adresse vous-même depuis l'administration.

Vous n'avez besoin de configurer rien pour en bénéficier — quel que soit le moyen par lequel vous envoyez des e-mails, Spwig surveille les échecs et maintient votre liste propre.

## Le tableau de bord de Campaign Studio

Ouvrez **Campaign Studio** et cherchez la carte **Adresses supprimées**. Elle affiche le nombre total d'adresses actuellement supprimées, ainsi que le nombre de nouvelles adresses au cours des 30 derniers jours. Cliquez sur la carte pour ouvrir la liste complète des suppressions.

![La carte de statistiques des adresses supprimées du tableau de bord de Campaign Studio, affichant un total et un compteur de "nouvelles au cours des 30 derniers jours"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Une augmentation constante du compteur est normale — chaque liste accumule certaines mauvaises adresses au fil du temps lorsque les personnes changent d'emploi, ferment des comptes ou abandonnent des boîtes aux lettres. Une augmentation soudaine mérite d'être investiguée ; consultez [Boîte d'envoi e-mail](email-outbox) pour vérifier si un envoi particulier a rencontré un nombre inhabituel d'échecs.

## La liste des suppressions

Cliquez sur **Suppressions** pour voir chaque adresse supprimée, la raison pour laquelle elle a été supprimée et d'où vient le signal.

![La liste des suppressions affichant les adresses supprimées avec leurs colonnes Raison et Source](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Utilisez les filtres à droite pour restreindre la liste par **Raison** ou **Source** — par exemple, pour examiner chaque adresse bloquée manuellement, ou tout ce qui est arrivé via un webhook de fournisseur.

## Ajouter une adresse manuellement

Pour bloquer une adresse vous-même — une adresse d'abus connue, un concurrent qui extrait votre infolettre, ou tout autre élément que vous souhaitez exclure de votre liste — cliquez sur **+ Ajouter une adresse supprimée** et remplissez :

- **Email** — l'adresse à bloquer
- **Reason** — choisissez **Manually blocked** pour une entrée ajoutée manuellement
- **Source** — choisissez **Added manually**
- **Detail** — une note facultative expliquant la raison (utile pour vos propres registres et pour tout le personnel qui examinera la liste plus tard)

Enregistrez l'entrée et Spwig cesse immédiatement d'envoyer tout e-mail de campagne ou de parcours à cette adresse.

## Quand devrais-je libérer une adresse ?

La libération (dés-suppression) d'une adresse doit être rare et délibérée. Ne le faites que lorsque vous êtes certain que le problème sous-jacent est réellement résolu — par exemple :

- Un client vous indique que sa boîte aux lettres était pleine et qu'elle a été vidée.
- Une adresse a été supprimée en raison d'une série de rebonds doux que vous savez avoir été causée par une panne temporaire chez leur fournisseur de messagerie, et non par une boîte aux lettres inexistante.
- Vous avez bloqué une adresse manuellement et décidez plus tard que le blocage était une erreur.

Pour libérer une adresse, ouvrez-la dans la liste des suppressions et supprimez l'entrée — cela lève le blocage afin que l'adresse puisse à nouveau recevoir des e-mails. Ne libérez pas une adresse ayant fait l'objet d'un rebond dur simplement parce qu'il est gênant de perdre un abonné ; l'adresse n'existe pas, et y envoyer à nouveau ne fera que provoquer un rebond et vous coûter votre réputation une seconde fois. De même, libérer une adresse ayant fait l'objet d'une plainte pour spam est rarement utile — ce destinataire a indiqué à son fournisseur de messagerie qu'il ne souhaite pas recevoir vos e-mails, et leur renvoyer des messages risque de provoquer une nouvelle plainte.

## Ce qui n'est pas affecté

La suppression ne s'applique qu'aux **campagnes marketing et parcours** envoyés via Campaign Studio. Elle n'affecte pas les **e-mails transactionnels** — les confirmations de commande, les mises à jour d'expédition, les réinitialisations de mot de passe et autres e-mails que votre boutique envoie dans le cadre d'une commande ou d'une action de compte passent toujours, même à une adresse supprimée. La suppression existe pour protéger votre réputation d'expéditeur marketing ; ce n'est pas une liste de blocage générale pour votre boutique.

## Conseils

- Ne luttez pas contre le système en libérant manuellement chaque rebond dur que vous voyez — un rebond dur signifie que l'adresse est disparue, et la réajouter à vos envois ne fera que provoquer un nouveau rebond.
- Vérifiez la liste des suppressions après un gros envoi si votre taux d'ouverture semble anormalement bas — une vague de rebonds doux sur un domaine partagé (par exemple, un serveur de messagerie d'entreprise ayant des problèmes) peut être le signe d'un problème de livraison temporaire qui mérite d'être investigué avec votre fournisseur.
- Si vous migrez vers Spwig depuis une autre plateforme, n'importez pas manuellement votre ancienne liste de blocage complète en tant que suppressions — laissez Spwig apprendre des rebonds et des plaintes réels sur cette liste, afin de ne pas bloquer accidentellement des adresses qui auraient été livrées sans problème.
- Examinez la colonne **Source** occasionnellement — un grand nombre d'entrées **Provider webhook** confirme que la signalisation des rebonds de votre fournisseur d'e-mail est connectée et fonctionnelle.
- Gardez le champ **Detail** significatif lors de l'ajout d'un blocage manuel ; c'est le seul enregistrement de la raison pour laquelle cette décision a été prise une fois le temps passé.