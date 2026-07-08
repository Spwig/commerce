---
title: Versanddienstleister
---

Versanddienstleister verbinden Ihren Shop mit Carrier-APIs für Echtzeit-Versandtarife, Etikettenerstellung und Paketverfolgung. Spwig unterstützt große Versandunternehmen weltweit und ermöglicht es Ihnen auch, manuelle Tariftabellen für Versandunternehmen ohne API-Integration einzurichten.

![Shipping providers](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Verfügbare Versandunternehmen

| Versandunternehmen | Regionen | Hauptfunktionen |
|--------------------|----------|-----------------|
| **FedEx** | Weltweit | Echtzeit-Tarife, Etikettendruck, Sendungsverfolgung, Mehrpaket |
| **UPS** | Weltweit | Echtzeit-Tarife, Etikettendruck, Sendungsverfolgung, Adressvalidierung |
| **USPS** | Vereinigte Staaten | Nationale und internationale Tarife, Sendungsverfolgung |
| **NinjaVan** | Südostasien | Letzte-Meile-Zustellung, Nachnahme-Unterstützung |
| **Canada Post** | Kanada | National und international, Paket- und Brieftarife |
| **Australia Post** | Australien | National und international, Paket und Express |

## Einen Versanddienstleister Verbinden

Navigieren Sie zu **Einstellungen > Versanddienstleister** und klicken Sie auf **Anbieter Verbinden**, um den Einrichtungsassistenten zu starten.

### Schritt 1: Anbieter Auswählen
Wählen Sie aus den verfügbaren Versandunternehmen. Jede Karte zeigt die unterstützten Regionen und Funktionen des Versandunternehmens.

### Schritt 2: Einrichtungsanleitung
Lesen Sie die versandunternehmensspezifische Einrichtungsanleitung:
- Wie Sie ein Entwickler-/Geschäftskonto beim Versandunternehmen erstellen
- Wo Sie Ihre API-Zugangsdaten finden
- Erforderliche Kontoeinstellungen (z. B. Versendernummer, Zählernummer)

### Schritt 3: Zugangsdaten Eingeben
Geben Sie die API-Zugangsdaten für Ihr Versandunternehmenskonto ein. Die erforderlichen Felder variieren je nach Versandunternehmen:
- **API-Schlüssel / Geheimschlüssel** — Authentifizierungsdaten
- **Kontonummer** — Ihre Konto- oder Versendernummer beim Versandunternehmen
- **Zählernummer** — Von einigen Versandunternehmen benötigt (z. B. FedEx)
- **Sandbox-Modus** — Aktivieren, um mit der Sandbox-API des Versandunternehmens zu testen, bevor Sie live gehen

### Schritt 4: Verbindung Testen
Klicken Sie auf **Verbindung Testen**, um Ihre Zugangsdaten zu überprüfen. Der Assistent bestätigt:
- Die API-Authentifizierung ist erfolgreich
- Die Kontoberechtigungen sind gültig
- Tarifabfragen liefern erwartete Ergebnisse

### Schritt 5: Konfigurieren und Speichern
Schließen Sie die Einstellungen ab:
- **Aktiv** — Versandunternehmen aktivieren oder deaktivieren
- **Anzeigename** — Der Name, der Kunden an der Kasse angezeigt wird
- **Ursprungsadresse** — Die Lager- oder Fulfillment-Adresse für Tarifberechnungen

## Versandzonen

Versandzonen definieren geografische Gebiete für Tarifberechnungen. Navigieren Sie zu **Einstellungen > Versandzonen**, um diese zu verwalten.

### Eine Zone Erstellen
1. Klicken Sie auf **+ Zone Hinzufügen**
2. Geben Sie der Zone einen Namen (z. B. "Inland", "Europa", "Asien-Pazifik")
3. Definieren Sie die Abdeckung der Zone mit einem oder mehreren der folgenden Kriterien:
   - **Länder** — Wählen Sie bestimmte Länder aus
   - **Bundesländer/Provinzen** — Beschränken Sie auf bestimmte Regionen innerhalb eines Landes
   - **Postleitzahlenmuster** — Ordnen Sie Postleitzahlen mit Mustern zu (z. B. "90*" für den Raum Los Angeles)
4. Legen Sie die **Priorität** fest — Wenn sich Zonen überschneiden, wird die Zone mit der höchsten Priorität verwendet

### Zonenzuordnung
Wenn ein Kunde seine Lieferadresse an der Kasse eingibt, führt das System folgende Prüfungen durch:
1. Zuerst Postleitzahlenmuster (am spezifischsten)
2. Dann Bundesland/Provinz-Übereinstimmungen
3. Dann Länder-Übereinstimmungen
4. Verwendet die übereinstimmende Zone mit der höchsten Priorität

## Versandregeln

Versandregeln wenden bedingte Modifikatoren auf Versandtarife an. Navigieren Sie zu **Einstellungen > Versandregeln**, um diese zu konfigurieren.

### Regeltypen

| Regeltyp | Beschreibung |
|----------|-------------|
| **Rabatt %** | Reduziert den Versandtarif um einen Prozentsatz |
| **Fester Rabatt** | Reduziert den Versandtarif um einen festen Betrag |
| **Kosten Festlegen** | Überschreibt den Tarif mit einem bestimmten Betrag |
| **Kostenloser Versand** | Setzt die Versandkosten auf null |
| **Zuschlag %** | Fügt einen prozentualen Zuschlag zum Tarif hinzu |
| **Fester Zuschlag** | Fügt einen festen Zuschlag zum Tarif hinzu |

### Bedingungen
Jede Regel kann eine oder mehrere Bedingungen haben, die erfüllt sein müssen:

| Bedingung | Beispiel |
|-----------|---------|
| **Warenkorbwert** | Kostenloser Versand bei Bestellungen über 100 $ |
| **Gesamtgewicht** | Zuschlag für Bestellungen über 30 kg |
| **Artikelanzahl** | Rabatt für Bestellungen mit 5+ Artikeln |
| **Versandzone** | Regel nur auf Inlandslieferungen anwenden |
| **Versandmethode** | Auf bestimmte Versandmethoden anwenden |
| **Produkte** | Sondertarife für bestimmte Produkte |
| **Kundengruppe** | VIP-Kunden erhalten kostenlosen Versand |
| **Datumsbereich** | Versandaktionen für die Feiertage |

### Regelpriorität
- Regeln werden in Prioritätsreihenfolge ausgewertet (niedrigste Nummer zuerst)
- **Weitere Regeln Stoppen** — Wenn aktiviert und diese Regel zutrifft, werden keine weiteren Regeln geprüft
- Mehrere Regeln können gestapelt werden (z. B. eine 10%-Rabatt-Regel plus eine Regel für kostenlosen Versand ab einem bestimmten Schwellenwert)

## Tariftabellen

Tariftabellen bieten gestaffelte Preise basierend auf Bestellattributen. Navigieren Sie zu **Einstellungen > Versand-Tariftabellen**, um diese zu konfigurieren.

### Tabellentypen
Erstellen Sie Tarifstufen basierend auf:
- **Gewicht** — Preisstufen nach Gesamtgewicht der Bestellung (z. B. 0-1 kg = 5 $, 1-5 kg = 10 $)
- **Bestellwert** — Preisstufen nach Warenkorb-Zwischensumme
- **Menge** — Preisstufen nach Artikelanzahl

### Eine Tariftabelle Erstellen
1. Klicken Sie auf **+ Tariftabelle Hinzufügen**
2. Benennen Sie die Tabelle und wählen Sie den Stufentyp
3. Fügen Sie Stufen mit Min/Max-Bereichen und Preisen hinzu
4. Ordnen Sie die Tariftabelle einer Versandzone zu

Tariftabellen sind nützlich, wenn Sie keine Carrier-API-Tarife verwenden und Ihre eigene Preisstruktur definieren möchten.

## Versandpakete

Definieren Sie Standard-Verpackungsgrößen für genaue Tarifberechnungen. Navigieren Sie zu **Einstellungen > Versandpakete**.

Für jeden Pakettyp legen Sie fest:
- **Name** — Beschreibung (z. B. "Kleine Box", "Große Pauschale")
- **Abmessungen** — Länge, Breite, Höhe
- **Maximalgewicht** — Maximales Gewicht, das das Paket aufnehmen kann
- **Standard** — Dieses Paket verwenden, wenn keine spezifische Verpackung zugewiesen ist

Versandunternehmen verwenden Paketabmessungen für Berechnungen des Volumensgewichts, was die Versandtarife beeinflussen kann.

## Manuelle Versandunternehmen (Versandunternehmen-Vorlagen)

Für Versandunternehmen ohne API-Integration erstellen Sie manuelle Versandunternehmen-Vorlagen:
1. Navigieren Sie zu **Einstellungen > Versandunternehmen-Vorlagen**
2. Klicken Sie auf **+ Vorlage Hinzufügen**
3. Konfigurieren Sie:
   - **Name des Versandunternehmens** — Anzeigename für die Kasse
   - **Tracking-URL-Vorlage** — URL-Muster mit einem `{tracking_number}`-Platzhalter (z. B. `https://track.versand.de/?id={tracking_number}`)
   - **Geschätzte Lieferzeit** — Lieferzeitrahmen, der den Kunden angezeigt wird
4. Kombinieren Sie mit einer Tariftabelle für die Preisgestaltung

Manuelle Versandunternehmen bieten Tracking-Links und Lieferschätzungen ohne Echtzeit-API-Integration.

## Multi-Warehouse-Versand

Wenn Sie mehrere Lager haben, kann der Versand von verschiedenen Standorten berechnet werden:
- **Länderspezifisches Lager** — Ordnen Sie Lager bestimmten Ländern zu für kürzere Versandwege
- **Rückfallkette** — Definieren Sie, welches Lager versendet, wenn das Hauptlager nicht vorrätig ist
- **Produktbezogene Zuordnung** — Einige Produkte können nur aus bestimmten Lagern versendet werden

Das System wählt automatisch das beste Lager basierend auf dem Standort des Kunden und der Produktverfügbarkeit aus.

## Tipps

- Verbinden Sie Carrier-APIs für **Echtzeit-Tarife** wann immer möglich — sie sind genauer als Pauschal-Tariftabellen und passen sich an Gewicht, Abmessungen und Zielort an.
- Erstellen Sie eine **"Restliche Welt"**-Versandzone als Auffanglösung für Länder, die nicht von spezifischen Zonen abgedeckt werden.
- Nutzen Sie den Regeltyp **Kostenloser Versand** mit einer Warenkorbwert-Bedingung als Verkaufsanreiz (z. B. "Kostenloser Versand ab 75 $ Bestellwert").
- Testen Sie die Versandtarifberechnungen mit verschiedenen Adressen und Warenkorbinhalten, bevor Sie live gehen.
- Richten Sie **Versandunternehmen-Vorlagen** mit Tracking-URL-Vorlagen für lokale Versandunternehmen ein, die keine API-Integrationen haben — Kunden erhalten trotzdem Tracking-Links.
- Verwenden Sie **Versandpakete**, um genaue Volumensgewicht-Preise von Versandunternehmen wie FedEx und UPS zu erhalten.
