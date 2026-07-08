---
title: Gutscheineinschränkungen
---

Gutscheineinschränkungen steuern, wer einen Gutschein verwenden kann, wann und wie oft. Konfigurieren Sie diese Einstellungen, wenn Sie einen Gutschein erstellen oder bearbeiten, unter **Marketing > Gutscheine**.

![Einschränkungsregeln](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Nutzungsgrenzen

Legen Sie globale und pro-Kunde-Grenzen in dem Abschnitt **Nutzungsgrenzen** des Gutscheins formulare fest.

- **Maximale Nutzung insgesamt** — Die maximale Anzahl, wie oft dieser Gutschein von allen Kunden eingelöst werden kann. Leer lassen, um unbegrenzt zu machen.
- **Maximale Nutzung pro Kunde** — Wie oft ein einzelner Kunde diesen Gutschein verwenden kann. Auf 1 setzen für die meisten Kampagnen.

| Muster | Maximale Gesamt | Pro Kunde | Verwendungsfall |
|---------|-----------|--------------|----------|
| Begrenzte Kampagne | 100 | 1 | "Erste 100 Kunden" Knappheit |
| Unbegrenzter geteilter Code | (leer) | 1 | Laufende Marketingcodes |
| Unbegrenzter Mehrfachverwendung | (leer) | (leer) | Interner/Staff-Abzug |
| Einmaliger eindeutiger Code | 1 | 1 | Massengenerierte Kampagnencodes |

## Mindestbestellwert

Das Feld **Mindestbestellwert** schützt Ihre Gewinne, indem es einen Warenkorb-Gesamtwert erfordert, bevor der Gutschein gilt. Zum Beispiel, "10 $ Rabatt auf Bestellungen über 50 $" stellt sicher, dass Sie niemals eine kleine Bestellung in eine unprofitable umwandeln.

| Rabatt | Empfohlener Mindestwert | Verhältnis |
|----------|-------------------|-------|
| 5 $ Rabatt | 30 $+ | ~6:1 |
| 10 $ Rabatt | 50 $+ | ~5:1 |
| 20 $ Rabatt | 100 $+ | ~5:1 |
| 15 % Rabatt | 40 $+ | Abhängig vom Katalog |

## Rabattgrenze (Maximaler Rabattbetrag)

Das Feld **Maximaler Rabattbetrag** in **Rabattkonfiguration** begrenzt, wie viel ein prozentualer Gutschein abziehen kann. Dies gilt nur für prozentuale Gutscheine und verhindert, dass Rabatte auf teure Warenkörbe ausufallen.

Beispiel: "20 % Rabatt, maximal 50 $ Rabatt"
- 200 $ Warenkorb = 40 $ Rabatt (20 %)
- 300 $ Warenkorb = 50 $ Rabatt (begrenzt)
- 1000 $ Warenkorb = immer noch 50 $ Rabatt (begrenzt)

Fügen Sie eine Rabattgrenze auf jeden prozentualen Gutschein hinzu, den Sie öffentlich teilen.

## Kombinationsregeln

Das Feld **Einschränkungen & Regeln** (klicken Sie, um auszuklappen) enthält Häkchenfelder, die steuern, wie Gutscheine mit anderen Rabatten interagieren.

| Einstellung | Was es tut | Wann aktivieren |
|---------|--------------|----------------|
| **Verkaufsartikel ausschließen** | Gutschein überspringt Produkte, die bereits im Verkauf sind | Für die meisten Kampagnen — schützt Verkaufsgewinne |
| **Kann nicht mit anderen Gutscheinen kombiniert werden** | Nur ein Gutschein pro Bestellung | Standard für die meisten Gutscheine |
| **Kann nicht mit Verkaufsartikeln kombiniert werden** | Blockiert Gutschein, wenn der Warenkorb JEGLICH Verkaufsartikel enthält | Strengere Kampagnen, bei denen der Gutschein den Verkaufspreis ersetzt |
| **Nur für Neukunden** | Nur Kunden mit null vorherigen Bestellungen | Willkommens-/Akquiskationskampagnen |

## Kundeneinschränkungen

Für einfache Zielgruppen, aktivieren Sie **Nur für Neukunden** im Feld **Einschränkungen & Regeln**.

Für erweiterte Zielgruppen, verwenden Sie die **Gutscheineinschränkungen** Tabelle am unteren Ende des Formulars. Klicken Sie auf **+ Fügen Sie eine weitere Gutscheineinschränkung hinzu**, um Zeilen hinzuzufügen. Jede Einschränkung hat drei Felder:

- **Typ** — Die Einschränkungskategorie (Dropdown-Liste)
- **Wert** — Der passende Wert (Komma-getrennt oder JSON)
- **Inklusiv** — Angekreuzt = Kunde muss übereinstimmen; nicht angekreuzt = Kunde muss NICHT übereinstimmen

| Typ | Wert | Inklusiv | Effekt |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Ja | Nur Mitarbeiter von company.com können ihn verwenden |
| shipping_country | US,CA | Ja | Nur Kunden aus den USA und Kanada |
| shipping_country | RU | Nein | Alle außer Russland |
| day_of_week | monday,tuesday | Ja | Nur gültig am Montag und Dienstag |
| payment_method | stripe | Ja | Nur für Stripe-Zahlungen |

Kombinieren Sie mehrere Zeilen für mehrschichtige Einschränkungen. Alle inklusiven Einschränkungen müssen übereinstimmen, und keine exklusiven Einschränkungen dürfen übereinstimmen, damit der Gutschein gilt.

## Ablaufstrategien

Steuern Sie, wann ein Gutschein abläuft, mithilfe der Datums- und Gültigkeitsfelder.

- **Enddatum** — Ein harter Abschlussdatum (z. B. 31.12.2026).

Der Gutschein funktioniert nicht mehr um Mitternacht.
- **Tage gültig** — Laufende Gültigkeit ab dem Erstellungs- oder ersten Verwendungsdatum des Gutscheins.

Überschreibt das Enddatum, wenn festgelegt.


Nützlich für Willkommenscodes: "gültig 30 Tage nach Erhalt".

| Strategie | Enddatum | Gültigkeitsdauer | Anwendungsfälle |
|----------|----------|------------|----------|
| Fester Endtermin | Festlegen | (leer) | Saisonale Kampagnen, Veranstaltungen |
| Laufender Zeitraum | (leer) | 30 | Willkommenscodes, Belohnungsgutscheine |
| Kein Ablaufdatum | (leer) | (leer) | Laufende Codes, Mitarbeiter-Rabatte |

## Missbrauch verhindern

Folgen Sie dieser Checkliste, um Ihre Gutscheine sicher zu halten:

- Legen Sie immer **Maximale Nutzung pro Kunde** auf 1 fest, es sei denn, es gibt einen spezifischen Grund, dies nicht zu tun.
- Legen Sie **Mindestbestellwert** für alle festen Betragsgutscheine fest.
- Fügen Sie einen **Maximalen Rabattbetrag** für öffentliche Prozentgutscheine hinzu.
- Verwenden Sie schwer zu erratende Codes für hochwertige Gutscheine – vermeiden Sie offensichtliche Codes wie "DISCOUNT50".
- Überwachen Sie die Nutzungsanalytik auf jeder Gutschein-Karte im Dashboard.
- Deaktivieren Sie einen Gutschein sofort, wenn Sie ungewöhnliche Auszahlungsmuster erkennen.
- Für hochwertige Kampagnen verwenden Sie stattdessen Bulk-generierte eindeutige Codes anstelle eines einzelnen gemeinsamen Codes.

## Tipps

- Beginnen Sie restriktiv und lockern Sie die Grenzen, wenn die Auszahlung zu niedrig ist – es ist einfacher, Regeln zu lockern, als sie nach der Verbreitung der Codes zu verschärfen.
- Testen Sie jeden Gutschein mit einem echten Checkout, bevor Sie ihn Kunden verteilen.
- Prüfen Sie das Gutschein-Analytik-Dashboard regelmäßig, um Probleme frühzeitig zu erkennen.
- Kombinieren Sie mehrere Einschränkungen für eine mehrschichtige Sicherheit – beispielsweise Nutzungsgrenze pro Kunde + Mindestbestellwert + Rabattgrenze + Verkaufsartikel ausschließen.