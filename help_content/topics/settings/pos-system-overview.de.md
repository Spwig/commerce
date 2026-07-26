---
title: Übersicht des POS-Systems
---

Das Spwig POS-System verwandelt Ihr Geschäft in eine vollständige Einzelhandelslösung mit modernen Kassenterminals. Es ist in jeder Edition enthalten – Community, Pro und Enterprise – mit unbegrenzten Terminals über unbegrenzte Standorte ohne zusätzliche Kosten. Jedes Terminal ist eine Progressive Web App (PWA), die offline funktioniert, sich automatisch synchronisiert und nahtlos mit Ihrem Lager, Kundendaten und Zahlungsverarbeitung integriert. Verwalten Sie alles über das Admin-Dashboard – Terminal-Konfiguration, Schichtabrechnung, Rechnungspersonalisierung und Hardwareintegration.

Verwenden Sie das POS-System, wenn Sie physische Einzelhandelsstandorte, Pop-up-Läden, Messen oder jede Umgebung haben, in der Kunden physisch statt online einkaufen.

![POS-Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Was ist Spwig POS?

Spwig POS ist ein vollständig integriertes Kassensystem, das für Händler entwickelt wurde, die sowohl online als auch in physischen Standorten verkaufen. Im Gegensatz zu Drittanbieter-Kassensystemen, die komplexe Integrationen erfordern, ist Spwig POS direkt in Ihre Plattform integriert, was eine perfekte Datensynchronisation über alle Verkaufskanäle gewährleistet.

**Hauptmerkmale**:
- **Unbegrenzte Terminals** - Stellen Sie so viele Terminals bereit, wie benötigt, ohne zusätzliche Kosten
- **Offline-first-Architektur** - Verarbeitet Verkäufe weiter, auch wenn die Internetverbindung verloren geht
- **Progressive Web App** - Keine Installation im App-Store erforderlich; Zugriff über Browser auf jedem Gerät (Tablets, Computer, dedizierte Terminals)
- **Echtzeit-Lager-Synchronisation** - Lagerreservierungen (15-minütiger TTL) verhindern Überverkauf über verschiedene Kanäle
- **Unterstützung für mehrere Zahlungsmethoden** - Akzeptieren Sie mehrere Zahlungsmethoden pro Transaktion (Bar + Karte + Geschenkkarte)
- **Hardwareintegration** - ESC/POS-Thermoprinter, Barcode-Scanner, Kassenkasse, Kundendisplays
- **Schichtverwaltung** - Bargeldabrechnung mit Öffnungs-/Schlusszahlen und Abweichungserfassung
- **Für mehrere Standorte geeignet** - Lagergruppen mit Einstellungenserbe für Franchise- und regionalen Management

## Editionen

POS ist in jeder Spwig-Edition enthalten – Community, Pro und Enterprise – ab Spwig 1.5.8. Es gibt keine separate POS-Lizenz, keine Aktivierungsschritt und keine Gebühren pro Terminal.

**In jeder Edition enthalten**:
- Unbegrenzte Terminalregistrierungen
- Unbegrenzte Mitarbeiterzuordnungen
- Alle POS-Funktionen (Schichten, Bargeldverwaltung, Rechnungspersonalisierung, Kundendisplays)
- Zahlungsanbieterintegrationen (Stripe Terminal und andere unterstützte Anbieter)
- Hardwareintegrationssupport

Händler, die Spwig-gehostete Stores betreiben oder für eine Pro/Enterprise-Lizenz zahlen, erhalten höhere Grenzwerte für die optionalen Spwig-gehosteten Dienste (GeoIP, Geocoder, Push-Benachrichtigungen) und Prioritätsupport, aber die POS-Funktionalität selbst ist in allen Editionen identisch.

## Systemarchitektur

**Frontend** - React 18 Progressive Web App:
- Offline-first mit Service Worker-Caching (funktioniert ohne Internet)
- Vite-Build-System für schnelles Laden
- CSS-Module + Design-Tokens (konsistent mit Ihrem Store-Theme)
- IndexedDB für lokale Datenpersistenz
- 10 unterstützte Sprachen (Englisch, Chinesisch Vereinfacht/Traditionell, Französisch, Deutsch, Spanisch, Portugiesisch, Japanisch, Russisch, Arabisch)

**Backend** - Backend-Integration:
- 13 POS-Modelle (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, usw.)
- 43+ REST-API-Endpunkte für Terminal-Operationen
- Lagerreservierungssystem mit TTL-Verwaltung
- Celery-Aufgaben für Hintergrund-Synchronisation
- Verschlüsselte Anmeldeinformationen für Zahlungsanbieter

**Sicherheit**:
- Terminal-Paaren über 8-Zeichen-Codes (serverseitig generiert, verfallen nach Verwendung)
- Mitarbeiterzuordnung bestimmt, welche Benutzer welches Terminal nutzen können
- Fernsperr-/Entsperrfunktion für Admin-Notfälle
- Verschlüsselte Zahlungsanbieter-Anmeldeinformationen
- Session-basierte Authentifizierung mit Unterstützung für biometrische Entsperrung (browserabhängig)

## Einstiegsworkflow

Folgen Sie diesen 4 Schritten, um Ihr erstes POS-Terminal bereitzustellen.

Für eine vollständige Schritt-für-Schritt-Checkliste, einschließlich der Einrichtung von Personal, Zahlungsdienstleistern und dem Durchführung des ersten Verkaufs, siehe [Getting Started with POS](getting-started-with-pos).

**Schritt 1: Lager erstellen**
- Navigieren Sie zu **Katalog > Lager**
- Erstellen Sie ein Lager, das Ihre Einzelhandelsstelle darstellt
- Konfigurieren Sie die Adresse und die Kontaktinformationen
- Dieses Lager verfolgt die physische Lagerbestände für POS-Verkäufe

**Schritt 2: Terminal registrieren**
- Navigieren Sie zu **POS > Terminals**
- Klicken Sie auf **+ Terminal hinzufügen**
- Geben Sie einen Terminalnamen an (z. B. "Hauptkasse", "Kasse 1")
- Weisen Sie ein Lager aus Schritt 2 zu
- Konfigurieren Sie die Hardwareeinstellungen (Drucker, Scanner, Kassenschublade)
- Speichern Sie, um einen 8-Zeichen-Paarungscod zu generieren

**Schritt 3: Personal zuweisen**
- In der Terminalkonfiguration, scrollen Sie zu **Zugewiesene Benutzer**
- Wählen Sie die Mitarbeiter aus, die berechtigt sind, diesen Terminal zu verwenden
- Nur zugewiesene Benutzer können sich am Terminal anmelden
- Benutzer müssen über die entsprechenden POS-Berechtigungen in ihrer Mitarbeiterrolle verfügen

**Schritt 4: Gerät pairen**
- Auf Ihrem Terminalgerät (Tablet/Computer), navigieren Sie zu der URL `/pos/`
- Geben Sie den 8-Zeichen-Paarungscod aus Schritt 3 ein
- Das Terminal lädt die Konfiguration und synchronisiert die anfänglichen Daten
- Melden Sie sich mit den zugewiesenen Mitarbeitercredentials an
- Das Terminal ist für Verkäufe bereit

Nach dem Paaren synchronisieren sich Terminals automatisch alle 5 Minuten (konfigurierbar). Der Offline-Modus ermöglicht weiterhin den Betrieb, wenn das Internet nicht verfügbar ist – Verkäufe synchronisieren sich automatisch, wenn die Verbindung wiederhergestellt wird.

## Kernfunktionen von POS

**Verkaufsabwicklung**:
- Produkt-Suche nach Name, SKU oder Barcode
- Aufteilung der Zahlung (mehrere Zahlungsmethoden pro Bestellung)
- Gespeicherte Warenkörbe (unvollständige Transaktionen speichern)
- Erstattungen und Stornierungen mit Grundverfolgung
- Rabattanwendung (Gutscheine, Geschenkkarten, Promotionen)
- Kunden-Suche und Loyalitätspunkte-Guthaben

**Kassenverwaltung**:
- Schichtbeginn mit Startgeldbestand
- Schichtende mit erwartetem vs. tatsächlichem Ausgleich
- Geldbewegungen (Geldscheinauffüllung, Auszahlung von Kleingeld mit Gründen)
- Automatische erwartete Geldberechnung basierend auf Bargeldverkäufen
- Nachverfolgung und Berichte zu Abweichungen

**Hardwareintegration**:
- ESC/POS-Thermoprinter (Netzwerk oder Seriell)
- USB-Barcodescanner
- Kassenschublade über Druckimpuls auslösen
- Kundenseitige Displays (werbende Karussell während Leerlauf)
- Stripe Terminal-Kartenleser (S700, WisePOS E, P400)

**Offline-Funktionen**:
- Service Worker speichert alle Terminalressourcen
- IndexedDB speichert kürzliche Bestellungen (konfigurierbar: 7–30 Tage, 200–1000 Bestellungen)
- Lagerreservierungen mit 15-Minuten-TTL verhindern Überverkauf
- Wartezeiten für Bestellungen, bis die Verbindung wiederhergestellt ist
- Automatische Neuanmeldungserkennung

## POS-Verwaltungsseiten

Greifen Sie über diese Verwaltungsseiten zu, um alle Aspekte Ihrer POS-Implementierung zu verwalten:

**POS-Dashboard** (`/admin/pos/`)
- Systemübersicht und schnelle Statistiken
- Kürzliche Terminalaktivitäten
- Zusammenfassung aktiver Schichten
- Kacheln für Hosted-Service-Nutzung (GeoIP, Geocoder, Push – siehe [Spwig Hosted Services](hosted-services))

**Terminalverwaltung** (`/admin/pos_app/posterminal/`)
- Registrieren und konfigurieren Sie Terminals
- Weisen Sie Personal und Lager zu
- Überwachen Sie den Online-/Offline-Status (Herzschlagverfolgung)
- Entfernen Sie Terminals ferngesteuert
- [Mehr erfahren: Terminalverwaltung für POS](managing-pos-terminals)

**Schichtverwaltung** (`/admin/pos_app/posshift/`)
- Zeigen Sie alle Schichten an (offen, geschlossen, historisch)
- Überprüfen Sie Berichte zur Geldabrechnung
- Verfolgen Sie Geldbewegungen und Abweichungen
- Prüfen Sie Schichtaktivitäten
- [Mehr erfahren: POS-Schichten und Geldverwaltung](pos-shifts-cash-management)

**Geschäftsgruppen** (`/admin/pos_app/storegroup/`)
- Ordnen Sie Terminals nach Standort/Region zu
- Konfigurieren Sie Gruppeneinstellungen (Währung, Sprache, Zeitzone)
- Implementieren Sie eine Einstellungshierarchie für Vererbung
- [Mehr erfahren: POS-Geschäftsgruppen](pos-store-groups)

**Belegvorlagen** (`/admin/pos_app/receipttemplate/`)
- Anpassen von gedruckten Belegen (Papierbreite, Logo, Kopf/Fußzeile)
- Konfigurieren von gesetzlich vorgeschriebenen Feldern (Steuer-ID, Gewerbeschein)
- QR-Codes für Werbungen hinzufügen
- Vorlagen auf bestimmte Geschäfte oder Gruppen beschränken
- [Mehr erfahren: Belegvorlagen anpassen](receipt-template-customization)

**Werbeslides** (`/admin/pos_app/promoslide/`)
- Erstellen von Inhalten für Kunden-Display-Karusselle
- Slides auf bestimmte Geschäfte oder Gruppen abzielen
- Saisonale Werbungen planen
- [Mehr erfahren: Werbeslides für Kunden-Displays](customer-display-promo-slides)

**Zahlungsdienstleister** (`/admin/pos_app/posterminalprovider/`)
- Konfigurieren der Stripe Terminal-Integration
- Verwalten von Zugangsdaten für Zahlungsdienstleister
- Verbindungszustand überwachen
- [Mehr erfahren: Zahlungsterminal-Dienstleister](payment-terminal-providers)

**Kartenleser** (`/admin/pos_app/posterminalreader/`)
- Physische Kartenleser registrieren
- Leser an Terminals zuweisen
- Splash-Screens anpassen (Markenidentität für Kundenanzeige)
- Leserstatus überwachen (online/abgeschaltet/beschäftigt)
- [Mehr erfahren: Kartenleser-Verwaltung](card-reader-management)

## Mehrstandort-Deployment

Für Händler mit mehreren Einzelhandelsstandorten unterstützt Spwig POS eine hierarchische Einstellungserbung:

**Einstellungshierarchie** (höchste Priorität zu niedrigster):
1. Terminal-spezifische Einstellungen (überschreiben alles)
2. Geschäftsspezifische Einstellungen (überschreiben Gruppe und Standort)
3. Gruppeneinstellungen (überschreiben Standortstandardwerte)
4. Standortstandardwerte (Standardwerte für alles)

Konfigurieren Sie gemeinsame Einstellungen auf Gruppenebene (z. B. regionale Währung, Sprache) und überschreiben Sie sie bei Bedarf für bestimmte Geschäfte oder Terminals. Siehe [POS-Geschäftsgruppen](pos-store-groups) für detaillierte Konfigurationsanleitungen.

## Tipps

- **Beginnen Sie mit einem Terminal** - Testen Sie die POS-Setup und -Workflow mit einem einzelnen Terminal, bevor Sie es flächendeckend einsetzen
- **Zuerst Lager zuweisen** - Terminals können keine Verkäufe verarbeiten, ohne eine Lagerzuordnung
- **Belegvorlagen früh konfigurieren** - Gesetzlich vorgeschriebene Felder (Steuer-IDs) variieren je nach Region; richten Sie sie vor der Live-Veröffentlichung ein
- **Offline-Modus testen** - Trennen Sie die Internetverbindung und überprüfen Sie, ob Verkäufe weiterlaufen; bestätigen Sie die Synchronisation, wenn die Verbindung wiederhergestellt wird
- **Für mehrere Standorte Store-Gruppen verwenden** - Vereinfacht die Konfigurationsverwaltung für Franchise- oder regionale Einrichtungen
- **Herzschlagstatus überwachen** - Terminals senden dem Server alle 5 Minuten einen Ping; offline Terminals erscheinen im Admin-Dashboard
- **Für Leistung Sync-Limits konfigurieren** - Terminals mit langsamen Verbindungen profitieren von niedrigeren sync_days/sync_limit-Einstellungen
- **Hardware-Konfiguration sichern** - Dokumentieren Sie Drucker-IPs, Scanner-Einstellungen, Kassenschublade-Konfiguration für Notfallwiederherstellung