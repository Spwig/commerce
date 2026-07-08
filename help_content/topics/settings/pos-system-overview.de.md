---
title: POS-System-Übersicht
---

Das Spwig POS-System verwandelt Ihr Geschäft in eine vollständige Einzelhandellösung mit modernen Kassenterminals. Stellen Sie beliebig viele Terminals an beliebig vielen Standorten bereit, mit einer Flatrate von €499/Jahr. Jedes Terminal ist eine Progressive Web App (PWA), die offline funktioniert, sich automatisch synchronisiert und nahtlos mit Ihrem Lager, Kundendaten und Zahlungsverarbeitung integriert. Verwalten Sie alles über das Admin-Dashboard: Terminal-Konfiguration, Schichtabrechnung, Rechnungspersonalisierung und Hardwareintegration.

Verwenden Sie das POS-System, wenn Sie physische Einzelhandelsgeschäfte, Pop-up-Läden, Messen oder jede Umgebung haben, in der Kunden physisch einkaufen, anstatt online.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Was ist Spwig POS?

Spwig POS ist ein vollständig integriertes Kassensystem, das für Händler entwickelt wurde, die sowohl online als auch in physischen Standorten verkaufen. Im Gegensatz zu Drittanbieter-Kassensystemen, die komplexe Integrationen erfordern, ist Spwig POS direkt in Ihre Plattform integriert, was eine perfekte Datensynchronisation über alle Verkaufskanäle sicherstellt.

**Hauptmerkmale**:
- **Unbegrenzte Terminals** - Stellen Sie so viele Terminals bereit, wie benötigt, ohne zusätzliche Kosten
- **Offline-first-Architektur** - Verarbeitet Verkäufe weiter, auch wenn die Internetverbindung verloren geht
- **Progressive Web App** - Keine Installation im App-Store; Zugriff über Browser auf jedem Gerät (Tablets, Computer, dedizierte Terminals)
- **Echtzeit-Lager-Synchronisation** - Lagerreservierungen (15-Minuten-TTL) verhindern Überverkauf über verschiedene Kanäle
- **Unterstützung für geteilte Zahlungsmethoden** - Akzeptieren Sie mehrere Zahlungsmethoden pro Transaktion (Bar + Karte + Geschenkkarte)
- **Hardwareintegration** - ESC/POS-Thermoprinter, Barcode-Scanner, Kassenkasse, Kundendisplays
- **Schichtverwaltung** - Bargeldabrechnung mit Öffnungs-/Schlusszahlen und Abweichungsverfolgung
- **Für mehrere Standorte geeignet** - Lagergruppen mit Einstellungenserbe für Franchise- und regionalen Management

## Lizenzierung und Aktivierung

**Flatrate-Preismodell**: €499 pro Jahr decken unbegrenzte Terminals an unbegrenzten Standorten ab. Keine Gebühren pro Terminal, keine Transaktionsgebühren, keine versteckten Kosten.

**Lizenzenformat**: `POS-XXXX-XXXX-XXXX-XXXX` (wird nach dem Kauf bereitgestellt)

**Aktivierung**: Geben Sie Ihren Lizenzschlüssel in **Einstellungen > POS-Lizenzierung** ein. Das System validiert mit dem Lizenzierungsserver von Spwig und aktiviert sofort alle POS-Funktionen. Lizenzen enthalten einen 14-tägigen Verlängerungszeitraum nach Ablauf, um Zahlungsverzögerungen zu ermöglichen.

**Was Sie erhalten**:
- Unbegrenzte Terminalregistrierungen
- Unbegrenzte Mitarbeiterzuordnungen
- Alle POS-Funktionen (Schichten, Bargeldverwaltung, Rechnungspersonalisierung, Kundendisplays)
- Zahlungsanbieterintegrationen (Stripe Terminal und erweiterbares Anbietersystem)
- Hardwareintegrationssupport
- Updates und Fehlerbehebungen während der Lizenzzeit

Keine POS-Funktionen sind ohne gültige Lizenz zugänglich – die Terminalpaarungsschnittstelle, Schichtverwaltung und POS-Adminseiten benötigen alle eine Aktivierung.

## Systemarchitektur

**Frontend** - React 18 Progressive Web App:
- Offline-first mit Service Worker-Caching (funktioniert ohne Internet)
- Vite-Buildsystem für schnelles Laden
- CSS-Module + Design-Token (konsistent mit Ihrem Store-Theme)
- IndexedDB für lokale Datenpersistenz
- 10 unterstützte Sprachen (Englisch, Chinesisch Vereinfacht/Traditionell, Französisch, Deutsch, Spanisch, Portugiesisch, Japanisch, Russisch, Arabisch)

**Backend** - Backend-Integration:
- 13 POS-Modelle (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, usw.)
- 43+ REST API-Endpunkte für Terminalvorgänge
- Lagerreservierungssystem mit TTL-Verwaltung
- Celery-Aufgaben für Hintergrundsynchrnisation
- Verschlüsselte Anmeldeinformationen für Zahlungsanbieter

