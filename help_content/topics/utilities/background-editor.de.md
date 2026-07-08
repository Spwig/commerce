---
title: Hintergrund-Editor
---

Der Hintergrund-Editor gibt Ihnen volle Kontrolle über die Hintergründe von Elementen mit vier Typen: Festen Farbe, Farbverlauf, Bild und Video. Er unterstützt auch separate Zustände **Normal** und **Hover**, damit Sie interaktive visuelle Effekte erstellen können. Öffnen Sie den **Stil-Tab** eines Elements und suchen Sie nach dem Abschnitt **Hintergrund**, um den Editor zu öffnen.

![Hintergrund-Editor](/static/core/admin/img/help/background-editor/background-editor.webp)

## Normal- und Hover-Zustände

Oben im Hintergrund-Editor wechselt ein Schalter zwischen den Zuständen **Normal** und **Hover**. Jeder Zustand hat seine eigene unabhängige Hintergrundkonfiguration:

- **Normal** — Der Standardhintergrund, der angezeigt wird, wenn die Seite geladen wird
- **Hover** — Der Hintergrund, der angewendet wird, wenn ein Besucher den Mauszeiger über das Element bewegt

Zwei kleine Vorschaublöcke neben dem Schalter zeigen die aktuellen Hintergründe für **Normal** und **Hover** nebeneinander an, damit Sie den Kontrast auf einen Blick erkennen können. Konfigurieren Sie zunächst den **Normal**-Zustand, dann wechseln Sie zu **Hover**, um bei Bedarf einen interaktiven Effekt hinzuzufügen.

## Hintergrundtypen

Wählen Sie einen Hintergrundtyp aus der Reihe von Ikonen oben im Editorpanel aus:

| Typ | Beschreibung |
|------|-------------|
| **Farbe** | Eine feste Ausfüllung mit einem einzelnen Farbwert. Schnell anzuwenden und leichtgewichtig. |
| **Farbverlauf** | Ein sanfter Übergang zwischen zwei oder mehr Farben, entweder linear oder radial. Enthält eingebaute Voreinstellungen wie Ozean, Sonnenuntergang, Wald und Beere. Für fortgeschrittene Bearbeitung von Farbverläufen siehe das Thema [Farbverlaufsersteller](gradient-creator). |
| **Bild** | Ein hochgeladenes Bild oder eines, das aus der Medienbibliothek ausgewählt wird. Unterstützt Positionierung, Größenanpassung und Wiederholungsoptionen. |
| **Video** | Eine Hintergrundvideodatei mit einer optionalen Vorschau, die während des Ladens des Videos oder auf mobilen Geräten angezeigt wird. |

Nur ein Typ kann pro Zustand aktiv sein. Das Wechseln von Typen löscht nicht Ihre vorherige Konfiguration – Sie können zurückwechseln und Ihre Einstellungen werden beibehalten.

## Farbhintergründe

Wenn **Farbe** ausgewählt ist:

- **Hex-Eingabe** — Geben Sie einen Hex-Code direkt ein (z. B. `#1A1A2E`)
- **Farbpaletten** — Klicken Sie auf eine Voreinstellung, um schnell auszuwählen. Die Paletten sind themenbewusst und spiegeln die aktuelle Farbpalette Ihres Themes wider.
- **Bearbeiten**-Schaltfläche — Öffnet den vollständigen Farbauswahler mit Farbspektrum, Schiebereglern und Formatoptionen (siehe das Thema [Farbauswahler](color-picker))

Farbhintergründe werden sofort gerendert und haben keinen Leistungsverlust, wodurch sie ideal für Abschnitte, Karten und Container geeignet sind.

## Farbverlaufshintergründe

Wenn **Farbverlauf** ausgewählt ist:

- **Voreingestellte Farbverläufe** — Wählen Sie aus eingebauten Farbverläufen: Ozean, Sonnenuntergang, Wald, Beere und andere
- **Benutzerdefinierter Farbverlauf** — Klicken Sie auf **Bearbeiten**, um den Farbverlaufsersteller zu öffnen, in dem Sie Richtung, Typ (linear oder radial) und Farbstops festlegen können
- **Winkel-Schieberegler** — Ändern Sie die Richtung des Farbverlaufs für lineare Farbverläufe (0–360 Grad)

