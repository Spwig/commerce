---
title: Produits réservables
---

Les produits réservables permettent aux clients de réserver une date et une heure spécifiques lors de leur achat. Cela prend en charge les rendez-vous, les locations, les cours, les événements et les réservations d'hébergement — tous gérés directement depuis votre interface d'administration Spwig.

## Types de réservation

| Type | Meilleur pour |
|------|----------|
| **Rendez-vous** | Services : consultations, coupes de cheveux, entraînement personnel |
| **Location** | Location d'équipement, location de véhicule, location de salle |
| **Cours / Atelier** | Sessions en groupe avec une capacité définie |
| **Hébergement** | Séjours de plusieurs nuits avec des horaires d'arrivée/départ |
| **Événement** | Événements uniques ou récurrents avec billetterie |

## Mise en place d'un produit réservable

### Étape 1 : Créer le produit

1. Accédez à **Produits > Tous les produits** et cliquez sur **+ Ajouter un produit**
2. Définissez **Type de produit** sur **Produit de réservation**
3. Remplissez les champs standard du produit (nom, description, prix)
4. Enregistrez le produit

### Étape 2 : Configurer les paramètres de réservation

Après l'enregistrement, une section **Configuration de réservation** apparaît sur le formulaire d'édition du produit. Remplissez les paramètres de réservation :

#### Type de réservation et durée

- **Type de réservation** — Sélectionnez le type qui correspond le mieux à votre service (Rendez-vous, Location, Cours, etc.)
- **Type de durée** — Choisissez **Durée fixe** pour des sessions de durée définie, ou **Le client choisit la durée** pour permettre aux clients de choisir combien de temps ils ont besoin
- **Durée** et **Unité de durée** — Définissez la durée (par exemple, `60` minutes, `1` heure, `2` jours)
- **Durée minimale/maximale** — Si les clients peuvent choisir la durée, définissez la plage autorisée

#### Temps de buffer

Le temps de buffer est ajouté automatiquement entre les réservations pour permettre la préparation ou le nettoyage :
- **Buffer avant** — Minutes réservées avant le début de la réservation
- **Buffer après** — Minutes réservées après la fin de la réservation

Par exemple, un rendez-vous de massage de 60 minutes avec un buffer de 15 minutes après permet 15 minutes pour se préparer pour le client suivant.

#### Fenêtre de réservation anticipée

- **Avertissement minimum** — Indique à quel point en avance un client doit réserver (par exemple, `24 heures` pour interdire les réservations du même jour)
- **Fenêtre maximale de réservation** — Indique à quel point dans le futur les clients peuvent réserver (par exemple, `365 jours`)

#### Capacité

- **Nombre maximum de réservations par créneau** — Pour les cours et les événements, définissez combien de clients peuvent réserver le même créneau horaire. Mettez à `1` pour les rendez-vous privés.

#### Confirmation

- **Exiger une confirmation manuelle** — Lorsqu'elle est cochée, les réservations ne sont pas confirmées automatiquement. Vous devez approuver manuellement chaque réservation depuis la liste des réservations. Utile lorsque vous souhaitez vérifier les clients avant de confirmer.

#### Politique d'annulation

- **Annulation autorisée** — Indique si les clients peuvent annuler leur réservation
- **Délai d'annulation** — Indique combien d'heures/jours avant la réservation les clients peuvent annuler (par exemple, `24 heures`)

#### Affichage du calendrier

La manière dont les clients sélectionnent leur date et leur heure sur la page du produit :

| Mode d'affichage | Meilleur pour |
|-------------|----------|
| **Vue calendrier** | Utilisation générale — calendrier mensuel complet |
| **Sélecteur de date** | Sélection simple d'une seule date |
| **Liste déroulante des dates disponibles** | Produits avec des créneaux d'availability limités |
| **Sélecteur de plage de dates** | Hébergement et locations de plusieurs jours |

#### Dépôts

Pour exiger un dépôt à la caisse au lieu d'un paiement complet :
1. Cochez **Dépôt activé**
2. Définissez **Type de dépôt** sur **Montant fixe** ou **Pourcentage du total**
3. Entrez le **Montant du dépôt** (par exemple, `50` pour 50 $, ou `25` pour 25 %)

#### Paramètres spécifiques aux hébergements

Pour les réservations d'hébergement, des champs supplémentaires apparaissent :
- **Heure d'arrivée** et **Heure de départ** — Heures standard pour la propriété
- **Occupation standard** — Nombre par défaut de personnes inclus dans le tarif de base

### Étape 3 : Ajouter des ressources de réservation (facultatif)

Les ressources sont les éléments physiques ou les membres du personnel qui sont assignés à une réservation — par exemple, « Salle 1 », « Court A » ou « Entraîneur Sam ».

