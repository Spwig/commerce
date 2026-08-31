---
title: Configuration des paramètres de magasin
---

Les paramètres du magasin sont l'endroit centralisé pour configurer l'identité, la localisation, la marque et les préférences opérationnelles de votre magasin. Accédez à **Paramètres > Paramètres du magasin** pour commencer.

![onglet Général des paramètres du magasin](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Onglet Général

L'onglet **Général** contient les paramètres d'identité de base de votre magasin.

### Identité du magasin

- **Nom du magasin** — Le nom d'affichage affiché dans les titres de page, les courriels et l'en-tête de l'administration.
- **Slogan** — Une brève description de votre magasin, utilisée pour le référencement et le partage sur les réseaux sociaux.
- **URL du site** — L'adresse web publique de votre magasin. Cela est utilisé dans les courriels, la génération de la carte du site et la construction de liens.

### Informations de contact

- **Courriel de contact** — Reçoit les notifications de commande et s'affiche dans les communications clients.
- **Numéro de téléphone** — Numéro de téléphone de soutien optionnel affiché dans le pied de page et les courriels.

### Adresse entreprise

Entrez votre adresse complète (rue, ville, état, code postal, pays). Cela est utilisé pour :
- Calculs de l'origine des envois
- Calculs d'impôts
- Exigences légales et factures

## Identification de la marque

### Logo

Téléversez le logo de votre magasin (PNG ou SVG recommandés, environ 200x50 pixels avec arrière-plan transparent). Le logo apparaît dans : 
- L'en-tête du magasin
- Les modèles d'e-mails
- Le panneau d'administration

### Icône (Favicon)

Téléversez une icône carrée (ICO ou PNG, 32x32 pixels). Elle apparaît en tant que : 
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
| Français | fr |
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

### Achat en tant que client

Autorisez les achats sans création de compte : 
- Flux de paiement plus rapide 
- Moins de friction pour les nouveaux clients 
- Capture d'une quantité moindre de données clients

### Création de compte

Contrôlez à quel moment les clients sont invités à créer un compte : 

| Option | Description |
|--------|-------------|
| **Après achat (recommandé)** | Invitez à la création de compte après une commande réussie — exploitez la bonne volonté post-achat pour une meilleure conversion |
| **Pendant le paiement** | Créez un compte avant le traitement du paiement |
| **Avant le paiement** | Exigez un compte avant d'acheter (non recommandé - réduit la conversion) |

Vous pouvez également définir un message personnalisé **Création de compte** pour expliquer les avantages de l'inscription.

### Valeurs par défaut du stock

- **Suivi du stock** — Activez le suivi du stock global
- **Seuil de stock faible** — Niveau de stock à partir duquel des alertes de stock faible sont envoyées à l'email de l'administrateur (valeur par défaut : 10 unités)

## Intelligence du stock

![carte Intelligence du stock montrant les champs Temps de réapprovisionnement par défaut, Multiplicateur de stock de sécurité, Fenêtre de calcul de vitesse, Autoriser les commandes en rupture de stock par défaut, et Fréquence des alertes de stock faible](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Ces paramètres ajustent les calculs d'approvisionnement automatique, de stock de sécurité et de vitesse de vente, et contrôlent comment les situations de rupture de stock et de stock faible sont gérées.

- **Temps de réapprovisionnement par défaut (jours)** — Combien de jours il faut généralement pour recevoir le réapprovisionnement de votre fournisseur une fois que vous passez commande (valeur par défaut : 14).

La prévision utilise cela pour signaler les produits qui nécessitent une réapprovisionnement *immédiat* afin d'éviter une rupture de stock avant l'arrivée des nouvelles marchandises.
- **Multiplicateur de stock de sécurité** — Une marge appliquée en plus de la demande prévue pour absorber les pics de ventes ou les retards des fournisseurs.

Par exemple, un multiplicateur de `1,5` intègre une marge de 50 % au-dessus de votre stock de sécurité calculé ; `2,0` le double.

Augmentez cette valeur pour les produits dont la rupture est coûteuse (meilleures ventes, articles saisonniers) ; réduisez-la pour les stocks à faible rotation que vous ne souhaitez pas surcommander.
- **Fenêtre de calcul de la vélocité (Jours)** — La fenêtre de référence que Spwig utilise pour calculer la vélocité de vente de chaque produit, ce qui entraîne les suggestions de réapprovisionnement et les chiffres de jours de stock (par défaut : 30).

Une fenêtre plus courte réagit plus rapidement aux récents changements de demande ; une fenêtre plus longue lisse les pics saisonniers afin qu'une seule semaine chargée ne fausse pas la prévision.
- **Autoriser les commandes par défaut** — Le paramètre initial de commande appliqué aux produits nouvellement créés (désactivé par défaut).

Chaque produit peut toujours le modifier individuellement sur sa propre page produit, et les produits existants conservent le paramètre qu'ils ont déjà — modifier cela ne change que la valeur par défaut avec laquelle les nouveaux produits démarrent, cela ne met pas à jour rétroactivement votre catalogue.
- **Fréquence des alertes de stock faible** — La fréquence à laquelle votre application mobile Spwig est notifiée des stocks faibles : **Temps réel** envoie une notification push dès qu'un produit franchit son seuil de stock faible ; **Résumé quotidien** et **Résumé hebdomadaire** envoient à la place une seule notification résumant tous les produits actuellement en stock faible selon ce calendrier.

Ce paramètre ne prend effet que lorsque les **Alertes de stock faible** (Paramètres d'e-mail, ci-dessous) sont activées — avec les alertes désactivées, aucune notification n'est envoyée à aucune fréquence.

### Documents et facturation

![Carte Documents et facturation montrant les champs Identifiant fiscal / Numéro de TVA, Texte de pied de facture, Texte de pied de bon de livraison et Largeur du logo du document remplis avec des valeurs d'exemple](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Ces champs remplissent les factures et les bons de livraison que Spwig génère pour les commandes — par exemple, lorsqu'un marchand télécharge ou envoie par e-mail une facture PDF, ou imprime un bon de livraison pour une expédition.

- **Identifiant fiscal / Numéro de TVA** — Votre numéro d'identification fiscale de l'entreprise. Imprimé sur les factures générées afin qu'elles répondent aux exigences de documentation fiscale locale.
- **Texte de pied de facture** — Texte libre affiché en bas de chaque facture générée. Usages courants : conditions de paiement (« Paiement dû sous 30 jours »), un message de remerciement ou les détails du virement bancaire.
- **Texte de pied de bon de livraison** — Texte libre affiché en bas de chaque bon de livraison généré. Usages courants : instructions de retour ou une note à l'équipe de l'entrepôt/du traitement des commandes.
- **Largeur du logo du document (px)** — La largeur de votre logo de boutique tel qu'il apparaît sur les factures PDF et les bons de livraison générés (par défaut : 200px). La hauteur est mise à l'échelle automatiquement pour correspondre, de sorte que les proportions de votre logo sont préservées. L'image du logo elle-même provient de votre **Logo** (Identité visuelle, ci-dessus) — les logos SVG ne sont pas dessinés sur les documents PDF, donc téléchargez une version PNG ou JPG de votre logo si vous utilisez de l'art vectoriel sur la boutique en ligne.

## Paramètres d'e-mail

Configurez les paramètres de livraison des e-mails dans **Paramètres > Comptes e-mail** et **Paramètres > Modèles d'e-mail**. Voir [Configuration des e-mails](/help/email-configuration) pour tous les détails.

Paramètres d'e-mail clés disponibles dans les Paramètres de la boutique :

- **E-mails de confirmation de commande** — Activer ou désactiver les e-mails de confirmation automatiques
- **E-mails de notification d'expédition** — Activer ou désactiver les notifications de mise à jour de l'expédition
- **Alertes de stock faible** — Envoyer des alertes à l'e-mail administrateur lorsque le stock passe sous le seuil
- **Mode de livraison des e-mails** — En direct (livraison normale), En pause (mettre tous les e-mails en attente) ou Journalisation uniquement (enregistrer mais ne jamais envoyer)
- **E-mail de redirection de test** — Rediriger tous les e-mails sortants vers une seule adresse pour les tests

## Paramètres de sécurité

### Authentification à deux facteurs (2FA)

Contrôlez si le personnel est tenu d'utiliser l'authentification à deux facteurs :


| Paramètre | Description |
|---------|-------------|
| **Facultatif** | Le personnel peut activer la 2FA mais ce n'est pas requis |
| **Recommandé** | Le personnel reçoit une invite les encourageant à activer la 2FA |
| **Obligatoire** | Le personnel ne peut pas accéder à l'administration tant que la 2FA n'est pas activée |

- **Période de grâce (jours)** — Nombre de jours pendant lesquels le personnel doit activer la 2FA après l'activation de l'application
- **Autoriser les appareils fiables** — Permet au personnel de sauter la vérification de la 2FA sur les appareils reconnus pendant un certain nombre de jours

## Consentement aux cookies

Configurez la bannière de consentement aux cookies affichée aux visiteurs du magasin :

- **Consentement aux cookies activé** — Afficher ou masquer la bannière de cookies
- **Position de la bannière** — Emplacement où la bannière apparaît à l'écran (barre inférieure, fenêtre contextuelle, etc.)
- **Mode de consentement** — Avertissement simple, opt-in ou opt-out
- **Titre et texte de la bannière** — En-tête et description personnalisables affichés aux visiteurs
- **Descriptions des catégories** — Descriptions distinctes pour les cookies analytiques, les cookies de marketing et les cookies fonctionnels

Tous les champs de texte de la bannière prennent en charge les traductions pour les magasins multilingues.

## Communications

L'onglet **Communications** gère comment votre magasin obtient, confirme et permet aux clients de gérer le consentement pour les courriels et messages SMS de marketing. Ces paramètres définissent votre posture de conformité légale (RGPD pour les courriels, TCPA pour les SMS), donc veuillez les examiner avec votre propre conseiller juridique avant le lancement — Spwig fournit les contrôles, pas les conseils.

![Onglet Communications montrant les cartes Email Marketing Consent, Preferences & Unsubscribe, et SMS Consent](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentement au marketing par courriel

- **Activer le double opt-in pour les courriels de marketing** — Lorsque activé, un client qui s'inscrit au marketing par courriel reçoit un courriel de confirmation et doit cliquer sur le lien avant que Spwig ne lui envoie un message de marketing. Lorsqu'il est désactivé, cocher la case d'opt-in au marketing suffit. Activé par défaut, conformément aux bonnes pratiques RGPD.
- **État par défaut de l'opt-in au marketing** — L'état initial d'opt-in au marketing appliqué aux nouveaux comptes clients. Désactivé par défaut (RGPD opt-out), donc les nouveaux clients commencent non abonnés aux courriels de marketing jusqu'à ce qu'ils s'abonnent activement.

Lorsque le double opt-in est activé, l'opt-in déclenche un courriel de confirmation avec un lien de vérification. Jusqu'à ce que le client clique dessus, il est enregistré comme ayant opté pour le marketing mais non confirmé, et les envois de marketing les ignorent — les courriels transactionnels (confirmations de commande, mises à jour d'expédition, réinitialisations de mot de passe) ne sont jamais affectés par ce paramètre.

### Préférences & Se désabonner

- **Activer le centre de préférences des clients** — Lorsque activé, les clients peuvent gérer leurs préférences par courriel et SMS depuis une page de service client reliée à leur tableau de bord de compte. Lorsqu'il est désactivé, cette page et son API associée renvoient indisponibles et le lien du tableau de bord est caché. Les liens de désabonnement à un clic dans vos courriels fonctionnent de toute façon — ce dispositif de secours est requis pour la conformité et n'est pas affecté par ce basculement.
- **Collecter les raisons du désabonnement** — Lorsque activé, la page de désabonnement à un clic demande au client une brève raison avant confirmation : *Je reçois trop de courriels*, *Le contenu n'est pas pertinent pour moi*, *Je ne me suis pas inscrit pour cela*, *Je n'ai plus d'intérêt*, ou *Autre*. La raison choisie par le client est enregistrée dans le registre de conformité afin que vous puissiez analyser les schémas de désabonnement au fil du temps.

### Consentement SMS

- **Exiger la vérification SMS** — Lorsque activé (par défaut), un client doit vérifier son numéro de téléphone avec un code à usage unique avant que Spwig ne lui envoie un SMS, y compris les textos de marketing. Lorsqu'il est désactivé, cocher la case d'opt-in SMS suffit à commencer à envoyer. Cette valeur par défaut a été passée à **activé** pour la sécurité TCPA — désactivez-la uniquement si vous avez une autre étape de vérification dans votre flux d'inscription.

## Mode maintenance

Activez le mode maintenance pour rendre votre magasin temporairement hors ligne :
- Affiche un message de maintenance personnalisé aux visiteurs
- Vous pouvez linker une **Page de maintenance** créée dans le constructeur de pages pour une expérience de maintenance pleinement marquée
- Restreint l'accès aux seuls utilisateurs administrateurs
- Utile pendant les mises à jour majeures ou les migrations

## Réseaux sociaux

Liez les profils de réseaux sociaux de votre boutique. Ils apparaissent dans le pied de page et les modèles d'e-mails :

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Paramètres SEO par défaut

Définissez les balises meta par défaut utilisées lorsque les pages n'ont pas leurs propres paramètres SEO :

- **Titre Meta** — Titre de page par défaut (60 caractères max)
- **Description Meta** — Description par défaut affichée dans les résultats de recherche (160 caractères max)
- **Mots-clés Meta** — Mots-clés par défaut séparés par des virgules

## Paramètres de taxe

Configurez la collecte des taxes dans **Paramètres > Paramètres de taxe** :

1. **Méthode de calcul** — Par adresse de livraison, adresse de facturation ou emplacement de la boutique
2. **Taux de taxe** — Définissez les taux par région et classe de taxe de produit
3. **Affichage des taxes** — Afficher les prix avec taxe, sans taxe, ou les deux

## Conseils

- Définissez votre fuseau horaire correctement avant de traiter des commandes — cela affecte tous les horodatages et rapports.
- Activez l'achat invité pour améliorer les taux de conversion.
- Renseignez votre adresse professionnelle pour des calculs de livraison et de taxe précis.
- Téléchargez à la fois un logo et un favicon pour une expérience professionnelle et marquée.
- Utilisez le moment de création de compte **Après l'achat** pour les meilleurs taux d'inscription.
- Activez l'application de l'authentification à deux facteurs pour le personnel afin de protéger l'administration de votre boutique.
- Testez les flux d'e-mails à l'aide du paramètre **E-mail de redirection de test** avant de passer en production.
- Définissez le **Délai de réapprovisionnement par défaut** pour correspondre à votre fournisseur régulier le plus lent — la prévision de réapprovisionnement applique cette valeur unique à tout votre catalogue, donc penchez du côté des produits ayant le délai le plus long.
- Raccourcissez la **Fenêtre de calcul de la vélocité** si vous organisez des promotions fréquentes ou des réapprovisionnements et souhaitez que la prévision réagisse rapidement aux ventes des derniers jours ; allongez-la pour une vue plus stable et moins sujette aux pics de la demande.
- Si vous activez **Autoriser les commandes en rupture par défaut**, rappelez-vous que cela ne définit que le point de départ pour les produits créés *après* le changement — revisitez les produits existants individuellement si vous souhaitez activer les commandes en rupture pour votre catalogue actuel également.
- Alignez la **Fréquence d'alerte de stock faible** sur la manière dont vous gérez votre stock : **Temps réel** pour les catalogues à forte rotation où chaque risque de rupture nécessite une attention immédiate, **Résumé quotidien** ou **Résumé hebdomadaire** pour éviter la fatigue des alertes sur un catalogue plus large.
- Renseignez votre **Numéro de TVA / Identifiant fiscal** et le texte du pied de page avant que votre première facture réelle ne soit envoyée à un client — les deux champs sont vides par défaut.
- Si votre **Logo** est un SVG, téléchargez également une version PNG ou JPG — la **Largeur du logo du document** n'a aucun effet sur les PDF car Spwig ne peut pas dessiner des graphismes SVG sur les factures et bons de livraison générés.
- Laissez **Activer la double confirmation pour les e-mails marketing** activé à moins que vous n'ayez une raison spécifique de le désactiver — c'est le paramètre par défaut le plus sûr pour le RGPD et il protège votre réputation d'expéditeur en gardant les adresses non vérifiées hors de vos envois marketing.
- Laissez l'**État par défaut de l'opt-in marketing** désactivé. Pré-cocher le consentement marketing pour les nouveaux comptes contrevient à l'exigence d'opt-in du RGPD, même si un client pourrait techniquement décocher la case.
- Ne désactivez pas le **Centre de préférences client** juste pour simplifier votre tableau de bord de compte — sans cela, les clients peuvent toujours se désabonner d'un seul type de message, mais ils perdent la possibilité d'affiner leurs préférences (par exemple, conserver les mises à jour de livraison mais supprimer le bulletin d'information).
- Gardez **Exiger la vérification par SMS** activé à moins que votre processus d'inscription ne confirme déjà les numéros de téléphone d'une autre manière (par exemple, une connexion basée sur SMS) — ce paramètre existe spécifiquement pour vous maintenir dans le respect des règles TCPA.

## Dépannage

**Les modifications n'apparaissent pas sur la boutique :**
- Videz le cache de votre navigateur
- Exécutez un effacement du cache depuis le panneau d'administration
- Vérifiez si le mode maintenance est activé par erreur

**Les e-mails ne sont pas envoyés :**
- Vérifiez les paramètres de votre fournisseur d'e-mails dans la Configuration des e-mails
- Vérifiez que le **Mode de livraison des e-mails** est défini sur **En direct**
- Assurez-vous que l'**E-mail de redirection de test** est vide si vous souhaitez que les e-mails soient envoyés à de vrais destinataires

**La conversion de devise ne fonctionne pas :**
- Vérifiez que votre fournisseur de taux de change est connecté
- Vérifiez les identifiants API dans les paramètres du taux de change
- Essayez de mettre à jour manuellement les taux

**Les e-mails marketing n'atteignent pas les clients ayant souscrit :**
- Vérifiez si **Activer la double validation pour les e-mails marketing** est activé - si c'est le cas, le client doit cliquer sur le lien de confirmation dans le courriel de vérification avant que les e-mails marketing ne reprennent
- Demandez au client de vérifier s'il y a des e-mails indésirables/indésirables pour le courriel de vérification
- Confirmez que l'option d'abonnement marketing du client est toujours activée dans ses préférences - un clic de désabonnement la désactive à nouveau

**Les clients disent ne pas trouver le centre de préférences :**
- Vérifiez que **Activer le centre de préférences des clients** est activé - lorsqu'il est désactivé, le lien du tableau de bord est masqué et la page n'est pas disponible par conception
- Le lien de désabonnement dans n'importe quel e-mail marketing fonctionne toujours, quel que soit ce paramètre, donc orientez les clients vers celui-ci en tant que solution de secours