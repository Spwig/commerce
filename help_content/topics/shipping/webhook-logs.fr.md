---
title: Journal des Webhooks
---

Les journaux des webhooks fournissent un journal d'audit permanent de toutes les demandes de webhook entrantes des transporteurs — en capturant la méthode de demande, l'URL de point de terminaison, les en-têtes, la charge utile, le statut de traitement (en attente/traité/échoué) et la réponse. Chaque webhook est enregistré avant le traitement pour garantir qu'aucun événement ne soit perdu en cas d'échec du traitement. Les journaux permettent de déboguer les problèmes d'intégration des webhooks, de surveiller la fiabilité des API des transporteurs, et de reconstruire les chronologies de livraison pour le service client.

Cette page d'administration en lecture seule aide à diagnostiquer les échecs des webhooks et à vérifier la santé de l'intégration des transporteurs.

## Structure du Journal des Webhooks

Chaque entrée de journal enregistre :

**Détails de la Demande**:
- **Clé du Fournisseur** : Le transporteur ayant envoyé le webhook (fedex, ups, dhl)
- **Point de Terminaison** : Chemin de l'URL du webhook (ex. `/webhooks/shipping/fedex/`)
- **Méthode** : Méthode HTTP (généralement POST)
- **En-têtes** : En-têtes de la demande (JSON)
- **Charge Utile** : Corps de la demande (JSON)

**Traitement**:
- **Statut de Traitement** : en attente, traité, échoué
- **Message d'Erreur** : Raison de l'échec (si statut=échoué)
- **Réponse** : Réponse HTTP envoyée au transporteur
- **Code de Statut de Réponse** : 200, 400, 500, etc.

**Horodatages**:
- **Reçu à** : Quand le webhook est arrivé
- **Traité à** : Quand le traitement est terminé

---

## Valeurs de Statut de Traitement

**en attente** : Webhook reçu, en attente de traitement
- Normal pour un bref moment après réception
- Si bloqué en attente, indique un arriéré de la file de traitement

**traité** : Webhook traité avec succès
- Événement de suivi créé
- Notification client envoyée (si applicable)
- Réponse 200 envoyée au transporteur

**échoué** : Échec du traitement du webhook
- Vérifiez le champ error_message pour la raison
- Causes courantes : JSON invalide, envoi inconnu, événement en double

---

## Flux des Webhooks

**Workflow Normal**:
```
1. Le transporteur scanne le colis
   ↓
2. Le transporteur envoie un POST à l'endpoint webhook de Spwig
   ↓
3. Spwig crée un WebhookLog (statut=en attente)
   ↓
4. Un worker en arrière-plan traite le webhook
   ↓
5. Analyse la charge utile JSON
   ↓
6. Trouve l'envoi correspondant (par numéro de suivi)
   ↓
7. Crée un Événement de Suivi
   ↓
8. Met à jour le WebhookLog (statut=traité)
   ↓
9. Envoie une réponse HTTP 200 au transporteur
```

**Scénarios d'Échec**:
- **JSON Invalide** : Le transporteur a envoyé des données malformées → statut=échoué, erreur="erreur de parsing JSON"
- **Envoi Inconnu** : Le numéro de suivi ne correspond à aucun envoi → statut=échoué, erreur="Envoi non trouvé"
- **En Double** : Événement déjà existant → statut=échoué, erreur="Événement en double"

---

## Débogage des Échecs des Webhooks

**Étapes à Suivre**:

**1. Filtrez par Statut=Échoué**
- Accédez à Envois > Journal des Webhooks
- Filtre : Statut de Traitement = "échoué"
- Examinez les échecs récents

**2. Vérifiez le Message d'Erreur**
- Cliquez sur l'entrée de journal
- Lisez le champ error_message
- Erreurs courantes :
  - "Envoi non trouvé" → Mismatch du numéro de suivi
  - "Erreur de décodage JSON" → Le transporteur a envoyé un JSON invalide
  - "Champ requis manquant" → Charge utile manque des données attendues

**3. Examinez la Charge Utile**
- Affichez la charge utile JSON brute
- Vérifiez que la structure correspond au format attendu
- Vérifiez l'absence de champs manquants (tracking_id, event_type, etc.)

**4. Vérifiez l'Existence de l'Envoi**
- Extrayez le numéro de suivi de la charge utile
- Recherchez les Envois par numéro de suivi
- Assurez-vous que l'envoi existe et utilise le transporteur correct

**5. Vérifiez la Configuration du Fournisseur**
- Vérifiez que le compte du fournisseur est actif
- Confirmez que l'URL du point de terminaison du webhook est correcte
- Testez les identifiants API du fournisseur

**6. Réessayer le Traitement** (si applicable)
- Certains traiteurs de webhooks supportent un réessai manuel
- Corrigez d'abord le problème sous-jacent
- Réessayez le webhook échoué

---

## Problèmes Courants des Webhooks

