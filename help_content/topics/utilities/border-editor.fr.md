---
title: Éditeur de bordure
---

L'Éditeur de bordure permet un contrôle fin des bordures des éléments, y compris le style, la couleur, la largeur par côté et le rayon de coin par coin. Il s'ouvre sous forme de panneau flottant avec un aperçu en temps réel et deux onglets pour les paramètres de base et avancés.

![Éditeur de bordure](/static/core/admin/img/help/border-editor/border-editor.webp)

## Aperçu en temps réel

Une boîte d'aperçu en haut de l'éditeur affiche vos modifications de bordure en temps réel. La boîte affiche le mot « Aperçu » à l'intérieur d'un rectangle bordé qui se met à jour instantanément à mesure que vous ajustez les valeurs de style, de couleur, de largeur et de rayon.

## Mode de base vs. mode avancé

L'éditeur est organisé en deux onglets :

| Onglet | Ce qu'il contient |
|--------|------------------|
| **De base** | Style de bordure, couleur, largeur (avec des contrôles par côté), et rayon de bordure (avec des contrôles par coin) |
| **Avancé** | Ajustement fin du rayon de coin individuel et la propriété expérimentale de forme de coin |

La plupart des travaux sur les bordures sont effectués entièrement dans l'onglet **De base**. L'onglet **Avancé** est utile lorsque vous avez besoin d'un contrôle précis sur les coins individuels ou que vous souhaitez expérimenter avec de nouvelles fonctionnalités CSS.

## Style de bordure

Un menu déroulant avec neuf options qui contrôlent l'apparence de la ligne de bordure :

| Style | Description |
|-------|-------------|
| **Aucun** | Aucune bordure (supprime toute bordure existante) |
| **Solide** | Une ligne continue unique (par défaut) |
| **Pointillée** | Une série de tirets courts |
| **Pointée** | Une série de points ronds |
| **Double** | Deux lignes solides parallèles |
| **Enfoncé** | Une bordure gravée, à effet 3D qui semble enfoncée dans la surface |
| **Soulevé** | Une bordure soulevée, à effet 3D (inverse de enfoncé) |
| **Enfoncé** | Rend l'élément apparemment embossé ou enfoncé |
| **Soulevé** | Rend l'élément apparemment soulevé ou sorti |

En définissant le style sur Aucun, la bordure est entièrement supprimée, indépendamment des paramètres de largeur ou de couleur.

## Couleur de bordure

Un champ de saisie de texte associé à un bouton de sélection de couleur. Entrez une valeur hexadécimale directement (ex. `#3b82f6`) ou cliquez sur la vignette de couleur pour ouvrir le sélecteur complet de couleur avec les modes d'entrée hexadécimal, RGB et HSL, ainsi qu'une zone visuelle de couleur. La couleur par défaut est noire (`#000000`).

## Largeur de bordure

Contrôle l'épaisseur de la bordure en pixels. L'onglet **De base** affiche quatre champs d'entrée individuels par côté :

| Côté | Champ d'entrée |
|------|----------------|
| **Haut** | Champ numérique, minimum 0 |
| **Droite** | Champ numérique, minimum 0 |
| **Bas** | Champ numérique, minimum 0 |
| **Gauche** | Champ numérique, minimum 0 |

Un **bouton basculant de liaison** (icône de chaîne) à côté de l'étiquette contrôle si les quatre côtés sont liés :

- **Lié** (par défaut) — changer toute valeur met à jour les quatre côtés en même temps
- **Déslié** — chaque côté peut avoir une largeur différente, utile pour des effets comme une bordure uniquement en bas ou des accents de bordure à gauche

## Rayon de bordure

Contrôle le rayon de chaque coin. L'onglet **De base** affiche quatre champs d'entrée par coin :

| Coin | Étiquette |
|------|-----------|
| **Haut gauche** | TL |
| **Haut droit** | TR |
| **Bas gauche** | BL |
| **Bas droit** | BR |

Un **bouton basculant de liaison** fonctionne de la même manière que la largeur de bordure :

- **Lié** (par défaut) — les quatre coins partagent la même valeur de rayon
- **Déslié** — chaque coin peut avoir un rayon différent

Valeurs de rayon courantes :

| Valeur | Effet |
|--------|--------|
| 0px | Coins carrés tranchants |
| 4-8px | Rondissement subtil, idéal pour les cartes et les boutons |
| 12-16px | Rondissement notable, un look moderne et doux |
| 50% | Cercle ou forme de pilule (selon les dimensions de l'élément) |

Le sélecteur d'unité prend en charge px, em, rem et % pour les valeurs de largeur et de rayon.

## Forme de coin (Avancé)

L'onglet **Avancé** inclut une propriété expérimentale **Forme de coin**. Cette fonctionnalité CSS contrôle si les coins arrondis utilisent la forme standard ronde ou une forme plus anguleuse « scoop ». Le support des navigateurs est limité, et l'éditeur affiche une alerte de compatibilité lorsque le navigateur actuel ne prend pas en charge cette propriété.

## Actions du pied de page

| Bouton | Action |
|--------|--------|
| **Réinitialiser** | Réinitialise toutes les valeurs à leur état lorsque l'éditeur a été ouvert |
| **Annuler** | Ferme l'éditeur sans appliquer les modifications |
| **Appliquer** | Enregistre les paramètres de bordure et ferme l'éditeur |

## Où il apparaît

L'Éditeur de bordure est disponible dans plusieurs outils de conception :

- **Page Builder** — sélectionnez tout élément, ouvrez l'onglet **Style**, puis cliquez sur la section **Bordure**
- **Builder d'en-tête/pied de page** — ajoutez des bordures aux sections d'en-tête, aux conteneurs de navigation et aux zones de pied de page
- **Builder de menu** — stylez les bordures des éléments de menu et des conteneurs de menus déroulants

L'éditeur lit les styles de bordure calculés actuels à partir de l'élément en temps réel sur le canevas, donc il s'ouvre toujours avec les valeurs existantes correctes.

## Conseils

- **Utilisez les bordures avec modération** — des bordures subtils de 1px en gris clair créent une séparation propre entre les sections sans ajouter de poids visuel.
- **Combiner rayon et ombre** — des coins arrondis associés à une ombre douce (via l'Éditeur d'ombre) produisent un effet de carte poli.
- **Essayez les bordures unilatérales** — désactivez la liaison des côtés et définissez uniquement une bordure en bas ou à gauche pour des lignes d'accent, des séparateurs de section ou des indicateurs de barre latérale.
- **Utilisez un rayon en pourcentage pour les pilules** — définissez tous les coins à 50 % sur un bouton ou un badge pour créer une forme de pilule qui s'adapte à toute taille de contenu.
- **Vérifiez l'aperçu** — la boîte d'aperçu en temps réel se met à jour immédiatement, donc expérimentez librement avant d'appliquer.
