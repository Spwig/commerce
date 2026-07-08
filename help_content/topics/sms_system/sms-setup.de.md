---
title: SMS-Anbieter-Setup
---

SMS-Benachrichtigungen halten Ihre Kunden über jeden Schritt ihres Bestellsprozesses auf dem Laufenden – von der Bestätigung bis zur Lieferung. Um SMS- oder WhatsApp-Nachrichten von Ihrem Store zu senden, verbinden Sie ein SMS-Anbieterkonto mit Ihren Zugangsdaten. Sobald die Verbindung hergestellt ist, verwendet Spwig dieses Konto, um alle ausgehenden Textnachrichten zu senden.

Navigieren Sie zu **SMS-System > SMS-Anbieterkonten**, um Ihre SMS-Anbieter zu verwalten.

![Liste der SMS-Anbieterkonten](/static/core/admin/img/help/sms-setup/provider-list.webp)

## SMS-Anbieter hinzufügen

Sie können einen Anbieter entweder mit dem **Einrichtungsführer** (empfohlen für die erste Einrichtung) oder mit dem manuellen Formular hinzufügen.

### Einrichtungsführer verwenden

1. Navigieren Sie zu **SMS-System > SMS-Anbieterkonten**
2. Klicken Sie auf **Einrichtungsführer** in der Symbolleiste
3. Folgen Sie den Schritten des Führers:
   - **Schritt 1**: Wählen Sie Ihren Anbieter aus der Liste der verfügbaren Anbieter
   - **Schritt 2**: Geben Sie Ihre Anbieterzugangsdaten ein (API-Schlüssel, Konto-SID usw.)
   - **Schritt 3**: Legen Sie den Anzeigenamen und die Standard-Einstellungen fest, dann speichern Sie
4. Der Führer testet die Verbindung automatisch, bevor er gespeichert wird

### Manuelles Hinzufügen eines Anbieters

1. Navigieren Sie zu **SMS-System > SMS-Anbieterkonten**
2. Klicken Sie auf **Anbieter durchsuchen**, um verfügbare SMS-Anbieter zu erkunden, oder klicken Sie direkt auf **+ SMS-Anbieterkonto hinzufügen**
3. Im Feld **Anbieter** wählen Sie Ihren SMS-Anbieter aus dem Dropdown-Menü aus
4. Nachdem Sie einen Anbieter ausgewählt haben, erscheinen automatisch Felder für die Zugangsdaten, basierend auf den Anforderungen dieses Anbieters
5. Füllen Sie die erforderlichen Zugangsdatenfelder aus (diese variieren je nach Anbieter – siehe die Abschnitte unten für gängige Anbieter)
6. Geben Sie einen **Anzeigenamen** an, um dieses Konto zu identifizieren (z. B. `Twilio – Hauptkonto`)
7. Legen Sie die **Standard-Einstellungen** fest (siehe unten)
8. Klicken Sie auf **Speichern**

## Anbieterzugangsdaten

### Twilio

| Feld | Wo Sie es finden können |
|-----|------------------------|
| Account SID | Twilio Console → Dashboard |
| Auth Token | Twilio Console → Dashboard |
| From Number | Ihre Twilio-Telefonnummer im E.164-Format (z. B. `+15551234567`) |

### Andere Anbieter

Andere installierte SMS-Anbieterkomponenten zeigen ihre eigenen spezifischen Zugangsdatenfelder an, wenn sie ausgewählt werden. Beziehen Sie sich auf die Dokumentation Ihres Anbieters, um die genauen Werte zu ermitteln – typischerweise ein API-Schlüssel oder Zugriffstoken und ein Absender-Identifikator.

## Standard-Einstellungen

Nachdem Sie die Zugangsdaten eingegeben haben, konfigurieren Sie, wie dieses Konto verwendet wird:

- **Aktiv** – aktivieren oder deaktivieren Sie dieses Konto. Inaktive Konten werden nicht für das Senden verwendet, auch wenn sie als Standard festgelegt sind
- **Standard-SMS-Konto** – wenn aktiviert, verwenden alle SMS-Benachrichtigungen von Ihrem Store dieses Konto. Nur ein Konto kann zum Zeitpunkt des Standard-SMS-Kontos sein
- **Standard-WhatsApp-Konto** – wenn dieser Anbieter WhatsApp unterstützt (z. B. Twilio über WhatsApp Business API), aktivieren Sie dies, um es als Standard für WhatsApp-Nachrichten zu verwenden

## Verbindung testen

Nachdem Sie ein Anbieterkonto gespeichert haben, testen Sie, ob die Zugangsdaten funktionieren:

1. Navigieren Sie zu **SMS-System > SMS-Anbieterkonten**
2. Klicken Sie auf Ihr Anbieterkonto, um es zu öffnen
3. Klicken Sie auf die Schaltfläche **Verbindung testen**
4. Spwig sendet eine Testanfrage an den Anbieter und aktualisiert das Feld **Verbindungsstatus**

| Status | Bedeutung |
|--------|----------|
| Verbunden | Zugangsdaten sind gültig und der Anbieter ist erreichbar |
| Verbindung fehlgeschlagen | Zugangsdaten sind falsch oder der Anbieter ist nicht erreichbar |
| Nicht getestet | Die Verbindung wurde noch nicht getestet |

Wenn der Test fehlschlägt, überprüfen Sie Ihre Zugangsdaten erneut und stellen Sie sicher, dass Ihr Konto über die erforderlichen Berechtigungen im Dashboard des Anbieters verfügt.

## Verbindungsstatus-Spalte

Die Liste der SMS-Anbieterkonten zeigt ein farbcodiertes **Verbindungs**-Abzeichen für jedes Konto:

- **Verbunden** (grün) – Konto funktioniert
- **Verbindung fehlgeschlagen** (rot) – Zugangsdaten sind fehlerhaft – aktualisieren Sie sie
- **Nicht getestet** (grau) – Konto wurde noch nicht getestet

## Tipps

- Verwenden Sie den Einrichtungsführer für Ihren ersten Anbieter – er führt Sie durch jedes Feld und testet die Verbindung, bevor er gespeichert wird
- Nur ein Konto kann zum Zeitpunkt des Standard-SMS-Kontos sein.

Wenn Sie ein zweites Konto hinzufügen und es als Standard markieren, wird das vorherige Standardkonto automatisch aufgehoben
- Bewahren Sie Ihre Anbieter-API-Anmeldeinformationen an einem sicheren Ort auf.

Wenn sich die Anmeldeinformationen ändern, aktualisieren Sie sie hier sofort, um fehlgeschlagene Benachrichtigungen zu vermeiden
- Inaktive Konten bleiben in der Liste, werden aber nicht zum Versenden verwendet – nützlich, um Backup-Anmeldeinformationen zu speichern, ohne sie zu aktivieren
- Die meisten Anbieter berechnen pro gesendeter Nachricht – überwachen Sie die Nutzung in Ihrem Anbieter-Dashboard, um unerwartete Rechnungen zu vermeiden