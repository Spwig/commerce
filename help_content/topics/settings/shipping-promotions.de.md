---
title: Versandaktionen
---

Versandregeln wenden bedingte Kostenanpassungen an Versandmethoden an, basierend auf Warenkorbinhalten, Kundeneigenschaften und Lieferzonen – bieten Sie beispielsweise automatisch kostenlosen Versand ab 50 $ an, fügen Sie Zuschläge für abgelegene Gebiete hinzu oder reduzieren Sie den Versandkosten für VIP-Kunden. Regeln werden priorisierungsorientiert ausgeführt (höhere Priorität zuerst) mit optionalen Stop-Flags, um weitere Verarbeitung zu verhindern. Jede Regel bewertet mehrere Bedingungen (Warenkorbwert, Gewicht, Zonen, Produkte, Kundengruppen) und führt eine der 6 Anpassungstypen aus, wenn alle Bedingungen erfüllt sind.

Verwenden Sie Versandaktionen, wenn Sie dynamische Versandkosten benötigen, die sich basierend auf dem Bestellkontext ändern, nicht nur statische Preise aus Versandmethoden.

## Typen von Versandaktionen

Versandregeln wenden 6 Arten von Kostenanpassungen an:

### Prozentsatzrabatt

**Was es tut**: Reduziert die Versandkosten um einen Prozentsatz (z. B. 25 % Rabatt).

**Formel**: `neuer_kosten = basis_kosten × (1 - prozent/100)`

**Beispiel**:
```
Basiskosten: 20 $
Rabatt: 25 %
Ergebnis: 15 $
```

**Anwendungsfälle**:
- VIP-Kundenrabatt (20 % Rabatt auf alle Versandkosten)
- Saisonale Aktionen (15 % Rabatt auf Versandkosten im Dezember)
- Mengenrabatt (10 % Rabatt auf Versandkosten bei 5+ Artikeln)

---

### Fixer Rabatt

**Was es tut**: Subtrahiert einen festen Betrag von den Versandkosten.

**Formel**: `neuer_kosten = basis_kosten - betrag` (Mindestwert 0 $)

**Beispiel**:
```
Basiskosten: 15 $
Rabatt: 5 $
Ergebnis: 10 $
```

**Anwendungsfälle**:
- Neukundenbonus (5 $ Rabatt auf die Versandkosten des ersten Bestells)
- Newsletter-Anmeldeprämie (3 $ Rabatt auf Versandkosten)
- Treueprogramm-Vorteil (10 $ Rabatt auf Versandkosten pro Monat)

---

### Kosten überschreiben

**Was es tut**: Überschreibt die Versandkosten mit einem festen Betrag.

**Formel**: `neuer_kosten = fixer_betrag`

**Beispiel**:
```
Basiskosten: 25 $
Auf: 9,99 $
Ergebnis: 9,99 $
```

**Anwendungsfälle**:
- Flash-Verkauf (flacher Versand von 5 $ für alle Bestellungen heute)
- Kategorie-spezifischer Versand (Bücher immer 3,99 $ Versand)
- Zeitbasierte Aktionen (Versandkosten auf 9,99 $ begrenzt diese Woche)

---

### Kostenlose Lieferung

**Was es tut**: Setzt die Versandkosten auf 0 $.

**Formel**: `neuer_kosten = 0 $`

**Beispiel**:
```
Basiskosten: 18 $
Regel gilt
Ergebnis: 0 $
```

**Anwendungsfälle**:
- Kostenlose Lieferung ab 50 $
- Kostenlose Lieferung für bestimmte Produkte (werbliche Artikel)
- Kostenlose Lieferung für VIP-Kunden
- Kostenlose Lieferung für Bestellungen mit 3+ Artikeln

---

### Zuschlag (Fix)

**Was es tut**: Fügt einen festen Betrag zu den Versandkosten hinzu.

**Formel**: `neuer_kosten = basis_kosten + betrag`

**Beispiel**:
```
Basiskosten: 12 $
Zuschlag: 5 $
Ergebnis: 17 $
```

