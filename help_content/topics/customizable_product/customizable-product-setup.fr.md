---
title: Configuration d'un produit personnalisable
---

Ce guide vous guide à travers le processus complet de configuration d'un produit personnalisable, depuis la création du produit jusqu'à la configuration des surfaces, du prix et des restrictions de téléchargement. Deux exemples pratiques sont utilisés tout au long du document : un **t-shirt personnalisé** (vêtement à plusieurs surfaces) et un **affiche personnalisée** (impression à une seule surface).

## Étape 1 : Créer le produit

1. Accédez à **Produits > Tous les produits** et cliquez sur **+ Ajouter un produit**
2. Définissez **Type de produit** sur **Produit personnalisable**
3. Remplissez le nom du produit, la description, les images et le prix comme vous le feriez pour tout autre produit
4. Enregistrez le produit

Après l'enregistrement, un nouveau bouton **Ouvrir l'éditeur de conception** apparaît sur le formulaire du produit. Cela vous mène à la page dédiée à la configuration où vous configurez l'éditeur de conception visuel.

## Étape 2 : Accéder à la configuration de l'éditeur de conception

1. Ouvrez le produit que vous venez de créer dans l'administration
2. Cliquez sur le bouton **Ouvrir l'éditeur de conception** (dans la section Produit personnalisable)
3. La page de configuration s'ouvre avec trois onglets : **Surfaces**, **Paramètres** et **Prix**

La page de configuration est l'endroit où vous définissez tout ce qui concerne l'éditeur de conception pour ce produit.

## Étape 3 : Ajouter des surfaces de conception

Une surface représente une face personnalisable de votre produit. Cliquez sur **+ Ajouter une surface** pour créer chaque surface.

### Exemple de t-shirt : 3 surfaces

| Surface | Nom | Dimensions | Zone de conception | Notes |
|---------|-----|------------|-------------------|-------|
| 1 | Avant | 300 x 400 mm | Zone centrale du torse | Zone principale de conception |
| 2 | Arrière | 300 x 400 mm | Zone supérieure du dos | Zone secondaire de conception |
| 3 | Manche gauche | 100 x 100 mm | Zone supérieure du bras | Zone uniquement pour le logo |

### Exemple d'affiche : 1 surface

| Surface | Nom | Dimensions | Zone de conception | Notes |
|---------|-----|------------|-------------------|-------|
| 1 | Avant | 210 x 297 mm (A4) | Zone imprimable complète | Une seule surface, haute résolution (DPI) |

### Configuration de chaque surface

Pour chaque surface, vous configurez ce qui suit :

**Informations de base :**
- **Nom** — Ce que les clients voient dans les onglets de surface (ex. : "Avant", "Arrière")
- **Slug** — Identifiant sécurisé pour l'URL, généré automatiquement à partir du nom
- **Ordre de tri** — Définit l'ordre d'apparition des surfaces (les numéros plus bas apparaissent en premier)

**Image de maquette :**
- Cliquez sur la zone d'image de maquette pour ouvrir la bibliothèque multimédia et sélectionner une photo du produit montrant cette surface
- Utilisez une photo de haute qualité de votre produit pris depuis l'angle correct

**Positionnement de la zone de conception :**
- Après avoir sélectionné une image de maquette, un surbrillance rectangulaire apparaît sur l'aperçu
- **Glissez** la surbrillance pour positionner là où la zone de conception doit être sur la maquette
- **Redimensionnez** la surbrillance en déplaçant ses bords pour définir les limites de la zone de conception
- La zone est stockée comme des coordonnées basées sur des pourcentages, donc elle s'adapte à toute taille d'écran

La zone de conception indique à l'éditeur exactement où sur l'image du produit la conception du client apparaîtra. Positionnez-la soigneusement pour correspondre à la zone imprimable réelle de votre produit.

**Dimensions physiques :**
- **Largeur** et **Hauteur** — Les dimensions réelles de la zone de conception
- **Unité** — Millimètres, pouces ou pixels
- Ces dimensions déterminent le rapport d'aspect du canevas de conception et sont utilisées pour calculer le DPI d'impression

