---
title: Webhook-Protokolle
---

Webhook-Protokolle bieten ein dauerhaftes Auditprotokoll aller eingehenden Webhook-Anfragen von Frachtführern – sie erfassen die Anfrage-Methode, den Endpunkt-URL, die Header, die Nutzlast, den Verarbeitungsstatus (ausstehend/verarbeitet/fehlgeschlagen) und die Antwort. Jeder Webhook wird vor der Verarbeitung protokolliert, um sicherzustellen, dass keine Ereignisse verloren gehen, wenn die Verarbeitung fehlschlägt. Protokolle ermöglichen das Debuggen von Webhook-Integrationen, die Überwachung der Zuverlässigkeit der Frachtführer-APIs und die Rekonstruktion von Lieferzeitleisten für den Kundensupport.

Diese schreibgeschützte Admin-Seite hilft bei der Behebung von Webhook-Fehlern und zur Überprüfung des Gesundheitszustands der Frachtführer-Integration.

## Struktur der Webhook-Protokolle

Jeder Protokoll-Eintrag dokumentiert:

**Anfrage-Details**:
- **Anbieter-Schlüssel**: Welcher Frachtführer den Webhook gesendet hat (fedex, ups, dhl)
- **Endpunkt**: Webhook-URL-Pfad (z. B. `/webhooks/shipping/fedex/`)
- **Methode**: HTTP-Methode (meist POST)
- **Header**: Anfrage-Header (JSON)
- **Nutzlast**: Anfrage-Körper (JSON)

**Verarbeitung**:
- **Verarbeitungsstatus**: ausstehend, verarbeitet, fehlgeschlagen
- **Fehlermeldung**: Grund des Fehlers (falls status=fehlgeschlagen)
- **Antwort**: HTTP-Antwort, die an den Frachtführer gesendet wurde
- **Antwort-Statuscode**: 200, 400, 500 usw.

**Zeitstempel**:
- **Empfangen um**: Zeitpunkt, zu dem der Webhook empfangen wurde
- **Verarbeitet um**: Zeitpunkt, zu dem die Verarbeitung abgeschlossen wurde

---

## Werte des Verarbeitungsstatus

**ausstehend**: Webhook empfangen, wartet auf Verarbeitung
- Normal für einen kurzen Moment nach Empfang
- Wenn der Status ausstehend bleibt, deutet dies auf einen Rückstau in der Verarbeitungsqueue hin

**verarbeitet**: Webhook erfolgreich verarbeitet
- TrackingEvent erstellt
- Kundennachricht gesendet (falls zutreffend)
- Antwort 200 an den Frachtführer gesendet

**fehlgeschlagen**: Webhook-Verarbeitung fehlgeschlagen
- Prüfen Sie die Fehlermeldung, um den Grund zu ermitteln
- Häufige Ursachen: Ungültiges JSON, unbekannte Sendung, doppeltes Ereignis

---

## Webhook-Ablauf

**Normaler Ablauf**:
```
1. Frachtführer scanniert Paket
   ↓
2. Frachtführer sendet POST an Spwig-Webhook-Endpunkt
   ↓
3. Spwig erstellt WebhookLog (status=ausstehend)
   ↓
4. Hintergrundworker verarbeitet Webhook
   ↓
5. Parsen Sie JSON-Nutzlast
   ↓
6. Finden Sie passende Sendung (über Tracking-Nummer)
   ↓
7. Erstellen Sie TrackingEvent
   ↓
8. Aktualisieren Sie WebhookLog (status=verarbeitet)
   ↓
9. Senden Sie HTTP 200-Antwort an Frachtführer
```

**Fehlerfälle**:
- **Ungültiges JSON**: Frachtführer hat fehlerhaftes Datenformat gesendet → status=fehlgeschlagen, Fehler="JSON-Parsee-Fehler"
- **Unbekannte Sendung**: Tracking-Nummer stimmt mit keiner Sendung überein → status=fehlgeschlagen, Fehler="Sendung nicht gefunden"
- **Doppelte**: Ereignis existiert bereits → status=fehlgeschlagen, Fehler="Doppeltes Ereignis"

