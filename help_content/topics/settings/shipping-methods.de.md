---
title: Versandmethoden
---

Versandmethoden sind die für Kunden sichtbaren Lieferoptionen, die beim Checkout angezeigt werden – jede Methode berechnet die Versandkosten mithilfe unterschiedlicher Preisgestaltungsstrategien. Spwig unterstützt 7 Methodentypen, die von einfachen Flachraten bis hin zu komplexen, von Versandpartnern berechneten Echtzeitpreisen reichen. Methoden können anhand von Mindest-/Höchstbestellwert, Gewicht und geografischen Zonen eingeschränkt werden. Kunden wählen während des Checkouts ihre bevorzugte Methode aus, und die berechneten Kosten werden ihrem Bestellgesamtbetrag hinzugefügt.

Verwenden Sie diesen Leitfaden, um Versandmethoden zu konfigurieren, die Ihrem Geschäftsmodell entsprechen, von grundlegenden Flachratenversand bis hin zu komplexen, auf Zonen basierenden Stufenpreisen.

## Typen der Versandmethoden

Spwig bietet 7 Typen von Versandmethoden an, wobei jeder Typ eine andere Kostenberechnungslogik verwendet:

### Flachratenversand

**Was es ist**: Fixer Preis, unabhängig vom Inhalt des Warenkorbs, Zielort oder Gewicht.

**Wann verwenden**: 
- Einfache Geschäfte mit vorhersehbaren Versandkosten
- Ein Produkttyp (ähnliche Größe/Gewicht)
- Nur nationale Versandoptionen mit Standardversandkosten
- Freiversand-Aktionen (verwenden Sie dies mit Versandaktionen)

**Konfiguration**: 
- Setzen Sie **Methodentyp** = Flachratenversand
- Geben Sie den **Fixen Preis** ein (z. B. 9,99 $)
- Optional: Legen Sie Mindest-/Höchstbestellwert-Einschränkungen fest

**Beispiel**: "Standardversand - 9,99 $" für alle nationalen Bestellungen.

---

### Freiversand

**Was es ist**: Versandoption mit Null Kosten (keine Gebühr für den Kunden).

**Wann verwenden**: 
- Freiversand-Aktionen
- Hochwertige Bestellungen (kombinieren Sie dies mit Mindestbestellwert)
- Alternative zum lokalen Abholen
- Vorteile von Treueprogrammen

**Konfiguration**: 
- Setzen Sie **Methodentyp** = Freiversand
- Optional: Legen Sie **Mindestbestellwert** fest (z. B. Freiversand ab 50 $)
- Funktioniert gut mit Versandaktionen für bedingten Freiversand

**Beispiel**: "Freiversand für Bestellungen über 50 $" mit min_order_value = 50 $.

---

### Gewichtsbasiert

**Was es ist**: Kosten werden anhand einer Stufenpreistabelle basierend auf dem Gesamtgewicht des Warenkorbs berechnet.

**Wann verwenden**: 
- Produkte mit variierenden Gewichten (Bücher, Hardware, Lebensmittel)
- Gewichtsbasierte Versandkostenmodelle der Versandpartner
- Vorhersehbare Gewichts-Kosten-Verhältnisse

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Gewichtsbasiert
2. Erstellen Sie eine **Versandkosten-Tabelle** mit basis_type = "gewicht"
3. Fügen Sie **Versandkosten-Stufen** hinzu (z. B. 0-5 kg = 10 $, 5-10 kg = 15 $, 10-20 kg = 25 $)
4. Optional: Einschränkung auf bestimmte Zonen

**Beispiel**: 
```
0-2 kg: 8 $
2-5 kg: 12 $
5-10 kg: 18 $
10 kg+: 25 $
```

**Funktionsweise**: Der Warenkorb berechnet das Gesamtgewicht → findet die passende Stufe → gibt die Stufenrate zurück.

---

### Preisbasiert

**Was es ist**: Kosten werden anhand einer Stufenpreistabelle basierend auf dem Warenkorb-Subtotal berechnet.

**Wann verwenden**: 
- Versandkosten korrelieren mit dem Bestellwert
- Höhere Warenkorbwerte fördern (niedrigere Rate pro Dollar bei höheren Stufen)
- Einfache Alternative zum Gewichtsbasierten für ähnliche Preise

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Preisbasiert
2. Erstellen Sie eine **Versandkosten-Tabelle** mit basis_type = "preis"
3. Fügen Sie **Versandkosten-Stufen** hinzu (z. B. 0-50 $ = 9,99 $, 50-100 $ = 14,99 $, 100+ $ = 19,99 $)

