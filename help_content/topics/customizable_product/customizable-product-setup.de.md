---
title: Ein individuierbares Produkt einrichten
---

Dieser Leitfaden führt Sie durch den gesamten Einrichtungsprozess eines individuierbaren Produkts, von der Erstellung des Produkts bis zur Konfiguration von Oberflächen, Preisen und Upload-Einschränkungen. Zwei praktische Beispiele werden während des gesamten Prozesses verwendet: eine **individuelle T-Shirt** (mehrflächiges Kleidungsstück) und ein **individuelles Poster** (einflächiges Druckprodukt).

## Schritt 1: Produkt erstellen

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt hinzufügen**
2. Wählen Sie **Produkttyp** auf **Individuierbares Produkt**
3. Geben Sie den Produktname, Beschreibung, Bilder und Preise ein, wie Sie es für jedes Produkt tun würden
4. Speichern Sie das Produkt

Nach dem Speichern erscheint ein neuer **Open Design Editor Setup**-Knopf auf dem Produktformular. Dies führt Sie zur dedizierten Einrichtungsseite, wo Sie den visuellen Design-Editor konfigurieren.

## Schritt 2: Zugang zum Design-Editor-Setup

1. Öffnen Sie das gerade erstellte Produkt im Admin-Bereich
2. Klicken Sie auf den **Open Design Editor Setup**-Knopf (im Abschnitt Individuierbares Produkt)
3. Die Einrichtungsseite öffnet sich mit drei Registerkarten: **Oberflächen**, **Einstellungen** und **Preise**

Die Einrichtungsseite ist der Ort, an dem Sie alles über den Design-Editor für dieses Produkt definieren.

## Schritt 3: Oberflächen hinzufügen

Eine Oberfläche stellt eine designbare Seite Ihres Produkts dar. Klicken Sie auf **+ Oberfläche hinzufügen**, um jede Oberfläche zu erstellen.

### T-Shirt-Beispiel: 3 Oberflächen

| Oberfläche | Name | Abmessungen | Designzone | Hinweise |
|-----------|------|-----------|-------------|-------|
| 1 | Vorderseite | 300 x 400 mm | Zentrierte Brustbereich | Hauptdesignbereich |
| 2 | Rückseite | 300 x 400 mm | Oberer Rückenbereich | Sekundärer Designbereich |
| 3 | Linker Ärmel | 100 x 100 mm | Oberer Armbereich | Nur für kleines Logo |

### Poster-Beispiel: 1 Oberfläche

| Oberfläche | Name | Abmessungen | Designzone | Hinweise |
|-----------|------|-----------|-------------|-------|
| 1 | Vorderseite | 210 x 297 mm (A4) | Vollständiger Druckbereich | Einflächig, hohe DPI |

### Jede Oberfläche konfigurieren

Für jede Oberfläche konfigurieren Sie Folgendes:

**Grundlegende Informationen:**
- **Name** — Was Kunden in den Oberflächen-Registerkarten sehen (z. B. „Vorderseite“, „Rückseite“)
- **Slug** — URL-sicherer Bezeichner, automatisch aus dem Namen generiert
- **Sortierreihenfolge** — Steuert die Reihenfolge, in der Oberflächen angezeigt werden (niedrigere Zahlen zuerst)

**Mockup-Bild:**
- Klicken Sie auf den Mockup-Bildbereich, um die Medienbibliothek zu öffnen und ein Produktfoto auszuwählen, das diese Oberfläche zeigt
- Verwenden Sie ein hochwertiges Produktfoto aus der richtigen Perspektive

**Positionierung der Designzone:**
- Nachdem Sie ein Mockup-Bild ausgewählt haben, erscheint eine rechteckige Überlagerung auf dem Vorschaubild
- **Ziehen** Sie die Überlagerung, um die Position anzugeben, an der die Designzone auf dem Mockup sein soll
- **Vergrößern/Verkleinern** Sie die Überlagerung, indem Sie ihre Kanten ziehen, um die Grenzen des Designbereichs zu definieren
- Die Zone wird als prozentbasierte Koordinaten gespeichert, sodass sie sich bei jeder Bildschirmgröße anpasst

