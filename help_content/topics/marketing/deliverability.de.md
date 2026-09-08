---
title: Runbook für die E-Mail-Lieferbarkeit
---

Eine E-Mail *versenden* zu lassen, ist einfach. Sie in den Posteingang statt in den Spam-Ordner zu bekommen, ist die eigentliche Aufgabe – und E-Mail-Anbieter wie Gmail und Yahoo stellen nun strenge technische Anforderungen, bevor sie eine E-Mail überhaupt in Betracht ziehen. Dieses Runbook erklärt Schritt für Schritt, was konfiguriert werden muss und in welcher Reihenfolge, damit Ihre Bestellbestätigungen und Kampagnen dort ankommen, wo Kunden sie sehen können.

Nichts hier ist eine einmalige Aufgabe. Die Lieferbarkeit ist ein Zustand, den Sie über die Zeit aufbauen und schnell wieder verlieren können – die Checkliste am Ende lohnt es sich, immer wieder zu überprüfen, wenn etwas nicht stimmt.

## Warum das wichtig ist

Jeder große Posteingangs-Anbieter bewertet eingehende E-Mails anhand des Absender-Rufs, bevor er entscheidet, ob sie zugestellt, in den Spam-Ordner verschoben oder ganz abgelehnt werden sollen. Seit 2024 haben Gmail und Yahoo dies für alle, die in relevantem Umfang senden, in explizite **Anforderungen für Massenabsender** formalisiert:

- **Domain authentifizieren** – gültige SPF-, DKIM- und DMARC-Einträge.
- **Abmeldung leicht machen** – eine funktionierende, reibungslose Abmeldung in jeder Marketing-E-Mail.
- **Spam-Beschwerden niedrig halten** – Massenabsender, die eine Beschwerderate von etwa 0,3 % überschreiten, riskieren, dass ihre E-Mails abgelehnt oder direkt in den Massenordner verschoben werden; das sicherste Ziel liegt deutlich unter 0,1 %.

Werden diese Anforderungen nicht erfüllt, leidet nicht nur der Marketing-Versand – ein beschädigter Domain-Ruf kann auch transaktionale E-Mails (Bestellbestätigungen, Passwort-Resets) in den Spam ziehen, da Gmail und Yahoo den Ruf zunehmend auf Ebene der Absender-Domain und nicht nur pro Nachrichtentyp bewerten. Die folgenden Schritte zeigen, wie Sie alle drei Punkte erfüllen.

## Schritt 1: Ihre Absender-Domain authentifizieren

SPF, DKIM und DMARC sind DNS-TXT-Einträge, die den empfangenden Mailservern beweisen, dass E-Mails, die angeblich von Ihrer Domain stammen, tatsächlich von Ihnen gesendet wurden. Wie Sie sie einrichten, hängt davon ab, welchen Versandmodus Ihr Shop verwendet – alle drei werden unter **E-Mail-Konfiguration** in der Admin-Seitenleiste konfiguriert (dies öffnet die Liste der E-Mail-Konten; siehe [E-Mail-Konfiguration](email-configuration) für die vollständige Anleitung zur Kontoeinrichtung).