Farbverläufe fügen visuelle Tiefe hinzu, ohne Bildressourcen zu benötigen und passen sich perfekt jeder Bildschirmgröße an.

## Bildhintergründe

Wenn **Bild** ausgewählt ist:

- **Hochladen oder Medienbibliothek** — Klicken Sie auf den Bildplatzhalter, um ein neues Bild hochzuladen oder eines aus Ihrer Medienbibliothek auszuwählen
- **Größe** — Wählen Sie **Decken** (füllt das Element, kann kappen), **Enthalten** (passt in das Element) oder eine benutzerdefinierte Größe
- **Position** — Legen Sie den Fokuspunkt mit einem 9-Punkt-Grid fest (oben links, Mitte, unten rechts usw.) oder geben Sie benutzerdefinierte X/Y-Prozentwerte ein
- **Wiederholung** — Schalten Sie Wiederholung an oder aus. Nützlich für Muster, die sich wiederholen
- **Überlagerung** — Fügen Sie eine Farbüberlagerung über das Bild hinzu, mit anpassbarer Deckkraft, was nützlich ist, um die Lesbarkeit von Text sicherzustellen

Optimieren Sie immer Bilder, bevor Sie sie hochladen. Große, nicht komprimierte Bilder verlangsamen die Ladezeiten der Seite.

## Videohintergründe

Wenn **Video** ausgewählt ist:

- **Video-URL** — Geben Sie eine direkte URL zu einer MP4- oder WebM-Videodatei ein
- **Vorschubbild** — Laden Sie ein Fallbackbild hoch, das während des Ladens des Videos und auf Geräten angezeigt wird, die Videos nicht automatisch abspielen
- **Automatisch abspielen / Wiederholen / Stumm** — Videohintergründe werden standardmäßig automatisch abgespielt, wiederholt und sind stumm, um den Browser-Richtlinien zu entsprechen

Halten Sie Hintergrundvideos kurz (10–30 Sekunden), komprimiert und visuell subtil.


Sie sollten den Abschnitt verbessern, ohne den Inhalt zu beeinträchtigen.

## Wo es erscheint

Der Hintergrund-Editor ist für jedes Element verfügbar, das Hintergründe unterstützt:

- **Page Builder** — Abschnitte, Container, Spalten und Einzelelemente haben alle eine Hintergrund-Option im Stil-Tab
- **Header/Footer Builder** — Zeilenhintergründe und Hintergründe einzelner Widgets
- **Menu Builder** — Hintergründe des Menü-Containers und des Dropdown-Panels

Die gleiche Editor-Oberfläche wird überall verwendet, sodass Ihr Workflow bei allen Bausteinen konsistent bleibt.

## Tipps

- Verwenden Sie eine halbtransparente Farbschicht auf Bildhintergründen, um sicherzustellen, dass der Text unabhängig vom Bildinhalt lesbar bleibt.
- Farbverläufe sind eine schnelle Möglichkeit, visuelle Aufmerksamkeit zu erzeugen — wenden Sie einen an und passen Sie dann den Winkel oder die Farben an, um Ihrem Markenimage zu entsprechen.
- Legen Sie sowohl den Normal- als auch den Hover-Hintergrund für interaktive Karten fest, um Besuchern eine klare visuelle Rückmeldung zu geben, wenn sie Ihren Inhalt erkunden.
- Bei Bildhintergründen sollten Sie immer einen Fokuspunkt festlegen, damit der wichtigste Teil des Bildes auf allen Bildschirmgrößen sichtbar bleibt.
- Verwenden Sie bei Abschnitten, bei denen die Ladezeit kritisch ist, wie z. B. dem Inhalt über der Faltlinie, lieber Farben oder Farbverläufe als Bilder.
- Testen Sie Videohintergründe auf mobilen Geräten — die meisten mobilen Browser zeigen das Posterbild anstelle des Videos an.