---
title: Configuration des paramètres de magasin
---

Les paramètres du magasin sont l'endroit centralisé pour configurer l'identité, la localisation, la marque et les préférences opérationnelles de votre magasin. Accédez à **Paramètres > Paramètres du magasin** pour commencer.

![onglet général des paramètres du magasin](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Onglet Général

L'onglet **Général** contient les paramètres d'identité de base de votre magasin.

### Identité du magasin

- **Nom du magasin** — Le nom d'affichage affiché dans les titres de page, les courriels et l'en-tête de l'administrateur.
- **Slogan** — Une brève description de votre magasin, utilisée pour le référencement (SEO) et le partage sur les réseaux sociaux.
- **URL du site** — L'adresse web publique de votre magasin. Cela est utilisé dans les courriels, la génération de la carte du site et le référencement.

### Informations de contact

- **Courriel de contact** — Reçoit les notifications de commande et s'affiche dans les communications clients.
- **Numéro de téléphone** — Numéro de téléphone de support optionnel affiché dans le pied de page et les courriels.

### Adresse de l'entreprise

Entrez votre adresse complète (rue, ville, état, code postal, pays). Cela est utilisé pour :
- Calculs de l'origine des envois
- Calculs d'impôts
- Exigences légales et factures

## Identification de marque

### Logo

Téléversez le logo de votre magasin (PNG ou SVG recommandés, environ 200x50 pixels avec fond transparent). Le logo s'affiche dans :
- L'en-tête du magasin
- Les modèles d'e-mails
- Le panneau d'administration

### Icône (Favicon)

Téléversez une icône carrée (ICO ou PNG, 32x32 pixels). Elle s'affiche en tant que :
- Icône de l'onglet du navigateur
- Icône de signet
- Icône de l'écran d'accueil mobile

## Localisation

### Langue par défaut

Choisissez la langue principale de votre magasin parmi 10 options prises en charge :

| Langue | Code |
|----------|------|
| Anglais | en |
| Espagnol | es |
| Francais | fr |
| Allemand | de |
| Portugais | pt |
| Japonais | ja |
| Chinois simplifié | zh-hans |
| Chinois traditionnel | zh-hant |
| Russe | ru |
| Arabe | ar |

La langue par défaut détermine la langue de l'interface d'administration et la valeur par défaut pour le contenu du magasin.

### Fuseau horaire

Sélectionnez le fuseau horaire de votre magasin pour des horodatages de commande précis, des promotions planifiées et des rapports.

### Devise

- **Devise par défaut** — La devise principale pour les prix et la comptabilité.
- **Multiple devises** — Activez-la pour permettre aux clients d'afficher les prix dans leur devise préférée avec une conversion automatique utilisant des taux de change en temps réel.

Configurez des devises supplémentaires dans **Paramètres > Paramètres du magasin > Devise**.

## Paramètres de commerce électronique

### Achat en tant que client sans compte

Autorisez les achats sans création de compte :
- Flux de paiement plus rapide
- Moins de friction pour les acheteurs pour la première fois
- Capture d'une moins grande quantité de données clients

### Création de compte

Contrôlez à quel moment les clients sont invités à créer un compte :

| Option | Description |
|--------|-------------|
| **Après achat (recommandé)** | Invite à la création de compte après une commande réussie — exploite la bonne volonté post-achat pour une meilleure conversion |
| **Pendant le paiement** | Créez un compte avant le traitement du paiement |
| **Avant le paiement** | Exigez un compte avant d'acheter (non recommandé - réduit la conversion) |

Vous pouvez également définir un message personnalisé **Création de compte** pour expliquer les avantages de l'inscription.

### Valeurs par défaut du stock

- **Suivi du stock** — Activez le suivi du stock global
- **Seuil de stock faible** — Niveau de stock à partir duquel des alertes de stock faible sont envoyées à l'email de l'administrateur (valeur par défaut : 10 unités)

## Intelligence du stock

![carte d'intelligence du stock montrant les champs Temps de réapprovisionnement par défaut et multiplicateur de stock de sécurité](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Ces paramètres ajustent les calculs automatiques de réapprovisionnement, de stock de sécurité et de vitesse des ventes, et contrôlent comment les situations de stock épuisé ou faible sont gérées.

- **Temps de réapprovisionnement par défaut (jours)** — Combien de jours il faut généralement pour recevoir le réapprovisionnement de votre fournisseur une fois que vous passez commande (valeur par défaut : 14).

La prévision s'en sert pour signaler les produits qui doivent être réapprovisionnés *maintenant* pour éviter un manque de stock avant que le nouveau stock n'arrive.
- **Multiplicateur de stock de sécurité** — Un tampon appliqué sur la demande attendue pour absorber les pics de ventes ou retards des fournisseurs.

Par exemple, un multiplicateur de `1,5` ajoute un buffer de 50 % par rapport à votre stock de sécurité calculé ; `2,0` le double.

Augmentez-le pour les produits dont le manque est coûteux (best-sellers, articles saisonniers) ; réduisez-le pour les stocks à faible rotation que vous ne souhaitez pas commander en excès.
- **Période de calcul de la vitesse (jours)** — La période de référence que Spwig utilise pour calculer la vitesse de vente de chaque produit, ce qui détermine à son tour les suggestions de réapprovisionnement et les chiffres de jours de stock (valeur par défaut : 30).

Une période plus courte réagit plus rapidement aux changements récents de la demande ; une période plus longue lisse les pics saisonniers, de sorte qu'une seule semaine chargée ne fausse pas la prévision.
- **Autoriser les commandes en attente par défaut** — Le paramètre initial d'autorisation des commandes en attente appliqué aux nouveaux produits (désactivé par défaut).

Chaque produit peut toujours le remplacer individuellement sur sa propre page produit, et les produits existants conservent le paramètre qu'ils ont déjà — modifier celui-ci ne change que le paramètre par défaut avec lequel les nouveaux produits commencent, cela ne met pas à jour rétroactivement votre catalogue.
- **Fréquence des alertes de stock faible** — Combien souvent l'application mobile Spwig est-elle notifiée en cas de stock faible : **En temps réel** envoie une notification push dès qu'un produit dépasse sa limite de stock faible ; **Résumé quotidien** et **Résumé hebdomadaire** envoient à la place une seule notification push résumant l'ensemble des produits à stock faible selon ce calendrier.

Ce paramètre n'est en vigueur que lorsque **Alertes de stock faible** (Paramètres e-mail, ci-dessous) est activé — avec les alertes désactivées, aucune notification n'est envoyée, quelle que soit la fréquence.

### Documents et factures

![Carte Documents et factures montrant les champs Tax ID / Numéro de TVA, Texte du pied de facture et Texte du pied de bon de livraison remplis avec des valeurs d'exemple](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Ces champs remplissent les factures et les bons de livraison générés par Spwig pour les commandes — par exemple, lorsqu'un commerçant télécharge ou envoie par courriel une facture PDF, ou imprime un bon de livraison pour un envoi.

- **ID fiscal / Numéro de TVA** — Votre numéro d'identification fiscal de votre entreprise. Imprimé sur les factures générées afin qu'elles respectent les exigences de documentation fiscale locales.
- **Texte du pied de facture** — Texte libre affiché en bas de chaque facture générée. Utilisations courantes : conditions de paiement (« Paiement dû dans les 30 jours »), un message de remerciement, ou des coordonnées bancaires.
- **Texte du pied de bon de livraison** — Texte libre affiché en bas de chaque bon de livraison généré. Utilisations courantes : instructions de retour ou un message au service de stockage/acheminement.
- **Largeur du logo du document (px)** — La largeur de votre logo de magasin tel qu'il apparaît sur les factures et bons de livraison PDF générés (valeur par défaut : 200 px). La hauteur est mise à l'échelle automatiquement pour correspondre, de sorte que les proportions de votre logo sont préservées. L'image du logo provient de votre **Logo** (Marque, ci-dessus) — les logos SVG ne sont pas dessinés sur les documents PDF, donc téléchargez une version PNG ou JPG de votre logo si vous utilisez un art vectoriel sur le site marchand.

## Paramètres de messagerie

Configurez les paramètres de livraison des e-mails dans **Paramètres > Comptes e-mail** et **Paramètres > Modèles e-mail**. Consultez [Configuration e-mail](/help/email-configuration) pour plus de détails.

Paramètres e-mail clés disponibles dans les paramètres du magasin :

- **E-mails de confirmation de commande** — Activez ou désactivez les e-mails de confirmation automatiques
- **E-mails de notification d'expédition** — Activez ou désactivez les notifications de mise à jour d'expédition
- **Alertes de stock faible** — Envoyez des alertes à l'e-mail administrateur lorsqu'un stock tombe en dessous de la limite
- **Mode de livraison des e-mails** — En ligne (livraison normale), En pause (tous les e-mails sont bloqués), ou Enregistrement uniquement (enregistre mais ne transmet jamais)
- **E-mail de redirection de test** — Redirigez tous les e-mails sortants vers une seule adresse pour les tests

## Paramètres de sécurité

### Authentification à deux facteurs (2FA)

Contrôlez si les employés doivent utiliser l'authentification à deux facteurs :

| Paramètre | Description |
|---------|-------------|
| **Facultatif** | Les employés peuvent choisir d'activer la 2FA mais ce n'est pas obligatoire |
| **Recommandé** | Les employés voient un message les incitant à configurer la 2FA |
| **Obligatoire** | Les employés ne peuvent pas accéder à l'administration tant que la 2FA n'est pas activée |

- **Délai de grâce (jours)** — Nombre de jours pendant lesquels le personnel a le temps de configurer l'authentification à deux facteurs après l'activation de l'application
- **Autoriser les appareils fiables** — Permettre au personnel de sauter la vérification de l'authentification à deux facteurs sur les appareils reconnus pendant un nombre de jours défini

## Consentement aux cookies

Configurez le bannière de consentement aux cookies affichée aux visiteurs du magasin :

- **Consentement aux cookies activé** — Afficher ou masquer la bannière de consentement
- **Emplacement de la bannière** — Emplacement où la bannière s'affiche à l'écran (barre inférieure, fenêtre contextuelle, etc.)
- **Mode de consentement** — Avertissement simple, opt-in ou opt-out
- **Titre et texte de la bannière** — Titre et description personnalisables affichés aux visiteurs
- **Descriptions des catégories** — Descriptions distinctes pour les cookies analytiques, les cookies de marketing et les cookies fonctionnels

Tous les champs de texte de la bannière prennent en charge les traductions pour les magasins multilingues.

## Communications

L'onglet **Communications** gère comment votre magasin obtient, confirme et permet aux clients de gérer le consentement pour les courriels et messages SMS de marketing. Ces paramètres définissent votre posture de conformité légale (RGPD pour les courriels, TCPA pour les SMS), donc veuillez les examiner avec votre propre conseiller juridique avant le lancement — Spwig fournit les contrôles, pas les conseils.

![Onglet Communications montrant les cartes Email Marketing Consent, Préférences & Annulation d'abonnement, et SMS Consent](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentement au marketing par courriel

- **Activer la double validation pour les courriels de marketing** — Lorsque activé, un client qui s'inscrit au marketing par courriel reçoit un courriel de confirmation et doit cliquer sur le lien pour que Spwig lui envoie un message de marketing. Lorsque désactivé, cocher la case d'opt-in au marketing suffit. Activé par défaut, conformément aux bonnes pratiques RGPD.
- **État par défaut d'opt-in au marketing** — L'état initial d'opt-in au marketing appliqué aux nouveaux comptes clients. Désactivé par défaut (RGPD opt-out), donc les nouveaux clients commencent non abonnés aux courriels de marketing jusqu'à ce qu'ils s'abonnent activement.

Lorsque la double validation est activée, l'opt-in déclenche un courriel de confirmation avec un lien de vérification. Jusqu'à ce que le client clique dessus, il est enregistré comme ayant opté pour le marketing mais non confirmé, et les envois de marketing les ignorent — les courriels transactionnels (confirmations de commande, mises à jour d'expédition, réinitialisations de mot de passe) ne sont jamais affectés par ce paramètre.

### Préférences & Annulation d'abonnement

- **Activer le centre de préférences des clients** — Lorsque activé, les clients peuvent gérer leurs préférences par courriel et SMS depuis une page de service client lié à leur tableau de bord de compte. Lorsque désactivé, cette page et son API associée renvoient une erreur et le lien du tableau de bord est caché. Les liens de désabonnement à un clic dans vos courriels fonctionnent de toute façon — ce dispositif de secours est requis pour la conformité et n'est pas affecté par ce basculement.
- **Collecter les raisons du désabonnement** — Lorsque activé, la page de désabonnement à un clic demande au client une brève raison avant confirmation : *Je reçois trop de courriels*, *Le contenu n'est pas pertinent pour moi*, *Je ne me suis pas inscrit pour cela*, *Je n'ai plus d'intérêt*, ou *Autre*. La raison choisie par le client est enregistrée dans le registre de conformité afin que vous puissiez analyser les schémas de désabonnement au fil du temps.

### Consentement SMS

- **Exiger la vérification SMS** — Lorsque activé (par défaut), un client doit vérifier son numéro de téléphone avec un code à usage unique avant que Spwig ne lui envoie un SMS, y compris les textos de marketing. Lorsque désactivé, cocher la case d'opt-in SMS suffit à commencer à envoyer. Cette valeur par défaut a été passée à **activé** pour la sécurité TCPA — désactivez-la uniquement si vous avez une autre étape de vérification dans votre flux d'inscription.

## Mode maintenance

Activez le mode maintenance pour rendre votre magasin temporairement hors ligne : 
- Affiche un message de maintenance personnalisé aux visiteurs
- Vous pouvez linker une **Page de maintenance** créée dans le constructeur de pages pour une expérience de maintenance pleinement marquée
- Restreint l'accès aux utilisateurs administrateurs uniquement
- Utile pendant les mises à jour majeures ou les migrations

## Réseaux sociaux

Liez les profils de réseaux sociaux de votre magasin. Ils s'affichent dans le pied de page et les modèles d'e-mail :

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Paramètres SEO par défaut

Conservez toutes les formattages markdown, les chemins d'images, les blocs de code et les termes techniques.

Définir les balises méta par défaut utilisées lorsquasiment aucune page n'a de paramètres SEO spécifiques :

- **Titre méta** — Titre par défaut de la page (maximum 60 caractères)
- **Description méta** — Description par défaut affichée dans les résultats de recherche (maximum 160 caractères)
- **Mots-clés méta** — Mots-clés séparés par des virgules par défaut

## Paramètres de taxes

Configurer la collecte d'impôts à **Paramètres > Paramètres des taxes** :

1. **Méthode de calcul** — Par adresse de livraison, adresse de facturation ou emplacement du magasin
2. **Taux de taxes** — Définir les taux par région et classe de produit taxé
3. **Affichage des taxes** — Afficher les prix avec taxes, sans taxes ou les deux

## Conseils

- Configurez correctement votre fuseau horaire avant de traiter toute commande — cela affecte toutes les dates et les rapports.
- Activez le paiement sans compte pour améliorer les taux de conversion.
- Remplissez votre adresse entreprise pour des calculs précis de livraison et de taxes.
- Téléversez à la fois un logo et un favicon pour une expérience professionnelle et de marque.
- Utilisez la configuration de création de compte **Après achat** pour obtenir les meilleurs taux d'inscription.
- Activez l'obligation d'authentification à deux facteurs pour le personnel afin de protéger votre administration de magasin.
- Testez les flux d'e-mails en utilisant le paramètre **Redirection de test d'e-mail** avant de passer en direct.
- Définissez le **Délai de réapprovisionnement par défaut** pour correspondre à votre fournisseur le plus lent — la prévision de réapprovisionnement applique cette valeur unique à l'ensemble de votre catalogue, donc privilégiez la valeur la plus longue.
- Remplissez votre **Numéro de TVA / ID fiscal** et le texte du pied de page avant votre première facture réelle envoyée à un client — les deux champs sont vides par défaut.
- Laissez **Activer la double confirmation pour les e-mails marketing** activé à moins d'avoir une raison spécifique de le désactiver — c'est la configuration par défaut la plus sécurisée pour le RGPD et protège votre réputation d'expéditeur en maintenant les adresses non vérifiées hors de vos envois marketing.
- Laissez **État de consentement marketing par défaut** désactivé. Cocher la case de consentement marketing pour les nouveaux comptes nuit à la demande de consentement du RGPD, même si un client pourrait techniquement décocher la case.
- Ne désactivez pas **Activer le centre de préférences client** juste pour simplifier votre tableau de bord de compte — sans celui-ci, les clients peuvent toujours se désabonner d'un type de message, mais ils perdent la possibilité de configurer précisément leurs préférences (par exemple, garder les mises à jour de livraison mais supprimer la newsletter).
- Gardez **Exiger la vérification par SMS** activée à moins que votre flux de création de compte n'ait déjà confirmé les numéros de téléphone d'une autre manière (par exemple, une connexion basée sur SMS) — le paramètre existe spécifiquement pour vous maintenir dans les règles TCPA.

## Dépannage

**Les modifications n'apparaissent pas sur le magasin :**
- Videz le cache de votre navigateur
- Exécutez une suppression de cache depuis le panneau d'administration
- Vérifiez si le mode maintenance est activé accidentellement

**Les e-mails ne s'envoient pas :**
- Vérifiez vos paramètres de fournisseur d'e-mail dans la configuration de l'e-mail
- Vérifiez que le **Mode d'envoi d'e-mail** est défini sur **En direct**
- Assurez-vous que la **Redirection de test d'e-mail** est vide si vous souhaitez envoyer des e-mails aux destinataires réels

**La conversion de devise ne fonctionne pas :**
- Vérifiez que votre fournisseur de taux de change est connecté
- Vérifiez les identifiants API dans les paramètres du taux de change
- Essayez de mettre à jour manuellement les taux

**Les e-mails marketing n'atteignent pas les clients ayant opté pour l'abonnement :**
- Vérifiez si **Activer la double confirmation pour les e-mails marketing** est activé — si c'est le cas, le client doit cliquer sur le lien de confirmation dans l'e-mail de vérification avant que les envois marketing ne reprendrent
- Demandez au client de vérifier s'il y a un e-mail de vérification dans le spam/les courriers indésirables
- Confirmez que l'abonnement marketing du client est toujours activé dans ses préférences — un clic de désabonnement le désactive à nouveau

**Les clients disent ne pas trouver le centre de préférences :**
- Vérifiez que **Activer le centre de préférences client** est activé — lorsqu'il est désactivé, le lien du tableau de bord est caché et la page est inutilisable par conception
- Le lien de désabonnement dans n'importe quel e-mail marketing fonctionne toujours, quel que soit ce paramètre, donc orientez les clients vers celui-ci en tant que solution de secours