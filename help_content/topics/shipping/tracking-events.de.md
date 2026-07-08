---
title: Verfolgungsereignisse
---

Verfolgungsereignisse protokollieren Statusänderungen des Versands während des Lieferprozesses – jedes Ereignis erfasst den Status (im Transport, zur Auslieferung unterwegs, geliefert), das Zeitstempel, die Lage, eine Beschreibung und die Rohdaten des Versandunternehmens. Ereignisse werden automatisch über Webhook-Benachrichtigungen des Versandunternehmens erstellt oder manuell von Händlern. Kunden sehen die Verfolgungshistorie in ihrem Konto und in den Bestätigungs-E-Mails, was eine Echtzeit-Übersicht über die Lieferung bietet.

Diese Admin-Seite zeigt schreibgeschützte Ereignishistorie für Audits und Kundensupport an.

## Struktur von Verfolgungsereignissen

Jedes Ereignis enthält:

**Statusinformationen**:
- **Status**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Beschreibung**: Menschlich lesbare Status (z. B. "Paket ist bei der Sortierstation angekommen")
- **Statuscode des Versandunternehmens**: Originalstatus des Versandunternehmens (z. B. "DEP" für abgefahren)

**Lagedaten**:
- **Stadt**: Stadt des Ereignisortes
- **Bundesland**: Bundesland/Provinz des Ereignisortes
- **Land**: Land des Ereignisortes
- **Postleitzahl**: Postleitzahl/ZIP-Code des Ereignisortes

**Zeitstempel**:
- **Geschehen um**: Wann das Ereignis tatsächlich stattfand (Zeit des Versandunternehmens)
- **Erstellt um**: Wann das Ereignis in Spwig protokolliert wurde (Systemzeit)

**Metadaten**:
- **Rohdaten**: Vollständige JSON-Antwort des Versandunternehmens-API
- **Versand**: Verknüpfter Versand-ID

---

## Typen von Ereignisstatus

**in_transit**: Paket bewegt sich durch das Netzwerk des Versandunternehmens
- Beispiele: "Von der Einrichtung abgereist", "Bei der Zentrale angekommen", "Im Transport zur nächsten Einrichtung"

**out_for_delivery**: Paket ist auf dem Lieferfahrzeug
- Beispiele: "Zur Auslieferung unterwegs", "Auf dem Lieferfahrzeug"

**delivered**: Paket wurde erfolgreich geliefert
- Beispiele: "Geliefert an die Vordertür", "Bei der Empfangsdame abgegeben", "Dem Empfänger übergeben"

**exception**: Lieferproblem, das Aufmerksamkeit erfordert
- Beispiele: "Wetterbedingte Verzögerung", "Falsche Adresse", "Auslieferungsversuch fehlgeschlagen"

**failed**: Lieferung ist dauerhaft gescheitert
- Beispiele: "Unzustellbar nach der angegebenen Adresse", "Vom Empfänger abgelehnt"

**returned**: Paket wird an den Absender zurückgesandt
- Beispiele: "Zurücksendung initiiert", "Paket wird zurückgesandt"

---

## Wie Verfolgungsereignisse erstellt werden

### Automatisch (Webhook des Versandunternehmens)

**Workflow**:
1. Versandunternehmen scannt Paket (Abgang, Ankunft, Lieferung)
2. Versandunternehmen sendet Webhook an den Spwig-Webhook-Endpunkt
3. Webhook wird im WebhookLog-Table protokolliert
4. System analysiert Webhook-Payload
5. TrackingEvent wird mit extrahierten Daten erstellt
6. Kunden-E-Mail-Benachrichtigung gesendet (wenn konfiguriert)

**Vorteile**:
- Echtzeit-Updates (keine Abfragen nötig)
- Genauere Zeitstempel vom Versandunternehmen
- Vollständige Ereignishistorie automatisch verwaltet

### Manuell (Händler-Eingabe)

**Workflow**:
1. Navigieren Sie zu Versanddetail
2. Klicken Sie auf "Trackingereignis hinzufügen"
3. Wählen Sie Status aus Dropdown-Liste
4. Geben Sie Beschreibung ein
5. Optional: Geben Sie Lagedaten ein
6. Setzen Sie den Zeitstempel von occurred_at
7. Speichern

**Anwendungsfälle**:
- Versandunternehmen ohne Webhook-Unterstützung
- Manuelle Korrekturen des Versands
- Lokale Lieferung (nicht durch Versandunternehmen)
- Interne Statusaktualisierungen

---

## Anzeige-Reihenfolge der Ereignisse

