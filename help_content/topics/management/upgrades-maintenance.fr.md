---
title: Mises à jour et maintenance
---

Spwig reçoit des mises à jour régulières avec de nouvelles fonctionnalités, des améliorations des performances et des correctifs de sécurité. Ce guide explique comment mettre à jour votre installation, utiliser l'outil de diagnostic et gérer les tâches de maintenance.

## Mise à jour de Spwig

### Avant de mettre à jour

1. **Créer une sauvegarde** — allez à **Gestion > Métriques du système > Créer une sauvegarde complète** ou exécutez le script de sauvegarde depuis la ligne de commande. C'est votre filet de sécurité si quelque chose se passe mal.
2. **Vérifier la version actuelle** — visible dans **Gestion > Métriques du système** ou dans le pied de page du tableau de bord administrateur.
3. **Revoir les changements** — ouvrez la page **Mise à jour du système** pour lire les notes de version complètes de la nouvelle version avant l'installation, y compris les étapes supplémentaires que la mise à jour indique (voir ci-dessous).

### Révision des nouveautés sur la page de mise à jour du système

Lorsque Spwig détecte une version plus récente, **Tableau de bord du système** affiche une action rapide **Mise à jour disponible**. Cliquez dessus — ou accédez d'abord à **Tableau de bord du système > Mises à jour du plateforme** pour prévisualiser le journal des modifications, puis continuez — pour ouvrir la page **Mise à jour du système**.

La page affiche :

- **Version actuelle** et **Version disponible** cartes, afin que vous puissiez confirmer exactement les versions entre lesquelles vous passez
- Une section **Nouveautés dans {version}** — un court résumé de la mise à jour, suivie des notes de version complètes formatées avec des titres et des listes à puces, exactement comme les mainteneurs les ont rédigées
- **Vérifications pré-mise à jour** — l'espace disque, la connexion à la base de données, une sauvegarde récente, les permissions d'écriture et la connectivité au serveur de mise à jour Spwig. Cliquez sur **Exécuter les vérifications pré-vol** ; le bouton **Démarrer la mise à jour** reste désactivé jusqu'à ce que toutes les vérifications passent
- Un bandeau **Avant de mettre à jour** qui vous rappelle que une sauvegarde est créée automatiquement, votre magasin entre en mode maintenance pendant un court moment pendant la mise à jour, et vous ne devriez pas fermer la page ou naviguer ailleurs pendant qu'elle s'exécute

Lisez soigneusement les **Notes de mise à jour** dans la section Nouveautés — certaines versions indiquent des étapes que vous devez effectuer vous-même après la mise à jour. Par exemple, une version qui ajoute un nouveau format d'image pourrait vous demander de régénérer vos miniatures de produit à partir de **Bibliothèque multimédia > Traitement des images** afin que les images déjà dans votre bibliothèque profitent de l'amélioration ; les nouvelles uploads obtiennent automatiquement cette amélioration, mais votre catalogue existant nécessite un rafraîchissement manuel.

Une fois que les vérifications pré-vol sont passées, cliquez sur **Démarrer la mise à jour** pour commencer depuis le navigateur. Une barre de progression suit chaque étape, et la page se recharge automatiquement une fois la mise à jour terminée. C'est le chemin recommandé pour la plupart des commerçants — utilisez le script basé sur SSH ci-dessous si vous avez besoin d'un contrôle plus direct du processus.

### Exécuter une mise à jour

Connectez-vous en SSH à votre serveur et accédez à votre répertoire d'installation de Spwig (généralement `/opt/spwig`) :

```bash
./upgrade.sh
```

Le script de mise à jour :

