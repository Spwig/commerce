---
title: Buchbare Produkte
---

Buchbare Produkte ermöglichen es Kunden, bei der Bestellung einen spezifischen Termin zu reservieren. Dies unterstützt Termine, Vermietungen, Kurse, Veranstaltungen und Buchungen von Unterkünften – alles direkt über die Spwig-Verwaltung.

## Buchungstypen

| Typ | Bestens geeignet für |
|------|----------|
| **Termin** | Dienstleistungen: Beratungen, Frisuren, persönliches Training |
| **Vermietung** | Geräteverleih, Fahrzeugverleih, Zimmerverleih |
| **Kurs / Workshop** | Gruppensitzungen mit einer festen Kapazität |
| **Unterkunft** | Mehrere Übernachtungen mit Check-in/Check-out-Zeiten |
| **Veranstaltung** | Einmalige oder wiederkehrende Veranstaltungen mit Eintrittskarten |

## Ein buchbares Produkt einrichten

### Schritt 1: Produkt erstellen

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt hinzufügen**
2. Wählen Sie **Produkttyp** auf **Buchungsprodukt**
3. Füllen Sie die Standardproduktfelder aus (Name, Beschreibung, Preis)
4. Speichern Sie das Produkt

### Schritt 2: Buchungseinstellungen konfigurieren

Nach dem Speichern erscheint eine **Buchungskonfiguration**-Sektion auf dem Produktbearbeitungsformular. Füllen Sie die Buchungseinstellungen aus:

#### Buchungstyp und Dauer

- **Buchungstyp** — Wählen Sie den Typ aus, der am besten zu Ihrem Dienstleistung passt (Termin, Vermietung, Kurs usw.)
- **Dauerart** — Wählen Sie **Feste Dauer** für Sitzungen mit fester Länge oder **Kunde wählt Dauer**, um Kunden zu ermöglichen, die Dauer selbst zu wählen
- **Dauer** und **Dauer-Einheit** — Legen Sie die Länge fest (z. B. `60` Minuten, `1` Stunde, `2` Tage)
- **Min/Max-Dauer** — Wenn Kunden die Dauer selbst wählen können, legen Sie den zulässigen Bereich fest

#### Pufferzeit

Pufferzeit wird automatisch zwischen Buchungen hinzugefügt, um Vorbereitungs- oder Reinigungszeit zu ermöglichen:
- **Puffer vor** — Minuten, die vor der Buchung reserviert werden
- **Puffer nach** — Minuten, die nach der Buchung reserviert werden

Ein Beispiel: Ein 60-minütiger Massagetermin mit 15 Minuten Pufferzeit nach der Buchung gibt 15 Minuten, um sich auf den nächsten Kunden vorzubereiten.

#### Vorausbuchungsfenster

- **Mindestens Vorausmeldung** — Wie weit im Voraus ein Kunde buchen muss (z. B. `24 Stunden`, um Buchungen am selben Tag zu verbieten)
- **Maximaler Vorausbuchungsbereich** — Wie weit in die Zukunft Kunden buchen können (z. B. `365 Tage`)

#### Kapazität

- **Maximale Buchungen pro Slot** — Für Kurse und Veranstaltungen legen Sie fest, wie viele Kunden den gleichen Zeitraum buchen können. Auf `1` setzen, um private Termine zu ermöglichen.

#### Bestätigung

- **Manuelle Bestätigung erforderlich** — Wenn aktiviert, werden Buchungen nicht automatisch bestätigt. Sie müssen jede Buchung manuell aus der Buchungsliste genehmigen. Nützlich, wenn Sie Kunden vor der Bestätigung prüfen möchten.

#### Stornierungsrichtlinie

- **Stornierung erlaubt** — Ob Kunden ihre Buchung stornieren können
- **Stornierungsfrist** — Wie viele Stunden/Tagen vor der Buchung Kunden stornieren können (z. B. `24 Stunden`)

#### Kalenderansicht

Wie Kunden auf der Produktseite ihren Termin und ihre Uhrzeit auswählen:

| Anzeigemodus | Bestens geeignet für |
|-------------|----------|
| **Kalenderansicht** | Allgemeiner Gebrauch – voller monatlicher Kalender |
| **Datumswähler** | Einfache Auswahl eines einzigen Datums |
| **Verfügbare Datumsauswahl** | Produkte mit begrenzten Verfügbarkeitszeitslots |
| **Datumsspannenwähler** | Unterkünfte und mehrere Tage Vermietung |

#### Kautionen

Um eine Kaution anstelle einer vollständigen Zahlung beim Checkout zu verlangen:
1. Aktivieren Sie **Kaution aktiviert**
2. Wählen Sie **Kautionstyp** auf **Fester Betrag** oder **Prozent des Gesamtbetrags**
3. Geben Sie den **Kautionsbetrag** ein (z. B. `50` für 50 $, oder `25` für 25 %)

#### Spezifische Einstellungen für Unterkünfte

Für Buchungen von Unterkünften erscheinen zusätzliche Felder:
- **Check-in-Zeit** und **Check-out-Zeit** — Standardzeiten für die Unterkunft
- **Standardbelegung** — Standardanzahl der Gäste, die in den Grundpreis einbezogen sind

### Schritt 3: Buchungsressourcen hinzufügen (optional)

Ressourcen sind die physischen Gegenstände oder Mitarbeiter, die einer Buchung zugewiesen werden – z. B. „Zimmer 1“, „Platz A“ oder „Lehrer Sam“.

