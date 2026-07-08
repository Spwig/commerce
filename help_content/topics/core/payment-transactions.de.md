---
title: Zahlungstransaktionen
---

Zahlungstransaktionen ist der vollständige Verlauf aller Zahlungsvorgänge, die über Ihr Geschäft verarbeitet wurden — Gebühren, Erstattungen, Genehmigungen und mehr. Dieser Abschnitt enthält auch Webhook-Protokolle von Ihren Zahlungsanbietern und Zahlungsvorgaben, die während des Checkouts erstellt wurden.

## Zahlungstransaktionen

Navigieren Sie zu **Zahlungen > Zahlungstransaktionen**, um jede Transaktion anzuzeigen, die Ihr Geschäft verarbeitet hat.

### Transaktionsarten

| Typ | Was es bedeutet |
|------|--------------|
| **Gebühr** | Sofortige Zahlung — Gelder werden zum Zeitpunkt der Transaktion eingezogen |
| **Genehmigung** | Gelder werden auf der Karte des Kunden geblockt, aber noch nicht eingezogen |
| **Einziehung** | Einzieht die Gelder aus einer vorherigen Genehmigung |
| **Stornieren** | Storniert eine Genehmigung, bevor sie eingezogen wird |
| **Erstattung** | Stellt die Zahlung dem Kunden zurückerstattet |

### Transaktionsstatusse

| Status | Was es bedeutet |
|--------|--------------|
| **Ausstehend** | Die Transaktion wurde initiiert, aber noch nicht verarbeitet |
| **Wird verarbeitet** | Wird von dem Zahlungsanbieter verarbeitet |
| **Genehmigt** | Gelder sind geblockt — auf Einziehung wartend |
| **Abgeschlossen** | Die Zahlung war erfolgreich |
| **Fehlgeschlagen** | Die Zahlung wurde abgelehnt oder es ist ein Fehler aufgetreten |
| **Storniert** | Die Genehmigung wurde vor der Einziehung storniert |
| **Erstattet** | Eine vollständige Erstattung wurde erteilt |
| **Teilweise erstattet** | Teil der Zahlung wurde zurückerstattet |

### Was Sie auf einer Transaktionsaufzeichnung sehen können

Jede Transaktion zeigt:
- **Transaktions-ID** — interner Verweis von Spwig
- **Zahlungsanbieter-Transaktions-ID** — der Verweis von Ihrem Zahlungsanbieter (z. B. Stripe-Gebühren-ID)
- **Betrag** — der Transaktionsbetrag und Währung
- **Status** und **Typ**
- **Kunden-E-Mail** und **Kundenname**
- **Zahlungsmethode** — Typ (Kreditkarte, Banküberweisung usw.) und letzte 4 Ziffern
- **Bestellung** — zu welcher Bestellung diese Transaktion gehört
- **Zahlungsanbieter-Konto** — welcher Zahlungsanbieter sie verarbeitet hat
- **Zahlungsanbieter-Antwort** — die rohe technische Antwort vom Zahlungsanbieter
- **Fehlermeldung** — wenn die Transaktion fehlgeschlagen ist, der Grund, der vom Anbieter gegeben wurde
- Zeitstempel für Erstellung, letzte Aktualisierung und Abschluss

### Filtern von Transaktionen

Verwenden Sie die Admin-Filter, um Transaktionen nach folgenden Kriterien zu filtern:
- Status (z. B. nur fehlgeschlagene Transaktionen anzeigen)
- Typ (z. B. nur Erstattungen anzeigen)
- Zahlungsanbieter-Konto
- Datumsbereich

Dies ist nützlich für die End-of-Day-Abstimmung oder die Untersuchung der Zahlungsgeschichte eines bestimmten Kunden.

### Wann kann eine Transaktion erstattet werden?

Eine Transaktion kann erstattet werden, wenn:
- Ihr Status **Abgeschlossen** ist
- Ihr Typ **Gebühr** oder **Einziehung** ist

