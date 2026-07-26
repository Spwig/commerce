---
title: Programme de fidélité
---

Le Programme de fidélité vous permet de récompenser les clients pour leurs achats et leur engagement via un système basé sur des points. Les clients gagnent des points, avancent dans les niveaux et échangent des récompenses. Accédez à **Marketing > Programme de fidélité** dans le menu latéral de l'admin.

![Tableau de bord de fidélité](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Tableau de bord de fidélité

Le tableau de bord fournit un aperçu complet de votre programme de fidélité:

### Métriques clés

- **Total Members** — Total des clients inscrits
- **Active Members (30d)** — Membres qui ont gagné ou échangé des points au cours des 30 derniers jours
- **Points Outstanding** — Total des points non échangés par tous les membres
- **Redemption Rate** — Pourcentage des points gagnés qui ont été échangés
- **Points Earned (30d)** — Points gagnés au cours des 30 derniers jours
- **Points Redeemed (30d)** — Points échangés au cours des 30 derniers jours
- **Avg Points/Member** — Moyenne de points par membre
- **Active Rules** — Nombre de règles de gains actives

### Actions rapides

Le tableau de bord dispose de cartes raccourcis pour gérer tous les aspects du programme:
- **Members** — Afficher et gérer les membres de fidélité
- **Tiers** — Configurer les niveaux de membre
- **Rewards** — Créer le catalogue de récompenses
- **Redemptions** — Afficher l'historique des échanges
- **Rules** — Configurer comment les points sont gagnés
- **Badges** — Gérer les badges d'accomplissement
- **Campaigns** — Lancer des campagnes de fidélité spéciales
- **Segments** — Créer des segments de membres pour cibler

### Graphiques et analyses

- **Member Enrollment Trend** — Inscriptions de nouveaux membres au fil du temps
- **Points Earned vs Redeemed** — Suivre l'équilibre du flux de points
- **Tier Distribution** — Voir la répartition des membres par niveau

## Configuration du programme

### Étape 1: Créer des niveaux

Les niveaux définissent les niveaux de membre avec des avantages croissants:

1. Accédez à **Loyalty > Tiers**
2. Créez des niveaux comme Bronze, Silver, Gold, Platinum
3. Pour chaque niveau, définissez:
   - **Name** — Nom d'affichage du niveau
   - **Rank** — Ordre de tri (rang plus bas = niveau plus bas, par exemple, Bronze = 1, Silver = 2)
   - **Color** — Couleur d'accent visuel affichée sur les badges des membres
   - **Min Points Earned** — Points cumulés au cours de la vie pour être éligible à ce niveau
   - **Min Spend** — Montant total à dépenser pour être éligible à ce niveau
   - **Min Orders** — Nombre de commandes pour être éligible à ce niveau
   - **Points Multiplier** — Taux de gain bonus pour les membres de ce niveau (par exemple, 2.0 = 2x points)

Un membre est éligible à un niveau si **n'importe laquelle** des trois seuils est atteinte. Vous pouvez utiliser un seul seuil ou combiner les trois.

### Étape 2: Configurer les règles de gains

Les règles définissent comment les clients gagnent des points:

1. Accédez à **Loyalty > Rules**
2. Créez des règles en utilisant l'un des quatre types de règles:

| Type de règle | Description | Exemple |
|---------------|-------------|---------|
| **Spend** | Points par montant dépensé | 1 point par $1 |
| **Item** | Points par article acheté | 50 points par produit dans une catégorie spécifique |
| **Action** | Points pour une action spécifique | 200 points pour s'inscrire |
| **Event** | Points pour un événement du calendrier | Points bonus d'anniversaire |

3. Configurez les paramètres supplémentaires de la règle:
   - **Scope / Scope Filters** — Limiter la règle à des produits, des catégories ou des niveaux de membre spécifiques
   - **Min Order Amount** — Montant minimum du panier pour que la règle s'applique
   - **Allowed Tiers** — Limiter la règle à des niveaux de membre spécifiques
   - **Is Exclusive** — Lorsqu'elle est activée, cette règle ne peut pas s'accumuler avec d'autres règles
   - **Points Pending Days** — Nombre de jours avant que les points gagnés soient disponibles (utile pour tenir compte des fenêtres de retour)
   - **Points Expire Days** — Nombre de jours après le gain avant que les points expirent (laissez vide pour aucune expiration)
   - **Start / End Date** — Limiter la règle à une plage de dates

### Étape 3: Configurer les récompenses

Les récompenses sont ce que les clients peuvent échanger contre leurs points:

1. Accédez à **Loyalty > Rewards**
2. Créez des récompenses comme:
   - **$5 Off Coupon** — 500 points
   - **Free Shipping** — 300 points
   - **10% Discount** — 1000 points


> **Les codes de réduction ne peuvent pas être utilisés pour le moment.** Une récompense avec **Type de récompense** défini sur **Code de réduction** — comme le coupon de 5 $ de réduction ou l'exemple de 10 % de réduction ci-dessus — ne parvient actuellement pas à être utilisée.

Le membre voit un message d'erreur clair et ses points lui sont automatiquement restitués sur son solde, donc rien n'est perdu, mais la récompense n'est pas utilisable pour le moment.

C'est une correction délibérée : le système de rédemption signalait autrefois un succès tout en déduisant silencieusement les points et en ne délivrant rien.

Si les membres mentionnent que la rédemption "ne fonctionne pas", il s'agit de cela — ce n'est pas un nouveau problème.

Les récompenses en points reprendront fonctionnement à partir d'une mise à jour à venir.

Cela n'affecte pas les récompenses de livraison gratuite, de produit gratuit ou d'expérience/avantage.

### Étape 4 : Créer des badges (facultatif)

Les badges reconnaissent les réalisations des clients :

1. Accédez à **Loyalty > Badges**
2. Créez des badges pour des paliers :
   - **Premier achat** — Attribué après le premier achat
   - **Gros dépensier** — Attribué après un dépense de 500 $ ou plus
   - **Client fidèle** — Attribué après 10 commandes

Les badges peuvent inclure des récompenses supplémentaires en points lorsqu'ils sont obtenus.

## Gestion des membres

### Liste des membres

Affichez tous les membres de fidélité avec leurs :
- Niveau actuel et statut
- Solde de points
- Date d'inscription
- Activité récente

### Meilleurs gagnants de points

Le tableau de bord met en évidence vos membres les plus actifs avec un classement montrant le rang, le nom, le niveau et les points gagnés pendant la période.

### Transactions récentes

Un journal des transactions affiche toute l'activité récente en points. Les types de transactions incluent :

| Type | Signification |
|------|---------|
| **Gagner** | Points crédités à partir d'un achat éligible ou d'une règle |
| **Réduire** | Points dépensés pour une récompense |
| **Bonus** | Points supplémentaires provenant d'un badge, d'une campagne ou d'une attribution manuelle |
| **Ajustement** | Correction manuelle des points effectuée par un membre du personnel |
| **Révoquer** | Points retirés (par exemple, après annulation d'une commande) |
| **Expirer** | Points qui ont dépassé leur date d'expiration |

### Ajustements manuels de points

Vous pouvez manuellement ajouter ou soustraire des points à tout membre :

1. Ouvrez la page de détails du membre
2. Cliquez sur **Ajuster les points**
3. Entrez le montant de points (positif pour ajouter, négatif pour soustraire)
4. Entrez une raison pour l'ajustement
5. Cliquez sur **Enregistrer**

L'ajustement est enregistré comme une transaction et est visible dans l'historique des transactions du membre.

## Campagnes

Les campagnes de fidélité vous permettent de lancer des promotions spéciales :
- **Double points le week-end** — Augmenter temporairement le taux de gains
- **Événements de points bonus** — Attribuer des points supplémentaires pour des actions spécifiques
- **Promotions de passage de niveau** — Réduire le seuil pour le passage de niveau

## Conseils

- Commencez avec des règles simples de gains (1 point par 1 $ dépensé) et développez progressivement.
- Fixez des seuils de récompense atteignables pour maintenir l'engagement des membres — si les récompenses semblent inaccessibles, les membres perdent l'intérêt.
- Utilisez des badges pour gamifier l'expérience et encourager des comportements spécifiques.
- Suivez le taux de rédemption — un programme sain a un taux de rédemption compris entre 10 et 30 %.
- Lancez des campagnes pendant les périodes creuses pour stimuler l'engagement.
- Utilisez le graphique Points gagnés vs Points réduits pour vous assurer que votre programme est durable.