Ereignisse werden in **umgekehrter chronologischer Reihenfolge** (neueste zuerst) angezeigt:

**Beispielanzeige**:
```
13. Feb 2026 10:30 AM - Geliefert (Brooklyn, NY)
13. Feb 2026 08:15 AM - Zur Auslieferung unterwegs (Brooklyn, NY)
12. Feb 2026 11:45 PM - Bei der lokalen Einrichtung angekommen (Brooklyn, NY)
12. Feb 2026 06:30 PM - Im Transport (Newark, NJ)
12. Feb 2026 02:15 PM - Von der Ursprungsort abgereist (Philadelphia, PA)
12. Feb 2026 09:00 AM - Abgeholt (Philadelphia, PA)
```

---

## Kundensichtbarkeit

Verfolgungsereignisse werden Kunden in folgenden Bereichen angezeigt:

**Bestätigungs-E-Mail**:
- Letzter Ereignisstatus
- Geschätztes Lieferdatum
- Verfolgungslink

**Kundenkonto > Bestelldetails**:
- Vollständige Ereigniszeitleiste
- Ereignisbeschreibungen
- Lagehistorie
- Zeitstempel

**Verfolgungsseite** (wenn aktiviert):
- Dedicierter Verfolgungs-URL
- Visuelle Zeitleiste
- Logo des Versandunternehmens
- Lieferkarte (wenn Lage-Daten vorhanden)

---

## Filterung von Verfolgungsereignissen

**Nützliche Filter**:
- **Versand**: Ereignisse für einen bestimmten Versand anzeigen
- **Status**: Nach Ereignistyp filtern (geliefert, in_transit, etc.)
- **Datumsbereich**: Ereignisse innerhalb eines Zeitraums
- **Lage**: Ereignisse in einer bestimmten Stadt/Bundesland

**Anwendungsfälle**:
- "Alle heute gelieferten Versände anzeigen"
- "Alle Ausnahmen der letzten Woche finden"
- "Versände verfolgen, die derzeit in_transit sind"

---

## Rohdaten (Debugging)

**Rohdatenfeld**:
- Speichert die vollständige Antwort der Versandunternehmen-API als JSON
- Nützlich für Debugging von Webhook-Problemen
- Enthält versandunternehmensspezifische Metadaten

**Beispiel für Rohdaten** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Zur Auslieferung unterwegs",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Wann Rohdaten überprüfen**:
- Ereignisbeschreibung ist unklar
- Fehlende Lage-Daten
- Webhook-Verarbeitungsfehler
- Escalation bei Unterstützung des Versandunternehmens

---

## Ereigniszeiten

**Occurred At** vs **Created At**:

**Occurred At**: Wann das Ereignis des Versandunternehmens tatsächlich stattfand
- Beispiel: Paket um 10:30 AM gescannt

**Created At**: Wann Spwig den Webhook empfangen hat
- Beispiel: Webhook um 10:32 AM empfangen (2 Minuten Verzögerung)

**Warum anders?**:
- Netzwerkverzögerung
- Batch-Verarbeitung des Versandunternehmens
- Webhook-Wiederholungsverzögerungen

**Verwenden Sie Occurred At für Kundendisplay** – genauere Darstellung des tatsächlichen Lieferfortschritts.

---

## Tipps

- **Ereignisse sind schreibgeschützt** – Nach der Erstellung können sie nicht bearbeitet werden (Audit-Integrität)
- **Überprüfen Sie Rohdaten für Details** – Mehr Informationen als die angezeigten Felder
- **Überwachen Sie Webhook-Verzögerungen** – Große Verzögerung zwischen occurred_at und created_at weisen auf Webhook-Probleme hin
- **Verwenden Sie für Kundensupport** – Ereigniszeitleiste hilft bei der Diagnose von Lieferproblemen
- **Verfolgen Sie Liefermuster** – Analysieren Sie Ereigniszeiten für Leistungsdaten des Versandunternehmens
- **Richten Sie Benachrichtigungen ein** – Automatisierte E-Mail-Benachrichtigung an Kunden bei Schlüsselereignissen (out_for_delivery, delivered)
- **Löschen Sie Ereignisse nicht** – Vollständige Audit-Trail erhalten
- **Überprüfen Sie WebhookLog auf Fehler** – Fehlende Ereignisse können auf Webhook-Verarbeitungsfehler hinweisen
- **Lagedaten variieren je nach Versandunternehmen** – Einige Versandunternehmen liefern detaillierte Lagedaten, andere nur minimal
- **Ausnahmereignisse benötigen Aufmerksamkeit** – Überwachen und folgen Sie Lieferausnahmen