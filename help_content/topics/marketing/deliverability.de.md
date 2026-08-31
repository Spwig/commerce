---
title: E-Mail-Zustellungsleitfaden
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Schritt 4 (DNS-Konfiguration) des E-Mail-Kontowizzards für den eingebauten SMTP-Anbieter, wobei die Einzeiler-Validierung für SPF/DKIM/DMARC und die DNS-Anbieter-Registerkarten (Cloudflare/GoDaddy/Namecheap/Route 53/Other) angezeigt werden, wobei mindestens ein Eintrag mit erweitertem "Details"-Panel sichtbar ist, um eine kopierbare TXT-Eintrag zu zeigen.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: Das Änderungsformular eines vorhandenen eingebauten SMTP-E-Mail-Accounts, das zum "DKIM-Schlüssel konfiguriert"-Bereich gescrollt wird, wobei der DNS-TXT-Eintrag Name/Wert und die Schaltfläche "DNS-Eintrag kopieren" angezeigt werden.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: Der Statistik-Card-Bereich "Unterdrückte Adressen" im Campaign Studio-Dashboard für den "monitor"-Abschnitt dieses Leitfadens.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Einen E-Mail-*Sendevorgang* zu haben, ist einfach. Es ist die eigentliche Aufgabe, sie in den Posteingang zu bringen und nicht in den Spam-Ordner. Mailbox-Anbieter wie Gmail und Yahoo setzen nun harte technische Anforderungen voraus, bevor sie ihn überhaupt in Betracht ziehen. Dieser Leitfaden erläutert, was zu konfigurieren ist und in welcher Reihenfolge, damit Ihre Bestellbestätigungen und Kampagnen dort landen, wo die Kunden sie sehen können.

Nichts davon ist eine Einmal-Aufgabe. Die Zustellbarkeit ist eine ständige Aufgabe, die Sie über die Zeit aufbauen und schnell verlieren können – der Checklist-Ende ist es wert, erneut überprüft zu werden, wenn etwas nicht stimmt.

## Warum es wichtig ist

Jeder große Postfach-Anbieter bewertet eingehende E-Mails anhand der Absenderreputation, bevor entschieden wird, ob sie geliefert, in einen Spam-Ordner gelegt oder gleich abgelehnt werden. Seit 2024 haben Gmail und Yahoo diese in explizite **Bulk-Sender-Anforderungen** formalisiert für alle, die eine bedeutende Menge senden:

- **Authentifizieren Sie Ihr Domain** – gültige SPF-, DKIM- und DMARC-Einträge.
- **Machen Sie es einfach, sich abzumelden** – einen funktionierenden, geringen Aufwand für die Opt-Out-Funktion in jeder Marketing-E-Mail.
- **Halten Sie die Spam-Beschwerden niedrig** – Bulk-Sender, die etwa 0,3 % Beschwerden überschreiten, riskieren, dass E-Mails abgelehnt oder in den Massenordner verschoben werden; das sicherste Ziel ist deutlich unter 0,1 %.

Fehlschlagen Sie diese, leiden nicht nur Marketing-Kampagnen darunter – eine beschädigte Domain-Reputation kann transaktionale E-Mails (Bestellbestätigungen, Passwort-Wiederherstellung) ebenfalls in den Spam-Ordner ziehen, da Gmail und Yahoo zunehmend die Reputation auf Ebene der sendenden Domain beurteilen, nicht nur pro Nachrichtentyp. Die Schritte unten sind, wie Sie alle drei erfüllen.

## Schritt 1: Authentifizieren Sie Ihre Sendedomäne

SPF, DKIM und DMARC sind DNS-TXT-Einträge, die den empfangenden Mailservern beweisen, dass E-Mails, die als von Ihrer Domain stammend geltend gemacht werden, wirklich von Ihnen gesendet wurden. Wie Sie sie einrichten, hängt davon ab, in welchem Sendemodus Ihr Store verwendet – alle drei werden unter **E-Mail-Konfiguration** im Admin-Seitenleistenmenü konfiguriert (dies öffnet die Liste der E-Mail-Accounts; siehe [E-Mail-Konfiguration](email-configuration) für die vollständige Anleitung zur Einrichtung des Kontos).

