---
title: Collections de produits
---

Les collections vous permettent de regrouper des produits pour les afficher sur votre boutique en ligne. Contrairement aux catégories — qui organisent votre catalogue entier dans une hiérarchie permanente — les collections sont des regroupements flexibles et ciblés que vous créez pour un objectif spécifique. Une collection peut mettre en avant les nouvelles arrivées, présenter des articles pour une campagne saisonnière ou afficher une sélection soigneusement choisie de best-sellers.

Accédez à **Catalogue > Collections** pour gérer vos collections.

## Collections vs catégories

Les catégories et les collections regroupent des produits, mais elles servent à des fins différentes :

|  | Catégories | Collections |
|---|---|---|
| **Objectif** | Structure permanente du catalogue | Regroupements flexibles et ciblés |
| **Hiérarchie** | Oui — structure imbriquée parent/enfant | Non — regroupements plats |
| **Produits par groupe** | Chaque produit appartient à une seule catégorie | Un produit peut apparaître dans plusieurs collections |
| **Utilisation typique** | Menu de navigation de la boutique, navigation par département | Pages d'accueil, campagnes, ensembles mis en avant |

Utilisez les catégories pour "la manière dont votre boutique est organisée" et les collections pour "ce que vous souhaitez mettre en avant en ce moment".

## Types de collections

Lors de la création d'une collection, choisissez un type qui correspond à la manière dont vous souhaitez gérer la liste de produits :

| Type | Comment les produits sont ajoutés |
|---|---|
| **Sélection manuelle** | Vous choisissez exactement les produits qui apparaissent, un par un |
| **Règles automatiques** | Les produits sont ajoutés automatiquement en fonction des critères que vous définissez |
| **Produits mis en avant** | Une sélection éditoriale ciblée, gérée manuellement |
| **Saisonnier** | Une sélection basée sur le temps, généralement gérée manuellement pour les campagnes |

Les types Manuel et Produits mis en avant vous donnent un contrôle précis. Les collections automatiques peuvent s'agrandir avec votre catalogue sans maintenance continue.

## Créer une collection

1. Accédez à **Catalogue > Collections**
2. Cliquez sur **+ Ajouter une collection**
3. Remplissez la section **Informations de base** :
   - **Nom** — le nom de la collection tel qu'il apparaîtra sur votre boutique en ligne
   - **Slug** — le chemin URL de la page de la collection (rempli automatiquement à partir du nom ; vous pouvez le personnaliser)
   - **Description** — une description affichée sur la page de la collection sur votre boutique en ligne
4. Sélectionnez un **Type de collection**
5. Ajoutez des produits :
   - Pour les types **Sélection manuelle** et **Produits mis en avant** : utilisez le champ **Produits** pour rechercher et ajouter des produits
   - Pour le type **Automatique** : définissez les critères dans le champ **Critères automatiques**
6. Téléchargez des images :
   - **Image** — l'image principale de la collection utilisée sur les pages de liste et les miniatures
   - **Image de bannière** — une image de bannière plus large affichée en haut de la page de la collection
7. Configurez les champs **SEO** (facultatif mais recommandé) :
   - **Titre meta** — le titre de la page affiché dans les résultats de recherche
   - **Description meta** — la description affichée sous le titre dans les résultats de recherche
8. Définissez les **Options d'affichage** :
   - **Actif** — contrôle si la collection est visible sur votre boutique en ligne
   - **Mis en avant** — marque la collection pour une mise en avant dans votre thème
   - **Ordre de tri** — contrôle l'ordre dans lequel les collections apparaissent sur les pages de liste (les numéros plus bas apparaissent en premier)
9. Cliquez sur **Enregistrer**

## Ajouter des produits à une collection

Pour les collections manuelles, utilisez le champ d'autocomplétion **Produits** pour rechercher dans votre catalogue et sélectionner des articles. Vous pouvez ajouter autant de produits que nécessaire — il n'y a pas de limite.

Les produits peuvent appartenir à plusieurs collections en même temps. Par exemple, un produit pourrait être dans votre collection "Vente d'été" et dans votre collection "Best-sellers" sans conflit.

## Afficher les collections sur votre boutique en ligne

Chaque collection obtient automatiquement sa propre page à l'adresse `/collection/{slug}/`. Vous pouvez lier les pages de collection à partir de votre menu de navigation, du constructeur de pages ou des bannières promotionnelles.

Le drapeau **Mis en avant** est utilisé par votre thème pour déterminer quelles collections apparaissent dans les emplacements mis en avant — par exemple, une grille de collections mises en avant sur la page d'accueil. Vérifiez la documentation de votre thème pour comprendre exactement comment les collections mises en avant sont affichées.

## Gérer la visibilité des collections

- **Actif** contrôle si la page de collection est accessible au public.

Une collection inactive est cachée aux clients mais conservée dans l'admin afin que vous puissiez la réactiver plus tard.
- **Ordre de tri** détermine l'ordre dans lequel les collections apparaissent sur les pages de liste.

Affectez des nombres plus bas aux collections que vous souhaitez afficher en premier.

## SEO pour les collections

Chaque collection possède ses propres champs **Titre meta** et **Description meta**. Ces éléments déterminent ce qui apparaît dans les résultats des moteurs de recherche lorsque quelqu'un trouve votre page de collection. Si vous laissez ces champs vides, votre thème utilisera généralement le nom et la description de la collection.

Les titres SEO de collection de bonne qualité sont descriptifs et précis :
- "Summer Dresses 2026 — Floral & Lightweight Styles" performe mieux que "Summer Collection"
- "Men's Running Shoes — Lightweight & Breathable" performe mieux que "Running Shoes"

## Conseils

- Gardez les noms de collection courts et clairs — ils apparaissent comme titres de page et textes de lien dans la navigation de votre boutique en ligne
- Utilisez des collections saisonnières ou des campagnes avec une planification de début et de fin : créez la collection, activez-la lorsque la campagne commence, et désactivez-la (plutôt que de la supprimer) lorsque celle-ci se termine afin de pouvoir y faire référence plus tard
- Le champ **Ordre de tri** vaut la peine d'être défini délibérément — la valeur par défaut est 0 pour toutes les collections, ce qui signifie qu'elles sont triées alphabétiquement. Affectez des numéros spécifiques pour contrôler lesquelles des collections apparaissent en premier
- Une collection sans produits affichera une page vide aux clients — ajoutez des produits avant d'activer la collection, ou laissez-la inactive jusqu'à ce qu'elle soit prête
- Vérifiez le drapeau **En vedette** uniquement pour les collections que vous souhaitez vraiment mettre en avant ; la plupart des thèmes réservent les emplacements en vedette pour un petit nombre de collections et l'affichage peut devenir encombré si trop sont marqués comme tels