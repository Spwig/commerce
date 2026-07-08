---
title: Affiliate-Tracking & -Links
---

Affiliate-Tracking ermöglicht das gesamte Kommissionsystem, indem es den Kauf von Kunden mit den Affiliate-Partnern verknüpft, die sie verweisen. Dieser Leitfaden erklärt, wie Tracking-Links funktionieren, welche Daten Spwig aufzeichnet, wenn Kunden auf diese Links klicken, und wie das Cookie-basierte Zuordnungssystem bestimmt, welcher Affiliate für jede Kommission berechtigt ist.

Das Verständnis der Tracking-Mechanismen hilft Ihnen bei der Behebung von Zuordnungsproblemen, bei der Analyse der Leistung von Links und bei der Aufklärung Ihrer Affiliates darüber, wie sie ihre Konversionen maximieren können.

## Was ist ein Tracking-Link?

Ein Tracking-Link ist eine eindeutige URL, die Kunden zu Ihrem Geschäft weiterleitet, während sie die Identität des Affiliates in einem Cookie aufzeichnen. Jeder Affiliate kann mehrere Tracking-Links erstellen, die auf verschiedene Ziele verweisen — die Startseite, bestimmte Produkte, Sammlungsseiten oder Landingpages.

Beispiel für einen Tracking-Link:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Dieser Link leitet zum Ziel weiter, während er ein Tracking-Cookie setzt, das zukünftige Käufe mit dem Affiliate verknüpft, der den Link-Code `a2b7f8c4d1e9` besitzt.

Affiliates generieren diese Links über ihr Portal-Dashboard. Sie kopieren die vollständige URL und teilen sie in Blog-Beiträgen, sozialen Medien, E-Mails oder jedem anderen Kanal, über den sie potenzielle Kunden erreichen.

## Komponenten eines Tracking-Links

Jeder Tracking-Link enthält diese Elemente:

| Komponente | Beispiel | Beschreibung |
|-----------|---------|-------------|
| **Grund-URL** | `https://yourstore.com` | Ihr Geschäftsbereich |
| **Tracking-Pfad** | `/affiliate/track/` | Spwig-Endpunkt für Tracking |
| **Link-Code** | `a2b7f8c4d1e9` | Automatisch generierter 12-stelliger eindeutiger Identifier |
| **Ziel** | Wird festgelegt, wenn der Link erstellt wird | Wo der Kunde nach der Weiterleitung landet (Startseite, Produkt, etc.) |

Wenn ein Affiliate einen Link erstellt, generiert Spwig automatisch den eindeutigen 12-stelligen Code. Der Affiliate muss diesen Code nie manuell erstellen oder bearbeiten — er wählt einfach das Ziel und Spwig übernimmt den Rest.

### Link-Bezeichnungen (optional)

Affiliates können jedem Link eine Bezeichnung hinzufügen, um ihre eigenen Organisation zu erleichtern:
- "Instagram Bio-Link"
- "YouTube-Beschreibung"
- "Black Friday E-Mail-Kampagne"

Bezeichnungen helfen Affiliates dabei, zu erkennen, welche Werbekanäle am besten funktionieren. Sie sind nur für den Affiliate und Sie sichtbar — Kunden sehen die Bezeichnung nie.

## Wie funktioniert das Tracking?

Der Tracking- und Zuordnungsprozess folgt fünf Schritten vom Klick bis zur Kommission:

### 1. Kunde klickt auf den Link

Ein potenzieller Kunde klickt auf den Tracking-Link des Affiliates aus jedem Werbekanal (sozialer Beitrag, Blog-Artikel, E-Mail-Newsletter).

### 2. Klick wird aufgezeichnet

Der Tracking-Endpunkt von Spwig protokolliert die Klickdetails:
- IP-Adresse
- User-Agent (Browser und Gerät)
- HTTP-Referer (Woher der Klick kam)
- Zeitstempel
- Sitzungsid

Diese Daten erscheinen im **Klicks**-Admin unter **Affiliate > Klicks** für Analysen und Betrugsdetektion.

### 3. Cookie wird gesetzt

Das Tracking-System setzt einen Cookie im Browser des Kunden, bevor er weitergeleitet wird. Der Cookie enthält:
- Affiliate-ID (wer die Kommission verdient)
- Programmid (welche Kommissionsstruktur gilt)
- Link-Code (welcher spezifische Link geklickt wurde)