Um eine Erstattung zu vergeben, verwenden Sie die Aktion **Erstattung** auf der Detailseite der Bestellung. Erstattungen, die über die Bestellung verarbeitet werden, erstellen eine neue Transaktionsaufzeichnung vom Typ **Erstattung**.

### Genehmigung und Einziehung

Einige Zahlungsmethoden (und einige Zahlungsanbieter) unterstützen separate Genehmigung und Einziehung. Dies ist nützlich, wenn Sie die Zahlung vor dem Versand überprüfen möchten:

1. **Genehmigung** — Gelder werden auf der Karte des Kunden geblockt (Status: `Genehmigt`)
2. **Einziehung** — wird ausgelöst, wenn die Bestellung versandt oder erfüllt wird
3. Wenn die Einziehung nicht innerhalb des Genehmigungszeitraums erfolgt, läuft die Blockierung **automatisch ab**

Das Feld **Ablaufdatum** auf der Transaktion zeigt an, wann eine Genehmigung abläuft.

## Zahlung webhooks

Zahlungsanbieter senden Webhook-Events, um Ihr Geschäft über Änderungen des Zahlungsstatus zu informieren — beispielsweise, wenn eine Zahlung erfolgreich ist, fehlschlägt oder eine Streitigkeit auftritt. Spwig protokolliert alle eingehenden Webhooks.

Navigieren Sie zu **Zahlungen > Zahlung webhooks**, um das Protokoll anzuzeigen.

### Was Webhook-Aufzeichnungen zeigen

| Feld | Beschreibung |
|-------|-------------|
| **Provider** | Welcher Zahlungsanbieter den Webhook gesendet hat |
| **Event ID** | Die eindeutige Ereignis-ID des Anbieters |
| **Event Type** | Der Typ des Ereignisses (z. B. `payment_intent.succeeded`, `charge.refunded`) |
| **Verarbeitet** | Ob Spwig auf diesen Webhook reagiert hat |
| **Signatur überprüft** | Ob die Sicherheitssignatur des Webhooks gültig war |
| **Nutzlast** | Die vollständigen Daten, die vom Anbieter gesendet wurden |
| **Verarbeitungsergebnis** | Was Spwig als Reaktion getan hat |
| **Verarbeitungsfehler** | Jegliche Fehler, die während der Verarbeitung aufgetreten sind |
| **Empfangen um** | Wann der Webhook empfangen wurde |

### Webhook-Protokolle zur Problembehandlung

Wenn eine Zahlung blockiert zu sein scheint oder der Bestellstatus nach der Zahlung nicht aktualisiert wurde:

1. Navigieren Sie zu **Zahlungen > Zahlungs-Webhooks**
2. Filtern Sie nach dem Anbieter und suchen Sie nach kürzlich Ereignissen
3. Überprüfen Sie die Spalte **Verarbeitet** – ein unverarbeiteter Webhook kann auf ein Lieferproblem hinweisen
4. Überprüfen Sie **Signatur überprüft** – ein fehlgeschlagene Signatur kann bedeuten, dass Ihr Webhook-Geheimnis falsch konfiguriert ist
5. Überprüfen Sie **Verarbeitungsfehler** auf Fehlermeldungen

Doppelte Ereignisse werden automatisch behandelt – die Kombination aus `Event ID` und Anbieter ist eindeutig, sodass der gleiche Webhook nicht zweimal verarbeitet werden kann.

## Zahlungsabsichten

Eine Zahlungsabsicht verfolgt den Lebenszyklus einer Checkout-Zahlung vom Moment an, in dem ein Kunde mit dem Zahlungsprozess beginnt, bis zum endgültigen Ergebnis. Zahlungsabsichten werden automatisch erstellt, wenn ein Kunde die Zahlungsphase im Checkout erreicht.

Navigieren Sie zu **Zahlungen > Zahlungsabsichten**, um die Liste anzuzeigen.

### Status von Zahlungsabsichten

