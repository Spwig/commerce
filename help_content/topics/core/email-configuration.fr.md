---
title: Configuration de l'e-mail
---

La configuration de l'e-mail contrôle la manière dont votre boutique envoie les e-mails transactionnels — confirmations de commande, notifications d'expédition, réinitialisations de mot de passe, et plus encore. Spwig inclut un serveur SMTP intégré et prend en charge les fournisseurs de messagerie externes pour une meilleure délivrabilité.

![Comptes e-mail](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Fournisseurs disponibles

| Fournisseur | Description |
|----------|-------------|
| **SMTP intégré** | Serveur de messagerie auto-hébergé gratuit inclus avec Spwig. Signature DKIM automatique. |
| **Gmail API** | Envoi via votre compte Gmail ou Google Workspace en utilisant l'authentification OAuth. |
| **SMTP générique** | Connectez n'importe quel serveur SMTP (SendGrid, Mailgun, Amazon SES, ou votre propre serveur de messagerie). |

## Configuration de l'e-mail

Accédez à **Paramètres > Comptes e-mail** et cliquez sur **Ajouter un compte e-mail** pour lancer l'assistant de configuration.

### Étape 1 : Sélection du fournisseur

Choisissez votre fournisseur de messagerie. Le serveur SMTP intégré est l'option la plus simple pour commencer — il ne nécessite aucun compte externe.

### Étape 2 : Configuration des identifiants

Saisissez les identifiants de votre fournisseur choisi :

- **SMTP intégré** — Aucun identifiant requis. Le serveur fonctionne sur votre installation Spwig.
- **Gmail API** — Authentifiez-vous via Google OAuth. Vous serez redirigé pour vous connecter avec votre compte Google.
- **SMTP générique** — Saisissez l'adresse du serveur SMTP, le port, le nom d'utilisateur et le mot de passe.

### Étape 3 : Configuration de l'expéditeur

Définissez l'identité de l'expéditeur pour les e-mails sortants :

- **E-mail de l'expéditeur** — L'adresse e-mail qui apparaît dans le champ « De » (par exemple, orders@yourstore.com)
- **Nom de l'expéditeur** — Le nom d'affichage à côté de l'adresse e-mail (par exemple, « Votre Nom de Boutique »)
- **E-mail de réponse** — L'endroit où les réponses des clients sont dirigées (peut différer de l'adresse de l'expéditeur)

### Étape 4 : Validation DNS

Vérifiez les enregistrements d'authentification e-mail de votre domaine. L'assistant vérifie trois enregistrements DNS :

| Enregistrement | Objectif |
|--------|---------|
| **SPF** | Autorise votre serveur à envoyer des e-mails au nom de votre domaine |
| **DKIM** | Signe numériquement les e-mails pour prouver qu'ils n'ont pas été altérés |
| **DMARC** | Indique aux serveurs destinataires quoi faire avec les e-mails qui échouent aux vérifications SPF/DKIM |

Pour chaque enregistrement, l'assistant affiche :
- **Statut actuel** — Si l'enregistrement est correctement configuré
- **Valeur requise** — L'enregistrement DNS exact à ajouter chez votre registrar de domaine
- **Statut de propagation** — Si les modifications récentes ont pris effet (les modifications DNS peuvent prendre jusqu'à 48 heures)

Le serveur SMTP intégré génère automatiquement les clés DKIM pour votre domaine.

### Étape 5 : Envoyer un e-mail de test

Envoyez un e-mail de test pour vérifier que tout fonctionne :
1. Saisissez une adresse e-mail du destinataire
2. Cliquez sur **Envoyer le test**
3. Vérifiez votre boîte de réception pour le message de test
4. Vérifiez que l'e-mail arrive sans avertissements de spam

### Étape 6 : Enregistrer et activer

Enregistrez la configuration et définissez le compte comme actif. Marquez-le comme **Par défaut** s'il doit être le compte e-mail principal.

## Modèles d'e-mail

Spwig inclut plus de 30 modèles d'e-mail pour chaque événement transactionnel. Accédez à **Paramètres > Modèles d'e-mail** pour les gérer.

### Types de modèles

Les modèles couvrent tous les événements de la boutique, y compris :
- **Cycle de vie de la commande** — Confirmation, traitement, expédiée, livrée, annulée
- **Paiement** — Reçu, confirmation de remboursement, paiement échoué
- **Compte client** — Bienvenue, réinitialisation du mot de passe, vérification de l'e-mail
- **Cartes cadeaux** — Livraison, notification de solde
- **Expédition** — Mises à jour de suivi, confirmation de livraison
- **Produits numériques** — Liens de téléchargement, clés de licence
- **Marketing** — Récupération de panier abandonné, demandes d'avis

### Personnalisation des modèles

1. Accédez à la liste des modèles
2. Cliquez sur un modèle pour le modifier
3. Modifiez la ligne d'objet, l'en-tête, le contenu du corps et le pied de page
4. Utilisez les variables de modèle (par exemple, `{{ order.number }}`, `{{ customer.name }}`) pour un contenu dynamique
5. Prévisualisez l'e-mail avant d'enregistrer

### Prise en charge multilingue

Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques. /no_think

Les modèles d'e-mails prennent en charge plusieurs langues :
- Chaque modèle peut avoir des traductions pour toutes les langues actives de votre boutique
- Le système envoie les e-mails dans la langue préférée du client
- **Chaîne de repli linguistique** — Si une traduction n'est pas disponible, le système utilise la langue par défaut de la boutique
- Utilisez la fonction **Traduction IA** pour traduire automatiquement les modèles dans d'autres langues

### Clonage des modèles

Pour créer une version personnalisée d'un modèle système :
1. Ouvrez le modèle que vous souhaitez modifier
2. Cliquez sur **Cloner le modèle**
3. Modifiez la version clonée
4. Le clone a la priorité sur le modèle système d'origine

## File d'attente des e-mails

Surveillez les e-mails sortants dans **Paramètres > File d'attente des e-mails** :

- **En file d'attente** — E-mails en attente d'envoi
- **Envoi en cours** — Actuellement en cours de transmission
- **Envoyé** — Livré avec succès
- **Échec** — N'a pas pu être livré (avec les détails de l'erreur)
- **Rebondi** — Rejeté par le serveur de messagerie du destinataire

Cliquez sur n'importe quel e-mail pour afficher tous ses détails, y compris le destinataire, l'objet, l'heure d'envoi et le statut de livraison.

## Suivi de la livraison

Suivez l'engagement des e-mails :
- **Ouvertures** — Nombre de destinataires ayant ouvert l'e-mail
- **Clics** — Clics sur les liens dans l'e-mail
- **Rebonds** — Suivi des rebonds durs et mous
- **Signalements** — Signalements de spam par les destinataires

## Multiples comptes

Vous pouvez configurer plusieurs comptes e-mail :
- **Compte par défaut** — Utilisé pour tous les e-mails sortants sauf s'il est remplacé
- **Repli** — Si le compte par défaut échoue, les e-mails sont mis en file d'attente pour une nouvelle tentative
- Utilisez des comptes différents pour des objectifs différents (par exemple, un pour les e-mails transactionnels, un autre pour le marketing)

## Mode de livraison des e-mails

Accédez à **Paramètres > Paramètres de la boutique** pour contrôler la manière dont votre boutique gère les e-mails sortants. Ces paramètres sont utiles lors du développement et des tests.

| Mode | Description |
|------|-------------|
| **En direct** | Les e-mails sont livrés normalement aux destinataires réels |
| **En pause** | Les e-mails sont maintenus en file d'attente et non envoyés jusqu'à ce que vous repassiez en mode En direct |
| **Journalisation uniquement** | Les e-mails sont enregistrés dans la boîte d'envoi mais jamais livrés |

### Redirection des e-mails de test

Définissez une adresse **E-mail de redirection de test** pour intercepter tous les e-mails sortants et les rediriger vers une seule adresse. Lorsqu'elle est définie, chaque e-mail — quel que soit le destinataire réel — est envoyé à cette adresse à la place. Cela est utile pour tester les modèles d'e-mails sans envoyer accidentellement à de vrais clients. Laissez vide pour envoyer les e-mails aux destinataires réels.

### Liste blanche des e-mails en bac à sable

En mode bac à sable ou développement, vous pouvez restreindre la livraison des e-mails à une liste blanche d'adresses approuvées. Seuls les e-mails destinés aux adresses de la liste blanche seront livrés. Tous les autres e-mails sont journalisés mais jamais envoyés. L'e-mail administrateur est toujours inclus automatiquement. Vous pouvez ajouter jusqu'à 10 adresses.

## Conseils

- Commencez par le serveur **SMTP intégré** pour une configuration rapide, puis passez à un fournisseur externe si vous avez besoin de volumes d'envoi plus élevés ou d'une meilleure délivrabilité.
- Configurez toujours les enregistrements **SPF, DKIM et DMARC** — sans eux, les e-mails ont beaucoup plus de chances d'atterrir dans les dossiers de spam.
- Envoyez un **e-mail de test** après toute modification de configuration pour vérifier que la livraison fonctionne.
- Surveillez régulièrement la file d'attente des e-mails pour les e-mails **échoués** ou **rebondis** — ceux-ci indiquent des problèmes de délivrabilité.
- Utilisez une **adresse d'expéditeur professionnelle** (par exemple, commandes@votreboutique.com) plutôt qu'une adresse e-mail gratuite pour une meilleure confiance et délivrabilité.
- Gardez vos modèles concis — les e-mails transactionnels doivent transmettre les informations rapidement, et ne doivent pas être des newsletters marketing.
