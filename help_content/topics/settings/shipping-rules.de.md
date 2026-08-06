---
title: Versandregeln
---

Versandregeln wenden bedingte Kostenanpassungen für Versandmethoden anhand des Warenkorbinhalts, der Kundeneigenschaften und der Lieferzonen – bieten Sie automatisch kostenlose Lieferung über 50 $ an, zusätzliche Gebühren für abgelegene Gebiete an oder vergünstigen Sie den Versand für VIP-Kunden. Regeln verwenden Prioritäts-Execution (höhere Priorität zuerst) mit optionalen Stop-Flags, um weitere Verarbeitung zu verhindern. Jede Regel prüft mehrere Bedingungen (Warenkorb-Wert, Gewicht, Zonen, Produkte, Kundengruppen) und führt eine der 6 Anpassungstypen aus, wenn alle Bedingungen übereinstimmen.

Verwenden Sie Versandregeln, wenn Sie dynamische Versandkosten benötigen, die sich basierend auf dem Bestellkontext ändern, nicht nur statische Raten von Versandmethoden.

## Versandregeltypen

Versandregeln wenden 6 Arten von Kostenanpassungen an:

### Prozentsatz Rabatt

**Was es tut**: Reduziert den Versandkosten um Prozentsatz (z. B. 25% Rabatt).

**Formel**: `new_cost = base_cost × (1 - percent/100)`

**Beispiel**:
```
Basiskosten: 20 $ 
Rabatt: 25% 
Ergebnis: 15 $ 
```

**Anwendungsfälle**:
- VIP-Kundenrabatt (20% Rabatt auf alle Versandkosten)
- Saisonale Aktionen (15% Rabatt auf Versand im Dezember)
- Großauftragsrabatt (10% Rabatt auf Versand für 5+ Artikel)

---

### Fixer Rabatt

**Was es tut**: Subtrahiert festen Betrag von den Versandkosten.

**Formel**: `new_cost = base_cost - amount` (Mindestbetrag 0 $)

**Beispiel**:
```
Basiskosten: 15 $ 
Rabatt: 5 $ 
Ergebnis: 10 $ 
```

**Anwendungsfälle**:
- Bonus für Erstkunden (5 $ Rabatt auf Versandkosten für erste Bestellung)
- Newsletter-Anmeldung Belohnung (3 $ Rabatt auf Versandkosten)
- Treueprogramm Vorteil (10 $ Rabatt auf Versandkosten pro Monat)

---

### Festkosten

**Was es tut**: Überschreibt die Versandkosten auf bestimmten Betrag.

**Formel**: `new_cost = fixed_amount`

**Beispiel**:
```
Basiskosten: 25 $ 
Setzen auf: 9,99 $ 
Ergebnis: 9,99 $ 
```

**Anwendungsfälle**:
- Flash-Sale (flache 5 $ Versandkosten für alle Bestellungen heute)
- Kategoriespezifische Versandkosten (Bücher immer 3,99 $ Versandkosten)
- Zeitspezifische Aktionen (Versandkosten max. 9,99 $ diese Woche)

---

### Kostenlose Lieferung

**Was es tut**: Setzt die Versandkosten auf 0 $.

**Formel**: `new_cost = 0 $`

**Beispiel**:
```
Basiskosten: 18 $ 
Regel gilt 
Ergebnis: 0 $ 
```

**Anwendungsfälle**:
- Kostenlose Lieferung über 50 $ 
- Kostenlose Lieferung für bestimmte Produkte (werbende Artikel)
- Kostenlose Lieferung für VIP-Kunden
- Kostenlose Lieferung bei Bestellungen mit 3+ Artikeln

---

### Gebühr (Fixbetrag)

**Was es tut**: Fügt festen Betrag zu den Versandkosten hinzu.

**Formel**: `new_cost = base_cost + amount`

**Beispiel**:
```
Basiskosten: 12 $ 
Gebühr: 5 $ 
Ergebnis: 17 $ 
```