**Anwendungsfälle**:
- Liefergebühren für abgelegene Gebiete
- Umgang mit überdimensionierten Artikeln
- Zuschlag für Lieferung am Samstag
- Verpackungskosten für zerbrechliche Artikel

---

### Zuschlag (Prozent)

**Was es tut**: Erhöht die Versandkosten um einen Prozentsatz.

**Formel**: `neuer_kosten = basis_kosten × (1 + prozent/100)`

**Beispiel**:
```
Basiskosten: 20 $
Zuschlag: 15 %
Ergebnis: 23 $
```

**Anwendungsfälle**:
- Saisonaler Zuschlag (20 % während der Feiertage)
- Expresslieferungsprämie (50 % Zuschlag)
- Kraftstoffzuschlag (variabel basierend auf aktuellen Preisen)

---

## Aktionenbedingungen

Aktionen bewerten **ALLE Bedingungen müssen erfüllt sein**, damit die Regel gilt:

### Zeitgültigkeit

- **Startdatum**: Regel ist erst ab diesem Datum aktiv
- **Enddatum**: Regel ist nur bis zu diesem Datum aktiv
- **Anwendungsfälle**: Saisonale Aktionen, zeitlich begrenzte Angebote

**Beispiel**: Kostenlose Lieferung nur am Black Friday-Wochenende
```
Start: 2026-11-27 00:00
Ende: 2026-11-30 23:59
```

---

### Warenkorbwertbereich

- **Mindest-Warenkorbwert**: Der Warenkorb-Subtotal muss ≥ Betrag sein
- **Maximaler Warenkorbwert**: Der Warenkorb-Subtotal muss ≤ Betrag sein
- **Anwendungsfälle**: Freiversand-Schwellenwerte, gestufte Rabatte

**Beispiel**: Freiversand für Bestellungen von 50 $ bis 200 $
```
Mindestwert: 50 $
Maximalwert: 200 $
```

---

### Warenkorb-Gewichtsbereich

- **Mindestgewicht**: Das Gesamtgewicht des Warenkorbs muss ≥ Betrag sein
- **Maximalgewicht**: Das Gesamtgewicht des Warenkorbs muss ≤ Betrag sein
- **Anwendungsfälle**: Rabatte für leichte Sendungen, Zuschläge für schwere Artikel

**Beispiel**: 5 $ Zuschlag für Bestellungen über 20 kg
```
Mindestgewicht: 20 kg
Maximalgewicht: null (unbegrenzt)
```

---

### Artikelanzahlbereich


- **Mindestanzahl**: Der Warenkorb muss ≥ Anzahl von Artikeln enthalten
- **Maxdestanzahl**: Der Warenkorb muss ≤ Anzahl von Artikeln enthalten
- **Verwendungszweck**: Mengenrabatte, Einzelartikelgebühren

**Beispiel**: Kostenlose Lieferung ab 5+ Artikeln
```
Mindestanzahl: 5
Maxdestanzahl: null
```

---

### Lieferzone

- **Zonen**: Regel gilt nur, wenn die Kundenadresse mindestens einer ausgewählten Zone entspricht
- **Leere Auswahl**: Regel gilt für ALLE Zonen
- **Verwendungszweck**: Zonen-spezifische Gebühren oder Rabatte

**Beispiel**: Kostenlose Lieferung nur für die Zone Domestic
```
Zonen: ["Domestic USA"]
```

---

### Liefermethode

- **Methoden**: Regel gilt nur für bestimmte Liefermethoden
- **Leere Auswahl**: Regel gilt für ALLE Methoden
- **Verwendungszweck**: Methodenspezifische Promotionen

**Beispiel**: 25 % Rabatt auf Expressversand
```
Methoden: ["Express Delivery"]
```

---

### Produktanforderungen

**Erfordert Produkte**: Der Warenkorb muss mindestens eines dieser Produkte enthalten

**Erfordert Kategorien**: Der Warenkorb muss mindestens ein Produkt aus diesen Kategorien enthalten

