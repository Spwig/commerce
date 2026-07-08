---
title: Éditeur de typographie
---

L'Éditeur de typographie est un utilitaire de style partagé qui vous donne un contrôle complet sur l'apparence du texte. Il s'ouvre en tant que panneau flottant chaque fois que vous modifiez les propriétés de typographie sur tout élément dans le Page Builder, Header/Footer Builder ou Menu Builder.

![Éditeur de typographie](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Aperçu en direct

L'éditeur affiche une comparaison côte à côte en haut du panneau :

| Boîte | Objectif |
|-----|---------|
| **Actuelle** | Affiche "The quick brown fox..." avec le style de typographie existant |
| **Nouvelle** | Met à jour en temps réel lorsque vous ajustez les paramètres, affichant le résultat avant l'application |

Cela vous permet de comparer avant et après sans appliquer de changements.

## Onglet Police

L'onglet Police est la vue par défaut lorsque l'éditeur s'ouvre.

**Famille de police** — Un menu déroulant rechercheable avec plus de 70 polices organisées par catégorie. Chaque police est prévisualisée dans sa propre police afin que vous puissiez voir à quoi elle ressemble avant de la sélectionner. Les polices sont chargées sur demande depuis Google Fonts lorsqu'elles sont nécessaires.

**Taille de police** — Champ numérique avec un sélecteur d'unité prenant en charge px, em, rem et %. La valeur par défaut est 16px.

**Poids de police** — Un curseur allant de 100 (Fin) à 900 (Noir) :

| Valeur | Nom |
|-------|------|
| 100 | Fin |
| 200 | Très léger |
| 300 | Léger |
| 400 | Normal |
| 500 | Moyen |
| 600 | Semi-gras |
| 700 | Gras |
| 800 | Très gras |
| 900 | Noir |

Toutes les polices ne prennent pas en charge les neuf poids. L'éditeur affiche les poids disponibles pour la famille de police sélectionnée.

**Style de police** — Boutons basculants pour Normal, Italic et Oblique.

## Onglet Espacement

Affiner l'espace autour et entre les caractères :

| Contrôle | Ce que cela fait | Défaut |
|---------|-------------|---------|
| **Hauteur de ligne** | Espace vertical entre les lignes de texte | normal |
| **Espacement des lettres** | Espace horizontal entre les caractères individuels | normal |
| **Espacement des mots** | Espace horizontal entre les mots | normal |
| **Indentation du texte** | Indentation de la première ligne d'un paragraphe | 0 |

Chaque contrôle d'espacement inclut un sélecteur d'unité (px, em, rem, %).

## Onglet Style

Contrôler la décoration du texte et les effets visuels :

- **Décoration du texte** — Aucun, Souligné, Sur ligne ou Ligne barrée
- **Style de décoration** — Solide, Pointillé, Pointé, Double ou Ondulé (s'applique lorsque la décoration est active)
- **Couleur de décoration** — Sélecteur de couleur pour la ligne de décoration, par défaut la couleur du texte
- **Ombre du texte** — Effet d'ombre optionnel avec des contrôles de décalage, flou et couleur

## Onglet Transformation

Modifier la mise en majuscule du texte sans modifier le contenu :

| Option | Résultat |
|--------|--------|
| **Aucun** | Le texte apparaît tel quel |
| **Majuscules** | TOUS LES CARACTÈRES SONT MAJUSCULES |
| **Minuscules** | tous les caractères sont en minuscules |
| **Majuscule initiale** | La première lettre de chaque mot est en majuscule |

D'autres contrôles sur cet onglet incluent **Alignement du texte** (gauche, centre, droite, justifié), **Alignement vertical** et **Direction du texte** (LTR ou RTL).

## Familles de police disponibles

L'éditeur inclut une bibliothèque soigneusement sélectionnée de polices système et Google Fonts, groupées par catégorie :

| Catégorie | Polices
|----------|-------|
| **Système** | Police par défaut du système, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **Sans-Serif (Moderne)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **Sans-Serif (Classique)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **Serif (Système)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **Affichage** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

Les polices de Google Fonts sont chargées automatiquement lorsqu'elles sont sélectionnées. Les polices du système utilisent des chaînes de secours CSS appropriées pour un rendu fiable sur tous les plateformes.

## Où elle apparaît

L'éditeur de typographie est disponible là où le stylisme du texte est nécessaire :

- **Page Builder** — Sélectionnez tout élément, ouvrez l'onglet Style, puis cliquez sur la section Typographie
- **Builder d'en-tête/pied de page** — Mettez en forme le texte dans les liens de navigation, le texte du logo, les éléments de menu et le contenu du pied de page
- **Builder de menu** — Contrôlez la typographie des étiquettes de menu et des éléments de sous-menu
- **Catalogue Admin** — Utilisé dans la description des produits et les éditeurs de contenu où les contrôles de typographie sont exposés

L'éditeur est toujours accessible via la même interface cohérente, indépendamment du contexte.

## Conseils

- **Associez les polices de manière intentionnelle** — utilisez une police d'affichage ou serif pour les titres et une police sans-serif propre pour le texte principal. Des combinaisons classiques comme Playfair Display + Inter ou Montserrat + Merriweather fonctionnent bien.
- **Limitez le nombre de familles de polices par page** — deux ou trois familles de polices par page sont généralement suffisantes. Plus que cela peut ralentir le temps de chargement et créer un désordre visuel.
- **Utilisez des unités relatives pour un texte réactif** — les unités em et rem s'adaptent à la taille de police de base, permettant à votre typographie de s'adapter automatiquement aux différentes tailles d'écran.
- **Vérifiez la disponibilité des poids** — si le texte semble identique à 400 et 500, la police sélectionnée ne prend peut-être pas en charge ce poids. L'éditeur indique quels poids chaque police propose.
- **Prévisualisez sur tous les appareils** — le texte qui semble bon aux tailles d'écran de bureau peut être trop petit ou trop grand sur les appareils mobiles. Utilisez la prévisualisation d'appareil du Page Builder pour vérifier.
- **Utilisez la prévisualisation en temps réel** — comparez toujours Current vs New dans les boîtes de prévisualisation avant d'appliquer pour éviter les changements inattendus.