| Status | Bedeutung |
|--------|---------|
| **Erstellt** | Absicht wurde erstellt, wartet auf Zahlungsmethode |
| **Zahlungsmethode erforderlich** | Warte auf den Kunden, um seine Karteninformationen einzugeben |
| **Bestätigung erforderlich** | Zahlungsdetails eingegeben, wartet auf Bestätigung |
| **Aktion erforderlich** | Der Kunde muss eine Aktion abschließen (z. B. 3D Secure-Authentifizierung) |
| **Wird verarbeitet** | Zahlung wird verarbeitet |
| **Erfolgreich** | Zahlung erfolgreich abgeschlossen |
| **Abgebrochen** | Die Zahlung wurde abgebrochen oder abgelehnt |
| **Fehlgeschlagen** | Zahlungsversuch fehlgeschlagen |

### Fluss von Zahlungsabsichten zu Bestellungen

1. Kunde erreicht Zahlungsphase im Checkout → Spwig erstellt eine **Zahlungsabsicht** und einen Entwurf einer **Bestellung** (unbezahlt)
2. Kunde gibt Zahlungsdetails ein und bestätigt
3. Zahlungsanbieter verarbeitet die Zahlung
4. Bei Erfolg wird die Bestellung auf **Bezahlt** aktualisiert und die Zahlungsabsicht wechselt in den Status **Erfolgreich**
5. Ein **Zahlungstransaktions**-Eintrag wird mit den endgültigen Gebührendetails erstellt

Die Zahlungsabsicht verknüpft die Checkout-Sitzung, den Anbieter-Konto und die Bestellung – sie gibt Ihnen einen vollständigen Überblick über den Checkout-Prozess des Kunden.

### Verwenden von Zahlungsabsichten für Support

Wenn ein Kunde meldet, dass er bezahlt hat, aber die Bestellung als unbezahlt angezeigt wird:

1. Finden Sie die Bestellung des Kunden in **Bestellungen**
2. Navigieren Sie zu **Zahlungen > Zahlungsabsichten** und suchen Sie nach Absichten, die mit dieser Bestellung verknüpft sind
3. Überprüfen Sie den Absichtsstatus – wenn er **Erfolgreich** ist, überprüfen Sie die verknüpfte Transaktion
4. Wenn die Absicht **Aktion erforderlich** ist, hat der Kunde möglicherweise die 3D Secure-Authentifizierung nicht abgeschlossen
5. Wenn die Absicht **Fehlgeschlagen** ist, erklären die Fehlerdetails, warum die Zahlung abgelehnt wurde

## Tipps

- Überprüfen Sie täglich fehlgeschlagene Transaktionen – Muster von Fehlern (z. B. eine bestimmte Zahlungsmethode oder ein Land) können auf ein Konfigurationsproblem oder einen Betrugsversuch hinweisen.
- Webhook-Protokolle sind unverzichtbar, wenn Zahlungsunterschiede untersucht werden.

Wenn eine Bestellung bezahlt, aber nicht bestätigt wurde, wird das Webhook-Protokoll normalerweise sagen, was schiefgelaufen ist.
- Autorisierungsblockierungen verfallen automatisch – wenn Sie autorisieren und dann erfassen verwenden, stellen Sie sicher, dass Ihr Erfüllungsprozess die Mittel vor dem Ablauffenster erfassen (typischerweise 7 Tage für die meisten Anbieter).
- Das Feld **Anbieterantwort** in Transaktionen enthält die Rohdaten vom Zahlungsanbieter.

Teilen Sie dies mit dem Support-Team Ihres Anbieters, wenn Sie Hilfe bei der Behebung eines bestimmten Transaktionsproblems benötigen.
- Fehler bei der Signaturüberprüfung bei Webhooks sollten sofort untersucht werden — sie können auf eine falsch konfigurierte Webhook-Secret oder einen Versuch hinweisen, betrügerische Webhook-Events an Ihr Geschäft zu senden.