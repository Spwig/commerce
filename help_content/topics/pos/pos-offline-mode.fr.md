---
title: Mode hors ligne du POS & Installation de l'application
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA at rest — main login/terminal chooser view showing the Spwig POS branding
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) are OS/browser-specific
         annotated reference shots. The session capturing this should use device emulation
         or reference images rather than attempting to trigger the browser install prompt.
-->

Le Spwig POS est une Progressive Web App (PWA). Elle s'exécute entièrement dans le navigateur et peut être installée sur l'écran d'accueil d'un appareil comme une application native. Puisque l'application, votre catalogue de produits et l'historique des commandes récentes sont stockés localement sur l'appareil, votre caisse continue de fonctionner même en cas de courte interruption de réseau ou de connexion lente.

Ce sujet explique exactement ce qui fonctionne lorsque la connexion est perdue, comment les ventes en attente sont synchronisées lorsqu'elle revient, comment installer le POS sur l'écran d'accueil d'un appareil et comment les mises à jour atteignent les appareils installés.

## Fonctionnement du mode hors ligne

Lorsque vous ouvrez le POS pour la première fois sur un appareil, le navigateur télécharge et stocke en cache l'ensemble de l'application — son interface, ses images et tout le code de support. Un composant en arrière-plan appelé Service Worker gère ce cache. À partir de ce moment, l'application se charge à partir du cache local même si le serveur est inatteignable.

En plus du cache de l'application, le POS maintient une base de données locale sur l'appareil (en utilisant le stockage IndexedDB intégré au navigateur). Cette base de données contient :

- **Produits et variantes** — synchronisés à partir de votre catalogue et mis à jour toutes les cinq minutes en ligne
- **Catégories** — synchronisées au démarrage et mises à jour en même temps que les produits
- **Niveaux de stock** — synchronisés toutes les deux minutes en ligne (en utilisant une stratégie réseau-first qui recourt aux données en cache si le serveur ne répond pas dans les trois secondes)
- **Enregistrements clients** — jusqu'à 1 000 clients récents
- **Historique des commandes** — un nombre configurable de commandes récentes du POS (par défaut : 500 commandes sur 14 jours ; paramétrable par terminal dans **POS > Terminaux POS**)
- **Images de produits** — stockées localement pendant un maximum de 24 heures

Lorsque le POS détecte que l'appareil est hors ligne, un bandeau apparaît en haut de l'écran : **"Mode hors ligne - Les ventes seront synchronisées lorsque la connexion sera rétablie."** La caisse continue d'opérer en utilisant les données stockées localement.

## Fonctionnalités disponibles hors ligne

| Fonctionnalité | Disponibilité hors ligne |
|----------------|--------------------------|
| Recherche et navigation dans les produits | Disponible — utilise le catalogue stocké localement |
| Scannage de codes-barres | Disponible — les scans recherchent les produits dans le cache local |
| Ajout d'articles au panier | Disponible |
| Application de remises manuelles | Disponible |
| Application de codes-cadeaux | Non disponible — le vérification du solde nécessite une connexion active |
| Paiements en espèces | Disponible — enregistrés localement et mis en file d'attente pour la synchronisation |
| Paiements par carte (saisie manuelle) | Disponible — le caissier traite sur un terminal séparé et entre la référence ; enregistrés localement et mis en file d'attente pour la synchronisation |
| Paiements par carte (lecteur intégré — Stripe Terminal, etc.) | Non disponible — les lecteurs de carte intégrés communiquent en temps réel avec le réseau de paiement |
| Paiements par carte-cadeau | Non disponible — la vérification du solde nécessite une connexion active |
| Paiements combinés en espèces et carte manuelle | Disponible |
| Impression de reçus vers une imprimante réseau | Disponible si l'imprimante est sur le même réseau local que l'appareil — l'impression n'a pas besoin d'accès internet, uniquement la connectivité réseau locale |
| Reçus numériques (email/SMS/WhatsApp) | Non disponible — l'envoi nécessite une connexion active |
| Navigation dans l'historique des commandes | Disponible — affiche les commandes stockées avec un bandeau indiquant que vous consultez des données hors ligne |
| Remboursements et annulations | Non disponible — ces fonctionnalités nécessitent une connexion active |
| Vérification des points de fidélité client | Non disponible |
| Ouverture et fermeture des shifts | Disponible — l'état du shift est stocké localement |

