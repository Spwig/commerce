---
title: Notifications de stock
---

Les notifications de stock permettent aux clients de s'inscrire pour recevoir un e-mail lorsqu'un produit en rupture de stock devient à nouveau disponible. Les paramètres d'affichage du stock contrôlent ce que les clients voient sur les pages de produits — tels que les étiquettes d'état du stock, les avertissements de faible stock et ce qui se produit lorsque le produit est épuisé.

## Paramètres d'affichage du stock

Les paramètres d'affichage du stock sont des paramètres par défaut applicables à l'ensemble du magasin, sauf si ils sont remplacés au niveau de la catégorie ou du produit.

Accédez à **Catalogue > Paramètres d'affichage du stock** pour configurer ces options. Il existe un enregistrement de paramètres pour votre magasin — cliquez-y pour l'éditer.

### Affichage de l'état du stock

| Paramètre | Description |
|---------|-------------|
| **Afficher l'état du stock** | Afficher les étiquettes "En stock" ou "En rupture de stock" sur les pages de produits |
| **Afficher l'avertissement de faible stock** | Afficher un message "Seulement X restant" lorsque le stock est faible |
| **Seuil de faible stock** | La quantité à laquelle ou en dessous de laquelle l'avertissement de faible stock s'affiche (par défaut : 5) |
| **Afficher la quantité exacte** | Afficher le nombre exact restant (par exemple, "Seulement 3 restant!") au lieu d'un avertissement générique |

### Comportement en cas de rupture de stock

Le paramètre **Action en cas de rupture de stock** détermine ce que les clients voient lorsqu'un produit n'a plus de stock disponible :

| Action | Ce que les clients voient |
|--------|-------------------|
| **Cacher dans les listes** | Le produit est retiré des pages de catégories et des résultats de recherche |
| **Afficher comme indisponible** | Le produit est visible mais ne peut pas être ajouté au panier |
| **Afficher le bouton "Notifier"** | Les clients peuvent s'inscrire avec leur e-mail pour être notifiés lorsqu'il y a de nouveau du stock |
| **Autoriser les commandes en attente** | Les clients peuvent acheter le produit même lorsque le stock est à zéro |

Définissez **Message en cas de rupture de stock** pour personnaliser le texte affiché lorsque le produit n'est pas disponible (par défaut : `En rupture de stock`).

Définissez **Message de commande en attente** pour personnaliser le texte affiché pour les produits commandables en attente (par défaut : `Disponible sur commande en attente`).

### Affichage des informations de livraison

| Paramètre | Description |
|---------|-------------|
| **Afficher l'emplacement "Expédié depuis"** | Afficher le nom du entrepôt sur la page du produit |
| **Afficher la livraison estimée** | Afficher les dates estimées de livraison calculées à partir de l'emplacement de l'entrepôt |

### Autoriser les commandes en attente (à l'échelle du site)

Cochez **Autoriser les commandes en attente** pour permettre aux clients d'acheter par défaut tout produit en rupture de stock. Les produits individuels et les catégories peuvent remplacer ce paramètre.

## Notifications de retour en stock

Lorsque vous définissez l'action en cas de rupture de stock sur **Afficher le bouton "Notifier"**, les clients peuvent entrer leur adresse e-mail sur la page du produit pour recevoir un e-mail lorsqu'il y a de nouveau du stock.

### Voir les demandes de notification

Accédez à **Catalogue > Notifications de stock** pour voir toutes les demandes de notification des clients. Chaque enregistrement affiche :
- Adresse e-mail du client
- Produit et variante (si applicable)
- Entreprise préférée (si le client a sélectionné une préférence régionale)
- Lorsque la demande a été créée
- Lorsque la notification a été envoyée (vide si elle n'a pas encore été envoyée)

### Lors de l'envoi des notifications

Spwig envoie automatiquement les e-mails de retour en stock lorsque le niveau de stock d'un produit dépasse zéro. Le champ **Notifié à** enregistre la date à laquelle l'e-mail a été envoyé.

Les clients reçoivent un seul e-mail de notification. Une fois notifiés, ils doivent s'inscrire à nouveau si le produit est à nouveau en rupture de stock.

### Filtre des demandes de notification

Utilisez les filtres administrateurs pour trouver :
- Des demandes pour un produit spécifique
- Des demandes qui ont déjà été notifiées (pour voir qui a été contacté)
- Des demandes en attente (clients en attente d'un réapprovisionnement)

## Remplacement au niveau du produit

Les paramètres d'affichage du stock à l'échelle du site peuvent être remplacés par produit ou par catégorie. Sur le formulaire d'édition du produit, cherchez la section **Stock** où vous pouvez définir une action **En cas de rupture de stock** spécifique au produit différente du paramètre par défaut global.

Cela est utile lorsque vous souhaitez que la plupart des produits autorisent les commandes en attente mais que quelques produits soient définis sur "Notifier" — ou lorsque un produit spécifique doit être caché lorsqu'il est en rupture de stock.

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- Définissez le **seuil de stock bas** sur le point de commande que vous utilisez habituellement, afin que les clients soient avertis de la disponibilité limitée avant que vous ne soyez complètement en rupture de stock.
- Utilisez l'option **Afficher le bouton « Alerter »** au lieu de cacher les produits en rupture de stock — les clients qui s'inscrivent représentent une demande réelle qui peut justifier une commande de réapprovisionnement.
- Activez **Afficher la quantité exacte** avec parcimonie.

Pour la plupart des magasins, afficher « Seulement 3 restants ! » fonctionne mieux que d'afficher le nombre exact, car cela crée de l'urgence sans révéler l'ensemble de votre stock.
- Vérifiez la liste des notifications de stock avant de passer une nouvelle commande — le nombre de demandes de notification en attente vous indique la demande existante pour ce produit.
- Si vous utilisez les commandes en attente, mettez à jour votre **message de commande en attente** pour fixer des attentes précises (ex. : « Expédié en 2 à 3 semaines — commandez maintenant pour réserver votre place »).
- Combinez les notifications de rupture de stock avec le marketing par e-mail : lorsque vous réapprovisionnez un produit populaire, envoyez une campagne à toutes les personnes inscrites, et non seulement à l'e-mail de notification automatique.