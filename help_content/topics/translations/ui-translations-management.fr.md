---
title: Gestion des traductions de l'interface utilisateur
---

La page de gestion des traductions de l'interface utilisateur vous permet de personnaliser l'apparence des chaînes d'interface frontend—boutons, étiquettes, messages d'erreur et autres textes de l'interface—dans chaque langue. Contrairement aux traductions de contenu de produits ou de pages, ce sont les éléments d'interface fixes que vos clients voient tout au long de votre magasin. Personnalisez-les pour correspondre à la voix de votre marque ou améliorer la clarté pour votre public cible.

Cette page affiche toutes les chaînes d'interface traduisibles et vous permet de remplacer les traductions par défaut fournies par Spwig.

## Comprendre les traductions de l'interface utilisateur

Les traductions de l'interface utilisateur sont les chaînes de texte qui composent votre interface de magasin :

**Exemples de chaînes d'interface utilisateur** :
- Boutons : "Ajouter au panier", "Passer à la caisse", "Rechercher"
- Étiquettes : "Prix", "Quantité", "Adresse de livraison"
- Messages : "Article ajouté au panier", "Commande confirmée", "Adresse e-mail non valide"
- Navigation : "Accueil", "Boutique", "Contactez-nous"
- Champs de formulaire : "E-mail", "Mot de passe", "Prénom"

Spwig inclut des traductions par défaut pour environ 300 chaînes d'interface utilisateur dans toutes les langues prises en charge. La page de gestion des traductions de l'interface utilisateur vous permet de remplacer l'une de ces traductions par défaut par vos propres traductions personnalisées.

## Pourquoi personnaliser les traductions de l'interface utilisateur ?

**Voix de la marque** : Changez "Ajouter au panier" en "Acheter maintenant" ou "Obtenez le vôtre" pour correspondre à la personnalité de votre marque

**Variations régionales** : Ajustez les traductions pour des marchés spécifiques (anglais britannique vs. américain, espagnol européen vs. latino-américain)

**Clarté** : Si la traduction par défaut n'a pas de sens pour vos produits ou votre public, remplacez-la par un texte plus clair

**Terminologie spécifique à un secteur** : Utilisez le vocabulaire que vos clients attendent (par exemple, "Réserver un rendez-vous" au lieu de "Ajouter au panier" pour les magasins basés sur des services)

## Recherche de chaînes

Utilisez la zone de recherche pour trouver des chaînes d'interface utilisateur spécifiques :

**Rechercher par texte anglais** : Tapez "add to cart" pour trouver les traductions de ce bouton

**Rechercher par traduction** : Tapez un texte dans n'importe quelle langue pour trouver des traductions correspondantes

**Rechercher par clé** : Si vous connaissez la clé de traduction (par exemple, `cart.add_item`), recherchez-la directement

La page se met à jour instantanément pendant que vous tapez, affichant uniquement les chaînes correspondantes.

## Affichage des détails de la traduction

Chaque chaîne d'interface utilisateur affiche :

**Texte source en anglais** - La version anglaise par défaut (votre point de référence)

**Clé de traduction** - L'identifiant interne utilisé dans le code (par exemple, `cart.add_to_cart`)

**Colonnes de langue** - La traduction actuelle pour chaque langue active

**Statut de remplacement** - Si vous avez personnalisé la traduction (mis en surbrillance si remplacement)

## Création de remplacements de traduction

Pour personnaliser la traduction d'une chaîne d'interface utilisateur :

1. **Trouver la chaîne** en utilisant la recherche (par exemple, recherchez "add to cart")
2. **Cliquez sur la cellule de langue** que vous souhaitez personnaliser
3. **Entrez votre traduction personnalisée** dans l'éditeur popup
4. **Enregistrer** - Votre remplacement prend effet immédiatement

La traduction par défaut originale est conservée - vous créez un remplacement qui a la priorité.

## Retourner aux traductions par défaut

Pour supprimer un remplacement personnalisé et restaurer la traduction par défaut :

