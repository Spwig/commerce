---
title: Gestion des abonnements clients
---

La section des abonnements clients vous donne une vue d'ensemble complète de tous les abonnements récurrents actifs, suspendus et annulés dans votre magasin. À partir de là, vous pouvez surveiller la santé des facturations, consulter les détails d'un abonnement individuel et prendre des mesures en cas de problème.

## Affichage des abonnements clients

Accédez à **Abonnements > Abonnements clients** pour voir la liste complète des abonnements de tous les clients.

![Liste des abonnements clients](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

La liste affiche pour chaque abonnement le client, le nom du plan, le statut actuel, la date de facturation suivante et le nombre de cycles de facturation terminés.

### Filtre et recherche

Utilisez le panneau de filtre à droite pour affiner les abonnements selon :

- **Statut** — Filtrez par Actif, Essai, En retard, Suspendu, Annulé ou Expiré
- **Plan** — Affichez les abonnements d'un plan spécifique
- **Mode du fournisseur** — Natif (géré par Stripe/PayPal) ou Fallback (facturation interne)

Utilisez la barre de recherche pour trouver des abonnements par adresse e-mail du client.

## États des abonnements

Comprendre chaque état vous aide à identifier les abonnements qui nécessitent une attention particulière :

| Statut | Ce que cela signifie |
|--------|---------------------|
| **Essai** | Le client est en période d'essai gratuite ou à prix réduit |
| **Actif** | L'abonnement est en bonne santé — les facturations sont à jour et l'accès est actif |
| **En retard** | Un paiement a échoué — le système tente à nouveau. Le client conserve l'accès pendant la période de grâce |
| **Suspendu** | L'abonnement est temporairement suspendu — aucun paiement, aucun accès |
| **Annulé** | L'annulation a été demandée. Le client peut encore avoir accès jusqu'à la date de fin du période |
| **Expire** | L'abonnement a totalement pris fin — l'essai a expiré, le nombre maximum de cycles de facturation a été atteint ou la période d'annulation est écoulée |

Les abonnements qui sont **En retard** nécessitent le plus d'attention — si les paiements continuent à échouer et que la période de grâce se termine, l'abonnement sera suspendu.

## Affichage des détails d'un abonnement

Cliquez sur tout abonnement pour ouvrir la vue détaillée. Cela affiche :

### Période de facturation actuelle

- **Début / Fin de la période actuelle** — Les dates de la fenêtre de facturation active
- **Date de facturation suivante** — Lors de laquelle le prochain paiement sera tenté
- **Date de facturation précédente** et **Statut de la dernière facturation** — Résultat de l'essai de facturation le plus récent
- **Compteur de cycles de facturation** — Le nombre de cycles de facturation réussis terminés

### Informations sur l'abonnement

- **Plan** et **Niveau tarifaire** — Le plan et la fréquence de facturation auxquels le client appartient
- **Produit / Variante** — Le produit du catalogue lié à cet abonnement (si applicable)
- **Quantité** — Nombre de postes ou d'unités (pour les plans basés sur la quantité)
- **Jeton de paiement** — Le mode de paiement stocké utilisé pour les facturations récurrentes

### Détails de l'essai

Si l'abonnement est en essai, la **Date de fin de l'essai** indique quand l'essai du client expire et la facturation complète commence.

### Détails d'annulation

Pour les abonnements annulés, vous pouvez voir :

- **Type d'annulation** — Si l'annulation a été immédiate, à la fin de la période ou planifiée
- **Annulé le** — Lorsque l'annulation a été demandée
- **Raison d'annulation** — Notes sur la raison pour laquelle le client a annulé (si enregistrée)
- **Date limite de réactivation** — La dernière date à laquelle le client peut réactiver sans s'abonner à nouveau depuis le début

### Période de grâce et engagements

- **Date de fin de la période de grâce** — Si un paiement a échoué, cela affiche la date limite avant que l'accès ne soit suspendu
- **Date de fin de l'engagement minimum** — Pour les plans avec des engagements minimum, la date la plus tôt possible pour l'annulation

## Suspension d'un abonnement

Une suspension d'abonnement arrête temporairement les facturations tout en suspendant l'accès. Cela est utile pour les clients qui souhaitent prendre une pause sans annuler complètement.

Pour afficher les abonnements suspendus, filtrez par **Statut : Suspendu**. La vue détaillée affiche :

- **Suspendu le** — Lorsque la suspension a commencé
- **Raison de la suspension** — Notes sur la raison pour laquelle il a été suspendu
- **Date de reprise automatique** — Si définie, la date à laquelle l'abonnement reprendra automatiquement les facturations et l'accès

Les abonnements reprennent soit à la date de reprise automatique, soit lorsque le client réactive manuellement l'abonnement.

## Journal des cycles de facturation

Chaque tentative de facturation — réussie ou échouée — est enregistrée dans le journal des cycles de facturation. Accédez à **Subscriptions > Journal des cycles de facturation** pour consulter ce historique.

![Journal des cycles de facturation](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lire une entrée du journal des cycles de facturation

Chaque entrée de journal enregistre :

- **Abonnement** — À quel abonnement du client appartient cette tentative de facturation
- **Numéro de cycle** — Cycle de facturation séquentiel (Cycle 1 = première charge après l'essai)
- **Date de facturation** — Quand la charge a été tentée
- **Statut** — En attente, En cours, Réussie, Échouée ou Réessayer
- **Détail du montant** :
  - **Montant de base** — Le prix du plan avant toute ajustement
  - **Montant de la quantité** — Frais supplémentaires pour la quantité de sièges/unités
  - **Montant des compléments** — Coût total des compléments actifs
  - **Montant des remises** — Total des remises appliquées
  - **Montant total** — Le montant final facturé (ou tenté)
- **Méthode de paiement** — La carte ou la méthode de paiement utilisée
- **ID de transaction du fournisseur** — Le numéro de référence du fournisseur de paiement (utile pour les recherches de remboursement)
- **Raison de l'échec** — Si la facturation a échoué, pourquoi elle a échoué (ex. : carte refusée, fonds insuffisants)

### Diagnostiquer les échecs de paiement

Si un client vous contacte à propos d'un problème de facturation, trouvez son abonnement et vérifiez les journaux des cycles de facturation. Le champ **Raison de l'échec** explique ce qui s'est produit. Les raisons d'échec courantes incluent :

- **Carte refusée** — La carte du client a été refusée par leur banque
- **Fonds insuffisants** — Le solde du compte était trop bas au moment de la facturation
- **Carte expirée** — La méthode de paiement enregistrée a expiré
- **Erreur réseau** — Un problème temporaire de connexion avec le fournisseur de paiement — généralement résolu en réessayant

Pour les échecs persistants, orientez le client à mettre à jour sa méthode de paiement dans ses paramètres de compte.

## Conseils

- Vérifiez le filtre **En retard** hebdomadairement pour repérer les abonnements à risque de churn. Un courriel rapide au client résout souvent les problèmes de paiement avant l'expiration de la période de grâce.
- Les journaux des cycles de facturation sont en lecture seule — ils sont créés automatiquement et ne peuvent pas être modifiés. Cela garantit un historique d'audit fiable.
- Si un abonnement d'un client affiche **En retard** mais qu'il a déjà mis à jour sa méthode de paiement, la prochaine tentative automatique de réessai utilisera la nouvelle carte. Les réessais suivent le calendrier de période de grâce configuré dans le plan.
- Les abonnements **expirés** ne sont pas supprimés — ils restent visibles pour les rapports. Utilisez les filtres de date pour vous concentrer sur les abonnements actifs.
- Pour les abonnements en **Essai**, vérifiez la **Date de fin de l'essai** pour anticiper les premières charges à venir et résoudre proactivement tout problème de méthode de paiement.