---
title: Rücksendeanfragen & Verarbeitung
---

Rücksendeanfragen verfolgen Kundenrücksendungen von der Initiierung bis zur vollständigen Erstattung – Kunden wählen Artikel aus, für die sie eine Rücksendung beantragen, und geben Gründe an, Händler genehmigen oder ablehnen Anfragen, erstellen Rücksendeschilder, prüfen zurückgegebene Artikel und verarbeiten Erstattungen. Der Workflow durchläuft 9 Statusstufen (ausstehend → genehmigt → label_sent → in_transit → received → inspected → completed/rejected/cancelled) mit artikelbezogenen Rücksendegründen, Prüfnotizen und optionalen Neuerstehungskosten.

Verwenden Sie diese Admin-Seite, um Kundenrücksendeanfragen effizient zu überprüfen, zu genehmigen und zu verarbeiten.

## Rücksendeanfrage-Workflow

**9-Stufen-Prozess**:

### 1. Ausstehend (Kunde initiiert)

Kunde sendet Rücksendeanfrage:
- Wählt Artikel aus der Bestellung aus
- Gibt Gründe für Rücksendung pro Artikel an
- Optional: Kundennotizen
- Status: `ausstehend`

### 2. Genehmigt/Ablehnen (Händler prüft)

Händler prüft Anfrage:
- **Genehmigen**: Rücksendung erlaubt, fortzufahren mit Schildererstellung
- **Ablehnen**: Rücksendung verweigert mit Ablehnungsgrund
- Status: `genehmigt` oder `abgelehnt`

### 3. Schild gesendet (Rücksendungsschiffung)

Rücksendeschild erstellt:
- Händler erstellt Rücksendung (optional)
- Rücksendeschild per E-Mail an Kunden gesendet
- Kunde sendet Artikel zurück
- Status: `label_sent`

### 4. In Transit (Kunde sendet)

Kunde sendet Artikel:
- Nachverfolgung zeigt Bewegung an
- Automatischer Statusupdate von Carrier-Webhook
- Status: `in_transit`

### 5. Empfangen (Eintreffen auf Lager)

Artikel eintreffen:
- Lager scannt Sendung
- Artikel werden eingelagert
- Status: `received`

### 6. Geprüft (Qualitätskontrolle)

Händler prüft Artikel:
- Dokumentiert Artikelzustand (exzellent/gut/akzeptabel/beschädigt/defekt)
- Fügt Prüfnotizen hinzu
- Wendet Neuerstehungskosten an, falls zutreffend
- Status: `inspected`

### 7. Abgeschlossen (Erstattung verarbeitet)

Erstattung ausgestellt:
- Erstellen Sie eine zugehörige Erstattung
- Zahlung verarbeitet
- Rücksendung geschlossen
- Status: `completed`

**Alternative Ergebnisse**:
- **Abgebrochen**: Kunde bricht vor der Versendung ab
- **Ablehnen**: Händler lehnt nach Prüfung ab

---

## Rücksendeanfragen verarbeiten

**Schritt-für-Schritt**:

**Schritt 1: Ausstehende Anfragen überprüfen**
- Navigieren Sie zu Bestellungen > Rücksendeanfragen
- Filtern Sie nach Status = "Ausstehend"
- Klicken Sie auf Anfrage, um Details anzuzeigen

**Schritt 2: Anfrage bewerten**
- Überprüfen Sie Bestelldetails
- Prüfen Sie Rücksendegründe
- Bestätigen Sie Einhaltung der Rückgabepolitik (innerhalb des Rückgabewindows, artikelberechtigt)

**Schritt 3: Genehmigen oder ablehnen**
- Klicken Sie auf "Genehmigen", um Rücksendung anzunehmen
- ODER klicken Sie auf "Ablehnen" und geben Sie Ablehnungsgrund ein
- Speichern Sie die Entscheidung

**Schritt 4: Rücksendeschild erstellen** (wenn genehmigt)
- Klicken Sie auf "Rücksendungsschiffung erstellen"
- Wählen Sie Carrier/Dienst aus
- System generiert Rücksendeschild
- Schild wird automatisch per E-Mail an Kunden gesendet
- Status → `label_sent`

**Schritt 5: Transit überwachen**
- Nachverfolgungsupdates werden automatisch von Carrier-Webhooks synchronisiert
- Status wird automatisch auf `in_transit` aktualisiert, wenn Carrier Paket scannt

**Schritt 6: Artikel empfangen**
- Wenn Artikel eintreffen, klicken Sie auf "Als empfangen markieren"
- Status → `received`

**Schritt 7: Artikel prüfen**
- Öffnen Sie Rücksendeanfrage
- Wählen Sie Artikelzustand aus Dropdown-Liste:
  - Exzellent (wie neu, wiederverkäuflich)
  - Gut (geringe Nutzung, wiederverkäuflich)
  - Akzeptabel (sichtbare Nutzung, wiederverkäuflich mit Rabatt)
  - Beschädigt (nicht wiederverkäuflich)
  - Defekt (Herstellungsfehler)
- Fügen Sie Prüfnotizen hinzu
- Optional: Wendet Neuerstehungskosten an (Prozent oder Fixkosten)
- Status → `inspected`

