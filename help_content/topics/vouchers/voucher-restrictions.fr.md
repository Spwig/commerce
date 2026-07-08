---
title: Restrictions des bons de réduction
---

Les restrictions des bons de réduction contrôlent qui peut utiliser un bon, quand et combien de fois. Configurez ces paramètres lors de la création ou de la modification d'un bon à **Marketing > Bons de réduction**.

![Règles de restriction](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Limites d'utilisation

Définissez des plafonds globaux et par client dans l'onglet **Limites d'utilisation** du formulaire du bon.

- **Max uses total** — Le nombre maximum de fois où ce bon peut être utilisé par tous les clients. Laissez vide pour une limite illimitée.
- **Max uses per customer** — Le nombre de fois qu'un seul client peut utiliser ce bon. Définissez à 1 pour la plupart des campagnes.

| Pattern | Max Total | Per Customer | Use Case |
|---------|-----------|--------------|----------|
| Campagne limitée | 100 | 1 | "Premiers 100 clients" - rareté |
| Code partagé illimité | (vide) | 1 | Code de marketing continu |
| Utilisation multiple illimitée | (vide) | (vide) | Réduction interne/employés |
| Codes uniques à usage unique | 1 | 1 | Codes générés en masse pour une campagne |

## Valeur minimale de commande

Le champ **Min order value** protège vos marges en exigeant un montant de panier avant que le bon ne s'applique. Par exemple, "$10 de réduction sur les commandes de plus de $50" garantit que vous ne réduirez jamais une commande petite au point de devenir non rentable.

| Réduction | Valeur minimale recommandée | Ratio |
|----------|-------------------|-------|
| $5 de réduction | $30+ | ~6:1 |
| $10 de réduction | $50+ | ~5:1 |
| $20 de réduction | $100+ | ~5:1 |
| 15% de réduction | $40+ | Dépend du catalogue |

## Plafond de réduction (Montant maximal de réduction)

Le champ **Max discount amount** dans **Discount Configuration** limite le montant que peut déduire un bon en pourcentage. Cela s'applique uniquement aux bons en pourcentage et empêche les réductions excessives sur les paniers de haute valeur.

Exemple : "20% de réduction, maximum $50 de réduction"
- Panier de $200 = $40 de réduction (20%)
- Panier de $300 = $50 de réduction (plafonné)
- Panier de $1 000 = toujours $50 de réduction (plafonné)

Ajoutez un plafond de réduction à tout bon en pourcentage que vous partagez publiquement.

## Règles de combinaison

Le groupe de champs **Restrictions & Rules** (cliquez pour développer) contient des cases à cocher qui contrôlent la manière dont les bons interagissent avec d'autres réductions.

| Paramètre | Ce que cela fait | Quand l'activer |
|---------|--------------|----------------|
| **Exclure les articles en promotion** | Le bon ignore les produits déjà en promotion | La plupart des campagnes — protège les marges des articles en promotion |
| **Ne peut pas être combiné avec d'autres bons** | Un seul bon par commande | Valeur par défaut pour la plupart des bons |
| **Ne peut pas être combiné avec des articles en promotion** | Bloque le bon si le panier contient AU MOINS UN article en promotion | Campagnes strictes où le bon remplace les prix en promotion |
| **Uniquement pour les nouveaux clients** | Uniquement pour les clients sans commandes précédentes | Campagnes de bienvenue/acquisition |

## Restrictions des clients

Pour une ciblage simple, cochez **Uniquement pour les nouveaux clients** dans le groupe de champs **Restrictions & Rules**.

Pour un ciblage avancé, utilisez le tableau **Voucher Restrictions** en ligne en bas du formulaire. Cliquez sur **+ Ajouter une autre restriction de bon** pour ajouter des lignes. Chaque restriction a trois champs :

- **Type** — La catégorie de restriction (liste déroulante)
- **Value** — La valeur correspondante (séparée par des virgules ou JSON)
- **Is inclusive** — Coché = le client doit correspondre ; non coché = le client ne doit pas correspondre

| Type | Value | Inclusive | Effet |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Oui | Seuls les employés de l'entreprise peuvent l'utiliser |
| shipping_country | US,CA | Oui | Seulement les clients des États-Unis et du Canada |
| shipping_country | RU | Non | Tout le monde SAUF la Russie |
| day_of_week | monday,tuesday | Oui | Valide uniquement le lundi et le mardi |
| payment_method | stripe | Oui | Seulement pour les paiements Stripe |

Combinez plusieurs lignes pour des restrictions en couches. Toutes les restrictions inclusives doivent correspondre, et aucune restriction exclusive ne doit correspondre, pour que le bon s'applique.

## Stratégies d'expiration

Contrôlez quand un bon expire en utilisant les champs de date et de validité.

- **End date** — Une date de fin rigide (par exemple, 31 décembre 2026).

Le bon cesse de fonctionner à minuit.
- **Days valid** — Validité roulante à partir de la création ou de la première utilisation du bon.

Remplace la date de fin lorsqu'elle est définie.


Utile pour les codes de bienvenue : "valide pendant 30 jours après réception".

| Stratégie | Date de fin | Jours valides | Cas d'utilisation |
|----------|----------|------------|----------|
| Date limite rigide | Définie | (vide) | Campagnes saisonnières, événements |
| Fenêtre glissante | (vide) | 30 | Codes de bienvenue, bons de réduction |
| Aucune date d'expiration | (vide) | (vide) | Codes permanents, réductions pour le personnel |

## Prévention de l'abuse

Suivez ce checklist pour garder vos bons sécurisés :

- Activez toujours **Max uses per customer** à 1 sauf si vous avez une raison spécifique de ne pas le faire.
- Définissez **Min order value** sur tous les bons d'un montant fixe.
- Ajoutez un **Max discount amount** sur les bons de pourcentage publics.
- Utilisez des codes difficiles à deviner pour les bons de grande valeur — évitez les codes évidents comme "DISCOUNT50".
- Suivez les statistiques d'utilisation sur chaque carte de bon dans le tableau de bord.
- Désactivez immédiatement un bon si vous remarquez des schémas de rédemption inhabituels.
- Pour les campagnes de grande valeur, utilisez des codes uniques générés en masse au lieu d'un seul code partagé.

## Conseils

- Commencez avec des restrictions strictes et relâchez les limites si la rédemption est trop faible — il est plus facile de relâcher les règles que de les resserrer après que les codes soient en circulation.
- Testez chaque bon avec un paiement réel avant de le distribuer aux clients.
- Vérifiez régulièrement le tableau de bord des statistiques des bons pour détecter les problèmes tôt.
- Combinez plusieurs restrictions pour une protection en couches — par exemple, limite par client + valeur minimale de commande + plafond de réduction + exclure les articles en promotion.