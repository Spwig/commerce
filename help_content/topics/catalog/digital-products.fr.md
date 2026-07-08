---
title: Produits Numériques
---

Les produits numériques vous permettent de vendre des fichiers téléchargeables, des licences logicielles et d'autres biens non physiques. Spwig prend en charge les produits numériques autonomes, ainsi que les produits hybrides qui combinent livraison physique et numérique.

![Fournisseurs de licences](/static/core/admin/img/help/digital-products/license-providers.webp)

## Types de Produits Numériques

### Produit Numérique Autonome

Définissez le **Type de Produit** sur **Produit Numérique** pour les articles purement numériques :
- Applications logicielles
- Livres numériques et PDFs
- Musique et fichiers audio
- Art numérique et modèles

### Produits Hybrides

Tout type de produit peut inclure une livraison numérique en cochant **Est un Produit Numérique** dans l'onglet Informations de Base. Cela est utile pour :
- **Produits numériques variables** — Logiciels avec éditions Basique/Pro/Entreprise
- **Produits numériques personnalisables** — Ressources numériques conçues sur mesure
- **Paquets physiques + numériques** — Un livre qui inclut un téléchargement numérique

## Configurer un Produit Numérique

### Étape 1 : Créer le Produit

1. Accédez à **Produits > Tous les Produits** et cliquez sur **+ Ajouter un Produit**
2. Définissez le **Type de Produit** sur **Produit Numérique** (ou cochez **Est un Produit Numérique** sur un autre type de produit)
3. Remplissez les détails du produit (nom, description, prix)
4. Enregistrez le produit

### Étape 2 : Ajouter des Fichiers Téléchargeables

1. Accédez à l'onglet **Inventaire** du produit
2. Dans la section **Fichiers Numériques**, téléchargez les fichiers que les clients recevront après l'achat
3. Pour chaque fichier, vous pouvez définir :
   - **Nom du fichier** — Nom d'affichage visible par les clients
   - **Limite de téléchargements** — Nombre maximum de téléchargements autorisés (0 = illimité)
   - **Jours d'expiration** — Nombre de jours pendant lesquels le lien de téléchargement reste actif

### Étape 3 : Configurer la Livraison de Licences (Optionnel)

Si votre produit numérique nécessite des clés de licence :

1. Accédez à **Paramètres > Gestion des Licences**
2. Connectez un fournisseur de licences (voir ci-dessous)
3. Dans le formulaire d'édition du produit, assignez le fournisseur de licences

## Fournisseurs de Licences

Les fournisseurs de licences sont des services externes qui génèrent et gèrent automatiquement les clés de licence logicielle lorsqu'un client achète votre produit.

### Types de Fournisseurs Disponibles

| Fournisseur | Description |
|-------------|-------------|
| **Serveur de Licences Intégré Spwig** | Génération simple de clés de licence intégrée à la plateforme |
| **Keygen.sh** | API complète de gestion des licences |
| **LicenseSpring** | Gestion de licences d'entreprise |
| **Cryptlex** | Licences logicielles avec support hors ligne |
| **API Personnalisée** | Connectez n'importe quel système de licences via REST API |

### Connecter un Fournisseur de Licences

1. Accédez à **Paramètres > Gestion des Licences**
2. Cliquez sur **Connecter un Fournisseur**
3. Suivez l'assistant de configuration :
   - **Étape 1** — Sélectionnez le type de fournisseur
   - **Étape 2** — Configurez les paramètres généraux
   - **Étape 3** — Saisissez les identifiants API
4. Testez la connexion pour vérifier son fonctionnement
5. Enregistrez la configuration

### Carte du Fournisseur

Chaque fournisseur connecté affiche :
- **Badges de statut** — Actif/Inactif et état de la connexion
- **Point d'accès API** — L'URL du serveur configurée
- **Capacités de synchronisation** — Support de synchronisation des Commandes, Activation et Désactivation
- **Boutons d'action** — Configurer, Tester et Synchroniser Maintenant

### Capacités de Synchronisation

Les fournisseurs de licences peuvent se synchroniser sur trois événements :

- **Commande** — Générer automatiquement une clé de licence lorsqu'un client finalise un achat
- **Activation** — Suivre le moment où un client active sa licence
- **Désactivation** — Gérer la désactivation de licence pour les remboursements ou les transferts

## Expérience Client

### Après l'Achat

Lorsqu'un client achète un produit numérique :

1. **Confirmation de commande** — Indique que la livraison numérique est incluse
2. **Livraison par e-mail** — Les liens de téléchargement et/ou les clés de licence sont envoyés automatiquement
3. **Page du compte** — Les clients peuvent accéder à leurs téléchargements depuis le tableau de bord de leur compte
4. **Page de téléchargement** — Liens de téléchargement sécurisés et à durée limitée

### Sécurité des Téléchargements

Les téléchargements de fichiers numériques sont protégés par :
- Des jetons de téléchargement uniques et à durée limitée
- Des limites optionnelles du nombre de téléchargements
- Des dates d'expiration après lesquelles les liens deviennent inactifs
- Une exigence de connexion (pour les clients enregistrés)

## Conseils

- Définissez des limites de téléchargement raisonnables (3 à 5 téléchargements) pour prévenir les abus tout en autorisant les re-téléchargements.
- Utilisez des jours d'expiration correspondant à votre période de support (ex. : 365 jours pour un an d'accès).
- Testez le flux d'achat complet avec une commande de test pour vous assurer que les liens de téléchargement et les clés de licence sont correctement livrés.
- Pour les produits logiciels, connectez un fournisseur de licences pour automatiser la génération de clés plutôt que de gérer les clés manuellement.
- Utilisez la fonctionnalité de produit hybride lorsque vous vendez des biens physiques incluant des extras numériques (ex. : livre imprimé + PDF).
