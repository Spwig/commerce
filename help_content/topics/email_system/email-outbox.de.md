---
title: E-Mail-Postausgang
---

Der E-Mail-Postausgang ist ein vollständiger Protokollverlauf aller E-Mails, die Ihr Geschäft gesendet oder versucht hat zu senden – Bestätigungen für Bestellungen, Versandupdates, Admin-Berichte und alle anderen transaktionalen Nachrichten. Nutzen Sie ihn, um Lieferungen zu bestätigen, Fehler zu untersuchen und die E-Mail-Warteschlange zu verwalten.

Navigieren Sie zu **E-Mail-System > E-Mail-Postausgang**, um das E-Mail-Protokoll anzuzeigen.

![E-Mail-Postausgang-Liste mit Status-Abzeichen](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Die Postausgangsliste ansehen

Die Zusammenfassungsleiste oben zeigt die Zahlen für jede Statuskategorie an. Die Liste darunter zeigt einzelne E-Mails mit:

- **Betreff** – der Betreffzeile der E-Mail
- **An** – die E-Mail-Adresse des Empfängers
- **Von** – die Absenderadresse, die verwendet wurde
- **Status** – der aktuelle Zustellstatus
- **In Warteschlange gestellt** – wann die E-Mail die Warteschlange betreten hat
- **Gesendet** – wann die E-Mail an den Anbieter gesendet wurde
- **Wiederholungsversuche** – wie viele Sendeveruche unternommen wurden

## E-Mail-Status

| Status | Bedeutung |
|--------|---------|
| In Warteschlange | Die E-Mail wartet in der Warteschlange darauf, gesendet zu werden |
| Wird gesendet | Die E-Mail wird gerade an den Anbieter gesendet |
| Gesendet | Der Anbieter hat die E-Mail akzeptiert |
| Aufbewahrt | Die E-Mail ist pausiert und wird nicht gesendet, bis sie freigegeben wird |
| Protokolliert | Die E-Mail wurde protokolliert, aber nicht gesendet (Testmodus oder nur Protokollierungskonfiguration) |
| Fehlgeschlagen | Der Anbieter hat die E-Mail abgelehnt oder konnte sie nicht liefern |
| Zurückgewiesen | Die E-Mail wurde gesendet, aber vom Empfänger-Mail-Server zurückgewiesen |
| Übersprungen | Der Versand wurde aus systembedingten Gründen übersprungen |

## E-Mail-Details ansehen

Klicken Sie auf eine E-Mail in der Liste, um die vollständigen Details anzuzeigen:

- Der vollständige **HTML-Textkörper** und **Textkörper** der E-Mail
- **Anbieter-Meldungs-ID** – die Referenz von Ihrem E-Mail-Anbieter (verwenden Sie dies, wenn Sie den Support des Anbieters kontaktieren)
- **Fehlermeldung** – die genaue Fehlermeldung für fehlgeschlagene oder zurückgewiesene E-Mails
- **Wiederholungsversuche** und **Maximale Wiederholungen** – wie oft der Versand versucht wurde
- Alle Zeitstempel: erstellt, in Warteschlange gestellt, gesendet und fehlgeschlagen

## Die Postausgangsliste filtern

Verwenden Sie die Filter auf der rechten Seite, um Ihre Ansicht zu verfeinern:

- **Status** – zeigen Sie E-Mails eines bestimmten Zustellstatus an
- **Datum** – filtern Sie nach dem Datum, an dem E-Mails erstellt oder gesendet wurden
- **Vorlagen-Typ** – zeigen Sie nur E-Mails eines bestimmten Benachrichtigungstyps an (z. B. nur Bestätigungen für Bestellungen)

Das Suchfeld oben durchsucht nach Betreff, Empfängeradresse, Absenderadresse oder Anbieter-Meldungs-ID.

## Aufbewahrte E-Mails freigeben

E-Mails im **Aufbewahrt**-Status sind pausiert – sie werden nicht gesendet, bis Sie sie freigeben. Eine E-Mail kann aufbewahrt werden, wenn Ihr Geschäft im Wartungsmodus war, als sie generiert wurde, oder wenn eine Admin-Aktion sie aufbewahrt hat.

Um aufbewahrte E-Mails freizugeben:
1. Wählen Sie die E-Mails aus, die Sie freigeben möchten (klicken Sie auf die Kästchen links)
2. Wählen Sie **Aufbewahrte E-Mails für den Versand freigeben** aus dem **Aktionen**-Dropdown-Menü aus
3. Klicken Sie auf **Weiter**

Freigegebene E-Mails wechseln in den **In Warteschlange**-Status und werden im nächsten Warteschlangenverarbeitungszyklus gesendet.

## Geplante E-Mails

Einige E-Mails sind für einen zukünftigen Zeitpunkt geplant – wöchentliche Zusammenfassungsberichte beispielsweise sind für einen bestimmten Tag und eine bestimmte Uhrzeit geplant. Navigieren Sie zu **E-Mail-System > Geplante E-Mails**, um bevorstehende geplante Versandvorgänge anzuzeigen.

Die Liste der geplanten E-Mails zeigt an:

- **Vorlagen-Typ** – der Typ der geplanten E-Mail
- **Empfänger-E-Mail** – die Adresse, an die sie gesendet wird
- **Geplant für** – das Datum und die Uhrzeit, zu der sie gesendet werden soll
- **Status** – Ausstehend (noch nicht gesendet), Gesendet oder Fehlgeschlagen

Geplante E-Mails werden automatisch verarbeitet, wenn ihre geplante Zeit kommt – keine manuelle Aktion ist erforderlich.

## Fehlerhafte Zustellungen beheben

Wenn E-Mails den **Fehlgeschlagen**-Status haben, klicken Sie darauf, um die Fehlermeldung anzuzeigen und folgen Sie diesen Schritten:

### Häufige Ursachen und Lösungen

| Symptom | Likely cause | What to do |
|---------|-------------|------------|
| "Authentication failed" | Die E-Mail-Anbieter-Anmeldeinformationen sind ungültig | Aktualisieren Sie die Anmeldeinformationen in **E-Mail-System > E-Mail-Konten** |
| "Connection refused" / "Timeout" | Ihr E-Mail-Server ist nicht erreichbar | Prüfen Sie die Statusseite Ihres E-Mail-Anbieters; testen Sie die Verbindung in **E-Mail-Konten** |
| "Invalid recipient" | Die E-Mail-Adresse des Kunden ist falsch formatiert | Prüfen Sie das Kundenkonto und korrigieren Sie ihre E-Mail-Adresse |
| Bounced emails | Der Empfänger-Server hat die E-Mail abgewiesen | Die E-Mail-Adresse existiert möglicherweise nicht oder der Posteingang ist voll; wiederholen Sie nicht zu oft |
| High failure rate suddenly | Problem beim Anbieter oder abgelaufene Anmeldeinformationen | Prüfen Sie den Anbieterstatus; testen Sie die Verbindung erneut in **E-Mail-Konten** |

### Checking your email account connection

Wenn viele E-Mails fehlschlagen, testen Sie Ihr E-Mail-Konto:

1. Navigieren Sie zu **E-Mail-System > E-Mail-Konten**
2. Finden Sie Ihr aktives Konto und prüfen Sie den **Verbindungs**-Status
3. Wenn die Verbindung einen Fehler anzeigt, klicken Sie auf das Konto und verwenden Sie die Option **Verbindung testen**, um das Problem zu diagnostizieren

### Retry behaviour

Spwig versucht automatisch, fehlgeschlagene E-Mails bis zu dem **Max Retries**-Limit zu senden. Die Anzahl der Wiederholungen, die auf jeder E-Mail angezeigt wird, zeigt an, wie viele Versuche bereits unternommen wurden. Sobald das Wiederholungslimit erreicht ist, bleibt die E-Mail im **Fehlgeschlagen**-Status und es erfolgen keine weiteren automatischen Wiederholungen.

## Bounced emails

Eine **Bounced**-E-Mail wurde gesendet, aber vom Empfänger-Server zurückgesendet. Es gibt zwei Arten von Bounces:

- **Hard bounce** — die E-Mail-Adresse existiert nicht oder der Domain akzeptiert keine E-Mails. Wiederholen Sie keine Hard Bounces; die Adresse ist ungültig
- **Soft bounce** — ein vorübergehendes Problem (Posteingang voll, Server vorübergehend nicht verfügbar). Kann bei erneuter Versendung erfolgreich sein

Wiederholte Bounces an dieselbe Adresse können Ihre Absenderreputation bei E-Mail-Anbietern schädigen. Wenn Sie wiederholte Bounces an dieselbe Kundenadresse sehen, aktualisieren Sie oder entfernen Sie diese Adresse aus dem Kundenkonto.

## Tips

- Prüfen Sie den Ausgangsspeicher nach großen Ereignissen wie einem Flash-Sale oder einer großen Produktveröffentlichung, um sicherzustellen, dass alle Bestätigungs-E-Mails erfolgreich gesendet wurden
- Wenn ein Kunde sagt, er habe eine E-Mail nicht erhalten, suchen Sie im Ausgangsspeicher nach seiner E-Mail-Adresse, um zu prüfen, ob sie gesendet, fehlgeschlagen oder übersprungen wurde
- Ein plötzlicher Anstieg an Fehlern deutet in der Regel auf ein Problem mit Anmeldeinformationen oder einem Konto hin — prüfen Sie **E-Mail-Konten** sofort
- Der **Held**-Status ist kein Fehler — es bedeutet nur, dass die E-Mail wartet. Geben Sie E-Mails, die aufgehalten wurden, frei, wenn Sie bereit sind, sie zu senden
- Verwenden Sie den Filter **Vorlagen-Typ**, um alle E-Mails eines bestimmten Typs schnell zu überprüfen — beispielsweise, um sicherzustellen, dass alle Bestätigungen der letzten 7 Tage den **Gesendet**-Status haben
- Die Datenhierarchie-Navigation (Tag / Monat / Jahr) oben in der Liste ist nützlich, um den Ausgangsspeicher für einen bestimmten Zeitraum zu überprüfen