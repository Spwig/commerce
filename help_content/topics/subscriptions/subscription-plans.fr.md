---
title: Abonnements
---

Les forfaits d'abonnement vous permettent d'offrir une facturation récurrente pour vos produits : idéal pour des consommables, des services, des colis personnalisés ou tout autre produit que les clients achètent régulièrement. Ce guide explique comment créer et configurer des forfaits, définir des tranches de prix, ajouter des périodes d'essai et attacher des accessoires optionnels.

## Premiers pas

Accédez à **Abonnements > Forfaits d'abonnement** dans la barre latérale d'administration. La liste des forfaits affiche tous vos forfaits avec leur modèle de tarification, le nombre d'abonnés actifs et leur statut de visibilité.

Pour créer un nouveau forfait, cliquez sur le bouton **+ Ajouter un forfait d'abonnement** - cela ouvre l'assistant de création de forfait, qui vous guide étape par étape.

![Liste des forfaits d'abonnement](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Un forfait seul n'est pas achetable - c'est un modèle. Une fois que vous l'avez créé ici, attachez-le à un ou plusieurs produits depuis l'onglet **Abonnements** du produit (seulement les produits simples, variables et numériques), afin que les clients puissent effectivement s'abonner. Consultez [Vendre des produits en tant qu'abonnements](/help/selling-products-as-subscriptions) pour cette étape.

## Informations sur le forfait

La première section capture l'identité principale de votre forfait.

- **Nom du forfait** - Le nom que les clients voient lors de leur abonnement. Cliquez sur l'icône du globe pour ajouter des traductions pour d'autres langues de magasin.
- **Slug** - Un identifiant convivial pour les URL généré automatiquement à partir du nom (par exemple, `forfait-premium`). Cela est utilisé en interne et dans les intégrations.
- **Description** - Texte optionnel décrivant ce que comprend le forfait. Prend en charge les traductions.

## Modèle de tarification

Choisissez comment la tarification est structurée pour ce forfait :

| Modèle de tarification | Idéal pour |
|----------------------|------------|
| **Tarification par tranches** | Offrir des options de engagement mensuel, trimestriel et annuel avec des remises pour des périodes plus longues |
| **Tarification par quantité** | Tarification par siège ou par utilisateur, où le total augmente avec la quantité (par exemple, licences d'équipe) |
| **Tarif fixe** | Un prix fixe unique sans variations |

Pour les forfaits à **Tarification par quantité**, définissez la **Quantité minimale** (nombre minimal de sièges requis) et éventuellement une **Quantité maximale** pour fixer un plafond sur le nombre de sièges qu'un abonné peut acheter.

## Tranches de tarification

Les tranches de tarification définissent la fréquence de facturation et les options de remise disponibles pour les clients sur ce forfait. Ajoutez-les dans la section **Tranches de tarification** ci-dessous le formulaire principal.

Chaque tranche comporte les champs suivants :

- **Nom de la tranche** - La légende affichée aux clients (par exemple, `Mensuel`, `Annuel - Économisez 20 %`). Prend en charge les traductions.
- **Cycle de facturation** - La fréquence à laquelle le client est facturé : quotidien, hebdomadaire, mensuel, trimestriel, semestriel ou annuel.
- **Intervalle de facturation** - Le multiplicateur pour le cycle de facturation. Définissez-le sur `2` avec le mensuel pour facturer tous les 2 mois.
- **Pourcentage de remise** - La remise appliquée au prix du produit pour cette tranche. Définissez sur `0` pour le prix plein, ou sur `20` pour une remise de 20 %. Cette remise s'ajoute à tout prix de vente sur le produit lui-même.
- **Tranche par défaut** - Cochez une tranche comme par défaut pour la sélectionner automatiquement pour les clients lorsqu'ils consultent les options d'abonnement.

La remise s'applique dès le premier cycle de facturation du client, et non seulement lors des renouvellements - une tranche avec une remise de 20 % facture 20 % de moins dès le premier jour (ou dès la première facture après une période d'essai, si le forfait en comporte un).

### Exemple : forfait par tranches avec trois options

Pour un forfait d'abonnement "Café Club" : 

| Nom de la tranche | Cycle de facturation | Remise |
|------------------|---------------------|--------|
| Mensuel | Mensuel | 0 % |
| Trimestriel - Économisez 10 % | Trimestriel | 10 % |
| Annuel - Économisez 20 % | Annuel | 20 % |

## Période d'essai

Une période d'essai permet aux clients d'essayer votre abonnement avant leur première facture complète. Configurez cela dans la section **Période d'essai** : 

- **Durée de la période d'essai (jours)** - Nombre de jours d'essai gratuits. Définissez sur `0` pour désactiver les essais. La limite est de 365 jours.
- **Prix d'essai** - Prix réduit optionnel pendant l'essai (par exemple, 1 $ pour le premier mois). Laissez vide pour un essai totalement gratuit.

## Politique de désistement

Contrôlez comment les clients peuvent annuler leur abonnement dans la section **Politique de désistement** :

| Policy | Description |
|--------|-------------|
| **Annulation à tout moment** | Les clients peuvent annuler immédiatement à tout moment |
| **Annulation à la fin de la période** | L'annulation prend effet à la fin de la période payante — les clients conservent l'accès jusqu'à expiration |
| **Engagement minimum requis** | Les clients doivent accomplir un nombre minimum de cycles de facturation avant d'annuler |

Paramètres supplémentaires :

- **Engagement minimum (cycles)** — Lors de l'utilisation de la politique d'engagement, définissez le nombre requis de cycles de facturation (par exemple, `3` pour un engagement de 3 mois).
- **Période de grâce (jours)** — Jours d'accès continu après un échec de paiement avant que l'abonnement ne soit suspendu. Définissez sur `0` pour une suspension immédiate.
- **Période de réactivation (jours)** — Jours après l'annulation pendant lesquels un client peut réactiver son abonnement sans devoir s'abonner à nouveau depuis le début.

## Comportement de changement de forfait

Lorsque les clients passent d'un forfait à un autre, vous pouvez contrôler à quel moment le changement prend effet :

- **Comportement de mise à niveau** — Définissez sur **Immédiat** (facturer un montant proportionnel maintenant) ou **À la rénovation** (passer à la date de facturation suivante).
- **Comportement de désactivation** — Définissez sur **Immédiat** (appliquer un crédit sur la prochaine facture) ou **À la rénovation** (passer à la date de facturation suivante).

## Limites et restrictions

- **Nombre maximum de cycles de facturation** — Le nombre total de cycles de facturation avant que l'abonnement ne se termine automatiquement. Laissez vide pour une facturation récurrente illimitée. Utile pour les plans de paiement par versements ou les abonnements limités dans le temps.
- **Frais de mise en place** — Une charge unique perçue lors de la création initiale de l'abonnement (par exemple, frais d'inscription ou d'activation). Définissez sur `0.00` pour aucun frais de mise en place.

## Accessoires de forfait

Les accessoires sont des options supplémentaires que les abonnés peuvent ajouter à leur forfait. Ajoutez-les dans la section **Accessoires de forfait** :

- **Nom de l'accessoire** — Le nom affiché aux clients. Prend en charge les traductions.
- **Description** — Ce que l'accessoire fournit.
- **Prix** — Coût de l'accessoire.
- **Fréquence de facturation** — Indiquez si l'accessoire est facturé **Par cycle de facturation** (récurrent) ou **Une fois** au début de l'abonnement.
- **Autoriser la quantité** — Activez pour permettre aux clients d'acheter plusieurs unités de l'accessoire.
- **Obligatoire** — Cochez cette case pour inclure automatiquement l'accessoire sur tous les nouveaux abonnements. Les accessoires obligatoires ne peuvent pas être supprimés par le client.

## Visibilité et statut

- **Actif** — Décochez pour désactiver un forfait afin qu'aucun nouvel abonnement ne puisse être créé. Les abonnements existants ne sont pas affectés.
- **Public** — Décochez pour cacher le forfait des pages visibles par les clients (utile pour les anciens forfaits internes ou obsolètes dont les abonnés existants y restent).
- **Ordre de tri** — Contrôle l'ordre d'affichage sur les pages de sélection d'abonnement. Les numéros plus bas s'affichent en premier.

## Conseils

- Utilisez une **période d'essai** pour réduire l'hésitation — même un essai gratuit de 7 jours court peut améliorer significativement les taux de conversion pour les produits d'abonnement.
- Configurez **trois niveaux de prix** (mensuel, trimestriel, annuel) avec des remises croissantes pour encourager les engagements annuels et améliorer votre trésorerie.
- Pour les abonnements de services, définissez **la politique de désactivation** sur **Annulation à la fin de la période** afin que les clients conservent l'accès pendant leur période payante — cela semble juste et réduit les réclamations.
- Gardez la **période de grâce** à 3 à 7 jours pour les échecs de paiement. Cela donne aux clients le temps de mettre à jour leur mode de paiement avant de perdre l'accès.
- Utilisez l'indicateur **Obligatoire** sur les accessoires avec modération — n'utilisez-le que pour les éléments qui sont vraiment obligatoires (par exemple, un accord de service), et non comme moyen d'augmenter les prix.
- Désactivez les forfaits sans abonnés plutôt que de les supprimer — cela préserve les données historiques pour tout client ayant autrefois souscrit.