Die Designzone teilt dem Editor mit, wo auf dem Produktbild der Kunde-Design genau erscheinen wird. Positionieren Sie sie sorgfältig, um den tatsächlichen Druckbereich Ihres Produkts zu entsprechen.

**Physische Abmessungen:**
- **Breite** und **Höhe** — Die realen Abmessungen des Designbereichs
- **Einheit** — Millimeter, Zoll oder Pixel
- Diese Abmessungen bestimmen das Seitenverhältnis des Design-Kanvases und werden verwendet, um die Druck-DPI zu berechnen

**Druckeinstellungen:**
- **Mindest-DPI** — Die niedrigste akzeptable Tropfen pro Zoll. Kunden erhalten eine Warnung, wenn ihre hochgeladenen Bilder unter diesem Wert liegen. Standard: 150
- **Empfohlene DPI** — Die ideale Auflösung für die beste Druckqualität. Standard: 300
- **Bleed (mm)** — Zusätzlicher Rand außerhalb des Designbereichs für den Druck-Bleed. Auf 0 mm setzen, wenn kein Bleed benötigt wird (häufig bei Kleidung), oder 3 mm für professionelle Druckprodukte
- **Maximale Farben** — Bei Siebdruck können Sie die Anzahl der Farben begrenzen. Leer lassen für unbegrenzt (digitaler Druck)
- **Hintergrundfarbe** — Standard-Hintergrundfarbe des Kanvases

### T-Shirt vs. Poster-Druckeinstellungen

| Einstellung | T-Shirt | Poster |
|-----------|---------|--------|
| Mindest-DPI | 150 | 200 |
| Empfohlene DPI | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Maximale Farben | 6 (Siebdruck) | Leer (unbegrenzt) |
| Hintergrundfarbe | Farbe des Kleidungsstücks | `#ffffff` (weiß) |

## Schritt 4: Oberflächen-spezifische Einschränkungen

Jede Oberfläche kann die globalen Einstellungen für Merkmale überschreiben. Dadurch können Sie verschiedene Werkzeuge für verschiedene Oberflächen zulassen.

Die Einschränkungsoptionen sind:

| Einstellung | Optionen | Beschreibung |
|---------|---------|-------------|
| **Text erlauben** | Erben / Ja / Nein | Ob Kunden Text auf dieser Oberfläche hinzufügen können |
| **Bildupload erlauben** | Erben / Ja / Nein | Ob Kunden Bilder auf diese Oberfläche hochladen können |
| **Clipart erlauben** | Erben / Ja / Nein | Ob Kunden Clipart auf dieser Oberfläche verwenden können |
| **Maximale Elemente** | Zahl oder leer | Maximale Anzahl an Gestaltungselementen, die auf dieser Oberfläche erlaubt sind |

Wenn auf **Erben** gesetzt wird, verwendet die Oberfläche die Konfiguration aus den globalen Einstellungen (Schritt 6). Wenn auf **Ja** oder **Nein** gesetzt wird, überschreibt dies die globale Einstellung für diese spezifische Oberfläche.

### Beispiel: Einschränkung für T-Shirt-Ärmel

Für die Oberfläche des T-Shirt-Ärmels möchten Sie möglicherweise die Anpassung auf ein kleines Logo beschränken:

| Einstellung | Wert | Grund |
|---------|-------|--------|
| Text erlauben | Nein | Zu klein für lesbaren Text |
| Bildupload erlauben | Ja | Erlaubt den Upload eines kleinen Logos |
| Clipart erlauben | Nein | Einfach halten |
| Maximale Elemente | 1 | Nur ein Logo |

