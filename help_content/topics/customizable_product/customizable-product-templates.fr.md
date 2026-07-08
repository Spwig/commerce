---
title: Modèles de conception pour produits personnalisables
---

Les modèles de conception sont des conceptions prêtes à l'emploi que vous créez pour vos clients. Au lieu de faire face à un canevas vide, les clients peuvent parcourir votre galerie de modèles, choisir un design qui leur plaît et le personnaliser selon leurs préférences. Les modèles améliorent significativement la conversion car ils réduisent l'effort et la créativité nécessaires pour commencer.

## Pourquoi les modèles sont importants

La plupart des clients visitant une page de produit personnalisable ne sont pas des graphistes. Un canevas vide peut être intimidant. Les modèles résolvent ce problème en offrant :

- **Inspiration** — Les clients voient ce qui est possible avec votre produit
- **Vitesse** — Commencer à partir d'un modèle est plus rapide que de construire à partir de zéro
- **Qualité** — Vos modèles conçus professionnellement assurent un meilleur résultat final
- **Orientation** — Les modèles montrent aux clients où placer les éléments pour obtenir le meilleur aspect

## Créer un modèle

Les modèles sont créés depuis la page **Paramètres de l'éditeur de conception** pour chaque produit.

1. Accédez à la page **Paramètres de l'éditeur de conception** du produit
2. Basculer vers la section **Modèles** (visible dans les onglets de la page de paramètres ou en tant que section défilante)
3. Cliquez sur **+ Ajouter un modèle**
4. Remplir les détails du modèle :
   - **Nom** — Nom descriptif que les clients verront (ex. : "Esprit d'équipe", "Célébration d'anniversaire")
   - **Slug** — identifiant sécurisé pour l'URL, généré automatiquement à partir du nom
   - **Description** — Description courte facultative
   - **Catégorie** — Groupe les modèles liés (ex. : "Anniversaire", "Entreprise", "Vacances", "Sport")
   - **Ordre de tri** — Contrôle l'ordre dans lequel les modèles apparaissent dans la galerie
5. Enregistrer le modèle

## L'éditeur de modèle visuel

Après avoir créé un modèle, vous pouvez ouvrir l'**éditeur de modèle visuel** pour concevoir le layout du canevas. C'est ici que vous placez du texte, des images et des illustrations sur chaque surface, et que vous définissez les contrôles de verrouillage pour les éléments individuels.

### Travailler avec le canevas

L'éditeur de modèle fournit les mêmes outils de canevas disponibles pour les clients :

- **Outil de texte** — Ajouter des éléments de texte avec des options de police, de taille, de couleur et d'alignement
- **Outil d'image** — Ajouter des images depuis la bibliothèque multimédia
- **Outil d'illustration** — Parcourir et ajouter des illustrations depuis votre bibliothèque

Vous travaillez une surface à la fois. Utilisez les **onglets de surface** en haut du canevas pour basculer entre les surfaces (ex. : passer du devant au dos pour un modèle de t-shirt).

### Ajouter des éléments

1. Sélectionnez un outil depuis le panneau d'outils (Texte, Image ou Illustration)
2. Cliquez sur **Ajouter du texte**, téléchargez une image ou cliquez sur une illustration pour l'ajouter au canevas
3. Positionnez et redimensionnez l'élément en le faisant glisser sur le canevas
4. Utilisez le panneau des propriétés pour ajuster le style (police, couleur, taille, alignement, etc.)
5. Répétez pour chaque élément que vous souhaitez inclure dans le modèle

### Enregistrer le modèle

Lorsque vous avez terminé de concevoir, cliquez sur **Enregistrer le modèle**. Le système capture automatiquement une image miniature à partir de l'état du canevas. Cette miniature est ce que les clients voient lorsqu'ils naviguent dans la galerie de modèles.

## Contrôles de verrouillage

Les contrôles de verrouillage sont une fonctionnalité puissante qui vous permet de limiter ce que les clients peuvent faire avec des éléments spécifiques dans un modèle. Cela est essentiel pour maintenir la cohérence de la marque, garantir la qualité du design et appliquer des règles commerciales.

Lorsqu'un élément est sélectionné dans l'éditeur de modèle, vous pouvez définir cinq types de verrous :

| Verrou | Effet | Cas d'utilisation |
|--------|-------|------------------|
| **Verrou de position** | Le client ne peut pas déplacer l'élément | Gardez un logo à sa place désignée |
| **Verrou de taille** | Le client ne peut pas redimensionner l'élément | Empêchez un logo de se déformer |
| **Verrou de rotation** | Le client ne peut pas faire pivoter l'élément | Gardez le texte horizontal et lisible |
| **Verrou de contenu** | Le client ne peut pas modifier le texte ou remplacer l'image | Protégez les noms de marque, le texte légal obligatoire |
| **Verrou de suppression** | Le client ne peut pas supprimer l'élément | Assurez-vous que les éléments obligatoires apparaissent toujours |

