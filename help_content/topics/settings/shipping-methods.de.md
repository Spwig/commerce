---
title: Versandmethoden
---

Versandmethoden sind die für Kunden sichtbaren Lieferoptionen, die am Checkout angezeigt werden – jede Methode berechnet die Versandkosten mit unterschiedlichen Preisstrategien. Spwig unterstützt 7 Methodentypen, die von einfachen Flachraten bis hin zu komplexen, von Transportunternehmen berechneten Echtzeitpreisen reichen. Methoden können anhand von Mindest-/Höchstbestellwert, Gewicht und geografischen Zonen eingeschränkt werden. Kunden wählen ihre bevorzugte Methode am Checkout aus, und die berechneten Kosten werden ihrem Bestellgesamtbetrag hinzugefügt.

Verwenden Sie diese Anleitung, um Versandmethoden zu konfigurieren, die Ihrem Geschäftsmodell entsprechen, von einfachen Flachratenversand bis hin zu komplexen, zonenbasierten Stufenpreisen.

## Typen von Versandmethoden

Spwig bietet 7 Typen von Versandmethoden an, jede mit unterschiedlicher Kostenberechnungslogik:

### Flachratenversand

**Was es ist**: Fixer Preis, unabhängig vom Inhalt des Warenkorbs, Zielort oder Gewicht.

**Wann verwenden**: 
- Einfache Geschäfte mit vorhersehbaren Versandkosten
- Ein Produkttyp (ähnliche Größe/Gewicht)
- Nur nationale Versandoptionen mit Standard-Transportunternehmen-Preisen
- Freiversand-Aktionen (verwenden Sie dies mit Versandregeln)

**Konfiguration**: 
- Setzen Sie **Methodentyp** = Flachraten
- Geben Sie den **Fixen Preis** ein (z. B. 9,99 $)
- Optional: Setzen Sie Mindest-/Höchstbestellwert-Einschränkungen

**Beispiel**: "Standardversand - 9,99 $" für alle nationalen Bestellungen.

---

### Freiversand

**Was es ist**: Versandoption mit Null Kosten (keine Gebühren für den Kunden).

**Wann verwenden**: 
- Freiverschiffsaktionen
- Hochwertige Bestellungen (kombinieren Sie dies mit Mindestbestellwert)
- Alternative zum lokalen Abholen
- Vorteile für Loyalitätsprogramme

**Konfiguration**: 
- Setzen Sie **Methodentyp** = Freiversand
- Optional: Setzen Sie **Mindestbestellwert** (z. B. Freiversand ab 50 $)
- Funktioniert gut mit Versandregeln für bedingten Freiversand

**Beispiel**: "Freiversand ab Bestellwert von 50 $" mit min_order_value = 50 $.

---

### Gewichtsbasiert

**Was es ist**: Kosten werden anhand einer Stufenpreistabelle basierend auf dem Gesamtgewicht des Warenkorbs berechnet.

**Wann verwenden**: 
- Produkte mit variierenden Gewichten (Bücher, Hardware, Lebensmittel)
- Gewichtsbasierte Preismodelle von Transportunternehmen
- Vorhersehbare Gewichts-Kosten-Verhältnisse

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Gewichtsbasiert
2. Erstellen Sie eine **Versandpreistabelle** mit basis_type = "gewicht"
3. Fügen Sie **Versandpreistufen** hinzu (z. B. 0-5kg = 10 $, 5-10kg = 15 $, 10-20kg = 25 $)
4. Optional: Einschränkung auf bestimmte Zonen

**Beispiel**: 
```
0-2kg: 8 $
2-5kg: 12 $
5-10kg: 18 $
10kg+: 25 $
```

**Funktionsweise**: Der Warenkorb berechnet das Gesamtgewicht → findet die passende Stufe → gibt die Stufenrate zurück.

---

### Preisbasiert

