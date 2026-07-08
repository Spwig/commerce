---
title: Produits personnalisables
---

Les produits personnalisables permettent à vos clients de concevoir leurs propres produits à l'aide d'un éditeur visuel directement sur votre boutique en ligne. Que vous vendiez des t-shirts personnalisés, des affiches personnalisées, des articles de merchandising de marque ou des cartes de vœux, cette fonctionnalité donne aux clients les outils nécessaires pour ajouter du texte, charger des images et utiliser des illustrations pour créer des designs uniques — sans quitter votre boutique.

## Fonctionnement

Un produit personnalisable combine un produit Spwig standard avec un **éditeur de conception visuel**. Vous définissez les surfaces concevables du produit (par exemple, l'avant et l'arrière d'un t-shirt), vous chargez des images de maquettes afin que les clients puissent voir leur conception dans le contexte, et vous définissez les règles concernant ce que les clients peuvent faire sur chaque surface.

Lorsqu'un client visite un produit personnalisable sur votre boutique en ligne, il voit un éditeur de toile vivant superposé à votre image de maquette. Il peut ajouter du texte, charger ses propres images et parcourir votre bibliothèque d'illustrations pour créer sa conception. L'éditeur affiche la conception exactement telle qu'elle apparaîtra sur le produit final.

### Deux cas d'utilisation

Les produits personnalisables s'adaptent bien à deux scénarios courants :

| Cas d'utilisation | Exemple | Surfaces | Configuration typique |
|------------------|---------|----------|----------------------|
| **Conception de vêtements** | T-shirts personnalisés, sweat-shirts, sacs à dos | Plusieurs (avant, arrière, manches) | Polices épaisse, illustrations humoristiques/sportives, contraintes par surface |
| **Conception d'impression** | Affiches, cartes de vœux, cartes de visite | Unique (avant uniquement) | Haute résolution, paramètres de débordement, polices élégantes, bordures décoratives |

Le processus de configuration est le même pour les deux — la différence réside dans le nombre de surfaces que vous définissez, les illustrations et polices que vous fournissez, et la manière dont vous configurez les paramètres d'impression.

## Concepts clés

### Configuration de conception

Chaque produit personnalisable a une **configuration de conception** qui contrôle le comportement global de l'éditeur : les outils disponibles (texte, téléchargement d'image, illustrations), les limites de téléchargement et les règles de tarification. C'est le tableau de bord principal pour l'éditeur de conception du produit.

### Surfaces

Une **surface** est une face concevable de votre produit. Un t-shirt a généralement trois surfaces (avant, arrière, manche), tandis qu'une affiche n'en a qu'une. Chaque surface a sa propre image de maquette, la position de la zone de conception, les dimensions physiques et les paramètres de qualité d'impression.

### Zone de conception

La **zone de conception** est la zone rectangulaire sur l'image de maquette où les clients peuvent placer leurs éléments de conception. Vous positionnez cette zone visuellement sur la page de configuration de l'administrateur en la déplaçant et en la redimensionnant sur l'image de maquette. Cette zone définit l'endroit où les conceptions apparaîtront sur le produit final.

### Modèles

Les **modèles de conception** sont des conceptions prêtes à l'emploi que vous créez pour les clients. Au lieu de commencer sur une toile vierge, les clients peuvent parcourir votre galerie de modèles, en choisir un qui leur plaît et le personnaliser. Les modèles peuvent inclure des éléments verrouillés que les clients ne peuvent pas modifier — par exemple, un logo d'entreprise qui doit toujours apparaître à la même position.

### Illustrations et polices

Vous créez une **bibliothèque d'illustrations** d'images que les clients peuvent ajouter à leurs conceptions, organisées en catégories (par exemple, « Sports », « Bordures », « Vacances »). Vous pouvez également charger des **polices personnalisées** en plus des polices système standard, offrant ainsi aux clients plus d'options créatives.

### Tarification

L'éditeur de conception prend en charge un modèle tarifaire flexible avec quatre composants de frais :

| Type de frais | Description |
|---------------|-------------|
| **Frais de conception de base** | Frais fixes ajoutés lorsqu'une personnalisation est appliquée |
| **Frais par surface** | Frais supplémentaires pour chaque surface utilisée au-delà de la première |
| **Frais par téléchargement** | Frais pour chaque image téléchargée par le client |
| **Frais par texte** | Frais pour chaque élément de texte ajouté |

