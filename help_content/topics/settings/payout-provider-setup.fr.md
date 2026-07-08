---
title: Configuration des fournisseurs de paiement
---

La configuration des fournisseurs de paiement vous permet de configurer PayPal et Airwallex pour des paiements d'affiliés automatisés. Ce guide vous montre comment connecter vos comptes de fournisseurs de paiement, configurer les webhooks et tester votre intégration.

## Fournisseurs de paiement pris en charge

Spwig s'intègre à deux fournisseurs de paiement pour automatiser les paiements d'affiliés:

| Fournisseur | Méthode de paiement | Traitement | Prise en charge des lots | Meilleur pour |
|----------|----------------|------------|---------------|----------|
| **PayPal** | Transferts via un compte PayPal | Basé sur l'API | Oui (jusqu'à 15 000) | La plupart des affiliés, portée mondiale |
| **Airwallex** | Transferts bancaires internationaux | Basé sur l'API | Non (individuel) | Transferts bancaires, paiements internationaux |

### Différences clés

**Paiements PayPal**:
- Nécessite que l'affilié ait un compte PayPal (adresse e-mail de paiement)
- Traite des lots jusqu'à 15 000 paiements à la fois
- Traitement plus rapide (1 à 2 jours ouvrés)
- Complexité de configuration plus faible
- Frais: ~2 % ou 0,25 $ à 1,00 $ par paiement
- Un seul webhook pour l'ensemble du lot

**Airwallex**:
- Prend en charge les transferts bancaires directs
- Traite les paiements individuels un par un
- Traitement plus long (2 à 5 jours ouvrés)
- Prend en charge plusieurs devises et pays
- Frais varient selon le pays de destination
- Webhook individuel par paiement

Vous pouvez configurer les deux fournisseurs et permettre aux affiliés de choisir leur méthode de paiement préférée.

## Pourquoi utiliser des fournisseurs de paiement ?

L'intégration de fournisseurs de paiement offre des avantages significatifs par rapport aux paiements manuels:

- **Traitement automatisé** — Aucune saisie de données manuelle ou exécution de paiement
- **Efficacité des lots** — Traitez des dizaines ou des centaines de paiements avec un seul clic
- **Confirmations via webhook** — Mises à jour automatiques du statut lors de la complétion des paiements
- **Réduction des erreurs** — Le système valide les détails du compte avant le traitement
- **Traçabilité des audits** — Enregistrement complet des transactions et des réponses du fournisseur
- **Paiements plus rapides** — Les affiliés reçoivent les fonds plus rapidement
- **Évolutivité** — Gérez des programmes d'affiliés en croissance sans travail administratif proportionnel

Sans l'intégration du fournisseur, vous devez traiter chaque paiement manuellement via votre banque ou le tableau de bord PayPal, puis revenir à Spwig pour marquer les paiements comme terminés.

## Configuration de PayPal

Suivez ces étapes pour configurer les paiements PayPal pour des paiements d'affiliés automatisés.

### Prérequis

