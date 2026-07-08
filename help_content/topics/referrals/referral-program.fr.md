---
title: Programme de parrainage
---

Le programme de parrainage permet à vos clients existants de partager un lien de parrainage unique avec leurs amis et leur famille. Lorsqu'un ami parrainé effectue son premier achat éligible, à la fois le parrain et le nouveau client peuvent recevoir une récompense — ce qui favorise l'acquisition de nouveaux clients par le bouche-à-oreille.

## Fonctionnement du programme de parrainage

1. Un client partage son lien de parrainage (ou code) avec un ami.
2. L'ami clique sur le lien et est suivi via un cookie pendant un maximum de 30 jours (configurable).
3. L'ami s'inscrit et passe sa première commande éligible.
4. Le système crée un enregistrement d'attribution de parrainage et exécute des vérifications anti-fraude et d'éligibilité.
5. Si l'attribution est approuvée, des récompenses sont attribuées aux deux parties.

Votre boutique dispose d'une seule configuration de programme de parrainage. Accédez à **Marketing > Programme de parrainage** pour le configurer.

## Configuration de votre programme de parrainage

### État du programme

Le programme possède trois états :

- **Brouillon** — Le programme est en cours de configuration mais pas encore actif. Les liens de parrainage sont inactifs.
- **Actif** — Le programme est actif. Les clients peuvent partager des liens et gagner des récompenses.
- **Suspendu** — Le programme est temporairement arrêté. Les attributions existantes continuent d'être traitées, mais aucun nouveau parrainage n'est suivi.

Définissez l'**État** sur **Actif** lorsque vous êtes prêt à lancer le programme. Vous pouvez le suspendre à tout moment.

### Configuration des récompenses

Définissez les récompenses qui sont attribuées lorsqu'un parrainage est converti. Le programme prend en charge les **récompenses doubles** — ce qui signifie que vous pouvez récompenser à la fois le parrain (le client qui a partagé le lien) et le parrainé (le nouveau client qui l'a utilisé).

Configurez les récompenses pour chaque destinataire dans le champ **Configuration des récompenses**. Les types de récompenses disponibles sont les suivants :

| Type de récompense | Description |
|-------------------|-------------|
| **Crédit de magasin** | Ajoute un crédit au portefeuille du client, utilisable sur les commandes futures |
| **Code de coupon** | Génère un code de voucher de réduction unique |
| **Réduction en pourcentage** | Attribue une réduction en pourcentage à utiliser lors du paiement |
| **Avantage exclusif** | Un avantage personnalisé (ex. : cadeau gratuit, accès prioritaire) — décrit dans le champ de description de la récompense |

**Exemple de configuration** — 10 $ de crédit de magasin pour le parrain et 10 $ de réduction pour le nouveau client :

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Définissez `"double_sided": false` si vous souhaitez uniquement récompenser le parrain.

### Règles d'éligibilité

Les règles d'éligibilité déterminent les parrainages qui qualifient pour des récompenses. Configurez-les dans le champ **Règles d'éligibilité** :

| Règle | Ce qu'elle fait |
|-------|----------------|
| `new_customer_only` | Si `true`, l'ami parrainé doit être un nouveau client (aucune commande antérieure) |
| `min_order_value` | Le montant minimum de commande (en devise de votre boutique) que l'ami parrainé doit dépenser |
| `exclude_discounts` | Si `true`, les commandes où le client parrainé a utilisé un voucher ne qualifient pas |
| `exclude_staff` | Si `true`, les comptes de personnel ne peuvent pas être des parrains ou des parrainés |

**Exemple** — uniquement de nouveaux clients, montant minimum de 40 $, personnel exclu :

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Configuration des délais

Le champ **Configuration des délais** contrôle quand les récompenses sont attribuées après une commande éligible :

| Paramètre | Ce qu'il fait |
|-----------|--------------|
| `issue_on` | Quand attribuer la récompense : `signup` (immédiatement à l'inscription), `first_purchase` (immédiatement après la commande), ou `post_refund` (après l'expiration de la période de remboursement) |
| `refund_window_days` | Nombre de jours à attendre avant d'attribuer les récompenses lors de l'utilisation de `post_refund` (par défaut : 14 jours) |

L'utilisation de `post_refund` est l'approche la plus prudente — elle attend que la période de retour soit passée avant d'attribuer les récompenses, réduisant ainsi le risque de récompenser des commandes qui seront ultérieurement remboursées.

### Plafonds et limites

