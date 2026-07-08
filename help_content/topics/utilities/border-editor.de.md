---
title: Rand-Editor
---

Der Rand-Editor bietet feine Steuerung über die Ränder von Elementen, einschließlich Stil, Farbe, Breite pro Seite und Eckradius pro Ecke. Er öffnet sich als schwebendes Panel mit einer Live-Vorschau und zwei Registerkarten für grundlegende und erweiterte Einstellungen.

![Rand-Editor](/static/core/admin/img/help/border-editor/border-editor.webp)

## Live-Vorschau

Ein Vorschau-Box am oberen Rand des Editors zeigt Ihre Änderungen an den Rändern in Echtzeit. Die Box zeigt das Wort "Vorschau" in einem gerahmten Rechteck an, das sich sofort aktualisiert, wenn Sie Stil, Farbe, Breite und Radius-Werte anpassen.

## Grundlegend vs. Erweitert

Der Editor ist in zwei Registerkarten organisiert:

| Registerkarte | Was es enthält |
|---------------|----------------|
| **Grundlegend** | Randstil, Farbe, Breite (mit Steuerung pro Seite), und Eckradius (mit Steuerung pro Ecke) |
| **Erweitert** | Feine Anpassung der einzelnen Eckradien und das experimentelle Eigenschaft **Eckform** |

Die meisten Arbeiten an Rändern werden vollständig im Registerkarte **Grundlegend** durchgeführt. Das Registerkarte **Erweitert** ist nützlich, wenn Sie präzise Steuerung über einzelne Ecken benötigen oder neue CSS-Funktionen ausprobieren möchten.

## Randstil

Ein Dropdown mit neun Optionen, die das Erscheinungsbild der Randlinie steuern:

| Stil | Beschreibung |
|------|-------------|
| **Keiner** | Kein Rand (entfernt jeden vorhandenen Rand) |
| **Einheitlich** | Eine einzelne kontinuierliche Linie (Standard) |
| **Strich** | Eine Reihe kurzer Striche |
| **Punkt** | Eine Reihe runder Punkte |
| **Doppelt** | Zwei parallele Einheitliche Linien |
| **Gefurcht** | Ein geschnitzter, 3D-Effekt-Rand, der in die Oberfläche eingeschnitten wirkt |
| **Erhöht** | Ein aufgeraumer, 3D-Effekt-Rand (Gegenstück zu gefurcht) |
| **Eingebettet** | Macht das Element so aussehen, als sei es eingebettet oder eingeschnitten |
| **Erhöht** | Macht das Element so aussehen, als sei es aufgerichtet oder herausgehoben |

Wenn Sie den Stil auf **Keiner** setzen, wird der Rand vollständig entfernt, unabhängig von den Einstellungen für Breite oder Farbe.

## Randfarbe

Ein Texteingabefeld mit einem Farbauswahl-Button. Geben Sie einen Hex-Wert direkt ein (z. B. `#3b82f6`) oder klicken Sie auf das Farbfeld, um den vollständigen Farbauswahl-Editor mit Hex-, RGB- und HSL-Eingabemodus sowie einem visuellen Farbbereich zu öffnen. Die Standardfarbe ist schwarz (`#000000`).

## Randbreite

Steuerung der Dicke des Rands in Pixel. Das Registerkarte **Grundlegend** zeigt vier separate Eingabefelder für die Seiten an:

| Seite | Eingabe |
|------|---------|
| **Oben** | Numerischer Eingabe, Minimum 0 |
| **Rechts** | Numerischer Eingabe, Minimum 0 |
| **Unten** | Numerischer Eingabe, Minimum 0 |
| **Links** | Numerischer Eingabe, Minimum 0 |

Ein **Link-Wechsel-Button** (Ketten-Icon) neben dem Label steuert, ob alle vier Seiten verknüpft sind:

- **Verknüpft** (Standard) — Ändern eines Werts aktualisiert alle vier Seiten gleichzeitig
- **Nicht verknüpft** — Jede Seite kann eine andere Breite haben, was für Effekte wie nur einen unteren Rand oder eine linke Akzent-Rand nützlich ist

## Eckradius

Steuerung der Rundung jeder Ecke. Das Registerkarte **Grundlegend** zeigt vier Ecken-Eingabefelder an:

| Ecke | Bezeichnung |
|------|-----------|
| **Oben links** | TL |
| **Oben rechts** | TR |
| **Unten links** | BL |
| **Unten rechts** | BR |

Ein **Link-Wechsel-Button** funktioniert auf die gleiche Weise wie die Randbreite:

- **Verknüpft** (Standard) — Alle vier Ecken teilen sich den gleichen Radiuswert
- **Nicht verknüpft** — Jede Ecke kann einen anderen Radius haben

Häufige Radiuswerte:

| Wert | Effekt |
|------|--------|
| 0px | Scharpfe Ecken |
| 4-8px | Subtile Rundung, gut für Karten und Schaltflächen |
| 12-16px | Auffällige Rundung, ein moderner, weicher Look |
| 50% | Vollkreis oder Pill-Form (abhängig von den Elementabmessungen) |

Der Einheitenauswahl-Button unterstützt px, em, rem und % für beide Breite und Radiuswerte.

## Eckform (Erweitert)

Das Registerkarte **Erweitert** enthält eine experimentelle **Eckform**-Eigenschaft. Diese CSS-Funktion steuert, ob abgerundete Ecken die Standardrunde Form oder eine spitzeren "Scoop"-Form verwenden. Die Browserunterstützung ist begrenzt, und der Editor zeigt eine Kompatibilitätswarnung an, wenn der aktuelle Browser diese Eigenschaft nicht unterstützt.

## Fußleiste-Aktionen

| Schaltfläche | Aktion |
|--------------|--------|
| **Zurücksetzen** | Wendet alle Werte auf den Zustand zurück, in dem der Editor geöffnet wurde |
| **Abbrechen** | Schließt den Editor, ohne Änderungen anzuwenden |
| **Anwenden** | Speichert die Rand-Einstellungen und schließt den Editor |

## Wo erscheint es

Der Rand-Editor ist in mehreren Bauern verfügbar:

- **Seiten-Bauer** — wählen Sie jedes Element aus, öffnen Sie das Registerkarte **Stil**, und klicken Sie auf den Abschnitt **Rand**
- **Header/Footer-Bauer** — fügen Sie Ränder zu Header-Elementen, Navigation-Containern und Footer-Bereichen hinzu
- **Menü-Bauer** — gestalten Sie Ränder an Menüelementen und Dropdown-Containern

Der Editor liest die aktuellen berechneten Randstile aus dem lebenden Element auf dem Canvas, sodass er immer mit den richtigen vorhandenen Werten geöffnet wird.

## Tipps

- **Verwenden Sie Ränder sparsam** — subtile 1px-Ränder in einem hellen Grau erzeugen eine saubere Trennung zwischen Abschnitten, ohne visuelle Gewichtung hinzuzufügen.
- **Kombinieren Sie Radius mit Schatten** — abgerundete Ecken, die mit einem weichen Boxschatten (über den Schatten-Editor) kombiniert werden, erzeugen einen polierten Karten-Effekt.
- **Probieren Sie Einzelseiten-Ränder aus** — trennen Sie die Seiten und setzen Sie nur einen unteren oder linken Rand für Akzentlinien, Abschnittstrenner oder Seitenleisten-Indikatoren.
- **Verwenden Sie Prozent-Radien für Pill-Formen** — setzen Sie alle Ecken auf 50% für eine Schaltfläche oder ein Badge, um eine Pill-Form zu erstellen, die sich an jede Inhaltsgröße anpasst.
- **Überprüfen Sie die Vorschau** — das Live-Vorschau-Feld aktualisiert sich sofort, also experimentieren Sie frei, bevor Sie anwenden.
