---
title: Typografie-Editor
---

Der Typografie-Editor ist ein gemeinsamer Stil-Utility, der Ihnen volle Kontrolle über das Erscheinungsbild von Text gewährt. Er öffnet sich als schwebendes Panel, sobald Sie Typografie-Eigenschaften auf jedem Element im Page Builder, Header/Footer Builder oder Menu Builder bearbeiten.

![Typografie-Editor](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Live-Vorschau

Der Editor zeigt eine Vergleichsansicht neben einander oben im Panel:

| Box | Zweck |
|-----|---------|
| **Aktuell** | Zeigt "The quick brown fox..." im bestehenden Typografie-Stil an |
| **Neu** | Wird in Echtzeit aktualisiert, sobald Sie Einstellungen anpassen, und zeigt das Ergebnis vor der Anwendung an |

Dies ermöglicht es Ihnen, vor und nach dem Ändern zu vergleichen, ohne Änderungen zu bestätigen.

## Schriftart-Tab

Der Schriftart-Tab ist der Standardansicht, wenn der Editor geöffnet wird.

**Schriftartfamilie** — Eine durchsuchbare Dropdown-Liste mit mehr als 70 Schriftarten, die nach Kategorie organisiert sind. Jede Schriftart wird in ihrer eigenen Schriftart vorgestellt, damit Sie sehen können, wie sie aussieht, bevor Sie sie auswählen. Schriftarten werden bei Bedarf von Google Fonts geladen.

**Schriftgrad** — Numerischer Eingabefeld mit einer Einheitenauswahl, die px, em, rem und % unterstützt. Der Standardwert ist 16px.

**Schriftgewicht** — Ein Schieberegler von 100 (Thin) bis 900 (Black):

| Wert | Name |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

Nicht jede Schriftart unterstützt alle neun Gewichte. Der Editor zeigt an, welche Gewichte für die ausgewählte Schriftartfamilie verfügbar sind.

**Schriftstil** — Schaltflächen zum Umschalten zwischen Normal, Kursiv und Schräg.

## Abstand-Tab

Feinabstimmung des Abstands um und zwischen Zeichen:

| Steuerelement | Was es tut | Standard |
|---------|-------------|---------|
| **Zeilenhöhe** | Vertikaler Abstand zwischen Zeilen Text | normal |
| **Buchstabenabstand** | Horizontaler Abstand zwischen einzelnen Buchstaben | normal |
| **Wortabstand** | Horizontaler Abstand zwischen Wörtern | normal |
| **Texteinzug** | Einzug der ersten Zeile in einem Absatz | 0 |

Jeder Abstandssteuerung enthält einen Einheitenauswahl (px, em, rem, %).

## Stil-Tab

Steuerung von Textdekoration und visuellen Effekten:

- **Textdekoration** — Keine, Unterstrich, Überstrich oder Durchgestrichen
- **Dekorationsstil** — Fest, Strich, Punkt, Doppelt oder Wellen (wird angewendet, wenn eine Dekoration aktiv ist)
- **Dekorationsfarbe** — Farbauswahl für die Dekorationslinie, standardmäßig ist dies die Textfarbe
- **Textschatten** — Optionaler Schatteneffekt mit Offset, Verschmierung und Farbauswahl

## Transform-Tab

Ändern Sie die Großschreibung des Textes, ohne den Inhalt zu bearbeiten:

| Option | Ergebnis |
|--------|--------|
| **Keine** | Der Text erscheint wie geschrieben |
| **Grossbuchstaben** | ALLE BUCHSTABEN WERDEN GROSSGESCHRIEBEN |
| **Kleinbuchstaben** | alle Buchstaben sind klein |
| **Kapitalisierung** | Der erste Buchstabe jedes Wortes wird großgeschrieben |

Zusätzliche Steuerungen auf diesem Tab umfassen **Textausrichtung** (links, zentriert, rechts, gerechtfertigt), **Vertikale Ausrichtung** und **Textrichtung** (LTR oder RTL).

## Verfügbare Schriftartfamilien

Der Editor enthält eine sorgfältig ausgewählte Bibliothek von System- und Google-Schriftarten, die nach Kategorie gruppiert sind:

| Kategorie | Schriftarten
|----------|-------
| **System** | Systemstandard, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **Sans-Serif (Klassisch)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **Serif (System)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **Display** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

Google Fonts werden automatisch geladen, wenn sie ausgewählt werden. System-Schriftarten verwenden korrekte CSS-Fallback-Ketten für eine zuverlässige Darstellung auf verschiedenen Plattformen.

## Wo es erscheint

Der Typografie-Editor ist an allen Stellen verfügbar, an denen Textstilierung benötigt wird:

- **Page Builder** — Wählen Sie jedes Element aus, öffnen Sie den Reiter **Stil** und klicken Sie auf den Abschnitt **Typografie**
- **Header/Footer Builder** — Stilisieren Sie Text in Navigation-Links, Logo-Text, Menüelementen und Footer-Inhalten
- **Menu Builder** — Steuern Sie die Typografie für Menülabels und Unter-Menüelemente
- **Catalog Admin** — Wird in Produktbeschreibungen und Inhalt-Editoren verwendet, an denen Typografie-Steuerungen verfügbar sind

Der Editor wird immer über die gleiche konsistente Oberfläche aufgerufen, unabhängig vom Kontext.

## Tipps

- **Kombinieren Sie Schriftarten bewusst** — verwenden Sie eine Display- oder Serifen-Schriftart für Überschriften und eine klare Sans-Serif-Schriftart für den Haupttext. Klassische Kombinationen wie Playfair Display + Inter oder Montserrat + Merriweather funktionieren gut.
- **Begrenzen Sie die Anzahl der Schriftarten pro Seite** — zwei oder drei Schriftarten pro Seite sind in der Regel ausreichend. Mehr als das kann die Ladezeiten verlangsamen und visuelle Unordnung verursachen.
- **Verwenden Sie relative Einheiten für responsiven Text** — em und rem skalieren mit der Basisschriftgröße, wodurch sich Ihre Typografie automatisch an verschiedene Bildschirmgrößen anpasst.
- **Überprüfen Sie die Gewichtsverfügbarkeit** — wenn der Text bei 400 und 500 gleich aussieht, unterstützt die ausgewählte Schriftart möglicherweise dieses Gewicht nicht. Der Editor zeigt an, welche Gewichte jede Schriftart bereitstellt.
- **Vorschau auf allen Geräten** — Text, der auf Desktop-Größen gut aussieht, kann auf Mobilgeräten zu klein oder zu groß sein. Verwenden Sie die Vorschau im Page Builder, um dies zu überprüfen.
- **Verwenden Sie die Live-Vorschau** — vergleichen Sie immer **Aktuell** vs. **Neu** in den Vorschaufeldern, bevor Sie anwenden, um unerwartete Änderungen zu vermeiden.