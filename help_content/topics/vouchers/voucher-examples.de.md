---
title: Gutscheinbeispiele
---

Dieser Leitfaden bietet konkrete, Feld für Feld Beispiele für die häufigsten Gutscheintypen. Jedes Beispiel zeigt genau ein, was Sie eingeben müssen, wenn Sie einen Gutschein unter **Marketing > Gutscheine** → **+ Gutschein hinzufügen** erstellen.

![Gutschein Karte](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Beispiel 1: Prozentsatz Rabatt mit Obergrenze

**Szenario:** Bieten Sie 20 % Rabatt auf den gesamten Warenkorb an, aber begrenzen Sie den Rabatt auf 50 $, um hohe Bestellungen profitabel zu halten. Kein Ablaufdatum.

| Feld | Wert |
|-------|-------|
| Code | `SAVE20` |
| Name | 20 % Rabatt — Max 50 $ |
| Rabatttyp | Prozentsatz |
| Rabattwert | 20 |
| Maximaler Rabattbetrag | 50 |
| Anwendungsbereich | Gesamter Warenkorb |
| Maximale Gesamtverwendung | *(leer — unbegrenzt)* |
| Maximale Verwendung pro Kunde | 1 |
| Mindestbestellwert | *(leer — kein Minimum)* |

**Wie die Obergrenze funktioniert:** Bei einer Bestellung von 200 $ beträgt der Rabatt 40 $. Bei einer Bestellung von 300 $ wäre der Rabatt 60 $, aber die Obergrenze begrenzt ihn auf 50 $. Bei einer Bestellung von 500 $ beträgt der Rabatt immer noch 50 $. Dies ermöglicht es Ihnen, eine großzügig klingende Promotion anzubieten, während der tatsächliche Rabatt vorhersehbar bleibt.

## Beispiel 2: Fixer Betrag Rabatt mit Minimum

**Szenario:** Geben Sie Kunden 10 $ Rabatt auf jede Bestellung über 75 $, um größere Warenkörbe zu fördern.

| Feld | Wert |
|-------|-------|
| Code | `TAKE10` |
| Name | 10 $ Rabatt auf Bestellungen über 75 $ |
| Rabatttyp | Fixer Betrag |
| Rabattwert | 10 |
| Anwendungsbereich | Gesamter Warenkorb |
| Mindestbestellwert | 75 |
| Maximale Verwendung pro Kunde | 0 *(unbegrenzt)* |
| Enddatum | *(leer — kein Ablauf)* |

> **Hinweis:** Die Festlegung eines Mindestbestellwerts schützt Ihre Gewinne. Ohne dies könnte ein Kunde diesen Code auf eine 12 $ Bestellung anwenden und Ihren Gewinn eliminieren. Kombinieren Sie immer fixe Beträge Gutscheine mit einem sinnvollen Minimum.

## Beispiel 3: Kostenlose Lieferung

**Szenario:** Bieten Sie kostenlose Lieferung für jede Bestellung ohne Mindestbestellwert an.

| Feld | Wert |
|-------|-------|
| Code | `FREESHIP` |
| Name | Kostenlose Lieferung |
| Rabatttyp | Kostenlose Lieferung |
| Anwendungsbereich | Gesamter Warenkorb |
| Maximale Gesamtverwendung | *(leer — unbegrenzt)* |
| Maximale Verwendung pro Kunde | 1 |
| Mindestbestellwert | *(leer — kein Minimum)* |

> **Hinweis:** Wählen Sie den **kostenlosen Lieferung** Rabatttyp, der die Lieferkosten automatisch aus der Bestellung entfernt. Dies ist der sauberste Ansatz und funktioniert unabhängig davon, welche Liefermethode der Kunde auswählt.

## Beispiel 4: Willkommenscode für Neukunden

**Szenario:** Geben Sie neuen Kunden 15 % Rabatt auf ihre erste Bestellung, um die Umwandlung zu fördern.

| Feld | Wert |
|-------|-------|
| Code | `WELCOME15` |
| Name | Willkommen — 15 % Rabatt auf erste Bestellung |
| Rabatttyp | Prozentsatz |
| Rabattwert | 15 |
| Anwendungsbereich | Gesamter Warenkorb |
| Maximale Verwendung pro Kunde | 1 |
| Nur für Neukunden | Angekreuzt |

Das System validiert den Neukundenzustand, indem es überprüft, ob der Kunde bereits frühere abgeschlossene Bestellungen hat. Wenn ein Kunde mit Bestellhistorie versucht, diesen Code anzuwenden, sieht er eine klare Fehlermeldung zur Kasse.

## Beispiel 5: Produkt-spezifischer Gutschein

**Szenario:** Bieten Sie 5 $ Rabatt auf ausgewählte Produkte — beispielsweise, um langsam verkaufte Artikel zu bewegen.

| Feld | Wert |
|-------|-------|
| Code | `PICK5` |
| Name | 5 $ Rabatt auf ausgewählte Artikel |
| Rabatttyp | Fixer Betrag |
| Rabattwert | 5 |
| Anwendungsbereich | Spezifische Produkte |
| Elegible Produkte | *(wählen Sie die Zielprodukte aus)* |
| Maximale Verwendung pro Kunde | 1 |

> **Hinweis:** Verwenden Sie den Produktbereich, wenn Sie einzelne SKU's abzüglich machen möchten. Verwenden Sie den Kategoriebereich (nächstes Beispiel), wenn Sie alles in einem Bereich abzüglich machen möchten. Der Produktbereich gibt Ihnen präzise Kontrolle; der Kategoriebereich ist einfacher zu verwalten, wenn sich Ihr Katalog häufig ändert.

## Beispiel 6: Kategorie-Gutschein

**Szenario:** Führen Sie eine 25 % Rabatt-Aktion für alle Artikel in der Elektronik-Kategorie durch.

| Feld | Wert |
|-------|-------|
| Code | `ELEC25` |
| Name | 25 % Rabatt auf Elektronik |
| Rabatttyp | Prozentsatz |
| Rabattwert | 25 |
| Anwendungsbereich | Spezifische Kategorien |
| Elegible Kategorien | Elektronik |
| Maximale Gesamtverwendung | *(leer — unbegrenzt)* |
| Maximale Verwendung pro Kunde | 1 |


Wenn der Rabatt einer Kategorie zugeordnet ist, gilt er nur für qualifizierende Artikel im Warenkorb.

Nicht-Elektronik-Artikel werden zum vollen Preis berechnet.

## Vergleich der Rabatttypen

| Typ | Wie es funktioniert | Bestes für | Beispiel |
|------|-------------|----------|---------|
| **Prozentual** | Deduziert einen Prozentsatz des qualifizierten Gesamtbetrags | Skalierbare Rabatte, die mit der Bestellgröße wachsen | 20 % Rabatt auf den gesamten Warenkorb |
| **Fixer Betrag** | Deduziert einen festen Geldbetrag | Einfache, vorhersehbare Promotionen | 10 $ Rabatt auf Bestellungen über 75 $ |
| **Kostenloser Versand** | Entfernt die Versandkosten aus der Bestellung | Reduzierung der Abbruchquote beim Checkout | Kostenloser Versand, ohne Mindestbestellwert |

## Vergleich der Scopes

| Scope | Wie es funktioniert | Bestes für |
|-------|-------------|----------|
| **Ganzer Warenkorb** | Der Rabatt gilt für den gesamten Bestellbetrag | Gesamtstore-Rabatte und Willkommenscodes |
| **Spezifische Produkte** | Der Rabatt gilt nur für ausgewählte Produkte im Warenkorb | Aufräumen von spezifischem Lager oder Spotlight-Angebote |
| **Spezifische Kategorien** | Der Rabatt gilt nur für Artikel in ausgewählten Kategorien | Verkaufsaktionen für Abteilungen und saisonale Promotionen |

## Tipps

- **Verwende merkenswerte Codes** — `SUMMER20` ist besser als `COUPONX1600406498`. Speichere automatisch generierte Codes für Bulk-Kampagnen.
- **Teste vor der Verteilung** — Platziere eine Testbestellung mit dem Gutscheincode, um sicherzustellen, dass er korrekt angewendet wird und alle Grenzen respektiert.
- **Überwache die Nutzung** — Überprüfe die Redemptions-Zahl auf jedem Gutschein-Karte, um die Kampagnenleistung in Echtzeit zu verfolgen.
- **Kombiniere mit der Announcement-Bar** — Werbe deinen Gutscheincode in einer site-weiten Announcement, damit Kunden ihn sehen, bevor sie mit dem Einkaufen beginnen.