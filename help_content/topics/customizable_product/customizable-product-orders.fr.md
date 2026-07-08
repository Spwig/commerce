---
title: Exécution des commandes de produits personnalisables
---

Lorsqu'un client conçoit un produit et passe une commande, son design est figé et stocké avec la commande. Ce guide explique comment les designs personnalisés circulent dans le cycle de vie des commandes et comment accéder aux fichiers prêts à l'impression dont vous avez besoin pour l'exécution.

## Cycle de vie du design

Un design du client passe par plusieurs étapes, de la création à l'exécution :

### 1. Création du design

Le client utilise l'éditeur visuel sur le site de vente pour créer son design. Pendant qu'ils travaillent, leur progression est automatiquement enregistrée dans le navigateur. Les clients enregistrés peuvent également sauvegarder des designs dans leur compte pour les modifier ultérieurement.

### 2. Brouillon de design

Lorsque le client clique sur **Ajouter au panier**, l'état actuel du design est enregistré comme **brouillon de design**. Le brouillon inclut :

- L'état complet du canevas pour chaque surface (positions des éléments, contenu du texte, images téléchargées, illustrations, styles)
- Un aperçu des coûts montrant toutes les frais applicables au design
- Aperçus en miniature de chaque surface

Le brouillon est lié à l'élément du panier via un jeton unique. Cela garantit que le design exact que le client a créé est préservé, même s'ils continuent à acheter avant de passer à la caisse.

**Expiration du brouillon :** Les brouillons de design expirent automatiquement après 7 jours si le client n'achève pas la commande. Cela empêche l'accumulation de designs abandonnés.

### 3. Capture d'écran du design

Lorsque le client termine le paiement et que la commande est passée, le brouillon de design est converti en **capture d'écran de design immuable**. C'est l'enregistrement permanent du design :

- La capture d'écran ne peut pas être modifiée par le client après l'achat
- Elle contient les mêmes données de design que le brouillon
- Elle est définitivement liée à l'élément spécifique de la commande

Cette immutabilité est importante — elle garantit que ce que le client a commandé est exactement ce que vous produisez et expédiez, sans possibilité de modification après le paiement.

### 4. Génération des fichiers d'exécution

Après la passation de commande, le système génère automatiquement des **fichiers d'exécution à haute résolution** pour chaque surface du design. Ce sont des images composées qui combinent tous les éléments du design (texte, images, illustrations) en un seul fichier prêt à l'impression à la DPI configurée pour chaque surface.

La génération se fait de manière asynchrone en arrière-plan. Pour la plupart des designs, la génération se termine en quelques secondes. L'état **Rendu** de la capture d'écran indique si les fichiers d'exécution sont prêts.

## Accès aux données de design dans les commandes

### Page détaillée de la commande

Lorsque vous consultez une commande contenant des produits personnalisables dans le panneau d'administration :

1. Accédez à **Commandes > Toutes les commandes**
2. Ouvrez la commande contenant le produit personnalisé
3. L'élément de commande pour le produit personnalisable affiche les informations de design, y compris les aperçus des surfaces et un lien vers la capture d'écran du design

### Liste des captures d'écran de design

Vous pouvez également consulter toutes les captures d'écran de design directement :

1. Accédez à **Produits personnalisables > Captures d'écran de design**
2. La liste affiche toutes les captures d'écran liées aux éléments de commande
3. Cliquez sur une capture d'écran pour afficher les données de design complètes, les images rendues et les fichiers d'exécution

Chaque capture d'écran affiche :

| Champ | Description |
|-------|-------------|
| **Élément de commande** | Lien vers l'élément de commande associé |
| **Données de design** | L'état complet du canevas (JSON) |
| **Images rendues** | Aperçus en miniature par surface |
| **Fichiers d'exécution** | Fichiers composés à haute résolution pour l'impression |
| **Rendu** | Indique si le rendu est terminé |
| **Rendu le** | Horodatage indiquant à quel moment les fichiers ont été générés |

## Téléchargement des fichiers d'exécution

Les fichiers d'exécution sont ceux que vous envoyez à votre imprimeur ou utilisez dans votre processus de production.

**Pour une commande de t-shirt personnalisé :**
- Téléchargez le fichier de la surface **Avant** (par exemple, image PNG composée à 300 DPI)
- Téléchargez le fichier de la surface **Arrière**
- Téléchargez le fichier de la surface **Manche** (si conçu)
- Envoyez tous les fichiers à votre imprimeur en sérigraphie ou DTG (impression directe sur vêtement)

**Pour une commande de poster personnalisé :**
- Téléchargez le fichier de surface **Front** unique à la résolution d'impression
- Le fichier inclut une zone de débordement si celle-ci a été configurée pour la surface
- Envoyez-le à votre imprimeur de posters/cartes

Chaque fichier est une image composite unique contenant tous les éléments du design fusionnés ensemble, rendus à la DPI que vous avez configurée pour cette surface.

