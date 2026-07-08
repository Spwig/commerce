---
title: Versandverpackungen
---

Versandverpackungen definieren vordefinierte Kasten- und Umschlagsgrößen für die Preisberechnung und automatische Verpackung – geben Sie die Innenmaße (verfügbare Fläche), Wanddicke (äußere Maße für Carrier-APIs), Gewichtsgrenzen und Verpackungskosten an. Carrier verwenden äußere Maße, um das Volumengewicht zu berechnen, um genaue Preisangebote zu erhalten. Verpackungen haben eine Prioritätsreihenfolge für Bin-Packing-Algorithmen, die automatisch optimale Verpackungskombinationen auswählen, um Warenkorbartikel zu passen.

Konfigurieren Sie Verpackungen, wenn Sie Carrier-APIs für Echtzeit-Preise verwenden oder wenn Sie genaue Volumengewichtsberechnungen benötigen.

## Verpackungskonfiguration

Jede Verpackung definiert:

**Maße**:
- **Innenlänge**: Verfügbare Fläche innen (cm)
- **Innenbreite**: Verfügbare Fläche innen (cm)
- **Innenhöhe**: Verfügbare Fläche innen (cm)
- **Wanddicke**: Dicke des Verpackungsmaterials (cm)

**Äußere Maße** (automatisch berechnet):
```
Äußere Länge = Innenlänge + (2 × Wanddicke)
Äußere Breite = Innenbreite + (2 × Wanddicke)
Äußere Höhe = Innenhöhe + (2 × Wanddicke)
```

**Gewicht & Kosten**:
- **Leergewicht**: Gewicht der leeren Verpackung (Gramm)
- **Maximalgewicht**: Maximale Belastbarkeit (Gramm)
- **Kosten**: Kosten für das Verpackungsmaterial (für Kostenoptimierung)

**Eigenschaften**:
- **Name**: Verpackungsbezeichnung (z. B. "Kleiner Kasten", "Großer Umschlag")
- **Typ**: Kasten oder Umschlag
- **Priorität**: Reihenfolge der automatischen Verpackungsauswahl (niedriger = höhere Priorität)
- **Aktiv**: Verfügbarkeit umschalten

---

## Warum äußere Maße wichtig sind

Carrier berechnen das **Volumengewicht** aus äußeren Maßen:

**Volumengewichtsformel**:
```
Volumengewicht = (Länge × Breite × Höhe) / Teiler

Gängige Teiler:
- DHL: 5000
- FedEx/UPS: 5000 (national), 6000 (international)
```

**Beispiel**:
```
Kleiner Kasten:
Innen: 20cm × 15cm × 10cm
Wanddicke: 0,5cm
Außen: 21cm × 16cm × 11cm

Volumengewicht = (21 × 16 × 11) / 5000 = 0,74kg

Wenn tatsächliches Gewicht = 0,5kg → Carrier rechnet mit 0,74kg (Volumengewicht ist höher)
```

**Warum Genauigkeit wichtig ist**: Ungenaue Maße → falsche Preisangebote → Kunde wird über- oder unterkostet.

---

## Häufige Verpackungsgrößen

### Kleiner gepolsterter Umschlag

```
Innen: 25cm × 18cm × 2cm
Wanddicke: 0,3cm
Maximalgewicht: 500g
Typ: Umschlag
Verwendung: Dokumente, Bücher, Schmuck
```

### Kleiner Kasten

```
Innen: 20cm × 15cm × 10cm
Wanddicke: 0,5cm
Maximalgewicht: 5kg
Typ: Kasten
Verwendung: Kleine Elektronik, Kosmetik, Accessoires
```

### Mittlerer Kasten

```
Innen: 30cm × 25cm × 20cm
Wanddicke: 0,5cm
Maximalgewicht: 15kg
Typ: Kasten
Verwendung: Kleidung, Schuhe, Küchenartikel
```

### Großer Kasten

```
Innen: 45cm × 35cm × 30cm
Wanddicke: 0,6cm
Maximalgewicht: 30kg
Typ: Kasten
Verwendung: Großverpackungen, mehrere Produkte, große Elektronik
```

---

## Automatische Verpackungsalgorithmen

Das System wählt automatisch Verpackungen für Warenkorbartikel aus:

**Funktionsweise**:
1. Berechnen Sie das Gesamtvolumen der Warenkorbartikel
2. Sortieren Sie die Verpackungen nach Priorität (niedrigste Zahl zuerst)
3. Versuchen Sie, die Artikel in eine einzelne Verpackung zu passen
4. Wenn das nicht funktioniert, versuchen Sie die nächste Verpackungsgöße
5. Wenn keine einzelne Verpackung passt, kombinieren Sie mehrere Verpackungen
6. Optimieren Sie basierend auf der Einstellung `optimize_for`

