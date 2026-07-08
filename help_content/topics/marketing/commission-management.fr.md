---
title: Gestion des commissions
---

La gestion des commissions est le processus de vérification et d'approbation des revenus des affiliés afin de s'assurer que seules les ventes légitimes sont créditées. Ce guide vous montre comment consulter les commissions en attente, approuver les valides, rejeter les commandes frauduleuses ou retournées, et gérer efficacement les commissions à l'aide d'actions en masse.

## Tableau de bord des commissions

Accédez à **Marketing > Commissions** pour accéder au tableau de bord de gestion des commissions.

Le tableau de bord fournit un aperçu de l'activité des commissions dans tous les programmes d'affiliation :

| Statistique | Description |
|-------------|-------------|
| **Commissions en attente** | Nombre de commissions en attente de votre vérification |
| **Commissions approuvées** | Commissions confirmées et prêtes au paiement |
| **Commissions payées** | Commissions qui ont été versées aux affiliés |
| **Commissions rejetées** | Commissions refusées en raison de fraude, de retours ou de violations des politiques |
| **Montant en attente de paiement** | Valeur totale des commissions approuvées mais non payées |

Ces statistiques vous aident à suivre votre charge de travail de vérification et à surveiller l'impact financier de votre programme d'affiliation.

![Tableau de bord des commissions](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Consultation des commissions

La liste des commissions affiche toutes les enregistrements de commissions dans l'ordre chronologique.

### Colonnes de la liste

| Colonne | Description |
|---------|-------------|
| **Affilié** | Nom et code unique de l'affilié |
| **Programme** | Le programme d'affiliation qui a généré cette commission |
| **Commande** | Numéro de commande (cliquez pour voir les détails complets de la commande) |
| **Montant** | Valeur de la commission en devise de votre magasin |
| **Statut** | En attente, Approuvée, Rejetée ou Payée |
| **Créé** | Lorsque la commission a été générée |

### Filtre des commissions

Utilisez la barre latérale de filtre pour affiner les commissions :

- **Par statut** — Afficher uniquement les commissions en attente, approuvées, rejetées ou payées
- **Par affilié** — Voir les commissions d'un partenaire spécifique
- **Par programme** — Voir les commissions d'un programme d'affiliation particulier
- **Par plage de dates** — Filtre par date de création

### Recherche de commissions

Utilisez la barre de recherche pour trouver des commissions spécifiques :

- Entrez un **numéro de commande** pour trouver une commission pour une vente spécifique
- Entrez un **code affilié** pour voir toutes les commissions d'un partenaire

## Détails des commissions

Cliquez sur une commission de la liste pour consulter ses détails complets.

### Champs de détail

La vue détaillée affiche :

- **Informations sur la commande** — Cliquez sur le numéro de commande pour consulter la commande complète dans un nouvel onglet, y compris les articles, l'adresse de livraison, le statut de paiement et les détails du client
- **Informations sur l'affilié** — Nom, code, adresse e-mail de paiement et statut d'appartenance au programme de l'affilié
- **Détails du programme** — Nom du programme, type de commission (pourcentage ou fixe), et taux de commission
- **Horodatages** — Date de création, date d'approbation/rejet et date de paiement
- **Section des notes** — Notes internes visibles uniquement par les marchands (expliqué ci-dessous)

Ces informations vous aident à vérifier la légitimité de la commission avant de l'approbation.

## Approbation des commissions

L'approbation d'une commission confirme qu'elle est valide et l'ajoute au solde disponible de l'affilié, la rendant éligible au paiement.

### Quand approuver

Approuvez les commissions lorsque :

- **La commande a été livrée avec succès** — Produit expédié ou biens numériques livrés
- **Aucun retour ou remboursement** — Le client n'a pas demandé de retour (considérez d'attendre 14 à 30 jours après la livraison)
- **Les normes de qualité sont respectées** — La vente respecte les termes de votre programme (par exemple, pas de self-referral, le client a utilisé une méthode de paiement authentique)
- **Aucune fraude détectée** — La commande passe le test de fraude (vérifiez l'IP, les incohérences entre l'adresse de facturation/livraison, les motifs d'ordre inhabituels)

### Comment approuver

**Approbation d'une commission unique :**

1. Accédez à **Marketing > Commissions**
2. Cliquez sur la commission que vous souhaitez approuver
3. Cliquez sur le bouton **Approuver** en haut de la page de détails
4. Ajoutez éventuellement une note (par exemple, "Approuvée après livraison réussie")
5. Le statut change en **Approuvée** et la commission est ajoutée au solde de l'affilié

**Approbation en masse :**

1. Accédez à **Marketing > Commissions**
2. Cochez les cases à côté des commissions que vous souhaitez approuver
3. Sélectionnez **Approuver les sélectionnées** dans le menu déroulant **Actions**
4. Cliquez sur **Go**
5. Toutes les commissions sélectionnées passent au statut **Approuvée**

Les commissions approuvées apparaissent dans le tableau de bord de l'affilié comme solde disponible et peuvent être incluses dans le prochain lot de paiement.

## Rejet des commissions

Le rejet d'une commission la retire du solde de l'affilié et la marque comme non éligible au paiement.

### Quand rejeter

Rejetez les commissions lorsque :

- **Commande frauduleuse** — La commande montre des signes de fraude (méthode de paiement volée, incohérence d'IP, affilié utilisant son propre lien)
- **Le client a retourné le produit** — Le client a retourné des articles pour un remboursement complet
- **Problèmes de qualité** — La vente ne respecte pas les termes du programme (par exemple, l'affilié a violé les directives de publicité)
- **Violation des termes** — L'affilié a utilisé des méthodes de promotion interdites (spams, enchères de marques, cookie stuffing)
- **Commande annulée** — Le client a annulé avant la livraison

### Comment rejeter

**Rejet d'une commission unique :**

1. Accédez à **Marketing > Commissions**
2. Cliquez sur la commission que vous souhaitez rejeter
3. Cliquez sur le bouton **Rejeter** en haut de la page de détails
4. **Ajoutez une note** expliquant la raison (très recommandé pour la résolution des litiges)
5. Le statut change en **Rejeté**

**Rejet en masse :**

1. Accédez à **Marketing > Commissions**
2. Cochez les cases à côté des commissions que vous souhaitez rejeter
3. Sélectionnez **Rejeter les sélectionnées** dans le menu déroulant **Actions**
4. Cliquez sur **Go**
5. Toutes les commissions sélectionnées passent au statut **Rejeté**

Les commissions rejetées sont retirées du solde de l'affilié et ne peuvent pas être payées. Elles restent visibles dans l'historique des commissions pour l'enregistrement.

## Actions en masse

Les actions en masse vous permettent d'approbation ou de rejeter plusieurs commissions à la fois, ce qui économise du temps lors du traitement de grands lots.

### Utilisation des actions en masse

1. Accédez à **Marketing > Commissions**
2. Filtrez la liste pour afficher uniquement les commissions que vous souhaitez traiter (par exemple, filtrez par statut **En attente**)
3. Cochez la case à côté de chaque commission, ou cliquez sur la case du titre pour sélectionner toutes les commissions de la page actuelle
4. Choisissez une action dans le menu déroulant **Actions** : 
   - **Approuver les sélectionnées** — Marquer toutes les commissions sélectionnées comme approuvées
   - **Rejeter les sélectionnées** — Marquer toutes les commissions sélectionnées comme rejetées
5. Cliquez sur **Go**
6. Vérifiez le message de confirmation indiquant combien de commissions ont été mises à jour

### Traitement en masse efficace

- **Filtrer par programme** — Approbation de toutes les commissions d'un affilié de confiance performant en une seule fois
- **Filtrer par plage de dates** — Traiter les commissions plus anciennes que 14 jours (après votre fenêtre de retour)
- **Réviser les hautes valeurs séparément** — Utilisez les actions en masse pour les petites commissions, révisez manuellement les grandes

## Notes des commissions

Le champ des notes vous permet de documenter vos décisions et de communiquer avec votre équipe.

### Ajout de notes

Les notes peuvent être ajoutées :

- **Lors de l'approbation** — Cliquez sur la commission, ajoutez une note dans le champ des notes, puis cliquez sur **Approuver**
- **Lors du rejet** — Ajoutez une note expliquant la raison du rejet
- **À tout moment** — Cliquez sur la commission, ajoutez ou modifiez la note dans le champ des notes, puis enregistrez

### Quand utiliser les notes

- **Commissions rejetées** — Documentez toujours la raison ("Le client a retourné la commande #12345 le 2/10/26")
- **Commissions de haute valeur** — Notez les étapes de vérification effectuées ("Vérification de la livraison via le numéro de suivi #ABC123")
- **Commissions contestées** — Documentez la communication avec l'affilié
- **Patterns de fraude** — Notez les activités suspectes pour référence future

Les notes sont **internes uniquement** — les affiliés ne peuvent pas les voir. Elles servent à votre outil de documentation.

## Flux des commissions

Voici le flux complet de gestion des commissions :

```
Commande passée → Commission créée (En attente)
                      ↓
              Marchand vérifie
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Approuvée     Rejetée
                ↓           ↓
        Prête pour le paiement  Non payable
                ↓
        Incluse dans le paiement
                ↓
              Payée
```

**Exemple de chronologie :**

- **Jour 1 :** Client passe une commande de 100 $ via un lien affilié → commission de 10 $ créée (En attente)
- **Jour 15 :** Commande livrée et fenêtre de retour expirée → Marchand approuve la commission
- **Jour 20 :** Marchand traite le lot de paiement mensuel → Statut de la commission change en Payée
- **Jour 21 :** Affilié reçoit le paiement via PayPal

## Bonnes pratiques

### Fenêtre de vérification

Établissez un horaire de vérification cohérent :

- **Vérifications quotidiennes** — Traitez les commissions en attente chaque matin (recommandé pour les programmes à fort volume)
- **Vérifications hebdomadaires** — Réservez du temps chaque lundi pour approuver les commissions de la semaine précédente
- **Vérifications bi-hebdomadaires** — Alignez-vous sur votre calendrier de paiement (approbation des commissions mi-mois, traitement des paiements fin de mois)

### Vérifications de qualité

Avant d'approbation des commissions, vérifiez :

1. **La commande est livrée** — Vérifiez le statut de la commande dans l'administration
2. **Le paiement est confirmé** — Vérifiez que la méthode de paiement a été traitée avec succès
3. **La fenêtre de retour est expirée** — Attendez 14 à 30 jours après la livraison pour tenir compte des retours
4. **Aucun drapeau de fraude** — Vérifiez la commande pour des motifs suspects (incohérence d'adresses, pays à risque, plusieurs commandes du même IP)
5. **Affilié en bonne standing** — Vérifiez l'historique de l'affilié pour des fraudes ou violations antérieures

### Prévention de la fraude

Surveillez ces signes rouges :

- **Auto-références** — L'affilié place des commandes en utilisant son propre lien de suivi
- **Cookie stuffing** — Ratio de conversion anormalement élevé avec des valeurs de commande basses
- **Commandes dupliquées** — Plusieurs commandes du même client/IP via le même lien affilié
- **Incohérences géolocalisées** — L'affilié basé dans le pays A génère des ventes exclusivement dans le pays B
- **Remboursements** — Taux élevé de remboursements sur les commandes référées par les affiliés

Si vous détectez de la fraude, **rejetez les commissions** et envisagez de terminer le membre du programme de l'affilié.

### Communication avec les affiliés

- **Fixez des attentes** — Documentez clairement votre politique d'approbation des commissions dans les termes du programme
- **Soyez transparent** — Si vous rejetez des commissions, envisagez d'envoyer un e-mail à l'affilié expliquant pourquoi (utilisez les notes comme référence)
- **Répondez aux contestations** — Si un affilié conteste un rejet, révisez les notes et les détails de la commande
- **Publiez des directives** — Créez une page "Politique d'approbation des commissions" sur votre portail affilié pour éviter les confusions

## Conseils

- Approbation des commissions **après la fermeture de votre fenêtre de retour** (généralement 14 à 30 jours) pour éviter d'approbation des commandes que les clients retournent plus tard
- Utilisez **des actions en masse avec des filtres** pour traiter efficacement les commissions des affiliés de confiance tout en révisant manuellement les nouveaux ou les affiliés à risque
- Documentez les raisons de rejet dans le **champ des notes** — cela vous protège si un affilié conteste la décision et vous aide à identifier les tendances
- Surveillez les **auto-références** — c'est une violation courante où les affiliés utilisent leurs propres liens pour gagner des commissions sur leurs propres achats
- Fixez un **seuil minimum d'approbation** — par exemple, approuvez automatiquement les commissions inférieures à 10 $ mais révisez manuellement tout ce qui dépasse 50 $ pour équilibrer l'efficacité et le risque
- Créez une **liste de vérification de fraude** — standardisez votre processus de vérification avec une liste de signes rouges (incohérences d'IP, motifs d'ordre suspects, méthodes de paiement à risque)
- Surveillez les **taux de rejet par affilié** — si un affilié a beaucoup de rejets, cela peut indiquer de la fraude ou un besoin de formation supplémentaire sur les termes du programme

Souvenez-vous : Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.