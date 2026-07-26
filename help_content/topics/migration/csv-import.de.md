---
title: Importieren aus CSV-Dateien
---

CSV-Import ist der Standardweg zur Migration für jede Store, zu der Spwig nicht direkt eine Verbindung herstellt. Wenn Sie von BigCommerce, PrestaShop, Squarespace, Wix, einer von Ihnen manuell verwalteten Tabelle oder einem maßgeschneiderten System kommen, das keinen API-Standard verwendet, den Spwig versteht, dann sind Sie hier richtig – exportieren Sie Ihre Daten in CSV-Dateien und laden Sie sie hier hoch, anstatt eine Live-Verbindung herzustellen.

Dieser Leitfaden behandelt, wann Sie CSV anstelle einer API-Verbindung verwenden sollten, was dieser Weg nicht übertragen kann, die fünf beteiligten Dateien, wie Sie sie vorbereiten und wie die Spaltenzuordnung funktioniert.

## Wann CSV anstelle einer API-Verbindung verwendet werden sollte

Spwig verbindet sich direkt mit WooCommerce, Shopify und Magento 2/Adobe Commerce – siehe [Data Migration Overview](migration-overview) für diese. Für jede andere Plattform ist CSV Ihre einzige Option; es gibt keine direkte Integration für BigCommerce, PrestaShop, Squarespace oder Wix. Es ist auch die richtige Wahl, wenn Sie Daten aus einer Tabelle konsolidieren, einen selbst erstellten Store außer Dienst stellen oder genau steuern möchten, was importiert wird, indem Sie die Dateien selbst erstellen.

## Was CSV nicht kann

Bevor Sie etwas vorbereiten, wissen Sie, was dieser Weg hinterlässt – dies ist der größte Quell der Überraschung für Händler, die CSV-Import verwenden:

- **Keine Produktbilder.** Produkte werden ohne Bilder importiert; laden Sie sie danach hoch.
- **Keine Varianten.** Jedes Produkt wird als einfaches Produkt erstellt. Erstellen Sie nach dem Import die Strukturen für Größe/Farbe/Design in Spwig neu.
- **Keine Gutscheine.** Rabattcodes und Promotionen sind nicht Teil des CSV-Formats.
- **Kein Blog-Inhalt.** Es gibt keine CSV-Datei für Beiträge oder Artikel.

Nichts davon blockiert den Import – es bedeutet nur, dass Produkte nach dem Import in Spwig weitere Arbeiten benötigen. Siehe [Nach Ihrer Migration](after-migration-review) für die vollständige Nach-Import-Überprüchungsliste.

## Die fünf Dateien

Der CSV-Schritt des Assistenten bietet fünf Datei-Eingaben, jede mit einem **Download-Vorlage**-Knopf. Beginnen Sie mit diesen Vorlagen anstelle davon, Dateien von Grund auf neu zu erstellen – sie garantieren die richtigen Spaltennamen und ermöglichen, dass die automatische Erkennung in Schritt 4 mehr Arbeit leistet.

| Datei | Erforderlich? |
|---|---|
| Produkte | **Erforderlich** |
| Kategorien | Optional |
| Kunden | Optional |
| Bestellungen | Optional |
| Bewertungen | Optional |

Produkte ist die einzige Datei, die Spwig erfordert – der Rest kann leer bleiben, wenn Sie diese Daten noch nicht haben.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Schritt 2 mit CSV ausgewählt, zeigt die fünf Datei-Eingaben und ihre Download-Vorlagen-Knöpfe
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Produkte (Erforderlich)

| Spalte | Beschreibung |
|---|---|
| `id` | Eindeutige Kennung in Ihren Quelldaten; wird Kunden nicht gezeigt. |
| `name` | Der Produktname. **Wichtig.** |
| `slug` | URL-freundliche Version des Namens; wird automatisch aus `name` generiert, wenn leer. |
| `description` | Die Beschreibung, die auf dem Verkaufsstand gezeigt wird. |
| `price` | Der reguläre Preis des Produkts. **Wichtig.** |
| `sku` | Lagerhaltungseinheit – wird verwendet, um Übereinstimmungen zu ermitteln, wenn **Bestehende Artikel überspringen** aktiviert ist. |
| `stock_quantity` | Einheiten, die derzeit auf Lager sind. |
| `category` | Kategorienamen, zu der dieses Produkt gehört. Muss mit einem `name` in Ihrer Kategorien-Datei übereinstimmen. |

