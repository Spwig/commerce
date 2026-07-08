---
title: Clipart und Schriftarten für anpassbare Produkte
---

Der Design-Editor verfüt über zwei Arten kreativer Assets, die Sie Kunden bereitstellen können: **Clipart** (vorgefertigte Grafiken, die sie zu ihren Designs hinzufügen können) und **benutzerdefinierte Schriftarten** (jenseits der Standard-System-Schriftarten). Die Erstellung einer gut durchdachten Asset-Bibliothek macht den Editor nützlicher und hilft Kunden dabei, bessere Designs schneller zu erstellen.

## Clipart-Bibliothek

Clipart gibt Kunden eine Bibliothek vorgefertigter Grafiken, die sie mit einem Klick zu ihren Designs hinzufügen können. Anstatt Kunden zu verlangen, eigene Bilder für gängige Elemente wie Ikonen, Rahmen oder dekorative Grafiken zu finden und hochzuladen, stellen Sie diese bereits bereit, um sie zu verwenden.

### Erstellen von Clipart-Kategorien

Clipart wird in Kategorien organisiert, die Kunden durchsuchen können. Kategorien helfen Kunden dabei, das zu finden, was sie benötigen, schneller.

1. Navigieren Sie zu **Anpassbare Produkte > Clipart-Kategorien**
2. Klicken Sie auf **+ Clipart-Kategorie hinzufügen**
3. Füllen Sie aus:
   - **Kategoriename** — Was Kunden sehen (z. B. "Sport", "Rahmen", "Feiertag")
   - **Slug** — Automatisch aus dem Namen generiert
   - **Ikone** — Eine Font Awesome-Ikonenklasse für die Kategorietabelle (z. B. `fas fa-football-ball`)
   - **Sortierreihenfolge** — Steuert die Reihenfolge, in der Kategorien im Editor angezeigt werden
4. Klicken Sie auf **Speichern**

**Beispielkategorien für einen T-Shirt-Shop:"

| Kategorie | Ikone | Beispiel-Clipart |
|----------|------|-----------------|
| Sport | `fas fa-football-ball` | Mannschaftslogos, Sportgeräte, sportliche Symbole |
| Humor | `fas fa-laugh` | Memes, lustige Zitate, Cartoons |
| Natur | `fas fa-leaf` | Tiere, Blumen, Landschaften |
| Geometrie | `fas fa-shapes` | Muster, abstrakte Formen, Stammeskunst |

**Beispielkategorien für einen Druck-/Plakat-Shop:"

| Kategorie | Ikone | Beispiel-Clipart |
|----------|------|-----------------|
| Rahmen | `fas fa-border-all` | Dekorative Rahmen, Eckenverzierungen |
| Jahreszeiten | `fas fa-snowflake` | Feiertagsikonen, saisonale Motive |
| Ikonen | `fas fa-icons` | Sterne, Herzen, Pfeile, Haken |
| Hintergründe | `fas fa-image` | Texturen, Schattierungen, Muster |

### Clipart-Assets hinzufügen

Jedes Clipart-Asset ist eine Bilddatei (PNG oder SVG), die Kunden auf ihrem Canvas platzieren können.

1. Navigieren Sie zu **Anpassbare Produkte > Clipart-Assets**
2. Klicken Sie auf **+ Clipart-Asset hinzufügen**
3. Füllen Sie aus:
   - **Name** — Beschreibender Name (z. B. "Goldener Stern", "Football-Helm")
   - **Kategorie** — Wählen Sie aus Ihren Clipart-Kategorien
   - **Bilddatei** — Klicken Sie, um die Medienbibliothek zu öffnen und die Bilddatei auszuwählen oder hochzuladen
   - **Bereich** — Wählen Sie die Verfügbarkeit (siehe unten)
   - **Tags** — Durchsuchbare Schlüsselwörter für dieses Clipart (z. B. `['star', 'gold', 'decoration']`)
   - **Sortierreihenfolge** — Steuert die Position innerhalb der Kategorie
