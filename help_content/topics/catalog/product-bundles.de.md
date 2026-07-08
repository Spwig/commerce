---
title: "Produktpakete"
---

Produktpakete ermoglichen es Ihnen, vorab zusammengestellte Produktsets zu einem Paketpreis zu verkaufen. Dies ist perfekt fuer Geschenksets, Starter-Kits oder jede Kombination von Produkten, die Sie zusammen mit einem Rabatt anbieten moechten.

![Bundle components admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Preisstrategien

Waehlen Sie, wie der Paketpreis berechnet wird:

| Strategie | Beschreibung |
|-----------|-------------|
| **Festpreis** | Legen Sie einen Pauschalpreis fuer das gesamte Paket fest, unabhaengig von den Komponentenpreisen. |
| **Prozentualer Rabatt** | Berechnen Sie den Preis automatisch als prozentualen Rabatt auf die kombinierten Komponentenpreise. |
| **Summe der Komponenten** | Der Paketpreis entspricht der Summe aller Komponentenpreise (nuetzlich fuer gruppierte Anzeige ohne Rabatt). |

## Erstellung eines Pakets

### Schritt 1: Produkt Erstellen

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt Hinzufuegen**
2. Setzen Sie den **Produkttyp** auf **Produktpaket**
3. Fuellen Sie den Paketnamen, die Beschreibung und Bilder aus
4. Speichern Sie das Produkt

### Schritt 2: Komponenten Hinzufuegen

Wechseln Sie zum Tab **Paketartikel**, um Produkte zu Ihrem Paket hinzuzufuegen:

1. Klicken Sie auf **+ Komponente Hinzufuegen**
2. Suchen und waehlen Sie ein Produkt aus dem Dropdown-Menu
3. Legen Sie die **Menge** fuer jede Komponente fest (z.B. 2x Gesichtsmasken in einem Hautpflegeset)
4. Legen Sie die **Sortierreihenfolge** fest, um die Anzeigereihenfolge zu steuern
5. Markieren Sie optional eine Komponente als **Optional** (Kunden koennen sie ausschliessen)
6. Wenn die Komponente ein variables Produkt ist, waehlen Sie entweder:
   - Eine **feste Variante** — alle Kunden erhalten die gleiche Variante
   - **Variantenauswahl erlauben** — Kunden waehlen ihre bevorzugte Variante beim Bezahlen

Die Zusammenfassung unten zeigt die **Gesamtanzahl der Komponenten** und den **Paketwert** (Summe der Komponentenpreise).

### Schritt 3: Preise Konfigurieren

Wechseln Sie zum Tab **Preise**:

1. Waehlen Sie Ihre **Paket-Preisstrategie**
2. Fuer **Festpreis** — geben Sie den Paketpreis direkt ein
3. Fuer **Prozentualer Rabatt** — legen Sie den Rabattprozentsatz fest (z.B. 15% Rabatt)
4. Fuer **Summe der Komponenten** — der Preis wird automatisch berechnet

## Was in ein Paket aufgenommen werden kann

| Produkttyp | Kann Komponente sein? |
|-----------|----------------------|
| Einfaches Produkt | Ja |
| Variables Produkt | Ja (feste Variante oder Kundenauswahl) |
| Digitales Produkt | Ja |
| Anpassbares Produkt | Nein |
| Konfigurierbares Produkt | Nein |
| Produktpaket | Nein (Pakete koennen nicht verschachtelt werden) |
| Geschenkkarte | Nein |

## Bestandsverwaltung

Der Paketbestand wird ueber seine Komponenten verwaltet:

- **Alle Komponenten muessen auf Lager sein**, damit das Paket kaufbar ist
- Wenn ein Paket bestellt wird, wird der Bestand von jedem Komponentenprodukt einzeln abgezogen
- Wenn eine Komponente nicht mehr auf Lager ist, wird das Paket nicht mehr verfuegbar
- Die Bestandsniveaus der Komponenten werden waehrend des Bezahlvorgangs in Echtzeit ueberprueft

## Optionale Komponenten

Markieren Sie eine Komponente als **Optional**, um Kunden die Anpassung ihres Pakets zu ermoeglichen:

- Optionale Komponenten sind standardmaessig enthalten, koennen aber vom Kunden entfernt werden
- Der Paketpreis passt sich entsprechend an, wenn optionale Komponenten ausgeschlossen werden
- Mindestens eine Komponente muss nicht-optional (erforderlich) sein

## Kundenerlebnis

Wenn ein Kunde ein Paket in Ihrem Schaufenster betrachtet:

1. **Komponentenliste** — Alle enthaltenen Produkte werden mit Bildern und Mengen angezeigt
2. **Paket-Ersparnis** — Der Rabatt im Vergleich zum Einzelkauf wird angezeigt
3. **Variantenauswahl** — Fuer Komponenten mit aktivierter Variantenauswahl waehlen Kunden ihre bevorzugte Option
4. **Optionale Artikel** — Kunden koennen optionale Komponenten ein- oder ausschalten
5. **Einmaliges Hinzufuegen zum Warenkorb** — Das gesamte Paket wird als ein Artikel hinzugefuegt

## Tipps

- Verwenden Sie die Strategie Prozentualer Rabatt fuer die groesste Preisflexibilitaet — sie passt sich automatisch an, wenn sich die Komponentenpreise aendern.
- Zeigen Sie den Sparbetrag prominent in Ihrer Produktbeschreibung an, um Paketkauefe zu foerdern.
- Begrenzen Sie Pakete auf 3-5 Komponenten fuer das beste Kundenerlebnis. Zu viele Artikel koennen ueberwaeltigend wirken.
- Verwenden Sie optionale Komponenten, um eine "Basis"- und "Premium"-Version desselben Pakets anzubieten.
- Ueberpruefen Sie regelmaessig, dass alle Komponentenprodukte noch aktiv und auf Lager sind.