**Optimierungsmethoden**:
- **Kosten**: Minimieren Sie Verpackungskosten
- **Volumen**: Minimieren Sie den verlorenen Raum
- **Anzahl**: Minimieren Sie die Anzahl der Verpackungen

**Beispiel**:
```
Warenkorbartikel:
- Artikel A: 10cm × 8cm × 5cm, 200g
- Artikel B: 15cm × 12cm × 8cm, 400g

Verpackungen (nach Priorität):
1. Kleiner Kasten (20×15×10, Priorität=1)
2. Mittlerer Kasten (30×25×20, Priorität=2)

Algorithmus:
Versuche mit Kleiner Kasten: Beide Artikel passen
Ergebnis: 1× Kleiner Kasten (optimiert für Anzahl)
```

---

## Verpackungsprioritäten

**Priorität bestimmt die Verpackungsreihenfolge**:

Priorität 1 (höchste): Kleine Verpackungen werden zuerst ausprobiert
Priorität 10: Große Verpackungen als letzte Option

**Strategie**:
- Kleine Verpackungen = niedrige Prioritätszahlen (1-3)
- Mittlere Verpackungen = mittlere Priorität (4-6)
- Große Verpackungen = hohe Prioritätszahlen (7-10)

**Warum**: Beginnen Sie mit der kleinsten Verpackung, erhöhen Sie bei Bedarf die Größe → minimiert Versandkosten.

---

## Wanddicke Genauigkeit

Messung der tatsächlichen Verpackung:

**Wie man misst**:
1. Holen Sie sich eine leere Box
2. Messen Sie die Innenmaße (innen)
3. Messen Sie die Außenmaße (außen)
4. Berechnen Sie: `(Außen - Innen) / 2 = Wanddicke`

**Beispiel**:
```
Innenbreite: 20cm
Außenbreite: 21cm
Wanddicke: (21 - 20) / 2 = 0,5cm
```

**Gängige Dicken**:
- Gepolsterter Umschlag: 0,2-0,4cm
- Einwandiger Karton: 0,4-0,6cm
- Zweiwandiger Karton: 0,8-1,0cm

---

## Erstellen einer Verpackungsvorlage

**Schritt-für-Schritt**:

1. Einstellungen > Versand > Versandverpackungen
2. Klicken Sie auf "Versandverpackung hinzufügen"
3. Geben Sie einen Namen ein (z. B. "Mittlerer Kasten")
4. Wählen Sie den Typ (Kasten oder Umschlag)
5. Geben Sie die Innenmaße ein (L × B × H in cm)
6. Geben Sie die Wanddicke ein (cm)
7. Das System berechnet automatisch die äußeren Maße
8. Geben Sie das Leergewicht ein (Gewicht der leeren Verpackung in Gramm)
9. Geben Sie das Maximalgewicht ein (Belastbarkeit in Gramm)
10. Optional: Geben Sie Kosten ein (für Kostenoptimierung)
11. Setzen Sie die Priorität (1-10)
12. Aktiv umschalten = Ja
13. Speichern

---

## Testen der Verpackungsauswahl

**Manueller Test**:
1. Fügen Sie Produkte zum Testwagen hinzu
2. Gehen Sie zur Kasse
3. Wählen Sie eine Echtzeit-Versandmethode (verwendet Verpackungen)
4. Überprüfen Sie, ob ein vernünftiges Preisangebot zurückgegeben wird
5. Überprüfen Sie die Carrier-Antwort (API-Protokolle zeigen ausgewählte Verpackungen an)

**Automatische Verpackungsvorschau**:
- Einige Versandsanbieterkonten zeigen die Verpackungsaufschlüsselung an
- Sehen Sie, welche Verpackungen für den Warenkorb ausgewählt wurden
- Überprüfen Sie die optimale Verpackung

---

## Tipps

- **Messungen genau durchführen** - Ungenaue Maße → falsche Carrier-Preise
- **Wanddicke einbeziehen** - Kritisch für Volumengewicht
- **Beginnen Sie mit 3-4 Größen** - Kleiner, mittlerer, großer decken die meisten Szenarien ab
- **Setzen Sie realistische Maximalgewichte** - Verpackungsfähigkeit, nicht theoretische Grenze
- **Verwenden Sie Prioritäten sinnvoll** - Kleine Kästen Priorität 1, große Kästen Priorität 10
- **Testen Sie mit echten Produkten** - Überprüfen Sie, ob automatische Verpackung die richtigen Größen auswählt
- **Aktualisieren Sie bei Verpackungsänderungen** - Neuer Lieferant = Maße erneut messen
- **Berücksichtigen Sie spezielle Artikel** - Zerbrechliche Artikel benötigen möglicherweise spezifische Kastengrößen
- **Halten Sie aktive Verpackungen minimal** - Zu viele Optionen verlangsamen den automatischen Verpackungsalgorithmus
- **Dokumentieren Sie die Verpackungen** - Notieren Sie, welche Produkte in welche Verpackungen passen
