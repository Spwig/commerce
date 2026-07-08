---
title: Cartes cadeaux multidevise
---

Si vous vendez à des clients dans plusieurs pays, vous pouvez émettre des cartes cadeaux dans des devises spécifiques. Par exemple, un client de Nouvelle-Zélande peut acheter une carte cadeaux de 50 $ NZD et le bénéficiaire la réclame en NZD — la valeur nominale reste la même, indépendamment des fluctuations des taux de change.

Cette fonctionnalité nécessite que la multidevise soit activée avec au moins un fournisseur de taux de change configuré.

## Fonctionnement

Lorsque vous définissez une **Devise de carte cadeau** sur un produit de carte cadeau, le système convertit le prix du produit en devise cible au moment de l'achat, en utilisant le taux de change actuel. La carte cadeau résultante est dénommée en cette devise et ne peut être réclamée que par des clients achetant dans la même devise.

| Étape | Ce qui se produit |
|------|-------------|
| **Configuration du produit** | Vous définissez le prix du produit de carte cadeau en devise de base et choisissez une devise cible (par exemple, NZD) |
| **Achat** | Un client achète la carte cadeau. Le prix de base est converti en NZD au taux de change actuel |
| **Carte cadeau créée** | La carte cadeau est émise avec sa valeur en NZD (par exemple, NZ$78,50) |
| **Réclamation** | Le bénéficiaire applique le code à la caisse tout en achetant en NZD. Le solde en NZD est déduit |

## Prérequis

Avant de configurer des cartes cadeaux multidevise, assurez-vous d'avoir :

1. **Multidevise activée** — Allez à **Paramètres > Paramètres du magasin** et activez le support multidevise
2. **Devises prises en charge configurées** — Ajoutez les devises que vous souhaitez proposer (par exemple, NZD, SGD, EUR)
3. **Fournisseur de taux de change connecté** — Allez à **Paramètres > Taux de change** et configurez un fournisseur afin que les taux en direct soient disponibles

## Configuration d'un produit de carte cadeau multidevise

### Étape 1 : Créer ou modifier un produit de carte cadeau

1. Accédez à **Produits > Tous les produits**
2. Cliquez sur **+ Ajouter un produit** ou ouvrez un produit de carte cadeau existant
3. Définissez **Type de produit** sur **Carte cadeau**

### Étape 2 : Définir la devise de la carte cadeau

1. Cliquez sur l'onglet **Carte cadeau**
2. Configurez vos paramètres de dénomination comme d'habitude (montants fixes, montants personnalisés ou les deux)
3. En bas de l'onglet Carte cadeau, trouvez le menu déroulant **Devise de carte cadeau**
4. Sélectionnez la devise cible (par exemple, **NZD - Dollar néo-zélandais**)
5. Enregistrez le produit

Le menu déroulant affiche toutes les devises activées dans les paramètres de votre magasin. Sélectionner **Devise de base du magasin (par défaut)** signifie que les cartes cadeaux seront émises en devise de base — c'est le comportement standard.

### Étape 3 : Définir le prix

Définissez le prix du produit en devise de base comme vous le feriez normalement. Lorsqu'un client achète cette carte cadeau, le prix est automatiquement converti en devise cible en utilisant le taux de change actuel.

**Exemple :** Votre devise de base est USD. Vous créez un produit de carte cadeau au prix de 50 $ USD avec la devise de carte cadeau définie sur NZD. Si le taux de change est de 1 USD = 1,57 NZD, la carte cadeau résultante aura une valeur de NZ$78,50.

## Correspondance de devise et réclamation

Les cartes cadeaux multidevise utilisent la **réclamation en même devise** — la devise active d'achat du client doit correspondre à la devise de la carte cadeau.

### Ce que les clients vivent

- Un client achetant en **NZD** peut appliquer une carte cadeau NZD à la caisse
- Un client achetant en **USD** ne peut pas appliquer une carte cadeau NZD — ils verront un message expliquant le désaccord de devise
- Les clients peuvent changer leur devise d'achat en utilisant le sélecteur de devise sur votre boutique avant d'appliquer la carte cadeau

### Comment le solde fonctionne

Le solde de la carte cadeau est toujours suivi en devise native : 