**Paramètres d'impression :**
- **DPI minimum** — Le nombre minimum acceptable de points par pouce. Les clients voient un avertissement si leurs images téléchargées sont en dessous de ce seuil. Valeur par défaut : 150
- **DPI recommandé** — La résolution idéale pour la meilleure qualité d'impression. Valeur par défaut : 300
- **Bleed (mm)** — Marge supplémentaire en dehors de la zone de conception pour l'impression de bleed. Mettez à 0 si aucun bleed n'est nécessaire (courant pour les vêtements), ou 3 mm pour les produits d'impression professionnelle
- **Nombre maximum de couleurs** — Pour l'impression en sérigraphie, vous pouvez limiter le nombre de couleurs. Laissez vide pour un nombre illimité (impression numérique)
- **Couleur d'arrière-plan** — Couleur par défaut du canevas

### Paramètres d'impression pour le t-shirt vs l'affiche

| Paramètre | T-shirt | Affiche |
|-----------|---------|--------|
| DPI minimum | 150 | 200 |
| DPI recommandé | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Nombre maximum de couleurs | 6 (sérigraphie) | Vide (illimité) |
| Couleur d'arrière-plan | Couleur correspondant au vêtement | `#ffffff` (blanc) |

## Étape 4 : Contraintes par surface

Chaque surface peut remplacer les paramètres globaux des fonctionnalités. Cela vous permet d'autoriser des outils différents sur différentes surfaces.

Les options de contraintes sont les suivantes :

| Paramètre | Options | Description |
|---------|---------|-------------|
| **Autoriser le texte** | Hériter / Oui / Non | Indique si les clients peuvent ajouter du texte sur cette surface |
| **Autoriser le téléchargement d'image** | Hériter / Oui / Non | Indique si les clients peuvent télécharger des images sur cette surface |
| **Autoriser les dessins** | Hériter / Oui / Non | Indique si les clients peuvent utiliser des dessins sur cette surface |
| **Nombre maximal d'éléments** | Nombre ou vide | Nombre maximal d'éléments de conception autorisés sur cette surface |

Lorsqu'il est défini sur **Hériter**, la surface utilise les paramètres configurés dans les paramètres globaux (Étape 6). Lorsqu'il est défini sur **Oui** ou **Non**, il remplace le paramètre global pour cette surface spécifique.

### Exemple : Contrainte de manche de t-shirt

Pour la surface de la manche du t-shirt, vous pouvez souhaiter limiter la personnalisation à un petit logo uniquement :

| Paramètre | Valeur | Raison |
|---------|-------|--------|
| Autoriser le texte | Non | Trop petit pour un texte lisible |
| Autoriser le téléchargement d'image | Oui | Permet le téléchargement d'un petit logo |
| Autoriser les dessins | Non | Garde simple |
| Nombre maximal d'éléments | 1 | Un seul logo |

Les surfaces avant et arrière resteront définies sur **Hériter**, permettant à tous les outils d'être utilisés comme définis dans les paramètres globaux.

### Exemple : Contrainte de poster

Pour un poster, toutes les surfaces héritent généralement des paramètres globaux, car il n'y a qu'une seule surface et tous les outils devraient être disponibles. Aucune surcharge par surface n'est nécessaire.

## Étape 5 : Configurer les restrictions de téléchargement

Sur l'onglet **Paramètres**, configurez la manière dont les clients peuvent télécharger des fichiers :

| Paramètre | Description | Exemple de t-shirt | Exemple de poster |
|---------|-------------|-----------------|----------------|
| **Taille maximale de téléchargement** | Taille maximale par téléchargement | 10 Mo | 20 Mo |
| **Nombre maximal de téléchargements par surface** | Nombre d'images par surface | 5 | 3 |
| **Types de téléchargement autorisés** | Formats de fichiers acceptés | JPG, PNG, WebP | JPG, PNG, WebP |

Des limites de taille de fichier plus importantes sont recommandées pour les produits d'impression où les clients doivent télécharger des images de haute résolution.

## Étape 6 : Paramètres de l'éditeur

Sur l'onglet **Paramètres**, configurez le comportement global de l'éditeur :

**Mode d'édition :**
- **Éditeur de toile** — Éditeur visuel complet avec aperçu en temps réel de la toile. Recommandé pour la plupart des produits.
- **Formulaire simple** — Champs de formulaire traditionnels pour une personnalisation basique (par exemple, du texte gravé uniquement).

**Paramètres de fonctionnalité (valeurs par défaut globales) :**
- **Autoriser le texte** — Permet aux clients d'ajouter des éléments de texte
- **Autoriser le téléchargement d'image** — Permet aux clients de télécharger leurs propres images
- **Autoriser les dessins** — Permet aux clients de parcourir et d'utiliser votre bibliothèque de dessins

