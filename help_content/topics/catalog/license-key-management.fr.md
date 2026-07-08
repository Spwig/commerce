---
title: Gestion des clés de licence
---

La gestion des clés de licence vous permet de contrôler la manière dont les clés de licence logicielle sont générées, stockées et envoyées aux clients lorsqu'ils achètent des produits numériques. Spwig prend en charge la génération de clés intégrée, des pools de clés préchargés et des intégrations avec des services externes de gestion de licence.

## Aperçu

Il existe trois méthodes pour gérer les clés de licence dans Spwig :

| Méthode | Meilleure pour |
|--------|---------|
| **Modèles de licence** | Générer automatiquement des clés uniques dans un format personnalisé au moment de l'achat |
| **Pools de licence** | Générer à l'avance un lot de clés pour une distribution en masse |
| **Fournisseurs externes** | Déléguer la génération et la gestion des clés à un service tiers comme Keygen.sh |

Ces méthodes peuvent être combinées — par exemple, un pool peut utiliser un modèle personnalisé pour définir le format de la clé, et peut éventuellement synchroniser les clés générées avec un fournisseur externe.

## Modèles de clés de licence

Un modèle de clé de licence définit le *format* des clés générées. Les modèles utilisent un motif avec des espaces réservés que Spwig remplit au moment de la génération.

### Création d'un modèle

1. Accédez à **Catalogue > Modèles de clés de licence**
2. Cliquez sur **+ Ajouter un modèle de clé de licence**
3. Entrez un **Nom** (par exemple, `Licence standard d'application`)
4. Configurez le **Motif** à l'aide d'espaces réservés (voir ci-dessous)
5. Définissez le **Préfixe** et le **Suffixe** si nécessaire (par exemple, un préfixe de `MYAPP` ajoute `MYAPP-` à chaque clé)
6. Choisissez le **Séparateur** (par défaut : `-`)
7. Définissez l'**Ensemble de caractères** — les caractères utilisés pour les segments aléatoires. Le par défaut exclut les caractères ambigus comme `0` et `O`, `1` et `I`
8. Définissez la **Longueur minimale/maximale** pour la validation
9. Cliquez sur **Enregistrer**

### Espaces réservés du motif

| Espace réservé | Description | Exemple de sortie |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N caractères aléatoires choisis dans l'ensemble de caractères | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | Code de vérification à N chiffres | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Valeur du préfixe du modèle | `MYAPP` |
| `{SUFFIX}` | Valeur du suffixe du modèle | `PRO` |
| `{ORDER_ID}` | Numéro de commande | `10045` |
| `{PRODUCT_SKU}` | SKU du produit | `SOFTPRO` |
| `{DATE:FORMAT}` | Date formatée | `{DATE:YYMMDD}` → `260318` |

**Exemple de motif** : `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Cela produit des clés comme : `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Aperçu des clés

Après avoir enregistré un modèle, une action **Générer une clé d'exemple** est disponible dans la liste des modèles. Utilisez-la pour vérifier que votre motif génère des clés dans le format attendu avant d'attribuer le modèle à un produit.

## Pools de licence

Un pool de licence est un lot de clés pré-générées pour un produit. Les pools sont utiles lorsque :
- Vous avez besoin de clés pour l'emballage physique (boîtes de vente au détail, cartes imprimées)
- Vous travaillez avec des revendeurs qui ont besoin de lots de clés
- Vous souhaitez que les clés soient générées à l'avance plutôt qu'à la demande

### Création d'un pool de licence

1. Accédez à **Catalogue > Pools de licence**
2. Cliquez sur **+ Ajouter un pool de licence**
3. Remplissez les détails du pool :

| Champ | Description |
|-------|-------------|
| **Nom** | Nom descriptif (par exemple, `Pack de détail Q1 2026`) |
| **Produit** | Le produit pour lequel ces clés sont destinées |
| **Modèle de licence** | Modèle pour le format de la clé (par défaut, le modèle du produit) |
| **Nombre total de clés** | Nombre de clés à générer |
| **Type de clé** | Perpétuel, abonnement ou essai |
| **Nombre maximal d'activations** | Nombre d'appareils sur lesquels chaque clé peut être activée |
| **Expire après X jours** | Nombre de jours avant que la licence n'expire après la première activation (laissez vide pour aucune expiration) |
| **Expire le** | Date après laquelle les clés non utilisées de ce pool deviennent invalides |
| **Synchroniser avec le fournisseur** | Optionnellement synchroniser les clés générées avec un fournisseur externe de licence |

4. Cliquez sur **Enregistrer** — Spwig commence à générer les clés en arrière-plan

### État du pool


