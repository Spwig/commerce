---
title: E-Mail-Vorlagen
---

E-Mail-Vorlagen steuern das Design und den Inhalt jeder automatisierten E-Mail, die Ihr Geschäft an Kunden und an Sie selbst sendet – Bestätigungen, Versandupdates, Passwortzurücksetzungen, Rückerstattungsnachrichten und vieles mehr. Das Bearbeiten einer Vorlage ändert alle zukünftigen E-Mails dieses Typs; bereits im Ausgangsordner befindliche E-Mails werden nicht beeinflusst.

Navigieren Sie zu **E-Mail-System > E-Mail-Vorlagen**, um Ihre Vorlagen anzuzeigen und zu verwalten.

![Liste der E-Mail-Vorlagen](/static/core/admin/img/help/email-templates/templates-list.webp)

## Vorlagentypen

Ihr Geschäft umfasst Vorlagen für eine Vielzahl von Ereignissen. Sie sind nach Kategorie gruppiert:

### Kundenseitige Bestell-E-Mails
| Vorlage | Wird gesendet, wenn |
|----------|-----------|
| Bestellbestätigung | Ein Kunde vervollständigt einen Kauf |
| Zahlungsbestätigung | Eine Zahlung wird erfolgreich verarbeitet |
| Bestellung versandt | Eine Bestellung wird als versandt markiert |
| Versandbestätigung | Eine Versandverfolgungsnummer wird hinzugefügt |
| Lieferbestätigung | Eine Bestellung wird als geliefert markiert |
| Bestellung storniert | Eine Bestellung wird storniert |
| Verspätungsbenachrichtigung | Eine Verspätung wird für eine Bestellung aufgezeichnet |
| Rückerstattungsbenachrichtigung | Eine Rückerstattung wird ausgestellt |

### Konto-E-Mails
| Vorlage | Wird gesendet, wenn |
|----------|-----------|
| Willkommens-E-Mail | Ein Kunde erstellt ein Konto |
| Konto-Einladung | Sie laden einen Kunden dazu ein, ein Konto zu erstellen |
| E-Mail-Verifikation | Ein Kunde verifiziert seine E-Mail-Adresse |
| Passwortzurücksetzung | Ein Kunde beantragt ein Passwortzurücksetzen |

### Rückgaben
| Vorlage | Wird gesendet, wenn |
|----------|-----------|
| Rückgaben: Antrag erhalten | Ein Kunde sendet einen Rückgabeantrag |
| Rückgaben: Genehmigt | Ein Rückgabeantrag wird genehmigt |
| Rückgaben: Abgelehnt | Ein Rückgabeantrag wird abgelehnt |
| Rückgaben: Paket erhalten | Das zurückgegebene Produkt kommt an Ihrem Standort an |
| Rückgaben: Rückerstattung verarbeitet | Die Rückerstattung für eine Rückgabe wird ausgestellt |

### Admin-Benachrichtigungen (an Sie gesendet)
| Vorlage | Wird gesendet, wenn |
|----------|-----------|
| Admin: Neue Bestellung | Eine neue Bestellung wird aufgegeben |
| Admin: Zahlung fehlgeschlagen | Ein Zahlungsversuch schlägt fehl |
| Admin: Täglicher Umsatzbericht | Der tägliche Umsatzzusammenfassung wird generiert |
| Admin: Lagerwarnung | Ein Produkt fällt unter den Lagerthreshold |
| Admin: Wöchentliche Zusammenfassung | Die wöchentliche Geschäftszusammenfassung wird generiert |

Zusätzliche Vorlagen umfassen Meilensteine der Versandverfolgung, Aktivitäten im Partnerprogramm, Buchungsbestätigungen (wenn das Buchungsfeature aktiviert ist) und Ereignisse im Treueprogramm.

## Eine Vorlage bearbeiten

1. Navigieren Sie zu **E-Mail-System > E-Mail-Vorlagen**
2. Finden Sie die Vorlage, die Sie bearbeiten möchten. Sie können nach **Vorlagentyp**, **Sprache** oder **Status** mit den Filtern auf der rechten Seite filtern
3. Klicken Sie auf die Vorlage, um sie zu öffnen
4. Bearbeiten Sie die **Betreffzeile** (den E-Mail-Betreff, der im Kundenposteingang angezeigt wird)
5. Bearbeiten Sie den **HTML-Inhalt** für die vollständige Designversion der E-Mail
6. Bearbeiten Sie optional den **Textinhalt** – eine Textalternative für E-Mail-Clients, die HTML nicht unterstützen
7. Klicken Sie auf **Speichern**

> **HTML-E-Mails:** Das Feld für den HTML-Inhalt akzeptiert Standard-HTML, einschließlich eingebetteter CSS. Spwig rendert dies in eine ordnungsgemäß formatierte E-Mail. Wenn Sie MJML-Markup verwenden, wird es beim Speichern automatisch kompiliert.

## Eine Vorlage vorab ansehen

Bevor Sie eine Vorlage speichern, können Sie sehen, wie sie in einem E-Mail-Client aussehen wird:

1. Öffnen Sie die Vorlage, die Sie vorab ansehen möchten
2. Klicken Sie auf die **Vorschau**-Schaltfläche (sichtbar in der Vorlagenliste oder auf der Detailseite der Vorlage)
3. Eine Vorschau wird in einem neuen Browser-Tab geöffnet, die die gerenderte E-Mail anzeigt