### 4. Kunde kauft

Der Kunde durchsucht Ihr Geschäft und vervollständigt einen Kauf. Dies kann sofort oder Tage/Wochen später geschehen, solange er innerhalb des Cookie-Laufzeitfensters kauft.

### 5. Kommission wird erstellt

Bei der Kasse prüft Spwig auf den Affiliate-Cookie. Wenn dieser gefunden und noch gültig ist (innerhalb der Cookie-Laufzeit), erstellt das System eine Kommissionsaufzeichnung mit dem **Ausstehend**-Status, die mit dem Affiliate, dem Programm und der Bestellung verknüpft ist.

## Cookie-basierte Zuordnung

Der Tracking-Cookie ist der zentrale Mechanismus, der Käufe mit Affiliates verknüpft. Das Verständnis davon hilft Ihnen, optimale Zuordnungsfenster festzulegen und Tracking-Probleme zu beheben.

### Cookie-Struktur

| Eigenschaft | Wert |
|----------|-------|
| **Name** | `aff_{program_id}` (z. B. `aff_7` für Programmid 7) |
| **Wert** | JSON mit Affiliate-ID, Link-Code, Zeitstempel |
| **Domain** | Ihr Geschäftsbereich |
| **Pfad** | `/` (Site-weit zugänglich) |
| **Dauer** | Cookie-Laufzeit des Programms (1–365 Tage) |
| **HttpOnly** | `true` (verhindert JavaScript-Zugriff für Sicherheit) |
| **SameSite** | `Lax` (erlaubt Tracking von externen Referern) |
| **Secure** | `true` auf HTTPS-Webseiten (empfohlen) |

### Cookie-Laufzeitfenster

Die Cookie-Laufzeit bestimmt, wie lange Kunden einen Kauf tätigen können, nachdem sie auf einen Affiliate-Link geklickt haben. Dieses Fenster wird pro Programm unter **Marketing > Affiliate-Programme** festgelegt, wenn Sie ein Programm erstellen oder bearbeiten.

Branchenübliche Cookie-Laufzeiten:
- **7 Tage**: Schnellentscheidungsprodukte (Lebensmittel, Veranstaltungstickets)
- **30 Tage**: Standard-E-Commerce (die häufigste Einstellung)
- **60–90 Tage**: Überlegte Käufe (Möbel, Elektronik, B2B-Produkte)
- **365 Tage**: Längere Verkaufszyklen (Luxusgüter, hochwertige Dienstleistungen)

Wenn ein Kunde am 1. Januar auf einen Affiliate-Link klickt und Ihre Cookie-Laufzeit 30 Tage beträgt, schreibt jeder Kauf, den er bis zum 30. Januar tätigt, diesen Affiliate. Käufe am 31. Januar oder später erzeugen keine Kommission, da der Cookie abgelaufen ist.

### Letzter Klick-Zuordnungsmodell

Spwig verwendet **letzter Klick-Zuordnung**: der neueste Affiliate-Link gewinnt. So funktioniert das:

**Szenario**: Ein Kunde klickt am Montag auf den Link von Affiliate A, dann am Mittwoch auf den Link von Affiliate B und kauft am Freitag.

**Ergebnis**: Affiliate B erhält die Kommission, da sein Link der neueste Klick war.

Der letzte Klick-Cookie überschreibt vorherige Affiliate-Cookies. Dieses Modell ist einfach zu verstehen und verhindert Doppelkommissionen, obwohl es bedeutet, dass nur ein Affiliate pro Bestellung Gutschrift erhält (der letzte vor dem Kauf).

## Klickaufzeichnung

Spwig protokolliert jeden Klick auf jeden Affiliate-Link, um Analysen sowohl für Sie als auch für den Affiliate bereitzustellen. Klickdaten helfen, die Leistung von Links zu messen, Betrug zu erkennen und Werbestrategien zu optimieren.

### Daten pro Klick

Navigieren Sie zu **Affiliate > Klicks**, um alle aufgezeichneten Klicks anzuzeigen. Jeder Eintrag enthält:

| Feld | Beschreibung |
|-------|-------------|
| **Link** | Welcher Tracking-Link geklickt wurde |
| **Affiliate** | Wer den Link erstellt hat |
| **IP-Adresse** | Kunden-IP (für Betrugsdetektion) |
| **User-Agent** | Browser- und Geräteinformationen |
| **Referer** | Die Seite, auf der der Kunde den Link geklickt hat (z. B. "https://instagram.com") |
| **Sitzungsid** | Eindeutiger Identifier für diese Browsesitzung |
| **Zeitstempel** | Genauer Datum und Uhrzeit des Klicks |

### Rate Limiting

Um Klickbetrug und Bot-Abuse zu verhindern, limitiert Spwig Klicks auf **100 pro Minute pro IP-Adresse**. Wenn die gleiche IP diesen Schwellenwert überschreitet, werden zusätzliche Klicks ignoriert und erhöhen die Klickzahlen nicht.

Diese Schutzmaßnahme verhindert, dass böswillige Akteure die Klickstatistiken manipulieren, ohne legitime Traffic zu blockieren. Echte Kunden überschreiten fast nie die 100 Klicks pro Minute.

### Datenschutzaspekte

Klickdaten enthalten IP-Adressen und User-Agents zur Betrugsdetektion. Stellen Sie sicher, dass Ihre Datenschutzrichtlinie erwähnt, dass Sie Affiliate-Verweisungen verfolgen und anonymisierte Leistungsdaten mit Affiliates teilen.

## Affiliate-Links ansehen

Alle von Affiliates erstellten Tracking-Links erscheinen in Ihrem Admin-Panel für Überwachung und Verwaltung.

### Links-Liste aufrufen

Navigieren Sie zu **Affiliate > Links**, um alle Tracking-Links über alle Affiliates und Programme anzuzeigen. Die Listenansicht zeigt an:

- **Link-Code**: Der eindeutige 12-stellige Identifier
- **Affiliate**: Wer den Link erstellt hat
- **Programm**: Welche Kommissionsstruktur gilt
- **Bezeichnung**: Optionaler von Affiliate bereitgestellter Beschreibungstext
- **Ziel**: Wo der Link Kunden weiterleitet
- **Gesamtzahl der Klicks**: Alle Zeiten Klickzahlen
- **Aktiver Status**: Ob der Link aktuell Tracking durchführt

### Links filtern

Verwenden Sie die Admin-Filter, um die Liste zu verfeinern:
- **Nach Affiliate**: Alle Links für einen bestimmten Partner ansehen
- **Nach Programm**: Links, die eine bestimmte Kommissionsstruktur bewerben
- **Nach Aktivstatus**: Deaktivierte Links finden

Diese Filterung hilft Ihnen, die Verteilung der Links über Ihr Affiliate-Netzwerk zu analysieren und die besten Links zu identifizieren.

## Link-Statistik

Jeder Tracking-Link sammelt Leistungsmetriken, die Affiliates dabei helfen, ihre Werbestrategien zu optimieren und Ihnen helfen, Ihre besten Partner zu identifizieren.

### Klicken Sie auf einen Link-Record, um detaillierte Statistiken anzuzeigen:

| Metrik | Beschreibung | Berechnung |
|--------|-------------|-------------|
| **Gesamtzahl der Klicks** | Alle aufgezeichneten Klicks seit Linkerstellung | Anzahl der Klickaufzeichnungen |
| **Klicks (7 Tage)** | Indikator für aktuelle Aktivität | Klicks in den letzten 7 Tagen |
| **Konversionen** | Bestellungen, die diesem Link zugeordnet sind | Anzahl der Kommissionen von diesem Link-Code |
| **Konversionsrate** | Prozentsatz der Klicks, die zu Käufen führten | (Konversionen ÷ Gesamtzahl der Klicks) × 100 |
| **Gesamter Umsatz** | Summe aller Bestellwerte von diesem Link | Summe der Bestellsummen für konvertierte Klicks |

### Statistik zur Optimierung verwenden

**Für Affiliates**: Diese Zahlen zeigen, welche Werbekanäle am besten funktionieren. Wenn ein Instagram-Bio-Link eine Konversionsrate von 5 % hat, aber ein Blog-Beitrag-Link 15 %, sollte der Affiliate sich mehr auf Blog-Inhalte konzentrieren.

**Für Händler**: Link-Statistiken zeigen, welche Affiliates qualitativ hochwertigen Traffic generieren. Hohe Klickzahlen mit niedrigen Konversionsraten deuten darauf hin, dass das Publikum des Affiliates nicht gut zu Ihren Produkten passt.

