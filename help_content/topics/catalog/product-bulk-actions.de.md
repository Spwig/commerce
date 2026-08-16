---
title: Massenaktionen für Produkte
---

Die **Produktliste** ermöglicht es, mehrere Produkte gleichzeitig zu bearbeiten, anstatt jedes einzelne Produkt separat zu öffnen. Aus dem **Massenaktionen**-Dropdown im Menü oberhalb des Produktgitterfelds können Sie Produkte veröffentlichen oder nicht veröffentlichen, sie als Markenprodukte kennzeichnen oder entkennzeichnen, Daten in CSV exportieren, prüfen, ob die Produkte für den internationalen Versand bereit sind, oder sie löschen — alles in einem Schritt.

Gehen Sie zu **Produkte > Alle Produkte**, um diese Aktionen zu verwenden.

![Die Produktlistenleiste mit drei ausgewählten Produktkarten und dem Massenaktionen-Dropdown, der alle Optionen anzeigt, einschließlich Export der Zollinformationen (CSV) und Prüfung der Bereitschaft für den internationalen Versand](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Ausführen einer Massenaktion

1. Verwenden Sie das Filterpanel oder das **Suchfeld**, um die gewünschten Produkte einzugrenzen, falls erforderlich
2. Klicken Sie auf das Kontrollkästchen in der oberen linken Ecke jedes Produktcards, das Sie einbeziehen möchten — die **Massenaktionen**-Leiste zeigt eine laufende Zählung an, wie viele Produkte ausgewählt wurden
3. Wählen Sie eine Aktion aus dem **Massenaktionen**-Dropdown aus
4. Klicken Sie auf **Anwenden**

Aktionen, die Daten ändern oder exportieren, werden sofort ausgeführt; **Ausgewählte löschen** bittet um Bestätigung, da es sich hierbei um die einzige Aktion handelt, die sich aus der Liste heraus nicht leicht rückgängig machen lässt.

## Verfügbare Aktionen

| Aktion | Was sie tun | 
|--------|---------------| 
| **Als Veröffentlicht markieren** | Setzt den Status der ausgewählten Produkte auf **Veröffentlicht**, sodass sie im Store sichtbar sind. | 
| **Als Entwurf markieren** | Setzt den Status der ausgewählten Produkte auf **Entwurf**, wodurch sie vom Store versteckt werden, während Sie weiter an der Bearbeitung arbeiten. | 
| **Als Markenprodukt kennzeichnen** | Aktiviert **Ist Markenprodukt** bei den ausgewählten Produkten. | 
| **Markenprodukt entfernen** | Deaktiviert **Ist Markenprodukt** bei den ausgewählten Produkten. | 
| **In CSV exportieren** | Lädt eine CSV-Datei mit der ID, dem Namen, SKU, dem Status, dem Markenprodukt-Flag und dem Preis der ausgewählten Produkte herunter. | 
| **Zollinformationen exportieren (CSV)** | Lädt eine CSV-Datei mit Zollinformationen der ausgewählten Produkte herunter. Siehe unten. | 
| **Prüfung der Bereitschaft für den internationalen Versand** | Zeigt eine Zusammenfassung an, welche ausgewählten Produkte die für internationale Sendungen benötigten Zollinformationen haben. Siehe unten. | 
| **Ausgewählte löschen** | Verschiebt die ausgewählten Produkte in den Papierkorb, nachdem ein Bestätigungsdialog angezeigt wurde. | 

## Zollinformationen exportieren (CSV)

Verwenden Sie dies, wenn Sie eine Zollerklärung benötigen, die Sie einem Spediteur, Kurierdienst oder Zollmakler übergeben können — beispielsweise, bevor eine große internationale Sendung stattfindet, oder wenn Sie einen neuen Versanddienst einrichten, der HS-Codes und Ursprungsdaten bereits im Voraus anfordert.

Wählen Sie die Produkte aus, wählen Sie **Zollinformationen exportieren (CSV)** aus dem Dropdown-Menü und klicken Sie auf **Anwenden**. Spwig lädt eine Datei mit dem Namen `product_customs_data.csv` herunter, wobei pro Produkt eine Zeile und folgende Spalten enthalten sind:

| Spalte | Quelle | 
|--------|--------| 
| **SKU** | Die SKU des Produkts | 
| **Name** | Der Produktname | 
| **HS-Code** | Der Harmonisierte System-Klassifizierungscode | 
| **Herstellungsort** | Wo das Produkt hergestellt wird | 
| **Zoll-Einheitpreis** | Der deklarierte Wert pro Einheit für den Zoll | 
| **Exportlizenz** | Die Exportlizenznummer, falls das Produkt eine benötigt | 
| **Lizenzablauf** | Das Ablaufdatum der Exportlizenz, falls festgelegt | 
| **International bereit** | `Ja` oder `Nein` — ob das Produkt die minimalen Daten für den internationalen Versand hat (siehe unten) | 

Diese Felder stammen aus dem Bereich **Internationaler Versand / Zoll** des Produktformulars. Wenn ein Produkt eines dieser Felder fehlt, wird die Spalte in der Exportdatei leer gelassen — füllen Sie die fehlenden Daten im Produkt vor der Verwendung dieser Datei für eine tatsächliche Sendung aus.

## Prüfung der Bereitschaft für den internationalen Versand

Verwenden Sie dies, um eine Gruppe von Produkten vor dem Start des internationalen Versands zu prüfen, ohne jedes Produkt einzeln öffnen zu müssen oder auf einen vollständigen CSV-Export warten zu müssen.

Wählen Sie die Produkte aus, wählen Sie **Prüfung der Bereitschaft für den internationalen Versand** und klicken Sie auf **Anwenden**. Spwig prüft jedes ausgewählte Produkt auf drei erforderliche Felder — **HS-Code**, **Herstellungsort** und **Zoll-Einheitpreis** — und zeigt eine Benachrichtigung mit einer Zusammenfassung des Ergebnisses an.

- Wenn bei jedem ausgewählten Produkt alle drei Felder ausgefüllt sind, wird eine Bestätigung angezeigt, dass alle bereit sind.
- Wenn bei einigen Daten fehlen, meldet die Benachrichtigung, wie viele bereit sind und wie viele nicht bereit sind, und listet jedes Produkt auf, das nicht bereit ist, zusammen mit den fehlenden Feldern (z. B. "Blauer Keramiktasse (fehlend: hs_code, land_of_origin)").

Wenn mehr als 10 Produkte Daten fehlen, listet die Benachrichtigung die ersten 10 auf und teilt mit, wie viele noch folgen.

Dieser Vorgang liest nur Daten, ändert jedoch nichts an den Produkten. Daher ist es sicher, ihn so oft auszuführen, wie Sie es wünschen, während Sie die Zollinformationen in Ihrem Katalog vervollständigen.

**Lizenznummer für den Export** und **Ablaufdatum der Exportlizenz** sind Teil der Bereitschaftsprüfung. Sie gelten nur für kontrollierte oder eingeschränkte Artikel. Ein Produkt kann also "bereit" für den internationalen Versand sein, ohne sie zu benötigen.

## Tipps

- Führen Sie **Prüfung der internationalen Versandbereitschaft** für Ihren gesamten Katalog (oder pro Kategorie) durch, bevor Sie die erste internationale Bestellung aufgeben – es ist viel schneller, als festzustellen, dass ein HS-Code fehlt, wenn die Sendung bereits an der Grenze ist.
- Halten Sie **Export-Zoll-Daten (CSV)** bereit, um sie Brokern und Frachtführern zu übergeben, und **Prüfung der internationalen Versandbereitschaft** für Ihre eigene interne Checkliste – die CSV-Datei ist ein Protokoll, die Bereitschaftsprüfung ist eine To-Do-Liste.
- Füllen Sie **HS-Code**, **Herkunftsland** und **Zoll-Einheitspreis** auf dem Produktformular (unter **Internationaler Versand / Zoll**) aus, während Sie neue Produkte hinzufügen, damit Sie sie später nicht in bulk-Form ausfüllen müssen.
- Das Produkt-Grid lädt bei Scrollen mehr Produkte automatisch (unendliches Scrollen), und Ihre Kontrollkästchen-Selektionen werden beibehalten, während neue Produkte geladen werden – also können Sie scrollen, um eine große Auswahl aufzubauen, bevor Sie einen Vorgang anwenden. Ändern Sie einen Filter oder laden Sie die Seite erneut, löscht dies Ihre Auswahl, also wenden Sie den Vorgang vor dem Anpassen der Filter an.
- **Als Entwurf markieren** ist eine schnelle Möglichkeit, mehrere Produkte gleichzeitig vom Geschäft zu entfernen – z. B. vor einer Lagerzählung – ohne etwas anderes an ihnen zu verändern.

Preserve all markdown formatting, image paths, code blocks, and technical terms.