---

## Debuggen von Webhook-Fehlern

**Schritt-für-Schritt**:

**1. Nach Status=fehlgeschlagen filtern**
- Navigieren Sie zu Versand > Webhook-Protokolle
- Filter: Verarbeitungsstatus = "fehlgeschlagen"
- Überprüfen Sie kürzliche Fehler

**2. Fehlermeldung prüfen**
- Klicken Sie auf den Protokolleintrag
- Lesen Sie das Feld error_message
- Häufige Fehler:
  - "Sendung nicht gefunden" → Tracking-Nummer stimmt nicht überein
  - "JSON-Decode-Fehler" → Frachtführer hat ungültiges JSON gesendet
  - "Fehlender erforderlicher Feld" → Nutzlast fehlt erwartete Daten

**3. Nutzlast untersuchen**
- Zeigen Sie die Roh-JSON-Nutzlast an
- Stellen Sie sicher, dass die Struktur dem erwarteten Format entspricht
- Prüfen Sie auf fehlende Felder (tracking_id, event_type usw.)

**4. Überprüfen Sie, ob die Sendung existiert**
- Extrahieren Sie die Tracking-Nummer aus der Nutzlast
- Suchen Sie Sendungen nach der Tracking-Nummer
- Stellen Sie sicher, dass die Sendung existiert und der richtige Frachtführer verwendet wird

**5. Anbieter-Konfiguration prüfen**
- Stellen Sie sicher, dass der Anbieter-Konto aktiv ist
- Bestätigen Sie, dass die Webhook-Endpunkt-URL korrekt ist
- Testen Sie die Anbieter-API-Anmeldeinformationen

**6. Verarbeitung erneut versuchen** (falls zutreffend)
- Einige Webhook-Verarbeiter unterstützen manuelle Wiederholung
- Beheben Sie zuerst den zugrunde liegenden Fehler
- Wiederholung des fehlgeschlagenen Webhook

---

## Häufige Webhook-Probleme

**Problem 1: "Sendung nicht gefunden"**

**Ursache**: Tracking-Nummer im Webhook stimmt mit keiner Sendung überein
- Tippfehler beim Erstellen der Sendung
- Webhook für ein anderes Konto
- Sendung wurde vor dem Empfang des Webhooks gelöscht

**Lösung**:
- Stellen Sie sicher, dass die Tracking-Nummer korrekt geschrieben ist
- Prüfen Sie, ob der Frachtführer des Webhooks mit der Sendung übereinstimmt
- Erstellen Sie die Sendung erneut, wenn nötig

---

**Problem 2: "JSON-Decode-Fehler"**

**Ursache**: Frachtführer hat fehlerhaftes JSON gesendet
- Selten, meist ein Fehler der Frachtführer-API
- Zeichencodierungsprobleme

**Lösung**:
- Kontaktieren Sie den Frachtführer-Support mit der Rohnutzlast
- Prüfen Sie die Header auf Zeichencodierung
- Bestätigen Sie die Endpunkt-URL im Frachtführer-Dashboard

---

**Problem 3: Doppelte Webhooks**

**Ursache**: Frachtführer sendet dasselbe Ereignis mehrmals
- Wiederholungslogik (Frachtführer hat 200-Antwort nicht empfangen)
- Fehler im Frachtführer-System

**Lösung**:
- Das System lehnt doppelte Webhooks automatisch ab (normaler Verhaltensweise)
- Stellen Sie sicher, dass der response_status_code 200 ist
- Falls das Problem besteht, kontaktieren Sie den Frachtführer-Support

---

**Problem 4: Fehlende Webhooks**

**Ursache**: Erwarteter Webhook wurde nie empfangen
- Frachtführer hat nichts gesendet (Scan verpasst)
- Webhook-Endpunkt falsch konfiguriert im Frachtführer-Dashboard
- Firewall blockiert Anfragen

