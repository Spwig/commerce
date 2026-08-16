---
title: Inventaire & entrepôts
---

Le système d'entrepôt vous permet de gérer l'inventaire à travers plusieurs emplacements, de définir les priorités de traitement des commandes et de suivre les niveaux de stock en temps réel. Accédez à **Produits > Entrepôts** dans la barre latérale d'administration pour gérer vos emplacements d'entrepôt.

![Liste des entrepôts](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Entrepôts

### Liste des entrepôts

La page des entrepôts affiche tous vos emplacements d'inventaire sous forme de cartes avec :

- **Nom et code** — Identifiant de l'entrepôt (par exemple, « Entrepôt principal », code « MAIN-WH»)
- **Région de vente** — Attribution de la région géographique
- **Badges de statut** — Actif/inactif, emplacement de vente au détail
- **Statistiques** — Produits stockés, priorité de traitement, pourcentage de marge de sécurité
- **Emplacement** — Ville et pays
- **Dernière mise à jour** — Lorsque les niveaux de stock ont été modifiés

### Création d'un entrepôt

1. Cliquez sur **+ Ajouter un entrepôt**
2. Remplissez les **Informations de base** : 
   - **Nom** — Étiquette descriptive (par exemple, « Entrepôt Est des États-Unis »)
   - **Code** — Identifiant unique court (par exemple, « US-EAST ») — doit être unique par rapport à tous les entrepôts
   - **Région de vente** — Attribution à une région géographique pour le routage des commandes
   - **Actif** — Activez-le pour l'inclure dans le traitement des commandes
3. Remplissez la section **Adresse** avec l'adresse complète de l'entrepôt
4. Configurez les **Paramètres de traitement** : 
   - **Priorité de traitement** — Les numéros plus élevés = priorité plus élevée pour le traitement des commandes
   - **Pourcentage de marge de sécurité** — Pourcentage de stock à réserver en tant que marge de sécurité (0–100)
   - **Emplacement d'expédition** — Lien éventuel vers un emplacement de retrait si cet entrepôt prend en charge le retrait client
5. Configurez le **Display client** (optionnel) : 
   - **Nom d'affichage** — Étiquette visible par le client (par exemple, « Expédié d'Australie »). Laissez vide pour utiliser le nom de l'entrepôt.
   - **Afficher sur le site web** — Afficher l'origine de cet entrepôt aux clients sur les pages de produit
6. Configurez le **Point de vente / magasin de détail** (optionnel) : 
   - **Emplacement de vente au détail** — Cochez si cet entrepôt sert également de magasin physique avec des terminaux de point de vente
   - **Nom d'affichage du point de vente** — Nom court affiché dans l'interface du point de vente
   - **Groupe de magasins** — Attribution à un groupe de magasins de point de vente pour hériter des paramètres
7. Ajoutez des **informations de contact** si nécessaire (nom, courriel, téléphone)
8. Cliquez sur **Enregistrer"

### Priorité de traitement

Lorsqu'une commande arrive, le système sélectionne le meilleur entrepôt en fonction de : 

1. **Valeur de priorité** — Les entrepôts à priorité plus élevée sont privilégiés
2. **Disponibilité du stock** — Doit avoir suffisamment de stock
3. **Correspondance de région** — Les entrepôts situés dans la région du client sont privilégiés

Par exemple, si vous avez un entrepôt aux États-Unis (priorité 100) et un entrepôt en Europe (priorité 60), les commandes américaines seront traitées par l'entrepôt américain en premier.

### Marge de sécurité

La marge de sécurité réserve un pourcentage d'inventaire qui ne sera pas vendu en ligne. Cela est utile pour : 

- Les magasins physiques qui ont besoin de stock sur le sol
- Le stock de sécurité pour éviter la survente
- L'inventaire réservé pour les commandes de gros

Un pourcentage de 10 % sur 100 unités signifie qu'il n'y a que 90 unités disponibles pour les commandes en ligne.

## Articles de stock

Les articles de stock représentent l'inventaire réel d'un produit spécifique dans un entrepôt spécifique.

### Affichage des niveaux de stock

