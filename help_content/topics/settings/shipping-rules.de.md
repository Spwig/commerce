---
title: Versandregeln
---

Versandregeln wenden bedingte Kostenanpassungen an Versandmethoden an, basierend auf Warenkorbinhalten, Kundeneigenschaften und Lieferzonen – bieten Sie beispielsweise automatisch kostenlosen Versand ab 50 $ an, fügen Sie Zuschläge für abgelegene Gebiete hinzu oder reduzieren Sie den Versandkosten für VIP-Kunden. Regeln verwenden eine priorisierte Ausführung (höhere Priorität zuerst) mit optionalen Stop-Flaggen, um weitere Verarbeitung zu verhindern. Jede Regel bewertet mehrere Bedingungen (Warenkorbwert, Gewicht, Zonen, Produkte, Kundengruppen) und führt eine der 6 Anpassungstypen aus, wenn alle Bedingungen erfüllt sind.

Verwenden Sie Versandregeln, wenn Sie dynamische Versandkosten benötigen, die sich basierend auf dem Bestellkontext ändern, nicht nur statische Raten aus Versandmethoden.

## Typen von Versandregeln

Versandregeln wenden 6 Arten von Kostenanpassungen an:

### Prozentsatzrabatt

**Was es tut**: Reduziert die Versandkosten um einen Prozentsatz (z. B. 25 % Rabatt).

**Formel**: `neuer_kosten = basis_kosten × (1 - prozent/100)`

**Beispiel**:
```
Basis-Kosten: 20 $
Rabatt: 25 %
Ergebnis: 15 $
```

**Anwendungsfälle**:
- VIP-Kundenrabatt (20 % Rabatt auf alle Versandkosten)
- Saisonale Promotionen (15 % Rabatt auf Versandkosten im Dezember)
- Rabatt für Großbestellungen (10 % Rabatt auf Versandkosten für 5+ Artikel)

---

### Fixer Rabatt

**Was es tut**: Subtrahiert einen festen Betrag von den Versandkosten.

**Formel**: `neuer_kosten = basis_kosten - betrag` (Mindestwert 0 $)

**Beispiel**:
```
Basis-Kosten: 15 $
Rabatt: 5 $
Ergebnis: 10 $
```

**Anwendungsfälle**:
- Bonus für Neukunden (5 $ Rabatt auf die Versandkosten des ersten Bestells)
- Belohnung für Newsletter-Anmeldung (3 $ Rabatt auf Versandkosten)
- Vorteil des Loyalitätsprogramms (10 $ Rabatt auf Versandkosten pro Monat)

---

### Festgelegte Kosten

**Was es tut**: Überschreibt die Versandkosten mit einem bestimmten Betrag.

**Formel**: `neuer_kosten = festgelegter_betrag`

**Beispiel**:
```
Basis-Kosten: 25 $
Auf: 9,99 $
Ergebnis: 9,99 $
```

**Anwendungsfälle**:
- Flash-Verkauf (flacher Versandkostenbetrag von 5 $ für alle Bestellungen heute)
- Kategorien-spezifischer Versand (Bücher immer 3,99 $ Versand)
- Zeitbasierte Promotionen (Versandkosten auf 9,99 $ begrenzt diese Woche)

---

### Kostenlose Lieferung

**Was es tut**: Setzt die Versandkosten auf 0 $.

**Formel**: `neuer_kosten = 0 $`

**Beispiel**:
```
Basis-Kosten: 18 $
Regel gilt
Ergebnis: 0 $
```

**Anwendungsfälle**:
- Kostenlose Lieferung ab 50 $
- Kostenlose Lieferung für bestimmte Produkte (Promotionsartikel)
- Kostenlose Lieferung für VIP-Kunden
- Kostenlose Lieferung für Bestellungen mit 3+ Artikeln

---

### Zuschlag (Fix)

**Was es tut**: Fügt einen festen Betrag zu den Versandkosten hinzu.

**Formel**: `neuer_kosten = basis_kosten + betrag`

**Beispiel**:
```
Basis-Kosten: 12 $
Zuschlag: 5 $
Ergebnis: 17 $
```

**Anwendungsfälle**:
- Liefergebühren für abgelegene Gebiete
- Bearbeitungsgebühren für über große Artikel
- Zuschlag für Samstaglieferung
- Verpackungsgebühr für zerbrechliche Artikel

---

### Zuschlag (Prozent)

**Was es tut**: Erhöht die Versandkosten um einen Prozentsatz.

**Formel**: `neuer_kosten = basis_kosten × (1 + prozent/100)`

