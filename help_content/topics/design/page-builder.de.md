---
title: Seiten-Editor
---

Der Seiten-Editor ist ein visueller Drag-and-Drop-Editor zur Erstellung reicher, responsiver Seiten ohne Code-Schreiben. Fügen Sie Elemente aus einer Bibliothek mit 39 Komponenten hinzu, stylen Sie sie mit leistungsstarken Utilities, richten Sie Animationen und Sichtbarkeitsregeln ein und veröffentlichen Sie sie mit voller Versionsgeschichte.

![Seiten-Editor](/static/core/admin/img/help/page-builder/builder-overview.webp)

## Die Builder-Oberfläche

Der Builder hat vier Hauptbereiche:

| Bereich | Ort | Zweck |
|--------|-----|-------|
| **Symbolleiste** | Obere Leiste | Gerätevorschau (Desktop/Tablet/Handy), Rückgängig/Wiederherstellen, Seiten-Einstellungen, Entwurf speichern, veröffentlichen |
| **Elementbibliothek** | Linken Seitenleistenbereich | Durchsuchen und ziehen Sie 39 Elemente, die in 9 Kategorien organisiert sind |
| **Canvas** | Mitte | Live WYSIWYG-Editierbereich – sehen Sie die Änderungen, während Sie sie vornehmen |
| **Eigenschaften-Panel** | Rechten Seitenleistenbereich | Bearbeiten Sie den Inhalt, das Styling, die Animationen und die erweiterten Einstellungen des ausgewählten Elements |

## Elementbibliothek

Elemente sind in Kategorien organisiert. Ziehen Sie jedes Element aus der Bibliothek auf das Canvas, um es auf Ihre Seite zu fügen.

| Kategorie | Elemente |
|----------|----------|
| **Layout** | Container, Trenner, Hero-Bereich, Modal-Beitrag, Navigation-Menü, Abstand |
| **Grundlegend** | Überschrift, Text, Schaltfläche, Icon |
| **Inhalt** | Blog-Beitrag-Karussell, Blog-Beitrag-Grid, FAQ-Accordion, Verwandte Beiträge, Zeugnisse |
| **Medien** | Bild, Bildgalerie, Bild-Accordion, Video-Einbettung |
| **Formulare** | Kontaktformular, Formular, Newsletter-Anmeldung |
| **Marketing** | Countdown-Timer, CTA-Banner, Blog-Banner, Treue-Banner, Werbebanner, Vertrauens-Siegel, Gutschein-Code-Anzeige |
| **E-Commerce** | Kategorie-Präsentation, Geschenkkarte-Präsentation, Produkt-Karussell, Produkt-Grid, Produkt-Liste, Bewertungen-Anzeige, Verkaufsprodukte, Store-Locator |
| **Sozial** | Sozial-Links |
| **Navigation** | Suchleiste |

### Container und Verschachtelung

Das **Container**-Element ist die Grundlage für komplexe Layouts. Container können andere Elemente – einschließlich anderer Container – enthalten, wodurch Sie mehrspaltige Grids und verschachtelte Strukturen erstellen können. Nutzen Sie die Layout-Vorgaben des Containers, um gängige Spaltenanordnungen schnell einzurichten (50/50, 33/33/33, 25/75 usw.).

## Elemente hinzufügen

1. Finden Sie das gewünschte Element in der linken Seitenleiste
2. **Ziehen** Sie es auf das Canvas und platzieren Sie es dort, wo Sie es haben möchten
3. Elemente können zwischen bestehenden Elementen oder innerhalb von Containern abgelegt werden
4. Die blaue Einfügeleiste zeigt an, wo das Element landen wird
5. Nach dem Ablegen wird das Element automatisch ausgewählt und das Eigenschaften-Panel öffnet sich

Sie können auch Elemente durch Ziehen nach oben oder unten auf dem Canvas neu anordnen.

## Inhalt bearbeiten

Wählen Sie jedes Element auf dem Canvas aus, um seine Eigenschaften im rechten Panel zu öffnen. Der **Inhalt**-Reiter zeigt Felder, die spezifisch für diesen Elementtyp sind.

![Eigenschaften-Panel](/static/core/admin/img/help/page-builder/properties-panel.webp)