1. Cliquez sur l'**icône de stock** sur n'importe quelle carte d'entrepôt pour voir ses articles de stock
2. Ou accédez à l'onglet **Inventaire** d'un produit pour voir le stock à travers tous les entrepôts

Chaque article de stock affiche : 

- **Nom du produit** et variante (le cas échéant)
- **En main** — Inventaire physique total
- **Alloué** — Quantité réservée pour les commandes en attente
- **Disponible** — En main moins alloué (ce qui peut être vendu)

### Ajout de stock

1. Accédez à **Produits > Articles de stock** et cliquez sur **+ Ajouter un article de stock**, ou
2. Ouvrez la forme d'édition d'un produit et utilisez la section **Articles de stock** en bas
3. Sélectionnez le **produit** et l'**entrepôt** (et éventuellement une **variante** pour les produits variables)
4. Entrez la quantité **en main**
5. Définissez le **seuil de stock faible** — ce seuil par article déclenche une alerte de stock faible
6. Enregistrer

### Mouvements de stock

Tout changement de stock est enregistré en tant que **mouvement de stock** :

| Type de mouvement | Description |
|--------------|-------------|
| **Réception** | Nouvelle entrée de stock provenant d'un fournisseur |
| **Vente** | Stock déduit pour une commande traitée |
| **Retour** | Stock retourné par un client |
| **Ajustement** | Correction manuelle (différence de comptage) |
| **Transfert** | Déplacé entre les entrepôts |
| **Réservation** | Temporairement retenu pour un panier actif |
| **Dommage** | Compte tenu comme endommagé ou perdu |
| **Recompte** | Corrigé pour correspondre à un comptage physique du stock |

Les mouvements de stock fournissent une trace complète des changements de stock. En plus de l'action **Ajuster les niveaux de stock**, Spwig propose également des actions en vrac sur la liste des articles de stock pour transférer, écrire, et recompter le stock sur plusieurs articles à la fois — voir [Actions de stock en vrac](/help/stock-bulk-actions).

## Suivi de l'inventaire sur les produits

### Activer le suivi de l'inventaire

Sur la section **Inventaire** d'un produit :

1. Activez **Suivre l'inventaire** pour activer la gestion du stock pour ce produit
2. Définissez le **Seuil de stock faible** — déclenche les alertes du tableau de bord lorsque le stock dans n'importe quelle usine tombe en dessous de ce seuil
3. Configurez **Autoriser les commandes en attente** si vous souhaitez accepter des commandes lorsque le stock est épuisé
4. Définissez éventuellement une **Action en cas de rupture de stock** pour remplacer le comportement du site ou de la catégorie pour ce produit spécifique

Après avoir activé le suivi, gérez les quantités réelles de stock à l'aide de la section **Articles de stock** intégrée en bas du formulaire du produit, ou via **Produits > Articles de stock**.

### Stock multi-entrepos

Lorsque le suivi de l'inventaire est activé, l'onglet Inventaire affiche les niveaux de stock dans tous les entrepôts dans un tableau récapitulatif :

- Total en main à travers toutes les locations
- Répartition par entrepôt
- Quantités disponibles après réservations et affectations

## Alertes de stock faible

Le système surveille automatiquement les niveaux de stock et vous alerte lorsqu':
- Un produit tombe en dessous de son **seuil de stock faible**
- Un produit atteint **zéro stock disponible**

Les alertes de stock faible s'affichent sur :
- Le **Tableau de bord de la boutique** dans la section Actions Requises
- La liste des produits avec un indicateur visuel

## Conseils

- Commencez par un seul entrepôt et ajoutez-en d'autres à mesure que votre entreprise grandit.
- Définissez des priorités de livraison en fonction de la vitesse et du coût de livraison vers chaque région.
- Utilisez des stocks de réserve pour les magasins de détail pour vous assurer de la disponibilité du stock en magasin.
- Examinez régulièrement les mouvements de stock pour identifier les pertes ou les écarts.
- Définissez les seuils de stock faible en fonction de votre délai de réapprovisionnement — si cela prend 2 semaines pour réapprovisionner, définissez le seuil pour couvrir 2 semaines de ventes.
- Activez le suivi de l'inventaire avant de lancer votre site pour éviter les ventes excessives.