## Ventes en attente et synchronisation lors du retour de la connexion

Les ventes hors ligne ne sont pas perdues.

Lorsque le terminal ne peut pas atteindre le serveur, chaque vente terminée est enregistrée dans une file d'attente locale (le stockage `pendingTransactions` de la base de données locale du dispositif).

La vente inclut tous les éléments du panier, les quantités, les prix, le mode de paiement et l'heure à laquelle elle a été terminée.

Lorsque l'accès à Internet est rétabli, le POS effectue automatiquement les opérations suivantes :

1. Détecte la reconnexion via l'événement `online` du navigateur
2. Affiche un bandeau : **"Synchronisation de N transaction(s) en attente..."**
3. Envoie les ventes en file d'attente au backend dans l'ordre, en utilisant un plan de réessai avec un écart exponentiel si la première tentative échoue (jusqu'à 10 réessais sur une fenêtre maximale de cinq minutes par tentative)
4. Marque chaque vente comme synchronisée une fois que le backend l'a confirmée

**Protection contre les doubles ventes** — chaque vente en file d'attente est attribuée un identifiant local unique avant de quitter le dispositif. Le backend vérifie cet identifiant avant de créer une commande. Si la même vente est soumise deux fois (par exemple, parce qu'un réessai s'est chevauché avec une première tentative réussie), le backend l'ignore. Vous ne finirez jamais avec des ventes comptées deux fois.

**Détection des conflits** — dans de rares cas, le backend peut signaler une vente en file d'attente comme un conflit (par exemple, si un produit a été supprimé côté serveur pendant que le dispositif était hors ligne). Les ventes en conflit apparaissent dans **POS > Paramètres > Transactions en attente** afin que vous puissiez les examiner et les résoudre manuellement.

**Ajustements de stock hors ligne** sont gérés de la même manière : les changements de stock effectués hors ligne sont mis en file d'attente et réappliqués lorsque la connexion est rétablie. Les chiffres de stock locaux sur le dispositif sont mis à jour immédiatement afin que le caissier voie un compte exact (estimé).

## Installation du POS sur l'écran d'accueil d'un dispositif

Installer le POS sur l'écran d'accueil vous permet d'avoir une expérience à l'écran plein, sans barre d'adresse du navigateur, un raccourci sur le dispositif et des temps de démarrage plus rapides.

### iPad (Safari)

1. Ouvrez Safari et accédez à l'URL du POS de votre magasin : `https://yourstore.com/pos/`
2. Connectez-vous et terminez le premier appairage si c'est un nouveau dispositif.
3. Appuyez sur le bouton **Partager** (le carré avec une flèche vers le haut) dans la barre d'outils de Safari.
4. Faites défiler vers le bas dans la fenêtre de partage et appuyez sur **Ajouter à l'écran d'accueil**.
5. Modifiez le nom si vous le souhaitez (il est par défaut "Spwig POS") et appuyez sur **Ajouter**.

L'icône du POS apparaît maintenant sur l'écran d'accueil de votre iPad. En la tapant, l'application s'ouvre à l'écran plein sans la barre du navigateur Safari.

> **Remarque :** Le bouton "Ajouter à l'écran d'accueil" est uniquement disponible sur Safari pour iPad. Les navigateurs tiers sur iOS (Chrome, Firefox) ne prennent pas en charge l'installation de PWA à partir de mi-2025.

### Android (Chrome)

1. Ouvrez Chrome et accédez à l'URL du POS de votre magasin : `https://yourstore.com/pos/`
2. Connectez-vous et terminez l'appairage si nécessaire.
3. Appuyez sur le **menu à trois points** (en haut à droite) et appuyez sur **Installer l'application** (ou **Ajouter à l'écran d'accueil** sur les anciennes versions de Chrome).
4. Confirmez en appuyant sur **Installer**.

L'icône du POS apparaît sur l'écran d'accueil et dans le menu des applications. Lancer depuis l'icône ouvre l'application en mode autonome.

### Ordinateur de bureau (Chrome ou Edge)

1. Accédez à l'URL du POS de votre magasin dans Chrome ou Edge.
2. Cherchez l'**icône d'installation** dans la barre d'adresse du navigateur (un écran d'ordinateur avec une flèche vers le bas, ou un icône "+" selon la version).
3. En alternative, ouvrez le **menu à trois points** et sélectionnez **Installer Spwig POS** (Chrome) ou **Apps > Installer ce site en tant qu'application** (Edge).
4. Confirmez l'installation.