**Was es ist**: Kosten werden anhand einer Stufenpreistabelle basierend auf dem Warenkorb-Subtotal berechnet.

**Wann verwenden**: 
- Versandkosten korrelieren mit dem Bestellwert
- Höherer Warenkorbwert fördern (niedrigerer Preis pro Dollar bei höheren Stufen)
- Einfache Alternative zum gewichtsbasierten für ähnliche Preise

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Preisbasiert
2. Erstellen Sie eine **Versandpreistabelle** mit basis_type = "preis"
3. Fügen Sie **Versandpreistufen** hinzu (z. B. 0-50 $ = 9,99 $, 50-100 $ = 14,99 $, 100+ = 19,99 $)

**Beispiel**: 
```
0-25 $: 6,99 $
25-75 $: 9,99 $
75-150 $: 12,99 $
150+: Frei
```

**Funktionsweise**: Der Warenkorb berechnet den Subtotal → findet die passende Stufe → gibt die Stufenrate zurück.

---

### Echtzeit-Transportunternehmen-Preise

**Was es ist**: Live-Raten, die von Transportunternehmen-APIs (FedEx, UPS, DHL) am Checkout abgerufen werden.

**Wann verwenden**: 
- Variable Versandkosten je nach Zielort
- Mehrere Transportunternehmensoptionen für Kunden
- Genauere Transportunternehmen-Preise ohne manuelle Raten-Tabellen
- Internationale Versandoptionen mit komplexen Preisen

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Echtzeit
2. Erstellen Sie ein **Provider-Konto** (Einstellungen > Versand > Provider-Konten)
3. Geben Sie die Transportunternehmen-API-Anmeldeinformationen ein (Kontonummer, API-Schlüssel, Geheimnis)
4. Verknüpfen Sie das Provider-Konto mit der Versandmethode
5. Optional: Fügen Sie eine Mark-up-Prozent oder einen Fix-Preis hinzu

**Voraussetzungen**: 
- Aktives Provider-Konto (FedEx, UPS, DHL, usw.)
- API-Anmeldeinformationen vom Provider
- Definierte Versandverpackungen (für die Berechnung des dimensionalen Gewichts)

**Beispiel**: Die Methode "FedEx Ground" ruft Live-FedEx-Raten basierend auf Warenkorb-Gewicht, Abmessungen und Zielort am Checkout ab.

**Funktionsweise**: 
1. Der Kunde gibt die Adresse am Checkout ein
2. Das System ruft die Transportunternehmen-API mit Ursprungs- und Zielort, Verpackungsabmessungen und Gewicht ab
3. Der Transportunternehmen gibt den Preis zurück
4. Optional wird eine Mark-up angewendet
5. Der Preis wird dem Kunden angezeigt

---

### Lokales Abholen

**Was es ist**: Der Kunde holt die Bestellung an einem physischen Standort ab (keine Lieferkosten).

**Wann verwenden**: 
- Einzelhandelsgeschäfte, die Abholung anbieten
- Lagerhaus-Abholoptionen
- Veranstaltungen oder Marktstände
- Eliminieren Sie Versandkosten für lokale Kunden

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Lokales Abholen
2. Erstellen Sie eine **Standort** (Einstellungen > Versand > Standorte)
   - Geben Sie die Adresse, Betriebszeiten und Abholkapazität ein
3. Verknüpfen Sie Standort(e) mit der Methode
4. Optional: Setzen Sie die Abholvorbereitungszeit (z. B. "Bereit in 2 Stunden")

**Kundenerlebnis**: 
- Wählt "Lokales Abholen" am Checkout aus
- Wählt den Abholort aus (wenn mehrere vorhanden)
- Wählt den Abholtermin basierend auf der Verfügbarkeit
- Erhält eine Benachrichtigung, wenn die Bestellung bereit ist

**Beispiel**: "Abholen im Geschäft - Kostenlos" mit 3 Einzelhandelsstandorten, bereit innerhalb von 24 Stunden.

