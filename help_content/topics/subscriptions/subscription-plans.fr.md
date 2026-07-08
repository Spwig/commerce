---
title: Plans d'abonnement
---

Les plans d'abonnement vous permettent d'offrir un paiement récurrent pour vos produits — idéal pour les produits consommables, les services, les coffrets personnalisés ou tout produit que les clients achètent régulièrement. Ce guide explique comment créer et configurer des plans, définir des niveaux tarifaires, ajouter des périodes d'essai et attacher des options supplémentaires facultatives.

## Démarrage

Accédez à **Abonnements > Plans d'abonnement** dans le menu latéral de l'administration. La liste des plans affiche tous vos plans avec leur modèle tarifaire, le nombre d'abonnés actifs et leur statut de visibilité.

Pour créer un nouveau plan, cliquez sur le bouton **+ Ajouter un plan d'abonnement** — cela ouvre l'assistant de création de plan, qui vous guide pas à pas dans la configuration.

![Liste des plans d'abonnement](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Informations sur le plan

La première section capture l'identité principale de votre plan.

- **Nom du plan** — Le nom que les clients verront lors de leur abonnement. Cliquez sur l'icône de la Terre pour ajouter des traductions pour d'autres langues du magasin.
- **Slug** — Un identifiant convivial pour les URL généré automatiquement à partir du nom (ex. `premium-plan`). Il est utilisé internement et dans les intégrations.
- **Description** — Texte optionnel décrivant ce que comprend le plan. Prend en charge les traductions.

## Modèle tarifaire

Choisissez comment le prix est structuré pour ce plan :

| Modèle tarifaire | Meilleur pour |
|------------------|---------------|
| **Tarification par palier** | Proposer des options de engagement mensuel, trimestriel et annuel avec des réductions pour des durées plus longues |
| **Tarification par quantité** | Tarification par siège ou par utilisateur où le total s'adapte à la quantité (ex. licences d'équipe) |
| **Tarif fixe** | Un prix fixe unique sans variations |

Pour les plans **Tarification par quantité**, définissez la **Quantité minimale** (nombre minimum de sièges requis) et, le cas échéant, une **Quantité maximale** pour limiter le nombre de sièges qu'un abonné peut acheter.

## Paliers tarifaires

Les paliers tarifaires définissent la fréquence de facturation et les options de réduction disponibles pour les clients sur ce plan. Ajoutez-les dans la section **Paliers tarifaires** située en dessous du formulaire principal.

Chaque palier comporte ces champs :

- **Nom du palier** — L'étiquette affichée aux clients (ex. `Mensuel`, `Annuel — Économisez 20 %`). Prend en charge les traductions.
- **Cycle de facturation** — La fréquence à laquelle le client est facturé : quotidien, hebdomadaire, mensuel, trimestriel, semestriel ou annuel.
- **Intervalle de facturation** — Le multiplicateur du cycle de facturation. Définissez à `2` avec Mensuel pour facturer toutes les 2 mois.
- **Pourcentage de réduction** — La réduction appliquée au prix du produit pour ce palier. Définissez à `0` pour le prix plein, ou `20` pour une réduction de 20 %. Cette réduction s'ajoute à toute réduction promotionnelle sur le produit lui-même.
- **Palier par défaut** — Marquez un palier comme par défaut pour le pré-sélectionner automatiquement aux clients lorsqu'ils consultent les options d'abonnement.

### Exemple : plan par palier avec trois options

Pour un plan d'abonnement "Club Café" :

| Nom du palier | Cycle de facturation | Réduction |
|---------------|----------------------|----------|
| Mensuel | Mensuel | 0 % |
| Trimestriel — Économisez 10 % | Trimestriel | 10 % |
| Annuel — Économisez 20 % | Annuel | 20 % |

## Période d'essai

Une période d'essai permet aux clients d'essayer votre abonnement avant leur première facture complète. Configurez cela dans la section **Période d'essai** :

- **Période d'essai (jours)** — Nombre de jours d'essai gratuits. Définissez à `0` pour désactiver les essais. Maximum de 365 jours.
- **Prix d'essai** — Prix réduit optionnel pendant la période d'essai (ex. 1 $ pour le premier mois). Laissez vide pour un essai totalement gratuit.

## Politique de résiliation

Contrôlez la manière dont les clients peuvent résilier leur abonnement dans la section **Politique de résiliation** :

