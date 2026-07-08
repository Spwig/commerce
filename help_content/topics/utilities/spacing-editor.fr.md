---
title: Éditeur d'espacement
---

L'éditeur d'espacement visuel vous permet de configurer les marges et les rembourrages à l'aide d'un diagramme de modèle de boîte intuitif. Un contrôle précis des espacements garantit des dispositions cohérentes et des expériences de lecture confortables à travers votre boutique en ligne. Ouvrez l'onglet **Style** de tout élément et cherchez la section **Espacement** pour accéder à l'éditeur.

![Éditeur d'espacement](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Le diagramme du modèle de boîte

L'éditeur affiche un modèle de boîte visuel avec trois couches imbriquées :

- **Marge** (anneau extérieur, généralement affiché en orange) — L'espace en dehors de la bordure de l'élément, le séparant des éléments voisins
- **Rembourrage** (anneau intérieur, généralement affiché en vert) — L'espace entre la bordure de l'élément et son contenu
- **Contenu** (zone centrale) — Le contenu réel de l'élément, tel que du texte ou une image

Chaque côté du diagramme (haut, droit, bas, gauche) dispose d'une poignée déplaçable et d'une entrée numérique. Déplacez une poignée vers l'extérieur pour augmenter la valeur, ou vers l'intérieur pour la diminuer. Vous pouvez également cliquer directement sur la valeur d'un côté pour taper un nombre précis.

## Onglets Marge et Rembourrage

Deux onglets en haut de l'éditeur basculent entre les vues **Marge** et **Rembourrage**. Lorsque Marge est sélectionnée, l'anneau extérieur est mis en surbrillance et modifiable. Lorsque Rembourrage est sélectionné, l'anneau intérieur est mis en surbrillance et modifiable. L'anneau non actif reste visible à titre de référence, mais est atténué.

Les deux onglets partagent les mêmes contrôles et options d'unités, donc le workflow est identique pour la configuration des marges et des rembourrages.

## Contrôles par côté

Chaque côté dispose d'une entrée de valeur indépendante et d'un sélecteur d'unité :

| Côté | Description |
|------|-------------|
| **Haut** | Espace au-dessus de l'élément (marge) ou au-dessus du contenu (rembourrage) |
| **Droite** | Espace à droite de l'élément ou du contenu |
| **Bas** | Espace en dessous de l'élément ou du contenu |
| **Gauche** | Espace à gauche de l'élément ou du contenu |

Cliquez sur la valeur d'un côté dans le diagramme pour la sélectionner, puis tapez un nombre ou utilisez les touches de direction haut/bas pour l'incrémenter de 1. Maintenez la touche Shift enfoncée tout en appuyant sur les touches de direction pour l'incrémenter de 10.

## Unités

Le sélecteur d'unité à côté de chaque entrée de valeur vous permet de choisir l'unité de mesure :

| Unité | Description |
|------|-------------|
| **px** | Pixels. Taille fixe, cohérente sur tous les appareils. Idéal pour des valeurs d'espacement précises et petites. |
| **em** | Relatif à la taille de police de l'élément. S'adapte aux changements de typographie. |
| **rem** | Relatif à la taille de police de base. Fournit une mise à l'échelle cohérente sur toute la page. |
| **%** | Pourcentage de la largeur de l'élément parent. Utile pour des dispositions fluides et réactives. |
| **auto** | Permet au navigateur de calculer automatiquement la valeur. Souvent utilisé pour le centrage horizontal avec les marges gauche/droite. |

Choisissez une unité qui correspond à votre intention — utilisez `px` pour des espacements fixes, `rem` pour des espacements adaptables qui respectent les tokens de typographie du thème, et `%` pour des dispositions qui doivent s'adapter à la largeur du conteneur.

## Lier les côtés

Un **icône de lien** au centre du diagramme bascule en mode lié :

- **Lien actif** (icône de chaîne connectée) — Changer la valeur d'un côté met à jour les quatre côtés avec la même valeur. Utile pour un espacement uniforme.
- **Lien inactif** (icône de chaîne brisée) — Chaque côté est contrôlé indépendamment. Utilisez cela lorsque vous avez besoin de valeurs différentes pour le haut/bas et le gauche/droite.

Cliquez sur l'icône de lien pour basculer entre les modes. Lorsque vous basculez du mode non lié au mode lié, les quatre côtés sont définis sur la valeur du côté modifié le plus récemment.

## Préférences rapides

Une rangée de boutons de préférences prédéfinies en dessous du diagramme fournit des configurations d'espacement en un clic :

| Préférence | Valeurs |
|--------|--------|
| **Aucune** | 0 sur tous les côtés |
| **Petite** | Espacement compact adapté aux dispositions serrées et aux éléments en ligne |
| **Moyenne** | Espacement équilibré pour une utilisation générale sur les cartes et les sections |
| **Grande** | Espacement généreux pour les zones héro et les sections à fort accent |
| **XL** | Espacement extra-large pour les bannières à largeur totale et les sections de niveau supérieur de la page |

Les préférences s'appliquent à l'onglet actif (Marge ou Rembourrage) et définissent les quatre côtés en même temps. Après avoir appliqué une préférence, vous pouvez ajuster les côtés individuels si nécessaire.

## Où il apparaît

L'éditeur d'espacement est disponible pour chaque élément qui prend en charge l'espacement de mise en page :

- **Construire une page** — Onglet **Style**, section **Espacement** sur les sections, conteneurs, colonnes et éléments individuels
- **Construire l'en-tête/pied de page** — Contrôles d'espacement des lignes et des widgets pour les espacements verticaux et horizontaux
- **Construire le menu** — Espacement des éléments du menu et des marges du conteneur

L'interface d'éditeur est la même dans toutes les zones, garantissant une expérience cohérente à travers les outils de construction.

## Conseils

- Utilisez des valeurs d'espacement cohérentes à travers vos pages — choisissez 2 à 3 tailles standard et restez-y pour une mise en page propre et professionnelle.
- Définissez la marge sur **auto** pour la gauche et la droite pour centrer horizontalement un élément à largeur fixe dans son parent.
- Privilégiez les unités `rem` pour l'espacement si votre thème utilise une typographie réactive, afin que l'espacement s'adapte proportionnellement à la taille du texte.
- Utilisez le mode lié pour définir rapidement un rembourrage uniforme, puis désactivez le lien et affinez les côtés individuels si le contenu nécessite un espacement asymétrique.
- Évitez un rembourrage excessif sur mobile — testez votre espacement à des largeurs de fenêtre étroites pour vous assurer que le contenu n'est pas écrasé ou trop rembourré.