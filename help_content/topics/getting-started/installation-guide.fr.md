---
title: Guide d'installation
---

Ce guide vous guide à travers l'installation de Spwig sur votre propre serveur. Tout le processus est automatisé — une seule commande gère la configuration de Docker, la création de la base de données, la configuration des services et les certificats SSL.

## Avant de commencer

Vous avez besoin de :

- Un serveur exécutant **Ubuntu 22.04 ou 24.04** (Debian 12 également pris en charge)
- **Accès root ou sudo** au serveur
- Au moins **4 Go de RAM** et **20 Go d'espace disque** (8 Go de RAM recommandés)
- Un **jeton de licence** provenant de votre achat Spwig (vérifiez votre reçu par e-mail)
- Facultatif, un **nom de domaine** pointant vers l'adresse IP de votre serveur

> **Conseil :** Vous pouvez installer sans nom de domaine et en ajouter un plus tard à l'aide de l'outil de configuration des domaines. Votre boutique sera accessible via l'adresse IP du serveur en attendant.

## Exécution de l'installeur

Connectez-vous à votre serveur via SSH et exécutez la commande d'installation depuis votre e-mail de confirmation d'achat. Elle ressemble à ceci :

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Remplacez `YOUR_LICENSE_TOKEN` par le jeton de votre e-mail.

L'installeur passe automatiquement par huit étapes :

1. **Vérifications préalables** — vérifie que votre serveur répond aux exigences (OS, disque, RAM, ports)
2. **Validation du jeton** — confirme votre licence et extrait la configuration de votre boutique
3. **Détection du mode** — détermine le mode d'installation le plus adapté à votre serveur (voir ci-dessous)
4. **Configuration** — génère des mots de passe sécurisés, des identifiants de base de données et la configuration des services
5. **Téléchargement des images** — récupère les images de l'application Spwig depuis le registre
6. **Démarrage des services** — démarre la base de données, le cache, l'application et les workers en arrière-plan dans l'ordre
7. **Configuration SSL** — obtient un certificat SSL si vous avez un nom de domaine configuré
8. **Finalisation** — crée votre compte administrateur et génère des scripts pratiques

Le processus prend 5 à 15 minutes selon la vitesse d'internet de votre serveur.

## Modes d'installation

L'installeur détecte automatiquement l'environnement de votre serveur et sélectionne le mode le plus adapté. Vous pouvez également en spécifier un manuellement avec le drapeau `--mode`.

### Mode autonome

**Recommandé pour :** Serveurs dédiés et instances VPS où Spwig est la seule application web.

- Utilise directement les ports 80 et 443
- Gère automatiquement les certificats SSL via Let's Encrypt
- C'est le mode le plus courant et recommandé

### Mode sidecar

**Recommandé pour :** Serveurs qui hébergent déjà une autre application web (WordPress, un site web d'entreprise, etc.) sur les ports 80/443.

- Spwig s'exécute sur un port alternatif (détecté automatiquement, généralement 8080 ou 8443)
- L'installeur génère un bloc de configuration nginx que vous pouvez ajouter à votre serveur web existant
- Votre serveur web existant gère SSL et proxye le trafic vers Spwig

### Mode local

**Recommandé pour :** Développement et tests sur votre propre ordinateur.

- Accessible uniquement à `localhost` ou `127.0.0.1`
- Utilise un certificat SSL auto-signé (votre navigateur affichera une alerte de sécurité — c'est normal)
- Les fonctionnalités de débogage sont activées
- Aucune validation de licence n'est requise

## Ce qui se produit pendant l'installation

### Docker

Si Docker n'est pas déjà installé, l'installeur propose de l'installer pour vous. Spwig s'exécute entièrement dans des conteneurs Docker — rien n'est installé directement sur le système d'exploitation de votre serveur en dehors de Docker.

### Services créés

L'installeur crée les services suivants :

| Service | Purpose |
|---------|---------|
| **Base de données** (PostgreSQL 16) | Stocke toutes vos données de magasin — produits, commandes, clients, paramètres |
| **Cache** (Redis) | Accélère le chargement des pages et gère les files d'attente des tâches en arrière-plan |
| **Pile de connexions** (PgBouncer) | Gère efficacement les connexions à la base de données |
| **Stockage d'objets** (MinIO) | Stocke les images, fichiers et médias téléchargés |
| **Application** (Spwig) | Le magasin lui-même — panneau d'administration et boutique en ligne |
| **Serveur web** (Nginx) | Fournit votre magasin aux visiteurs avec du compression et du cache |
| **Travailleur en arrière-plan** (Celery) | Traite les e-mails, traductions, analyses et autres tâches en arrière-plan |
| **Planificateur de tâches** (Celery Beat) | Exécute les tâches planifiées comme les sauvegardes automatiques et les campagnes d'e-mail |
| **Traducteur** | Service de traduction alimenté par l'IA pour les magasins multilingues |
| **Mise à jour** | Gère les mises à jour des composants depuis le marché Spwig |

### Compte administrateur

À la fin de l'installation, vous êtes invité à créer un compte administrateur. C'est le compte que vous utiliserez pour vous connecter au panneau d'administration de votre magasin.

### Mode maintenance

Votre magasin démarre en **mode maintenance** — les visiteurs voient une page « À venir ». Cela vous donne le temps de configurer votre magasin (ajouter des produits, configurer les méthodes de paiement, personnaliser votre thème) avant de lancer.

Quand vous êtes prêt, exécutez le script de commodité créé par l'installateur :

```bash
./go-live.sh
```

Ou désactivez le mode maintenance depuis **Admin > Paramètres du magasin > Maintenance**.

## Après l'installation

Une fois que l'installateur a terminé, vous verrez un résumé avec :

- L'URL de votre magasin
- L'URL du panneau d'administration (généralement `https://yourdomain.com/en/admin/`)
- L'emplacement de vos fichiers de configuration
- Les scripts de commodité disponibles

### Scripts de commodité

L'installateur crée ces scripts dans votre répertoire d'installation :

- **`./go-live.sh`** — sort votre magasin du mode maintenance
- **`./configure-domain.sh`** — ajoute ou modifie votre domaine et obtient un certificat SSL

### Étapes suivantes

1. Connectez-vous à votre panneau d'administration
2. Terminez le **Assistant d'installation** — il vous guide à travers le nom du magasin, la devise, le fuseau horaire et les paramètres de base
3. Ajoutez vos produits
4. Configurez une méthode de paiement
5. Choisissez et personnalisez un thème
6. Exécutez `./go-live.sh` quand vous êtes prêt

## Installation sur des marchés cloud

Spwig est disponible en tant qu'application d'un clic sur plusieurs fournisseurs de cloud :

- **DigitalOcean** — déployez depuis le marché DigitalOcean
- **Akamai (Linode)** — déployez depuis le marché Linode
- **Vultr** — déployez depuis le marché Vultr

Ces images de marché viennent avec l'installateur préchargé. Après avoir créé le serveur, connectez-vous en SSH et suivez les instructions à l'écran pour terminer l'installation avec votre jeton de licence.

## Obtenir de l'aide

Si l'installation échoue ou si vous rencontrez une erreur :

1. Exécutez l'**outil de diagnostic** : `./doctor.sh` (créé pendant l'installation)
2. Le médecin vérifie tous les services, la connectivité, le SSL et les problèmes courants
3. Utilisez `./doctor.sh --fix` pour tenter des réparations automatiques
4. Contactez le support Spwig avec la sortie du médecin si le problème persiste