---

### Tabellebasiert

**Was es ist**: Flexibler Stufenpreis basierend auf Gewicht, Preis oder Menge mit erweiterten Zonen-Zielsetzungen.

**Wann verwenden**: 
- Komplexe Preise (unterschiedliche Raten je nach Zone und Gewicht)
- Mehr Kontrolle als bei Gewichts- oder Preisbasiert allein
- Mehrere Preisfaktoren (z. B. Gewicht + Zielort + Menge)

**Konfiguration**: 
1. Setzen Sie **Methodentyp** = Tabellebasiert
2. Erstellen Sie eine **Versandpreistabelle**
3. Definieren Sie **basis_type**: Gewicht, Preis oder Menge
4. Fügen Sie **Versandpreistufen** mit Min-/Max-Werten hinzu
5. Optional: Einschränkung der Stufen auf bestimmte Zonen oder Länder

**Unterschied zu Gewicht/Preisbasiert**: Tabellebasiert unterstützt geografische Einschränkungen pro Stufe, was unterschiedliche Raten für dasselbe Gewicht/Preis in verschiedenen Zonen ermöglicht.

**Beispiel**: 
```
Zone A (Domestisch):
  0-5kg: 10 $
  5-10kg: 15 $

Zone B (Entfernt):
  0-5kg: 18 $
  5-10kg: 25 $
```

**Funktionsweise**: Der Warenkorb berechnet den Basiswert (Gewicht/Preis/Menge) → findet die passende Stufe für den Kunden-Zone → gibt die Stufenrate zurück.

---

## Konfiguration von Versandmethoden

Alle Versandmethoden teilen sich diese allgemeinen Einstellungen:

### Grundlegende Einstellungen

- **Name**: Interner Bezeichner (nicht für Kunden sichtbar)
- **Anzeigename**: Für Kunden sichtbarer Name am Checkout (z. B. "Standardversand", "Expresslieferung")
- **Beschreibung**: Optionaler Hilfetext, der am Checkout angezeigt wird (z. B. "Lieferung in 3-5 Werktagen")
- **Methodentyp**: Einer der 7 Typen oben
- **Aktiv**: Schalter zum Aktivieren/Deaktivieren der Methode ohne Löschen

### Kosten-Einstellungen

- **Fixer Preis**: Nur für Flachratenmethoden
- **Preistabelle**: Für gewichtsbasierte, preisbasierte, tabellebasierte Methoden
- **Provider-Konto**: Für Echtzeit-Transportunternehmen-Methoden
- **Steuerklasse**: Steuer auf Versandkosten anwenden (wenn zutreffend)

### Einschränkungen

**Bestellwert-Einschränkungen**: 
- **Mindestbestellwert**: Methode nur verfügbar, wenn Warenkorb-Subtotal ≥ Betrag (z. B. Freiversand ab 50 $)
- **Höchstbestellwert**: Methode verborgen, wenn Warenkorb-Subtotal > Betrag (z. B. Flachraten nur für Bestellungen unter 100 $)

**Gewichtseinschränkungen**: 
- **Mindestgewicht**: Methode nur verfügbar, wenn Warenkorb-Gewicht ≥ Betrag
- **Höchstgewicht**: Methode verborgen, wenn Warenkorb-Gewicht > Betrag (häufig bei leichten Versandoptionen)

**Geografische Einschränkungen**: 
- **Versandzonen**: Verknüpfen Sie die Methode mit bestimmten Zonen (national, international, regional)
- Leere Zonen = für alle Adressen verfügbar
- Mehrere Zonen = für jede passende Zone verfügbar

### Erweiterte Einstellungen

- **Priorität**: Anzeige-Reihenfolge am Checkout (niedrigere Zahl = höher in der Liste)
- **Bearbeitungsgebühr**: Zusätzliche Flachgebühr, die zur berechneten Kosten hinzugefügt wird
- **Freiversand-Schwellenwert**: Setzt den Kosten automatisch auf 0 $, wenn Warenkorb-Subtotal ≥ Schwellenwert (Alternative zu min_order_value)

