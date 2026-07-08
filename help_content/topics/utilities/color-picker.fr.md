---
title: Sélecteur de couleur
---

Le sélecteur de couleur avancé vous permet de choisir des couleurs en utilisant plusieurs méthodes d'entrée et des préférences prédéfinies sensibles aux thèmes. Il apparaît partout où une propriété de couleur est utilisée sur la plateforme — dans le constructeur de pages, le constructeur d'en-tête/pied de page, le constructeur de menu et l'administration du catalogue. Cliquez sur n'importe quelle miniature de couleur ou champ d'entrée de couleur pour ouvrir le sélecteur.

![Sélecteur de couleur](/static/core/admin/img/help/color-picker/color-picker.webp)

## Méthodes d'entrée de couleur

Le sélecteur prend en charge plusieurs façons de définir une couleur:

| Méthode | Description | Exemple |
|--------|-------------|---------|
| **Hex** | Entrez directement un code hexadécimal à 6 chiffres | `#FF5733` |
| **RGB** | Ajustez les curseurs Rouge, Vert et Bleu (0-255 chacun) | `rgb(255, 87, 51)` |
| **HSL** | Définissez le Ton (0-360), la Saturation (0-100%) et la Luminosité (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB avec un canal de transparence alpha | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL avec un canal de transparence alpha | `hsla(14, 100%, 60%, 0.8)` |
| **Spectre visuel** | Cliquez ou faites glisser sur la zone du spectre de couleur pour choisir visuellement | Sélection par pointeur et clic |

Vous pouvez également taper une valeur directement dans le champ de texte en bas du sélecteur.

## Sélecteur de format

Un menu déroulant en haut du sélecteur vous permet de basculer entre les modes de sortie **HEX**, **RGB**, **RGBA**, **HSL** et **HSLA**. Lorsque vous basculez de formats, la couleur actuelle est automatiquement convertie — aucune valeur n'est perdue. Choisissez le format qui convient le mieux à votre flux de travail ou aux exigences de votre système de conception.

## Préférences de couleur

En dessous de la zone du spectre, une rangée de miniatures de couleur à accès rapide permet une sélection en un clic pour les couleurs courantes. Ces miniatures sont **sensibles aux thèmes** : elles reflètent automatiquement les couleurs primaires, secondaires, d'accent et neutres du thème actif. Cela facilite le maintien d'une cohérence avec votre marque sans avoir à mémoriser les codes hexadécimaux.

Pour appliquer une préférence, cliquez sur la miniature. Le sélecteur met à jour immédiatement pour afficher la couleur sélectionnée dans le spectre et les champs d'entrée.

## Opacité / Alpha

Lorsque vous utilisez le mode RGBA ou HSLA, un curseur horizontal **alpha** apparaît en dessous du spectre. Glissez-le pour définir la transparence de 0 % (entièrement transparent) à 100 % (entièrement opaque). La valeur d'opacité est également modifiable via un champ numérique à côté du curseur pour un contrôle précis.

Les couleurs semi-transparentes sont utiles pour les surcouches, les effets de survol et les éléments de conception en couches.

## Couleur actuelle vs nouvelle prévisualisation

En bas du sélecteur, deux boîtes côte à côte affichent la **couleur actuelle** appliquée et la **nouvelle** couleur sélectionnée. Cette comparaison vous permet d'évaluer le changement avant de l'appliquer. Cliquez sur **Appliquer** pour accepter la nouvelle couleur, ou cliquez en dehors du sélecteur pour annuler et conserver la valeur actuelle.

## Où il apparaît

Le sélecteur de couleur est un outil partagé utilisé dans tout l'administration:

- **Constructeur de pages** — Couleur du texte, arrière-plan, bordure et états de survol dans l'onglet Style
- **Constructeur d'en-tête/pied de page** — Couleurs du texte, arrière-plan, icône et liens des widgets
- **Constructeur de menu** — Couleurs des liens des éléments de menu et états de survol/actif
- **Administration du catalogue** — Couleurs des badges de produit et des couleurs d'accentuation des catégories

Tout champ qui accepte une valeur de couleur ouvre le même sélecteur, ce qui garantit une expérience cohérente partout.

## Conseils

- Utilisez les miniatures de préférences de votre thème pour maintenir la cohérence de la marque sur toutes les pages et composants.
- Basculer en mode HSL lorsque vous avez besoin de créer des variantes plus claires ou plus sombres de la même teinte — ajustez simplement la valeur de luminosité.
- Copiez le code hexadécimal à partir du champ de texte pour réutiliser exactement la même couleur dans un autre champ ou la partager avec un designer.
- Utilisez RGBA avec une opacité réduite pour des effets de surcouche subtils sur les images et les sections héros.
- Le sélecteur se souvient des couleurs récemment utilisées pendant votre session, donc les couleurs personnalisées utilisées fréquemment restent accessibles.
- Si vous collez une valeur de couleur dans n'importe quel format pris en charge dans le champ hexadécimal, le sélecteur la reconnaîtra et la convertira automatiquement.