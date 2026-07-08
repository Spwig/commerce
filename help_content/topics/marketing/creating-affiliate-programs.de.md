---
title: Affiliate-Programme erstellen
---

Affiliate-Programme definieren, wie Ihre Partner Provisionen verdienen, wenn sie Kunden auf Ihre Store verweisen. Jedes Programm hat seine eigene Provisionenstruktur, Tracking-Regeln und Auszahlungsgrenzen. Sie können mehrere Programme erstellen, um verschiedene Affiliate-Gruppen zu bedienen – wie Influencer, Content-Ersteller oder Bulk-Verweispartner.

![Programmliste](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Komponenten eines Programms

Jedes Affiliate-Programm besteht aus:

- **Name und Beschreibung** — Identifizieren Sie das Programm und erklären Sie es den Affiliates
- **Provisionenstruktur** — Wie viel Affiliates pro Verkauf verdienen (Prozent oder festen Betrag)
- **Cookie-Laufzeit** — Wie lange das Verweis-Tracking nach einem Klick gilt (1–365 Tage)
- **Automatische Genehmigung** — Ob neue Affiliates automatisch beitreten oder eine manuelle Prüfung erfordern
- **Mindestauszahlungsgrenze** — Wie viel Affiliates verdienen müssen, bevor sie eine Auszahlung anfordern
- **Status** — Aktiv, pausiert oder archiviert

## Provisionstypen

Wählen Sie bei der Erstellung Ihres Programms zwischen zwei Provisionstypen:

| Typ | Funktionsweise | Wann verwenden | Beispielberechnung |
|------|-------------|-------------|---------------------|
| **Prozent** | Der Affiliate erhält einen Prozentsatz des Bestellbetrags | Skalierbare Belohnungen, die mit dem Bestellwert wachsen | 10 % von $150 Bestellung = $15 Provision |
| **Fester Betrag** | Der Affiliate erhält einen festen Betrag pro Verkauf | Vorhersehbare Kosten; am besten für hochvolumige, geringe Gewinnmargen Produkte | $25 pro Verkauf, unabhängig vom Bestellwert |

**Prozentbasierte Provisionen** skalieren natürlich – Affiliates verdienen mehr, wenn sie hochwertige Kunden verweisen. Dies stellt ihre Anreize mit Ihren eigenen in Einklang und ist der häufigste Modell (typischerweise 5–15 %).

**Feste Provisionen** eignen sich gut für Dienstleistungen, Abonnements oder Bulk-Verweisprogramme, bei denen Sie vorhersehbare Kosten pro Verkauf haben. Sie sind einfach zu verstehen und zu planen, können aber Affiliates untercompensieren, die große Bestellungen vermitteln.

## Ein Programm erstellen

Navigieren Sie zu **Marketing > Affiliate-Programme** und klicken Sie auf **+ Programm hinzufügen**.

### Schritt-für-Schritt-Einrichtung

1. **Programmname**
   Geben Sie einen beschreibenden Namen ein, der für Affiliates sichtbar ist (z. B. "Partnerprogramm" oder "Influencer-Tier").

2. **Slug**
   Ein URL-freundlicher Bezeichner, der automatisch aus dem Namen generiert wird. Wird in URLs und internen Referenzen verwendet. Sie können ihn bei Bedarf anpassen.

3. **Beschreibung**
   Optionaler Text, der die Vorteile und Bedingungen des Programms erklärt. Affiliates sehen dies, wenn sie Programme prüfen, zu denen sie beitreten können.

4. **Provisionstyp**
   Wählen Sie **Prozent** oder **Fester Betrag**.

5. **Provisionswert**
   - Für Prozent: Geben Sie einen Wert zwischen 0 und 100 ein (z. B. `10` für 10 %)
   - Für festen Betrag: Geben Sie den Dollarbetrag pro Verkauf ein (z. B. `25.00` für $25)

6. **Cookie-Laufzeit in Tagen**
   Wie viele Tage das Tracking-Cookie gilt (1–365). Siehe den Abschnitt unten für Anleitungen.

7. **Affiliates automatisch genehmigen**
   - **Markiert** — Neue Affiliates beitreten automatisch
   - **Nicht markiert** — Sie prüfen und genehmigen jede Anwendung manuell

8. **Mindestauszahlung**
   Der Mindestbestand, den ein Affiliate vor der Anforderung einer Auszahlung sammeln muss (z. B. `50.00` für $50).

9. **Status**
   Auf **Aktiv** setzen, um neue Affiliates zu akzeptieren und Verweisungen zu verfolgen.

10. **Speichern** Sie das Programm.

## Cookie-Laufzeit erläutert

Die Cookie-Laufzeit bestimmt, wie lange Spwig sich daran erinnert, dass ein Kunde auf einen Affiliate-Verweislink geklickt hat.

### Wie es funktioniert

1. Ein Kunde klickt auf einen Affiliate-Link
2. Spwig setzt ein Tracking-Cookie im Browser des Kunden
3. Wenn der Kunde einen Kauf **innerhalb der Cookie-Laufzeit** abschließt, wird der Auftrag dem Affiliate zugeordnet
4. Wenn das Cookie abläuft, bevor der Kauf abgeschlossen wird, erhält der Affiliate keine Provision

### Dauer auswählen

| Dauer | Anwendungsfall | Typisches Szenario |
|----------|----------|------------------|
| **1–7 Tage** | Impulskäufe, Flash-Verkäufe | Schnellverkaufende Konsumgüter, zeitlich begrenzte Angebote |
| **30 Tage** | Standard E-Commerce | Allgemeiner Online-Retail, Standardempfehlung |
| **60–90 Tage** | Überlegte Käufe | Höherwertige Artikel, B2B, Dienstleistungen |
| **180+ Tage** | Längere Verkaufszyklen | Unternehmenssoftware, Abonnements, Luxusgüter |

**Branchenstandard ist 30 Tage.** Dies bietet eine faire Zuordnung für Affiliates, aber praktische Tracking-Grenzen. Kürzere Laufzeiten begünstigen Kunden, die sich schnell umwandeln; längere Laufzeiten geben Kunden Zeit, zu recherchieren und zurückzukommen, um ihren Kauf abzuschließen.

### Technische Hinweis

Die Cookie-Laufzeit beeinflusst nur die **Zuordnung**. Genehmigte Provisionen bleiben für immer gültig – die Cookie-Laufzeit bestimmt nur, ob ein Auftrag dem Affiliate ursprünglich gutgeschrieben wird.

## Einstellungen für automatische Genehmigung

Die Einstellung für automatische Genehmigung steuert, ob neue Affiliate-Anträge eine manuelle Prüfung erfordern.

### Wann automatische Genehmigung aktivieren

- **Öffentliche Programme** — Sie möchten Ihre Affiliate-Basis schnell ausbauen, ohne Engpässe
- **Niedrig-Risiko-Produkte** — Betrug oder Markenrisiko ist minimal
- **Hochvolumen-Programme** — Sie erwarten viele Anträge und können nicht jeden manuell prüfen

### Wann manuelle Prüfung erforderlich ist

- **Einladungs-basierte Programme** — Sie akzeptieren nur vorab geprüfte Partner
- **Premium-Programme** — Hohe Provisionen oder exklusive Vorteile
- **Marken-sensitive Produkte** — Sie müssen sicherstellen, dass Affiliates mit Ihren Markenwerten übereinstimmen
- **Betrugsprävention** — Sie möchten Konten mit verdächtigen Aktivitäten prüfen

### Sicherheitsaspekte

Manuelle Prüfung von Affiliates hilft, folgende Dinge zu verhindern:
- Selbstverweis-Systeme (Affiliates erstellen Fake-Konten, um Provisionen zu verdienen)
- Markenverletzungen (Affiliates bieten Ihre Markenbegriffe in bezahlter Suchwerbung an)
- Markenunpassendheit (Affiliates bewerben Ihre Produkte in unpassenden Kontexten)

Für die meisten Geschäfte ist es sicherer, mit **manueller Genehmigung** zu beginnen. Sie können immer automatische Genehmigung später aktivieren, sobald Sie Muster für Vertrauenswürdigkeit etabliert haben.

## Mindestauszahlungsgrenze

Die Mindestauszahlungsgrenze verhindert, dass administrative Aufwendungen durch die Verarbeitung vieler kleiner Auszahlungen entstehen.

### Warum eine Mindestgrenze setzen

- **Verringert Transaktionsgebühren** — Zahlungsdienstleister verlangen pro Transaktion Gebühren, daher spart das Zusammenfassen von Auszahlungen Geld
- **Vereinfacht die Buchhaltung** — Weniger Auszahlungsvorgänge bedeuten weniger Rekonvaleszenz-Arbeit
- **Branchenstandard** — Die meisten Affiliate-Programme haben Mindestgrenzen ($25–$100)

### Typische Grenzen

| Grenze | Anwendungsfall |
|-----------|----------|
| **$25–$50** | Hochvolumen-Programme, bei denen Affiliates schnell die Mindestgrenze erreichen |
| **$50–$100** | Standardgrenze für die meisten Programme |
| **$100–$200** | Premium-Programme oder internationale Auszahlungen mit hohen Verarbeitungsgebühren |

### Ausgewogene Affiliate-Zufriedenheit

Eine zu hohe Grenze frustriert Affiliates, die möglicherweise Monate warten müssen, um ihre erste Auszahlung zu erhalten. Eine zu niedrige Grenze führt zu administrativen Belastungen und vermindert Ihre Gewinnmargen durch Gebühren.

**Empfehlung:** Beginnen Sie mit $50. Dies ist niedrig genug, damit aktive Affiliates es innerhalb ihrer ersten paar Verkäufe erreichen, aber hoch genug, um Auszahlungen effizient zu bündeln.

### Keine Obergrenze

Es gibt keine Obergrenze – Affiliates können ihre Einnahmen unbegrenzt anhäufen, bevor sie eine Auszahlung anfordern. Einige Affiliates bevorzugen es, ihre Anfragen quartalsweise oder jährlich zu bündeln, um Steuerplanung zu ermöglichen.

## Verwaltung des Programmsstatus

Programme können in einem von drei Status sein:

| Status | Beschreibung | Verhalten |
|--------|-------------|----------|
| **Aktiv** | Das Programm läuft | Akzeptiert neue Affiliates, verfolgt Verweisungen, berechnet Provisionen |
| **Pausiert** | Temporär deaktiviert | Bestehende Affiliates bleiben, aber keine neuen Anmeldungen; bestehende Verweis-Cookies funktionieren weiter |
| **Archiviert** | Permanent geschlossen | Keine neuen Affiliates, keine neuen Verweisungen verfolgt; historische Daten werden für Berichte beibehalten |

### Wann ein Programm pausieren

- Sie bearbeiten die Provisionen oder die Bedingungen
- Sie sind in diesem Quartal über dem Budget für Affiliate-Auszahlungen
- Sie testen eine neue Programmgrundstruktur und möchten verhindern, dass neue Affiliates das alte Programm beitreten

Pausierte Programme honorieren weiterhin bestehende Tracking-Cookies und ausstehende Provisionen – Sie verhindern nur, dass neue Affiliates beitreten.

### Wann ein Programm archivieren

- Sie haben das Programm durch ein neues Struktur ersetzt
- Das Programm war zeitlich begrenzt (z. B. eine Saisonkampagne)
- Sie konsolidieren mehrere Programme in eines

Archivierte Programme bleiben in der Datenbank für historische Berichte, werden aber aus aktiven Verwaltungsansichten entfernt.

## Beispielprogramme

### Beispiel 1: Influencer-Programm (Prozent)

| Feld | Wert |
|-------|-------|
| Name | Influencer-Programm |
| Provisionstyp | Prozent |
| Provisionswert | 10 |
| Cookie-Laufzeit in Tagen | 30 |
| Automatische Genehmigung | Nicht markiert (manuelle Prüfung) |
| Mindestauszahlung | 50.00 |
| Status | Aktiv |

**Anwendungsfall:** Rekrutieren Sie Influencer und Content-Ersteller. Die 10 % Provision skaliert mit dem Bestellwert und belohnt Affiliates, die hochverbrauchende Kunden anziehen. Manuelle Genehmigung stellt sicher, dass Sie die Zielgruppe und Markenpassung jedes Influencers prüfen.

### Beispiel 2: Bulk-Verweisprogramm (Fester Betrag)

| Feld | Wert |
|-------|-------|
| Name | Verweis-Partnerprogramm |
| Provisionstyp | Fester Betrag |
| Provisionswert | 25.00 |
| Cookie-Laufzeit in Tagen | 7 |
| Automatische Genehmigung | Markiert |
| Mindestauszahlung | 100.00 |
| Status | Aktiv |

**Anwendungsfall:** Partner mit Deal-Sites, Coupon-Aggregatoren und Verweis-Netzwerken, die hohe Volumina vermitteln. Die $25 feste Provision hält die Kosten vorhersehbar, und die kurze Cookie-Laufzeit (7 Tage) zielt auf schnelle Umwandlungen ab. Automatische Genehmigung ist aktiviert, da diese Partner typischerweise selbstbedienungsbasiert sind.

### Beispiel 3: Premium-Partner (Hohe Prozent)

| Feld | Wert |
|-------|-------|
| Name | Premium-Partner-Tier |
| Provisionstyp | Prozent |
| Provisionswert | 15 |
| Cookie-Laufzeit in Tagen | 90 |
| Automatische Genehmigung | Nicht markiert |
| Mindestauszahlung | 200.00 |
| Status | Aktiv |

**Anwendungsfall:** Exklusives Programm für Top-Affiliates oder strategische Partner. Höhere Provision (15 %) belohnt ihre qualitativ hochwertige Traffic, und die 90-Tage Cookie-Laufzeit berücksichtigt längere Überlegungszyklen. Nur manuelle Genehmigung – dies ist ein Einladungs-basiertes Tier.

## Tipps

- Beginnen Sie mit einer **Prozentbasierten Provision** (5–15 %), für die meisten Programme – es ist einfacher, Affiliates zu erklären und skaliert natürlich mit dem Bestellwert.
- Verwenden Sie eine **30-Tage Cookie-Laufzeit** als Baseline – es ist der Branchenstandard und balanciert faire Zuordnung mit praktischen Tracking-Grenzen.
- Aktivieren Sie zunächst **manuelle Genehmigung**, um Affiliates zu prüfen, und wechseln Sie dann zu automatischer Genehmigung, sobald Sie Muster für Vertrauenswürdigkeit und Betrugskontrollen etabliert haben.
- Setzen Sie Ihre **Mindestauszahlung** auf $50–$100, um Affiliate-Zufriedenheit (nicht zu hoch, um erreicht zu werden) mit administrativer Effizienz (nicht zu viele kleine Auszahlungen) zu balancieren.
- Erstellen Sie **separate Programme** für verschiedene Affiliate-Gruppen (Influencer, Content-Sites, Deal-Aggregatoren), damit Sie Leistungen verfolgen und Provisionen unabhängig anpassen können.
- Überwachen Sie regelmäßig das **Analytics-Dashboard**, um hochleistungsfähige Affiliates zu erkennen und die Provisionen anzupassen, um Top-Partner zu behalten.