1. **Cliquez sur la traduction remplacement** (ces dernières sont mises en surbrillance)
2. **Cliquez sur "Revenir à la traduction par défaut"** dans l'éditeur
3. **Confirmer** - La traduction par défaut est immédiatement restaurée

Vous pouvez revenir en arrière aux remplacements de langue individuels sans affecter vos remplacements dans d'autres langues.

## Filtre par statut de remplacement

Utilisez le menu déroulant de filtre pour afficher :

**Toutes les chaînes** - Toutes les chaînes d'interface utilisateur du système (~300 au total)

**Seulement les remplacements** - Chaînes pour lesquelles vous avez créé des traductions personnalisées

**Seulement les traductions par défaut** - Chaînes qui utilisent encore les traductions par défaut de Spwig

Cela vous aide à réviser les chaînes que vous avez personnalisées et à identifier les lacunes.

## Exemples de personnalisation courante

| Traduction par défaut en anglais | Remplacement personnalisé | Cas d'utilisation |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Appel à l'action plus direct |
| Checkout | Secure Checkout | Mettre l'accent sur la sécurité |
| Search | Find Products | Plus spécifique au commerce électronique |
| Contact Us | Get in Touch | Tonalité plus amicale |
| Subscribe | Join Our Newsletter | Proposition de valeur plus claire |

## Validation des traductions

Lors de l'entrée de traductions personnalisées, validez que :

**La longueur correspond à l'espace de l'interface utilisateur** - Les traductions peuvent être plus longues ou plus courtes que l'anglais (les mots allemands sont souvent plus longs, par exemple)

**Le sens est maintenu** - Ne changez pas la fonctionnalité dans la traduction (un bouton "Annuler" ne devrait pas dire "Supprimer")

**Terminologie cohérente** - Utilisez la même traduction pour les termes répétés à travers l'interface

**Formalité appropriée** - Adaptez le ton à votre marché cible (formel vs. informel)

## Cohérence multilingue

Lors de la personnalisation d'une chaîne pour plusieurs langues :

1. **Commencez par votre langue par défaut** - Définissez la base

2. **Personnalisez les autres langues** pour correspondre au même objectif

3. **Testez dans chaque langue** pour vérifier le mise en page et le sens

4. **Utilisez des locuteurs natifs** lorsqu'il est possible de réviser les personnalisation non anglaises

Les personnalisation non cohérentes à travers les langues créent une expérience client confuse.

## Exportation/Importation en lots

Pour des personnalisation étendues, envisagez d'utiliser le workflow d'exportation/importation :

1. **Exporter** les traductions actuelles au format JSON ou CSV

2. **Éditer dans une feuille de calcul** ou un éditeur de texte (plus facile pour les modifications en lots)

3. **Importer** les traductions mises à jour vers le système

Ce workflow est disponible via la page des tâches de traduction pour gérer des projets de traduction à grande échelle.

## Conseils

- **Recherchez avant de personnaliser** - Assurez-vous que vous modifiez la bonne chaîne ; certaines chaînes similaires servent à des fins différentes
- **Testez sur le frontend après avoir enregistré** - Vérifiez que votre traduction personnalisée s'affiche correctement dans l'interface utilisateur réelle
- **Gardez les traductions concises** - Plus court est généralement meilleur pour les boutons et les étiquettes
- **Documentez vos remplacements** - Notez pourquoi vous avez personnalisé des chaînes spécifiques pour référence future
- **Utilisez une terminologie cohérente** - Si vous personnalisez "Cart" en "Basket", faites-le de manière cohérente à travers toutes les chaînes liées
- **Pensez aux dispositions mobiles** - Les traductions longues peuvent s'enrouler ou se tronquer à l'écran petit
- **Révisez après les mises à jour de langue** - Lorsque Spwig ajoute de nouvelles traductions par défaut, révisez et personnalisez-les pour maintenir la cohérence

Souvenez-vous : Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.