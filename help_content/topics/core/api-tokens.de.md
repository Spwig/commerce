---
title: API-Tokens
---

API-Tokens sind sichere Schlüssel, die es externen Diensten und Integrationen ermöglichen, mit Ihrem Geschäft zu kommunizieren. Wenn ein Drittanbieter-Dienst oder ein Tool auf die Daten Ihres Geschäfts zugreifen oder Aktionen auslösen muss, sendet es mit jeder Anfrage ein API-Token, damit Ihr Geschäft die Anfrage autorisieren kann. Sie erstellen und verwalten alle Tokens im Abschnitt **API-Tokens** Ihres Admin-Bereichs.

## Wann Sie ein API-Token benötigen

Sie benötigen normalerweise ein API-Token, wenn:

- Sie ein externes Dienstprogramm oder eine Automatisierungstool verbinden, das auf Ihre Geschäfte zugreifen muss
- Sie einen Webhook-Receiver einrichten, der sich bei eingehenden Anrufen authentifizieren muss
- Sie das Spwig-Hilfesystem für Ihre Installation konfigurieren
- Sie eine benutzerdefinierte Integration mit der Spwig-API erstellen
- Sie Daten zwischen Ihrem Spwig-Geschäft und einem anderen System synchronisieren

Jede Integration sollte ihr eigenes Token haben, damit Sie den Zugriff für einen Dienst widerrufen können, ohne andere zu beeinträchtigen.

## Token-Typen

Bei der Erstellung eines Tokens wählen Sie einen Typ, der seinen Zweck beschreibt. Der Typ dient nur zur Referenz und hilft Ihnen dabei, zu erkennen, was jedes Token tut.

| Typ | Zweck |
|------|---------|
| **Hilfesystem** | Wird vom Spwig-Hilfesystem verwendet |
| **Externe Integration** | Drittanbieter-Dienste, Automatisierungstools (z. B. Zapier) oder Daten-Synchronisationstools |
| **Webhook** | Authentifizierung für Webhook-Receiver oder Endpunkte |
| **Benutzerdefiniert** | Jeder andere Zweck, der nicht in die oben genannten Kategorien passt |
| **Instanz-Synchronisation** | Synchronisation zwischen Spwig-Installationen oder externen Spwig-Diensten |

## API-Token erstellen

1. Navigieren Sie zu **Einstellungen > API-Tokens**
2. Klicken Sie auf **+ API-Token hinzufügen**
3. Geben Sie einen **Namen** ein, der klar beschreibt, wofür das Token verwendet wird (z. B. `Zapier Produkt-Synchronisation` oder `Hilfesystem-API`)
4. Wählen Sie den passenden **Token-Typ** aus
5. Fügen Sie optional eine **Beschreibung** mit weiteren Details zur Integration hinzu
6. Konfigurieren Sie den **Aktiv**-Status, das **Ablaufdatum** und die **Erlaubten IPs** nach Bedarf (siehe unten)
7. Klicken Sie auf **Speichern**

Nach dem Speichern wird der vollständige Token-Wert auf der Detailseite angezeigt. **Kopieren Sie ihn sofort** – der Token wird in der Listenansicht gemaskiert, um Sicherheit zu gewährleisten und kann nachdem Sie diese Seite verlassen haben nicht vollständig wiederhergestellt werden.

