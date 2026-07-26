---
title: API-Tokens
---

API-Tokens sind sichere Schlüssel, die es externen Diensten und Integrationen ermöglichen, mit Ihrem Geschäft zu kommunizieren. Wenn ein Drittanbieter-Dienst oder ein Werkzeug auf die Daten Ihres Geschäfts zugreifen oder Aktionen auslösen muss, sendet es mit jeder Anfrage ein API-Token, damit Ihr Geschäft die Anfrage autorisieren kann. Sie erstellen und verwalten alle Tokens, einschließlich der genauen Bereiche Ihres Geschäfts, auf die sie zugreifen können, im Abschnitt API-Tokens Ihres Admin-Bereichs.

## Wann Sie ein API-Token benötigen

Sie benötigen normalerweise ein API-Token, wenn:

- Sie einen externen Dienst oder ein Automatisierungstool verbinden, das auf Ihre Daten zugreifen oder sie ändern muss
- Sie einen Webhook-Receiver einrichten, der sich bei eingehenden Anrufen authentifizieren muss
- Sie das Spwig-Hilfesystem für Ihre Installation einrichten
- Sie eine benutzerdefinierte Integration mit der Spwig-API erstellen
- Sie Daten zwischen Ihrem Spwig-Geschäft und einem anderen System synchronisieren

Jede Integration sollte ihr eigenes Token haben, damit Sie den Zugriff für einen Dienst widerrufen können, ohne andere zu beeinträchtigen.

## Token-Typen

Beim Erstellen eines Tokens wählen Sie einen Typ, der seinen Zweck beschreibt. Der Typ dient nur zur Referenz und hilft Ihnen dabei, zu erkennen, was jedes Token tut.

| Typ | Zweck |
|------|---------|
| **Hilfesystem** | Wird vom Spwig-Hilfesystem verwendet |
| **Externe Integration** | Drittanbieter-Dienste, Automatisierungstools (z. B. Zapier) oder Daten-Synchronisationstools |
| **Webhook** | Authentifizierung für Webhook-Receiver oder Endpunkte |
| **Benutzerdefiniert** | Jeder andere Zweck, der nicht in die oben genannten Kategorien passt |
| **Instanz-Synchronisation** | Synchronisation zwischen Spwig-Installationen oder externen Spwig-Diensten |

## API-Bereiche: Steuerung darüber, wohin ein Token zugreifen kann

Jedes Token hat auch einen Abschnitt **API-Bereiche**, der bestimmt, welche Teile Ihres Geschäfts es aufrufen darf. Anstatt einem Token uneingeschränkten Zugriff auf alles zu gewähren, gewähren Sie Zugriff Bereich für Bereich – und auf der Ebene, die die Integration tatsächlich benötigt.

**Ein Token, das keine Bereiche ausgewählt hat, kann keinen API-Zugriff erhalten**, auch wenn es andernfalls aktiv und gültig ist. Dies ist der Standardwert für ein neues Token, sodass eine Integration nicht funktioniert, bis Sie ihm gezielt Zugriff gewähren.

Für jeden Bereich wählen Sie eine der drei Zugriffsstufen:

| Zugriffsstufe | Was es erlaubt |
|--------------|-----------------|
| **Kein Zugriff** | Das Token kann keine Endpunkte in diesem Bereich aufrufen |
| **Lesen** | Das Token kann Daten aus diesem Bereich abrufen, kann aber nichts ändern |
| **Lesen & Schreiben** | Das Token kann Daten abrufen und sie auch erstellen, aktualisieren oder löschen |

Bereiche sind in Gruppen unterteilt, die den Bereichen Ihres Admin-Bereichs entsprechen:

| Gruppe | Bereich | Lesen & Schreiben verfügbar? | Gewährt Zugriff auf |
|-------|-------|:---:|-------------------|
| Analytics | **Verkaufsanalyse** | Nur Lesen | Verkaufs-Dashboards, KPIs, Produkt-/Kunden-/Kategorie-Analysen, Vergleiche und Exporte |
| Analytics | **Webanalyse** | Nur Lesen | Besucher- und Traffic-Analysen: Übersicht, Trends, Top-Seiten, Geografie und Verweisquellen |
| Katalog | **Produkte** | Ja | Produkte, Varianten, Bilder, Lageränderungen und Attributzuordnungen |
| Katalog | **Kategorien** | Ja | Produktkategorien, einschließlich Bilder und Bannern |
| Katalog | **Marken** | Ja | Produktmarken |
| Katalog | **Attribute** | Ja | Produktattributdefinitionen |
| Katalog | **Lager** | Ja | Lager-Dashboards, Lagergeschwindigkeit, Bewegungen, Neubestellvorschläge und Lager-Einstellungen |
| Bestellungen | **Bestellungen** | Ja | Bestellungen, Bestellnotizen, Status/Tracking-Updates, Stornierungen, Rückerstattungen und Bestellunterlagen |
| Kunden | **Kundennachrichten** | Ja | Kundennachrichten aus Kontaktformularen und Bestellnotizen, einschließlich Statusupdates und Antworten |
| Geschäft & Einstellungen | **Geschäftseinstellungen** | Ja | Geschäftseinstellungen, verfügbare Sprachen und Branding (Name, Farben, Logo) |
| Benutzer & Zugriff | **Mitarbeiter & Rollen** | Ja | Mitarbeiterkonten, Einladungen, Rollen und das Berechtigungsverzeichnis |

Die beiden **Analytics**-Bereiche sind immer nur zum Lesen verfügbar – Berichtdaten haben keinen „Schreiben“-Begriff, sodass der Auswahler nur **Kein Zugriff** oder **Lesen** für sie anbietet.

