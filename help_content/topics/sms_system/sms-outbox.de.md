---
title: SMS- Ausgangsspeicher
---

Der SMS-Ausgangsspeicher ist ein vollständiges Protokoll aller Textnachrichten, die Ihr Geschäft versucht hat zu senden. Nutzen Sie ihn, um sicherzustellen, dass Benachrichtigungen bei Kunden angekommen sind, Lieferfehler zu untersuchen und Ihre Gesamtaktivität im Nachrichtenversand zu verstehen.

Navigieren Sie zu **SMS-System > SMS-Ausgangsspeicher**, um das Nachrichtenprotokoll anzuzeigen.

![SMS-Ausgangsspeicher-Liste mit Status-Abzeichen](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Ausgangsspeicher ansehen

J Zeile im Ausgangsspeicher stellt einen Nachrichtenversuch dar und zeigt:

- **Telefon** — die Telefonnummer des Empfängers
- **Nachrichtentyp** — SMS oder WhatsApp
- **Status** — der aktuelle Lieferstatus (siehe unten)
- **Erstellt** — wann die Nachricht erstellt wurde
- **Gesendet um** — wann die Nachricht an den Anbieter gesendet wurde

Die Zusammenfassungsleiste oben zeigt aggregierte Zahlen für die wichtigsten Statuswerte im Überblick.

## Nachrichtenstatus

| Status | Bedeutung |
|--------|---------|
| Wartend | Die Nachricht wartet darauf, von der Sendeschlange abgeholt zu werden |
| In Warteschlange | Die Nachricht wurde in die Warteschlange gestellt und wird bald gesendet |
| Gesendet | Der Anbieter hat die Nachricht zur Lieferung angenommen |
| Geliefert | Der Anbieter hat bestätigt, dass die Nachricht auf dem Empfängergerät angekommen ist |
| Fehlgeschlagen | Der Anbieter hat die Nachricht abgelehnt oder konnte sie nicht liefern |
| Übersprungen | Der Versand wurde absichtlich übersprungen (siehe unten die Gründe für Überspringen) |
| Sandbox-Protokoll | Die Nachricht wurde nur protokolliert (Geschäft ist im Test-/Sandbox-Modus) |

> **Gesendet vs. Geliefert:** Ein **Gesendet**-Status bedeutet, dass die Nachricht Ihr Geschäft verlassen hat und vom Anbieter angenommen wurde. Ein **Geliefert**-Status bedeutet, dass der Anbieter eine Lieferbestätigung vom Anbieter erhalten hat. Nicht alle Anbieter unterstützen Lieferbestätigungen — wenn Ihr Anbieter dies nicht tut, können Nachrichten **Gesendet** anzeigen, aber nie zu **Geliefert** weitergehen, was normal ist.

## Nachrichtendetails ansehen

Klicken Sie auf eine Zeile im Ausgangsspeicher, um die vollständigen Details dieser Nachricht anzuzeigen:

- Die vollständige **Nachricht**, die gesendet wurde
- Die **Provider-Nachrichten-ID** — die Referenznummer vom SMS-Anbieter (nützlich, wenn Sie den Support des Anbieters kontaktieren)
- Die **Fehlermeldung** (für fehlgeschlagene Nachrichten) — die genaue Fehlermeldung, die vom Anbieter zurückgegeben wurde
- Die **Wiederholungszahl** — wie oft Spwig versucht hat, die Nachricht zu senden
- Alle Zeitstempel (erstellt, in Warteschlange, gesendet, geliefert)

## Ausgangsspeicher filtern

Nutzen Sie die Filter auf der rechten Seite, um die Liste zu verfeinern:

- **Status** — nur Nachrichten mit einem bestimmten Status anzeigen
- **Nachrichtentyp** — nur SMS oder nur WhatsApp-Nachrichten anzeigen
- **Datum** — nach dem Tag filtern, an dem eine Nachricht erstellt wurde

Das Suchfeld oben ermöglicht die Suche nach Telefonnummer, Nachrichteninhalt oder Provider-Nachrichten-ID.

## Gründe für Überspringen verstehen

Übersprungene Nachrichten wurden nicht gesendet, weil Spwig entschieden hat, dass der Versand unangemessen oder unnötig war. Häufige Gründe für Überspringen:

| Überspringungsgrund | Was es bedeutet |
|-------------|---------------|
| `user_preference_disabled` | Der Kunde hat SMS-Benachrichtigungen in seinen Kontoeinstellungen deaktiviert |
| `unsubscribed` | Der Kunde hat sich von SMS-Nachrichten abgemeldet |
| `no_provider` | Es ist kein aktiver Standard-SMS-Anbieter-Konto konfiguriert |
| `template_inactive` | Das Vorlage für diesen Benachrichtigungstyp ist inaktiv |

Eine übersprungene Nachricht ist kein Fehler — es bedeutet, dass das System wie vorgesehen funktioniert hat. Allerdings deutet eine hohe Anzahl von `no_provider`-Überspringungen darauf hin, dass Sie ein SMS-Anbieter-Konto konfigurieren und aktivieren müssen.

## Problemlösung bei fehlgeschlagenen Lieferungen

Wenn Nachrichten den Status **Fehlgeschlagen** haben, befolgen Sie diese Schritte:

1. Klicken Sie auf die fehlgeschlagene Nachricht, um ihre **Fehlermeldung** anzuzeigen
2. Häufige Fehlerursachen:

   | Fehler | Wahrscheinliche Ursache |
   |-------|-------------|
   | Ungültige Telefonnummer | Die Telefonnummer des Kunden fehlt oder ist nicht im E.164-Format |
   | Authentifizierung fehlgeschlagen | Ihre Anbieter-Anmeldeinformationen sind ungültig oder abgelaufen — aktualisieren Sie sie in **SMS-Anbieterkonten** |
   | Konto gesperrt | Ihr Anbieterkonto wurde gesperrt — melden Sie sich im Dashboard des Anbieters an |
   | Unzureichende Mittel | Der Kontostand Ihres Anbieterkontos ist zu niedrig — laden Sie ihn auf |
   | Carrier-Abweisung | Der Zielcarrier hat die Nachricht blockiert (häufig aufgrund von Inhaltsscreening) |

3. Nach Behebung des zugrunde liegenden Problems werden zukünftige Nachrichten normal gesendet — der Ausgangsspeicher ist ein schreibgeschütztes Protokoll, und einzelne Nachrichten können nicht manuell erneut gesendet werden

## Ausgangsspeicher ist schreibgeschützt

Der SMS-Ausgangsspeicher ist ein Protokoll. Sie können keine Nachrichten manuell zum Ausgangsspeicher hinzufügen, und Sie können keine einzelnen Nachrichten von hier erneut senden. Nachrichten werden automatisch von Spwig gesendet, wenn die relevanten Ereignisse eintreten (z. B. bei einem bestellten Artikel).

## Tipps

- Überprüfen Sie den Ausgangsspeicher nach einer beschäftigten Periode, um sicherzustellen, dass alle Bestätigungs-Nachrichten erfolgreich zugestellt wurden
- Wenn ein Kunde sagt, er habe eine SMS nicht erhalten, suchen Sie im Ausgangsspeicher nach seiner Telefonnummer, um zu sehen, ob die Nachricht gesendet, fehlgeschlagen oder übersprungen wurde
- Ein plötzlicher Anstieg von **Fehlgeschlagenen** Nachrichten deutet in der Regel auf ein Problem mit Ihren Anbieter-Anmeldeinformationen oder Ihrem Kontostand hin — überprüfen Sie diese sofort
- Wenn Sie viele **Übersprungene** Nachrichten mit dem Grund `no_provider` sehen, navigieren Sie zu **SMS-System > SMS-Anbieterkonten** und stellen Sie sicher, dass ein aktives Standardkonto konfiguriert ist
- Die Datenhierarchie oben in der Liste ermöglicht es Ihnen, sich schnell nach Tag, Monat oder Jahr durch historische Nachrichten zu navigieren