Dies ermöglicht es Ihnen, Layout, Formatierung und Erscheinungsbild der Platzhaltervariablen zu überprüfen, bevor die Vorlage aktiv wird.

## Vorlagenvariablen

Variablen sind Platzhalter in Ihrer Vorlage, die Spwig durch echte Daten ersetzt, wenn die E-Mail gesendet wird. Sie werden als `{{ variable_name }}` geschrieben.

Gängige Variablen, die in den meisten Vorlagen verfügbar sind:

| Variable | Wird ersetzt durch |
|----------|---------------|
| `{{ customer_name }}` | Der vollständige Name des Kunden |
| `{{ order_number }}` | Die Bestellreferenznummer |
| `{{ order_total }}` | Der Gesamtbetrag der Bestellung |
| `{{ store_name }}` | Der Name Ihres Geschäfts |
| `{{ store_url }}` | Die Webadresse Ihres Geschäfts |
| `{{ tracking_number }}` | Die Sendungsverfolgungsnummer |
| `{{ tracking_url }}` | Ein klickbarer Link zur Sendungsverfolgung |

Die genauen Variablen, die verfügbar sind, hängen vom Template-Typ ab. Variablen, die für ein bestellbezogenes Template (wie `{{ order_number }}`) relevant sind, sind in einem Konto-Template (wie Passwort zurücksetzen) nicht verfügbar. Wenn Sie eine Variable einfügen, die nicht zutrifft, wird sie leer oder unersetzt angezeigt.

## Sprachunterstützung

Jeder Template-Typ kann eine Version für jede Sprache haben, die Ihr Geschäft unterstützt. Das Feld **Sprache** auf jedem Template bestimmt, welche Sprachversion aktiv ist.

Spwig wählt automatisch die richtige Sprachversion basierend auf der Sprachpräferenz des Kunden beim Versenden. Wenn kein Template für die Sprache des Kunden vorhanden ist, greift Spwig auf die englische Version zurück.

Um ein Template für eine neue Sprache hinzuzufügen:
1. Öffnen Sie ein vorhandenes Template
2. Klicken Sie auf **Vorlage klonen** im Menü **Aktionen**
3. Legen Sie den **Sprachcode** auf der Kopie auf die neue Sprache fest
4. Übersetzen Sie den Inhalt
5. Aktivieren Sie die geklonte Vorlage

## Klonen, Aktivieren und Deaktivieren von Templates

### Ein Template klonen

Das Klonen erstellt eine exakte Kopie eines Templates – nützlich, um Sprachvarianten zu erstellen oder verschiedene Versionen zu testen, ohne die Live-Vorlage zu beeinflussen.

1. Wählen Sie ein oder mehrere Templates aus der Liste aus
2. Wählen Sie **Ausgewählte Templates klonen** aus dem Dropdown-Menü **Aktionen** aus
3. Der Klon wird als inaktiv erstellt – bearbeiten Sie ihn und aktivieren Sie ihn, sobald Sie bereit sind

### Aktivieren und Deaktivieren von Templates

Ein Template muss **aktiv** sein, um für das Versenden verwendet zu werden. Nur ein aktives Template pro Typ und Sprachkombination wird gleichzeitig verwendet.

Um in Bulk zu aktivieren oder deaktivieren:
1. Wählen Sie die Templates aus
2. Wählen Sie **Ausgewählte Templates aktivieren** oder **Ausgewählte Templates deaktivieren** aus dem Dropdown-Menü **Aktionen** aus

Oder öffnen Sie ein einzelnes Template und schalten Sie das **Aktiv**-Kästchen um.

## Systemvorlagen

Vorlagen, die mit einem **System**-Badge markiert sind, sind die Standardvorlagen, die von Spwig bereitgestellt werden. Sie können nicht gelöscht werden. Sie können sie direkt bearbeiten oder sie klonen, um eine benutzerdefinierte Version zu erstellen.

## Tipps

- Vorsicht: Previewen Sie immer ein Template nach der Bearbeitung, um Formatierungsprobleme zu erkennen, bevor Kunden sie sehen
- Halten Sie Betreffzeilen kurz und präzise – `Ihre Bestellung #10045 ist versandt` ist besser als generische Betreffzeilen wie `Update von unserem Geschäft`
- Bearbeiten Sie auch den reinen Textinhalt – einige E-Mail-Clients zeigen nur die reinen Textversionen an, und einige Kunden bevorzugen diese
- Klonen Sie die englische Version eines Templates als Ausgangspunkt, bevor Sie eine übersetzte Version erstellen
- Wenn Sie eine Änderung testen möchten, ohne die Live-E-Mails zu beeinflussen, klonen Sie das Template, bearbeiten Sie die Kopie und lassen Sie beide aktiv, während Sie die Vorschau überprüfen – deaktivieren Sie dann die ursprüngliche Vorlage
- Admin-Benachrichtigungsvorlagen (wie **Admin: Neue Bestellung**) werden an Ihre Geschäfts-Admin-E-Mail-Adresse gesendet – stellen Sie sicher, dass diese E-Mail-Adresse in Ihren Geschäftseinstellungen korrekt ist