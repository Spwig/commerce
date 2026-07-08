---
title: Générateur d'optimisation SEO par IA
---

Le Générateur d'optimisation SEO par IA écrit automatiquement les titres méta, les descriptions méta et d'autres contenus SEO pour vos produits à l'aide d'un fournisseur d'IA. Au lieu d'écrire manuellement le contenu SEO pour chaque produit, vous pouvez générer en masse un contenu précis et optimisé avec une seule action.

Votre boutique est équipée d'un générateur SEO intégré qui fonctionne immédiatement. Vous pouvez également installer des composants supplémentaires de fournisseurs d'IA depuis le marché des composants Spwig pour accéder à des modèles de langage plus puissants.

## Fonctionnement du générateur SEO

Le générateur SEO lit le nom, la description, la catégorie et les attributs de votre produit, puis utilise le fournisseur d'IA configuré pour écrire un contenu SEO adapté à ce produit. Le contenu généré est enregistré directement dans les champs SEO du produit.

Vous pouvez générer du contenu SEO pour des produits individuels depuis la page d'édition du produit, ou exécuter une génération en masse sur plusieurs produits depuis la liste des produits.

## Configuration d'un fournisseur SEO

### Utilisation du fournisseur intégré

Votre boutique inclut un fournisseur SEO intégré qui génère du contenu SEO de manière déterministe à partir des données de vos produits — aucun clé API externe n'est nécessaire. Il est automatiquement défini comme fournisseur principal lors d'une nouvelle installation.

Pour vérifier s'il est actif:

1. Accédez à **Marketing > Fournisseurs SEO**
2. Vérifiez que le fournisseur intégré apparaît avec un badge **PRINCIPAL** et un statut **ACTIF**
3. Si aucun fournisseur n'est listé, cliquez sur **+ Ajouter un compte de fournisseur SEO** et définissez **Clé du fournisseur** sur `deterministic`

### Connexion à un composant de fournisseur d'IA

Pour un contenu SEO plus riche et contextualisé, vous pouvez installer un composant de fournisseur d'IA (tel qu'un fournisseur basé sur OpenAI ou Claude) depuis le marché des composants Spwig.

1. Installez le composant du fournisseur via le système de mise à jour des composants (demandez à votre administrateur de boutique)
2. Accédez à **Marketing > Fournisseurs SEO**
3. Cliquez sur **+ Ajouter un compte de fournisseur SEO**
4. Remplissez le formulaire:

**Section Informations sur le fournisseur:**
- **Site** — sélectionnez votre boutique
- **Composant du fournisseur** — choisissez le composant du fournisseur d'IA installé
- **Clé du fournisseur** — laissez vide lors de l'utilisation d'un fournisseur basé sur un composant
- **Nom du compte** — un nom descriptif tel que `Fournisseur SEO OpenAI`

**Section Configuration:**
- **Actif** — cochez pour activer ce fournisseur
- **Principal** — cochez pour utiliser ce fournisseur comme fournisseur par défaut pour toute la génération SEO
- **Priorité** — les nombres plus bas sont essayés en premier dans la chaîne de secours
- **Paramètres** — paramètres spécifiques au fournisseur sous forme d'objet JSON (par exemple, nom du modèle, ton, langue)

5. Cliquez sur **Enregistrer**

Un seul fournisseur peut être défini comme principal. Si vous marquez un nouveau fournisseur comme principal, le fournisseur principal précédent est automatiquement dégradé.

### Chaîne de secours des fournisseurs

Si votre fournisseur principal échoue (par exemple, en raison d'une panne d'API), votre boutique bascule automatiquement vers le prochain fournisseur actif dans l'ordre de priorité. Cela garantit que la génération SEO continue à fonctionner même si un fournisseur est temporairement indisponible.

## Génération de contenu SEO pour un produit

### Produit individuel

1. Accédez à **Produits > Produits** et ouvrez tout produit
2. Faites défiler jusqu'à la section **SEO** du formulaire du produit
3. Cliquez sur le bouton **Générer le SEO**
4. Le fournisseur d'IA génère un titre méta et une description méta basés sur les détails du produit
5. Vérifiez le contenu généré et modifiez-le si nécessaire
6. Cliquez sur **Enregistrer** pour appliquer les modifications

### Génération en masse

Pour générer ou mettre à jour le contenu SEO de plusieurs produits à la fois:

1. Accédez à **Produits > Produits**
2. Sélectionnez les produits que vous souhaitez mettre à jour à l'aide de leurs cases à cocher, ou sélectionnez tous
3. Ouvrez le menu déroulant **Action**
4. Choisissez **Générer du contenu SEO** (ou un nom d'action similaire — vérifiez le menu déroulant pour l'étiquette exacte)
5. Cliquez sur **Aller**

Spwig met en file d'attente les tâches de génération et les traite en arrière-plan. Actualisez la liste des produits après une minute ou deux pour voir les champs SEO mis à jour.

## Vérification de la couverture SEO

Le générateur SEO suit les produits qui ont déjà du contenu SEO. Pour identifier les produits qui ont encore besoin de SEO:

1.

Accédez à **Produits > Produits**
2.


Utilisez le filtre **Statut SEO** (s'il est disponible) pour afficher les produits dont les titres ou descriptions méta sont manquants
3.

Sélectionnez ces produits et exécutez l'action de génération par lots

## Paramètres du fournisseur

Le champ **Paramètres** d'un compte de fournisseur SEO accepte un objet JSON avec une configuration spécifique au fournisseur. Les options courantes incluent :

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Ces paramètres varient selon le composant du fournisseur. Consultez la documentation du fournisseur pour obtenir la liste complète des options disponibles.

## Gestion de plusieurs fournisseurs

Si vous avez plus d'un compte de fournisseur SEO configuré, la liste des fournisseurs affiche leur statut à un coup d'œil :

- **Étiquette PRINCIPALE** — ce fournisseur est utilisé par défaut pour toute génération SEO
- **Étiquette ACTIVE** — le fournisseur est activé
- **Étiquette INACTIVE** — le fournisseur est désactivé et ne sera pas utilisé

Pour changer quel fournisseur est principal, ouvrez le compte de fournisseur que vous souhaitez promouvoir, cochez la case **Est principal**, puis enregistrez. Le système garantit automatiquement qu'un seul fournisseur possède l'indicateur principal à tout moment.

## Conseils

- Générez du contenu SEO pour les nouveaux produits immédiatement après leur création — cela ne prend que quelques secondes et fournit quelque chose d'utile aux moteurs de recherche à indexer dès maintenant
- Vérifiez les descriptions méta générées par l'IA avant de publier si vos produits ont des noms inhabituels ou techniques ; le générateur fonctionne le mieux avec des noms de produits clairs et descriptifs
- Définissez "max_title_length": 60 et "max_description_length": 160 dans les paramètres du fournisseur pour garder le contenu généré dans les limites de caractères recommandées par Google
- Exécutez une génération SEO par lots après avoir importé un grand catalogue de produits pour remplir rapidement tous les champs SEO
- Si vous mettez à jour de manière significative la description d'un produit, régénérez son contenu SEO pour maintenir les balises méta alignées avec le nouveau texte
- Le fournisseur déterministe intégré est un bon point de départ ; misez sur un composant alimenté par l'IA une fois que votre catalogue est configuré et que vous souhaitez des textes SEO plus riches et plus naturels