---
title: Vollständige Systemmigration
---

Die Vollständige Systemmigration überträgt Ihr gesamtes Geschäft – Einstellungen, Produkte, Kunden, Bestellungen, Mediendateien und alle anderen Daten – von einer Spwig-Installation zu einer anderen. Verwenden Sie dies, wenn Sie zu einem neuen Server wechseln oder eine vollständige Kopie Ihres Geschäfts einrichten möchten.

## Wann eine Vollmigration verwendet werden sollte

- **Serverumzug**: Ihr Geschäft auf einen neuen Hosting-Anbieter oder Server verschieben
- **Erstellung einer Testumgebung**: Einrichten einer vollständigen Testumgebung aus der Produktionsumgebung
- **Wiederherstellung nach Katastrophen**: Wiederherstellung eines vollständigen Geschäfts aus einer Backup-Instanz

Die Vollmigration umfasst alles, was die Einstellungen-Synchronisation umfasst, plus alle Transaktionsdaten (Produkte, Kunden, Bestellungen, Bewertungen, Lagerbestände, Medien usw.).

## Was migriert wird

Die Vollmigration kann alle Einstellungs-Kategorien plus diese Datenkategorien übertragen:

| Kategorie | Beschreibung |
|----------|-------------|
| **Installierte Komponenten** | Themes, Anbieterintegrationen und Hilfskomponenten mit ihren Paketdateien |
| **Produkte, Kategorien & Marken** | Produkte, Varianten, Bilder, Kategorien, Marken und Attribute |
| **Medienbibliothek** | Alle hochgeladenen Mediendateien und Assets |
| **Kunden & Adressen** | Kundenkonten, Profile und Adressen |
| **Bestellhistorie** | Bestellungen, Bestellpositionen und Transaktionsdaten |
| **Produktbewertungen** | Kundenbewertungen und Bewertungen |
| **Lagerbestände** | Lagerbestände pro Lager und Neubestellpunkte |
| **Digitale Produkte & Lizenzen** | Digitale Assets, Lizenzvorlagen und Lizenzpools |
| **Gutscheine & Gutscheinverwendung** | Gutscheinkonten und Gutscheinverwendungsaufzeichnungen |
| **Geschäfts-Kredit & Wallets** | Kunden-Wallet-Balancen und Transaktionshistorie |
| **Loyalitätsprogramm-Mitglieder** | Loyalitätsmitglieder, Punkte, Transaktionen und Abzeichen |
| **Aktive Abonnements** | Abonnementpläne, aktive Abonnements und Zahlungshistorie |
| **Versand & Tracking** | Versanddokumente und Tracking-Events |
| **Rückerstattungen, Rückgaben & Bestellnotizen** | Rückerstattungsdokumente, Rückgabeanfragen und Notizen |
| **Affiliate-Mitglieder** | Affiliate-Konten, Referral-Codes und Provisionshistorie |

## Schritt-für-Schritt-Anleitung

### Schritt 1: Verbindung zur Quellinstanz herstellen

1. Navigieren Sie zu **Datenmigration > Spwig-zu-Spwig-Synchronisation** in der Admin-Seitenleiste
2. Klicken Sie auf **Vollständige Migration starten**
3. Verbinden Sie sich mit dem Quellgeschäft (dem Geschäft, das Sie **von** migrieren):
   - Geben Sie die URL des Quellgeschäfts ein
   - Fügen Sie den Synchronisationstoken aus dem Quellgeschäft ein
   - Benennen Sie die Verbindung (z. B. "Old Production Server")
4. Klicken Sie auf **Verbindung testen**, um zu überprüfen
5. Klicken Sie auf **Weiter**

> **Wichtig:** Die Vollmigration zieht **immer** Daten aus dem verbundenen Geschäft in dieses Geschäft. Führen Sie den Assistenten auf dem **Ziel** (neuen) Geschäft aus.

### Schritt 2: Umfang auswählen

Wählen Sie aus, welche Datenkategorien in die Migration einbezogen werden sollen. Kategorien sind in Gruppen organisiert:

- **Einstellungen**: Geschäftskonfiguration, Themes, Anbieter, Inhalte
- **Daten**: Produkte, Kunden, Bestellungen, Medien und andere Transaktionsdaten

Einige Kategorien haben Abhängigkeiten (z. B. hängen Bestellungen von Kunden und Produkten ab). Abhängigkeiten werden automatisch mit einbezogen, wenn Sie eine Kategorie auswählen.

