---
title: "Konfigurierbare Produkte"
---

Konfigurierbare Produkte ermoglichen es Kunden, ihr eigenes Produkt zu erstellen, indem sie Optionen aus verschiedenen Konfigurationsplatzen wahlen. Dies ist ideal fuer Build-to-Order-Artikel wie individuelle PCs, personalisierte Geschenkboxen oder massgefertigte Moebel, bei denen jede Komponente ein echtes Produkt in Ihrem Katalog ist.

![Product configurator admin](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Wie es Funktioniert

Ein konfigurierbares Produkt besteht aus **Platzen** (Kategorien von Auswahlmoeglichkeiten) und **Optionen** (die tatsaechlichen Produkte, die Kunden waehlen koennen). Zum Beispiel koennte ein individueller PC Plaetze fuer Prozessor, Grafikkarte, RAM und Speicher haben — jeder Platz enthaelt mehrere Produktoptionen zur Auswahl.

## Preisstrategien

Waehlen Sie, wie der Endpreis berechnet wird:

| Strategie | Beschreibung |
|-----------|-------------|
| **Summe der Komponenten** | Endpreis = Summe aller ausgewaehlten Optionspreise. Kein Basispreis erforderlich. |
| **Basispreis + Anpassungen** | Beginnen Sie mit dem Basispreis des Produkts, dann addieren/subtrahieren Sie Preisanpassungen pro Option. |
| **Festpreis** | Ein Pauschalpreis unabhaengig davon, welche Optionen der Kunde waehlt. |

## Einrichtung eines Konfigurierbaren Produkts

### Schritt 1: Produkt Erstellen

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt Hinzufuegen**
2. Setzen Sie den **Produkttyp** auf **Konfigurierbares Produkt**
3. Waehlen Sie Ihre **Preisstrategie** (Summe der Komponenten ist am gaengigsten)
4. Fuellen Sie den Produktnamen, die Beschreibung und andere grundlegende Details aus
5. Speichern Sie das Produkt

### Schritt 2: Konfigurationsplaetze Hinzufuegen

Nach dem Speichern wechseln Sie zum Tab **Konfiguration**, um Ihre Plaetze einzurichten.

1. Klicken Sie auf **+ Platz Hinzufuegen**, um eine neue Konfigurationskategorie zu erstellen
2. Konfigurieren Sie fuer jeden Platz:
   - **Name** — Was der Kunde sieht (z.B. "Prozessor", "Farbe")
   - **Symbol** — Font Awesome Icon-Klasse zur visuellen Identifikation
   - **Erforderlich** — Ob der Kunde eine Auswahl treffen muss
   - **Min/Max Auswahl** — Wie viele Optionen der Kunde waehlen kann (Standard: genau 1)
   - **Sortierreihenfolge** — Steuert die Reihenfolge, in der Plaetze im Konfigurationsassistenten erscheinen

### Schritt 3: Optionen zu Jedem Platz Hinzufuegen

Jeder Platz benoetigt Produktoptionen, aus denen Kunden waehlen koennen:

1. Klicken Sie auf **Optionen Verwalten** bei einem Platz
2. Suchen und fuegen Sie bestehende Produkte aus Ihrem Katalog hinzu
3. Konfigurieren Sie fuer jede Option:
   - **Preisanpassung** — Betrag zum Addieren oder Subtrahieren (verwendet bei Basispreis + Anpassungen)
   - **Standard** — Diese Option vorauswaehlen, wenn der Konfigurator geladen wird
   - **Beliebt** — Ein "Beliebt"-Abzeichen anzeigen, um Kunden bei der Entscheidung zu helfen
   - **Menge** — Wie viele Einheiten dieser Komponente enthalten sind
   - **Kompatibilitaetstags** — Tags fuer die massenhafte Generierung von Kompatibilitaetsregeln

**Tipp:** Komponentenprodukte koennen im Schaufenster ausgeblendet werden, indem Sie **Vom Schaufenster Ausblenden** auf dem Tab Basisinformationen des Komponentenprodukts aktivieren. Dies haelt sie als Konfiguratoroptionen verfuegbar, ohne Ihren Produktkatalog zu ueberladen.

### Schritt 4: Kompatibilitaetsregeln Definieren

Kompatibilitaetsregeln verhindern, dass Kunden inkompatible Kombinationen auswaehlen:

| Regeltyp | Beschreibung |
|----------|-------------|
| **Erfordert** | Wenn Option A ausgewaehlt wird, sind nur die aufgelisteten Optionen im Zielplatz verfuegbar |
| **Schliesst aus** | Wenn Option A ausgewaehlt wird, werden die aufgelisteten Optionen im Zielplatz ausgeblendet |

Um Regeln hinzuzufuegen:

1. Scrollen Sie zum Abschnitt **Kompatibilitaetsregeln** im Tab Konfiguration
2. Klicken Sie auf **+ Regel Hinzufuegen**
3. Waehlen Sie die **Quelloption** (den Ausloeser)
4. Waehlen Sie den **Regeltyp** (Erfordert oder Schliesst aus)
5. Waehlen Sie den **Zielplatz** und die **betroffenen Optionen**

Sie koennen auch automatisch Regeln aus den Kompatibilitaetstags generieren, die den Optionen zugewiesen sind, was schneller ist, wenn viele Kombinationen verwaltet werden.

### Schritt 5: Voreinstellungen Erstellen (Optional)

Voreinstellungen sind vorgefertigte Konfigurationen, die Kunden einen schnellen Startpunkt bieten:

1. Scrollen Sie zum Abschnitt **Konfigurationsvoreinstellungen**
2. Klicken Sie auf **+ Voreinstellung Hinzufuegen**
3. Geben Sie der Voreinstellung einen Namen und eine Beschreibung (z.B. "Gaming-Build", "Budget-Starter")
4. Waehlen Sie die Optionen fuer jeden Platz
5. Laden Sie optional ein Vorschaubild hoch und markieren Sie es als **Hervorgehoben**

Kunden koennen von einer Voreinstellung ausgehen und dann einzelne Plaetze nach ihren Wuenschen anpassen.

## Kundenerlebnis

Wenn ein Kunde ein konfigurierbares Produkt in Ihrem Schaufenster ansieht:

1. **Assistenten-Oberflaeche** — Plaetze werden als Schritte praesentiert und fuehren den Kunden durch jede Auswahl
2. **Filterung** — Inkompatible Optionen werden automatisch basierend auf Kompatibilitaetsregeln ausgeblendet
3. **Beliebt-Abzeichen** — Als beliebt markierte Optionen zeigen ein Abzeichen zur Entscheidungshilfe
4. **Voreinstellungen** — Hervorgehobene Voreinstellungen erscheinen als Schnellstart-Optionen
5. **Preisaktualisierungen** — Der Gesamtpreis aktualisiert sich in Echtzeit, waehrend Optionen ausgewaehlt werden
6. **Zusammenfassung** — Ein Ueberpruefungsschritt zeigt alle ausgewaehlten Optionen vor dem Hinzufuegen zum Warenkorb

## Tipps

- Beginnen Sie mit der Preisstrategie "Summe der Komponenten" — sie ist fuer Kunden am intuitivsten und am einfachsten zu pflegen.
- Verwenden Sie Kompatibilitaetsregeln, um ungueltige Konfigurationen zu verhindern, anstatt sich auf das Wissen des Kunden zu verlassen.
- Erstellen Sie 2-3 Voreinstellungen fuer Ihre beliebtesten Konfigurationen, um Entscheidungsermuedung zu reduzieren.
- Blenden Sie Komponentenprodukte im Schaufenster aus, wenn sie nur ueber den Konfigurator verfuegbar sein sollen.
- Testen Sie den vollstaendigen Konfigurationsablauf im Frontend nach der Einrichtung, um sicherzustellen, dass alle Regeln wie erwartet funktionieren.