| Versandmodus | Wie die Authentifizierung funktioniert |
|---|---|
| **Eigener SMTP-Server** (Spwig-eigener E-Mail-Server) | Spwig generiert automatisch ein DKIM-Schlüsselpaar für Ihre Domain. Fügen Sie eine E-Mail-Adresse hinzu, und **Schritt 4** des Einrichtungswizards zeigt Ihnen den SPF-, DKIM- und DMARC-Status sowie den exakten Eintrag an, den Sie hinzufügen müssen, mit Kopieren-in-Zwischenspeicher und anbieterspezifischen Anweisungen für Cloudflare, GoDaddy, Namecheap und AWS Route 53. Der gleiche DKIM-DNS-Eintrag wird später auch auf der eigenen Admin-Seite des Kontos unter **DKIM-Schlüssel, die konfiguriert wurden**, angezeigt, falls Sie ihn später erneut benötigen. |
| **Allgemeiner SMTP-Server** (ein eigenes Anbieter-Setup wie SendGrid, Mailgun, Amazon SES oder Google Workspace, verbunden über SMTP-Anmeldeinformationen) | Die Authentifizierung erfolgt teilweise in der eigenen Dashboard-Oberfläche des Anbieters. Der DNS-Schritt des Einrichtungswizards enthält tabbasierte Anweisungen für Gmail, Outlook, SendGrid, Mailgun und Amazon SES — jeder erklärt, was Sie in der Konsole des Anbieters konfigurieren müssen (z. B. die Überprüfung eines Absenderdomains in SendGrid) und welche DNS-Einträge Sie bei Ihrem DNS-Anbieter hinzufügen müssen. |
| **Spwig-hosted-Mail-Gateway** | Verfügbar auf Spwig-hosted-Plänen als verwalteter Versandmodus. Es signiert ausgehende E-Mails automatisch mit DKIM und verwendet standardmäßig eine Adresse auf Spwigs eigenem verifizierten Domain, sodass es mit keiner Einrichtung funktioniert. Wenn Sie von Ihrer eigenen Domain aus senden möchten, sprechen Sie mit Ihrem Hosting-Anbieter über die Überprüfung — dies ist ein verwalteter Dienst, kein Selbstbedienungs-DNS-Fluss. |

Unabhängig vom Modus, **das Hinzufügen des DNS-Eintrags ist immer ein externer Schritt** — Sie führen es bei Ihrem Domain-Registrierer oder DNS-Anbieter (Cloudflare, GoDaddy, Namecheap, Route 53 oder wo auch immer Ihre Domain-Namenserver verweisen) durch, nicht innerhalb von Spwig. Spwig kann Ihnen genau sagen, was Sie hinzufügen müssen, und prüfen, ob er live ist, aber es kann nicht in Ihren Registrierer eingreifen und ihn für Sie hinzufügen.

Ein paar Dinge, die Sie vor Beginn wissen sollten:

- **DNS-Änderungen sind nicht sofort wirksam.** Die Verbreitung kann zwischen ein paar Minuten und 48 Stunden dauern. Der Prüfschritt des Einrichtungswizards zeigt einen Eintrag als fehlerhaft oder nicht vorhanden an, bis er tatsächlich verarbeitet wurde — das ist zu erwarten, nicht ein Zeichen dafür, dass etwas schiefgelaufen ist.
- **Pro Domain ist nur ein SPF-Eintrag erlaubt.** Wenn Sie bereits einen haben (z. B. von Google Workspace oder einem anderenMailer), fügen Sie Ihren neuen Absender dem vorhandenen Eintrag mit `include:` hinzu, anstatt einen zweiten SPF-TXT-Eintrag zu erstellen — zwei SPF-Einträge werden die Authentifizierung für alle brechen.
- **DMARC benötigt SPF oder DKIM, um bereits zu funktionieren.** Richten Sie es erst ein, nachdem SPF und DKIM beide überprüft wurden.