1. Auf dem Produktbearbeitungsformular navigieren Sie zur **Buchungsressourcen**-Sektion
2. Klicken Sie auf **Ressource hinzufügen**
3. Geben Sie der Ressource einen **Namen** und legen Sie ihre **Kapazität** fest (wie viele Buchungen sie gleichzeitig verarbeiten kann)
4. Fügen Sie optional Ressourcenbilder hinzu

Ressourcen ermöglichen es Ihnen, die Verfügbarkeit pro einzelner Ressource oder Mitarbeiter zu verfolgen, nicht nur pro Zeitfenster.

### Schritt 4: Verfügbarkeitsregeln festlegen

Verfügbarkeitsregeln definieren, wann Buchungen vorgenommen werden können:

1. Unter dem **Verfügbarkeits**-Abschnitt des Produkts auf **Verfügbarkeitsregel hinzufügen** klicken
2. Wählen Sie die **Ressource** aus, zu der diese Regel gilt
3. Wählen Sie die **Wochentage**, an denen Buchungen möglich sind
4. Legen Sie **Startzeit** und **Endzeit** für das verfügbare Zeitfenster fest
5. Optional können Sie einen Datumsbereich (**Gültig ab** / **Gültig bis**) für die Saisonverfügbarkeit festlegen
6. Speichern

## Buchungen ansehen und verwalten

### Buchungsliste

Navigieren Sie zu **Katalog > Buchungen**, um alle Buchungen anzuzeigen. Sie können nach folgenden Kriterien filtern:
- Status (In Bearbeitung, Bestätigt, Storniert, Abgeschlossen, Nicht erschienen)
- Produkt
- Datumsbereich

### Buchungsstatusse

| Status | Bedeutung |
|--------|---------|
| **In Bearbeitung** | Warte auf manuelle Bestätigung (wenn Bestätigung erforderlich ist) |
| **Bestätigt** | Die Buchung ist bestätigt und aktiv |
| **Storniert** | Die Buchung wurde vom Kunden oder Ihnen storniert |
| **Abgeschlossen** | Der Buchungstag ist vorbei und die Buchung wurde erfüllt |
| **Nicht erschienen** | Der Kunde ist nicht erschienen |

### Eine in Bearbeitung befindliche Buchung bestätigen

1. Öffnen Sie die Buchung über **Katalog > Buchungen**
2. Ändern Sie den **Status** in **Bestätigt**
3. Speichern — der Kunde erhält automatisch eine Bestätigungs-E-Mail

### Eine Buchung stornieren

1. Öffnen Sie die Buchung
2. Ändern Sie den **Status** in **Storniert**
3. Geben Sie einen **Stornierungsgrund** an (wird dem Kunden per E-Mail angezeigt)
4. Speichern

## Warteliste verwalten

Wenn ein Zeitfenster voll ist, können Kunden sich selbst in die Warteliste aufnehmen. Spwig informiert warteliste-Kunden automatisch, wenn eine Stornierung einen Platz freigibt.

### Warteliste ansehen

Navigieren Sie zu **Katalog > Buchungswarteliste**, um alle Einträge der Warteliste anzuzeigen. Jeder Eintrag zeigt an:
- Kundenname und E-Mail-Adresse
- Das Produkt und das gewünschte Datum
- Status: **Warte**, **Benachrichtigt**, **In Buchung umgewandelt** oder **Abgelaufen**

### Wartelistenstatusse

| Status | Bedeutung |
|--------|---------|
| **Warte** | Der Kunde wartet in der Schlange, der Platz ist noch nicht verfügbar |
| **Benachrichtigt** | Der Kunde wurde per E-Mail über einen verfügbaren Platz informiert |
| **In Buchung umgewandelt** | Der Kunde hat den Platz genommen und eine Buchung abgeschlossen |
| **Abgelaufen** | Der gewünschte Tag ist vorbei, ohne dass ein Platz verfügbar wurde |

### Einen warteliste-Kunden manuell benachrichtigen

Wenn Sie einen bestimmten warteliste-Kunden vor der automatischen Benachrichtigung kontaktieren möchten:
1. Öffnen Sie den Eintrag der Warteliste
2. Kopieren Sie ihre E-Mail-Adresse und kontaktieren Sie sie direkt
3. Sobald sie eine Buchung abschließen, wird der Status ihres Warteliste-Eintrags auf **In Buchung umgewandelt** aktualisiert

## Tipps

- Aktivieren Sie manuelle Bestätigung für hochwertige Buchungen (z. B. Fototerminen, private Veranstaltungen), damit Sie die Verfügbarkeit prüfen und Anforderungen abgleichen können, bevor Sie sich verpflichten.
- Legen Sie zuerst großzügig Pufferzeit fest — Sie können diese immer reduzieren, sobald Sie die tatsächlichen Umstellungszeiten kennen.
- Für Gruppenkurse legen Sie **Maximale Buchungen pro Slot** auf die Kapazität des Kurses fest und aktivieren Sie die Warteliste, damit beliebte Sitzungen automatisch eine Schlange bilden.
- Verwenden Sie den Datumsbereichs-Selektor im Anzeigemodus für Unterkunftprodukte — Kunden erwarten, dass sie den Check-in- und Check-out-Tag gemeinsam auswählen können.
- Legen Sie eine Mindestvorankündigung fest, um letzte-Minuten-Buchungen zu verhindern, wenn Sie Vorbereitungszeit benötigen (z. B. 48-Stunden-Mindestvorankündigung für maßgeschneiderte Catering-Bestellungen).
- Prüfen Sie Ihre Warteliste regelmäßig während der Hochsaison — manuelle Kontaktaufnahme mit warteliste-Kunden kann Stornierungen schneller füllen als die automatische Benachrichtigung.