**Beispiel**: 
```
0-25 $: 6,99 $
25-75 $: 9,99 $
75-150 $: 12,99 $
150+ $: Frei
```

**Funktionsweise**: Der Warenkorb berechnet den Subtotal → findet die passende Stufe → gibt die Stufenrate zurück.

---

### Echtzeit-Versandkosten

**Was es ist**: Live-Raten, die von Versandpartner-APIs (FedEx, UPS, DHL) beim Checkout abgerufen werden.

**Wann verwenden**: 
- Variable Versandkosten je nach Zielort
- Mehrere Versandoptionen für Kunden
- Genauere Versandkosten ohne manuelle Ratenlisten
- Internationale Versandoptionen mit komplexen Preisen

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Echtzeit
2. Erstellen Sie ein **Anbieterkonto** (Einstellungen > Versand > Anbieterkonten)
3. Geben Sie die API-Anmeldeinformationen des Versandpartners ein (Kontonummer, API-Schlüssel, Geheimnis)
4. Verknüpfen Sie das Anbieterkonto mit der Versandmethode
5. Optional: Fügen Sie eine Mark-up-Prozent oder einen festen Mark-up hinzu

**Voraussetzungen**: 
- Aktives Versandkonto (FedEx, UPS, DHL usw.)
- API-Anmeldeinformationen vom Versandpartner
- Definierte Versandverpackungen (für die Berechnung des Volumengewichts)


**Beispiel**: Die Methode "FedEx Ground" ruft live FedEx-Preise basierend auf dem Warenkorb-Gewicht, den Abmessungen und dem Zielort zur Kasse ab.

**Funktionsweise**:
1. Der Kunde gibt seine Adresse zur Kasse ein
2. Das System ruft die API des Versandunternehmers mit Ursprung, Zielort, Paketabmessungen und Gewicht auf
3. Das Versandunternehmen gibt ein Preisangebot zurück
4. Optional wird eine Aufschlagsspanne angewendet
5. Das Angebot wird dem Kunden angezeigt

---

### Lokale Abholung

**Was es ist**: Der Kunde holt die Bestellung an einem physischen Standort ab (keine Versandkosten).

**Wann verwenden**:
- Einzelhandelsgeschäfte, die Abholung anbieten
- Lagerhaus-Abholoptionen
- Veranstaltungen oder Marktstände
- Versandkosten für lokale Kunden eliminieren

**Konfiguration**:
1. Setze **Methode-Typ** = Lokale Abholung
2. Erstelle **Standort** (Einstellungen > Versand > Standorte)
   - Setze Adresse, Betriebszeiten, Abholkapazität
3. Verknüpfe Standort(e) mit der Methode
4. Optional: Setze die Vorbereitungszeit für die Abholung (z. B. "In 2 Stunden bereit")

**Kundenerlebnis**:
- Wählt "Lokale Abholung" zur Kasse
- Wählt den Abholstandort (wenn mehrere vorhanden sind)
- Wählt Datum/Zeit basierend auf der Verfügbarkeit
- Erhält eine Benachrichtigung, wenn die Bestellung bereit ist

**Beispiel**: "Abholung im Geschäft - Kostenlos" mit 3 Einzelhandelsgeschäften, bereit innerhalb von 24 Stunden.

---

### Tabellenbasierte Versandkosten

**Was es ist**: Flexibles, gestaffeltes Preismodell basierend auf Gewicht, Preis oder Menge mit erweiterten Zonen-Targeting.

**Wann verwenden**:
- Komplexe Preisgestaltung (unterschiedliche Preise pro Zone und Gewicht)
- Mehr Kontrolle als bei Gewichts- oder preisbasierten Methoden
- Mehrere Preisfaktoren (z. B. Gewicht + Zielort + Menge)

**Konfiguration**:
1. Setze **Methode-Typ** = Tabellenbasiert
2. Erstelle **Versandkosten-Tabelle**
3. Definiere **Basis-Typ**: Gewicht, Preis oder Menge
4. Füge **Versandkosten-Stufen** mit Min-/Max-Werten hinzu
5. Optional: Beschränke Stufen auf bestimmte Zonen oder Länder

**Unterschied zu Gewicht-/Preisbasiert**: Tabellenbasierte Versandkosten unterstützen geografische Einschränkungen pro Stufe, was unterschiedliche Preise für dasselbe Gewicht/Preis in verschiedenen Zonen ermöglicht.