---

## Erstellen einer Versandmethode

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigieren Sie zu Versandmethoden**
   - Gehen Sie zu Einstellungen > Warenkorb > Versandmethoden
   - Klicken Sie auf "Versandmethode hinzufügen"

2. **Wählen Sie Methodentyp**
   - Wählen Sie den passenden Typ basierend auf Ihrer Preisstrategie
   - Der Typ bestimmt die verfügbaren Kostenkonfigurationsfelder

3. **Konfigurieren Sie Grundinformationen**
   - Name: Interner Bezug (z. B. "domestic_ground")
   - Anzeigename: Für Kunden sichtbar (z. B. "Groundversand")
   - Beschreibung: Lieferzeitraum (z. B. "5-7 Werktagen")

4. **Setzen Sie die Kostenberechnung**
   - **Flachraten**: Geben Sie den Fixpreis ein
   - **Gewicht/Preis/Tabellebasiert**: Erstellen Sie eine Preistabelle (siehe unten)
   - **Echtzeit**: Verknüpfen Sie das Provider-Konto
   - **Frei/Abholen**: Keine Kostenkonfiguration erforderlich

5. **Fügen Sie Einschränkungen hinzu (optional)**
   - Mindest-/Höchstbestellwert
   - Mindest-/Höchstgewicht
   - Versandzonen

6. **Setzen Sie die Priorität**
   - Niedrigere Zahlen werden zuerst am Checkout angezeigt
   - Empfohlene Reihenfolge: Frei (1), Lokales Abholen (2), Standard (3), Express (4)

7. **Aktivieren Sie die Methode**
   - Schalten Sie "Aktiv" = Ja
   - Speichern

---

## Erstellen von Preistabellen

Für gewichtsbasierte, preisbasierte und tabellebasierte Methoden:

**Schritt 1: Erstellen Sie eine Preistabelle**
- Gehen Sie zu Einstellungen > Versand > Preistabellen
- Klicken Sie auf "Preistabelle hinzufügen"
- Setzen Sie **Name** (z. B. "Domestische Gewichtsstufen")
- Setzen Sie **Basis-Typ**: Gewicht, Preis oder Menge

**Schritt 2: Fügen Sie Stufen hinzu**
- Klicken Sie auf "Stufe hinzufügen"
- Setzen Sie **Mindestwert** und **Höchstwert** (Bereich für Übereinstimmung)
- Setzen Sie **Rate** (Kosten für diese Stufe)
- Optional: Einschränkung auf bestimmte Zonen oder Länder
- Speichern Sie die Stufe

**Schritt 3: Wiederholen Sie für alle Stufen**
- Decken Sie den gesamten Bereich ab (0 bis maximaler erwarteter Wert)
- Stellen Sie sicher, dass keine Lücken vorhanden sind (z. B. 0-5, 5-10, 10-20, 20+)
- Verwenden Sie `null` für den Höchstwert in der letzten Stufe (unbegrenzt)

**Schritt 4: Verknüpfen Sie mit der Versandmethode**
- Bearbeiten Sie die Versandmethode
- Wählen Sie die Preistabelle aus dem Dropdown aus
- Speichern

**Beispiel einer gewichtsbasierten Tabelle**: 
```
Name: Domestische Gewichtsstufen
Basis: Gewicht

Stufen:
1. Min: 0g, Max: 2000g, Rate: 8 $
2. Min: 2000g, Max: 5000g, Rate: 12 $
3. Min: 5000g, Max: 10000g, Rate: 18 $
4. Min: 10000g, Max: null, Rate: 25 $
```

---

## Typische Versand-Szenarien

### Szenario 1: Grundlegender nationaler Versand

