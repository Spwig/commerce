---
title: Réductions d'abonnement
---

Les réductions d'abonnement vous permettent d'appliquer des réductions de prix à des abonnements individuels de clients — par exemple, récompenser les abonnés fidèles, honorer un coupon promotionnel ou résoudre un litige de facturation avec un crédit de bonne volonté. Contrairement aux niveaux de tarification au niveau du plan, ces réductions sont appliquées directement à un abonnement spécifique.

## Affichage des réductions d'abonnement

Accédez à **Abonnements > Réductions d'abonnement** pour voir toutes les réductions actuellement appliquées à vos abonnements.

Chaque entrée affiche l'abonnement auquel elle appartient, le type et la valeur de la réduction, la durée de la réduction et si elle est toujours active.

Vous pouvez également trouver des réductions liées à un abonnement spécifique en ouvrant **Abonnements > Abonnements clients**, en cliquant sur un abonnement, puis en faisant défiler jusqu'à la section **Réductions** en bas de la page de détails.

## Ajout d'une réduction à un abonnement

Pour ajouter une nouvelle réduction :

1. Accédez à **Abonnements > Réductions d'abonnement**
2. Cliquez sur **+ Ajouter une réduction d'abonnement**
3. Sélectionnez l'**Abonnement** auquel vous souhaitez appliquer la réduction
4. Configurez les paramètres de la réduction (décrits ci-dessous)
5. Cliquez sur **Enregistrer**

La réduction prendra effet au prochain cycle de facturation.

## Types de réductions

Choisissez comment la réduction est calculée :

| Type de réduction | Fonctionnement | Exemple |
|-------------------|----------------|---------|
| **Pourcentage réduit** | Réduit la facture d'un pourcentage | `20` réduit une facture de 50 $ à 40 $ |
| **Montant fixe réduit** | Soustrait un montant fixe de la facture | `10` réduit une facture de 50 $ à 40 $ |
| **Prix fixe remplacé** | Fixe l'abonnement à un prix spécifique, indépendamment du prix normal du plan | `29` fixe la facture à 29 $/cycle |

Définissez le champ **Valeur de la réduction** sur le nombre correspondant à votre type choisi (pourcentage, montant en dollars ou prix fixe).

### Exemple : offre de fidélisation

Un client vous contacte pour annuler. Vous lui proposez 3 mois à 25 % de réduction pour rester :

| Champ | Valeur |
|-------|-------|
| Type de réduction | Pourcentage réduit |
| Valeur de la réduction | `25` |
| Type de durée | Répétitif |
| Durée (mois) | `3` |

## Durée de la réduction

Contrôlez la durée pendant laquelle la réduction s'applique aux cycles de facturation futurs :

| Type de durée | Quand s'applique |
|---------------|------------------|
| **Appliquer une seule fois** | Réduit uniquement le prochain cycle de facturation, puis expire automatiquement |
| **À toujours** | S'applique à chaque cycle de facturation futur jusqu'à ce qu'elle soit désactivée manuellement |
| **Répétitif** | S'applique pendant un nombre fixe de mois, puis expire |

Pour les réductions **Répétitives**, définissez le champ **Durée (mois)** sur le nombre de mois pendant lesquels la réduction doit durer. Le champ **Cycles restants** suit le nombre de cycles restants — il diminue à chaque cycle de facturation.

## Codes de coupon

Si la réduction a été déclenchée par un code de coupon promotionnel, entrez-le dans le champ **Code de coupon**. Cela est informatif — il enregistre quelles promotions ont déclenché la réduction pour votre propre suivi.

## Désactiver une réduction

Pour arrêter une réduction avant qu'elle n'expire naturellement, ouvrez le dossier de la réduction et décochez la case **Active**, puis enregistrez. La réduction ne s'appliquera plus aux cycles de facturation futurs. L'abonnement retournera à son prix normal du plan au prochain cycle de facturation.

Vous pouvez également définir une date **Expire à** lors de la création de la réduction — le système désactivera automatiquement la réduction après cette date.

## Conseils

- Utilisez les réductions **Appliquer une seule fois** pour des gestes de bonne volonté ponctuels (par exemple, compenser un abonné pour une interruption de service).

Elles sont propres et s'expireront automatiquement.
- Les réductions **Pourcentage réduit** sont plus sûres que les **Montant fixe réduit** pour les abonnements à prix variable, car la réduction s'adapte au montant de la facture réelle.
- Lorsque vous proposez une offre de fidélisation, utilisez **Répétitif** avec une durée de 3 mois — cela donne aux clients une raison de rester sans réduire définitivement vos revenus.
- Gardez le champ **Code de coupon** cohérent avec le code utilisé par les clients.

# Faciliter l'audit des promotions

Cela facilite l'audit des promotions qui ont entraîné quelles réductions lors de la revue de votre revenu abonnement.
- Les réductions s'appliquent à des abonnements individuels, et non aux plans.

Si vous souhaitez réduire le prix d'un plan pour tous les nouveaux abonnés, mettez à jour les niveaux tarifaires du plan au lieu de cela.