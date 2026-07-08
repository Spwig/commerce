---
title: Zahlungsterminal-Anbieter
---

Zahlungsterminal-Anbieter ermöglichen die Annahme von Kredit- und Debitkarten an Ihren POS-Terminals. Stripe Terminal ist der primär unterstützte Anbieter, der moderne Kartenleser (S700, WisePOS E, P400), wettbewerbsfähige Verarbeitungsraten und eine nahtlose Integration anbietet. Konfigurieren Sie Anbieterkonten mit API-Anmeldeinformationen, überwachen Sie den Verbindungsstatus in Echtzeit und verwalten Sie mehrere Anbieter, wenn Sie in verschiedenen Regionen tätig sind. Das Anbieter-System ist erweiterbar – weitere Zahlungsdienstleister können über das Anbieter-Framework integriert werden, wenn Stripe Terminal in Ihrem Markt nicht verfügbar ist.

Verwenden Sie Zahlungsdienstleister, um Kartenzahlungen sicher zu akzeptieren, den Zahlungsverarbeitungsstatus zu verfolgen und Leserzuordnungen über Terminals zu verwalten.

![Zahlungsdienstleister-Liste](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Übersicht über Zahlungsdienstleister

Zahlungsdienstleister sind Drittanbieter-Dienste, die im Namen Ihres Geschäfts Kartenzahlungen verarbeiten:

**Verantwortlichkeiten des Anbieters**:
- Autorisierung von Karten-transaktionen in Echtzeit
- Kommunikation mit physischen Kartenlesern
- Sicherstellung der Zahlungssicherheit (PCI-Konformität, Verschlüsselung)
- Überweisung der Gelder auf Ihr Bankkonto (Abrechnung)
- Bereitstellung von Transaktionsberichten und Streitmanagement

**Rolle von Spwig**:
- Leitet Zahlungsanfragen an den konfigurierten Anbieter weiter
- Speichert verschlüsselte Anbieteranmeldeinformationen
- Überwacht den Verbindungsstatus
- Ordnet Leser Terminals zu
- Dokumentiert Zahlungsergebnisse in Bestellungen

## Stripe Terminal (Hauptanbieter)

Stripe Terminal ist der empfohlene Zahlungsdienstleister für die meisten Händler:

**Funktionen**:
- Moderne EMV-Chipkartenleser
- Unterstützung für kontaktlose Zahlungen (NFC) (Apple Pay, Google Pay, Karten mit Tap-to-Pay)
- Integriertes Streitmanagement
- Echtzeit-Autorisierung
- Entwicklerfreundliche API
- Verfügbar in mehr als 40 Ländern

**Preise** (Stand 2024, aktuelle Preise prüfen):
- Transaktionsgebühren: 2,7 % + 0,05 $ pro persönlichen Transaktionen (USA)
- Keine monatlichen Gebühren, keine Einrichtungsgebühren, keine Gebühren für PCI-Konformität
- Kartenleser-Hardware: Einmalige Kaufpreise (59 $–299 $, je nach Modell)

**Unterstützte Regionen**:
- Vereinigte Staaten, Kanada, Vereinigtes Königreich, Europäische Union, Australien, Singapur und mehr
- Stripe-Verfügbarkeit prüfen: https://stripe.com/terminal

**Unterstützte Leser**:
- BBPOS WisePOS E (All-in-One Android-Terminal)
- Stripe Reader S700 (Kassenterminal)
- Verifone P400 (Legacy-Leser, weiterhin unterstützt)

## Einrichtung von Stripe Terminal

**Schritt 1: Stripe-Konto erstellen**
- Registrieren Sie sich auf stripe.com
- Vollenden Sie die Geschäftsverifikation (Bankkonto, Steuernummer)
- Aktivieren Sie Zahlungen

**Schritt 2: Stripe Terminal aktivieren**
- Navigieren Sie im Stripe-Dashboard zu **Produkte > Terminal**
- Klicken Sie auf **Erste Schritte**
- Akzeptieren Sie die Geschäftsbedingungen für Terminal

**Schritt 3: Standort erstellen**
- Stripe Terminal erfordert einen "Standort", der Ihren physischen Einzelhandelsgeschäftsort darstellt
- Navigieren Sie zu **Terminal > Standorte**
- Klicken Sie auf **Standort erstellen**
- Geben Sie die Ladenadresse und Details ein
- Speichern Sie die Standort-ID (sieht aus wie `tml_1ABC123...`)

**Schritt 4: API-Schlüssel generieren**
- Navigieren Sie zu **Entwickler > API-Schlüssel**
- Finden Sie Ihren **Geheimen Schlüssel** (beginnt mit `sk_live_...` für Produktion, `sk_test_...` für Tests)
- Kopieren Sie den geheimen Schlüssel (teilen Sie ihn nicht öffentlich)

**Schritt 5: In Spwig konfigurieren**
- Navigieren Sie zu **POS > Zahlungsdienstleister**
- Klicken Sie auf **+ Zahlungsdienstleister hinzufügen**
- Wählen Sie **Anbieter**: "Stripe Terminal"
- Geben Sie **API-Geheimen Schlüssel** ein (aus Schritt 4)
- Geben Sie **Standort-ID** ein (aus Schritt 3)
- Speichern Sie

**Schritt 6: Verbindung testen**
- Nach dem Speichern sollte der Anbieterstatus in "Verbunden" (grün) geändert werden
- Wenn der Status "Fehler" (rot) anzeigt, überprüfen Sie API-Schlüssel und Standort-ID
- Prüfen Sie die Fehlermeldung im Detailansicht des Anbieters

![Zahlungsdienstleister-Hinzufügen-Formular](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Konfigurationsfelder für Anbieter

**Anbieter-Schlüssel** - Wählen Sie den Zahlungsdienstleister aus:
- **stripe_terminal** - Stripe Terminal (empfohlen)
- **manual** - Manuelle Zahlungseingabe (nur für Tests, keine tatsächliche Verarbeitung)
- Weitere Anbieter können erscheinen, wenn sie über das Komponentensystem installiert werden

**Anmeldeinformationen (verschlüsselt)** - JSON-Struktur mit API-Anmeldeinformationen:
- Wird automatisch vor dem Speichern verschlüsselt
- Nie im Klartext sichtbar nach dem Speichern
- Beispielstruktur (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Anbieter-Einstellungen** - Zusätzliche Konfiguration (anbieterabhängig):
- Statement-Descriptor (erscheint auf der Kreditkartenabrechnung des Kunden)
- Auto-Capture (sofortige Erfassung autorisierter Zahlungen vs. manuelle Erfassung)
- Währungsüberschreibung (wenn das Anbieterkonto eine andere Währung als das Geschäft verwendet)

**Verbindungsstatus** - Echtzeit-Statusanzeige:
- **Verbunden** (grün) - Anbieter ist erreichbar und korrekt konfiguriert
- **Fehler** (rot) - Verbindung fehlgeschlagen oder ungültige Anmeldeinformationen
- **Unbekannt** (grau) - Noch nicht getestet (unmittelbar nach der Erstellung)

**Zuletzt getestet** - Zeitstempel der letzten Verbindungstest:
- Wird automatisch aktualisiert, wenn Transaktionen verarbeitet werden
- Testen Sie manuell über die **Verbindung testen**-Verwaltungsaktion

## Überwachung des Verbindungsstatus

Das System überwacht die Anbieterverbindung, um Sie vor Problemen zu warnen, bevor Kunden Zahlungen vornehmen:

**Automatische Tests**:
- Jede Zahlungstransaktion löst einen Verbindungstest aus (aus Gründen der Notwendigkeit)
- Hintergrundauftrag testet die Verbindung alle 6 Stunden (präventive Überwachung)

**Statusbedeutungen**:

**Verbunden** - Anbieter-API ist erreichbar, Anmeldeinformationen sind gültig, bereit zur Verarbeitung von Zahlungen

**Fehler** - Häufige Ursachen:
- Ungültiger API-Schlüssel (revokiert, abgelaufen oder falsch)
- Ungültige Standort-ID (Standort in Stripe gelöscht, falsche ID eingegeben)
- Netzwerkverbindungsprobleme (Firewall blockiert Stripe-API)
- Stripe-Dienstausfall (selten)

**Unbekannt** - Anbieter wurde noch nie getestet (neues Konto, das noch keine erste Transaktion verarbeitet hat)

**Fehlerstatus beheben**:
1. Prüfen Sie die Fehlermeldung in der Detailansicht des Anbieters (erklärt das spezifische Problem)
2. Stellen Sie sicher, dass der API-Schlüssel im Stripe-Dashboard immer noch gültig ist
3. Stellen Sie sicher, dass die Standort-ID im Stripe-Dashboard immer noch existiert
4. Testen Sie die Verbindung manuell über die **Verbindung testen**-Verwaltungsaktion
5. Aktualisieren Sie die Anmeldeinformationen bei Bedarf

![Zahlungsdienstleister-Details](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Vergleich unterstützter Kartenleser

Stripe Terminal bietet mehrere Hardware-Optionen für Kartenleser:

| Modell | Typ | Zahlungsmethoden | Anzeige | Bestens geeignet für | Preis |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | All-in-One | EMV-Chip, NFC, Swipe | 5-Zoll-Farbbildschirm | Vollwertiges Einzelhandels-POS | ~$299 |
| **S700** | Kassenterminal | EMV-Chip, NFC, Swipe | Monochrom-LCD | Standard-Einzelhandelskasse | ~$249 |
| **P400** | Kassenterminal | EMV-Chip, NFC, Swipe | Monochrom-LCD | Legacy-Bereitstellungen | ~$299 |

**Vorteile von WisePOS E**:
- Android-basiert (Läuft Apps ab, kann benutzerdefinierte Inhalte anzeigen)
- Farbbildschirm (bessere Benutzererfahrung für Tip-Anfragen, Unterschriftserfassung)
- Integrierter Belegdrucker (optional)
- Schnellste Transaktionsgeschwindigkeit

**Vorteile von S700**:
- Günstiger als WisePOS E
- Kompakte Größe
- Spritzwasserfestes Design

**P400** (älteres Modell):
- Wird weiterhin unterstützt, aber nicht für neue Bereitstellungen empfohlen
- Langsamere Chipkartenverarbeitung als S700/WisePOS E

Alle Leser verbinden sich über die Stripe Terminal API mit dem Spwig POS (keine direkte USB-/Bluetooth-Verbindung zum POS-Gerät erforderlich).

## Sicherheitsaspekte

**Verschlüsselung der Anmeldeinformationen**:
- Alle Anbieteranmeldeinformationen sind im Datenbank-System verschlüsselt
- Die Verschlüsselung erfolgt mit dem Anwendungsschlüssel (definiert in den Anwendungseinstellungen)
- Anmeldeinformationen werden nie in Protokollen oder Fehlermeldungen angezeigt

**Berechtigungen des API-Schlüssels**:
- Verwenden Sie **beschränkte API-Schlüssel** in der Produktion (Berechtigungen auf Terminal beschränken)
- Verwenden Sie keine unbegrenzten Geheimnisschlüssel (breitere Zugriffsrechte als notwendig = Sicherheitsrisiko)
- Im Stripe-Dashboard erstellen Sie einen beschränkten Schlüssel mit nur **Terminal**-Berechtigungen

**PCI-Konformität**:
- Stripe Terminal übernimmt die PCI-Konformität (Karteninformationen erreichen nie die Spwig-Server)
- Kartennummern werden vollständig auf der Leserhardware verarbeitet → Stripe-Server → Karten-netzwerke
- Spwig speichert nur die Zahlungsergebnisse (genehmigt/abgelehnt), nie Karteninformationen

**Schlüsselrotation**:
- Drehen Sie API-Schlüssel jährlich als Sicherheitsmaßnahme
- Bei der Schlüsselrotation aktualisieren Sie die Anmeldeinformationen in der Anbieterkonfiguration
- Alte Schlüssel können im Stripe-Dashboard nach Bestätigung des neuen Schlüssels widerrufen werden

## Mehrere Anbieter

Einige Händler benötigen mehrere Anbieterkonten:

**Mehrwährungsoperationen**:
- US-Geschäfte verwenden Stripe US-Konto (verarbeitet USD)
- Europäische Geschäfte verwenden Stripe EU-Konto (verarbeitet EUR)
- Konfigurieren Sie einen separaten Anbieter pro Währung

**Backup-Anbieter**:
- Hauptanbieter (Stripe Terminal)
- Backup-Anbieter (manuelle Eingabe) bei Leserproblemen
- Kassierer wählt den Anbieter beim Starten der Zahlung

**Testen vs. Produktion**:
- Test-Anbieter mit `sk_test_...` API-Schlüssel
- Produktions-Anbieter mit `sk_live_...` API-Schlüssel
- Wechseln Sie nach dem Testphase zu den Anbieter

## Behebung häufiger Probleme

**Problem 1: Status zeigt "Fehler" mit der Nachricht "Ungültiger API-Schlüssel"**
- **Ursache**: API-Schlüssel wurde widerrufen oder falsch kopiert
- **Lösung**: Generieren Sie einen neuen API-Schlüssel im Stripe-Dashboard, aktualisieren Sie die Anbieteranmeldeinformationen und testen Sie die Verbindung

**Problem 2: Leser nicht während der Zahlung entdeckt**
- **Ursache**: Leser nicht dem Anbieterstandort registriert
- **Lösung**: Im Stripe-Dashboard prüfen, ob der Leser dem gleichen Standort-ID wie in der Anbieterkonfiguration registriert ist

**Problem 3: Zahlungen abgelehnt, obwohl Karte gültig ist**
- **Ursache**: Stripe-Konto nicht vollständig aktiviert (Verifikation ausstehend)
- **Lösung**: Geschäftsverifikation im Stripe-Dashboard vervollständigen (Bankkonto, Steuernummer)

**Problem 4: Verbindungsstatus zeigt "Unbekannt" und aktualisiert sich nie**
- **Ursache**: Anbieter wurde nie getestet (keine Transaktionen versucht)
- **Lösung**: Verbindungstest über die **Verbindung testen**-Verwaltungsaktion manuell auslösen

## Tipps

- **Testmodus vor der Produktion** - Verwenden Sie Stripe-Test-API-Schlüssel (`sk_test_...`) für die erste Einrichtung und Tests
- **Ein Anbieter pro Währung** - Vermeiden Sie die Verarbeitung von EUR mit einem USD-basierten Stripe-Konto; erstellen Sie separate Anbieter
- **Verbindungsstatus wöchentlich überwachen** - Proaktive Überwachung verhindert Zahlungsausfälle am Kassentisch
- **Berechtigungen des API-Schlüssels einschränken** - Begrenzen Sie Stripe-API-Schlüssel auf nur Terminal-Berechtigungen (Prinzip der kleinsten Berechtigung)
- **Standort-IDs dokumentieren** - Halten Sie ein Verzeichnis, welcher Stripe-Standort welchem physischen Geschäft entspricht
- **Leserzuordnung testen** - Nach der Anbieterkonfiguration testen Sie eine Zahlung mit einem echten Leser, um den End-to-End-Fluss zu überprüfen
- **Stripe-Kontaktdaten aktualisieren** - Stellen Sie sicher, dass die Geschäfts-Kontaktdaten im Stripe-Konto aktuell sind (wichtig für Streitigkeiten, Konformität)