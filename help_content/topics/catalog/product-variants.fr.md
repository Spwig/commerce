---
title: Variantes de Produit
---

Les variantes de produit vous permettent de proposer un seul produit en plusieurs options — comme différentes tailles, couleurs ou matériaux — chacune avec son propre SKU, prix et niveau de stock. Accédez à n'importe quel **Produit Variable** et cliquez sur l'onglet **Variations**.

![Variantes de produit](/static/core/admin/img/help/product-variants/product-variants.webp)

## Comprendre les Variantes

Un **Produit Variable** est un type de produit qui prend en charge plusieurs variations. Par exemple, un T-Shirt peut être disponible en :
- **Couleurs** : Bleu, Rouge, Vert
- **Tailles** : S, M, L, XL

Chaque combinaison (ex. : "Bleu / Grand") devient une variante distincte avec son propre inventaire et son propre prix.

## Configurer un Produit Variable

### Étape 1 : Définir le Type de Produit

1. Ouvrez le formulaire d'édition du produit (ou créez un nouveau produit)
2. Dans l'onglet **Informations de Base**, définissez **Type de Produit** sur **Produit Variable**
3. Enregistrez le produit

### Étape 2 : Définir les Attributs

Les attributs sont les options qui différencient vos variantes (ex. : Taille, Couleur).

1. Accédez à l'onglet **Variations**
2. Dans la section **Attributs du Produit**, cliquez sur **+ Ajouter un Attribut** pour assigner un attribut existant, ou **Créer Nouveau** pour en définir un nouveau
3. Pour chaque attribut, spécifiez les valeurs disponibles (ex. : Petit, Moyen, Grand)

### Étape 3 : Créer les Variantes

1. Dans la section **Variantes du Produit**, cliquez sur **+ Ajouter une Nouvelle Variante**
2. Configurez chaque variante :
   - **Nom** — Étiquette descriptive (ex. : "Bleu", "Grand / Rouge")
   - **SKU** — Code unique d'unité de gestion des stocks
   - **Prix** — Prix spécifique à la variante (peut différer du produit de base)
   - **Stock** — Niveau d'inventaire actuel
3. Répétez pour chaque variante nécessaire

## Gérer les Variantes

### Détails de la Variante

Chaque carte de variante affiche :
- **Nom** et **SKU** — Informations d'identification
- **Prix** — Prix de vente actuel
- **Niveau de stock** — Quantité disponible avec indicateur de statut (En Stock / Stock Faible / Rupture de Stock)

Cliquez sur une carte de variante pour développer et modifier tous ses détails.

### Paramètres Spécifiques à la Variante

Chaque variante peut avoir ses propres paramètres :

| Paramètre | Description |
|-----------|-------------|
| **Prix** | Remplacer le prix du produit de base |
| **Prix de comparaison** | Afficher un prix promotionnel avec barré |
| **SKU** | Identifiant unique pour l'inventaire |
| **Niveau de Stock** | Suivi d'inventaire indépendant |
| **Poids** | Pour les calculs d'expédition |
| **Image** | Image de produit spécifique à la variante |

### Modifier une Variante

1. Cliquez sur l'**icône de modification** sur la carte de la variante
2. Modifiez les champs souhaités
3. Cliquez sur **Enregistrer** pour mettre à jour

### Supprimer une Variante

1. Cliquez sur l'**icône de suppression** sur la carte de la variante
2. Confirmez la suppression

**Remarque :** La suppression d'une variante supprime son enregistrement d'inventaire. Cette action est irréversible.

## Attributs

### Que Sont les Attributs ?

Les attributs sont des définitions d'options réutilisables. Une fois que vous avez créé un attribut comme "Taille" avec les valeurs "S, M, L, XL", vous pouvez l'assigner à n'importe quel produit variable.

### Créer des Attributs

1. Dans l'onglet Variations, cliquez sur **Créer Nouveau** dans la section Attributs du Produit
2. Saisissez le nom de l'attribut (ex. : "Couleur")
3. Ajoutez des valeurs (ex. : "Rouge", "Bleu", "Vert")
4. Enregistrez l'attribut

### Assigner des Attributs

Les attributs peuvent être assignés à plusieurs produits. Le même attribut "Taille" peut être utilisé pour les T-Shirts, Pantalons et Chaussures.

## Affichage en Boutique

Sur la boutique, les produits variables affichent :
- Des sélecteurs d'options (menus déroulants ou échantillons) pour chaque attribut
- Des mises à jour automatiques du prix lorsqu'une variante est sélectionnée
- La disponibilité du stock par variante
- Les images spécifiques à la variante

## Conseils

- Utilisez des noms d'attributs cohérents sur tous les produits pour une expérience d'achat uniforme.
- Configurez tous les attributs avant de créer les variantes pour rationaliser le processus.
- Téléchargez des images spécifiques pour chaque variante afin que les clients puissent voir exactement ce qu'ils commandent.
- Gardez les SKU systématiques (ex. : "TSHIRT-BLEU-G") pour faciliter la gestion de l'inventaire.
- Utilisez le prix de comparaison sur les variantes pour lancer des promotions spécifiques par taille ou couleur.
