---
title: Steuerkonfiguration
---

Steuersätze definieren Umsatzsteuer, Mehrwertsteuer und andere Konsumsteuern, die am Kassenautomaten basierend auf der Kundenstandort und Produktart angewendet werden – konfigurieren Sie Steuersätze auf Land/Bundesland/Stadt-Ebene mit optionalen Produktkategorie-Ausnahmen. Spwig unterstützt zusammengesetzte Steuern (Steuer auf Steuer), priorisierte Steuerauswahl und Steuervorlagen für die schnelle Einrichtung regionaler Steuersysteme (EU Mehrwertsteuer, US Umsatzsteuer). Steuersätze können bestimmte Produkttypen (Lebensmittel, Bücher, digitale Waren) oder Kategorien ausnehmen, um den lokalen Steuergesetzen zu entsprechen.

Verwenden Sie die Steuerkonfiguration, um die gesetzliche Einhaltung der Steuererhebungsanforderungen in Ihren Verkaufsgebieten sicherzustellen.

## Steuersatzkonfiguration

Jeder Steuersatz definiert:

**Geografischer Umfang**:
- Land (erforderlich)
- Bundesland/Provinz (optional)
- Stadt (optional)
- Postleitzahlenmuster (optional, Regex)

**Satzdetails**:
- **Steuersatz**: Prozent (z. B. 8,5 %)
- **Name**: Anzeigename (z. B. "Kalifornische Umsatzsteuer")
- **Priorität**: Höhere Priorität gewinnt, wenn mehrere Sätze übereinstimmen
- **Aktiv**: Schalter ohne Löschen

**Ausnahmen**:
- **Ausgenommene Produkttypen**: Digitale Waren, physische Waren, Dienstleistungen
- **Ausgenommene Kategorien**: Bestimmte Produktkategorien (Lebensmittel, Bücher, Medizin)

**Zusammengesetzte Steuern**:
- **Ist zusammengesetzt**: Wenden Sie diesen Satz auf vorherige Steuern an (Steuer auf Steuer)
- Beispiel: Die Quebec PST wird auf die GST angewendet

---

## Häufige Steuerszenarien

### US Umsatzsteuer (Bundeslandsebene)

```
Name: California Sales Tax
Land: US
Bundesland: CA
Satz: 7,25 %
Priorität: 50
```

### EU Mehrwertsteuer (Landesebene)

```
Name: UK VAT
Land: GB
Satz: 20 %
Priorität: 50

Name: Deutschland Mehrwertsteuer
Land: DE
Satz: 19 %
Priorität: 50
```

### Kanadische GST/PST (Zusammengesetzt)

```
Satz 1: Bundesweite GST
Land: CA
Satz: 5 %
Priorität: 100
Ist zusammengesetzt: Nein

Satz 2: Quebec PST
Land: CA
Bundesland: QC
Satz: 9,975 %
Priorität: 50
Ist zusammengesetzt: Ja  (wird auf den Gesamtbetrag + GST angewendet)
```

### Stadtebene Steuer

```
Name: Seattle Umsatzsteuer
Land: US
Bundesland: WA
Stadt: Seattle
Satz: 10,1 %
Priorität: 100
```

---

## Steuerfreistellungen

### Produkttyp-Steuerfreistellungen

Ganze Produkttypen freistellen:

- **Digitale Waren**: Software, E-Books, Musik
- **Physische Waren**: Tangible Produkte
- **Dienstleistungen**: Beratung, Installation

Beispiel: EU Mehrwertsteuer gilt nicht für digitale Waren für Verbraucher (in einigen Fällen)

### Kategorie-Steuerfreistellungen

Bestimmte Produktkategorien freistellen:

- Lebensmittel & Lebensmittelgeschäfte (häufig freigestellt oder reduzierter Satz)
- Bücher & Bildungsmaterialien
- Medizinische Produkte & Pharmazeutika
- Kleidung (einige Gebiete)

Konfiguration:
```
Name: California Sales Tax
Satz: 7,25 %
Exempt Categories: ["Food & Beverages", "Prescription Medicine"]
```

