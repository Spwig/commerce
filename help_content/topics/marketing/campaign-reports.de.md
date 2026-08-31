---
title: Kampagnenberichte
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: Die Berichtsseite, auf der der "Engagement over time"-Diagrammkarte angezeigt wird, bei einer Kampagne mit mehreren Tagen an Versandhistorie, sodass alle drei Linien (Gesendet, Geöffnet, Klicks) ein realistisches Aussehen aufweisen.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: Die "Top links"-Karte der Berichtsseite, bei einer Kampagne, deren E-Mail mindestens 3 unterschiedliche Links enthält und realistische Werte für Klicks/Unique/CTR aufweist.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: Die Empfängerseite mit geöffnetem Filterbereich und einer gemischten Liste von Zeilen (einige geöffnet, einige geklickt, einige geblockt), sodass die Engagement-Zustände sichtbar unterschieden werden können.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: Die Empfängerseite mit geöffnetem "Empfänger-Aktivitäts"-Modul für einen Empfänger, der mehrere Ereignistypen (geliefert, geöffnet, mindestens ein Klick-Eintrag mit Namen eines Links) aufweist.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: Ein Nahaufnahme der "Zugeordnete Umsätze"-Statistik-Karte der Berichtsseite, bei einer Kampagne mit einem protokollierten Ausgabenbetrag, sodass die Unterpunkte Orders/AOV/Umsatz pro E-Mail/ROAS vollständig gefüllt sind.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: Das Statistik-Karten-Grid des Campaign Studio-Dashboards, gescrollt/geschnitten, um das "Zugeordnete Umsätze (30d)"-Feld neben den angrenzenden Karten anzuzeigen, bei einem nicht-null Umsatz-Betrag.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: das vorhandene report-stat-cards.webp zeigt nur 6 Karten (Empfänger, Geliefert, Öffnungsquote, Klickquote, Bounce-Rate, Spam-Beschwerden) an. Das Statistik-Grid hat nun eine 7. Karte "Zugeordnete Umsätze" - erneut aufnehmen mit einer Kampagne, die sowohl Zuordnungsdaten als auch einen protokollierten Ausgabenbetrag hat, sodass alle 7 Karten in einem realistischen Zustand sichtbar sind.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Jede Kampagne, die Sie über Campaign Studio versenden, erhält ihre eigene **Berichtsseite** – eine einseitige Zusammenfassung davon, wie viele Menschen erreicht wurden, wie viele E-Mails tatsächlich eingetroffen sind und wie sich die Empfänger verhalten haben. Nutzen Sie sie, um zu prüfen, ob ein Versand problemlos verlaufen ist, frühzeitig ein Lieferprobleme zu erkennen, oder zu vergleichen, wie sich verschiedene Kampagnen im Zeitablauf verhalten.

## Öffnen eines Berichts

Aus **Campaign Studio > Kampagnen** finden Sie die Kampagne, die Sie überprüfen möchten, und klicken Sie auf das Diagramm-Symbol (**Bericht**) auf deren Karte.

