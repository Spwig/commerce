---
title: Gutschein-Codes
---

Gutschein-Codes ermöglichen es Ihnen, Rabattcodes, Gutscheine und Geschenkkarten zu erstellen, die Kunden am Checkout eingeben können, um einen Rabatt zu erhalten. Navigieren Sie zu **Marketing > Gutscheine** in der Admin-Seitenleiste.

![Gutschein-Liste](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Gutschein-Dashboard

Die Gutschein-Seite zeigt einen Überblick mit:

- **Statistik-Karten** — Aktive, Inaktive, Einlösungen und Gesamtanzahl an Gutscheinen
- **Filter** — Nach Code oder Name suchen, filtern nach Typ, Status und Umfang
- **Gutschein-Karten** — Jeder Gutschein wird mit Einlösungs- und Statusdetails angezeigt

## Gutschein erstellen

1. Klicken Sie auf **+ Gutschein hinzufügen** in der oberen rechten Ecke
2. Füllen Sie die Gutschein-Details aus:
   - **Code** — Der Code, den Kunden am Checkout eingeben (z. B. "SAVE20", "FREESHIP")
   - **Name/Beschreibung** — Interne Beschreibung für Ihre Referenz
   - **Rabatttyp** — Wählen Sie, wie der Rabatt angewendet wird
   - **Rabattwert** — Der Betrag oder der Prozentsatz des Rabatts
3. Konfigurieren Sie die Nutzungsvorgaben:
   - **Nutzungsgrenze** — Maximale Gesamtzahl der Einlösungen (0 = unbegrenzt)
   - **Pro-Kunden-Grenze** — Maximale Nutzung pro Kunde
   - **Mindestbestellwert** — Mindestbestellwert, der erforderlich ist
4. Legen Sie den **Umfang** fest:
   - **Ganzes Warenkorb** — Der Rabatt gilt für die gesamte Bestellung
   - **Spezifische Produkte** — Gilt nur für ausgewählte Artikel
   - **Spezifische Kategorien** — Gilt nur für Artikel in ausgewählten Kategorien
5. Setzen Sie optional ein Ablaufdatum:
   - **Ablaufdatum** — Datum, an dem der Gutschein nicht mehr gültig ist
6. Klicken Sie auf **Speichern**

## Gutschein-Typen

| Typ | Beschreibung | Beispiel |
|------|-------------|---------|
| **Fixer Betrag** | Deduziert einen festen Geldbetrag | 20 $ Rabatt auf die Bestellung |
| **Prozent** | Deduziert einen Prozentsatz des Gesamtbetrags | 15 % Rabatt auf die Bestellung |
| **Kostenlose Lieferung** | Entfernt die Versandkosten | Kostenlose Lieferung für jede Bestellung |

## Gutscheine verwalten

### Gutschein-Karten

Jede Gutschein-Karte zeigt:
- **Code** — Der Gutschein-Code in fett
- **Beschreibung** — Was der Gutschein bewirkt
- **Status-Abzeichen** — Aktiv oder Inaktiv
- **Rabattdetails** — Typ und Wert (z. B. "$ 20,00" oder "15,00%")
- **Umfang** — Ob er für den gesamten Warenkorb oder spezifische Artikel gilt
- **Nutzungszahl** — Wie oft der Gutschein eingelöst wurde
- **Erstellungsdatum** — Wann der Gutschein erstellt wurde
- **Ablauf** — Ablaufdatum oder "Kein Ablauf"

### Gutschein-Aktionen

Jede Karte hat Aktionstasten:
- **Bearbeiten** — Ändern Sie die Gutschein-Einstellungen
- **Historie ansehen** — Sehen Sie die Einlösungs-Historie
- **Löschen** — Entfernen Sie den Gutschein

### Gutscheine filtern

Verwenden Sie die Filterleiste, um spezifische Gutscheine zu finden:
- **Suchen** — Nach Code, Name oder Beschreibung suchen
- **Typ** — Fixer Betrag, Prozent oder kostenlose Lieferung
- **Status** — Aktiv oder Inaktiv
- **Umfang** — Ganzes Warenkorb oder artikelbezogen

## Massengenerator für Gutscheine

Für große Kampagnen können Sie Gutscheine in Massen generieren:
1. Das System generiert automatisch eindeutige Codes (z. B. "COUPONX1600406498")
2. Legen Sie gemeinsame Parameter für alle generierten Gutscheine fest
3. Verteilen Sie die Codes per E-Mail, sozialen Medien oder Druck

## Kundenerfahrung

Wenn ein Kunde einen Gutschein-Code hat:
1. Er geht zum **Checkout**
2. Gibt den Code im **Rabatt-Code**-Feld ein
3. Der Rabatt wird sofort angewendet, wenn der Gutschein gültig ist
4. Die Bestellübersicht wird aktualisiert, um den Rabatt anzuzeigen

Wenn ein Gutschein ungültig ist (abgelaufen, Nutzungsgrenze erreicht, Mindestbestellwert nicht erfüllt), sieht der Kunde eine klare Fehlermeldung.

## Tipps

- Verwenden Sie merkenswerte Codes für Marketingkampagnen (z. B. "SUMMER20" anstelle von Zufallszeichenketten).
- Legen Sie pro-Kunden-Grenzen fest, um Missbrauch wertvoller Rabatte zu verhindern.
- Verwenden Sie Mindestbestellwerte, um die Profitabilität zu sichern (z. B. "10 $ Rabatt auf Bestellungen über 50 $").
- Überwachen Sie die Einlösungsanzahl auf dem Dashboard, um die Effektivität der Kampagnen zu verfolgen.
- Erstellen Sie zeitlich begrenzte Gutscheine, um Dringlichkeit zu erzeugen (z. B. "Nur dieses Wochenende gültig").
- Verwenden Sie den Aktiv/Inaktiv-Status, um Gutscheine ohne sie zu löschen zu pausieren.