**Verwendungszweck**: Produkt-spezifische kostenlose Lieferung, Promo-Bundles

**Beispiel**: Kostenlose Lieferung, wenn der Warenkorb das Produkt "Promotion Item A" enthält
```
Erfordert Produkte: [Produkt-ID 123]
```

---

### Produkt-Ausschlüsse

**Ausschließt Produkte**: Regel gilt nicht, wenn der Warenkorb eines dieser Produkte enthält

**Ausschließt Kategorien**: Regel gilt nicht, wenn der Warenkorb Produkte aus diesen Kategorien enthält

**Verwendungszweck**: Schwere/übergrößte Artikel von der kostenlosen Lieferung ausschließen

**Beispiel**: Kostenlose Lieferung, außer für die Kategorie Möbel
```
Ausschließt Kategorien: [Möbel]
```

---

### Kundengruppe

- **Kundengruppen**: Regel gilt nur für Kunden in den ausgewählten Gruppen (VIP, Großhandel, etc.)
- **Leere Auswahl**: Regel gilt für ALLE Kundengruppen
- **Verwendungszweck**: VIP-Vorteile, Großhandelsrabatte

**Beispiel**: 15 % Lieferkostenrabatt für VIP-Mitglieder
```
Kundengruppen: ["VIP"]
```

---

### Neukunde

- **Neukunde**: Schalter, um die Regel auf Kunden mit noch keinen vorherigen Bestellungen zu beschränken
- **Verwendungszweck**: Willkommensangebote für neue Kunden

**Beispiel**: 5 $ Rabatt auf Lieferkosten für die erste Bestellung
```
Neukunde: Ja
```

---

## Promotion-Priorität & Ausführung

Promotions werden in **Prioritätsreihenfolge** ausgeführt (höhere Zahl = frühere Ausführung):

### Prioritätsmechanik

**Ausführungsbeispiel**:
```
Promotion A (Priorität 100): Kostenlose Lieferung, wenn Warenkorb > 50 $
Promotion B (Priorität 50): 10 % Rabatt auf alle Lieferkosten
Promotion C (Priorität 1): 2 $ Gebühr für entfernte Zonen

Warenkorb: 60 $, entfernte Zone
Basislieferkosten: 15 $

Schritt 1: Promotion A wird bewertet (Priorität 100)
  Warenkorb > 50 $? JA
  Anwenden: Kosten auf 0 $ setzen
  Kosten jetzt: 0 $

Schritt 2: Promotion B wird bewertet (Priorität 50)
  10 % Rabatt auf 0 $ anwenden
  Kosten jetzt: 0 $ (immer noch kostenlos)

Schritt 3: Promotion C wird bewertet (Priorität 1)
  2 $ Gebühr auf 0 $ hinzufügen
  Kosten jetzt: 2 $

Endkosten: 2 $
```

**Flag für weitere Promotionen stoppen**:

Wenn Promotion A `stop_further_promotions = True` hat:
```
Promotion A (Priorität 100, stop_further_promotions=True): Kostenlose Lieferung, wenn Warenkorb > 50 $
Promotion B (Priorität 50): 10 % Rabatt
Promotion C (Priorität 1): 2 $ Gebühr für entfernte Zonen

Warenkorb: 60 $
Basis: 15 $

Schritt 1: Promotion A wird angewendet, setzt Kosten auf 0 $
        stop_further_promotions = True → STOPPEN

Endkosten: 0 $ (Regeln B und C werden nie angewendet)
```

---

## Erstellen von Lieferpromotions

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigieren zu Regeln**
   - Einstellungen > Lieferung > Lieferpromotions
   - Klicken Sie auf "Lieferpromotion hinzufügen"

2. **Grundkonfiguration**
   - **Name**: Interner Bezeichner (z. B. "Kostenlose Lieferung ab 50 $")
   - **Beschreibung**: Optionale Notizen (nicht für Kunden sichtbar)
   - **Aktiv**: Schalter zum Aktivieren/Deaktivieren
   - **Priorität**: Setzen Sie die Ausführungsreihenfolge (100 für hohe Priorität, 1 für niedrige)

