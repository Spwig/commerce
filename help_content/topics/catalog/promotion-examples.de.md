---
title: Beispiel für Promotionen
---

Dieser Leitfaden zeigt konkrete Beispiele, wie Sie verschiedene Promotion-Typen konfigurieren können. Jedes Beispiel enthält die genauen Feldwerte, die Sie im Promotion-Assistenten eingeben müssen, damit Sie Schritt für Schritt folgen können oder sie für Ihr Geschäft anpassen können.

![Promotion Card](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Beispiel: Prozentualer Rabatt auf eine Kategorie

**Szenario:** 30 % Rabatt auf alle Schuhe für die Winter-Ausverkaufsaktion.

Navigieren Sie zu **Marketing > Sales & Promotions** und klicken Sie auf **+ Promotion erstellen**. Geben Sie die folgenden Werte in jedem Schritt des Assistenten ein:

| Schritt | Feld | Wert |
|---------|------|------|
| Basics | Name | Winter-Ausverkauf — 30 % Rabatt auf Schuhe |
| Basics | Beschreibung | Saisonende-Ausverkauf für alle Schuhe |
| Basics | Aktiv | Angekreuzt |
| Rabatt | Typ | Prozentualer Rabatt |
| Rabatt | Wert | 30 |
| Zeitplan | Startdatum | 15. Januar 2026 |
| Zeitplan | Enddatum | 28. Februar 2026 |
| Produkte | Anwenden auf | Kategorien |
| Produkte | Ausgewählt | Schuhe, Stiefel, Sandalen |

Dies erstellt einen zeitlich begrenzten Verkauf, der alle Produkte in den ausgewählten Kategorien automatisch reduziert. Ein Paar Stiefel im Wert von 120 $ wird 84 $, und ein Paar Sandalen im Wert von 60 $ wird 42 $.

## Beispiel: Fixer Betrag Rabatt auf eine Kollektion

**Szenario:** 15 $ Rabatt auf Artikel der Kollektion Summer Essentials.

| Schritt | Feld | Wert |
|---------|------|------|
| Basics | Name | Summer Essentials — 15 $ Rabatt |
| Basics | Aktiv | Angekreuzt |
| Rabatt | Typ | Betrag Rabatt |
| Rabatt | Wert | 15,00 |
| Zeitplan | Startdatum | 1. Juni 2026 |
| Zeitplan | Enddatum | (leer — keine Ablaufdatum) |
| Produkte | Anwenden auf | Kollektionen |
| Produkte | Ausgewählt | Summer Essentials |

> **Hinweis:** Der 15 $ Rabatt gilt für jedes qualifizierende Produkt einzeln. Ein Produkt im Wert von 50 $ wird 35 $, ein Produkt im Wert von 30 $ wird 15 $. Das Feld Enddatum leer zu lassen bedeutet, dass die Promotion unbegrenzt läuft, bis Sie sie manuell deaktivieren.

## Beispiel: Fixer Verkaufspreis für Ausverkauf

**Szenario:** Alle Ausverkaufsartikel auf 9,99 $ setzen.

| Schritt | Feld | Wert |
|---------|------|------|
| Basics | Name | Finaler Ausverkauf — Alles zu 9,99 $ |
| Basics | Aktiv | Angekreuzt |
| Rabatt | Typ | Fixer Verkaufspreis |
| Rabatt | Wert | 9,99 |
| Zeitplan | Startdatum | (heute) |
| Produkte | Anwenden auf | Kollektionen |
| Produkte | Ausgewählt | Finaler Ausverkauf |

> **Hinweis:** Fixer Verkaufspreis legt den genauen Verkaufspreis fest, unabhängig vom ursprünglichen Preis. Ein Artikel im Wert von 75 $ und ein Artikel im Wert von 25 $ werden beide 9,99 $. Verwenden Sie dies für Ausverkaufsregale oder einheitliche Preise, bei denen Sie alle Artikel auf denselben Preispunkt setzen möchten.

![Kategorie Promotion](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Die richtige Rabattart auswählen

| Typ | Wie es funktioniert | Bestens geeignet für | Beispiel |
|-----|------------------|---------------------|--------|
| **Prozentualer Rabatt** | Reduziert den Preis um einen Prozentsatz | Breite Verkäufe, bei denen die Produkte unterschiedliche Preise haben | 20 % Rabatt — 100 $ wird 80 $, 50 $ wird 40 $ |
| **Betrag Rabatt** | Subtrahiert einen festen Geldbetrag | Promotionen mit einer spezifischen Geldsparmeldung | 15 $ Rabatt — 100 $ wird 85 $, 50 $ wird 35 $ |
| **Fixer Verkaufspreis** | Legt den genauen Verkaufspreis fest | Ausverkauf, einheitliche Preise, "Alles zu X $" | 9,99 $ — alle Artikel werden zu 9,99 $, unabhängig vom ursprünglichen Preis |

## Die richtige Zielgruppe auswählen

| Zielgruppe | Wie es funktioniert | Bestens geeignet für |
|-----------|------------------|---------------------|
| **Alle Produkte** | Wird auf jedes Produkt im Geschäft angewendet | Sitewide-Verkäufe, Geschäftsevents |
| **Kategorien** | Wird auf alle Produkte in den ausgewählten Kategorien angewendet | Abteilungsverkäufe, Saison-Ausverkauf nach Typ |
| **Marken** | Wird auf alle Produkte aus den ausgewählten Marken angewendet | Markenpartnerschaften, markenspezifische Events |
| **Kollektionen** | Wird auf alle Produkte in den ausgewählten Kollektionen angewendet | Kurationale Promotionen, thematische Verkäufe |
| **Produkte** | Wird auf individuell ausgewählte Produkte angewendet | Handverlesene Angebote, begrenzte Auswahl |

## Zeitplanungsmuster

Drei gängige Muster zur Einrichtung von Promotion-Zeitplänen:

| Muster | Startdatum | Enddatum | Anwendungsfälle |
|--------|-----------|----------|--------------|
| **Sofort, laufend** | Heute | (leer) | Dauerhafte Preisreduzierung, langfristige Verkäufe |
| **Datumsumfang** | Zukünftiges Datum | Zukünftiges Datum | Saisonale Events, Feiertagsverkäufe |
| **Zukünftiger Start, kein Enddatum** | Zukünftiges Datum | (leer) | Neue dauerhafte Preise, die an einem bestimmten Datum beginnen |

Ein Startdatum in der Zukunft erstellt eine geplante Promotion. Sie wird im **Geplant**-Tab auf dem Promotion-Dashboard angezeigt und aktiviert sich automatisch, wenn das Datum erreicht ist. Das Feld Enddatum leer zu lassen bedeutet, dass die Promotion aktiv bleibt, bis Sie sie manuell deaktivieren.

## Tipps

- **Verwenden Sie beschreibende Namen** — Geben Sie den Rabattwert und das Ziel in den Namen ein (z. B. "Sommer 20 % Rabatt auf Schuhe"), damit Sie Promotionen auf dem Dashboard schnell erkennen können.
- **Überprüfen Sie die Anzahl der betroffenen Produkte** — Der Schritt "Überprüfen" zeigt an, wie viele Produkte rabattiert werden. Wenn die Zahl falsch erscheint, kehren Sie zurück und überprüfen Sie Ihre Zielgruppen.
- **Beginnen Sie klein** — Wenn Sie sich unsicher sind, beginnen Sie mit einem kleineren Rabatt und erhöhen Sie ihn, wenn nötig.
- **Verwenden Sie Betrag Rabatt für Marketing** — "15 $ Rabatt" ist eine konkrete Einsparung, die sich leicht in Werbeanzeigen und E-Mail-Kampagnen kommunizieren lässt.
- **Verwenden Sie Prozentualen Rabatt für Fairness** — Ein prozentualer Rabatt passt sich dem Preis an und bietet proportionale Einsparungen bei verschiedenen Preisniveaus.