- Une carte cadeau NZ$78,50 commence avec un solde de NZ$78,50
- Si un client effectue un achat de NZ$30, le solde restant est de NZ$48,50
- Le solde ne fluctue pas avec les taux de change — la valeur nominale est fixe

Lorsque la carte cadeau est appliquée à la caisse, le système convertit le rabais en devise de base du magasin internement pour les calculs de commande, mais le solde de la carte cadeau est toujours déduit en devise native.

## Gestion des cartes cadeaux multidevise

Accédez à **Produits > Cartes cadeaux** pour consulter toutes les cartes cadeaux émises. Les cartes cadeaux multidevise s'affichent avec leur devise native : 

- **Solde** affiche en devise de la carte cadeau (par exemple, NZ$48,50)
- **Transactions** enregistrent les montants en devise de la carte cadeau
- **Valeur initiale** affiche le montant converti au moment de l'achat

### Vérification des détails des taux de change

Chaque transaction de carte cadeau enregistre le taux de change utilisé au moment de la transaction. Cela fournit une trace complète des opérations pour les besoins comptables.

## Exemples

### Exemple 1 : Carte cadeau régionale pour la Nouvelle-Zélande

**Scénario :** Vous opérez depuis les États-Unis mais avez des clients en Nouvelle-Zélande. Vous souhaitez vendre des cartes cadeaux dénommées en NZD.

| Paramètre | Valeur |
|---------|-------|
| Nom du produit | Carte cadeau NZ |
| Type de produit | Carte cadeau |
| Prix | 50,00 $ (USD — votre devise de base) |
| Type de dénomination | Dénominations fixes |
| Dénominations fixes | 25, 50, 100, 200 |
| Devise de carte cadeau | NZD - Dollar néo-zélandais |
| Date d'expiration | 365 jours |

Lorsqu'un client sélectionne la dénomination de 50 $ : 
- Le système convertit 50 $ USD en NZD au taux actuel
- Une carte cadeau est créée avec l'équivalent en NZD (par exemple, NZ$78,50)
- Le bénéficiaire peut la réclamer en achetant en NZD

### Exemple 2 : Cartes cadeaux en plusieurs devises

**Scénario :** Vous vendez à des clients en Singapour, en Australie et au Royaume-Uni. Créez trois produits de carte cadeau : 

1. **Carte cadeau SG** — Devise de carte cadeau : SGD
2. **Carte cadeau AU** — Devise de carte cadeau : AUD
3. **Carte cadeau UK** — Devise de carte cadeau : GBP

Chaque produit convertit votre prix de base en devise cible au moment de l'achat. Les clients de chaque région peuvent réclamer la carte cadeau en devise locale.

### Exemple 3 : Offre mixte de cartes cadeaux

**Scénario :** Vous souhaitez proposer à la fois des cartes cadeaux en devise de base et des cartes cadeaux régionales.

- **Carte cadeau du magasin** — Devise de carte cadeau : *Devise de base du magasin (par défaut)* — réclamable en devise de base
- **Carte cadeau NZ** — Devise de carte cadeau : NZD — réclamable uniquement en NZD

Les deux produits peuvent coexister dans votre catalogue. Les clients voient dans quelle devise une carte cadeau est dénommée lorsqu'ils vérifient le solde.

## Conseils

- Commencez par une seule devise régionale et testez le flux complet (achat, livraison, réclamation) avant d'ajouter d'autres devises.
- Le taux de change au moment de l'achat détermine la valeur de la carte cadeau. Si les taux changent significativement, la valeur de la carte cadeau reste fixe — cela protège à la fois vous et vos clients.
- Faites en sorte que la devise soit claire dans le nom du produit (par exemple, "Carte cadeau NZ" ou "Carte cadeau (NZD)") afin que les clients sachent ce qu'ils achètent.
- Les cartes cadeaux sans devise définie continuent de fonctionner exactement comme avant en devise de base — les produits existants ne sont pas affectés.
- Surveillez votre fournisseur de taux de change pour vous assurer que les taux sont à jour. Des taux obsolètes pourraient entraîner des cartes cadeaux surévaluées ou sous-évaluées.
- Réfléchissez soigneusement à vos dénominations. Une dénomination de 25 $ USD se convertit approximativement en NZ$39 — les dénominations arrondies en devise cible peuvent sembler meilleures. Vous pouvez créer des produits séparés avec des dénominations qui sont des nombres arrondis en devise cible.