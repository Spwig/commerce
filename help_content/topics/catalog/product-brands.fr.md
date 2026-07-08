---
title: Marques de produits
---

Les marques vous permettent d'associer des produits à leur fabricant ou étiquette et donnent aux clients un moyen de naviguer dans votre magasin par marque. Chaque marque dispose de sa propre page sur votre boutique en ligne, où les clients peuvent découvrir tous les produits de cette marque, lire l'histoire de la marque et suivre un lien vers le site web de la marque.

Accédez à **Catalogue > Marques** pour gérer vos marques.

## Pourquoi utiliser des marques

Les marques servent à deux fins dans Spwig :

1. **Organisation** — les produits sont étiquetés avec une marque, ce qui rend facile pour les clients fidèles à une marque particulière de trouver ce qu'ils cherchent
2. **Merchandising** — les pages de marque sont un espace dédié pour mettre en valeur l'histoire de la marque, son logo et toute sa gamme de produits, ce qui peut améliorer la conversion pour les clients sensibles aux marques

Les marques fonctionnent également avec le système de promotions — vous pouvez lancer une promotion qui s'applique à tous les produits d'une marque spécifique sans avoir à sélectionner les produits individuellement.

## Créer une marque

1. Accédez à **Catalogue > Marques**
2. Cliquez sur **+ Ajouter une marque**
3. Remplissez la section **Informations de base** : 
   - **Nom** — le nom de la marque tel qu'il apparaîtra sur votre boutique en ligne (doit être unique)
   - **Slug** — le chemin URL de la page de la marque (rempli automatiquement à partir du nom ; vous pouvez le personnaliser)
   - **Description** — une courte description de la marque affichée sur la page de la marque
   - **Site web** — l'URL du site web officiel de la marque (facultatif — affiché en tant que lien sur la page de la marque)
4. Ajoutez des éléments graphiques de la marque : 
   - **Logo** — l'image du logo de la marque, utilisée dans les listes de marques et sur la page de la marque
   - **Image d'en-tête** — une image large affichée en haut de la page de la marque
5. Rédigez l'**Histoire de la marque** (facultatif) — un article éditorial plus long sur l'histoire, les valeurs ou ce qui rend la marque spéciale. Cela apparaît sur la page de la marque sur votre boutique en ligne et peut être un moyen efficace de raconter l'histoire de la marque aux clients intéressés.
6. Configurez les champs **SEO** : 
   - **Titre meta** — le titre de la page affiché dans les résultats des moteurs de recherche
   - **Description meta** — la courte description affichée sous le titre dans les résultats de recherche
7. Configurez les options d'affichage : 
   - **Afficher la page de la marque** — contrôle si la marque a une page publique accessible. Désélectionnez pour cacher une marque de la boutique en ligne tout en la conservant dans le système.
   - **Actif** — contrôle si la marque est disponible pour être attribuée à des produits et visible dans le magasin
   - **En vedette** — marque la marque pour une mise en avant dans votre thème (par exemple, une rangée de logos de marques sur la page d'accueil)
8. Cliquez sur **Enregistrer**

## Attribuer des produits à une marque

Les marques sont attribuées sur les enregistrements de produits individuels, et non depuis la page de gestion des marques. Pour attribuer une marque à un produit : 

1. Accédez à **Catalogue > Produits** et ouvrez le produit
2. Dans le formulaire du produit, trouvez le champ **Marque**
3. Recherchez et sélectionnez la marque appropriée
4. Enregistrez le produit

Une fois qu'une marque est attribuée, le produit apparaîtra automatiquement sur la page de la marque sur votre boutique en ligne.

## Pages de marque sur votre boutique en ligne

Chaque marque avec **Afficher la page de la marque** activé dispose de sa propre page à l'adresse `/brand/{slug}/`. La page affiche :

- Le logo de la marque et l'image d'en-tête
- Le nom de la marque et la description
- L'histoire de la marque (si fournie)
- Un lien vers le site web de la marque (si fourni)
- Tous les produits actifs attribués à cette marque

Les clients peuvent accéder aux pages de marque en cliquant sur le nom de la marque sur une page de produit, ou via les liens que vous créez dans votre navigation ou votre constructeur de pages.

## SEO pour les pages de marque

Remplir les champs **Titre meta** et **Description meta** pour chaque marque aide vos pages de marque à apparaître bien dans les résultats de recherche. Les titres SEO efficaces pour les marques combinent généralement le nom de la marque avec ce que la marque vend : 

| Marque | Bon titre meta |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Si vous laissez les champs SEO vides, votre thème utilisera par défaut le nom de la marque.

### Génération automatique de SEO

Si **SEO Auto Généré** est activé pour une marque, Spwig générera automatiquement le titre et la description métas lors de la sauvegarde de la marque.

Cela est pratique pour les magasins ayant de nombreuses marques, mais cela vous donne moins de contrôle sur le texte exact.

Vous pouvez toujours remplacer le contenu généré en tapant directement dans les champs et en désactivant le commutateur de génération automatique.

## Marques en vedette

Le drapeau **Is Featured** est utilisé par les thèmes pour afficher une rangée ou une grille de logos de marques sélectionnées — généralement sur la page d'accueil. Seules un petit nombre de marques devraient être en vedette à la fois ; consultez la documentation de votre thème pour comprendre combien de marques en vedette s'affichent de manière optimale.

## Conseils

- Téléchargez un logo de marque au format PNG ou WebP avec un fond transparent — il s'affichera proprement sur n'importe quelle couleur de fond de votre thème
- Rédigez une histoire de marque percutante, même pour les marques moins connues ; les clients qui ne connaissent pas une marque apprécieront le contexte qui les aidera à décider si les produits conviennent à leurs besoins
- Si vous lancez des promotions ciblant des marques spécifiques, assurez-vous que le nom de la marque dans Spwig correspond exactement — les promotions utilisent la relation de marque sur les produits pour déterminer l'éligibilité
- Désactivez une marque plutôt que de la supprimer lorsque vous arrêtez de la vendre — la suppression supprime la référence de la marque de tous les produits associés, alors que la désactivation préserve l'historique
- Utilisez le drapeau **Is Featured** avec parcimonie ; une page d'accueil affichant 20 logos de marques perd de son impact par rapport à 6 à 8 choix soigneusement sélectionnés