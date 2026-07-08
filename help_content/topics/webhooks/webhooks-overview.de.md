---
title: Übersicht zu Webhooks
---

Webhooks ermöglichen es Ihrem Geschäft, externe Systeme automatisch zu benachrichtigen – wie z. B. Lagerverwaltungstools, ERP-Systeme, Versanddienste oder benutzerdefinierte Anwendungen – sobald etwas in Ihrem Geschäft geschieht. Anstatt, dass diese Systeme immer wieder fragen, ob sich etwas geändert hat, sendet Ihr Geschäft eine Benachrichtigung, sobald ein Ereignis eintritt.

## Was Webhooks tun

Wenn ein Ereignis in Ihrem Geschäft stattfindet (z. B. wird eine Bestellung aufgegeben, eine Zahlung empfangen oder ein Produkt ausverkauft ist), sendet Spwig eine HTTP-POST-Anfrage mit den Ereignisdaten an eine von Ihnen konfigurierte URL. Das empfangende System kann dann sofort mit diesen Daten arbeiten – beispielsweise das Lager aktualisieren, eine Versandetikette auslösen oder eine benutzerdefinierte Benachrichtigung senden.

Häufige Anwendungsfälle für Webhooks sind:

- Echtzeit-Synchronisation von Bestellungen mit einem Versandpartner
- Aktualisierung des Lagers in einem ERP, wenn sich der Lagerbestand ändert
- Auslösung von SMS- oder Push-Benachrichtigungen bei Änderungen des Bestellstatus
- Erfassen von Ereignissen in einem Datenwarehouse für Berichte
- Verbindung mit Automatisierungstools wie Zapier oder Make

## Anzeigen und Verwalten von Endpunkten

Navigieren Sie zu **Integrationen > Webhooks**, um alle konfigurierten Webhook-Endpunkte anzuzeigen.