Empêchez un seul parrain de gagner des récompenses illimitées en définissant des plafonds dans le champ **Plafonds & Limites** :

Exemple — 20 parrainages par mois, 200 au total, 50 $ maximum de récompense par conversion :

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

Configuration de suivi

Configurez la manière dont les liens de parrainage sont suivis dans le champ **Configuration de suivi** :

Politique de fraude

Le système de détection de fraude évalue automatiquement chaque attribution de parrainage pour le risque avant de l'approbation. Configurez la politique dans le champ **Politique de fraude** :

Les attributions dont le score de risque se situe entre les seuils d'auto-rejet et d'auto-approbation entrent dans un statut **En attente** et nécessitent une revue manuelle.

Entrez tout terme et condition juridique pour le programme dans le champ **Termes et conditions**. Ce texte est affiché aux clients lorsqu'ils consultent le programme de parrainage. Le formatage Markdown est pris en charge.

Affichage des attributions de parrainage

Accédez à **Marketing > Attributions de parrainage** pour voir tous les cas de parrainage — le lien entre un parrain et un client parrainé.

Liste des attributions de parrainage

/static/core/admin/img/help/referral-program/attribution-list.webp

Chaque attribution affiche le parrain, le client parrainé, la première commande qu'ils ont passée, le statut actuel et le score de risque.

Statuts d'attribution

Pour les attributions en statut **En attente**, vous pouvez approuver ou rejeter manuellement en ouvrant l'enregistrement d'attribution et en utilisant les boutons d'action. Lors du rejet, choisissez une **raison de rejet** :

- Parrainage auto
- Pas un nouveau client
- En dessous du montant minimum de commande
- Email temporaire
- Plafond dépassé
- Risque de fraude
- Commande remboursée ou annulée
- Rejet manuel

Vous pouvez également ajouter des **notes de rejet** pour vos propres dossiers.

Utilisez le filtre **Niveau de risque** dans la barre latérale pour vous concentrer sur les attributions à haut risque nécessitant une revue :

- Faible risque (score 0–30) — Auto-approuvé
- Risque moyen (score 31–70) — Revue manuelle
- Haut risque (score 71–89) — Revue manuelle, traiter avec prudence
- Très haut risque (score 90+) — Auto-rejeté

Affichage des récompenses attribuées

Accédez à **Marketing > Récompenses attribuées** pour voir toutes les récompenses qui ont été attribuées en raison d'attributions approuvées.

Chaque entrée de récompense affiche le client, s'il s'agit du référent ou du réfééré, le type et le montant de la récompense, ainsi que le statut actuel de sa rédemption.

### États des récompenses

| État | Ce que cela signifie |
|------|-------------------|
| **En attente** | La récompense a été créée mais n'a pas encore été livrée au client |
| **Attribuée** | La récompense est active et disponible pour le client |
| **Réclamée** | Le client a utilisé la récompense |
| **Expirée** | La récompense a expiré sans avoir été utilisée |
| **Annulée** | La récompense a été annulée manuellement (par exemple, si le commande originale a été remboursée après l'attribution de la récompense) |

### Annuler une récompense

Si une récompense doit être annulée — par exemple, la commande qualifiante a été retournée — ouvrez le dossier de la récompense et utilisez l'action **Annuler**. Ajoutez une note expliquant pourquoi elle a été annulée pour vos dossiers.

## Conseils

- Commencez par le paramètre de timing `post_refund`. Attendre que la période de retour expire avant d'attribuer des récompenses empêche de récompenser des commandes qui finiront par être retournées.
- La politique de fraude `balanced` est un bon paramètre par défaut pour la plupart des magasins. Passez à `strict` si vous remarquez une augmentation inhabituelle de références provenant d'un petit nombre de comptes.
- Fixez des plafonds mensuels et de toute vie réalistes. Si la valeur de votre récompense est élevée, un plafond de 10 à 20 par mois par référent est raisonnable pour éviter les abus.
- Révisez les attributions **En attente** hebdomadairement. Laisser ces attributions sans examen pendant trop longtemps peut frustrer les référents légitimes qui attendent leur récompense.
- Utilisez le filtre **Niveau de risque** pour prioriser votre file d'attente de vérification manuelle — commencez par les attributions à très haut risque avant de passer aux attributions à risque moyen.
- Gardez vos Conditions générales courtes et en langage simple. Les clients sont plus enclins à participer lorsqu'ils comprennent clairement les règles.