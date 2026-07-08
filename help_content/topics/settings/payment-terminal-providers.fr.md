---
title: Fournisseurs de terminaux de paiement
---

Les fournisseurs de terminaux de paiement permettent l'acceptation des cartes de crédit et de débit sur vos terminaux de caisse. Stripe Terminal est le fournisseur principal pris en charge, offrant des lecteurs de cartes modernes (S700, WisePOS E, P400), des taux de traitement compétitifs et une intégration fluide. Configurez les comptes de fournisseur avec des identifiants API, surveillez l'état de la connexion en temps réel et gérez plusieurs fournisseurs si vous opérez dans différentes régions. Le système de fournisseur est extensible - d'autres processeurs de paiement peuvent être intégrés via le framework de fournisseur si Stripe Terminal n'est pas disponible sur votre marché.

Utilisez les fournisseurs de paiement pour accepter les paiements par carte de manière sécurisée, suivre l'état du traitement des paiements et gérer les affectations de lecteurs sur les terminaux.

![Liste des fournisseurs de paiement](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Aperçu des fournisseurs de paiement

Les fournisseurs de paiement sont des services tiers qui traitent les paiements par carte au nom de votre entreprise :

**Responsabilités du fournisseur** :
- Autoriser les transactions de carte en temps réel
- Communiquer avec les lecteurs physiques de cartes
- Gérer la sécurité des paiements (conformité PCI, chiffrement)
- Transférer les fonds sur votre compte bancaire (règlement)
- Fournir des rapports de transactions et la gestion des contestations

**Rôle de Spwig** :
- Achemine les demandes de paiement vers le fournisseur configuré
- Stocke les identifiants du fournisseur chiffrés
- Surveille l'état de la connexion
- Associe les lecteurs aux terminaux
- Enregistre les résultats des paiements dans les commandes

## Stripe Terminal (fournisseur principal)

Stripe Terminal est le fournisseur de paiement recommandé pour la plupart des commerçants :

**Fonctionnalités** :
- Lecteurs de cartes à puce EMV modernes
- Prise en charge des paiements sans contact (NFC) (Apple Pay, Google Pay, cartes tap-to-pay)
- Gestion des contestations intégrée
- Autorisation en temps réel
- API conviviale pour les développeurs
- Disponible dans plus de 40 pays

**Tarification** (au 2024, vérifiez les tarifs actuels) :
- Frais de transaction : 2,7 % + 0,05 $ par transaction en personne (États-Unis)
- Aucuns frais mensuels, aucun frais d'installation, aucun frais de conformité PCI
- Matériel de lecteur de carte : Achat unique (59 $ à 299 $ selon le modèle)

**Régions prises en charge** :
- États-Unis, Canada, Royaume-Uni, Union européenne, Australie, Singapour et plus
- Vérifiez la disponibilité de Stripe : https://stripe.com/terminal

**Lecteurs pris en charge** :
- BBPOS WisePOS E (terminal Android tout-en-un)
- Stripe Reader S700 (lecteur de comptoir)
- Verifone P400 (lecteur hérité, toujours pris en charge)

## Configuration de Stripe Terminal

**Étape 1 : Créer un compte Stripe**
- Inscription sur stripe.com
- Compléter la vérification de l'entreprise (compte bancaire, identifiant fiscal)
- Activer les paiements

**Étape 2 : Activer Stripe Terminal**
- Dans le tableau de bord Stripe, accédez à **Produits > Terminal**
- Cliquez sur **Commencer**
- Accepter les conditions d'utilisation du Terminal

**Étape 3 : Créer un emplacement**
- Stripe Terminal nécessite un "emplacement" représentant votre site de vente physique
- Accédez à **Terminal > Emplacements**
- Cliquez sur **Créer un emplacement**
- Entrez l'adresse du magasin et les détails
- Enregistrez l'ID de l'emplacement (ressemble à `tml_1ABC123...`)

**Étape 4 : Générer une clé API**
- Accédez à **Développeurs > Clés API**
- Localisez votre **Clé secrète** (commence par `sk_live_...` pour la production, `sk_test_...` pour le test)
- Copiez la clé secrète (ne la partagez pas publiquement)

**Étape 5 : Configurer dans Spwig**
- Accédez à **POS > Fournisseurs de paiement**
- Cliquez sur **+ Ajouter un fournisseur de paiement**
- Sélectionnez **Fournisseur** : "Stripe Terminal"
- Entrez **Clé secrète API** (de l'étape 4)
- Entrez **ID de l'emplacement** (de l'étape 3)
- Enregistrer

**Étape 6 : Tester la connexion**
- Après l'enregistrement, l'état du fournisseur doit passer à "Connecté" (vert)
- Si l'état affiche "Erreur" (rouge), vérifiez la clé API et l'ID de l'emplacement
- Vérifiez le message d'erreur dans la vue détaillée du fournisseur

![Formulaire d'ajout de fournisseur de paiement](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Champs de configuration du fournisseur

**Clé du fournisseur** - Sélectionnez le processeur de paiement :
- **stripe_terminal** - Stripe Terminal (recommandé)
- **manual** - Saisie manuelle de paiement (uniquement pour les tests, aucun traitement réel)
- D'autres fournisseurs peuvent apparaître si installés via le système de composants

**Identifiants (chiffrés)** - Structure JSON contenant les identifiants API :
- Chiffrés automatiquement avant le stockage
- Jamais visibles en texte clair après l'enregistrement
- Structure d'exemple (Stripe Terminal) :
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Paramètres du fournisseur** - Configuration supplémentaire (spécifique au fournisseur) :
- Descripteur de compte (apparaît sur l'échéancier de la carte de crédit du client)
- Capture automatique (capture immédiatement les paiements autorisés par rapport à la capture manuelle)
- Surcharge de devise (si le compte du fournisseur utilise une devise différente de celle du magasin)

**État de la connexion** - Indicateur d'état en temps réel :
- **Connecté** (vert) - Le fournisseur est accessible et configuré correctement
- **Erreur** (rouge) - La connexion a échoué ou les identifiants sont invalides
- **Inconnu** (gris) - Pas encore testé (immédiatement après la création)

**Dernier test** - Horodatage de la dernière vérification de connexion
- Met à jour automatiquement lorsqu'une transaction est traitée
- Déclenchez manuellement le test via l'action d'administration **Tester la connexion**

## Surveillance de l'état de la connexion

Le système surveille la connectivité des fournisseurs pour vous alerter des problèmes avant que les clients n'essaient de payer : 

**Test automatique** : 
- Chaque transaction de paiement déclenche un test de connexion (par nécessité)
- Un travail en arrière-plan teste la connexion toutes les 6 heures (surveillance préventive)

**Significations des états** : 

**Connecté** - L'API du fournisseur est accessible, les identifiants sont valides, prêts à traiter les paiements

**Erreur** - Causes courantes : 
- Clé API invalide (révoquée, expirée ou incorrecte)
- ID d'emplacement invalide (emplacement supprimé dans Stripe, ID incorrect entré)
- Problèmes de connectivité réseau (pare-feu bloquant l'API Stripe)
- Panne du service Stripe (rare)

**Inconnu** - Fournisseur jamais testé (compte nouvellement créé en attente de première transaction)

**Résolution de l'état d'erreur** : 
1. Vérifiez le message d'erreur dans la vue détaillée du fournisseur (explique le problème spécifique)
2. Vérifiez que la clé API est toujours valide dans le tableau de bord Stripe
3. Vérifiez que l'ID d'emplacement existe toujours dans le tableau de bord Stripe
4. Testez manuellement la connexion via l'action d'administration **Tester la connexion**
5. Mettez à jour les identifiants si nécessaire

![Détail du fournisseur de paiement](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Comparaison des lecteurs de cartes pris en charge

Stripe Terminal propose plusieurs options de matériel de lecteur : 

| Modèle | Type | Méthodes de paiement | Écran | Meilleur pour | Prix |
|-------|------|---------------------|-------|--------------|-------|
| **WisePOS E** | Tout-en-un | Puce EMV, NFC, frottement | Écran tactile couleur 5" | Point de vente de détail complet | ~299 $ |
| **S700** | Comptoir | Puce EMV, NFC, frottement | Écran LCD monochrome | Encaissement de détail standard | ~249 $ |
| **P400** | Comptoir | Puce EMV, NFC, frottement | Écran LCD monochrome | Déploiements hérités | ~299 $ |

**Avantages du WisePOS E** : 
- Basé sur Android (exécute des applications, peut afficher du contenu personnalisé)
- Écran tactile couleur (meilleure UX pour les demandes de pourboire, la capture de signature)
- Imprimante de reçus intégrée (optionnelle)
- Vitesse de transaction la plus rapide

**Avantages de l'S700** : 
- Coût inférieur au WisePOS E
- Encombrement réduit
- Conception résistante aux éclaboussures

**P400** (modèle plus ancien) : 
- Toujours pris en charge mais non recommandé pour les nouveaux déploiements
- Moins rapide pour le traitement des cartes à puce que l'S700/WisePOS E

Tous les lecteurs se connectent au POS Spwig via l'API Stripe Terminal (aucune connexion directe USB/Bluetooth au dispositif POS requise).

## Considérations de sécurité

**Chiffrement des identifiants** : 
- Tous les identifiants des fournisseurs sont chiffrés au repos dans la base de données
- Le chiffrement utilise la clé secrète de l'application (définie dans les paramètres de l'application)
- Les identifiants ne figurent jamais dans les journaux ou les messages d'erreur

**Permissions des clés API** : 
- Utilisez des **clés API restreintes** en production (limitez les permissions au Terminal uniquement)
- Ne pas utiliser des clés secrètes non restreintes (accès plus large que nécessaire = risque de sécurité)
- Dans le tableau de bord Stripe, créez une clé restreinte avec uniquement les **permissions Terminal**

**Conformité PCI** : 
- Stripe Terminal gère la conformité PCI (les données de carte ne touchent jamais les serveurs Spwig)
- Les numéros de carte sont traités entièrement sur le matériel du lecteur → serveurs Stripe → réseaux de cartes
- Spwig n'entrepose que les résultats des paiements (approuvé/refusé), jamais les détails de la carte

**Rotation des clés** : 
- Tournez les clés API annuellement comme bonnes pratiques de sécurité
- Lors de la rotation, mettez à jour les identifiants dans la configuration du fournisseur
- Les anciennes clés peuvent être révoquées dans le tableau de bord Stripe après avoir confirmé que la nouvelle clé fonctionne

## Plusieurs fournisseurs

Certains commerçants ont besoin de plusieurs comptes de fournisseur : 

**Opérations multi-devise** : 
- Les magasins aux États-Unis utilisent le compte Stripe US (traite en USD)
- Les magasins européens utilisent le compte Stripe EU (traite en EUR)
- Configurez un fournisseur distinct par devise

**Fournisseurs de secours** : 
- Fournisseur principal (Stripe Terminal)
- Fournisseur de secours (saisie manuelle) lorsque les lecteurs ne fonctionnent pas
- Le caissier sélectionne le fournisseur lors de l'initiation du paiement

**Test vs Production** : 
- Fournisseur de test avec la clé API `sk_test_...`
- Fournisseur de production avec la clé API `sk_live_...`
- Changez de fournisseur après la phase de test

## Résolution des problèmes courants

**Problème 1 : L'état affiche "Erreur" avec le message "Clé API invalide"**
- **Cause** : Clé API révoquée ou copiée incorrectement
- **Solution** : Générez une nouvelle clé API dans le tableau de bord Stripe, mettez à jour les identifiants du fournisseur, testez la connexion

**Problème 2 : Lecteur non découvert lors du paiement**
- **Cause** : Lecteur non enregistré à l'emplacement du fournisseur
- **Solution** : Dans le tableau de bord Stripe, vérifiez que le lecteur est enregistré à l'ID d'emplacement utilisé dans la configuration du fournisseur

**Problème 3 : Paiements refusés malgré une carte valide**
- **Cause** : Compte Stripe non entièrement activé (vérification en attente)
- **Solution** : Terminez la vérification de l'entreprise dans le tableau de bord Stripe (compte bancaire, identifiant fiscal)

**Problème 4 : L'état de la connexion affiche "Inconnu" et ne se met jamais à jour**
- **Cause** : Fournisseur jamais testé (aucune transaction tentée)
- **Solution** : Utilisez l'action d'administration **Tester la connexion** pour déclencher manuellement le test de connectivité

## Conseils

- **Mode de test avant la production** - Utilisez les clés API de test de Stripe (`sk_test_...`) pour la configuration initiale et les tests
- **Un fournisseur par devise** - Ne tentez pas de traiter l'EUR avec un compte Stripe basé sur le USD ; créez des fournisseurs distincts
- **Surveillez l'état de la connexion hebdomadairement** - La surveillance proactive empêche les échecs de paiement au moment du passage en caisse
- **Restreindre les permissions des clés API** - Limitez les clés API Stripe uniquement aux permissions Terminal (principe du moindre privilège)
- **Documentez les ID d'emplacement** - Tenez un registre de l'emplacement Stripe correspondant à chaque magasin physique
- **Testez l'affectation des lecteurs** - Après la configuration du fournisseur, testez un paiement avec un lecteur de carte réel pour vérifier le flux d'extrémité à extrémité
- **Maintenez les informations de contact Stripe à jour** - Assurez-vous que les informations de contact de l'entreprise dans Stripe correspondent aux informations actuelles (important pour les contestations, la conformité)