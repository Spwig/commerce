---
title: "Lots de Produits"
---

Les lots de produits vous permettent de vendre des ensembles pre-assembles de produits a un prix groupe. C'est parfait pour les coffrets cadeaux, les kits de demarrage ou toute combinaison de produits que vous souhaitez proposer ensemble avec une remise.

![Bundle components admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Strategies de Tarification

Choisissez comment le prix du lot est calcule :

| Strategie | Description |
|-----------|-------------|
| **Prix Fixe** | Definissez un prix unique pour l'ensemble du lot, independamment des prix des composants. |
| **Remise en Pourcentage** | Calculez automatiquement le prix comme un pourcentage de reduction sur les prix combines des composants. |
| **Somme des Composants** | Le prix du lot est egal au total de tous les prix des composants (utile pour un affichage groupe sans remise). |

## Creation d'un Lot

### Etape 1 : Creer le Produit

1. Naviguez vers **Produits > Tous les Produits** et cliquez sur **+ Ajouter un Produit**
2. Definissez le **Type de Produit** sur **Lot de Produits**
3. Remplissez le nom du lot, la description et les images
4. Enregistrez le produit

### Etape 2 : Ajouter des Composants

Basculez vers l'onglet **Articles du Lot** pour ajouter des produits a votre lot :

1. Cliquez sur **+ Ajouter un Composant**
2. Recherchez et selectionnez un produit dans le menu deroulant
3. Definissez la **Quantite** pour chaque composant (ex., 2x masques faciaux dans un coffret soin)
4. Definissez l'**Ordre de Tri** pour controler l'ordre d'affichage
5. Marquez optionnellement un composant comme **Optionnel** (les clients peuvent l'exclure)
6. Si le composant est un produit a variantes, choisissez entre :
   - Une **variante fixe** — tous les clients recoivent la meme variante
   - **Permettre la selection de variante** — les clients choisissent leur variante preferee lors du paiement

Le resume en bas affiche le nombre de **Composants Totaux** et la **Valeur du Lot** (somme des prix des composants).

### Etape 3 : Configurer la Tarification

Basculez vers l'onglet **Tarification** :

1. Selectionnez votre **Strategie de Tarification du Lot**
2. Pour **Prix Fixe** — saisissez directement le prix du lot
3. Pour **Remise en Pourcentage** — definissez le pourcentage de remise (ex., 15% de reduction)
4. Pour **Somme des Composants** — le prix est calcule automatiquement

## Que Peut-on Inclure dans un Lot

| Type de Produit | Peut etre un Composant ? |
|----------------|------------------------|
| Produit Simple | Oui |
| Produit a Variantes | Oui (variante fixe ou choix du client) |
| Produit Numerique | Oui |
| Produit Personnalisable | Non |
| Produit Configurable | Non |
| Lot de Produits | Non (les lots ne peuvent pas etre imbriques) |
| Carte Cadeau | Non |

## Gestion des Stocks

Le stock du lot est gere a travers ses composants :

- **Tous les composants doivent etre en stock** pour que le lot soit achetable
- Lorsqu'un lot est commande, le stock est deduit de chaque produit composant individuellement
- Si un composant est en rupture de stock, le lot devient indisponible
- Les niveaux de stock des composants sont verifies en temps reel lors du paiement

## Composants Optionnels

Marquez un composant comme **Optionnel** pour permettre aux clients de personnaliser leur lot :

- Les composants optionnels sont inclus par defaut mais peuvent etre retires par le client
- Le prix du lot s'ajuste en consequence lorsque des composants optionnels sont exclus
- Au moins un composant doit etre non optionnel (obligatoire)

## Experience Client

Lorsqu'un client consulte un lot sur votre vitrine :

1. **Liste des Composants** — Tous les produits inclus sont affiches avec images et quantites
2. **Economies du Lot** — La remise par rapport a l'achat des articles individuellement est affichee
3. **Selection de Variante** — Pour les composants avec selection de variante activee, les clients choisissent leur option preferee
4. **Articles Optionnels** — Les clients peuvent activer ou desactiver les composants optionnels
5. **Ajout au Panier Unique** — L'ensemble du lot est ajoute comme un seul article

## Conseils

- Utilisez la strategie de Remise en Pourcentage pour la plus grande flexibilite tarifaire — elle s'ajuste automatiquement lorsque les prix des composants changent.
- Mettez en evidence le montant des economies dans la description du produit pour encourager les achats de lots.
- Limitez les lots a 3-5 composants pour la meilleure experience client. Trop d'articles peuvent sembler ecrasants.
- Utilisez les composants optionnels pour offrir une version "de base" et "premium" du meme lot.
- Verifiez regulierement que tous les produits composants sont toujours actifs et en stock.
