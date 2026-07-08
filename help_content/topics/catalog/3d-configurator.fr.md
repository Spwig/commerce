---
title: Configureur de produits 3D
---

Le Configureur 3D permet à vos clients d'apercevoir les produits configurables via un visionneur 3D interactif directement sur la page du produit. Lorsque les clients sélectionnent des options — telles que les couleurs, les matériaux ou les variations de composants — le modèle 3D se met à jour en temps réel pour refléter leurs choix. Sur les appareils mobiles pris en charge, les clients peuvent également visualiser le produit en réalité augmentée (AR), le plaçant virtuellement dans leur propre espace avant l'achat.

Le Configureur 3D fonctionne avec les produits configurables. Chaque produit configurable peut avoir une seule configuration de scène 3D qui relie un fichier de modèle GLB au choix de configuration du produit.

## Avant de commencer

Pour configurer une scène 3D, vous avez besoin de :

- Un **produit configurable** déjà créé dans votre catalogue
- Un **modèle 3D de base** téléchargé dans votre Bibliothèque multimédia sous forme de fichier GLB — c'est le modèle assemblé qui s'affiche par défaut
- En option, d'autres fichiers GLB pour les échanges de géométrie (par exemple, différentes formes de colliers), et des images de texture pour les variations de matériaux

Si vous n'avez pas encore créé le produit configurable et ses options de configuration, faites-le d'abord avant de configurer la scène 3D.

## Création d'une configuration de scène

1. Accédez à **Catalogue > Configurations de scènes 3D**
2. Cliquez sur **+ Ajouter une configuration de scène 3D**
3. Sélectionnez le **Produit** auquel appartient cette scène — seuls les produits configurables sont disponibles
4. Choisissez le **Modèle 3D de base** depuis votre Bibliothèque multimédia — c'est le fichier GLB qui s'affiche par défaut
5. Configurez les paramètres du visionneur (voir ci-dessous)
6. Enregistrez l'enregistrement

Après l'enregistrement, le champ **Arborescence des nœuds** se remplit automatiquement. Il s'agit du graphe de scène analysé extrait de votre fichier GLB — il liste chaque nœud nommé à l'intérieur du modèle, que vous allez référencer lors de l'ajout des correspondances de nœuds.

## Paramètres du visionneur

Ces paramètres contrôlent l'apparence du visionneur 3D sur votre page produit.

### Caméra et éclairage

| Champ | Description | Défaut |
|-------|-------------|---------|
| **Position de la caméra** | Position de départ de la caméra au format `angle élévation distance` (par exemple, `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Cible de la caméra** | Le point vers lequel la caméra regarde, en mètres à partir du centre du modèle (par exemple, `0m 0m 0m`) | `0m 0m 0m` |
| **Image d'environnement** | Une image HDR de votre Bibliothèque multimédia utilisée pour l'éclairage basé sur l'image — donne des réflexions et des ombres plus réalistes | Aucune |
| **Exposition** | Luminosité globale de la scène — des valeurs plus basses sont plus sombres, des valeurs plus élevées sont plus lumineuses | `1.0` |

### Ombres

| Champ | Description | Défaut |
|-------|-------------|---------|
| **Intensité de l'ombre** | Intensité de l'ombre projetée sous le modèle — `0` signifie pas d'ombre, `1` signifie intensité maximale | `0.5` |
| **Douceur de l'ombre** | Niveau de flou des bords de l'ombre — `0` signifie net, `1` signifie très doux | `0.5` |

### Grading des couleurs

| Champ | Description |
|-------|-------------|
| **Carte de tons** | Algorithme de grading des couleurs appliqué à la scène. **Commerce** produit des couleurs vives et adaptées aux produits. **Neutre** est précis en couleur. **ACES** donne un look de film cinématographique. |
| **Intensité du flou lumineux** | Ajoute un effet de lueur aux parties émissives (auto-éclairées) du modèle. `0` désactive le flou. Les valeurs entre `1` et `5` produisent un flou subtil à dramatique. |

### Comportement et arrière-plan

| Champ | Description | Défaut |
|-------|-------------|---------|
| **Rotation automatique** | Détermine si le modèle tourne lentement à l'ouverture pour attirer l'attention du client | Activé |
| **AR activé** | Détermine si les clients sur les appareils pris en charge voient un bouton **Voir en réalité augmentée** | Activé |
| **Arrière-plan** | Couleur ou dégradé CSS du fond du visionneur — entrez une couleur hexadécimale (par exemple, `#f5f5f5`) ou une valeur de dégradé CSS | `#ffffff` |

### Miniature

Le champ **Miniature** contient une capture d'écran prévue du visionneur 3D, affichée avant le chargement du visionneur. Vous pouvez capturer une capture d'écran depuis la page du produit en direct et la télécharger dans votre Bibliothèque multimédia, puis la lier ici pour une expérience de chargement de page plus fluide.

Lorsqu'elle est désactivée, le produit revient à la configuration d'image 2D standard.

Cela vous permet de préparer une configuration de scène avant de la rendre visible aux clients.

## Connexion des options de configuration aux actions 3D

Une fois que la scène de base est configurée, vous pouvez lier chaque option de configuration à un changement visuel dans le modèle 3D. Ces liens sont appelés **Node Mappings** et sont ajoutés dans la section **Node Mappings** en bas du formulaire de configuration de la scène.

### Champs de mappage de nœud

| Champ | Description |
|-------|-------------|
| **Option de fente** | L'option de configuration qui déclenche ce changement (ex. : "Cuir rouge") |
| **Type d'action** | Ce qui change visuellement (voir les types d'action ci-dessous) |
| **Nœud cible** | Le nom du nœud du graphe de scène qui change — choisissez parmi les noms listés dans votre **Arbre des nœuds** |
| **Données d'action** | Données spécifiques à l'action telles qu'un code couleur hexadécimal, une URL de texture ou une URL de fichier GLB |
| **Ordre de tri** | Contrôle l'ordre dans lequel plusieurs mappages pour la même option sont appliqués |