4. Klicken Sie auf **Speichern**

### Verstehen der Clipart-Bereiche

Jedes Clipart-Asset hat einen Bereich, der bestimmt, wo es verfügbar ist:

| Bereich | Beschreibung | Verwendungsfall |
|-------|-------------|----------|
| **Für alle Produkte verfügbar** | Wird im Clipart-Explorer für jedes anpassbare Produkt angezeigt | Allgemeine Grafiken wie Sterne, Rahmen und gängige Ikonen |
| **Nur für ein bestimmtes Produkt** | Wird nur für ein ausgewähltes Produkt angezeigt | Produkt-spezifische Grafiken wie Markenlogos oder thematische Kunstwerke für das Produkt |

Für die meisten Assets verwenden Sie **Für alle Produkte verfügbar**. Reservieren Sie den produkt-spezifischen Bereich für Assets, die nur im Kontext eines Produkts sinnvoll sind – zum Beispiel, Team-spezifische Logos für ein Team-Merchandise-Produkt.

### Clipart-Dateirichtlinien

- **Format:** Verwenden Sie PNG für Rastergrafiken und SVG für Vektorgrafiken. SVG-Dateien lassen sich ohne Qualitätsverlust skalieren, was sie ideal für Clipart macht, das Kunden erheblich vergrößern können
- **Auflösung:** PNG-Dateien sollten mindestens 500x500 Pixel haben, um eine gute Druckqualität zu gewährleisten
- **Hintergrund:** Verwenden Sie transparente Hintergründe (PNG mit Alpha-Kanal oder SVG), damit das Clipart sich natürlich mit dem Design vermischt
- **Dateigröße:** Halten Sie einzelne Clipart-Dateien unter 500 KB, um eine schnelle Ladezeit im Editor zu gewährleisten

## Benutzerdefinierte Schriftarten

Benutzerdefinierte Schriftarten erweitern den Schriftarten-Selektor im Design-Editor jenseits der Standard-System-Schriftarten.

Dies ermöglicht es Ihnen, eine kurierte Typografie anzubieten, die zu Ihrem Marken- oder Produktstil passt.

### Eine benutzerdefinierte Schrift hinzufügen

1. Navigieren Sie zu **Anpassbare Produkte > Benutzerdefinierte Schriften**
2. Klicken Sie auf **+ Benutzerdefinierte Schrift hinzufügen**
3. Füllen Sie aus:
   - **Schriftname** — Anzeigename, der im Schriftauswahlfeld angezeigt wird (z. B. "Playfair Display")
   - **Schriftfamilie** — CSS-Schriftfamilienname, der intern verwendet wird (z. B. `PlayfairDisplay`)
   - **Regulär** — Klicken Sie, um die reguläre Schriftgewichtungsdatei (WOFF2 oder TTF) über die Medienbibliothek hochzuladen
   - **Fett** — Optionaler fettgewichteter Variantentyp
   - **Kursiv** — Optionaler kursiver Variantentyp
   - **Fett kursiv** — Optionaler fett-kursiver Variantentyp
4. Klicken Sie auf **Speichern**

Das **Regulär**-Gewicht ist für benutzerdefinierte Schriften erforderlich. Fett, kursiv und fett-kursiv Varianten sind optional – wenn sie nicht bereitgestellt werden, versucht der Browser, diese Stile aus der regulären Schrift zu synthetisieren, wobei die Ergebnisse möglicherweise nicht so poliert aussehen wie dedizierte Schriftdateien.

### Systemschriften vs. benutzerdefinierte Schriften

Sie können auch Systemschriften registrieren, die auf den meisten Geräten vorinstalliert sind:

1. Fügen Sie einen neuen Eintrag für eine benutzerdefinierte Schrift hinzu
2. Markieren Sie **Systemschrift**
3. Geben Sie den Schriftfamilien-Namen genau so an, wie er in CSS erscheint (z. B. `Georgia`, `Courier New`)
4. Für Systemschriften ist keine Datei hochzuladen

