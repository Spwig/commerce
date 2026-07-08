---
title: Configuration des emails
---

La configuration des emails contrôle la manière dont votre magasin envoie les emails transactionnels — confirmations de commande, notifications d'expédition, réinitialisation de mot de passe, etc. Spwig inclut un serveur SMTP intégré et prend en charge les fournisseurs d'email externes pour une meilleure deliverabilité.

![Comptes email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Fournisseurs Disponibles

| Fournisseur | Description |
|----------|-------------|
| **SMTP intégré** | Serveur d'email auto-hébergé gratuit inclus avec Spwig. Signature DKIM automatique. |
| **API Gmail** | Envoyez via votre compte Gmail ou Google Workspace en utilisant l'authentification OAuth. |
| **SMTP générique** | Connectez tout serveur SMTP (SendGrid, Mailgun, Amazon SES, ou votre propre serveur de messagerie). |

## Configuration des Emails

Accédez à **Paramètres > Comptes email** et cliquez sur **Ajouter un compte email** pour lancer le guide d'installation.

### Étape 1 : Sélectionner le Fournisseur

Choisissez votre fournisseur d'email. Le serveur SMTP intégré est l'option la plus simple pour commencer — il n'exige aucun compte externe.

### Étape 2 : Configurer les Identifiants

Entrez les identifiants pour votre fournisseur choisi :

- **SMTP intégré** — Aucun identifiant requis. Le serveur fonctionne sur votre installation Spwig.
- **API Gmail** — Authentifiez-vous via Google OAuth. Vous serez redirigé pour vous connecter avec votre compte Google.
- **SMTP générique** — Entrez l'adresse du serveur SMTP, le port, le nom d'utilisateur et le mot de passe.

### Étape 3 : Configuration de l'Expéditeur

Définissez l'identité de l'expéditeur pour les emails sortants :

- **Email de l'expéditeur** — L'adresse email qui apparaît dans le champ « De » (par exemple, orders@yourstore.com)
- **Nom de l'expéditeur** — Le nom d'affichage à côté de l'adresse email (par exemple, « Votre Nom de Magasin »)
- **Email de réponse** — L'endroit où les réponses des clients sont dirigées (peut différer de l'adresse de l'expéditeur)

### Étape 4 : Validation DNS

Vérifiez les enregistrements d'authentification d'email de votre domaine. Le guide vérifie trois enregistrements DNS :

| Enregistrement | Objectif |
|--------|---------|
| **SPF** | Autorise votre serveur à envoyer des emails au nom de votre domaine |
| **DKIM** | Signe numériquement les emails pour prouver qu'ils n'ont pas été altérés |
| **DMARC** | Indique aux serveurs de réception ce qu'ils doivent faire des emails qui échouent les vérifications SPF/DKIM |

Pour chaque enregistrement, le guide affiche :
- **Statut actuel** — Si l'enregistrement est correctement configuré
- **Valeur requise** — L'enregistrement DNS exact à ajouter auprès de votre registrar de domaine
- **Statut de propagation** — Si les dernières modifications ont pris effet (les changements DNS peuvent prendre jusqu'à 48 heures)

Le serveur SMTP intégré génère automatiquement des clés DKIM pour votre domaine.

### Étape 5 : Envoyer un Email de Test

Envoyez un email de test pour vérifier que tout fonctionne :
1. Entrez une adresse email destinataire
2. Cliquez sur **Envoyer le test**
3. Vérifiez votre boîte de réception pour le message de test
4. Vérifiez que l'email arrive sans avertissements de spam

### Étape 6 : Enregistrer et Activer

Enregistrez la configuration et définissez le compte comme actif. Marquez-le comme **Par défaut** s'il doit être le compte d'email principal.

## Modèles d'Email

Spwig inclut plus de 30 modèles d'email pour chaque événement transactionnel. Accédez à **Paramètres > Modèles d'email** pour les gérer.

### Types de Modèles

Les modèles couvrent tous les événements du magasin, notamment :
- **Cycle de vie de la commande** — Confirmation, traitement, expédition, livraison, annulation
- **Paiement** — Reçu, confirmation de remboursement, paiement échoué
- **Compte client** — Bienvenue, réinitialisation du mot de passe, vérification de l'email
- **Cartes cadeaux** — Envoi, notification de solde
- **Expédition** — Mises à jour de suivi, confirmation de livraison
- **Produits numériques** — Liens de téléchargement, clés de licence
- **Marketing** — Récupération de panier abandonné, demandes d'avis

### Personnalisation des Modèles

1. Accédez à la liste des modèles
2. Cliquez sur un modèle pour l'éditer
3. Modifiez le sujet, l'en-tête, le contenu du corps et le pied de page
4. Utilisez les variables de modèle (par exemple, `{{ order.number }}`, `{{ customer.name }}`) pour du contenu dynamique
5. Prévisualisez l'email avant de l'enregistrer

### Support Multilingue

Les modèles d'email prennent en charge plusieurs langues :
- Chaque modèle peut avoir des traductions pour tous les langages actifs de votre magasin
- Le système envoie les emails dans la langue préférée du client
- **Chaîne de secours linguistique** — Si une traduction n'est pas disponible, le système recourt à la langue par défaut du magasin
- Utilisez la fonctionnalité **Traduction par IA** pour traduire automatiquement les modèles dans d'autres langues

### Dupliquer des Modèles

Pour créer une version personnalisée d'un modèle système :
1. Ouvrez le modèle que vous souhaitez modifier
2. Cliquez sur **Dupliquer le modèle**
3. Modifiez la version dupliquée
4. La duplication a la priorité sur le modèle système d'origine

## File d'attente des emails

Surveillez les emails sortants à **Paramètres > File d'attente des emails** : 

- **En attente** — Emails en attente d'envoi
- **En cours d'envoi** — Actuellement en transmission
- **Envoyés** — Livrés avec succès
- **Échoués** — N'ont pas pu être livrés (avec les détails d'erreur)
- **Rejetés** — Rejetés par le serveur de messagerie du destinataire

Cliquez sur un email pour afficher ses détails complets, y compris l'expéditeur, le sujet, l'heure d'envoi et le statut de livraison.

## Suivi de la livraison

Suivez l'engagement des emails : 
- **Ouvertures** — Combien de destinataires ont ouvert l'email
- **Clics** — Clics sur les liens dans l'email
- **Rejets** — Suivi des rejets durs et mous
- **Réclamations** — Signalements de spam par les destinataires

## Plusieurs comptes

Vous pouvez configurer plusieurs comptes email : 
- **Compte par défaut** — Utilisé pour tous les emails sortants sauf s'ils sont surchargés
- **Compte de secours** — Si le compte par défaut échoue, les emails sont mis en file d'attente pour une nouvelle tentative
- Utilisez différents comptes pour différentes finalités (par exemple, un pour les emails transactionnels, un autre pour le marketing)

## Conseils

- Commencez par le **serveur SMTP intégré** pour une configuration rapide, puis passez à un fournisseur externe si vous avez besoin de volumes de diffusion plus élevés ou d'une meilleure deliverabilité.
- Configurez toujours les enregistrements **SPF, DKIM et DMARC** — sans eux, les emails ont beaucoup plus de chances d'atterrir dans les dossiers spam.
- Envoyez un **email de test** après toute modification de configuration pour vérifier que la livraison fonctionne.
- Surveillez régulièrement la file d'attente des emails pour les emails **échoués** ou **rejetés** — cela indique des problèmes de deliverabilité.
- Utilisez une **adresse d'expéditeur professionnelle** (par exemple, orders@yourstore.com) plutôt qu'une adresse email gratuite pour une meilleure confiance et deliverabilité.
- Gardez vos modèles concis — les emails transactionnels doivent transmettre l'information rapidement, sans être des lettres d'information marketing.