Avant de commencer, vous avez besoin de:
- Un compte PayPal Business (les comptes personnels ne peuvent pas utiliser l'API de paiement)
- Accès au tableau de bord du développeur PayPal
- Approbation en production pour l'API de paiement (après les tests en sandbox)

### Étape 1: Créer une application PayPal

1. **Accédez** à [Tableau de bord du développeur PayPal](https://developer.paypal.com/dashboard/)
2. **Connectez-vous** avec votre compte PayPal Business
3. **Cliquez** sur **Mes applications et mes identifiants** dans le menu de gauche
4. **Sélectionnez** l'onglet **En production** (ou Sandbox pour les tests)
5. **Cliquez** sur **Créer une application**
6. **Entrez le nom de l'application** (par exemple, "Paiements d'affiliés Spwig")
7. **Sélectionnez le type d'application** : Marchand
8. **Cliquez** sur **Créer une application**

PayPal génère vos identifiants.

### Étape 2: Obtenir les identifiants API

Après avoir créé l'application:

1. **Copiez l'ID client** — Chaîne alphanumérique longue
2. **Cliquez** sur **Afficher** sous Secret
3. **Copiez le secret client** — Gardez-le confidentiel
4. **Notez le mode** — Sandbox ou En production

### Étape 3: Activer la fonctionnalité de paiement

Les applications PayPal nécessitent une autorisation explicite pour utiliser les paiements:

1. **Faites défiler** jusqu'à la section **Fonctionnalités** de votre application
2. **Trouvez** la fonctionnalité **Paiements**
3. **Cliquez** sur **Ajouter** si elle n'est pas déjà activée
4. **Soumettez pour approbation** si vous utilisez le mode En production (l'approbation prend 1 à 2 jours ouvrés)

### Étape 4: Ajouter le fournisseur dans Spwig

Ajoutez maintenant le compte PayPal à Spwig:

1. **Accédez** à **Paramètres > Fournisseurs de paiement**
2. **Cliquez** sur **+ Ajouter un compte PayPal**
3. **Remplissez le formulaire**:
   - **Nom du compte** : Étiquette descriptive (par exemple, "Compte PayPal principal")
   - **ID client** : Coller depuis le tableau de bord du développeur PayPal
   - **Secret client** : Coller depuis le tableau de bord du développeur PayPal
   - **Mode** : Sélectionnez Sandbox (test) ou Production (en production)
   - **Actif** : Cochez pour activer
4. **Cliquez sur Enregistrer**

Spwig valide les identifiants en demandant un jeton d'accès. Si la validation échoue, vérifiez à nouveau votre ID client et votre secret.

### Étape 5: Tester la connexion

Vérifiez votre intégration PayPal:

1. Créez un paiement de test dans **Programme d'affiliation > Paiements**
2. Utilisez votre propre adresse e-mail PayPal comme destinataire
3. Définissez le montant à 0,01 $ (si en production) ou tout montant (si Sandbox)
4. Traitez avec le fournisseur
5. Vérifiez le compte PayPal pour le paiement entrant
6. Vérifiez les mises à jour du webhook sur le statut du paiement dans Spwig

Si vous utilisez le mode Sandbox, créez un compte PayPal de test à [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) pour recevoir des paiements de test.

## Configuration d'Airwallex

Airwallex prend en charge les transferts bancaires internationaux pour les affiliés qui préfèrent le dépôt direct.

### Prérequis

Avant de commencer, vous avez besoin de:
- Un compte Airwallex (créer à [airwallex.com](https://www.airwallex.com))
- Statut de compte professionnel vérifié
- Accès API activé (contactez le support Airwallex si nécessaire)
- Solde suffisant dans votre compte Airwallex

### Étape 1: Générer les identifiants API

1. **Connectez-vous** à [Tableau de bord d'Airwallex](https://www.airwallex.com/app/)
2. **Accédez** à **Paramètres > Clés API**
3. **Cliquez** sur **Créer une clé API**
4. **Entrez une description** : "Paiements d'affiliés Spwig"
5. **Sélectionnez les permissions** : Activez **Paiements** (lecture et écriture)
6. **Cliquez** sur **Générer**
7. **Copiez la clé API** — Affichée une seule fois
8. **Copiez l'ID client** — Affiché avec la clé

### Étape 2: Notez votre environnement

Airwallex fournit deux environnements:

- **Démo** : Pour les tests avec des transactions fictives
- **Production** : Pour les transferts d'argent réels

Assurez-vous de savoir à quel environnement appartient votre clé API.

### Étape 3: Ajouter le fournisseur dans Spwig

Ajoutez le compte Airwallex à Spwig:

1. **Accédez** à **Paramètres > Fournisseurs de paiement**
2. **Cliquez** sur **+ Ajouter un compte Airwallex**
3. **Remplissez le formulaire**:
   - **Nom du compte** : Étiquette descriptive (par exemple, "Compte Airwallex EUR")
   - **Clé API** : Coller depuis le tableau de bord d'Airwallex
   - **ID client** : Coller depuis le tableau de bord d'Airwallex
   - **Environnement** : Sélectionnez Démo ou Production
   - **Actif** : Cochez pour activer
4. **Cliquez sur Enregistrer**

Spwig valide les identifiants en interrogeant votre solde de compte.

### Étape 4: Vérifier les pays pris en charge

Airwallex prend en charge les transferts vers de nombreux pays mais pas tous. Vérifiez la page [Couverture Airwallex](https://www.airwallex.com/global-business-account/global-transfers) pour confirmer que les pays de vos affiliés sont pris en charge.

Les pays couramment pris en charge incluent:
- États-Unis
- Royaume-Uni
- Pays de l'Union européenne
- Australie
- Canada
- Singapour
- Hong Kong

### Étape 5: Tester le transfert bancaire

Testez votre intégration Airwallex:

1. Créez un paiement de test pour un affilié avec des détails bancaires
2. Utilisez un petit montant (1 à 5 $) si vous êtes en mode Production
3. Traitez avec le fournisseur
4. Vérifiez le tableau de bord Airwallex pour la transaction
5. Attendez la confirmation du webhook
6. Vérifiez que le paiement est terminé dans Spwig

Le mode Démo traite instantanément. Le mode Production prend 2 à 5 jours ouvrés.

## Logique de sélection du fournisseur

Lorsque vous traitez un paiement, Spwig sélectionne automatiquement le fournisseur approprié en fonction de la méthode de paiement de l'affilié.

### Flux de sélection

1. **Vérifiez la méthode de paiement de l'affilié**:
   - Si `payment_email` est défini → L'affilié préfère PayPal
   - Si des détails bancaires sont définis → L'affilié préfère le transfert bancaire
2. **Correspondre au fournisseur**:
   - E-mail PayPal → Utiliser le compte de fournisseur PayPal actif
   - Détails bancaires → Utiliser le compte de fournisseur Airwallex actif
3. **Revenir au premier disponible** si le fournisseur préféré n'est pas configuré
4. **Afficher une erreur** si aucun fournisseur correspondant n'existe

### Plusieurs comptes de fournisseur

Vous pouvez configurer plusieurs comptes pour le même fournisseur (par exemple, deux comptes PayPal pour différentes régions). Spwig sélectionne le premier compte actif qui correspond à la méthode de paiement. Pour contrôler quel compte est utilisé, réordonnez-les dans la liste d'administration ou définissez uniquement un compte comme actif.

## Test de l'intégration des paiements

Testez toujours votre intégration de fournisseur avant de traiter des paiements réels aux affiliés.

### Test en mode Sandbox/Demo

1. **Définissez le fournisseur en mode sandbox** (PayPal Sandbox ou Airwallex Demo)
2. **Créez un affilié de test** avec des détails de paiement de test
3. **Créez des commissions de test** et approuvez-les
4. **Créez un paiement de test** incluant ces commissions
5. **Traitez avec le fournisseur** en utilisant le menu d'action
6. **Surveillez les journaux Celery** pour les requêtes API
7. **Vérifiez le tableau de bord du fournisseur** pour la transaction
8. **Attendez la confirmation du webhook** pour mettre à jour le statut du paiement
9. **Vérifiez que les commissions sont marquées comme payées**

### Test en production

Avant de passer en production:

1. **Activez le mode production** dans les paramètres du fournisseur
2. **Créez un petit paiement de test** à vous-même (0,01 $ à 1,00 $)
3. **Traitez-le** et attendez la complétion
4. **Vérifiez que les fonds ont été reçus** dans votre propre compte
5. **Vérifiez que le webhook a été déclenché** et que le statut a été mis à jour
6. **Révisez les frais de transaction du fournisseur**

### Problèmes courants lors des tests

| Problème | Cause | Solution |
|-------|-------|----------|
| "Identifiants invalides" | Mauvaise clé API ou mode non correspondant | Vérifiez à nouveau les identifiants, vérifiez le mode sandbox vs production |
| Webhook ne se déclenche jamais | URL non configurée dans le fournisseur | Ajoutez l'URL du webhook dans le tableau de bord du fournisseur |
| Paiement reste en traitement | Échec de la signature du webhook | Vérifiez que le secret du webhook correspond |
| Aucun fournisseur disponible | Aucun fournisseur actif pour la méthode de paiement | Activez au moins un compte de fournisseur |

## Traitement par lots (PayPal)

PayPal prend en charge le traitement par lots pour l'efficacité et l'économie de coûts.

### Fonctionnement du traitement par lots

Lorsque vous sélectionnez plusieurs paiements et cliquez sur **Traiter avec le fournisseur**:

1. Spwig groupe tous les paiements PayPal dans un seul lot
2. Le système envoie une seule demande API avec tous les détails des paiements (jusqu'à 15 000)
3. PayPal traite l'ensemble du lot comme une seule transaction
4. Le webhook renvoie avec les résultats du lot
5. Spwig met à jour tous les paiements en fonction de la réponse du lot

### Avantages du traitement par lots

- **Réduction des appels API** — Une demande pour des centaines de paiements
- **Frais réduits** — Certaines structures de frais de PayPal favorisent le traitement par lots
- **Traitement plus rapide** — Exécution parallèle pour l'ensemble du lot
- **Un seul webhook** — Plus facile à surveiller et à logger

### Limites de traitement par lots

PayPal impose ces limites:
- Maximum 15 000 destinataires par lot
- Maximum 100 000 $ au total par lot
- Le traitement se termine généralement en quelques minutes

Si vous dépassez 15 000 paiements, Spwig divise automatiquement en plusieurs lots.

## Traitement individuel (Airwallex)

Airwallex traite les paiements un par un, ce qui apporte des compromis différents.

### Fonctionnement du traitement individuel

Lorsque vous traitez les paiements Airwallex:

1. Le système envoie une demande API séparée pour chaque paiement
2. Airwallex file les transferts individuellement
3. Chaque transfert se termine indépendamment (2 à 5 jours)
4. Un webhook individuel se déclenche lors de la complétion de chaque transfert
5. Spwig met à jour les paiements à mesure que les webhooks arrivent

### Avantages du traitement individuel

- **Meilleure isolation des erreurs** — Une erreur ne bloque pas les autres
- **Suivi par paiement** — Identifiants de transaction individuels
- **Plus de détails de paiement** — Informations spécifiques à la banque par transfert
- **Timing flexible** — Les transferts se terminent à des vitesses différentes

### Durée de traitement

Contrairement au traitement par lots instantané de PayPal, les transferts Airwallex prennent plus de temps:
- Transferts nationaux : 1 à 2 jours ouvrés
- Transferts internationaux : 3 à 5 jours ouvrés
- Certains pays : Jusqu'à 7 jours ouvrés

Ajustez les attentes des affiliés en conséquence dans les termes de votre programme.

## Configuration des webhooks

Les webhooks permettent des mises à jour automatiques du statut des paiements lorsque les fournisseurs terminent les transactions.

### Format de l'URL du webhook

Configurez cette URL dans le tableau de bord de votre fournisseur:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Remplacez `{provider}` par:
- `paypal` pour les webhooks PayPal
- `airwallex` pour les webhooks Airwallex

Exemples:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Configuration du webhook PayPal

1. **Accédez** à [Tableau de bord du développeur PayPal](https://developer.paypal.com/dashboard/)
2. **Cliquez** sur le nom de votre application
3. **Faites défiler** jusqu'à la section **Webhooks**
4. **Cliquez** sur **Ajouter un webhook**
5. **Entrez l'URL du webhook** (format ci-dessus)
6. **Sélectionnez les événements**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Cliquez sur Enregistrer**

PayPal fournit une clé de signature du webhook. Spwig utilise celle-ci pour vérifier l'authenticité du webhook.

### Configuration du webhook Airwallex

1. **Accédez** à [Tableau de bord d'Airwallex](https://www.airwallex.com/app/)
2. **Allez à** **Paramètres > Webhooks**
3. **Cliquez** sur **Créer un webhook**
4. **Entrez l'URL du webhook** (format ci-dessus)
5. **Sélectionnez les événements**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Cliquez sur Créer**

Airwallex signe les webhooks avec votre secret API.

### Sécurité des webhooks

Les webhooks sont validés à l'aide de ces mécanismes:

- **Vérification de la signature** — Le fournisseur signe le payload du webhook avec une clé secrète
- **Vérification de l'horodatage** — Rejette les webhooks anciens (prévention des attaques de répétition)
- **Liste blanche des adresses IP** (optionnelle) — Restreindre aux plages d'IP du fournisseur
- **HTTPS obligatoire** — Les webhooks ne fonctionnent qu'en SSL

Ne désactivez jamais la vérification de la signature en production.

### Test des webhooks

La plupart des fournisseurs proposent des outils de test des webhooks:

**PayPal** : Utilisez le "Simulateur" dans le tableau de bord du développeur pour déclencher des webhooks de test

**Airwallex** : Créez un transfert de test en mode Démo et observez le webhook

Vous pouvez également vérifier les journaux des webhooks dans Spwig à **Paramètres > Journaux du système** (si le journal est activé).

## Dépannage

### Erreur d'identifiants invalides

**Symptôme** : "Authentification échouée" lors de l'enregistrement du compte du fournisseur

**Causes**:
- ID client ou secret incorrect
- Identifiants de sandbox utilisés en mode production (ou inversement)
- Clé API expirée ou révoquée
- Compte non vérifié

**Solutions**:
- Recopiez les identifiants depuis le tableau de bord du fournisseur
- Vérifiez que le mode correspond (sandbox vs production)
- Regénérez les clés API
- Contactez le support du fournisseur pour vérifier le statut du compte

### Webhook non reçu

**Symptôme** : Le paiement reste en statut "En traitement" indéfiniment

**Causes**:
- URL du webhook non configurée dans le tableau de bord du fournisseur
- Certificat SSL invalide
- Pare-feu bloquant les adresses IP du fournisseur
- Échec de la validation de la signature du webhook

**Solutions**:
- Vérifiez à nouveau l'URL du webhook dans les paramètres du fournisseur
- Vérifiez que le certificat SSL est valide
- Autorisez les plages d'IP du fournisseur dans le pare-feu
- Vérifiez les journaux Celery pour les erreurs de signature
- Testez le webhook avec l'outil de simulateur du fournisseur

### Paiement échoué

**Symptôme** : Le statut du paiement change en "Échoué" avec un message d'erreur

**Causes**:
- Détails de paiement de l'affilié invalides (e-mail ou compte bancaire incorrect)
- Solde insuffisant sur le compte du fournisseur
- Compte du destinataire ne peut pas recevoir de paiements
- Pays non pris en charge (Airwallex)
- Paiement dépasse les limites du fournisseur

**Solutions**:
- Vérifiez l'erreur dans le champ **Réponse du fournisseur**
- Vérifiez que les détails de paiement de l'affilié sont corrects
- Ajoutez des fonds au compte du fournisseur
- Demandez à l'affilié de vérifier le statut de son compte
- Vérifiez le support de pays et de devises du fournisseur
- Divisez les paiements importants s'ils dépassent les limites

### Mismatch de mode

**Symptôme** : Les paiements de test fonctionnent mais les paiements en production échouent

**Causes**:
- Fournisseur configuré en mode Sandbox mais utilisant des comptes d'affiliés en production
- Clés API provenant d'un environnement incorrect

**Solutions**:
- Changez le mode du fournisseur en Production
- Regénérez les clés API en production
- Vérifiez que l'URL du webhook pointe vers le domaine de production

## Bonnes pratiques de sécurité

Protégez votre intégration de paiement avec ces mesures de sécurité:

### Stockage des identifiants

- **Ne committez jamais les identifiants dans le contrôle de version** — Utilisez des variables d'environnement ou un stockage sécurisé
- **Renouvelez les clés API trimestriellement** — Générez de nouvelles clés toutes les 3 mois
- **Utilisez des clés séparées pour le sandbox et la production** — Ne mélangez jamais les environnements
- **Limitez les permissions API** — Accordez uniquement l'accès aux paiements, pas un contrôle complet du compte

Spwig stocke les identifiants des fournisseurs chiffrés dans la base de données. Gardez vos sauvegardes de base de données sécurisées.

### Sécurité des webhooks

- **Vérifiez toujours les signatures** — Ne sautez jamais la validation des signatures
- **Utilisez exclusivement HTTPS** — Les webhooks HTTP ne sont pas pris en charge
- **Implémentez une liste blanche des adresses IP** — Restreignez les webhooks aux plages d'IP du fournisseur
- **Journalisez tous les webhooks** — Surveillez les activités suspectes
- **Limitez le taux des points de terminaison de webhook** — Empêchez l'abus

### Contrôle d'accès

- **Limitez l'accès du personnel** — Seuls les employés de confiance doivent traiter les paiements
- **Utilisez l'authentification à deux facteurs** — Exigez la 2FA pour les comptes du personnel
- **Auditez les actions de paiement** — Révisez qui a traité quels paiements
- **Séparez les responsabilités** — Différents employés pour l'approbation vs le traitement

### Surveillance

- **Vérifiez quotidiennement les paiements échoués** — Résolvez les problèmes rapidement
- **Surveillez les soldes des comptes fournisseurs** — Assurez-vous qu'il y a suffisamment de fonds
- **Révisez les journaux de transactions hebdomadaires** — Détectez les anomalies tôt
- **Configurez des alertes** — Notifications par e-mail pour les paiements importants ou échoués

## Conseils

- Testez votre intégration en détail en mode sandbox avant de passer en production — détectez les problèmes avec de l'argent fictif.
- Configurez à la fois PayPal et Airwallex pour donner aux affiliés le choix de leur méthode de paiement — différents affiliés préfèrent différentes méthodes.
- Configurez les URLs des webhooks lors de la mise en place initiale et vérifiez qu'elles se déclenchent correctement — les webhooks sont essentiels pour l'automatisation.
- Gardez les soldes des comptes fournisseurs suffisamment alimentés pour éviter les paiements échoués lors du traitement par lots.
- Utilisez des noms de comptes descriptifs si vous configurez plusieurs fournisseurs (par exemple, "PayPal USD", "PayPal EUR").
- Renouvelez les identifiants API toutes les trois mois en tant que bonne pratique de sécurité.
- Documentez vos URLs des webhooks et vos identifiants dans un gestionnaire de mots de passe sécurisé partagé avec votre équipe.
- Surveillez immédiatement les paiements échoués — les retards frustrent les affiliés et abîment la réputation du programme.
- Utilisez toujours HTTPS pour votre installation Spwig — les webhooks nécessitent des certificats SSL.
- Contactez le support du fournisseur si vous rencontrez des erreurs persistantes — ils peuvent vérifier le statut de votre compte et vos autorisations.