Beispiel:
- **Überschrift** – Text, HTML-Tag (H1–H6), Ausrichtung, Anker-ID
- **Bild** – Bildquelle (Medienbibliothek), Alternativtext, Link, Größenanpassung
- **Schaltfläche** – Beschriftung, URL, Stil-Variante, Icon
- **Produkt-Grid** – Datensource, Anzahl der Spalten, Produkte pro Seite, Sortierreihenfolge
- **Hero-Bereich** – Titel, Untertitel, Beschreibung, Hintergrund, CTA-Schaltflächen

Übersetzbare Inhaltsfelder zeigen ein Übersetzungssymbol – klicken Sie darauf, um Übersetzungen für mehrsprachige Stores hinzuzufügen.

## Styling von Elementen

Der **Stil**-Reiter bietet visuelle Steuerelemente für jedes Element. Jeder Abschnitt öffnet einen dedizierten Utility-Editor.

![Stil-Reiter](/static/core/admin/img/help/page-builder/style-tab.webp)

| Abschnitt | Was es steuert | Utility |
|----------|----------------|--------|
| **Typografie** | Schriftfamilie, Größe, Gewicht, Zeilenhöhe, Buchstabenabstand, Textstil | Typografie-Editor |
| **Farben** | Textfarbe mit Hex/RGB/HSL-Eingabe und Theme-Tokens | Farbauswahl |
| **Hintergrund** | Festen Farbe, Farbverlauf, Bild- oder Videohintergrund mit Hover-Zuständen | Hintergrund-Editor |
| **Rand** | Randbreite, Stil, Farbe und Radius pro Seite | Rand-Editor |
| **Abstand** | Abstand und Puffer mit visuellem Box-Modell-Editor | Abstand-Editor |
| **Effekte** | Boxschatten mit Vorgaben und Unterstützung für mehrere Schichten, Opazitäts-Schieberegler | Schatten-Editor |

Jeder Utility ist in seinem eigenen Hilfe-Thema dokumentiert – suchen Sie nach "Farbauswahl", "Hintergrund-Editor" usw., um mehr zu erfahren.

## Animationen

Der **Animationen**-Reiter ermöglicht es Ihnen, Bewegung zu Elementen hinzuzufügen.

### Einführungsanimationen

Wird ausgelöst, wenn das Element in den Sichtbereich scrollt:

| Animation | Beschreibung |
|-----------|-------------|
| Einblenden | Schrittweise erscheint |
| Einblenden (Oben/Unten/Links/Rechts) | Schiebt sich von einer Richtung ein |
| Zoomen ein | Wächst von klein auf vollständige Größe |
| Einblenden mit Sprung | Springt an seinen Platz |
| Puls / Schütteln / Springen / Leuchten / Drehen | Aufmerksamkeitserregende Effekte |

Konfigurieren Sie **Dauer** (0,3s–1,5s), **Verzögerung** (0–1s), **Zeitfunktion** (leicht, ein, aus, linear) und **Wiederholung** (einmalig oder unendlich).

### Hover-Animationen

Wird ausgelöst, wenn ein Besucher über das Element hinhält:

| Effekt | Beschreibung |
|--------|-------------|
| Vergrößern / Verkleinern | Wächst oder schrumpft |
| Hochheben | Nach oben schwebt |
| Drehen (im Uhrzeigersinn / gegen den Uhrzeigersinn) | Drehen im Uhrzeigersinn oder gegen den Uhrzeigersinn |
| Helligkeit / Durchlässigkeit | Ändert Helligkeit oder Opazität |
| Schatten vergrößern | Schatten vergrößert |
| Hochheben mit Schatten | Steigt mit wachsendem Schatten |
| Puls-Vergrößerung / Verzerrung / Rand-Glow | Spezielle Effekte |

Konfigurieren Sie **Dauer**, **Zeitfunktion** und **Intensität** (subtil, normal, stark).

## Erweiterte Einstellungen

Der **Erweitert**-Reiter bietet feine Steuerung:

### Sichtbarkeitsregeln

Steuerung, wann ein Element angezeigt oder ausgeblendet wird, basierend auf Bedingungen:

- **Benutzerstatus** – angemeldet, abgemeldet, neuer Kunde, zurückkehrender Kunde
- **Gerät** – Desktop, Tablet, Handy
- **Zeit** – Datumsbereich, Uhrzeit des Tages, Tag der Woche
- **Kundengruppe** – VIP, Großhandel usw.
- **Warenkorbwert** – Mindest- oder Höchstwert des Warenkorbs
- **Geografie** – Land, Region
- Und 20+ weitere Regeln

Regeln können mit AND/OR-Logik kombiniert werden, um komplexe Zielgruppen zu erstellen.

### Benutzerdefinierte CSS

