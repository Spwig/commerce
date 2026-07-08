---
title: Traitement des paiements
---

Le traitement des paiements vous permet de payer les affiliés pour leurs commissions approuvées. Ce guide vous montre comment créer, gérer et traiter des paiements via PayPal ou des fournisseurs de virements bancaires.

![Liste des paiements](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Aperçu des paiements

Un paiement est un lot de paiement qui regroupe plusieurs commissions approuvées pour un seul affilié. Pensez-y comme un chèque pour tous les revenus impayés.

Caractéristiques clés:
- **Inclut plusieurs commissions** — Un paiement peut couvrir des dizaines de commissions approuvées
- **Nécessite un seuil minimum** — La plupart des programmes ont des montants minimum de paiement ($50-$100 typique)
- **Traité via des fournisseurs** — PayPal ou Airwallex gèrent effectivement le transfert d'argent
- **A un cycle de vie** — En attente → En traitement → Terminé (ou Échoué)

## Flux de paiement

Le processus complet de paiement suit six étapes:

1. **L'affilié génère des commissions** — Ventes attribuées aux liens de suivi des affiliés
2. **Le marchand approuve les commissions** — Réviser et approuver les commissions en attente
3. **Le solde atteint le minimum** — Le solde approuvé de l'affilié atteint le seuil du programme
4. **L'affilié demande un paiement** — L'affilié soumet une demande de paiement dans son tableau de bord
5. **Le marchand traite le paiement** — Vous créez et traitez le paiement
6. **Paiement terminé** — Le fournisseur envoie les fonds, les commissions sont marquées comme payées

## Afficher les paiements

Accédez à **Programme d'affiliation > Paiements** pour accéder au tableau de bord de gestion des paiements.

Le panneau de statistiques affiche:
- **En attente** — Paiements créés mais pas encore traités
- **En traitement** — Actuellement envoyés au fournisseur de paiement
- **Terminé** — Paiement réussi
- **Échoué** — Le paiement a échoué (nécessite une attention)

La vue en liste affiche:
- Nom et code de l'affilié
- Montant du paiement
- Méthode de paiement (PayPal ou Virement bancaire)
- Étiquette d'état
- Dates de création et de fin
- Boutons d'action

Utilisez des filtres pour affiner par:
- Affilié
- Méthode de paiement
- État
- Plage de dates

## Créer un paiement

Suivez ces étapes pour créer un nouveau paiement:

1. **Accédez à** **Programme d'affiliation > Paiements**
2. **Cliquez sur** le bouton **+ Ajouter un paiement**
3. **Sélectionnez l'affilié** dans le menu déroulant
4. **Vérifiez les commissions approuvées** — Le système affiche toutes les commissions non payées et approuvées pour cet affilié
5. **Sélectionnez les commissions à inclure** — Cochez les cases des commissions à payer (généralement toutes)
6. **Vérifiez le montant total** — Le système calcule automatiquement la somme
7. **Choisissez la méthode de paiement** — PayPal ou Virement bancaire (selon la préférence de l'affilié)
8. **Sélectionnez le compte du fournisseur** — Choisissez quel compte PayPal/Airwallex utiliser
9. **Ajoutez des notes** (facultatif) — Notes internes pour le suivi des dossiers
10. **Cliquez sur Enregistrer** — Le paiement est créé avec l'état "En attente"

Le paiement est maintenant prêt à être traité.

## Traitement des paiements

Vous avez deux options pour traiter les paiements : manuelle ou basée sur le fournisseur.

### Traitement manuel

Utilisez le traitement manuel lorsque vous gérez les paiements en dehors du système (chèques, virements, etc.) :

1. Sélectionnez le paiement dans la liste
2. Cliquez sur l'action **Marquer comme en traitement**
3. Terminez le paiement via votre méthode externe
4. Retournez au paiement
5. Cliquez sur l'action **Marquer comme terminé**
6. Les commissions sont automatiquement mises à jour en "Payées"

Le traitement manuel offre de la flexibilité mais nécessite plus de travail administratif.

### Traitement par fournisseur (Recommandé)

Le traitement par fournisseur automatise les paiements via PayPal ou Airwallex :

1. **Sélectionnez le(s) paiement(s)** dans la liste (vous pouvez traiter plusieurs)
2. **Cliquez sur** l'action **Traiter avec le fournisseur**
3. **Confirmez** dans la boîte de dialogue
4. **Le système met en file d'attente la tâche** — Le worker Celery gère l'appel API
5. **Le fournisseur traite le paiement**:
   - **PayPal** : Regroupe jusqu'à 15 000 paiements par demande
   - **Airwallex** : Virements bancaires individuels
6. **Le webhook met à jour l'état** — Le fournisseur confirme la fin
7. **Les commissions sont marquées comme payées** — Le système met à jour toutes les commissions incluses

Le traitement par fournisseur est plus rapide, plus fiable et crée un audit trail automatique.

## Méthodes de paiement

Spwig prend en charge deux méthodes de paiement avec des exigences différentes:

| Méthode | Fournisseur | Exigences | Temps de traitement | Frais | Meilleur pour |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | L'affilié doit avoir un `payment_email` valide | 1-2 jours ouvrés | ~2% ou $0,25-$1,00 par paiement | La plupart des affiliés, portée mondiale |
| **Virement bancaire** | Airwallex | Détails du compte bancaire (numéro de compte, routage, SWIFT) | 2-5 jours ouvrés | Varie selon le pays | Affiliés internationaux, montants importants |

Les affiliés configurent leur méthode de paiement et leurs détails dans leur tableau de bord. Le système sélectionne automatiquement le fournisseur approprié en fonction de leur préférence.

### Logique de sélection de la méthode de paiement

Lors du traitement d'un paiement, Spwig sélectionne le fournisseur comme suit:

1. Vérifiez la méthode de paiement préférée de l'affilié (PayPal ou Virement bancaire)
2. Correspondre à un compte de fournisseur configuré (PayPal → PayPal, Banque → Airwallex)
3. Revenir au premier fournisseur disponible si la préférence n'est pas disponible
4. Afficher une erreur si aucun fournisseur n'est configuré

## Flux d'état des paiements

Comprendre les états des paiements vous aide à suivre l'avancement des paiements:

| État | Signification | Prochaine action |
|--------|---------|-------------|
| **En attente** | Créé mais pas encore envoyé au fournisseur | Traiter avec le fournisseur ou marquer comme en traitement |
| **En traitement** | Soumis au fournisseur de paiement, en attente de confirmation | Attendez le webhook ou vérifiez le tableau de bord du fournisseur |
| **Terminé** | Paiement réussi, fonds envoyés | Aucune — les commissions sont marquées comme payées |
| **Échoué** | Paiement échoué (voir les détails d'erreur) | Vérifiez l'erreur, corrigez le problème, réessayez ou annulez |
| **Annulé** | Annulé manuellement avant la fin | Aucune — les commissions restent impayées |

### Chemin de succès

En attente → En traitement → Terminé

C'est le chemin idéal. Les webhooks du fournisseur mettent automatiquement à jour l'état à mesure que le paiement progresse.

### Chemin d'échec

En attente → En traitement → Échoué

Lorsqu'un paiement échoue, l'état du paiement change en Échoué et vous devez enquêter.

## Gestion des paiements échoués

Les paiements échoués nécessitent une intervention manuelle. Raisons courantes d'échec:

| Cause | Erreur du fournisseur | Solution |
|-------|--------------------------------|----------|
| Compte invalide | "Compte du destinataire non trouvé" | Vérifiez l'adresse e-mail de paiement ou les détails bancaires de l'affilié |
| Solde insuffisant | "Fonds insuffisants" | Ajoutez des fonds à votre compte du fournisseur |
| Erreur de détails bancaires | "Numéro de routage invalide" | Demandez à l'affilié de mettre à jour ses informations bancaires |
| Restriction de compte | "Le destinataire ne peut pas recevoir de paiements" | Contactez l'affilié pour résoudre son statut de compte |
| Problème du fournisseur | "Service temporairement indisponible" | Attendez et réessayez après quelques heures |

### Comment réessayer un paiement échoué

1. **Affichez le paiement échoué** — Cliquez dessus dans la liste
2. **Lisez le message d'erreur** — Vérifiez le champ **Réponse du fournisseur** pour les détails
3. **Corrigez le problème sous-jacent** — Mettez à jour les détails de l'affilié, ajoutez des fonds au fournisseur, etc.
4. **Réinitialisez l'état** — Changez l'état de nouveau en En attente (formulaire d'édition)
5. **Traitez à nouveau** — Utilisez l'action **Traiter avec le fournisseur**

### Comment annuler et recréer

Si le réessai ne fonctionne pas:

1. **Ouvrez le paiement échoué**
2. **Changez l'état en Annulé**
3. **Enregistrez le paiement**
4. **Créez un nouveau paiement** — Suivez à nouveau les étapes de création
5. **Traitez le nouveau paiement**

Les paiements annulés ne marquent pas les commissions comme payées, donc elles restent éligibles pour de nouveaux paiements.

## Intégration des fournisseurs de paiement

Le traitement des paiements nécessite un compte de fournisseur de paiement configuré. Spwig s'intègre avec:

- **API de paiement PayPal** — Pour les paiements PayPal
- **Airwallex** — Pour les virements bancaires internationaux

### Exigences de configuration

Avant de traiter des paiements:
1. Configurez au moins un fournisseur dans **Paramètres > Fournisseurs de paiement**
2. Ajoutez les identifiants API (ID client, Secret, Clé API)
3. Mettez en mode production (sandbox pour les tests)
4. Configurez l'URL du webhook dans le tableau de bord du fournisseur
5. Vérifiez la connectivité avec un paiement de test

Voir le guide [Configuration des fournisseurs de paiement](#) pour des instructions détaillées.

### Sélection du fournisseur par l'affilié

Les affiliés choisissent leur méthode de paiement préférée dans leur tableau de bord:
- PayPal: Entrez `payment_email`
- Virement bancaire: Entrez les détails du compte bancaire

Le système route automatiquement les paiements vers le fournisseur correspondant.

## Meilleures pratiques pour les horaires de paiement

Établissez un horaire régulier de paiement pour construire la confiance avec les affiliés:

| Horaires | Fréquence | Charge de travail | Satisfaction des affiliés | Recommandé pour |
|----------|-----------|----------|------------------------|-----------------|
| Hebdomadaire | Chaque vendredi | Élevée | Excellente | Programmes nouveaux, volume élevé |
| Bissemanuelle | 1er et 15e | Moyenne | Bonne | Programmes de volume moyen |
| Mensuel | 1er du mois | Faible | Acceptable | Programmes établis |
| Trimestriel | Tous les 3 mois | Très faible | Mauvaise | Non recommandé |

Tenez compte de la taille de votre programme et de votre capacité administrative lors du choix d'un horaire.

## Meilleures pratiques pour le traitement

Suivez ces directives pour des opérations de paiement fluides:

- **Groupez les paiements par horaire** — Traitez tous les paiements éligibles le même jour chaque semaine/mois
- **Vérifiez les détails avant le traitement** — Vérifiez à nouveau les informations de paiement de l'affilié, surtout pour les montants importants
- **Surveillez le solde du fournisseur** — Assurez-vous que votre compte PayPal/Airwallex a suffisamment de fonds
- **Définissez des seuils minimums clairs** — Communiquez les montants minimum de paiement dans les termes du programme ($50-$100 typique)
- **Documentez votre horaire** — Ajoutez l'horaire de paiement aux termes du programme et aux paramètres du portail
- **Utilisez le traitement par fournisseur** — Évitez le traitement manuel sauf si absolument nécessaire
- **Révisez immédiatement les paiements échoués** — Traitez les échecs dans les 24 heures
- **Maintenez les webhooks du fournisseur configurés** — Les webhooks permettent les mises à jour d'état automatiques
- **Exportez régulièrement les rapports de paiement** — Téléchargez les rapports mensuels pour la comptabilité

## Enregistrements de paiement et rapports

Chaque paiement crée un enregistrement immuable avec:
- Informations sur l'affilié
- Identifiants des commissions incluses
- Montant total
- Méthode et fournisseur de paiement
- Horodatages de création et de fin
- Identifiant de transaction du fournisseur (après traitement)
- Données de réponse du fournisseur (pour le débogage)
- Notes internes

Accédez à ces données en cliquant sur tout paiement dans la liste. Utilisez la fonction d'exportation de l'interface d'administration pour télécharger les rapports de paiement pour la comptabilité ou les impôts.

## Conseils

- Traitez les paiements sur un horaire fixe (par exemple, tous les vendredis à 14h) afin que les affiliés sachent quand s'attendre à un paiement.
- Utilisez toujours le traitement par fournisseur au lieu du traitement manuel — c'est plus rapide, plus fiable et crée de meilleures traces d'audit.
- Définissez des seuils minimums de paiement dans vos programmes pour réduire la charge administrative — $50 ou $100 est standard.
- Surveillez le solde de votre compte fournisseur avant de traiter des lots importants pour éviter les échecs.
- Testez votre intégration de paiement en mode sandbox avant de passer à des paiements réels.
- Ajoutez une note à chaque paiement expliquant la période qu'il couvre (par exemple, "Commissions pour janvier 2026").
- Vérifiez immédiatement les paiements échoués — les retards frustrent les affiliés et affectent la confiance.
- Communiquez proactivement les retards — si vous ne pouvez pas traiter à l'heure prévue, informez les affiliés concernés à l'avance.

