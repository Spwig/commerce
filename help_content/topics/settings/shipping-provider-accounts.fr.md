---
title: Comptes des fournisseurs d'expédition
---

Les comptes des fournisseurs d'expédition connectent votre magasin aux API des transporteurs (FedEx, UPS, DHL) pour le calcul des tarifs en temps réel et l'achat automatique d'étiquettes. Chaque compte stocke des informations d'API chiffrées, surveille l'état de la connexion et se relie aux méthodes d'expédition en temps réel. Les fournisseurs récupèrent des tarifs en direct à la caisse en fonction des dimensions du colis, du poids, de l'origine et de la destination - éliminant ainsi la maintenance manuelle des tableaux de tarifs et assurant des prix exacts des transporteurs.

Utilisez les comptes des fournisseurs lorsque vous avez besoin de tarifs d'expédition calculés par le transporteur ou de génération d'étiquettes automatisée au lieu de la création manuelle des envois.

## Fournisseurs d'expédition pris en charge

Spwig prend en charge les principaux transporteurs via des composants de fournisseur installables:

### FedEx

**Services**: Terrestre, Express, International
**API**: FedEx Web Services
**Fonctionnalités**: Tarifs en temps réel, achat d'étiquettes, suivi, douane internationale

### UPS

**Services**: Terrestre, Aérien, Mondial
**API**: UPS Developer API
**Fonctionnalités**: Tarifs en temps réel, génération d'étiquettes, suivi, validation des adresses

### DHL

**Services**: Express, E-commerce, International
**API**: DHL Express API
**Fonctionnalités**: Tarifs internationaux, documents de douane, suivi

### Fournisseurs supplémentaires

Installez-les depuis le marché des composants selon vos besoins (USPS, Canada Post, Australia Post, etc.)

---

## Configuration du compte du fournisseur

Chaque compte de fournisseur nécessite:

### Informations de base

- **Nom d'affichage**: Comment le compte s'affiche dans l'administration (ex. : « Compte de production FedEx »)
- **Fournisseur**: Sélectionnez le composant de fournisseur installé à partir du menu déroulant
- **Actif**: Activez/désactivez sans supprimer les informations d'identification
- **Est par défaut**: Définir comme compte par défaut pour ce fournisseur (un seul compte par défaut par fournisseur)

### Informations d'API (chiffrées)

**Varie selon le fournisseur**, généralement inclut:

**FedEx**:
- Numéro de compte
- Numéro de mètre
- Clé API
- Secret API

**UPS**:
- Numéro de licence d'accès
- ID utilisateur
- Mot de passe
- Numéro de compte

**DHL**:
- ID du site
- Mot de passe
- Numéro de compte

**Toutes les informations d'identification sont chiffrées au repos** et ne sont déchiffrées que lors de l'appel de l'API.

### Adresse d'origine

- **Adresse d'expédition par défaut**: Adresse du entrepôt/origine pour le calcul des tarifs
- Certains fournisseurs exigent une configuration spécifique d'origine dans leur tableau de bord

### Paramètres

Options spécifiques au fournisseur (varient selon le transporteur):

- **Mode test**: Utiliser les points de terminaison d'API de test/sandbox du transporteur
- **Tarifs négociés**: Utiliser vos tarifs négociés avec le transporteur (si disponibles)
- **Inclure l'assurance**: Citer automatiquement l'assurance dans les tarifs
- **Surcoût résidentiel**: Appliquer les frais de livraison résidentielle
- **Signature requise**: Exigences de signature par défaut

---

## Création d'un compte de fournisseur

**Processus de configuration en 6 étapes**:

**Étape 1: Obtenir l'accès à l'API du transporteur**
1. Créez un compte auprès du transporteur (FedEx.com, UPS.com, DHL.com)
2. Demandez l'accès à l'API/au développement
3. Terminez l'intégration de l'API du transporteur (peut prendre 1 à 3 jours ouvrables)
4. Recevez les informations d'API par e-mail ou via le portail du développeur

**Étape 2: Installer le composant du fournisseur** (si non préinstallé)
1. Allez dans Paramètres > Composants > Marché
2. Recherchez le nom du transporteur (ex. : « FedEx »)
3. Installez le composant du fournisseur d'expédition
4. Attendez la fin de l'installation

**Étape 3: Créer un compte de fournisseur dans Spwig**
1. Accédez à Paramètres > Expédition > Comptes de fournisseur
2. Cliquez sur « Ajouter un compte de fournisseur »
3. Sélectionnez le fournisseur à partir du menu déroulant
4. Entrez le nom d'affichage

**Étape 4: Entrer les informations d'API**
1. Remplissez les champs des informations d'API (varient selon le fournisseur)
2. Les informations d'API sont automatiquement chiffrées à l'enregistrement
3. Optionnel: Activer le mode test pour les tests initiaux

**Étape 5: Tester la connexion**
1. Cliquez sur le bouton « Tester la connexion »
2. Le système tente d'effectuer une appel API vers le transporteur
3. Vérifiez que le statut « Connecté » s'affiche
4. Vérifiez le timestamp last_tested_at

**Étape 6: Lier à une méthode d'expédition**
1. Créez ou modifiez une méthode d'expédition (Paramètres > Panier > Méthodes d'expédition)
2. Définissez method_type = « Temps réel »
3. Sélectionnez le compte du fournisseur à partir du menu déroulant
4. Enregistrez la méthode

---

## Surveillance du statut de la connexion

Les comptes des fournisseurs surveillent l'état de la connexion:

### Valeurs de statut

**Inconnu** (gris): Jamais testé ou non encore connecté