| Versandmodus | So funktioniert die Authentifizierung |
|---|---|
| **Integriertes SMTP** (der eigene E-Mail-Server von Spwig) | Spwig generiert automatisch ein DKIM-Schlüsselpaar für Ihre Domain. Fügen Sie ein E-Mail-Konto hinzu, und **Schritt 4** des Einrichtungswizards zeigt Ihren SPF-, DKIM- und DMARC-Status sowie den exakten Eintrag an, der hinzugefügt werden muss, mit Kopieren-in-die-Zwischenablage-Funktion und anbieter-spezifischen Anweisungen für Cloudflare, GoDaddy, Namecheap und AWS Route 53. Der gleiche DKIM-DNS-Eintrag wird später auch auf der eigenen Admin-Seite des Kontos unter **Konfigurierte DKIM-Schlüssel** angezeigt, falls Sie ihn erneut finden müssen. |
| **Generisches SMTP** (ein eigener Anbieter wie SendGrid, Mailgun, Amazon SES oder Google Workspace, verbunden über SMTP-Zugangsdaten) | Die Authentifizierung erfolgt teilweise im eigenen Dashboard dieses Anbieters. Der DNS-Schritt des Einrichtungswizards enthält tabellarische Anweisungen speziell für Gmail, Outlook, SendGrid, Mailgun und Amazon SES – jede erklärt, was im Anbieter-Console konfiguriert werden muss (z. B. die Verifizierung einer Absender-Domain in SendGrid) und welche resultierenden DNS-Einträge bei Ihrem DNS-Host hinzugefügt werden sollen. |
| **Von Spwig gehostetes Mail-Gateway** | Verfügbar in Spwig-gehosteten Plänen als verwaltete Versandoption. Es signiert ausgehende E-Mails automatisch mit DKIM und sendet standardmäßig von einer Adresse auf der eigenen verifizierten Domain von Spwig, sodass es ohne Einrichtung funktioniert. Wenn Sie über das Gateway von Ihrer eigenen Domain senden möchten, sprechen Sie mit Ihrem Hosting-Anbieter über die Verifizierung – dies ist ein verwalteter Dienst und kein selbstbedienbarer DNS-Workflow. |

