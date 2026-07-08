---
title: Loyalitätskampagnen
---

Loyalitätskampagnen ermöglichen es Ihnen, zeitlich begrenzte Promotionen und automatisierte Belohnungen durchzuführen, die über Ihre alltäglichen Erwerbsregeln hinausgehen. Nutzen Sie sie, um Doppel-Punkte-Wochenenden durchzuführen, Kunden an ihrem Geburtstag zu belohnen, inaktive Käufer zurückzugewinnen und gezielte Boni an bestimmte Gruppen von Mitgliedern zu verteilen.

Jede Kampagne definiert einen Auslöser oder einen Zeitplan, die Mitglieder, auf die sie sich bezieht, und die Aktionen, die durchgeführt werden sollen. Sobald eine Kampagne aktiv ist, wird sie automatisch ausgelöst – Sie richten sie einmal ein und Spwig kümmert sich um den Rest.

## Typen von Kampagnen

| Typ | Wann wird sie ausgelöst |
|------|---------------|
| **Auslöser-basiert** | Wenn ein bestimmtes Ereignis auftritt (z. B. ein Kauf wird getätigt, ein Geburtstag wird erkannt) |
| **Geplant** | Auf einem wiederkehrenden Zeitplan (täglich, wöchentlich, monatlich) |
| **Manuell** | Nur wenn Sie sie explizit aus dem Admin ausführen |
| **Verhaltensbasiert** | Wenn ein Kunde ein Verhaltensmuster erfüllt (z. B. Surfen ohne Kauf) |

## Eine Kampagne erstellen

Navigieren Sie zu **Promotions > Loyalitätskampagnen** und klicken Sie auf **+ Loyalitätskampagne hinzufügen**.

### Schritt 1: Grundinformationen

- **Name** – ein klarer, beschreibender Name, der nur im Admin sichtbar ist (z. B. `Geburtstagsbonus – 200 Punkte`)
- **Slug** – automatisch aus dem Namen generiert; wird intern verwendet
- **Beschreibung** – optionale Notizen über den Zweck der Kampagne
- **Kampagnetyp** – wählen Sie den Typ aus der Tabelle oben aus

### Schritt 2: Auslöser oder Zeitplan

**Für auslöserbasierte Kampagnen**, legen Sie den **Auslöser-Ereignis** fest, der die Kampagne auslöst. Verfügbare Auslöser umfassen:

| Auslöser | Beschreibung |
|---------|-------------|
| Bestellung platziert | Wird ausgelöst, wenn ein Mitglied eine Bestellung abschließt |
| Erster Kauf | Wird ausgelöst, wenn ein Mitglied seine erste Bestellung tätigt |
| Kunden-Geburtstag | Wird anlässlich des Geburtstags eines Mitglieds ausgelöst |
| Mitgliedschafts-Jahrestag | Wird jedes Jahr anlässlich des Beitritts-Jahrestags eines Mitglieds ausgelöst |
| Warenkorb verlassen | Wird ausgelöst, wenn ein Warenkorb ohne Bezahlung verlassen wird |
| Stufe-Verbesserung | Wird ausgelöst, wenn ein Mitglied in eine höhere Stufe aufsteigt |
| Punkte bald ablaufen | Wird ausgelöst, wenn ein Mitglied Punkte hat, die bald ablaufen |
| Inaktiv 90 Tage | Wird ausgelöst, wenn ein Mitglied 90 Tage lang nicht gekauft hat |
| Bewertung abgegeben | Wird ausgelöst, wenn ein Mitglied eine Produktbewertung abgibt |
| Verweis umgewandelt | Wird ausgelöst, wenn ein verwiesener Kunde einen Kauf tätigt |

Sie können **Auslöser-Bedingungen** als JSON-Objekt hinzufügen, um weiter zu filtern, wann die Kampagne ausgelöst wird. Zum Beispiel, um nur für Bestellungen über 100 $ auszulösen:

```json
{
  "min_order_amount": 100
}
```

**Für geplante Kampagnen**, legen Sie den **Zeitplan-Typ** (Täglich, Wöchentlich, Monatlich oder benutzerdefiniertes Cron) und konfigurieren Sie die Zeiteinstellungen im Feld **Zeitplan-Konfiguration**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Schritt 3: Aktionen