## Link-Verwaltung

Sie können Affiliate-Links über das Admin-Panel verwalten, um Wartung und Problemlösung durchzuführen.

### Links deaktivieren

Um einen bestimmten Link daran zu hindern, neue Klicks zu verfolgen, während historische Daten beibehalten werden:

1. Navigieren Sie zu **Affiliate > Links**
2. Klicken Sie auf den Link, den Sie deaktivieren möchten
3. Deaktivieren Sie das **Aktiv**-Kästchen
4. Klicken Sie auf **Speichern**

Deaktivierte Links leiten Kunden immer noch zum Ziel weiter, setzen aber keine Tracking-Cookies oder protokollieren Klicks. Dies ist nützlich, wenn ein Affiliate eine temporäre Kampagne läuft oder Sie einen bestimmten Werbekanal deaktivieren müssen.

### Link-Details bearbeiten

Sie können folgende Elemente ändern:
- **Bezeichnung**: Aktualisieren Sie die vom Affiliate bereitgestellte Beschreibung
- **Ziel**: Ändern Sie, wohin der Link weiterleitet (nützlich, wenn Sie eine Produktseite verschieben)
- **Aktivstatus**: Aktivieren oder Deaktivieren Sie das Tracking

Sie können den Link-Code nicht bearbeiten — er ist dauerhaft und mit allen historischen Klick- und Kommissionsdaten verknüpft.

### Inaktive Links löschen

Löschen Sie Links, die nicht mehr in Gebrauch sind und keine historischen Klicks oder Konversionen haben. Dies hält Ihre Linkliste sauber, ohne wertvolle Analyse-Daten zu verlieren.

**Warnung**: Das Löschen eines Links entfernt alle damit verbundenen Klickaufzeichnungen. Löschen Sie nur Links mit null Klicks oder wenn Sie sich absolut sicher sind, dass Sie keine historischen Daten benötigen.

## Zuordnungsmodell

Das Verständnis der Zuordnungslogik von Spwig hilft Ihnen, Erwartungen mit Affiliates zu setzen und Streitigkeiten über Kommissionen zu beheben.

### Letzter Klick-Zuordnung

Wie bereits erwähnt, verwendet Spwig letzter Klick-Zuordnung: wenn ein Kunde mehrere Affiliate-Links vor dem Kauf klickt, erhält nur der letzte Affiliate eine Kommission.

**Vorteile**:
- Einfach zu verstehen und zu erklären
- Verhindert Doppelkommissionen
- Belohnt Affiliates, die den Verkauf abschließen

**Nachteile**:
- Frühere Affiliates, die den Kunden eingeführt haben, erhalten keine Gutschrift
- Spiegelt nicht die mehrfach berührten Kundenreisen wider
- Kann Anreize für "Link Hijacking" schaffen (Affiliates, die auf Kunden mit hohem Kaufinteresse zielen, die bereits von jemand anderem verweist wurden)

### Cookie-Laufzeit bestimmt die Berechtigung

Nur Käufe innerhalb des Cookie-Laufzeitfensters erzeugen Kommissionen. Wenn der Cookie vor dem Checkout abgelaufen ist, wird keine Kommission erstellt, auch wenn der Kunde später über ein Lesezeichen zurückkehrt.

**Beispiel**: 30-Tage-Cookie-Laufzeit
- Kunde klickt am 1. Januar auf den Link → Cookie wird gesetzt, läuft am 31. Januar ab
- Kunde kauft am 25. Januar → Kommission wird erstellt
- Kunde kauft am 5. Februar → Keine Kommission (Cookie abgelaufen)

### Sitzungsverfolgung

Zusätzlich zum Cookie verfolgt Spwig die Sitzungsid für jeden Klick. Dies ermöglicht die Zuordnung mehrerer Besuche innerhalb der gleichen Sitzung, auch wenn Cookies blockiert oder gelöscht werden.

Wenn ein Kunde einen Link klickt, navigiert er durch Ihr Geschäft, was mehrere Seitenaufrufe auslöst, und kauft dann — alles in der gleichen Sitzung — erhält der Affiliate die Gutschrift, auch ohne einen persistenten Cookie.

## Problembehandlung

Häufige Tracking-Probleme und deren Lösungen:

### Link verfolgt keine Klicks