1. **Vérifications pré-vol** — vérifie l'espace disque, l'état de Docker et l'état des services
2. **Migrations de base de données en mode sec** — teste que les changements de base de données s'appliqueront proprement sans effectuer réellement aucun changement
3. **Entre en mode maintenance** — votre magasin affiche une page de maintenance aux visiteurs pendant la mise à jour
4. **Crée une sauvegarde** — sauvegarde automatique de sécurité avant d'apporter des modifications
5. **Draine les workers en arrière-plan** — attend que les tâches en cours (envois d'e-mails, traductions) se terminent correctement
6. **Télécharge les nouvelles images** — télécharge l'application mise à jour depuis le registre Spwig
7. **Applique les migrations de base de données** — met à jour le schéma de base de données pour la nouvelle version
8. **Redémarre les services** — lance l'application avec la nouvelle version
9. **Vérification de l'état** — vérifie que tous les services fonctionnent correctement
10. **Sort du mode maintenance** — votre magasin est de nouveau en ligne

Si la vérification de l'état échoue après la mise à jour, le script **annule automatiquement** la mise à jour et restaure la sauvegarde.

### Options de mise à jour

```bash
./upgrade.sh              # Mise à jour standard avec mode maintenance
./upgrade.sh --dry-run    # Vérifier ce qui changerait sans l'appliquer
```

## L'outil de diagnostic

Spwig inclut un outil de diagnostic intégré qui vérifie toute votre installation pour détecter les problèmes :

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
| **Stockage d'objets** | Connectivité MinIO, accessibilité des buckets |
| **Réseau** | Résolution DNS, accessibilité des ports, validité du certificat SSL |
| **Application** | Points de terminaison de santé des services, statut des workers en arrière-plan |

Chaque vérification affiche un résultat pass/fail avec des détails si quelque chose ne va pas.

### Mode de réparation automatique

Pour les problèmes courants, le médecin peut tenter des réparations automatiques :

```bash
./doctor.sh --fix
```

La réparation automatique peut résoudre :

- Conteneurs arrêtés (les redémarre)
- Connexions de base de données obsolètes (recycle le pool de connexions)
- Certificats SSL expirés (déclenche la renouvellement)
- Disque plein à cause d'images Docker anciennes (nettoie les images non utilisées)

Le médecin explique toujours ce qu'il va réparer avant d'agir.

## Mode maintenance

Le mode maintenance affiche aux visiteurs une page "le magasin est temporairement indisponible" pendant que vous effectuez des modifications. Votre panneau d'administration reste accessible.

### Activer le mode maintenance

À partir du panneau d'administration : **Paramètres du magasin > Maintenance > Activer le mode maintenance**

Ou à partir de la ligne de commande :

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Désactiver le mode maintenance

À partir du panneau d'administration : basculer le commutateur de mode maintenance sur Off.

Ou à partir de la ligne de commande :

```bash
./go-live.sh
```

### Contournement d'accès pendant le mode maintenance

Lorsque le mode maintenance est actif, vous pouvez accéder au magasin normalement en ajoutant un paramètre secret à l'URL. Le secret de contournement est affiché dans votre fichier de configuration `.env` sous `MAINTENANCE_SECRET`.

## Gestion des services

### Vérifier l'état des services

Vérifiez l'état de tous les services Spwig :

```bash
docker compose ps
```

Cela affiche chaque service, son état (en cours d'exécution, arrêté, redémarrage), et son statut de santé.

### Vérifier les journaux

Vérifiez les journaux d'un service spécifique :

```bash
docker logs spwig_shop          # Journaux de l'application
docker logs spwig_celery         # Journaux des workers en arrière-plan
docker logs spwig_nginx          # Journaux d'accès du serveur web
docker logs spwig_db             # Journaux de la base de données
```

Ajoutez `--tail 100` pour voir les 100 dernières lignes, ou `--follow` pour suivre les journaux en temps réel.

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

Accédez à **Gestion > Mises à jour des composants** pour vérifier les mises à jour des composants disponibles. Les mises à jour sont téléchargées et appliquées automatiquement lorsque vous les approuvez.

## Conseils

- **Mettez régulièrement à jour** — rester sur la dernière version vous assure des correctifs de sécurité et l'accès aux nouvelles fonctionnalités
- **Lisez la section Qu'est-ce de neuf avant de cliquer sur Démarrer la mise à jour** — c'est la façon la plus rapide d'identifier une migration de base de données requise, un correctif de sécurité ou une note de mise à jour **à laquelle vous devez agir après**
- **Faites toujours une sauvegarde** — même si le script de mise à jour crée une sauvegarde automatique, avoir votre propre sauvegarde offre une sécurité supplémentaire
- **Exécutez le médecin après les problèmes** — si votre magasin se comporte de manière inattendue, `./doctor.sh` est la façon la plus rapide d'identifier les problèmes
- **Planifiez les mises à jour à des heures à faible trafic** — le mode maintenance interrompt brièvement l'accès des clients, donc mettez à jour pendant les heures creuses
- **Maintenez de l'espace disque disponible** — les mises à jour nécessitent un espace temporaire pour de nouvelles images et des sauvegardes. Gardez au moins 5 Go libres.