---
title: Ausgelöste Journeys
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Die **Journeys** im Campaign Studio sind automatisierte, mehrstufige E-Mail-Sequenzen, die von selbst starten, sobald ein Kunde eine bestimmte Aktion ausführt – sich anmeldet, eine Bestellung aufgibt, Artikel im Warenkorb zurücklässt, sich eine Weile nicht meldet oder eine Bestellung zugestellt bekommt. Anstatt sich daran zu erinnern, eine Willkommens-E-Mail, eine Erinnerung zum Warenkorb oder eine Bewertungsanfrage manuell zu senden, erstellen Sie die Sequenz einmal und Spwig führt sie für jeden qualifizierten Kunden aus, solange die Journey aktiv ist.

## Drei Möglichkeiten zum E-Mail-Versand

Das Campaign Studio deckt nun drei unterschiedliche Versandmuster ab:

| Typ | Verhalten |
|------|-----------|
| **Broadcast** | Wird einmalig gesendet – sofort oder zu einem einzelnen geplanten Datum und einer Uhrzeit. Ideal für einmalige Ankündigungen oder Sales. |
| **Recurring** | Eine Vorlage, die nach einem wiederkehrenden Zeitplan gesendet wird (siehe [Recurring Campaigns](/help/recurring-campaigns)). |
| **Journey** | Eine mehrstufige Sequenz, die automatisch für einen einzelnen Kunden startet, wenn ein Lifecycle-Ereignis eintritt, und die Schritte dann über Stunden oder Tage verteilt. |

Eine Journey hat keinen eigenen "Senden"-Button und keinen zu konfigurierenden Zeitplan – sie reagiert auf Ereignisse statt auf die Uhr.

## Trigger

Jede Journey lauscht auf genau ein Ereignis, das als **Trigger** der Journey festgelegt wird:

| Trigger | Wird ausgelöst, wenn |
|---------|-----------|
| **Kunde meldet sich an** | Ein neues Kundenkonto erstellt wird. |
| **Bestellung wird aufgegeben** | Eine Bestellung aufgegeben wird, von einem neuen oder wiederkehrenden Kunden. |
| **Erste Bestellung wird aufgegeben** | Speziell die allererste Bestellung eines Kunden. |
| **Warenkorb aufgegeben** | Ein Käufer fügt etwas in seinen Warenkorb, wird dann inaktiv, ohne die Kasse zu durchlaufen. |
| **Kunde inaktiv (Win-back)** | Ein Kunde hat seit einer Weile keine Bestellung aufgegeben. |
| **Bestellung zugestellt** | Der Status einer Bestellung wird auf "Zugestellt" geändert. |
| **Produkt wieder auf Lager** | Ein Produkt, über das ein Kunde benachrichtigt werden wollte, ist wieder verfügbar. |

## Die Wiederherstellungs- und Re-Engagement-Trigger im Detail

**Bestellung zugestellt** und **Produkt wieder auf Lager** werden sofort ausgelöst, auf dieselbe Weise wie **Bestellung wird aufgegeben**. **Warenkorb aufgegeben** und **Kunde inaktiv (Win-back)** funktionieren anders: Anstatt auf einen einzelnen Moment zu reagieren, prüft Spwig regelmäßig nach Käufern und Kunden, die die Kriterien erfüllen, sodass es zu einer kurzen Verzögerung zwischen dem Inaktivwerden des Warenkorbs (oder dem Inaktivwerden eines Kunden) und der Registrierung kommen kann.

**Warenkorb aufgegeben** – registriert einen Käufer, der etwas in seinen Warenkorb gelegt und dann inaktiv geworden ist, ohne den Kauf abzuschließen. Standardmäßig geschieht dies nach etwa einer Stunde Inaktivität; das genaue Inaktivitätsfenster (und wie weit in die Vergangenheit Spwig noch zurückblickt) ist ein Schwellenwert, den Ihr Host für Ihren Shop anpassen kann. Es funktioniert sowohl für angemeldete Käufer als auch für Gäste – für einen Gast verwendet Spwig die bei der Kasse erfasste E-Mail-Adresse. Wenn der Käufer zurückkehrt und seine Bestellung abschließt, wird er automatisch aus der Journey entfernt, sodass eine abgeschlossene Bestellung niemals eine "Haben Sie etwas vergessen?"-E-Mail erhält. Fügen Sie der Wiederherstellungs-E-Mail einen **Abandoned Cart**-Inhaltsblock hinzu, um genau das anzuzeigen, was zurückgelassen wurde, mit aktuellen Preisen, Bildern und einem Link zurück zum Warenkorb – oder verwenden Sie einen **Featured Product**-Block, um stattdessen einen einzelnen Artikel hervorzuheben.

