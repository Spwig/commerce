---
title: Datenbank-Backups
---

Regelmäßige Backups schützen Ihre Store-Daten – Bestellungen, Kunden, Produkte und Konfiguration – vor Hardwareausfällen, versehentlichen Löschungen und anderen unerwarteten Ereignissen. Das Backup-System von Spwig ermöglicht es Ihnen, auf Anfrage Backups zu erstellen, automatische Zeitpläne festzulegen, Backups lokal herunterzuladen, aus einem beliebigen gespeicherten Backup wiederherzustellen und Backups auf entfernte Speicherorte wie Amazon S3 oder Google Drive zu kopieren.

Navigieren Sie zu **Management > System Metrics** und verwenden Sie die Symbolleisten-Links, um die Backup-Tools zu öffnen.

![System Dashboard mit Backup-Tools](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Manuelles Erstellen eines Backups

Führen Sie ein Backup jederzeit vor dem Durchführen wichtiger Änderungen durch – beispielsweise bei einem Produktimport, einer Theme-Aktualisierung oder einer Plattform-Upgrade.

1. Navigieren Sie zu **Management > System Metrics**
2. Klicken Sie auf **Create Full Backup** in der Symbolleiste
3. Geben Sie einen beschreibenden **Name** für das Backup an (z. B. `before-july-import`)
4. Fügen Sie optional eine **Beschreibung** hinzu, um sich daran zu erinnern, warum dieses Backup erstellt wurde
5. Wählen Sie einen **Backup-Typ**:
   - **Full System** – sichert die Datenbank und alle Mediendateien (empfohlen)
   - **Database Only** – sichert nur die Store-Daten, ohne hochgeladene Bilder und Dateien
6. Wählen Sie **Kompression** (`gzip` ist der Standard und eignet sich gut für die meisten Stores)
7. Klicken Sie auf **Create Backup**

Spwig erstellt das Backup im Hintergrund. Ein Fortschrittsindikator zeigt den aktuellen Status an. Nach Abschluss erscheint das Backup in der Liste **Database Backups** mit dem Status **Completed** und der Dateigröße.

## Backup herunterladen

Sie können jedes abgeschlossene Backup herunterladen, um eine lokale Kopie auf Ihrem Computer zu speichern.

1. Navigieren Sie zu **Management > Database Backups**
2. Finden Sie das Backup, das Sie herunterladen möchten
3. Klicken Sie auf den **Download**-Button neben dem Backup

Das Backup-Datei wird als komprimiertes Archiv heruntergeladen. Speichern Sie es an einem sicheren Ort – auf einem separaten Gerät oder in der Cloud –, damit Sie eine Kopie haben, die unabhängig von Ihrem Server ist.

## Automatische Backups planen

Automatische Backups laufen im Hintergrund, ohne dass Sie etwas tun müssen, sodass Ihre Daten auch geschützt sind, wenn Sie versehentlich manuelle Backups vergessen.

1. Navigieren Sie zu **Management > System Metrics**
2. Klicken Sie auf **Backup Schedule**
3. Aktivieren Sie **Enable Automatic Backups**
4. Wählen Sie die **Frequency**:
   - **Daily** – läuft einmal pro Tag zur von Ihnen festgelegten Zeit
   - **Weekly** – läuft einmal pro Woche an dem Tag, den Sie auswählen
   - **Monthly** – läuft an einem bestimmten Tag im Monat
5. Wählen Sie die **Time**, zu der das Backup laufen soll (Serverzeit, typischerweise UTC – 03:00 AM ist eine gute Zeit mit geringem Verkehr)
6. Wählen Sie den **Backup-Typ** (Full System oder Database Only)
7. Legen Sie **Retention Days** fest – Backups, die älter als diese Anzahl von Tagen sind, werden automatisch gelöscht (Standard: 30 Tage)
8. Aktivieren Sie optional **Encrypt Backup**, um das Backup-Datei im Ruhezustand zu verschlüsseln
9. Wenn Sie entfernte Speicherorte konfiguriert haben, wählen Sie sie unter **Remote Destinations** aus, um geplante Backups automatisch hochzuladen
10. Klicken Sie auf **Save Schedule**

Der **Next Run**-Zeitstempel wird sofort aktualisiert und zeigt an, wann das nächste automatische Backup stattfinden wird.

## Aus einem Backup wiederherstellen

Das Wiederherstellen ersetzt Ihre aktuellen Store-Daten durch den Inhalt eines Backups. Verwenden Sie dies, um aus Datenverlusten zu recoveren oder unerwünschte Änderungen rückgängig zu machen.

> **Wichtig:** Das Wiederherstellen ersetzt alle aktuellen Daten durch die Daten des Backups. Der Store wird während des Wiederherstellungsprozesses in den Wartungsmodus versetzt. Informieren Sie Ihr Team, bevor Sie eine Wiederherstellung durchführen.

1. Navigieren Sie zu **Management > System Metrics**
2. Klicken Sie auf **Restore** in der Symbolleiste
3. Die Wiederherstellungsliste zeigt alle verfügbaren Backups mit ihren Daten und Größen an
4. Klicken Sie auf **Restore** neben dem Backup, das Sie verwenden möchten
5. Überprüfen Sie das Bestätigungsdialogfeld – es listet genau auf, was ersetzt wird
6. Geben Sie bei Bedarf das Bestätigungsphrasen ein und klicken Sie auf **Execute Restore**

Spwig zeigt eine Fortschrittsleiste an, während die Wiederherstellung durch ihre Schritte läuft (Sichern des aktuellen Zustands, Herunterladen des Backups, wenn es remote ist, Wiederherstellen der Datenbank, Wiederherstellen der Mediendateien). Nach Abschluss verlässt der Store automatisch den Wartungsmodus.

## Remote Storage einrichten

Remote Storage kopiert Ihre Backups automatisch an einen externen Zielort – Amazon S3, Google Drive, Dropbox oder einen SFTP-Server. Dies schützt Sie vor Serverfehlern.

1. Navigieren Sie zu **Management > System Metrics**
2. Klicken Sie auf **Remote Storage**
3. Klicken Sie auf **Ziel hinzufügen**
4. Der Einrichtungsführer führt Sie durch drei Schritte:
   - **Schritt 1**: Wählen Sie den Speichertyp (S3, Google Drive, Dropbox oder SFTP)
   - **Schritt 2**: Geben Sie die Anmeldeinformationen für Ihren gewählten Anbieter ein (siehe Details unten)
   - **Schritt 3**: Benennen Sie das Ziel und testen Sie die Verbindung
5. Nachdem der Verbindungstest erfolgreich war, klicken Sie auf **Speichern**

### Amazon S3 (und S3-kompatible Dienste)

Sie benötigen:
- **Access Key ID** und **Secret Access Key** von Ihrem AWS IAM-Benutzer
- **Bucket Name** – den S3-Bucket, in den Backups hochgeladen werden sollen
- **Region** – die AWS-Region, in der sich der Bucket befindet (z. B. `us-east-1`)
- Optional ein **Prefix** (Ordnerpfad innerhalb des Buckets, z. B. `spwig-backups/`)

S3-kompatible Dienste (Backblaze B2, Wasabi, MinIO usw.) funktionieren auf die gleiche Weise – geben Sie die benutzerdefinierte Endpunkt-URL ein, wenn Sie dazu aufgefordert werden.

### Google Drive

Klicken Sie auf **Mit Google verbinden**, wenn Sie auf dem Schritt der Anmeldeinformationen sind. Spwig öffnet ein Google OAuth-Fenster – melden Sie sich an und erteilen Sie die Berechtigung, Dateien hochzuladen. Es gibt keine Anmeldeinformationen, die Sie manuell kopieren müssen.

### Dropbox

Klicken Sie auf **Mit Dropbox verbinden**, wenn Sie auf dem Schritt der Anmeldeinformationen sind. Melden Sie sich bei Dropbox an und genehmigen Sie den Zugriff. Backups werden in den Ordner `Apps/Spwig` in Ihrem Dropbox-Ordner hochgeladen.

### SFTP

Sie benötigen:
- **Hostname** Ihres SFTP-Servers
- **Port** (Standard: 22)
- **Benutzername** und **Passwort** (oder SSH-Privatschlüssel)
- **Remote Path** – den Ordner auf dem Server, in den Backups hochgeladen werden sollen

### Ziel als Standard einstellen

Auf der Seite **Remote Storage** klicken Sie auf den Schalter neben einem beliebigen Ziel, um es zum **Standard** zu machen. Das Standardziel erhält automatisch jede Backup – manuell und geplant – ohne, dass Sie es jedes Mal auswählen müssen.

## Tipps

- Führen Sie vor jeder bedeutenden Änderung eine manuelle Sicherung durch: Produkteinläufe, Theme-Änderungen, Plattform-Upgrades oder Rabattkampagnen
- Planen Sie tägliche Backups zu einer Zeit mit geringer Auslastung (z. B. 03:00 Uhr) um den Leistungsverlust zu minimieren
- Richten Sie mindestens ein Remote Storage-Ziel ein, damit Backups auch dann noch vorhanden sind, wenn der Server selbst ein Problem hat
- Die Einstellung **Retention Days** bestimmt, wie lange lokale Backups gespeichert werden – 30 Tage ist eine vernünftige Standardoption für die meisten Geschäfte, erhöhen Sie sie jedoch, wenn der Speicherplatz es zulässt
- Nach einer Wiederherstellung überprüfen Sie einige Bestellungen und Produkte, um sicherzustellen, dass die Daten korrekt aussehen, bevor Sie das Geschäft manuell aus dem Wartungsmodus nehmen
- Verschlüsselte Backups bieten eine zusätzliche Sicherheitsschicht, erfordern jedoch den Entschlüsselungsschlüssel, um sie wiederherzustellen – verlieren Sie ihn nicht