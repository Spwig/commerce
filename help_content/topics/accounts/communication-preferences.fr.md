---
title: Préférences de communication
---

Les préférences de communication permettent aux clients de contrôler les e-mails et messages SMS qu'ils reçoivent de votre magasin. Ce système garantit la conformité RGPD et vous aide à respecter les préférences de communication des clients sur tous les canaux.

Accédez à **Clients > Préférences de communication** dans la barre latérale d'administration pour gérer les préférences de communication des clients.

## Comprendre les préférences de communication

Le système de préférences de communication permet aux clients de contrôler précisément les messages qu'ils reçoivent. Cela comprend :

- **E-mails transactionnels** — Confirmations de commande, mises à jour d'expédition, e-mails de sécurité de compte (toujours activés)
- **E-mails marketing** — Lettres d'information, promotions, recommandations de produits (nécessite une validation d'opt-in)
- **Notifications spécifiques à l'application** — Articles de blog, points de fidélité, récompenses de parrainage, commissions d'associé
- **Notifications par SMS** — Notifications par message texte (nécessite une validation d'opt-in explicite selon le TCPA)

Toutes les communications marketing nécessitent la permission du client et la vérification par courriel pour garantir la conformité RGPD.

## Explication des types de préférences

### Communications transactionnelles (toujours activées)

Les messages transactionnels sont essentiels pour le compte et les commandes de votre client. Ces **ne peuvent pas être désactivés** par les clients :

| Type | Description | Exemples |
|------|-------------|----------|
| **Confirmations de commande** | Confirmation lors de la passation de commande | La commande #12345 a été reçue |
| **Mises à jour d'expédition** | Notifications lors du changement de statut de commande | Votre commande a été expédiée |
| **Confirmations de paiement** | Paiement reçu, remboursement traité | Paiement de 49,99 $ confirmé |
| **Sécurité du compte** | Réinitialisation de mot de passe, vérification par courriel | Réinitialisez votre mot de passe |

### Communications marketing (opt-in requis)

Les messages marketing nécessitent la permission du client et la vérification par courriel :

| Type | Description | Valeur par défaut |
|------|-------------|------------------|
| **Newsletter** | Lettres d'information et mises à jour générales | Option de désactivation |
| **Offres promotionnelles** | Ventes, remises, offres spéciales | Option de désactivation |
| **Recommandations de produits** | Suggestions de produits personnalisées | Option de désactivation |
| **Produit de retour en stock** | Notifications lors du retour des produits | Option de désactivation |

Les clients doivent **vérifier leur adresse courriel** avant de recevoir des e-mails marketing (exigence RGPD de double opt-in).

### Préférences spécifiques à l'application

Les clients peuvent contrôler les notifications provenant de fonctionnalités spécifiques :

**Notifications de blog**
- Nouvel article de blog publié (immédiat, résumé hebdomadaire ou mensuel)
- Abonnements aux catégories spécifiques
- Préférences de fréquence

**Programme de fidélité**
- Notifications de points gagnés
- Passage de niveau
- Récompenses déverrouillées
- Points bientôt expirants
- Cadeaux d'anniversaire
- Offres de campagne

**Programme de parrainage**
- Récompense octroyée (parrain et parrainé)
- Inscription réussie au parrainage
- Récompense bientôt expirante
- Invitations de parrainage

**Programme d'associé**
- Commission gagnée
- Approbation ou rejet de la commission
- Paiement traité, achevé ou échoué
- Rapports mensuels sur les performances

### Notifications par SMS (opt-in explicite requis)

Toutes les notifications par SMS nécessitent un **opt-in explicite** selon les réglementations TCPA. Les clients doivent cocher la case d'opt-in SMS activement :

- **SMS transactionnels** — Commande expédiée, livrée (opt-in requis)
- **SMS marketing** — Promotions, offres spéciales (opt-in séparé requis)

Même les SMS transactionnels nécessitent un opt-in, car l'envoi de messages texte non sollicités est plus réglementé que le courriel.

## Gestion des préférences des clients dans l'administration

### Affichage de toutes les préférences

Accédez à **Clients > Préférences de communication** pour voir toutes les préférences des clients :

| Colonne | Description |
|--------|-------------|
| **E-mail de l'utilisateur** | Adresse e-mail du client (lien vers l'administration utilisateur) |
| **Statut de l'e-mail** | Vert ✓ si les e-mails sont activés, gris ○ si désactivés |
| **Statut du SMS** | Vert ✓ si les SMS sont activés, gris ○ si désactivés |
| **Statut du marketing** | Badge « Inscrit » ou « Désinscrit » |
| **Statut de vérification** | 📧✓ si l'e-mail est vérifié, 📱✓ si le SMS est vérifié |
| **Source du consentement** | Lieu où le client a donné son consentement (inscription, paiement, centre de préférences) |
| **Mis à jour le** | Dernière modification des préférences |

