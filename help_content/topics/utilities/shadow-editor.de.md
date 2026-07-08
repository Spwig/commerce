---
title: Schatten-Editor
---

Der Schatten-Editor ermöglicht es Ihnen, Tiefe und Dimension zu Elementen hinzuzufügen, indem Sie konfigurierbare Kastenschatten und Textschatten verwenden. Schatten schaffen eine visuelle Hierarchie, lenken die Aufmerksamkeit auf wichtige Elemente und verleihen Ihrem Online-Shop ein poliertes, modernes Aussehen. Öffnen Sie den **Stil-Tab** eines Elements und suchen Sie nach der Gruppe **Effekte**, um den Schatten-Editor zu öffnen.

![Schatten-Editor](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Schattentypen

Der Editor bietet zwei Registerkarten oben:

- **Kastenschatten** — Fügt einen Schatten um den gesamten Bounding-Box des Elements hinzu. Verwenden Sie dies für Karten, Schaltflächen, Container, Bilder und Abschnitte.
- **Textschatten** — Fügt einen Schatten hinter die Textzeichen hinzu. Verwenden Sie dies für Überschriften oder Text, der auf Bildern überlagert ist, um die Lesbarkeit zu verbessern.

Jede Registerkarte hat ihre eigene unabhängige Konfiguration. Sie können sowohl einen Kastenschatten als auch einen Textschatten auf dasselbe Element anwenden, wenn dies erforderlich ist.

## Schatten-Eigenschaften

Jeder Schatten-Schicht wird durch die folgenden Eigenschaften definiert:

| Eigenschaft | Beschreibung | Bereich |
|-------------|--------------|--------|
| **Offset X** | Horizontale Distanz des Schattens vom Element | -50px bis 50px |
| **Offset Y** | Vertikale Distanz des Schattens vom Element | -50px bis 50px |
| **Unschärfe-Radius** | Bestimmt, wie weich oder diffus der Schattenrand erscheint. Höhere Werte erzeugen weichere Schatten. | 0px bis 100px |
| **Ausdehnungs-Radius** | Erweitert oder verkleinert die Schattengröße im Verhältnis zum Element (nur Kastenschatten) | -50px bis 50px |
| **Farbe** | Die Schattenfarbe, konfigurierbar mit voller Opazität über den Farbauswahl-Button | Jede Farbe mit Alpha-Wert |
| **Einbetten** | Schalter, um den Schatten innerhalb des Elements anstelle von außen anzuzeigen (nur Kastenschatten) | An/Aus |

Passen Sie die Werte mithilfe der Schieberegler an oder geben Sie präzise Zahlen direkt in die Eingabefelder ein.

## Mehrere Schatten

Sie können mehrere Schatten-Schichten auf ein einzelnes Element stapeln, um komplexe, realistische Tiefeffekte zu erstellen:

- Klicken Sie auf den **+**-Button, um eine neue Schatten-Schicht hinzuzufügen
- Jede Schicht wird als Zeile in der Schatten-Liste angezeigt und hat eigene Steuerelemente
- Ziehen Sie Schichten, um sie zu sortieren — Schatten werden in der Reihenfolge der Liste gerendert, wobei die erste Schicht oben liegt
- Schalten Sie den **Auge-Icon** auf einer Schicht um, um sie vorübergehend zu verbergen, ohne die Konfiguration zu löschen
- Klicken Sie auf das **Müll-Icon**, um eine Schicht zu entfernen

Die Kombination eines engen, dunklen Schattens mit einem weiten, weichen Schatten erzeugt einen natürlichen "angehobenen" Effekt, der die physische Tiefe nachahmt.

## Schatten-Voreinstellungen

Voreinstellungen mit schnellem Anwenden ermöglichen es Ihnen, gängige Schattenstile mit einem Klick hinzuzufügen:

| Voreinstellung | Beschreibung |
|----------------|-------------|
| **Klein** | Subtiler, nahe Schatten für eine leichte Erhöhung (Karten, Eingabefelder) |
| **Mittel** | Mäßige Tiefe für interaktive Elemente (Schaltflächen, Dropdowns) |
| **Groß** | Prominenter Schatten für schwebende Elemente (Modals, Popovers) |
| **Weich** | Breite Unschärfe mit geringer Opazität für einen sanften, diffusen Glanz |
| **Schwer** | Minimale Unschärfe mit höherer Opazität für einen scharfen, definierten Rand |
| **Einbetten** | Innerer Schatten für einen gedrückten oder eingesunkenen Erscheinungsbild |

Nachdem Sie eine Voreinstellung angewendet haben, können Sie einzelne Eigenschaften anpassen, um das Ergebnis feiner zu justieren.

## Aktueller vs. Neuer Vorschau

Am unteren Rand des Editors werden zwei Vergleichsfenster angezeigt, die den **aktuellen** Schatten (wie gespeichert) und den **neuen** Schatten (Ihre noch nicht gespeicherten Änderungen) darstellen. Diese Seite-zu-seite-Ansicht macht es einfach, den Unterschied vor dem Speichern zu bewerten. Klicken Sie auf **Anwenden**, um die Änderungen zu akzeptieren, oder klicken Sie anderswo, um sie zu verworfen.

## Wo es erscheint

Der Schatten-Editor ist an folgenden Stellen verfügbar:

- **Seiten-Builder** — Stil-Tab, Effekte-Gruppe auf Abschnitten, Containern, Spalten und einzelnen Elementen
- **Header/Footer-Builder** — Schatten-Einstellungen auf Widget-Ebene für Elemente wie Logos, Suchleisten und Navigationselemente

Jedes Element, das die Effekte-Stil-Gruppe unterstützt, zeigt die Steuerelemente des Schatten-Editors.

## Tipps

- Verwenden Sie subtile Schatten (Klein- oder Weich-Voreinstellungen) für die meisten Elemente — schwere Schatten können das Design überladen.
- Kombinieren Sie einen nahen, dunklen Schatten mit einem entfernten, hellen Schatten für den natürlichsten Erhöhungseffekt.
- Einbettungsschatten eignen sich gut für Eingabefelder und Container, um einen "vertieften" Panel-Effekt zu erzeugen.
- Textschatten sollten minimal sein — ein 1px-Offset mit leichter Unschärfe verbessert die Lesbarkeit auf Bildhintergründen, ohne altmodisch zu wirken.
- Testen Sie Ihre Schatten sowohl auf hellen als auch dunklen Hintergründen, wenn Ihr Theme eine Dunkelmodus-Option unterstützt.