### Kategorien

| Spalte | Beschreibung |
|---|---|
| `id` | Eindeutige Kennung in Ihren Quelldaten. |
| `name` | Der Kategorienamen. **Wichtig.** |
| `slug` | URL-freundliche Version des Namens; wird automatisch generiert, wenn leer. |
| `description` | Kategorienbeschreibungstext. |
| `parent_id` | Die `id` der übergeordneten Kategorie. Leer bedeutet, dass es sich um eine Oberkategorie handelt. |

### Kunden

| Spalte | Beschreibung |
|---|---|
| `id` | Eindeutige Kennung in Ihren Quelldaten. |
| `email` | E-Mail-Adresse des Kunden. **Wichtig** – verknüpft Bestellungen und Bewertungen mit dem richtigen Kunden. |
| `first_name` | Vorname des Kunden. |
| `last_name` | Nachname des Kunden. |
| `phone` | Telefonnummer des Kunden. |

### Bestellungen

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Spalte | Beschreibung |
|---|---|
| `id` | Eindeutige Kennung in Ihren Quelldaten. |
| `customer_email` | E-Mail-Adresse des Kunden, der die Bestellung aufgegeben hat. **Wichtig** — verknüpft die Bestellung mit einem Kundenrekord. |
| `order_date` | Das Datum, an dem die Bestellung aufgegeben wurde. |
| `status` | Der Bestellstatus (z. B. abgeschlossen, in Bearbeitung). |
| `total` | Der Gesamtbetrag der Bestellung. **Wichtig.** |
| `currency` | Währungskode für den Gesamtbetrag der Bestellung. |

### Bewertungen (Optional)

| Spalte | Beschreibung |
|---|---|
| `id` | Eindeutige Kennung in Ihren Quelldaten. |
| `product_id` | Die `id` des bewerteten Produkts, die mit Ihrer Produktdatei übereinstimmt. **Wichtig** — verknüpft die Bewertung mit dem richtigen Produkt. |
| `customer_email` | E-Mail-Adresse des Bewertenden. |
| `rating` | Die vergebene Sternebewertung. |
| `comment` | Der Bewertungstext. |
| `date` | Das Datum, an dem die Bewertung veröffentlicht wurde. |

## Vorbereitung Ihrer Dateien

- **Speichern Sie als UTF-8**, um verfälschte Akzente zu vermeiden, insbesondere wenn die Datei aus einer anderen Kodierung stammt.
- **Zitieren Sie Felder, die Kommas enthalten** — um eine Beschreibung oder einen Namen mit einem Komma in Anführungszeichen zu setzen, damit es nicht fälschlicherweise als Spaltenabstand interpretiert wird.
- **Fügen Sie eine Kopfzeile hinzu.** Die erste Zeile muss Ihre Spaltennamen enthalten — eine Datei ohne Kopfzeile wird abgewiesen.
- **Erstellen Sie eine Kategorienhierarchie mit `parent_id`.** Geben Sie jeder Kategorie eine eindeutige `id`, und setzen Sie dann die `parent_id` einer Unterkategori auf die `id` ihrer übergeordneten Kategorie. Leer bedeutet, dass es sich um eine Oberkategorie handelt.
- **Verknüpfen Sie Bestellungen mit Kunden über `customer_email`**, die mit der `email`-Spalte in Ihrer Kundendatei übereinstimmt (oder ein Gastrekord wird erstellt), anstatt sich auf interne ID-Nummern zu verlassen, die selten übereinstimmen.
- **Verknüpfen Sie Bewertungen mit Produkten über `product_id`**, die mit einem Wert in der `id`-Spalte Ihrer Produktdatei übereinstimmt, oder die Bewertung wird übersprungen.

## Zuordnen von Spalten im Schritt 4

