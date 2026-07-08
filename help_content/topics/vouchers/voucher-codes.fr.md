---
title: Codes de bon d'achat
---

Les codes de bon d'achat vous permettent de créer des codes de réduction, des coupons et des cartes cadeaux que les clients entrent à la caisse pour obtenir une réduction. Accédez à **Marketing > Vouchers** dans le menu latéral de l'admin.

![Liste des vouchers](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Tableau de bord des vouchers

La page des vouchers affiche un aperçu avec :

- **Cartes de statistiques** — Comptes de vouchers actifs, inactifs, utilisés et totaux
- **Filtres** — Recherche par code ou nom, filtre par Type, Statut et Portée
- **Cartes de vouchers** — Chaque voucher affiché avec des détails d'utilisation et de statut

## Créer un voucher

1. Cliquez sur **+ Ajouter un voucher** en haut à droite
2. Remplissez les détails du voucher :
   - **Code** — Le code que les clients entrent à la caisse (ex. : "SAVE20", "FREESHIP")
   - **Nom/Description** — Description interne pour votre référence
   - **Type de réduction** — Choisissez comment la réduction est appliquée
   - **Valeur de réduction** — Le montant ou le pourcentage de réduction
3. Configurez les règles d'utilisation :
   - **Limite d'utilisation** — Nombre maximum total d'utilisations (0 = illimité)
   - **Limite par client** — Nombre maximum d'utilisations par client
   - **Valeur minimale de commande** — Valeur minimale du panier requise
4. Définissez la **portée** :
   - **Tout le panier** — La réduction s'applique à l'ensemble de la commande
   - **Produits spécifiques** — S'applique uniquement aux articles sélectionnés
   - **Catégories spécifiques** — S'applique uniquement aux articles des catégories sélectionnées
5. Définissez éventuellement une date d'expiration :
   - **Date d'expiration** — Date à laquelle le voucher cesse de fonctionner
6. Cliquez sur **Enregistrer**

## Types de vouchers

| Type | Description | Exemple |
|------|-------------|---------|
| **Montant fixe** | Soustrait un montant fixe en dollars | 20 $ de réduction sur la commande |
| **Pourcentage** | Soustrait un pourcentage du total | 15 % de réduction sur la commande |
| **Livraison gratuite** | Supprime les frais de livraison | Livraison gratuite sur toute commande |

## Gestion des vouchers

### Cartes de vouchers

Chaque carte de voucher affiche :
- **Code** — Le code du voucher en gras
- **Description** — Ce que fait le voucher
- **Étiquette de statut** — Actif ou Inactif
- **Détails de la réduction** — Type et valeur (ex. : "$ 20.00" ou "15.00%")
- **Portée** — Si elle s'applique à tout le panier ou à des articles spécifiques
- **Compteur d'utilisation** — Le nombre de fois où le voucher a été utilisé
- **Date de création** — Lorsque le voucher a été créé
- **Expiration** — Date d'expiration ou "Aucune expiration"

### Actions sur les vouchers

Chaque carte dispose de boutons d'actions :
- **Modifier** — Modifier les paramètres du voucher
- **Voir l'historique** — Voir l'historique des utilisations
- **Supprimer** — Supprimer le voucher

### Filtre des vouchers

Utilisez la barre de filtre pour trouver des vouchers spécifiques :
- **Recherche** — Trouver par code, nom ou description
- **Type** — Montant fixe, Pourcentage ou Livraison gratuite
- **Statut** — Actif ou Inactif
- **Portée** — Tout le panier ou articles spécifiques

## Génération de vouchers en masse

Pour des campagnes importantes, vous pouvez générer des vouchers en masse :
1. Le système génère automatiquement des codes uniques (ex. : "COUPONX1600406498")
2. Définissez des paramètres communs pour tous les vouchers générés
3. Distribuez les codes par e-mail, réseaux sociaux ou impression

## Expérience client

Lorsqu'un client a un code de voucher :
1. Ils passent à **la caisse**
2. Ils entrent le code dans le **champ de code de réduction**
3. La réduction est appliquée immédiatement si le voucher est valide
4. Le résumé de la commande est mis à jour pour afficher la réduction

Si un voucher est invalide (expiré, limite d'utilisation atteinte, valeur minimale non atteinte), le client voit un message d'erreur clair.

## Conseils

- Utilisez des codes mémorables pour les campagnes de marketing (ex. : "SUMMER20" au lieu de chaînes aléatoires).
- Définissez des limites par client pour empêcher l'abus de réductions précieuses.
- Utilisez des valeurs minimales de commande pour maintenir la rentabilité (ex. : "20 $ de réduction sur les commandes supérieures à 50 $").
- Suivez le compteur de réductions sur le tableau de bord pour mesurer l'efficacité des campagnes.
- Créez des vouchers limités dans le temps pour créer de l'urgence (ex. : "Valide uniquement ce week-end").
- Utilisez l'état Actif/Inactif pour suspendre les vouchers sans les supprimer.