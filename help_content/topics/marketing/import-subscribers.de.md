---
title: Importieren von Abonnenten aus einer CSV-Datei
---

Wenn Sie bereits eine E-Mail-Liste an anderer Stelle haben - ein altes E-Mail-Tool, eine Tabellenkalkulation mit Newsletter-Anmeldungen, ein Stapel von Messe-Name-Plaketten - müssen Sie diese Kontakte nicht einzeln in Spwig hinzufügen. Der Subscriber-Import von Campaign Studio liest eine CSV- oder Excel-Datei und fügt alle gültigen Kontakte in einem Zug Ihrer Zielgruppe hinzu, bereit, um sie zu kennzeichnen, zu segmentieren und zu e-mailen.

## Bevor Sie importieren: Einwilligung

Jeder Import erfordert, dass Sie ein Kästchen abhaken, um zu bestätigen: **"Diese Kontakte haben zugestimmt, Marketing-e-mails von mir zu erhalten."** Dies ist keine Formality - importieren Sie nur Kontakte, die tatsächlich in Ihr Marketing-e-mail eingewilligt haben. Es gibt zwei Gründe, warum es wichtig ist:

- **Es ist eine gesetzliche Vorschrift in den meisten Regionen.** Das Senden von Marketing-e-mails an Personen, die niemals zugestimmt haben, verletzt die Einwilligungsgesetze in vielen Jurisdiktionen.
- **Es schützt Ihre Zustellbarkeit.** Das E-mailen von Personen, die niemals zugestimmt haben, führt zu Spam-Beschwerden und Fehlschlägen, wodurch E-Mail-Anbieter entscheiden, ob *jede* Ihrer E-Mails - einschließlich derer an Personen, die tatsächlich zugestimmt haben - in den Posteingang gelangt.

Wenn eine Liste nicht eindeutig aus eingetragenen Anmeldungen stammt, importieren Sie sie nicht.

## Vorbereiten Ihrer Datei

Der Importierer akzeptiert eine `.csv`- oder `.xlsx`-Datei mit einer Kopfzeile. Nur eine Spalte ist erforderlich:

| Spalte | Erforderlich? | Hinweise |
|--------|-----------|-------|
| **E-Mail** | Ja | Muss eine gültige E-Mail-Adresse sein. |
| **Vorname** | Nein | Wird verwendet, um E-Mails zu personalisieren. |
| **Nachname** | Nein | Wird verwendet, um E-Mails zu personalisieren. |
| **Sprache** | Nein | Der bevorzugte Sprachcode des Abonnenten (z. B. `en`, `es`). |

Spalten werden automatisch an diese Felder gematcht, basierend auf dem Spaltennamen, sodass Sie nichts umbenennen müssen - gängige Variationen wie `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname` oder `Locale` werden alle erkannt.

Jeder Import ist mit **5 MB** und **5.000 Zeilen** begrenzt. Wenn Ihre Liste größer ist, teilen Sie sie in kleinere Dateien auf und importieren Sie sie nacheinander.

## Importieren Sie Ihre Kontakte

