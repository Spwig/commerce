---
title: Abo-Pläne
---

Abo-Pläne ermöglichen es Ihnen, wiederkehrende Abrechnungen für Ihre Produkte anzubieten — ideal für Verbrauchsmaterialien, Dienstleistungen, kuratierte Boxen oder jedes Produkt, das Kunden häufig kaufen. Dieser Leitfaden erklärt, wie Sie Pläne erstellen und konfigurieren, Preistarife einrichten, Probephase hinzufügen und optionale Zusatzfunktionen anhängen.

## Einstieg

Gehen Sie zu **Abonnements > Abo-Pläne** im Admin-Seitenleistenmenü. Die Liste der Pläne zeigt alle Ihre Pläne mit ihrem Preismodell, der Anzahl der aktiven Abonnenten und dem Sichtbarkeitsstatus an.

![Liste der Abo-Pläne](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Um einen neuen Plan zu erstellen, klicken Sie auf die Schaltfläche **Mit Assistenten erstellen** — dies öffnet den Plan-Assistenten, der Sie Schritt für Schritt durch die Einrichtung führt. Die Schaltfläche **+ Plan hinzufügen** neben ihr öffnet ein leeres Formular für Händler, die lieber alles manuell konfigurieren möchten.

Ein Plan allein ist nicht käuflich — er ist ein Vorlage. Sobald Sie ihn hier erstellt haben, hängen Sie ihn an ein oder mehrere Produkte aus dem **Abonnements**-Tab des Produkts (nur für einfache, variable und digitale Produkte), damit Kunden sich tatsächlich abonnieren können. Siehe [Produkte als Abonnements verkaufen](/help/selling-products-as-subscriptions) für diesen Schritt.

## Der Plan-Editor

Das Öffnen eines vorhandenen Plans (klicken Sie auf dessen Namen oder das Bleistift-Symbol aus der Liste) führt Sie zum Plan-Editor. Die Kopfzeile zeigt den Plan-Namen, sein Preismodell, die Status-Schaltflächen **Aktiv**/**Inaktiv** und **Öffentlich**/**Privat**, sowie das Erstellungsdatum. Die beiden Schaltflächen in der oberen rechten Ecke der Kopfzeile speichern Ihre Änderungen — das Kreis-Symbol mit dem Haken speichert und kehrt zur Liste zurück, das einfache Kreis-Symbol mit dem Haken speichert und lässt Sie auf der Seite, damit Sie weiter bearbeiten können.

Unter der Kopfzeile ist eine Statistik-Streifen, die den Plan im Überblick zusammenfasst: **Aktive Abonnements**, **Preistarifen**, **Zusatzfunktionen** und **Gesamteinnahmen**.

Der Rest des Formulars ist in fünf Tabs organisiert:

| Tab | Was es enthält |
|-----|-----------------|
| **Allgemein** | Plan-Informationen (Name, Slug, Beschreibung) und Status (aktiv/öffentlich) |
| **Preisgestaltung** | Preiskonfiguration, Probephase und Grenzen & Einschränkungen |
| **Stufenpreis & Zusatzfunktionen** | Die Preistarifen- und Zusatzfunktionen-Editor |
| **Lebenszyklus** | Stornierungsbedingungen und Plan-Änderungsverhalten |
| **Erweitert** | Anbieter-Integration und Statistiken |

Die Abschnitte darunter durchlaufen die Einstellungen jedes Tab. Wenn Sie einen brandneuen Plan direkt aus **+ Plan hinzufügen** (anstelle des Assistenten) erstellen, erscheinen dieselben Felder in einem einzigen scrollbaren Formular anstelle von Tabs — speichern Sie den Plan einmal und öffnen Sie ihn erneut, um den vollständigen Tab-Editor zu erhalten.

## Plan-Informationen (Allgemeiner Tab)

Der **Plan-Informationen**-Bereich fasst die Kernidentität Ihres Plans zusammen.

- **Plan-Name** — Der Name, den Kunden beim Abonnieren sehen. Klicken Sie auf das Globus-Symbol, um Übersetzungen für andere Store-Sprachen hinzuzufügen.
- **Slug** — Ein URL-freundlicher Bezeichner, der automatisch aus dem Namen generiert wird (z. B. `premium-plan`). Dies wird intern und in Integrationen verwendet.
- **Beschreibung** — Optionaler Text, der beschreibt, was der Plan enthält. Unterstützt Übersetzungen.

Der **Status**-Bereich auf demselben Tab steuert die Schalter **Aktiv** und **Öffentlich** — siehe [Sichtbarkeit und Status](#visibility-and-status) unten.

![Allgemeiner Tab des Plan-Editors](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Preismodell (Preisgestaltungs-Tab)

Der **Preisgestaltungs-Karte** steuert, wie die Preise für diesen Plan strukturiert sind:

| Preismodell | Am besten für |
|---------------|----------------|
| **Stufenpreis** | Angebot von monatlichen, quartalsweisen und jährlichen Verpflichtungsoptionen mit Rabatten für längere Laufzeiten |
| **Mengenbasiert** | Pro-Sitz- oder pro-Benutzer-Preisgestaltung, bei der sich der Gesamtpreis mit der Menge verändert (z. B. Team-Lizenzen) |
| **Fester Preis** | Ein einziger fester Preis ohne Variationen |

Für **Mengenbasierte** Pläne, prüfen Sie **Menge erlauben** und setzen Sie die **Mindestmenge** (mindestens erforderliche Sitzplätze) und optional eine **Maximalmenge**, um die Anzahl der Sitzplätze, die ein Abonnent erwerben kann, zu begrenzen.

[![](https://d35p197z48916e.cloudfront.net/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Preistarife (Registerkarte "Ebenen & Zusatzleistungen")

Preistarife definieren die Zahlungshäufigkeit und Rabattoptionen, die Kunden für diesen Plan erhalten können. Fügen Sie sie im **Preistarif-Karte** auf der **Ebenen & Zusatzleistungen**-Registerkarte zusammen mit dem **Zusatzleistungen-Editor** hinzu.

Jeder Tarif hat diese Felder:

- **Tarifname** — Die Bezeichnung, die den Kunden angezeigt wird (z. B. `Monatlich`, `Jährlich - 20% sparen`). Wird unterstützt.
- **Abrechnungszyklus** — Wie oft der Kunde abgerechnet wird: Täglich, Wöchentlich, Monatlich, Quartalsweise, Halbjährlich oder Jährlich.
- **Abrechnungsintervall** — Der Multiplikator für den Abrechnungszyklus. Auf `2` setzen, um alle 2 Monate abzurechnen.
- **Rabattprozentsatz** — Der Rabatt, der auf den Produktpreis für diesen Tarif angewandt wird. Auf `0` setzen, um den Vollpreis zu erhalten, oder auf `20`, um 20 % Rabatt zu gewähren. Dieser Rabatt wird zusätzlich zu jedem Verkaufspreis des Produkts selbst angewandt.
- **Standardtarif** — Markieren Sie einen Tarif als Standard, um ihn für Kunden vorzuselektieren, wenn sie die Abonnementoptionen ansehen.

Der Rabatt gilt ab dem ersten Abrechnungszyklus des Kunden, nicht nur bei Verlängerungen — ein Tarif mit 20 % Rabatt berechnet 20 % Rabatt ab dem ersten Tag (oder vom ersten Abrechnungsvorgang nach einem Testzeitraum, falls der Plan einen hat).

### Beispiel: einstufiger Plan mit drei Optionen

Für einen "Kaffee-Club"-Abonnementplan:

| Tarifname | Abrechnungszyklus | Rabatt |
|-----------|-------------------|--------|
| Monatlich | Monatlich | 0% |
| Quartalsweise - 10% sparen | Quartalsweise | 10% |
| Jährlich - 20% sparen | Jährlich | 20% |

## Abonnement-Zusatzleistungen (Registerkarte "Ebenen & Zusatzleistungen")

Zusatzleistungen sind optionale Extras, die Abonnenten an ihren Plan anhängen können. Fügen Sie sie in der **Zusatzleistungen-Karte** direkt unter den Preistarifen auf derselben Registerkarte hinzu:

- **Zusatzleistungsname** — Der Name, der den Kunden angezeigt wird. Wird unterstützt.
- **Beschreibung** — Was die Zusatzleistung bietet.
- **Preis** — Kosten der Zusatzleistung.
- **Abrechnungshäufigkeit** — Ob die Zusatzleistung **Pro Abrechnungszyklus** (wiederkehrend) oder **Einmalig** bei Abonnementbeginn abgerechnet wird.
- **Menge erlauben** — Aktivieren, um Kunden zu ermöglichen, mehrere Einheiten der Zusatzleistung zu kaufen.
- **Erforderlich** — Dieses Kontrollkästchen markieren, um die Zusatzleistung automatisch auf allen neuen Abonnements zu beinhalten. Erforderliche Zusatzleistungen können von den Kunden nicht entfernt werden.

[![](https://d35p197z48916e.cloudfront.net/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Probeperioden (Registerkarte "Preis")

Eine Probeperode ermöglicht es Kunden, Ihr Abonnement vor der ersten vollen Abrechnung auszuprobieren. Konfigurieren Sie dies in der **Probeperioden-Karte**, unterhalb der Preiskonfiguration:

- **Probeperioden (Tage)** — Anzahl der kostenlosen Probetage. Auf `0` setzen, um Probephasen zu deaktivieren. Maximal sind 365 Tage.
- **Probepreis** — Optionaler reduzierter Preis während der Probephase (z. B. $1 für den ersten Monat). Leer lassen, um eine vollständig kostenlose Probephase zu erhalten.

## Begrenzungen und Einschränkungen (Registerkarte "Preis")

Die **Begrenzungen & Einschränkungen**-Karte, die sich ebenfalls auf der Registerkarte "Preis" befindet, enthält:

- **Maximale Abrechnungszyklen** — Die Gesamtanzahl der Abrechnungszyklen, bevor das Abonnement automatisch endet. Leer lassen, um unbegrenzte wiederkehrende Abrechnungen zu ermöglichen. Nützlich für Ratenpläne oder zeitlich begrenzte Abonnements.

**Einrichtungsgebühr** und **Sortierreihenfolge** sind nicht Teil dieser Karte - sie werden einmalig festgelegt, wenn Sie den Plan über den **Wizard erstellen**-Fluss erstellen, und können danach nicht mehr über das Bearbeitungsbildschirm geändert werden. Wenn Sie einen dieser Werte anpassen müssen, deaktivieren Sie den Plan und erstellen Sie ihn erneut mit dem Wizard, anstatt den vorhandenen zu bearbeiten. Beachten Sie, dass Einrichtungsgebühren in dieser Version nicht automatisch bei der Kasse berechnet werden - behandeln Sie das Feld als reserviert für ein zukünftiges Update anstelle eines funktionierenden Gebühren.

## Stornierungsbedingungen (Registerkarte "Lebenszyklus")

Kontrollieren Sie, wie Kunden ihr Abonnement stornieren können, in der **Stornierungsbedingungen**-Karte:

{
  "Policy": "Richtlinie",
  "Description": "Beschreibung",
  "**Cancel Anytime**": "Kunden können jederzeit widerrufen",
  "**Cancel at Period End**": "Die Kündigung tritt am Ende des bezahlten Zeitraums in Kraft – Kunden behalten den Zugang bis zum Ablaufdatum",
  "**Minimum Commitment Required**": "Kunden müssen eine minimale Anzahl von Abrechnungszyklen absolvieren, bevor sie kündigen können",
  "Additional settings": "Zusätzliche Einstellungen",
  "- **Minimum Commitment (Cycles)**": "- **Mindestverpflichtung (Zyklen)**",
  "- **Grace Period (Days)**": "- **Frist (Tage)**",
  "- **Reactivation Period (Days)**": "- **Wiederherstellung (Tage)**",
  "## Plan change behavior (Lifecycle tab)": "## Planänderungsverhalten (Registerkarte Lebenszyklus)",
  "The **Plan Change Behavior** card, below Cancellation Policy, controls what happens when customers upgrade or downgrade between plans": "Das **Planänderungsverhalten**-Karten, unter Kündigungsrichtlinie, steuert, was passiert, wenn Kunden zwischen Plänen upgraden oder downgraden",
  "- **Upgrade Behavior**": "- **Upgradeverhalten**",
  "- **Downgrade Behavior**": "- **Downgradeverhalten**",
  "![Lifecycle tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)": "![Lifecycle-Registerkarte des Plan-Editors](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)",
  "## Advanced tab": "## Erweiterte Registerkarte",
  "The **Advanced** tab holds settings you'll rarely need day to day": "Die **Erweiterte**-Registerkarte enthält Einstellungen, die Sie selten täglich benötigen",
  "- **Provider Integration**": "- **Anbieter-Integration**",
  "- **Statistics**": "- **Statistiken**",
  "![Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)": "![Erweiterte Registerkarte des Plan-Editors](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)",
  "## Visibility and status (General tab)": "## Sichtbarkeit und Status (Allgemeine Registerkarte)",
  "- **Active**": "- **Aktiv**",
  "- **Public**": "- **Öffentlich**",
  "## Tips": "## Tipps",
  "- Use a **trial period** to reduce hesitation": "- Verwenden Sie einen **Probierzeitraum**, um Zögernisse zu reduzieren",
  "- Set up **three pricing tiers**": "- Richten Sie **drei Preistypen** ein",
  "- For service-based subscriptions": "- Für servicebasierte Abonnements",
  "- Keep the **Grace Period** at 3–7 days for payment failures": "- Halten Sie die **Frist** bei 3–7 Tagen für Zahlungsfehler",
  "- Use the **Required** flag on add-ons sparingly": "- Verwenden Sie das **Erforderlich**-Flag bei Zusatzprodukten sparsam",
  "- Deactivate plans with no subscribers rather than deleting them": "- Deaktivieren Sie Pläne ohne Abonnenten, anstatt sie zu löschen"
}