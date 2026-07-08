---
title: Préférences de communication
---

Les préférences de communication permettent aux clients de contrôler les e-mails et les messages SMS qu'ils reçoivent de votre magasin. Ce système garantit la conformité au RGPD et vous aide à respecter les préférences de communication des clients sur tous les canaux.

Accédez à **Clients > Préférences de communication** dans le menu latéral d'administration pour gérer les préférences de communication des clients.

## Comprendre les préférences de communication

Le système de préférences de communication donne aux clients un contrôle granulaire sur les messages qu'ils reçoivent. Cela inclut :

- **E-mails transactionnels** — Confirmations essentielles des commandes, mises à jour d'expédition, e-mails de sécurité du compte (toujours activés)
- **E-mails de marketing** — Lettres d'information, promotions, recommandations de produits (nécessite un consentement)
- **Notifications spécifiques à l'application** — Articles de blog, points de fidélité, récompenses de parrainage, commissions d'affiliation
- **Notifications SMS** — Notifications par message texte (nécessite un consentement explicite selon le TCPA)

Toutes les communications de marketing nécessitent le consentement du client et la vérification de l'e-mail pour garantir la conformité RGPD.

## Explication des types de préférences

### Communications transactionnelles (toujours activées)

Les messages transactionnels sont essentiels pour le compte et les commandes de votre client. Ces **ne peuvent pas être désactivés** par les clients :

| Type | Description | Exemples |
|------|-------------|----------|
| **Confirmations de commande** | Confirmation lorsque la commande est passée | La commande #12345 a été reçue |
| **Mises à jour d'expédition** | Notifications lorsque le statut de la commande change | Votre commande a été expédiée |
| **Confirmations de paiement** | Paiement reçu, remboursement traité | Paiement de 49,99 $ confirmé |
| **Sécurité du compte** | Réinitialisation du mot de passe, vérification de l'e-mail | Réinitialisez votre mot de passe |

### Communications de marketing (consentement requis)

Les messages de marketing nécessitent le consentement du client et la vérification de l'e-mail :

| Type | Description | Défaut |
|------|-------------|---------|
| **Lettre d'information** | Lettres d'information et mises à jour générales | Désabonné |
| **Offres promotionnelles** | Ventes, réductions, offres spéciales | Désabonné |
| **Recommandations de produits** | Suggestions de produits personnalisées | Désabonné |
| **Retour en stock** | Notifications lors du retour des produits | Désabonné |

Les clients doivent **vérifier leur adresse e-mail** avant de recevoir tout e-mail de marketing (exigence RGPD de double consentement).

### Préférences spécifiques à l'application

Les clients peuvent contrôler les notifications provenant de fonctionnalités spécifiques :

**Notifications de blog**
- Nouvel article de blog publié (immédiat, résumé hebdomadaire ou mensuel)
- Abonnements spécifiques à la catégorie
- Préférences de fréquence

**Programme de fidélité**
- Notifications sur les points gagnés
- Mises à niveau de niveau
- Récompenses déverrouillées
- Points proches de l'expiration
- Bonus d'anniversaire
- Offres de campagne

**Programme de parrainage**
- Récompense attribuée (parrain et parrainé)
- Inscription réussie de parrainage
- Récompense proche de l'expiration
- Invitations de parrainage

**Programme d'affiliation**
- Commission gagnée
- Commission approuvée ou rejetée
- Paiement traité, terminé ou échoué
- Rapports mensuels de performance

### Notifications SMS (consentement explicite requis)

Toutes les notifications SMS nécessitent un **consentement explicite** selon les réglementations TCPA. Les clients doivent activer la case à cocher de consentement SMS :

- **SMS transactionnels** — Commande expédiée, livrée (consentement requis)
- **SMS de marketing** — Promotions, offres spéciales (consentement séparé requis)

Même les SMS transactionnels nécessitent un consentement car l'envoi de messages texte non sollicités est réglementé plus strictement que l'e-mail.

## Gestion des préférences des clients dans l'administration

### Afficher toutes les préférences

Accédez à **Clients > Préférences de communication** pour voir toutes les préférences des clients :

