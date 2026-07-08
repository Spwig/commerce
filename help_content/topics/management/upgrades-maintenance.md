---
slug: upgrades-maintenance
title_i18n_key: Upgrades & Maintenance
category: getting-started
component: management
keywords:
  - upgrade
  - update
  - maintenance
  - version
  - doctor
  - diagnostics
  - health check
  - rollback
  - backup before upgrade
url_patterns: []
related:
  - database-backups
  - maintenance-mode
  - installation-guide
  - system-requirements
published: true
---

Spwig receives regular updates with new features, performance improvements, and security fixes. This guide covers how to upgrade your installation, use the diagnostic tool, and handle maintenance tasks.

## Upgrading Spwig

### Before you upgrade

1. **Create a backup** — go to **Management > System Metrics > Create Full Backup** or run the backup script from the command line. This is your safety net if anything goes wrong.
2. **Check current version** — visible in **Management > System Metrics** or on the admin dashboard footer.
3. **Read the release notes** — available in the admin panel under **Management > Component Updates** when a new version is detected.

### Running an upgrade

SSH into your server and navigate to your Spwig installation directory (typically `/opt/spwig`):

```bash
./upgrade.sh
```

The upgrade script:

1. **Pre-flight checks** — verifies disk space, Docker health, and service status
2. **Dry-run database migrations** — tests that database changes will apply cleanly without actually changing anything
3. **Enters maintenance mode** — your store shows a maintenance page to visitors during the upgrade
4. **Creates a backup** — automatic safety backup before making changes
5. **Drains background workers** — waits for in-progress tasks (email sends, translations) to finish gracefully
6. **Pulls new images** — downloads the updated application from the Spwig registry
7. **Applies database migrations** — updates your database schema for the new version
8. **Restarts services** — brings up the application with the new version
9. **Health check** — verifies all services are running correctly
10. **Exits maintenance mode** — your store is back online

If the health check fails after the upgrade, the script **automatically rolls back** to the previous version and restores the backup.

### Upgrade options

```bash
./upgrade.sh              # Standard upgrade with maintenance mode
./upgrade.sh --dry-run    # Check what would change without applying
```

## The diagnostic tool

Spwig includes a built-in diagnostic tool that checks your entire installation for issues:

```bash
./doctor.sh
```

The doctor checks:

| Category | What it checks |
|----------|---------------|
| **System** | Disk space, RAM usage, CPU load |
| **Docker** | Docker engine health, container states, image versions |
| **Database** | PostgreSQL connectivity, migration status, connection pool health |
| **Cache** | Redis connectivity, memory usage |
| **Object storage** | MinIO connectivity, bucket accessibility |
| **Network** | DNS resolution, port accessibility, SSL certificate validity |
| **Application** | Service health endpoints, background worker status |

Each check shows a pass/fail result with details if something is wrong.

### Auto-fix mode

For common issues, the doctor can attempt automatic repairs:

```bash
./doctor.sh --fix
```

Auto-fix can resolve:

- Stopped containers (restarts them)
- Stale database connections (recycles the connection pool)
- Expired SSL certificates (triggers renewal)
- Full disk from old Docker images (prunes unused images)

The doctor always explains what it will fix before taking action.

## Maintenance mode

Maintenance mode shows visitors a "store is temporarily unavailable" page while you make changes. Your admin panel remains accessible.

### Enabling maintenance mode

From the admin panel: **Store Settings > Maintenance > Enable Maintenance Mode**

Or from the command line:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Disabling maintenance mode

From the admin panel: toggle the maintenance mode switch off.

Or from the command line:

```bash
./go-live.sh
```

### Bypass access during maintenance

While maintenance mode is active, you can access the store normally by adding a secret parameter to the URL. The bypass secret is shown in your `.env` configuration file under `MAINTENANCE_SECRET`.

## Managing services

### Viewing service status

Check the status of all Spwig services:

```bash
docker compose ps
```

This shows each service, its state (running, stopped, restarting), and its health status.

### Viewing logs

Check logs for a specific service:

```bash
docker logs spwig_shop          # Application logs
docker logs spwig_celery         # Background worker logs
docker logs spwig_nginx          # Web server access logs
docker logs spwig_db             # Database logs
```

Add `--tail 100` to see the last 100 lines, or `--follow` to watch logs in real time.

### Restarting a service

If a specific service needs restarting:

```bash
docker compose restart shop      # Restart the application
docker compose restart celery    # Restart background workers
docker compose restart nginx     # Restart the web server
```

To restart all services:

```bash
docker compose restart
```

## Component updates

Spwig features a component marketplace where you can install themes, payment providers, shipping integrations, and other extensions. Components update independently from the core platform.

Navigate to **Management > Component Updates** to check for available component updates. Updates are downloaded and applied automatically when you approve them.

## Tips

- **Upgrade regularly** — staying on the latest version ensures you have security fixes and access to new features
- **Always backup first** — even though the upgrade script creates an automatic backup, having your own gives extra safety
- **Run doctor after issues** — if your store behaves unexpectedly, `./doctor.sh` is the fastest way to identify problems
- **Schedule upgrades for low-traffic times** — maintenance mode briefly interrupts customer access, so upgrade during quiet hours
- **Keep disk space available** — upgrades need temporary space for new images and backups. Maintain at least 5 GB free.
