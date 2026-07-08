---
title: Kommissionen verstehen
---

Kommissionen sind Gewinnberichte, die erstellt werden, wenn ein Affiliate erfolgreich einen Verkauf auf Ihre Store vermittelt. Jede Kommission ist mit einer bestimmten Bestellung, einem Affiliate und einem Programm verbunden und geht durch einen Lebenszyklus von ausstehend zu bezahlt. Dieser Leitfaden erläutert, wie Kommissionen funktionieren, wie sie berechnet werden und wie Sie sie effektiv verwalten.

## Was ist eine Kommission?

Eine Kommission stellt den Betrag dar, der einem Affiliate für die Vermittlung eines Kunden, der einen Kauf abgeschlossen hat, geschuldet ist. Wenn ein Kunde auf einen Verweislink eines Affiliates klickt und innerhalb des Cookie-Verfallsfensters eine Bestellung tätigt, erstellt Spwig automatisch eine Kommissionsaufzeichnung.

Jede Kommission enthält:
- **Affiliate** — Der Partner, der den Kunden vermittelt hat
- **Programm** — Das Affiliate-Programm, das die Kommissionsregeln definiert
- **Bestellung** — Die Bestellung, die die Kommission erzeugt hat
- **Betrag** — Der berechnete Kommissionswert
- **Status** — Der aktuelle Zustand im Kommissionslebenszyklus
- **Datumsangaben** — Erstellungsdatum, Genehmigungs-/Ablehnungsdatum und Zahlungsdatum

## Kommissionsberechnung

Kommissionen werden automatisch basierend auf dem KommissionsTyp und dem Satz des Programms berechnet.

| KommissionsTyp | Berechnung | Beispiel |
|----------------|-----------|---------|
| **Prozentual** | Gesamtbetrag der Bestellung × Kommissionsprozent ÷ 100 | Bestellung: $200, Rate: 10% → **$20 Kommission** |
| **Fixbetrag** | Flacher Betrag pro Bestellung | Rate: $15 → **$15 Kommission** (unabhängig vom Bestellwert) |

### Berechnungsbeispiele

**Prozentuale Kommission (10%)**:
- Kunde tätigt eine $50 Bestellung → $5 Kommission
- Kunde tätigt eine $150 Bestellung → $15 Kommission
- Kunde tätigt eine $300 Bestellung → $30 Kommission

**Fixe Kommission ($20)**:
- Kunde tätigt eine $50 Bestellung → $20 Kommission
- Kunde tätigt eine $150 Bestellung → $20 Kommission
- Kunde tätigt eine $300 Bestellung → $20 Kommission

Die Kommission wird auf der **Zwischensumme der Bestellung** (vor Versand und Steuern) berechnet und wird sofort erstellt, sobald die Bestellung platziert wird.

## Kommissionslebenszyklus

Jede Kommission geht durch eine Reihe von Statusänderungen vom Erstellen bis zur Auszahlung:

```
Ausstehend → Genehmigt → Bezahlt
   ↓
Ablehnen
```

### Statusdefinitionen

| Status | Beschreibung | Was passiert |
|--------|-------------|--------------|
| **Ausstehend** | Bestellung platziert, Kommission wartet auf Prüfung | Kommission wird erstellt, aber noch nicht bestätigt. Der Affiliate kann sie sehen, kann aber keine Mittel abheben. |
| **Genehmigt** | Händler bestätigt, dass der Verkauf gültig ist | Kommission wird bestätigt und dem verfügbaren Guthaben des Affiliates hinzugefügt. Eignet sich für die Auszahlung. |
| **Ablehnen** | Händler lehnt die Kommission ab | Kommission wird abgelehnt (z. B. Bestellung wurde erstattet, betrügerisch oder Vertragsbedingungen verletzt). Nicht für Auszahlung geeignet. |
| **Bezahlt** | Kommission wurde in einer abgeschlossenen Auszahlung enthalten | Affiliate wurde bezahlt. Kommission ist final und kann nicht mehr geändert werden. |

![Kommissionsliste](/static/core/admin/img/help/commission-management/commission-list.webp)

## Wann werden Kommissionen erstellt

Kommissionen werden automatisch erstellt, nachdem diese Sequenz abgeschlossen wurde:

1. **Kunde klickt auf Affiliate-Link** — Der Verweis-URL enthält den eindeutigen Tracking-Code des Affiliates (z. B., `?ref=JOHNSMITH`)
2. **Cookie wird gesetzt** — Ein Tracking-Cookie wird im Browser des Kunden mit dem Affiliate-Code gespeichert
3. **Kauf innerhalb des Cookie-Verfallsfensters** — Kunde vervollständigt eine Bestellung, bevor der Cookie abläuft (Standard: 30 Tage)
4. **System weist die Bestellung zu** — Spwig prüft auf einen aktiven Tracking-Cookie und identifiziert den verweisenden Affiliate
5. **Kommission wird automatisch erstellt** — Eine Kommissionsaufzeichnung wird mit dem Status **Ausstehend** erstellt

Die Kommission wird **sofort** erstellt, sobald die Bestellung platziert wird, auch noch bevor die Zahlung bestätigt wurde. Dies ermöglicht Händlern, Kommissionen zu überprüfen, während Bestellungen verarbeitet werden.

