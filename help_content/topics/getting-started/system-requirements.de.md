---
title: Systemanforderungen
---

Spwig läuft auf den meisten modernen Linux-Servern. Diese Seite behandelt die Mindest- und empfohlenen Spezifikationen, was bei kleineren Servern passiert und welche Cloud-Anbieter gut funktionieren.

## Mindestanforderungen

| Ressource | Mindest | Empfohlen |
|----------|---------|-------------|
| **Betriebssystem** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS oder Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB oder mehr |
| **Speicherplatz** | 20 GB | 40 GB oder mehr |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Architektur** | x86_64 (AMD64) | x86_64 |
| **Netzwerk** | Öffentliche IP-Adresse (für den standalone-Modus) | Statische öffentliche IP |
| **Ports** | 80 und 443 (standalone) oder beliebigen alternativen Port (sidecar) | 80 und 443 |

> **Hinweis:** ARM-basierte Server (z. B. AWS Graviton, Oracle Ampere) werden derzeit nicht unterstützt.

## Ressourcenstufen

Der Installer erkennt automatisch die verfügbare RAM des Servers und wählt die entsprechende Ressourcenstufe.

### Standardstufe (6 GB+ RAM)

Alle Dienste laufen mit voller Funktionalität:

- KI-gestützter **Übersetzungsdienst** aktiv – übersetzen Sie Produktbeschreibungen, Seiteninhalte und SEO-Texte in mehrere Sprachen direkt aus Ihrem Admin-Panel
- Vollständige Speicherzuordnung für Anwendung, Datenbank und Hintergrundarbeiter
- Hintergrundarbeiter-Konkurrenz optimiert für Ihre CPU-Anzahl

### Kleine Stufe (4–6 GB RAM)

Der Installer passt sich an, um Speicher zu sparen:

- KI-Übersetzungsdienst ist **deaktiviert**, um ca. 2 GB RAM zu sparen. Sie können weiterhin Übersetzungen manuell verwalten oder externe Übersetzungstools verwenden – nur der integrierte KI-Übersetzer wird beeinflusst.
- Speicherbegrenzungen für Anwendung und Worker werden reduziert
- Alle anderen Funktionen funktionieren identisch wie bei der Standardstufe

> **Tipp:** Wenn Sie mit einem kleinen Server beginnen und später auf 6 GB+ RAM upgraden, führen Sie den Installer erneut aus, um den Übersetzungsdienst zu aktivieren.

## Empfohlene Cloud-Anbieter

Spwig funktioniert auf jedem Linux-Server, der die Anforderungen erfüllt. Diese Anbieter wurden getestet und bieten gute Wert:

| Anbieter | Empfohlener Plan | RAM | Speicher | Approximative Kosten |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Basic Droplet | 4 GB | 80 GB | $24 pro Monat |
| **Linode (Akamai)** | Shared 4 GB | 4 GB | 80 GB | $24 pro Monat |
| **Vultr** | Cloud Compute | 4 GB | 100 GB | $24 pro Monat |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8 pro Monat |
| **OVH** | Starter VPS | 4 GB | 80 GB | €7 pro Monat |

Für Stores mit erwarteter hohen Traffic oder großen Produktkatalogen (10.000+ Produkte), beginnen Sie mit 8 GB RAM und 2+ vCPUs.

## Speicherplatzverwendung

Eine frische Spwig-Installation verwendet ungefähr 8 GB Speicherplatz:

| Komponente | Größe |
|-----------|------|
| Docker-Images | ~4 GB |
| Datenbank (leere Store) | ~200 MB |
| KI-Übersetzungmodelle (wenn aktiviert) | ~2 GB |
| Anwendung und Konfigurationsdateien | ~500 MB |
| Betriebssystem und Docker-Engine | ~3 GB |

Planen Sie zusätzlichen Speicherplatz für:

- **Produktbilder und Medien** – hängt von der Größe Ihres Katalogs ab. Budgetieren Sie 1–5 GB für einen typischen Store mit hunderten von Produkten.
- **Datenbankwachstum** – wächst mit Bestellungen, Kunden und Analyse-Daten. Ein Store, der 100 Bestellungen pro Tag verarbeitet, wächst typischerweise um ~1 GB pro Jahr.
- **Backups** – wenn Sie Backups lokal speichern, ist jeder vollständige Backup ungefähr so groß wie Ihre Datenbank plus Medien. Mit einer 30-Tage-Retentionspolitik, planen Sie 2–3× die aktuelle Datenmenge.

## Domain und DNS

Ein Domain-Name ist während der Installation optional, aber für die Produktion erforderlich. Sie benötigen:

- Eine Domain oder einen Subdomain (z. B. `shop.example.com`)
- Eine **A-Record**, der auf die öffentliche IP-Adresse Ihres Servers zeigt
- DNS-Propagation abgeschlossen (typischerweise 5–60 Minuten nach Hinzufügen des Eintrags)

Der Installer erhält automatisch ein kostenloses SSL-Zertifikat von Let's Encrypt, wenn eine gültige Domain erkannt wird. Sie können auch nach der Installation einen Domain mit dem Skript `./configure-domain.sh` hinzufügen.

## Firewall

Wenn Ihr Server eine Firewall hat (die meisten Cloud-Anbieter aktivieren eine standardmäßig), stellen Sie sicher, dass diese Ports geöffnet sind:

| Port | Protokoll | Zweck |
|------|----------|---------|
| **22** | TCP | SSH-Zugriff (für die Serververwaltung) |
| **80** | TCP | HTTP (erforderlich für die Zertifikatsvalidierung von Let's Encrypt) |
| **443** | TCP | HTTPS (sicherer Datenverkehr Ihres Geschäfts) |

In der Sidecar-Modus verwenden Sie stattdessen den alternativen Port, den der Installer zuweist, anstelle von 80/443.

## Softwarevoraussetzungen

Der Installer installiert alle Software automatisch. Als Referenz sind dies die Komponenten, die er installiert oder überprüft:

- **Docker Engine** — Container-Engine (wird automatisch installiert, wenn sie nicht vorhanden ist)
- **Docker Compose** — Dienstorchestrierung (enthalten in Docker Engine)
- **curl** — wird vom Installer selbst verwendet (ist auf fast allen Linux-Systemen vorhanden)

Es ist keine andere Software vorab zu installieren. Spwig erfordert nicht, dass Sie Python, Node.js, PostgreSQL, Redis oder Nginx manuell installieren — alles läuft in Docker-Containern.
