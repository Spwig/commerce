---
title: POS-Terminals verwalten
---

Die Verwaltung von POS-Terminals bildet die Grundlage Ihrer Einzelhandelsoperationen. Jeder Terminal stellt ein physisches Gerät (Tablet, Computer oder dediziertes POS-Hardware) dar, mit dem das Personal Verkäufe abwickelt. Konfigurieren Sie Terminals mit Lagerzuordnungen, Personalberechtigungen, Hardware-Integrationen und Einstellungen für die Offline-Synchronisation. Überwachen Sie den Terminalstatus mit der Echtzeit-Heartbeat-Verfolgung und entsperren Sie Terminals ferngesteuert, wenn Probleme auftreten. Eine ordnungsgemäße Terminalverwaltung gewährleistet reibungslose Verkaufsprozesse im Geschäft und verhindert Konfigurationskonflikte zwischen Standorten.

Navigieren Sie zu **POS > Terminals**, um neue Terminals zu registrieren, den Online-/Offline-Status anzuzeigen und alle Terminal-Einstellungen zu verwalten.

![Terminal List](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Terminal List View

Die Terminal-Liste zeigt alle registrierten Terminals mit wichtigen Statusinformationen an:

**Terminal Name** - Beschreibender Bezeichner für das Terminal (z. B. "Checkout 1", "Main Register", "Mobile Terminal")

**UUID** - Eindeutige Kennung, die automatisch beim Erstellen generiert wird (wird intern zur Geräteidentifizierung verwendet)

**Warehouse** - Physischer Standort, der diesem Terminal zugewiesen ist (bestimmt die Lagerverfügbarkeit und die Zuordnung von Bestellungen)

**Online Status** - Live-Indikator, der anzeigt, ob das Terminal aktuell verbunden ist:
- **Green dot** - Online (Heartbeat innerhalb der letzten 5 Minuten empfangen)
- **Red dot** - Offline (kein Heartbeat seit mehr als 5 Minuten)
- **Gray dot** - Nie gepaart (Terminal erstellt, aber Gerät nie verbunden)

**Last Heartbeat** - Zeitstempel des letzten Pings vom Terminal (wird alle 5 Minuten aktualisiert, wenn online)

**Pairing Code** - 8-stelliger alphanumerischer Code, der für die erste Gerätepaarung verwendet wird (wird nach der ersten Verwendung ausgeblendet)

**Assigned Users** - Anzahl der Mitarbeiter, die berechtigt sind, dieses Terminal zu verwenden

## Creating a New Terminal

Klicken Sie auf **+ Add Terminal**, um ein neues POS-Gerät zu registrieren:

![Add Terminal Form](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Basic Configuration

**Terminal Name** - Wählen Sie einen beschreibenden Namen, der anzeigt:
- Physischer Standort: "North Entrance Register"
- Funktion: "Returns Desk Terminal"
- Sequenz: "Checkout 1", "Checkout 2", "Checkout 3"

Namen helfen dem Personal, Terminals während der Schichtzuordnung und bei der Fehlerbehebung zu identifizieren. Verwenden Sie konsistente Namenskonventionen in allen Standorten.

**Warehouse** - **REQUIRED** - Wählen Sie das Lager aus, das dieses Terminal verwendet:
- Bestimmt, welche Lagerbestände für den Verkauf verfügbar sind
- Bestellungen, die auf diesem Terminal aufgegeben werden, werden diesem Lager zugeordnet
- Lagerreservierungen prüfen die Verfügbarkeit im zugewiesenen Lager
- **Kann keine Verkäufe verarbeiten, wenn kein Lager zugewiesen ist**

Wenn Sie mehrere Einzelhandelsstandorte haben, erstellen Sie ein separates Lager für jeden Standort und weisen Sie Terminals entsprechend zu.

**Is Active** - Schalten Sie das Terminal ein oder aus, ohne die Konfiguration zu löschen:
- Inaktive Terminals können nicht gepaart werden
- Bestehende Sitzungen auf inaktiven Terminals verfallen sofort
- Verwenden Sie dies, um gestohlene oder beschädigte Terminals vorübergehend zu deaktivieren

### Staff Assignment

**Assigned Users** - Wählen Sie aus, welche Mitarbeiter dieses Terminal nutzen dürfen:
- Nur zugewiesene Benutzer können sich am Terminal anmelden
- Benutzer müssen auch POS-Berechtigungen in ihrer Mitarbeiterrolle haben
- Die Zuweisung von null Benutzern sperrt das Terminal effektiv
- Typisches Muster: Weisen Sie alle Store-Mitarbeiter allen Store-Terminals zu

**Use Case Examples**:
- **General Store**: Weisen Sie alle Mitarbeiter allen Terminals zu (jeder Kassierer kann jede Kasse bedienen)
- **Department Store**: Weisen Sie lager- oder abteilungsspezifische Mitarbeiter den entsprechenden Terminals zu
- **Multi-Location**: Weisen Sie standortbezogene Mitarbeiter den Terminals der Standorte zu
- **Managers**: Weisen Sie Manager allen Terminals zu, um Zugriff für Überwachungszwecke zu ermöglichen

Benutzer ohne Terminalzuordnung erhalten beim Versuch, sich anzumelden, eine Fehlermeldung: "Not authorized for this terminal".

### Hardware Configuration

Das Feld **Hardware Config** ist eine JSON-Struktur, die Peripheriegeräte definiert:

**Thermal Printer**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**USB Barcode Scanner**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Cash Drawer** (an den Drucker angeschlossen):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Complete Example**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Wenn das Terminal keine Peripheriegeräte hat, lassen Sie das Feld leer (geeignet für mobile Terminals oder Tablets ohne Drucker/Scanner).

### Offline Cache Settings

Konfigurieren Sie, wie viel Daten das Terminal für die Offline-Betriebsart zwischenspeichert:

**Order Sync Days** (7-30 Tage, Standard: 14):
- Anzahl der Tage mit kürzlichsten Bestellungen, die lokal zwischengespeichert werden
- Höhere Werte = mehr historische Daten für den Offline-Betrieb verfügbar
- Niedrigere Werte = schnellere Synchronisation, weniger Speicherplatzverbrauch
- **Empfehlung**: 7 Tage für Terminals mit hohem Aufkommen, 14 Tage für den normalen Gebrauch, 30 Tage für Betriebe mit vielen Prüfungen

**Order Sync Limit** (200-1000 Bestellungen, Standard: 500):
- Maximale Anzahl der Bestellungen, die unabhängig vom Datumsbereich zwischengespeichert werden
- Verhindert übermäßigen Speicherplatzverbrauch bei Terminals mit hohem Aufkommen
- **Empfehlung**: 200 für Tablets mit begrenztem Speicherplatz, 500 für Standardterminals, 1000 für dedizierte POS-Geräte

**Trade-offs**:
- **Höhere Einstellungen**: Bessere Offline-Zugänglichkeit zu historischen Daten, langsamerer Anfangssynchronisation, mehr Speicherplatzverbrauch
- **Niedrigere Einstellungen**: Schnellere Synchronisation, weniger Speicherplatz, begrenzte Offline-Geschichte

Das Terminal lädt bei jedem Synchronisationszyklus die letzten X Bestellungen (innerhalb von Y Tagen) herunter. Wenn das Terminal 50 Bestellungen/Tag verarbeitet und sync_days auf 14 gesetzt ist, erwarten Sie ca. 700 Bestellungen im Cache (könnte die sync_limit-Obergrenze erreichen).

## Terminal Pairing Workflow

Nachdem Sie ein Terminal erstellt haben, paaren Sie das physische Gerät:

1. **Generate Pairing Code** - Wird automatisch erstellt, wenn Sie das Terminal speichern (8 alphanumerische Zeichen)

2. **Note the Code** - Wird im Terminal-Liste und im Detailansicht angezeigt (verfällt nach der ersten erfolgreichen Paarung)

3. **Navigate to Terminal Device** - Auf dem physischen Gerät (Tablet/Computer), öffnen Sie den Browser und navigieren Sie zu: `https://yourstore.com/pos/`

4. **Enter Pairing Code** - Geben Sie den 8-stelligen Code ein, wenn Sie aufgefordert werden

5. **Terminal Downloads Configuration** - Das Gerät empfängt:
   - Lagerzuordnung
   - Hardware-Konfiguration (Drucker, Scanner, Schublade)
   - Offline-Cache-Einstellungen
   - Liste der zugewiesenen Benutzer
   - Anfangssynchronisation des Produktkatalogs

6. **Login Prompt Appears** - Das Terminal zeigt eine Anmeldeoberfläche für zugewiesene Benutzer an

7. **Staff Logs In** - Geben Sie die Anmeldeinformationen des Benutzers ein, der diesem Terminal zugewiesen ist

8. **Initial Sync Completes** - Das Terminal lädt herunter:
   - Kürzlichste Bestellungen (je nach sync_days und sync_limit)
   - Vollständigen Produktkatalog für das zugewiesene Lager
   - Kundendatenbank
   - Werbe-Konfigurationen

9. **Terminal Ready** - Der Bildschirm "Ready to Sell" erscheint mit Suchleiste

10. **Pairing Code Consumed** - Der Code wird aus der Verwaltung entfernt; generieren Sie einen neuen Code, wenn eine erneute Paarung erforderlich ist

**Pairing Code Regeneration**: Wenn Sie ein Terminal erneut paaren müssen (Gerät wurde zurückgesetzt, Browser-Cache wurde gelöscht, neues Hardware), verwenden Sie die Verwaltungsaktion **Regenerate Pairing Code**. Dies macht den alten Code ungültig und erstellt einen neuen.

## Monitoring Terminal Status

### Heartbeat System

Terminals senden dem Server alle **5 Minuten** ein Heartbeat-Signal, das folgende Informationen enthält:
- Terminal UUID
- Aktueller Zeitstempel
- Anzahl der online Benutzer
- Zeitstempel der letzten Synchronisation
- Status des Service Workers

**Online Status Indicator**:
- **Green** - Heartbeat innerhalb der letzten 5 Minuten empfangen (Terminal ist online und betriebsbereit)
- **Red** - Kein Heartbeat seit mehr als 5 Minuten (Terminal ist offline oder getrennt)
- **Gray** - Terminal wurde nie gepaart (kein Heartbeat jemals empfangen)

**Use Cases**:
- **Daily open**: Prüfen Sie, ob alle Terminals online sind, bevor das Geschäft öffnet
- **Troubleshooting**: Identifizieren Sie, welche Terminals Verbindungsprobleme haben
- **Audit**: Stellen Sie sicher, dass Terminals während der Geschäftszeiten aktiv sind

### Last Heartbeat Timestamp

Zeigt das genaue Datum und die Uhrzeit des letzten Heartbeats an. Verwenden Sie dies, um:
- Zu bestimmen, wie lange ein Terminal offline ist
- Muster zu erkennen (z. B. Terminal geht jede Nacht bei Schließung offline)
- Die Synchronisationsfrequenz zu überprüfen (sollte alle ~5 Minuten aktualisiert werden, wenn online)

## Remote Unlock Feature

Wenn ein Terminal unreaktiv oder auf einem Bildschirm feststeckt (Softwareabsturz, Sitzungstimeout-Probleme, Browser-Hängen), verwenden Sie die Verwaltungsaktion **Remote Unlock**:

**How It Works**:
1. Wählen Sie das problematische Terminal in der Verwaltungsliste aus
2. Wählen Sie **Remote Unlock** aus dem Dropdown-Menü der Verwaltungsaktionen aus
3. Bestätigen Sie die Aktion
4. Der Server sendet ein Entsperrsignal über die Heartbeat-Antwort
5. Das Terminal erhält das Signal beim nächsten Heartbeat-Zyklus (<5 Min)
6. Das Terminal zwingt den aktuellen Benutzer abzumelden und kehrt zur Anmeldeoberfläche zurück

**When to Use**:
- Terminal ist auf dem Transaktionsbildschirm gefroren
- Personal kann sich nicht abmelden (Abmeldetaste reagiert nicht)
- Sitzung erscheint aktiv, aber Terminal ist unreaktiv
- Browser ist abgestürzt, aber die Sitzungskochi bleibt bestehen

**Important**: Remote Unlock startet das Gerät oder den Browser nicht neu – es zwingt nur zur Abmeldung und löscht die Sitzung. Wenn das Terminal vollständig blockiert ist, muss das Personal den Browser oder das Gerät manuell neu starten.

## Editing Terminal Configuration

Klicken Sie auf ein Terminal in der Liste, um seine Konfiguration zu bearbeiten:

![Edit Terminal Form](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Safe to Change While Terminal is Online**:
- Terminal name
- Assigned users
- Hardware config (wird nach Neustart der Anwendung wirksam)
- Offline cache settings (wirksam bei der nächsten Synchronisation)

**Requires Re-Pairing**:
- Warehouse assignment (Änderung des Lagers erfordert erneute Paarung zur Synchronisation der neuen Lagerbestände)

**Cannot Change**:
- UUID (unveränderliche Kennung)

Änderungen an den meisten Einstellungen werden beim nächsten Heartbeat/Synchronisationszyklus angewendet. Änderungen an der Hardwarekonfiguration erfordern, dass das Personal die POS-App schließt und erneut öffnet (oder den Browser aktualisiert).

## Troubleshooting Common Issues

**Terminal zeigt bei der Anmeldung "Not Authorized" an**:
- Stellen Sie sicher, dass der Benutzer in der Liste **Assigned Users** für dieses Terminal steht
- Stellen Sie sicher, dass der Benutzer POS-Berechtigungen in **Staff & Permissions > Roles** hat
- Prüfen Sie, ob das Terminal als **Is Active** markiert ist

**Terminal paart sich nicht (ungültiger Code)**:
- Paarungscodes verfallen nach der ersten Verwendung – generieren Sie sie bei Bedarf erneut
- Codes sind fallsensitiv – prüfen Sie die Großschreibung
- Stellen Sie sicher, dass das Terminal als **Is Active** markiert ist

**Terminal zeigt offline (Roter Punkt) an**:
- Stellen Sie sicher, dass das Gerät Internetzugang hat
- Prüfen Sie, ob das Terminal tatsächlich läuft (Browser ist auf die URL /pos/ geöffnet)
- Stellen Sie sicher, dass der Firewall nichts die Heartbeat-Anfragen blockiert
- Warten Sie 5 Minuten, bis der nächste Heartbeat-Zyklus stattfindet

**Terminal ist langsam bei der Synchronisation**:
- Reduzieren Sie **Order Sync Days** von 30 auf 7
- Reduzieren Sie **Order Sync Limit** von 1000 auf 200
- Prüfen Sie die Netzwerkgeschwindigkeit am Terminalstandort
- Stellen Sie sicher, dass der Server nicht unter hohem Last steht

**Drucker funktioniert nicht**:
- Prüfen Sie die Drucker-IP-Adresse und den Port in **Hardware Config**
- Testen Sie die Verbindung zum Drucker vom Terminalgerät aus (pingen Sie die IP-Adresse)
- Stellen Sie sicher, dass der Drucker ESC/POS-kompatibel ist
- Prüfen Sie, ob der Drucker eingeschaltet und online ist

## Tips

- **Namenskonvention ist wichtig** - Verwenden Sie konsistente Namensgebung (Standort + Nummer), um die Verwaltung im großen Stil zu vereinfachen
- **Weisen Sie immer ein Lager zu, bevor Sie das Terminal paaren** - Terminals können keine Verkäufe verarbeiten, wenn kein Lager zugewiesen ist
- **Testen Sie die Hardwarekonfiguration vor der Bereitstellung** - Drucken Sie eine Testquittung, um die Integration von Drucker/Schublade zu überprüfen
- **Überwachen Sie den Heartbeat täglich** - Richten Sie eine Routine ein, um sicherzustellen, dass alle Terminals bei der Öffnung des Geschäfts online sind
- **Verringern Sie die Synchronisationseinstellungen für mobile Terminals** - Tablets und Handys profitieren von sync_days: 7, sync_limit: 200
- **Verwenden Sie Remote Unlock sparsam** - Die Zwang-Abmeldung unterbricht aktuelle Transaktionen; bestätigen Sie zunächst, dass das Terminal tatsächlich blockiert ist
- **Dokumentieren Sie Paarungscodes** - Schreiben Sie den Code auf, bevor Sie das Terminal auf den Verkaufsstandort bereitstellen (im Fall, dass die Einrichtung länger dauert als erwartet)
- **Weisen Sie Manager allen Terminals zu** - Stellen Sie sicher, dass Supervisor Zugriff auf jede Kasse für Stornos, Rückerstattungen und Fehlerbehebung haben