**Anwendungsfälle**:
- Gebühr für abgelegene Gebiete
- Übermäßige Artikel Handhabung
- Samstag Liefergebühr
- Zerbrechliches Artikel Verpackungsgebühr

---

### Gebühr (Prozentsatz)

**Was es tut**: Erhöht die Versandkosten um Prozentsatz.

**Formel**: `new_cost = base_cost × (1 + percent/100)`

**Beispiel**:
```
Basiskosten: 20 $ 
Gebühr: 15% 
Ergebnis: 23 $ 
```

**Anwendungsfälle**:
- Hochsaison Gebühr (20% während Feiertage)
- Express Lieferung Premium (50% Gebühr)
- Kraftstoffgebühr (variabel basierend auf aktuellen Raten)

---

## Regelbedingungen

Regeln bewerten **ALLE Bedingungen müssen erfüllt werden**, damit die Regel angewandt wird:

### Zeitliche Gültigkeit

- **Startdatum**: Regel nur nach diesem Datum aktiv
- **Enddatum**: Regel nur vor diesem Datum aktiv
- **Anwendungsfall**: Saisonale Aktionen, zeitlich begrenzte Angebote

**Beispiel**: Kostenlose Lieferung am Black Friday Wochenende nur
```
Start: 2026-11-27 00:00 
Ende: 2026-11-30 23:59 
```

---

### Warenkorb-Wertebereich

- **Mindest-Warenkorb-Wert**: Warenkorb-Unterstufe muss ≥ Betrag sein
- **Maximal-Warenkorb-Wert**: Warenkorb-Unterstufe muss ≤ Betrag sein
- **Anwendungsfall**: Kostenlose Lieferung Schwellenwerte, gestaffelte Rabatte

**Beispiel**: Kostenlose Lieferung für Bestellungen 50 $ - 200 $
```
Min: 50 $ 
Max: 200 $ 
```

---

### Gewichtebereich des Warenkorbs

- **Mindestgewicht**: Gesamt-Warenkorbgewicht muss ≥ Betrag sein
- **Maximalgewicht**: Gesamt-Warenkorbgewicht muss ≤ Betrag sein
- **Anwendungsfall**: Leichtes Versandkostenrabatt, schweres Artikelgebühr

**Beispiel**: 5 $ Gebühr für Bestellungen über 20 kg
```
Mindestgewicht: 20 kg 
Maximalgewicht: null (unbegrenzt) 
```

---

### Anzahl der Artikel

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **Min Item Count**: Der Warenkorb muss ≥ Anzahl von Artikeln enthalten
- **Max Item Count**: Der Warenkorb muss ≤ Anzahl von Artikeln enthalten
- **Use Case**: Mengenrabatte für Großaufträge, Einzelartikelgebühren

**Beispiel**: Kostenlose Lieferung für 5+ Artikel
```
Min Items: 5
Max Items: null
```


### Versandzone

- **Zonen**: Die Regel gilt nur, wenn die Adresse des Kunden mindestens einer ausgewählten Zone entspricht
- **Leere Auswahl**: Die Regel gilt für ALLE Zonen
- **Use Case**: Zonenspezifische Gebühren oder Rabatte

**Beispiel**: Kostenlose Lieferung nur für die Inlandzone
```
Zones: ["Domestic USA"]
```


### Versandmethode

- **Methode**: Die Regel gilt nur für bestimmte Versandmethoden
- **Leere Auswahl**: Die Regel gilt für ALLE Methoden
- **Use Case**: Methodenspezifische Aktionen

**Beispiel**: 25 % Rabatt auf Express-Versand
```
Methods: ["Express Delivery"]
```


### Produktauswahl

**Erfordert Produkte**: Der Warenkorb muss mindestens eines dieser Produkte enthalten

**Erfordert Kategorien**: Der Warenkorb muss mindestens ein Produkt aus diesen Kategorien enthalten

