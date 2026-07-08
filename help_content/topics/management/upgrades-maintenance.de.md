---
title: Upgrades & Wartung
---

Spwig erhält regelmäßig Updates mit neuen Funktionen, Leistungsverbesserungen und Sicherheitskorrekturen. Dieser Leitfaden behandelt, wie Sie Ihre Installation aktualisieren, das Diagnose-Tool verwenden und Wartungsaufgaben durchführen können.

## Spwig aktualisieren

### Vor der Aktualisierung

1. **Backup erstellen** — gehen Sie zu **Management > System Metrics > Full Backup erstellen** oder führen Sie das Backup-Skript über die Kommandozeile aus. Dies ist Ihr Sicherheitsnetz, falls etwas schief geht.
2. **Aktuelle Version prüfen** — sichtbar in **Management > System Metrics** oder im Fußbereich der Admin-Dashboard.
3. **Release Notes lesen** — verfügbar im Admin-Panel unter **Management > Component Updates**, wenn eine neue Version erkannt wird.

### Upgrade durchführen

SSH in Ihren Server ein und navigieren Sie zu Ihrem Spwig-Installationverzeichnis (typischerweise `/opt/spwig`):

```bash
./upgrade.sh
```

Das Upgrade-Skript:

1. **Vor-Flug-Prüfungen** — überprüft die Festplattenspeicher, den Docker-Status und den Dienststatus
2. **Dry-run-Datenbankmigrationen** — testet, ob Datenbankänderungen sauber angewendet werden können, ohne etwas zu ändern
3. **Wartungsmodus aktivieren** — Ihr Geschäft zeigt während des Upgrades eine Wartungsseite für Besucher an
4. **Backup erstellen** — automatisches Sicherheitsbackup vor Änderungen
5. **Hintergrundarbeiter entladen** — wartet, bis laufende Aufgaben (E-Mail-Versand, Übersetzungen) sanft abgeschlossen werden
6. **Neue Bilder abrufen** — lädt die aktualisierte Anwendung aus dem Spwig-Register herunter
7. **Datenbankmigrationen anwenden** — aktualisiert Ihre Datenbankschema für die neue Version
8. **Dienste neu starten** — startet die Anwendung mit der neuen Version
9. **Gesundheitscheck** — überprüft, ob alle Dienste korrekt laufen
10. **Wartungsmodus beenden** — Ihr Geschäft ist wieder online

Falls der Gesundheitscheck nach dem Upgrade fehlschlägt, rollt das Skript **automatisch zurück** auf die vorherige Version und stellt das Backup wieder her.

### Upgrade-Optionen

```bash
./upgrade.sh              # Standard-Upgrade mit Wartungsmodus
./upgrade.sh --dry-run    # Prüfen, was sich ändern würde, ohne Anwendung
```

## Das Diagnose-Tool

Spwig enthält ein integriertes Diagnose-Tool, das Ihre gesamte Installation auf Probleme überprüft:

```bash
./doctor.sh
```

Das Diagnose-Tool prüft:

| Kategorie | Was es prüft |
|----------|---------------|
| **System** | Festplattenspeicher, RAM-Nutzung, CPU-Auslastung |
| **Docker** | Gesundheit des Docker-Motors, Containerzustände, Bildversionen |
| **Datenbank** | PostgreSQL-Verbindung, Migrationsstatus, Gesundheit des Verbindungs-Pools |
| **Cache** | Redis-Verbindung, Speichernutzung |
| **Objekt-Speicher** | MinIO-Verbindung, Zugänglichkeit von Buckets |
| **Netzwerk** | DNS-Auflösung, Port-Zugänglichkeit, Gültigkeit des SSL-Zertifikats |
| **Anwendung** | Gesundheitsendpunkte der Dienste, Status der Hintergrundarbeiter |

Jede Prüfung zeigt ein Bestanden/ Nicht-bestanden-Ergebnis mit Details, wenn etwas falsch ist.