## Schritt 2: Verwenden Sie eine echte Absender-Identität

Sobald Ihre Domain authentifiziert ist, stellen Sie sicher, dass das, was die Empfänger tatsächlich sehen, damit übereinstimmt:

- **Absender-Adresse** — verwenden Sie eine Adresse auf Ihrer eigenen authentifizierten Domain (`orders@yourstore.com`), nie eine kostenlose Provider-Adresse (`yourstore@gmail.com`). Eine kostenlose Provider-Absender-Adresse kann überhaupt nicht durch Ihre SPF/DKIM/DMARC-Protokolle authentifiziert werden, und E-Mail-Provider behandeln sie als starkes Spam-Signal eines Ladens.
- **Absender-Name** — verwenden Sie einen erkennbaren Namen Ihres Ladens, nicht ein generisches Etikett wie "Benachrichtigungen" oder "Keine Antwort".
- **Antwort-Adresse** — setzen Sie eine überwachte Adresse. Eine nicht überwachte `noreply@`-Adresse, die zurückgeworfen wird oder stillschweigend gelöscht wird, ist selbst ein schwacher Reputationssignal und blockiert den einen Kanal, den Kunden haben, um Ihnen mitzuteilen, dass etwas schiefgelaufen ist.

Richten Sie alle drei unter **E-Mail-Konfiguration > (Ihr Konto) > Absender-Konfiguration** ein — siehe [E-Mail-Konfiguration](email-configuration) für eine vollständige Feld-Begleitung.

## Schritt 3: Aufwärmen, bevor Sie skalieren

Eine Domain oder IP-Adresse mit keiner Versandgeschichte hat noch keine Reputation — gut oder schlecht — und E-Mail-Provider sind bei Unbekanntem vorsichtig. Ein riesiger erster Schuss von einer brandneuen Domain sieht statistisch identisch mit einem Spammer, der eine neue Kampagne startet, und kann in den Ordner "Bulk" verschoben werden, auch wenn jeder technische Punkt überprüft wurde.

- Beginnen Sie kleiner.

Senden Sie Ihre ersten Kampagnen an Ihr engagiertestes Publikum mit der höchsten Öffnungswahrscheinlichkeit, anstatt sofort Ihre gesamte Liste zu verwenden – siehe [Zielgruppen](audiences), um ein gezieltes Startsegment zu erstellen.
- Erhöhen Sie das Volumen in den ersten Wochen schrittweise, anstatt sofort an die gesamte Liste zu senden.
- Wenn Sie eine bestehende Liste von einer anderen Plattform migrieren, behandeln Sie dies auch aus Reputationsgesichtspunkten als Tag eins – die Versandhistorie Ihrer alten Plattform wird nicht mit der Domain übertragen.

## Schritt 4: Halten Sie Ihre Liste sauber

Jede Beschwerde oder jeder Bounce kostet Sie Reputation, und beides hängt weitgehend davon ab, wer sich auf Ihrer Liste befindet und wie er dort gelandet ist:

- **Versenden Sie nur an Personen, die eingewilligt haben.** Importierte Kontakte, gekaufte Listen und gescrapte Adressen sind der schnellste Weg, um Spam-Beschwerden und harte Bounces zu erhöhen.
- **Verwenden Sie die doppelte Opt-in-Methode.** Der Marketing-Einwilligungsprozess von Spwig verifiziert die E-Mail-Adresse eines Abonnenten, bevor ihm Marketing-E-Mails gesendet werden – siehe [Kommunikationseinstellungen](communication-preferences), um zu erfahren, wie dies konfiguriert wird.
- **Lassen Sie die automatische Unterdrückung von Spwig ihre Arbeit tun.** Spwig überwacht harte Bounces, Spam-Beschwerden und wiederholte weiche Bounces und stoppt das Versenden an diese Adressen automatisch, ohne dass eine Einrichtung erforderlich ist – siehe [Listenhaltung und Unterdrückungen](list-hygiene), um genau zu erfahren, wie dies funktioniert und wann (selten) Sie es außer Kraft setzen sollten.
- **Entfernen Sie inaktive Abonnenten regelmäßig**, anstatt dieselben nicht engagierten Adressen endlos zu beliefern – eine schrumpfende Liste, die geöffnet und angeklickt wird, ist für Ihre Reputation wertvoller als eine große, die dies nicht tut.

