---
title: Listenhigieneprobleme und Unterdrückung
---

Eine E-Mail-Adresse, die einen Hard-Bounce verursacht, Ihre E-Mails als Spam markiert oder häufig nicht empfangen werden kann, stellt die gesamte Liste in Gefahr – E-Mail-Postfächer beurteilen Ihre Absenderreputation anhand der Sauberkeit Ihres Versands, und eine unreine Liste bedeutet, dass *jeder* Kampagnenversand häufiger in den Spam-Ordner gelangt. Campaign Studio schützt Sie automatisch vor diesem Problem mit **Listenhigieneproblemen**: Es überwacht unempfangbare und beschwerdefreudige Adressen und unterbricht den Versand von Werbe-E-Mails an sie, ohne dass Sie dafür etwas tun müssen.

Dies ist von Abmeldungen unterschieden. Eine abgemeldete Adresse hat ihre Zustimmung zurückgezogen; eine **unterdrückte** Adresse ist eine, die Spwig erkannt hat, für unsafe oder unmöglich zu versenden, unabhängig von der Zustimmung.

## Wie Adressen unterdrückt werden

Spwig fügt eine Adresse der **Unterdrückungsliste** automatisch hinzu, wenn:

| Auslöser | Was es bedeutet |
|---------|----------------|
| **Hard-Bounce** | Die Adresse existiert nicht oder der Domain-Server hat den E-Mail-Versand abgelehnt – dauerhaft nicht lieferbar. |
| **Spam-Beschwerde** | Ein Empfänger hat Ihre E-Mail als Spam oder Junk-Mail markiert. |
| **Wiederholte Soft-Bounces** | Die Adresse hat innerhalb eines 30-Tage-Intervalls 5 Mal einen Soft-Bounce (Postfach voll, Server vorübergehend nicht erreichbar) erzielt. Ein einzelner Soft-Bounce wird als vorübergehender Störfall betrachtet und ignoriert – erst ein Muster wiederholter Fehlschläge löst die Unterdrückung aus. |
| **Manuell blockiert** | Sie haben die Adresse selbst hinzugefügt. |

Sobald eine Adresse unterdrückt wird, hört Spwig sofort mit dem Versand von **Kampagnen** oder **Journeys**-E-Mails auf – Sie müssen dafür keine weiteren Maßnahmen ergreifen.

## Aus welcher Quelle stammt das Signal

Spwig kann von einem Bounce oder einer Beschwerde anhand verschiedener Quellen erfahren, die als **Quelle** auf jeder unterdrückten Adresse angezeigt werden:

- **Bei Versand abgelehnt** – Ihr E-Mail-Server hat die Adresse sofort abgelehnt, als Spwig versuchte, ihr eine E-Mail zu senden.
- **Provider-Webhook** – Wenn Sie einen E-Mail-Provider (z. B. SendGrid, Amazon SES, Mailgun oder Postmark) verbunden haben, meldet dieser Provider Bounces und Beschwerden in Echtzeit an Spwig zurück.
- **E-Mail-Gateway** – Wenn Ihr Shop über das Spwig-hosted E-Mail-Gateway sendet, zieht Spwig die Bounce-Meldungen vom Gateway für Sie ab.
- **Manuell hinzugefügt** – Sie haben die Adresse selbst aus dem Admin-Bereich eingetragen.

Sie müssen nichts konfigurieren, um davon zu profitieren – egal, auf welche Weise Sie E-Mails versenden, Spwig überwacht Fehler und hält Ihre Liste sauber.

## Das Campaign Studio-Dashboard

Öffnen Sie **Campaign Studio** und suchen Sie nach dem **unterdrückten Adressen**-Karten. Sie zeigt die Gesamtanzahl der derzeit unterdrückten Adressen an, sowie die Anzahl der neuen Adressen in den letzten 30 Tagen. Klicken Sie auf die Karte, um die vollständige Unterdrückungsliste zu öffnen.