**Beispiel**:
```
Zone A (Inland):
  0-5kg: $10
  5-10kg: $15

Zone B (Entfernt):
  0-5kg: $18
  5-10kg: $25
```

**Funktionsweise**: Der Warenkorb berechnet den Basiswert (Gewicht/Preis/Menge) → findet die passende Stufe für die Zone des Kunden → gibt die Stufenrate zurück.

---

## Konfiguration der Versandmethode

Alle Versandmethoden teilen sich diese allgemeinen Einstellungen:

### Grundlegende Einstellungen

- **Name**: Interner Bezeichner (wird Kunden nicht angezeigt)
- **Anzeigename**: Kundenfreundlicher Name zur Kasse (z. B. "Standardversand", "Expresslieferung")
- **Beschreibung**: Optionaler Hilfetext zur Kasse (z. B. "Lieferung in 3-5 Werktagen")
- **Methode-Typ**: Einer der 7 Typen oben
- **Aktiv**: Schalter zum Aktivieren/Deaktivieren der Methode ohne Löschen

### Kosten-Einstellungen

- **Fixkosten**: Nur für Flachrate-Methoden
- **Kostentabelle**: Für gewichtsbasierte, preisbasierte und tabellenbasierte Methoden
- **Provider-Konto**: Für Echtzeit-Versandunternehmen-Methoden
- **Steuerklasse**: Steuer auf Versandkosten anwenden (wenn zutreffend)

### Einschränkungen

**Bestellwert-Einschränkungen**:
- **Mindestbestellwert**: Methode nur verfügbar, wenn der Warenkorb-Subtotal ≥ Betrag (z. B. kostenlose Lieferung ab $50)
- **Höchstbestellwert**: Methode verborgen, wenn der Warenkorb-Subtotal > Betrag (z. B. Flachrate nur für Bestellungen unter $100)

**Gewichtseinschränkungen**:
- **Mindestgewicht**: Methode nur verfügbar, wenn das Warenkorb-Gewicht ≥ Betrag
- **Maximalgewicht**: Methode verborgen, wenn das Warenkorb-Gewicht > Betrag (häufig bei leichten Versandoptionen)

**Geografische Einschränkungen**:
- **Versandzonen**: Verknüpfe Methode mit bestimmten Zonen (inländisch, international, regional)
- Leere Zonen = für alle Adressen verfügbar
- Mehrere Zonen = für jede passende Zone verfügbar

### Erweiterte Einstellungen

- **Priorität**: Anzeigereihenfolge zur Kasse (kleinere Zahl = höher in der Liste)
- **Bearbeitungsgebühr**: Zusätzliche Flachgebühr, die zur berechneten Kosten hinzugefügt wird
- **Freiversand-Schwellenwert**: Setze Kosten automatisch auf $0, wenn der Warenkorb-Subtotal ≥ Schwellenwert (Alternative zu min_order_value)

---

## Versandmethode erstellen

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigiere zu Versandmethoden**
   - Gehe zu Einstellungen > Warenkorb > Versandmethoden
   - Klicke auf "Versandmethode hinzufügen"


2. **Methode auswählen**
   - Wählen Sie die passende Methode basierend auf Ihrer Preisstrategie
   - Die Methode bestimmt die verfügbaren Kostenkonfigurationsfelder

3. **Basisinformationen konfigurieren**
   - Name: Interne Referenz (z. B. "domestic_ground")
   - Anzeigename: Kundenseitig (z. B. "Ground Shipping")
   - Beschreibung: Lieferzeitraum (z. B. "5-7 Werktagen")

4. **Kostenberechnung festlegen**
   - **Flachrate**: Festen Preis eingeben
   - **Gewicht/Preis/Tabelle**: Tabelle erstellen (siehe unten)
   - **Echtzeit**: Anbieterkonto verknüpfen
   - **Kostenlos/Abholung**: Keine Kostenkonfiguration erforderlich

5. **Einschränkungen hinzufügen (optional)**
   - Mindest-/Höchstbestellwert
   - Mindest-/Höchstgewicht
   - Versandzonen

6. **Priorität festlegen**
   - Niedrigere Zahlen werden zuerst im Checkout angezeigt
   - Empfohlene Reihenfolge: Kostenlos (1), Lokale Abholung (2), Standard (3), Express (4)

7. **Methode aktivieren**
   - Schalter "Aktiv" = Ja
   - Speichern

---

## Rate-Tabellen erstellen

Für gewichtsbasierte, preisbasierte und tabellenbasierte Methoden:

**Schritt 1: Rate-Tabelle erstellen**
- Gehe zu Einstellungen > Versand > Rate-Tabellen
- Klicke auf "Rate-Tabelle hinzufügen"
- Setze **Name** (z. B. "Domestic Weight Tiers")
- Setze **Basis-Typ**: Gewicht, Preis oder Menge

**Schritt 2: Tiers hinzufügen**
- Klicke auf "Tier hinzufügen"
- Setze **Mindestwert** und **Höchstwert** (Bereich für Übereinstimmung)
- Setze **Rate** (Kosten für dieses Tier)
- Optional: Einschränkung auf bestimmte Zonen oder Länder
- Speichere das Tier

**Schritt 3: Für alle Tiers wiederholen**
- Decke den gesamten Bereich ab (0 bis maximaler erwarteter Wert)
- Stelle sicher, dass keine Lücken vorhanden sind (z. B. 0-5, 5-10, 10-20, 20+)
- Verwende `null` für den Höchstwert im letzten Tier (unbegrenzt)

**Schritt 4: Mit der Versandmethode verknüpfen**
- Bearbeite die Versandmethode
- Wähle die Rate-Tabelle aus dem Dropdown aus
- Speichere

**Beispiel einer gewichtsbasierten Tabelle**:
```
Name: Domestic Weight Tiers
Basis: Gewicht

Tiers:
1. Min: 0g, Max: 2000g, Rate: $8
2. Min: 2000g, Max: 5000g, Rate: $12
3. Min: 5000g, Max: 10000g, Rate: $18
4. Min: 10000g, Max: null, Rate: $25
```

---

## Typische Versand-Szenarien

### Szenario 1: Grundlegender Inlandsversand

**Ziel**: Einfache Flachrate von $9,99 für alle Inlandsbestellungen.

**Lösung**:
- Methode-Typ: Flachrate
- Fixer Preis: $9,99
- Versandzone: "Domestic" (nur Ihr Land)

---

### Szenario 2: Kostenloser Versand ab $50

**Ziel**: Höhere Warenkorbwerte durch einen kostenlosen Versandsschwellenwert fördern.

**Lösungsoption A** (Empfohlen):
- Methode-Typ: Kostenloser Versand
- Mindestbestellwert: $50
- Anzeigename: "Kostenloser Versand (Bestellungen $50+)")

**Lösungsoption B** (Mit Regeln):
- Methode-Typ: Flachrate
- Fixer Preis: $9,99
- Erstelle einen Versandrabatt:
  - Bedingung: Warenkorbwert ≥ $50
  - Aktion: Kosten auf $0 setzen

---

### Szenario 3: Gewichtsbasiert Inland + International

**Ziel**: Unterschiedliche Preise für Inland und International basierend auf Gewicht.

**Lösung**:
1. Erstelle 2 Zonen: "Domestic", "International"
2. Erstelle 2 Rate-Tabellen: "Domestic Weight", "International Weight"
3. Erstelle 2 Methoden:
   - "Domestic Shipping" → verknüpft mit Domestic-Zone + Domestic Weight-Tabelle
   - "International Shipping" → verknüpft mit International-Zone + International Weight-Tabelle

---

### Szenario 4: Mehrere Versandoptionen

**Ziel**: Kunden können zwischen FedEx Ground, FedEx Express und UPS Ground wählen.

**Lösung**:
1. Erstelle Anbieterkonto für FedEx API
2. Erstelle Anbieterkonto für UPS API
3. Erstelle 3 Echtzeitmethoden:
   - "FedEx Ground" → FedEx-Anbieter, Dienstcode = "FEDEX_GROUND"
   - "FedEx Express" → FedEx-Anbieter, Dienstcode = "FEDEX_EXPRESS"
   - "UPS Ground" → UPS-Anbieter, Dienstcode = "UPS_GROUND"
4. Alle 3 Methoden fragen die Anbieter-APIs beim Checkout ab und zeigen Live-Raten an

---

### Szenario 5: Lokale Abholung + Lieferung

**Ziel**: Ein Einzelhandelsgeschäft bietet sowohl Abholung als auch Lieferoptionen an.

**Lösung**:
1. Erstelle Standort: "Main Store" mit Adresse, Öffnungszeiten und Vorbereitungszeit
2. Erstelle 2 Methoden:
   - "Local Pickup" → Lokale Abholung, verknüpft mit Main Store-Position
   - "Standard Delivery" → Flachrate $9,99
3. Kunden sehen beide Optionen beim Checkout

