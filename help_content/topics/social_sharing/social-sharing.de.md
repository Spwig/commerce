---
title: Soziale Teilen
---

Soziale Teilen-Buttons ermöglichen es Kunden, Ihre Produkte, Blogbeiträge und Seiten direkt von Ihrem Online-Shop auf soziale Netzwerke zu teilen. Sie bestimmen, welche Plattformen angezeigt werden, wie die Buttons aussehen, wo sie platziert werden und ob das Teilen aktiviert und gezählt wird.

## Konfigurieren der sozialen Teilen-Einstellungen

Alle sozialen Teilen-Verhaltensweisen werden über eine einzige Einstellungsseite gesteuert. Navigieren Sie zu **Marketing > Soziale Teilen-Einstellungen** (die Seite leitet automatisch zum Einstellungsformular weiter – es gibt nur ein Einstellungsprotokoll).

### Platzierung: Wo die Buttons erscheinen

Der Abschnitt **Platzierung** steuert, welche Arten von Inhalten automatisch Teilen-Buttons anzeigen.

| Einstellung | Beschreibung |
|---------|-------------|
| **Auf Produkten aktivieren** | Teilen-Buttons auf Produktseiten anzeigen |
| **Auf Kategorien aktivieren** | Teilen-Buttons auf Kategorielisten-Seiten anzeigen |
| **Auf Blogbeiträgen aktivieren** | Teilen-Buttons auf Blogbeitragsseiten anzeigen |
| **Auf benutzerdefinierten Seiten aktivieren** | Teilen-Buttons auf benutzerdefinierten Shopseiten anzeigen |

Markieren Sie die Inhaltstypen, an denen Sie Buttons haben möchten. Sie können jede Kombination aktivieren – beispielsweise nur Produkte und Blogbeiträge.

**Platzierung Position** steuert, wo auf der Seite die Buttons angezeigt werden:

| Option | Beschreibung |
|--------|-------------|
| **Unten am Inhalt** (Standard) | Nach dem Hauptinhalt angezeigt |
| **Oben am Inhalt** | Vor dem Hauptinhalt angezeigt |
| **Seitenleiste** | In der Seitenleiste angezeigt |
| **Schwebend (fest)** | An der Seite des Bildschirms befestigt, während der Besucher scrollt |

### Erscheinungsbild: Wie die Buttons aussehen

Der Abschnitt **Erscheinungsbild** steuert, welche Plattformen angezeigt werden und wie die Buttons gestaltet werden.

**Aktivierte Plattformen** – lassen Sie dies leer, um alle unterstützten Plattformen anzuzeigen, oder geben Sie ein JSON-Array an, um die angezeigten Plattformen einzuschränken:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Unterstützte Plattformschlüssel: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Button-Stil**-Optionen:

| Stil | Beschreibung |
|-------|-------------|
| **Nur Icon** (Standard) | Nur das Plattform-Icon anzeigt |
| **Icon + Bezeichnung** | Zeigt das Icon und den Plattformnamen an |
| **Nur Bezeichnung** | Zeigt nur den Plattformnamen als Text an |

**Button-Größe** – wählen Sie **Klein**, **Mittel** (Standard) oder **Groß**, um dem Design Ihres Online-Shops zu entsprechen.

**Layout-Richtung** – ordnen Sie die Buttons **Horizontal** (Standard, nebeneinander) oder **Vertikal** (gestapelt) an.

**Titel anzeigen** – wenn aktiviert, erscheint eine "Teilen"-Überschrift über der Gruppe der Buttons.

**Mobile-Ansicht** steuert die Anzeige der Buttons auf kleineren Bildschirmen:

| Option | Beschreibung |
|--------|-------------|
| **Immer anzeigen** (Standard) | Buttons sind auf allen Geräten sichtbar |
| **Auf Mobilgeräten ausblenden** | Buttons werden auf mobilen Geräten ausgeblendet |
| **Nur auf Mobilgeräten** | Buttons werden nur auf mobilen Geräten angezeigt |

### Tracking-Einstellungen

**Teilen-Zähler anzeigen** – wenn aktiviert, erscheint ein Zähler auf jedem Button, der anzeigt, wie oft diese Plattform geteilt wurde. Die Zähler werden in Echtzeit aktualisiert, sobald Teilenvorgänge erfasst werden.

**Teilen verfolgen** – wenn aktiviert, wird jeder Klick auf Teilen in den Teilen-Analysen erfasst. Das Deaktivieren dieser Funktion stoppt die Speicherung neuer Datensätze, löscht aber keine bestehenden Daten. Das Tracking verleiht auch Treueabzeichen an Kunden, die teilen (wenn das Treueprogramm aktiv ist).

Klicken Sie auf **Speichern** am unteren Rand des Formulars, um Ihre Änderungen anzuwenden. Die Einstellungen wirken sich sofort aus.