**Kunde inaktiv (Win-back)** – registriert einen Kunden, der seit einer Weile keine Bestellung aufgegeben hat, um ihm einen Grund zu geben, zurückzukehren.

Standardmäßig sind das 90 Tage ohne Kauf (ebenfalls ein vom Host anpassbarer Schwellenwert).

Ein Kunde wird innerhalb dieses Zeitfensters höchstens einmal in eine Win-back-Reise aufgenommen, sodass jemand, der weiterhin inaktiv bleibt, nicht sofort erneut eingeschaltet wird.

**Bestellung zugestellt** — nimmt einen Kunden auf, sobald der Status seiner Bestellung auf **Zugestellt** wechselt, was ein natürlicher Zeitpunkt ist, um einige Tage später um eine Bewertung zu bitten. Es wird einmal pro Bestellung ausgelöst, beim Übergang in den Status „Zugestellt“ — spätere Änderungen an einer bereits zugestellten Bestellung lösen es nicht erneut aus. Beachten Sie, dass die Massenaktion **Ausgewählte Bestellungen als zugestellt markieren** in der Bestellliste Bestellungen direkt aktualisiert und diesen Auslöser (oder die Zustellbestätigungs-E-Mail) nicht auslöst; aktualisieren Sie Bestellungen einzeln oder über die Spwig-App, damit er ausgelöst wird.

**Produkt wieder auf Lager** — wenn ein Produkt, über das ein Kunde benachrichtigt werden wollte, wieder auf Lager ist, prüft Spwig, ob Sie eine aktive Reise haben, die auf diesen Auslöser wartet. Wenn ja, wird der Kunde in diese Reise aufgenommen, anstatt die einfache Einmal-Benachrichtigung zu erhalten — so können Sie eine Verzögerung, einen **Empfohlenes Produkt**-Block mit dem wieder auf Lager befindlichen Artikel oder eine Follow-up-E-Mail hinzufügen. Wenn keine Reise für „wieder auf Lager“ aktiv ist, erhalten Kunden weiterhin die standardmäßige Einmal-Benachrichtigungs-E-Mail genau wie zuvor, sodass das Aktivieren einer Reise für diesen Auslöser völlig optional ist.

## Eine Reise erstellen

Navigieren Sie zu **Campaign Studio > Journeys** und klicken Sie auf **Reise hinzufügen**.