**Symptome**: Klickzähler bleibt bei null, obwohl der Affiliate berichtet hat, den Link geteilt zu haben.

**Ursachen und Lösungen**:
1. **Link ist deaktiviert**: Prüfen Sie den **Aktiv**-Status auf der Link-Detailseite
2. **Programm ist inaktiv**: Navigieren Sie zu **Affiliate > Programme** und prüfen Sie, ob der Programstatus **Aktiv** ist
3. **Affiliate-Konto ist deaktiviert**: Prüfen Sie den Affiliate-Kontostatus unter **Affiliate > Affiliates**
4. **Rate Limiting**: Prüfen Sie, ob die gleiche IP zu viele Klicks erzeugt (Bot-Traffic)

### Niedrige Konversionsrate

**Symptome**: Hohe Klickzahlen, aber nur wenige Bestellungen werden zugeordnet.

**Ursachen und Lösungen**:
1. **Cookie-Laufzeit zu kurz**: Erhöhen Sie die Cookie-Laufzeit des Programms, wenn Ihre Produkte Forschung und Überlegung erfordern
2. **Qualität der Zielseite**: Prüfen Sie die Landingpage — ist sie mobilfreundlich? Lädt sie schnell? Ist das Produkt auf Lager?
3. **Unpassende Zielgruppe**: Die Zielgruppe des Affiliates passt möglicherweise nicht zu Ihren Produkten
4. **Browser blockiert Cookies**: Einige Datenschutz-Tools blockieren Drittanbieter-Cookies, obwohl Spwig Erstanbieter-Cookies verwendet, die weniger wahrscheinlich blockiert werden

### Duplizierte Klickaufzeichnungen

**Symptome**: Der gleiche Kunde erzeugt mehrere Klickaufzeichnungen in schneller Folge.

**Ursache**: Dieses Verhalten ist normal. Jeder Seitenaufruf des Tracking-Links erzeugt eine Klickaufzeichnung. Wenn ein Kunde auf einen Link klickt, die Seite langsam lädt und er erneut klickt, sehen Sie mehrere Einträge.

**Lösung**: Keine Aktion erforderlich. Der Rate-Limiter verhindert Missbrauch (100 Klicks/Minute/IP), und duplizierte Klicks aus der gleichen Sitzung beeinflussen die Zuordnung nicht — nur ein Cookie wird gesetzt.

## Tipps

- **Testen Sie das Tracking vor der Veröffentlichung** — Erstellen Sie ein Test-Affiliate-Konto, generieren Sie einen Tracking-Link, klicken Sie ihn in einem Incognito-Browser an und vervollständigen Sie einen Testkauf. Stellen Sie sicher, dass die Kommission mit der richtigen Affiliate-Zuordnung erscheint.
- **Eduzieren Sie Affiliates über die Cookie-Laufzeit** — Stellen Sie sicher, dass Affiliates verstehen, dass sie nur für Käufe innerhalb des Cookie-Fensters Kommissionen erhalten. Dies hilft ihnen, realistische Erwartungen zu setzen und sich auf Traffic mit hohem Kaufinteresse zu konzentrieren.
- **Überwachen Sie Klickmuster auf Betrug** — Unusually hohe Klickzahlen von einer einzigen IP oder Klicks ohne User-Agent-String können auf Bot-Traffic hindeuten. Prüfen Sie diese Affiliates sorgfältig, bevor Sie Kommissionen genehmigen.
- **Verwenden Sie konsistent Link-Bezeichnungen** — Fordern Sie Affiliates an, ihre Links nach Kanälen (Instagram, Blog, E-Mail) zu kennzeichnen, damit Sie beide analysieren können, welche Werbekanäle die besten Konversionen erzielen.
- **Überlegen Sie sich längere Cookie-Laufzeiten für hochwertige Produkte** — Wenn Ihr durchschnittlicher Bestellwert hoch ist und Kunden normalerweise vor dem Kauf recherchieren, verlängern Sie die Cookie-Laufzeit auf 60–90 Tage, um diese verzögerten Konversionen zu erfassen.
- **Prüfen Sie Referer-Daten für Kanal-Einsichten** — Das Referer-Feld zeigt an, woher die Klicks kommen. Wenn Sie viele Klicks von "instagram.com" oder "youtube.com" sehen, wissen Sie, welche sozialen Plattformen Ihre Affiliates am effektivsten nutzen.