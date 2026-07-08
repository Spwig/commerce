---
title: Règles de tarification séduisante
---

La tarification séduisante (aussi appelée tarification psychologique) ajuste automatiquement les prix de vos produits pour qu'ils se terminent par des chiffres spécifiques qui semblent plus attractifs pour les clients. Par exemple, au lieu d'afficher un prix de 20,00 $, la tarification séduisante peut afficher 19,99 $ — une technique largement utilisée qui fait paraître les prix plus bas à première vue.

Spwig applique automatiquement les règles de tarification séduisante dans votre magasin, par devise, donc vous n'avez besoin de définir chaque règle qu'une seule fois.

## Fonctionnement de la tarification séduisante

Lorsqu'un prix de produit est calculé (y compris après des promotions ou des réductions), Spwig vérifie s'il existe une règle de tarification séduisante active pour cette devise. Si c'est le cas, le prix est ajusté avant d'être affiché aux clients. L'ajustement s'applique aux prix supérieurs à votre seuil minimum choisi.

Vous pouvez configurer des règles distinctes pour chaque devise acceptée par votre magasin. Par exemple, vous pourriez utiliser des finales en .99 pour le USD mais arrondir au plus proche de 10 ¥ pour le JPY.

## Création d'une règle de tarification séduisante

1. Accédez à **Catalogue > Règles de tarification séduisante**
2. Cliquez sur **+ Ajouter une règle de tarification séduisante**
3. Sélectionnez la **Devise** à laquelle cette règle s'applique (par exemple, `USD`, `EUR`, `NZD`)
4. Choisissez un **Type de règle** (voir le tableau ci-dessous)
5. Définissez éventuellement un **Seuil de prix minimum** pour exclure les prix très bas
6. Cochez **Appliquer aux prix de vente** si vous souhaitez également appliquer la tarification séduisante lorsque les articles sont en promotion
7. Assurez-vous que **Actif** est coché
8. Cliquez sur **Enregistrer**

Un seul règle peut exister par devise. Si vous avez besoin de modifier une règle, modifiez celle existante.

## Types de règles

| Type de règle | Exemple | Meilleur pour |
|---------------|---------|---------------|
| **Séduire avec une fin .99** | 20,50 $ → 19,99 $ | La plupart des produits de détail — le prix psychologique classique |
| **Séduire avec une fin .95** | 20,50 $ → 19,95 $ | Alternative légèrement plus douce à .99 |
| **Séduire avec une fin .90** | 20,50 $ → 19,90 $ | Arrondi mais toujours inférieur au dollar suivant |
| **Arrondir à la baisse** | 19,50 $ → 19,00 $ | Les magasins qui préfèrent les nombres entiers |
| **Arrondir à la hausse** | 19,50 $ → 20,00 $ | Arrondir légèrement pour des affichages propres |
| **Arrondir au plus proche de 5** | 23,00 $ → 25,00 $ | Les détaillants à fort trafic et marchés |
| **Arrondir au plus proche de 10** | 23,00 $ → 20,00 $ | Les articles plus chers tels que les électroménagers |
| **Arrondir au plus proche de 100** | 1 234 $ → 1 200 $ | Les articles de haute valeur tels que le mobilier ou l'électronique |
| **Fin personnalisée** | N'importe laquelle — spécifiez ci-dessous | Lorsque votre marque utilise une fin spécifique telle que `.88` |

### Fins personnalisées

Si vous choisissez **Fin personnalisée**, entrez la valeur de fin dans le champ **Fin personnalisée**. Par exemple, entrez `0.88` pour que tous les prix se terminent par `.88` (courant dans certains marchés asiatiques).

## Seuil de prix minimum

Utilisez le champ **Seuil de prix minimum** pour ignorer la tarification séduisante pour les articles très peu chers où l'ajustement semblerait étrange. Par exemple, en définissant un seuil de `5,00`, les produits dont le prix est inférieur à 5 $ seront affichés à leur prix calculé réel sans tarification séduisante.

Laissez-le à `0` pour appliquer la tarification séduisante à tous les prix.

## Prix de vente

Par défaut, la tarification séduisante s'applique aux prix réguliers et aux prix de vente. Si vous souhaitez que vos prix de vente affichent leurs valeurs calculées exactes (utile pour les prix promotionnels limités dans le temps où les chiffres exacts comptent), décochez **Appliquer aux prix de vente**.

## Désactiver une règle

Pour arrêter temporairement la tarification séduisante sans supprimer la règle, décochez **Actif** et enregistrez. La règle est conservée et peut être réactivée à tout moment.

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- Commencez par des finales en .99 si vous n'êtes pas sûr — c'est la technique de tarification psychologique la plus reconnue et fonctionne bien pour la plupart des types de produits.
- Fixez un seuil minimum si vous vendez des articles à faible coût (moins de 5 $) afin qu'un article à 3,50 $ ne descende pas jusqu'à 2,99 $.
- Vérifiez vos prix après avoir activé une nouvelle règle en consultant un produit sur le site de vente — les prix charmés s'affichent en temps réel.
- Le Yen japonais et les monnaies à nombres entiers similaires fonctionnent le mieux avec **Arrondir au plus proche 10** ou **Arrondir au plus proche 100**, car les finales décimales semblent inhabituelles.
- Le tarif charmé est appliqué après toutes les remises et promotions, donc vos prix de vente apparaîtront également charmés à moins que vous ne décochiez **Appliquer aux prix de vente**.
- Vous pouvez avoir différents types de règles pour différentes monnaies, ce qui est utile si vous vendez dans plusieurs marchés avec des conventions de tarification différentes.