**Ziel**: Einfacher Flachraten von 9,99 $ für alle nationalen Bestellungen.

**Lösung**: 
- Methodentyp: Flachraten
- Fixer Preis: 9,99 $
- Versandzone: "Domestisch" (nur Ihr Land)

---

### Szenario 2: Freiversand ab 50 $ Bestellwert

**Ziel**: Höheren Warenkorbwert mit Freiverschiffs-Schwellenwert fördern.

**Lösungsoption A** (Empfohlen): 
- Methodentyp: Freiversand
- Mindestbestellwert: 50 $
- Anzeigename: "Freiversand (Bestellungen ab 50 $)"

**Lösungsoption B** (Mit Regeln): 
- Methodentyp: Flachraten
- Fixer Preis: 9,99 $
- Erstellen Sie eine Versandregel:
  - Bedingung: Warenkorbwert ≥ 50 $
  - Aktion: Kosten auf 0 $ setzen

---

### Szenario 3: Gewichtsbasiert national + international

**Ziel**: Unterschiedliche Raten für national und international basierend auf Gewicht.

**Lösung**: 
1. Erstellen Sie 2 Zonen: "Domestisch", "International"
2. Erstellen Sie 2 Preistabellen: "Domestische Gewicht", "Internationale Gewicht"
3. Erstellen Sie 2 Methoden:
   - "Domestischer Versand" → verknüpft mit der Domestischen Zone + Domestische Gewicht-Tabelle
   - "Internationaler Versand" → verknüpft mit der Internationalen Zone + Internationale Gewicht-Tabelle

---

### Szenario 4: Mehrere Transportunternehmensoptionen

**Ziel**: Kunden können zwischen FedEx Ground, FedEx Express, UPS Ground wählen.

**Lösung**: 
1. Erstellen Sie ein Provider-Konto für die FedEx-API
2. Erstellen Sie ein Provider-Konto für die UPS-API
3. Erstellen Sie 3 Echtzeitmethoden:
   - "FedEx Ground" → FedEx-Provider, Service-Code = "FEDEX_GROUND"
   - "FedEx Express" → FedEx-Provider, Service-Code = "FEDEX_EXPRESS"
   - "UPS Ground" → UPS-Provider, Service-Code = "UPS_GROUND"
4. Alle 3 Methoden fragen die Transportunternehmen-API am Checkout ab und zeigen Live-Raten an

---

### Szenario 5: Lokales Abholen + Lieferung

**Ziel**: Einzelhandelsgeschäft bietet sowohl Abholen als auch Lieferoptionen an.

**Lösung**: 
1. Erstellen Sie Standort: "Hauptgeschäft" mit Adresse, Stunden und Vorbereitungszeit
2. Erstellen Sie 2 Methoden:
   - "Lokales Abholen" → Lokales Abholen-Typ, verknüpft mit Hauptgeschäft-Position
   - "Standardlieferung" → Flachraten 9,99 $
3. Kunden sehen beide Optionen am Checkout

---

## Testen von Versandmethoden

Bevor Sie online gehen, testen Sie alle Methoden:

1. **Erstellen Sie einen Test-Warenkorb**
   - Fügen Sie Produkte mit unterschiedlichen Gewichten/Preisen hinzu
   - Gehen Sie zum Checkout

2. **Testen Sie jede Methode**
   - Geben Sie Adressen in verschiedenen Zonen ein
   - Stellen Sie sicher, dass die richtigen Methoden angezeigt werden
   - Prüfen Sie, ob die berechneten Kosten den Erwartungen entsprechen

3. **Testen Sie Einschränkungen**
   - Fügen Sie Artikel hinzu, bis der Mindestbestellwert erreicht ist → prüfen Sie, ob Freiversand angezeigt wird
   - Fügen Sie schwere Artikel hinzu → prüfen Sie, ob die gewichtsbasierten Stufen funktionieren
   - Testen Sie Zonen-Einschränkungen → prüfen Sie, ob Methoden für ausgeschlossene Zonen verborgen sind

