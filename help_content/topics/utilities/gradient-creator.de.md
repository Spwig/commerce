---
title: Gradient Creator
---

Der Gradient Creator ermöglicht es Ihnen, sanfte Farbverläufe für Hintergründe von Elementen zu erstellen. Er wird über den Gradient-Tab im Hintergrund-Editor aufgerufen und öffnet sich als schwebendes Panel mit einer visuellen Farbverlauf-Leiste, Steuerelementen für Farbstops und vorgefertigten Optionen.

![Gradient Creator](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Zugriff auf den Gradient Creator

1. Wählen Sie ein Element im Page Builder oder im Header/Footer Builder aus
2. Öffnen Sie den **Style**-Tab im Eigenschafts-Panel
3. Klicken Sie auf den **Hintergrund**-Abschnitt, um den Hintergrund-Editor zu öffnen
4. Wechseln Sie zum **Gradient**-Tab
5. Das Panel des Gradient Creators öffnet sich mit einer Live-Vorschau und Bearbeitungssteuerelementen

## Live-Vorschau

Oben im Panel wird ein Vergleich nebeneinander angezeigt:

| Box | Zweck |
|-----|---------|
| **Current** | Der vorhandene Gradient (oder transparent, wenn keiner festgelegt ist) |
| **New** | Wird in Echtzeit aktualisiert, wenn Sie Änderungen vornehmen |

Eine Pfeil zwischen den beiden Boxen zeigt die Richtung der Änderung an.

## Gradient-Typen

Drei Gradient-Typen sind verfügbar, die über Tabs am oberen Rand des Editors ausgewählt werden können:

| Typ | Beschreibung | Steuerelemente |
|------|-------------|----------|
| **Linear** | Farbverläufe entlang einer geraden Linie | Winkel-Schieberegler (0–360 Grad) mit vorgefertigten Richtungstasten (nach oben, diagonal, nach rechts, nach unten, usw.) |
| **Radial** | Farbverläufe, die sich von einem Zentrum nach außen erstrecken | Form-Auswahl (Kreis oder Ellipse) und Position-Auswahl (Mitte, oben, unten, Ecken) |
| **Conic** | Farbverläufe, die sich um ein Zentrum drehen | Startwinkel-Schieberegler (0–360 Grad) und Position-Auswahl |

### Steuerelemente für die Richtung von Linear-Gradienten

Für Linear-Gradienten können Sie den Winkel auf drei Arten festlegen:
- **Winkel-Schieberegler** — ziehen Sie von 0 bis 360 Grad
- **Winkel-Eingabe** — geben Sie einen präzisen Gradwert ein
- **Vorgefertigte Schaltflächen** — klicken Sie auf Pfeil-Symbole für gängige Richtungen (nach oben, nach oben-rechts, nach rechts, nach unten-rechts, nach unten, nach unten-links, nach links, nach oben-links)

## Farbstops

Die Farbverlauf-Leiste zeigt Ihre aktuellen Farbstops als ziehbare Markierungen an. Jeder Stop definiert eine Farbe an einer bestimmten Position entlang des Verlaufs.

**Hinzufügen von Stops** — Klicken Sie auf die **+**-Schaltfläche im Abschnitt *Farbstops*, um einen neuen Stop hinzuzufügen. Es gibt keine feste Obergrenze für die Anzahl der Stops.

**Bearbeiten von Stops** — Jeder Stop in der Liste zeigt:
- Eine Farbpalette, die den Farb-Auswahl-Editor öffnet, wenn sie geklickt wird
- Ein Positions-Wert (0 % bis 100 %), den Sie eingeben oder anpassen können
- Ein Opazitätssteuerung (0 bis 1)
- Eine Löschen-Schaltfläche, um den Stop zu entfernen

**Sortieren** — Ziehen Sie Stops entlang der Farbverlauf-Leiste, um sie visuell neu zu ordnen.

## Gradient-Vorlagen

Sechs eingebaute Vorlagen sind für schnellen Start verfügbar. Klicken Sie auf eine Vorlage, um sie sofort anzuwenden:

| Vorlage | Farben | Winkel |
|--------|--------|-------|
| **Ocean** | Hellblau zu Blau | 120 Grad |
| **Sunset** | Warmes Orange zu Kirschrosa (3 Stops) | 45 Grad |
| **Forest** | Indigo zu Smaragdgrün | 135 Grad |
| **Berry** | Rosa zu Violett-Blau | 90 Grad |
| **Flame** | Rot zu Goldgelb | 45 Grad |
| **Night** | Dunkler Schiefer zu Ozeanblau | 180 Grad |

Vorlagen sind nur Ausgangspunkte. Nachdem Sie eine angewendet haben, können Sie die Farben bearbeiten, Stops hinzufügen oder entfernen und den Winkel ändern, um Ihre eigene Variante zu erstellen.

## Fußleiste-Aktionen

| Schaltfläche | Aktion |
|--------|--------|
| **Löschen** | Entfernt den Gradient vollständig und setzt ihn auf transparent zurück |
| **Anwenden** | Speichert den Gradient und schließt den Editor |

Der Editor wird ohne Klick auf *Anwenden* geschlossen, und Ihre Änderungen werden verworfen.

## Wo es verwendet wird

Der Gradient Creator wird verwendet in:

- **Page Builder** — über den Gradient-Tab im Hintergrund-Editor für jedes Element
- **Header/Footer Builder** — für Gradient-Hintergründe in Header-Bereichen, Navigationsschaltflächen und Footer-Bereichen

Er arbeitet zusammen mit dem Hintergrund-Editor, der auch feste Farben, Bilder und Video-Hintergründe anbietet.

## Tipps

- **Beginnen Sie mit einer Vorlage** — wenden Sie eine Vorlage an, die sich Ihrem Ziel nahe ist, und passen Sie dann die Farben und den Winkel an, anstatt von Grund auf zu beginnen.
- **Verwenden Sie zwei oder drei Stops** — einfache Gradienten mit zwei Stops wirken sauber und professionell. Mehr Stops sind für komplexe Effekte nützlich, können aber schnell überwältigend wirken.
- **Passen Sie Ihre Markenfarben an** — verwenden Sie den Farb-Auswahl-Editor, um genaue Hex-Werte aus Ihrem Markenpalette einzugeben, um konsistente, markenkonforme Gradienten zu erstellen.
- **Testen Sie mit Inhalten** — Gradienten, die allein beeindruckend wirken, können die Lesbarkeit von Text reduzieren. Prüfen Sie immer, ob Text über Gradienten-Hintergründen ausreichend Kontrast aufweist.
- **Probieren Sie radial für Spotlight-Effekte** — radialer Gradient eignet sich gut, um Aufmerksamkeit auf einen Zentrumsbereich zu lenken, wie z. B. einen Fokusbereich in einem Hero-Section.