**Beispiel**:
```
Basis-Kosten: 20 $
Zuschlag: 15 %
Ergebnis: 23 $
```

**Anwendungsfälle**:
- Spitzenzeit-Zuschlag (20 % während der Feiertage)
- Expresslieferungsprämie (50 % Zuschlag)
- Kraftstoffzuschlag (variabel basierend auf aktuellen Preisen)

---

## Regelbedingungen

Regeln bewerten **ALLE Bedingungen müssen erfüllt sein**, damit die Regel gilt:

### Zeitliche Gültigkeit

- **Startdatum**: Regel ist nur ab diesem Datum aktiv
- **Enddatum**: Regel ist nur bis zu diesem Datum aktiv
- **Anwendungsfälle**: Saisonale Promotionen, zeitlich begrenzte Angebote

**Beispiel**: Kostenlose Lieferung nur am Black Friday-Weekend
```
Start: 2026-11-27 00:00
Ende: 2026-11-30 23:59
```

---

### Warenkorbwertbereich

- **Mindest-Warenkorbwert**: Der Warenkorb-Subtotal muss ≥ Betrag sein
- **Maximaler Warenkorbwert**: Der Warenkorb-Subtotal muss ≤ Betrag sein
- **Anwendungsfälle**: Freiversand-Schwellenwerte, Staffelpreise

**Beispiel**: Freiversand für Bestellungen von 50 $–200 $
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

- **Mindestanzahl an Artikeln**: Der Warenkorb muss mindestens eine Anzahl an Artikeln enthalten
- **Maximale Anzahl an Artikeln**: Der Warenkorb muss maximal eine Anzahl an Artikeln enthalten
- **Anwendungsfälle**: Rabatte für Großbestellungen, Gebühren für Einzelartikel

**Beispiel**: Freiversand für 5+ Artikel
```
Mindestanzahl an Artikeln: 5
Maximale Anzahl an Artikeln: null
```

---

### Versandzone

- **Zonen**: Regel gilt nur, wenn die Kundeadresse mit mindestens einer ausgewählten Zone übereinstimmt
- **Leere Auswahl**: Regel gilt für ALLE Zonen
- **Anwendungsfälle**: Zonen-spezifische Zuschläge oder Rabatte

**Beispiel**: Freiversand nur für die Zone Domestic
```
Zonen: ["Domestic USA"]
```

---

### Versandmethode

- **Methoden**: Regel gilt nur für bestimmte Versandmethoden
- **Leere Auswahl**: Regel gilt für ALLE Methoden
- **Anwendungsfälle**: Methodenspezifische Promotionen

**Beispiel**: 25 % Rabatt auf Expressversand
```
Methoden: ["Express Delivery"]
```

---

### Produktanforderungen

**Erfordert Produkte**: Der Warenkorb muss mindestens eines dieser Produkte enthalten

**Erfordert Kategorien**: Der Warenkorb muss mindestens ein Produkt aus diesen Kategorien enthalten

**Anwendungsfälle**: Produkt-spezifischer Freiversand, Promotion-Pakete

**Beispiel**: Freiversand, wenn der Warenkorb das Produkt "Promotion Item A" enthält
```
Erfordert Produkte: [Produkt-ID 123]
```

---

### Produkt-Ausschlüsse

**Ausschlussprodukte**: Regel gilt nicht, wenn der Warenkorb eines dieser Produkte enthält

**Ausschlusskategorien**: Regel gilt nicht, wenn der Warenkorb Produkte aus diesen Kategorien enthält

**Anwendungsfälle**: Ausschluss schwerer/übergrößer Artikel aus Freiversand

**Beispiel**: Freiversand, außer für die Kategorie Möbel
```
Ausschlusskategorien: [Möbel]
```

---

### Kundengruppe

- **Kundengruppen**: Regel gilt nur für Kunden in den ausgewählten Gruppen (VIP, Großhandel, etc.)
- **Leere Auswahl**: Regel gilt für ALLE Kundengruppen
- **Anwendungsfälle**: VIP-Vorteile, Großhandelsrabatte

**Beispiel**: 15 % Versandrabatt für VIP-Mitglieder
```
Kundengruppen: ["VIP"]
```

---

### Neukunde

- **Neukunde**: Schalter, um die Regel auf Kunden mit keiner vorherigen Bestellung zu beschränken
- **Anwendungsfälle**: Willkommensangebote für neue Kunden

**Beispiel**: 5 $ Rabatt auf Versandkosten für die erste Bestellung
```
Neukunde: Ja
```

---

## Regelpriorität und Ausführung

Regeln werden in **Prioritätsreihenfolge** (höhere Zahl = frühere Ausführung) ausgeführt:

### Prioritätsmechanik

**Beispiel der Ausführung**:
```
Regel A (Priorität 100): Freiversand, wenn Warenkorb > 50 $
Regel B (Priorität 50): 10 % Rabatt auf alle Versandkosten
Regel C (Priorität 1): 2 $ Zuschlag für abgelegene Zonen

Warenkorb: 60 $, abgelegene Zone
Basis-Versandkosten: 15 $

Schritt 1: Regel A bewertet (Priorität 100)
  Warenkorb > 50 $? JA
  Anwenden: Kosten auf 0 $ setzen
  Kosten jetzt: 0 $

Schritt 2: Regel B bewertet (Priorität 50)
  10 % Rabatt auf 0 $ anwenden
  Kosten jetzt: 0 $ (immer noch kostenlos)

Schritt 3: Regel C bewertet (Priorität 1)
  2 $ Zuschlag auf 0 $ hinzufügen
  Kosten jetzt: 2 $

Endkosten: 2 $
```

**Flag für weitere Regeln stoppen**:

Wenn Regel A `stop_further_rules = True` hat:
```
Regel A (Priorität 100, stop_further_rules=True): Freiversand, wenn Warenkorb > 50 $
Regel B (Priorität 50): 10 % Rabatt
Regel C (Priorität 1): 2 $ Zuschlag

Warenkorb: 60 $
Basis: 15 $

Schritt 1: Regel A gilt, setzt Kosten auf 0 $
        stop_further_rules = True → STOPPEN

Endkosten: 0 $ (Regeln B und C werden nie ausgeführt)
```

---

## Erstellen von Versandregeln

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigieren Sie zu den Regeln**
   - Einstellungen > Versand > Versandregeln
   - Klicken Sie auf "Versandregel hinzufügen"

2. **Grundkonfiguration**
   - **Name**: Interner Bezeichner (z. B. "Freiversand ab 50 $")
   - **Beschreibung**: Optionale Notizen (nicht für Kunden sichtbar)
   - **Aktiv**: Schalter, um zu aktivieren/deaktivieren
   - **Priorität**: Setzen Sie die Ausführungsreihenfolge (100 für hohe Priorität, 1 für niedrige)

3. **Wählen Sie die Regelart**
   - Wählen Sie den Anpassungstyp (Prozentsatzrabatt, Fixer Rabatt, Festgelegte Kosten, Freiversand, Prozentsatz-Zuschlag, Fixer Zuschlag)
   - Geben Sie einen Betrag oder Prozentsatz ein

4. **Setzen Sie das Stop-Flag** (Optional)
   - Aktivieren Sie "Weitere Regeln stoppen", wenn diese Regel die Ausführung von Regeln niedriger Priorität verhindern soll
   - Verwenden Sie dies für endgültige/absolute Regeln (z. B. Freiversand sollte nicht nachträglich Zuschläge erhalten)

5. **Definieren Sie Bedingungen** (Optional – lassen Sie sie leer, um "immer anzuwenden")
   - Zeitliche Gültigkeit: Start-/Enddatum
   - Warenkorbwert: Mindest-/Maximalwert
   - Warenkorb-Gewicht: Mindest-/Maximalgewicht
   - Artikelanzahl: Mindest-/Maximalanzahl
   - Zonen: Wählen Sie anwendbare Zonen
   - Methoden: Wählen Sie anwendbare Methoden
   - Produkte: Erfordert oder ausschließt
   - Kunde: Gruppen oder nur für Neukunden

6. **Speichern Sie die Regel**
   - Klicken Sie auf Speichern
   - Regel wird sofort aktiv (wenn Aktiv-Schalter auf Ja steht)

---

## Typische Versandregel-Szenarien

### Szenario 1: Freiversand ab 50 $

**Ziel**: Freiversand anbieten, wenn der Warenkorb-Subtotal ≥ 50 $ ist.

**Konfiguration**:
```
Name: Freiversand ab 50 $
Typ: Freiversand
Priorität: 100
Bedingungen:
  Mindest-Warenkorbwert: 50 $
Stoppen weitere Regeln: Ja
```

---

### Szenario 2: Zuschlag für abgelegene Gebiete

**Ziel**: 10 $ Zuschlag für Lieferungen in abgelegene Zonen hinzufügen.

**Konfiguration**:
```
Name: Zuschlag für abgelegene Gebiete
Typ: Zuschlag (Fix)
Betrag: 10 $
Priorität: 50
Bedingungen:
  Zonen: ["Abgelegene Gebiete"]
Stoppen weitere Regeln: Nein
```