1. Sur le formulaire d'édition du produit, allez à la section **Ressources de réservation**
2. Cliquez sur **Ajouter une ressource**
3. Donnez à la ressource un **Nom** et définissez sa **Capacité** (combien de réservations elle peut gérer simultanément)
4. Ajoutez éventuellement des images de ressource


Les ressources vous permettent de suivre la disponibilité par actif ou membre du personnel individuel, et non seulement par créneau horaire.

### Étape 4 : Définir les règles de disponibilité

Les règles de disponibilité définissent les moments où les réservations peuvent être effectuées :

1. Dans l'onglet **Disponibilité** du produit, cliquez sur **Ajouter une règle de disponibilité**
2. Sélectionnez la **Ressource** à laquelle cette règle s'applique
3. Définissez les **Jours de la semaine** pendant lesquels les réservations sont disponibles
4. Définissez l'**Heure de début** et l'**Heure de fin** de la fenêtre disponible
5. Définissez éventuellement une plage de dates (**Valide à partir du**) / (**Valide jusqu'au**) pour une disponibilité saisonnière
6. Enregistrer

## Affichage et gestion des réservations

### Liste des réservations

Accédez à **Catalogue > Réservations** pour voir toutes les réservations. Vous pouvez filtrer par :
- Statut (En attente de confirmation, Confirmée, Annulée, Terminée, Non présentée)
- Produit
- Plage de dates

### Statuts des réservations

| Statut | Signification |
|--------|---------|
| **En attente de confirmation** | En attente d'approbation manuelle (si la confirmation est requise) |
| **Confirmée** | La réservation est confirmée et active |
| **Annulée** | La réservation a été annulée par le client ou par vous |
| **Terminée** | La date de réservation est passée et la réservation a été effectuée |
| **Non présentée** | Le client n'est pas venu |

### Confirmer une réservation en attente

1. Ouvrez la réservation depuis **Catalogue > Réservations**
2. Changez le **Statut** en **Confirmée**
3. Enregistrez — le client reçoit automatiquement un e-mail de confirmation

### Annuler une réservation

1. Ouvrez la réservation
2. Changez le **Statut** en **Annulée**
3. Entrez une **raison d'annulation** (affichée dans l'e-mail du client)
4. Enregistrez

## Gestion de la liste d'attente

Lorsqu'un créneau horaire est pleinement réservé, les clients peuvent s'inscrire à la liste d'attente. Spwig informe automatiquement les clients inscrits à la liste d'attente lorsqu'une annulation crée un créneau disponible.

### Affichage de la liste d'attente

Accédez à **Catalogue > Liste d'attente des réservations** pour voir toutes les entrées de la liste d'attente. Chaque entrée affiche :
- Le nom et l'adresse e-mail du client
- Le produit et la date souhaitée
- Statut : **En attente**, **Notifié**, **Converti en réservation** ou **Expiré**

### Statuts de la liste d'attente

| Statut | Signification |
|--------|---------|
| **En attente** | Le client est en file d'attente, le créneau n'est pas encore disponible |
| **Notifié** | Le client a reçu un e-mail concernant un créneau disponible |
| **Converti en réservation** | Le client a pris le créneau et a effectué une réservation |
| **Expiré** | La date souhaitée est passée sans que de créneau ne devienne disponible |

### Notifier manuellement un client de la liste d'attente

Si vous souhaitez contacter un client spécifique de la liste d'attente avant la notification automatique :
1. Ouvrez l'entrée de la liste d'attente
2. Copiez leur adresse e-mail et contactez-les directement
3. Une fois qu'ils effectuent une réservation, le statut de leur entrée dans la liste d'attente passe à **Converti en réservation**

## Conseils

- Activez la confirmation manuelle pour les réservations de haute valeur (par exemple, séances de photographie, événements privés) afin que vous puissiez vérifier la disponibilité et correspondre aux exigences avant de vous engager.
- Définissez un temps de buffer généreux au début — vous pouvez toujours le réduire une fois que vous comprendrez les besoins réels de traitement.
- Pour les cours en groupe, définissez **Max Bookings Per Slot** à la capacité de la classe et activez la liste d'attente afin que les séances populaires créent automatiquement une file d'attente.
- Utilisez le mode d'affichage du sélecteur de plage de dates pour les produits d'hébergement — les clients s'attendent à sélectionner ensemble les dates d'arrivée et de départ.
- Définissez un délai minimum d'avance pour empêcher les réservations de dernière minute si vous avez besoin de temps de préparation (par exemple, un délai minimum de 48 heures pour les commandes de restauration personnalisées).
- Révisez régulièrement votre liste d'attente pendant les périodes occupées — le contact manuel avec les clients de la liste d'attente peut combler plus rapidement les annulations que la notification automatique.