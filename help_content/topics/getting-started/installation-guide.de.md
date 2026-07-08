---
title: Installationsanleitung
---

Diese Anleitung führt Sie durch den Prozess, Spwig auf Ihrem eigenen Server zu installieren. Der gesamte Prozess ist automatisiert – ein einzelner Befehl kümmert sich um die Docker-Setup, die Datenbankerstellung, die Dienstkonfiguration und SSL-Zertifikate.

## Vor der Installation

Sie benötigen:

- Einen Server, auf dem **Ubuntu 22.04 oder 24.04** läuft (Debian 12 wird ebenfalls unterstützt)
- **Root- oder sudo-Zugriff** auf den Server
- Mindestens **4 GB RAM** und **20 GB Speicherplatz** (8 GB RAM wird empfohlen)
- Ein **Lizenztoken** aus Ihrem Spwig-Kauf (prüfen Sie Ihre E-Mail-Rechnung)
- Optional, ein **Domain-Name**, der auf die IP-Adresse Ihres Servers verweist

> **Tipp:** Sie können ohne Domain installieren und eine später hinzufügen, indem Sie das Domain-Konfigurationswerkzeug verwenden. In der Zwischenzeit ist Ihr Geschäft über die IP-Adresse des Servers zugänglich.

## Installer ausführen

Verbinden Sie sich per SSH mit Ihrem Server und führen Sie den Installationsbefehl aus der Bestätigungs-E-Mail Ihres Kaufs aus. Er sieht so aus:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Ersetzen Sie `YOUR_LICENSE_TOKEN` durch das Token aus Ihrer E-Mail.

Der Installer läuft automatisch durch acht Phasen:

1. **Vor-Flug-Überprüfung** – überprüft, ob Ihr Server die Anforderungen erfüllt (Betriebssystem, Speicher, RAM, Ports)
2. **Token-Überprüfung** – bestätigt Ihre Lizenz und extrahiert Ihre Geschäftskonfiguration
3. **Modus-Erkennung** – ermittelt den besten Installationsmodus für Ihren Server (siehe unten)
4. **Konfiguration** – generiert sichere Passwörter, Datenbank-Anmeldeinformationen und Dienstkonfiguration
5. **Bild-Download** – zieht die Spwig-Anwendungsbilder aus dem Registry
6. **Dienststart** – startet nacheinander Datenbank, Cache, Anwendung und Hintergrundarbeiter
7. **SSL-Setup** – erhält ein SSL-Zertifikat, wenn Sie eine Domain konfiguriert haben
8. **Abschluss** – erstellt Ihr Admin-Konto und generiert Hilfs-Skripte

Der Prozess dauert 5–15 Minuten, abhängig von der Internetgeschwindigkeit Ihres Servers.

## Installationsmodi

Der Installer erkennt automatisch Ihre Serverumgebung und wählt den besten Modus. Sie können auch einen manuell mit dem `--mode`-Flag angeben.

### Standalone-Modus

**Beste für:** Dedicated-Server und VPS-Instanzen, bei denen Spwig die einzige Webanwendung ist.

- Nutzt Ports 80 und 443 direkt
- Verwaltet SSL-Zertifikate automatisch über Let's Encrypt
- Dies ist der häufigste und empfohlene Modus

### Sidecar-Modus

**Beste für:** Server, die bereits eine andere Webanwendung (WordPress, ein Firmenwebsite usw.) auf Ports 80/443 laufen lassen.

- Spwig läuft auf einem alternativen Port (automatisch erkannt, typischerweise 8080 oder 8443)
- Der Installer generiert einen nginx-Proxy-Konfigurationsblock, den Sie Ihrem bestehenden Webserver hinzufügen können
- Ihr bestehender Webserver verwaltet SSL und leitet den Datenverkehr an Spwig weiter

### Lokaler Modus

**Beste für:** Entwicklung und Tests auf Ihrem eigenen Computer.

- Nur über `localhost` oder `127.0.0.1` zugänglich
- Nutzt ein selbstsigniertes SSL-Zertifikat (Ihr Browser zeigt eine Sicherheitswarnung – das ist normal)
- Debug-Funktionen sind aktiviert
- Keine Lizenzprüfung erforderlich

## Was während der Installation passiert

### Docker

Wenn Docker noch nicht installiert ist, bietet der Installer an, es für Sie zu installieren. Spwig läuft vollständig in Docker-Containern – nichts wird direkt auf Ihrem Server-Betriebssystem außerhalb von Docker installiert.

### Erstellte Dienste

Der Installer erstellt diese Dienste:

| Dienst | Zweck |
|---------|---------|
| **Datenbank** (PostgreSQL 16) | Speichert alle Daten Ihres Geschäfts — Produkte, Bestellungen, Kunden, Einstellungen |
| **Cache** (Redis) | Beschleunigt die Seitenladung und verwaltet Warteschlangen für Hintergrundaufgaben |
| **Verbindungsverwalter** (PgBouncer) | Verwaltet Datenbankverbindungen effizient |
| **Objekt-Speicher** (MinIO) | Speichert hochgeladene Bilder, Dateien und Medien |
| **Anwendung** (Spwig) | Das Geschäft selbst — Admin-Panel und Frontend |
| **Webserver** (Nginx) | Liefert Ihr Geschäft an Besucher mit Komprimierung und Caching |
| **Hintergrundarbeitsprozess** (Celery) | Verarbeitet E-Mails, Übersetzungen, Analysen und andere Hintergrundaufgaben |
| **Aufgabenplaner** (Celery Beat) | Führt geplante Aufgaben wie automatische Backups und E-Mail-Kampagnen aus |
| **Übersetzer** | KI-gestützter Übersetzungsdienst für mehrsprachige Geschäfte |
| **Updater** | Verwaltet Komponenten-Updates aus dem Spwig-Marktplatz |

### Admin-Konto

Am Ende der Installation werden Sie aufgefordert, ein Admin-Konto zu erstellen. Dies ist das Konto, das Sie verwenden werden, um sich in das Admin-Panel Ihres Geschäfts einzuloggen.

### Wartungsmodus

Ihr Geschäft startet im **Wartungsmodus** — Besucher sehen eine „Coming Soon“-Seite. Dies gibt Ihnen Zeit, Ihr Geschäft zu konfigurieren (Produkte hinzufügen, Zahlungsmethoden einrichten, Ihr Theme anpassen), bevor Sie online gehen.

Wenn Sie bereit sind, führen Sie das Hilfsskript aus, das der Installer erstellt hat:

```bash
./go-live.sh
```

Oder deaktivieren Sie den Wartungsmodus unter **Admin > Store Einstellungen > Wartung**.

## Nach der Installation

Sobald der Installer fertig ist, sehen Sie eine Zusammenfassung mit:

- Ihrer Geschäfts-URL
- Ihrer Admin-Panel-URL (typischerweise `https://yourdomain.com/en/admin/`)
- Der Lage Ihrer Konfigurationsdateien
- Verfügbare Hilfsskripte

### Hilfsskripte

Der Installer erstellt diese Skripte in Ihrem Installationsverzeichnis:

- **`./go-live.sh`** — nimmt Ihr Geschäft aus dem Wartungsmodus heraus
- **`./configure-domain.sh`** — fügt Ihr Domain hinzu oder ändert es und erhält ein SSL-Zertifikat

### Nächste Schritte

1. Melden Sie sich in Ihrem Admin-Panel an
2. Führen Sie den **Einrichtungsführer** ab — er führt Sie durch den Geschäftsname, Währung, Zeitzone und grundlegende Einstellungen
3. Fügen Sie Ihre Produkte hinzu
4. Konfigurieren Sie eine Zahlungsmethode
5. Wählen Sie und passen Sie ein Theme an
6. Führen Sie `./go-live.sh` aus, wenn Sie bereit sind

## Installation auf Cloud-Marktplätzen

Spwig ist als One-Click-Anwendung auf mehreren Cloud-Anbietern verfügbar:

- **DigitalOcean** — deployen Sie von der DigitalOcean-Marktplatz
- **Akamai (Linode)** — deployen Sie von der Linode-Marktplatz
- **Vultr** — deployen Sie von der Vultr-Marktplatz

Diese Marktplatz-Images sind mit dem Installer vorkonfiguriert. Nachdem Sie den Server erstellt haben, melden Sie sich per SSH an und folgen Sie den auf dem Bildschirm angezeigten Anweisungen, um die Einrichtung mit Ihrem Lizenztoken abzuschließen.

## Hilfe erhalten

Wenn die Installation fehlschlägt oder Sie einen Fehler erhalten:

1. Führen Sie das **Diagnose-Tool** aus: `./doctor.sh` (während der Installation erstellt)
2. Das Diagnose-Tool überprüft alle Dienste, Verbindungen, SSL und häufige Probleme
3. Verwenden Sie `./doctor.sh --fix`, um automatische Reparaturen zu versuchen
4. Kontaktieren Sie den Spwig-Support mit der Ausgabe des Diagnose-Tools, wenn das Problem weiterhin besteht