![Liste der Webhook-Endpunkte](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

Die Liste zeigt für jeden Endpunkt den Namen, die URL, den Aktivstatus, die Anzahl der Ereignisse, zu denen er abonniert ist, seinen Gesundheitsstatus und den Zeitpunkt des letzten Empfangs einer Lieferung an.

### Gesundheitsindikatoren

Die Spalte **Gesundheit** zeigt auf einen Blick an, wie gut jeder Endpunkt funktioniert:

- **Gesund** – Alle kürzlichen Lieferungen waren erfolgreich
- **Eingeschränkt** – Einige kürzliche Fehler, aber der Endpunkt ist weiterhin aktiv
- **Nicht gesund / Deaktiviert** – Der Endpunkt wurde automatisch deaktiviert, nachdem zu viele aufeinanderfolgende Fehler aufgetreten sind (standardmäßig 10). Sie müssen ihn manuell erneut aktivieren, sobald das zugrunde liegende Problem behoben ist.

## Erstellen eines Webhook-Endpunkts

Klicken Sie auf **+ Webhook-Endpunkt hinzufügen**, um den Einrichtungsführer zu öffnen. Der Führer führt Sie durch vier Schritte.

### Schritt 1: Grundlegende Informationen

- **Name** – Ein freundlicher Bezeichner, um diesen Endpunkt zu identifizieren (z. B. `Order Fulfilment Service` oder `Inventory Sync`).
- **URL** – Die vollständige URL des Servers, der die Webhook-POST-Anfragen empfangen wird. Dies muss öffentlich erreichbar sein (keine localhost-URL).
- **Beschreibung** – Optionale Notizen, um zu beschreiben, wofür dieser Endpunkt verwendet wird.
- **Aktiv** – Ob dieser Endpunkt Lieferungen empfangen soll. Deaktivieren Sie dies, um den Endpunkt vorübergehend zu pausieren, ohne ihn zu löschen.

### Schritt 2: Ereignisabonnements

Wählen Sie aus, welche Ereignisse eine Lieferung an diesen Endpunkt auslösen sollen. Ereignisse sind nach Kategorien gruppiert:

#### Bestellereignisse

| Ereignis | Wann wird es ausgelöst |
|---------|----------------------|
| `order.created` | Eine neue Bestellung wird aufgegeben |
| `order.paid` | Die Zahlung für eine Bestellung wird bestätigt |
| `order.cancelled` | Eine Bestellung wird storniert |
| `order.fulfilled` | Alle Artikel einer Bestellung werden versandt |
| `order.partially_fulfilled` | Einige Artikel einer Bestellung werden versandt |
| `order.status_changed` | Der Bestellstatus ändert sich |
| `order.note_added` | Eine Notiz wird einer Bestellung hinzugefügt |

#### Zahlungsevents

| Ereignis | Wann wird es ausgelöst |
|---------|----------------------|
| `payment.received` | Eine Zahlung wird empfangen |
| `payment.failed` | Ein Zahlungsversuch schlägt fehl |
| `payment.pending` | Eine Zahlung wartet auf Bestätigung |

#### Versandereignisse

| Ereignis | Wann wird es ausgelöst |
|---------|----------------------|
| `shipment.created` | Ein Versand wird erstellt |
| `shipment.shipped` | Ein Versand wird versandt |
| `shipment.delivered` | Ein Versand wird geliefert |
| `shipment.returned` | Ein Versand wird zurückgesandt |
| `shipment.tracking_updated` | Versandverfolgungsinformationen werden aktualisiert |

#### Lagerereignisse

| Ereignis | Wann wird es ausgelöst |
|---------|----------------------|
| `inventory.low_stock` | Der Lagerbestand fällt unter den Schwellenwert |
| `inventory.out_of_stock` | Ein Produkt geht aus dem Lager |
| `inventory.restocked` | Ein Produkt wird wieder aufgefüllt |
| `inventory.adjusted` | Der Lagerbestand wird manuell angepasst |

#### Produktereignisse

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

#### Kundenevents


`customer.created`, `customer.updated`, `customer.deleted`

#### Subscription events

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Other events

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Um alle Ereignisse zu erhalten, abonnieren Sie `*` (Wildcard). Dies ist nützlich für allgemeine Protokollierungsendpunkte, erzeugt aber mehr Traffic – abonnieren Sie nur die Ereignisse, die Sie tatsächlich für Produktionsintegrationen benötigen.

### Schritt 3: Konfiguration

- **Max Retries** — Wie oft Spwig eine fehlgeschlagene Lieferung wiederholen soll, bevor es aufgibt (Standardwert: 5). Jede Wiederholung verwendet exponentielle Abstandsberechnung.
- **Timeout (Sekunden)** — Wie lange gewartet werden soll, bis der Empfangsserver antwortet, bevor die Lieferung als fehlgeschlagen markiert wird (Standardwert: 30 Sekunden). Erhöhen Sie dies nur, wenn Ihr Server bekanntermaßen langsam ist.

### Schritt 4: Sicherheit

Jeder Webhook-Endpunkt erhält einen automatisch generierten **Signaturgeheimnis** – einen 64-Zeichen langen Zufallsschlüssel. Spwig verwendet diesen Schlüssel, um jede Webhook-Nutzlast mit einer HMAC-SHA256-Signatur zu signieren.

Die Signatur wird im Anfrageheader `X-Webhook-Signature` enthalten. Ihr Empfangsserver sollte diese Signatur überprüfen, um sicherzustellen, dass die Anfrage tatsächlich von Ihrem Store stammt und nicht manipuliert wurde.

Das Geheimnis wird im Admin-Bereich maskiert angezeigt. Um das Geheimnis anzuzeigen oder zu drehen, verwenden Sie die Spwig-API. Drehen Sie Ihr Geheimnis sofort um, wenn Sie vermuten, dass es kompromittiert wurde.

## Aktivieren und Deaktivieren von Endpunkten

Um Endpunkte schnell zu aktivieren oder zu deaktivieren, ohne jeden einzeln zu öffnen:

1. Wählen Sie die Kontrollkästchen neben den Endpunkten, die Sie ändern möchten
2. Verwenden Sie das **Aktion**-Dropdown, um **Ausgewählte Endpunkte aktivieren** oder **Ausgewählte Endpunkte deaktivieren** auszuwählen
3. Klicken Sie auf **Weiter**

Um einen Endpunkt zu reaktivieren, der aufgrund von Fehlern automatisch deaktiviert wurde, wählen Sie ihn aus und verwenden Sie die Aktion **Fehlerzähler zurücksetzen**, dann aktivieren Sie ihn erneut. Beheben Sie zunächst das Problem, das die Fehler verursacht hat, andernfalls wird der Endpunkt schnell erneut deaktiviert.

## Tipps

- Abonnieren Sie nur die Ereignisse, die Sie tatsächlich benötigen – unnötige Ereignisse erzeugen Lärm in Ihren Protokollen und erhöhen die Lieferlast.
- Überprüfen Sie immer die Webhook-Signatur auf Ihrem Empfangsserver, bevor Sie die Nutzlast verarbeiten. Dies schützt Sie vor gefälschten Anfragen.
- Verwenden Sie das **Beschreibung**-Feld, um zu dokumentieren, welches System oder welche Integration dieser Endpunkt verbindet. Dies hilft bei der Fehlerbehebung Monate später.
- Legen Sie einen **Timeout** etwas über die typische Antwortzeit Ihres Servers fest. Ein Timeout von 10–15 Sekunden ist für die meisten Integrationen ausreichend.
- Wenn ein Endpunkt **Unhealthy** wird, prüfen Sie zunächst die Lieferprotokolle (siehe **Webhook-Lieferungen**), um das Fehlervpattern zu verstehen, bevor Sie ihn erneut aktivieren.
- Für Tests können Sie Webhooks an ein Tool wie [webhook.site](https://webhook.site) weiterleiten, um die Rohnutzlasten zu inspizieren, ohne einen Live-Server zu benötigen.