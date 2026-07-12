---
title: Versandzonen
---

Versandzonen definieren geografische Regionen für gezielte Versandkosten – gruppiere Länder, Bundesstaaten oder Postleitzahlen in Zonen und verbinde Versandmethoden mit spezifischen Zonen, um präzise Kostenkontrolle zu ermöglichen. Zonen verwenden priorisierte Zuordnung, wenn Adressen für mehrere Zonen qualifiziert sind (höchste Priorität gewinnt). Dieses System ermöglicht fortgeschrittene Preisstrategien: Höhere Kosten für abgelegene Gebiete, kostenlose Lieferung im Inland oder reduzierte Preise für bestimmte Regionen.

Verwende Zonen, wenn du unterschiedliche Versandkosten für verschiedene geografische Gebiete benötigst, von einfachen Inlands- vs. Internationalen Aufteilungen bis hin zu komplexen mehrstufigen Preisstrukturen für mehrere Regionen.

## Verständnis von Versandzonen

**Was Zonen sind**: Benannte geografische Regionen, die durch Länder, Bundesstaaten/Provinzen und Postleitzahlpattern definiert werden.

**Wie Zonen funktionieren**:
1. Der Kunde gibt bei der Kasse die Versandadresse ein
2. Das System bewertet alle aktiven Zonen
3. Zonen, die der Kundenadresse entsprechen, sind Kandidaten
4. Wenn mehrere Zonen übereinstimmen, gewinnt die Zone mit der höchsten Priorität
5. Versandmethoden, die mit der gewinnenden Zone verknüpft sind, werden angezeigt
6. Methoden, die mit keiner Zone verknüpft sind (oder mit einer übereinstimmenden Zone) werden angezeigt

**Zonentypen**:
- **Name**: Zonenbezeichner (z. B. "Domestic", "EU", "Remote Areas")
- **Länder**: Liste der enthaltenen Ländercodes (leer = alle Länder)
- **Bundesstaaten/Provinzen**: Land-spezifische Bundesstaatsbeschränkungen (optional)
- **Postleitzahlpattern**: Regex-Patterns für die Übereinstimmung mit Postleitzahlen (optional)
- **Priorität**: Höherer Zahl = höhere Priorität, wenn mehrere Zonen übereinstimmen

---

## Logik der Zonenzuordnung

Zonen verwenden **progressive Verengung**, um Adressen zu übereinstimmen:

### Ebene 1: Länderübereinstimmung

**Leere Länderliste** → Zone passt zu allen Ländern

**Länderliste bereitgestellt** → Land der Adresse muss in der Liste enthalten sein

Beispiel:
```
Zone: "Domestic"
Länder: ["US"]
→ Übereinstimmung: Jede US-Adresse
→ Keine Übereinstimmung: Kanada, UK, etc.
```

### Ebene 2: Bundesstaat/Provinz-Übereinstimmung

**Keine Bundesstaaten definiert** → Zone passt zu allen Bundesstaaten in den erlaubten Ländern

**Bundesstaaten für bestimmte Länder definiert** → Bundesstaat der Adresse muss übereinstimmen

Beispiel:
```
Zone: "West Coast"
Länder: ["US"]
Bundesstaaten: {"US": ["CA", "OR", "WA"]}
→ Übereinstimmung: Adressen aus Kalifornien, Oregon und Washington
→ Keine Übereinstimmung: New York, Texas, etc.
```

### Ebene 3: Postleitzahlaufbereinstimmung

**Keine Pattern definiert** → Zone passt zu allen Postleitzahlen in den erlaubten Ländern/Bundesstaaten

**Pattern definiert** → Postleitzahl der Adresse muss mindestens einem Pattern entsprechen

Beispiel:
```
Zone: "Los Angeles Metro"
Länder: ["US"]
Bundesstaaten: {"US": ["CA"]}
Postleitzahlpattern: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Übereinstimmung: 90001, 91210, 90245
→ Keine Übereinstimmung: 94102 (San Francisco)
```

