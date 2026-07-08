---
title: Webhook-Lieferprotokolle
---

Jedes Mal, wenn Ihr Geschäft versucht, einen Webhook zu senden, wird ein Lieferprotokoll erstellt. Diese Protokolle ermöglichen es Ihnen, genau zu sehen, was gesendet wurde, ob es erfolgreich war und was während der Wiederholungsversuche passiert ist. Dieser Leitfaden erklärt, wie Sie die Lieferprotokolle lesen und Probleme beheben, wenn Lieferungen fehlschlagen.

## Anzeigen von Lieferprotokollen

Navigieren Sie zu **Integrationen > Webhook-Lieferungen**, um die vollständige Historie aller Webhook-Lieferversuche für alle Ihre Endpunkte anzuzeigen.

![Webhook-Lieferprotokolle](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

Die Liste zeigt den Namen des Endpunkts, den Ereignistyp, den Status, den HTTP-Antwortcode, die Antwortzeit und die Anzahl der Versuche für jede Lieferung an.

Lieferprotokolle sind schreibgeschützt – sie werden automatisch erstellt, wenn Ereignisse ausgelöst werden und können nicht bearbeitet werden.

## Lieferstatus

Jede Lieferung hat einen dieser Status:

| Status | Was es bedeutet |
|--------|---------------|
| **Ausstehend** | Die Lieferung ist in der Warteschlange und wurde noch nicht versucht |
| **Erfolgreich** | Der Empfangsserver antwortete mit einem HTTP 2xx-Statuscode – Lieferung bestätigt |
| **Fehlgeschlagen** | Alle Lieferversuche sind abgeschlossen – die Lieferung wird nicht erneut versucht |
| **Wiederholung** | Der letzte Versuch ist fehlgeschlagen, aber das System wird zur geplanten Wiederholungszeit erneut versuchen |
| **Sandbox-Blockiert** | Die Lieferung wurde blockiert, weil die Endpunkt-URL im aktuellen Umfeld nicht erreichbar ist |

Eine Lieferung gilt als erfolgreich, wenn der Empfangsserver einen beliebigen HTTP 2xx-Antwortcode (200, 201, 202 usw.) zurückgibt. Jede andere Antwort – einschließlich 3xx-Umleitungen oder 4xx/5xx-Fehler – wird als Fehlschlag behandelt.

## Filtern von Lieferungen

Verwenden Sie das Filterpanel auf der rechten Seite, um die Liste zu verfeinern:

- **Status** – Zeigen Sie nur fehlgeschlagene, wiederholte oder erfolgreiche Lieferungen an
- **Ereignistyp** – Zeigen Sie alle Lieferungen für einen bestimmten Ereignistyp an (z. B. alle `order.created`-Lieferungen)
- **Endpunkt** – Zeigen Sie Lieferungen für einen bestimmten Endpunkt an
- **Erstellt um** – Filtern Sie nach Datumsbereich

Verwenden Sie die Suchleiste, um nach Ereignistyp oder Endpunktname zu suchen oder eine bestimmte Lieferung anhand ihrer ID zu finden.

## Lieferdetail ansehen

Klicken Sie auf eine Lieferung, um ihre vollständigen Details anzuzeigen. Lieferprotokolle sind schreibgeschützt.

### Zusammenfassung

- **ID** – Die eindeutige Kennung für diesen Lieferversuch
- **Endpunkt** – Zu welchem Webhook-Endpunkt diese gesendet wurde (verknüpft mit dem Endpunkt-Protokoll)
- **Ereignistyp** – Das Ereignis, das diese Lieferung ausgelöst hat (z. B. `order.paid`)
- **Status** – Aktueller Lieferstatus

### Nutzlast

Der Abschnitt **Nutzlast** zeigt die exakte JSON-Daten an, die an Ihren Endpunkt gesendet wurden. Dies umfasst den Ereignistyp, einen Zeitstempel und die vollständigen Ereignisdaten. Verwenden Sie dies, um sicherzustellen, dass Ihr Empfangsserver die richtige Datenstruktur erhält.

### Antwort

Der Abschnitt **Antwort** zeigt an, was Ihr Server zurückgab:

- **Antwortstatuscode** – Der HTTP-Statuscode, der von Ihrem Server zurückgegeben wurde. Farbkodiert: grün für 2xx (Erfolg), gelb für 4xx (Clientfehler), rot für 5xx (Serverfehler).
- **Antwortzeit** – Wie lange Ihr Server benötigte, um zu antworten, in Millisekunden. Farbkodiert: grün unter 500 ms, gelb bis zu 2 Sekunden, rot über 2 Sekunden.
- **Antworttext** – Der Text der Antwort Ihres Servers (auf 1.000 Zeichen gekürzt). Dies kann helfen, den Grund zu erkennen, warum Ihr Server den Webhook abgelehnt hat.
- **Antwortheader** – Die Header, die von Ihrem Server zurückgegeben wurden.

### Fehlerdetails

Wenn die Lieferung fehlgeschlagen ist, zeigt der Abschnitt **Fehlerdetails** die Fehlermeldung an – z. B. `Verbindung abgelehnt`, `Zeitüberschreitung nach 30s` oder den HTTP-Fehler von Ihrem Server.

### Wiederholungsinformationen

- **Anzahl der Versuche** – Wie viele Lieferversuche durchgeführt wurden (einschließlich des ersten Versuchs)
- **Nächster Wiederholungsversuch um** – Wann der nächste Wiederholungsversuch stattfinden wird (nur für Lieferungen im Status **Wiederholung** angezeigt)

Wiederholungen folgen einem exponentiellen Abstandsschema – der Abstand zwischen Wiederholungen wird mit jedem Versuch vergrößert, um einen Server zu vermeiden, der vorübergehend nicht erreichbar ist. Mit maximal 5 Wiederholungen (Standard) erstreckt sich das Wiederholungsschema über mehrere Stunden.

## Manuell fehlgeschlagene Lieferungen erneut versuchen

Wenn Sie eine Lieferung sofort erneut versenden möchten, ohne auf den automatischen Zeitplan zu warten:

1. Markieren Sie die Kontrollkästchen neben den Lieferungen, die Sie erneut versenden möchten
2. Wählen Sie aus dem **Aktion**-Dropdownmenü **Ausgewählte Lieferungen erneut versenden** aus
3. Klicken Sie auf **Weiter**

Nur Lieferungen, die nicht bereits den Status **Erfolgreich** haben, werden für eine erneute Verarbeitung in die Warteschlange gestellt. Erfolgreiche Lieferungen werden übersprungen.

Dies ist nützlich, wenn Sie ein Problem mit Ihrem Empfangsserver behoben haben und fehlgeschlagene Ereignisse ohne Wartezeit erneut verarbeiten möchten.

## Diagnose häufiger Fehler

### HTTP 4xx-Statuscodes

Eine 4xx-Antwort von Ihrem Server bedeutet in der Regel, dass ein Problem mit der Anfrage besteht – die Authentifizierung ist fehlgeschlagen, die Endpunkt-URL hat sich geändert oder Ihr Server hat das Payload-Format abgelehnt. Überprüfen Sie:

- Ist die Endpunkt-URL korrekt?
- Überprüft Ihr Server den HMAC-Signatur richtig? Ein Mismatch führt bei vielen Servern zu einer 401- oder 403-Antwort.
- Hat sich die Payload-Struktur geändert? Vergleichen Sie die Payload in der Lieferprotokollierung mit dem, was Ihr Server erwartet.

### HTTP 5xx-Statuscodes

Eine 5xx-Antwort bedeutet, dass Ihr Server während der Verarbeitung des Webhooks einen internen Fehler hatte. Überprüfen Sie die eigenen Fehlerprotokolle Ihres Servers, um das Problem zu diagnostizieren.

### Verbindung abgelehnt / Timeout

Diese Fehler bedeuten, dass Spwig Ihren Server überhaupt nicht erreichen konnte:

- Läuft der Server und ist öffentlich zugänglich?
- Ist die URL korrekt (einschließlich des richtigen Protokolls – http oder https)?
- Blockiert ein Firewall die eingehenden Anfragen?
- Überschreitet die Antwortzeit des Servers die konfigurierte Timeout-Zeit? Wenn ja, erhöhen Sie die **Timeout**-Einstellung am Endpunkt oder optimieren Sie den Webhook-Handler Ihres Servers, um schnell zu reagieren (idealerweise innerhalb von 5 Sekunden).

### Sandbox Blockiert

Lieferungen werden an localhost-URLs oder interne Netzwerkadressen blockiert. Webhook-Endpunkte müssen öffentlich erreichbar sein. Verwenden Sie während der Entwicklung ein Tool wie ngrok, um einen lokalen Server öffentlich zu machen.

## Tipps

- Behandeln Sie **Fehlgeschlagene** Lieferungen schnell – die Ereignisdaten sind immer noch im Payload enthalten, und Sie können die Lieferung manuell erneut versenden, sobald das Problem behoben ist.
- Wenn Sie viele **Wiederholungen** für einen Endpunkt sehen, öffnen Sie das Endpunktrekord und prüfen Sie den **Gesundheitszustand**-Abschnitt – der Endpunkt könnte bald automatisch deaktiviert werden.
- Antwortzeit ist wichtig: Konfigurieren Sie Ihren Webhook-Handler so, dass er schnell reagiert (innerhalb weniger Sekunden) und verarbeiten Sie das Payload asynchron im Hintergrund. Ein langsamer Handler führt zu Timeout-Fehlern, auch wenn Ihre Logik korrekt ist.
- Verwenden Sie den **Ereignistyp**-Filter, um die Lieferhistorie für einen bestimmten Ereignistyp zu überprüfen, wenn Sie untersuchen, ob Ihre Integration die richtigen Ereignisse empfängt.
- Lieferprotokolle sammeln sich im Laufe der Zeit an. Verwenden Sie den Datumsfilter, um sich auf kürzliche Lieferungen zu konzentrieren und alte Historie zu vermeiden.