1. Öffnen Sie **Campaign Studio > Abonnenten** und klicken Sie auf **CSV importieren**.
2. Wählen Sie Ihre `.csv`- oder `.xlsx`-Datei.
3. Wählen Sie, was **für Kontakte, die bereits auf Ihrer Liste sind**, geschieht - siehe unten [Duplikate behandeln](#duplikate-behandeln).
4. Wählen Sie optional einen Tag unter **Tag importierte Kontakte als** aus, um alle in diesem Import zu kennzeichnen (z. B. `Event 2026`) - siehe [Abonnententags](/help/subscriber-tags) für mehr zu Tags.
5. Klicken Sie auf **Einwilligung bestätigen**.
6. Klicken Sie auf **Weiter**.

![Das Import-Upload-Formular mit einer Datei ausgewählt, einem Tag ausgewählt und Einwilligung bestätigt](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig zeigt Ihnen dann eine Vorschau an, bevor etwas importiert wird:

![Der Import-Vorschau-Bildschirm mit Zahlen für neu, bereits auf der Liste und übersprungen - ungültig mit Gründen](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Neue Kontakte** - Zeilen, die einen brandneuen Abonnenten erstellen werden.
- **Bereits auf Ihrer Liste** - Zeilen, deren E-Mail-Adresse mit einem bestehenden Abonnenten übereinstimmt.
- **Übersprungen (ungültig)** - Zeilen, die nicht gelesen werden konnten, wobei jede mit ihrer Zeilennummer und dem Grund aufgelistet wird (ungültiges E-Mail-Format, leeres E-Mail-Feld oder Duplikat einer früheren Zeile in derselben Datei).

Überprüfen Sie diese Zahlen und klicken Sie auf **Jetzt importieren**, um den Import zu bestätigen, oder auf **Abbrechen**, um ohne Änderungen zurückzutreten.

## Umgang mit Duplikaten

Eine Zeile gilt als Duplikat, wenn ihre E-Mail-Adresse mit einem Abonnenten übereinstimmt, den Sie bereits haben. Sie wählen, wie Spwig diese Zeilen im Upload-Formular behandelt:

| Option | Was passiert |
|--------|--------------|
| **Sie unverändert lassen** *(Standard)* | Der Name und die Sprache des bestehenden Abonnenten werden beibehalten. |
| **Ihr Namen / Ihre Sprache aktualisieren** | Der Vorname, Nachname und die Sprache des bestehenden Abonnenten werden aus der Datei aktualisiert (nur für die Felder, die die Datei tatsächlich bereitstellt). |

Der von Ihnen für den Import gewählte Tag wird **allen in der Datei enthaltenen** Personen zugewiesen - egal, ob neue oder bestehende Kontakte - egal, welche Duplikatoption Sie wählen.

So führt das Importieren Ihrer "VIP-Liste" mit dem **VIP**-Tag auch die Personen, die Sie bereits haben, mit diesem Tag aus.

Die Duplikat-Option steuert nur, ob der *Name und die Sprache* eines vorhandenen Kontakts überschrieben werden.

## Nach dem Import

Jeder durch einen Import erstellte Kontakt wird mit der Quelle **Import** erfasst und zum Zeitpunkt des Importlaufs als eingewilligt markiert (nicht an einem früheren Datum, an dem sie möglicherweise woanders eingewilligt haben). Ihr Vor- und Nachname – falls die Datei diese bereitgestellt hat – werden in ihrem Abonnentenrecord gespeichert. Das bedeutet, dass die `[[first_name]]`- und `[[last_name]]`-Mergfelder in Ihren Kampagnen nun auch für sie korrekt personalisiert werden, obwohl sie nie ein Spwig-Konto erstellt haben.

## Tipps

- Exportieren Sie Ihre Quellliste vor dem Hochladen in eine CSV- oder `.xlsx`-Datei mit nur einem Blatt und einer sauberen Kopfzeile – zusätzliche Blätter, zusammengeführte Zellen oder Zusammenfassungszeilen können die Spaltenzuordnung verwirren.
- Verwenden Sie **Importierte Kontakte als Taggen**, um sofort die genaue Zielgruppe zu erstellen, die Sie anschließend ansprechen möchten – siehe [Abonnenten-Tags](/help/subscriber-tags), um daraus ein Segment zu erstellen.
- Lesen Sie immer die Gründe unter **Übersprungen (ungültig)**, bevor Sie davon ausgehen, dass ein Import fehlerhaft war – eine Handvoll übersprungener Zeilen mit klaren Gründen ist für die meisten realen Listen normal.
- Das erneute Ausführen derselben Datei ist sicher: Kontakte, die Sie bereits importiert haben, werden beim zweiten Mal als Duplikate behandelt und nicht neu erstellt.
- Wenn Sie mehrere kleine Listen zusammenführen, taggen Sie jeden Import unterschiedlich (z. B. `Import: Jan Event`, `Import: Trade Show`), damit Sie sie später unterscheiden können, auch wenn sie alle in Ihre Hauptzielgruppe gemischt sind.
- Für Listen mit mehr als 5.000 Zeilen teilen Sie sie an einer offensichtlichen Grenze auf (alphabetisch, nach Quelle oder nach Erfassungsdatum), anstatt einen willkürlichen Schnitt zu wählen, damit jede Charge später leicht zu identifizieren bleibt.