---

## Steuervorlagen

Schnellladen von gängigen Steuerkonfigurationen:

**US Umsatzsteuer-Vorlage**:
- Alle 50 Bundesländer + DC
- Bundeslandsebene Sätze
- Automatisch aktualisiert, wenn Sätze geändert werden

**EU Mehrwertsteuer-Vorlage**:
- Alle 27 EU-Mitgliedstaaten
- Standard-Mehrwertsteuersätze
- Umkehrungslogik für B2B

**Um Vorlagen zu verwenden**:
1. Einstellungen > Warenkorb > Steuervorlagen
2. Wählen Sie eine Vorlagengruppe aus (z. B. "US Umsatzsteuer 2026")
3. Klicken Sie auf "Vorlage laden"
4. Steuersätze werden automatisch importiert
5. Anpassungen nach Bedarf vornehmen

---

## Prioritätsauflösung

Wenn mehrere Sätze übereinstimmen, gewinnt die höchste Priorität:

Beispiel:
```
Kunde in Seattle, WA:

Satz A: US Bundes (Priorität 1) - 0 %
Satz B: Washington Bundesland (Priorität 50) - 6,5 %
Satz C: Seattle Stadt (Priorität 100) - 3,6 %

Ergebnis: Seattle-Satz (Gesamtsatz 10,1 %) gilt
```

---

## Steuerauswahl-Optionen

Konfigurieren Sie in Einstellungen > Warenkorb > Steuereinstellungen:

- **Preise enthalten Steuer**: Zeigen Sie Preise mit Steuer an (EU-Stil)
- **Steuern separat anzeigen**: Zeigen Sie Steuern als Zeilenposten an (US-Stil)
- **Steuern runden**: Pro Artikel oder pro Bestellung
- **Steuersatzbezeichnung**: Bezeichnung anpassen ("Mehrwertsteuer", "Umsatzsteuer", "GST")

---

## Testen der Steuerkonfiguration

Vor der Veröffentlichung:

1. Erstellen Sie Testbestellungen aus verschiedenen Jurisdiktionen
2. Überprüfen Sie, ob der richtige Steuersatz angewendet wird
3. Prüfen Sie, ob Ausnahmen für ausgeschlossene Kategorien funktionieren
4. Testen Sie die Berechnung der zusammengesetzten Steuern
5. Überprüfen Sie die Steuern in Rechnungen

---

## Einhaltungshinweise

- **US**: Nexus-Regeln erfordern Steuererhebung in Bundesländern, in denen Sie physischen Aufenthalt oder wirtschaftlichen Nexus haben
- **EU**: Mehrwertsteuerregistrierte Unternehmen müssen Mehrwertsteuer von EU-Kunden erheben
- **Kanada**: GST/HST/PST variiert nach Bundesland
- **Konsultieren Sie einen Steuerberater**: Steuergesetze ändern sich häufig, überprüfen Sie die aktuellen Anforderungen

---

## Tipps

- **Verwenden Sie Steuervorlagen** – Schneller als manuelle Eingabe, automatisch aktualisiert
- **Überwachen Sie Nexus-Schwellenwerte** – Verfolgen Sie Verkäufe nach Bundesland für US wirtschaftlichen Nexus
- **Setzen Sie die Priorität richtig** – Stadt > Bundesland > Land
- **Testen Sie zusammengesetzte Steuern** – Überprüfen Sie, ob Berechnungen mit den erwarteten Beträgen übereinstimmen
- **Aktualisieren Sie jährlich** – Steuersätze ändern sich, überprüfen Sie jedes Jahr im Januar
- **Dokumentieren Sie Ausnahmen** – Halten Sie Aufzeichnungen, warum Kategorien ausgenommen sind
- **Verwenden Sie beschreibende Namen** – "California Sales Tax 2026" ist besser als "Tax 1"
- **Aktivieren Sie Steuern standardmäßig** – Sicherer als das Vergessen, Steuern anzuwenden

