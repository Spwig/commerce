---
title: Abstand-Editor
---

Der visuelle Abstand-Editor ermöglicht die Konfiguration von Abständen (Margin) und Paddings (Padding) mithilfe eines intuitiven Box-Modell-Diagramms. Präzise Abstandssteuerung gewährleistet konsistente Layouts und angenehme Leserfahrungen über Ihr Online-Shop-System. Öffnen Sie den **Stil-Tab** eines Elements und suchen Sie nach dem Abschnitt **Abstand**, um den Editor zu öffnen.

![Abstand-Editor](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Das Box-Modell-Diagramm

Der Editor zeigt ein visuelles Box-Modell mit drei ineinander verschachtelten Schichten:

- **Abstand (Margin)** (äußere Ring, typischerweise in Orange dargestellt) — Der Raum außerhalb des Element-Rahmens, der es von benachbarten Elementen trennt
- **Padding** (innerer Ring, typischerweise in Grün dargestellt) — Der Raum zwischen dem Element-Rahmen und dessen Inhalt
- **Inhalt (Content)** (Zentrum) — Der tatsächliche Inhalt des Elements, z. B. Text oder ein Bild

Jede Seite des Diagramms (oben, rechts, unten, links) hat einen ziehbaren Griff und eine numerische Eingabe. Ziehen Sie einen Griff nach außen, um den Wert zu erhöhen, oder nach innen, um ihn zu verringern. Sie können auch direkt auf den Wert einer Seite klicken, um eine präzise Zahl einzugeben.

## Abstand- und Padding-Registerkarten

Zwei Registerkarten oben im Editor wechseln zwischen den Ansichten **Abstand** und **Padding**. Wenn **Abstand** ausgewählt ist, wird der äußere Ring hervorgehoben und bearbeitbar. Wenn **Padding** ausgewählt ist, wird der innere Ring hervorgehoben und bearbeitbar. Der inaktive Ring bleibt sichtbar, um sich als Referenz zu dienen, ist aber abgedunkelt.

Beide Registerkarten teilen sich dieselben Steuerelemente und Einheitsoptionen, sodass der Workflow für die Konfiguration von Abständen und Padding identisch ist.

## Steuerung pro Seite

Jede Seite hat eine unabhängige Wert-Eingabe und eine Einheitenauswahl:

| Seite | Beschreibung |
|------|-------------|
| **Oben** | Abstand über dem Element (Abstand) oder über dem Inhalt (Padding) |
| **Rechts** | Abstand rechts vom Element oder Inhalt |
| **Unten** | Abstand unter dem Element oder Inhalt |
| **Links** | Abstand links vom Element oder Inhalt |

Klicken Sie auf den Wert einer Seite im Diagramm, um sie auszuwählen, und geben Sie eine Zahl ein oder verwenden Sie die Pfeiltasten nach oben/unten, um den Wert um 1 zu erhöhen. Halten Sie Shift gedrückt, während Sie die Pfeiltasten drücken, um den Wert um 10 zu erhöhen.

## Einheiten

Der Einheitenauswahler neben jeder Wert-Eingabe ermöglicht die Auswahl der Maßeinheit:

| Einheit | Beschreibung |
|------|-------------|
| **px** | Pixel. Fixe Größe, konsistent über alle Geräte. Bestens geeignet für präzise, kleine Abstandsangaben. |
| **em** | Relativ zur Schriftgröße des Elements. Skaliert sich mit Änderungen der Typografie. |
| **rem** | Relativ zur Wurzel-Schriftgröße. Gewährleistet eine konsistente Skalierung über die gesamte Seite. |
| **%** | Prozent des Breitens der Elternelement. Nützlich für flüssige, responsive Layouts. |
| **auto** | Lässt den Browser den Wert automatisch berechnen. Häufig verwendet für horizontale Zentrierung mit linken/rechten Abständen. |

Wählen Sie eine Einheit, die Ihrem Zweck entspricht — verwenden Sie `px` für feste Abstände, `rem` für skalierbare Abstände, die die Typografie-Token des Themes respektieren, und `%` für Layouts, die sich an die Breite des Containers anpassen müssen.

## Seiten verknüpfen

Ein **Link-Icon** in der Mitte des Diagramms schaltet den Verknüpfungsmodus um:

- **Verknüpft** (verknüpftes Ketten-Icon) — Ändern Sie den Wert einer Seite, um alle vier Seiten auf denselben Wert zu aktualisieren. Nützlich für gleichmäßige Abstände.
- **Nicht verknüpft** (gebrochenes Ketten-Icon) — Jede Seite wird unabhängig gesteuert. Verwenden Sie dies, wenn Sie unterschiedliche Werte für oben/unten und links/rechts benötigen.

Klicken Sie auf das Link-Icon, um zwischen den Modi zu wechseln. Wenn Sie von nicht verknüpft zu verknüpft wechseln, werden alle vier Seiten auf den Wert der zuletzt bearbeiteten Seite gesetzt.

## Schnellvorlagen

Eine Reihe von Schnellvorlagen-Buttons unter dem Diagramm bietet eine Ein-Klick-Abstands-Konfiguration:

| Vorlage | Werte |
|--------|--------|
| **Keine** | 0 auf allen Seiten |
| **Klein** | Kompakte Abstände, geeignet für enge Layouts und Inline-Elemente |
| **Mittel** | Ausgewogene Abstände für allgemeine Verwendung auf Karten und Abschnitten |
| **Groß** | Generöse Abstände für Hero-Bereiche und Abschnitte mit hohem Fokus |
| **XL** | Extra breite Abstände für Full-Width-Banner und Hauptseitenabschnitte |

Vorlagen gelten für die aktuell ausgewählte Registerkarte (Abstand oder Padding) und setzen alle vier Seiten gleichzeitig. Nach Anwendung einer Vorlage können Sie bei Bedarf einzelne Seiten anpassen.

## Wo es erscheint

Der Abstand-Editor ist für jedes Element verfügbar, das Layout-Abstände unterstützt:

- **Seiten-Builder** — Stil-Tab, Abstand-Abschnitt für Abschnitte, Container, Spalten und einzelne Elemente
- **Header/Footer-Builder** — Steuerung für Zeilen- und Widget-Abstände für vertikale und horizontale Lücken
- **Menü-Builder** — Padding-Einstellungen für Menüelemente und Rahmen-Abstände

Die gleiche Editor-Oberfläche wird in allen Bereichen verwendet, um eine konsistente Erfahrung über alle Builder hinweg zu gewährleisten.

## Tipps

- Verwenden Sie konsistente Abstandsangaben über Ihre Seiten — wählen Sie 2–3 Standardgrößen und verwenden Sie diese, um ein sauberes, professionelles Layout zu erzielen.
- Setzen Sie den Abstand auf **auto** für links und rechts, um ein festbreites Element horizontal im Elternelement zu zentrieren.
- Verwenden Sie `rem`-Einheiten für Abstände, wenn Ihr Theme responsive Typografie verwendet, damit sich die Abstände proportional zur Schriftgröße skalieren.
- Verwenden Sie den verknüpften Modus, um Padding schnell gleichmäßig zu setzen, und trennen Sie die Verknüpfung, um einzelne Seiten feiner anzupassen, wenn der Inhalt asymmetrische Abstände benötigt.
- Vermeiden Sie übermäßiges Padding auf mobilen Geräten — testen Sie Ihre Abstände bei schmalen Bildschirmbreiten, um sicherzustellen, dass der Inhalt nicht zusammengedrückt oder übermäßig gepaddet wird.