Le POS s'ouvre en tant que fenêtre autonome sans onglets du navigateur ni barre d'adresse. Il apparaît dans la liste des applications de votre système et peut être fixé à la barre des tâches.

## Mise à jour de l'application

Le POS gère ses propres mises à jour via le Service Worker. Vous n'avez pas besoin de visiter un magasin d'applications ou de télécharger manuellement quelque chose.

**Cycle de mise à jour :**

1.

Chaque fois que vous ouvrez le POS (ou que l'onglet devient actif après avoir été en arrière-plan), le Service Worker vérifie le serveur à la recherche d'une nouvelle version.
2.

Si une nouvelle version est disponible, le Service Worker la télécharge en arrière-plan pendant que vous continuez à travailler — votre session actuelle n'est pas interrompue.
3.

La mise à jour prend effet la prochaine fois que vous ouvrez le POS.

Si l'application est déjà ouverte et qu'une synchronisation est en attente, le POS attend que la file d'attente se vide avant d'indiquer que le rechargement est prêt, afin d'éviter d'interrupter un shift actif avec des ventes non synchronisées.

**Ce que signifie "recharger" lorsque des ventes sont en attente** — si vous voyez un message vous demandant de recharger pour une mise à jour et que vous avez des ventes hors ligne en attente, clôturez proprement le shift en cours (ou attendez que le bandeau de synchronisation disparaisse) avant de recharger. Le rechargement pendant que des ventes sont en file d'attente ne les supprime pas — elles restent dans la base de données locale — mais il est plus sûr de synchroniser d'abord pour confirmer qu'elles ont été reçues.

**Vérifier la version installée** — ouvrez le POS, touchez l'**icône du menu** (trois lignes horizontales), puis allez dans **Paramètres**. La version actuelle du build est affichée en bas du panneau des paramètres.

## Stockage et suppression de l'installation

Le POS stocke plusieurs types de données localement :

| Quoi | Taille typique |
|------|-------------|
| Coque de l'application (HTML, CSS, JS, icônes) | ~3–5 Mo |
| Catalogue des produits (texte et métadonnées) | 1–10 Mo selon la taille du catalogue |
| Images des produits (en cache) | 5–50 Mo selon la taille du catalogue |
| Historique des commandes | 1–5 Mo (500 commandes) |
| Enregistrements clients | 1–3 Mo (1 000 clients) |
| File d'attente des transactions en attente | Minimale ; effacée lors de la synchronisation |

**Si l'appareil manque d'espace de stockage** — les navigateurs appliquent une pression sur le stockage en cache lorsque l'appareil est plein. Le POS définit ses caches comme persistants là où le navigateur le permet, mais sur des appareils très pleins, le navigateur peut supprimer d'abord les images de produits. Si les images ne se chargent plus, le POS les rechargera lors de la prochaine synchronisation. Les ventes synchronisées et la coque de l'application ne sont pas affectées.

**Réinitialiser l'installation** — si le POS se comporte de manière inattendue (bloqué sur une ancienne version, catalogue non actualisé, synchronisation bloquée définitivement), vous pouvez effectuer une réinitialisation propre :

1. **Désinstallez l'application** — sur mobile, appuyez et maintenez l'icône du POS et choisissez **Supprimer** ou **Désinstaller**. Sur le bureau, cliquez droit sur la barre de titre de la fenêtre de l'application et choisissez **Désinstaller**.
2. Ouvrez directement l'URL du POS dans le navigateur et reconnectez-vous.
3. L'appareil vous demandera à nouveau le code de pairage à 8 caractères du terminal. Vous pouvez trouver ou régénérer ce code dans l'admin à **POS > Terminaux POS** — ouvrez le terminal et cliquez sur **Régénérer le code de pairage**.
4. Une nouvelle paire force une synchronisation complète de toutes les données en cache.

> **Après la réinitialisation** : toutes les ventes hors ligne qui étaient en file d'attente mais pas encore synchronisées avant la réinitialisation seront perdues, car la base de données locale est effacée. Assurez-vous toujours que la connexion est rétablie et que le bandeau de synchronisation disparaît avant de réinitialiser une installation.

## Dépannage

### Le POS est bloqué sur une ancienne version

Le Service Worker n'a peut-être pas encore activé la nouvelle version. Essayez de fermer tous les onglets du navigateur qui ont le POS ouvert, puis rouvrez-le. Si le problème persiste, réinitialisez l'installation comme décrit ci-dessus.

### Le bandeau "Aucune connexion" ne disparaît pas

Vérifiez que l'appareil a un accès à Internet en dehors du POS (essayez de charger un autre site). Si l'appareil est en ligne mais que le bandeau persiste :

- Le serveur POS peut être temporairement inaccessible — attendez une minute et le POS tentera automatiquement à nouveau.
- Si vous êtes sur un réseau qui nécessite une page de connexion (portail captif), ouvrez un nouvel onglet de navigateur, complétez la connexion, puis revenez au POS.

### Un produit est absent du POS alors qu'il existe dans l'admin

Le POS synchronise les produits toutes les cinq minutes lorsqu'il est en ligne. Si vous avez ajouté un produit dans l'admin très récemment, touchez l'**icône du menu** et allez dans **Paramètres > Synchroniser maintenant** pour déclencher une synchronisation immédiate. Si le produit n'apparaît toujours pas, vérifiez qu'il est marqué comme **Actif** et qu'il n'est pas exclu de la disponibilité du POS dans les paramètres du produit.

### Les transactions en attente sont bloquées dans le statut "Conflit"

Allez dans **POS > Paramètres** (dans l'application POS elle-même) et vérifiez le panneau **Transactions en attente**.

Les transactions en conflit sont généralement causées par un produit ou un prix qui a changé entre le moment où la vente a été effectuée hors ligne et le moment où elle a été synchronisée.

Vous pouvez consulter les détails de la vente et, si la vente a été reçue correctement, la marquer comme examinée.

## Conseils

- Exécutez le POS sur un appareil dédié qui reste connecté à votre Wi-Fi local. Les interruptions brèves du Wi-Fi sont gérées automatiquement, mais un appareil qui passe de longues périodes hors ligne aura besoin de plus de temps pour se resynchroniser lorsqu'il se reconnectera.
- Les intervalles de synchronisation sont par appareil. Si vous avez plusieurs terminaux, chacun se synchronise indépendamment. Une vente sur un terminal apparaît immédiatement dans l'admin lors de la synchronisation, mais le cache des commandes locales de l'autre terminal ne se met à jour qu'à son propre cycle de synchronisation.
- Avant une coupure internet planifiée (par exemple, en passant à un événement sans Wi-Fi), ouvrez le POS tout en étant encore connecté afin que le catalogue et les données d'inventaire soient à jour. Les ventes en espèces seront mises en file d'attente de manière fiable ; évitez simplement les paiements par carte intégrés jusqu'à ce que vous soyez de nouveau en ligne.
- Si vous avez besoin uniquement de ventes en espèces à un événement, la méthode de paiement par carte manuelle (le caissier traite sur un terminal autonome et entre une référence) fonctionne également hors ligne pour les transactions par carte.
- Gardez l'appareil branché pendant une longue période de travail — la base de données locale et le processus de synchronisation n'ont pas un impact significatif sur la batterie par rapport à l'écran, mais un appareil chargé est toujours plus sûr pour le commerce.