---
title: Configuration des paramètres du magasin
---

Les paramètres du magasin sont le lieu central pour configurer l'identité, la localisation, la marque et les préférences opérationnelles de votre magasin. Accédez à **Paramètres > Paramètres du magasin** pour commencer.

![Onglet général des paramètres du magasin](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Onglet Général

L'onglet **Général** contient les paramètres d'identité de base de votre magasin.

### Identité du magasin

- **Nom du magasin** — Le nom affiché dans les titres de page, les e-mails et l'en-tête de l'admin.
- **Slogan** — Une courte description de votre magasin, utilisée pour le référencement et le partage social.
- **URL du site** — L'adresse web publique de votre magasin. Cela est utilisé dans les e-mails, la génération de carte de site et la création de liens.

### Informations de contact

- **E-mail de contact** — Receve les notifications de commande et est affiché dans les communications avec les clients.
- **Numéro de téléphone** — Numéro de téléphone de support facultatif affiché dans le pied de page et les e-mails.

### Adresse du commerce

Entrez votre adresse complète (rue, ville, état, code postal, pays). Cela est utilisé pour:
- Calculs d'origine de livraison
- Calculs d'impôts
- Exigences légales et factures

## Marquage

### Logo

Téléchargez votre logo de magasin (PNG ou SVG recommandés, ~200x50px avec arrière-plan transparent). Le logo s'affiche dans:
- L'en-tête du magasin
- Les modèles d'e-mail
- Le panneau d'administration

### Favicon

Téléchargez un favicon carré (ICO ou PNG, 32x32px). Il s'affiche comme:
- Icône de l'onglet du navigateur
- Icône de signet
- Icône d'écran d'accueil mobile

## Localisation

### Langue par défaut

Choisissez la langue principale de votre magasin parmi 10 options prises en charge:

| Langue | Code |
|----------|------|
| Anglais | en |
| Espagnol | es |
| Français | fr |
| Allemand | de |
| Portugais | pt |
| Japonais | ja |
| Chinois simplifié | zh-hans |
| Chinois traditionnel | zh-hant |
| Russe | ru |
| Arabe | ar |

La langue par défaut contrôle la langue de l'interface d'administration et le recours pour le contenu du magasin.

### Fuseau horaire

Sélectionnez le fuseau horaire de votre magasin pour des horodatages de commande précis, des promotions planifiées et des rapports.

### Devise

- **Devise par défaut** — La devise principale pour les prix et le comptabilité.
- **Multi-devise** — Activez pour permettre aux clients de voir les prix dans leur devise préférée avec une conversion automatique en utilisant les taux de change en temps réel.

Configurez des devises supplémentaires dans **Paramètres > Paramètres du magasin > Devise**.

## Paramètres de commerce électronique

### Achat en tant que client non inscrit

Permettre les achats sans créer de compte:
- Flux de paiement plus rapide
- Moins de friction pour les premiers achats
- Capture moins de données client

### Format du numéro de commande

Personnalisez l'apparence des numéros de commande:
- **Préfixe** — par exemple, "ORD-"
- **Numéro de départ** — Le premier numéro de commande
- **Remplissage** — par exemple, 00001

### Paramètres par défaut de l'inventaire

- **Suivre l'inventaire** — Activer le suivi des stocks globalement
- **Seuil de stock bas** — Niveau d'alerte (par défaut: 5 unités)
- **Permettre les commandes en attente** — Accepter les commandes lorsqu'il n'y a plus de stock

## Paramètres d'e-mail

### Informations d'expéditeur

- **Nom de l'expéditeur** — Apparaît comme l'expéditeur de l'e-mail (généralement le nom de votre magasin)
- **E-mail de l'expéditeur** — Doit provenir d'un domaine vérifié
- **E-mail de réponse** — Où les réponses des clients sont dirigées

### Fournisseur d'e-mail

Configurez votre service de livraison d'e-mails dans **Paramètres > Configuration des e-mails**. Les fournisseurs pris en charge comprennent SMTP, SendGrid, Mailgun et Amazon SES.

## Juridique et conformité

Ajoutez vos politiques de magasin pour répondre aux exigences légales:

- **Conditions générales** — Obligatoire pour le paiement; les clients doivent accepter avant d'acheter
- **Politique de confidentialité** — Conformité RGPD/CCPA; liée dans le pied de page
- **Politique de retour** — Définir votre fenêtre de retour, les conditions et le processus de remboursement

## Mode maintenance

Activez le mode maintenance pour mettre temporairement votre magasin hors ligne:
- Affiche un message de maintenance personnalisé aux visiteurs
- Restreint l'accès aux utilisateurs administrateurs uniquement
- Utile lors de mises à jour majeures ou de migrations

## Paramètres fiscaux

Configurez la collecte d'impôts à **Paramètres > Paramètres fiscaux**:

1. **Méthode de calcul** — Par adresse de livraison, adresse de facturation ou emplacement du magasin
2. **Taux d'impôt** — Définir les taux par région et classe d'impôt des produits
3. **Affichage des impôts** — Afficher les prix avec impôt, sans impôt ou les deux

## Conseils

- Définissez correctement votre fuseau horaire avant de traiter toute commande — cela affecte tous les horodatages et rapports.
- Activez l'achat en tant que client non inscrit pour améliorer les taux de conversion.
- Remplissez votre adresse commerciale pour des calculs de livraison et d'impôts précis.
- Téléchargez à la fois un logo et un favicon pour une expérience professionnelle et marquée.
- Vérifiez régulièrement vos pages juridiques pour rester conforme aux réglementations locales.

## Dépannage

**Les modifications ne s'affichent pas sur le magasin:"
- Effacez le cache de votre navigateur
- Exécutez une suppression du cache depuis le panneau d'administration
- Vérifiez si le mode maintenance est accidentellement activé

**Les e-mails ne sont pas envoyés:"
- Vérifiez les paramètres de votre fournisseur d'e-mails dans la Configuration des e-mails
- Vérifiez que le domaine de l'e-mail "expéditeur" est vérifié
- Testez la connexion depuis la page de configuration du fournisseur

**La conversion de devise ne fonctionne pas:"
- Vérifiez que votre fournisseur de taux de change est connecté
- Vérifiez les identifiants API dans les paramètres des taux de change
- Essayez de mettre à jour les taux manuellement

