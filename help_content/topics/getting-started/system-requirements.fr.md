---
title: Exigences système
---

Spwig fonctionne sur la plupart des serveurs Linux modernes. Cette page couvre les spécifications minimales et recommandées, ce qui se produit sur des serveurs plus petits, ainsi que les fournisseurs de cloud qui fonctionnent bien.

## Exigences minimales

| Ressource | Minimum | Recommandé |
|----------|---------|-------------|
| **Système d'exploitation** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS ou Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 Go | 8 Go ou plus |
| **Espace disque** | 20 Go | 40 Go ou plus |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Architecture** | x86_64 (AMD64) | x86_64 |
| **Réseau** | Adresse IP publique (en mode autonome) | Adresse IP publique statique |
| **Ports** | 80 et 443 (autonome) ou tout autre port (sidecar) | 80 et 443 |

> **Note :** Les serveurs basés sur ARM (par exemple, AWS Graviton, Oracle Ampere) ne sont actuellement pas pris en charge.

## Niveaux de ressources

L'installeur détecte automatiquement la RAM disponible sur votre serveur et sélectionne le niveau de ressource approprié.

### Niveau standard (6 Go+ de RAM)

Tous les services fonctionnent avec toutes les fonctionnalités :

- Service de **traduction alimenté par l'IA** activé — traduisez les descriptions de produits, le contenu des pages et le texte SEO en plusieurs langues directement depuis votre tableau de bord
- Allocation complète de mémoire pour l'application, la base de données et les workers en arrière-plan
- Concurrency des workers en arrière-plan optimisée pour le nombre de CPU

### Niveau petit (4–6 Go de RAM)

L'installeur s'adapte pour économiser de la mémoire :

- Le service de traduction par IA est **désactivé** pour économiser environ 2 Go de RAM. Vous pouvez toujours gérer les traductions manuellement ou utiliser des outils de traduction externes — seul le traducteur IA intégré est affecté.
- Les limites de mémoire de l'application et des workers sont réduites
- Toutes les autres fonctionnalités fonctionnent de la même manière que le niveau standard

> **Conseil :** Si vous commencez sur un petit serveur et que vous mettez plus tard à niveau vers 6 Go+ de RAM, exécutez à nouveau l'installeur pour activer le service de traduction.

## Fournisseurs de cloud recommandés

Spwig fonctionne sur tout serveur Linux qui répond aux exigences. Ces fournisseurs ont été testés et offrent une bonne valeur :

| Fournisseur | Plan recommandé | RAM | Disque | Coût approximatif |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet de base | 4 Go | 80 Go | 24 $/mois |
| **Linode (Akamai)** | Partagé 4 Go | 4 Go | 80 Go | 24 $/mois |
| **Vultr** | Calcul en nuage | 4 Go | 100 Go | 24 $/mois |
| **Hetzner** | CX31 | 8 Go | 80 Go | 8 €/mois |
| **OVH** | VPS Starter | 4 Go | 80 Go | 7 €/mois |

Pour les magasins anticipant un trafic important ou de grands catalogues de produits (10 000+ produits), commencez avec 8 Go de RAM et 2+ vCPUs.

## Utilisation de l'espace disque

Une installation Spwig fraîche utilise environ 8 Go d'espace disque :

| Composant | Taille |
|-----------|------|
| Images Docker | ~4 Go |
| Base de données (magasin vide) | ~200 Mo |
| Modèles de traduction par IA (si activés) | ~2 Go |
| Fichiers d'application et de configuration | ~500 Mo |
| Système d'exploitation et moteur Docker | ~3 Go |

Planifiez un espace supplémentaire pour :

- **Images et médias de produits** — dépend de la taille de votre catalogue. Prévoyez 1–5 Go pour un magasin typique avec des centaines de produits.
- **Croissance de la base de données** — augmente avec les commandes, les clients et les données d'analyse. Un magasin traitant 100 commandes par jour augmente généralement de ~1 Go par an.
- **Sauvegardes** — si vous stockez des sauvegardes localement, chaque sauvegarde complète est approximativement de la taille de votre base de données plus les médias. Avec une politique de rétention de 30 jours, prévoyez 2–3× la taille de vos données actuelles.

## Domaine et DNS

Un nom de domaine est optionnel lors de l'installation mais requis pour l'utilisation en production. Vous avez besoin de :

- Un domaine ou un sous-domaine (par exemple, `shop.example.com`)
- Un **enregistrement A** pointant vers l'adresse IP publique de votre serveur
- Une propagation DNS terminée (généralement 5–60 minutes après l'ajout de l'enregistrement)

L'installeur obtient automatiquement un certificat SSL gratuit de Let's Encrypt lorsqu'un domaine valide est détecté. Vous pouvez également ajouter un domaine après l'installation en utilisant le script `./configure-domain.sh`.

## Pare-feu

Si votre serveur dispose d'un pare-feu (la plupart des fournisseurs de cloud en activent un par défaut), assurez-vous que ces ports sont ouverts :

| Port | Protocole | Objectif |
|------|----------|---------|
| **22** | TCP | Accès SSH (pour que vous puissiez gérer le serveur) |
| **80** | TCP | HTTP (nécessaire pour la validation du certificat Let's Encrypt) |
| **443** | TCP | HTTPS (le trafic sécurisé de votre magasin) |

En mode sidecar, ouvrez le port alternatif assigné par l'installateur au lieu de 80/443.

## Prérequis logiciels

L'installateur gère automatiquement l'installation de tous les logiciels. À titre de référence, ce sont les composants qu'il installe ou vérifie :

- **Docker Engine** — runtime de conteneurs (installé automatiquement s'il manque)
- **Docker Compose** — orchestration de services (inclus avec Docker Engine)
- **curl** — utilisé par l'installateur lui-même (présent sur la plupart des systèmes Linux)

Aucun autre logiciel n'a besoin d'être préinstallé. Spwig ne vous oblige pas à installer manuellement Python, Node.js, PostgreSQL, Redis ou Nginx — tout fonctionne à l'intérieur des conteneurs Docker.