**Use Case**: Produktspezifische kostenlose Lieferung, Werbepakete

**Beispiel**: Kostenlose Lieferung, wenn der Warenkorb "Beworbenes Produkt A" enthält
```
Erfordert Produkte: [Produkt-ID 123]
```


### Produktexklusionen

**Exkludiert Produkte**: Die Regel gilt nicht, wenn der Warenkorb eines dieser Produkte enthält

**Exkludiert Kategorien**: Die Regel gilt nicht, wenn der Warenkorb Produkte aus diesen Kategorien enthält

**Use Case**: Schweres/Oversized-Objekte von kostenlosem Versand ausschließen

**Beispiel**: Kostenlose Lieferung außerhalb der Möbelkategorie
```
Exkludiert Kategorien: [Möbel]
```


### Kundengruppe

- **Kundengruppen**: Die Regel gilt nur für Kunden in ausgewählten Gruppen (VIP, Großhandel, etc.)
- **Leere Auswahl**: Die Regel gilt für ALLE Kundengruppen
- **Use Case**: VIP-Benefits, Großhandelsrabatte

**Beispiel**: 15 % Rabatt auf Versand für VIP-Mitglieder
```
Kundengruppen: ["VIP"]
```


### Erstmaliger Kunde

- **Erstmaliger Kunde**: Schalter, um die Regel auf Kunden mit keinem vorherigen Auftrag zu beschränken
- **Use Case**: Willkommensangebote für neue Kunden

**Beispiel**: 5 $ Rabatt auf Versand für den ersten Auftrag
```
Erstmaliger Kunde: Ja
```


## Regel-Priorität & Ausführung

Regeln werden in **Prioritätsreihenfolge** ausgeführt (höhere Nummer = frühere Ausführung):

### Prioritätsmechanismen

**Beispiel-Ausführung**:
```
Regel A (Priorität 100): Kostenlose Lieferung, wenn Warenkorb > 50 $
Regel B (Priorität 50): 10 % Rabatt auf alle Versandkosten
Regel C (Priorität 1): 2 $ Gebühr für abgelegene Zonen

Warenkorb: 60 $, abgelegene Zone
Grundlieferkosten: 15 $

Schritt 1: Regel A prüft (Priorität 100)
  Warenkorb > 50 $? JA
  Anwenden: Kosten auf 0 setzen
  Kosten jetzt: 0 $

Schritt 2: Regel B prüft (Priorität 50)
  10 % Rabatt auf 0 $
  Kosten jetzt: 0 $ (immer noch kostenlos)

Schritt 3: Regel C prüft (Priorität 1)
  2 $ Gebühr zu 0 $ hinzufügen
  Kosten jetzt: 2 $

Endgültiger Betrag: 2 $
```

**Weiteres Ausführen-Flag**:

Wenn Regel A `stop_further_rules = True` hat:
```
Regel A (Priorität 100, stop_further_rules=True): Kostenlose Lieferung, wenn Warenkorb > 50 $
Regel B (Priorität 50): 10 % Rabatt auf alle Versandkosten
Regel C (Priorität 1): 2 $ Gebühr für abgelegene Zonen

Warenkorb: 60 $
Basis: 15 $

Schritt 1: Regel A greift, setzt Kosten auf 0 $
        stop_further_rules = True → STOP

Endgültiger Betrag: 0 $ (Regel B und C werden nie ausgeführt)
```


## Erstellen von Versandregeln

**Schritt-für-Schritt-Workflow**:

1. **Zu Regeln navigieren**
   - Einstellungen > Versand > Versandregeln
   - Auf "Neue Versandregel hinzufügen" klicken

2. **Grundlegende Konfiguration**
   - **Name**: Interner Bezeichner (z. B. "Kostenlose Lieferung über 50 $")
   - **Beschreibung**: Optionale Notizen (nicht für Kunden sichtbar)
   - **Aktiv**: Schalter zum Aktivieren/Deaktivieren
   - **Priorität**: Ausführungsreihenfolge festlegen (100 für hohe Priorität, 1 für niedrige)