## Designs enregistrés

Les clients inscrits peuvent enregistrer leurs designs dans leur compte pour les modifier ultérieurement. En tant que vendeur, vous pouvez consulter ces designs enregistrés dans une liste en lecture seule :

1. Accédez à **Produits personnalisables > Designs enregistrés**
2. La liste affiche tous les designs enregistrés par les clients avec le nom du client, le produit, le nom du design et la date

Les designs enregistrés sont :
- **Propriétés du client** — Ils appartiennent au compte du client
- **En lecture seule pour les vendeurs** — Vous pouvez les consulter mais pas les modifier
- **Séparés des commandes** — Un design enregistré ne devient une commande que lorsque le client l'ajoute au panier et passe à la caisse
- **Réutilisables** — Les clients peuvent charger un design enregistré, le modifier et passer plusieurs commandes

## Workflow de traitement

### Workflow standard

1. **Réception de la commande** — La commande apparaît dans votre liste de commandes avec les articles personnalisés
2. **Vérification du rendu** — Vérifiez que l'aperçu du design affiche **Rendu : Oui**. Si le rendu n'est pas encore terminé, attendez quelques instants et actualisez
3. **Téléchargement des fichiers** — Téléchargez le fichier de traitement pour chaque surface personnalisée
4. **Vérification de la qualité** — Ouvrez les fichiers et vérifiez que le design correspond à vos normes de qualité d'impression (vérifiez la DPI, la position des éléments et la lisibilité du texte)
5. **Envoi à la production** — Transmettez les fichiers à votre fournisseur d'impression ou à votre équipe de production
6. **Expédition et finalisation** — Après la production, expédiez le produit et marquez la commande comme traitée

### Exemple de traitement de t-shirt

1. Commande reçue : "T-shirt d'équipe personnalisé" avec des designs sur le devant et le dos
2. Ouvrez la commande → consultez l'aperçu du design
3. Téléchargez `front.png` (300 DPI, 300x400mm) et `back.png` (300 DPI, 300x400mm)
4. Envoyez les deux fichiers à votre imprimante DTG avec la couleur du vêtement et la taille sélectionnées dans la variante de la commande
5. Après l'impression et la vérification de la qualité, expédiez au client

### Exemple de traitement de poster

1. Commande reçue : "Poster A4 personnalisé" avec une seule surface personnalisée
2. Ouvrez la commande → consultez l'aperçu du design
3. Téléchargez `front.png` (300 DPI, 210x297mm avec 3mm de débordement)
4. Envoyez-le à votre service d'impression de posters
5. Après l'impression et le découpage, expédiez au client

## Dépannage

**Problème :** L'aperçu du design affiche "Rendu : Non" et le rendu n'est pas terminé

- **Cause :** La tâche de rendu en arrière-plan peut avoir échoué ou est toujours en cours de traitement
- **Solution :** Attendez quelques minutes. Si le rendu ne se termine pas, vérifiez les journaux des tâches en arrière-plan. Vous pouvez également consulter directement les données du design dans l'aperçu pour confirmer que le design du client est préservé

**Problème :** Le fichier de traitement semble de moindre qualité que prévu

- **Cause :** Le client a peut-être téléchargé des images de faible résolution
- **Solution :** Vérifiez les paramètres de DPI de la surface. Si des avertissements de DPI minimum ont été configurés, le client aurait été averti lors du processus de conception. Pour les produits futurs, envisagez d'augmenter les exigences minimales en termes de DPI

**Problème :** Le client demande des modifications à son design après avoir passé une commande

- **Solution :** Les aperçus de design sont immuables par conception. Si le client a besoin de modifications, il doit passer une nouvelle commande avec le design mis à jour. Si vous acceptez de faire une exception, le client peut utiliser son design enregistré (s'il en a enregistré un) comme point de départ pour une nouvelle commande

## Conseils

- Vérifiez toujours que le rendu est terminé avant de commencer la production.

Vérifiez le champ **Rendu** sur l'aperçu du design.
- Gardez les paramètres de DPI adaptés à votre méthode d'impression.

Un DPI plus élevé produit une meilleure qualité mais des fichiers plus volumineux. 300 DPI est la norme pour la plupart des produits d'impression professionnels.
- Encouragez les clients à enregistrer leurs designs avant de passer commande.

Conservez tous les formats de mise en forme Markdown, les chemins d'image, les blocs de code et les termes techniques.

# Si un problème de production survient et que la commande doit être refaite, la conception enregistrée simplifie le réapprovisionnement.
- Intégrez un buffer dans votre calendrier de production pour les produits personnalisables.

Contrairement aux produits standard, chaque article nécessite un traitement de fichiers individuel.
- Si vous traitez de fortes quantités de commandes personnalisables, envisagez d'automatiser l'étape de téléchargement des fichiers en intégrant l'API de votre fournisseur d'impression.