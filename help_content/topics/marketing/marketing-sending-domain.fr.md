---
title: Domaine d'envoi marketing
---

# Domaine d'envoi marketing

Votre boutique envoie deux types d'e-mails très différents :

- **Transactionnel** — confirmations de commande, mises à jour d'expédition, réinitialisations de mot de passe. Ces e-mails doivent toujours arriver dans la boîte de réception.
- **Marketing** — newsletters, promotions, récupération de panier, alertes de retour en stock.

Par défaut, les deux sont envoyés sous la même identité d'envoi, ce qui signifie qu'ils **partagent une seule réputation d'expéditeur**. Si une campagne marketing génère des plaintes pour spam ou atteint des adresses obsolètes, cette réputation diminue — et vos confirmations de commande et réinitialisations de mot de passe peuvent commencer à atterrir dans le spam.

Un **domaine d'envoi marketing** corrige ce problème. Vous configurez une seconde identité d'envoi — sur son propre sous-domaine tel que `news.yourstore.com` — et vous la marquez pour le marketing. Spwig envoie alors chaque campagne depuis cette identité et conserve les e-mails transactionnels sur votre domaine principal. Une campagne approximative ne peut plus entraîner vers le bas les e-mails dont vos clients *ont besoin*.

> Cela s'applique aux boutiques auto-hébergées. Sur les plans hébergés par Spwig, la réputation d'envoi est gérée pour vous.

## Comment Spwig décide quelle identité utiliser

Une fois qu'un compte d'envoi marketing existe, le routage est automatique — vous n'avez rien à étiqueter :

- **E-mails marketing** (campagnes, parcours, newsletters, récupération de panier, retour en stock) →
  le domaine d'envoi marketing.
- **E-mails transactionnels** (commandes, expédition, réinitialisations de mot de passe, vérification) → votre domaine
  principal.

Si vous ne configurez jamais de domaine marketing, rien ne change : tout continue d'être envoyé
depuis votre compte par défaut exactement comme avant.

## Configuration

Vous pouvez commencer depuis l'un des deux points d'entrée :

- Le bouton **« Configurer le domaine marketing »** sur la bannière du tableau de bord de Campaign Studio, ou
- **Comptes e-mail → « Domaine d'envoi marketing »**.

![Le tableau de bord de Campaign Studio avec la bannière « Protégez vos e-mails transactionnels » et son bouton Configurer le domaine marketing](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![Le bouton Domaine d'envoi marketing sur la liste des Comptes e-mail, à côté de Parcourir les fournisseurs](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Les deux ouvrent l'assistant de configuration e-mail pré-marqué pour un compte marketing. Ensuite :

1. **Choisissez un sous-domaine.** Utilisez quelque chose comme `news.yourstore.com` ou
   `mail.yourstore.com`. C'est l'étape la plus importante : l'identité marketing doit être un
   **(sous)domaine différent** de celui utilisé par vos e-mails transactionnels — cette séparation
   est exactement ce qui protège votre réputation transactionnelle. Envoyer du marketing depuis votre
   domaine principal ne vous offre aucune isolation.
2. **Saisissez l'adresse de l'expéditeur** sur ce sous-domaine, par exemple `news@news.yourstore.com`.
3. **Ajoutez les enregistrements DNS.** L'assistant génère les enregistrements SPF, DKIM et DMARC pour le
   sous-domaine — y compris une clé DKIM unique pour cette identité marketing. Ajoutez-les chez votre
   fournisseur DNS (l'assistant dispose de boutons de copie et d'onglets par fournisseur), puis exécutez la
   vérification jusqu'à ce que tous les enregistrements soient validés.
4. **Terminer.** Le compte est créé et marqué **Marketing uniquement**. Désormais, vos
   campagnes sont envoyées depuis ce compte.

Vous pouvez confirmer que cela a fonctionné sur la liste des **Comptes e-mail** : vous verrez un second compte avec
une finalité **Marketing uniquement**, et la bannière de Campaign Studio disparaît.

## Bon à savoir

- **Vous ne pouvez pas casser accidentellement les e-mails transactionnels.** Spwig ne vous permettra pas de définir votre seul
  compte sur « Marketing uniquement », ni de désactiver/supprimer votre dernier compte transactionnel — il y a
  toujours un endroit où envoyer les confirmations de commande et les réinitialisations de mot de passe.
- **Échauffez progressivement.** Un domaine d'envoi tout nouveau n'a pas encore de réputation.

Augmentez votre
  volume sur quelques semaines plutôt que d'envoyer à toute votre liste dès le premier jour.
- **Gardez le DNS du sous-domaine en bonne santé.** SPF, DKIM et DMARC sur le sous-domaine marketing
  doivent rester valides, tout comme votre domaine principal.

Voir le
  [Guide d'exploitation de la délivrabilité des e-mails](deliverability) pour une vue d'ensemble.
- **Le consentement s'applique toujours.** Les e-mails marketing ne sont envoyés qu'aux abonnés qui ont donné leur consentement,
  et chaque campagne comporte un lien de désinscription — la séparation du domaine ne modifie
  rien de tout cela.