**Sicherheit**:
- Terminalpaarung über 8-Zeichen-Codes (serverseitig generiert, verfallen nach Verwendung)
- Mitarbeiterzuordnung bestimmt, welche Benutzer welches Terminal nutzen können
- Fernsperr-/Entsperrfunktion für Admin-Notfälle
- Verschlüsselte Zahlungsanbieteranmeldeinformationen
- Session-basierte Authentifizierung mit biometrischer Entsperrung (browserabhängig)

## Einstiegsworkflow

Folgen Sie diesen 5 Schritten, um Ihr erstes POS-Terminal bereitzustellen:

**Schritt 1: Aktivieren Sie die POS-Lizenz**
- Navigieren Sie zu **Einstellungen > POS-Lizenzierung**
- Geben Sie Ihren Lizenzschlüssel ein (`POS-XXXX-XXXX-XXXX-XXXX`)
- Validieren Sie die Lizenz (erfordert Internetverbindung)
- Bestätigen Sie die Aktivierung

**Schritt 2: Erstellen Sie ein Lager**
- Navigieren Sie zu **Katalog > Lager**
- Erstellen Sie ein Lager, das Ihren Einzelhandelsstandort darstellt
- Konfigurieren Sie Adresse und Kontaktdaten
- Dieses Lager wird die physische Lagerverwaltung für POS-Verkäufe verfolgen

**Schritt 3: Registrieren Sie ein Terminal**
- Navigieren Sie zu **POS > Terminals**
- Klicken Sie auf **+ Terminal hinzufügen**
- Geben Sie einen Terminalnamen an (z. B. "Hauptkasse", "Kasse 1")
- Weisen Sie das Lager aus Schritt 2 zu
- Konfigurieren Sie Hardwareeinstellungen (Drucker, Scanner, Kassenkasse)
- Speichern Sie, um einen 8-Zeichen-Paarungscod zu generieren

**Schritt 4: Weisen Sie Mitarbeiter zu**
- In der Terminalkonfiguration, scrollen Sie zu **Zugewiesene Benutzer**
- Wählen Sie Mitarbeiter aus, die berechtigt sind, dieses Terminal zu verwenden
- Nur zugewiesene Benutzer können sich am Terminal anmelden
- Benutzer müssen in ihrer Mitarbeiterrolle die entsprechenden POS-Berechtigungen haben

**Schritt 5: Gerät paaren**
- Auf Ihrem Terminalgerät (Tablet/Computer), navigieren Sie zu `/pos/` URL
- Geben Sie den 8-Zeichen-Paarungscod aus Schritt 3 ein
- Das Terminal lädt die Konfiguration herunter und synchronisiert die anfänglichen Daten
- Melden Sie sich mit den zugewiesenen Mitarbeiteranmeldeinformationen an
- Das Terminal ist bereit für Verkäufe

Nach dem Paaren synchronisieren sich die Terminals automatisch alle 5 Minuten (konfigurierbar). Die Offline-Modus ermöglicht weiter Betrieb, wenn Internet nicht verfügbar ist – Verkäufe synchronisieren sich automatisch, wenn die Verbindung wiederhergestellt wird.

## Kern-POS-Funktionen

**Verkaufsverarbeitung**:
- Produkt-Suche nach Name, SKU oder Barcode
- Geteilte Zahlung (mehrere Zahlungsmethoden pro Bestellung)
- Gespeicherte Warenkörbe (unvollständige Transaktionen speichern)
- Erstattungen und Stornierungen mit Grundverfolgung
- Rabattanwendung (Gutscheine, Geschenkkarten, Promotionen)
- Kundensuche und Loyalitätspunkte-Guthaben

**Bargeldverwaltung**:
- Schichtbeginn mit Startgeldbestand
- Schichtende mit erwartetem vs. tatsächlichem Abrechnung
- Bargeldbewegungen (Zuschüsse, Kassenkasse-Abhebungen mit Gründen)
- Automatische erwartete Bargeldberechnung basierend auf Bargeldverkäufen
- Abweichungsverfolgung und -berichterstattung

**Hardwareintegration**:
- ESC/POS-Thermoprinter (Netzwerk oder Seriell)
- USB-Barcodescanner
- Kassenkassenauslösung über Druckerpuls
- Kundenseitige Displays (Promotion-Karussell während Leerlauf)
- Stripe Terminal-Kartenleser (S700, WisePOS E, P400)

**Offline-Fähigkeiten**:
- Service Worker cache alle Terminal-Assets
- IndexedDB speichert kürzliche Bestellungen (konfigurierbar: 7-30 Tage, 200-1000 Bestellungen)
- Lagerreservierungen mit 15-Minuten-TTL verhindern Überverkauf
- Wartezeiten für Sync, wenn die Verbindung wiederhergestellt wird
- Automatische Wiederherstellungserkennung

## POS-Adminseiten

Zugriff auf diese Adminseiten, um alle Aspekte Ihrer POS-Bereitstellung zu verwalten:

**POS-Dashboard** (`/admin/pos/`)
- Systemübersicht und schnelle Statistiken
- Kürzliche Terminalaktivität
- Übersicht aktiver Schichten
- Lizenzstatus und Ablaufdatum

