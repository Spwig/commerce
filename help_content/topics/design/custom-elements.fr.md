---
title: Éléments personnalisés
---

Les éléments personnalisés vous permettent de créer des blocs réutilisables du constructeur de pages adaptés aux besoins de votre magasin. Vous concevez un élément visuellement à l'aide des outils existants du constructeur de pages, puis vous pouvez le connecter à des données du magasin en temps réel — comme les noms de produits, les prix ou les images — afin que l'élément s'actualise automatiquement avec du contenu réel lorsqu'il est placé sur une page. Une fois créé, vos éléments personnalisés apparaissent dans la bibliothèque d'éléments du constructeur de pages, à côté des blocs intégrés.

![Bibliothèque d'éléments personnalisés](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Quand utiliser des éléments personnalisés

Les éléments personnalisés sont les plus utiles lorsque vous vous retrouvez à créer régulièrement le même mise en page. Au lieu de recréer une « carte de produit mis en avant » à partir de zéro sur chaque page, vous la construisez une seule fois en tant qu'élément personnalisé et vous l'insérez là où vous en avez besoin. Si l'élément est lié à des données, il extrait automatiquement les informations actuelles du produit — aucune mise à jour manuelle n'est nécessaire lorsque les prix ou les noms changent.

Utilisations courantes :

- Cartes de mise en avant des produits affichant le nom, le prix et l'image principale
- Blocs de promotion de catégorie avec bannière, titre et lien
- Panneaux de présentation de marque avec logo et description
- Aperçus d'articles de blog avec image mise en avant, titre et extrait

## Créer un nouvel élément personnalisé

1. Accédez à **Design > Éléments personnalisés**
2. Cliquez sur **+ Ajouter un élément personnalisé**
3. Spwig crée immédiatement un brouillon d'élément et ouvre le **Constructeur visuel** — vous n'avez pas besoin de remplir un formulaire en premier
4. Dans le Constructeur visuel, concevez la mise en page de votre élément à l'aide des outils du constructeur de pages disponibles
5. Lorsque vous êtes satisfait de la conception, configurez les paramètres de l'élément (nom, liaison de données, icône) dans la barre latérale
6. Activez **Actif** lorsque vous êtes prêt à publier l'élément dans la bibliothèque
7. Enregistrez l'élément

L'élément est désormais disponible dans le panneau d'éléments du constructeur de pages sous la catégorie que vous avez assignée.

## Le constructeur visuel

Le Constructeur visuel est un canevas dédié à la conception de votre élément. Il fonctionne comme le constructeur de pages standard mais se concentre sur un seul élément plutôt qu'une page entière. Vous pouvez :

- Ajouter et organiser des éléments enfants (blocs de texte, images, conteneurs, etc.)
- Définir le style, l'espacement et la mise en page de chaque élément enfant
- Prévisualiser l'aspect de l'élément avec des données d'exemple

Les modifications apportées dans le Constructeur visuel sont enregistrées directement dans la définition de l'élément. Il n'y a pas d'étape de publication séparée — l'enregistrement dans le constructeur met immédiatement à jour l'élément pour toutes les pages qui l'utilisent déjà.

## Configuration des paramètres de l'élément

Chaque élément personnalisé possède les paramètres suivants :

| Champ | Description |
|-------|-------------|
| **Nom** | Nom affiché dans la bibliothèque d'éléments |
| **Slug** | Identifiant sécurisé pour les URL, généré automatiquement à partir du nom |
| **Description** | Note optionnelle sur l'utilisation de cet élément |
| **Modèle cible** | Le modèle de magasin à partir duquel lier les données (voir ci-dessous) |
| **Icône** | Icône affichée dans la bibliothèque d'éléments |
| **Catégorie** | Groupe les éléments liés ensemble dans la bibliothèque |
| **Actif** | Indique si l'élément est disponible dans le constructeur de pages |

## Liaison de données

La liaison de données connecte des parties de la mise en page de votre élément aux données du magasin en temps réel. Lorsqu'un éditeur de page place un élément lié à des données sur une page, ils sélectionnent un enregistrement spécifique (par exemple, un produit), et tous les champs liés s'actualisent automatiquement à partir de cet enregistrement.

### Sélectionner un modèle cible

Le paramètre **Modèle cible** détermine quel type de données du magasin l'élément peut afficher. Les modèles disponibles sont :

| Modèle | Ce qu'il fournit |
|-------|-----------------|
| **Produit** | Nom, prix, statut de stock, images, description, SKU, catégorie, marque, et plus |
| **Catégorie** | Nom, description, image, bannière, nombre de produits, et URL |
| **Marque** | Nom, logo, description, histoire de la marque, et URL |
| **Article de blog** | Titre, extrait, image mise en avant, auteur, date de publication, et URL |

Laissez **Modèle cible** vide pour créer un élément statique sans données dynamiques. Les éléments statiques sont utiles pour des composants de design fixes comme des bannières décoratives ou des espaces de mise en page.

### Fonctionnement des liaisons


Dans le Visual Builder, vous pouvez marquer individuellement les éléments enfants comme liés à des données en sélectionnant le champ du modèle qu'ils doivent afficher.

Par exemple:
- Un élément enfant **texte** peut être lié à **Nom du produit**, afin d'afficher le nom du produit sélectionné
- Un élément enfant **image** peut être lié à **Image principale**, afin d'afficher la photo principale du produit
- Un élément enfant **texte** peut être lié à **Prix**, afin de refléter toujours le prix actuel

Chaque liaison mappe un champ de contenu d'un élément à un champ de modèle. Vous pouvez ajouter plusieurs liaisons à un seul élément personnalisé — par exemple, lier un bloc de texte à **Nom du produit** et un bloc d'image séparé à **Image principale** en même temps.

### Préférences de miniature d'image

Pour les liaisons d'image, vous pouvez optionnellement spécifier un **Préfixe de miniature** (tel que `thumbnail` ou `medium`). Cela contrôle la taille de l'image chargée, aidant les pages à charger plus rapidement en servant l'image de la taille appropriée pour le layout de l'élément.

## Désactiver et réactiver des éléments

Désactiver un élément le retire de la bibliothèque d'éléments afin qu'il ne puisse pas être ajouté à de nouvelles pages. Les pages existantes qui utilisent déjà l'élément ne sont pas affectées — l'élément continue d'être rendu sur ces pages.

Pour désactiver:
1. Accédez à **Design > Éléments personnalisés**
2. Cliquez sur le nom de l'élément
3. Désélectionnez **Actif**
4. Enregistrez

Pour réactiver, suivez les mêmes étapes et sélectionnez à nouveau **Actif**.

## Filtrage de la bibliothèque d'éléments

La liste des éléments prend en charge le filtrage par:
- **Actif / Inactif** — afficher uniquement les éléments publiés ou uniquement les brouillons
- **Modèle cible** — filtrer par le modèle auquel un élément est lié
- **Catégorie** — filtrer par catégorie d'élément
- **Recherche** — rechercher par nom, slug ou description

Cela aide lorsque vous avez de nombreux éléments personnalisés et que vous avez besoin de trouver un élément spécifique rapidement.

## Exemple : carte de mise en avant de produit

**Objectif :** Une carte d'élément qui affiche l'image principale, le nom et le prix d'un produit.

| Paramètre | Valeur |
|---------|-------|
| Nom | Carte de mise en avant de produit |
| Modèle cible | Produit |
| Catégorie | Produits |
| Icône | fas fa-box |

Dans le Visual Builder, ajoutez:
- Un élément **Image** lié à **Image principale** avec le préfixe de miniature `medium`
- Un élément **Texte** lié à **Nom du produit**
- Un élément **Texte** lié à **Prix**

Une fois enregistré et activé, l'élément apparaît dans le constructeur de pages sous la catégorie Produits. Lorsqu'un éditeur de page l'ajoute à une page, il sélectionne quel produit mettre en avant, et la carte s'auto-remplit automatiquement.

## Conseils

- Donnez aux éléments des noms descriptifs qui incluent leur objectif et le type de données — par exemple, « Carte de mise en avant de produit » plutôt que « Carte 1 » — afin que la bibliothèque reste facile à naviguer à mesure qu'elle grandit
- Utilisez le champ **Catégorie** pour regrouper les éléments liés (Produits, Blog, Promotions) — cela permet de garder la bibliothèque d'éléments organisée pour vos éditeurs de page
- Testez les éléments liés à des données en les ajoutant à une page brouillon et en sélectionnant un enregistrement réel avant de publier, afin de confirmer que la liaison affiche les informations correctes
- Désactivez les éléments obsolètes au lieu de les supprimer — cela préserve toutes les pages qui y font encore référence et vous donne l'option de les réactiver plus tard
- Les éléments statiques (sans modèle cible) sont idéaux pour les modèles de mise en page que vous réutilisez sur tout le site, tels que des séparateurs, des panneaux CTA ou des espaces réservés personnalisés