4. **Testen Sie Echtzeitmethoden** (wenn zutreffend)
   - Verwenden Sie Test-Anmeldeinformationen des Providers
   - Prüfen Sie, ob die Raten erfolgreich zurückgegeben werden
   - Prüfen Sie die Genauigkeit der Raten im Vergleich zur Website des Transportunternehmens

---

## Problembehandlung

**Problem 1: Methode wird am Checkout nicht angezeigt**

**Ursachen**: 
- Methode ist inaktiv
- Warenkorb erfüllt nicht Mindest-/Höchstbestellwert
- Warenkorb erfüllt nicht Mindest-/Höchstgewicht
- Kundenadresse entspricht keiner verknüpften Zone
- Keine Preistabelle-Stufen decken Warenkorb-Gewicht/Preis ab

**Lösung**: Prüfen Sie Einschränkungen, prüfen Sie den Aktivstatus, stellen Sie sicher, dass Zonen/Stufen den Kundenfall abdecken.

---

**Problem 2: Echtzeit-Raten fehlschlagen**

**Ursachen**: 
- Ungültige API-Anmeldeinformationen
- Inaktives Provider-Konto
- Keine definierten Versandverpackungen (Transportunternehmen benötigt Abmessungen)
- Ursprungsadresse nicht festgelegt
- Transportunternehmen-API ist nicht verfügbar

**Lösung**: Testen Sie die Verbindung zum Provider, prüfen Sie die Anmeldeinformationen, stellen Sie sicher, dass Verpackungen konfiguriert sind, prüfen Sie die Ursprungsadresse in den Einstellungen.

---

**Problem 3: Falsch berechnete Kosten**

**Ursachen**: 
- Preistabelle-Stufen haben Lücken oder Überschneidungen
- Min-/Max-Werte der Stufen sind in falschen Einheiten (Gramm vs. kg)
- Bearbeitungsgebühr wurde unerwartet hinzugefügt
- Versandregel verändert die Kosten

**Lösung**: Prüfen Sie die Preistabelle-Stufen, prüfen Sie die Einheiten, prüfen Sie die Priorität der Versandregeln.

---

## Tipps

- **Beginnen Sie einfach** - Verwenden Sie Flachraten für die erste Methode, fügen Sie Komplexität bei Bedarf hinzu
- **Testen Sie gründlich** - Stellen Sie sicher, dass alle Methoden in der Testumgebung funktionieren, bevor Sie sie in der Produktion aktivieren
- **Verwenden Sie beschreibende Namen** - "Standardversand (5-7 Tage)" ist besser als "Methode 1"
- **Setzen Sie realistische Lieferzeiten** - Unter-Promisen, über-Liefern für Kundenzufriedenheit
- **Bieten Sie Abholung an, wenn möglich** - Reduziert Versandkosten, verbessert Kundennutzbarkeit
- **Überwachen Sie die Zuverlässigkeit der Transportunternehmen-API** - Haben Sie eine Flachraten-Alternative, wenn Echtzeit-Raten fehlschlagen
- **Verwenden Sie Zonen für internationale Lieferungen** - Unterschiedliche Raten je nach Region verhindern Verluste an teuren Zielorten
- **Kombinieren Sie mit Versandregeln** - Regeln fügen bedingte Logik hinzu (Freiverschiffsaktionen, Zuschläge für abgelegene Gebiete)
- **Begrenzen Sie die Methoden** - 2-4 Optionen am Checkout verhindern Entscheidungsparalyse
- **Aktualisieren Sie die Preistabellen saisonal** - Transportunternehmen-Raten ändern sich, prüfen Sie jährlich
- **Verwenden Sie Priorität sinnvoll** - Setzen Sie kostenlose/teurere Optionen zuerst, teure Optionen zuletzt

