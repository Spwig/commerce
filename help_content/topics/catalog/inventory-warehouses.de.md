---
title: Bestandsverwaltung und Lager
---

Das Lagersystem ermoeglicht es Ihnen, den Bestand ueber mehrere Standorte hinweg zu verwalten, Erfuellungsprioritaeten festzulegen und Lagerbestaende in Echtzeit zu verfolgen. Navigieren Sie zu **Einstellungen > Lizenzverwaltung** in der Seitenleiste, oder greifen Sie ueber den Inventar-Tab des Produkts auf die Lager zu.

![Lagerliste](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Lager

### Lagerliste

Die Lagerseite zeigt alle Ihre Inventarstandorte als Karten mit:

- **Name und Code** — Lagerkennung (z. B. "Hauptlager", Code "MAIN-WH")
- **Verkaufsregion** — Zuordnung der geografischen Region
- **Status-Badges** — Aktiv/inaktiv, Einzelhandelsstandort
- **Statistiken** — Gelagerte Produkte, Erfuellungsprioritaet, Prozentsatz der Bestandsreserve
- **Standort** — Stadt und Land
- **Letzte Aktualisierung** — Wann die Lagerbestaende zuletzt geaendert wurden

### Ein Lager erstellen

1. Klicken Sie auf **+ Lager hinzufuegen**
2. Fuellen Sie die Lagerdetails aus:
   - **Name** — Beschreibende Bezeichnung (z. B. "US-Ostlager")
   - **Code** — Kurzer eindeutiger Identifikator (z. B. "US-EAST")
   - **Verkaufsregion** — Einer geografischen Region fuer die Auftragsweiterleitung zuordnen
   - **Adresse** — Vollstaendige Lageradresse fuer Versandberechnungen
3. Konfigurieren Sie die Einstellungen:
   - **Aktiv** — Aktivieren, um in die Auftragsabwicklung einzubeziehen
   - **Einzelhandelsstandort** — Markieren, wenn dieses Lager auch als physisches Geschaeft dient
   - **Erfuellungsprioritaet** — Hoehere Zahlen bedeuten hoehere Prioritaet fuer die Auftragsabwicklung
   - **Bestandsreserve** — Prozentsatz des Bestands, der als Sicherheitspuffer reserviert wird
4. Klicken Sie auf **Speichern**

### Erfuellungsprioritaet

Wenn eine Bestellung eingeht, waehlt das System das beste Lager basierend auf:

1. **Prioritaetswert** — Lager mit hoeherer Prioritaet werden bevorzugt
2. **Bestandsverfuegbarkeit** — Es muss ausreichend Bestand vorhanden sein
3. **Regionsabgleich** — Lager in der Region des Kunden werden bevorzugt

Wenn Sie beispielsweise ein US-Lager (Prioritaet 100) und ein EU-Lager (Prioritaet 60) haben, werden US-Bestellungen zuerst aus dem US-Lager erfuellt.

### Bestandsreserve

Die Bestandsreserve haelt einen Prozentsatz des Inventars zurueck, der nicht online verkauft wird. Dies ist nuetzlich fuer:
- Physische Einzelhandelsgeschaefte, die Ausstellungsbestand benoetigen
- Sicherheitsbestand zur Vermeidung von Ueberverkauf
- Reserviertes Inventar fuer Grosshandelsbestellungen

Eine Reserva von 10 % bei 100 Einheiten bedeutet, dass nur 90 Einheiten fuer Online-Bestellungen verfuegbar sind.

## Bestandsartikel

Bestandsartikel repraesentieren den tatsaechlichen Bestand eines bestimmten Produkts in einem bestimmten Lager.

### Lagerbestaende einsehen

1. Klicken Sie auf das **Bestandssymbol** auf einer beliebigen Lagerkarte, um die Bestandsartikel zu sehen
2. Oder navigieren Sie zum **Inventar**-Tab eines Produkts, um den Bestand ueber alle Lager zu sehen

Jeder Bestandsartikel zeigt:
- **Produktname** und Variante (falls zutreffend)
- **Vorraaetig** — Gesamter physischer Bestand
- **Zugewiesen** — Fuer ausstehende Bestellungen reservierte Menge
- **Verfuegbar** — Vorraetig abzueglich zugewiesen (was verkauft werden kann)

### Bestand hinzufuegen

1. Klicken Sie in der Lagerbestandsansicht auf **Bestandsartikel hinzufuegen**
2. Waehlen Sie das Produkt und die Variante
3. Geben Sie die **vorraaetige** Menge ein
4. Speichern

### Bestandsbewegungen

Jede Aenderung am Inventar wird als **Bestandsbewegung** erfasst:

| Bewegungstyp | Beschreibung |
|-------------|-------------|
| **Wareneingang** | Neuer Bestand vom Lieferanten erhalten |
| **Verkauf** | Bestand fuer eine erfuellte Bestellung abgezogen |
| **Retoure** | Bestand von einem Kunden zurueckgegeben |
| **Anpassung** | Manuelle Korrektur (Zaehlabweichung) |
| **Transfer** | Zwischen Lagern verschoben |
| **Reservierung** | Voruebergehend fuer einen aktiven Warenkorb gehalten |

Bestandsbewegungen bieten eine vollstaendige Pruefungshistorie der Inventaraenderungen.

## Bestandsverfolgung bei Produkten

### Bestandsverfolgung aktivieren

Im **Inventar**-Tab eines Produkts:

1. Aktivieren Sie **Bestand verfolgen**, um die Lagerverwaltung zu aktivieren
2. Legen Sie den **Schwellenwert fuer niedrigen Bestand** fest — loest Benachrichtigungen aus, wenn der Bestand unter diesen Wert faellt
3. Konfigurieren Sie **Nachbestellungen zulassen**, wenn Sie Bestellungen bei ausverkauften Produkten annehmen moechten

### Multi-Lager-Bestand

Wenn die Bestandsverfolgung aktiviert ist, zeigt der Inventar-Tab die Lagerbestaende aller Lager in einer Zusammenfassungstabelle:

- Gesamtbestand ueber alle Standorte
- Aufschluesselung nach Lager
- Verfuegbare Mengen nach Reservierungen und Zuweisungen

## Benachrichtigungen bei niedrigem Bestand

Das System ueberwacht automatisch die Lagerbestaende und benachrichtigt Sie, wenn:
- Ein Produkt unter seinen **Schwellenwert fuer niedrigen Bestand** faellt
- Ein Produkt **keinen verfuegbaren Bestand** mehr hat

Benachrichtigungen bei niedrigem Bestand erscheinen:
- Im **Shop-Dashboard** im Bereich Erforderliche Aktionen
- In der Produktliste mit einem visuellen Indikator

## Tipps

- Beginnen Sie mit einem einzelnen Lager und fuegen Sie weitere hinzu, wenn Ihr Geschaeft waechst.
- Legen Sie die Erfuellungsprioritaeten basierend auf Versandgeschwindigkeit und -kosten fuer jede Region fest.
- Verwenden Sie Bestandsreserven fuer Einzelhandelsstandorte, um die Verfuegbarkeit von Ausstellungsbestand sicherzustellen.
- Ueberpruefen Sie Bestandsbewegungen regelmaessig, um Schwund oder Abweichungen zu erkennen.
- Legen Sie die Schwellenwerte fuer niedrigen Bestand basierend auf Ihrer Nachbestellzeit fest — wenn die Nachlieferung 2 Wochen dauert, setzen Sie den Schwellenwert so, dass er 2 Wochen Verkaeufe abdeckt.
- Aktivieren Sie die Bestandsverfolgung vor dem Start, um Ueberverkaeufe zu vermeiden.
