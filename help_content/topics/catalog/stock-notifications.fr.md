---
title: Notifications de stock
---

Les notifications de stock permettent aux clients de s'inscrire pour recevoir un e-mail lorsqu'un produit en rupture de stock est à nouveau disponible. Les paramètres d'affichage du stock contrôlent ce que les clients voient sur les pages de produits - tels que les étiquettes de statut de stock, les avertissements de faible stock et ce qui se passe lorsqu'un produit est épuisé.

## Paramètres d'affichage du stock

Les paramètres d'affichage du stock sont des paramètres par défaut pour l'ensemble du magasin qui s'appliquent à tous les produits à moins d'être modifiés au niveau de la catégorie ou du produit.

Accédez à **Catalogue > Paramètres d'affichage du stock** pour configurer ces options. Il y a un enregistrement de paramètres pour votre magasin - cliquez dessus pour le modifier.

### Affichage du statut du stock

| Paramètre | Description |
|---------|-------------|
| **Afficher le statut du stock** | Afficher les étiquettes "En stock" ou "En rupture de stock" sur les pages de produits |
| **Afficher l'avertissement de faible stock** | Afficher un message "Plus que X restants" lorsqu'il y a un faible stock |
| **Seuil de faible stock** | La quantité à partir de laquelle l'avertissement de faible stock s'affiche (par défaut : 5) |
| **Afficher la quantité exacte** | Afficher le nombre exact restant (par exemple, "Plus que 3 restants!") au lieu d'un avertissement générique |

### Comportement en cas de rupture de stock

Le paramètre **Action en cas de rupture de stock** détermine ce que les clients voient lorsqu'un produit n'a plus de stock disponible :

| Action | Ce que les clients voient |
|--------|-------------------|
| **Masquer des listes** | Le produit est supprimé des pages de catégorie et des résultats de recherche |
| **Afficher comme indisponible** | Le produit est visible mais ne peut pas être ajouté au panier |
| **Afficher le bouton "Avertissez-moi"** | Les clients peuvent entrer leur adresse e-mail pour être informés lorsqu'il y a du stock |
| **Autoriser les commandes en attente** | Les clients peuvent acheter le produit même s'il n'y a plus de stock |

Définissez **Message en cas de rupture de stock** pour personnaliser le texte affiché lorsqu'un produit n'est pas disponible (par défaut : `En rupture de stock`).

Définissez **Message de commande en attente** pour personnaliser le texte affiché pour les produits commandables en attente (par défaut : `Disponible en commande en attente`).

### Affichage de la livraison et de la livraison

| Paramètre | Description |
|---------|-------------|
| **Afficher l'emplacement "Expédié depuis"** | Afficher le nom du centre de stockage sur la page du produit |
| **Afficher la livraison estimée** | Afficher les dates de livraison estimées calculées à partir de l'emplacement du centre de stockage |

### Autoriser les commandes en attente (général)

Cochez **Autoriser les commandes en attente** pour permettre aux clients d'acheter tout produit en rupture de stock par défaut. Les produits et catégories individuels peuvent remplacer ce paramètre.

## Notifications de réapprovisionnement

Lorsque vous définissez l'action en cas de rupture de stock sur **Afficher le bouton "Avertissez-moi"**, les clients peuvent entrer leur adresse e-mail sur la page du produit pour recevoir un e-mail lorsqu'il y a du stock à nouveau.

### Affichage des demandes de notification

Accédez à **Catalogue > Notifications de stock** pour voir toutes les demandes de notification des clients. Chaque enregistrement affiche : 
- L'adresse e-mail du client
- Le produit et la variante (le cas échéant)
- Le centre de stockage préféré (si le client a sélectionné une préférence régionale)
- Lorsque la demande a été créée
- Lorsque la notification a été envoyée (vide si elle n'a pas encore été envoyée)

### Lors de l'envoi des notifications

Spwig envoie automatiquement les e-mails de réapprovisionnement lorsqu'un produit atteint un niveau de stock supérieur à zéro. Le champ **Notified At** enregistre l'heure à laquelle le courriel a été envoyé.

Les clients reçoivent une seule notification par courriel. Une fois notifiés, ils doivent s'inscrire à nouveau s'ils veulent à nouveau être notifiés lorsqu'un produit est à nouveau en rupture de stock.

Si vous préférez envoyer plus qu'un simple avertissement - par exemple, afficher le produit réapprovisionné avec un bloc de contenu **Produit phare**, ou faire un suivi après une journée - créez un **Parcours de produit réapprovisionné** dans **Campaign Studio > Journeys** et définissez-le sur **Actif**. Une fois que ce parcours existe, les clients en attente y sont inscrits au lieu de recevoir le courriel unique. Sans parcours actif, ce courriel unique continue d'être envoyé exactement comme décrit ci-dessus. Consultez [Journeys déclenchés](/help/triggered-journeys) pour comprendre comment se comporte le déclencheur.

### Filtres des demandes de notification

Utilisez les filtres de l'administrateur pour trouver : 
- Les demandes pour un produit spécifique 
- Les demandes qui ont déjà été notifiées (pour voir qui a été contacté) 
- Les demandes toujours en attente (les clients attendant un réapprovisionnement) 

## Remplacements au niveau du produit

Les paramètres d'affichage du stock applicables à tout le site peuvent être remplacés par produit ou par catégorie. Dans le formulaire d'édition du produit, recherchez la section **Stock** où vous pouvez définir une **Action en cas de rupture de stock** spécifique au produit, différente de la valeur par défaut globale.

C'est utile lorsque vous souhaitez que la plupart des produits autorisent les commandes anticipées, mais que vous maintenez certains produits en mode « Me prévenir » — ou lorsqu'un produit spécifique doit être masqué en cas de rupture de stock.

## Conseils

- Définissez le **Seuil de stock faible** sur le point de réapprovisionnement que vous utilisez habituellement, afin que les clients soient avertis de la disponibilité limitée avant la rupture totale.
- Utilisez l'option **Afficher le bouton « Me prévenir »** au lieu de masquer les produits en rupture de stock — les clients qui s'inscrivent représentent une demande réelle qui peut justifier une commande de réapprovisionnement.
- Activez **Afficher la quantité exacte** avec parcimonie. Pour la plupart des magasins, afficher « Plus que 3 en stock ! » fonctionne mieux que d'afficher le nombre exact, car cela crée un sentiment d'urgence sans révéler l'ensemble de votre inventaire.
- Vérifiez la liste des notifications de stock avant de passer une nouvelle commande — le nombre de demandes de notification en attente vous indique la demande existante pour ce produit.
- Si vous utilisez les commandes anticipées, mettez à jour votre **Message de commande anticipée** pour définir des attentes précises (par exemple, « Expédié sous 2 à 3 semaines — commandez maintenant pour réserver votre place »).
- Associez les notifications de rupture de stock au marketing par e-mail : lorsque vous réapprovisionnez un produit populaire, envoyez une campagne à tous ceux qui se sont inscrits, et pas seulement l'e-mail de notification automatique.