---
title: Attributs des produits
---

Les attributs des produits définissent les dimensions selon lesquelles un produit peut varier — par exemple, la Taille, la Couleur ou le Matériau. Une fois que vous avez créé un attribut et ses valeurs possibles, vous pouvez l'assigner à tout produit variable et Spwig générera le sélecteur de variation que les clients utiliseront lors du paiement.

Accédez à **Catalogue > Attributs des produits** pour gérer les attributs et leurs valeurs.

## Fonctionnement des attributs

Les attributs sont réutilisables dans tout votre catalogue. Vous les créez une seule fois et les assignez à autant de produits que nécessaire. Chaque attribut possède :

- Un **nom** qui l'identifie (ex. : "Taille")
- Un **type d'affichage** qui contrôle l'apparence du sélecteur sur la page du produit
- Un ou plusieurs **valeurs** qui représentent les options disponibles (ex. : "Petit", "Moyen", "Grand")

Lorsque vous assignez un attribut à un produit, vous spécifiez également lesquelles de ses valeurs sont disponibles pour ce produit particulier. Cela signifie qu'un attribut "Taille" pourrait avoir des valeurs allant de S à 3XL, mais un t-shirt spécifique pourrait ne proposer que S, M et L.

## Types d'affichage des attributs

Le champ **Type** d'un attribut contrôle l'apparence du widget de sélection sur la page du produit de votre boutique en ligne :

| Type | Apparence | Meilleur pour |
|---|---|---|
| **Sélecteur déroulant** | Un menu déroulant que le client ouvre pour choisir une valeur | Les attributs avec de nombreuses valeurs (ex. : une gamme de tailles avec 10+ tailles) |
| **Échantillons de couleur** | Des cercles ou carrés colorés que le client clique | Les attributs de couleur où l'identification visuelle est utile |
| **Groupe de boutons** | Des boutons en forme de pastille affichés en ligne | Les attributs avec un petit nombre de valeurs (ex. : S, M, L, XL) |
| **Boutons radio** | Liste classique de boutons radio | Tout attribut où vous souhaitez un agencement clair et accessible |

Choisissez le type d'affichage qui correspond à la manière dont vos clients pensent à l'attribut. Pour la couleur, les échantillons sont presque toujours préférables à un menu déroulant. Pour la taille, les groupes de boutons fonctionnent bien lorsque le nombre d'options est inférieur à 8.

## Créer un attribut

1. Accédez à **Catalogue > Attributs des produits**
2. Cliquez sur **+ Ajouter un attribut de produit**
3. Entrez le **Nom** (ex. : `Taille`, `Couleur`, `Matériau`)
4. Le **Slug** est rempli automatiquement — vous pouvez le laisser tel quel
5. Sélectionnez le **Type** (Sélecteur déroulant, Échantillon de couleur, Groupe de boutons ou Boutons radio)
6. Cochez **Obligatoire** si les clients doivent sélectionner cet attribut avant de pouvoir ajouter le produit à leur panier — c'est approprié pour la plupart des attributs de taille et de couleur
7. Définissez un **Ordre de tri** — les attributs avec des numéros plus bas apparaissent en premier dans le sélecteur de variation sur la page du produit
8. Ajoutez les valeurs de l'attribut directement dans la section **Valeurs** (voir ci-dessous)
9. Cliquez sur **Enregistrer**

## Ajouter des valeurs d'attribut

Les valeurs d'attribut sont les options individuelles au sein d'un attribut. Vous pouvez les ajouter directement lors de la création ou de la modification d'un attribut, en utilisant le formulaire de valeurs intégré en bas de la page de détails de l'attribut.

Pour chaque valeur :

- **Valeur** — l'étiquette d'affichage (ex. : `Petit`, `Rouge`, `Coton`)
- **Slug** — rempli automatiquement à partir de la valeur ; utilisé dans les URL et les identifiants de variantes
- **Code hexadécimal de la couleur** — pertinent uniquement pour les attributs de type **Échantillon de couleur**. Entrez un code de couleur hexadécimal (ex. : `#FF0000` pour le rouge) afin que l'échantillon affiche la bonne couleur.
- **Ordre de tri** — contrôle l'ordre dans lequel les valeurs apparaissent dans le sélecteur. Attribuez des numéros plus bas aux valeurs que vous souhaitez afficher en premier.

### Classer les valeurs de manière logique

Pour les attributs de taille, définissez l'ordre de tri de sorte que les tailles passent du petit au grand :

| Valeur | Ordre de tri |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Pour les attributs de couleur, vous pouvez trier alphabetiquement ou regrouper des couleurs similaires — tout ce qui a le plus de sens pour vos clients.

## Gérer les valeurs d'attribut séparément

Vous pouvez également gérer les valeurs d'attribut de manière indépendante à **Catalogue > Valeurs d'attribut**. Cette liste est utile lorsque vous avez besoin de trouver ou de mettre à jour une valeur spécifique dans votre catalogue sans ouvrir chaque attribut individuellement. La liste peut être filtrée par nom d'attribut.

## Assigner des attributs aux produits

Les attributs sont assignés au niveau du produit, et non de manière globale.

Pour ajouter un attribut à un produit :

1. Accédez à **Catalogue > Produits** et ouvrez un produit variable
2. Dans l'onglet **Variations**, trouvez la section **Attributs**
3. Sélectionnez l'attribut que vous souhaitez ajouter
4. Choisissez lesquelles des valeurs de cet attribut sont disponibles pour ce produit
5. Enregistrez le produit — Spwig générera les combinaisons de variantes correspondantes

Pour obtenir des instructions détaillées sur la configuration des variantes de produit, consultez le sujet d'aide **Product Variants**.

## Exemples pratiques

### Exemple : Attribut de taille de vêtement

| Champ | Valeur |
|---|---|
| Nom | Size |
| Type | Button Group |
| Est obligatoire | Oui |
| Ordre de tri | 1 |
| Valeurs | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Exemple : Attribut de palette de couleurs

| Champ | Valeur |
|---|---|
| Nom | Colour |
| Type | Color Swatch |
| Est obligatoire | Oui |
| Ordre de tri | 2 |
| Valeurs | Black (#000000), White (#FFFFFF), Navy (#001F5B), Red (#CC0000) |

### Exemple : Attribut de matériau

| Champ | Valeur |
|---|---|
| Nom | Material |
| Type | Dropdown Select |
| Est obligatoire | Non |
| Ordre de tri | 3 |
| Valeurs | 100% Cotton, Cotton/Polyester Blend, Merino Wool, Linen |

## Conseils

- Créez des attributs qui représentent des décisions d'achat réelles que les clients font — si les clients n'ont pas besoin de les choisir, ils n'ont peut-être pas besoin d'être un attribut
- Utilisez un nommage cohérent à travers votre catalogue : si certains produits utilisent « Colour » et d'autres « Color », les clients et votre équipe trouveront cette incohérence confuse
- L'ordre de tri à la fois pour les attributs et les valeurs est important — placez l'attribut le plus important en premier (généralement Size ou Colour) et classez les valeurs dans une séquence logique
- Le type Color Swatch nécessite des codes hexacimaux précis ; testez les couleurs dans un sélecteur de couleurs de navigateur avant d'enregistrer pour vous assurer que la palette correspond à la couleur réelle du produit
- Si vous avez besoin de renommer un attribut (par exemple, de « Color » à « Colour »), mettez à jour le champ **Nom** plutôt que de créer un nouveau attribut — le changement de nom n'affecte pas les assignations existantes des produits