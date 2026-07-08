---
title: Migration du système complet
---

La migration du système complet transfère votre magasin entier -- paramètres, produits, clients, commandes, fichiers multimédias et toutes autres données -- d'une installation Spwig à une autre. Utilisez cela lors du passage à un nouveau serveur ou lors de la création d'une copie complète de votre magasin.

## Quand utiliser une migration complète

- **Déplacement de serveur** : Passage de votre magasin à un nouveau fournisseur d'hébergement ou serveur
- **Création d'une copie de test** : Mise en place d'un environnement de test complet à partir de la production
- **Récupération après sinistre** : Restauration d'un magasin complet à partir d'une instance de sauvegarde

La migration complète inclut tout ce que fait la synchronisation des paramètres, plus toutes les données transactionnelles (produits, clients, commandes, avis, stock, fichiers multimédias, etc.).

## Ce qui est migré

La migration complète peut transférer toutes les catégories de paramètres ainsi que ces catégories de données :

| Catégorie | Description |
|----------|-------------|
| **Composants installés** | Thèmes, intégrations de fournisseurs et composants utilitaires avec leurs fichiers de package |
| **Produits, catégories et marques** | Produits, variantes, images, catégories, marques et attributs |
| **Bibliothèque multimédia** | Tous les fichiers multimédias et actifs téléchargés |
| **Clients et adresses** | Comptes clients, profils et adresses |
| **Historique des commandes** | Commandes, éléments de commande et enregistrements de transactions |
| **Avis sur les produits** | Avis clients et notes |
| **Niveaux de stock** | Quantités d'inventaire par entrepôt et points de commande |
| **Produits numériques et licences** | Actifs numériques, modèles de licence et pools de licence |
| **Cartes-cadeaux et utilisation de bons** | Solde des cartes-cadeaux et enregistrements d'utilisation de bons |
| **Crédits de magasin et portefeuilles** | Solde des portefeuilles clients et historique des transactions |
| **Membres du programme de fidélité** | Membres de fidélité, points, transactions et badges |
| **Abonnements actifs** | Plans d'abonnement, abonnements actifs et historique de facturation |
| **Envois et suivi** | Enregistrements d'envoi et événements de suivi |
| **Remboursements, retours et notes de commande** | Enregistrements de remboursement, demandes de retour et notes |
| **Membres affiliés** | Comptes affiliés, codes de parrainage et historique de commissions |

## Guide étape par étape

### Étape 1 : Se connecter à l'instance source

1. Accédez à **Data Migration > Spwig-to-Spwig Sync** dans le menu latéral de l'administration
2. Cliquez sur **Start Full Migration**
3. Connectez-vous au magasin source (le magasin que vous migrez **de**) :
   - Entrez l'URL du magasin source
   - Collez le jeton de synchronisation du magasin source
   - Nommez la connexion (ex. : "Ancien serveur de production")
4. Cliquez sur **Test Connection** pour vérifier
5. Cliquez sur **Next**

> **Important** : La migration complète **tire** toujours les données depuis le magasin connecté vers ce magasin. Exécutez l'assistant sur le **destinataire** (le nouveau) magasin.

### Étape 2 : Choisir l'étendue

Sélectionnez les catégories de données à inclure dans la migration. Les catégories sont organisées en groupes :

- **Paramètres** : Configuration du magasin, thèmes, fournisseurs, contenu
- **Données** : Produits, clients, commandes, fichiers multimédias et autres données transactionnelles

Certaines catégories ont des dépendances (ex. : les commandes dépendent des clients et des produits). Les dépendances sont automatiquement incluses lors de la sélection d'une catégorie.

Catégories avec des indicateurs spéciaux :
- **Icône clé** : Contient des identifiants transférés de manière sécurisée
- **Icône fichier** : Inclut des fichiers binaires (images, fichiers multimédias, packages)
- **Icône d'avertissement** : Considérations spéciales pour les environnements de production

### Étape 3 : Vérifications préalables

Avant le début de la migration, des vérifications automatiques préalables vérifient :

- **Santé de la connexion** : Le magasin source est accessible et authentifié
- **Compatibilité des versions** : Les deux magasins exécutent des versions compatibles de Spwig
- **Espace disque** : Un stockage suffisant est disponible pour les fichiers multimédias
- **Préparation de la base de données** : La base de données de destination peut recevoir les données

Si l'une des vérifications échoue, vous verrez des instructions spécifiques sur la manière de résoudre le problème avant de continuer.

### Étape 4 : Progrès de la migration

La migration s'exécute en arrière-plan. Vous pouvez naviguer librement -- le processus continuera.



La page de progression affiche : 
- Le pourcentage global avec le temps estimé restant
- L'état de progression par catégorie
- Journal d'activité en direct avec les détails de transfert
- Statistiques de transfert de médias (fichiers et octets transférés) pour la catégorie médias

Pour les grandes boutiques avec de nombreux produits et fichiers multimédias, la migration peut prendre un certain temps. La phase de transfert des médias est généralement la plus longue.

### Étape 5 : Résultats

Après la migration, la page des résultats affiche :

- Statistiques récapitulatives (éléments migrés, ignorés, échoués)
- Détail par catégorie avec l'état
- Détails des erreurs pour les éléments échoués

## Liste de vérification après la migration

Après une migration réussie, effectuez ces étapes sur votre nouvelle boutique :

1. **Activez votre licence** sur l'installation nouvelle
2. **Re-saisissez les identifiants du fournisseur de paiement** qui ont été ignorés pendant la migration (les clés de test/sandbox ne sont pas transférées vers la production)
3. **Configurez le DNS** pour pointer votre domaine vers le nouveau serveur
4. **Testez le processus de paiement** avec une commande de test
5. **Vérifiez que l'envoi d'e-mails** fonctionne correctement
6. **Vérifiez les fichiers multimédias** et assurez-vous que les images s'affichent correctement

## Retour en arrière

Après une migration complète, vous avez **24 heures** pour effectuer un retour en arrière. Un retour en arrière supprime toutes les données migrées du magasin de destination, les ramenant à leur état avant la migration.

Pour effectuer un retour en arrière :
1. Allez sur la page des résultats ou le tableau de bord de synchronisation
2. Cliquez sur **Retour en arrière de la migration** et confirmez
3. Attendez la fin du retour en arrière

> **Avertissement :** Le retour en arrière supprime définitivement toutes les données migrées. Toute modification effectuée sur le magasin de destination après la migration (nouvelles commandes, inscriptions clients, etc.) sera également affectée.

Après 24 heures, l'option de retour en arrière expire.

## Conseils

- **Exécuter sur le magasin de destination** : Le guide de migration complète doit être exécuté sur le **nouveau** magasin, en extrayant les données du magasin ancien
- **Migrer vers une installation propre** : Pour les meilleurs résultats, exécutez la migration sur une installation Spwig fraîche avant de mettre en ligne
- **Vérifier l'espace disque** : Assurez-vous que le magasin de destination dispose d'un stockage suffisant pour tous les fichiers multimédias
- **Garder le magasin source en marche** : Ne fermez pas le magasin source tant que vous n'avez pas vérifié que tout fonctionne sur le magasin de destination
- **Planifier la transition DNS** : Après avoir vérifié la migration, mettez à jour vos enregistrements DNS pour pointer vers le nouveau serveur