[![Der API-Bereichs-Selektor mit einer Zugriffsnotiz über den Analytics- und Katalog-Bereichsgruppen](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Unter dem Bereichs-Selektor wird eine schreibgeschützte **"Dieser Token kann auf folgende Bereiche zugreifen:"**-Zusammenfassung angezeigt, die jeden gewährten Bereich und sein Zugriffslevel auflistet. So können Sie den Zugriff eines Tokens im Blick behalten, ohne den Selektor zu entschlüsseln.

![Die "Dieser Token kann auf folgende Bereiche zugreifen:"-Zusammenfassung, die jeden gewährten Bereich und sein Lesen- oder Lesen/Schreiben-Level auflistet](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Welche Berechtigungen ein Token tatsächlich verwendet

Die Bereiche eines Tokens beschreiben das *Maximum* dessen, was es tun kann – aber das Token erbt auch die echten Berechtigungen des Mitarbeiters, der es erstellt hat:

- Das Token kann niemals mit **superuser**-Berechtigungen handeln, auch wenn der erstellende Mitarbeiter ein Superuser ist.
- **Lesen & Schreiben** in einem Bereich funktioniert nur, wenn die Rolle des erstellenden Mitarbeiters auch Schreibzugriff auf diesen Bereich erlaubt. Wenn ihre Rolle beispielsweise nur den Lesen Zugriff auf Produkte erlaubt, kann ein Token, das sie mit "Produkte: Lesen & Schreiben" erstellen, immer noch nur lesen – die Rolle fungiert als zweite Schranke über dem Bereich.
- Wenn der Mitarbeiter, der ein Token erstellt hat, gelöscht oder sein Konto deaktiviert wird, verliert das Token sofort den API-Zugriff, unabhängig von seinen Bereichen – es gibt keinen mehr zugelassenen Benutzer, für den es handeln kann.

Das bedeutet, der sicherste Weg, einen Token eng umzuschreiben, ist, ihn zu erstellen, während Sie sich als Mitarbeiter anmelden, dessen eigene Rolle bereits dem Zugriff entspricht, den Sie dem Token geben möchten.

## Erstellen eines API-Tokens

1. Navigieren Sie zu **Einstellungen > API-Tokens**
2. Klicken Sie auf **+ API-Token hinzufügen**
3. Geben Sie einen **Namen** ein, der klar beschreibt, wofür der Token verwendet wird (z. B. `Zapier Product Sync` oder `Help System API`)
4. Wählen Sie den passenden **Token-Typ** aus
5. Fügen Sie optional eine **Beschreibung** mit weiteren Details zur Integration hinzu
6. In **API-Bereichen** wählen Sie **Kein Zugriff**, **Lesen** oder **Lesen & Schreiben** für jeden Bereich, den die Integration benötigt – lassen Sie alle anderen Bereiche auf **Kein Zugriff**
7. Konfigurieren Sie den **Aktiv**-Status, das **Ablaufdatum** und die **Erlaubten IPs** nach Bedarf (siehe unten)
8. Klicken Sie auf **Speichern**

Nach dem Speichern wird der vollständige Token-Wert auf der Detailseite angezeigt. **Kopieren Sie ihn sofort** – der Token wird in der Listenansicht gemaskiert, um Sicherheit zu gewährleisten und kann nicht vollständig erneut abgerufen werden, nachdem Sie diese Seite verlassen haben.

![API-Token-Details](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sicherheit des Token-Werts

Spwig zeigt den vollständigen Token-Wert nur einmal an: unmittelbar nachdem Sie einen neuen Token gespeichert haben. Danach zeigt die Listenansicht nur eine gemaskierte Version an (z. B. `spw_••••••••••••••••••••3f8a`).

Wenn Sie einen Token-Wert verlieren, können Sie ihn nicht wiederherstellen. Sie müssen den alten Token löschen und einen neuen erstellen, und dann die Integration, die ihn verwendet hat, aktualisieren.

**Teilen Sie niemals Token-Werte per E-Mail, Chat-Nachrichten oder Quellcode.** Behandeln Sie sie wie Passwörter.

## Ablaufdatum festlegen

Das Feld **Ablaufdatum** legt ein Datum und eine Uhrzeit fest, nach der der Token automatisch nicht mehr funktioniert. Lassen Sie es leer, wenn der Token nicht ablaufen soll.

Ablaufdaten sind nützlich für:

- Temporäre Integrationen mit einem festen Enddatum
- Tokens, die Dritten gegeben werden, bei denen Sie den automatischen Zugriff entfernen möchten
- Eine zusätzliche Sicherheitsschicht für Integrationen mit hohen Berechtigungen

Wenn ein Token abläuft, werden Anfragen, die ihn verwenden, abgewiesen. Sie können den Zugriff verlängern, indem Sie das **Ablaufdatum** aktualisieren oder einen Ersatz-Token erstellen.

## Einschränkung auf bestimmte IP-Adressen

Das Feld **Erlaubte IPs** akzeptiert eine Liste von IP-Adressen. Wenn die Liste nicht leer ist, funktioniert der Token nur, wenn die Anfrage von einer dieser Adressen kommt.

Beispiel: Wenn Ihre Analysetool auf einem Server mit der IP `203.0.113.42` läuft, bedeutet das Hinzufügen dieser IP, dass der Token nicht von anderen Orten missbraucht werden kann, auch wenn er geleakt wird.

Lassen Sie **Erlaubte IPs** leer, um Anfragen von jeder IP-Adresse zuzulassen.

**Ablauf und IP-Einschränkungen werden unabhängig von Bereichen überprüft.** Ein abgelaufenes oder nicht auf der Whitelist befindliches Token wird bereits abgewiesen, bevor seine Bereiche überhaupt berücksichtigt werden, und ein Token mit umfangreichen Bereichen wird dennoch abgewiesen, sobald es abgelaufen ist oder von einer nicht aufgelisteten IP aufgerufen wird.

## API-Aufruf mit einem Token

Integrationen authentifizieren sich bei der Spwig-Admin-API, indem sie das Token in einem `Authorization`-Header senden:

```
Authorization: Bearer <your-token-value>
```

Jeder Admin-API-Endpunkt befindet sich unter `/api/admin/...`. Der Entwickler, der Ihre Integration erstellt, entscheidet, welche Endpunkte aufgerufen werden sollen – Ihre Aufgabe als Händler ist es, sicherzustellen, dass der Token-**API-Bereich** diese Endpunkte abdeckt. Wenn eine Anfrage mit einem Berechtigungsfehler abgewiesen wird, ist die erste Sache, die Sie überprüfen sollten, ob dem Token der richtige Bereich auf der richtigen Zugriffsstufe erteilt wurde.

### Beispiel: Lesen von Web-Traffic-Analysen

Spwig stellt einen Endpunkt `GET /api/admin/analytics/traffic/` bereit, der Besucher- und Traffic-Analysen für Ihr Geschäft zurückgibt – einen Überblick über Besuche und eindeutige Besucher, Trends im Zeitverlauf, beliebte Seiten, Besuchergeografie und Quellen der Besucher. Um einem Berichtstool oder Dashboard die Möglichkeit zu geben, diese Daten zu lesen:

1. Erstellen Sie ein Token (oder bearbeiten Sie ein vorhandenes) für diese Integration
2. In **API-Bereichen** setzen Sie **Web-Analysen** auf **Lesen**
3. Speichern Sie das Token und geben Sie es der Integration weiter

Da **Web-Analysen** ein schreibgeschützter Bereich ist, gibt es keine „Lesen & Schreiben“-Option zur Auswahl – die Integration kann nur Analysedaten abrufen, nie die Konfiguration Ihres Geschäfts ändern.

## Überwachung der Token-Nutzung

Die Token-Liste zeigt an:

- **Nutzungszähler** – Gesamtzahl der Male, die das Token genutzt wurde
- **Zuletzt genutzt** – Wann das Token zuletzt genutzt wurde, um eine Anfrage zu stellen

Diese Felder helfen Ihnen dabei, ungenutzte Tokens (Kandidaten für die Widerrufung) zu identifizieren und unerwartete Aktivitäten zu erkennen. Ein plötzlicher Anstieg der Nutzungszahl kann darauf hindeuten, dass das Token von jemand anderem als der vorgesehenen Integration genutzt wird.

## Widerrufen eines Tokens

Um ein Token sofort zu deaktivieren, ohne es zu löschen:

1. Klicken Sie auf den Token-Namen
2. Deaktivieren Sie **Aktiv**
3. Speichern Sie die Änderung

Das Token bleibt in Ihrer Liste als Referenz vorhanden, wird aber bei allen nachfolgenden Anfragen abgewiesen. Dies ist nützlich, wenn Sie eine Integration vorübergehend aussetzen müssen, während Sie ein Problem untersuchen.

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
| API-Bereiche | **Bestellungen**: Lesen & Schreiben |
| Aktiv | Ja |
| Ablaufdatum | *(leer lassen)* |
| Erlaubte IPs | *(leer lassen – Zapier verwendet dynamische IPs)* |

Nur der **Bestellungen**-Bereich wird erteilt, sodass dieses Token, selbst wenn es jemals exponiert würde, keine Produkte, Kundennachrichten, Mitarbeiterkonten oder andere Teile Ihres Geschäfts berühren könnte. Nach dem Speichern kopieren Sie den vollständigen Token-Wert und fügen Sie ihn in die Spwig-Integrationseinstellungen von Zapier ein.

- Geben Sie jedem Token einen klaren, spezifischen Namen – `Shopify Sync v2` ist viel nützlicher als `Token 3`, wenn Sie sich Monate später bei Problemen befinden
- Erstellen Sie ein Token pro Integration – wenn eine Integration kompromittiert wird, können Sie nur dieses Token widerrufen, ohne andere zu stören
- **Geben Sie nur die Bereiche (Scopes) zu, die eine Integration tatsächlich benötigt** – ein Berichtstool benötigt nur Lesezugriff auf Verkaufsanalysen oder Webanalysen, nicht Lese- und Schreibzugriff auf Produkte oder Mitarbeiter und Rollen
- Überprüfen Sie die Zusammenfassung **„Dieses Token kann auf folgende Bereiche zugreifen:“** auf dem Änderungsformular, bevor Sie ein Token einer dritten Partei übergeben – dies ist die schnellste Möglichkeit, um sicherzustellen, dass Sie nicht mehr Zugriff gewährt haben, als beabsichtigt
- Denken Sie daran, dass Schreibzugriff auch vom eigenen Rollenstatus des erstellenden Mitarbeiters abhängt – wenn ein Bereich Lese- und Schreibzugriff anzeigt, aber Schreibvorgänge dennoch fehlschlagen, überprüfen Sie auch die Berechtigungen dieser Benutzerrolle
- Setzen Sie ein Ablaufdatum für Tokens, die in Einmalprojekten oder temporären Integrationen verwendet werden – dies verringert das Risiko, dass vergessene Tokens unbegrenzt aktiv bleiben
- Überprüfen Sie Ihre Tokenliste alle paar Monate und deaktivieren Sie alle Tokens, deren **Letzter Verwendet**-Datum unerwartet alt ist, da diese möglicherweise zu Integrationen gehören, die nicht mehr laufen
- Wenn Sie vermuten, dass ein Token preisgegeben wurde, deaktivieren Sie es sofort, erstellen Sie ein Ersatztoken und aktualisieren Sie die betroffene Integration, bevor Sie den Zugriff wieder aktivieren