Die Vorder- und Rückseite bleiben auf **Erben** gesetzt, wodurch alle Werkzeuge wie in den globalen Einstellungen definiert verwendet werden können.

### Beispiel: Poster-Einschränkung

Bei einem Poster erben normalerweise alle Oberflächen von der globalen Konfiguration, da es nur eine Oberfläche gibt und alle Werkzeuge verfügbar sein sollten. Keine Oberflächen-spezifischen Überschreibungen sind erforderlich.

## Schritt 5: Upload-Einschränkungen konfigurieren

Auf dem **Einstellungen**-Reiter können Sie konfigurieren, wie Kunden Dateien hochladen können:

| Einstellung | Beschreibung | T-Shirt-Beispiel | Poster-Beispiel |
|---------|-------------|-----------------|----------------|
| **Maximaler Upload-Größe** | Maximale Dateigröße pro Upload | 10 MB | 20 MB |
| **Maximaler Uploads pro Oberfläche** | Wie viele Bilder pro Oberfläche | 5 | 3 |
| **Erlaubte Upload-Typen** | Akzeptierte Dateiformate | JPG, PNG, WebP | JPG, PNG, WebP |

Für Druckprodukte, bei denen Kunden hochauflösende Bilder hochladen müssen, sind größere Dateigrößenbegrenzungen empfohlen.

## Schritt 6: Editor-Einstellungen

Auf dem **Einstellungen**-Reiter können Sie das globale Verhalten des Editors konfigurieren:

**Editor-Modus:**
- **Canvas-Editor** — Vollständiger visueller Editor mit Live-Vorschau des Canvas. Empfohlen für die meisten Produkte.
- **Einfache Form** — Traditionelle Formularfelder für grundlegende Anpassungen (z. B. nur Textgravur).

**Funktionsschalter (globale Standardwerte):**
- **Text erlauben** — Erlaubt es Kunden, Textelemente hinzuzufügen
- **Bildupload erlauben** — Erlaubt es Kunden, ihre eigenen Bilder hochzuladen
- **Clipart erlauben** — Erlaubt es Kunden, in Ihrem Clipart-Repository zu suchen und Clipart zu verwenden

Diese globalen Einstellungen gelten für alle Oberflächen, es sei denn, sie werden durch Oberflächen-spezifische Einschränkungen (Schritt 4) überschrieben.

## Schritt 7: Preisgestaltung konfigurieren

Auf dem **Preisgestaltung**-Reiter legen Sie die Designgebühren fest, die dem Grundpreis des Produkts hinzugefügt werden:

| Gebühr | Beschreibung |
|-----|-------------|
| **Grundgebühr für Design** | Flache Gebühr, die hinzugefügt wird, wenn irgendeine Anpassung angewendet wird |
| **Pro-Oberflächen-Gebühr** | Zusätzliche Gebühr für jede Oberfläche, die über die erste hinausgenutzt wird |
| **Pro-Upload-Gebühr** | Gebühr für jeden vom Kunden hochgeladenen Bild |
| **Pro-Text-Gebühr** | Gebühr für jedes hinzugefügte Textelement |

### Beispiel: T-Shirt-Preisgestaltung

| Gebühr | Betrag | Begründung |
|-----|--------|-----------|
| Grundgebühr für Design | 5,00 $ | Deckt die Einrichtungskosten für jede benutzerdefinierte Bestellung ab |
| Pro-Oberflächen-Gebühr | 2,00 $ | Jede zusätzliche Oberfläche erhöht die Druckkosten |
| Pro-Upload-Gebühr | 1,00 $ | Benutzerdefinierte Bilder benötigen Verarbeitung |
| Pro-Text-Gebühr | 0,50 $ | Text ist einfacher als Bilder zu produzieren |