### Automatische Reparaturmodus

Für häufige Probleme kann das Diagnose-Tool automatische Reparaturen versuchen:

```bash
./doctor.sh --fix
```

Automatische Reparatur kann folgende Probleme beheben:

- Gestoppte Container (startet sie erneut)
- Veraltete Datenbankverbindungen (recycelt den Verbindungs-Pool)
- Abgelaufene SSL-Zertifikate (löst die Erneuerung aus)
- Vollständige Festplatte durch alte Docker-Images (entfernt nicht genutzte Images)

Das Diagnose-Tool erklärt immer, was es beheben wird, bevor es handelt.

## Wartungsmodus

Der Wartungsmodus zeigt Besuchern eine Seite an, die besagt, dass das Geschäft vorübergehend nicht verfügbar ist, während Sie Änderungen vornehmen. Ihr Admin-Panel bleibt weiterhin zugänglich.

### Wartungsmodus aktivieren

Vom Admin-Panel: **Store Settings > Maintenance > Enable Maintenance Mode**

Oder über die Kommandozeile:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Wartungsmodus deaktivieren

Vom Admin-Panel: Schalten Sie den Wartungsmodus-Schalter aus.

Oder über die Kommandozeile:

```bash
./go-live.sh
```

### Zugang umgehen während Wartung

Wenn der Wartungsmodus aktiv ist, können Sie das Geschäft normal betreten, indem Sie einen geheimen Parameter zur URL hinzufügen. Der Umgehungsgeheimnis wird in Ihrer `.env`-Konfigurationsdatei unter `MAINTENANCE_SECRET` angezeigt.

## Dienste verwalten

### Dienststatus ansehen

# Dienststatus prüfen

Überprüfen Sie den Status aller Spwig-Dienste:

```bash
docker compose ps
```

Dies zeigt jeden Dienst, seinen Zustand (laufend, gestoppt, Neustart), und seinen Gesundheitsstatus an.

### Protokolle ansehen

Überprüfen Sie die Protokolle eines bestimmten Dienstes:

```bash
docker logs spwig_shop          # Anwendungssprotokolle
docker logs spwig_celery         # Hintergrundarbeitsprotokolle
docker logs spwig_nginx          # Webserver-Zugriffsprotokolle
docker logs spwig_db             # Datenbankprotokolle
```

Fügen Sie `--tail 100` hinzu, um die letzten 100 Zeilen anzuzeigen, oder `--follow`, um Protokolle in Echtzeit zu beobachten.

### Dienst neu starten

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

## Komponentenupdates

Spwig verfügt über einen Komponentenmarkt, in dem Sie Themes, Zahlungsanbieter, Versandintegrationen und andere Erweiterungen installieren können. Komponenten werden unabhängig von der Kernplattform aktualisiert.

Navigieren Sie zu **Management > Komponentenupdates**, um verfügbare Komponentenupdates zu prüfen. Updates werden automatisch heruntergeladen und angewendet, sobald Sie sie genehmigen.

## Tipps

- **Regelmäßig aktualisieren** – das Halten auf der neuesten Version stellt sicher, dass Sie Sicherheitskorrekturen und Zugang zu neuen Funktionen haben
- **Immer zuerst sichern** – obwohl das Upgrade-Skript eine automatische Sicherung erstellt, bietet Ihre eigene Sicherung zusätzliche Sicherheit
- **Nach Problemen Doctor ausführen** – wenn sich Ihr Geschäft unerwartet verhält, ist `./doctor.sh` der schnellste Weg, um Probleme zu identifizieren
- **Upgrades zu Zeiten mit geringem Verkehr planen** – der Wartungsmodus unterbricht kurzzeitig den Kundenzugriff, daher aktualisieren Sie während ruhiger Zeiten
- **Platz auf der Festplatte freihalten** – Upgrades benötigen temporären Platz für neue Images und Sicherungen. Halten Sie mindestens 5 GB freiem Platz bereit.