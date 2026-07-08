---
title: Versandzonen
---

Versandzonen definieren geografische Regionen für gezielte Versandkosten – gruppieren Sie Länder, Bundesstaaten oder Postleitzahlen in Zonen und verknüpfen Sie Versandmethoden mit spezifischen Zonen, um eine präzise Kontrolle der Kosten zu ermöglichen. Zonen verwenden eine priorisierte Zuordnung, wenn Adressen mehreren Zonen entsprechen (die Zone mit der höchsten Priorität gewinnt). Dieses System ermöglicht komplexe Preisstrategien: Höhere Kosten für abgelegene Gebiete, kostenlose Versandkosten innerhalb des Landes oder reduzierte Preise für bestimmte Regionen.

Verwenden Sie Zonen, wenn Sie unterschiedliche Versandkosten für verschiedene geografische Gebiete benötigen, von einfachen Unterscheidungen zwischen national und international bis hin zu komplexen, mehrstufigen Preismodellen für mehrere Regionen.

## Verständnis von Versandzonen

**Was Zonen sind**: Benannte geografische Regionen, die durch Länder, Bundesstaaten/Bundesländer und Postleitzahlenmuster definiert werden.

**Wie Zonen funktionieren**:
1. Der Kunde gibt beim Checkout die Versandadresse ein
2. Das System bewertet alle aktiven Zonen
3. Zonen, die der Kundenadresse entsprechen, sind Kandidaten
4. Wenn mehrere Zonen übereinstimmen, gewinnt die Zone mit der höchsten Priorität
5. Versandmethoden, die mit der gewinnenden Zone verknüpft sind, werden angezeigt
6. Methoden, die nicht mit einer Zone verknüpft sind (oder mit einer übereinstimmenden Zone verknüpft sind), werden angezeigt

**Zonentypen**:
- **Name**: Zonenbezeichner (z. B. "Domestic", "EU", "Remote Areas")
- **Länder**: Liste der enthaltenen Ländercodes (leer = alle Länder)
- **Bundesstaaten/Bundesländer**: Landesspezifische Bundesstaatenbeschränkungen (optional)
- **Postleitzahlenmuster**: Regex-Muster für die Übereinstimmung der Postleitzahlen (optional)
- **Priorität**: Höherer Zahl = höhere Priorität, wenn mehrere Zonen übereinstimmen

---

## Logik der Zonenzuordnung

Zonen verwenden **progressive Verengung**, um Adressen zu übereinstimmen:

### Ebene 1: Länderübereinstimmung

**Leere Länderliste** → Zone stimmt mit **allen Ländern** überein

**Länderliste bereitgestellt** → Die Adresse-Länder muss in der Liste enthalten sein

Beispiel:
```
Zone: "Domestic"
Länder: ["US"]
→ Übereinstimmung: Jede US-Adresse
→ Keine Übereinstimmung: Kanada, UK, etc.
```

### Ebene 2: Bundesstaaten/Bundesländerübereinstimmung

**Keine Bundesstaaten definiert** → Zone stimmt mit **allen Bundesstaaten** in den erlaubten Ländern überein

**Bundesstaaten für bestimmte Länder definiert** → Die Adresse-Bundesstaat muss übereinstimmen

Beispiel:
```
Zone: "West Coast"
Länder: ["US"]
Bundesstaaten: {"US": ["CA", "OR", "WA"]}
→ Übereinstimmung: Kalifornien, Oregon, Washington-Adressen
→ Keine Übereinstimmung: New York, Texas, etc.
```

### Ebene 3: Postleitzahlenübereinstimmung

**Keine Muster definiert** → Zone stimmt mit **allen Postleitzahlen** in den erlaubten Ländern/Bundesstaaten überein

**Muster definiert** → Die Adresse-Postleitzahl muss mindestens einem Muster entsprechen

Beispiel:
```
Zone: "Los Angeles Metro"
Länder: ["US"]
Bundesstaaten: {"US": ["CA"]}
Postleitzahlenmuster: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Übereinstimmung: 90001, 91210, 90245
→ Keine Übereinstimmung: 94102 (San Francisco)
```

