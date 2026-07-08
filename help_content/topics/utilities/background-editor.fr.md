---
title: Éditeur d'arrière-plan
---

L'éditeur d'arrière-plan vous donne un contrôle complet sur les arrière-plans des éléments avec quatre types : couleur solide, dégradé, image et vidéo. Il prend également en charge des états Normal et Hover distincts afin que vous puissiez créer des effets visuels interactifs. Ouvrez l'onglet **Style** d'un élément et cherchez la section **Arrière-plan** pour accéder à l'éditeur.

![Éditeur d'arrière-plan](/static/core/admin/img/help/background-editor/background-editor.webp)

## États Normal et Hover

En haut de l'éditeur d'arrière-plan, un interrupteur bascule entre les états **Normal** et **Hover**. Chaque état a sa propre configuration d'arrière-plan indépendante :

- **Normal** — L'arrière-plan par défaut affiché lorsque la page se charge
- **Hover** — L'arrière-plan appliqué lorsque les visiteurs déplacent leur curseur sur l'élément

Deux petits blocs de prévisualisation à côté de l'interrupteur montrent les arrière-plans Normal et Hover côte à côte, afin que vous puissiez voir le contraste d'un coup d'œil. Configurez d'abord l'état Normal, puis basculez vers Hover pour ajouter un effet interactif si souhaité.

## Types d'arrière-plan

Sélectionnez un type d'arrière-plan à partir de la rangée d'icônes en haut du panneau d'édition :

| Type | Description |
|------|-------------|
| **Couleur** | Un remplissage solide à l'aide d'une seule valeur de couleur. Rapide à appliquer et léger. |
| **Dégradé** | Un mélange fluide entre deux ou plusieurs couleurs, soit linéaire, soit radial. Comprend des préconfigurations intégrées comme Ocean, Sunset, Forest et Berry. Pour un édition de dégradé avancée, consultez le sujet [Créateur de dégradé](gradient-creator). |
| **Image** | Une image téléchargée ou une image sélectionnée depuis la bibliothèque multimédia. Prend en charge le positionnement, le redimensionnement et le contrôle de répétition. |
| **Vidéo** | Une URL de vidéo d'arrière-plan avec une image de mise en page facultative qui s'affiche pendant le chargement de la vidéo ou sur les appareils mobiles. |

Un seul type peut être actif à la fois par état. Passer d'un type à un autre ne supprime pas votre configuration précédente — vous pouvez revenir en arrière et vos paramètres seront conservés.

## Arrière-plans de couleur

Lorsque **Couleur** est sélectionné :

- **Entrée Hex** — Tapez directement un code hexadécimal (par exemple, `#1A1A2E`)
- **Échantillons de couleur** — Cliquez sur un échantillon prédéfini pour une sélection rapide. Les échantillons sont sensibles aux thèmes et reflètent la palette du thème actif.
- **Bouton Éditer** — Ouvre le sélecteur de couleur complet avec un spectre, des curseurs et des options de format (voir le sujet [Sélecteur de couleur](color-picker))

Les arrière-plans de couleur s'affichent instantanément et n'ont aucun impact sur les performances, ce qui les rend idéaux pour les sections, les cartes et les conteneurs.

## Arrière-plans dégradés

Lorsque **Dégradé** est sélectionné :

- **Dégradés prédéfinis** — Choisissez parmi les dégradés intégrés : Ocean, Sunset, Forest, Berry et d'autres
- **Dégradé personnalisé** — Cliquez sur **Éditer** pour ouvrir le créateur de dégradé où vous pouvez définir la direction, le type (linéaire ou radial) et les points de couleur
- **Curseur d'angle** — Ajustez la direction du dégradé pour les dégradés linéaires (0-360 degrés)

Les dégradés ajoutent une profondeur visuelle sans nécessiter d'actifs d'images et s'adaptent parfaitement à toute taille d'écran.

## Arrière-plans d'image

Lorsque **Image** est sélectionné :

- **Télécharger ou Bibliothèque multimédia** — Cliquez sur le placeholder d'image pour télécharger une nouvelle image ou sélectionner une image depuis votre bibliothèque multimédia
- **Taille** — Choisissez **Couvrir** (remplit l'élément, peut couper), **Contenir** (s'adapte à l'intérieur de l'élément) ou une taille personnalisée
- **Position** — Définissez le point focal à l'aide d'une grille de 9 points (en haut à gauche, centre, en bas à droite, etc.) ou entrez des pourcentages personnalisés X/Y
- **Répétition** — Activez ou désactivez la répétition. Utile pour les motifs de carrelage
- **Superposition** — Ajoutez une superposition de couleur sur l'image avec une opacité ajustable, utile pour garantir la lisibilité du texte

Optimisez toujours les images avant de les télécharger. Les images non compressées de grande taille ralentissent le temps de chargement des pages.

## Arrière-plans de vidéo

Lorsque **Vidéo** est sélectionné :

- **URL de la vidéo** — Entrez une URL directe vers un fichier vidéo MP4 ou WebM
- **Image de mise en page** — Téléchargez une image de secours affichée pendant le chargement de la vidéo et sur les appareils qui ne reproduisent pas automatiquement la vidéo
- **Lecture automatique / Boucle / Muet** — Les arrière-plans vidéo se jouent automatiquement, en boucle et sont muets par défaut pour se conformer aux politiques des navigateurs

Gardez les vidéos d'arrière-plan courtes (10 à 30 secondes), compressées et visuellement subtilles. Elles devraient renforcer la section sans distraire du contenu.

## Où s'affiche-t-il

L'éditeur d'arrière-plan est disponible pour chaque élément qui prend en charge les arrière-plans :

- **Construire une page** — Les sections, les conteneurs, les colonnes et les éléments individuels ont tous une section Arrière-plan dans l'onglet Style
- **Construire l'en-tête/pied de page** — Les arrière-plans de ligne et les arrière-plans des widgets individuels
- **Construire le menu** — Les arrière-plans du conteneur de menu et des panneaux déroulants

Le même interface d'édition est utilisée partout, donc votre workflow reste cohérent à travers les constructeurs.

## Conseils

- Utilisez une superposition de couleur semi-transparente sur les arrière-plans d'images pour garantir la lisibilité du texte indépendamment du contenu de l'image.
- Les dégradés prédéfinis sont une méthode rapide pour ajouter de l'intérêt visuel — appliquez-en un, puis personnalisez l'angle ou les couleurs pour correspondre à votre marque.
- Définissez à la fois les arrière-plans Normal et Hover sur les cartes interactives pour donner aux visiteurs un retour visuel clair lorsqu'ils explorent votre contenu.
- Pour les arrière-plans d'images, définissez toujours un point focal afin que la partie la plus importante de l'image reste visible sur toutes les tailles d'écran.
- Privilégiez les arrière-plans de couleur ou de dégradé par rapport aux images pour les sections où la vitesse de chargement est critique, comme le contenu au-dessus de la pliure.
- Testez les arrière-plans vidéo sur les appareils mobiles — la plupart des navigateurs mobiles afficheront l'image de mise en page au lieu de jouer la vidéo.