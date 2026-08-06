---
title: Upgrades & Wartung
---

Spwig erhält regelmäßig Updates mit neuen Funktionen, Leistungsverbesserungen und Sicherheitskorrekturen. Dieser Leitfaden behandelt, wie Sie Ihre Installation aktualisieren, das Diagnose-Tool verwenden und Wartungsaufgaben durchführen können.

## Spwig aktualisieren

### Vor der Aktualisierung

1. **Backup erstellen** — navigieren Sie zu **Management > System Metrics > Create Full Backup** oder führen Sie das Backup-Skript über die Kommandozeile aus. Dies ist Ihr Sicherheitsnetz, falls etwas schief geht.
2. **Aktuelle Version prüfen** — sichtbar in **Management > System Metrics** oder im Fußbereich der Admin-Dashboard.
3. **Änderungen überprüfen** — öffnen Sie die Seite **System Upgrade**, um die vollständigen Release Notes der neuen Version vor der Installation zu lesen, einschließlich aller zusätzlichen Schritte, die der Release erwähnt (siehe unten).

### Neue Funktionen auf der Seite System Upgrade überprüfen

Wenn Spwig eine neuere Version erkennt, zeigt **System Dashboard** eine schnelle Aktion **Update Available** an. Klicken Sie darauf — oder navigieren Sie zunächst zu **System Dashboard > Platform Updates**, um den Änderungsprotokoll vorab anzusehen, und dann fortfahren —, um die Seite **System Upgrade** zu öffnen.

Die Seite zeigt:

- **Current Version** und **Available Version** Karten, damit Sie genau bestätigen können, zwischen welchen Versionen Sie wechseln
- Ein Abschnitt **What's New in {version}** — eine kurze Zusammenfassung des Releases, gefolgt von den vollständigen Release Notes, formatiert mit Überschriften und Aufzählungen, genau wie die Maintainer sie geschrieben haben
- **Pre-Upgrade Checks** — Speicherplatz, Datenbankverbindung, eine kürzliche Sicherung, Schreibrechte und die Verbindung zum Spwig-Update-Server. Klicken Sie auf **Run Pre-flight Checks**; der **Start Upgrade**-Button bleibt deaktiviert, bis alle Prüfungen bestanden sind
- Ein Banner **Before You Upgrade**, der Sie daran erinnert, dass ein Backup automatisch erstellt wird, Ihr Geschäft kurzzeitig in den Wartungsmodus wechselt, während die Aktualisierung läuft, und Sie währenddessen die Seite nicht schließen oder navigieren sollten

Lesen Sie die **Upgrade notes** im Abschnitt What's New sorgfältig — einige Releases erwähnen Schritte, die Sie nach der Aktualisierung selbst durchführen müssen. Zum Beispiel könnte ein Release, das ein neues Bildformat hinzufügt, Sie bitten, Ihre Produktvorschaubilder aus **Media Library > Image Processing** neu zu generieren, damit bereits vorhandene Bilder in Ihrer Bibliothek die Verbesserung nutzen; neue Uploads erhalten dies automatisch, aber Ihr bestehender Katalog benötigt eine manuelle Aktualisierung.

Sobald die Vorflug-Prüfungen bestanden sind, klicken Sie auf **Start Upgrade**, um den Vorgang über den Browser zu starten. Ein Fortschrittsbalken verfolgt jede Phase, und die Seite lädt sich automatisch neu, sobald die Aktualisierung abgeschlossen ist. Dies ist der empfohlene Weg für die meisten Händler — verwenden Sie das unten stehende SSH-basierte Skript, wenn Sie mehr direkte Kontrolle über den Prozess benötigen.

### Eine Aktualisierung durchführen

SSH in Ihren Server und navigieren Sie zu Ihrem Spwig-Installationverzeichnis (typischerweise `/opt/spwig`):

```bash
./upgrade.sh
```

Das Upgrade-Skript:

1. **Vorflug-Prüfungen** — überprüft den Speicherplatz, den Docker-Status und den Dienststatus
2. **Test-Übertragung der Datenbankmigrationen** — testet, ob Datenbankänderungen sauber angewendet werden können, ohne tatsächlich etwas zu ändern
3. **In den Wartungsmodus wechseln** — Ihr Geschäft zeigt während der Aktualisierung eine Wartungsseite für Besucher an
4. **Backup erstellen** — automatisches Sicherheitsbackup vor Änderungen
5. **Hintergrundarbeiter entladen** — wartet, bis laufende Aufgaben (E-Mail-Versand, Übersetzungen) sanft abgeschlossen werden
6. **Neue Bilder abrufen** — lädt die aktualisierte Anwendung von der Spwig-Registrierung herunter
7. **Datenbankmigrationen anwenden** — aktualisiert Ihre Datenbankschema für die neue Version
8. **Dienste neu starten** — startet die Anwendung mit der neuen Version
9. **Gesundheitsprüfung** — überprüft, ob alle Dienste korrekt laufen
10. **Aus dem Wartungsmodus austreten** — Ihr Geschäft ist wieder online

Falls die Gesundheitsprüfung nach der Aktualisierung fehlschlägt, rollt das Skript **automatisch zurück** auf die vorherige Version und stellt das Backup wieder her.

### Upgrade-Optionen

```bash
./upgrade.sh              # Standard-Upgrade mit Wartungsmodus
./upgrade.sh --dry-run    # Prüfen, was sich ändern würde, ohne es anzuwenden
```

## Das Diagnose-Tool

Spwig verfügt über ein eingebautes Diagnose-Tool, das Ihre gesamte Installation auf Probleme überprüft:

```bash
./doctor.sh
```

Der Doctor überprüft:

| Kategorie | Was er überprüft |
|----------|---------------|
| **System** | Speicherplatz, RAM-Nutzung, CPU-Auslastung |
| **Docker** | Gesundheit des Docker-Engines, Containerzustände, Bildversionen |
| **Datenbank** | PostgreSQL-Verbindung, Migrationsstatus, Gesundheit des Verbindungssees |
| **Cache** | Redis-Verbindung, Speichernutzung |
| **Objekt-Speicher** | MinIO-Verbindung, Zugänglichkeit von Buckets |
| **Netzwerk** | DNS-Auflösung, Port-Zugänglichkeit, Gültigkeit des SSL-Zertifikats |
| **Anwendung** | Gesundheitsendpunkte der Dienste, Status der Hintergrundarbeiter |

Jede Überprüfung zeigt ein Bestanden/Nicht-bestanden-Ergebnis mit Details, wenn etwas falsch ist.

### Automatische Reparaturmodus

Für häufige Probleme kann der Doctor automatische Reparaturen versuchen:

```bash
./doctor.sh --fix
```

Automatische Reparatur kann folgende Probleme beheben:

- Gestoppte Container (startet sie erneut)
- Veraltete Datenbankverbindungen (verwirft den Verbindungssee)
- Abgelaufene SSL-Zertifikate (löst die Verlängerung aus)
- Voller Speicher aufgrund alter Docker-Images (entfernt nicht verwendete Images)

Der Doctor erklärt immer, was er reparieren wird, bevor er Handlungen durchführt.

## Wartungsmodus

Der Wartungsmodus zeigt Besuchern eine Seite mit der Meldung "Der Shop ist vorübergehend nicht verfügbar", während Sie Änderungen vornehmen. Ihr Admin-Panel bleibt weiterhin zugänglich.

### Aktivieren des Wartungsmodus

Von der Admin-Oberfläche: **Store Einstellungen > Wartung > Wartungsmodus aktivieren**

Oder von der Kommandozeile:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Deaktivieren des Wartungsmodus

Von der Admin-Oberfläche: Schalten Sie den Wartungsmodus-Schalter aus.

Oder von der Kommandozeile:

```bash
./go-live.sh
```

### Umgehen des Wartungsmodus

Wenn der Wartungsmodus aktiv ist, können Sie den Shop normal betreten, indem Sie einen geheimen Parameter zur URL hinzufügen. Der Umgehungsgeheimnis wird in Ihrer `.env`-Konfigurationsdatei unter `MAINTENANCE_SECRET` angezeigt.

## Dienstverwaltung

### Anzeigen des Dienststatus

Überprüfen Sie den Status aller Spwig-Dienste:

```bash
docker compose ps
```

Dies zeigt jeden Dienst, seinen Zustand (laufend, gestoppt, Neustart), und seinen Gesundheitsstatus an.

### Anzeigen der Protokolle

Überprüfen Sie die Protokolle eines bestimmten Dienstes:

```bash
docker logs spwig_shop          # Anwendungsprotokolle
docker logs spwig_celery         # Hintergrundarbeiter-Protokolle
docker logs spwig_nginx          # Webserver-Zugriffsprotokolle
docker logs spwig_db             # Datenbankprotokolle
```

Fügen Sie `--tail 100` hinzu, um die letzten 100 Zeilen anzuzeigen, oder `--follow`, um Protokolle in Echtzeit zu beobachten.

### Neustarten eines Dienstes

Wenn ein bestimmter Dienst neu gestartet werden muss:

```bash
docker compose restart shop      # Anwendung neu starten
docker compose restart celery    # Hintergrundarbeiter neu starten
docker compose restart nginx     # Webserver neu starten
```

Um alle Dienste neu zu starten:

```bash
docker compose restart
```

## Komponenten-Updates

Spwig verfügt über einen Komponenten-Marktplatz, in dem Sie Themes, Zahlungsanbieter, Versandintegrierungen und andere Erweiterungen installieren können. Komponenten werden unabhängig von der Kernplattform aktualisiert.

Navigieren Sie zu **Verwaltung > Komponenten-Updates**, um verfügbare Komponenten-Updates zu überprüfen. Updates werden automatisch heruntergeladen und angewendet, sobald Sie sie genehmigen.

## Tipps

- **Regelmäßige Updates durchführen** – das Verbleiben auf der neuesten Version stellt sicher, dass Sie Sicherheitskorrekturen und Zugang zu neuen Funktionen haben
- **Lesen Sie den Abschnitt Was ist neu, bevor Sie Starten Sie das Update** – dies ist der schnellste Weg, um erforderliche Datenbankmigrationen, Sicherheitskorrekturen oder **Updatehinweise** zu erkennen, auf die Sie nachfolgend reagieren müssen
- **Backup erstellen** – obwohl das Upgrade-Skript ein automatisches Backup erstellt, bietet ein eigenes Backup zusätzliche Sicherheit
- **Doctor nach Problemen ausführen** – wenn sich Ihr Shop unerwartet verhält, ist `./doctor.sh` der schnellste Weg, um Probleme zu identifizieren
- **Planen Sie Updates zu Zeiten mit geringer Auslastung** – der Wartungsmodus unterbricht vorübergehend den Kundenzugriff, daher aktualisieren Sie während ruhiger Zeiten
- **Halten Sie Speicherplatz frei** – Updates benötigen temporären Speicherplatz für neue Images und Backups. Halten Sie mindestens 5 GB frei.