**Regex-Musterbeispiele**:
- `^90[0-9]{3}$` - Los Angeles Bereich (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Kanadisches Postleitzahlenformat (K1A 0B1)
- `^SW[0-9]{1,2}` - London UK-Postleitzahlen, die mit SW beginnen

---

## Zonenwahl basierend auf Priorität

Wenn mehrere Zonen einer Adresse entsprechen, bestimmt die **Priorität**, welche Zone gilt:

**Wie Priorität funktioniert**:
- Höherer Zahl = höhere Priorität
- Wenn die Adresse Zonen mit Priorität 100 und 50 übereinstimmt, gewinnt Priorität 100
- Nur die Versandmethoden der gewinnenden Zone sind verfügbar

**Anwendungsfälle**:

**Szenario 1: Spezifische Zone überschreibt allgemeine Zone**
```
Zone A: "Remote Alaska"
  Länder: ["US"]
  Bundesstaaten: {"US": ["AK"]}
  Priorität: 100

Zone B: "Domestic USA"
  Länder: ["US"]
  Priorität: 50

Adresse: Anchorage, AK
→ Übereinstimmung mit beiden Zonen
→ Priorität 100 gewinnt
→ "Remote Alaska"-Zone gilt (höhere Versandkosten)
```

**Szenario 2: Postleitzahl überschreibt Bundesstaat**
```
Zone A: "Manhattan Premium"
  Länder: ["US"]
  Bundesstaaten: {"US": ["NY"]}
  Postleitzahlenmuster: ["^100[0-2][0-9]$"]
  Priorität: 100

Zone B: "New York State"
  Länder: ["US"]
  Bundesstaaten: {"US": ["NY"]}
  Priorität: 50

Adresse: New York, NY 10001
→ Übereinstimmung mit beiden Zonen
→ Priorität 100 gewinnt
→ "Manhattan Premium" gilt (Premium-Versanddienst)
```

---

## Erstellen von Versandzonen

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigieren Sie zu Zonen**
   - Gehen Sie zu Einstellungen > Versand > Versandzonen
   - Klicken Sie auf "Versandzone hinzufügen"

2. **Grundkonfiguration**
   - **Name**: Beschreibender Bezeichner (z. B. "European Union", "West Coast", "Remote Areas")
   - **Priorität**: Setzen Sie die relative Wichtigkeit (100 für spezifisch, 50 für allgemein, 1 für Fallback)
   - **Aktiv**: Schalten Sie um, um zu aktivieren/deaktivieren

3. **Definition der geografischen Abdeckung**

   **Option A: Alle Länder** (Länderliste leer lassen)
   - Zone stimmt mit jeder Adresse weltweit überein
   - Verwenden Sie für Standard-/Fallback-Zonen

   **Option B: Spezifische Länder**
   - Klicken Sie auf "Land hinzufügen"
   - Wählen Sie Länder aus dem Dropdown (US, CA, UK, etc.)
   - Wiederholen Sie dies für alle enthaltenen Länder

   **Option C: Spezifische Bundesstaaten/Bundesländer**
   - Nachdem Sie Länder hinzugefügt haben, klicken Sie auf "Bundesstaaten hinzufügen" für jedes Land
   - Wählen Sie Bundesstaaten aus dem Dropdown
   - Beispiel: US → CA, OR, WA für West Coast

   **Option D: Postleitzahlenmuster** (erweitert)
   - Geben Sie Regex-Muster ein (ein pro Zeile)
   - Testen Sie Muster mit Beispiel-Postleitzahlen
   - Klicken Sie auf "Muster validieren", um die Syntax zu prüfen

4. **Verknüpfen mit Versandmethoden**
   - Methoden können während der Bearbeitung der Methode verknüpft werden (nicht in der Zonenkonfiguration)
   - Oder verknüpfen Sie Zonen mit vorhandenen Methoden: Methode bearbeiten → Versandzonen → Zonen auswählen

5. **Setzen Sie die Anzeigepriorität**
   - Höhere Prioritätszonen überschreiben niedrigere Prioritätszonen, wenn mehrere übereinstimmen
   - Empfohlen: Spezifische Zonen (100), Regionale Zonen (50), Standardzone (1)

6. **Aktivieren Sie die Zone**
   - Schalten Sie "Aktiv" = Ja
   - Speichern Sie

---

## Typische Zoneneinstellungen

### Einstellung 1: National vs. International

**Ziel**: Unterschiedliche Preise für national vs. alle anderen Länder.

```
Zone 1: "Domestic"
  Länder: [Ihr Ländercode]
  Priorität: 50

Zone 2: "International"
  Länder: [Leer lassen oder alle anderen Länder auswählen]
  Priorität: 1
```

**Versandmethoden**:
- "Domestic Standard" → Verknüpft mit der Domestic-Zone
- "International Shipping" → Verknüpft mit der International-Zone

---

### Einstellung 2: Mehrregionales Internationales

**Ziel**: Unterschiedliche Preise für EU, Nordamerika, Asien, Rest der Welt.

```
Zone 1: "European Union"
  Länder: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priorität: 100

Zone 2: "North America"
  Länder: [US, CA, MX]
  Priorität: 100

Zone 3: "Asia Pacific"
  Länder: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priorität: 100

Zone 4: "Rest of World"
  Länder: [Leer lassen]
  Priorität: 1
```

**Versandmethoden**:
- "EU Shipping" → EU-Zone
- "North America Shipping" → North America-Zone
- "Asia Pacific Shipping" → Asia Pacific-Zone
- "International Standard" → Rest of World-Zone

---

### Einstellung 3: Abgaben für abgelegene Gebiete

**Ziel**: Abgaben für abgelegene Postleitzahlen innerhalb der nationalen Zone.

```
Zone 1: "Remote Domestic"
  Länder: [US]
  Postleitzahlenmuster: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priorität: 100

Zone 2: "Standard Domestic"
  Länder: [US]
  Priorität: 50
```

**Versandmethoden**:
- "Remote Shipping" → Remote Domestic-Zone (höhere Kosten)
- "Standard Shipping" → Standard Domestic-Zone

---

### Einstellung 4: Bundesstaat-spezifische Zonen

**Ziel**: Unterschiedliche Preise für jede Region der USA.

```
Zone 1: "West Coast"
  Länder: [US]
  Bundesstaaten: {"US": ["CA", "OR", "WA"]}
  Priorität: 100

Zone 2: "East Coast"
  Länder: [US]
  Bundesstaaten: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Priorität: 100

Zone 3: "Midwest"
  Länder: [US]
  Bundesstaaten: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Priorität: 100

Zone 4: "South"
  Länder: [US]
  Bundesstaaten: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Priorität: 100

Zone 5: "Other US States"
  Länder: [US]
  Priorität: 50
```

---

## Beispiele für Postleitzahlenmuster

Postleitzahlen verwenden **Regex** (reguläre Ausdrücke) für Musterübereinstimmung:

### Vereinigte Staaten (ZIP-Codes)

**Format**: 5 Ziffern (z. B. 90210)

```
Kalifornien (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Kanada (Postleitzahlen)

**Format**: A1A 1A1 (Buchstabe-Ziffer-Buchstabe Leerzeichen Ziffer-Buchstabe-Ziffer)

```
Alle kanadischen Postleitzahlen:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$ 
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$ 
Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$ 
```

### Vereinigtes Königreich (Postcodes)

**Format**: AA1A 1AA oder A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Australien (Postleitzahlen)

**Format**: 4 Ziffern (z. B. 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Muster-Testen

**Bevor Sie Muster speichern**, testen Sie sie mit bekannten Postleitzahlen:

1. Geben Sie das Muster ein: `^90[0-9]{3}$`
2. Testeingabe: "90210" → Sollte übereinstimmen
3. Testeingabe: "10001" → Sollte **nicht** übereinstimmen
4. Testeingabe: "9021" → Sollte **nicht** übereinstimmen (nur 4 Ziffern)

Verwenden Sie Online-Regex-Tester (regex101.com), um komplexe Muster zu validieren.

---

## Zusammenfassung der Zonenabdeckung

Zonen zeigen eine **Zusammenfassung der Abdeckung** in der Verwaltungsansicht an, die anzeigt, was enthalten ist:

**Beispiele**:
- "All countries" → Keine Länderbeschränkungen
- "US, CA, MX" → 3 Länder
- "US (CA, OR, WA)" → US mit 3 Bundesstaaten
- "US (90xxx-91xxx)" → US mit Postleitzahlenmustern

**Zusammenfassung verwenden, um**:
- Schnell die Zonenabdeckung zu überprüfen, ohne sie zu öffnen
- Überschneidungen oder Lücken in der Abdeckung erkennen
- Die Zonenkonfiguration im Überblick prüfen

---

## Verknüpfen von Zonen mit Versandmethoden

Zonen und Methoden haben eine **Viele-zu-Viele-Beziehung**:

**Von der Methode aus** (Empfohlen):
1. Bearbeiten Sie die Versandmethode
2. Scrollen Sie zu Abschnitt "Versandzonen"
3. Wählen Sie die anwendbaren Zonen (Multi-Auswahl)
4. Speichern Sie die Methode

**Von der Zone aus**:
- Zonen verknüpfen sich nicht direkt mit Methoden
- Die Verknüpfung erfolgt immer von der Methode-Konfiguration aus

**Verhalten von Methode-Zone**:

**Keine Zonen verknüpft** → Methode ist für **alle Adressen** verfügbar

**Zonen verknüpft** → Methode ist nur verfügbar, wenn die Kundenadresse mindestens einer verknüpften Zone entspricht

**Beispiel**:
```
Methode: "Domestic Standard"
Verknüpfte Zonen: ["Domestic USA"]
→ Nur für US-Adressen sichtbar

Methode: "International Express"
Verknüpfte Zonen: ["EU", "Asia Pacific", "Rest of World"]
→ Für alle nicht-US-Adressen sichtbar
```

---

## Testen der Zonenübereinstimmung

Bevor Sie online gehen, testen Sie die Zonenkonfiguration:

1. **Erstellen Sie Testbestellungen**
   - Verwenden Sie Adressen in verschiedenen Zonen
   - Überprüfen Sie, ob die korrekten Zonen übereinstimmen

2. **Überprüfen Sie die Prioritätsauflösung**
   - Verwenden Sie eine Adresse, die mehreren Zonen entspricht
   - Überprüfen Sie, ob die Zone mit der höchsten Priorität gewinnt
   - Bestätigen Sie, dass die erwarteten Versandmethoden angezeigt werden

3. **Testen Sie Randfälle**
   - Grenzpostleitzahlen (z. B. 90999 vs. 91000)
   - Bundesstaatsgrenzen
   - Internationale Adressen mit ähnlichen Postleitzahlen

4. **Verwenden Sie das Zonenvorschau-Tool** (wenn vorhanden)
   - Geben Sie eine Testadresse ein
   - Sehen Sie, welche Zonen übereinstimmen
   - Sehen Sie die Prioritätsauflösung

---

## Problembehandlung

**Problem 1: Keine Versandmethoden am Checkout verfügbar**

**Ursachen**:
- Kundenadresse stimmt mit keiner Zone überein
- Alle Methoden sind mit Zonen verknüpft, die nicht übereinstimmen
- Es gibt keine Methoden ohne Zonenbeschränkungen

**Lösung**:
- Erstellen Sie eine Fallback-Zone (alle Länder, Priorität 1)
- ODER entfernen Sie Zonenbeschränkungen von mindestens einer Methode
- Überprüfen Sie die Länder-/Bundesstaaten-/Postleitzahlenmuster der Zonen

---

**Problem 2: Falsche Zonenübereinstimmung**

**Ursachen**:
- Eine Zone mit niedriger Priorität wird ausgewählt, obwohl eine Zone mit höherer Priorität übereinstimmt
- Syntaxfehler im Postleitzahlenmuster (das Muster schlägt stumm)
- Bundesstaaten-Code-Mismatch (CA vs. California)

**Lösung**:
- Überprüfen Sie Prioritätswerte (höherer Zahl = höhere Priorität)
- Testen Sie Postleitzahlenmuster mit Regex-Validator
- Verwenden Sie 2-Buchstaben-Bundesstaaten-Codes (CA, nicht California)

---

**Problem 3: Unerwartete Methode angezeigt**

**Ursachen**:
- Methode hat keine Zonen verknüpft (verfügbar überall)
- Mehrere Zonen stimmen überein, und eine unerwartete Zone hat höhere Priorität
- Zonenabdeckung überschneidet sich unbeabsichtigt

**Lösung**:
- Überprüfen Sie die verknüpften Zonen der Methode
- Prüfen Sie die Priorität der übereinstimmenden Zonen
- Prüfen Sie die Zusammenfassung der Zonenabdeckung auf Überschneidungen

---

## Tipps

- **Beginnen Sie mit 2 Zonen** – Domestic und International, erweitern Sie bei Bedarf
- **Verwenden Sie Prioritäten sorgfältig** – Spezifische Zonen 100, regionale 50, Fallback 1
- **Testen Sie Postleitzahlenmuster gründlich** – Regex-Fehler schlagen stumm, was dazu führt, dass Zonen nicht übereinstimmen
- **Dokumentieren Sie die Logik der Zonen** – Fügen Sie Notizen zur Zonenbeschreibung hinzu, um den Abdeckungsabsicht zu erklären
- **Vermeiden Sie zu viele Zonen** – Zu viele Zonen komplizieren die Konfiguration; verwenden Sie Versandregeln für komplexe Szenarien
- **Verwenden Sie Bundesstaaten-Codes, nicht Namen** – "CA" nicht "California", "NY" nicht "New York"
- **Erstellen Sie eine Fallback-Zone** – Alle Länder, Priorität 1, stellt sicher, dass immer mindestens eine Versandoption verfügbar ist
- **Überwachen Sie die Leistung der Zonen** – Wenn viele Kunden "kein Versand verfügbar" sehen, prüfen Sie die Zonenabdeckung
- **Aktualisieren Sie Zonen für neue Regionen** – Fügen Sie Länder zur EU-Zone hinzu, wenn neue Mitglieder beitreten
- **Verwenden Sie beschreibende Namen** – "EU (Excluding UK)" ist besser als "Zone 3"
- **Testen Sie mit echten Adressen** – Verwenden Sie echte Kundenadressen während des Tests, nicht erfundene