![Das Dashboard des Campaign Studio mit der Karte "unterdrückte Adressen", die eine Gesamtanzahl und einen "neuen in den letzten 30 Tagen"-Zähler anzeigt](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Ein stetig ansteigender Wert ist normal – jede Liste sammelt im Laufe der Zeit einige schlechte Adressen, da Menschen ihre Jobs wechseln, Konten schließen oder E-Mails-Postfächer verlassen. Ein plötzlicher Anstieg ist es wert, untersucht zu werden; siehe [E-Mail-Ausgang](email-outbox), um zu prüfen, ob ein bestimmter Versand eine ungewöhnliche Anzahl von Fehlern verzeichnet hat.

## Die Unterdrückungsliste

Klicken Sie auf **Unterdrückungen**, um jede unterdrückte Adresse, den Grund für die Unterdrückung und die Quelle des Signals anzuzeigen.

![Die Unterdrückungsliste mit unterdrückten Adressen und den Spalten "Grund" und "Quelle"](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Verwenden Sie die Filter auf der rechten Seite, um die Liste nach **Grund** oder **Quelle** zu filtern – beispielsweise, um jede manuell blockierte Adresse zu überprüfen oder alles, was über einen Provider-Webhook hereingekommen ist.

## Manuelle Hinzufügung einer Adresse

Um eine Adresse selbst zu blockieren – eine bekannte Missbrauchsadresse, einen Wettbewerber, der Ihre Newsletter abgräbt, oder etwas anderes, was Sie von Ihrer Liste fernhalten möchten – klicken Sie auf **+ Unterdruckte Adresse hinzufügen** und füllen Sie folgendes aus:

- **E-Mail** — die zu blockierende Adresse
- **Grund** — wählen Sie **Manuell blockiert** für einen manuell hinzugefügten Eintrag
- **Quelle** — wählen Sie **Manuell hinzugefügt**
- **Details** — ein optionaler Hinweis, der erklärt, warum (nützlich für Ihre eigenen Aufzeichnungen und für Mitarbeiter, die die Liste später überprüfen)

Speichern Sie den Eintrag, und Spwig sendet an diese Adresse sofort keine Kampagnen- oder Journey-E-Mails mehr.

## Wann sollte ich eine Adresse freigeben?

Das Freigeben (Aufheben der Unterdrückung) einer Adresse sollte selten und bewusst erfolgen. Führen Sie dies nur durch, wenn Sie sicher sind, dass das zugrunde liegende Problem tatsächlich behoben wurde – zum Beispiel:

- Ein Kunde teilt Ihnen mit, dass sein Postfach voll war und es inzwischen geleert wurde.
- Eine Adresse wurde aufgrund einer Serie von Soft-Bounces unterdrückt, die Sie wissen, durch eine vorübergehende Störung bei ihrem E-Mail-Anbieter verursacht wurde, nicht durch ein ungültiges Postfach.
- Sie haben eine Adresse manuell blockiert und entscheiden später, dass die Blockade ein Fehler war.

Um eine Adresse freizugeben, öffnen Sie sie in der Liste der Unterdrückungen und löschen Sie den Eintrag – dies hebt die Blockade auf, sodass die Adresse wieder E-Mails empfangen kann. Geben Sie eine Adresse mit einem Hard-Bounce nicht einfach deshalb frei, weil es lästig ist, einen Abonnenten zu verlieren; die Adresse existiert nicht, und ein erneutes Senden daran wird nur erneut abprallen und Ihren Ruf ein zweites Mal kosten. Ebenso hilft das Freigeben einer Adresse mit einer Spam-Beschwerde selten – dieser Empfänger hat seinem Postfachanbieter mitgeteilt, dass er Ihre E-Mails nicht erhalten möchte, und ein erneutes Senden an ihn birgt das Risiko einer weiteren Beschwerde.

## Was nicht betroffen ist

Unterdrückung gilt nur für **Marketing-Kampagnen und Journeys**, die über Campaign Studio gesendet werden. Sie betrifft **transaktionale E-Mails** nicht – Bestellbestätigungen, Versandupdates, Passwort-Resets und andere E-Mails, die Ihr Shop als Teil einer Bestellung oder einer Kontoaktion sendet, werden immer zugestellt, auch an eine unterdrückte Adresse. Die Unterdrückung dient dem Schutz Ihres Marketing-Sender-Rufs; sie ist keine allgemeine E-Mail-Blocklist für Ihren Shop.

## Tipps

- Kämpfen Sie nicht gegen das System, indem Sie jeden Hard-Bounce, den Sie sehen, manuell freigeben – ein Hard-Bounce bedeutet, dass die Adresse weg ist, und ein erneutes Hinzufügen zu Ihren Sendeaktionen wird nur erneut abprallen.
- Prüfen Sie die Liste der Unterdrückungen nach einem großen Versand, wenn Ihre Öffnungsrate ungewöhnlich niedrig aussieht – eine Welle von Soft-Bounces auf einer gemeinsamen Domain (z. B. ein Unternehmens-Mailserver mit Problemen) kann ein Anzeichen für ein vorübergehendes Zustellproblem sein, das es wert ist, mit Ihrem Anbieter untersucht zu werden.
- Wenn Sie von einer anderen Plattform zu Spwig wechseln, importieren Sie Ihre gesamte alte Blocklist nicht manuell als Unterdrückungen – lassen Sie Spwig stattdessen von echten Bounces und Beschwerden auf dieser Liste lernen, damit Sie Adressen nicht versehentlich blockieren, die ohne Probleme zugestellt worden wären.
- Überprüfen Sie die Spalte **Quelle** gelegentlich – viele Einträge mit **Provider webhook** bestätigen, dass die Bounce-Meldung Ihres E-Mail-Anbieters verbunden und funktionsfähig ist.
- Halten Sie das Feld **Details** bei der manuellen Blockade einer Adresse aussagekräftig; es ist die einzige Aufzeichnung darüber, warum diese Entscheidung getroffen wurde, wenn die Zeit vergangen ist.