| Feld | Zweck |
|-------|---------|
| **Element-ID** | Eindeutige ID für Ankerlinks oder CSS-Zielsetzung |
| **Benutzerdefinierte CSS-Klassen** | Zusätzliche Klassen, die angewendet werden sollen |
| **Benutzerdefinierte CSS-Stile** | Inline CSS für einmalige Überschreibungen |
| **Datenattribute** | Benutzerdefinierte data-*-Attribute als Schlüssel-Wert-Paare |
| **Z-Index** | Stapelreihenfolge für überlappende Elemente |

## Veröffentlichungsablauf

Seiten verwenden ein Entwurf/Veröffentlichungssystem mit voller Versionsgeschichte:

| Status | Bedeutung |
|--------|---------|
| **Entwurf** | Arbeit in Bearbeitung – nicht sichtbar für Besucher |
| **Veröffentlicht** | Live auf Ihrem Store |
| **Archiviert** | Von der Website entfernt, aber beibehalten |

### Wie es funktioniert

1. Ändern Sie im Builder – sie werden als **Entwurf** gespeichert
2. Klicken Sie auf **Entwurf speichern**, um ohne Veröffentlichung zu speichern
3. Klicken Sie auf **Veröffentlichen**, um den aktuellen Entwurf live zu machen
4. Jede Veröffentlichung erstellt eine **Versionssnapshot**
5. Sie können **wiederherstellen** jede frühere Version aus der Versionsgeschichte (Uhrsymbol in der Symbolleiste)

Das bedeutet, dass Sie frei experimentieren können – Ihre Live-Seite bleibt unverändert, bis Sie explizit veröffentlichen.

## Seitenvorlagen

Sparen Sie Zeit, indem Sie mit Vorlagen arbeiten:

- **Als Vorlage speichern** – speichern Sie das Design jeder Seite als wiederverwendbare Vorlage
- **Aus Vorlage erstellen** – starten Sie eine neue Seite von einer vorhandenen Vorlage
- **Vorlagenkategorien** – organisieren Sie Vorlagen nach Zweck (Landingpage, Über uns, Produktpräsentation usw.)

Vorlagen erfassen die vollständige Seitenstruktur, einschließlich aller Elemente, Inhalte und Styling.

## Responsive Design

Verwenden Sie die Gerätevorschau-Schaltflächen in der Symbolleiste, um zu sehen, wie Ihre Seite auf verschiedenen Bildschirmgrößen aussieht:

- **Desktop** – Vollbreitenschema
- **Tablet** – Mittlerer Bildschirmbereich
- **Handy** – Schmaler Bildschirmbereich

Elemente passen sich automatisch an, basierend auf den Einstellungen ihres Containers. Sie können auch Sichtbarkeitsregeln verwenden, um bestimmte Elemente auf bestimmten Geräten anzuzeigen oder auszublenden.

## Tipps

- **Beginnen Sie mit einem Container** – die meisten Layouts beginnen mit einem Container, um Spalten und Struktur zu erstellen. Nutzen Sie Layout-Vorgaben für gängige Anordnungen.
- **Verwenden Sie Hero-Bereiche für Seitenüberschriften** – das Hero-Element bietet Titel, Untertitel, Hintergrundbild und CTA-Schaltflächen in einem Komponenten.
- **Vorschau vor Veröffentlichung** – klicken Sie auf Vorschau, um zu sehen, was Besucher sehen werden, und veröffentlichen Sie dann, wenn Sie zufrieden sind.
- **Verwenden Sie Sichtbarkeitsregeln für Personalisierung** – zeigen Sie unterschiedlichen Inhalt für angemeldete vs. abgemeldete Besucher an oder richten Sie spezifische Kundengruppen aus.
- **Behalten Sie Animationen subtil** – eine oder zwei Einführungsanimationen pro Seitenabschnitt wirken professionell. Zu viele Animationen können überwältigend wirken.
- **Benennen Sie Ihre Container** – verwenden Sie das Feld Element-ID, um Container zu kennzeichnen (z. B. "hero-section", "features"), damit sie in komplexen Seiten leicht zu finden sind.
- **Testen Sie auf allen Geräten** – verwenden Sie die Gerätevorschau, um Ihre Layout auf Desktop, Tablet und Handy zu prüfen, bevor Sie veröffentlichen.
- **Nutzen Sie Vorlagen** – speichern Sie Ihre besten Seiten-Designs als Vorlagen, um die Erstellung zukünftiger Seiten zu beschleunigen.