**Terminalverwaltung** (`/admin/pos_app/posterminal/`)
- Registrieren und konfigurieren Terminals
- Mitarbeiter und Lager zuweisen
- Überwachen Sie den Online/Offline-Status (Herzschlag-Tracking)
- Fernentriegeln von Terminals
- [Mehr erfahren: Terminalverwaltung von POS](managing-pos-terminals)

**Schichtverwaltung** (`/admin/pos_app/posshift/`)
- Alle Schichten ansehen (offen, geschlossen, historisch)
- Überprüfen Sie Berichte zur Bargeldabrechnung
- Verfolgen Sie Bargeldbewegungen und Abweichungen
- Prüfen Sie Schichtaktivitäten
- [Mehr erfahren: POS-Schichten und Bargeldverwaltung](pos-shifts-cash-management)

**Lagergruppen** (`/admin/pos_app/storegroup/`)
- Ordnen Sie Terminals nach Standort/Region
- Konfigurieren Sie Gruppeneinstellungen (Währung, Sprache, Zeitzone)
- Implementieren Sie eine Einstellungserbe-Hierarchie
- [Mehr erfahren: POS-Lagergruppen](pos-store-groups)

**Rechnungsvorlagen** (`/admin/pos_app/receipttemplate/`)
- Personalisieren Sie gedruckte Rechnungen (Papierbreite, Logo, Header/Footer)
- Konfigurieren Sie Compliance-Felder (Steuer-ID, Geschäftsregistrierung)
- Fügen Sie QR-Codes für Promotionen hinzu
- Begrenzen Sie Vorlagen auf bestimmte Stores oder Gruppen
- [Mehr erfahren: Rechnungsvorlagenpersonalisierung](receipt-template-customization)

**Promotionalslides** (`/admin/pos_app/promoslide/`)
- Erstellen Sie Inhalt für das Kundendisplay-Karussell
- Zielgruppen für Slides (spezifische Stores oder Gruppen)
- Planen Sie Saisonale Promotionen
- [Mehr erfahren: Kundendisplay-Promotionalslides](customer-display-promo-slides)

**Zahlungsanbieter** (`/admin/pos_app/posterminalprovider/`)
- Konfigurieren Sie Stripe Terminal-Integration
- Verwalten Sie Zahlungsanbieteranmeldeinformationen
- Überwachen Sie Verbindungsstatus
- [Mehr erfahren: Zahlungsterminal-Anbieter](payment-terminal-providers)

**Kartenleser** (`/admin/pos_app/posterminalreader/`)
- Registrieren Sie physische Kartenleser
- Weisen Sie Leser Terminals zu
- Personalisieren Sie Splash-Screens (Markenidentität für Kundendisplay)
- Überwachen Sie Leserstatus (Online/Offline/Busy)
- [Mehr erfahren: Kartenleser-Verwaltung](card-reader-management)

## Mehrstandortbereitstellung

Für Händler mit mehreren Einzelhandelsgeschäften unterstützt Spwig POS hierarchische Einstellungserbe:

**Einstellungshierarchie** (höchste Priorität zu niedrigster):
1. Terminal-spezifische Einstellungen (überschreiben alles)
2. Store-spezifische Einstellungen (überschreiben Gruppe und Site)
3. Gruppeneinstellungen (überschreiben Site-Standard)
4. Site-Standard (Standard für alles)

Konfigurieren Sie gemeinsame Einstellungen auf Gruppenebene (z. B. regionale Währung, Sprache) und überschreiben Sie sie bei Bedarf für bestimmte Stores oder Terminals. Siehe [POS-Lagergruppen](pos-store-groups) für detaillierte Konfigurationsanleitung.

## Tipps

- **Beginnen Sie mit einem Terminal** - Testen Sie die POS-Setup und Workflow mit einem einzelnen Terminal, bevor Sie flächendeckend bereitstellen
- **Weisen Sie Lager zu, bevor Sie paaren** - Terminals können keine Verkäufe verarbeiten, ohne eine Lagerzuordnung
- **Konfigurieren Sie Rechnungsvorlagen frühzeitig** - Compliance-Felder (Steuer-IDs) variieren je nach Region; richten Sie sie vor der Live-Veröffentlichung ein
- **Testen Sie den Offline-Modus** - Trennen Sie die Internetverbindung und überprüfen Sie, ob Verkäufe weiterlaufen; bestätigen Sie die Synchronisation, wenn die Verbindung wiederhergestellt wird
- **Verwenden Sie Lagergruppen für mehrere Standorte** - Vereinfacht die Konfigurationsverwaltung für Franchise- oder regionale Bereitstellungen
- **Überwachen Sie den Herzschlagstatus** - Terminals senden dem Server alle 5 Minuten einen Ping; offline Terminals erscheinen im Admin-Dashboard
- **Konfigurieren Sie Sync-Grenzwerte für Leistung** - Terminals mit langsamen Verbindungen profitieren von niedrigeren sync_days/sync_limit-Einstellungen
- **Sichern Sie Hardwarekonfigurationen** - Dokumentieren Sie Drucker-IPs, Scanner-Einstellungen, Kassenkassenkonfiguration für Katastrophenwiederherstellung