| Colonne | Description |
|--------|-------------|
| **E-mail utilisateur** | Adresse e-mail du client (lien vers l'administration utilisateur) |
| **Statut e-mail** | ✓ vert si les e-mails sont activés, ○ gris si désactivés |
| **Statut SMS** | ✓ vert si les SMS sont activés, ○ gris si désactivés |
| **Statut marketing** | Étiquette "Opted In" ou "Opted Out" |
| **Statut de vérification** | 📧✓ si l'e-mail est vérifié, 📱✓ si le SMS est vérifié |
| **Source de consentement** | Endroit où le client a donné son consentement (enregistrement, checkout, centre de préférences) |
| **Mis à jour à** | Dernière fois où les préférences ont été modifiées |

### Filtrage des préférences

Utilisez le menu latéral de filtre pour trouver des clients :

- **E-mail activé** — Oui/Non
- **SMS activé** — Oui/Non
- **Marketing par e-mail** — Oui/Non (souscrit au marketing)
- **Marketing par SMS** — Oui/Non (souscrit au marketing par SMS)
- **E-mail vérifié** — Oui/Non (a vérifié son adresse e-mail)
- **SMS vérifié** — Oui/Non (a vérifié son numéro de téléphone)
- **Source de consentement** — Enregistrement, Checkout, Centre de préférences, API, Migration
- **Code de langue** — Langue préférée pour les communications

### Recherche de préférences

Recherchez des clients par :
- E-mail utilisateur
- Nom d'utilisateur
- Prénom
- Nom de famille
- Jeton de désabonnement

### Actions en bloc

Sélectionnez plusieurs clients et appliquez des actions en bloc :

**✓ Marquer l'e-mail comme vérifié**
- Vérifiez manuellement les adresses e-mail des clients
- Utile lors de l'importation de clients depuis un autre système
- Invalide le cache des préférences pour appliquer les changements immédiatement

**🚫 Désabonner de toute la communication marketing**
- Désactive toutes les communications marketing (e-mail, SMS, toutes les applications)
- Garde les e-mails transactionnels activés
- Utilisez cela pour les clients qui souhaitent être entièrement désabonnés
- Respecte le droit RGPD de se désabonner

**📥 Exporter les préférences au format CSV**
- Exporter les préférences des clients vers une feuille de calcul
- Inclut tous les champs de préférences et les paramètres spécifiques à l'application
- Utile pour les audits de conformité et l'analyse
- Format : CSV avec en-têtes

## Centre de préférences de l'utilisateur (auto-service)

Les clients peuvent gérer leurs propres préférences à `/accounts/preferences/` lorsqu'ils sont connectés.

### Fonctionnalités du centre de préférences

**Actions rapides**
- **S'abonner à toute la communication marketing** — Activer toutes les communications marketing en un clic
- **Désabonner de tout** — Désactiver toutes les communications marketing (les e-mails transactionnels restent activés)

**Cartes de préférences**
- **E-mails transactionnels** — En lecture seule (toujours activés, marqués comme "Requis")
- **Communications marketing** — Activer/désactiver avec un badge de vérification
- **Préférences du blog** — Activer/désactiver, sélectionner la fréquence (immédiat, hebdomadaire, mensuel)
- **Programme de fidélité** — Activer/désactiver les types de notifications individuels
- **Programme de parrainage** — Activer/désactiver les notifications de récompenses
- **Programme d'affiliation** — Activer/désactiver les notifications de commission et de paiement
- **Notifications SMS** — S'abonner/désabonner aux SMS (affiche l'état de vérification)

**Mises à jour en temps réel**
- Les changements sont sauvegardés immédiatement via AJAX
- Aucun rechargement de page nécessaire
- Feedback visuel lors de la sauvegarde

### Processus de vérification de l'e-mail

Lorsqu'un client active les e-mails marketing :

1. Le client bascule "E-mails marketing" sur ON
2. Le système envoie un e-mail de vérification avec un lien unique
3. Le client clique sur le lien de vérification
4. L'e-mail est marqué comme vérifié (badge 📧✓ apparaît)
5. Les e-mails marketing seront désormais envoyés

**Les clients non vérifiés ne recevront PAS les e-mails marketing** même si le basculement est sur ON. Cela garantit la conformité RGPD avec le double consentement.

## Désabonnement d'un clic

Tous les e-mails marketing incluent un lien de désabonnement dans le pied de page. En cliquant sur ce lien :

1. Le client est redirigé vers `/accounts/unsubscribe/<token>/` (aucune connexion requise)
2. Affiche ce à quoi le client se désabonne
3. Permet un retour d'information optionnel (raison du désabonnement)
4. Désactive les communications marketing
5. Garde les e-mails transactionnels activés
6. Fournit un lien vers le centre complet des préférences

Les clients peuvent se réabonner à tout moment via le centre de préférences.

## Conformité et exigences légales

### Conformité à l'article 7 du RGPD

Le système garantit une conformité complète à l'article 7 du RGPD :

