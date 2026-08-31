---
title: Massenaktionen für Produkte
---

Die **Produkte**-Liste ermöglicht es Ihnen, auf viele Produkte gleichzeitig zuzugreifen, anstatt jedes einzelne davon zu öffnen. Über das **Massenaktionen**-Dropdown-Menü in der Symbolleiste über dem Produkt-Raster können Sie Produkte veröffentlichen oder zurückziehen, hervorheben oder die Hervorhebung entfernen, Daten als CSV exportieren, prüfen, welche Produkte für den internationalen Versand bereit sind, oder sie löschen – alles in einem einzigen Schritt.

Navigieren Sie zu **Produkte > Alle Produkte**, um diese Aktionen zu verwenden.

![Symbolleiste der Produktliste mit drei ausgewählten Produktkarten und dem Massenaktionen-Dropdown, das alle Optionen anzeigt, einschließlich Zolldaten exportieren (CSV) und Internationale Versandbereitschaft prüfen](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Eine Massenaktion ausführen

1. Verwenden Sie bei Bedarf das Filterpanel oder das **Suche**-Feld, um die gewünschten Produkte einzugrenzen
2. Aktivieren Sie das Kästchen in der oberen linken Ecke jeder Produktkarte, die Sie einbeziehen möchten – die **Massenaktionen**-Leiste zeigt eine laufende Zählung der ausgewählten Produkte an
3. Wählen Sie eine Aktion aus dem **Massenaktionen**-Dropdown-Menü
4. Klicken Sie auf **Anwenden**

Aktionen, die Daten ändern oder exportieren, werden sofort ausgeführt; **Ausgewählte löschen** fordert Sie zunächst zur Bestätigung auf, da dies die einzige Aktion hier ist, die sich nicht leicht aus der Liste selbst rückgängig machen lässt.

## Verfügbare Aktionen

| Aktion | Beschreibung |
|--------|---------------|
| **Als veröffentlicht markieren** | Setzt den Status der ausgewählten Produkte auf Veröffentlicht, damit sie im Shop sichtbar sind. |
| **Als Entwurf markieren** | Setzt den Status der ausgewählten Produkte auf Entwurf und blendet sie im Shop aus, während Sie weiter bearbeiten. |
| **Als hervorgehoben markieren** | Aktiviert **Ist hervorgehoben** für die ausgewählten Produkte. |
| **Hervorhebung entfernen** | Deaktiviert **Ist hervorgehoben** für die ausgewählten Produkte. |
| **Als CSV exportieren** | Lädt eine CSV-Datei mit der ID, dem Namen, der SKU, dem Status, dem Hervorhebungs-Flag und dem Preis der ausgewählten Produkte herunter. |
| **Zolldaten exportieren (CSV)** | Lädt eine CSV-Datei mit Zollinformationen für die ausgewählten Produkte herunter. Siehe unten. |
| **Internationale Versandbereitschaft prüfen** | Zeigt eine Zusammenfassung der ausgewählten Produkte, die über die für internationale Sendungen erforderlichen Zolldaten verfügen. Siehe unten. |
| **Ausgewählte löschen** | Verschiebt die ausgewählten Produkte in den Papierkorb, nachdem eine Bestätigung abgefragt wurde. |

## Zolldaten exportieren (CSV)

Verwenden Sie diese Funktion, wenn Sie ein Zollanmeldungsblatt benötigen, das Sie einem Spediteur, Kurierdienst oder Zollagenten übergeben – beispielsweise vor einer großen internationalen Sendung oder bei der Einrichtung eines neuen Carriers, der vorab HS-Codes und Herkunftsdaten verlangt.

Wählen Sie die Produkte aus, wählen Sie **Zolldaten exportieren (CSV)** aus dem Dropdown-Menü und klicken Sie auf **Anwenden**. Spwig lädt eine Datei namens `product_customs_data.csv` herunter, die eine Zeile pro Produkt und folgende Spalten enthält:

| Spalte | Quelle |
|--------|--------|
| **SKU** | Die SKU des Produkts |
| **Name** | Der Produktname |
| **HS-Code** | Der Harmonisierte System-Klassifizierungscode |
| **Herkunftsland** | Der Ort, an dem das Produkt hergestellt wird |
| **Zoll-Einheitspreis** | Der für den Zoll deklarierte Wert pro Einheit |
| **Exportlizenz** | Die Exportlizenznummer, falls das Produkt eine benötigt |
| **Lizenzablauf** | Das Ablaufdatum der Exportlizenz, falls festgelegt |
| **International bereit** | `Ja` oder `Nein` – ob das Produkt über die Mindestdaten für den internationalen Versand verfügt (siehe unten) |

Diese Felder stammen aus dem Abschnitt **Internationaler Versand / Zoll** des Produktformulars. Wenn einem Produkt ein Feld fehlt, bleibt seine Spalte im Export leer – füllen Sie die fehlenden Daten im Produkt aus, bevor Sie diese Datei für eine tatsächliche Sendung verwenden.

## Internationale Versandbereitschaft prüfen

Verwenden Sie diese Funktion, um eine Charge von Produkten zu überprüfen, bevor Sie sie international versenden, ohne jedes Produkt einzeln zu öffnen oder auf einen vollständigen CSV-Export zu warten.

Wählen Sie die Produkte aus, wählen Sie **Internationale Versandbereitschaft prüfen** und klicken Sie auf **Anwenden**. Spwig prüft jedes ausgewählte Produkt anhand von drei erforderlichen Feldern – **HS-Code**, **Herkunftsland** und **Zoll-Einheitspreis** – und zeigt eine Benachrichtigung mit einer Zusammenfassung des Ergebnisses an:

- Wenn alle ausgewählten Produkte alle drei Felder ausgefüllt haben, wird eine Bestätigung angezeigt, dass alle bereit sind.
- Wenn bei einigen Daten fehlen, meldet die Benachrichtigung, wie viele bereit sind und wie viele nicht, und listet jedes Produkt auf, das nicht bereit ist, zusammen mit den fehlenden Feldern (zum Beispiel „Blaue Keramik-Tasse (fehlend: hs_code, country_of_origin)").

Wenn bei mehr als 10 Produkten Daten fehlen, listet die Benachrichtigung die ersten 10 auf und gibt an, wie viele weitere betroffen sind.

Diese Aktion liest nur Daten – sie ändert nichts an den Produkten, sodass sie so oft ausgeführt werden kann, wie gewünscht, während Sie Zollinformationen im gesamten Katalog ausfüllen.

**Export License Number** und **Export License Expiry** sind nicht Teil der Bereitheitsprüfung. Sie gelten nur für kontrollierte oder eingeschränkte Artikel, daher kann ein Produkt für den internationalen Versand „bereit“ sein, ohne diese Angaben zu haben.

## Tipps

- Führen Sie **Check International Shipping Readiness** für Ihren gesamten Katalog (oder Kategorie für Kategorie) vor Ihrer ersten internationalen Bestellung aus – es ist viel schneller, als einen fehlenden HS-Code zu entdecken, wenn eine Sendung bereits an der Grenze ist.
- Verwenden Sie **Export Customs Data (CSV)** für die Übergabe an Spediteure und Carrier und **Check International Shipping Readiness** für Ihre interne Checkliste – die CSV-Datei ist eine Aufzeichnung, die Bereitheitsprüfung ist eine To-do-Liste.
- Füllen Sie **HS Code**, **Country of Origin** und **Customs Unit Price** im Produktformular (unter **International Shipping / Customs**) aus, wenn Sie neue Produkte hinzufügen, damit Sie es später nicht in Massen erledigen müssen.
- Das Produkt-Raster lädt automatisch weitere Produkte, während Sie scrollen (unendliches Scrollen), und Ihre Checkbox-Auswahl bleibt erhalten, wenn neue Produkte geladen werden – so können Sie scrollen, um eine große Auswahl zu erstellen, bevor Sie eine Aktion anwenden. Wenn Sie jedoch einen Filter ändern oder die Seite neu laden, wird Ihre Auswahl gelöscht, daher wenden Sie die Aktion an, bevor Sie Filter anpassen.
- **Mark as Draft** ist eine schnelle Möglichkeit, mehrere Produkte gleichzeitig aus dem Storefront zu entfernen – zum Beispiel vor einer Bestandsaufnahme – ohne etwas anderes an ihnen zu ändern.