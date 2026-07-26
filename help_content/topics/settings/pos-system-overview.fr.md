---
title: Aperçu du système POS
---

Le système POS de Spwig transforme votre magasin en une solution de vente au détail complète grâce à des terminaux de caisse modernes. Il est inclus dans toutes les éditions — Communautaire, Pro et Entreprise — avec un nombre illimité de terminaux à travers un nombre illimité de lieux, sans coût supplémentaire. Chaque terminal est une application Web Progressive (PWA) qui fonctionne hors ligne, synchronise automatiquement et s'intègre parfaitement à votre inventaire, vos données clients et votre traitement des paiements. Gérez tout depuis le tableau de bord administrateur : configuration des terminaux, conciliation des shifts, personnalisation des reçus et intégration matérielle.

Utilisez le système POS lorsque vous avez des emplacements de vente au détail physiques, des boutiques éphémères, des foires commerciales ou tout environnement où les clients achètent en personne plutôt en ligne.

![Tableau de bord POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Qu'est-ce que Spwig POS ?

Spwig POS est un système de point de vente entièrement intégré conçu pour les commerçants qui vendent à la fois en ligne et en magasin physique. Contrairement aux systèmes de point de vente tiers qui nécessitent des intégrations complexes, Spwig POS est construit directement dans votre plateforme, assurant une synchronisation parfaite des données à travers tous les canaux de vente.

**Caractéristiques clés**:
- **Terminals illimités** - Déployez autant de terminaux que nécessaire sans coût supplémentaire
- **Architecture priorisant le hors ligne** - Continue à traiter les ventes même en cas de perte de connectivité internet
- **Application Web Progressive** - Aucune installation depuis un magasin d'applications ; accès via un navigateur sur tout appareil (tablettes, ordinateurs, terminaux dédiés)
- **Synchronisation de stock réelle** - Réservation de stock (TTL de 15 minutes) empêche le survente à travers les canaux
- **Prise en charge du paiement fractionné** - Acceptez plusieurs méthodes de paiement par transaction (espèces + carte + carte cadeau)
- **Intégration matérielle** - Imprimantes thermiques ESC/POS, scanners de codes-barres, caisses enregistreuses, écrans clients
- **Gestion des shifts** - Conciliation de trésorerie avec des comptages d'ouverture/fermeture et suivi des écarts
- **Prêt pour plusieurs emplacements** - Groupes de magasins avec héritage des paramètres pour la gestion de franchises et régionales

## Éditions

Le POS est inclus dans toutes les éditions de Spwig — Communautaire, Pro et Entreprise — à partir de Spwig 1.5.8. Il n'y a pas de licence POS séparée, pas d'étape d'activation et pas de frais par terminal.

**Ce qui est inclus dans chaque édition**:
- Enregistrement de terminaux illimités
- Attribution d'employés illimitée
- Toutes les fonctionnalités POS (shifts, gestion de trésorerie, personnalisation des reçus, écrans clients)
- Intégrations des fournisseurs de paiement (Stripe Terminal et autres fournisseurs pris en charge)
- Support d'intégration matérielle

Les commerçants qui utilisent des magasins hébergés par Spwig ou qui paient pour une licence Pro/Entreprise obtiennent des limites plus élevées pour les services hébergés par Spwig (GeoIP, géocodeur, notifications push) et un support prioritaire, mais l'ensemble des fonctionnalités POS est identique à travers les éditions.

## Architecture du système

**Frontend** - Application Web Progressive (PWA) React 18:
- Priorisation du hors ligne avec mise en cache via le Service Worker (fonctionne sans internet)
- Système de construction Vite pour un chargement rapide
- Modules CSS + tokens de design (cohérent avec le thème de votre magasin)
- IndexedDB pour la persistance des données locales
- 10 langues prises en charge (anglais, chinois simplifié/traditionnel, français, allemand, espagnol, portugais, japonais, russe, arabe)

**Backend** - Intégration backend:
- 13 modèles POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ points de terminaison REST pour les opérations de terminal
- Système de réservation de stock avec gestion du TTL
- Tâches Celery pour la synchronisation en arrière-plan
- Stockage chiffré des identifiants des fournisseurs de paiement

**Sécurité**:
- Association de terminal via des codes de 8 caractères (générés côté serveur, expire après utilisation)
- Contrôle de l'attribution des employés qui utilisent quels terminaux
- Capacité de verrouillage/déverrouillage à distance en cas d'urgence administrative
- Identifiants chiffrés des fournisseurs de paiement
- Authentification basée sur les sessions avec prise en charge du déverrouillage biométrique (dépend du navigateur)

## Workflow pour commencer

Suivez ces 4 étapes pour déployer votre premier terminal POS.

Pour obtenir une checklist étape par étape complète incluant la configuration du personnel, les fournisseurs de paiement et le lancement de votre première vente, consultez [Getting Started with POS](getting-started-with-pos).

**Étape 1 : Créer un entrepôt**
- Accédez à **Catalogue > Entrepôts**
- Créez un entrepôt représentant votre emplacement de vente au détail
- Configurez l'adresse et les informations de contact
- Cet entrepôt suivra l'inventaire physique pour les ventes en caisse

**Étape 2 : Enregistrer un terminal**
- Accédez à **POS > Terminaux**
- Cliquez sur **+ Ajouter un terminal**
- Définissez le nom du terminal (ex. : « Encaissement principal », « Caisse 1 »)
- Attribuez l'entrepôt de l'étape 2
- Configurez les paramètres matériels (imprimante, scanner, tiroir caisse)
- Enregistrez pour générer un code de pairage à 8 caractères

**Étape 3 : Attribuer du personnel**
- Dans la configuration du terminal, faites défiler jusqu'à **Utilisateurs attribués**
- Sélectionnez les membres du personnel autorisés à utiliser ce terminal
- Seuls les utilisateurs attribués peuvent se connecter au terminal
- Les utilisateurs doivent avoir les autorisations POS appropriées dans leur rôle de personnel

**Étape 4 : Pairez le dispositif**
- Sur votre appareil terminal (tablette/ordinateur), accédez à l'URL `/pos/`
- Entrez le code de pairage à 8 caractères de l'étape 3
- Le terminal télécharge la configuration et synchronise les données initiales
- Connectez-vous avec les identifiants du personnel attribué
- Le terminal est prêt pour les ventes

Après la paire, les terminaux synchronisent automatiquement toutes les 5 minutes (configurable). Le mode hors ligne permet une utilisation continue lorsque l'internet n'est pas disponible — les ventes synchronisent automatiquement lorsque la connectivité revient.

## Fonctionnalités principales de POS

**Traitement des ventes**:
- Recherche de produit par nom, SKU ou code-barres
- Paiement fractionné (plusieurs méthodes de paiement par commande)
- Paniers mis en attente (enregistrez les transactions incomplètes)
- Remboursements et annulations avec suivi des raisons
- Application de réductions (bons, cartes cadeaux, promotions)
- Recherche de client et utilisation des points de fidélité

**Gestion de trésorerie**:
- Ouvrir un shift avec un décompte de trésorerie initial
- Fermer un shift avec un rapprochement entre prévu et réel
- Mouvements de trésorerie (ajouts de trésorerie, retraits de trésorerie avec motif)
- Calcul automatique de la trésorerie prévue en fonction des ventes en espèces
- Suivi et rapports de déséquilibres

**Intégration matérielle**:
- Imprimantes de reçus thermiques ESC/POS (réseau ou série)
- Scanners de codes-barres USB
- Déclenchement du tiroir caisse via un signal d'imprimante
- Écrans destinés aux clients (carrousel promotionnel pendant l'inactivité)
- Liseurs de cartes Stripe Terminal (S700, WisePOS E, P400)

**Fonctionnalités hors ligne**:
- Le Service Worker stocke toutes les ressources du terminal en cache
- IndexedDB stocke les commandes récentes (configurable : 7 à 30 jours, 200 à 1000 commandes)
- Réservations d'inventaire avec un TTL de 15 minutes empêchent le survente
- File d'attente des ventes pour la synchronisation lors de la reprise de la connectivité
- Détection automatique de la reconnexion

## Pages d'administration POS

Accédez à ces pages d'administration pour gérer tous les aspects de votre déploiement POS :

**Tableau de bord POS** (`/admin/pos/`)
- Aperçu du système et statistiques rapides
- Activité récente des terminaux
- Résumé des shifts actifs
- Tuiles d'utilisation des services hébergés (GeoIP, géocodeur, push — voir [Spwig Hosted Services](hosted-services))

**Gestion des terminaux** (`/admin/pos_app/posterminal/`)
- Enregistrer et configurer les terminaux
- Attribuer du personnel et des entrepôts
- Surveiller l'état en ligne/hors ligne (suivi des battements de cœur)
- Désbloquer à distance les terminaux
- [En savoir plus : Gestion des terminaux POS](managing-pos-terminals)

**Gestion des shifts** (`/admin/pos_app/posshift/`)
- Afficher tous les shifts (ouverts, fermés, historiques)
- Vérifier les rapports de rapprochement de trésorerie
- Suivre les mouvements de trésorerie et les déséquilibres
- Audit de l'activité des shifts
- [En savoir plus : Shifts POS et gestion de trésorerie](pos-shifts-cash-management)

**Groupes de magasins** (`/admin/pos_app/storegroup/`)
- Organiser les terminaux par emplacement/région
- Configurer les paramètres au niveau du groupe (devise, langue, fuseau horaire)
- Implémenter une hiérarchie d'héritage des paramètres
- [En savoir plus : Groupes de magasins POS](pos-store-groups)

**Modèles de reçus** (`/admin/pos_app/receipttemplate/`)
- Personnalisez les reçus imprimés (largeur du papier, logo, en-tête/pied de page)
- Configurez les champs de conformité (numéro d'identification fiscale, inscription commerciale)
- Ajoutez des codes QR pour les promotions
- Définissez la portée des modèles pour des magasins ou des groupes spécifiques
- [En savoir plus : Personnalisation des modèles de reçus](receipt-template-customization)

**Diapositives promotionnelles** (`/admin/pos_app/promoslide/`)
- Créez du contenu de carrousel pour les écrans clients
- Ciblez les diapositives pour des magasins ou des groupes spécifiques
- Planifiez des promotions saisonnières
- [En savoir plus : Diapositives promotionnelles pour écrans clients](customer-display-promo-slides)

**Fournisseurs de paiement** (`/admin/pos_app/posterminalprovider/`)
- Configurez l'intégration Stripe Terminal
- Gérez les identifiants des fournisseurs de paiement
- Surveillez l'état de la connexion
- [En savoir plus : Fournisseurs de terminaux de paiement](payment-terminal-providers)

**Lecteurs de cartes** (`/admin/pos_app/posterminalreader/`)
- Enregistrez les lecteurs de cartes physiques
- Attribuez des lecteurs aux terminaux
- Personnalisez les écrans d'accueil (branding de l'écran client)
- Surveillez l'état du lecteur (en ligne/hors ligne/occupé)
- [En savoir plus : Gestion des lecteurs de cartes](card-reader-management)

## Déploiement multi-sites

Pour les commerçants ayant plusieurs emplacements de vente, Spwig POS prend en charge l'héritage hiérarchique des paramètres :

**Hiérarchie des paramètres** (priorité la plus élevée à la plus basse) :
1. Paramètres spécifiques au terminal (remplacement de tout)
2. Paramètres spécifiques au magasin (remplacement du groupe et du site)
3. Paramètres du groupe (remplacement des paramètres par défaut du site)
4. Paramètres par défaut du site (valeur par défaut pour tous)

Configurez les paramètres partagés au niveau du groupe (ex. devise régionale, langue) et remplacez-les si nécessaire pour des magasins ou terminaux spécifiques. Consultez [Groupes de magasins POS](pos-store-groups) pour obtenir des instructions détaillées de configuration.

## Conseils

- **Commencez par un seul terminal** - Testez le setup POS et le workflow avec un seul terminal avant de déployer à l'échelle de la flotte
- **Affectez un entrepôt avant de paire** - Les terminaux ne peuvent pas traiter des ventes sans une affectation d'entrepôt
- **Configurez les modèles de reçus tôt** - Les champs de conformité (numéros d'identification fiscale) varient selon la région ; configurez-les avant de mettre en ligne
- **Testez le mode hors ligne** - Désactivez Internet et vérifiez que les ventes continuent ; confirmez la synchronisation lors de la reconnexion
- **Utilisez des groupes de magasins pour les déploiements multi-sites** - Simplifie la gestion des configurations pour les déploiements en franchise ou régionaux
- **Surveillez l'état du battement cardiaque** - Les terminaux envoient un ping au serveur toutes les 5 minutes ; les terminaux hors ligne apparaissent dans le tableau de bord administrateur
- **Configurez des limites de synchronisation pour les performances** - Les terminaux avec des connexions lentes bénéficient de paramètres sync_days/sync_limit plus bas
- **Sauvegardez la configuration matérielle** - Documentez les adresses IP des imprimantes, les paramètres des scanners, la configuration du tiroir caisse pour la récupération en cas de catastrophe