---
title: Abo-Pläne
---

Abo-Pläne ermöglichen es Ihnen, wiederkehrende Abrechnungen für Ihre Produkte anzubieten — ideal für Verbrauchsmaterialien, Dienstleistungen, kuratierte Boxen oder jedes Produkt, das Kunden häufig kaufen. Dieser Leitfaden erklärt, wie Sie Pläne erstellen und konfigurieren, Preistarife einrichten, Probephase hinzufügen und optionale Zusatzfunktionen anhängen.

## Einstieg

Gehen Sie zu **Abonnements > Abo-Pläne** im Admin-Seitenleistenmenü. Die Planliste zeigt alle Ihre Pläne mit ihrem Preismodell, der Anzahl der aktiven Abonnenten und dem Sichtbarkeitsstatus.

![Liste der Abo-Pläne](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Um einen neuen Plan zu erstellen, klicken Sie auf die Schaltfläche **Mit Assistenten erstellen** — dies öffnet den Plan-Assistenten, der Sie Schritt für Schritt durch die Einrichtung führt. Die Schaltfläche **+ Plan hinzufügen** neben ihr öffnet ein leeres Formular für Händler, die lieber alles manuell konfigurieren möchten.

Ein Plan allein ist nicht käuflich — er ist ein Vorlage. Sobald Sie ihn hier erstellt haben, hängen Sie ihn an ein oder mehrere Produkte aus dem **Abonnements**-Tab des Produkts (nur für einfache, variable und digitale Produkte), damit Kunden sich tatsächlich abonnieren können. Siehe [Produkte als Abonnements verkaufen](/help/selling-products-as-subscriptions) für diesen Schritt.

## Der Plan-Editor

Das Öffnen eines vorhandenen Plans (klicken Sie auf dessen Namen oder das Bleistift-Symbol aus der Liste) bringt Sie zum Plan-Editor. Die Kopfzeile zeigt den Plan-Namen, sein Preismodell, die Status-Schlagwörter **Aktiv**/**Inaktiv** und **Öffentlich**/**Privat** sowie das Erstellungsdatum. Die beiden Schaltflächen in der oberen rechten Ecke der Kopfzeile speichern Ihre Änderungen — das Kreis-Symbol mit Haken speichert und kehrt zur Liste zurück, das einfache Kreis-Symbol mit Haken speichert und lässt Sie auf der Seite, damit Sie weiter bearbeiten können.

Unter der Kopfzeile ist eine Statistik-Streifen, die den Plan im Blickfeld zusammenfasst: **Aktive Abonnements**, **Preistarifen**, **Zusatzfunktionen** und **Gesamteinnahmen**.

Der Rest des Formulars ist in fünf Tabs organisiert:

| Tab | Was er enthält |
|-----|-----------------|
| **Allgemein** | Plan-Informationen (Name, Slug, Beschreibung) und Status (aktiv/öffentlich) |
| **Preisgestaltung** | Preiskonfiguration, Probephase und Grenzen & Einschränkungen |
| **Stufenpreis & Zusatzfunktionen** | Die Preistarifen- und Zusatzfunktionen-Editoren |
| **Lebenszyklus** | Stornierungsbedingungen und Plan-Änderungsverhalten |
| **Erweitert** | Anbieter-Integration und Statistiken |

Die Abschnitte darunter durchlaufen die Einstellungen jedes Tabs. Wenn Sie einen brandneuen Plan direkt aus **+ Plan hinzufügen** (anstelle des Assistenten) erstellen, erscheinen dieselben Felder in einem einzigen scrollbaren Formular anstelle von Tabs — speichern Sie den Plan einmal und öffnen Sie ihn erneut, um den vollständigen Tab-Editor zu erhalten.

## Plan-Informationen (Allgemeiner Tab)

Der **Plan-Informationen**-Bereich fasst die Kernidentität Ihres Plans zusammen.

- **Plan-Name** — Der Name, den Kunden beim Abonnieren sehen. Klicken Sie auf das Globus-Symbol, um Übersetzungen für andere Store-Sprachen hinzuzufügen.
- **Slug** — Ein URL-freundlicher Bezeichner, der automatisch aus dem Namen generiert wird (z. B. `premium-plan`). Dies wird intern und in Integrationen verwendet.
- **Beschreibung** — Optionaler Text, der beschreibt, was der Plan enthält. Unterstützt Übersetzungen.

Der **Status**-Bereich auf demselben Tab steuert die **Aktiv**- und **Öffentlich**-Schalter — siehe [Sichtbarkeit und Status](#visibility-and-status) unten.

![Allgemeiner Tab des Plan-Editors](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Preismodell (Preisgestaltungs-Tab)

Der **Preisgestaltungs-Karte** steuert, wie die Preise für diesen Plan strukturiert sind:

| Preismodell | Am besten für |
|---------------|----------------|
| **Stufenpreis** | Angebot von monatlichen, quartalsweisen und jährlichen Verpflichtungsmodi mit Rabatten für längere Laufzeiten |
| **Mengenbasiert** | Pro-Sitz- oder pro-Benutzer-Preisgestaltung, bei der sich der Gesamtpreis mit der Menge verändert (z. B. Team-Lizenzen) |
| **Fester Preis** | Ein einzelner fester Preis ohne Variationen |

Für **Mengenbasierte**-Pläne **Erlaubnis für Menge** prüfen und **Mindestmenge** (mindestens erforderliche Sitzplätze) festlegen und optional eine **Maximalmenge** festlegen, um die Anzahl der Sitzplätze, die ein Abonnent erwerben kann, zu begrenzen.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Preistarife (Tabulator & Ergänzungen)

Preistarife definieren die Abrechnungshäufigkeit und Rabattoptionen, die Kunden für diesen Plan erhalten. Fügen Sie sie im **Preistarif-Karte** auf dem **Tabulator & Ergänzungen**-Tab hinzu, neben dem Ergänzungs-Editor.

Jeder Tarif hat diese Felder:

- **Tarifname** — Die Bezeichnung, die Kunden angezeigt wird (z. B. `Monatlich`, `Jährlich - 20% sparen`). Unterstützt Übersetzungen.
- **Abrechnungszyklus** — Wie oft der Kunde abgerechnet wird: Täglich, Wöchentlich, Monatlich, Quartalsweise, Halbjährlich oder Jährlich.
- **Abrechnungsintervall** — Der Multiplikator für den Abrechnungszyklus. Auf `2` setzen, um alle 2 Monate abzurechnen.
- **Rabattprozentsatz** — Der Rabatt, der auf den Produktpreis für diesen Tarif angewandt wird. Auf `0` setzen, um den Vollpreis zu erhalten, oder auf `20`, um 20 % Rabatt zu gewähren. Dieser Rabatt wird zusätzlich zu jedem Verkaufspreis des Produkts selbst addiert.
- **Standard-Tarif** — Markieren Sie einen Tarif als Standard, um ihn für Kunden vorzuselektieren, wenn sie die Abonnementoptionen ansehen.

Der Rabatt gilt ab dem ersten Abrechnungszyklus des Kunden, nicht nur bei Verlängerungen — ein Tarif mit 20 % Rabatt berechnet 20 % Rabatt ab dem ersten Tag (oder vom ersten Abrechnungstermin nach einem Testzeitraum, falls der Plan einen hat).

### Beispiel: mehrstufiger Plan mit drei Optionen

Für einen Abonnementplan "Kaffee-Club":

| Tarifname | Abrechnungszyklus | Rabatt |
|-----------|-------------------|--------|
| Monatlich | Monatlich | 0% |
| Quartalsweise - 10% sparen | Quartalsweise | 10% |
| Jährlich - 20% sparen | Jährlich | 20% |

## Testphase

Eine Testphase ermöglicht es Kunden, Ihr Abonnement vor der ersten vollen Abrechnung auszuprobieren. Konfigurieren Sie dies im **Testphase**-Abschnitt:

- **Testphase (Tage)** — Anzahl der kostenlosen Testtage. Auf `0` setzen, um Testphasen zu deaktivieren. Maximal sind 365 Tage.
- **Testpreis** — Optionaler reduzierter Preis während der Testphase (z. B. $1 für den ersten Monat). Leer lassen, um eine vollständig kostenlose Testphase zu gewähren.

## Kündigungsbedingungen

Kontrollieren Sie, wie Kunden ihr Abonnement kündigen können, im **Kündigungsbedingungen**-Abschnitt:

| Politik | Beschreibung |
|--------|-------------|
| **Kündigen Sie jederzeit** | Kunden können jederzeit sofort kündigen |
| **Kündigen Sie am Ende des Zeitraums** | Die Kündigung tritt am Ende des abgerechneten Zeitraums in Kraft — Kunden behalten den Zugang bis zum Ablauf |
| **Mindestverpflichtung erforderlich** | Kunden müssen eine minimale Anzahl von Abrechnungszyklen absolvieren, bevor sie kündigen können |

Zusätzliche Einstellungen:

- **Mindestverpflichtung (Zyklen)** — Wenn die Verpflichtungspolitik verwendet wird, setzen Sie die erforderliche Anzahl von Abrechnungszyklen (z. B. `3` für eine Mindestverpflichtung von 3 Monaten).
- **Graziationszeitraum (Tage)** — Tage des weiteren Zugangs nach einem Zahlungsfehler, bevor das Abonnement ausgesetzt wird. Auf `0` setzen, um sofortige Aussetzung zu gewährleisten.
- **Wiederherstellungskontingenz (Tage)** — Tage nach der Kündigung, innerhalb derer ein Kunde sein Abonnement ohne Neuanmeldung wieder aktivieren kann.

## Planänderungsverhalten

Wenn Kunden zwischen Plänen aufwärts- oder abwärtsweisen, können Sie steuern, wann die Änderung wirksam wird:

- **Upgradeverhalten** — Auf **Sofort** (pro-rata-Betrag jetzt berechnen) oder **Bei Erneuerung** (Wechsel am nächsten Abrechnungstermin).
- **Downgradeverhalten** — Auf **Sofort** (Guthaben auf das nächste Rechnungskonto anwenden) oder **Bei Erneuerung** (Wechsel am nächsten Abrechnungstermin).

## Begrenzungen und Einschränkungen

- **Maximale Abrechnungszyklen** — Die Gesamtanzahl von Abrechnungszyklen, bevor das Abonnement automatisch endet. Leer lassen für unbegrenzte wiederkehrende Abrechnung. Nützlich für Ratenpläne oder zeitlich begrenzte Abonnements.
- **Einrichtungsgebühr** — Eine Einmalgebühr, die bei der ersten Erstellung des Abonnements erhoben wird (z. B. Einrichtungs- oder Aktivierungsgebühr). Auf `0.00` setzen, um keine Einrichtungsgebühr zu haben.

## Plan-Erweiterungen

Erweiterungen sind optionale Zusätze, die Abonnenten an ihren Plan anhängen können. Fügen Sie sie im **Plan-Erweiterungen**-Bereich hinzu:

- **Erweiterungsname** — Der Name, der Kunden angezeigt wird.

Unterstützt Übersetzungen.
- **Beschreibung** — Was das Add-on bietet.
- **Preis** — Kosten des Add-ons.
- **Abrechnungshäufigkeit** — Ob das Add-on **Pro Abrechnungszyklus** (wiederkehrend) oder **Einmalig** beim Abonnementbeginn berechnet wird.
- **Mengenverfügbarkeit** — Aktivieren, um Kunden zu erlauben, mehrere Einheiten des Add-ons zu kaufen.
- **Erforderlich** — Markieren Sie dies, um das Add-on automatisch auf allen neuen Abonnements zu beinhalten.

Erforderliche Add-ons können von den Kunden nicht entfernt werden.

## Sichtbarkeit und Status

- **Aktiv** — Abwählen, um ein Abonnement zu deaktivieren, sodass keine neuen Abonnements erstellt werden können. Bestehende Abonnements werden nicht beeinflusst.
- **Öffentlich** — Abwählen, um das Abonnement vor Kundenseiten zu verbergen (nützlich für interne oder veraltete Abonnements, bei denen die bestehenden Abonnenten weiterhin dabei sind).
- **Sortierreihenfolge** — Steuert die Anzeigereihenfolge auf Seiten zur Abonnementauswahl. Kleinere Zahlen erscheinen zuerst.

## Tipps

- Verwenden Sie einen **Probemonat**, um Zögern zu reduzieren – selbst ein kurzer 7-Tage-Probemonat kann die Conversion-Raten bei Abonnementprodukten erheblich steigern.
- Richten Sie **drei Preisstufen** (monatlich, quartalsweise, jährlich) mit zunehmenden Rabatten ein, um jährliche Verpflichtungen zu fördern und Ihr Cashflow-Management zu verbessern.
- Bei Dienstleistungs-Abonnements setzen Sie die **Kündigungsfrist** auf **Kündigung am Ende des Zeitraums**, damit Kunden Zugang bis zu ihrem Zahlungszeitraum behalten – dies fühlt sich fair an und reduziert Chargebacks.
- Halten Sie die **Frist für Fristverlängerung** bei 3–7 Tagen für Zahlungsfehler. Dies gibt den Kunden Zeit, ihre Zahlungsmethode zu aktualisieren, bevor sie den Zugang verlieren.
- Verwenden Sie das **Erforderlich**-Flag bei Add-ons sparsam – verwenden Sie es nur für Dinge, die wirklich obligatorisch sind (z. B. einen Dienstleistungsvertrag), und nicht, um Preise zu erhöhen.
- Deaktivieren Sie Abonnements ohne Abonnenten, anstatt sie zu löschen – dies erhält historische Daten für alle Kunden, die ursprünglich abonniert haben.