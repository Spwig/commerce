---
title: Vue d'ensemble du système POS
---

Le système POS Spwig transforme votre magasin en une solution de commerce complet avec des terminaux de caisse modernes. Déployez des terminaux illimités dans des emplacements illimités pour un tarif d'abonnement plat de 499 € par an. Chaque terminal est une application Web Progressive (PWA) qui fonctionne hors ligne, synchronise automatiquement et s'intègre parfaitement à votre stock, vos données clients et votre traitement des paiements. Gérez tout depuis le tableau de bord d'administration : configuration des terminaux, conciliation des shifts, personnalisation des reçus et intégration matérielle.

Utilisez le système POS lorsque vous avez des emplacements de commerce physiques, des boutiques pop-up, des foires commerciales ou tout environnement où les clients achètent en personne plutôt qu'en ligne.

![Tableau de bord POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Qu'est-ce que Spwig POS ?

Spwig POS est un système de caisse entièrement intégré conçu pour les commerçants qui vendent à la fois en ligne et en magasin physique. Contrairement aux systèmes de caisse tiers qui nécessitent des intégrations complexes, Spwig POS est construit directement dans votre plateforme, assurant une synchronisation parfaite des données sur tous les canaux de vente.

**Caractéristiques clés**:
- **Terminals illimités** - Déployez autant de terminaux que nécessaire sans coût supplémentaire
- **Architecture priorisant le hors ligne** - Continue à traiter les ventes même en cas de perte de la connexion internet
- **Application Web Progressive** - Aucune installation depuis les magasins d'applications ; accès via le navigateur sur tout appareil (tablettes, ordinateurs, terminaux dédiés)
- **Synchronisation du stock réelle** - Les réservations de stock (TTL de 15 minutes) empêchent le survente sur les canaux
- **Prise en charge de la division des paiements** - Acceptez plusieurs méthodes de paiement par transaction (espèces + carte + carte cadeau)
- **Intégration matérielle** - Imprimantes thermiques ESC/POS, scanners de codes-barres, caisses enregistreuses, écrans clients
- **Gestion des shifts** - Conciliation de l'argent avec les comptages d'ouverture/fermeture et suivi des écarts
- **Prêt pour plusieurs emplacements** - Groupes de magasins avec héritage des paramètres pour la gestion de franchises et régionales

## Tarification et activation de la licence

**Tarification au forfait** : 499 € par an couvre les terminaux illimités à des emplacements illimités. Aucun frais par terminal, aucun frais de transaction, aucun coût caché.

**Format de licence** : `POS-XXXX-XXXX-XXXX-XXXX` (fourni après achat)

**Activation** : Entrez votre clé de licence dans **Paramètres > Licence POS**. Le système se valide avec le serveur de licence Spwig et active immédiatement toutes les fonctionnalités POS. Les licences comprennent une période de grâce de 14 jours après l'expiration pour permettre les retards de traitement des paiements.

**Ce que vous obtenez**:
- Enregistrement de terminaux illimités
- Attribution de personnel illimitée
- Toutes les fonctionnalités POS (shifts, gestion de l'argent, personnalisation des reçus, écrans clients)
- Intégrations des fournisseurs de paiement (Stripe Terminal et système extensible de fournisseurs)
- Support d'intégration matérielle
- Mises à jour et corrections de bugs pendant la période de licence

Aucune fonctionnalité POS n'est accessible sans une licence valide — l'interface de liaison des terminaux, la gestion des shifts et les pages d'administration POS nécessitent toutes l'activation.

## Architecture du système

**Frontend** - Application Web Progressive React 18:
- Priorité au mode hors ligne avec mise en cache via les workers de service (fonctionne sans internet)
- Système de construction Vite pour un chargement rapide
- Modules CSS + jetons de conception (cohérent avec votre thème de magasin)
- IndexedDB pour la persistance des données locales
- 10 langues prises en charge (anglais, chinois simplifié/traditionnel, français, allemand, espagnol, portugais, japonais, russe, arabe)

**Backend** - Intégration Backend:
- 13 modèles POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ points de terminaison REST pour les opérations de terminal
- Système de réservation de stock avec gestion du TTL
- Tâches Celery pour la synchronisation en arrière-plan
- Stockage chiffré des identifiants des fournisseurs de paiement

**Sécurité**:
- Association de terminal via des codes de 8 caractères (générés côté serveur, expire après utilisation)
- Contrôle d'affectation du personnel qui permet aux utilisateurs d'accéder aux terminaux
- Capacité de verrouillage/déverrouillage à distance en cas d'urgence administrative
- Identifiants chiffrés des fournisseurs de paiement
- Authentification basée sur les sessions avec prise en charge du déverrouillage biométrique (dépend du navigateur)

## Workflow pour commencer

Suivez ces 5 étapes pour déployer votre premier terminal POS : 

**Étape 1 : Activer la licence POS**
- Accédez à **Paramètres > Licence POS**
- Entrez votre clé de licence (`POS-XXXX-XXXX-XXXX-XXXX`)
- Validez la licence (nécessite une connexion internet)
- Confirmez l'activation

**Étape 2 : Créer un entrepôt**
- Accédez à **Catalogue > Entrepôts**
- Créez un entrepôt représentant votre emplacement de commerce
- Configurez l'adresse et les informations de contact
- Cet entrepôt suivra le stock physique pour les ventes POS

**Étape 3 : Enregistrer un terminal**
- Accédez à **POS > Terminaux**
- Cliquez sur **+ Ajouter un terminal**
- Définissez le nom du terminal (ex. : "Caisse principale", "Vente 1")
- Attribuez l'entrepôt créé à l'étape 2
- Configurez les paramètres matériels (imprimante, scanner, caisse enregistreuse)
- Enregistrez pour générer un code de liaison à 8 caractères

**Étape 4 : Attribuer du personnel**
- Dans la configuration du terminal, faites défiler jusqu'à **Utilisateurs attribués**
- Sélectionnez les employés autorisés à utiliser ce terminal
- Seuls les utilisateurs attribués peuvent se connecter au terminal
- Les utilisateurs doivent avoir les autorisations POS appropriées dans leur rôle d'employé

**Étape 5 : Associer l'appareil**
- Sur votre appareil terminal (tablette/ordinateur), accédez à l'URL `/pos/`
- Entrez le code de liaison à 8 caractères de l'étape 3
- Le terminal télécharge la configuration et synchronise les données initiales
- Connectez-vous avec les identifiants du personnel attribué
- Le terminal est prêt pour les ventes

Après l'association, les terminaux synchronisent automatiquement toutes les 5 minutes (configurable). Le mode hors ligne permet une opération continue lorsque l'internet n'est pas disponible — les ventes synchronisent automatiquement lors de la reconnexion.

## Fonctionnalités principales du POS

**Traitement des ventes**:
- Recherche de produit par nom, SKU ou code-barres
- Division des paiements (plusieurs méthodes de paiement par commande)
- Caddies mis en attente (enregistrez les transactions incomplètes)
- Remboursements et annulations avec suivi des raisons
- Application des remises (bons, cartes cadeaux, promotions)
- Recherche de client et rédemption des points de fidélité

**Gestion de l'argent**:
- Ouverture de shift avec décompte de l'argent initial
- Fermeture de shift avec conciliation prévue vs. réelle
- Mouvements d'argent (ajouts de trésorerie, retraits de trésorerie avec raisons)
- Calcul automatique de l'argent prévu en fonction des ventes en espèces
- Suivi et rapports d'écarts

**Intégration matérielle**:
- Imprimantes de reçus thermiques ESC/POS (réseau ou série)
- Scanners de codes-barres USB
- Déclencheur de caisse enregistreuse via un pulse d'imprimante
- Écrans destinés aux clients (carrousel promotionnel pendant l'inactivité)
- Liseurs de cartes Stripe Terminal (S700, WisePOS E, P400)

**Capacités hors ligne**:
- Worker de service met en cache tous les actifs du terminal
- IndexedDB stocke les commandes récentes (configurable : 7-30 jours, 200-1000 commandes)
- Réservations de stock avec TTL de 15 minutes empêchent le survente
- File d'attente des ventes pour synchronisation lors de la reconnexion
- Détection automatique de la reconnexion

## Pages d'administration POS

Accédez à ces pages d'administration pour gérer tous les aspects de votre déploiement POS : 

**Tableau de bord POS** (`/admin/pos/`)
- Aperçu du système et statistiques rapides
- Activité récente des terminaux
- Résumé des shifts actifs
- Statut de la licence et date d'expiration

**Gestion des terminaux** (`/admin/pos_app/posterminal/`)
- Enregistrer et configurer les terminaux
- Attribuer du personnel et des entrepôts
- Surveillance de l'état en ligne/hors ligne (suivi des battements de cœur)
- Déverrouiller à distance les terminaux
- [En savoir plus : Gestion des terminaux POS](managing-pos-terminals)

**Gestion des shifts** (`/admin/pos_app/posshift/`)
- Voir tous les shifts (ouverts, fermés, historiques)
- Vérifier les rapports de conciliation de l'argent
- Suivre les mouvements d'argent et les écarts
- Audit de l'activité des shifts
- [En savoir plus : Shifts POS et gestion de l'argent](pos-shifts-cash-management)

**Groupes de magasins** (`/admin/pos_app/storegroup/`)
- Organiser les terminaux par emplacement/région
- Configurer les paramètres au niveau du groupe (devise, langue, fuseau horaire)
- Implémenter une hiérarchie d'héritage des paramètres
- [En savoir plus : Groupes de magasins POS](pos-store-groups)

**Modèles de reçus** (`/admin/pos_app/receipttemplate/`)
- Personnaliser les reçus imprimés (largeur du papier, logo, en-tête/pied de page)
- Configurer les champs de conformité (ID de taxe, inscription commerciale)
- Ajouter des codes QR pour les promotions
- Définir des modèles pour des magasins ou des groupes spécifiques
- [En savoir plus : Personnalisation des modèles de reçus](receipt-template-customization)

**Diapositives promotionnelles** (`/admin/pos_app/promoslide/`)
- Créer du contenu de carrousel pour les écrans clients
- Cibler les diapositives pour des magasins ou des groupes spécifiques
- Planifier des promotions saisonnières
- [En savoir plus : Diapositives promotionnelles pour les écrans clients](customer-display-promo-slides)

**Fournisseurs de paiement** (`/admin/pos_app/posterminalprovider/`)
- Configurer l'intégration Stripe Terminal
- Gérer les identifiants des fournisseurs de paiement
- Surveiller l'état de la connexion
- [En savoir plus : Fournisseurs de terminaux de paiement](payment-terminal-providers)

**Liseurs de cartes** (`/admin/pos_app/posterminalreader/`)
- Enregistrer les lecteurs de cartes physiques
- Attribuer les lecteurs aux terminaux
- Personnaliser les écrans d'accueil (branding de l'écran client)
- Surveiller l'état du lecteur (en ligne/hors ligne/occupé)
- [En savoir plus : Gestion des lecteurs de cartes](card-reader-management)

## Déploiement multi-emplacement

Pour les commerçants avec plusieurs emplacements de commerce, Spwig POS prend en charge l'héritage hiérarchique des paramètres : 

**Hiérarchie des paramètres** (priorité la plus élevée à la plus basse) : 
1. Paramètres spécifiques au terminal (remplacement de tout)
2. Paramètres spécifiques au magasin (remplacement du groupe et du site)
3. Paramètres du groupe (remplacement des paramètres par défaut du site)
4. Paramètres par défaut du site (remplacement pour tout)

Configurez les paramètres partagés au niveau du groupe (ex. : devise régionale, langue) et remplacez-les comme nécessaire pour des magasins ou terminaux spécifiques. Voir [Groupes de magasins POS](pos-store-groups) pour des instructions détaillées de configuration.

## Conseils

- **Commencez par un seul terminal** - Testez la configuration POS et le workflow avec un seul terminal avant de déployer à l'échelle de la flotte
- **Assignez l'entrepôt avant de lier** - Les terminaux ne peuvent pas traiter les ventes sans une attribution d'entrepôt
- **Configurez les modèles de reçus tôt** - Les champs de conformité (IDs de taxe) varient par région ; configurez-les avant de mettre en ligne
- **Testez le mode hors ligne** - Désactivez internet et vérifiez que les ventes continuent ; confirmez la synchronisation lors de la reconnexion
- **Utilisez des groupes de magasins pour les déploiements multi-emplacement** - Simplifie la gestion des configurations pour les déploiements de franchises ou régionaux
- **Surveillez l'état des battements de cœur** - Les terminaux envoient un ping au serveur toutes les 5 minutes ; les terminaux hors ligne apparaissent dans le tableau de bord d'administration
- **Configurez des limites de synchronisation pour les performances** - Les terminaux avec des connexions lentes bénéficient de paramètres sync_days/sync_limit plus bas
- **Sauvegardez la configuration matérielle** - Documentez les adresses IP des imprimantes, les paramètres des scanners, la configuration de la caisse enregistreuse pour la récupération après sinistre

