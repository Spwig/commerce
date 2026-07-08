---
title: Bestellungen verwalten
---

Dieser Leitfaden deckt alles ab, was Sie zur Verwaltung von Kundenbestellungen benötigen -- von der Prüfung neuer Bestellungen über die Versandabwicklung bis hin zur Bearbeitung von Rückerstattungen.

## Bestellliste

Navigieren Sie zu **Bestellungen > Alle Bestellungen** in der Seitenleiste, um alle Bestellungen einzusehen. Die Liste zeigt Bestellnummer, Status, Kunde, Gesamtbetrag und Datum jeder Bestellung.

![Order list](/static/core/admin/img/help/manage-orders/order-list.webp)

Verwenden Sie die Filter oben, um Bestellungen nach Status, Zeitraum einzugrenzen oder nach Bestellnummer oder Kundenname zu suchen.

## Bestelldetails

Klicken Sie auf eine beliebige Bestellung, um die Detailseite zu öffnen. Hier finden Sie alle Informationen zur Bestellung übersichtlich in Abschnitte gegliedert.

![Order detail](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Bestellinformationen

Der obere Bereich zeigt:

- **Bestellnummer** — Die eindeutige Kennung dieser Bestellung
- **Status** — Aktueller Bestellstatus (Ausstehend, In Bearbeitung, Versendet, Zugestellt, Abgeschlossen, Storniert)
- **Kunde** — Name und E-Mail-Adresse des Kunden, der die Bestellung aufgegeben hat
- **Erstellt** — Wann die Bestellung aufgegeben wurde

### Bestellartikel

Der Artikelbereich listet alles auf, was der Kunde bestellt hat:

- Produktname und SKU
- Bestellte Menge
- Stückpreis und Zeilensumme
- Angewendete Rabatte

### Zahlungsdetails

Zeigt die verwendete Zahlungsmethode, Transaktions-ID und den Zahlungsstatus an. Bei Bestellungen mit ausstehender Zahlung können Sie hier den Status des Zahlungsanbieters verfolgen.

### Lieferadresse

Die Lieferadresse des Kunden. Wenn die Rechnungsadresse abweicht, werden beide angezeigt.

## Bestelllebenszyklus

Bestellungen durchlaufen typischerweise diese Status:

1. **Ausstehend** — Neue Bestellung eingegangen, warten auf Zahlungsbestätigung
2. **In Bearbeitung** — Zahlung bestätigt, Versand wird vorbereitet
3. **Versendet** — Bestellung mit Sendungsverfolgung versandt
4. **Zugestellt** — Kunde hat die Bestellung erhalten
5. **Abgeschlossen** — Bestellung abgeschlossen

## Eine Bestellung bearbeiten

### 1. Bestellung prüfen

Überprüfen Sie, dass:

- Artikel und Mengen korrekt sind
- Die Lieferadresse vollständig ist
- Die Zahlung eingegangen ist
- Etwaige Kundenhinweise berücksichtigt wurden

### 2. Sendung erstellen

Um die Bestellung zu versenden:

1. Klicken Sie auf **Sendung erstellen** auf der Bestelldetailseite
2. Wählen Sie die zu versendenden Artikel aus (für Teillieferungen nur bestimmte Artikel auswählen)
3. Wählen Sie den Versanddienstleister und den Service
4. Geben Sie die Sendungsverfolgungsnummer ein
5. Klicken Sie auf **Sendung speichern**

Der Bestellstatus wird automatisch auf **Versendet** aktualisiert und der Kunde erhält eine Versandbenachrichtigung per E-Mail mit den Sendungsverfolgungsinformationen.

### 3. Als Zugestellt markieren

Sobald der Kunde die Zustellung bestätigt oder die Sendungsverfolgung die Zustellung anzeigt, aktualisieren Sie den Status auf **Zugestellt** und dann auf **Abgeschlossen**.

## Bestellaktionen

### Notizen hinzufügen

Fügen Sie interne Notizen oder für den Kunden sichtbare Nachrichten hinzu:

1. Scrollen Sie zum Bereich **Notizen** auf der Bestelldetailseite
2. Geben Sie Ihre Nachricht ein
3. Wählen Sie, ob es sich um eine interne Notiz (nur für Mitarbeiter) oder eine Kundenbenachrichtigung handelt
4. Klicken Sie auf **Notiz hinzufügen**

Für den Kunden sichtbare Notizen lösen eine E-Mail-Benachrichtigung aus.

### Rückerstattung durchführen

Um eine Rückerstattung auszustellen:

1. Klicken Sie auf **Rückerstattung** auf der Bestelldetailseite
2. Wählen Sie die zu erstattenden Artikel aus (oder geben Sie einen benutzerdefinierten Betrag ein)
3. Wählen Sie einen Rückerstattungsgrund
4. Bestätigen Sie die Rückerstattung

Rückerstattungen werden über den ursprünglichen Zahlungsanbieter abgewickelt. Der Kunde erhält eine Bestätigung per E-Mail.

### Bestellung stornieren

Zum Stornieren:

1. Klicken Sie auf **Bestellung stornieren**
2. Wählen Sie einen Stornierungsgrund
3. Wählen Sie, ob die Artikel wieder eingelagert werden sollen
4. Bestätigen Sie

Der Kunde wird automatisch benachrichtigt und eine Rückerstattung wird eingeleitet, falls die Zahlung bereits erfolgt ist.

## Massenaktionen

In der Bestellliste können Sie mehrere Bestellungen auswählen und Massenaktionen anwenden:

- **Status aktualisieren** — Mehrere Bestellungen in denselben Status versetzen
- **Exportieren** — Ausgewählte Bestellungen als CSV herunterladen
- **Drucken** — Packzettel oder Rechnungen erstellen

## Bestellbenachrichtigungen

Kunden erhalten automatisch E-Mails in den wichtigsten Phasen:

- **Bestellbestätigung** — Sofort nach Aufgabe der Bestellung
- **Zahlungseingang** — Wenn die Zahlung bestätigt wird
- **Versandbenachrichtigung** — Wenn eine Sendung erstellt wird (enthält Sendungsverfolgungslink)
- **Zustellbestätigung** — Wenn die Bestellung als zugestellt markiert wird

Konfigurieren Sie E-Mail-Vorlagen unter **Einstellungen > E-Mail-Konfiguration**.

## Tipps

- Bearbeiten Sie Bestellungen täglich, um schnelle Versandzeiten aufrechtzuerhalten.
- Verwenden Sie die Statusfilter, um sich auf Bestellungen zu konzentrieren, die Aufmerksamkeit erfordern (Ausstehend und In Bearbeitung).
- Fügen Sie interne Notizen hinzu, um besondere Bearbeitungsanforderungen zu dokumentieren.
- Nutzen Sie in Spitzenzeiten Massenaktionen, um mehrere Bestellungen gleichzeitig zu aktualisieren.
- Richten Sie Versandregeln ein, um die Auswahl des Versanddienstleisters basierend auf Bestellgewicht und Zielort zu automatisieren.