3. **Regeltyp auswählen**
   - Wählen Sie den Anpassungstyp (Rabatt %, fester Rabatt, Kosten setzen, kostenlos, Prozentgebühr, feste Gebühr)
   - Geben Sie Betrag oder Prozentsatz ein

4. **Stop-Flag setzen** (Optional)
   - Wenn diese Regel die Ausführung von niedrigeren Prioritätsregeln verhindern soll, "Weitere Regeln stoppen" markieren
   - Für endgültige/absolute Regeln verwenden (z. B. kostenlose Lieferung sollte keine Gebühren nachträglich enthalten)


5. **Bedingungen definieren** (Optional - leer lassen für "immer anwenden")
  - Zeitliche Gültigkeit: Start-/Enddaten
  - Warenkorb-Wert: Min./Max.
  - Warenkorb-Gewicht: Min./Max.
  - Anzahl der Artikel: Min./Max.
  - Zonen: Angegebene Zonen auswählen
  - Methoden: Angegebene Methoden auswählen
  - Produkte: Erforderlich oder ausgeschlossen
  - Kunden: Gruppen oder nur erstmals

6. **Regel speichern**
  - Auf Speichern klicken
  - Die Regel ist sofort aktiv (wenn der Aktivierungsschalter auf Ja steht)


## Häufige Versandregel-Szenarien

### Szenario 1: Kostenlose Lieferung ab $50

**Ziel**: Kostenlose Lieferung anbieten, wenn der Warenkorbbetrag ≥ $50.

**Konfiguration**:
```
Name: Kostenlose Lieferung ab $50
Typ: Kostenlose Lieferung
Priorität: 100
Bedingungen:
  Min. Warenkorb-Wert: $50
Weitere Regeln unterbrechen: Ja
```


### Szenario 2: Gebühr für abgelegene Gebiete

**Ziel**: Eine Gebühr von $10 für Lieferungen in abgelegene Gebiete hinzufügen.

**Konfiguration**:
```
Name: Gebühr für abgelegene Gebiete
Typ: Gebühr (Fixbetrag)
Betrag: $10
Priorität: 50
Bedingungen:
  Zonen: ["Abgelegene Gebiete"]
Weitere Regeln unterbrechen: Nein
```


### Szenario 3: 20 % Rabatt für VIP-Kunden

**Ziel**: VIP-Kunden erhalten 20 % Rabatt auf alle Versandkosten.

**Konfiguration**:
```
Name: VIP-Versandrabatt
Typ: Rabatt (Prozentsatz)
Prozentsatz: 20
Priorität: 75
Bedingungen:
  Kundengruppen: ["VIP"]
Weitere Regeln unterbrechen: Nein
```


### Szenario 4: Festpreis-Aktion im Dezember

**Ziel**: Alle Versandkosten im Dezember auf $9.99 begrenzen.

**Konfiguration**:
```
Name: Dezember-Festpreis-Aktion
Typ: Festpreis
Betrag: $9.99
Priorität: 100
Bedingungen:
  Startdatum: 2026-12-01
  Enddatum: 2026-12-31
Weitere Regeln unterbrechen: Ja
```


### Szenario 5: Gebühr für schwere Artikel

**Ziel**: Gebühr von $15 für Bestellungen über 25 kg hinzufügen.

**Konfiguration**:
```
Name: Gebühr für schwere Bestellungen
Typ: Gebühr (Fixbetrag)
Betrag: $15
Priorität: 50
Bedingungen:
  Mindestgewicht: 25kg
Weitere Regeln unterbrechen: Nein
```


### Szenario 6: Kostenlose Lieferung für Neukunden

**Ziel**: Neue Kunden erhalten kostenlose Lieferung bei Erstbestellung.

**Konfiguration**:
```
Name: Kostenlose Lieferung für Erstbestellung
Typ: Kostenlose Lieferung
Priorität: 100
Bedingungen:
  Erstmaliger Kunde: Ja
Weitere Regeln unterbrechen: Ja
```