### Filtrage des préférences

Utilisez la barre latérale de filtres pour trouver des clients :

- **E-mail activé** — Oui/Non
- **SMS activé** — Oui/Non
- **Marketing par e-mail** — Oui/Non (inscrit au marketing par e-mail)
- **Marketing par SMS** — Oui/Non (inscrit au marketing par SMS)
- **E-mail vérifié** — Oui/Non (a vérifié son adresse e-mail)
- **SMS vérifié** — Oui/Non (a vérifié son numéro de téléphone)
- **Source du consentement** — Inscription, Paiement, Centre de préférences, API, Migration
- **Code de langue** — Langue préférée pour les communications

### Recherche des préférences

Recherchez des clients par :
- E-mail de l'utilisateur
- Nom d'utilisateur
- Prénom
- Nom
- Jeton de désinscription

### Actions groupées

Sélectionnez plusieurs clients et appliquez des actions groupées :

**✓ Marquer l'e-mail comme vérifié**
- Vérifier manuellement les adresses e-mail des clients
- Utile lors de l'importation de clients depuis un autre système
- Invalide le cache des préférences pour appliquer les modifications immédiatement

**🚫 Désinscrire de tout le marketing**
- Désactive toutes les communications marketing (e-mail, SMS, toutes les applications)
- Conserve les e-mails transactionnels activés
- À utiliser pour les clients qui demandent à être entièrement désinscrits
- Respecte le droit au retrait du consentement au titre du RGPD

**📥 Exporter les préférences vers CSV**
- Exporter les préférences des clients vers un tableur
- Inclut tous les champs de préférences et les paramètres spécifiques aux applications
- Utile pour les audits de conformité et l'analyse
- Format : CSV avec en-têtes

## Centre de préférences en libre-service pour les clients

Les clients peuvent gérer leurs propres préférences sur `/accounts/preferences/` lorsqu'ils sont connectés.

### Fonctionnalités du centre de préférences

**Actions rapides**
- **S'abonner à tout le marketing** — Activer toutes les communications marketing en un clic
- **Se désinscrire de tout** — Désactiver toutes les communications marketing (les e-mails transactionnels restent activés)

**Cartes de préférences**
- **E-mails transactionnels** — Lecture seule (toujours activés, marqués comme « Obligatoire »)
- **Communications marketing** — Activation/désactivation avec badge de vérification
- **Préférences du blog** — Activer/désactiver, sélectionner la fréquence (immédiate, hebdomadaire, mensuelle)
- **Programme de fidélité** — Activer/désactiver les types de notifications individuels
- **Programme de parrainage** — Activer/désactiver les notifications de récompenses
- **Programme d'affiliation** — Activer/désactiver les notifications de commissions et de paiements
- **Notifications SMS** — S'inscrire/se désinscrire des SMS (affiche le statut de vérification)

**Mises à jour en temps réel**
- Les modifications sont enregistrées immédiatement via AJAX
- Aucun rechargement de page requis
- Retour visuel lors de l'enregistrement

### Processus de vérification de l'e-mail

Lorsqu'un client active les e-mails marketing :

1. Le client active « E-mails marketing »
2. Le système envoie un e-mail de vérification avec un lien unique
3. Le client clique sur le lien de vérification
4. L'e-mail est marqué comme vérifié (le badge 📧✓ apparaît)
5. Les e-mails marketing seront désormais envoyés

**Les clients non vérifiés ne recevront PAS d'e-mails marketing** même si l'interrupteur est activé. Cela garantit la conformité au double opt-in du RGPD.

## Désinscription en un clic

Tous les e-mails marketing incluent un lien de désinscription dans le pied de page. En cliquant sur ce lien :

1. Le client est redirigé vers `/accounts/unsubscribe/<token>/` (aucune connexion requise)
2. Il voit de quoi il se désinscrit
3. Il peut fournir un retour facultatif (raison de la désinscription)
4. Les communications marketing sont désactivées
5. Les e-mails transactionnels restent activés
6. Un lien vers le centre de préférences complet est fourni

Les clients peuvent se réabonner à tout moment via le centre de préférences.

## Conformité et exigences légales

### Conformité à l'article 7 du RGPD

Le système garantit une conformité complète à l'article 7 du RGPD :


