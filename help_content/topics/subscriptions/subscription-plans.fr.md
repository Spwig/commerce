---
title: Abonnements
---

Les forfaits d'abonnement vous permettent d'offrir une facturation récurrente pour vos produits : idéal pour des consommables, des services, des colis personnalisés ou tout produit que les clients achètent régulièrement. Ce guide explique comment créer et configurer des forfaits, définir des tranches de prix, ajouter des périodes d'essai et attacher des accessoires optionnels.

## Premiers pas

Accédez à **Abonnements > Forfaits d'abonnement** dans la barre latérale d'administration. La liste des forfaits affiche tous vos forfaits avec leur modèle de tarification, le nombre d'abonnés actifs et leur statut de visibilité.

![Liste des forfaits d'abonnement](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Pour créer un nouveau forfait, cliquez sur le bouton **Créer avec le wizard** - cela ouvre le wizard de création de forfait, qui vous guide étape par étape. Le bouton **+ Ajouter un forfait** à côté ouvre un formulaire vide pour les commerçants qui souhaitent configurer tout par eux-mêmes.

Un forfait seul n'est pas achetable - c'est un modèle. Une fois que vous l'avez construit ici, attachez-le à un ou plusieurs produits depuis l'onglet **Abonnements** du produit (seulement les produits simples, variables et numériques), afin que les clients puissent s'abonner. Consultez [Vendre des produits en tant qu'abonnements](/help/selling-products-as-subscriptions) pour cette étape.

## L'éditeur de forfaits