## Schritt 5: Überwachen

Lieferbarkeitsprobleme zeigen sich in den Zahlen, bevor ein Kunde Ihnen mitteilt, dass eine E-Mail nicht angekommen ist.

Öffnen Sie den [Bericht](campaign-reports) einer Kampagne nach jedem Versand und beobachten Sie:

| Metrik | Worauf Sie achten sollten |
|---|---|
| **Bounce-Rate** | Überwiegend weiche Bounces sind normal; ein steigender Anteil an **harten Bounces** bedeutet, dass sich veraltete oder ungültige Adressen auf Ihrer Liste ansammeln. |
| **Spam-Beschwerden** | Sollte bei jedem Versand nahe null liegen. Halten Sie diesen Wert deutlich unter der Schwelle von etwa 0,3 %, die bei Gmail und Yahoo die Durchsetzung für Massenversender auslöst – behandeln Sie selbst einen kleinen Anstieg als sofortige Untersuchungswürdigkeit. |
| **Öffnungsrate / Klick-zu-Öffnungs-Rate** | Ein plötzlicher, unerklärlicher Rückgang über mehrere Versände an dieselbe Liste (nicht nur eine Kampagne) kann ein frühes Anzeichen dafür sein, dass E-Mails im Spam-Ordner statt im Posteingang landen, noch bevor sich Bounce- oder Beschwerdezahlen ändern. |

Prüfen Sie auch regelmäßig die Karte **Unterdrückte Adressen** im Campaign Studio-Dashboard – ein stetiger, geringer Zufluss ist normaler Listenverfall, aber ein plötzlicher Anstieg ist vor Ihrem nächsten Versand untersuchenswert (siehe [Listenhaltung](list-hygiene)).

Wenn etwas ansteigt: Pausieren Sie und prüfen Sie zuerst, ob Ihre DNS-Einträge noch gültig sind (eine abgelaufene Domainverlängerung oder eine versehentliche DNS-Änderung kann SPF/DKIM stillschweigend brechen), und sehen Sie sich dann an, was sich am Inhalt oder Publikum des auslösenden Versands geändert hat.

## Schritt 6: Inhalts-Hygiene

Authentifizierung und Listenqualität bringen Sie an die Tür; der Inhalt beeinflusst immer noch, wie Sie behandelt werden, sobald Sie dort sind.

- **Vermeiden Sie Spam-Auslöser-Muster** in Betreffzeilen – GROSSE BUCHSTABEN, übermäßige Interpunktion ("!!!") und Phrasen wie "jetzt handeln" oder "kostenloses Geld" wirken sich nachteilig auf Sie aus, selbst von einer authentifizierten Domain aus.
- **Senden Sie keine rein bildbasierten E-Mails.** Eine E-Mail, die nur ein einzelnes Bild ohne echten Text enthält, ist ein klassisches Spam-Muster; halten Sie eine bedeutende Menge an echtem Textinhalt neben den Bildern aufrecht.
- **Vorschau vor dem Senden.** Prüfen Sie, wie die E-Mail tatsächlich gerendert wird – einschließlich auf Mobilgeräten –, bevor sie an Ihre gesamte Liste geht.
- **Der Abmeldelink wird bereits behandelt.** Spwig fügt automatisch einen funktionierenden Abmeldelink ohne Login-Erfordernis in den Fußbereich jeder Marketing-E-Mail ein – Sie müssen keinen eigenen hinzufügen (siehe [Kommunikationseinstellungen](communication-preferences), um genau zu erfahren, wie dieser Ablauf funktioniert). Entfernen oder verstecken Sie ihn nicht; ein fehlender oder defekter Abmeldelink ist an sich bereits ein Verstoß gegen die Richtlinien für Massenversender von Gmail und Yahoo, unabhängig von Ihren anderen Kennzahlen.