La tarification est mise à jour en temps réel à mesure que le client ajoute des éléments, il n'y a donc aucune surprise à la caisse.

## Modes d'éditeur

Spwig propose deux modes d'éditeur :

- **Éditeur de toile** — Un éditeur de conception visuel complet avec une toile vivante, des outils de texte, un téléchargement d'image, un navigateur d'illustrations et une prévisualisation en temps réel sur l'image de maquette du produit.

# Mode recommandé pour la plupart des produits personnalisables

C'est le mode recommandé pour la plupart des produits personnalisables.
- **Formulaire simple** — Une approche traditionnelle basée sur un formulaire où les clients remplissent des champs de texte et téléchargent des images sans canevas visuel.

Adapté aux produits avec une personnalisation minimale (par exemple, graver un nom sur un bijou).

## Workflow du vendeur

La création d'un produit personnalisable suit ce workflow :

1. **Créer le produit** — Ajouter un nouveau produit avec le type défini sur **Produit personnalisable**
2. **Configurer les surfaces** — Définir chaque face pouvant être conçue, télécharger des images de maquettes et positionner les zones de conception
3. **Configurer les paramètres** — Choisir les outils à activer, définir les limites de téléchargement et configurer le prix
4. **Ajouter des éléments** — Construire votre bibliothèque d'images vectorielles et télécharger des polices personnalisées
5. **Créer des modèles** — Concevoir des points de départ prédéfinis avec des contrôles de verrouillage optionnels
6. **Tester et publier** — Prévisualiser l'éditeur sur le site de vente et vérifier que tout fonctionne

Pour des instructions détaillées sur la configuration, consultez [Configuration d'un produit personnalisable](/admin/customizable-product/).

## Expérience client

Lorsqu'un client visite un produit personnalisable sur votre site de vente :

1. **Parcourir les modèles** — Ils peuvent commencer par un modèle prédéfini ou commencer avec un canevas vide
2. **Changer de surface** — Les onglets en haut permettent de basculer entre les surfaces (par exemple, avant et arrière d'un t-shirt)
3. **Ajouter des éléments** — Le panneau d'outils fournit des outils de texte, de téléchargement d'images et d'images vectorielles
4. **Personnaliser** — Ils peuvent ajuster les polices, les couleurs, les tailles, les positions et appliquer des filtres d'images
5. **Voir le prix** — Le coût de conception s'affiche en temps réel à mesure qu'ils ajoutent des éléments
6. **Enregistrer les conceptions** — Les clients inscrits peuvent enregistrer leurs conceptions pour continuer à les modifier plus tard
7. **Ajouter au panier** — La conception est liée à l'élément du panier et figée lors de la passation de commande

## Ce qui se passe après la commande

Lorsqu'un client passe une commande contenant un produit personnalisé :

- La conception est **figée en tant que capture d'écran** — elle ne peut plus être modifiée après l'achat
- Le système génère **des fichiers de livraison à haute résolution** pour chaque surface
- Vous pouvez télécharger ces fichiers prêts à imprimer depuis la page des détails de la commande dans votre tableau de bord administrateur
- Les fichiers sont rendus à la résolution en DPI que vous avez configurée pour chaque surface

Pour plus de détails sur la livraison des commandes personnalisées, consultez [Livraison des commandes de produits personnalisables](/admin/orders/).

## Conseils

- Commencez par un produit simple (une seule surface, comme une affiche) pour apprendre le processus de configuration avant de passer aux produits à plusieurs surfaces comme les t-shirts.
- Téléchargez des images de maquettes de haute qualité — ce sont les premières choses que les clients voient et fixent l'attente de qualité pour toute l'expérience.
- Créez 3 à 5 modèles de conception pour chaque produit afin de réduire l'intimidation du "canevas vide" et d'inspirer les clients.
- Utilisez des contraintes par surface pour contrôler ce que les clients peuvent faire sur chaque surface. Par exemple, autorisez uniquement le téléchargement d'un petit logo sur le manche d'un t-shirt tout en permettant une liberté totale de conception sur le devant.
- Définissez des exigences minimales en DPI adaptées à votre méthode d'impression — 150 DPI pour l'impression par serigraphie, 300 DPI pour l'impression numérique de haute qualité.
- Testez le flux client complet (conception, enregistrement, ajout au panier, paiement) avant de publier un produit personnalisable.