Schritt 4 zeigt ein Panel zur Zuordnung von CSV-Spalten an. Spwig scannt Ihre Kopfzeilen und erkennt automatisch wahrscheinliche Übereinstimmungen mit einer Liste von gängigen Aliassen — eine `sku`-Spalte entspricht beispielsweise auch `barcode`, `part_number` oder `item_number`. Kopfzeilen, die direkt aus einer anderen Plattform exportiert wurden, passen oft ohne manuelle Arbeit korrekt zu.

Für jede Spalte können Sie die automatisch erkannte Zuordnung akzeptieren, sie durch das Auswählen einer anderen Zielspalte überschreiben oder „— Diese Spalte überspringen —“ auswählen, um sie auszulassen. Die Zuordnungen werden gespeichert und bei zukünftigen CSV-Migrationen wiederverwendet. Siehe [Migration Field Mapping](migration-field-mapping), um einen vollständigen Überblick über Schritt 4 zu erhalten, einschließlich automatischer Feldzuordnungen, Kategorienzuordnungen und den Steueroptionen/Shipping-Optionen.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Step 4 CSV Column Mapping panel showing auto-detected mappings with override dropdowns
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Häufige Fehler und ihre Bedeutung

| Fehler | Bedeutung |
|---|---|
| `Products CSV is required.` | Sie haben versucht, weiterzugehen, ohne eine Produktdatei hochzuladen. Es ist die einzige Datei, die Spwig erfordert — laden Sie eine hoch, um fortzufahren. |
| `{Type} CSV has no headers.` | Die erste Zeile der genannten Datei ist leer oder fehlt. Fügen Sie eine Kopfzeile mit Spaltennamen hinzu und laden Sie sie erneut hoch. |
| `{Type} CSV could not be read: ...` | Spwig konnte die genannte Datei nicht parsen — dies geschieht in der Regel bei einer beschädigten Datei, falscher Kodierung oder einer Datei, die nicht tatsächlich CSV ist, obwohl die Dateiendung es vorgibt. Exportieren Sie sie erneut und stellen Sie sicher, dass sie sauber geöffnet werden kann, bevor Sie sie erneut hochladen. |

## Ausführung des Imports

Sobald die Zuordnung bestätigt ist, starten Sie die Migration ab Schritt 5. Sie läuft im Hintergrund ab, sodass Sie das Fenster schließen können — Fortschritt und ein Live-Protokoll sind verfügbar, wenn Sie zurückkehren, bevor die Migration abgeschlossen ist. Siehe [Nach Ihrer Migration](after-migration-review), um die Ergebnisse zu überprüfen.

Denken Sie daran, dass der CSV-Import speziell **Produktbilder** und **Varianten** für Sie verbleibt, die Sie manuell beenden müssen — weder von diesen kommen automatisch über, egal wie vollständig Ihre Dateien waren.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe.


- **Beginnen Sie mit dem Download-Template-Button für jede Datei** — dadurch sparen Sie sich das Nachsuchen nach Typos in Spaltennamen, die andernfalls beim manuellen Zuordnen durchfallen würden.
- **Beheben Sie `product_id`-Missmatches vor dem Hochladen von Bewertungen** — eine Bewertung, deren `product_id` mit keiner Produkt-`id` übereinstimmt, hat nichts, an das sie sich anhängen kann, und wird übersprungen.
- **Renennen Sie keine Header aus einer anderen Plattform-Exportdatei** — die automatische Erkennung erkennt sie oft so wie sie sind über Aliase, sodass eine manuelle Zuordnung überhaupt nicht erforderlich sein könnte.
- **Reservieren Sie Zeit für Bilder und Varianten direkt nach dem Import** — diese beiden Dinge bringt CSV nie mit, und sie sind leicht zu vergessen, bis ein Kunde auf eine leere Produktseite aufmerksam wird.
- **Verwenden Sie `parent_id`, um mehrstufige Kategorien zu modellieren** — weisen Sie die `parent_id` einer Unterkategoriens `id` ihrer übergeordneten Kategorie zu, um sie einzubetten; lassen Sie sie leer, um Kategorien auf der obersten Ebene darzustellen.
- **Erneut exportieren und erneut prüfen bei einem Fehler „konnte nicht gelesen werden“** — es handelt sich fast immer um eine Kodierung oder Korruption in der Quelldatei, nicht um etwas, das in Spwig behoben werden muss.