## "Meine E-Mails landen im Spam" — Fehlerbehebung

Gehen Sie diese Punkte in der Reihenfolge durch:

1. **Prüfen Sie Ihre DNS-Einträge erneut.** Öffnen Sie den DNS-Schritt des Einrichtungswizards des Kontos (oder das DKIM-Panel auf der Admin-Seite des Kontos für integriertes SMTP) und stellen Sie sicher, dass SPF, DKIM und DMARC weiterhin als bestanden angezeigt werden. Eine Domainverlängerung, eine Migration des DNS-Anbieters oder eine unbekannte Änderung an Ihrer Zonendatei kann eine dieser Einstellungen stillschweigend beeinträchtigen.
2. **Prüfen Sie die Bounce- und Beschwerde-Zahlen im Kampagnenbericht** für die betroffenen Sendeaktionen — siehe [Kampagnenberichte](campaign-reports). Ein Anstieg bei einem der beiden Werte deutet auf ein Problem mit der Listenqualität oder dem Inhalt hin, nicht auf ein Authentifizierungsproblem.
3. **Prüfen Sie die Unterdrückungsliste** ([Listenhygiene](list-hygiene)) auf einen plötzlichen Anstieg — wenn ein großer Teil Ihrer Liste seit einiger Zeit fehlschlägt, verschlechtert sich auch die Zustellbarkeit für den Rest.
4. **Stellen Sie sicher, dass Ihre Absenderadresse auf Ihrer authentifizierten Domain liegt**, nicht auf einer Adresse eines kostenlosen Anbieters oder einer Domain, die nicht mit dem übereinstimmt, für das SPF/DKIM/DMARC eingerichtet wurden.
5. **Senden Sie eine Test-E-Mail an eine Gmail- und eine Yahoo/Outlook-Adresse, die Sie kontrollieren**, und prüfen Sie den tatsächlichen Ordner, in dem sie landet, nicht nur, ob sie angekommen ist.
6. **Wenn Sie kürzlich das Sendevolumen oder das Zielpublikum stark geändert haben,** behandeln Sie es wie ein neues Warm-up — senken Sie das Volumen und steigern Sie es schrittweise.
7. **Wenn alles oben genannte in Ordnung ist und das Problem weiterhin besteht,** handelt es sich möglicherweise um drosselungsspezifische Maßnahmen des Anbieters und nicht um einen Fehler in Ihrer Einrichtung — dies kann einige Zeit dauern, bis es sich von selbst löst, sobald die Ursache (in der Regel Beschwerden oder Bounces) behoben wurde.

## Tipps

- Beheben Sie die DNS-Authentifizierung, bevor Sie etwas anderes beheben — jeder andere Hebel für die Zustellbarkeit (Inhalt, Listenhygiene, Warm-up) ist weniger wichtig, wenn SPF/DKIM/DMARC nicht bestanden werden.
- Betrachten Sie die DNS-Validierung des Einrichtungswizards als einen Momentaufnahme-Check, nicht als einmalige Aktion — führen Sie sie jedes Mal erneut aus, wenn Sie DNS-Anbieter wechseln oder eine Domain über einen anderen Registrar verlängern.
- Eine saubere Liste, die geöffnet und angeklickt wird, wird immer besser abschneiden als eine größere Liste, die das nicht tut — widerstehen Sie dem Drang, eine alte, nicht verifizierte Liste "nur für den Fall" zu importieren.
- Beobachten Sie Ihre Zahlen im Verhältnis zu Ihren eigenen früheren Sendeaktionen, nicht zu einer generischen Branchenbenchmark — Ihre eigene Historie ist das zuverlässigste Signal für ein echtes Problem.
- Wenn Sie einen von Spwig gehosteten Plan nutzen, werden das DKIM-Signieren und das Reputationsmanagement des gehosteten Mail-Gateways für Sie übernommen — Ihre verbleibende Verantwortung liegt in der Listenqualität und dem Inhalt, nicht im DNS.