## Tracking & Zuordnung

Spwig verwendet **Last-Click-Zuordnung**, um festzustellen, welcher Affiliate für einen Verkauf Kredit bekommt.

### Wie die Zuordnung funktioniert

- **Last-Click-Modell** — Der zuletzt geklickte Affiliate-Link bekommt den Kredit (auch wenn mehrere Affiliates den Kunden verweisen)
- **Cookie-basiertes Tracking** — Ein Cookie speichert den Affiliate-Code im Browser des Kunden
- **Cookie-Verfallszeit** — Bestimmt das Fenster, in dem ein Verkauf zugeordnet werden kann (pro Programm konfiguriert, typischerweise 30 Tage)
- **IP- und Sitzungstracking** — Zusätzliche Daten helfen, betrügerische Muster zu erkennen

### Zuordnungsbeispiel

- Tag 1: Kunde klickt auf den Link von Affiliate A → Cookie für Affiliate A gesetzt
- Tag 5: Kunde klickt auf den Link von Affiliate B → Cookie **wird aktualisiert** auf Affiliate B (Last-Click gewinnt)
- Tag 7: Kunde tätigt eine Bestellung → Kommission geht an **Affiliate B**

Wenn der Kunde am Tag 35 (nach Ablauf des 30-Tage-Cookie) zurückkehrt und eine Bestellung tätigt, wird **keine Kommission** erstellt, da das Tracking-Fenster geschlossen ist.

## Kommissionsdetails

Navigieren Sie zu **Marketing > Kommissionen**, um alle Kommissionsaufzeichnungen anzuzeigen.

### Kommissionsfelder

Jede Kommission zeigt an:

| Feld | Beschreibung |
|-------|-------------|
| **Affiliate** | Name und Code des Affiliates |
| **Programm** | Name des Affiliate-Programms |
| **Bestellung** | Bestellnummer (klickbarer Link, um die vollständigen Bestelldetails anzuzeigen) |
| **Betrag** | Berechneter Kommissionswert |
| **Status** | Aktueller Zustand (Ausstehend, Genehmigt, Ablehnen, Bezahlt) |
| **Erstellt** | Wann die Kommission erstellt wurde |
| **Genehmigt/Ablehnen Datum** | Wann der Status aktualisiert wurde |
| **Bezahlungsdatum** | Wann die Auszahlung verarbeitet wurde |
| **Notizen** | Interne Notizen zur Kommission |

### Anzeigen von Bestelldetails

Klicken Sie auf die **Bestellnummer** in der Kommissionsaufzeichnung, um die ursprüngliche Bestellung anzuzeigen. Dies ermöglicht Ihnen, zu überprüfen:
- Gesamtbetrag und gekaufte Artikel
- Kundendaten
- Zahlungsstatus
- Versandstatus
- Eventuelle Erstattungen oder Rückgaben

Dieser Kontext hilft Ihnen, zu entscheiden, ob Sie die Kommission genehmigen oder ablehnen sollen.

## Kommissionen verwalten

Obwohl dieser Leitfaden sich auf das Verständnis von Kommissionen konzentriert, werden die praktischen Schritte zur Genehmigung, Ablehnung und Zahlung von Kommissionen detailliert im Hilfe-Thema **Kommissionsverwaltung** behandelt.

### Schneller Überblick

- **Genehmigen** — Bestätigen Sie, dass die Bestellung legitim ist und die Kommission gültig ist
- **Ablehnen** — Lehnen Sie Kommissionen für betrügerische Bestellungen, Erstattungen oder Verstöße gegen Richtlinien ab
- **Notizen hinzufügen** — Dokumentieren Sie Gründe für Genehmigung oder Ablehnung für zukünftige Referenzen
- **Auszahlungen verarbeiten** — Gruppieren Sie genehmigte Kommissionen in Batch-Auszahlungen

Sehen Sie sich die verwandten Hilfe-Themen an, um Schritt-für-Schritt-Anweisungen für jede Verwaltungsaufgabe zu erhalten.

## Tipps

- Überprüfen Sie ausstehende Kommissionen **täglich** während Ihres ersten Monats, um einen Rhythmus zu etablieren und eventuelle Tracking-Probleme frühzeitig zu erkennen
- Richten Sie **E-Mail-Benachrichtigungen** ein, um Sie zu informieren, wenn neue Kommissionen erstellt werden, damit Sie sie überprüfen können, während die Bestelldetails noch frisch sind
- Genehmigen Sie Kommissionen **nach der Bestellabwicklung** (nicht sofort nach Bestellungserfassung), um Stornierungen und Rückgaben zu berücksichtigen
- Verwenden Sie das **Notizenfeld**, um Entscheidungen zu dokumentieren, insbesondere bei abgelehnten Kommissionen, damit Sie ein Protokoll haben, wenn Affiliates Fragen stellen
- Achten Sie auf **Muster in Ablehnungen** — wenn ein Affiliate viele abgelehnte Kommissionen hat, kann dies auf Betrug oder Missverständnis der Programmbestimmungen hindeuten
- Erwägen Sie, eine **Genehmigungspolitik für Kommissionen** (z. B., "genehmigt nach 14-Tage-Rückgabewindow") zu erstellen und sie den Affiliates mitzuteilen, um klare Erwartungen zu setzen