---
title: Éditeur d'ombres
---

L'éditeur d'ombres vous permet d'ajouter de la profondeur et des dimensions aux éléments à l'aide d'ombres de boîte et d'ombres de texte configurables. Les ombres créent une hiérarchie visuelle, attirent l'attention sur les éléments importants et donnent à votre boutique en ligne un aspect raffiné et moderne. Ouvrez l'onglet **Style** de n'importe quel élément et cherchez le groupe **Effets** pour accéder à l'éditeur d'ombres.

![Éditeur d'ombres](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Types d'ombres

L'éditeur propose deux onglets en haut de l'interface :

- **Ombre de boîte** — Ajoute une ombre autour de la boîte délimitée de l'élément. Utilisez-la pour les cartes, les boutons, les conteneurs, les images et les sections.
- **Ombre de texte** — Ajoute une ombre uniquement derrière les caractères de texte. Utilisez-la pour les titres ou le texte superposé sur des images afin d'améliorer la lisibilité.

Chaque onglet dispose d'une configuration indépendante. Vous pouvez appliquer à la fois une ombre de boîte et une ombre de texte au même élément si nécessaire.

## Propriétés des ombres

Chaque couche d'ombre est définie par les propriétés suivantes :

| Propriété | Description | Plage |
|----------|-------------|-------|
| **Décalage X** | Distance horizontale de l'ombre par rapport à l'élément | -50px à 50px |
| **Décalage Y** | Distance verticale de l'ombre par rapport à l'élément | -50px à 50px |
| **Rayon de flou** | Définit la douceur ou la diffusion de la bordure de l'ombre. Des valeurs plus élevées produisent des ombres plus douces. | 0px à 100px |
| **Rayon de dispersion** | Agrandit ou réduit la taille de l'ombre par rapport à l'élément (ombre de boîte uniquement) | -50px à 50px |
| **Couleur** | Couleur de l'ombre, configurable avec un support d'opacité complet via le sélecteur de couleur | N'importe quelle couleur avec alpha |
| **Intérieur** | Basculer pour afficher l'ombre à l'intérieur de l'élément au lieu de l'extérieur (ombre de boîte uniquement) | Activé / Désactivé |

Ajustez les valeurs à l'aide des curseurs ou saisissez directement des nombres précis dans les champs d'entrée.

## Ombres multiples

Vous pouvez empiler plusieurs couches d'ombres sur un seul élément pour créer des effets de profondeur complexes et réalistes :

- Cliquez sur le bouton **+** pour ajouter une nouvelle couche d'ombre
- Chaque couche apparaît comme une ligne dans la liste des ombres avec ses propres contrôles
- Glissez les couches pour les réordonner — les ombres s'affichent dans l'ordre de la liste, avec la première couche en haut
- Activez ou désactivez l'**icône de l'œil** sur n'importe quelle couche pour cacher temporairement cette couche sans supprimer la configuration
- Cliquez sur l'**icône de la poubelle** pour supprimer une couche

Combiner une ombre étroite et sombre avec une ombre large et douce crée un effet naturel de « levage » qui imite la profondeur physique.

## Ombres prédéfinies

Les préférences prédéfinies permettent d'appliquer rapidement des styles d'ombres courants avec un seul clic :

| Préférence | Description |
|--------|-------------|
| **Petite** | Ombre subtile et proche pour une légère élévation (cartes, champs d'entrée) |
| **Moyenne** | Profondeur modérée pour les éléments interactifs (boutons, menus déroulants) |
| **Grande** | Ombre prominente pour les éléments flottants (modaux, popovers) |
| **Douce** | Grande diffusion avec une faible opacité pour un effet de lumière douce et diffusée |
| **Dure** | Faible diffusion avec une opacité élevée pour un bord net et défini |
| **Intérieur** | Ombre intérieure pour un aspect appuyé ou enfoncé |

Après avoir appliqué une préférence, vous pouvez ajuster les propriétés individuelles pour affiner le résultat.

## Aperçu actuel vs. nouveau

En bas de l'éditeur, deux boîtes de comparaison affichent l'**ombre actuelle** (enregistrée) et l'**ombre nouvelle** (vos modifications en attente). Cette vue côte à côte facilite l'évaluation des différences avant de valider. Cliquez sur **Appliquer** pour accepter, ou cliquez ailleurs pour rejeter vos modifications.

## Où l'utiliser

L'éditeur d'ombres est disponible dans les emplacements suivants :

- **Construire une page** — Onglet **Style**, groupe **Effets** sur les sections, conteneurs, colonnes et éléments individuels
- **Construire l'en-tête/pied de page** — Paramètres d'ombre au niveau des widgets pour des éléments tels que les logos, les barres de recherche et les éléments de navigation

Tout élément qui prend en charge le groupe de style **Effets** affichera les contrôles de l'éditeur d'ombres.

## Conseils

- Utilisez des ombres subtilles (préférences **Petite** ou **Douce**) pour la plupart des éléments — des ombres lourdes peuvent rendre une conception encombrée.
- Combinez une ombre proche et sombre avec une ombre lointaine et claire pour obtenir l'effet d'élévation le plus naturel.
- Les ombres intérieures fonctionnent bien sur les champs d'entrée et les conteneurs pour créer un effet de panneau enfoncé.
- Les ombres de texte devraient être minimales — un décalage de 1px avec un léger flou améliore la lisibilité sur les arrière-plans d'images sans paraître daté.
- Testez vos ombres sur des arrière-plans clairs et sombres si votre thème prend en charge un basculement en mode sombre.
