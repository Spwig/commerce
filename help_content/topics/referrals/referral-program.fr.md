---
title: Programme de parrainage
---

Le programme de parrainage permet à vos clients existants de partager un lien de parrainage unique avec leurs amis et leur famille. Lorsqu'un ami parrainé effectue son premier achat éligible, à la fois le parrain et le nouveau client peuvent recevoir une récompense — ce qui favorise l'acquisition de nouveaux clients par le bouche-à-oreille.

## Fonctionnement du programme de parrainage

1. Un client partage son lien de parrainage (ou code) avec un ami.
2. L'ami clique sur le lien et est suivi via un cookie pendant jusqu'à 30 jours (configurable).
3. L'ami s'inscrit et passe sa première commande éligible.
4. Le système crée un enregistrement d'attribution de parrainage et effectue des vérifications anti-fraude et d'éligibilité.
5. Si l'attribution est approuvée, des récompenses sont attribuées aux deux parties.

Votre boutique dispose d'une seule configuration de programme de parrainage. Accédez à **Marketing > Programme de parrainage** pour le configurer.

## Configuration du programme de parrainage

### État du programme

Le programme possède trois états :

- **Brouillon** — Le programme est en cours de configuration mais pas encore actif. Les liens de parrainage sont inactifs.
- **Actif** — Le programme est actif. Les clients peuvent partager des liens et gagner des récompenses.
- **Suspendu** — Le programme est temporairement arrêté. Les attributions existantes continuent d'être traitées, mais aucun nouveau parrainage n'est suivi.

Définissez l'**État** sur **Actif** lorsque vous êtes prêt à lancer le programme. Vous pouvez le suspendre à tout moment.

### Configuration des récompenses

Définissez les récompenses qui sont attribuées lorsqu'un parrainage est converti. Le programme prend en charge les **récompenses à double face** — ce qui signifie que vous pouvez récompenser à la fois le parrain (le client qui a partagé le lien) et le parrainé (le nouveau client qui l'a utilisé).

Configurez les récompenses pour chaque destinataire dans le champ **Configuration des récompenses**. Les types de récompenses disponibles sont :

| Type de récompense | Description |
|-------------------|-------------|
| **Crédit de magasin** | Ajoute un crédit au portefeuille du client, utilisable sur les commandes futures |
| **Code de coupon** | Génère un code de voucher de réduction unique |
| **Réduction en pourcentage** | Attribue une réduction en pourcentage à utiliser lors du paiement |
| **Avantage exclusif** | Un avantage personnalisé (ex. : cadeau gratuit, accès prioritaire) — décrit dans le champ de description de la récompense |

Les récompenses de type Code de coupon et Réduction en pourcentage sont verrouillées au client qui les a gagnées — le code de voucher ne fonctionne que lorsque ce client est connecté. Si un parrain partage son code de récompense avec quelqu'un d'autre au lieu de son lien de parrainage, l'ami ne pourra pas l'utiliser ; seul le lien de parrainage lui-même doit être partagé.

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
| `exclude_staff` | Si `true`, les comptes de personnel ne peuvent pas être parrains ou parrainés |

**Exemple** — uniquement nouveaux clients, montant minimum de 40 $, personnel exclu :

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


L'utilisation de `post_refund` est l'approche la plus prudente — elle attend que la période de retour soit terminée avant d'attribuer les récompenses, réduisant ainsi le risque d'attribuer des récompenses à des commandes qui seront ultérieurement remboursées.

### Plafonds et limites

Empêchez un seul affilié de gagner des récompenses illimitées en définissant des plafonds dans le champ **Plafonds & Limites** :

| Paramètre | Ce que cela fait |
|---------|--------------|
| `monthly_per_referrer` | Nombre maximum de références réussies récompensées par mois, par affilié |
| `lifetime_per_referrer` | Nombre total maximum de références réussies récompensées jamais, par affilié |
| `max_reward_per_order` | Valeur maximale de récompense (en devise de votre magasin) attribuée pour une seule conversion de référence |

**Exemple** — 20 références par mois, 200 au total, 50 $ maximum de récompense par conversion :

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configuration de suivi

Configurez la manière dont les liens de référence sont suivis dans le champ **Configuration de suivi** :

| Paramètre | Ce que cela fait |
|---------|--------------|
| `cookie_ttl_days` | Nombre de jours pendant lesquels le cookie de suivi des références reste actif après que votre ami a cliqué sur le lien (par défaut : 30) |
| `attribution` | Méthode d'attribution — actuellement `last_touch` (la dernière clic sur le lien de référence est crédité) |

### Politique de fraude

Le système de détection de fraude attribue automatiquement un score de risque à chaque attribution de référence avant de l'approbation. Configurez la politique dans le champ **Politique de fraude** :

