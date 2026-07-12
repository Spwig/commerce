---
title: Massenimport von Gutschein-Code
---

Der Gutschein-Import-Assistent erlaubt es Ihnen, Hunderte von Gutschein-Codes auf einmal durch das Hochladen einer CSV- oder XLSX-Datei zu erstellen. Dies ist ideal, wenn Sie bereits gedruckte Codes, Loyalitätsprogramm-Codes aus einem Drittsystem oder einfach einen großen Kampagnenstart ohne manuelles Hinzufügen jedes Codes benötigen.

![Gutscheinliste mit Import-Button](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Import starten

Navigieren Sie zu **Marketing > Gutscheine** und klicken Sie auf den **Import**-Button in der oberen rechten Ecke der Seite. Dies öffnet den dreistufigen Import-Assistenten.

## Schritt 1: Datei hochladen und Batch-Einstellungen festlegen

![Import-Upload-Formular](/static/core/admin/img/help/voucher-import/import-upload.webp)

Die erste Seite besteht aus zwei Teilen: dem Dateiupload und den Batch-Rabatteinstellungen.

### Ihre Datei vorbereiten

Laden Sie eine `.csv`- oder `.xlsx`-Datei mit einer maximalen Größe von 5 MB hoch. Die Datei muss eine Kopfzeile als erste Zeile enthalten. Die Mindestanforderung ist eine einzelne Spalte, die die Gutschein-Codes enthält – alle anderen Spalten sind optional.

Der Importer erkennt automatisch gängige Spaltennamen. Wenn Ihre Datei einen der unten genannten Namen verwendet, wählt Spwig auf der nächsten Seite automatisch die richtige Zuordnung aus, ohne zusätzliche Klicks:

| Ihr Spaltenname | Zuordnung |
|----------------|---------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Gutschein-Code |
| `name`, `title`, `campaign` | Interner Name |
| `description`, `details`, `note` | Kundenfreundliche Beschreibung |
| `external_id`, `member_id`, `reference` | Externe ID |

**Tipp:** Laden Sie zunächst das XLSX-Vorlagen-Datei herunter (siehe [Gutscheine als Vorlage exportieren](#exporting-vouchers-as-a-template) unten) – es verwendet die genauen Spaltennamen, die der Importer erwartet, sodass die Spaltenzuordnung automatisch erfolgt.

### Dateigrößenbeschränkungen

- Maximale Dateigröße: **5 MB**
- Maximale Zeilen pro Import: **5.000 Codes**

### Batch-Rabatteinstellungen festlegen

Jeder Gutschein im Batch teilt sich die gleichen Rabatteinstellungen, die Sie auf dieser Seite konfigurieren. Füllen Sie die Felder aus, wie Sie es bei der Erstellung eines einzelnen Gutscheins tun würden:

**Rabattabschnitt**

| Feld | Beschreibung |
|-------|-------------|
| **Rabatttyp** | Prozentsatz, Fixbetrag oder Versandkostenfrei |
| **Rabattwert** | Der Prozentsatz (0–100) oder der Fixbetrag, der abgezogen wird |
| **Maximaler Rabattbetrag** | Optionaler Obergrenze für Prozentsatz-Rabatte (z. B. 20 % Rabatt auf 50 $ begrenzen) |
| **Anwendungsbereich** | Gesamter Warenkorb, bestimmte Produkte oder bestimmte Kategorien |

**Gültigkeitsabschnitt**

| Feld | Beschreibung |
|-------|-------------|
| **Startdatum** | Wann die Codes aktiv werden (Standard ist jetzt, wenn leer gelassen) |
| **Enddatum** | Wann die Codes ablaufen (leer lassen, um keine Ablaufdatum festzulegen) |
| **Gültigkeit in Tagen** | Alternative zum Enddatum – Codes laufen nach dieser Anzahl von Tagen nach der Erstellung ab |

**Nutzungsgrenzenabschnitt**

| Feld | Beschreibung |
|-------|-------------|
| **Maximaler Gesamtnutzung** | Gesamtzahl der Abredemöglichkeiten für alle Kunden (leer = unbegrenzt) |
| **Maximaler Nutzungspro-Kunde** | Wie oft ein Kunde einen Code aus diesem Batch verwenden kann |
| **Mindestbestellwert** | Mindestbestellwert, der erforderlich ist, bevor der Code angewendet wird |

**Einschränkungen**

Markieren Sie eine beliebige Kombination von:
- **Nicht auf Verkaufsartikel anwendbar** – verhindert, dass der Code mit bereits vergünstigten Produkten kombiniert wird
- **Kann nicht mit anderen Gutscheinen kombiniert werden** – verhindert, dass Kunden zwei Codes für denselben Auftrag verwenden
- **Kann nicht mit Verkaufsartikeln kombiniert werden** – ähnlich wie oben, aber auf Verkaufspreis-Artikel ausgerichtet
- **Nur für Neukunden** – beschränkt den Code auf Kunden, die noch keine abgeschlossenen Bestellungen haben
- **Sofort aktivieren** – lassen Sie dies aktiviert, um die Codes sofort nach dem Import zu aktivieren

Wenn Sie mit den Einstellungen zufrieden sind, klicken Sie auf **Weiter zur Vorschau**.

## Schritt 2: Spalten zuordnen und überprüfen

![Spaltenzuordnung und Vorschauseite](/static/core/admin/img/help/voucher-import/import-preview.webp)

Die Vorschau-Seite zeigt vier Zusammenfassungszähler oben an:


- **Zeilen analysiert** — Gesamtzahl der Datensätze in Ihrer Datei

- **Wird importiert** — neue Codes, die erstellt werden

- **Duplikate** — Codes, die bereits in Ihrem Katalog vorhanden sind

- **Wird übersprungen (ungültig)** — Zeilen, die aufgrund von Validierungsfehlern abgelehnt wurden (leerer Code, Code zu lang usw.)

### Spaltenzuordnung

Die **Spaltenzuordnung**-Tabelle ermöglicht es Ihnen, Spwig mitzuteilen, welche Spalte in Ihrer Datei jeweils einem Gutscheinfeld entspricht. Spwig erkennt automatisch gängige Spaltenüberschriften (siehe die Tabelle oben), doch Sie können jede Zuordnung mithilfe des Dropdown-Menüs in jeder Zeile ändern.

Nur die Spalte **Gutschein-Code** ist erforderlich. Die anderen Felder — **Interne Bezeichnung**, **Kundenfreundliche Beschreibung** und **Externe ID** — sind optional. Wenn Sie sie überspringen, verwendet Spwig sinnvolle Standardwerte (die interne Bezeichnung lautet standardmäßig "Importierter Gutschein {code}").

### Duplikat-Code-Strategie

Wenn sich in Ihrer Datei bereits Codes in Ihrem Katalog befinden, müssen Sie entscheiden, wie Sie sie behandeln möchten:

| Strategie | Was passiert |

|----------|-------------|

| **Duplikate überspringen** | Bestehende Codes bleiben genau so, wie sie sind. Nur neue Codes werden erstellt. |

| **Einstellungen überschreiben** | Bestehende Codes werden mit den Rabatt-Einstellungen dieser Charge aktualisiert. Ihre Codes, Nutzungszähler und Erstellt-Daten bleiben erhalten. |

| **Import fehlschlagen** | Der gesamte Import wird abgebrochen, wenn auch nur ein Duplikat gefunden wird. Verwenden Sie dies, wenn Sie sicherstellen möchten, dass keine bestehenden Codes beeinflusst werden. |

Alle gefundenen Duplikate werden in einem erweiterbaren Panel aufgelistet, damit Sie sie vor der Entscheidung überprüfen können.

### Datenvorschau-Tabelle

Der untere Teil der Seite zeigt die ersten 20 Zeilen Ihrer Datei an, damit Sie sicherstellen können, dass die Spaltenzuordnung korrekt aussieht, bevor Sie den Import bestätigen. Zeilen, die mit bestehenden Codes übereinstimmen, sind hervorgehoben.

Wenn alles korrekt aussieht, klicken Sie auf **N Gutscheine importieren**, um die Charge zu bestätigen.

## Schritt 3: Ergebnis überprüfen

![Import-Ergebnisseite](/static/core/admin/img/help/voucher-import/import-result.webp)

Nachdem der Import abgeschlossen ist, sehen Sie eine Zusammenfassung, die Folgendes anzeigt:

- **Importiert** — Codes, die erfolgreich erstellt wurden

- **Übersprungen** — Codes, die nicht erstellt wurden (Duplikate oder ungültige Zeilen)

- **Zeilen verarbeitet** — Gesamtzahl der Zeilen aus Ihrer Datei, die bewertet wurden

- **Fehlgeschlagen** — Zeilen, die auf einen unerwarteten Fehler stießen

Klicken Sie auf **Importierte Gutscheine ansehen**, um die Gutscheinliste zu öffnen, gefiltert auf nur die Codes aus dieser Charge, wodurch es einfach ist, das Ergebnis zu überprüfen oder die neuen Codes in Bulk zu aktivieren.

Wenn etwas falsch aussieht — beispielsweise wurde der falsche Rabatttyp angewendet — können Sie die Strategie **Einstellungen überschreiben** bei einem erneuten Import verwenden, um die Charge zu korrigieren, ohne die Codes löschen und erneut erstellen zu müssen.

Klicken Sie auf **Eine weitere Charge importieren**, um einen neuen Upload zu starten, oder auf **Zurück zur Gutscheinliste**, um zu Ihrem vollständigen Katalog zurückzukehren.

## Gutscheine als Vorlage exportieren

Die Gutscheinliste unterstützt eine Export-Aktion in XLSX-Format, die eine Datei in exakt derselben Spaltenreihenfolge erzeugt, wie sie der Importer erwartet. Dies ist der einfachste Weg, um eine korrekt formatierte Vorlage zu erhalten:

1. Navigieren Sie zu **Marketing > Gutscheine**

2. Wählen Sie die Gutscheine aus, die Sie exportieren möchten (oder wählen Sie alle aus)

3. Wählen Sie **Ausgewählte Gutscheine in XLSX exportieren** aus dem **Aktion**-Dropdown-Menü aus

4. Klicken Sie auf **Weiter**

Die heruntergeladene Datei enthält alle 21 Spalten, die der Importer versteht, einschließlich Felder, die auf Charge-Ebene im Import-Assistenten sind (Rabatttyp, Daten, Nutzungsgrenzen usw.). Sie können diese Datei als Referenz verwenden oder Ihre bestehenden Codes mithilfe der Strategie **Einstellungen überschreiben** durch einen Bearbeitungs-→-Neuimport-Zyklus senden.

## Tipps

Alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Laden Sie zunächst eine XLSX-Exportdatei herunter, um sie als Vorlage zu verwenden — die Spaltennamen sind vorgefertigt, sodass das automatische Zuordnen sie ohne Anpassungen auf der Vorschauseite erkennt.
- Führen Sie zunächst einen kleinen Test mit 5–10 Codes durch, bevor Sie Hunderte importieren, um sicherzustellen, dass Ihre Spaltenzuordnung und Batch-Einstellungen korrekt sind.
- Verwenden Sie **Days valid** anstelle eines festen **End dates**, wenn die Codes über die Zeit verteilt werden — die Ablaufzeit jedes Codes beginnt dann mit dem Importdatum und nicht mit einem einzelnen Kalendertag.
- Wenn Sie Codes von einem Drittanbieter-Loyalitätsystem erhalten, ordnen Sie die Mitglieds- oder Kundennr. des Lieferanten der Spalte **External ID** zu, damit Sie später die Gutscheinausredemungen abgleichen können.
- Nach einem großen Import klicken Sie auf **View imported vouchers** auf der Ergebnisseite, um die Liste auf nur den neuen Batch zu filtern — Sie können diese dann in Gruppen bearbeiten, aktivieren oder deaktivieren.
- Ein fehlgeschlagener Import (mit der **Fail**-Duplikat-Strategie) verändert Ihr Katalog nicht, daher ist es sicher, die Datei zu korrigieren und so oft wie nötig erneut zu versuchen.