Les verrous peuvent être combinés.

Par exemple, un logo d'entreprise pourrait avoir les cinq verrous activés (impossible de le déplacer, redimensionner, faire pivoter, modifier ou supprimer), tandis qu'un champ de texte "Votre nom ici" pourrait ne verrouiller que la position et la taille (le client peut modifier le contenu du texte mais pas le repositionner).

### Exemple : Modèle de t-shirt "Team Spirit"

Un modèle de t-shirt conçu pour des équipes sportives :

**Éléments de la surface avant :**

| Élément | Type | Verrous | Le client peut... |
|---------|------|-------|----------------|
| Logo de l'équipe (haut centre) | Image | Position, Taille, Contenu, Supprimer | Rien — le logo est entièrement verrouillé |
| Nom du joueur | Texte | Position, Taille | Modifier le nom |
| Numéro du joueur | Texte | Position, Taille | Modifier le numéro |

**Éléments de la surface arrière :**

| Élément | Type | Verrous | Le client peut... |
|---------|------|-------|----------------|
| Nom de l'équipe (en haut) | Texte | Position, Taille, Contenu, Supprimer | Rien — le nom de l'équipe est fixe |
| Message personnalisé | Texte | Position | Modifier le texte, redimensionner et faire pivoter |

Ce modèle garantit une cohérence de la marque d'équipe sur toutes les commandes tout en permettant aux clients de personnaliser leur nom et leur numéro.

### Exemple : Modèle de carte de naissance

Un modèle de carte de vœux pour un produit imprimé :

**Éléments de la surface avant :**

| Élément | Type | Verrous | Le client peut... |
|---------|------|-------|----------------|
| Bordure décorative | Image | Position, Taille, Rotation, Supprimer | Rien — la bordure encadre le design |
| Texte "Joyeux anniversaire" | Texte | Position | Modifier le texte, changer la police/couleur/taille |
| Emplacement de photo | Image | Position, Taille | Remplacer par leur propre photo |
| Petits éléments de dessin (étoiles) | Clipart | Supprimer | Déplacer, redimensionner, mais pas supprimer |

Ce modèle fournit un cadre professionnel tout en donnant aux clients une liberté créative dans les zones sécurisées.

## Catégories de modèles

Utilisez des catégories pour organiser les modèles lorsque vous en avez plus d'une dizaine. Les clients peuvent filtrer les modèles par catégorie dans l'éditeur du magasin.

Bonnes structures de catégories :

**Pour un magasin de t-shirts :**
- Sports
- Professionnel
- Événements
- Humour
- Saisonnier

**Pour un magasin d'impression/posters :**
- Anniversaire
- Mariage
- Vacances
- Motivational
- Entreprise

Gardez les noms de catégories courts et intuitifs. Les clients doivent immédiatement comprendre quel type de designs ils trouveront dans chaque catégorie.

## Comment les modèles apparaissent aux clients

Sur le magasin, l'éditeur de conception inclut un onglet **Modèles** dans le panneau d'outils. Les clients voient :

1. **Galerie de modèles** — Aperçus en miniature de tous les modèles disponibles, filtrables par catégorie
2. **Chargement en un clic** — Cliquez sur un modèle pour le charger instantanément sur le canevas
3. **Personnalisation complète** — Après le chargement, les clients peuvent modifier tout élément non verrouillé
4. **Option de démarrer à partir de zéro** — Les clients peuvent toujours choisir de commencer avec un canevas vide

Lorsqu'un client charge un modèle, tous les éléments apparaissent sur le canevas avec leurs états de verrouillage activés. Les éléments verrouillés affichent des indicateurs visuels (comme des poignées restreintes) pour que les clients comprennent les parties qu'ils peuvent et ne peuvent pas modifier.

## Conseils

- Créez au moins 3 à 5 modèles par produit pour donner aux clients un choix significatif. Un seul modèle semble limitant ; trop de modèles peuvent être écrasants.
- Faites de votre meilleur et plus versatile modèle le premier (ordre de tri le plus bas) — il fixe le ton pour l'ensemble du produit.
- Utilisez les contrôles de verrouillage de manière stratégique. Verrouillez uniquement ce qui doit absolument être fixe. Un verrouillage excessif irrite les clients et les fait se sentir comme s'ils ne pouvaient pas personnaliser le produit.
- Testez chaque modèle du point de vue du client. Chargez-le dans l'éditeur du magasin, essayez d'éditer les éléments verrouillés (vérifiez qu'ils sont effectivement verrouillés), et vérifiez que les éléments non verrouillés sont naturels à personnaliser.
- Mettez à jour les modèles saisonnièrement. Ajoutez des modèles thématiques de fêtes avant les grandes fêtes et archivez-les par la suite.
- Utilisez des noms de modèles significatifs qui aident les clients à comprendre le style du design à première vue — "Athlétique audacieux" est plus utile que "Modèle 1".