### Szenario 7: Kategoriespezifische kostenlose Lieferung

**Ziel**: Kostenlose Lieferung für Bestellungen, die Artikel aus der Kategorie "Promotion" enthalten.

**Konfiguration**:
```
Name: Kostenlose Lieferung für Promotion-Kategorie
Typ: Kostenlose Lieferung
Priorität: 90
Bedingungen:
  Erforderliche Kategorien: ["Promotionen"]
Weitere Regeln unterbrechen: Ja
```


### Szenario 8: Möbel von kostenlosem Versand ausschließen

**Ziel**: Kostenlose Lieferung ab $50, außer wenn der Warenkorb Möbel enthält.

**Lösung**: Zwei Regeln

**Regel 1**:
```
Name: Allgemeine kostenlose Lieferung
Typ: Kostenlose Lieferung
Priorität: 50
Bedingungen:
  Min. Warenkorb-Wert: $50
  Ausschlüsse Kategorien: ["Möbel"]
Weitere Regeln unterbrechen: Nein
```

**Regel 2**:
```
Name: $5 Rabatt für Möbelbestellungen
Typ: Rabatt (Fixbetrag)
Betrag: $5
Priorität: 40
Bedingungen:
  Erforderliche Kategorien: ["Möbel"]
  Min. Warenkorb-Wert: $50
Weitere Regeln unterbrechen: Nein
```


## Strategien zur Kombination von Regeln

### Strategie 1: Aufeinanderstehende Rabatte

**Mehrere Rabatte können kombiniert werden**:
```
Regel A (Priorität 100): 10 % Rabatt für VIP → stop_further_rules=Nein
Regel B (Priorität 50): 15 % Rabatt für Bestellungen >$100 → stop_further_rules=Nein

VIP-Kunde mit $120 Bestellung:
Grundbetrag: $15
Nach Regel A: $13.50 (10 % Rabatt)
Nach Regel B: $11.48 (15 % Rabatt von $13.50)
```


### Strategie 2: Exklusive Regeln

**Nur eine Regel gilt** (höchste Priorität):
```
Regel A (Priorität 100): Kostenlose Lieferung >$50 → stop_further_rules=Ja
Regel B (Priorität 50): 20 % Rabatt auf alle Versandkosten → stop_further_rules=Ja

Warenkorb > $50:
Regel A gilt → Kostenlose Lieferung → STOPP
Regel B wird nie ausgeführt
```


### Strategie 3: Bedingte Gebühren

**Rabatte zuerst, Gebühren zuletzt**:
```
Regel A (Priorität 100): Kostenlose Lieferung >$75
Regel B (Priorität 75): 15 % VIP-Rabatt
Regel C (Priorität 50): 10 % allgemeiner Rabatt
Regel D (Priorität 25): $5 Gebühr für abgelegene Gebiete
Regel E (Priorität 1): 10 % Kraftstoffgebühr

Bestellung: $80, abgelegene Zone, VIP-Kunde
Grundbetrag: $20
A: $80 > $75 → Kostenlose Lieferung ($0)
B: VIP → 15 % Rabatt von $0 = $0
C: 10 % Rabatt von $0 = $0
D: Abgelegene Zone +$5 = $5
E: Kraftstoff +10 % von $5 = $5.50
```


Preserve all markdown formatting, image paths, code blocks, and technical terms.

Endgültig: 5,50 € (nicht kostenlos aufgrund von Zuschlägen)
```

**Um dies zu verhindern, stop_further_rules=Ja verwenden**:
```
Regel A (Priorität 100, stop=Ja): Kostenlose Lieferung >75 €

