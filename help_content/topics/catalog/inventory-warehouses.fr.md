---
title: Inventaire et Entrepôts
---

Le système d'entrepôts vous permet de gérer l'inventaire sur plusieurs sites, de définir les priorités de traitement des commandes et de suivre les niveaux de stock en temps réel. Accédez à **Paramètres > Gestion des Licences** dans la barre latérale, ou accédez aux entrepôts depuis l'onglet inventaire du produit.

![Liste des entrepôts](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Entrepôts

### Liste des Entrepôts

La page des entrepôts affiche tous vos emplacements d'inventaire sous forme de cartes avec :

- **Nom et code** — Identifiant de l'entrepôt (ex. : "Entrepôt Principal", code "MAIN-WH")
- **Région de vente** — Attribution de la région géographique
- **Badges de statut** — Actif/inactif, point de vente
- **Statistiques** — Produits stockés, priorité de traitement, pourcentage de réserve de stock
- **Emplacement** — Ville et pays
- **Dernière mise à jour** — Date de la dernière modification des niveaux de stock

### Créer un Entrepôt

1. Cliquez sur **+ Ajouter un Entrepôt**
2. Remplissez les détails de l'entrepôt :
   - **Nom** — Étiquette descriptive (ex. : "Entrepôt Est des États-Unis")
   - **Code** — Identifiant unique court (ex. : "US-EAST")
   - **Région de Vente** — Assigner à une région géographique pour le routage des commandes
   - **Adresse** — Adresse complète de l'entrepôt pour les calculs d'expédition
3. Configurez les paramètres :
   - **Actif** — Activer pour inclure dans le traitement des commandes
   - **Point de Vente** — Cocher si cet entrepôt sert également de magasin physique
   - **Priorité de Traitement** — Les nombres plus élevés signifient une priorité plus haute pour le traitement des commandes
   - **Réserve de Stock** — Pourcentage de stock réservé comme marge de sécurité
4. Cliquez sur **Enregistrer**

### Priorité de Traitement

Lorsqu'une commande arrive, le système sélectionne le meilleur entrepôt en fonction de :

1. **Valeur de priorité** — Les entrepôts à priorité plus élevée sont privilégiés
2. **Disponibilité du stock** — Doit disposer d'un stock suffisant
3. **Correspondance de région** — Les entrepôts de la région du client sont préférés

Par exemple, si vous avez un entrepôt aux États-Unis (priorité 100) et un entrepôt en UE (priorité 60), les commandes américaines seront traitées en priorité depuis l'entrepôt américain.

### Réserve de Stock

La réserve de stock met de côté un pourcentage de l'inventaire qui ne sera pas vendu en ligne. Cela est utile pour :
- Les magasins physiques qui ont besoin de stock d'exposition
- Le stock de sécurité pour éviter la survente
- L'inventaire réservé pour les commandes en gros

Une réserve de 10 % sur 100 unités signifie que seulement 90 unités sont disponibles pour les commandes en ligne.

## Articles de Stock

Les articles de stock représentent l'inventaire réel d'un produit spécifique dans un entrepôt spécifique.

### Consulter les Niveaux de Stock

1. Cliquez sur l'**icône de stock** sur n'importe quelle carte d'entrepôt pour voir ses articles de stock
2. Ou accédez à l'onglet **Inventaire** d'un produit pour voir le stock dans tous les entrepôts

Chaque article de stock affiche :
- **Nom du produit** et variante (le cas échéant)
- **En stock** — Inventaire physique total
- **Alloué** — Quantité réservée pour les commandes en attente
- **Disponible** — En stock moins alloué (ce qui peut être vendu)

### Ajouter du Stock

1. Depuis la vue de stock de l'entrepôt, cliquez sur **Ajouter un Article de Stock**
2. Sélectionnez le produit et la variante
3. Entrez la quantité **en stock**
4. Enregistrez

### Mouvements de Stock

Chaque modification de l'inventaire est enregistrée comme un **mouvement de stock** :

| Type de Mouvement | Description |
|-------------------|-------------|
| **Réception** | Nouveau stock reçu du fournisseur |
| **Vente** | Stock déduit pour une commande traitée |
| **Retour** | Stock retourné par un client |
| **Ajustement** | Correction manuelle (écart de comptage) |
| **Transfert** | Déplacé entre entrepôts |
| **Réservation** | Temporairement retenu pour un panier actif |

Les mouvements de stock fournissent une piste d'audit complète des modifications d'inventaire.

## Suivi d'Inventaire sur les Produits

### Activer le Suivi d'Inventaire

Dans l'onglet **Inventaire** d'un produit :

1. Activez **Suivre l'Inventaire** pour activer la gestion des stocks
2. Définissez le **Seuil de Stock Bas** — déclenche des alertes lorsque le stock tombe en dessous de ce niveau
3. Configurez **Autoriser les Commandes en Attente** si vous souhaitez accepter des commandes en rupture de stock

### Stock Multi-Entrepôts

Lorsque le suivi d'inventaire est activé, l'onglet Inventaire affiche les niveaux de stock dans tous les entrepôts dans un tableau récapitulatif :

- Total en stock sur tous les emplacements
- Répartition par entrepôt
- Quantités disponibles après réservations et allocations

## Alertes de Stock Bas

Le système surveille automatiquement les niveaux de stock et vous alerte lorsque :
- Un produit tombe en dessous de son **seuil de stock bas**
- Un produit atteint un **stock disponible nul**

Les alertes de stock bas apparaissent dans :
- Le **Tableau de Bord de la Boutique** dans la section Actions Requises
- La liste des produits avec un indicateur visuel

## Conseils

- Commencez avec un seul entrepôt et ajoutez-en d'autres au fur et à mesure que votre activité se développe.
- Définissez les priorités de traitement en fonction de la rapidité d'expédition et du coût vers chaque région.
- Utilisez les réserves de stock pour les points de vente afin de garantir la disponibilité du stock d'exposition.
- Vérifiez régulièrement les mouvements de stock pour identifier les pertes ou les écarts.
- Définissez les seuils de stock bas en fonction de votre délai de réapprovisionnement — s'il faut 2 semaines pour reconstituer le stock, fixez le seuil pour couvrir 2 semaines de ventes.
- Activez le suivi d'inventaire avant la mise en ligne pour éviter la survente.
