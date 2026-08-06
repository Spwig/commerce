---
title: Régions de vente
---

Les régions de vente vous permettent de définir des marchés géographiques pour votre magasin et de contrôler quels produits sont disponibles dans chaque région. Cela est utile lorsque vous vendez dans plusieurs pays ou territoires et que vous avez besoin de catalogues de produits différents, de devises régionales ou de disponibilité du stock par emplacement.

## Qu'est-ce qu'une région de vente ?

Une région de vente est une zone géographique nommée composée d'un ou plusieurs pays. Chaque région a une devise par défaut, une priorité et peut être liée à un ou plusieurs entrepôts. Lorsqu'un client parcourt votre magasin, Spwig détermine leur région en fonction de leur emplacement et applique la devise appropriée et les règles de visibilité des produits.

Cas d'utilisation courants:
- Afficher uniquement les produits disponibles localement aux clients de chaque pays
- Attribuer des devises par défaut spécifiques à la région (par exemple, NZD pour les clients de la Nouvelle-Zélande)
- Contrôler quels entrepôts effectuent les commandes pour chaque région
- Masquer les produits qui ne sont pas encore disponibles sur certains marchés

## Création d'une région de vente

1. Accédez à **Inventaire > Régions de vente**. Si vous ne la voyez pas, activez **Activer plusieurs entrepôts** sous **Paramètres > Paramètres du magasin > E-commerce** pour afficher l'élément de menu — vous n'avez pas besoin d'utiliser réellement plusieurs entrepôts pour cela, cela ne déverrouille que le lien. Vous pouvez également accéder directement à `/admin/catalog/salesregion/`.
2. Cliquez sur **+ Ajouter une région de vente**
3. Remplissez les détails de la région:

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Nom de la région** | Nom d'affichage de cette région | `Asie-Pacifique` |
| **Code de la région** | Identifiant unique court | `APAC` |
| **Pays** | Codes ISO des pays inclus dans cette région | `["NZ", "AU", "SG", "FJ"]` |
| **Devise par défaut** | Code ISO de la devise pour cette région | `NZD` |
| **Priorité** | Les régions à priorité plus élevée sont sélectionnées en premier | `10` |
| **Active** | Si cette région est actuellement utilisée | Coché |

4. Cliquez sur **Enregistrer**

### Codes des pays

Entrez les pays sous forme de liste JSON de codes à deux lettres. Par exemple:
- Nouvelle-Zélande et Australie: `["NZ", "AU"]`
- Une seule Singapour: `["SG"]`
- L'ensemble de l'Europe: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorité

Si le pays d'un client correspond à plus d'une région, la région avec le plus haut numéro de priorité est utilisée. Donnez une priorité plus élevée aux régions plus spécifiques (par exemple, donnez à `NZ` une priorité de 20 et à `APAC` une priorité de 10 afin que les clients de la Nouvelle-Zélande soient d'abord associés à la région `NZ`).

## Contrôle de la visibilité des produits par région

Par défaut, chaque produit est visible dans toutes les régions. Pour restreindre un produit, ouvrez-le sous **Produits > Tous les produits** et définissez le champ **Disponibilité des régions** (dans la section Statut) sur l'autorisation d'être uniquement dans des régions spécifiques ou dans toutes les régions sauf des régions spécifiques, puis sélectionnez les régions dans le tableau ci-dessous ce champ.

Cela détermine également ce que voient les acheteurs en dehors des régions disponibles pour un produit — s'il est masqué des listes entièrement, ou s'il est affiché avec un avertissement « Ne livre pas vers [région] ». Consultez le guide **Disponibilité des régions** pour obtenir la procédure complète, y compris ce paramètre d'affichage et le sélecteur de livraison du magasin.

## Devise régionale

Chaque région a une devise par défaut. Si votre magasin prend en charge explicitement plus d'une devise (**Paramètres > Multi-devises**), la devise affichée par le client passe à la devise par défaut de leur région dès que leur région change — qu'il s'agisse d'une invite de région automatique ou du sélecteur de livraison. Les magasins n'ayant qu'une seule devise, ou n'ayant pas délibérément activé le multi-devises, affichent toujours cette seule devise, quel que soit la région.

Pour configurer des prix dans plusieurs devises, configurez les taux de change sous **Paramètres > Taux de change**. Les prix peuvent être convertis automatiquement ou définis manuellement par devise.

## Lier des entrepôts aux régions

Les entrepôts sont liés aux régions lorsque vous créez ou modifiez un entrepôt sous **Catalogue > Entrepôts**. Chaque entrepôt appartient à une région, ce qui détermine quelle stock de région est utilisé pour effectuer les commandes.

Pour plus de détails sur les entrepôts, voir le sujet d'aide **Inventaire et entrepôts**.

## Astuces

- Gardez les codes régionaux courts et descriptifs (NZ, APAC, EU, US) - ils sont utilisés en interne et dans les journaux.
- Utilisez des numéros de priorité plus élevés pour les régions plus petites et plus spécifiques afin qu'elles prennent le pas sur les régions plus larges.
- Si vous ne vendez qu'en une seule région, vous n'avez pas besoin de configurer de régions du tout - Spwig fonctionne parfaitement avec un seul catalogue mondial.
- Ne définissez la **Disponibilité des régions** d'un produit qu'à partir de **Disponible dans toutes les régions** que lorsque vous avez réellement besoin de la restreindre - la valeur par défaut rend les produits universellement disponibles sans entretien.
- Revoyez les règles de région de chaque produit chaque fois que vous ajoutez une nouvelle région de vente, afin que les restrictions correspondent toujours à ce que vous souhaitez.
- Ajoutez le sélecteur de destination à votre en-tête (voir le guide **Disponibilité des régions**) afin que vous puissiez basculer les régions vous-même et vérifier que les produits restreints se comportent comme prévu.