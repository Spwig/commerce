---
title: Sauvegardes de base de données
---

Les sauvegardes régulières protègent les données de votre magasin — commandes, clients, produits et configuration — contre les pannes matérielles, les suppressions accidentelles et d'autres événements imprévus. Le système de sauvegarde de Spwig vous permet de créer des sauvegardes à la demande, de définir des plages horaires automatiques, de télécharger des sauvegardes localement, de restaurer à partir de toute sauvegarde enregistrée et de copier des sauvegardes vers des destinations de stockage à distance comme Amazon S3 ou Google Drive.

Accédez à **Management > System Metrics** et utilisez les liens de la barre d'outils pour accéder aux outils de sauvegarde.

![Tableau de bord du système avec les outils de sauvegarde](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Créer une sauvegarde manuelle

Exécutez une sauvegarde à tout moment avant de faire des changements importants — tels qu'une importation de produits, une mise à jour de thème ou une mise à niveau de la plateforme.

1. Accédez à **Management > System Metrics**
2. Cliquez sur **Create Full Backup** dans la barre d'outils
3. Entrez un **Nom** descriptif pour la sauvegarde (ex. : `before-july-import`)
4. Ajoutez éventuellement une **Description** pour vous rappeler pourquoi cette sauvegarde a été effectuée
5. Choisissez un **Type de sauvegarde** : 
   - **Full System** — sauvegarde la base de données et tous les fichiers multimédias (recommandé)
   - **Database Only** — sauvegarde uniquement les données du magasin, en excluant les images et fichiers téléchargés
6. Choisissez la **Compression** (`gzip` est la valeur par défaut et fonctionne bien pour la plupart des magasins)
7. Cliquez sur **Create Backup**

Spwig crée la sauvegarde en arrière-plan. Un indicateur de progression montre l'étape actuelle. Lorsqu'elle est terminée, la sauvegarde apparaît dans la liste **Database Backups** avec un statut **Completed** et sa taille de fichier.

## Télécharger une sauvegarde

Vous pouvez télécharger toute sauvegarde terminée pour conserver une copie locale sur votre ordinateur.

1. Accédez à **Management > Database Backups**
2. Trouvez la sauvegarde que vous souhaitez télécharger
3. Cliquez sur le bouton **Download** à côté de celle-ci

Le fichier de sauvegarde se télécharge sous forme d'archive compressée. Stockez-le dans un endroit sécurisé — sur un appareil distinct ou un stockage en nuage — afin d'avoir une copie indépendante de votre serveur.

## Planifier des sauvegardes automatiques

Les sauvegardes automatiques s'exécutent en arrière-plan sans que vous ayez à faire quoi que ce soit, donc vos données sont protégées même si vous oubliez de créer des sauvegardes manuelles.

1. Accédez à **Management > System Metrics**
2. Cliquez sur **Backup Schedule**
3. Cochez **Enable Automatic Backups**
4. Définissez la **Fréquence** : 
   - **Daily** — s'exécute une fois par jour à l'heure que vous spécifiez
   - **Weekly** — s'exécute une fois par semaine le jour que vous choisissez
   - **Monthly** — s'exécute un jour spécifique du mois
5. Définissez l'**Heure** à laquelle la sauvegarde doit s'exécuter (heure du serveur, généralement UTC — 03:00 AM est une bonne heure à faible trafic)
6. Choisissez le **Type de sauvegarde** (Full System ou Database Only)
7. Définissez les **Jours de conservation** — les sauvegardes plus anciennes que ce nombre de jours sont supprimées automatiquement (par défaut : 30 jours)
8. Cochez éventuellement **Encrypt Backup** pour chiffrer le fichier de sauvegarde au repos
9. Si vous avez des destinations de stockage à distance configurées, sélectionnez-les sous **Remote Destinations** pour télécharger automatiquement les sauvegardes planifiées
10. Cliquez sur **Save Schedule**

Le **Next Run** met à jour immédiatement et affiche quand la prochaine sauvegarde automatique aura lieu.

## Restaurer à partir d'une sauvegarde

La restauration remplace les données actuelles de votre magasin par le contenu d'une sauvegarde. Utilisez-la pour récupérer des données perdues ou pour annuler des changements indésirables.

> **Important :** La restauration remplacera toutes les données actuelles par celles de la sauvegarde. Votre magasin sera placé en mode maintenance pendant la restauration. Informez votre équipe avant d'exécuter une restauration.

1. Accédez à **Management > System Metrics**
2. Cliquez sur **Restore** dans la barre d'outils
3. La liste de restauration affiche toutes les sauvegardes disponibles avec leurs dates et tailles
4. Cliquez sur **Restore** à côté de la sauvegarde que vous souhaitez utiliser
5. Vérifiez l'écran de confirmation — il liste exactement ce qui sera remplacé
6. Tapez la phrase de confirmation si demandé, puis cliquez sur **Execute Restore**

Spwig affiche une barre de progression pendant que la restauration passe par ses étapes (sauvegarde de l'état actuel, téléchargement de la sauvegarde si elle est distante, restauration de la base de données, restauration des fichiers multimédias). Lorsqu'elle est terminée, le magasin sort automatiquement du mode maintenance.

## Configuration du stockage distant

Le stockage distant copie automatiquement vos sauvegardes vers une destination externe — Amazon S3, Google Drive, Dropbox ou un serveur SFTP. Cela vous protège contre les pannes au niveau du serveur.

1. Accédez à **Management > System Metrics**
2. Cliquez sur **Remote Storage**
3. Cliquez sur **Add Destination**
4. L'assistant d'installation vous guide à travers trois étapes :
   - **Étape 1** : Choisissez votre type de stockage (S3, Google Drive, Dropbox ou SFTP)
   - **Étape 2** : Entrez les identifiants de votre fournisseur choisi (voir les détails ci-dessous)
   - **Étape 3** : Nommez la destination et testez la connexion
5. Après que le test de connexion ait réussi, cliquez sur **Save**

### Amazon S3 (et services compatibles S3)

Vous aurez besoin de :
- **Access Key ID** et **Secret Access Key** de votre utilisateur AWS IAM
- **Bucket Name** — le bucket S3 vers lequel charger les sauvegardes
- **Region** — la région AWS où se trouve le bucket (ex. `us-east-1`)
- En option un **Prefix** (chemin d'un dossier à l'intérieur du bucket, ex. `spwig-backups/`)

Les services compatibles S3 (Backblaze B2, Wasabi, MinIO, etc.) fonctionnent de la même manière — entrez l'URL de point de terminaison personnalisé lorsque cela vous est demandé.

### Google Drive

Cliquez sur **Connect with Google** à l'étape des identifiants. Spwig ouvre une fenêtre Google OAuth — connectez-vous et accordez l'autorisation pour charger des fichiers. Aucun identifiant à copier manuellement.

### Dropbox

Cliquez sur **Connect with Dropbox** à l'étape des identifiants. Connectez-vous à Dropbox et approuvez l'accès. Les sauvegardes sont chargées dans un dossier `Apps/Spwig` de votre Dropbox.

### SFTP

Vous aurez besoin de :
- **Hostname** de votre serveur SFTP
- **Port** (par défaut : 22)
- **Username** et **Password** (ou clé privée SSH)
- **Remote Path** — le répertoire sur le serveur vers lequel charger les sauvegardes

### Définir une destination comme par défaut

Sur la page **Remote Storage**, cliquez sur le bouton d'activation à côté de toute destination pour la rendre **par défaut**. La destination par défaut reçoit automatiquement toutes les sauvegardes — manuelles et planifiées — sans avoir besoin de la sélectionner à chaque fois.

## Conseils

- Exécutez une sauvegarde manuelle avant chaque modification importante : importations de produits, modifications de thème, mises à niveau de la plateforme ou campagnes de réductions
- Planifiez des sauvegardes quotidiennes à un moment à faible trafic (ex. 03:00) pour minimiser tout impact sur les performances
- Configurez au moins une destination de stockage distant afin que les sauvegardes survivent même si le serveur lui-même a un problème
- Le paramètre **Retention Days** contrôle la durée pendant laquelle les sauvegardes locales sont conservées — 30 jours est une valeur par défaut raisonnable pour la plupart des magasins, mais augmentez-la si l'espace de stockage le permet
- Après une restauration, vérifiez quelques commandes et produits pour confirmer que les données semblent correctes avant de sortir manuellement le magasin du mode maintenance
- Les sauvegardes chiffrées ajoutent une couche de sécurité mais nécessitent la clé de déchiffrement pour les restaurer — ne la perdez pas