| Statut | Signification |
|--------|-------------|
| **Génération en cours** | Les clés sont générées en arrière-plan |
| **Prêt** | Toutes les clés ont été générées et sont disponibles pour la distribution |
| **Épuisé** | Toutes les clés ont été attribuées à des commandes |
| **Expiré** | La date d'expiration du pool est passée |

### Surveillance d'un pool

La liste des pools indique combien de clés ont été distribuées par rapport au nombre total de clés générées. Ouvrez un pool pour voir la liste complète des clés et leurs états individuels.

## Fournisseurs de licences externes

Les fournisseurs externes sont des services de gestion de licences tiers qui gèrent la génération de clés et le suivi de leur activation. Lorsqu'un client termine un achat, Spwig communique avec le fournisseur pour générer et enregistrer la clé.

### Fournisseurs pris en charge

| Fournisseur | Type |
|----------|------|
| **Serveur de licence intégré de Spwig** | Intégré — aucun compte externe requis |
| **Keygen.sh** | API de gestion de licence basée en cloud |
| **LicenseSpring** | Gestion de licence d'entreprise |
| **Cryptlex** | Gestion de licence avec prise en charge hors ligne |
| **API personnalisée** | Tout système de licence basé sur REST |

### Connexion à un fournisseur

1. Accédez à **Catalogue > Fournisseurs de licences**
2. Cliquez sur **+ Ajouter un fournisseur de licence**
3. Remplissez les détails du fournisseur :

| Champ | Description |
|-------|-------------|
| **Nom** | Étiquette pour cette connexion (ex. : `Keygen Production`) |
| **Type de fournisseur** | Sélectionnez parmi les fournisseurs pris en charge |
| **Point de terminaison API** | URL de base de l'API du fournisseur |
| **Clé API** | Clé d'authentification pour le fournisseur |
| **Clé secrète API** | Si requis par le fournisseur |

4. Configurez le comportement de synchronisation :
   - **Synchronisation à la commande** — Synchronisation automatique lorsqu'un client termine un achat
   - **Synchronisation à l'activation** — Signaler les activations d'appareils au fournisseur
   - **Synchronisation à la désactivation** — Signaler les désactivations (utile pour les transferts de licence et les remboursements)
   - **Synchronisation bidirectionnelle** — Permettre au fournisseur de mettre à jour les enregistrements de Spwig via des webhooks

5. Cliquez sur **Enregistrer**, puis cliquez sur **Tester la connexion** pour vérifier que les identifiants fonctionnent

### Statut de la connexion

Chaque fournisseur affiche l'un des trois statuts de connexion suivants :

| Statut | Signification |
|--------|-------------|
| **Non testé** | La connexion n'a pas encore été vérifiée |
| **Connecté** | Le dernier test a réussi |
| **Erreur** | Le test de connexion a échoué — vérifiez le message d'erreur |

### Synchronisation des licences existantes

Pour pousser manuellement des clés de licence existantes vers un fournisseur (pour la configuration initiale ou après une synchronisation échouée), utilisez l'action **Synchroniser maintenant** depuis la liste des fournisseurs.

## Surveillance de l'activité de synchronisation

Accédez à **Catalogue > Synchronisation des licences externes** pour consulter le journal de synchronisation. Chaque enregistrement affiche :
- La clé de licence qui a été synchronisée
- Le fournisseur vers lequel elle a été envoyée
- Direction (Spwig → Fournisseur ou Fournisseur → Spwig)
- Statut (En attente, Réussi, Échoué)
- Détails d'erreur pour les synchronisations échouées

Les synchronisations échouées sont réessayées automatiquement. Vous pouvez également forcer un nouveau réessai en modifiant l'enregistrement et en effaçant l'erreur.

## Conseils

- Utilisez l'ensemble de caractères par défaut (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) pour éviter les caractères ambigus que les clients lisent souvent de travers — il exclut `0`, `O`, `1` et `I`.
- Ajoutez un segment `{CHECKSUM}` à votre modèle de motif afin que les clients et votre équipe de support puissent rapidement détecter les clés mal tapées.
- Pour les produits à grande échelle, utilisez un pool plutôt que la génération à la demande pour garantir que les clés sont livrées instantanément à la caisse.
- Définissez **Expire à** sur les lots de clés saisonniers ou limités dans le temps afin que les anciennes clés non utilisées soient automatiquement invalidées.
- Testez toujours la connexion du fournisseur après l'installation et après tout changement d'identifiants — une connexion cassée signifie que les clients ne reçoivent pas leurs clés.
- Si vous utilisez une synchronisation bidirectionnelle, configurez l'URL de webhook de votre fournisseur pour pointer vers le point de terminaison de webhook de licence de votre magasin.