Ouvrir un forfait existant (cliquez sur son nom, ou l'icône crayon, depuis la liste) vous amène à l'éditeur de forfait. En haut de l'en-tête, le nom du forfait, son modèle de tarification, les badges **Actif**/**Inactif** et **Public**/**Privé**, et la date de création. Les deux boutons en haut à droite de l'en-tête enregistrent vos modifications - l'icône cercle vert enregistre et retourne à la liste, l'icône cercle simple enregistre et vous maintient sur la page afin que vous puissiez continuer à éditer.

Sous l'en-tête, une bande d'informations résume le forfait d'un coup d'œil : **Abonnements actifs**, **Tranches de prix**, **Accessoires**, et **Revenu total**.

Le reste du formulaire est organisé en cinq onglets :

| Onglet | Ce qu'il contient |
|-----|-------------------|
| **Général** | Informations sur le forfait (nom, slug, description) et Statut (actif/public) |
| **Tarification** | Configuration de tarification, Période d'essai et Limites & Restrictions |
| **Tranches & Accessoires** | Les éditeurs de tranches de prix et d'accessoires |
| **Cycle de vie** | Politique de désabonnement et comportement de changement de forfait |
| **Avancé** | Intégration du fournisseur et Statistiques |

Les sections suivantes décrivent les paramètres de chaque onglet. Lorsque vous créez un nouveau forfait directement depuis **+ Ajouter un forfait** (plutôt que le wizard), les mêmes champs s'affichent dans un formulaire défilable unique au lieu d'onglets - enregistrez d'abord le forfait, puis rouvrez-le pour obtenir l'éditeur avec des onglets complets.

## Informations sur le forfait (onglet Général)

La carte **Informations sur le forfait** capture l'identité principale de votre forfait.

- **Nom du forfait** - Le nom que les clients voient lors de l'abonnement. Cliquez sur l'icône globe pour ajouter des traductions pour d'autres langues de magasin.
- **Slug** - Un identifiant convivial pour les URL généré automatiquement à partir du nom (par exemple, `forfait-premium`). Cela est utilisé en interne et dans les intégrations.
- **Description** - Texte optionnel décrivant ce que comprend le forfait. Prend en charge les traductions.

La carte **Statut** sur le même onglet contrôle les bascules **Actif** et **Public** - voir [Visibilité et statut](#visibilité-et-statut) ci-dessous.

![Onglet Général de l'éditeur de forfait](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modèle de tarification (onglet Tarification)

La carte **Configuration de tarification** contrôle comment la tarification est structurée pour ce forfait :

| Modèle de tarification | Idéal pour |
|---------------|----------|
| **Tarification par tranches** | Offrir des options d'engagement mensuel, trimestriel et annuel avec des remises pour des périodes plus longues |
| **Tarification par quantité** | Tarification par siège ou utilisateur où le total augmente avec la quantité (par exemple, licences d'équipe) |
| **Tarif fixe** | Un prix fixe unique sans variations |

Pour les forfaits **Tarification par quantité**, cochez **Autoriser la quantité** et définissez la **Quantité minimale** (nombre minimum de sièges requis) et éventuellement une **Quantité maximale** pour limiter le nombre de sièges qu'un abonné peut acheter.

[![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](https://spwig.com)

## Tarifs par tranches (onglet Tranches & Accessoires)

Les tranches de tarification définissent la fréquence de facturation et les options de remise disponibles pour les clients sur ce plan. Ajoutez-les dans la carte **Tranches de tarification** de l'onglet **Tranches & Accessoires**, à côté de l'éditeur d'accessoires.

Chaque tranche comporte les champs suivants :

- **Nom de la tranche** — Étiquette affichée aux clients (par exemple, `Mensuel`, `Annuel - Économisez 20 %`). Prise en charge des traductions.
- **Cycle de facturation** — Fréquence à laquelle le client est facturé : Journalier, Hebdomadaire, Mensuel, Trimestriel, Semestriel ou Annuel.
- **Intervalle de facturation** — Multiplicateur du cycle de facturation. Défini sur `2` avec Mensuel pour facturer tous les 2 mois.
- **Pourcentage de remise** — La remise appliquée au prix du produit pour cette tranche. Défini sur `0` pour le prix plein, ou `20` pour une remise de 20 %. Cette remise s'ajoute à toute remise en cours sur le produit lui-même.
- **Tranche par défaut** — Cochez une tranche comme par défaut pour la sélectionner automatiquement pour les clients lorsqu'ils consultent les options d'abonnement.

La remise s'applique dès le premier cycle de facturation du client, et non seulement lors des renouvellements — une tranche avec une remise de 20 % facture 20 % de moins dès le premier jour (ou dès la première facture après un essai, si le plan en comporte un).

### Exemple : plan par tranches avec trois options

Pour un plan d'abonnement "Café Club" : 

| Nom de la tranche | Cycle de facturation | Remise |
|-----------|---------------|----------|
| Mensuel | Mensuel | 0 % |
| Trimestriel - Économisez 10 % | Trimestriel | 10 % |
| Annuel - Économisez 20 % | Annuel | 20 % |

## Période d'essai

Une période d'essai permet aux clients d'essayer votre abonnement avant leur première facture complète. Configurez-la dans la section **Période d'essai** : 

- **Durée de la période d'essai (jours)** — Nombre de jours d'essai gratuits. Défini sur `0` pour désactiver les essais. La limite est de 365 jours.
- **Prix d'essai** — Prix réduit optionnel pendant l'essai (par exemple, 1 $ pour le premier mois). Laissez vide pour un essai totalement gratuit.

## Politique de désistement

Contrôlez comment les clients peuvent annuler leur abonnement dans la section **Politique de désistement** : 

| Politique | Description |
|--------|-------------|
| **Annuler à tout moment** | Les clients peuvent annuler immédiatement à tout moment |
| **Annuler à la fin de la période** | L'annulation prend effet à la fin de la période payante — les clients conservent l'accès jusqu'à expiration |
| **Engagement minimum requis** | Les clients doivent accomplir un nombre minimum de cycles de facturation avant d'annuler |

Paramètres supplémentaires : 

- **Engagement minimum (cycles)** — Lors de l'utilisation de la politique d'engagement, définissez le nombre de cycles de facturation requis (par exemple, `3` pour un engagement de 3 mois).
- **Période de grâce (jours)** — Jours d'accès continu après un échec de paiement avant que l'abonnement ne soit suspendu. Défini sur `0` pour une suspension immédiate.
- **Période de réactivation (jours)** — Jours après l'annulation pendant lesquels un client peut réactiver son abonnement sans devoir s'abonner à nouveau.

## Comportement des changements de forfait

Lorsque les clients passent d'un forfait à un autre, vous pouvez contrôler à quel moment le changement prend effet : 

- **Comportement de mise à niveau** — Défini sur **Immédiat** (facturer un montant proportionnel maintenant) ou **À la rénovation** (passer à la date de facturation suivante).
- **Comportement de désactivation** — Défini sur **Immédiat** (appliquer un crédit sur la prochaine facture) ou **À la rénovation** (passer à la date de facturation suivante).

## Plafonds et restrictions

- **Nombre maximum de cycles de facturation** — Nombre total de cycles de facturation avant que l'abonnement ne se termine automatiquement. Laissez vide pour une facturation récurrente illimitée. Utile pour les plans de paiement par versements ou les abonnements limités dans le temps.
- **Frais d'ouverture** — Frais unique perçu lors de la création initiale de l'abonnement (par exemple, frais d'inscription ou d'activation). Défini sur `0.00` pour aucun frais d'ouverture.

## Accessoires du forfait

Les accessoires sont des options supplémentaires que les abonnés peuvent ajouter à leur forfait. Ajoutez-les dans la section **Accessoires du forfait** : 

- **Nom de l'accessoire** — Le nom affiché aux clients.

Prise en charge des traductions.
- **Description** — Ce module fournit.
- **Prix** — Coût du module.
- **Fréquence de facturation** — Indique si le module est facturé **par cycle de facturation** (récurrent) ou **une fois** au début de l'abonnement.
- **Autoriser la quantité** — Activez pour permettre aux clients d'acheter plusieurs unités du module.
- **Obligatoire** — Cochez cette case pour inclure automatiquement le module sur tous les nouveaux abonnements.

Les modules obligatoires ne peuvent pas être supprimés par le client.

## Visibilité et statut

- **Actif** — Décochez pour désactiver un plan afin qu'aucun nouvel abonnement ne puisse être créé. Les abonnements existants ne sont pas affectés.
- **Public** — Décochez pour cacher le plan des pages visibles par les clients (utile pour les anciens plans internes ou obsolètes dont les abonnés existants restent).
- **Ordre de tri** — Contrôle l'ordre d'affichage sur les pages de sélection d'abonnement. Les numéros plus bas s'affichent en premier.

## Conseils

- Utilisez une **période d'essai** pour réduire les hésitations — même une période d'essai gratuite de 7 jours peut améliorer significativement les taux de conversion pour les produits d'abonnement.
- Configurez **trois niveaux de tarification** (mensuel, trimestriel, annuel) avec des remises croissantes pour encourager les engagements annuels et améliorer votre trésorerie.
- Pour les abonnements basés sur un service, définissez la **politique de désistement** sur **Annuler à la fin de la période** afin que les clients conservent l'accès pendant leur période payante — cela semble juste et réduit les remboursements.
- Gardez la **période de grâce** à 3 à 7 jours en cas d'échec de paiement. Cela donne aux clients le temps de mettre à jour leur mode de paiement avant de perdre l'accès.
- Utilisez le drapeau **Obligatoire** sur les modules avec modération — n'utilisez-le que pour les choses qui sont véritablement obligatoires (par exemple, un accord de service), et non comme moyen d'augmenter les prix.
- Désactivez les plans sans abonnés au lieu de les supprimer — cela préserve les données historiques pour tout client ayant autrefois souscrit.