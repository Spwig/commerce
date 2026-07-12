---
title: Versandpartner
---

Versandpartner verbinden Ihr Geschäft mit Carrier-APIs für Live-Versandkosten, Etiketten-Generierung und Paketverfolgung. Spwig unterstützt führende Carrier weltweit und ermöglicht auch die Einrichtung manueller Preislisten für Carrier ohne API-Integration.

![Versandpartner](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Verfügbare Carrier

| Carrier | Regionen | Schlüsselmerkmale |
|---------|---------|-------------|
| **FedEx** | Global | Live-Kosten, Etiketten-Druck, Verfolgung, mehrere Pakete |
| **UPS** | Global | Live-Kosten, Etiketten-Druck, Verfolgung, Adressvalidierung |
| **USPS** | Vereinigte Staaten | Inländische und internationale Kosten, Verfolgung |
| **NinjaVan** | Südostasien | Letzte Meile, Barzahlung bei Lieferung |
| **Canada Post** | Kanada | Inländische und internationale, Paket- und Briefkosten |
| **Australia Post** | Australien | Inländische und internationale, Paket- und Expresskosten |

## Verbindung zu einem Carrier

Navigieren Sie zu **Einstellungen > Versandpartner** und klicken Sie auf **Verbindung herstellen**, um den Einrichtungsführer zu starten.

### Schritt 1: Provider auswählen

Wählen Sie aus den verfügbaren Versandpartnern. Jede Karte zeigt die unterstützten Regionen und Merkmale des Providers an.

### Schritt 2: Einrichtungsanweisungen

Überprüfen Sie den carrier-spezifischen Einrichtungsführer:
- Wie Sie einen Entwickler/Geschäftsaccount bei dem Carrier erstellen
- Wo Sie Ihre API-Anmeldeinformationen finden
- Erforderliche Kontoeinstellungen (z. B. Shipper-Nummer, Meter-Nummer)

### Schritt 3: Anmeldeinformationen eingeben

Geben Sie die API-Anmeldeinformationen für Ihr Carrier-Konto ein. Die erforderlichen Felder variieren je nach Carrier:

- **API-Schlüssel / Geheimnis** — Authentifizierungsanmeldeinformationen
- **Kontonummer** — Ihre Carrier-Kontonummer oder Shipper-Nummer
- **Meter-Nummer** — Erfordert von einigen Carriern (z. B. FedEx)
- **Sandbox-Modus** — Aktivieren Sie diesen, um mit der Sandbox-API des Carriers zu testen, bevor Sie live gehen

### Schritt 4: Verbindung testen

Klicken Sie auf **Verbindung testen**, um Ihre Anmeldeinformationen zu überprüfen. Der Assistent bestätigt:
- Die API-Authentifizierung ist erfolgreich
- Die Kontoberechtigungen sind gültig
- Die Abfragen der Kosten liefern die erwarteten Ergebnisse

### Schritt 5: Konfigurieren und Speichern

Finalisieren Sie die Einstellungen:
- **Aktiv** — Aktivieren oder deaktivieren Sie den Carrier
- **Anzeigename** — Der Name, der bei der Kasse den Kunden angezeigt wird
- **Herkunftsadresse** — Der Lager- oder Fulfillment-Adresse für Kostenberechnungen

## Versandzonen

Versandzonen definieren geografische Bereiche für Kostenberechnungen. Navigieren Sie zu **Einstellungen > Versandzonen**, um sie zu verwalten.

### Zone erstellen

1. Klicken Sie auf **+ Zone hinzufügen**
2. Geben Sie der Zone einen Namen (z. B. "Inländisch", "Europa", "Asien-Pazifik")
3. Definieren Sie den Bereich der Zone mit einer oder mehreren der folgenden Optionen:
   - **Länder** — Wählen Sie spezifische Länder
   - **Bundesländer/Provinzen** — Beschränken Sie sich auf spezifische Regionen innerhalb eines Landes
   - **Postleitzahlpatterns** — Übereinstimmung mit Postleitzahlen/ZIP-Codes mithilfe von Mustern (z. B. "90*" für den Los Angeles-Bereich)
4. Setzen Sie die **Priorität** — Wenn Zonen sich überschneiden, wird die Zone mit der höchsten Priorität verwendet

### Zonenzuordnung

Wenn ein Kunde seine Versandadresse bei der Kasse eingibt, überprüft das System:
1. Zuerst Postleitzahnpatterns (spezifischste)
2. Dann Übereinstimmungen mit Bundesländern/Provinzen
3. Dann Übereinstimmungen mit Ländern
4. Verwendet die Zone mit der höchsten Priorität

## Versandaktionen

Versandaktionen wenden bedingte Modifikatoren auf Versandkosten an. Navigieren Sie zu **Einstellungen > Versandaktionen**, um sie zu konfigurieren.

### Aktionstypen

| Aktionstyp | Beschreibung |
|-----------|-------------|
| **Prozentualer Rabatt** | Reduziert die Versandkosten um einen bestimmten Prozentsatz |
| **Fester Rabatt** | Reduziert die Versandkosten um einen festen Betrag |
| **Kosten überschreiben** | Überschreibt die Kosten mit einem bestimmten Betrag |
| **Kostenlos versenden** | Setzt die Versandkosten auf null |
| **Prozentualer Aufschlag** | Fügt einem Prozentsatz der Kosten einen Aufschlag hinzu |
| **Fester Aufschlag** | Fügt den Kosten einen festen Aufschlag hinzu |

### Bedingungen

Jede Aktion kann eine oder mehrere Bedingungen haben, die erfüllt werden müssen:

| Bedingung | Beispiel |
|-----------|---------|
| **Warenkorbwert** | Kostenlose Lieferung ab 100 $ |
| **Gesamtgewicht** | Zusatzkosten für Bestellungen über 30 kg |
| **Artikelanzahl** | Rabatt für Bestellungen mit 5+ Artikeln |
| **Lieferzone** | Aktion nur für nationale Lieferungen anwenden |
| **Liefermethode** | Auf bestimmte Versandmethoden anwenden |
| **Produkte** | Sonderkonditionen für bestimmte Produkte |
| **Kundengruppe** | VIP-Kunden erhalten kostenlose Lieferung |
| **Zeitraum** | Feiertagslieferungsförderungen |

### Aktionenpriorität

- Aktionen werden in Prioritätsreihenfolge bewertet (niedrigste Zahl zuerst)
- **Weitere Aktionen stoppen** — Wenn aktiviert, wird bei Übereinstimmung dieser Aktion keine weitere Aktion geprüft
- Mehrere Aktionen können sich叠加 (z. B. 10 % Rabattaktion plus kostenlose Lieferungsgrenze)

## Preislisten

Preislisten bieten Staffelpreise basierend auf Bestellattributen an. Navigieren Sie zu **Einstellungen > Versandpreislisten**, um sie zu konfigurieren.

### Listenarten

Erstellen Sie Staffelstufen basierend auf:
- **Gewicht** — Preisstufen basierend auf dem Gesamtgewicht der Bestellung (z. B. 0–1 kg = 5 $, 1–5 kg = 10 $)
- **Bestellwert** — Preisstufen basierend auf dem Warenkorb-Subtotal
- **Menge** — Preisstufen basierend auf der Artikelanzahl

### Preisliste erstellen

1. Klicken Sie auf **+ Preisliste hinzufügen**
2. Benennen Sie die Liste und wählen Sie den Stufen-Typ aus
3. Fügen Sie Stufen mit Min-/Max-Bereichen und Preisen hinzu
4. Weisen Sie die Preisliste einer Lieferzone zu

Preislisten sind nützlich, wenn Sie keine API-Rate der Versandunternehmen verwenden und Ihre eigenen Preisstruktur definieren möchten.

## Versandverpackungen

Definieren Sie Standardverpackungsgrößen für genaue Preisberechnungen. Navigieren Sie zu **Einstellungen > Versandverpackungen**.

Für jeden Verpackungstyp legen Sie fest:
- **Name** — Beschreibung (z. B. „Kleine Box“, „Große Flachrate“)
- **Abmessungen** — Länge, Breite, Höhe
- **Maximalgewicht** — Maximales Gewicht, das die Verpackung tragen kann
- **Standard** — Verwenden Sie diese Verpackung, wenn keine spezifische Verpackung zugewiesen ist

Versandunternehmen verwenden die Verpackungsabmessungen für die dimensionsgewichtberechnung, was die Versandkosten beeinflussen kann.

## Manuelle Versandunternehmen (Versandvorlagen)

Für Versandunternehmen ohne API-Integration können Sie manuelle Versandvorlagen erstellen:

1. Navigieren Sie zu **Einstellungen > Versandvorlagen**
2. Klicken Sie auf **+ Vorlage hinzufügen**
3. Konfigurieren Sie:
   - **Name des Versandunternehmens** — Anzeigename im Checkout
   - **Tracking-URL-Vorlage** — URL-Muster mit einem `{tracking_number}`-Platzhalter (z. B. `https://track.carrier.com/?id={tracking_number}`)
   - **Geschätzte Lieferzeit** — Lieferzeitraum, der Kunden angezeigt wird
4. Weisen Sie eine Preisliste für die Preisgestaltung zu

Manuelle Versandunternehmen bieten Tracking-Links und Lieferzeitschätzungen ohne Live-API-Integration an.

## Mehrlager-Versand

Wenn Sie über mehrere Lager verfügen, kann der Versand von verschiedenen Ursprungsorten berechnet werden:

- **Lager für bestimmte Länder** — Weisen Sie Lager bestimmten Ländern zu, um kürzere Lieferwege zu ermöglichen
- **Fallback-Kette** — Definieren Sie, welches Lager für den Versand verwendet wird, wenn das primäre Lager ausverkauft ist
- **Pro-Produkt-Zuordnung** — Einige Produkte können nur von bestimmten Lagern versandt werden

Das System wählt automatisch das beste Lager basierend auf der Kundenstandort und Produktverfügbarkeit.

## Tipps

- Verbinden Sie Versand-APIs für **Live-Raten**, wenn möglich — sie sind genauer als Flachrate-Tabellen und berücksichtigen Gewicht, Abmessungen und Zielort.
- Erstellen Sie eine **„Rest der Welt“**-Lieferzone als Sammelkategorie für Länder, die nicht von spezifischen Zonen abgedeckt werden.
- Verwenden Sie den **Kostenlosen Versand**-Aktionstyp mit einer Warenkorbwert-Bedingung als Verkaufsankurbelung (z. B. „Kostenloser Versand ab 75 $“).
- Testen Sie die Versandkostenberechnung mit verschiedenen Adressen und Warenkorbinhalten, bevor Sie online gehen.
- Richten Sie **Versandvorlagen** mit Tracking-URL-Vorlagen für lokale Versandunternehmen ein, die keine API-Integrationen haben — Kunden erhalten dennoch Tracking-Links.
- Verwenden Sie **Versandverpackungen**, um genaue dimensionsgewichtspreise von Versandunternehmen wie FedEx und UPS zu erhalten.