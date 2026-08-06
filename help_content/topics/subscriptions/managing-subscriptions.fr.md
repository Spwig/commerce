---
title: Gestion des abonnements clients
---

La section des abonnements clients vous donne une vue complète de tous les abonnements récurrents actifs, mis en pause et annulés dans votre magasin. Ici, vous pouvez surveiller l'état de la facturation, consulter les détails individuels d'un abonnement et intervenir en cas de problèmes.

## Visualisation des abonnements clients

Accédez à **Abonnements > Abonnements clients** pour voir la liste complète des abonnements de tous les clients.

![Liste des abonnements clients](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

La liste affiche chaque abonnement avec le client, le nom du forfait, le statut actuel, la date de prochaine facturation et le nombre de cycles de facturation terminés.

### Filtrage et recherche

Utilisez le panneau de filtre à droite pour réduire les abonnements par :

- **Statut** — Filtrez par Actif, Essai, Impayé, Mis en pause, Annulé ou Expiré
- **Forfait** — Affichez les abonnements pour un forfait spécifique
- **Mode du fournisseur** — Naturel (géré par Stripe/PayPal) ou Sauvegarde (facturation interne)

Utilisez la barre de recherche pour trouver des abonnements par adresse e-mail du client.

## Statuts d'abonnement

Comprendre chaque statut vous aide à identifier les abonnements nécessitant de l'attention :

| Statut | Ce que cela signifie |
|--------|--------------------|
| **Essai** | Le client est en période d'essai gratuite ou à prix réduit |
| **Actif** | L'abonnement est sain — la facturation est à jour et l'accès est actif |
| **Impayé** | Une tentative de paiement a échoué — le système réessaie. Le client conserve l'accès pendant la période de grâce |
| **Mis en pause** | L'abonnement est temporairement suspendu — pas de facturation, pas d'accès |
| **Annulé** | La demande d'annulation a été effectuée. Le client peut toujours avoir accès jusqu'à la date de fin de période |
| **Expiré** | L'abonnement s'est terminé complètement — l'essai a expiré, le nombre maximum de cycles de facturation a été atteint ou la période d'annulation est écoulée |

Les abonnements en **Impayé** nécessitent le plus d'attention — si le paiement continue d'échouer et que la période de grâce arrive à terme, l'abonnement sera suspendu.

## Visualisation des détails d'un abonnement

Cliquez sur n'importequel abonnement pour ouvrir la vue détaillée. Cela affiche :

### Période de facturation en cours

- **Date de début / fin de la période** — Les dates de la fenêtre de facturation active
- **Date de prochaine facturation** — Quand la prochaine tentative de facturation aura lieu
- **Date de dernière facturation** et **Statut de la dernière facturation** — Résultat de la dernière tentative de facturation
- **Nombre de cycles de facturation** — Combien de cycles de facturation ont été terminés avec succès

### Informations sur l'abonnement

- **Forfait** et **Niveau de tarification** — Le forfait et la fréquence de facturation sur lesquels le client est inscrit
- **Produit / Variante** — Le produit du catalogue lié à cet abonnement (le cas échéant)
- **Quantité** — Nombre de sièges ou d'unités (pour les forfaits basés sur la quantité)
- **Jeton de paiement** — La méthode de paiement stockée utilisée pour la facturation récurrente

### Détails de l'essai

Si l'abonnement est en essai, **Date de fin de l'essai** indique quand l'essai du client expire et que la facturation complète commence.

### Détails d'annulation

Pour les abonnements annulés, vous pouvez voir :

- **Type d'annulation** — Si l'annulation était immédiate, à la fin de la période, ou planifiée
- **Annulé à** — Quand l'annulation a été demandée
- **Raison de l'annulation** — Des notes sur la raison pour laquelle le client a annulé (le cas échéant)
- **Date limite de réactivation** — La dernière date à laquelle le client peut réactiver sans devoir s'abonner à nouveau

### Période de grâce et engagements

- **Date de fin de la période de grâce** — Si une facturation a échoué, cela indique le délai avant que l'accès ne soit suspendu
- **Date de fin de l'engagement minimum** — Pour les forfaits avec engagement minimum, la date la plus précoce de l'annulation

## Mise en pause d'un abonnement

Un abonnement mis en pause met temporairement un terme à la facturation tout en suspendant l'accès. Cela est utile pour les clients souhaitant prendre une pause sans annuler complètement.

Pour consulter les abonnements mis en pause, filtrez par **Statut : Mis en pause**. La vue détaillée affiche :

- **Mis en pause à** — Quand la mise en pause a commencé
- **Raison de la mise en pause** — Des notes sur la raison pour laquelle il a été mis en pause
- **Date de reprise automatique** — Si elle est définie, la date à laquelle l'abonnement reprendra automatiquement la facturation et l'accès

Les abonnements reprendront soit la date d'auto-reprise, soit lorsqu'un client les réactive manuellement.

## Journal des cycles de facturation

Chaque tentative de facturation - réussi ou échoué - est enregistré dans le journal des cycles de facturation. Accédez à **Abonnements > Journal des cycles de facturation** pour consulter cet historique.

![Liste du journal des cycles de facturation](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lecture d'une entrée du journal des cycles de facturation

Chaque entrée enregistre :

- **Abonnement** - Lequel des abonnements clients cette tentative de facturation appartient
- **Numéro de cycle** - Cycle de facturation séquentiel (Cycle 1 = premier paiement après l'essai)
- **Date de facturation** - À quelle date le paiement a-t-il été tenté
- **Statut** - En attente, En cours de traitement, Réussi, Échoué ou En cours de nouvelle tentative
- **Détail du montant** : 
  - **Montant de base** - Le prix du plan avant toute modification
  - **Montant de quantité** - Frais supplémentaires pour la quantité de sièges/unités
  - **Montant des accessoires** - Coût total des accessoires actifs
  - **Montant des remises** - Total des remises appliquées
  - **Montant total** - Le montant final facturé (ou tenté)
- **Mode de paiement** - La carte ou le mode de paiement utilisé
- **Identifiant de transaction du fournisseur** - Numéro de référence du fournisseur de paiement (utile pour les recherches de remboursement)
- **Raison de l'échec** - Si la facturation a échoué, pourquoi elle a échoué (exemple : carte refusée, fonds insuffisants)

### Diagnostic des échecs de paiement

Si un client vous contacte concernant un problème de facturation, trouvez son abonnement et vérifiez les journaux des cycles de facturation. Le champ **Raison de l'échec** explique ce qui ne va pas. Les raisons courantes d'échec comprennent :

- **Carte refusée** - La carte du client a été rejetée par sa banque
- **Fonds insuffisants** - Le solde du compte était trop faible au moment de la facturation
- **Carte expirée** - La méthode de paiement sauvegardée a expiré
- **Erreur réseau** - Un problème de connexion temporaire avec le fournisseur de paiement - généralement résolu lors d'une nouvelle tentative

Pour les échecs persistants, orientez le client vers la mise à jour de sa méthode de paiement dans ses paramètres de compte.

## Comment les renouvellements sont effectués

Chaque paiement de renouvellement réussi crée un nouveau bon de commande payé pour ce cycle de facturation - ce n'est pas seulement un enregistrement de paiement. Cet ordre suit votre processus de livraison normal, exactement comme un achat effectué lors de la caisse :

- **Produits physiques** - La commande de renouvellement entre dans la file de traitement habituelle pour le tri, l'emballage et l'expédition. Elle n'est pas automatiquement allouée en stock dès que la carte est chargée, donc un manque temporaire de stock ne bloque jamais un paiement qui a déjà réussi - vous verrez toujours la commande et pourrez la traiter en fonction des stocks disponibles.
- **Produits numériques** - L'accès (liens de téléchargement, clés de licence) est réattribué automatiquement dès la création de la commande de renouvellement, de la même manière qu'un achat pour la première fois.

Les commandes de renouvellement copient les coordonnées de livraison et de facturation de la commande qui a lancé l'abonnement, donc vous n'avez pas besoin de saisir à nouveau quoi que ce soit. Elles ne portent pas de badge spécial dans votre liste **Commandes**, mais vous pouvez toujours remonter un cycle spécifique à sa commande : ouvrez **Abonnements > Journal des cycles de facturation**, cliquez sur l'entrée du journal pour ce cycle, et le champ **Commande** y accède directement.

## E-mails de suivi des abonnements

Spwig envoie automatiquement des e-mails de suivi des abonnements - vous n'avez pas besoin de les déclencher manuellement. Ceux que les commerçants demandent le plus :

| E-mail | Quand il est envoyé |
|-------|------------------|
| **Rappel de renouvellement** | Avant un prochain paiement de renouvellement |
| **Fin de l'essai** | Avant qu'un essai gratuit ou à prix réduit ne passe à la facturation complète |
| **Échec de paiement** | Immédiatement après un échec de paiement de renouvellement, et à nouveau en tant que message final si la période de grâce est sur le point de s'achever (dunning) |
| **Confirmation de suppression** | Lorsqu'un abonnement est annulé |

Spwig envoie également des e-mails de bienvenue, de succès de paiement, de pause/reprise, d'expiration, de réactivation, de changement de forfait, et de fin de validité de la méthode de paiement aux moments pertinents dans le cycle de vie d'un abonnement.

Tous ces modèles de courriel sont ordinaires : consultez [Modèles de courriel](/help/email-templates) pour réviser ou personnaliser leur contenu et vérifier qu'ils sont actifs.

## Auto-service client

Les clients n'ont pas besoin de vous contacter pour des modifications de souscription courantes - ils peuvent gérer leurs propres abonnements depuis leur compte : consulter les détails et l'historique des factures, reporter, reprendre, annuler et mettre à jour la méthode de paiement enregistrée. Cela couvre la plupart des demandes qui atterriraient autrement dans votre file d'attente de support, donc lorsqu'un client contacte concernant son abonnement, il est utile de vérifier d'abord s'ils ont essayé la page de leur compte avant que vous ne fassiez le changement pour eux dans l'administration.

## Conseils

- Vérifiez la filtre **Impayé** hebdomadairement pour repérer les abonnements à risque de désabonnement. Un court courriel au client résout souvent les problèmes de paiement avant l'expiration de la période de grâce.
- Les journaux des cycles de facturation sont en lecture seule - ils sont créés automatiquement et ne peuvent pas être modifiés. Cela garantit une trace d'audit fiable.
- Si un abonnement client affiche **Impayé** mais qu'ils ont déjà mis à jour leur mode de paiement, le prochain essai automatique prendra en charge la nouvelle carte. Les tentatives suivantes suivent le calendrier de la période de grâce configuré dans le plan.
- Les abonnements **Expirés** ne sont pas supprimés - ils restent visibles pour les rapports. Utilisez les filtres de date pour vous concentrer sur les abonnements actifs actuellement.
- Pour les abonnements en **Essai**, vérifiez la **Date de fin de l'essai** pour anticiper les premières factures à venir et intervenez en amont pour tout problème lié à la méthode de paiement.
- Si un client dit qu'une rénovation physique « n'est pas partie », vérifiez votre file de traitement normal plutôt que le registre d'abonnement - les commandes de renouvellement sont traitées de la même manière qu'une autre commande et ne passent pas devant la file.