1. Geben Sie der Reise einen **Namen** — dies dient nur Ihrer Referenz; Kunden sehen ihn nie.
2. Wählen Sie das **Auslöser**-Ereignis.
3. Setzen Sie optional **Nur für Segment** auf ein Segment — wenn gesetzt, werden nur Abonnenten, die diesem Segment angehören, aufgenommen. Lassen Sie es leer, um jeden qualifizierten Abonnenten aufzunehmen.
4. Setzen Sie **Einmal pro Abonnent** und **Wiederanmeldungs-Kühlzeit (Tage)** — siehe [Schutz vor Überanmeldung](#guarding-against-over-enrollment) unten.
5. Setzen Sie **Status** auf **Aktiv**, um die Reise zu aktivieren. Lassen Sie es als **Entwurf**, während Sie noch daran arbeiten, oder setzen Sie es auf **Pausiert**, um neue Anmeldungen zu stoppen, ohne Ihre Einstellungen zu verlieren.
6. Klicken Sie auf **Speichern** — Spwig leitet Sie direkt in den [Journey Builder](/help/journey-builder) weiter, die visuelle Leinwand, auf der Sie die tatsächliche Sequenz gestalten: welche E-Mails gesendet werden, wie lange zwischen ihnen gewartet wird und ob verschiedene Abonnenten unterschiedliche Pfade folgen sollten.

Eine einfache dreistufige Willkommensserie könnte nach der Gestaltung auf der Leinwand wie folgt aussehen:

| Schritt | Wartet | Sendet |
|------|-------|-------|
| 1 | Sofort | Willkommens-E-Mail |
| 2 | 3 Tage später | Tipps zum Einstieg |
| 3 | 7 Tage danach | Rabatt für die erste Bestellung |

Die E-Mails selbst sind gewöhnliche Kampagnen, die Sie im selben visuellen Builder gestalten, den Sie für eine Broadcast-Kampagne verwenden würden — Betreffzeile, Inhaltsblöcke, alles. Es ist nicht nötig, sie selbst zu planen oder zu senden; lassen Sie sie als **Entwurf** und wählen Sie sie einfach aus dem Dropdown-Menü des Schritts im Builder aus. Die Reise sendet sie für Sie, einmal pro Abonnent, der diesen Schritt erreicht.

Siehe [Journey Builder](/help/journey-builder) für die vollständige Anleitung zum Gestalten von Schritten auf der Leinwand, zum Verzweigen einer Reise mit einer **Ja/Nein**-Bedingung und zum Starten von einer fertigen Vorlage anstelle einer leeren Leinwand.

## A/B-Test eines Schritts

Jeder **E-Mail senden**-Schritt kann in einen A/B-Test umgewandelt werden, sodass eine Reise automatisch herausfindet — und dann beibehält — die E-Mail, die am besten funktioniert. Da eine Reise kontinuierlich läuft (Abonnenten kommen im Laufe der Zeit hinzu), testet Spwig keine feste Charge und stoppt dann; stattdessen **verteilt es die Anmeldungen gleichmäßig über die Varianten, während sie einlaufen, beobachtet, wie jede performt, und schließt diese Variante für alle zukünftigen Anmeldungen ein, sobald sie ein klarer statistischer Gewinner ist.** Abonnenten, die bereits mitten in der Reise sind, behalten die Version, die sie zuerst erhalten haben.

Öffnen Sie einen E-Mail senden-Schritt im [Journey Builder](/help/journey-builder) und setzen Sie **Schritttyp**:

- **Einzelnachricht** — das normale Verhalten: Alle erhalten die eine E-Mail, die Sie auswählen.
- **A/B: verschiedene E-Mails** — wählen Sie **zwei bis vier** E-Mails (unterschiedliche Designs, Angebote oder Layouts); jeder Teilnehmer erhält eine davon.
- **A/B: verschiedene Betreffzeilen** — wählen Sie eine E-Mail und geben Sie **zwei bis vier** Betreffzeilen ein; jeder Teilnehmer erhält diese E-Mail mit einer anderen Betreffzeile.

Wählen Sie dann **Gewinner bestimmen nach** — **Öffnungsrate** (in der Regel am besten für einen Betrefftest) oder **Klickrate** — und Sie sind fertig. Stellen Sie die Journey auf **Aktiv** und die Teilnehmer werden auf die Varianten aufgeteilt.

Das Panel des Schritts zeigt eine **Live-Anzeige**, während Daten einlaufen — die Empfänger, die Öffnungsrate und die Klickrate jeder Variante sowie, wie zuversichtlich Spwig in Bezug auf den führenden ist („Führt mit 92 % Zuversicht“). Ein Gewinner wird erst dann festgelegt, wenn Spwig mindestens **95 % zuversichtlich** ist *und* genügend Daten vorliegen, um dies zu vertrauen, damit eine Journey mit wenig Verkehr keine vorschnellen Schlüsse zieht. Sobald festgelegt, liest der Schritt **„Gewinner festgelegt: Variante B“** und jeder neue Teilnehmer erhält diese Variante; auf der Leinwand zeigt die Karte während des Tests **„A/B · N E-Mails“** und nach der Entscheidung **„A/B-Gewinner: B“**.

Ein paar Dinge, die Sie wissen sollten:

- **Stellen Sie Verkehr bereit.** Die Zuversicht hängt vom Volumen ab — ein Schritt, den nur eine Handvoll Personen erreicht, kann eine Weile bei „Noch nicht genügend Daten“ verweilen. A/B-Tests glänzen bei Journeys mit stetiger Anmeldung.
- **Das Bearbeiten der Varianten oder der Gewinnermetrik startet einen neuen Test** — ein zuvor festgelegter Gewinner wird gelöscht, damit die neue Konfiguration ihr eigenes Ergebnis erzielt.
- Ein A/B-Schritt mit weniger als zwei Varianten **blockiert die Journey daran, auf Aktiv zu gehen**, bis Sie ihn vervollständigen (oder auf eine einzelne E-Mail zurückwechseln).

Siehe [A/B-Test](ab-testing) für weitere Informationen dazu, wie Spwig Zuversicht und Signifikanz liest.

## So funktioniert die Anmeldung

Wenn das Triggerereignis für einen Kunden eintritt, prüft Spwig jede aktive Journey, die auf dieses Ereignis wartet, und **meldet** den Kunden für jede Journey, für die er qualifiziert ist, am Startpunkt des Flows an. Von dort aus bewegt Spwig den Abonnenten durch das, was Sie auf der Leinwand entworfen haben — wartet jeden **Warten**-Schritt ab, sendet die E-Mail jedes **E-Mail senden**-Schritts und folgt dem richtigen **Ja**/**Nein**-Pfad an jeder **Zweigung** — bis sie einen **Beenden**-Schritt erreichen, an dem die Journey für diesen Abonnenten als **Abgeschlossen** markiert wird.

**Einwilligung wird immer respektiert.** Ein Abonnent, der sich nicht für Marketing-E-Mails angemeldet hat oder sich seitdem abgemeldet hat, wird einfach übersprungen — die Journey stoppt nicht für andere Abonnenten, und Abmeldungen während der Journey stoppen die verbleibenden Sendeaktionen dieses Abonnenten automatisch. Sie müssen Ihre Journeys nie selbst nach dem Einwilligungsstatus filtern.

## Schutz vor übermäßiger Anmeldung

Zwei Einstellungen in der Journey steuern, wie oft ein Abonnent sie durchlaufen kann:

| Einstellung | Was sie tut | Typischer Verwendungszweck |
|---------|--------------|-------------|
| **Einmal pro Abonnent** *(standardmäßig aktiviert)* | Jeder Abonnent wird höchstens einmal angemeldet, unabhängig davon, wie oft das Triggerereignis für ihn erneut eintritt. | Eine Willkommensserie — ein Kunde sollte sie nur einmal erhalten. |
| **Wiederanmelde-Kühlzeit (Tage)** | Wenn **Einmal pro Abonnent** deaktiviert ist, legt eine Mindestanzahl an Tagen fest, die seit der letzten Anmeldung eines Abonnenten verstreichen müssen, bevor er erneut angemeldet werden kann. Auf `0` setzen für keine Kühlzeit. | Eine bestellungsgetriggerte Serie, die für eine neue Bestellung erneut ausgeführt werden soll, aber nicht für jede Bestellung in derselben Woche erneut ausgelöst werden soll. |

Schalten Sie **Einmal pro Abonnent** für eine Journey aus, die Sie pro Bestellung ausführen möchten (wie ein Dankeschön nach dem Kauf), und kombinieren Sie dies mit einer Kühlzeit, damit ein Kunde, der zweimal am selben Tag bestellt, nur einmal angemeldet wird. Ein Abonnent, der bereits aktiv eine Journey durchläuft, wird unabhängig von diesen Einstellungen nie in eine zweite, überlappende Ausführung derselben Journey angemeldet.

## Journeys überwachen


Die Liste **Campaign Studio > Journeys** zeigt für jede Journey den **Trigger**, den **Status**, die Anzahl der gesendeten **E-Mails** sowie die laufenden Summen für **Registrierte** / **Abgeschlossene**, sodass Sie auf einen Blick sehen können, ob eine Journey tatsächlich Menschen erreicht.

![Die Journeys-Liste zeigt zwei aktive Journeys mit Registrierungs- und Abschlusszahlen](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Um einzelne Abonnenten anstatt Summen zu sehen, öffnen Sie die Liste **Journey Enrollments** unter `/admin/email_marketing/journeyenrollment/`. Jede Zeile zeigt den Fortschritt eines Abonnenten in einer Journey: in welcher **Journey** er sich befindet, sein **Aktueller Schritt**, sein **Status** (Aktiv, Abgeschlossen oder Storniert) und wann sein **Nächster Schritt** fällig ist. Verwenden Sie die Filter, um die Liste auf eine bestimmte Journey oder einen bestimmten Status einzugrenzen — beispielsweise zeigt der Filter **Aktiv** alle Personen, die sich derzeit in der Mitte der Sequenz befinden.

![Die Journey Enrollments-Liste zeigt den Fortschritt der Abonnenten in zwei Journeys](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Journey-Bericht

Jede Journey hat eine eigene **Bericht**-Seite, die geöffnet wird, indem Sie auf die **Bericht**-Schaltfläche auf der Journey-Karte in **Campaign Studio > Journeys** oder auf der eigenen Einstellungsseite der Journey klicken. Es handelt sich um eine einseitige Zusammenfassung, wie weit die Teilnehmer in der Sequenz gekommen sind und, sofern Ihre E-Mails getrackte Links enthalten, welchen Umsatz die Journey generiert hat.

![Die Journey-Berichtsseite zeigt den Registrierungs-Trichter, die Umsatz-Zuordnungs-Karte und die Umsatz-tabelle nach Schritten](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Registrierungs-Trichter

Vier Karten zeigen, wo sich die Teilnehmer derzeit befinden:

| Karte | Was sie anzeigt |
|------|---------------|
| **Registrierte** | Die Gesamtzahl der Abonnenten, die jemals in diese Journey eingetreten sind. |
| **Aktiv jetzt** | Teilnehmer, die sich derzeit in der Mitte der Sequenz befinden und auf ihren nächsten Schritt warten oder diesen bearbeiten. |
| **Abgeschlossen** | Teilnehmer, die den **Exit**-Schritt der Journey erreicht haben. |
| **Ausgetreten** | Teilnehmer, die vor dem Abschluss aus der Journey entfernt wurden — beispielsweise ein Käufer, der den Checkout in der Mitte einer Warenkorb-Abbruch-Sequenz abgeschlossen hat, oder ein Abonnent, der sich abgemeldet hat. |

Wenn die Journey noch keine Registrierungen hat, zeigen alle vier Karten null an, und ein Hinweis erinnert Sie daran, dass Kennzahlen erst angezeigt werden, wenn Kunden in die Journey eintreten.

### Zugeordneter Umsatz

Die Karte **Zugeordneter Umsatz** funktioniert auf die gleiche Weise wie ein [Kampagnenbericht](campaign-reports) — Spwig verfolgt Bestellungen zurück bis zu Klicks auf Links in den E-Mails der Journey, dieselbe klickbasierte, consent-gesteuerte Zuordnung, die in [Zugeordneter Umsatz](campaign-reports#attributed-revenue) auf dieser Seite beschrieben ist. Die gleichen Einschränkungen gelten hier: Die Zuordnung erfolgt nur über Klicks (ein Öffnen allein ordnet nie Umsatz zu), sie folgt dem aktiven Zuordnungsmodell und dem Rückblickfenster Ihres Shops, sie respektiert die Analytics-Einwilligung und ist nicht rückwirkend — eine Journey zeigt nur Umsatz aus E-Mails, die nach dem Aktivieren der Umsatz-Zuordnung für Ihren Shop gesendet wurden.

Die Zeile unter der Karte unterteilt die Gesamtsumme in:

- **Bestellungen** — wie viele Bestellungen dieser Journey zugeschrieben werden, über alle E-Mails aller Schritte zusammen.
- **AOV** — der durchschnittliche Bestellwert über diese Bestellungen.
- **Umsatz pro Teilnehmer** — zugeordneter Umsatz geteilt durch die Gesamtzahl der **Registrierten**. Eine Journey hat nicht einen einzelnen „Ausgaben“-Wert wie eine Kampagne — sie läuft kontinuierlich anstatt einmalig Kosten zu verursachen — daher gibt es hier keine ROAS-Zahl. **Umsatz pro Teilnehmer** ist das nächstliegende Äquivalent: eine stabile, vergleichbare Kennzahl dafür, wie effizient die Journey eine Registrierung in einen Verkauf umwandelt, die Sie über die Zeit verfolgen oder mit einer anderen Journey vergleichen können.

### Umsatz nach Schritt

Wenn die Journey mindestens einen **E-Mail senden**-Schritt hat, unterteilt die Tabelle **Umsatz nach Schritt** die Gesamtsumme weiter, eine Zeile pro Schritt, sodass Sie sehen können, welche E-Mail in der Sequenz tatsächlich ihren Beitrag leistet:

| Spalte | Was sie anzeigt |
|--------|---------------|
| **Schritt** | Die E-Mail des Schritts, mit einem **A/B**-Badge, falls dieser Schritt einen [A/B-Test](ab-testing) durchführt. |
| **Umsatz** | Der zugeordnete Umsatz aus Bestellungen, die auf die E-Mail dieses Schritts zurückgeführt werden. |
| **Bestellungen** | Die Anzahl der Bestellungen, die hinter dieser Umsatzzahl stehen. |
| **Gesendet** | Wie oft die E-Mail dieses Schritts versendet wurde. |
| **Öffnungen** / **Klicks** | Wie viele dieser Versendungen geöffnet und wie viele angeklickt wurden. Spwig erfasst Öffnungen und Klicks für alle Versendungen der Schritte, sowohl für normale als auch für A/B-Varianten. |

Verwenden Sie diese Tabelle, um eine schwache Stelle in ansonsten gesunden Customer Journeys zu identifizieren – zum Beispiel könnte eine Willkommensserie, bei der die erste E-Mail den Großteil des Umsatzes generiert und ein späterer Schritt nur wenig beiträgt, ein Kandidat für ein stärkeres Angebot oder eine Überarbeitung sein, anstatt anzunehmen, dass die gesamte Sequenz überdacht werden muss.

## Tipps

- Der schnellste Weg, eine Customer Journey für verlassene Warenkörbe, Reaktivierung, Post-Lieferungs-Feedback oder Lagerbestandsbenachrichtigungen zu starten, ist eine Startvorlage – wenn Sie eine neue Journey mit einem dieser Trigger speichern, bietet der **Vorlagen**-Auswahlbereich des [Journey Builder](/help/journey-builder) einen fertigen Flow (**Wiederherstellung verlassener Warenkorb**, **Reaktivierung inaktiver Kunden**, **Anfrage nach Post-Lieferungs-Feedback** oder **Lagerbestandsbenachrichtigung**), den Sie anpassen können, anstatt ihn von Grund auf zu erstellen.
- Starten Sie jede Journey als **Entwurf**, während Sie die Schritte erstellen, und wechseln Sie dann den **Status** zu **Aktiv**, sobald Sie die E-Mails und Verzögerungen überprüft haben – keine Abonnenten werden angemeldet, bis sie aktiv ist.
- Lassen Sie **Einmal pro Abonnent** für alles, was an einen einmaligen Meilenstein gebunden ist (Registrierung, erste Bestellung), aktiviert; deaktivieren Sie es mit einer sinnvollen Abklingzeit für alles, was wiederholt werden sollte, wie eine Post-Kauf-Serie.
- Verwenden Sie **Nur für Segment**, um eine andere Willkommensserie für ein bestimmtes Publikum auszuführen – z. B. erhält ein VIP-Segment eine reichhaltigere Sequenz als alle anderen.
- Setzen Sie die Wartezeit des ersten Schritts auf `0`, wenn Sie möchten, dass die erste E-Mail sofort nach dem Auslösen des Triggers gesendet wird, anstatt zu warten.
- Prüfen Sie die Liste **Journey-Anmeldungen** nach der Aktivierung einer neuen Journey, um sicherzustellen, dass Abonnenten tatsächlich angemeldet werden und wie erwartet durch ihre Schritte fortschreiten.
- Das Pausieren einer Journey (**Status: Pausiert**) stoppt neue Anmeldungen, hebt aber Abonnenten, die bereits mitten drin sind, nicht auf – sie erhalten weiterhin ihre verbleibenden Schritte.