Das Feld **Aktionen** definiert, was geschieht, wenn die Kampagne ausgelöst wird. Geben Sie ein JSON-Array von Aktionen-Objekten ein. Die häufigste Aktion ist die Verleihung von Bonuspunkten:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Geburtstagsbonus – vielen Dank, dass Sie Mitglied sind!"
  }
]
```

Weitere verfügbare Aktionen umfassen das Senden einer E-Mail-Benachrichtigung oder das Verleihen einer Medaille. Siehe die Dokumentation Ihres Anbieterkomponenten für die vollständige Liste.

### Schritt 4: Zielgruppen

Steuern Sie mit den Zielgruppen-Feldern, welche Mitglieder von der Kampagne betroffen sind:

- **Alle Mitglieder Zielgruppe** – standardmäßig aktiviert; die Kampagne gilt für jedes aktive Loyalitätsmitglied
- **Segment Zielgruppe** – beschränken Sie die Kampagne auf Mitglieder in einem bestimmten Segment (siehe [Segmente](#managing-member-segments) unten)
- **Stufen Zielgruppe** – beschränken Sie die Kampagne auf Mitglieder in bestimmten Loyalitätsstufen

### Schritt 5: Grenzen und Abkühlzeiten

- **Maximaler Auslöser pro Mitglied** – wie oft dasselbe Mitglied von dieser Kampagne profitieren kann. Auf `1` setzen, um einmalige Boni wie einen Geburtstagsbonus zu gewährleisten. Leer lassen, um unbegrenzt zu gestalten.
- **Abkühlzeit in Tagen** – minimale Tage zwischen Auslösern der Kampagne für dasselbe Mitglied. Zum Beispiel, auf `365` setzen, um sicherzustellen, dass eine Geburtstagskampagne nicht mehr als einmal pro Jahr ausgelöst wird.

### Schritt 6: Kampagnendaten

Legen Sie **Startdatum** und **Enddatum** fest, um die Kampagne zeitlich zu begrenzen. Beide leer lassen, um eine laufende Kampagne zu erstellen.

Kampagnen können sich in einem dieser Status befinden:

| Status | Beschreibung |
|--------|-------------|
| **Entwurf** | Erstellt, aber noch nicht aktiv; sicher zum Konfigurieren und Testen |
| **Aktiv** | Wird ausgeführt und löst sich aus, wenn die Bedingungen erfüllt sind |
| **Pausiert** | Temporär gestoppt, ohne die Konfiguration zu verlieren |
| **Beendet** | Vor dem Enddatum; löst sich nicht mehr aus |
| **Archiviert** | Aus der aktiven Liste ausgeblendet, aber für die Aufzeichnungen gespeichert |

Nachdem Sie alle Felder ausgefüllt haben, klicken Sie auf **Speichern**. Ändern Sie dann den Status in **Aktiv**, um die Kampagne zu starten.

## Praktische Beispiele

### Beispiel: Doppelte Punkte am Wochenende

**Szenario:** Vergeben Sie 2x Punkte für alle Bestellungen, die während eines bestimmten Wochenendes platziert werden.

| Feld | Wert |
|-------|-------|
| Name | `Double Points Weekend — March` |
| Kampagnentyp | Trigger-basiert |
| Trigger-Event | Bestellung platziert |
| Aktionen | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Startdatum | Freitagabend |
| Enddatum | Sonntagnacht |
| Alle Mitglieder Ziel | Angekreuzt |

### Beispiel: Geburtstagsbonus

**Szenario:** Geben Sie jedem Treue-Mitglied 200 Bonuspunkte an seinem Geburtstag.

| Feld | Wert |
|-------|-------|
| Name | `Birthday Bonus` |
| Kampagnentyp | Trigger-basiert |
| Trigger-Event | Kunden-Geburtstag |
| Aktionen | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Maximaler Trigger pro Mitglied | 1 |
| Kühlschrank-Tage | 365 |
| Alle Mitglieder Ziel | Angekreuzt |

### Beispiel: Wiederherstellungskampagne

**Szenario:** Senden Sie 100 Bonuspunkte an Mitglieder, die in 90 Tagen nicht gekauft haben.

| Feld | Wert |
|-------|-------|
| Name | `90-Day Win-Back Bonus` |
| Kampagnentyp | Trigger-basiert |
| Trigger-Event | Inaktiv 90 Tage |
| Aktionen | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Maximaler Trigger pro Mitglied | 1 |
| Kühlschrank-Tage | 180 |
| Alle Mitglieder Ziel | Angekreuzt |

## Verwaltung von Mitgliedsegmenten

Segmentierung ermöglicht es Ihnen, Kampagnen an bestimmte Gruppen von Treue-Mitgliedern zu richten. Navigieren Sie zu **Promotions > Treue-Segmente**, um sie zu verwalten.

### Segmenttypen

| Typ | Beschreibung |
|------|-------------|
| **Regelbasiert** | Mitgliedschaft wird durch Regeln bestimmt (z. B. Mitglieder mit mehr als 1.000 Punkten) |
| **Dynamische Berechnung** | Mitgliedschaft wird aus Echtzeitkriterien auf Anfrage berechnet |
| **Manuelle Zuordnung** | Mitglieder werden manuell dem Segment hinzugefügt |

### Erstellen eines Segments

1. Navigieren Sie zu **Promotions > Treue-Segmente** und klicken Sie auf **+ Treue-Segment hinzufügen**
2. Füllen Sie aus:
   - **Name** — beschreibender Name (z. B. `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — automatisch generiert
   - **Kriterientyp** — wie die Mitgliedschaft bestimmt wird
   - **Kriterienkonfiguration** — JSON-Objekt, das die Mitgliedschaftsregeln definiert