**✅ Preuve de consentement**
- Horodatage de la date d'accord
- Source du consentement (enregistrement, checkout, centre de préférences)
- Adresse IP du consentement
- User agent (informations du navigateur)

**✅ Consentement séparé**
- Les e-mails marketing et transactionnels sont des basculeurs séparés
- Chaque application (blog, fidélité, etc.) nécessite un consentement individuel

**✅ Désistement facile**
- Désabonnement d'un clic dans tous les e-mails marketing
- Centre de préférences disponible pour tous les clients connectés
- Le désabonnement prend effet immédiatement

**✅ Consentement librement donné**
- État par défaut est désabonné pour le marketing (meilleilleure pratique RGPD)
- Aucune case précochée (les clients doivent activer le consentement)

**✅ Consentement spécifique et informé**
- Descriptions claires de ce que chaque préférence contrôle
- Préférences granulaires au niveau de l'application (pas tout ou rien)

**✅ Consentement vérifiable**
- Double opt-in pour les e-mails marketing
- Journal des transactions via le statut de suivi EmailOutbox

### Conformité au TCPA (règlementations des SMS aux États-Unis)

Toutes les notifications SMS nécessitent un **consentement explicite** :

- Les clients doivent activer la case de consentement SMS
- Aucune case précochée autorisée
- Description claire de ce à quoi ils s'abonnent
- Désabonnement facile via le centre de préférences
- Tous les envois SMS sont enregistrés pour l'audit de conformité

### Conformité au CAN-SPAM (règlementations des e-mails aux États-Unis)

Le système garantit la conformité CAN-SPAM :

- Lien de désabonnement dans chaque e-mail marketing
- Désabonnement traité immédiatement (dans les 10 jours ouvrés requis, nous le faisons instantanément)
- Nom clair dans le champ "De" (le nom de votre boutique)
- Adresse physique dans le pied de page de l'e-mail
- Aucun objet trompeur

## Comprendre l'état des e-mails dans EmailOutbox

Lorsque vous consultez **Système e-mail > Boîte de sortie e-mail**, vous verrez comment les préférences affectent la livraison des e-mails :

| État | Signification | Raison |
|--------|---------|--------|
| **En attente** | E-mail en file d'attente pour l'envoi | Les préférences permettent cet e-mail |
| **En file d'attente** | Dans la file d'envoi | Les préférences permettent cet e-mail |
| **Ignoré** | E-mail non envoyé | Préférence du client désactivée |
| **Envoyé** | Envoyé avec succès | E-mail envoyé normalement |

Quand un e-mail est **ignoré**, le champ `skip_reason` indique pourquoi :

- **user_preference_disabled** — Le client a désactivé ce type d'e-mail dans les préférences
- **email_not_verified** — Le client n'a pas vérifié son adresse e-mail
- **email_disabled** — Le client a désactivé tous les e-mails (bascule principal)

Ce journal des transactions est important pour la conformité RGPD — vous pouvez prouver que vous avez respecté les préférences du client.

## Paramètres du site pour les préférences

Accédez à **Paramètres > Paramètres du site** pour configurer les paramètres de préférences globaux :

**Activer le double opt-in pour les e-mails marketing** (Par défaut : Oui)
- Exige la vérification de l'e-mail avant l'envoi des e-mails marketing
- Meilleure pratique RGPD
- Recommandé : Laissez activé

**État par défaut du consentement marketing** (Par défaut : Non - Désabonné)
- État par défaut lors de l'enregistrement des nouveaux clients
- RGPD exige un désabonnement par défaut
- Recommandé : Laissez comme désabonné (Faux)

**Centre de préférences activé** (Par défaut : Oui)
- Permet aux clients de gérer leurs propres préférences
- Requis pour le droit RGPD de se désabonner
- Recommandé : Laissez activé

**Exiger la vérification du SMS** (Par défaut : Non)
- Exiger la vérification du numéro de téléphone pour les notifications SMS
- Optionnel mais recommandé pour les envoyeurs de SMS à grande échelle
- Peut être activé si vous souhaitez un double opt-in pour le SMS

**Afficher les raisons du désabonnement** (Par défaut : Oui)
- Collecter un retour d'information optionnel lors du désabonnement des clients
- Aide à comprendre pourquoi les clients s'abonnent
- Recommandé : Laissez activé pour des insights

## Bonnes pratiques

### 1. Préférez le désabonnement par défaut pour le marketing

Définissez toujours les communications marketing sur **désabonné** (non cochée) :
- Conforme au RGPD
- Construit la confiance des clients
- Réduit les plaintes contre les spams
- Envoie uniquement aux clients engagés

