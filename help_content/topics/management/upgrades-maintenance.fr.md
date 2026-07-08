---
title: Mises à jour et maintenance
---

Spwig reçoit des mises à jour régulières avec de nouvelles fonctionnalités, des améliorations des performances et des correctifs de sécurité. Ce guide explique comment mettre à jour votre installation, utiliser l'outil de diagnostic et gérer les tâches de maintenance.

## Mise à jour de Spwig

### Avant de mettre à jour

1. **Créer une sauvegarde** — allez dans **Gestion > Métriques du système > Créer une sauvegarde complète** ou exécutez le script de sauvegarde depuis la ligne de commande. C'est votre filet de sécurité si quelque chose se passe mal.
2. **Vérifier la version actuelle** — visible dans **Gestion > Métriques du système** ou dans le pied de page du tableau de bord administrateur.
3. **Lire les notes de version** — disponibles dans le panneau administrateur sous **Gestion > Mises à jour des composants** lorsqu'une nouvelle version est détectée.

### Exécuter une mise à jour

Connectez-vous en SSH à votre serveur et accédez au répertoire d'installation de Spwig (généralement `/opt/spwig`) :

```bash
./upgrade.sh
```

Le script de mise à jour :

1. **Vérifications préalables** — vérifie l'espace disque, l'état de Docker et l'état des services
2. **Migrations de base de données en mode sec** — teste que les changements de base de données s'appliqueront proprement sans effectuer aucun changement
3. **Active le mode maintenance** — votre magasin affiche une page de maintenance aux visiteurs pendant la mise à jour
4. **Crée une sauvegarde** — sauvegarde automatique de sécurité avant d'apporter des modifications
5. **Vide les workers en arrière-plan** — attend que les tâches en cours (envoi d'e-mails, traductions) se terminent correctement
6. **Télécharge les nouvelles images** — télécharge l'application mise à jour depuis le registre Spwig
7. **Applique les migrations de base de données** — met à jour le schéma de base de données pour la nouvelle version
8. **Redémarre les services** — lance l'application avec la nouvelle version
9. **Vérification de l'état** — vérifie que tous les services fonctionnent correctement
10. **Désactive le mode maintenance** — votre magasin est de nouveau en ligne

Si la vérification de l'état échoue après la mise à jour, le script **retourne automatiquement à la version précédente** et restaure la sauvegarde.

### Options de mise à jour

```bash
./upgrade.sh              # Mise à jour standard avec mode maintenance
./upgrade.sh --dry-run    # Vérifie ce qui changerait sans l'appliquer
```

## L'outil de diagnostic

Spwig inclut un outil de diagnostic intégré qui vérifie toute votre installation pour détecter des problèmes :

```bash
./doctor.sh
```

Le médecin vérifie :

| Catégorie | Ce qu'il vérifie |
|----------|---------------|
| **Système** | Espace disque, utilisation de la RAM, charge CPU |
| **Docker** | Santé du moteur Docker, états des conteneurs, versions des images |
| **Base de données** | Connectivité PostgreSQL, statut des migrations, santé du pool de connexions |
| **Cache** | Connectivité Redis, utilisation de la mémoire |
| **Stockage objet** | Connectivité MinIO, accessibilité des buckets |
| **Réseau** | Résolution DNS, accessibilité des ports, validité du certificat SSL |
| **Application** | Points de terminaison de santé des services, statut des workers en arrière-plan |

Chaque vérification affiche un résultat pass/fail avec des détails si quelque chose ne va pas.

### Mode de réparation automatique

Pour les problèmes courants, le médecin peut tenter des réparations automatiques :

```bash
./doctor.sh --fix
```

Le mode de réparation automatique peut résoudre :

- Conteneurs arrêtés (les redémarre)
- Connexions de base de données obsolètes (recycle le pool de connexions)
- Certificats SSL expirés (déclenche le renouvellement)
- Disque plein à cause d'images Docker anciennes (supprime les images inutilisées)

Le médecin explique toujours ce qu'il va réparer avant d'agir.

## Mode maintenance

Le mode maintenance affiche aux visiteurs une page "le magasin est temporairement indisponible" pendant que vous apportez des modifications. Votre panneau administrateur reste accessible.

### Activer le mode maintenance

À partir du panneau administrateur : **Paramètres du magasin > Maintenance > Activer le mode maintenance**

Ou à partir de la ligne de commande :

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Désactiver le mode maintenance

À partir du panneau administrateur : basculez le commutateur de mode maintenance sur Off.

Ou à partir de la ligne de commande :

```bash
./go-live.sh
```

### Contournement de l'accès pendant le mode maintenance

Lorsque le mode maintenance est actif, vous pouvez accéder au magasin normalement en ajoutant un paramètre secret à l'URL. Le secret de contournement est affiché dans votre fichier de configuration `.env` sous `MAINTENANCE_SECRET`.

## Gestion des services

### Afficher l'état des services

Vérifiez l'état de tous les services Spwig :

```bash
docker compose ps
```

Cela affiche chaque service, son état (en cours d'exécution, arrêté, redémarrage) et son état de santé.

### Affichage des journaux

Vérifiez les journaux d'un service spécifique :

```bash
docker logs spwig_shop          # Journaux de l'application
docker logs spwig_celery         # Journaux des workers en arrière-plan
docker logs spwig_nginx          # Journaux d'accès du serveur web
docker logs spwig_db             # Journaux de la base de données
```

Ajoutez `--tail 100` pour afficher les 100 dernières lignes, ou `--follow` pour suivre les journaux en temps réel.

### Redémarrer un service

Si un service spécifique doit être redémarré :

```bash
docker compose restart shop      # Redémarrer l'application
docker compose restart celery    # Redémarrer les workers en arrière-plan
docker compose restart nginx     # Redémarrer le serveur web
```

Pour redémarrer tous les services :

```bash
docker compose restart
```

## Mises à jour des composants

Spwig propose un marché de composants où vous pouvez installer des thèmes, des fournisseurs de paiement, des intégrations de livraison et d'autres extensions. Les composants se mettent à jour indépendamment de la plateforme principale.

Accédez à **Management > Mises à jour des composants** pour vérifier les mises à jour de composants disponibles. Les mises à jour sont téléchargées et appliquées automatiquement lorsqu'on les approuve.

## Conseils

- **Mettez à jour régulièrement** — rester sur la dernière version garantit que vous avez les correctifs de sécurité et l'accès aux nouvelles fonctionnalités
- **Faites toujours une sauvegarde en premier** — même si le script de mise à jour crée une sauvegarde automatique, avoir la vôtre offre une sécurité supplémentaire
- **Exécutez doctor après les problèmes** — si votre magasin se comporte de manière inattendue, `./doctor.sh` est la méthode la plus rapide pour identifier les problèmes
- **Planifiez les mises à jour à des heures à faible trafic** — le mode maintenance interrompt brièvement l'accès des clients, donc mettez à jour pendant des heures calmes
- **Gardez de l'espace disque disponible** — les mises à jour nécessitent un espace temporaire pour de nouvelles images et des sauvegardes. Maintenez au moins 5 Go libres.