Systemschriften laden sofort, da sie bereits auf dem Gerät des Kunden vorhanden sind. Benutzerdefinierte hochgeladene Schriften müssen zuerst heruntergeladen werden, was bei der ersten Auswahl der Schrift eine kleine Verzögerung verursacht.

### Schriftvorschläge nach Produkttyp

**Für T-Shirts und Kleidung:**
- Fette, einprägsame Schriften sind am besten geeignet: Impact, Anton, Bebas Neue, Oswald
- Blockbuchstaben und sans-serif-Schriften sind am besten lesbar auf Stoff
- Vermeiden Sie dünne oder feine Schriften, die auf texturierten Oberflächen möglicherweise nicht gut bedruckt werden

**Für Poster und Druckprodukte:**
- Elegante Serifen-Schriften für formelle Designs: Playfair Display, Merriweather, Lora
- Schreibschriften für Einladungen und Karten: Great Vibes, Dancing Script, Pacifico
- Klarer sans-serif für moderne Designs: Montserrat, Raleway, Open Sans

### Schriftdateiformate

| Format | Erweiterung | Empfehlung |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Empfohlen – kleinste Dateigröße, schnellste Ladezeit |
| TrueType | `.ttf` | Gute Alternative – weit verbreitete Kompatibilität |

WOFF2-Dateien sind in der Regel 30–50 % kleiner als TTF-Dateien, wodurch sie im Editor des Kunden schneller geladen werden. Verwenden Sie WOFF2, wenn verfügbar.

## Ihre Asset-Bibliothek verwalten

### Für Kunden organisieren

Die Reihenfolge, in der Assets im Editor angezeigt werden, wird durch das Feld **Sortierreihenfolge** für Kategorien und einzelne Assets gesteuert. Niedrigere Zahlen werden zuerst angezeigt. Verwenden Sie dies, um:
- Ihre beliebtesten Clipart-Kategorien an die Spitze zu setzen
- Die besten und vielseitigsten Clipart-Elemente in jeder Kategorie an die Spitze zu setzen
- Schriften mit den am häufigsten verwendeten Optionen an die Spitze zu setzen

### Die Bibliothek aktuell halten

- Fügen Sie saisonale Clipart-Elemente vor Feiertagen hinzu (Halloween, Weihnachten, Valentinstag) und deaktivieren Sie sie danach
- Verwenden Sie das **Aktiv**-Kästchen, um Assets vorübergehend zu verbergen, ohne sie zu löschen
- Überwachen Sie, welche Clipart-Elemente und Schriften Kunden am häufigsten verwenden, und erweitern Sie diese Kategorien

## Tipps

- Beginnen Sie klein – 20–30 hochwertige Clipart-Assets über 3–4 Kategorien sind besser als Hunderte von mittelmäßigen Optionen. Sie können immer mehr hinzufügen, sobald Sie wissen, was Kunden möchten.
- Verwenden Sie SVG-Format für Clipart, wenn möglich. SVG-Dateien sind kleiner, passen sich jeder Größe perfekt an und erzeugen schärfere Drucke als Rasterbilder.
- Testen Sie jede hochgeladene Schrift im Design-Editor, um sicherzustellen, dass alle Zeichen korrekt gerendert werden, insbesondere Sonderzeichen und Akzente, wenn Ihre Kunden mehrere Sprachen verwenden.
- Kennzeichnen Sie Clipart gründlich – Kunden suchen nach Schlüsselwörtern, daher helfen beschreibende Tags wie "gold", "Stern", "5-eckig", "dekoration" dabei, das richtige Asset schnell zu finden.
- Gruppieren Sie verwandte Clipart-Elemente in dieselbe Kategorie. Wenn Sie Team-Merchandise verkaufen, erstellen Sie eine Kategorie pro Sportart anstelle einer riesigen "Sport"-Kategorie.
- Überprüfen Sie regelmäßig Ihre Clipart-Bibliothek aus der Sicht des Kunden, indem Sie den Design-Editor auf der Frontseite besuchen.