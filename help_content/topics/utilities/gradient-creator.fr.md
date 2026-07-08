---
title: Créateur de dégradés
---

Le Créateur de dégradés vous permet de créer des transitions de couleurs fluides pour les arrière-plans d'éléments. Il est accessible via l'onglet Dégradé de l'éditeur d'arrière-plan et s'ouvre sous forme de panneau flottant avec une barre de dégradé visuelle, des contrôles de points de couleur et des options prédéfinies.

![Créateur de dégradés](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Accéder au Créateur de dégradés

1. Sélectionnez un élément dans le Page Builder ou l'éditeur d'entête/pied de page
2. Ouvrez l'onglet **Style** dans le panneau des propriétés
3. Cliquez sur la section **Arrière-plan** pour ouvrir l'éditeur d'arrière-plan
4. Basculer vers l'onglet **Dégradé**
5. Le panneau du Créateur de dégradés s'ouvre avec un aperçu en temps réel et des contrôles d'édition

## Aperçu en temps réel

En haut du panneau, une comparaison côte à côte est affichée :

| Boîte | Objectif |
|-------|---------|
| **Actuel** | Le dégradé existant (ou transparent s'il n'en est aucun) |
| **Nouveau** | Mises à jour en temps réel à mesure que vous apportez des modifications |

Une flèche entre les deux boîtes indique la direction des changements.

## Types de dégradés

Trois types de dégradés sont disponibles, sélectionnables via des onglets en haut de l'éditeur :

| Type | Description | Contrôles |
|------|-------------|----------|
| **Linéaire** | Transitions de couleur le long d'une ligne droite | Curseur d'angle (0-360 degrés) avec des boutons de direction prédéfinie (haut, diagonal, droite, bas, etc.) |
| **Radial** | Transitions de couleur rayonnant depuis un point central | Sélecteur de forme (cercle ou ellipse) et sélectionneur de position (centré, haut, bas, coins) |
| **Conique** | Transitions de couleur tournant autour d'un point central | Curseur d'angle de départ (0-360 degrés) et sélectionneur de position |

### Contrôles de direction linéaire

Pour les dégradés linéaires, vous pouvez définir l'angle de trois façons :
- **Curseur d'angle** — glissez de 0 à 360 degrés
- **Champ de saisie d'angle** — tapez une valeur précise en degrés
- **Boutons prédéfinis** — cliquez sur les icônes de flèche pour les directions courantes (vers le haut, vers le haut à droite, vers la droite, vers le bas à droite, vers le bas, vers le bas à gauche, vers la gauche, vers le haut à gauche)

## Points de couleur

La barre de dégradé affiche vos points de couleur actuels sous forme de marqueurs déplaçables. Chaque point définit une couleur à une position spécifique le long du dégradé.

**Ajouter des points** — Cliquez sur le bouton **+** dans la section Points de couleur pour ajouter un nouveau point. Il n'y a pas de limite stricte au nombre de points.

**Modifier des points** — Chaque point de la liste affiche :
- Une miniature de couleur qui ouvre le Sélecteur de couleur lorsqu'on clique dessus
- Une valeur de position (0 % à 100 %) que vous pouvez taper ou ajuster
- Un contrôle d'opacité (0 à 1)
- Un bouton Supprimer pour supprimer le point

**Réordonner** — Glissez les points le long de la barre de dégradé pour les réorganiser visuellement.

## Prédéfinis de dégradés

Six prédéfinis sont disponibles pour un point de départ rapide. Cliquez sur n'importe quel prédéfini pour l'appliquer immédiatement :

| Prédéfini | Couleurs | Angle |
|-----------|--------|-------|
| **Océan** | Bleu clair à bleu | 120 degrés |
| **Coucher de soleil** | Orange chaud à rose corail (3 points) | 45 degrés |
| **Forêt** | Indigo à vert émeraude | 135 degrés |
| **Baies** | Rose à bleu-violet | 90 degrés |
| **Flamme** | Rouge à jaune doré | 45 degrés |
| **Nuit** | Gris foncé à bleu océan | 180 degrés |

Les prédéfinis sont des points de départ. Après avoir appliqué l'un d'eux, vous pouvez modifier les couleurs, ajouter ou supprimer des points et changer l'angle pour créer votre propre variation.

## Actions du pied de page

| Bouton | Action |
|--------|--------|
| **Effacer** | Supprime complètement le dégradé, revenant à transparent |
| **Appliquer** | Enregistre le dégradé et ferme l'éditeur |

Fermer l'éditeur sans cliquer sur Appliquer supprime vos modifications.

## Où s'applique-t-il

Le Créateur de dégradés est utilisé dans :

- **Page Builder** — via l'onglet Dégradé de l'éditeur d'arrière-plan sur n'importe quel élément
- **Header/Footer Builder** — pour les arrière-plans de dégradé sur les sections d'entête, les barres de navigation et les zones de pied de page

Il fonctionne en conjonction avec l'éditeur d'arrière-plan, qui propose également des options d'arrière-plan en couleur solide, en image et en vidéo.

## Conseils

- **Commencez par un prédéfini** — appliquez un prédéfini proche de ce que vous souhaitez, puis ajustez les couleurs et l'angle plutôt que de tout construire à partir de zéro.
- **Utilisez deux ou trois points** — les dégradés simples avec deux points ont l'air propres et professionnels. Plus de points sont utiles pour des effets complexes, mais peuvent rapidement devenir écrasants.
- **Utilisez les couleurs de votre marque** — utilisez le Sélecteur de couleur pour entrer les valeurs hexadécimales exactes de votre palette de couleurs de marque pour des dégradés cohérents et conformes à votre marque.
- **Testez avec du contenu** — les dégradés qui semblent spectaculaires seuls peuvent réduire la lisibilité du texte. Vérifiez toujours que le texte sur les arrière-plans de dégradé a un contraste suffisant.
- **Essayez radial pour les effets de spot** — les dégradés radiaux conviennent bien pour attirer l'attention sur une zone centrale, telle qu'un point focal de section héro.