---

### Szenario 3: 20 % Rabatt für VIP-Kunden

**Ziel**: VIP-Kunden erhalten 20 % Rabatt auf alle Versandkosten.

**Konfiguration**:
```
Name: VIP-Versandrabatt
Typ: Rabatt (Prozent)
Prozent: 20
Priorität: 75
Bedingungen:
  Kundengruppen: ["VIP"]
Stoppen weitere Regeln: Nein
```

---

### Szenario 4: Festpreis während Dezember

**Ziel**: Alle Versandkosten während Dezember auf 9,99 $ begrenzen.

**Konfiguration**:
```
Name: Dezember-Festpreis-Promotion
Typ: Festgelegte Kosten
Betrag: 9,99 $
Priorität: 100
Bedingungen:
  Startdatum: 2026-12-01
  Enddatum: 2026-12-31
Stoppen weitere Regeln: Ja
```

---

### Szenario 5: Zuschlag für schwere Artikel

**Ziel**: 15 $ Gebühr für Bestellungen über 25 kg hinzufügen.

**Konfiguration**:
```
Name: Zuschlag für schwere Bestellungen
Typ: Zuschlag (Fix)
Betrag: 15 $
Priorität: 50
Bedingungen:
  Mindestgewicht: 25 kg
Stoppen weitere Regeln: Nein
```

---

### Szenario 6: Freiversand für erste Bestellung

**Ziel**: Neue Kunden erhalten Freiversand für ihre erste Bestellung.

**Konfiguration**:
```
Name: Freiversand für erste Bestellung
Typ: Freiversand
Priorität: 100
Bedingungen:
  Neukunde: Ja
Stoppen weitere Regeln: Ja
```

---

### Szenario 7: Freiversand für Kategorien mit Promotion

**Ziel**: Freiversand für Bestellungen, die Artikel aus der Promotion-Kategorie enthalten.

**Konfiguration**:
```
Name: Freiversand für Promotion-Kategorie
Typ: Freiversand
Priorität: 90
Bedingungen:
  Erfordert Kategorien: ["Promotionen"]
Stoppen weitere Regeln: Ja
```

---

### Szenario 8: Möbel aus Freiversand ausschließen

**Ziel**: Freiversand ab 50 $, außer wenn der Warenkorb Möbel enthält.

**Lösung**: Zwei Regeln

**Regel 1**:
```
Name: Allgemeiner Freiversand
Typ: Freiversand
Priorität: 50
Bedingungen:
  Mindest-Warenkorbwert: 50 $
  Ausschlusskategorien: ["Möbel"]
Stoppen weitere Regeln: Nein
```

**Regel 2**:
```
Name: Möbelbestellungen mit 5 $ Rabatt
Typ: Rabatt (Fix)
Betrag: 5 $
Priorität: 40
Bedingungen:
  Erfordert Kategorien: ["Möbel"]
  Mindest-Warenkorbwert: 50 $
Stoppen weitere Regeln: Nein
```

---

## Strategien zur Kombination von Regeln

### Strategie 1: Rabatte叠加

**Mehrere Rabatte叠加 erlauben**:
```
Regel A (Priorität 100): 10 % Rabatt für VIP → stop_further_rules=Nein
Regel B (Priorität 50): 15 % Rabatt für Bestellungen > 100 $ → stop_further_rules=Nein

VIP-Kunde mit 120 $ Bestellung:
Basis: 15 $
Nach Regel A: 13,50 $ (10 % Rabatt)
Nach Regel B: 11,48 $ (15 % Rabatt auf 13,50 $)
```

### Strategie 2: Exklusive Regeln

**Nur eine Regel gilt** (höchste Priorität):
```
Regel A (Priorität 100): Freiversand > 50 $ → stop_further_rules=Ja
Regel B (Priorität 50): 20 % Rabatt auf alle Versandkosten → stop_further_rules=Ja

Bestellung > 50 $:
Regel A gilt → Freiversand → STOPPEN
Regel B wird nie ausgeführt
```

### Strategie 3: Bedingte Zuschläge