| Politique | Description |
|----------|-------------|
| **Annuler à tout moment** | Les clients peuvent annuler immédiatement à tout moment |
| **Annuler à la fin du période** | La résiliation prend effet à la fin de la période payée — les clients conservent l'accès jusqu'à l'expiration |
| **Engagement minimum requis** | Les clients doivent terminer un nombre minimum de cycles de facturation avant de pouvoir annuler |

Paramètres supplémentaires :

- **Minimum Commitment (Cycles)** — Lors de l'utilisation de la politique d'engagement, définissez le nombre requis de cycles de facturation (par exemple, `3` pour un engagement minimum de 3 mois).
- **Grace Period (Days)** — Jours d'accès continu après un échec de paiement avant que l'abonnement ne soit suspendu.

Définir à `0` pour une suspension immédiate.
- **Reactivation Period (Days)** — Jours après l'annulation pendant lesquels un client peut réactiver son abonnement sans devoir s'abonner à nouveau depuis le début.

## Plan change behavior

Lorsque les clients passent d'un plan à un autre (upgrade ou downgrade), vous pouvez contrôler le moment où le changement prend effet :

- **Upgrade Behavior** — Définir sur **Immediate** (facturer un montant proratisé dès maintenant) ou **At Renewal** (passer au prochain date de facturation).
- **Downgrade Behavior** — Définir sur **Immediate** (appliquer un crédit à la prochaine facture) ou **At Renewal** (passer au prochain date de facturation).

## Limits and restrictions

- **Maximum Billing Cycles** — Le nombre total de cycles de facturation avant que l'abonnement ne se termine automatiquement. Laissez vide pour un facturation récurrente illimitée. Utile pour des plans en mensualités ou des abonnements à durée limitée.
- **Setup Fee** — Un frais unique facturé lors de la création initiale de l'abonnement (par exemple, frais d'inscription ou d'activation). Définir à `0.00` pour aucun frais d'installation.

## Plan add-ons

Les add-ons sont des extras optionnels que les abonnés peuvent ajouter à leur plan. Ajoutez-les dans la section **Plan Add-ons** :

- **Add-on Name** — Le nom affiché aux clients. Les traductions sont prises en charge.
- **Description** — Ce que l'add-on fournit.
- **Price** — Coût de l'add-on.
- **Billing Frequency** — Définir si l'add-on est facturé **Per Billing Cycle** (récurrence) ou **One-Time** à la création de l'abonnement.
- **Allow Quantity** — Activer pour permettre aux clients d'acheter plusieurs unités de l'add-on.
- **Required** — Cocher pour inclure automatiquement l'add-on à toutes les nouvelles abonnements. Les add-ons obligatoires ne peuvent pas être supprimés par le client.

## Visibility and status

- **Active** — Désactiver pour désactiver un plan afin qu'aucun nouveau abonnement ne puisse être créé. Les abonnements existants ne sont pas affectés.
- **Public** — Désactiver pour cacher le plan des pages destinées aux clients (utile pour des plans internes ou hérités que les abonnés existants continuent d'utiliser).
- **Sort Order** — Contrôle l'ordre d'affichage sur les pages de sélection d'abonnement. Les numéros plus bas apparaissent en premier.

## Tips

- Utilisez une **période d'essai** pour réduire les réticences — même une courte période d'essai gratuite de 7 jours peut considérablement améliorer les taux de conversion des produits abonnés.
- Configurez **trois niveaux de tarification** (mensuel, trimestriel, annuel) avec des remises croissantes pour encourager les engagements annuels et améliorer votre trésorerie.
- Pour les abonnements basés sur un service, définissez la **politique de résiliation** sur **Cancel at Period End** afin que les clients conservent l'accès pendant leur période payée — cela semble juste et réduit les remboursements.
- Gardez la **période de grâce** à 3 à 7 jours en cas d'échec de paiement. Cela donne aux clients le temps de mettre à jour leur méthode de paiement avant de perdre l'accès.
- Utilisez rarement le drapeau **Required** sur les add-ons — utilisez-le uniquement pour les choses qui sont véritablement obligatoires (par exemple, un accord de service), et non comme un moyen d'augmenter le prix.
- Désactivez les plans sans abonnés plutôt que de les supprimer — cela préserve les données historiques pour les clients qui ont précédemment souscrit.