| Paramètre | Ce que cela fait |
|---------|--------------|
| `policy` | Stricteur global : `strict`, `balanced` ou `lenient` |
| `auto_reject_threshold` | Score de risque (0–100) au-delà duquel les attributions sont automatiquement rejetées (par défaut : 80) |
| `auto_approve_threshold` | Score de risque en dessous duquel les attributions sont automatiquement approuvées (par défaut : 30) |
| `check_ip` | Si `true`, vérifie si l'affilié et le client référencé partagent la même adresse IP |
| `check_device` | Si `true`, vérifie si l'affilié et le client référencé partagent le même empreinte de dispositif |
| `check_velocity` | Si `true`, surveille les taux de références anormalement élevés provenant d'une seule source |
| `velocity_window_hours` | La fenêtre de temps (en heures) pour la vérification de la vitesse |
| `max_referrals_per_window` | Nombre maximum de références autorisées provenant d'une seule source dans la fenêtre de vitesse |

Les attributions dont le score de risque se situe entre les seuils d'auto-rejet et d'auto-approbation entrent dans un statut **En attente** et nécessitent une revue manuelle.

### Conditions générales

Entrez tout terme ou condition juridique pour le programme dans le champ **Conditions générales**. Ce texte est affiché aux clients lorsqu'ils consultent le programme de référence. Le formatage Markdown est pris en charge.

## Affichage des attributions de référence

Accédez à **Marketing > Attributions de référence** pour voir toutes les cas de référence — le lien entre un affilié et un client référencé.

![Liste des attributions de référence](/static/core/admin/img/help/referral-program/attribution-list.webp)

Chaque attribution affiche l'affilié, le client référencé, la première commande qu'ils ont passée, le statut actuel et le score de risque.

### Statuts d'attribution

| Statut | Ce que cela signifie |
|--------|---------------|
| **En attente** | En attente de revue — le score de risque se situe dans la plage de revue manuelle |
| **Approuvé** | La référence est valide — les récompenses ont été ou seront attribuées |
| **Rejeté** | La référence n'était pas éligible ou a été signalée comme frauduleuse |
| **Expiré** | La référence n'a pas été convertie dans la fenêtre de suivi |

### Approbation ou rejet manuel des attributions

Pour les attributions en statut **En attente**, vous pouvez approuver ou rejeter manuellement en ouvrant le dossier d'attribution et en utilisant les boutons d'action. Lors d'un rejet, choisissez une **raison de rejet** :

- Référence auto
- Pas un nouveau client
- En dessous du montant minimum de commande
- Email temporaire
- Plafond dépassé
- Risque de fraude
- Commande remboursée ou annulée
- Rejet manuel

Vous pouvez également ajouter des **notes de rejet** pour vos propres dossiers.

### Filtre par niveau de risque

Utilisez le filtre **Niveau de risque** dans la barre latérale pour vous concentrer sur les attributions à haut risque nécessitant une revue :

- Risque faible (score 0–30) — Approbation automatique
- Risque modéré (score 31–70) — Révision manuelle
- Risque élevé (score 71–89) — Révision manuelle, traiter avec prudence
- Risque très élevé (score 90+) — Refus automatique

## Affichage des récompenses attribuées

Accédez à **Marketing > Récompenses attribuées** pour voir toutes les récompenses qui ont été attribuées en raison d'attribution approuvée.

Chaque entrée de récompense affiche le client, s'il s'agit du référent ou du réfééré, le type et le montant de la récompense, ainsi que le statut actuel de rédemption.

### Statuts des récompenses

| Statut | Ce que cela signifie |
|--------|---------------------|
| **En attente** | La récompense a été créée mais n'a pas encore été livrée au client |
| **Attribuée** | La récompense est active et disponible pour le client |
| **Réclamée** | Le client a utilisé la récompense |
| **Expirée** | La récompense a dépassé sa date d'expiration sans avoir été utilisée |
| **Révoquée** | La récompense a été annulée manuellement (par exemple, si le commande originale a été remboursée après l'attribution de la récompense) |

### Révocation d'une récompense

Si une récompense doit être annulée — par exemple, la commande qualifiante a été retournée — ouvrez le dossier de récompense et utilisez l'action **Révoquer**. Ajoutez une note expliquant pourquoi elle a été révoquée pour vos archives.

## Conseils

- Commencez par le paramètre de timing `post_refund`. Attendre que la période de retour expire avant d'attribuer des récompenses empêche de récompenser des commandes qui finiront par être retournées.
- La politique de fraude `balanced` est un bon paramètre par défaut pour la plupart des magasins. Passez à `strict` si vous remarquez une augmentation inhabituelle de références provenant d'un petit nombre de comptes.
- Fixez des plafonds mensuels et de toute vie réalistes. Si la valeur de votre récompense est élevée, un plafond de 10 à 20 par mois par référent est raisonnable pour éviter les abus.
- Révisez les attributions **En attente** hebdomadairement. Laisser ces attributions sans révision pendant trop longtemps peut frustrer les référents légitimes qui attendent leur récompense.
- Utilisez le filtre **Niveau de risque** pour prioriser votre file d'attente de révision manuelle — commencez par les attributions à très haut risque avant de passer aux attributions à risque modéré.
- Gardez vos Conditions générales courtes et en langage simple. Les clients sont plus enclins à participer lorsqu'ils comprennent clairement les règles.