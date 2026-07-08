---
title: Farbauswahl
---

Der erweiterte Farbauswahler ermöglicht es Ihnen, Farben mithilfe mehrerer Eingabemethoden und theme-bewusster Voreinstellungen zu wählen. Er erscheint an jeder Stelle, an der eine Farbeigenschaft verwendet wird – im Seiten-Editor, im Header/Footer-Editor, im Menü-Editor und im Katalog-Admin. Klicken Sie auf eine Farbschaltfläche oder ein Farbeingabefeld, um den Farbauswahler zu öffnen.

![Farbauswahl](/static/core/admin/img/help/color-picker/color-picker.webp)

## Farbeingabemethoden

Der Farbauswahler unterstützt mehrere Methoden, um eine Farbe zu definieren:

| Methode | Beschreibung | Beispiel |
|--------|-------------|---------|
| **Hex** | Geben Sie einen 6-stelligen Hex-Code direkt ein | `#FF5733` |
| **RGB** | Justieren Sie die Schieberegler für Rot, Grün und Blau (jeweils 0–255) | `rgb(255, 87, 51)` |
| **HSL** | Stellen Sie Hue (0–360), Sättigung (0–100%) und Helligkeit (0–100%) ein | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB mit einem Alpha-Transparenzkanal | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL mit einem Alpha-Transparenzkanal | `hsla(14, 100%, 60%, 0.8)` |
| **Visuelles Spektrum** | Klicken Sie oder ziehen Sie im Farbspektrum-Bereich, um visuell eine Farbe auszuwählen | Auswahl durch Klicken oder Ziehen |

Sie können auch einen Wert direkt in das Texteingabefeld am unteren Rand des Farbauswahlers eingeben.

## Format-Selektor

Ein Dropdown am oberen Rand des Farbauswahlers ermöglicht den Wechsel zwischen den Ausgabemodellen **HEX**, **RGB**, **RGBA**, **HSL** und **HSLA**. Wenn Sie zwischen den Formaten wechseln, wird die aktuelle Farbe automatisch konvertiert – keine Werte gehen verloren. Wählen Sie das Format, das am besten zu Ihrem Arbeitsablauf oder Ihren Designanforderungen passt.

## Farb-Voreinstellungen

Unterhalb des Spektrum-Bereichs befindet sich eine Reihe von schnellen Farbschaltflächen, die eine Ein-Klick-Auswahl für gängige Farben ermöglichen. Diese Schaltflächen sind **theme-bewusst**: Sie spiegeln automatisch die primären, sekundären, Akzent- und neutralen Farben des aktiven Themes wider. Dies macht es einfach, mit Ihrer Marke konsistent zu bleiben, ohne Hex-Codes auswendig zu lernen.

Um eine Voreinstellung anzuwenden, klicken Sie auf die Schaltfläche. Der Farbauswahler aktualisiert sich sofort, um die ausgewählte Farbe im Spektrum und in den Eingabefeldern anzuzeigen.

## Deckkraft / Alpha

Wenn Sie den Modus **RGBA** oder **HSLA** verwenden, erscheint ein horizontaler **Alpha-Schieberegler** unter dem Spektrum. Ziehen Sie ihn, um die Transparenz von 0 % (voll transparent) bis 100 % (voll undurchsichtig) einzustellen. Der Deckkraftwert kann auch als numerischer Eingabewert neben dem Schieberegler bearbeitet werden, um präzise Steuerung zu ermöglichen.

Halbtransparente Farben sind nützlich für Overlays, Hover-Effekte und geschichtete Designelemente.

## Aktuelle vs. Neue Vorschau

Am unteren Rand des Farbauswahlers werden zwei nebeneinander angeordnete Felder angezeigt, die die **aktuell** angewendete Farbe und die **neu** ausgewählte Farbe darstellen. Diese Vergleichsmöglichkeit ermöglicht es Ihnen, die Änderung vor der Bestätigung zu bewerten. Klicken Sie auf **Anwenden**, um die neue Farbe zu akzeptieren, oder klicken Sie außerhalb des Farbauswahlers, um die Änderung zu stornieren und den aktuellen Wert beizubehalten.

## Wo es erscheint

Der Farbauswahler ist ein gemeinsam genutztes Werkzeug, das im gesamten Admin-Bereich verwendet wird:

- **Seiten-Editor** – Textfarbe, Hintergrundfarbe, Rahmengrenze und Hover-Zustände im Stil-Tab
- **Header/Footer-Editor** – Textfarbe, Hintergrundfarbe, Ikonenfarbe und Linkfarbe der Widgets
- **Menü-Editor** – Linkfarbe der Menüelemente und Hover-/Aktivzustandsfarben
- **Katalog-Admin** – Farben für Produkt-Abzeichen und Kategorie-Akzentfarben

Jedes Feld, das eine Farbewert akzeptiert, öffnet denselben Farbauswahler, wodurch die Erfahrung überall konsistent bleibt.

## Tipps

- Verwenden Sie die Voreinstellungsschaltflächen Ihres Themes, um die Markenkonsistenz über alle Seiten und Komponenten hinweg zu gewährleisten.
- Wechseln Sie in den HSL-Modus, wenn Sie hellere oder dunklere Varianten derselben Farbe erstellen müssen – einfach den Helligkeitswert anpassen.
- Kopieren Sie den Hex-Code aus dem Texteingabefeld, um die exakt gleiche Farbe in einem anderen Feld oder um sie einem Designer zu teilen.
- Verwenden Sie RGBA mit reduzierter Deckkraft für subtile Overlay-Effekte auf Bildern und Hero-Bereichen.
- Der Farbauswahler erinnert sich während Ihrer Sitzung an kürzlich verwendete Farben, sodass häufig verwendete benutzerdefinierte Farben weiterhin zugänglich bleiben.
- Wenn Sie einen Farbwert in einem unterstützten Format in das Hex-Eingabefeld einfügen, erkennt der Farbauswahler diesen automatisch und konvertiert ihn.