## Anzeigen von Teilen-Aktivitäten

### Einzelne Teilen-Events

Navigieren Sie zu **Marketing > Soziale Teilen**, um ein Protokoll aller erfassten Teilen-Events anzuzeigen. Jeder Eintrag zeigt:

- **Plattform** – welches soziale Netzwerk verwendet wurde (als farbcodiertes Badge angezeigt)
- **Geteiltes Inhalt** – der Typ und Name des geteilten Inhalts (z. B. `product: Blue Widget`)
- **Nutzer** – der Kunde, der geteilt hat, oder "Anonym" für Besucher, die nicht angemeldet waren
- **Geräteart** – Desktop, Mobilgerät oder Tablet
- **Geteilt am** – Datum und Uhrzeit des Teils

Das Teilen-Protokoll ist schreibgeschützt – Einträge werden automatisch erstellt, wenn Kunden auf Teilen-Buttons klicken.

Verwenden Sie die Filter **Plattform** und **Geräteart**, um Teilenmuster zu erkunden, und die Datenhierarchie, um bestimmte Zeiträume zu betrachten.

### Teilezahlen nach Inhalt

Navigieren Sie zu **Marketing > Teilezahlen**, um aggregierte Teilezahlen anhand von Inhaltselementen und Plattformen anzuzeigen. Diese Ansicht ermöglicht es Ihnen, Ihre am häufigsten geteilten Produkte und Beiträge schnell zu erkennen.

Jahr Eintrag zeigt:
- **Inhalt** — der Typ und Name des Elements (z. B. `product: Blue Widget`)
- **Plattform** — das soziale Netzwerk
- **Teilezahl** — Gesamtzahl der Teile auf dieser Plattform
- **Zuletzt aktualisiert** — wann die Zahl zuletzt neu berechnet wurde

Die Liste ist nach Teilezahl absteigend sortiert, sodass Ihr viralster Inhalt oben angezeigt wird. Teilezahlen werden automatisch aktualisiert, sobald ein neues Teileereignis aufgezeichnet wird — es ist keine manuelle Aktualisierung erforderlich.

## Verständnis davon, wie Teile verfolgt werden

Wenn ein Kunde auf eine Teilen-Schaltfläche klickt, protokolliert Spwig:

1. Welche Plattform er genutzt hat
2. Welchen Inhalt er geteilt hat (Produkt, Blogbeitrag, Seite usw.)
3. Ob er angemeldet war (wenn ja, wird das Teilen mit seinem Konto verknüpft, um Loyalty-Integration zu ermöglichen)
4. Seine Geräteart
5. Die URL, die geteilt wurde

Die Teilezahl für diese Plattform und dieses Inhaltselement wird dann automatisch erhöht. Wenn **Teilezahlen anzeigen** aktiviert ist, erscheint die aktualisierte Zahl auf der Schaltfläche, sobald die Seite erneut geladen wird.

## Loyalty-Integration

Wenn Ihr Loyalty-Programm aktiv ist und **Teile verfolgen** aktiviert ist, erhalten angemeldete Kunden Loyalty-Abzeichen, wenn sie Inhalt teilen. Das soziale Teilen-Abzeichen ist Teil der regelbasierten Aktionen des Loyalty-Programms.

Um Punkte für das Teilen zu konfigurieren, navigieren Sie zu **Kunden > Loyalty-Regeln** und suchen Sie nach Regeln mit dem Typ **Aktionenbasiert** und der Aktion **Soziales Teilen**.

## Tipps

- Aktivieren Sie zuerst das Teilen für Produkte und Blogbeiträge — diese Inhaltstypen werden am wahrscheinlichsten organisch geteilt
- Pinterest ist besonders wertvoll für visuelle Produktkategorien wie Mode, Einrichtung und Essen — priorisieren Sie es in der Liste `enabled_platforms` für diese Geschäfte
- Das Teilen über WhatsApp führt zu starken Konversionen durch warme Empfehlungen, insbesondere auf mobilen Geräten; erwägen Sie die Verwendung des **Nur Mobil**-Anzeigemodus für WhatsApp, während Sie andere Plattformen auf allen Geräten sichtbar lassen
- Wenn Sie bemerken, dass die Teilezahlen zu hoch sind, prüfen Sie, ob Testverkehr (aus Admin-Sitzungen) vor dem vollständigen Funktionieren des **Ist Admin-Verkehr**-Flags gezählt wurde — Sie können die Zahlen zurücksetzen, indem Sie Einträge aus der Teilen-Analyse löschen
- Überprüfen Sie die Liste der Teilezahlen monatlich, um Ihre am häufigsten geteilten Produkte zu identifizieren und sie auf Ihrer Startseite oder in Marketing-E-Mails stärker in den Vordergrund zu stellen