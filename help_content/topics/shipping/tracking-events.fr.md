---
title: Suivi des événements
---

Les événements de suivi enregistrent les points de contrôle du statut d'expédition tout au long du cycle de livraison — chaque événement capture le statut (en cours de livraison, en route vers la livraison, livré), l'horodatage, la localisation, la description et les données brutes du transporteur. Les événements sont créés automatiquement via les notifications de webhook des transporteurs ou manuellement par les commerçants. Les clients voient l'historique des événements de suivi dans leur compte et dans les e-mails de confirmation de commande, offrant une visibilité en temps réel sur la livraison.

Cette page d'administration affiche un historique d'événements en lecture seule pour des raisons de vérification et de support client.

## Structure d'événement de suivi

Chaque événement contient :

**Informations sur l'état**:
- **Statut** : en_cours_de_livraison, en_route_pour_la_livraison, livré, exception, échoué, retourné
- **Description** : État lisible par l'homme (ex. : "Colis arrivé à l'usine de tri")
- **Code de statut du transporteur** : Statut original du transporteur (ex. : "DEP" pour départ)

**Données de localisation**:
- **Ville** : Ville de la localisation de l'événement
- **État** : État/province de la localisation de l'événement
- **Pays** : Pays de la localisation de l'événement
- **Code postal** : Code postal/ZIP de la localisation de l'événement

**Horodatages**:
- **Survenu à** : Quand l'événement s'est réellement produit (heure du transporteur)
- **Créé à** : Quand l'événement a été enregistré dans Spwig (heure système)

**Métadonnées**:
- **Données brutes** : Réponse JSON complète du transporteur
- **Expédition** : ID d'expédition lié

---

## Types de statuts d'événement

**en_cours_de_livraison** : Colis en mouvement via le réseau du transporteur
- Exemples : "Départ de l'usine", "Arrivé au centre", "En cours de livraison vers l'usine suivante"

**en_route_pour_la_livraison** : Colis sur le véhicule de livraison
- Exemples : "En route pour la livraison", "Sur le véhicule de livraison"

**livré** : Colis livré avec succès
- Exemples : "Livré à la porte d'entrée", "Laissé à la réception", "Remis au destinataire"

**exception** : Problème de livraison nécessitant une attention
- Exemples : "Retard dû aux conditions météorologiques", "Adresse incorrecte", "Essai de livraison échoué"

**échoué** : Échec permanent de la livraison
- Exemples : "Indélivérable à l'adresse indiquée", "Refusé par le destinataire"

**retourné** : Colis en cours de retour au destinataire
- Exemples : "Retour au destinataire initié", "Colis en retour"

---

## Création des événements de suivi

### Automatique (Webhook du transporteur)

**Workflow**:
1. Le transporteur scanne le colis (départ, arrivée, livraison)
2. Le transporteur envoie un webhook à l'endpoint de webhook de Spwig
3. Le webhook est enregistré dans la table WebhookLog
4. Le système analyse la charge utile du webhook
5. L'événement de suivi est créé avec les données extraites
6. Notification par e-mail au client (si configuré)

**Avantages**:
- Mises à jour en temps réel (pas besoin de sondage)
- Horodatages précis du transporteur
- Historique d'événements entièrement automatisé

### Manuel (Saisie du commerçant)

**Workflow**:
1. Accédez aux détails de l'expédition
2. Cliquez sur "Ajouter un événement de suivi"
3. Sélectionnez le statut dans le menu déroulant
4. Entrez la description
5. Optionnel : Entrez les données de localisation
6. Définissez l'horodatage survenu à
7. Enregistrez

**Cas d'utilisation**:
- Transporteurs sans support de webhook
- Corrections manuelles des expéditions
- Livraisons locales (non par transporteur)
- Mises à jour d'état internes

---

## Ordre d'affichage des événements

Les événements sont affichés dans l'**ordre chronologique inversé** (plus récents en premier) : 

**Exemple d'affichage**:
```
13 févr. 2026 à 10:30 - Livré (Brooklyn, NY)
13 févr. 2026 à 08:15 - En route pour la livraison (Brooklyn, NY)
12 févr. 2026 à 23:45 - Arrivé à l'usine locale (Brooklyn, NY)
12 févr. 2026 à 18:30 - En cours de livraison (Newark, NJ)
12 févr. 2026 à 14:15 - Départ de l'origine (Philadelphie, PA)
12 févr. 2026 à 09:00 - Réceptionné (Philadelphie, PA)
```

---

## Visibilité client

Les événements de suivi sont affichés aux clients dans : 

**E-mail de confirmation de commande**:
- Statut d'événement le plus récent
- Date estimée de livraison
- Lien de suivi

**Compte client > Détails de la commande**:
- Chronologie complète des événements
- Descriptions des événements
- Historique des localisations
- Horodatages

**Page de suivi** (si activée) : 
- URL dédiée au suivi
- Chronologie visuelle
- Logo du transporteur
- Carte de livraison (si les données de localisation sont disponibles)

---

## Filtrage des événements de suivi

**Filtres utiles**:
- **Expédition** : Afficher les événements pour une expédition spécifique
- **Statut** : Filtre par type d'événement (livré, en_cours_de_livraison, etc.)
- **Plage de dates** : Événements dans un intervalle de temps
- **Localisation** : Événements dans une ville/état spécifique

**Cas d'utilisation**:
- "Afficher toutes les livraisons effectuées aujourd'hui"
- "Trouver toutes les exceptions de la semaine dernière"
- "Suivre les expéditions actuellement en_cours_de_livraison"

---

## Données brutes (Débogage)

**Champ de données brutes**:
- Stocke la réponse complète de l'API du transporteur au format JSON
- Utile pour déboguer les problèmes de webhook
- Contient des métadonnées spécifiques au transporteur

**Exemple de données brutes** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "En route pour la livraison",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Quand vérifier les données brutes**:
- Description de l'événement obscure
- Données de localisation manquantes
- Erreurs de traitement des webhooks
- Escalade au support du transporteur

---

## Timing des événements

**Survenu à** vs **Créé à**:

**Survenu à** : Quand l'événement du transporteur s'est réellement produit
- Exemple : Colis scanné à 10h30

**Créé à** : Quand Spwig a reçu le webhook
- Exemple : Webhook reçu à 10h32 (délai de 2 minutes)

**Pourquoi différent**:
- Latence réseau
- Traitement en lot par le transporteur
- Retards de réessai des webhooks

**Utilisez Survenu à pour l'affichage client** - plus précise pour refléter le progrès réel de la livraison.

---

## Conseils

- **Les événements sont en lecture seule** - Impossible de les modifier après leur création (intégrité de vérification)
- **Vérifiez les données brutes pour les détails** - Plus d'informations que les champs affichés
- **Surveillez le délai des webhooks** - Un grand écart entre survenu à et créé à indique des problèmes de webhook
- **Utilisez pour le support client** - La chronologie des événements aide à diagnostiquer les problèmes de livraison
- **Suivez les modèles de livraison** - Analysez le timing des événements pour évaluer les performances des transporteurs
- **Configurez des notifications** - Envoyez automatiquement des e-mails aux clients pour les événements clés (en_route_pour_la_livraison, livré)
- **Ne supprimez pas les événements** - Conservez la trace complète des vérifications
- **Vérifiez WebhookLog pour les échecs** - L'absence d'événements peut indiquer des erreurs de traitement des webhooks
- **Les données de localisation varient selon le transporteur** - Certains transporteurs fournissent des données détaillées, d'autres minimales
- **Les événements d'exception nécessitent une attention** - Surveillez et suivez les exceptions de livraison