Ces paramètres globaux s'appliquent à toutes les surfaces sauf si elles sont remplacées par des contraintes par surface (Étape 4).

## Étape 7 : Configurer les prix

Sur l'onglet **Prix**, définissez les frais de conception qui sont ajoutés au prix de base du produit :

| Frais | Description |
|-----|-------------|
| **Frais de conception de base** | Frais fixes ajoutés lorsqu'une personnalisation est appliquée |
| **Frais par surface** | Frais supplémentaires pour chaque surface utilisée au-delà de la première |
| **Frais par téléchargement** | Frais pour chaque image téléchargée par le client |
| **Frais par texte** | Frais pour chaque élément de texte ajouté |

### Exemple : Prix du t-shirt

| Frais | Montant | Raison |
|-----|--------|-----------|
| Frais de conception de base | 5,00 $ | Couvre le coût de mise en place pour toute commande personnalisée |
| Frais par surface | 2,00 $ | Chaque surface supplémentaire ajoute un coût d'impression |
| Frais par téléchargement | 1,00 $ | Les images personnalisées nécessitent un traitement |
| Frais par texte | 0,50 $ | Le texte est plus simple à produire que les images |

**Exemple de calcul :** Un client conçoit un t-shirt avec du texte sur le devant et un logo sur le dos :
- Frais de conception de base : 5,00 $
- 1 surface supplémentaire (dos) : 2,00 $
- 1 logo téléchargé : 1,00 $
- 1 élément de texte : 0,50 $
- **Total des frais de conception : 8,50 $** (ajouté au prix de base du produit)

### Exemple : Prix du poster


| Frais | Montant | Justification |
|-----|--------|-----------|
| Frais de conception de base | $0,00 | Aucun frais de base — le prix du produit le couvre |
| Frais par surface | $0,00 | Une seule surface, non applicable |
| Frais par téléchargement | $2,00 | Traitement en haute résolution |
| Frais par texte | $0,00 | Le texte est inclus dans l'expérience de base |

**Exemple de calcul :** Un client crée un poster avec 2 photos téléchargées et 3 éléments de texte :
- Frais de conception de base : $0,00
- 2 photos téléchargées : $4,00
- 3 éléments de texte : $0,00
- **Total des frais de conception : $4,00**

Le frais de conception est affiché aux clients en temps réel à mesure qu'ils ajoutent des éléments, afin qu'ils puissent voir l'impact des coûts de chaque ajout avant d'ajouter au panier.

## Comparaison des paramètres à vue d'œil

| Aspect | T-shirt personnalisé | Poster personnalisé |
|--------|---------------|---------------|
| Surfaces | 3 (avant, arrière, manche) | 1 (avant) |
| Images de présentation | 3 photos du produit | 1 photo du produit |
| Positionnement de la zone | Zones torse/arrière/bras | Zone imprimable complète |
| Dimensions | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI minimum | 150 | 200 |
| Marge de sécurité | 0 mm | 3 mm |
| Nombre maximum de couleurs | 6 | Illimité |
| Contraintes par surface | Manche restreinte | Aucune nécessaire |
| Modèle de tarification | Base + surface + téléchargement + texte | Seuls les frais de téléchargement |

## Conseils

- Testez toujours l'éditeur de conception du point de vue du client après avoir terminé la configuration. Visitez la page du produit sur le site de vente et essayez d'ajouter du texte, de télécharger une image et de basculer entre les surfaces.
- Téléchargez des images de présentation qui correspondent le plus à l'apparence réelle du produit. Pour les t-shirts, photographiez chaque angle séparément. Pour les posters, utilisez une photo nette en format plat ou un modèle de cadre.
- Positionnez la zone de conception de manière conservatrice — il vaut mieux définir une zone légèrement plus petite que d'avoir des conceptions qui impriment dans les coutures ou les bords.
- Définissez le DPI minimum en fonction de votre méthode d'impression : 150 pour l'impression par serigraphie, 200 pour l'impression numérique standard, 300 pour une impression offset de haute qualité.
- Utilisez une marge de sécurité de 3 mm pour tout produit qui sera coupé après l'impression (posters, cartes de visite, flyers). Définissez la marge de sécurité à 0 pour les produits où le design est appliqué à une surface existante (t-shirts, tasses, coques de téléphone).
- Commencez par un tarif simple et ajustez-le en fonction des retours des clients. Beaucoup de commerçants commencent par un seul frais de conception de base et ajoutent des frais par élément plus tard.