Kategorien mit besonderen Kennzeichnungen:
- **Schlüssel-Icon**: Enthält Anmeldeinformationen, die sicher übertragen werden
- **Datei-Icon**: Enthält Binärdateien (Bilder, Medien, Pakete)
- **Warn-Icon**: Besondere Überlegungen für Produktionsumgebungen

### Schritt 3: Vorab-Prüfungen

Bevor die Migration beginnt, überprüfen automatische Vorab-Prüfungen:

- **Verbindungsstatus**: Das Quellgeschäft ist erreichbar und authentifiziert
- **Versionskompatibilität**: Beide Geschäfte laufen mit kompatiblen Spwig-Versionen
- **Speicherplatz**: Ausreichend Speicher ist für Mediendateien vorhanden
- **Datenbankbereitschaft**: Die Ziel-Datenbank kann die Daten empfangen

Wenn eine Prüfung fehlschlägt, erhalten Sie spezifische Anweisungen, wie Sie das Problem vor der Fortsetzung beheben können.

### Schritt 4: Migrationserfolg

Die Migration läuft im Hintergrund. Sie können sicher weiter navigieren – der Prozess wird fortgesetzt.



Die Fortschrittsseite zeigt an:
- Gesamtprozent mit geschätzter verbleibender Zeit
- Vervollständigungsstatus pro Kategorie
- Live-Aktivitätsprotokoll mit Übertragungsdetails
- Medienübertragungsstatistiken (übertragene Dateien und Bytes) für die Medienkategorie

Bei großen Stores mit vielen Produkten und Mediendateien kann die Migration etwas Zeit in Anspruch nehmen. Die Medienübertragungsphase ist in der Regel die längste.

### Schritt 5: Ergebnisse

Nach Abschluss der Migration zeigt die Ergebnisseite an:

- Zusammenfassungsstatistiken (migrierte, übersprungene, fehlgeschlagene Elemente)
- Aufschlüsselung pro Kategorie mit Status
- Fehlerdetails für alle fehlgeschlagenen Elemente

## Nach-Migration-Checkliste

Nach einer erfolgreichen Migration führen Sie diese Schritte auf Ihrem neuen Store durch:

1. **Aktivieren Sie Ihre Lizenz** auf der neuen Installation
2. **Geben Sie die Zahlungsdienstanbieterdaten erneut ein**, die während der Migration übersprungen wurden (Test-/Sandbox-Schlüssel werden nicht auf die Produktionsumgebung übertragen)
3. **Konfigurieren Sie DNS**, um Ihren Domain-Namen auf den neuen Server zu verweisen
4. **Testen Sie den Checkout-Vorgang** mit einer Testbestellung
5. **Überprüfen Sie, ob das Versenden von E-Mails** korrekt funktioniert
6. **Prüfen Sie Mediendateien**, ob Bilder korrekt geladen werden

## Rollback

Nach Abschluss einer Vollmigration haben Sie **24 Stunden**, um einen Rollback durchzuführen. Ein Rollback löscht alle migrierten Daten aus dem Ziel-Store und stellt ihn in den Zustand vor der Migration zurück.

Um einen Rollback durchzuführen:
1. Gehen Sie zur Ergebnisseite oder zum Sync-Dashboard
2. Klicken Sie auf **Migration rollbacken** und bestätigen Sie
3. Warten Sie, bis der Rollback abgeschlossen ist

> **Warnung:** Ein Rollback entfernt alle migrierten Daten dauerhaft. Alle Änderungen, die nach der Migration auf dem Ziel-Store vorgenommen wurden (z. B. neue Bestellungen, Kundenregistrierungen usw.), werden ebenfalls beeinflusst.

Nach 24 Stunden läuft die Rollback-Option ab.

## Tipps

- **Führen Sie die Migration auf dem Ziel-Store durch**: Der Vollmigrations-Assistent sollte auf dem **neuen** Store ausgeführt werden, um Daten vom alten Store zu ziehen
- **Migrieren Sie auf eine saubere Installation**: Für die besten Ergebnisse führen Sie die Migration auf einer frischen Spwig-Installation durch, bevor Sie online gehen
- **Überprüfen Sie den Speicherplatz**: Stellen Sie sicher, dass der Zielserver genügend Speicherplatz für alle Mediendateien hat
- **Lassen Sie die Quelle laufen**: Schalten Sie den Quell-Store nicht aus, bevor Sie alles auf dem Ziel-Store überprüft haben
- **Planen Sie die DNS-Übertragung**: Nachdem Sie die Migration überprüft haben, aktualisieren Sie Ihre DNS-Einträge, um auf den neuen Server zu weisen