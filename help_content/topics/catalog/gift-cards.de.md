---
title: Gutscheinkarten
---

Gutscheinkarten ermöglichen es Ihren Kunden, Loyalitätsguthaben zu kaufen, das an jemanden als Geschenk gesendet oder für den persönlichen Gebrauch behalten werden kann. Empfänger erhalten einen eindeutigen Code per E-Mail, den sie am Checkout einlösen können.

![Gutscheinkarten-Verwaltung](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Bezeichnungsarten

Kontrollieren Sie, wie Kunden den Betrag der Gutscheinkarte wählen:

| Typ | Beschreibung |
|------|-------------|
| **Feste Bezeichnungen** | Kunden wählen aus vordefinierten Beträgen (z. B. $25, $50, $100) |
| **Benutzerdefinierter Betrag** | Kunden können einen beliebigen Betrag innerhalb eines Min-/Max-Bereichs eingeben |
| **Beide** | Vordefinierte Bezeichnungen plus eine Option für einen benutzerdefinierten Betrag anbieten |

## Erstellen eines Gutscheinkarten-Produkts

### Schritt 1: Produkt einrichten

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt hinzufügen**
2. Wählen Sie **Produkttyp** auf **Gutscheinkarte**
3. Geben Sie den Produktnamen und die Beschreibung ein
4. Konfigurieren Sie die Bezeichnungs-Einstellungen:
   - Wählen Sie eine **Bezeichnungsart** (Fest, Benutzerdefiniert oder Beide)
   - Für Fest: legen Sie die verfügbaren Bezeichnungs-Beträge fest
   - Für Benutzerdefiniert: setzen Sie den **Mindest-** und **Höchstbetrag**
5. Setzen Sie **Ablaufdatum in Tagen** (0 = nie abläuft) — dies bestimmt, wie lange Gutscheinkarten nach dem Kauf gültig sind
6. Speichern und veröffentlichen Sie das Produkt

### Schritt 2: Veröffentlichen und Verkaufen

Nach der Veröffentlichung erscheint die Gutscheinkarte in Ihrem Onlineshop wie jedes andere Produkt. Kunden können sie durchsuchen, einen Betrag auswählen und sie in ihren Warenkorb legen.

## Lebenszyklus einer Gutscheinkarte

Eine Gutscheinkarte folgt diesem Lebenszyklus:

1. **Kauf** — Der Kunde kauft das Gutscheinkarten-Produkt und gibt die Empfängerdetails an
2. **Lieferung** — Eine E-Mail mit dem Gutscheinkarten-Code wird dem Empfänger automatisch gesendet
3. **Einlösung** — Der Empfänger gibt den Code am Checkout ein, um den Betrag zu verwenden
4. **Bilanzverfolgung** — Jeder Gebrauch reduziert die Bilanz, bis sie auf null kommt

## Kaufablauf für Kunden

Wenn ein Kunde eine Gutscheinkarte kauft:

1. **Betrag auswählen** — Wählen Sie eine Bezeichnung oder geben Sie einen benutzerdefinierten Betrag ein
2. **Empfängerdetails** — Geben Sie die E-Mail-Adresse und den Namen des Empfängers ein
3. **Persönliche Nachricht** — Fügen Sie eine optionale Nachricht hinzu, die in der Liefer-E-Mail enthalten wird
4. **Absendername** — Geben Sie den Namen des Absenders für die E-Mail an
5. **Geplante Lieferung** — Optional können Sie die E-Mail für einen zukünftigen Tag planen (z. B. einen Geburtstag)
6. **Bezahlung abschließen** — Beenden Sie den Kauf wie bei jedem anderen Produkt

## Automatische Lieferung

Nach dem Kauf wird die Gutscheinkarte automatisch geliefert:

- Eine gestaltete E-Mail wird an den Empfänger gesendet, die enthält:
  - Den eindeutigen Gutscheinkarten-Code
  - Den Wert der Gutscheinkarte
  - Die persönliche Nachricht vom Absender
  - Einen Link, um den verbleibenden Betrag zu prüfen
- Wenn eine geplante Lieferung festgelegt wurde, wird die E-Mail am festgelegten Datum und zur festgelegten Uhrzeit gesendet
- Der Absender erhält eine Bestätigungs-E-Mail mit den Details der Gutscheinkarte

## Verwaltung von Gutscheinkarten im Admin-Bereich

Navigieren Sie zu **Produkte > Gutscheinkarten**, um alle Gutscheinkarten zu verwalten:

### Statistik-Dashboard

Am oberen Rand der Seite zeigen vier Karten die wichtigsten Kennzahlen:

- **Gesamtzahl der Gutscheinkarten** — Gesamtzahl der ausgestellten Gutscheinkarten
- **Aktiv** — Aktuelle Karten mit verfügbarem Guthaben
- **Gesamtguthaben** — Gesamt verbleibendes Guthaben aller Karten
- **Teilweise genutzt** — Karten, die teilweise eingelöst wurden

### Filter

Filtern Sie Gutscheinkarten nach:

- **Suche** — Nach Code, E-Mail oder Empfängername suchen
- **Status** — Aktiv, Inaktiv, Abgelaufen, Vollständig eingelöst oder Teilweise genutzt
- **Guthaben** — Guthaben vorhanden oder Guthaben null
- **Erstellt** — Zeitraum (Heute, Diese Woche, Dieser Monat, Dieses Jahr)

### Gutscheinkarten-Details

Jede Gutscheinkarte zeigt:

- **Code** — Der eindeutige Einlösungscod (z. B. GC-XXXX-XXXX-XXXX)
- **Empfänger** — E-Mail-Adresse und Name
- **Status-Abzeichen** — Aktueller Status mit Farbcodierung
- **Guthaben / Anfangsbetrag / Einlösung** — Finanzübersicht mit Prozent genutzt
- **Wichtige Daten** — Erstellt, ausgestellt, erster Gebrauch
- **Absender** — Wer die Gutscheinkarte gekauft hat

### Aktionen

Für jede Gutscheinkarte können Sie:

- **Bearbeiten** — Details der Gutscheinkarte ansehen und bearbeiten
- **Transaktionen ansehen** — Die vollständige Transaktionshistorie einsehen
- **E-Mail erneut senden** — Die Liefer-E-Mail an den Empfänger erneut senden
- **Deaktivieren** — Die Karte deaktivieren (Guthaben bleibt erhalten, aber die Karte kann nicht verwendet werden)

## Einlösung am Checkout

Wenn ein Kunde einen Gutscheinkarten-Code am Checkout eingibt:

1. Der Code wird validiert (aktiv, nicht abgelaufen, Guthaben vorhanden)
2. Das verfügbare Guthaben wird angezeigt
3. Das Guthaben wird auf den Gesamtbetrag der Bestellung angewendet
4. Wenn das Guthaben den gesamten Bestellbetrag abdeckt, ist keine zusätzliche Zahlung erforderlich
5. Wenn das Guthaben kleiner als der Gesamtbetrag der Bestellung ist, zahlt der Kunde den Restbetrag
6. Die Transaktion wird protokolliert und das Guthaben wird aktualisiert

## Rückerstattungsverfahren

Bei Rückerstattungen von Bestellungen, die eine Gutscheinkarte verwendet haben:

- **Nicht genutzte Gutscheinkarten** — Deaktivieren Sie die Gutscheinkarte vollständig
- **Teilweise genutzte Karten** — Das Guthaben muss manuell über eine Transaktion angepasst werden
- **Vollständige Rückerstattung** — Kreditieren Sie den Betrag über eine Rückerstattungstransaktion auf das Gutscheinkarten-Guthaben

## Tipps

- Legen Sie vernünftige Ablaufzeiten fest (z. B. 365 Tage), um den lokalen Gutscheinkarten-Vorschriften zu entsprechen — einige Jurisdiktionen erfordern Mindestgültigkeitszeiträume.
- Verwenden Sie die Bezeichnungsart **Beide**, um Bequemlichkeit (vordefinierte Beträge) und Flexibilität (benutzerdefinierte Beträge) anzubieten.
- Überwachen Sie regelmäßig die Kennzahl **Gesamtguthaben** — sie stellt eine offene Verbindlichkeit auf Ihren Büchern dar.
- Verwenden Sie geplante Lieferungen für saisonale Promotionen — Kunden können Gutscheinkarten frühzeitig kaufen und erhalten sie am genauen Tag geliefert.
- Testen Sie den gesamten Ablauf (Kauf, E-Mail-Lieferung, Einlösung) mit einer Testbestellung, bevor Sie loslegen.
- Wenn Sie Kunden in mehreren Ländern verkaufen, können Sie Gutscheinkarten in bestimmten Währungen ausstellen — siehe den Hilfe-Themenpunkt **Multi-Währungs-Gutscheinkarten** für Details.