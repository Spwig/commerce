---
title: Benutzerdefinierte Elemente
---

Benutzerdefinierte Elemente ermöglichen es Ihnen, wiederverwendbare Blöcke im Seitenbaukasten zu erstellen, die auf die Bedürfnisse Ihres Geschäfts abgestimmt sind. Sie entwerfen ein Element visuell mithilfe der vorhandenen Werkzeuge des Seitenbaukastens und verbinden es optional mit Live-Daten aus dem Geschäft – wie Produktbezeichnungen, Preisen oder Bildern – sodass das Element automatisch mit echten Inhalten gefüllt wird, wenn es auf einer Seite platziert wird. Nach der Erstellung erscheinen Ihre benutzerdefinierten Elemente in der Elementbibliothek des Seitenbaukastens neben den integrierten Blöcken.

![Benutzerdefinierte Elementbibliothek](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Wann benutzerdefinierte Elemente verwenden

Benutzerdefinierte Elemente sind am wertvollsten, wenn Sie sich häufig denselben Layout wiederholen. Anstatt ein "hervorgehobenes Produktkarten"-Element auf jeder Seite von Grund auf neu zu erstellen, erstellen Sie es einmal als benutzerdefiniertes Element und fügen es einfach dort hinzu, wo Sie es benötigen. Wenn das Element datenbasiert ist, zieht es automatisch aktuelle Produktinformationen – keine manuellen Updates sind erforderlich, wenn sich Preise oder Namen ändern.

Häufige Anwendungen:

- Produkt-Highlight-Karten, die Bezeichnung, Preis und Hauptbild anzeigen
- Kategorie-Präsentationsblöcke mit Banner, Titel und Link
- Marken-Präsentationspanels mit Logo und Beschreibung
- Blog-Beitrags-Vorschau mit Hauptbild, Titel und Auszug

## Ein neues benutzerdefiniertes Element erstellen

1. Navigieren Sie zu **Design > Benutzerdefinierte Elemente**
2. Klicken Sie auf **+ Benutzerdefiniertes Element hinzufügen**
3. Spwig erstellt sofort einen Entwurf des Elements und öffnet den **Visuellen Baukasten** – Sie müssen nicht zuerst ein Formular ausfüllen
4. Im Visuellen Baukasten erstellen Sie das Layout Ihres Elements mithilfe der verfügbaren Seitenbaukasten-Werkzeuge
5. Wenn Sie mit dem Design zufrieden sind, konfigurieren Sie die Einstellungen des Elements (Name, Datenbindung, Icon) in der Seitenleiste
6. Aktivieren Sie **Aktiv**, wenn Sie bereit sind, das Element in die Bibliothek zu veröffentlichen
7. Speichern Sie das Element

Das Element ist jetzt in der Elementleiste des Seitenbaukastens unter der von Ihnen zugewiesenen Kategorie verfügbar.

## Der visuelle Baukasten

Der Visuelle Baukasten ist ein dedizierter Canvas zur Gestaltung Ihres Elements. Er funktioniert wie der Standardseitenbaukasten, konzentriert sich aber auf ein einzelnes Element anstelle einer ganzen Seite. Sie können:

- Kinderelemente hinzufügen und anordnen (Textblöcke, Bilder, Container usw.)
- Für jedes Kinderelement Stil, Abstand und Layout festlegen
- Vorschau, wie das Element mit Beispiel-Daten aussehen wird

Änderungen im Visuellen Baukasten werden direkt in die Elementdefinition gespeichert. Es gibt keinen separaten Veröffentlichungsschritt – das Speichern im Baukasten aktualisiert das Element sofort für alle Seiten, die es bereits verwenden.

## Einstellungen für Elemente konfigurieren

Jedes benutzerdefinierte Element hat diese Einstellungen:

| Feld | Beschreibung |
|-------|-------------|
| **Name** | Anzeigename, der in der Elementbibliothek angezeigt wird |
| **Slug** | URL-sicherer Bezeichner, automatisch aus dem Namen generiert |
| **Beschreibung** | Optionaler Hinweis, zu dem Zweck dieses Elements |
| **Zielmodell** | Das Geschäftmodell, aus dem Daten gebunden werden sollen (siehe unten) |
| **Icon** | Icon, das in der Elementbibliothek angezeigt wird |
| **Kategorie** | Gruppiert verwandte Elemente in der Bibliothek |
| **Aktiv** | Ob das Element im Seitenbaukasten verfügbar ist |

## Datenbindung

Datenbindung verbindet Teile des Layouts Ihres Elements mit Live-Daten aus dem Geschäft. Wenn ein Seiteneditor ein datenbasiertes Element auf einer Seite platziert, wählt er ein bestimmtes Datensatz (z. B. ein Produkt) aus, und alle gebundenen Felder werden automatisch aus diesem Datensatz befüllt.

### Zielmodell auswählen

Die Einstellung **Zielmodell** bestimmt, welche Art von Geschäftsinformationen das Element anzeigt. Die verfügbaren Modelle sind:

| Modell | Was es bereitstellt |
|-------|-----------------|
| **Produkt** | Name, Preis, Lagerstatus, Bilder, Beschreibung, SKU, Kategorie, Marke und mehr |
| **Kategorie** | Name, Beschreibung, Bild, Banner, Produktanzahl und URL |
| **Marke** | Name, Logo, Beschreibung, Markengeschichte und URL |
| **Blogbeitrag** | Titel, Auszug, Hauptbild, Autor, Veröffentlichungsdatum und URL |

Lassen Sie **Zielmodell** leer, um ein statisches Element ohne dynamische Daten zu erstellen. Statische Elemente sind nützlich für feste Designkomponenten wie dekorative Banner oder Layout-Abstandshalter.

### Wie Bindungen funktionieren

# Visueller Builder

Innerhalb des visuellen Builders können Sie einzelne Kind-Elemente als datenverknüpft markieren, indem Sie das Modellfeld auswählen, das sie anzeigen sollen.

Beispiel:

- Ein **Text**-Kind-Element kann an **Produktname** gebunden werden, damit es den Namen des ausgewählten Produkts anzeigt
- Ein **Bild**-Kind-Element kann an **Hauptbild** gebunden werden, damit es das Hauptfoto des Produkts anzeigt
- Ein **Text**-Kind-Element kann an **Preis** gebunden werden, damit es immer den aktuellen Preis anzeigt

Jede Verknüpfung ordnet ein Elementinhalt-Feld einem Modellfeld zu. Sie können mehrere Verknüpfungen zu einem einzigen benutzerdefinierten Element hinzufügen – beispielsweise ein Textblock an **Produktname** und einen separaten Bildblock an **Hauptbild** gleichzeitig.

### Vorgaben für Miniaturansichten

Bei Bildverknüpfungen können Sie optional eine **Miniaturvorgabe** (z. B. `thumbnail` oder `medium`) angeben. Dies steuert die Größe des geladenen Bildes und hilft, Seiten schneller zu laden, indem die entsprechend groß formatierte Datei für das Layout des Elements bereitgestellt wird.

## Deaktivieren und erneut aktivieren von Elementen

Das Deaktivieren eines Elements entfernt es aus der Elementbibliothek, sodass es nicht zu neuen Seiten hinzugefügt werden kann. Bestehende Seiten, die das Element bereits verwenden, sind davon nicht betroffen – das Element wird weiterhin auf diesen Seiten gerendert.

Um ein Element zu deaktivieren:

1. Navigieren Sie zu **Design > Benutzerdefinierte Elemente**
2. Klicken Sie auf den Elementnamen
3. Deaktivieren Sie **Aktiv**
4. Speichern Sie die Änderung

Um ein Element erneut zu aktivieren, führen Sie die gleichen Schritte durch und aktivieren Sie **Aktiv** erneut.

## Filtern der Elementbibliothek

Die Elementliste unterstützt das Filtern nach:

- **Aktiv / Inaktiv** – nur veröffentlichte oder nur Entwurfselemente anzeigen
- **Zielmodell** – nach dem Modell filtern, zu dem ein Element gebunden ist
- **Kategorie** – nach Elementkategorie filtern
- **Suche** – nach Name, Slug oder Beschreibung suchen

Dies hilft, wenn Sie viele benutzerdefinierte Elemente haben und ein bestimmtes schnell finden müssen.

## Beispiel: Produkt-Highlight-Karte

**Ziel:** Ein Karte-Element, das das Hauptbild, den Namen und den Preis eines Produkts anzeigt.

| Einstellung | Wert |
|-----------|-----|
| Name | Produkt-Highlight-Karte |
| Zielmodell | Produkt |
| Kategorie | Produkte |
| Icon | fas fa-box |

Im visuellen Builder fügen Sie hinzu:
- Ein **Bild**-Element, das an **Hauptbild** gebunden ist, mit der Miniaturvorgabe `medium`
- Ein **Text**-Element, das an **Produktname** gebunden ist
- Ein **Text**-Element, das an **Preis** gebunden ist

Nachdem das Element gespeichert und aktiviert wurde, erscheint es im Seitenbuilder unter der Kategorie Produkte. Wenn ein Seitenbearbeiter es einer Seite hinzufügt, wählt er aus, welches Produkt hervorgehoben werden soll, und die Karte füllt sich automatisch.

## Tipps

- Geben Sie Elementen beschreibende Namen, die ihre Funktion und den Datentyp enthalten – beispielsweise „Produkt-Highlight-Karte“ anstelle von „Karte 1“ – damit die Bibliothek weiterhin leicht navigierbar bleibt, wenn sie wächst
- Verwenden Sie das **Kategorie**-Feld, um verwandte Elemente (Produkte, Blog, Promotionen) zu gruppieren – dies hält die Elementbibliothek für Ihre Seitenbearbeiter organisiert
- Testen Sie datenverknüpfte Elemente, indem Sie sie einer Entwurfseite hinzufügen und eine reale Datensatzvorlage auswählen, bevor Sie sie veröffentlichen, um sicherzustellen, dass die Verknüpfung die richtigen Informationen abruft
- Deaktivieren Sie veraltete Elemente anstelle von deren Löschen – dies bewahrt alle Seiten, die sie noch verwenden, und gibt Ihnen die Möglichkeit, sie später erneut zu aktivieren
- Statische Elemente (kein Zielmodell) sind ideal für Layoutmuster, die Sie über die gesamte Website wiederverwenden können, wie Trenner, CTA-Panels oder markenbasierte Abstände