**Connecté** (vert): Dernière appel API réussie, informations d'identification valides

**Erreur** (rouge): Dernière appel API échouée, informations d'identification peuvent être invalides

### Dernier test

- **Horodatage**: Quand la connexion a été vérifiée pour la dernière fois
- **Mise à jour automatique**: Chaque fois que le fournisseur est utilisé (recherche de tarif, achat d'étiquette)
- **Test manuel**: Cliquez sur le bouton « Tester la connexion » à tout moment

### Dépannage des connexions échouées

**Causes courantes**:
- Informations d'API incorrectes (faute de frappe, copiées avec un espace supplémentaire)
- Clé API du transporteur expirée ou révoquée
- Mode test activé mais avec des informations d'identification de production (ou inversement)
- Adresse IP non autorisée par le transporteur
- Pannes de l'API du transporteur

**Étapes de résolution**:
1. Vérifiez que les informations d'identification correspondent exactement au tableau de bord du transporteur
2. Vérifiez que le mode test est activé ou désactivé selon le type d'informations d'identification
3. Consultez la page d'état de l'API du transporteur pour vérifier les pannes
4. Contactez le support du transporteur pour vérifier le compte

---

## Workflow de recherche des tarifs

Fonctionnement des tarifs en temps réel à la caisse:

**1. Le client entre son adresse**
- Adresse d'expédition entrée
- Panier calcule le poids total + dimensions

**2. Le système prépare la demande de tarif**
- Récupère les informations d'identification du compte du fournisseur (déchiffrées)
- Calcule les dimensions du colis à partir des éléments du panier (utilise les packages d'expédition si définis)
- Prépare la demande API avec l'origine, la destination, les colis

**3. API du fournisseur appelée**
- Demande envoyée à l'API du transporteur avec les informations d'authentification
- Le transporteur calcule le tarif en fonction de la zone, du poids, des dimensions
- La réponse inclut les options de service (Terrestre, Express, etc.)

**4. Tarifs affichés**
- Le système analyse la réponse du transporteur
- Normalise au format standard
- Markup optionnel appliqué (si configuré)
- Tarifs affichés au client à la caisse

**5. Le client sélectionne le service**
- Le client choisit l'option préférée
- Le tarif sélectionné est enregistré dans la commande

**Exemple de flux API**:
```
Demande à l'API FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // grammes
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Réponse FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Achat d'étiquette (facultatif)

Si le fournisseur prend en charge la génération d'étiquette:

**Workflow**:
1. Le client termine son commande
2. Le vendeur crée l'envoi (Commandes > Détail de la commande > Créer un envoi)
3. Sélectionnez le compte du fournisseur + service
4. Le système appelle l'API d'étiquette du fournisseur
5. L'étiquette PDF est générée et attachée à l'envoi
6. Le numéro de suivi est automatiquement rempli
7. L'étiquette est prête à l'impression

**Avantages**:
- Aucune connexion manuelle au site du transporteur
- Le suivi est synchronisé automatiquement
- Les formulaires de douane sont générés automatiquement (internationaux)
- Génération d'étiquettes en lot possible

---

## Markup des tarifs

Ajoutez un markup du vendeur aux tarifs du transporteur:

**Configuration** (dans la méthode d'expédition, pas dans le compte du fournisseur):
- **Type de markup**: Pourcentage ou Fixe
- **Montant du markup**: Ex. : 15% ou $2,50

**Exemple**:
```
Tarif du transporteur: $12,50
Markup: 15%
Le client paie: $14,38

OU

Tarif du transporteur: $12,50
Markup: $2,50 (fixe)
Le client paie: $15,00
```

**Cas d'utilisation**:
- Couvrir les coûts d'emballage/gestion
- Ajouter un marge bénéficiaire sur l'expédition
- Compenser les frais de carte de crédit sur l'expédition

---

## Plusieurs comptes de fournisseur

Vous pouvez créer plusieurs comptes pour le même fournisseur:

**Cas d'utilisation**:
1. **Test vs Production**
   - Compte de test: Informations d'identification du sandbox du transporteur
   - Compte de production: Informations d'identification en direct

2. **Plusieurs entrepôts**
   - Compte de l'entrepôt A: Origine = Los Angeles
   - Compte de l'entrepôt B: Origine = New York

3. **Différents tarifs négociés**
   - Compte A: Tarifs standard
   - Compte B: Tarifs de réduction par volume

**Chaque compte peut se lier à différentes méthodes d'expédition** pour une configuration flexible.

---

## Conseils

- **Testez dans le sandbox d'abord** - Utilisez les informations d'identification de test du transporteur avant de passer en production
- **Surveillez l'état de la connexion** - Vérifiez régulièrement le tableau de bord pour les statuts d'erreur
- **Définissez des packages d'expédition** - Des dimensions précises améliorent les devis de tarif
- **Utilisez les tarifs négociés** - Activez si vous avez des réductions de volume avec le transporteur
- **Définissez une origine réaliste** - Utilisez l'adresse réelle d'expédition pour des zones précises
- **Gardez les informations d'identification sécurisées** - Ne partagez jamais les clés API, renouvelez-les périodiquement
- **Ayez une méthode de secours** - Gardez une méthode à tarif fixe active si l'API du transporteur échoue
- **Surveillez les limites de l'API du transporteur** - Certains transporteurs limitent les appels API par jour
- **Mettez à jour les informations d'identification rapidement** - Quand le transporteur renouvelle les clés, mettez-les à jour immédiatement
- **Utilisez des noms descriptifs** - « FedEx LA Warehouse » est meilleur que « FedEx 1 »