Selbe Bestellung:
A: 80 € > 75 € → Kostenlos (0 €) → STOPP
Endgültig: 0 € (echt kostenlos)
```


## Shipping-Regeln testen

**Bevor Sie live gehen**:

1. **Test-Körbe erstellen**
   - Korb A: 25 € (unter Grenzwert)
   - Korb B: 55 € (über Grenzwert)
   - Korb C: 200 € + abgelegenes Gebiet
   - Korb D: VIP-Kunde

2. **Jede Regel testen**
   - Zur Kasse gehen
   - Prüfen, ob die richtige Versandkostenanzeige angezeigt wird
   - Prüfen, in welcher Reihenfolge die Regel ausgeführt wird

3. **Priorität lösen**
   - Mehrere übereinstimmende Regeln
   - Prüfen, ob die höchste Priorität zuerst ausgeführt wird
   - Prüfen, wie sich stop_further_rules verhält

4. **Randfälle testen**
   - Der Warenkorbwert liegt genau am Schwellwert
   - Mehrere Bedingungen passen
   - Konfliktregeln


## Fehlerbehebung

**Problem 1: Regel wird nicht angewandt**

**Ursachen**:
- Die Regel ist deaktiviert
- Eine oder mehrere Bedingungen sind nicht erfüllt
- Eine höhere Prioritätsregel hat stop_further_rules=Ja gesetzt
- Der Gültigkeitszeitraum liegt außerhalb des aktuellen Datums

**Lösung**: Überprüfen Sie alle Bedingungen, prüfen Sie die Priorität und stellen Sie sicher, dass der Status aktiviert ist.


**Problem 2: Unerwarteter Rabattbetrag**

**Ursachen**:
- Mehrere Regeln werden übereinandergelegt
- Ein Prozentsatz wird auf bereits reduzierten Preis angewandt
- Die Priorität der Regel ist falsch

**Lösung**: Prüfen Sie die Prioritätsreihenfolge, überprüfen Sie die Flags von stop_further_rules und führen Sie die Ausführung manuell nachvollziehbar durch.


**Problem 3: Kostenlose Lieferung funktioniert nicht**

**Ursachen**:
- Eine niedrigere Prioritäts-Zuschlagsregel fügt Kosten hinzu, nachdem die kostenlose Lieferungsregel angewandt wurde
- Der Warenkorb erfüllt nicht den Mindestwert
- Ausgeschlossene Produkte im Warenkorb

**Lösung**: Setzen Sie stop_further_rules=Ja auf der kostenlosen Lieferungsregel ein, prüfen Sie die Bedingungen und überprüfen Sie die Ausschlüsse.


## Tipps

- **Verwenden Sie eine hohe Priorität für kostenlose Lieferung** - Priorität 100 stellt sicher, dass sie vor anderen Anpassungen ausgeführt wird
- **Setzen Sie stop_further_rules für absolute Regeln** - Kostenlose Lieferung sollte die weitere Verarbeitung stoppen
- **Testen Sie Regelkombinationen** - Mehrere Regeln können unerwartet interagieren
- **Verwenden Sie beschreibende Namen** - „VIP-20%-Rabatt (Priorität 75)“ ist besser als „Regel 3“
- **Dokumentieren Sie komplexe Logik** - Fügen Sie Notizen in das Beschreibungsfeld ein
- **Beginnen Sie mit einfachen Regeln** - Fügen Sie die Komplexität schrittweise hinzu
- **Überwachen Sie die Regelperformance** - Prüfen Sie, ob Regeln genutzt werden oder Verwirrung stiften
- **Vermeiden Sie zu viele Regeln** - Zu viele Regeln verlangsamen die Kasse, verwenden Sie maximal 5-10
- **Verwenden Sie Gebiete für Geografie** - Besser als mehrere ähnliche Regeln pro Land
- **Kombinieren Sie mit Methoden** - Regeln + Methoden arbeiten zusammen, um fortgeschrittene Preise zu erstellen
- **Legen Sie klare Zeitspannen fest** - Nehmen Sie immer Enddaten für Promotionen auf
- **Testen Sie Randfälle** - Genau 50 €, genau 5 Artikel usw.