---

## Versandmethoden testen

Bevor Sie online gehen, testen Sie alle Methoden:


1. **Testwagen erstellen**
   - Produkte mit unterschiedlichen Gewichten/Preisen hinzufügen
   - Zum Checkout weitergehen

2. **Jede Methode testen**
   - Adressen in verschiedenen Zonen eingeben
   - Überprüfen, ob die richtigen Methoden angezeigt werden
   - Prüfen, ob die berechneten Kosten den Erwartungen entsprechen

3. **Einschränkungen testen**
   - Artikel hinzufügen, bis der Mindestbestellwert erreicht ist → überprüfen, ob kostenlose Lieferung angezeigt wird
   - Schwere Artikel hinzufügen → überprüfen, ob die gewichtsbasierten Stufen funktionieren
   - Zonenbeschränkungen testen → überprüfen, ob Methoden für ausgeschlossene Zonen ausgeblendet werden

4. **Echtzeit-Methoden testen** (falls zutreffend)
   - Test-Anmeldeinformationen des Versanddienstes verwenden
   - Überprüfen, ob die Preise erfolgreich zurückgegeben werden
   - Prüfen, ob die Preise mit der Website des Versanddienstes übereinstimmen

---

## Problembehandlung

**Problem 1: Methode erscheint nicht beim Checkout**

**Ursachen**:
- Methode ist inaktiv
- Warenkorb erfüllt nicht den Mindest-/Höchstbestellwert
- Warenkorb erfüllt nicht das Mindest-/Höchstgewicht
- Kundenadresse stimmt nicht mit einer verknüpften Zone überein
- Keine Preistabelle-Stufen decken das Gewicht/Preis des Warenkorbs ab

**Lösung**: Einschränkungen prüfen, aktiven Status überprüfen, sicherstellen, dass Zonen/Stufen den Kundenfall abdecken.

---

**Problem 2: Echtzeit-Preise fehlschlagen**

**Ursachen**:
- Ungültige API-Anmeldeinformationen
- Konto des Anbieters ist inaktiv
- Keine Versandverpackungen definiert (der Anbieter benötigt Abmessungen)
- Ursprungsadresse nicht festgelegt
- API des Versanddienstes ist nicht erreichbar

**Lösung**: Verbindung zum Anbieter testen, Anmeldeinformationen überprüfen, sicherstellen, dass Verpackungen konfiguriert sind, Ursprungsadresse in den Einstellungen prüfen.

---

**Problem 3: Falscher Kostenbetrag berechnet**

**Ursachen**:
- Preistabelle-Stufen haben Lücken oder Überschneidungen
- Mindest-/Höchstwerte der Stufen sind in falschen Einheiten (Gramm vs. kg)
- Versandkosten werden unerwartet hinzugefügt
- Versandregel verändert den Kostenbetrag

**Lösung**: Preistabelle-Stufen überprüfen, Einheiten prüfen, Versandaktionen-Priorität überprüfen.

---

## Tipps

- **Einfach beginnen** - Verwenden Sie zuerst eine Flachrate für die erste Methode, fügen Sie Komplexität bei Bedarf hinzu
- **Gründlich testen** - Überprüfen Sie, ob alle Methoden im Testumfeld funktionieren, bevor Sie sie im Produktionsumfeld aktivieren
- **Beschreibende Namen verwenden** - "Standardversand (5-7 Tage)" ist besser als "Methode 1"
- **Realistische Lieferzeiten festlegen** - Unterversprechen und Übertreffen für Kundenzufriedenheit
- **Abholung anbieten, wenn möglich** - Reduziert Versandkosten und verbessert die Kundennachricht
- **Überwachen Sie die Zuverlässigkeit der Versand-API** - Verwenden Sie eine Flachrate als Ausweichlösung, wenn Echtzeit-Raten fehlschlagen
- **Zonen für internationale Lieferungen verwenden** - Unterschiedliche Preise nach Region verhindern Verluste an teuren Zielorten
- **Mit Versandaktionen kombinieren** - Regeln fügen bedingte Logik hinzu (kostenlose Versandaktionen, Gebühren für abgelegene Gebiete)
- **Methoden begrenzen** - 2-4 Optionen am Checkout verhindern Entscheidungsparalyse
- **Rate-Tabellen saisonal aktualisieren** - Versandkosten ändern sich, prüfen Sie jährlich
- **Priorität sinnvoll verwenden** - Kostenlose/ungeldige Optionen zuerst, teure Optionen zuletzt platzieren