**Schritt 8: Erstattung verarbeiten**
- Klicken Sie auf "Erstattung erstellen"
- System berechnet Erstattungsbetrag:
  - Originalartikelpreis
  - Minus Neuerstehungskosten (wenn angewendet)
  - Minus Versandkosten (wenn nicht erstattbar)
- Erstellen Sie Erstattung (verknüpft mit Rücksendeanfrage)
- Status → `completed`

---

## Artikelbezogene Rücksendegründe

Kunden wählen Grund pro Artikel:

**Häufige Gründe**:
- Falsches Produkt erhalten
- Produkt defekt/beschädigt
- Geändertes Verständnis/keine länger benötigt
- Produkt stimmt nicht mit Beschreibung überein
- Bessere Preis gefunden
- Versehentlich bestellt
- Qualität nicht wie erwartet

**Verwenden Sie Gründe für**:
- Analytics (verfolgen Sie häufige Rücksendegründe)
- Qualitätssicherung (identifizieren Sie defekte Produkte)
- Prozessverbesserung (verringern Sie vermeidbare Rücksendungen)

---

## Neuerstehungskosten

Wenden Sie Gebühren an, um Kosten für Rücksendeverarbeitung zu kompensieren:

**Konfiguration**:
- **Typ**: Prozent (z. B. 15%) oder Fixkosten (z. B. 5 $)
- **Wann anwenden**: Nicht defekte Rücksendungen, geöffnete Artikel, Spezialbestellungen

**Beispiel**:
```
Originaler Kauf: 100 $
Neuerstehungskosten: 15%
Erstattungsbetrag: 85 $
```

**Best Practices**:
- Kommunizieren Sie Neuerstehungskostenpolitik klar
- Wenden Sie nicht auf defekte Artikel an
- Erwägen Sie Freigabe für VIP-Kunden

---

## Rücksendeinspektion-Richtlinien

Erstellen Sie konsistente Inspektionskriterien:

**Exzellent**:
- Ungeöffnete Originalverpackung
- Keine sichtbare Abnutzung
- Alle Zubehörteile enthalten
- Vollständig wiederverkäuflich zum vollen Preis

**Gut**:
- Geöffnet, aber geringe Nutzung
- Leichte Verpackungsabnutzung
- Alle Komponenten vorhanden
- Vollständig wiederverkäuflich zum vollen Preis

**Akzeptabel**:
- Sichtbare Nutzung/Abnutzung
- Verpackung beschädigt
- Fehlende nicht-essentielle Zubehörteile
- Wiederverkäuflich mit Rabatt

**Beschädigt**:
- Physikalisch beschädigt
- Fehlende Teile
- Nicht wiederverkäuflich
- Entsorgen oder Reparieren erforderlich

**Defekt**:
- Herstellungsfehler
- Funktionsausfall
- Garantieanspruch
- Zurücksenden an Hersteller

---

## Rücksendeverkehrsoptionen

**Option 1: Kunde zahlt Rücksendekosten**
- Kein Rücksendeschild bereitgestellt
- Kunde wählt eigene Carrier
- Manuelle Eingabe der Tracking-Nummer

**Option 2: Händler stellt vorbezahltes Schild bereit**
- Erstellen Sie Rücksendeschild über Provider-Konto
- Kosten werden von Erstattung abgezogen ODER von Händler übernommen
- Tracking wird automatisch synchronisiert

**Option 3: Kostenlose Rücksendeverkehr**
- Händler übernimmt Rücksendekosten
- Verbessert Kundenzufriedenheit
- Erhöht Rücksenderate (bedenken Sie den Trade-off)

---

## Filtern & Berichte

**Nützliche Filter**:
- Status: Ausstehend (Aktion erforderlich)
- Datumsbereich: Letzte 30 Tage
- Bestellung: Spezifische Bestellung suchen
- Grund: Rücksendegründe verfolgen

**Rücksendeanalytik**:
- Rücksendequote pro Produkt
- Häufigste Rücksendegründe
- Durchschnittliche Verarbeitungszeit (ausstehend → abgeschlossen)
- Neuerstehungskosten-Einnahmen

---

## Tipps

- **Klarer Rückgabepolitik festlegen** - Kommunizieren Sie Zeitraum (30 Tage), Bedingungen, Gebühren
- **Anfragen schnell verarbeiten** - Reagieren Sie auf ausstehende Anfragen innerhalb von 24 Stunden
- **Gründlich prüfen** - Dokumentieren Sie Zustand, um Streitigkeiten zu vermeiden
- **Rücksendegründe verfolgen** - Nutzen Sie Daten, um Produkte/Beschreibungen zu verbessern
- **Automatisieren, wo möglich** - Carrier-Webhooks aktualisieren automatisch Transitstatus
- **Mit Kunden kommunizieren** - E-Mail-Benachrichtigungen bei jedem Statuswechsel
- **Seien Sie fair mit Neuerstehungskosten** - Anwenden Sie konsistent, Freigabe für Defekte
- **Überwachen Sie Rücksendebetrug** - Kennzeichnen Sie Kunden mit übermäßigen Rücksendungen
- **Verbessern Sie Verpackung** - Reduzieren Sie Rücksendungen aufgrund von Schäden
- **Aktualisieren Sie Lagerbestände schnell** - Wiederherstellen von Lagerbeständen nach Prüfung
- **Lernen Sie aus Muster** - Hohe Rücksendequote für bestimmte Produkte kann Qualitätsproblem signalisieren