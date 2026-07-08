---
title: Régions de vente
---

Les régions de vente vous permettent de définir des marchés géographiques pour votre magasin et de contrôler quels produits sont disponibles dans chaque région. Cela est utile lorsque vous vendez dans plusieurs pays ou territoires et que vous avez besoin de catalogues de produits différents, de devises régionales ou de disponibilité d'inventaire par emplacement.

## Qu'est-ce qu'une région de vente ?

Une région de vente est une zone géographique nommée composée d'un ou plusieurs pays. Chaque région a une devise par défaut, une priorité, et peut être liée à un ou plusieurs entrepôts. Lorsqu'un client navigue dans votre magasin, Spwig détermine sa région en fonction de son emplacement et applique les règles de devise et de visibilité des produits appropriées.

Cas d'utilisation courants:
- Afficher uniquement les produits disponibles localement aux clients de chaque pays
- Affecter des devises par défaut spécifiques à une région (par exemple, NZD pour les clients de Nouvelle-Zélande)
- Contrôler quels entrepôts traitent les commandes pour chaque région
- Cacher les produits non encore disponibles sur certains marchés

## Créer une région de vente

1. Accédez à **Catalogue > Régions de vente**
2. Cliquez sur **+ Ajouter une région de vente**
3. Remplissez les détails de la région:

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Nom de la région** | Nom d'affichage pour cette région | `Asia-Pacific` |
| **Code de la région** | Identifiant unique court | `APAC` |
| **Pays** | Codes ISO des pays inclus dans cette région | `["NZ", "AU", "SG", "FJ"]` |
| **Devise par défaut** | Code ISO de la devise pour cette région | `NZD` |
| **Priorité** | Les régions avec une priorité plus élevée sont correspondantes en premier | `10` |
| **Actif** | Indique si cette région est actuellement utilisée | Coché |

4. Cliquez sur **Enregistrer**

### Codes de pays

Entrez les pays sous forme d'une liste JSON de codes ISO à deux lettres. Par exemple:
- Nouvelle-Zélande et Australie: `["NZ", "AU"]`
- Singapour uniquement: `["SG"]`
- Toute l'Europe: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorité

Si le pays d'un client correspond à plus d'une région, la région avec le numéro de priorité le plus élevé est utilisée. Affectez une priorité plus élevée aux régions plus spécifiques (par exemple, attribuez à `NZ` une priorité de 20 et à `APAC` une priorité de 10 afin que les clients de Nouvelle-Zélande soient d'abord associés à la région NZ).

## Contrôler la visibilité des produits par région

Par défaut, chaque produit est visible dans toutes les régions. Pour restreindre un produit à des régions spécifiques, utilisez des **enregistrements de visibilité des régions de produits**.

### Restreindre un produit à des régions spécifiques

1. Accédez à **Catalogue > Visibilité des régions de produits**
2. Cliquez sur **+ Ajouter une visibilité des régions de produits**
3. Sélectionnez le **produit**
4. Sélectionnez la **région**
5. Activez ou désactivez **Visible** selon vos besoins
6. Cliquez sur **Enregistrer**

Une fois qu'il existe un enregistrement de visibilité pour un produit, Spwig applique les règles. Les produits sans enregistrement de visibilité restent visibles partout.

### Schémas courants

**Limiter à une seule région**

Ajoutez un enregistrement de visibilité par région que vous souhaitez prendre en charge, en activant **Visible** sur `Oui` pour les régions autorisées. Les clients des autres régions ne verront pas le produit.

**Exclure d'une seule région**

Ajoutez un seul enregistrement de visibilité pour la région que vous souhaitez exclure et activez **Visible** sur `Non`. Le produit reste visible dans toutes les autres régions.

### Modifier la visibilité à partir de la page du produit

Vous pouvez également gérer la visibilité par région directement depuis le formulaire d'édition du produit. Dans la section **Visibilité par région** du produit, vous trouverez un tableau inline affichant toutes les régions et leurs paramètres de visibilité pour ce produit.

## Devise régionale

Chaque région a une devise par défaut. Les clients naviguant depuis cette région voient les prix affichés dans la devise de la région. La devise utilisée est déterminée à la caisse.

Pour configurer les prix en plusieurs devises, configurez les taux de change sous **Paramètres > Taux de change**. Les prix peuvent être convertis automatiquement ou définis manuellement par devise.

## Lier des entrepôts à des régions

Les entrepôts sont liés à des régions lors de la création ou de la modification d'un entrepôt sous **Catalogue > Entrepôts**. Chaque entrepôt appartient à une région, qui contrôle quelle stock de la région est utilisé pour traiter les commandes.

Pour plus de détails sur les entrepôts, consultez le sujet d'aide **Inventory and Warehouses**.

## Conseils

- Gardez les codes de région courts et descriptifs (`NZ`, `APAC`, `EU`, `US`) — ils sont utilisés internement et dans les journaux.
- Utilisez des numéros de priorité plus élevés pour des régions plus petites et plus spécifiques afin qu'elles prennent le pas sur les régions plus larges et plus générales.
- Si vous vendez uniquement dans un pays, vous n'avez pas besoin de configurer des régions du tout — Spwig fonctionne parfaitement avec un seul catalogue mondial.
- Testez la visibilité basée sur la région en prévisualisant votre magasin tout en filtrant par une région spécifique dans l'administration.
- Les enregistrements de visibilité des produits ne doivent être créés que si vous souhaitez restreindre les produits. Laisser un produit sans enregistrements de visibilité le rend disponible universellement.
- Vérifiez toujours vos règles de visibilité chaque fois que vous ajoutez une nouvelle région pour vous assurer que les restrictions des produits existantes sont correctes.