3. Klicken Sie auf **Speichern**

#### Beispiel: Segment für Mitglieder mit 500+ Punkten

```json
{
  "min_available_points": 500
}
```

#### Beispiel: Segment nur für Gold-Tier-Mitglieder

```json
{
  "tier_slugs": ["gold"]
}
```

Die Spalte **Mitgliederanzahl** in der Segmentliste zeigt an, wie viele Mitglieder aktuell übereinstimmen. Klicken Sie auf ein Segment und verwenden Sie die Aktion **Mitgliederanzahl aktualisieren**, um sie neu zu berechnen, wenn sich Ihre Daten geändert haben.

## Kampagnenleistung verfolgen

### Kampagnen-Ausführungsverlauf

Navigieren Sie zu **Promotions > Kampagnen-Ausführungen**, um einen Verlauf aller Male anzuzeigen, bei denen eine Kampagne für jedes Mitglied ausgelöst wurde. Jeder Ausführungsverlauf zeigt an, welche Kampagne ausgeführt wurde, für welches Mitglied und das Ergebnis.

### Kampagnenreichweite überprüfen

Öffnen Sie jeden Kampagnenvertrag, um die **Anzahl der Auslösungen** anzuzeigen und zu sehen, wann die Kampagne zuletzt ausgelöst wurde. Dies gibt Ihnen einen schnellen Überblick darüber, wie viele Mitglieder von der Kampagne profitiert haben.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Erstellen Sie zunächst Kampagnen im **Entwurf**-Status, damit Sie alle Einstellungen überprüfen können, bevor sie online gehen
- Verwenden Sie **Max Triggers Per Member** für alle Einmalbonuss-Kampagnen (Geburtstag, erste Kauf, Registrierung), um zu verhindern, dass Kunden den Bonus mehr als einmal erhalten
- Kombinieren Sie eine **Zielgruppe** mit einer triggerbasierten Kampagne, um Schichten-exklusive Promotion zu starten – beispielsweise doppelte Punkte für Käufe nur für Gold- und Platinum-Mitglieder
- Legen Sie einen **Cooldown Days**-Wert für Win-back-Kampagnen fest, damit Mitglieder nicht bombardiert werden, wenn sie einen kleinen Kauf tätigen und dann kurz darauf wieder inaktiv werden
- Die Kampagnenliste ist Ihr bestes Werkzeug, um festzustellen, welche Promotion derzeit aktiv sind – überprüfen Sie sie vor dem Start neuer Angebote, um sicherzustellen, dass Kampagnen nicht unbeabsichtigt叠加 werden
- Archivieren Sie abgeschlossene Kampagnen anstelle von deren Löschen, damit Sie eine historische Aufzeichnung darüber haben, welche Promotion Sie durchgeführt und wann