![Schritt 4 des E-Mail-Konto-Einrichtungswizards, der die SPF/DKIM/DMARC-Validierung, DNS-Anbieter-Tabs und einen erweiterten DKIM-Eintrag zum Kopieren zeigt](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Das Panel „Konfigurierte DKIM-Schlüssel“ eines bestehenden integrierten SMTP-E-Mail-Kontos, mit dem DNS-TXT-Eintrag und einer Schaltfläche „DNS-Eintrag kopieren“](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Unabhängig davon, in welchem Modus Sie arbeiten, ist das **Hinzufügen des DNS-Eintrags immer ein externer Schritt** – Sie führen es bei Ihrem Domain-Registrar oder DNS-Anbieter (Cloudflare, GoDaddy, Namecheap, Route 53 oder wo immer Ihre Domain-Namensserver hinweisen) durch, nicht innerhalb von Spwig.

Spwig kann Ihnen genau sagen, was Sie hinzufügen müssen, und prüfen, ob es live ist, kann aber nicht in Ihren Registrar eingreifen und es für Sie hinzufügen.

Ein paar Dinge, die Sie vor Beginn wissen sollten:

- **DNS-Änderungen sind nicht sofort wirksam.** Die Verbreitung kann zwischen ein paar Minuten und 48 Stunden dauern. Der Prüfschritt des Assistenten zeigt einen Eintrag als fehlerhaft oder nicht vorhanden an, bis er tatsächlich verarbeitet wurde – das ist zu erwarten, nicht ein Zeichen dafür, dass etwas schiefgelaufen ist.
- **Pro Domain ist nur ein SPF-Eintrag erlaubt.** Wenn Sie bereits einen haben (z. B. von Google Workspace, einem anderen E-Mail-Dienst usw.), fügen Sie Ihren neuen Absender dem vorhandenen Eintrag mit `include:` hinzu, anstatt einen zweiten SPF-TXT-Eintrag zu erstellen – zwei SPF-Einträge werden die Authentifizierung für alle brechen.
- **DMARC benötigt SPF oder DKIM, um bereits zu funktionieren.** Richten Sie es erst ein, nachdem SPF und DKIM beide überprüft wurden.

## Schritt 2: Verwenden Sie eine echte Absender-Identität

Sobald Ihre Domain authentifiziert ist, stellen Sie sicher, dass das, was die Empfänger tatsächlich sehen, dies unterstützt:

- **Absender-Adresse** – verwenden Sie eine Adresse auf Ihrer eigenen authentifizierten Domain (`bestellungen@ihrshop.com`), nie eine Adresse eines kostenlosen Anbieters (`ihrshop@gmail.com`). Eine Absender-Adresse eines kostenlosen Anbieters kann überhaupt nicht durch Ihre SPF/DKIM/DMARC-Einträge authentifiziert werden, und E-Mail-Anbieter betrachten sie als starkes Spam-Signal eines Ladens.
- **Absender-Name** – verwenden Sie einen erkennbaren Namen Ihres Ladens, nicht ein generisches Etikett wie „Benachrichtigungen“ oder „Keine Antwort“.
- **Antwort-Adresse** – legen Sie eine überwachte Adresse fest. Eine nicht überwachte `keine_antwort@`-Adresse, die nicht antwortet oder Antworten stillschweigend löscht, ist selbst ein schwaches Reputationssignal, und sie blockiert den einen Kanal, den Kunden haben, um Ihnen mitzuteilen, dass etwas schiefgelaufen ist.

Richten Sie alle drei unter **E-Mail-Konfiguration > (Ihr Konto) > Absender-Konfiguration** ein – siehe [E-Mail-Konfiguration](email-configuration) für eine vollständige Anleitung zu den Feldern.

## Schritt 3: Aufwärmen, bevor Sie skalieren

Eine Domain oder IP-Adresse mit keinem Versand-Verlauf hat noch keine Reputation – gut oder schlecht – und E-Mail-Anbieter sind vorsichtig mit dem Unbekannten. Ein riesiger erster Schuss von einer brandneuen Domain sieht statistisch identisch mit einem Spammer, der eine neue Kampagne startet, und kann in den Massenpost-Ordner gelandet sein, obwohl jeder technische Punkt abgehakt ist.

- Beginnen Sie kleiner. Senden Sie Ihre ersten paar Kampagnen an Ihre am meisten engagierten, am wahrscheinlichsten öffnenden Zielgruppen, anstatt Ihre gesamte Liste gleichzeitig zu versenden – siehe [Zielgruppen](audiences), um eine gezielte Start-Gruppe zu erstellen.
- Erhöhen Sie das Volumen schrittweise in den ersten Wochen, anstatt direkt zu Volllisten-Versand zu springen.
- Wenn Sie eine bestehende Liste von einer anderen Plattform migrieren, behandeln Sie dies ebenfalls als Tag 1 für die Reputation – der Versand-Verlauf Ihrer alten Plattform transferiert nicht mit der Domain.

## Schritt 4: Listen sauber halten

Jede Beschwerde oder Rückmeldung kostet Ihre Reputation, und beide sind größtenteils eine Funktion davon, wer auf Ihrer Liste ist und wie sie dorthin gekommen sind:

- **Senden Sie nur an Personen, die zugestimmt haben.** Importierte Kontakte, gekaufte Listen und abgegriffene Adressen sind der schnellste Weg, um Spam-Beschwerden und harte Rückmeldungen zu erhöhen.
- **Verwenden Sie die Doppel-Opt-in-Methode.** Der Anmeldeprozess von Spwig verifiziert die E-Mail-Adresse eines Abonnenten, bevor er Marketing-E-Mails sendet – siehe [Kommunikationsvorlieben](communication-preferences), wie dies konfiguriert wird.
- **Lassen Sie die automatische Unterdrückung von Spwig ihre Arbeit tun.** Spwig beobachtet, ob es zu harten Rückmeldungen, Spam-Beschwerden und wiederholten weichen Rückmeldungen kommt, und unterbricht den Versand dieser Adressen automatisch, ohne Setup-Anforderungen – siehe [Listen-Sauberkeit und Unterdrückung](list-hygiene), wie dies genau funktioniert und wann (selten) es übersprungen werden sollte.
- **Entfernen Sie unaktive Abonnenten periodisch**, anstatt die gleichen unengagierten Adressen unendlich lang zu versenden – eine sich verkleinernde Liste, die öffnet und klickt, ist wertvoller für Ihre Reputation als eine große Liste, die es nicht tut.

## Schritt 5: Überwachen

Bewahren Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

Liefbarkeitsprobleme zeigen sich in den Kennzahlen, bevor ein Kunde Ihnen mitteilt, dass eine E-Mail nicht angekommen ist.

Öffnen Sie nach jedem Versand den [Bericht](campaign-reports) einer Kampagne und beobachten Sie Folgendes:

| Kennzahl | Worauf zu achten ist |
|---|---|
| **Bounce-Rate** | Überwiegend weiche Bounces sind normal; ein steigender Anteil an **harten Bounces** bedeutet, dass sich in Ihrer Liste veraltete oder ungültige Adressen ansammeln. |
| **Spam-Beschwerden** | Sollte bei jedem Versand nahe bei null liegen. Halten Sie diesen Wert deutlich unter der Schwelle von etwa 0,3 %, die bei Gmail und Yahoo die Durchsetzung der Regeln für Massenversender auslöst – behandeln Sie selbst einen kleinen Anstieg als sofortige Untersuchungsangelegenheit. |
| **Öffnungsrate / Klick-zu-Öffnungs-Rate** | Ein plötzlicher, unerklärlicher Rückgang über mehrere Versände an dieselbe Liste hinweg (nicht nur bei einer einzigen Kampagne) kann ein frühes Anzeichen dafür sein, dass Mails im Spam-Ordner statt im Posteingang landen, noch bevor sich die Bounce- oder Beschwerde-Zahlen verändern. |

Prüfen Sie außerdem regelmäßig die Karte **Unterdrückte Adressen** im Dashboard des Campaign Studio – ein stetiger, kleiner Zufluss ist normaler Listenabbau, aber ein plötzlicher Anstieg sollte vor Ihrem nächsten Versand untersucht werden (siehe [Liste Hygiene](list-hygiene)).

![Die Statistik-Karte für unterdrückte Adressen im Campaign-Studio-Dashboard](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Wenn etwas ansteigt: Pausieren Sie und prüfen Sie zuerst, ob Ihre DNS-Einträge noch gültig sind (eine abgelaufene Domainverlängerung oder eine versehentliche DNS-Änderung kann SPF/DKIM stillschweigend beschädigen), und schauen Sie sich dann an, was sich am Inhalt oder Publikum des auslösenden Versands geändert hat.

## Schritt 6: Inhalts-Hygiene

Authentifizierung und Listenqualität bringen Sie durch die Tür; der Inhalt beeinflusst weiterhin, wie Sie behandelt werden, sobald Sie dort sind.

- **Vermeiden Sie Spam-Auslöser-Muster** in Betreffzeilen – GROSSBUCHSTABEN, übermäßige Interpunktion ("!!!") und Phrasen wie "jetzt handeln" oder "kostenloses Geld" wirken sich weiterhin negativ auf Spam-Filter aus, selbst von einer authentifizierten Domain.
- **Senden Sie keine rein bildbasierten E-Mails.** Eine E-Mail, die nur ein einzelnes Bild ohne echten Text enthält, ist ein klassisches Spam-Muster; halten Sie eine bedeutende Menge an echtem Textinhalt neben allen Bildern aufrecht.
- **Vorschau vor dem Versand.** Prüfen Sie, wie die E-Mail tatsächlich gerendert wird – einschließlich auf Mobilgeräten – bevor sie an Ihre vollständige Liste geht.
- **Der Abmeldelink wird bereits behandelt.** Spwig fügt automatisch einen funktionierenden, ohne Anmeldung erforderlichen Abmeldelink in den Fußbereich jeder Marketing-E-Mail ein – Sie müssen keinen eigenen hinzufügen (siehe [Kommunikationseinstellungen](communication-preferences) für genau diese Abläufe). Entfernen oder verstecken Sie ihn nicht; ein fehlender oder defekter Abmeldelink ist an sich bereits ein Verstoß gegen die Richtlinien für Massenversender von Gmail und Yahoo, unabhängig von Ihren anderen Kennzahlen.

## "Meine E-Mails landen im Spam" – Fehlersuchliste

Gehen Sie diese Punkte in der Reihenfolge durch:

1. **Prüfen Sie Ihre DNS-Einträge erneut.** Öffnen Sie den DNS-Schritt des Setup-Assistenten des Kontos (oder das DKIM-Panel auf der Admin-Seite des Kontos für integriertes SMTP) und stellen Sie sicher, dass SPF, DKIM und DMARC alle weiterhin als bestanden angezeigt werden.

Eine Domainverlängerung, eine Migration des DNS-Anbieters oder eine unverwandte Änderung an Ihrer Zonendatei kann einen dieser Einträge stillschweigend beschädigen.
2. **Prüfen Sie die Bounce- und Beschwerde-Zahlen im Kampagnenbericht** für die betroffenen Versände – siehe [Kampagnenberichte](campaign-reports).


Ein Anstieg bei einem der beiden Werte deutet auf ein Problem mit der Listenqualität oder dem Inhalt hin, nicht auf ein Authentifizierungsproblem.
3. **Prüfen Sie die Unterdrückungsliste** ([Listenhygiene](list-hygiene)) auf einen plötzlichen Anstieg — wenn ein großer Teil Ihrer Liste seit einiger Zeit fehlschlägt, leidet auch die Zustellbarkeit für den Rest.
4. **Stellen Sie sicher, dass Ihre Absenderadresse auf Ihrer authentifizierten Domain liegt**, nicht auf einer Adresse eines kostenlosen Anbieters oder einer Domain, die nicht mit dem übereinstimmt, für das SPF/DKIM/DMARC eingerichtet wurden.
5. **Senden Sie eine Test-E-Mail an eine Gmail- und eine Yahoo/Outlook-Adresse, die Sie kontrollieren**, und prüfen Sie den tatsächlichen Ordner, in dem sie landet, nicht nur, ob sie angekommen ist.
6. **Wenn Sie kürzlich das Versandvolumen oder das Zielpublikum stark geändert haben,** behandeln Sie es wie einen neuen Warm-up — reduzieren Sie das Volumen und steigern Sie es schrittweise.
7. **Wenn alles oben genannte in Ordnung ist und das Problem weiterhin besteht,** kann es sich um eine drosselungsspezifische Maßnahme des Anbieters handeln, nicht um einen Fehler in Ihrer Einrichtung — dies kann einige Zeit in Anspruch nehmen, bis es sich von selbst löst, sobald die zugrunde liegende Ursache (in der Regel Beschwerden oder Bounces) behoben wurde.

## Tipps

- Beheben Sie die DNS-Authentifizierung, bevor Sie etwas anderes beheben — jeder andere Hebel für die Zustellbarkeit (Inhalt, Listenhygiene, Warm-up) ist weniger wichtig, wenn SPF/DKIM/DMARC nicht bestehen.
- Behandeln Sie die DNS-Validierung des Assistenten als zeitpunktbezogene Prüfung, nicht als einmalige Aktion — führen Sie sie jedes Mal erneut aus, wenn Sie DNS-Anbieter wechseln oder eine Domain über einen anderen Registrar verlängern.
- Eine saubere Liste, die geöffnet und angeklickt wird, wird immer besser abschneiden als eine größere Liste, die dies nicht tut — widerstehen Sie dem Drang, eine alte, nicht verifizierte Liste „nur für den Fall“ zu importieren.
- Beobachten Sie Ihre Zahlen im Verhältnis zu Ihren eigenen früheren Versendungen, nicht zu einer generischen Branchenbenchmark — Ihre eigene Historie ist das zuverlässigste Signal für ein echtes Problem.
- Wenn Sie einen von Spwig gehosteten Plan nutzen, werden das DKIM-Signieren und das Reputationsmanagement des gehosteten Mail-Gateways für Sie übernommen — Ihre verbleibende Verantwortung liegt in der Listenqualität und dem Inhalt, nicht im DNS.