**Rabatte zuerst, Zuschläge zuletzt**:
```
Regel A (Priorität 100): Freiversand > 75 $
Regel B (Priorität 75): 15 % VIP-Rabatt
Regel C (Priorität 50): 10 % allgemeiner Rabatt
Regel D (Priorität 25): 5 $ Zuschlag für abgelegene Gebiete
Regel E (Priorität 1): 10 % Kraftstoffzuschlag

Bestellung: 80 $, abgelegene Zone, VIP-Kunde
Basis: 20 $
A: 80 $ > 75 $ → Freiversand (0 $)
B: VIP → 15 % Rabatt auf 0 $ = 0 $
C: 10 % Rabatt auf 0 $ = 0 $
D: Abgelegene Zone + 5 $ = 5 $
E: Kraftstoff + 10 % von 5 $ = 5,50 $

Ende: 5,50 $ (nicht kostenlos aufgrund der Zuschläge)

**Um dies zu verhindern, verwenden Sie stop_further_rules=Ja**:
```
Regel A (Priorität 100, stop=Ja): Freiversand > 75 $

Selbe Bestellung:
A: 80 $ > 75 $ → Freiversand (0 $) → STOPPEN
Ende: 0 $ (wirklich kostenlos)
```

---

## Testen von Versandregeln

**Bevor Sie online gehen**:

1. **Testwagenkörbe erstellen**
   - Warenkorb A: 25 $ (unterhalb des Schwellenwerts)
   - Warenkorb B: 55 $ (über dem Schwellenwert)
   - Warenkorb C: 200 $ + abgelegene Zone
   - Warenkorb D: VIP-Kunde

2. **Jede Regel testen**
   - Zum Checkout gehen
   - Überprüfen Sie, ob die korrekten Versandkosten angezeigt werden
   - Überprüfen Sie die Ausführungsreihenfolge der Regeln

3. **Testen Sie die Prioritätsauflösung**
   - Mehrere übereinstimmende Regeln
   - Überprüfen Sie, ob die höchste Priorität zuerst ausgeführt wird
   - Überprüfen Sie das Verhalten von stop_further_rules

4. **Testen Sie Randfälle**
   - Warenkorbwert genau am Schwellenwert
   - Mehrere Bedingungen, die übereinstimmen
   - Konfliktregeln

---

## Problembehandlung

**Problem 1: Regel gilt nicht**

**Ursachen**:
- Regel ist inaktiv
- Eine oder mehrere Bedingungen nicht erfüllt
- Höhere Prioritätsregel hat stop_further_rules=Ja
- Zeitliche Gültigkeit außerhalb des aktuellen Datums

**Lösung**: Alle Bedingungen überprüfen, Priorität prüfen, aktiven Status überprüfen.

---

**Problem 2: Unerwarteter Rabattbetrag**

**Ursachen**:
- Mehrere Regeln叠加
- Prozentsatz auf bereits rabattierte Kosten angewendet
- Falsche Priorität der Regel

**Lösung**: Prioritätsreihenfolge prüfen, stop_further_rules-Flaggen überprüfen, Ausführung manuell verfolgen.

---

**Problem 3: Freiversand funktioniert nicht**

**Ursachen**:
- Niedrigere Prioritätsregel fügt Kosten nach Freiversandregel hinzu
- Warenkorb erfüllt nicht den Mindestwert-Schwellenwert
- Ausschlussprodukte im Warenkorb

**Lösung**: Verwenden Sie stop_further_rules=Ja für Freiversandregel, Bedingungen überprüfen, Ausschlüsse prüfen.

---

## Tipps

- **Verwenden Sie eine hohe Priorität für Freiversand** – Priorität 100 stellt sicher, dass sie vor anderen Anpassungen ausgeführt wird
- **Setzen Sie stop_further_rules für absolute Regeln** – Freiversand sollte weitere Verarbeitung stoppen
- **Testen Sie Regelkombinationen** – Mehrere Regeln können unerwartet interagieren
- **Verwenden Sie beschreibende Namen** – "VIP 20 % Rabatt (Priorität 75)" ist besser als "Regel 3"
- **Dokumentieren Sie komplexe Logik** – Fügen Sie Notizen im Beschreibungsfeld hinzu
- **Beginnen Sie mit einfachen Regeln** – Fügen Sie Komplexität schrittweise hinzu
- **Überwachen Sie die Leistung der Regeln** – Prüfen Sie, ob Regeln verwendet werden oder Verwirrung verursachen
- **Vermeiden Sie zu viele Regeln** – Zu viele Regeln verlangsamen den Checkout, verwenden Sie maximal 5–10
- **Verwenden Sie Zonen für Geografie** – Besser als mehrere ähnliche Regeln pro Land
- **Kombinieren Sie mit Methoden** – Regeln + Methoden arbeiten zusammen für komplexere Preisgestaltung
- **Setzen Sie klare Zeitfenster** – Schließen Sie immer Enddaten für Promotionen ein
- **Testen Sie Randfälle** – Genau 50 $, genau 5 Artikel, etc.

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe genau wie in den Erhaltungsvorschriften gezeigt.
