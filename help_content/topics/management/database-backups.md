---
slug: database-backups
title_i18n_key: Database Backups
category: getting-started
component: management
keywords:
  - database backup
  - create backup
  - backup schedule
  - automatic backup
  - download backup
  - restore backup
  - remote storage
  - Amazon S3
  - Google Drive
  - Dropbox
  - SFTP backup
  - backup encryption
  - data protection
  - backup retention
url_patterns:
  - /admin/management/systemmetrics/create-full-backup/
  - /admin/management/systemmetrics/backup-schedule/
  - /admin/management/systemmetrics/restore/
  - /admin/management/systemmetrics/remote-storage/
related:
  - maintenance-mode
  - shop-dashboard
published: true
---

Regular backups protect your store's data — orders, customers, products, and configuration — against hardware failures, accidental deletions, and other unexpected events. Spwig's backup system lets you create on-demand backups, set automatic schedules, download backups locally, restore from any saved backup, and copy backups to remote storage destinations like Amazon S3 or Google Drive.

Navigate to **Management > System Metrics** and use the toolbar links to access the backup tools.

![System Dashboard with backup tools](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Creating a manual backup

Run a backup any time before making significant changes — such as a product import, a theme update, or a platform upgrade.

1. Navigate to **Management > System Metrics**
2. Click **Create Full Backup** from the toolbar
3. Enter a descriptive **Name** for the backup (e.g., `before-july-import`)
4. Optionally add a **Description** to remind yourself why this backup was taken
5. Choose a **Backup Type**:
   - **Full System** — backs up the database and all media files (recommended)
   - **Database Only** — backs up store data only, excluding uploaded images and files
6. Choose **Compression** (`gzip` is the default and works well for most stores)
7. Click **Create Backup**

Spwig creates the backup in the background. A progress indicator shows the current stage. When complete, the backup appears in the **Database Backups** list with a **Completed** status and its file size.

## Downloading a backup

You can download any completed backup to keep a local copy on your computer.

1. Navigate to **Management > Database Backups**
2. Find the backup you want to download
3. Click the **Download** button next to it

The backup file downloads as a compressed archive. Store it in a safe place — on a separate device or cloud storage — so you have a copy independent of your server.

## Scheduling automatic backups

Automatic backups run in the background without any action from you, so your data is protected even if you forget to create manual backups.

1. Navigate to **Management > System Metrics**
2. Click **Backup Schedule**
3. Check **Enable Automatic Backups**
4. Set the **Frequency**:
   - **Daily** — runs once per day at the time you specify
   - **Weekly** — runs once per week on the day you choose
   - **Monthly** — runs on a specific day of the month
5. Set the **Time** the backup should run (server time, typically UTC — 03:00 AM is a good low-traffic time)
6. Choose the **Backup Type** (Full System or Database Only)
7. Set **Retention Days** — backups older than this many days are deleted automatically (default: 30 days)
8. Optionally check **Encrypt Backup** to encrypt the backup file at rest
9. If you have remote storage destinations configured, select them under **Remote Destinations** to automatically upload scheduled backups
10. Click **Save Schedule**

The **Next Run** timestamp updates immediately and shows when the next automatic backup will occur.

## Restoring from a backup

Restoring replaces your current store data with the contents of a backup. Use this to recover from data loss or to undo unwanted changes.

> **Important:** Restoring will replace all current data with the backup's data. Your store will be placed in maintenance mode during the restore. Inform your team before running a restore.

1. Navigate to **Management > System Metrics**
2. Click **Restore** from the toolbar
3. The restore list shows all available backups with their dates and sizes
4. Click **Restore** next to the backup you want to use
5. Review the confirmation screen — it lists exactly what will be replaced
6. Type the confirmation phrase if prompted, then click **Execute Restore**

Spwig shows a progress bar as the restore runs through its stages (backing up the current state, downloading the backup if remote, restoring the database, restoring media files). When complete, the store automatically exits maintenance mode.

## Setting up remote storage

Remote storage automatically copies your backups to an external destination — Amazon S3, Google Drive, Dropbox, or an SFTP server. This protects you against server-level failures.

1. Navigate to **Management > System Metrics**
2. Click **Remote Storage**
3. Click **Add Destination**
4. The setup wizard guides you through three steps:
   - **Step 1**: Choose your storage type (S3, Google Drive, Dropbox, or SFTP)
   - **Step 2**: Enter credentials for your chosen provider (see details below)
   - **Step 3**: Name the destination and test the connection
5. After the connection test passes, click **Save**

### Amazon S3 (and S3-compatible services)

You will need:
- **Access Key ID** and **Secret Access Key** from your AWS IAM user
- **Bucket Name** — the S3 bucket to upload backups to
- **Region** — the AWS region where the bucket is located (e.g., `us-east-1`)
- Optionally a **Prefix** (folder path inside the bucket, e.g., `spwig-backups/`)

S3-compatible services (Backblaze B2, Wasabi, MinIO, etc.) work the same way — enter the custom endpoint URL when prompted.

### Google Drive

Click **Connect with Google** on the credentials step. Spwig opens a Google OAuth window — sign in and grant permission to upload files. No credentials to copy manually.

### Dropbox

Click **Connect with Dropbox** on the credentials step. Sign in to Dropbox and approve access. Backups are uploaded to an `Apps/Spwig` folder in your Dropbox.

### SFTP

You will need:
- **Hostname** of your SFTP server
- **Port** (default: 22)
- **Username** and **Password** (or SSH private key)
- **Remote Path** — the directory on the server to upload backups to

### Setting a destination as default

On the **Remote Storage** page, click the toggle next to any destination to make it the **default**. The default destination automatically receives every backup — manual and scheduled — without needing to select it each time.

## Tips

- Run a manual backup before every significant change: product imports, theme edits, platform upgrades, or discount campaigns
- Schedule daily backups at a low-traffic time (e.g., 03:00 AM) to minimise any performance impact
- Set up at least one remote storage destination so backups survive even if the server itself has a problem
- The **Retention Days** setting controls how long local backups are kept — 30 days is a reasonable default for most stores, but increase it if storage space allows
- After a restore, check a few orders and products to confirm the data looks correct before taking the store out of maintenance mode manually
- Encrypted backups add a layer of security but require the decryption key to restore — do not lose it