![Statistik-Karten-Grid der Kampagnenberichtsseite, die Empfänger, gelieferte, Öffnungsquote, Klickquote, Bounce-Rate und Spam-Beschwerden zeigt](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Ein Bericht hat nur Zahlen, sobald eine Kampagne tatsächlich versendet wurde – eine Kampagne, die noch in **Entwurf** ist, zeigt alle Statistiken als Null, da es noch nichts zu messen gibt.

## Die Statistik-Karten

Bleiben Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe erhalten.

| Karte | Was sie anzeigt |
|------|---------------|
| **Empfänger** | Wie viele Abonnenten diese Kampagne angesprochen hat, plus eine Untertitel-Note, wie viele übersprungen wurden und, davon ausgehend, wie viele aus dem Grund, dass die Adresse auf Ihrer [Unterdrückungsliste](list-hygiene) steht. Ein Überspringen ist nicht immer eine Unterdrückung – Spwig überspringt beispielsweise auch einen Abonnenten, der keine verwendbare E-Mail-Adresse hat – daher werden die beiden Zahlen getrennt angezeigt. |
| **Eingeliefert** | Wie viele E-Mails tatsächlich von dem Empfänger-Mailserver akzeptiert und nie zurückgeworfen wurden, plus der **Lieferquote** – eingeliefert als Anteil jeder Sendung, die Spwig *versucht* hat (akzeptiert durch Ihren Mailserver oder Anbieter, egal, ob sie später zurückgeworfen wurde oder nicht). |
| **Öffnungsquote** | Der Anteil der *eingelieferten* E-Mails, die geöffnet wurden, plus die Rohanzahl der **geöffneten** E-Mails. |
| **Klickquote** | Der Anteil der *eingelieferten* E-Mails, die geklickt wurden, plus die Rohanzahl der **geklickten** E-Mails und der **Klick-Öffnungsquote** – Klicks als Anteil der Öffnungen, eine Bewertung, wie überzeugend Ihr Inhalt für diejenigen war, die die E-Mail bereits geöffnet haben. |
| **Rückgabeprozentsatz** | Der Anteil der *versuchten* Sendungen, die zurückgeworfen wurden, unterteilt in **harte** und **weiche** Rückgabeprozentsätze. |
| **Spam-Beschwerden** | Wie viele Empfänger die E-Mail als Spam oder Junk markiert haben, plus der **Beschwerdenprozentsatz** – Beschwerden als Anteil der *eingelieferten* E-Mails. |
| **Zugeordnete Umsätze** | Umsätze aus Bestellungen, die Spwig dieser Kampagne zuordnen kann, plus die Anzahl der Bestellungen, der Durchschnittsbestellwert (**AOV**), Umsatz pro E-Mail, und – sobald Sie den Kampagnenkosten eingegeben haben – deren **ROAS**. Siehe [Zugeordnete Umsätze](#attributed-revenue) unten. |

## Warum die Raten unterschiedliche Nenner verwenden

Öffnungsquote, Klickquote und Beschwerdenquote werden alle gegen **eingelieferte** E-Mails gemessen – die Empfänger, die die E-Mail tatsächlich sehen konnten – während Lieferquote und Rückgabeprozentsatz gegen **versuchte** Sendungen gemessen werden. Dies ist eine übliche Praxis in der E-Mail-Branche, und es ist der Grund, warum keine dieser Raten jemals über 100 % liegen kann: Eine E-Mail, die zurückgeworfen wurde, wurde nie eingeliefert, also kann sie nicht gegen Ihre Öffnungs- oder Klickquote zählen, und eine E-Mail, die nie versucht wurde (ein Überspringen), zählt nicht gegen eine davon.

## Harte Rückgabeprozentsätze vs. weiche Rückgabeprozentsätze

- **Harter Rückgabeprozentsatz** – die Adresse ist dauerhaft nicht lieferbar. Sie existiert nicht, oder der Domain-Name lehnt es ab, E-Mails für sie zu akzeptieren.
- **Weicher Rückgabeprozentsatz** – ein vorübergehendes Problem: ein voller Postfach, ein Empfänger-Server, der kurzzeitig nicht erreichbar war, und ähnliches. Weiche Rückgabeprozentsätze sind oft selbstauflösend.

Beobachten Sie den Unterschied, nicht nur die Gesamtanzahl. Ein ansteigender **harter Rückgabeprozentsatz** deutet oft darauf hin, dass Ihre Liste veraltete oder falsch geschriebene Adressen enthält; ein ansteigender **weicher Rückgabeprozentsatz** ist oft ein vorübergehender Störfall auf der Seite des Empfängers. Jeder harte Rückgabeprozentsatz, jeder Spam-Beschwerde und eine Adresse, die mehrere weiche Rückgabeprozentsätze aufweist, fließen in Spwigs automatische [Unterdrückungsliste](list-hygiene) – Sie müssen sich nicht selbst darum kümmern, aber der Bericht ist der Ort, an dem Sie zuerst einen Anstieg bemerken werden, der untersucht werden sollte.

## Zugeordnete Umsätze

Weil Ihr Geschäft und der Campaign Studio in derselben Systemumgebung sind, benötigt Spwig keine externe Analyplattform oder einen Tracking-Pixel, um Ihnen zu sagen, ob eine Kampagne tatsächlich Verkäufe verursacht hat. Wenn ein Kunde auf einen Link in dieser Kampagnen-E-Mail klickt und auf Ihrem Geschäft landet, kann Spwig diesen Besuch bis zur Kasse verfolgen und den Umsatz des resultierenden Auftrags der Kampagne zuordnen – das ist das, was die **Zugeordnete Umsätze**-Karte anzeigt.

Die Untertitel der Karte unterteilt die Zahl weiter:

- **Bestellungen** – wie viele Bestellungen dieser Kampagne zugeordnet sind.
- **AOV** – der Durchschnittsbestellwert dieser Bestellungen.
- **Umsatz pro E-Mail** – zugeordnete Umsätze geteilt durch die Anzahl der E-Mails *eingeliefert*, der gleiche Nenner, den der Bericht für Öffnungsquote und Klickquote verwendet.
- **ROAS** – Return on ad spend, wird nur angezeigt, sobald Sie einen **Kosten**-Wert für die Kampagne selbst eingegeben haben.

Es wird berechnet als zugeordnete Umsätze geteilt durch Kosten.

Wenn der Ausgabenbetrag in einer anderen Währung als der Standardwährung Ihres Ladens erfasst wurde, versteckt Spwig die ROAS, anstatt einen Wert anzuzeigen, der nicht direkt vergleichbar ist – geben Sie die Ausgaben in der Basiswährung Ihres Ladens ein, um sie zu sehen.

Einige Dinge, die Sie über die Berechnung dieses Werts wissen sollten:

- **Es handelt sich um Klicks, nicht um Öffnungen.** Ein Kunde muss auf einen verfolgten Link in der E-Mail klicken und Ihre Website besuchen – eine reine Öffnung allein verleiht kein Umsatz. Dies ist beabsichtigt: Die Öffnungsverfolgung ist aufgrund der Tatsache, dass Dienste wie Apple Mail Privacy Protection Bilder für nahezu jede Nachricht vorladen, zunehmend unzuverlässig, wodurch die Öffnungszahlen unabhängig davon, ob jemand die E-Mail tatsächlich gelesen hat, erhöht werden.
- **Es folgt dem Attribution-Modell Ihres Ladens.** Standardmäßig ist dies **last non-direct touch** mit einem 90-Tage-Retrospektivfenster – derselbe Klick muss innerhalb dieses Fensters zu einem Kauf führen, um als erfasst zu gelten, und ein späterer direkter Besuch erlischt den bereits erzielten Kredit durch diesen Kampagnen-Klick nicht.
- **Es respektiert die Analyse-Einwilligung.** Nur Besucher, die in Ihrem Cookie-Banner die Analyse-Einwilligung erteilt haben, werden verfolgt (falls Sie kein Einwilligungsbanner betreiben, folgt die Verfolgung der eigenen Einwilligungspolitik Ihres Ladens). Ein Kunde, der die Einwilligung abgelehnt hat, kann dennoch kaufen – seine Bestellung wird einfach nicht einer Kanal zugeordnet, einschließlich dieses.
- **Es ist nicht rückwirkend.** Die Umsatzverfolgung umfasst nur Kampagnen, die nach dem Aktivieren der Attribution-Verfolgung für Ihren Laden gesendet wurden. Eine Kampagne, die davor gesendet wurde, zeigt hier keinen zugeordneten Umsatz an, auch wenn sie echte Verkäufe verursacht hat, einfach weil Spwig für sie keinen Klick-Daten-Record hat.
- **A/B-Tests und Wiederholungskampagnen summieren ebenfalls ihre zugeordneten Umsätze auf** – siehe [Berichte zu einem A/B-Test](#berichte-zu-einem-a-b-test) unten.

Sie finden außerdem eine Karte **Zugeordneter Umsatz (30d)** auf dem Dashboard des Kampagnen-Studio, die den zugeordneten Umsatz aus E-Mails aus allen Kampagnen in den letzten 30 Tagen zusammenfasst – ein schneller Überblick, ohne eine individuelle Berichtsdatei öffnen zu müssen. Für eine lagerweite Übersicht, die jeden Kanal, nicht nur E-Mails – organische Suchanfragen, soziale Medien, Partner usw. – einschließt, siehe das [Umsatzzuordnungs-](/help/umsatzzuordnung) Dashboard unter **Insights**.

## Engagement im Zeitablauf

Unter den Stat-Karten zeigt der **Engagement im Zeitablauf**-Chart drei Linien – **Gesendet**, **Geöffnet** und **Klicks** – einen Punkt pro Tag, wobei die 30 Tage bis heute abgedeckt sind (oder weniger, falls die Kampagne nicht so lange gesendet hat – der Chart fängt niemals früher als am Tag der ersten Sendung der Kampagne an).

Einige Dinge, die Sie über die Zählweise der Linien wissen sollten:

- **Geöffnet** und **Klicks** zählen jeden Empfänger einmal – den Tag ihrer *ersten* Öffnung oder *ersten* Klicks – nicht jedes Mal, wenn sie die E-Mail erneut öffnen oder einen Link erneut klicken. Dies verhindert, dass der Chart durch eine Handvoll Leute, die dieselbe E-Mail mehrmals öffnen, verzerrt wird.
- Die Gesamtwerte dieses Diagramms stimmen mit den Stat-Karten darüber überein: **Gesendet** spiegelt den Versuch wider, die E-Mail zu liefern, während **Geöffnet** und **Klicks** anhand der gelieferten E-Mails gemessen werden, genau wie bei den Karten **Öffnungsquote** und **Klickquote**.
- Das Diagramm wird erst angezeigt, wenn die Kampagne mindestens einen Versand aufweist – eine Kampagne, die noch im **Entwurf**-Status ist, zeigt stattdessen die Meldung "Noch keine Versuche" an, genau wie die Stat-Karten.

Verwenden Sie dieses Diagramm, um die *Form* eines Versands zu sehen, nicht nur die Endzahlen – eine Kampagne, die an eine große Liste gesendet wird, zeigt oft einen scharfen Anstieg bei den Öffnungen am ersten oder zweiten Tag, der sich danach verringert. Ein zweiter Anstieg ein paar Tage später kann auf einen Warteschlangen-Status des E-Mail-Servers eines Empfängers hindeuten, oder darauf, dass Ihr Betreffzeile später als üblich wahrgenommen wird.

## Top-Links

Wenn Ihre E-Mail Links enthält und mindestens ein Empfänger einen davon geklickt hat, wird unter dem Diagramm eine **Top-Links**-Tabelle angezeigt, die jeden verfolgten Link nach Beliebtheit auflistet.

Bewahren Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

| Spalte | Anzeige |
|--------|---------------|
| **Link** | Die Ziel-URL, wie sie in Ihrer E-Mail angezeigt wurde. |
| **Klicks** | Die Gesamtanzahl der Klicks auf diesen Link, einschließlich wiederholter Klicks vom selben Empfänger. |
| **Eindeutig** | Wie viele verschiedene Empfänger diesen bestimmten Link mindestens einmal angeklickt haben. |
| **CTR** | Die **Klickrate** dieses Links — die Anzahl der **Eindeutigen** Klicks als Anteil der zugestellten E-Mails. Dies verwendet denselben Nenner wie die **Klickrate**-Karte im Bericht, sodass Sie die Wirkung eines einzelnen Links direkt mit der gesamten Klickleistung der Kampagne vergleichen können. |

Wenn Ihre E-Mail auf mehrere Produkte oder eine Mischung aus Call-to-Action-Buttons verweist, ist diese Tabelle der schnellste Weg, um zu sehen, welcher Link tatsächlich den Klick verdient hat — nützlich, um zu entscheiden, was beim nächsten Mal prominenter dargestellt werden sollte.

## Empfänger

Klicken Sie oben im Bericht auf **Empfänger**, um eine vollständige, durchsuchbare Liste aller Personen zu öffnen, an die diese Kampagne gesendet wurde, einschließlich des Zustellungsstatus und der Interaktion jeder Person.

Zwei Möglichkeiten, die Liste einzugrenzen:

- **Suche** — filtert nach E-Mail-Adresse (eine Teilübereinstimmung funktioniert, sodass das Eingeben eines Teils einer Domain oder eines Namens ausreicht).
- **Interaktion** — filtert nach einem Zustand auf einmal: **Geöffnet**, **Geklickt**, **Zugestellt, nicht geöffnet** oder **Abgeprallt**. Lassen Sie es auf **Alle** stehen, um die vollständige Liste zu sehen.

Die Liste zeigt jeweils die 100 neuesten übereinstimmenden Empfänger an, beginnend mit den neuesten — die Anzahl über der Liste spiegelt immer die tatsächliche Gesamtzahl wider, die Ihren aktuellen Filtern entspricht, selbst wenn sie größer ist als die angezeigte Anzahl. Bei einem großen Versand grenzen Sie die Liste zuerst mit Suche oder Interaktion ein, anstatt durch alle Einträge zu scrollen.

### Anzeigen der Aktivitätschronik eines Empfängers

Klicken Sie auf das Aktivitätssymbol in der Zeile eines beliebigen Empfängers, um dessen **Empfängeraktivität**-Chronik zu öffnen — alle erfassten Ereignisse für die Kopie der E-Mail dieser Person, in der Reihenfolge: zugestellt, geöffnet, geklickt (mit Angabe des Links), abgeprallt (mit dem Grund für das Abprallen), als Spam markiert oder abgemeldet, jeweils mit eigenem Zeitstempel.

Dies ist der schnellste Weg, um eine spezifische Frage zu einem einzelnen Kunden zu beantworten — zum Beispiel, um zu bestätigen, ob ein bestimmter Abonnent eine Kampagne tatsächlich erhalten hat, bevor Sie ihn über einen anderen Kanal kontaktieren, oder um zu prüfen, welchen Link ein Kunde angeklickt hat, bevor er eine Bestellung aufgegeben hat.

## Berichte zu einem A/B-Test

Wenn die angezeigte Kampagne der Container für einen [A/B-Test](ab-testing) ist, aggregiert ihr Bericht über **jede Variante** — den gesamten Test, kombiniert, einschließlich **Attributierter Umsatz** — anstatt eine einzelne Variante allein anzuzeigen. Um zu sehen, wie jede einzelne Variante abgeschnitten hat, öffnen Sie stattdessen die eigene Ergebnisseite des Tests. Eine [wiederkehrende Kampagne](recurring-campaigns) funktioniert auf die gleiche Weise: Ihr Bericht fasst alle gesendeten Vorkommnisse zusammen.

## Was gut aussieht

Es gibt keine einzelne gesunde Zahl, die für jeden Shop oder jede Liste passt — Publikum, Branche und Inhalt verschieben alle die Baseline — aber einige Muster sind bei jeder Kampagne wertvoll zu beobachten:

- Eine **Abprallrate**, die überwiegend aus weichen Abprallern besteht, mit seltenen harten Abprallern, deutet auf eine saubere, gut gepflegte Liste hin. Ein plötzlicher Anstieg der harten Abpraller ist vor dem nächsten Versand einer Untersuchung wert.
- **Spam-Beschwerden** nahe null sind das Ziel bei jedem Versand. Beschwerden schaden Ihrem Absender-Ruf mehr als fast alles andere — siehe [Liste Hygiene](list-hygiene), warum sie über diese eine Kampagne hinaus wichtig sind.
- Eine **Klick-zu-Öffnungsrate**, die im Verhältnis zu Ihrer Öffnungsrate gesund ist, zeigt Ihnen, dass die Personen, die geöffnet haben, den Inhalt als handlungsrelevant empfunden haben — eine niedrige Klick-zu-Öffnungsrate bei einer starken Öffnungsrate deutet in der Regel darauf hin, dass die Betreffzeile besser funktioniert hat als der Inhalt im Inneren.

## Tipps

- Prüfen Sie das Berichtsdatum etwas später nach dem Versenden, nicht sofort — Öffnungen und Klicks (und einige Fehlerberichte) können einige Zeit brauchen, um von Ihrem E-Mail-Anbieter zu kommen.
- Wenn **Gesendet** niedriger ist, als erwartet, prüfen Sie zuerst die Aufschlüsselung der **Empfänger**-Karte — eine Reihe von Auslassungen aufgrund von Unterdrückung ist oft die wahre Ursache, nicht ein Lieferproblem.
- Nutzen Sie den Bericht, um eine Kampagne mit Ihren eigenen früheren Sendungen zu vergleichen, anstatt sie mit einer allgemeinen Branchenzahl zu vergleichen — Ihre Liste, Inhalte und Zielgruppe sind es, die Ihre realistische Ausgangsposition bestimmen.
- Ein Anstieg von Beschwerden bei einer bestimmten Sendung lohnt es, genauer auf den Inhalt oder die Zielgruppenansprache dieser Kampagne zu achten, nicht nur, um weiterzumachen.
- Bei einer A/B-Test-Kampagne lesen Sie diesen Bericht, um das Gesamtergebnis zu erhalten, und die Seite [A/B-Test-Ergebnisse](ab-testing), um zu erfahren, welche Variante tatsächlich gewonnen und um wie viel gewonnen hat.
- Nutzen Sie die Tabelle **Top-Links**, um das am meisten geklickte Link zu finden, und prüfen Sie, ob es mit dem übereinstimmt, was Sie *wollten*, dass die Empfänger klicken — wenn ein sekundäres Link Ihren Hauptaufruf zur Aktion schlägt, lohnt es sich, ihn beim nächsten Mal in der E-Mail höher zu platzieren.
- Die Filter **Geöffnet** und **Klicks** auf der Seite **Empfänger** sind eine schnelle Möglichkeit, eine Zielgruppe für eine Nachverfolgung zu erstellen — beispielsweise, um zu prüfen, wer geöffnet, aber nicht geklickt hat, bevor Sie eine Erinnerungssendung an den Rest der Liste senden.
- Wenn Sie für eine Promotion um eine Sendung bezahlt haben — einen vergrößerten Social-Media-Post, eine Influencer-Erwähnung, einen bezahlten Listen-Verleih — tragen Sie dies als **Ausgaben** der Kampagne ein, um **ROAS** im Bericht zu aktivieren.

Das ist der schnellste Weg, um zu sehen, welche Arten von Sendungen tatsächlich wiederholt werden sollten.