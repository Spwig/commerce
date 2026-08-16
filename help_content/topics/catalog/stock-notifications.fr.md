---
title: Notifications de stock
---

Les notifications de stock permettent aux clients de s'inscrire pour recevoir un e-mail lorsqu'un produit en rupture de stock est à nouveau disponible. Les paramètres d'affichage du stock contrôlent ce que les clients voient sur les pages de produit - tels que les étiquettes de statut du stock, les avertissements de faible stock et ce qui se passe lorsqu'un produit est épuisé.

## Paramètres d'affichage du stock

Les paramètres d'affichage du stock sont des paramètres par défaut pour l'ensemble de la boutique qui s'appliquent à tous les produits à moins d'être modifiés au niveau de la catégorie ou du produit.

Accédez à **Catalogue > Paramètres d'affichage du stock** pour configurer ces options. Il y a un enregistrement de paramètres pour votre boutique - cliquez dessus pour le modifier.

### Affichage du statut du stock

| Paramètre | Description |
|---------|-------------|
| **Afficher le statut du stock** | Afficher les étiquettes "En stock" ou "En rupture de stock" sur les pages de produit |
| **Afficher l'avertissement de faible stock** | Afficher un message "Plus que X restants" lorsqu'il y a un faible stock |
| **Seuil de faible stock** | La quantité à partir de laquelle l'avertissement de faible stock s'affiche (par défaut : 5) |
| **Afficher la quantité exacte** | Afficher le nombre exact restant (par exemple, "Plus que 3 restants!") au lieu d'un avertissement générique |

### Comportement en rupture de stock

Le paramètre **Action en rupture de stock** détermine ce que les clients voient lorsqu'un produit n'a plus de stock disponible :

| Action | Ce que les clients voient |
|--------|-------------------|
| **Masquer des listes** | Le produit est supprimé des pages de catégorie et des résultats de recherche |
| **Afficher comme indisponible** | Le produit est visible mais ne peut pas être ajouté au panier |
| **Afficher le bouton "Avertissez-moi"** | Les clients peuvent entrer leur adresse e-mail pour être avertis lorsqu'il y a du stock |
| **Autoriser les commandes en attente** | Les clients peuvent acheter le produit même s'il n'y a plus de stock |

Définissez **Message en rupture de stock** pour personnaliser le texte affiché lorsqu'un produit n'est pas disponible (par défaut : `En rupture de stock`).

Définissez **Message de commande en attente** pour personnaliser le texte affiché pour les produits commandables en attente (par défaut : `Disponible en commande en attente`).

### Affichage de la livraison et de la livraison

| Paramètre | Description |
|---------|-------------|
| **Afficher l'emplacement "Expédié depuis"** | Afficher le nom du centre de distribution sur la page du produit |
| **Afficher la livraison estimée** | Afficher les dates de livraison estimées calculées à partir de l'emplacement du centre de distribution |

### Autoriser les commandes en attente (général)

Cochez **Autoriser les commandes en attente** pour permettre aux clients d'acheter tout produit en rupture de stock par défaut. Les produits et catégories individuels peuvent remplacer ce paramètre.

## Notifications de réapprovisionnement

Lorsque vous définissez l'action en rupture de stock sur **Afficher le bouton "Avertissez-moi"**, les clients peuvent entrer leur adresse e-mail sur la page du produit pour recevoir un e-mail lorsqu'il y a du stock.

### Affichage des demandes de notification

Accédez à **Catalogue > Notifications de stock** pour voir toutes les demandes de notification des clients. Chaque enregistrement affiche : 
- L'adresse e-mail du client
- Le produit et la variante (le cas échéant)
- Le centre de distribution préféré (si le client a sélectionné une préférence régionale)
- Lorsque la demande a été créée
- Lorsque la notification a été envoyée (vide si elle n'a pas encore été envoyée)

### Lorsque les notifications sont envoyées

Spwig envoie automatiquement les e-mails de réapprovisionnement lorsqu'un produit atteint un niveau de stock supérieur à zéro. Le champ **Notified At** enregistre l'heure à laquelle le courriel a été envoyé.

Les clients reçoivent une seule notification par courriel. Une fois notifiés, ils doivent s'inscrire à nouveau s'il y a à nouveau une rupture de stock.

### Filtrage des demandes de notification

Utilisez les filtres de l'administration pour trouver : 
- Les demandes pour un produit spécifique
- Les demandes qui ont déjà été notifiées (pour voir qui a été contacté)
- Les demandes toujours en attente (les clients attendant un réapprovisionnement)

## Remplacements au niveau du produit

Les paramètres d'affichage du stock par défaut peuvent être remplacés au niveau du produit ou de la catégorie. Sur le formulaire d'édition du produit, cherchez la section **Stock** où vous pouvez définir une **Action en rupture de stock** spécifique au produit qui diffère de la valeur par défaut globale.

Cela est utile lorsque vous souhaitez que la plupart des produits autorisent les commandes en attente, mais que quelques-uns soient configurés sur "Avertissez-moi" - ou lorsqu'un produit spécifique doit être masqué lorsqu'il est en rupture de stock.

## Conseils

Conservez tous les formats de markdown, les chemins d'images, les blocs de code et les termes techniques.

- Configurez le **Seuil de stock faible** à votre point de réapprovisionnement habituel, afin que les clients soient avertis de la disponibilité limitée avant que vous n'ayez plus du tout de stock.
- Utilisez l'option **Afficher le bouton "Avertissez-moi"** au lieu de cacher les produits en rupture de stock — les clients qui s'inscrivent représentent une demande réelle qui peut justifier une commande de réapprovisionnement.
- Activez **Afficher la quantité exacte** avec modération.

Pour la plupart des magasins, afficher "Plus que 3 restants !" fonctionne mieux que d'afficher le nombre exact, car cela crée une urgence sans révéler l'ensemble de votre tableau de stock.
- Vérifiez la liste des notifications de stock avant de passer une nouvelle commande — le nombre de demandes de notification en attente vous indique combien de demande existe pour ce produit.
- Si vous utilisez des commandes en attente, mettez à jour votre **Message de commande en attente** pour fixer des attentes précises (par exemple, "Expédié en 2-3 semaines - commandez maintenant pour réserver votre place").
- Combiner les notifications de rupture de stock avec le marketing par courriel : lorsque vous réapprovisionnez un produit populaire, envoyez une campagne à tous ceux qui se sont inscrits, et non seulement à l'e-mail de notification automatique.