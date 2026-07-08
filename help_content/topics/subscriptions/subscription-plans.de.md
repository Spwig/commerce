---
title: Abonnement-Pläne
---

Abonnement-Pläne ermöglichen es Ihnen, wiederkehrende Zahlungen für Ihre Produkte anzubieten – ideal für Verbraucherprodukte, Dienstleistungen, kurierte Boxen oder jedes Produkt, das Kunden wiederholt kaufen. Dieser Leitfaden erklärt, wie Sie Pläne erstellen und konfigurieren, Preisstufen einrichten, Testphasen hinzufügen und optionaler Zusatzoptionen beifügen können.

## Getting started

Navigieren Sie zu **Abonnements > Abonnement-Pläne** in der Admin-Seitenleiste. Die Planliste zeigt alle Ihre Pläne mit ihrem Preismodell, der Anzahl aktiver Abonnenten und dem Sichtbarkeitsstatus an.

Um einen neuen Plan zu erstellen, klicken Sie auf die Schaltfläche **+ Abonnement-Plan hinzufügen** – dies öffnet den Plan-Erstellungs-Assistenten, der Sie Schritt für Schritt durch die Einrichtung führt.

![Subscription plans list](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Plan information

Der erste Abschnitt erfasst die Kernidentität Ihres Plans.

- **Plan Name** — Der Name, den Kunden beim Abonnieren sehen. Klicken Sie auf das Globus-Symbol, um Übersetzungen für andere Laden-Sprachen hinzuzufügen.
- **Slug** — Ein URL-freundlicher Bezeichner, der automatisch aus dem Namen generiert wird (z. B. `premium-plan`). Dies wird intern und in Integrationen verwendet.
- **Description** — Optionaler Text, der beschreibt, was der Plan enthält. Unterstützt Übersetzungen.

## Pricing model

Wählen Sie aus, wie der Preis für diesen Plan strukturiert wird:

| Pricing Model | Best For |
|---------------|----------|
| **Tiered Pricing** | Angebot von monatlichen, quartalsweisen und jährlichen Verpflichtungszeiträumen mit Rabatten für längere Zeiträume |
| **Quantity-Based** | Preis pro Sitzplatz oder pro Nutzer, bei dem der Gesamtpreis mit der Anzahl skaliert (z. B. Team-Lizenzen) |
| **Flat Rate** | Ein fester Preis ohne Variationen |

Für **Quantity-Based**-Pläne legen Sie die **Mindestanzahl** (mindestens erforderliche Sitzplätze) fest und optional eine **Maximalanzahl**, um festzulegen, wie viele Sitzplätze ein Abonnent kaufen kann.

## Pricing tiers

Preisstufen definieren die Abrechnungshäufigkeit und die Rabattoptionen, die Kunden für diesen Plan haben. Fügen Sie sie im Abschnitt **Pricing Tiers** unter dem Hauptformular hinzu.

Jede Stufe hat diese Felder:

- **Tier Name** — Die Bezeichnung, die Kunden sehen (z. B. `Monthly`, `Annual — Save 20%`). Unterstützt Übersetzungen.
- **Billing Cycle** — Wie oft der Kunde abgerechnet wird: Täglich, Wöchentlich, Monatlich, Quartalsweise, Halbjährlich oder Jahresweise.
- **Billing Interval** — Der Multiplikator für den Abrechnungszyklus. Setzen Sie auf `2` mit Monatlich, um alle 2 Monate abzurechnen.
- **Discount Percentage** — Der Rabatt, der auf den Produktpreis für diese Stufe angewendet wird. Setzen Sie auf `0`, um den vollen Preis zu berechnen, oder auf `20`, um 20 % Rabatt zu gewähren. Dieser Rabatt wird auf alle Verkaufspreise des Produkts selbst叠加.
- **Default Tier** — Markieren Sie eine Stufe als Standard, um sie automatisch für Kunden auszuwählen, wenn sie die Abonnementoptionen ansehen.

### Beispiel: tiered plan with three options

Für einen „Coffee Club“-Abonnement-Plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Trial period

Eine Testphase ermöglicht es Kunden, Ihr Abonnement vor der ersten vollständigen Zahlung zu testen. Konfigurieren Sie dies im Abschnitt **Trial Period**:

- **Trial Period (Days)** — Anzahl der kostenlosen Testtage. Setzen Sie auf `0`, um Testphasen zu deaktivieren. Maximale Anzahl ist 365 Tage.
- **Trial Price** — Optionaler reduzierter Preis während der Testphase (z. B. $1 für den ersten Monat). Leer lassen, um eine vollständig kostenlose Testphase anzubieten.

## Cancellation policy

Steuern Sie im Abschnitt **Cancellation Policy**, wie Kunden ihr Abonnement kündigen können:

| Policy | Description |
|--------|-------------|
| **Cancel Anytime** | Kunden können das Abonnement jederzeit sofort kündigen |
| **Cancel at Period End** | Die Kündigung tritt am Ende des bezahlten Zeitraums in Kraft – Kunden behalten den Zugriff bis zum Ablauf |
| **Minimum Commitment Required** | Kunden müssen eine Mindestanzahl an Abrechnungszyklen absolvieren, bevor sie das Abonnement kündigen können |

Additional settings:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **Mindestverpflichtung (Zyklen)** — Bei Verwendung der Verpflichtungspolitik legen Sie die erforderliche Anzahl von Abrechnungszyklen fest (z. B. `3` für eine Mindestverpflichtung von 3 Monaten).
- **Gnadenfrist (Tage)** — Tage der weiteren Zugriffsberechtigung nach einem Zahlungsausfall, bevor die Abonnement sperriert wird.

Auf `0` setzen, um eine sofortige Sperrung vorzunehmen.
- **Wiederherstellungsfrist (Tage)** — Tage nach der Kündigung, während denen ein Kunde sein Abonnement ohne erneutes Abonnieren von Grund auf wieder aktivieren kann.

## Verhaltensweisen bei Planwechseln

Wenn Kunden zwischen Plänen aufwärts oder abwärts wechseln, können Sie steuern, wann der Wechsel wirksam wird:

- **Aufwärtsverhalten** — Wählen Sie **Sofort** (Gutschrift des anteiligen Betrags jetzt) oder **Bei Erneuerung** (Wechsel am nächsten Abrechnungstermin).
- **Abwärtsverhalten** — Wählen Sie **Sofort** (Gutschrift auf die nächste Rechnung) oder **Bei Erneuerung** (Wechsel am nächsten Abrechnungstermin).

## Grenzen und Einschränkungen

- **Maximale Abrechnungszyklen** — Die Gesamtzahl der Abrechnungszyklen, bevor das Abonnement automatisch endet. Leer lassen, um unbeschränkte wiederkehrende Abrechnungen zu ermöglichen. Nützlich für Ratenzahlungspläne oder zeitlich begrenzte Abonnements.
- **Einrichtungsgebühr** — Ein Einmalbetrag, der beim Erstellen des Abonnements erhoben wird (z. B. Onboarding- oder Aktivierungsgebühr). Auf `0,00` setzen, um keine Einrichtungsgebühr zu erheben.

## Plan-Add-ons

Add-ons sind optionale Zusatzleistungen, die Abonnenten an ihren Plan anhängen können. Fügen Sie sie in dem Abschnitt **Plan-Add-ons** hinzu:

- **Add-on-Name** — Der Name, der Kunden angezeigt wird. Unterstützt Übersetzungen.
- **Beschreibung** — Was das Add-on bietet.
- **Preis** — Kosten des Add-ons.
- **Abrechnungshäufigkeit** — Ob das Add-on **Pro Abrechnungszyklus** (wiederkehrend) oder **Einmalig** bei Beginn des Abonnements berechnet wird.
- **Menge erlauben** — Aktivieren Sie dies, um Kunden zu ermöglichen, mehrere Einheiten des Add-ons zu erwerben.
- **Erforderlich** — Aktivieren Sie dies, um das Add-on automatisch auf allen neuen Abonnements einzuschließen. Erforderliche Add-ons können von Kunden nicht entfernt werden.

## Sichtbarkeit und Status

- **Aktiv** — Deaktivieren Sie dies, um einen Plan zu deaktivieren, sodass keine neuen Abonnements erstellt werden können. Bestehende Abonnements werden nicht beeinflusst.
- **Öffentlich** — Deaktivieren Sie dies, um den Plan von Kundenfreiflächen zu verbergen (nützlich für interne oder veraltete Pläne, auf denen bestehende Abonnenten weiterhin bleiben).
- **Sortierreihenfolge** — Steuert die Anzeigereihenfolge auf den Abonnementauswahlseiten. Niedrigere Zahlen werden zuerst angezeigt.

## Tipps

- Nutzen Sie eine **Testphase**, um Hesitation zu reduzieren — selbst eine kurze 7-tägige kostenlose Testphase kann die Umwandlungsrate bei Abonnementprodukten erheblich verbessern.
- Richten Sie **drei Preistiere** (monatlich, vierteljährlich, jährlich) mit zunehmenden Rabatten ein, um jährliche Verpflichtungen zu fördern und Ihre Liquidität zu verbessern.
- Bei abonnementbasierten Dienstleistungen setzen Sie die **Kündigungsrichtlinie** auf **Bei Ende des Zeitraums kündigen**, damit Kunden Zugriff bis zu ihrem bezahlten Zeitraum behalten — dies fühlt sich fair an und reduziert Rücklastungen.
- Halten Sie die **Gnadenfrist** auf 3–7 Tage bei Zahlungsausfällen. Dies gibt Kunden Zeit, ihre Zahlungsmethode zu aktualisieren, bevor sie den Zugriff verlieren.
- Nutzen Sie die **Erforderlichkeit**-Flagge bei Add-ons sparsam — verwenden Sie sie nur für Dinge, die tatsächlich obligatorisch sind (z. B. einen Dienstvertrag), nicht als Mittel, um Preise zu erhöhen.
- Deaktivieren Sie Pläne ohne Abonnenten, anstatt sie zu löschen — dies bewahrt historische Daten für Kunden, die früher abonniert haben.