**✅ Preuve du consentement**
- Horodatage du moment où le consentement a été donné
- Source du consentement (inscription, paiement, centre de préférences)
- Adresse IP du consentement
- Agent utilisateur (informations sur le navigateur)

**✅ Consentement séparé**
- Les e-mails marketing et transactionnels sont des options distinctes
- Chaque application (blog, fidélité, etc.) nécessite un consentement individuel

**✅ Retrait facile**
- Désinscription en un clic dans tous les e-mails marketing
- Centre de préférences disponible pour tous les clients connectés
- La désinscription prend effet immédiatement

**✅ Consentement librement donné**
- Par défaut, l'option est désactivée pour le marketing (meilleure pratique RGPD)
- Aucune case pré-cochée (les clients doivent s'inscrire activement)

**✅ Consentement spécifique et éclairé**
- Des descriptions claires de ce que chaque préférence contrôle
- Préférences granulaires au niveau de l'application (pas tout ou rien)

**✅ Consentement vérifiable**
- Double inscription pour les e-mails marketing
- Piste d'audit via le suivi de l'état de la boîte d'envoi (EmailOutbox)

### Conformité TCPA (Réglementations SMS aux États-Unis)

Toutes les notifications SMS nécessitent un **opt-in explicite** :

- Les clients doivent cocher activement la case d'opt-in SMS
- Les cases pré-cochées ne sont pas autorisées
- Description claire de ce à quoi ils s'inscrivent
- Désinscription facile via le centre de préférences
- Tous les envois SMS sont journalisés pour l'audit de conformité

### Conformité CAN-SPAM (Réglementations e-mail aux États-Unis)

Le système assure la conformité CAN-SPAM :

- Lien de désinscription dans chaque e-mail marketing
- Désinscription traitée immédiatement (10 jours ouvrables requis, nous le faisons instantanément)
- Nom "De" clair (le nom de votre boutique)
- Adresse physique dans le pied de page de l'e-mail
- Pas de lignes d'objet trompeuses

## Comprendre l'état des e-mails dans EmailOutbox

Lors de la consultation de **Système d'e-mails > Boîte d'envoi**, vous verrez comment les préférences affectent la livraison des e-mails :

| Statut | Signification | Raison |
|--------|---------|--------|
| **En attente** | E-mail mis en file d'attente pour envoi | Les préférences autorisent cet e-mail |
| **En file d'attente** | Dans la file d'attente d'envoi | Les préférences autorisent cet e-mail |
| **Ignoré** | E-mail non envoyé | Préférence du client désactivée |
| **Envoyé** | Livré avec succès | E-mail envoyé normalement |

Lorsqu'un e-mail est **ignoré**, le champ `skip_reason` indique la raison :

- **user_preference_disabled** — Le client a désactivé ce type d'e-mail dans ses préférences
- **email_not_verified** — Le client n'a pas vérifié son adresse e-mail
- **email_disabled** — Le client a désactivé tous les e-mails (interrupteur principal)

Cette piste d'audit est importante pour la conformité RGPD — vous pouvez prouver que vous avez respecté les préférences des clients.

## Paramètres du site pour les préférences

Accédez à **Paramètres > Paramètres du site** pour configurer les préférences par défaut globales :

**Activer la double inscription pour les e-mails marketing** (Par défaut : Oui)
- Nécessite la vérification de l'e-mail avant l'envoi d'e-mails marketing
- Meilleure pratique RGPD
- Recommandé : Laisser activé

**État d'opt-in marketing par défaut** (Par défaut : Non - Opt-Out)
- État par défaut lors de l'inscription de nouveaux clients
- Le RGPD exige l'opt-out par défaut
- Recommandé : Laisser en opt-out (False)

**Centre de préférences activé** (Par défaut : Oui)
- Permet aux clients de gérer leurs propres préférences
- Requis pour le droit RGPD de retirer le consentement
- Recommandé : Laisser activé

**Exiger la vérification SMS** (Par défaut : Non)
- Exiger la vérification du numéro de téléphone pour les notifications SMS
- Optionnel mais recommandé pour les expéditeurs SMS à fort volume
- Peut être activé si vous souhaitez une double inscription pour les SMS

**Afficher les raisons de désinscription** (Par défaut : Oui)
- Collecter des commentaires facultatifs lorsque les clients se désinscrivent
- Aide à comprendre pourquoi les clients se désinscrivent
- Recommandé : Laisser activé pour les analyses

## Meilleures pratiques

### 1. Opt-Out par défaut pour le marketing

Définissez toujours les communications marketing sur **opt-out** (non coché) par défaut :
- Conforme au RGPD
- Crée la confiance avec les clients
- Réduit les plaintes pour spam
- N'envoyez qu'aux clients engagés

### 2. Exiger la vérification de l'e-mail

Gardez la **double inscription** activée :
- S'assure que les adresses e-mail sont valides
- Confirme que le client souhaite réellement recevoir des e-mails marketing
- Réduit le taux de rebond
- Requis pour la conformité RGPD

### 3. Respecter les préférences immédiatement



Lorsqu'un client modifie ses préférences :
- Les modifications prennent effet immédiatement
- Le cache des préférences est invalidé
- Le prochain envoi d'e-mail vérifiera les préférences mises à jour
- Aucun délai dans le respect des demandes de désinscription

### 4. Surveiller les e-mails ignorés

Vérifiez régulièrement la **Boîte d'envoi des e-mails** pour les e-mails ignorés :
- Un taux d'ignorance élevé indique que les clients se désinscrivent
- Peut signaler que le contenu des e-mails doit être amélioré
- Aide à identifier les problèmes de préférences

### 5. Audits de conformité réguliers

Exportez les préférences périodiquement pour la conformité :
1. Accédez à **Préférences de communication**
2. Sélectionnez tous les clients
3. Choisissez **Exporter les préférences vers CSV**
4. Enregistrez pour la piste d'audit GDPR

Conservez les exports **pendant au moins 3 ans** pour vous conformer aux exigences de conservation des données du RGPD.

### 6. Communication claire

Lors de la collecte du consentement :
- Utilisez un langage simple, pas de jargon juridique
- Expliquez ce que les clients recevront
- Indiquez la fréquence (quotidienne, hebdomadaire, mensuelle)
- Rendez les cases de consentement visibles mais non pré-cochées

### 7. Segmenter par préférence

Lors de l'envoi de campagnes marketing :
- N'envoyez qu'aux clients vérifiés et ayant consenti
- Respectez les préférences spécifiques aux applications (n'envoyez pas d'e-mails de blog aux clients qui ont désactivé le blog)
- Utilisez les préférences de fréquence (n'envoyez pas d'e-mails immédiats aux abonnés du digest hebdomadaire)

## Conseils

**💡 Vérifier les préférences avant l'envoi**

Le système vérifie automatiquement les préférences lorsque vous envoyez des e-mails en utilisant `EmailSendingService.send_template_email()`. Assurez-vous que tous les envois d'e-mails utilisent ce service, et non des appels SMTP directs.

**💡 Le statut ignoré est normal**

Ne vous alarmez pas des e-mails ignorés dans la boîte d'envoi — cela signifie que le système fonctionne correctement et respecte les préférences des clients. Il est préférable d'ignorer les e-mails non désirés que de risquer des amendes RGPD ou des plaintes pour spam.

**💡 Le cache des préférences est de 5 minutes**

Les vérifications de préférences sont mises en cache pendant 5 minutes pour des raisons de performance. Lorsque les clients modifient leurs préférences via le centre de préférences ou des actions administrateur, le cache est immédiatement invalidé pour que les modifications prennent effet immédiatement.

**💡 Les clients invités contournent les vérifications**

Les clients en paiement invité (sans compte) recevront tous les e-mails normalement car ils n'ont pas d'enregistrement de préférences. C'est intentionnel — ils ont consenti en fournissant leur e-mail lors du paiement.

**💡 Les e-mails transactionnels sont toujours envoyés**

Les confirmations de commande, les mises à jour d'expédition et les e-mails de sécurité du compte **sont toujours envoyés** indépendamment des préférences. Cela garantit que les clients reçoivent des informations essentielles sur leurs commandes et leurs comptes.

**💡 Utiliser les actions groupées avec prudence**

L'action groupée « Se désinscrire de tout le marketing » affecte **toutes les applications** (blog, fidélité, parrainage, affiliation). N'utilisez ceci que pour les clients qui ont explicitement demandé à être entièrement désinscrits. Pour des préférences spécifiques, modifiez les enregistrements individuels des clients.

**💡 Piste d'audit pour la conformité**

Le système suit :
- Horodatage et source du consentement
- Adresse IP et agent utilisateur
- Horodatage de la vérification de l'e-mail
- Chaque modification de préférence via le statut ignoré de la Boîte d'envoi des e-mails

Cette piste d'audit prouve la conformité au RGPD si les autorités demandent des preuves de consentement.

## Sujets connexes

- [Gestion des comptes clients](/help/managing-customer-accounts) — Gestion des profils clients
- [Configuration des e-mails](/help/email-configuration) — Configuration SMTP et modèles d'e-mails