**Berechnungsbeispiel:** Ein Kunde gestaltet ein T-Shirt mit Text auf der Vorderseite und einem Logo auf der Rückseite:
- Grundgebühr für Design: 5,00 $
- 1 zusätzliche Oberfläche (Rückseite): 2,00 $
- 1 hochgeladenes Logo: 1,00 $
- 1 Textelement: 0,50 $
- **Gesamtdesigngebühr: 8,50 $** (wird zum Grundpreis des Produkts hinzugefügt)

### Beispiel: Poster-Preisgestaltung


| Gebühr | Betrag | Begründung |
|-----|--------|-----------|
| Grundgebühr für das Design | $0,00 | Keine Grundgebühr – der Produktpreis deckt sie ab |
| Gebühr pro Oberfläche | $0,00 | Einzelne Oberfläche, nicht anwendbar |
| Gebühr pro Upload | $2,00 | Hochauflösende Verarbeitung |
| Gebühr pro Text | $0,00 | Text ist im Grundangebot enthalten |

**Berechnungsbeispiel:** Ein Kunde erstellt ein Plakat mit 2 hochgeladenen Fotos und 3 Textelementen:
- Grundgebühr für das Design: $0,00
- 2 hochgeladene Fotos: $4,00
- 3 Textelemente: $0,00
- **Gesamtgebühr für das Design: $4,00**

Die Designgebühr wird Kunden in Echtzeit angezeigt, wenn sie Elemente hinzufügen, damit sie den Kostenimpact jedes Hinzufügens vor dem Hinzufügen zum Warenkorb sehen können.

## Übersicht der Einrichtung

| Aspekt | Selbstgestalteter T-Shirt | Selbstgestalteter Plakat |
|--------|---------------|---------------|
| Oberflächen | 3 (Vorderseite, Rückseite, Ärmel) | 1 (Vorderseite) |
| Mockup-Bilder | 3 Produktbilder | 1 Produktbild |
| Positionierung der Zonen | Brust/Rücken/Arm-Bereiche | Vollständiger druckbarer Bereich |
| Abmessungen | 300x400mm, 100x100mm | 210x297mm (A4) |
| Mindest-DPI | 150 | 200 |
| Schneidebereich | 0 mm | 3 mm |
| Maximalfarben | 6 | Unbegrenzt |
| Einschränkungen pro Oberfläche | Ärmel eingeschränkt | Keine erforderlich |
| Preismodell | Grundgebühr + Oberfläche + Upload + Text | Nur Upload-Gebühren |

## Tipps

- Testen Sie den Design-Editor immer aus der Sicht des Kunden nach Abschluss der Einrichtung. Besuchen Sie die Produktseite im Onlineshop und versuchen Sie, Text hinzuzufügen, ein Bild hochzuladen und Oberflächen zu wechseln.
- Laden Sie Mockup-Bilder hoch, die sich der tatsächlichen Produkterscheinung sehr nahekommen. Für T-Shirts fotografieren Sie jeden Winkel separat. Für Plakate verwenden Sie ein sauberes Flachbild oder ein Rahmen-Mockup.
- Positionieren Sie den Designbereich vorsichtig – es ist besser, einen leicht kleineren Bereich zu definieren, als dass Designs in Nähte oder Kanten drucken.
- Legen Sie die Mindest-DPI basierend auf Ihrem Druckverfahren fest: 150 für Siebdruck, 200 für Standarddigitaldruck, 300 für hochwertigen Offsetdruck.
- Verwenden Sie 3 mm Schneidebereich für jedes Produkt, das nach dem Drucken geschnitten wird (Plakate, Visitenkarten, Flyer). Setzen Sie Schneidebereich auf 0 für Produkte, bei denen das Design auf eine vorhandene Oberfläche aufgebracht wird (T-Shirts, Becher, Handyhüllen).
- Beginnen Sie mit einer einfachen Preisgestaltung und passen Sie diese basierend auf Kundenfeedback an. Viele Händler beginnen mit nur einer Grundgebühr für das Design und fügen später Gebühren pro Element hinzu.