**Lösung**:
- Prüfen Sie die Webhook-Konfiguration im Frachtführer-Dashboard
- Bestätigen Sie, dass die Endpunkt-URL öffentlich und erreichbar ist
- Testen Sie den Endpunkt mit curl/Postman
- Prüfen Sie die Firewall-Regeln des Servers

---

## Webhook-Endpunkt-Konfiguration

**Typische Webhook-URLs**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Konfiguration im Frachtführer-Dashboard**:
1. Melden Sie sich im Frachtführer-Entwicklerportal an
2. Navigieren Sie zu Webhook-Einstellungen
3. Geben Sie die Spwig-Webhook-URL ein
4. Wählen Sie Ereignisse aus, auf die Sie abonnieren möchten (Tracking-Updates, Lieferung, Ausnahmen)
5. Speichern Sie die Konfiguration
6. Testen Sie den Webhook mit dem Test-Tool des Frachtführers

**Sicherheit**:
- Webhooks erfordern HTTPS (nicht HTTP)
- Einige Frachtführer signieren Anfragen (Prüfen Sie die Signatur)
- IP-Whitelist (falls der Frachtführer statische IPs bereitstellt)

---

## Überwachung der Webhook-Gesundheit

**Wichtige Metriken**:

**Erfolgsquote**:
```
Erfolgsquote = (Verarbeitet / Gesamt) × 100%

Ziel: >98%
```

**Verarbeitungszeit**:
```
Durchschnittliche Zeit = Verarbeitet um - Empfangen um

Ziel: <2 Sekunden
```

**Fehlermuster**:
- Sudden Anstieg an Fehlern → Änderung oder Ausfall der Frachtführer-API
- Konsistente Fehlermeldung "Sendung nicht gefunden" → Synchronisationsproblem der Tracking-Nummer
- Alle Webhooks fehlgeschlagen → Problem mit der Endpunkt-Konfiguration

**Überwachungsstrategie**:
- Prüfen Sie die Fehlerquote täglich
- Benachrichtigen Sie, wenn die Fehlerquote >5% ist
- Überprüfen Sie die Fehlermeldungen wöchentlich
- Vergleichen Sie mit dem Status-Portal des Frachtführers

---

## Webhook-Beibehaltung

**Protokolle sind dauerhaft** - werden nie automatisch gelöscht

**Warum dauerhaft**:
- Audit-Konformität
- Kundensupport (Rekonstruktion der Lieferzeitlinie)
- Streitbeilegung
- Webhook-Debuggen

**Speicher**: Protokolle werden effizient gespeichert (komprimiertes JSON)

---

## Tipps

- **Webhooks sind permanente Audit-Protokolle** - Löschen Sie sie nie, auch wenn sie erfolgreich verarbeitet wurden
- **Prüfen Sie täglich fehlgeschlagene Webhooks** - Erkennen Sie Integration-Probleme frühzeitig
- **Überwachen Sie Verarbeitungsverzögerung** - Langes Verzögerung deutet auf ein Leistungsproblem hin
- **Speichern Sie Rohnutzlasten** - Essential für Debuggen von Änderungen an der Frachtführer-API
- **Testen Sie die Endpunkt-Konfiguration** - Verwenden Sie Test-Tools des Frachtführers, um die Einrichtung zu überprüfen
- **Aktivieren Sie Webhook-Unterschrift** - Bestätigen Sie, dass Anfragen tatsächlich vom Frachtführer stammen
- **Whitelisten Sie Frachtführer-IPs** - Wenn der Frachtführer statische IP-Bereiche bereitstellt
- **Richten Sie Alerts ein** - Benachrichtigen Sie, wenn die Fehlerquote den Schwellenwert überschreitet
- **Vergleichen Sie mit dem Frachtführer-Status** - Lücken in Webhooks können auf einen Ausfall des Frachtführers hinweisen
- **Dokumentieren Sie Frachtführer-Nutzlastformate** - Hilft, wenn der Frachtführer die API aktualisiert
- **Behalten Sie Webhook-URLs stabil** - Änderungen an URLs erfordern eine Aktualisierung im Frachtführer-Dashboard