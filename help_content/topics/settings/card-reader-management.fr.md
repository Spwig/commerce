---
title: Gestion des lecteurs de carte
---

La gestion des lecteurs de carte suit les appareils physiques de matériel de paiement, les affecte aux terminaux de caisse et surveille leur état opérationnel. Chaque lecteur de carte représente un matériel réel (Stripe S700, WisePOS E ou P400) enregistré auprès de votre fournisseur de paiement. Les lecteurs ont une relation un-à-un avec les terminaux - chaque caisse a son propre lecteur de carte. Surveillez l'état du lecteur (en ligne, hors ligne, occupé) en temps réel, personnalisez les écrans d'accueil avec votre branding, et résolvez les problèmes de connectivité avant qu'ils n'affectent l'expérience de paiement des clients.

Utilisez la gestion des lecteurs de carte pour vous assurer que le matériel de paiement est correctement configuré, affecté et opérationnel dans toutes les locations.

![Liste des lecteurs de carte](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Comprendre les lecteurs de carte

Les lecteurs de carte sont des appareils physiques qui traitent les paiements par carte de crédit et de débit:

**Composants matériels**:
- Emplacement pour carte à puce EMV
- Antenne NFC (sans contact/payer en tapant)
- Liseur de bande magnétique (héritage, rarement utilisé)
- Écran d'affichage (affiche le montant, demande le code PIN, la signature)
- Connectivité réseau (Wi-Fi ou Ethernet, selon le modèle)

**Intégration logicielle**:
- Les lecteurs se connectent à l'API Stripe Terminal (basée en cloud, pas de connexion directe au terminal de caisse)
- Le terminal de caisse demande un paiement via l'API
- Stripe route la demande vers le lecteur enregistré
- Le lecteur traite la carte et renvoie le résultat au terminal de caisse
- Aucune connexion USB/Bluetooth nécessaire entre le terminal de caisse et le lecteur

**Un lecteur par terminal**:
- Chaque terminal de caisse doit avoir exactement un lecteur de carte affecté
- La relation un-à-un garantit une responsabilité claire et un dépannage simplifié
- Plusieurs terminaux ne peuvent pas partager un seul lecteur (causes des conflits)

## Types de lecteurs de carte

Spwig POS prend en charge les lecteurs de carte Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Terminal Android tout-en-un avec écran tactile couleur de 5"
- Option d'imprimante intégrée (reçu thermique)
- Idéal pour: caisse de détail complète, restaurants (demandes de pourboires sur l'écran couleur)
- Connectivité: Wi-Fi uniquement
- Écran d'accueil: couleur complète 480×800 portrait

**Stripe Reader S700** (`stripe_s700`):
- Lecteur de comptoir avec écran LCD monochrome
- Design compact, résistant à l'eau
- Idéal pour: détail standard, comptoirs de caisse compacts
- Connectivité: Wi-Fi ou Ethernet
- Écran d'accueil: monochrome 480×800 portrait

**Verifone P400** (`verifone_p400`):
- Lecteur de comptoir héritage (modèle plus ancien)
- Toujours pris en charge mais non recommandé pour les nouvelles déploiements
- Idéal pour: déploiements existants (ne remplacez pas le matériel fonctionnel)
- Connectivité: Wi-Fi ou Ethernet
- Écran d'accueil: monochrome 480×800 portrait

**Compatibilité future**:
- D'autres modèles de lecteurs peuvent être ajoutés à mesure que Stripe Terminal étend ses offres matérielles
- Le menu déroulant du type de lecteur se remplit automatiquement à partir des capacités du fournisseur

## Workflow d'enregistrement du lecteur

**Étape 1: Acheter et recevoir le matériel**
- Commandez le lecteur auprès de Stripe (stripe.com/terminal) ou d'un revendeur autorisé
- Déméquillez et allumez le lecteur
- Connectez-vous au réseau Wi-Fi (suivez la configuration à l'écran du lecteur)

**Étape 2: Enregistrer dans le tableau de bord Stripe**
- Accédez à **Tableau de bord Stripe > Terminal > Lecteurs**
- Cliquez sur **Enregistrer un nouveau lecteur**
- Suivez le processus de liaison à l'écran (le lecteur affiche le code d'enregistrement)
- Affectez le lecteur à une localisation Stripe (doit correspondre à la localisation dans la configuration du fournisseur de paiement)
- Notez l'**ID du lecteur** (ressemble à `tmr_ABC123...`)

**Étape 3: Synchronisation avec Spwig (automatique)**
- Spwig détecte automatiquement les lecteurs enregistrés à votre localisation Stripe
- Une tâche en arrière-plan synchronise toutes les 30 minutes
- Les nouveaux lecteurs apparaissent dans la liste **POS > Lecteurs de carte** dans les 30 minutes

**Étape 4: Affecter à un terminal (manuelle)**
- Accédez à **POS > Lecteurs de carte**
- Trouvez le nouveau lecteur détecté dans la liste
- Cliquez pour éditer
- Sélectionnez **Terminal** pour affecter le lecteur
- Enregistrez

**Étape 5: Tester le paiement**
- Au terminal de caisse, effectuez une transaction de test
- Sélectionnez le mode de paiement par carte
- Le POS doit détecter le lecteur affecté
- Utilisez la carte de test Stripe (4242 4242 4242 4242) pour terminer le test
- Vérifiez que le paiement s'achève avec succès

Si le lecteur n'apparaît pas lors du test, vérifiez l'affectation du terminal et l'état du lecteur.

## Surveillance de l'état du lecteur

Les lecteurs signalent leur état à l'API Stripe Terminal, que Spwig synchronise toutes les 5 minutes:

**En ligne** (vert) - Le lecteur est allumé, connecté au réseau et prêt à accepter les paiements

**Hors ligne** (rouge) - Le lecteur est éteint, déconnecté du réseau ou inatteignable

**Occupé** (jaune) - Le lecteur traite actuellement une transaction de paiement

**Dernière connexion** - Horodatage de la dernière vérification du lecteur avec l'API Stripe
- Mises à jour toutes les ~2 minutes lorsque le lecteur est en ligne
- Utile pour diagnostiquer les problèmes de connectivité (« le lecteur est hors ligne depuis 3 heures » = problème d'alimentation ou de réseau pendant les heures d'ouverture)

**Cas d'utilisation de l'état**:
- **Vérification pré-ouverture** : Vérifiez que tous les lecteurs du magasin sont en ligne avant d'ouvrir les portes
- **Dépannage** : « Le registre 3 n'accepte pas les cartes » → Vérifiez l'état du lecteur → Affiche hors ligne → Vérifiez l'alimentation/réseau
- **Audit** : « Les paiements ont-ils été traités au Terminal 5 hier ? » → Vérifiez l'horodatage de la dernière connexion

## Affectation du terminal

Les lecteurs de carte utilisent une **relation un-à-un** avec les terminaux:

**Pourquoi l'affectation compte**:
- Pendant le paiement, le POS doit savoir à quel lecteur communiquer
- Plusieurs terminaux partageant un seul lecteur causent des conflits (deux caissières ne peuvent pas utiliser le même lecteur en même temps)
- Les lecteurs non affectés ne seront pas utilisés (matériel orphelin)

**Règles d'affectation**:
- Chaque terminal peut avoir **exactement un** lecteur de carte affecté
- Chaque lecteur de carte peut être affecté à **exactement un** terminal
- Affecter un lecteur au Terminal A le désaffecte automatiquement du terminal précédent

**Changement d'affectation**:
- Éditez le dossier du lecteur
- Modifiez le champ **Terminal** pour le nouveau terminal
- Enregistrez
- Le terminal précédent perd l'affectation du lecteur (affichera l'erreur « Aucun lecteur affecté » pendant le paiement)

**Lecteurs non affectés**:
- Les nouveaux lecteurs détectés commencent non affectés
- Les lecteurs non affectés apparaissent dans la liste mais ne sont pas utilisables
- Affectez-les à un terminal pour les activer

## Personnalisation de l'écran d'accueil

Les écrans d'accueil des lecteurs affichent le branding sur l'écran face client lorsqu'ils sont inactifs:

**Qu'est-ce qu'un écran d'accueil ?**
- Image affichée sur l'écran du lecteur lorsqu'il ne traite pas un paiement
- Remplace le logo Stripe par défaut par votre branding
- Visible par les clients pendant l'attente au caisse

**Écran d'accueil généré automatiquement vs personnalisé**:

**Écran d'accueil généré automatiquement** (par défaut):
- Spwig génère l'écran d'accueil à partir de votre logo de magasin (si le logo est configuré dans les paramètres du magasin)
- Taille automatiquement adaptée aux spécifications du lecteur (480×800 portrait)
- Noir et blanc pour S700/P400, couleur pour WisePOS E
- Aucune configuration nécessaire

**Écran d'accueil personnalisé** (avancé):
- Téléchargez votre propre image conçue pour l'écran d'accueil
- Contrôle total sur la conception et le branding
- Doit respecter les exigences d'image (voir ci-dessous)

**Exigences pour l'écran d'accueil personnalisé**:
- **Résolution** : Exactement 480×800 pixels (orientation portrait)
- **Format** : PNG ou JPG
- **S700/P400** : Noir et blanc uniquement (noir et blanc, pas de gris)
- **WisePOS E** : Couleurs complètes prises en charge
- **Taille du fichier** : <200KB

**Paramétrage de l'écran d'accueil personnalisé**:
1. Éditez le dossier du lecteur de carte
2. Téléchargez une image dans le champ **Image de remplacement de l'écran d'accueil** (ou sélectionnez-la dans la bibliothèque multimédia)
3. Enregistrez
4. L'écran d'accueil est synchronisé avec le lecteur dans les 5 minutes

**Suppression de l'écran d'accueil personnalisé**:
- Effacez le champ **Image de remplacement de l'écran d'accueil**
- Enregistrez
- Le lecteur revient à l'écran d'accueil généré automatiquement (ou au logo Stripe par défaut si aucun logo de magasin n'est configuré)

**Test de l'écran d'accueil**:
- Après le téléchargement, attendez 5 minutes pour la synchronisation
- Visitez l'appareil lecteur
- Vérifiez que l'écran d'accueil apparaît sur l'écran inactif
- Vérifiez la qualité de l'image, le centrage et le contraste

## Configuration de l'écran d'accueil Stripe

En coulisses, Spwig gère la configuration de l'écran d'accueil Stripe Terminal:

**stripe_splash_file_id** - ID interne Stripe pour le fichier d'image d'écran d'accueil téléchargé
- Automatiquement défini lors du téléchargement de l'écran d'accueil
- Utilisé pour référencer l'écran d'accueil dans l'API Stripe

**stripe_splash_config_id** - ID interne Stripe pour la configuration de l'écran d'accueil
- Relie le fichier d'écran d'accueil au lecteur
- Géré automatiquement lors de l'affectation de l'écran d'accueil au lecteur

Ces champs sont en lecture seule et gérés automatiquement - vous n'avez pas besoin d'interagir avec eux directement.

## Dépannage des problèmes courants

**Problème 1: Le lecteur affiche hors ligne mais est allumé**
- **Causes** : Problème de connectivité réseau, mot de passe Wi-Fi changé, lecteur hors de portée
- **Solution** : Vérifiez les paramètres réseau du lecteur, reconnectez-vous au Wi-Fi, vérifiez que l'API Stripe est accessible depuis le réseau

**Problème 2: Le POS affiche « Aucun lecteur affecté » pendant le paiement**
- **Cause** : Lecteur non affecté à un terminal, ou affectation incomplète
- **Solution** : Éditez le lecteur, affectez-le à un terminal, enregistrez, testez à nouveau le paiement

**Problème 3: Le lecteur reste occupé indéfiniment (bloqué à l'écran de paiement)**
- **Cause** : Transaction expirée ou plantée, état du lecteur non réinitialisé
- **Solution** : Redémarrez le lecteur (cycle d'alimentation), contactez le support Stripe si le problème persiste

**Problème 4: L'écran d'accueil personnalisé n'apparaît pas**
- **Causes** : Image de mauvaise résolution, non synchronisée encore, exigence de noir et blanc non respectée (S700/P400)
- **Solution** : Vérifiez que l'image est exactement 480×800, attendez 5 minutes pour la synchronisation, assurez-vous qu'elle est en noir et blanc pour les lecteurs non colorés

**Problème 5: Le lecteur est enregistré dans Stripe mais n'apparaît pas dans Spwig**
- **Cause** : Le lecteur est enregistré à une localisation Stripe différente de celle de la configuration du fournisseur
- **Solution** : Dans le tableau de bord Stripe, vérifiez que la localisation du lecteur correspond à l'ID de localisation du fournisseur

## Conseils

- **Un lecteur par terminal** - Ne partagez pas les lecteurs entre terminaux ; cela empêche les conflits et simplifie la responsabilité
- **Enregistrez les lecteurs avant de les déployer** - Terminez l'enregistrement Stripe et l'affectation Spwig avant de placer le lecteur à la caisse
- **Testez les écrans d'accueil en magasin** - La luminosité varie selon le modèle de lecteur et l'éclairage ; vérifiez que l'écran d'accueil a l'air bon dans l'environnement réel
- **Surveillez l'état avant l'ouverture** - Vérifiez la liste des lecteurs chaque matin pour vous assurer que tous les lecteurs sont en ligne avant l'ouverture du magasin
- **Étiquetez le matériel physiquement** - Utilisez un étiqueteur pour marquer le lecteur avec le nom du terminal (« Terminal 1 Reader ») pour une identification facile lors du dépannage
- **Maintenez les lecteurs sur une alimentation ininterrompue** - Les coupures de courant pendant une transaction peuvent corrompre l'état du lecteur ; un onduleur est recommandé
- **Documentez les numéros de série des lecteurs** - Tenez un registre des numéros de série pour la garantie et le support (trouvé sur l'étiquette du matériel du lecteur)
- **Mettez à jour le firmware des lecteurs** - Stripe推送 firmware updates automatically, but verify readers are on latest version periodically (check Stripe Dashboard)