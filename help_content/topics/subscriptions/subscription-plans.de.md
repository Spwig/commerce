---
title: Abo-Pläne
---

Abo-Pläne ermöglichen es Ihnen, wiederkehrende Abrechnungen für Ihre Produkte anzubieten — ideal für Verbrauchsmaterialien, Dienstleistungen, kuratierte Boxen oder jedes Produkt, das Kunden häufig kaufen. Dieser Leitfaden erklärt, wie Sie Pläne erstellen und konfigurieren, Preistarife einrichten, Probephase hinzufügen und optionale Zusatzfunktionen anhängen.

## Einstieg

Gehen Sie zu **Abonnements > Abo-Pläne** im Admin-Seitenleistenmenü. Die Liste der Pläne zeigt alle Ihre Pläne mit ihrem Preismodell, der Anzahl der aktiven Abonnenten und dem Sichtbarkeitsstatus.

Um einen neuen Plan zu erstellen, klicken Sie auf die Schaltfläche **+ Abo-Plan hinzufügen** — dies öffnet den Plan-Erstellungs-Wizard, der Sie Schritt für Schritt durch die Einrichtung führt.

![Liste der Abo-Pläne](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Ein Plan allein ist nicht käuflich — er ist ein Vorlage. Sobald Sie ihn hier erstellt haben, hängen Sie ihn an ein oder mehrere Produkte aus dem **Abonnements**-Tab des Produkts (nur für einfache, variable und digitale Produkte), damit Kunden sich tatsächlich abonnieren können. Siehe [Produkte als Abonnements verkaufen](/help/selling-products-as-subscriptions) für diesen Schritt.

## Planinformationen

Der erste Abschnitt fasst die Kernidentität Ihres Plans zusammen.

- **Plan-Name** — Der Name, den Kunden beim Abonnieren sehen. Klicken Sie auf das Globus-Symbol, um Übersetzungen für andere Sprachen des Ladens hinzuzufügen.
- **Slug** — Ein URL-freundlicher Bezeichner, der automatisch aus dem Namen generiert wird (z. B. `premium-plan`). Dies wird intern und in Integrationen verwendet.
- **Beschreibung** — Optionaler Text, der beschreibt, was der Plan umfasst. Unterstützt Übersetzungen.

## Preismodell

Wählen Sie aus, wie das Preismodell für diesen Plan strukturiert ist:

| Preismodell | Am besten geeignet für |
|---------------|----------|
| **Stufenpreis** | Angebot von monatlichen, vierteljährlichen und jährlichen Verpflichtungsoptionen mit Rabatten für längere Laufzeiten |
| **Mengenbasiert** | Pro-Sitz- oder pro-Benutzer-Preisgestaltung, bei der sich der Gesamtpreis mit der Menge erhöht (z. B. Team-Lizenzen) |
| **Fixpreis** | Ein einziger fester Preis ohne Variationen |

Für **Mengenbasierte**-Pläne legen Sie die **Mindestmenge** (erforderliche Sitzplätze) fest und optional eine **Maximalmenge**, um die Anzahl der Sitzplätze, die ein Abonnent erwerben kann, zu begrenzen.

## Preistarifen

Preistarifen definieren die Zahlungshäufigkeit und Rabattoptionen, die Kunden auf diesem Plan erhalten können. Fügen Sie sie im Abschnitt **Preistarifen** unter dem Hauptformular hinzu.

Jeder Tarif hat diese Felder:

- **Tarifname** — Die Bezeichnung, die Kunden angezeigt werden (z. B. `Monatlich`, `Jährlich — 20 % sparen`). Unterstützt Übersetzungen.
- **Abrechnungszyklus** — Wie oft der Kunde abgerechnet wird: Täglich, Wöchentlich, Monatlich, Quartalsweise, Halbjährlich oder jährlich.
- **Abrechnungsintervall** — Der Multiplikator für den Abrechnungszyklus. Legen Sie auf `2` für die Abrechnung alle 2 Monate fest.
- **Rabattprozentsatz** — Der Rabatt, der auf den Produktpreis für diesen Tarif angewandt wird. Legen Sie auf `0` für den Vollpreis fest, oder auf `20`, um 20 % Rabatt zu gewähren. Dieser Rabatt wird auf den Verkaufspreis des Produkts addiert.
- **Standard-Tarif** — Markieren Sie einen Tarif als Standard, um ihn für Kunden vorzuselektieren, wenn sie die Abonnementsoptionen ansehen.

Der Rabatt gilt ab dem ersten Abrechnungszyklus des Kunden, nicht nur bei Verlängerungen — ein Tarif mit 20 % Rabatt berechnet 20 % Rabatt ab Tag 1 (oder vom ersten Abrechnungsvorgang nach einer Probezeit, falls der Plan einen hat).

### Beispiel: Stufenpreis mit drei Optionen

Für einen 

| Policy | Beschreibung |
|--------|-------------|
| **Jederzeit kündbar** | Kunden können jederzeit jederzeit widerrufen |
| **Am Ende des Zeitraums kündigen** | Die Kündigung tritt am Ende des bezahlten Zeitraums in Kraft — Kunden behalten den Zugang bis zum Ablauf |
| **Mindestverpflichtung erforderlich** | Kunden müssen eine minimale Anzahl von Abrechnungszyklen absolvieren, bevor sie kündigen können |

Zusätzliche Einstellungen:

- **Mindestverpflichtung (Zyklen)** — Wenn Sie die Verpflichtungspolitik verwenden, legen Sie die erforderliche Anzahl von Abrechnungszyklen fest (z. B. `3` für eine Mindestverpflichtung von 3 Monaten).
- **Frist (Tage)** — Tage des weiteren Zugangs nach einem Zahlungsfehler, bevor das Abonnement ausgesetzt wird. Auf `0` setzen, um sofortige Aussetzung zu erreichen.
- **Wiederherstellungsfrist (Tage)** — Tage nach der Kündigung, in denen ein Kunde sein Abonnement ohne Neuanmeldung wiederherstellen kann.

## Änderungsverhalten für Pläne

Wenn Kunden zwischen Plänen upgraden oder downgraden, können Sie steuern, wann die Änderung wirksam wird:

- **Upgrades Verhalten** — Auf **Sofort** (pro-rata-Betrag jetzt berechnen) oder **Bei Erneuerung** (Wechsel bei nächster Abrechnung).
- **Downgrade Verhalten** — Auf **Sofort** (Guthaben auf das nächste Rechnung anwenden) oder **Bei Erneuerung** (Wechsel bei nächster Abrechnung).

## Grenzen und Einschränkungen

- **Maximale Abrechnungszyklen** — Die Gesamtanzahl der Abrechnungszyklen, bevor das Abonnement automatisch endet. Leer lassen für unbegrenzte wiederkehrende Abrechnung. Nützlich für Ratenpläne oder zeitlich begrenzte Abonnements.
- **Einrichtungsgebühr** — Eine Einmalgebühr, die bei der ersten Erstellung des Abonnements erhoben wird (z. B. Onboarding- oder Aktivierungsgebühr). Auf `0.00` setzen, um keine Einrichtungsgebühr zu haben.

## Plan-Erweiterungen

Erweiterungen sind optionale Extras, die Abonnenten an ihren Plan anhängen können. Fügen Sie sie im **Plan-Erweiterungen**-Bereich hinzu:

- **Erweiterungsname** — Der Name, der den Kunden angezeigt wird. Unterstützt Übersetzungen.
- **Beschreibung** — Was die Erweiterung bietet.
- **Preis** — Kosten der Erweiterung.
- **Abrechnungshäufigkeit** — Ob die Erweiterung **Pro Abrechnungszyklus** (wiederkehrend) oder **Einmalig** bei Abonnementbeginn berechnet wird.
- **Menge zulassen** — Aktivieren, um Kunden zu ermöglichen, mehrere Einheiten der Erweiterung zu kaufen.
- **Erforderlich** — Dieses Kontrollkästchen aktivieren, um die Erweiterung automatisch auf allen neuen Abonnements einzuschließen. Erforderliche Erweiterungen können von den Kunden nicht entfernt werden.

## Sichtbarkeit und Status

- **Aktiv** — Abwählen, um einen Plan zu deaktivieren, damit keine neuen Abonnements erstellt werden können. Bestehende Abonnements werden nicht beeinflusst.
- **Öffentlich** — Abwählen, um den Plan von den kundenseitigen Seiten zu verbergen (nützlich für interne oder veraltete Pläne, bei denen sich bestehende Abonnenten befinden).
- **Sortierreihenfolge** — Steuert die Anzeigereihenfolge auf Seiten zur Abonnementauswahl. Niedrigere Zahlen erscheinen zuerst.

## Tipps

- Verwenden Sie einen **Probezeitraum**, um Zögern zu reduzieren — selbst ein kurzer 7-Tage-Probemonat kann die Konversionsraten bei Abonnementprodukten erheblich steigern.
- Richten Sie **drei Preistypen** (monatlich, quartalsweise, jährlich) ein, wobei die Rabatte mit zunehmender Dauer zunehmen, um jährliche Verpflichtungen zu fördern und Ihr Cashflow-Management zu verbessern.
- Bei Dienstleistungsabonnements den **Kündigungszeitraum** auf **Am Ende des Zeitraums kündigen** setzen, damit Kunden Zugang bis zu ihrem bezahlten Zeitraum behalten — dies fühlt sich fair an und reduziert Chargebacks.
- Halten Sie die **Frist** bei 3–7 Tagen für Zahlungsfehler. Dies gibt den Kunden Zeit, ihre Zahlungsmethode zu aktualisieren, bevor der Zugang verloren geht.
- Verwenden Sie das **Erforderlich**-Flag bei Erweiterungen sparsam — nur für Dinge verwenden, die wirklich obligatorisch sind (z. B. einen Dienstvertrag), nicht als Möglichkeit, Preise zu erhöhen.
- Deaktivieren Sie Pläne ohne Abonnenten, anstatt sie zu löschen — dies erhält historische Daten für alle Kunden, die ursprünglich abonniert haben.