**Regex-Pattern-Beispiele**:
- `^90[0-9]{3}$` - Los Angeles Bereich (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Kanadische Postleitzahlförder (K1A 0B1)
- `^SW[0-9]{1,2}` - London UK Postleitzahlen, die mit SW beginnen

---

## Prioritätsbasierte Zonenauswahl

Wenn mehrere Zonen einer Adresse entsprechen, bestimmt die **Priorität**, welche Zone gilt:

**Wie Priorität funktioniert**:
- Höherer Zahl = höhere Priorität
- Wenn die Adresse Zonen mit Priorität 100 und 50 übereinstimmt, gewinnt Priorität 100
- Nur die Versandmethoden der gewinnenden Zone sind verfügbar

**Anwendungsfälle**:

**Szenario 1: Spezifisch überschreibt Allgemein**
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
  Postleitzahlpattern: ["^100[0-2][0-9]$"]
  Priorität: 100

Zone B: "New York State"
  Länder: ["US"]
  Bundesstaaten: {"US": ["NY"]}
  Priorität: 50

Adresse: New York, NY 10001
→ Übereinstimmung mit beiden Zonen
→ Priorität 100 gewinnt
→ "Manhattan Premium" gilt (Premiumlieferdienst)
```

---

## Erstellen von Versandzonen

**Schritt-für-Schritt-Arbeitsablauf**:

1. **Navigiere zu Zonen**
   - Gehe zu Einstellungen > Versand > Versandzonen
   - Klicke auf "Versandzone hinzufügen"


Beschreibender Bezeichner (z. B. „Europäische Union“, „Westküste“, „Abgelegene Gebiete")

Setzen Sie die relative Wichtigkeit (100 für spezifisch, 50 für allgemein, 1 für den Standardfall)

Schalten Sie dies ein/aus

Alle kanadischen Postleitzahlen:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$",
  "",
  "### Vereinigtes Königreich (Postleitzahlen)",
  "",
  "**Format**: AA1A 1AA oder A1A 1AA",
  "",
  "```,
  "London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}",
  "Manchester (M):                        ^M[0-9]{1,2}",
  "Birmingham (B):                        ^B[0-9]{1,2}",
  "```",
  "",
  "### Australien (Postleitzahlen)",
  "",
  "**Format**: 4 Ziffern (z. B. 2000)",
  "",
  "```,
  "New South Wales (1000-2999):  ^[12][0-9]{3}$",
  "Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$",
  "Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$",
  "```",
  "",
  "### Muster-Testen",
  "",
  "**Bevor Muster gespeichert werden**, mit bekannten Postleitzahlen testen:",
  "",
  "1. Muster eingeben: `^90[0-9]{3}$`",
  "2. Testeingabe: "90210" → Sollte übereinstimmen",
  "3. Testeingabe: "10001" → Sollte NICHT übereinstimmen",
  "4. Testeingabe: "9021" → Sollte NICHT übereinstimmen (nur 4 Ziffern)",
  "",
  "Online-Regex-Tester (regex101.com) verwenden, um komplexe Muster zu validieren.",
  "",
  "---",
  "",
  "## Zusammenfassung der Zone-Abdeckung",
  "",
  "Zonen zeigen **Abdeckungszusammenfassung** in der Admin-Liste an, was enthalten ist:",
  "",
  "**Beispiele**:",
  "- "Alle Länder" → Keine Länderbeschränkungen",
  "- "US, CA, MX" → 3 Länder",
  "- "US (CA, OR, WA)" → US mit 3 Bundesstaaten",
  "- "US (90xxx-91xxx)" → US mit Postleitzahlenmustern",
  "",
  "**Zusammenfassung verwenden für**:",
  "- Schnelle Überprüfung der Zone-Abdeckung, ohne zu öffnen",
  "- Überschneidungen oder Lücken in der Abdeckung erkennen",
  "- Zone-Konfiguration im Überblick prüfen",
  "",
  "---",
  "",
  "## Verknüpfen von Zonen mit Versandmethoden",
  "",
  "Zonen und Methoden haben eine **Viele-zu-Viele-Beziehung**:",
  "",
  "**Von der Methode aus** (Empfohlen):",
  "1. Bearbeite Versandmethode",
  "2. Scroll zu Abschnitt "Versandzonen"",
  "3. Wähle anwendbare Zonen (Multi-Auswahl)",
  "4. Methode speichern",
  "",
  "**Von der Zone aus**:",
  "- Zonen verknüpfen sich nicht direkt mit Methoden",
  "- Verknüpfung erfolgt immer von der Methode-Konfiguration aus",
  "",
  "**Verhalten von Methode-Zone**:",
  "",
  "**Keine Zonen verknüpft** → Methode ist für **ALLE** Adressen verfügbar",
  "",
  "**Zonen verknüpft** → Methode ist nur dann verfügbar, wenn die Kundenadresse mindestens eine verknüpfte Zone entspricht",
  "",
  "**Beispiel**:",
  "```,
  "Methode: "Domestic Standard"",
  "Verknüpfte Zonen: ["Domestic USA"]",
  "→ Nur für US-Adressen angezeigt",
  "",
  "Methode: "International Express"",
  "Verknüpfte Zonen: ["EU", "Asia Pacific", "Rest of World"]",
  "→ Für alle nicht-US-Adressen angezeigt",
  "```",
  "",
  "---",
  "",
  "## Testen der Zonen-Übereinstimmung",
  "",
  "Bevor Live-Modus aktiviert wird, testen Sie die Zonen-Konfiguration:",
  "",
  "1. **Testbestellungen erstellen**",
  "- Adressen in verschiedenen Zonen verwenden",
  "- Überprüfen Sie, ob die korrekten Zonen übereinstimmen",
  "",
  "2. **Prioritätsauflösung prüfen**",
  "- Adresse verwenden, die mehreren Zonen entspricht",
  "- Überprüfen Sie, ob die Zone mit der höchsten Priorität gewinnt",
  "- Bestätigen Sie, ob die erwarteten Versandmethoden angezeigt werden",
  "",
  "3. **Randfälle testen**",
  "- Grenzpostleitzahlen (z. B. 90999 vs 91000)",
  "- Bundesstaatsgrenzen",
  "- Internationale Adressen mit ähnlichen Postleitzahlen",
  "",
  "4. **Zonen-Vorschau-Tool verwenden** (falls verfügbar)",
  "- Testadresse eingeben",
  "- Sehen Sie, welche Zone(n) übereinstimmen",
  "- Prioritätsauflösung ansehen",
  "",
  "---",
  "",
  "## Problembehandlung",
  "",
  "**Problem 1: Keine Versandmethoden am Kasse verfügbar**",
  "",
  "**Ursachen**:",
  "- Kundenadresse entspricht keiner Zone",
  "- Alle Methoden sind an Zonen verknüpft, die nicht übereinstimmen",
  "- Es gibt keine Methoden ohne Zonenbeschränkungen",
  "",
  "**Lösung**:",
  "- Fallback-Zone erstellen (alle Länder, Priorität 1)",
  "- ODER entfernen Sie Zonenbeschränkungen von mindestens einer Methode",
  "- Überprüfen Sie Zonen-Länder-/Bundesstaat-/Postleitzahlenmuster",
  "",
  "---",
  "",
  "**Problem 2: Falsche Zonen-Übereinstimmung**",
  "",
  "**Ursachen**:",
  "- Niedrigere Prioritätszone ausgewählt, obwohl eine höhere Prioritätszone übereinstimmt",
  "- Postleitzahlenmuster-Syntaxfehler (Muster schlägt stumm)",
  "- Bundesstaatscode-Mismatch (CA vs California)",
  "",
  "**Lösung**:",
  "- Prioritätswerte überprüfen (höhere Zahl = höhere Priorität)",
  "- Postleitzahlenmuster mit Regex-Validator testen",
  "- 2-Buchstaben-Bundesstaatscodes verwenden (CA, nicht California)",
  "",
  "---",
  "",
  "**Problem 3: Unerwartete Methode angezeigt**",
  "",
  "**Ursachen**:",
  "- Methode hat keine Zonen verknüpft (verfügbar überall)",
  "- Mehrere Zonen übereinstimmen, unerwartete Zone hat höhere Priorität",
  "- Zonenabdeckung überschneidet sich unbeabsichtigt",
  "",
  "**Lösung**:",
  "- Prüfen Sie die verknüpften Zonen der Methode",
  "- Priorität der übereinstimmenden Zonen prüfen",
  "- Zonenabdeckungszusammenfassung auf Überschneidungen prüfen",
  "",
  "---",
  "",
  "## Tipps",
  "",
  "Alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Mit 2 Zonen beginnen** - Inländisch und International, erweitern Sie bei Bedarf
- **Prioritäten sinnvoll nutzen** - Spezifische Zonen 100, regional 50, Fallback 1
- **Postmuster gründlich testen** - Regex-Fehler schlagen stumm, wodurch Zonen nicht übereinstimmen
- **Zonenlogik dokumentieren** - Notizen zur Zonenbeschreibung hinzufügen, um den Abdeckungszweck zu erklären
- **Übermäßige Zonen vermeiden** - Zu viele Zonen komplizieren die Konfiguration; verwenden Sie Versandaktionen für komplexe Szenarien
- **Staatscodes anstelle von Namen verwenden** - "CA" statt "Kalifornien", "NY" statt "New York"
- **Fallback-Zone erstellen** - Alle Länder, Priorität 1, stellt sicher, dass immer mindestens eine Versandoption verfügbar ist
- **Zonenleistung überwachen** - Wenn viele Kunden "kein Versand verfügbar" sehen, prüfen Sie die Zonenabdeckung
- **Zonen für neue Regionen aktualisieren** - Länder zum EU-Zonen hinzufügen, wenn neue Mitglieder beitreten
- **Beschreibende Namen verwenden** - "EU (ohne UK)" ist besser als "Zone 3"
- **Mit echten Adressen testen** - Verwenden Sie während des Tests tatsächlich Adressen der Kunden, nicht erfundene