---
title: Versand einrichten
---

Dieser Leitfaden erklärt, wie Sie den Versand für Ihren Shop konfigurieren -- von der Einrichtung grundlegender Versandmethoden bis zur Anbindung von Versanddienstleistern für Echtzeit-Tarife.

## Versandübersicht

Spwig bietet zwei Ansätze für den Versand:

- **Manuelle Versandmethoden** — Pauschalpreis-Methoden, die Sie selbst definieren (z.B. "Standardversand — 5,99 EUR")
- **Versanddienstleister-Integrationen** — Echtzeit-Tarife von Anbietern wie FedEx, UPS und DHL

Sie können einen der beiden Ansätze verwenden oder beide kombinieren.

## Versandmethoden

Versandmethoden sind die Optionen, die Ihre Kunden beim Bezahlvorgang sehen. Navigieren Sie zu **Bestellungen > Sendungen** in der Seitenleiste, um diese zu verwalten.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Versandmethode erstellen

1. Klicken Sie auf **Versandmethode hinzufügen**
2. Füllen Sie die Details aus:
   - **Name** — Anzeigename für Kunden (z.B. "Expresslieferung")
   - **Beschreibung** — Kurze Beschreibung des Dienstes
   - **Preis** — Fester Versandpreis
   - **Geschätzte Lieferzeit** — Lieferzeitschätzung (z.B. "3-5 Werktage")
3. Klicken Sie auf **Speichern**

## Versandzonen

Versandzonen definieren die geografischen Regionen, in denen Ihre Versandmethoden gelten. Navigieren Sie zum Bereich **Versandzonen**, um diese zu verwalten.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Zone erstellen

1. Klicken Sie auf **Versandzone hinzufügen**
2. Konfigurieren Sie die Zone:
   - **Zonenname** — Interner Name (z.B. "Inland", "Europa")
   - **Länder** — Wählen Sie die Länder aus, die zu dieser Zone gehören
   - **Bundesländer/Regionen** — Optional auf bestimmte Bundesländer eingrenzen
   - **Postleitzahlen-Muster** — Verwenden Sie Muster wie "9*", um bestimmte Gebiete anzusprechen
3. Weisen Sie dieser Zone Versandmethoden zu
4. Klicken Sie auf **Speichern**

### Zonenpriorität

Wenn die Adresse eines Kunden mehreren Zonen entspricht, hat die spezifischste Zone Vorrang. Eine Zone mit Ausrichtung auf Bundeslandebene hat Vorrang vor einer Zone auf Landesebene.

## Versanddienstleister-Integrationen

Verbinden Sie sich mit Versanddienstleistern, um beim Bezahlvorgang in Echtzeit berechnete Tarife anzubieten.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Verfügbare Anbieter

Durchsuchen und installieren Sie Versandanbieter aus dem Marketplace.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Unterstützte Versanddienstleister umfassen:

- **FedEx** — Landweg, Express, International
- **UPS** — Landweg, 2-Tage, Übernacht, Weltweit
- **DHL** — Express, eCommerce
- **USPS** — Priority, First Class, Media Mail
- Und weitere, verfügbar über den Marketplace

### Versanddienstleister einrichten

1. Gehen Sie zur Seite der Versandanbieter und klicken Sie beim bevorzugten Dienstleister auf **Installieren**
2. Folgen Sie dem Einrichtungsassistenten:
   - **Schritt 1** — Anbieterdetails prüfen
   - **Schritt 2** — Allgemeine Einstellungen konfigurieren
   - **Schritt 3** — Ihre API-Zugangsdaten eingeben (Kontonummer, API-Schlüssel usw.)
   - **Schritt 4** — Bestimmte Dienste aktivieren (Landweg, Express usw.)
   - **Schritt 5** — Verbindung testen
3. Nach der Verbindung erscheinen die Tarife des Dienstleisters automatisch beim Bezahlvorgang

### API-Zugangsdaten

Jeder Versanddienstleister erfordert ein API-Konto:

- **FedEx** — Registrieren Sie sich beim FedEx Developer Portal, erstellen Sie eine App und kopieren Sie Ihren API-Schlüssel und Ihr Geheimnis
- **UPS** — Registrieren Sie sich beim UPS Developer Kit, fordern Sie einen Zugriffsschlüssel an
- **DHL** — Kontaktieren Sie DHL für API-Zugangsdaten über deren Geschäftsportal

## Versandregeln

Erstellen Sie erweiterte Regeln, um zu steuern, wann und wie Versandmethoden angeboten werden.

### Häufige Regeln

- **Kostenloser Versand ab 50 EUR** — Legen Sie einen Mindestwarenkorbwert für kostenlosen Versand fest
- **Pauschaltarif für leichte Bestellungen** — Fester Tarif, wenn das Bestellgewicht unter einem Schwellenwert liegt
- **Express für abgelegene Gebiete deaktivieren** — Express-Optionen basierend auf Postleitzahlen ausblenden
- **Prozentualer Aufschlag** — Bearbeitungsgebühr als Prozentsatz der Versanddienstleister-Tarife hinzufügen

### Regel erstellen

1. Navigieren Sie zum Bereich der Versandregeln
2. Klicken Sie auf **Regel hinzufügen**
3. Legen Sie Bedingungen fest (Warenkorbsumme, Gewicht, Zone usw.)
4. Definieren Sie die Aktion (Tarif anpassen, Methode ausblenden, kostenlosen Versand aktivieren)
5. Speichern Sie die Regel

Regeln werden der Reihe nach ausgewertet; die erste zutreffende Regel wird angewendet.

## Kostenloser Versand

### Shopweiter kostenloser Versand

Aktivieren Sie kostenlosen Versand global unter **Einstellungen > Shop-Einstellungen**:

- Schalten Sie **Kostenloser Versand** ein
- Legen Sie optional einen Mindestbestellwert fest
- Wählen Sie, welche Regionen in Frage kommen

### Kostenloser Versand als Aktion

Erstellen Sie zeitlich begrenzte Angebote für kostenlosen Versand:

1. Gehen Sie zu **Marketing > Verkäufe & Aktionen**
2. Erstellen Sie eine neue Aktion
3. Legen Sie die Bedingung fest: "Warenkorbsumme über X"
4. Legen Sie die Aktion fest: "Kostenloser Versand"
5. Konfigurieren Sie Start- und Enddatum

## Internationaler Versand

Für internationale Bestellungen stellen Sie sicher, dass Ihre Produkte folgende Angaben haben:

- **HS-Code** — Zolltarifnummer des Harmonisierten Systems
- **Ursprungsland** — Herstellungsland
- **Zollwert** — Deklarierter Wert für den Zoll

Diese Felder befinden sich auf der Registerkarte **Inventar** jedes Produkts. Versanddienstleister verwenden diese Informationen, um automatisch Zolldokumente zu erstellen.

## Tipps

- Beginnen Sie mit manuellen Versandmethoden, um Ihren Shop schnell zum Laufen zu bringen, und fügen Sie später Versanddienstleister-Integrationen hinzu.
- Erstellen Sie zuerst Versandzonen für Ihre häufigsten Zielorte.
- Testen Sie Ihre Versandkonfiguration immer, indem Sie Testbestellungen mit verschiedenen Adressen aufgeben.
- Nutzen Sie die Tarifaufschlagsfunktion, um Bearbeitungs- und Verpackungskosten abzudecken.
- Richten Sie Schwellenwerte für kostenlosen Versand ein, um den durchschnittlichen Bestellwert zu erhöhen.
