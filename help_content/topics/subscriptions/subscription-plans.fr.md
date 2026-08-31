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

Ouvrir un forfait existant (cliquez sur son nom, ou l'icône crayon, depuis la liste) vous amène à l'éditeur de forfaits. En haut, l'en-tête affiche le nom du forfait, son modèle de tarification, les badges **Actif**/**Inactif** et **Public**/**Privé**, et la date de création. Les deux boutons en haut à droite de l'en-tête enregistrent vos modifications - l'icône cercle vert enregistre et retourne à la liste, l'icône cercle simple enregistre et vous laisse sur la page afin que vous puissiez continuer à éditer.

Sous l'en-tête, une bande d'informations résume le forfait d'un coup d'œil : **Abonnements actifs**, **Tranches de tarification**, **Accessoires**, et **Revenu total**.

Le reste du formulaire est organisé en cinq onglets :

| Onglet | Ce qu'il contient |
|-----|-------------------|
| **Général** | Informations sur le forfait (nom, slug, description) et Statut (actif/public) |
| **Tarification** | Configuration de tarification, Période d'essai et Limites & Restrictions |
| **Tranches et accessoires** | Les éditeurs de tranches de tarification et d'accessoires |
| **Cycle de vie** | Politique de désistement et comportement de changement de forfait |
| **Avancé** | Intégration du fournisseur et Statistiques |

Les sections suivantes décrivent les paramètres de chaque onglet. Lorsque vous créez un nouveau forfait directement depuis **+ Ajouter un forfait** (plutôt que le wizard), les mêmes champs s'affichent dans un formulaire défilant unique au lieu d'onglets - enregistrez d'abord le forfait, puis rouvrez-le pour obtenir l'éditeur avec les onglets complets.

## Informations sur le forfait (onglet Général)

La carte **Informations sur le forfait** capture l'identité principale de votre forfait.

- **Nom du forfait** - Le nom que les clients voient lors de l'abonnement. Cliquez sur l'icône globe pour ajouter des traductions pour d'autres langues de magasin.
- **Slug** - Un identifiant convivial pour les URL généré automatiquement à partir du nom (ex. `premium-plan`). Cela est utilisé en interne et dans les intégrations.
- **Description** - Texte optionnel décrivant ce que comprend le forfait. Prend en charge les traductions.

La carte **Statut** sur le même onglet contrôle les bascules **Actif** et **Public** - voir [Visibilité et statut](#visibility-et-statut) ci-dessous.

![Onglet Général de l'éditeur de forfait](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modèle de tarification (onglet Tarification)

La carte **Configuration de tarification** contrôle comment la tarification est structurée pour ce forfait :

| Modèle de tarification | Idéal pour |
|---------------|----------|
| **Tarification par tranches** | Offrir des options d'engagement mensuel, trimestriel et annuel avec des remises pour des périodes plus longues |
| **Tarification par quantité** | Tarification par siège ou utilisateur où le total augmente avec la quantité (ex. licences d'équipe) |
| **Tarif fixe** | Un prix fixe unique sans variations |

Pour les forfaits **Tarification par quantité**, cochez **Autoriser la quantité** et définissez la **Quantité minimale** (nombre minimum de sièges requis) et éventuellement une **Quantité maximale** pour limiter le nombre de sièges qu'un abonné peut acheter.

[![](https://www.spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Tarifs par tranches (onglet Tranches & Accessoires)

Les tranches de tarification définissent la fréquence de facturation et les options de remise disponibles pour les clients sur ce plan. Ajoutez-les dans la carte **Tranches de tarification** de l'onglet **Tranches & Accessoires**, à côté de l'éditeur d'accessoires.

Chaque tranche comporte les champs suivants :

- **Nom de la tranche** — Étiquette affichée aux clients (par exemple, `Mensuel`, `Annuel - Économisez 20 %`). Prise en charge des traductions.
- **Cycle de facturation** — Fréquence à laquelle le client est facturé : Journalier, Hebdomadaire, Mensuel, Trimestriel, Semestriel ou Annuel.
- **Intervalle de facturation** — Multiplicateur du cycle de facturation. Défini sur `2` avec Mensuel pour facturer tous les 2 mois.
- **Pourcentage de remise** — La remise appliquée au prix du produit pour cette tranche. Défini sur `0` pour le prix plein, ou `20` pour une remise de 20 %. Cette remise s'ajoute à toute remise en cours sur le produit lui-même.
- **Tranche par défaut** — Cochez une tranche comme par défaut pour la sélectionner automatiquement pour les clients lorsqu'ils consultent les options d'abonnement.

La remise s'applique dès le tout premier cycle de facturation du client, et non seulement lors des renouvellements — une tranche avec une remise de 20 % facture 20 % de moins dès le premier jour (ou dès la première facture après un essai, si le plan en comporte un).

### Exemple : plan en tranches avec trois options

Pour un plan d'abonnement "Café Club" : 

| Nom de la tranche | Cycle de facturation | Remise |
|-----------|---------------|----------|
| Mensuel | Mensuel | 0 % |
| Trimestriel - Économisez 10 % | Trimestriel | 10 % |
| Annuel - Économisez 20 % | Annuel | 20 % |

## Accessoires du plan (onglet Tranches & Accessoires)

Les accessoires sont des options supplémentaires que les abonnés peuvent ajouter à leur plan. Ajoutez-les dans la carte **Accessoires**, directement sous les tranches de tarification sur le même onglet : 

- **Nom de l'accessoire** — Nom affiché aux clients. Prise en charge des traductions.
- **Description** — Ce que l'accessoire fournit.
- **Prix** — Coût de l'accessoire.
- **Fréquence de facturation** — Indiquez si l'accessoire est facturé **par cycle de facturation** (récurrent) ou **une fois** au début de l'abonnement.
- **Autoriser la quantité** — Activez pour permettre aux clients d'acheter plusieurs unités de l'accessoire.
- **Obligatoire** — Cochez pour inclure automatiquement l'accessoire sur tous les nouveaux abonnements. Les accessoires obligatoires ne peuvent pas être supprimés par le client.

[![](https://www.spwig.com/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Période d'essai (onglet Tarifs)

Une période d'essai permet aux clients d'essayer votre abonnement avant leur première facture complète. Configurez-la dans la carte **Période d'essai**, sous la configuration de tarification : 

- **Durée de la période d'essai (jours)** — Nombre de jours d'essai gratuits. Définissez sur `0` pour désactiver les essais. La limite est de 365 jours.
- **Prix d'essai** — Prix réduit optionnel pendant l'essai (par exemple, 1 $ pour le premier mois). Laissez vide pour un essai totalement gratuit.

## Limites et restrictions (onglet Tarifs)

La carte **Limites & Restrictions**, également sur l'onglet Tarifs, contient : 

- **Nombre maximum de cycles de facturation** — Nombre total de cycles de facturation avant la fin automatique de l'abonnement. Laissez vide pour une facturation récurrente illimitée. Utile pour les plans à plusieurs versements ou les abonnements limités dans le temps.

**Frais de mise en service** et **Ordre de tri** ne font pas partie de cette carte — ils sont définis une fois, lors de la création initiale du plan via le **Processus de création**, et ne peuvent pas être modifiés à partir de l'écran de modification par la suite. Si vous avez besoin d'ajuster l'une de ces valeurs, désactivez le plan et recréez-le avec le processus plutôt que d'éditer le plan existant. Notez que les frais de mise en service ne sont pas encore facturés automatiquement lors de la validation dans cette version — considérez le champ comme réservé à une mise à jour future plutôt qu'en tant que frais fonctionnels.

## Politique de désabonnement (onglet Cycle de vie)

Contrôlez comment les clients peuvent désabonner leur abonnement dans la carte **Politique de désabonnement** :

| Politique | Description |
|--------|-------------|
| **Annulation à tout moment** | Les clients peuvent annuler immédiatement à tout moment |
| **Annulation à la fin de la période** | L'annulation prend effet à la fin de la période payée — les clients conservent l'accès jusqu'à l'expiration |
| **Engagement minimum requis** | Les clients doivent compléter un nombre minimum de cycles de facturation avant d'annuler |

Paramètres supplémentaires :

- **Engagement minimum (Cycles)** — Lors de l'utilisation de la politique d'engagement, définissez le nombre de cycles de facturation requis (par exemple, `3` pour un minimum de 3 mois).
- **Délai de grâce (Jours)** — Nombre de jours d'accès continu après un échec de paiement avant que l'abonnement ne soit suspendu. Définissez sur `0` pour une suspension immédiate.
- **Période de réactivation (Jours)** — Nombre de jours après l'annulation pendant lesquels un client peut réactiver son abonnement sans avoir à se réabonner depuis le début.

## Comportement de changement de plan (Onglet Cycle de vie)

La carte **Comportement de changement de plan**, située sous la Politique d'annulation, contrôle ce qui se passe lorsque les clients passent d'un plan à un autre (mise à niveau ou rétrogradation) :

- **Comportement de mise à niveau** — Définissez sur **Immédiat** (facturation du montant prorata maintenant) ou **Au renouvellement** (changement à la prochaine date de facturation).
- **Comportement de rétrogradation** — Définissez sur **Immédiat** (application d'un avoir à la prochaine facture) ou **Au renouvellement** (changement à la prochaine date de facturation).

![Onglet Cycle de vie de l'éditeur de plan](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Onglet Avancé

L'onglet **Avancé** contient des paramètres dont vous aurez rarement besoin au quotidien :

- **Intégration du fournisseur** — Associez ce plan aux identifiants de plan/prix de vos fournisseurs de paiement (par exemple, `{"stripe": "price_xxx", "paypal": "P-xxx"}`), pour les boutiques qui gèrent les abonnements nativement via le fournisseur plutôt que via le moteur de facturation de Spwig.
- **Statistiques** — Chiffres en lecture seule : **Abonnements actifs**, **Revenu total** et les horodatages **Créé le** / **Mis à jour le** du plan. Ces éléments reflètent la bande de statistiques en haut de la page.

![Onglet Avancé de l'éditeur de plan](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Visibilité et statut (Onglet Général)

- **Actif** — Décochez pour désactiver un plan afin qu'aucun nouvel abonnement ne puisse être créé. Les abonnements existants ne sont pas affectés.
- **Public** — Décochez pour masquer le plan des pages destinées aux clients (utile pour les plans internes ou anciens sur lesquels les abonnés existants restent inscrits).

## Conseils

- Utilisez une **période d'essai** pour réduire l'hésitation — même une courte période d'essai gratuite de 7 jours peut considérablement améliorer les taux de conversion sur les produits d'abonnement.
- Mettez en place **trois niveaux de prix** (mensuel, trimestriel, annuel) avec des remises croissantes pour encourager les engagements annuels et améliorer votre trésorerie.
- Pour les abonnements basés sur des services, définissez la **Politique d'annulation** sur **Annulation à la fin de la période** afin que les clients conservent l'accès pendant leur période payée — cela semble équitable et réduit les litiges de paiement.
- Maintenez le **Délai de grâce** à 3–7 jours en cas d'échec de paiement. Cela donne aux clients le temps de mettre à jour leur moyen de paiement avant de perdre l'accès.
- Utilisez l'indicateur **Requis** sur les options supplémentaires avec parcimonie — ne l'utilisez que pour les éléments véritablement obligatoires (par exemple, un accord de service), et non comme un moyen d'augmenter les prix.
- Désactivez les plans sans abonnés plutôt que de les supprimer — cela préserve les données historiques pour les clients qui se sont abonnés précédemment.