### Types d'action

| Action | Ce qu'elle fait |
|--------|-------------|
| **Couleur de matériau** | Change la couleur d'un matériau sur le nœud cible — fournissez un code couleur hexadécimal dans **Données d'action** |
| **Texture de matériau** | Remplace la texture appliquée à un matériau — liez à une image de texture dans **Données d'action** |
| **Échange de géométrie** | Remplace une partie du modèle par un fichier GLB différent — utile pour des changements structurels comme une forme de poignée différente |
| **Visibilité** | Affiche ou masque un nœud dans la scène — définissez `visible: true` ou `visible: false` dans **Données d'action** |

Plusieurs mappages peuvent être ajoutés pour une seule option de fente. Par exemple, la sélection de "Jean bleu" pourrait changer la couleur du matériau *et* masquer un nœud de garniture en cuir en même temps.

## Actifs de géométrie

Si votre configuration inclut des actions **Échange de géométrie**, vous devez enregistrer les fichiers GLB de remplacement comme des actifs de géométrie. Ils sont ajoutés dans la section **Actifs de géométrie** du formulaire de configuration de la scène.

| Champ | Description |
|-------|-------------|
| **Étiquette** | Nom descriptif pour cet actif de géométrie, par exemple, "Col en V" |
| **Fichier GLB** | Le fichier GLB de remplacement depuis votre bibliothèque multimédia |
| **Nœud cible** | Le nœud du modèle de base que ce géométrie remplace |

Après avoir enregistré un actif de géométrie, les noms de nœuds sont extraits du GLB et stockés dans **Données de nœud**, les rendant disponibles comme nœuds cibles dans vos mappages.

## Actifs de texture

Les images de texture utilisées dans les mappages **Texture de matériau** peuvent être enregistrées comme actifs de texture pour une référence plus facile. Ils sont ajoutés dans la section **Actifs de texture**.

| Champ | Description |
|-------|-------------|
| **Étiquette** | Nom descriptif, par exemple, "Cuir rouge" |
| **Image de texture** | L'image de texture depuis votre bibliothèque multimédia |
| **Type de texture** | Le canal PBR auquel cette texture s'applique — Couleur de base, Carte normale, Carte de rugosité, Carte de métallisation, Occlusion ambiante ou Carte émissive |

## Exemple : manteau configurable avec des options de couleur

**Scénario :** Un manteau pouvant être commandé en noir, bleu marine ou bordeaux, avec chaque couleur appliquée au maillage du corps du manteau.

**Configuration :**

1. Créez une configuration de scène pour le produit manteau avec le fichier GLB du manteau assemblé comme modèle de base
2. Définissez **Tone Mapping** sur Commerce et **Auto Rotate** sur on
3. Dans les **Node Mappings**, ajoutez trois entrées — une par option de couleur :

| Option de fente | Type d'action | Nœud cible | Données d'action |
|----------------|--------------|------------|----------------|
| Noir | Couleur de matériau | JacketBody | `{"color": "#1a1a1a"}` |
| Bleu marine | Couleur de matériau | JacketBody | `{"color": "#1b2a4a"}` |
| Bordeaux | Couleur de matériau | JacketBody | `{"color": "#6b2737"}` |

Lorsqu'un client sélectionne le bleu marine sur la page du produit, le visualiseur met immédiatement à jour le matériau JacketBody en couleur bleu marine.

## Conseils

Conservez tous les formats de mise en forme markdown, les chemins d'image, les blocs de code et les termes techniques.

- Donnez des noms clairs à vos nœuds GLB lors de la création de votre modèle 3D — des noms de nœuds comme "JacketBody" ou "CollarMesh" sont beaucoup plus faciles à utiliser que des noms générés automatiquement comme "Mesh_023"
- Utilisez la **Carte de tons Commerce** pour la plupart des produits — elle est optimisée pour une présentation de produit vibrante et attrayante
- Désactivez **Auto Rotate** pour les produits dont l'angle de caméra par défaut montre déjà les caractéristiques les plus importantes, afin d'éviter de désorienter le client à l'ouverture
- Testez le bouton AR sur un appareil mobile réel avant de le promouvoir — la disponibilité de l'AR dépend de l'appareil et du navigateur du client (iOS Safari et Android Chrome avec le support WebXR sont les plus fiables)
- Téléchargez une image **Miniature** pour chaque configuration de scène — cela évite qu'une boîte blanche vide ne s'affiche pendant que le visionneur 3D se charge
- Si le visionneur 3D n'est pas encore prêt, désactivez-le avec le curseur **Activé** afin que les clients voient l'outil de configuration d'image standard à la place