**Problème 1 : "Envoi non trouvé"**

**Cause** : Le numéro de suivi du webhook ne correspond à aucun envoi
- Faute de frappe lors de la création de l'envoi
- Webhook pour un autre compte
- Envoi supprimé avant réception du webhook

**Solution**:
- Vérifiez l'orthographe du numéro de suivi
- Vérifiez que le transporteur de l'envoi correspond au fournisseur du webhook
- Recréez l'envoi si nécessaire

---

**Problème 2 : "Erreur de décodage JSON"**

**Cause** : Le transporteur a envoyé un JSON malformé
- Rare, généralement un bug de l'API du transporteur
- Problèmes d'encodage des caractères

**Solution**:
- Contactez le support du transporteur avec la charge utile brute
- Vérifiez les en-têtes pour l'encodage du charset
- Vérifiez l'URL du point de terminaison sur le tableau de bord du transporteur

---

**Problème 3 : Webhooks en double**

**Cause** : Le transporteur envoie le même événement plusieurs fois
- Logique de réessai (le transporteur n'a pas reçu la réponse 200)
- Bug du transporteur

**Solution**:
- Le système rejette automatiquement les doublons (comportement normal)
- Vérifiez que le code de statut de réponse est 200
- Si persistant, contactez le support du transporteur

---

**Problème 4 : Webhooks manquants**

**Cause** : Webhook attendu jamais reçu
- Le transporteur n'a pas envoyé (scan raté)
- Point de terminaison du webhook mal configuré sur le tableau de bord du transporteur
- Pare-feu bloquant les demandes

**Solution**:
- Vérifiez la configuration du webhook sur le tableau de bord du transporteur
- Vérifiez que l'URL du point de terminaison est publique et accessible
- Testez le point de terminaison avec curl/Postman
- Vérifiez les règles du pare-feu du serveur

---

## Configuration du Point de Terminaison des Webhooks

**URLs de Webhook Typiques**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Configuration sur le Tableau de Bord du Transporteur**:
1. Connectez-vous au portail du développeur du transporteur
2. Accédez aux paramètres du webhook
3. Entrez l'URL du webhook de Spwig
4. Sélectionnez les événements auxquels vous souhaitez vous abonner (mises à jour de suivi, livraison, exceptions)
5. Enregistrez la configuration
6. Testez le webhook avec l'outil de test du transporteur

**Sécurité**:
- Les webhooks nécessitent HTTPS (pas HTTP)
- Certains transporteurs signent les demandes (vérifiez la signature)
- Liste blanche des adresses IP (si le transporteur fournit des adresses IP statiques)

---

## Surveillance de la Santé des Webhooks

**Métriques Clés**:

**Taux de Réussite**:
```
Taux de Réussite = (Traité / Total) × 100%

Objectif : >98%
```

**Temps de Traitement**:
```
Temps Moyen = Traité À - Reçu À

Objectif : <2 secondes
```

**Patterns d'Échec**:
- Saut soudain d'échecs → Changement ou panne de l'API du transporteur
- Échecs récurrents "envoi non trouvé" → Problème de synchronisation des numéros de suivi
- Tous les webhooks échoués → Problème de configuration du point de terminaison

**Stratégie de Surveillance**:
- Vérifiez le taux d'échec quotidiennement
- Alerte si le taux d'échec dépasse 5%
- Révisez les messages d'erreur hebdomadairement
- Comparez avec la page d'état du transporteur

---

## Retention des Webhooks

**Les journaux sont permanents** - jamais supprimés automatiquement

**Pourquoi Permanents**:
- Conformité aux audits
- Service client (reconstruction des chronologies de livraison)
- Résolution des litiges
- Débogage des webhooks

**Stockage** : Les journaux sont stockés de manière efficace (JSON compressé)

---

## Conseils

- **Les webhooks sont un journal d'audit permanent** - Ne jamais les supprimer, même s'ils ont été traités avec succès
- **Vérifiez quotidiennement les webhooks échoués** - Détecter les problèmes d'intégration tôt
- **Surveillez le délai de traitement** - Un retard long indique un problème de performance
- **Enregistrez les charges utiles brutes** - Essentiel pour déboguer les changements d'API des transporteurs
- **Testez la configuration du point de terminaison** - Utilisez les outils de test du transporteur pour vérifier la configuration
- **Activez la signature des webhooks** - Vérifiez que les demandes proviennent effectivement du transporteur
- **Liste blanche des adresses IP du transporteur** - Si le transporteur fournit des plages d'IP statiques
- **Configurez des alertes** - Avertissez quand le taux d'échec dépasse le seuil
- **Comparez avec l'état du transporteur** - Les lacunes de webhooks peuvent indiquer une panne du transporteur
- **Documentez les formats de charge utile du transporteur** - Utile quand le transporteur met à jour son API
- **Gardez les URLs des webhooks stables** - Un changement d'URL nécessite une mise à jour sur le tableau de bord du transporteur