### 2. Exiger la vérification de l'e-mail

Gardez **Double Opt-In** activé :
- Assure que les adresses e-mail sont valides
- Confirme que le client souhaite réellement recevoir des e-mails marketing
- Réduit le taux de rebond
- Requis pour la conformité RGPD

### 3. Respecter les préférences immédiatement

Lorsqu'un client modifie ses préférences :
- Les changements prennent effet immédiatement
- Le cache des préférences est invalidé
- L'envoi d'e-mail suivant vérifiera les préférences mises à jour
- Aucun délai pour respecter les demandes de désabonnement

### 4. Surveiller les e-mails ignorés

Vérifiez régulièrement **la boîte de sortie des e-mails** pour les e-mails ignorés :
- Un taux d'ignorance élevé indique que les clients s'abonnent
- Peut signaler que le contenu des e-mails a besoin d'amélioration
- Aide à identifier les problèmes de préférences

### 5. Audit de conformité régulier

Exporter les préférences périodiquement pour la conformité :
1. Accédez à **Préférences de communication**
2. Sélectionnez tous les clients
3. Choisissez **Exporter les préférences au format CSV**
4. Enregistrez pour le journal d'audit RGPD

Conservez les exports pendant **au moins 3 ans** pour respecter les exigences de conservation des données RGPD.

### 6. Communication claire

Lors de la collecte de consentement :
- Utilisez un langage simple, pas des termes juridiques
- Expliquez ce que les clients recevront
- Montrez la fréquence (quotidienne, hebdomadaire, mensuelle)
- Mettez en évidence les cases d'abonnement mais ne les précochez pas

### 7. Segmenter par préférences

Lors de l'envoi de campagnes marketing :
- Envoyez uniquement aux clients vérifiés et abonnés
- Respectez les préférences spécifiques aux applications (ne envoyez pas d'e-mails de blog aux clients ayant désactivé le blog)
- Utilisez les préférences de fréquence (ne envoyez pas d'e-mails immédiats aux abonnés de résumé hebdomadaire)

## Conseils

**💡 Vérifiez les préférences avant d'envoyer**

Le système vérifie automatiquement les préférences lors de l'envoi d'e-mails via `EmailSendingService.send_template_email()`. Assurez-vous que tous les envois d'e-mails utilisent ce service et non des appels SMTP directs.

**💡 L'état "Ignoré" est normal**

Ne soyez pas inquiet des e-mails ignorés dans la boîte de sortie — cela signifie que le système fonctionne correctement et respecte les préférences du client. C'est mieux de ne pas envoyer les e-mails non souhaités que de risquer des amendes RGPD ou des plaintes contre les spams.

**💡 Le cache des préférences est de 5 minutes**

Les vérifications de préférences sont mises en cache pendant 5 minutes pour des performances. Lorsque les clients modifient leurs préférences via le centre de préférences ou des actions d'administration, le cache est immédiatement invalidé afin que les changements prennent effet immédiatement.

**💡 Les clients invités contournent les vérifications**

Les clients ayant effectué un achat en tant qu'invités (sans compte) recevront tous les e-mails normalement car ils n'ont aucun enregistrement de préférences. C'est intentionnel — ils se sont abonnés en fournissant leur e-mail lors de la validation.

**💡 Les e-mails transactionnels sont toujours envoyés**

Les confirmations de commande, les mises à jour d'expédition et les e-mails de sécurité du compte **sont toujours envoyés** indépendamment des préférences. Cela garantit que les clients reçoivent des informations critiques sur leurs commandes et comptes.

**💡 Utilisez les actions en bloc avec soin**

L'action en bloc "Désabonner de toute la communication marketing" affecte **toutes les applications** (blog, fidélité, parrainage, affiliation). Utilisez-la uniquement pour les clients qui ont explicitement demandé d'être entièrement désabonnés. Pour des préférences spécifiques, modifiez les enregistrements clients individuellement.

**💡 Journal des transactions pour la conformité**

Le système suit :
- Horodatage et source du consentement
- Adresse IP et user agent
- Horodatage de vérification de l'e-mail
- Chaque modification de préférence via le statut de saut EmailOutbox

Ce journal des transactions prouve la conformité RGPD si les autorités demandent des preuves de consentement.

## Sujets liés

- [Gestion des comptes client](/help/managing-customer-accounts) — Gestion du profil client
- [Configuration des e-mails](/help/email-configuration) — Configuration SMTP et modèles d'e-mails