![API-Token-Details](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sicherheit des Token-Werts

Spwig zeigt den vollständigen Token-Wert nur einmal an: unmittelbar nachdem Sie einen neuen Token gespeichert haben. Danach zeigt die Listenansicht nur eine gemaskierte Version an (z. B. `spw_••••••••••••••••••••3f8a`).

Wenn Sie einen Token-Wert verlieren, können Sie ihn nicht wiederherstellen. Sie müssen den alten Token löschen und einen neuen erstellen und dann die Integration aktualisieren, die ihn verwendet hat.

**Teilen Sie niemals Token-Werte per E-Mail, Chat-Nachricht oder Quellcode.** Behandeln Sie sie wie Passwörter.

## Ablaufdatum festlegen

Das Feld **Ablaufdatum** legt ein Datum und eine Uhrzeit fest, nach der der Token automatisch nicht mehr funktioniert. Lassen Sie es leer, wenn der Token nicht ablaufen soll.

Ablaufdaten sind nützlich für:

- Temporäre Integrationen mit einem festen Enddatum
- Tokens, die Dritten gegeben werden, bei denen Sie eine automatische Zugriffsberechtigungsbekanntgabe wünschen
- Eine zusätzliche Sicherheitsschicht für Integrationen mit hohen Berechtigungen

Wenn ein Token abgelaufen ist, werden Anfragen, die ihn verwenden, abgewiesen. Sie können den Zugriff durch Aktualisierung des **Ablaufdatums** oder durch Erstellen eines Ersatztokens verlängern.

## Einschränkung auf bestimmte IP-Adressen

Das Feld **Erlaubte IPs** akzeptiert eine Liste von IP-Adressen. Wenn die Liste nicht leer ist, funktioniert der Token nur, wenn die Anfrage von einer dieser Adressen kommt.

Beispiel: Wenn Ihr Analysetool auf einem Server mit der IP-Adresse `203.0.113.42` läuft, bedeutet das Hinzufügen dieser IP, dass der Token nicht von anderen Orten missbraucht werden kann, auch wenn er geleakt wird.

Lassen Sie **Erlaubte IPs** leer, um Anfragen von jeder IP-Adresse zuzulassen.

## Überwachung der Token-Nutzung

Die Token-Liste zeigt an:

- **Nutzungszähler** – Gesamtzahl der Male, in denen der Token genutzt wurde
- **Zuletzt genutzt** – Wann der Token zuletzt genutzt wurde, um eine Anfrage zu stellen

Diese Felder helfen Ihnen dabei, ungenutzte Tokens (Kandidaten für Widerruf) zu identifizieren und unerwartete Aktivitäten zu erkennen.

Ein plötzlicher Anstieg der Nutzungszahl kann darauf hindeuten, dass ein Token von jemandem verwendet wird, der nicht der beabsichtigten Integration entspricht.

## Token widerrufen

Um ein Token sofort zu deaktivieren, ohne es zu löschen:

1. Klicken Sie auf den Token-Namen
2. Deaktivieren Sie **Aktiv**
3. Speichern Sie die Änderung

Das Token bleibt in Ihrer Liste, um sich als Referenz dienen zu können, wird aber bei allen nachfolgenden Anfragen abgelehnt. Dies ist nützlich, wenn Sie eine Integration vorübergehend aussetzen müssen, während Sie ein Problem untersuchen.

Um ein Token dauerhaft zu entfernen:

1. Wählen Sie das Häkchen in der Liste aus
2. Wählen Sie **Ausgewählte API-Tokens löschen** aus dem Aktionen-Menü aus
3. Löschen Sie bestätigt

Nach dem Löschen kann ein Token nicht wiederhergestellt werden. Wenn die Integration weiterhin Zugriff benötigt, erstellen Sie ein neues Token und aktualisieren Sie die Konfiguration der Integration.

## Beispiel: Einrichten einer Zapier-Integration

**Szenario:** Sie möchten Ihr Geschäft mit Zapier verbinden, um Bestellbenachrichtigungen zu automatisieren.

| Feld | Wert |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token-Typ | Externe Integration |
| Beschreibung | Wird von Zapier verwendet, um neue Bestellungen zu lesen und Benachrichtigungen auszulösen |
| Aktiv | Ja |
| Ablaufdatum | *(leer lassen)* |
| Erlaubte IPs | *(leer lassen — Zapier verwendet dynamische IPs)* |

Nach dem Speichern kopieren Sie den vollständigen Token-Wert und fügen Sie ihn in die Zapier-Einstellungen für die Spwig-Integration ein.

## Tipps

- Geben Sie jedem Token einen klaren, spezifischen Namen — `Shopify Sync v2` ist viel nützlicher als `Token 3`, wenn Sie sich Monate später bei der Problembehebung befinden
- Erstellen Sie ein Token pro Integration — wenn eine Integration kompromittiert wird, können Sie nur dieses Token widerrufen, ohne andere zu stören
- Setzen Sie ein Ablaufdatum für Tokens, die in Einmalprojekten oder temporären Integrationen verwendet werden — dies verringert das Risiko, dass vergessene Tokens unbegrenzt aktiv bleiben
- Überprüfen Sie Ihre Token-Liste alle paar Monate und deaktivieren Sie alle Tokens, deren **Letzter Verwendungstag** unerwartet alt ist, da diese möglicherweise zu Integrationen gehören, die nicht mehr laufen
- Wenn Sie vermuten, dass ein Token preisgegeben wurde, deaktivieren Sie es sofort, erstellen Sie einen Ersatz und aktualisieren Sie die betroffene Integration, bevor Sie den Zugriff wieder aktivieren