3. **Wählen Sie Promotion-Typ**
   - Wählen Sie Anpassungstyp (Prozentsatz-Rabatt, fester Rabatt, Kosten setzen, kostenlos, Gebühr in Prozent, feste Gebühr)
   - Geben Sie einen Betrag oder Prozentsatz ein


- Aktivieren Sie "Weitere Promotionen stoppen", wenn diese Regel verhindern soll, dass Promotionen niedrigerer Priorität ausgeführt werden

- Verwenden Sie dies für endgültige/absolute Regeln (z. B. kostenlose Versandkosten sollten nachträglich keine Gebühren erhalten)

- Gültigkeitszeitraum: Start-/Enddatum

- Warenkorbwert: Min/Max

- Warenkorbgewicht: Min/Max

- Artikelanzahl: Min/Max

- Zonen: Passende Zonen auswählen

- Methoden: Passende Methoden auswählen

- Produkte: Erforderlich oder ausgeschlossen

- Kunde: Gruppen oder nur für Neukunden

- Klicken Sie auf Speichern

- Die Regel wird sofort aktiv (wenn der Aktiv-Schalter auf Ja steht)

**Ziel**: Kostenlose Versandkosten anbieten, wenn der Warenkorb-Subtotal ≥ $50 ist.

```
Name: Promo Category Free Shipping
Type: Free Shipping
Priority: 90
Conditions:
  Requires Categories: ["Promotions"]
Stop Further Promotions: Yes
```

**Ziel**: 10 $ Gebühr für Lieferungen in abgelegene Zonen hinzufügen.

**Ziel**: VIP-Kunden erhalten 20 % Rabatt auf alle Versandkosten.

**Ziel**: Alle Versandkosten während Dezember auf $9,99 begrenzen.

**Ziel**: 15 $ Gebühr für Bestellungen über 25 kg hinzufügen.

**Ziel**: Neue Kunden erhalten kostenlose Versandkosten für ihre erste Bestellung.

**Ziel**: Kostenlose Versandkosten für Bestellungen, die Artikel aus der Werbekategorie enthalten.

**Ziel**: Kostenlose Versandkosten über $50, außer wenn der Warenkorb Möbel enthält.

**Lösung**: Zwei Regeln

```
Name: General Free Shipping
Type: Free Shipping
Priority: 50
Conditions:
  Min Cart Value: $50
  Excludes Categories: ["Furniture"]
Stop Further Promotions: No
```

```
Name: Furniture Orders $5 Discount
Type: Discount (Fixed)
Amount: $5
Priority: 40
Conditions:
  Requires Categories: ["Furniture"]
  Min Cart Value: $50
Stop Further Promotions: No
```

**Mehrere Rabatte können叠加 werden**:

```
Promotion A (Priority 100): 10 % Rabatt für VIP → stop_further_promotions=No
Promotion B (Priority 50): 15 % Rabatt für Bestellungen >$100 → stop_further_promotions=No

VIP-Kunde mit $120 Bestellung:
Grundwert: $15
Nach Promotion A: $13,50 (10 % Rabatt)
Nach Promotion B: $11,48 (15 % Rabatt von $13,50)
```

**Nur eine Regel gilt** (höchste Priorität):

```
Promotion A (Priority 100): Kostenlose Versandkosten >$50 → stop_further_promotions=Yes
Promotion B (Priority 50): 20 % Rabatt auf alle Versandkosten → stop_further_promotions=Yes

Warenkorb > $50:
Promotion A gilt → Kostenlose Versandkosten → STOP
Promotion B wird nie ausgeführt
```

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technische Begriffe.

**Zuerst Rabatte, zuletzt Gebühren**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (nicht kostenlos aufgrund von Gebühren)
```

**Um dies zu verhindern, verwenden Sie stop_further_promotions=Yes**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Selbe Bestellung:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (wirklich kostenlos)
```

---

## Testing Shipping Promotions

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.