---
title: Affiliate-Programm
---

Das Affiliate-Programm ermöglicht es Ihnen, Partner zu gewinnen, die Ihre Produkte bewerben und an den Umsätzen, die sie erzeugen, Provisionen verdienen. Affiliate-Mitglieder teilen eindeutige Verweis-Links, und Spwig verfolgt automatisch Klicks, weist Bestellungen zu und berechnet Provisionen.

![Affiliate programs](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Wie es funktioniert

1. Sie erstellen ein oder mehrere **Affiliate-Programme** mit Provisionssätzen und Regeln
2. Affiliate-Mitglieder **melden sich** über einen öffentlichen Portal oder werden manuell hinzugefügt
3. Jeder Affiliate erhält einen **eindeutigen Verweis-Link** mit einem Tracking-Code
4. Wenn ein Kunde auf den Link klickt und eine Bestellung tätigt, wird eine **Provision** erfasst
5. Sie prüfen und genehmigen Provisionen und verarbeiten anschließend **Auszahlungen**

## Ein Programm erstellen

Navigieren Sie zu **Marketing > Affiliate-Programme** und klicken Sie auf **Programm hinzufügen**.

### Programm-Einstellungen

| Einstellung | Beschreibung |
|---------|-------------|
| **Name** | Der Programmname, der für Affiliate-Mitglieder sichtbar ist (z. B. "Partnerprogramm") |
| **Provisionsart** | **Prozentualer** Anteil des Bestellbetrags oder **Fester** Betrag pro Verkauf |
| **Provisionsrate** | Der Prozentsatz oder feste Betrag, den Affiliate-Mitglieder verdienen |
| **Cookie-Laufzeit** | Wie viele Tage der Verweis-Tracking-Cookie besteht (Standard: 30 Tage) |
| **Mindestauszahlung** | Mindestverdienst, bevor ein Affiliate-Mitglied eine Auszahlung anfordern kann |
| **Automatisch genehmigen** | Neue Affiliate-Anträge automatisch akzeptieren oder manuelle Genehmigung erfordern |
| **Status** | Aktiv, pausiert oder geschlossen |

### Provisionsarten

- **Prozentual** — Affiliate-Mitglieder erhalten einen bestimmten Prozentsatz des Gesamtbetrags der vermittelten Bestellung (z. B. 10 % von einer 100 $-Bestellung = 10 $ Provision)
- **Fest** — Affiliate-Mitglieder erhalten einen festen Betrag pro Verkauf, unabhängig vom Bestellwert (z. B. 5 $ pro Verkauf)

## Affiliate-Mitglieder verwalten

Navigieren Sie zu **Marketing > Affiliate-Mitglieder**, um Affiliate-Konten anzuzeigen und zu verwalten.

### Affiliate-Mitglieder-Details

Jedes Affiliate-Mitglied hat:
- **Affiliate-Code** — Ein eindeutiger Code, der in Verweis-URLs verwendet wird (automatisch generiert oder benutzerdefiniert)
- **Verweis-Link** — Der vollständige Tracking-URL, den das Affiliate-Mitglied teilt (z. B., `yourstore.com/?ref=CODE`)
- **Status** — Ausstehend, genehmigt oder abgelehnt
- **Zahlungsmethode** — Wie das Affiliate-Mitglied Auszahlungen erhält (PayPal oder Banküberweisung)
- **Programm-Mitgliedschaft** — Zu welchen Programmen das Affiliate-Mitglied gehört

### Affiliate-Mitglieder manuell hinzufügen

1. Klicken Sie auf **Affiliate-Mitglied hinzufügen**
2. Wählen Sie ein vorhandenes Kundenkonto aus oder erstellen Sie ein neues
3. Weisen Sie das Affiliate-Mitglied einem oder mehreren Programmen zu
4. Legen Sie den Affiliate-Code fest (oder lassen Sie ihn leer, um ihn automatisch zu generieren)

### Affiliate-Portal

Affiliate-Mitglieder erhalten Zugang zu einem öffentlich zugänglichen Portal, in dem sie:
- Ihren Dashboard mit Einnahmen und Klick-Statistiken ansehen können
- Ihre Verweis-Links kopieren
- Ihre Provisionshistorie verfolgen
- Auszahlungen anfordern

Die Portal-URL ist automatisch unter `/affiliate/` auf Ihrem Store verfügbar.

## Tracking und Provisionen

### Wie das Tracking funktioniert

1. Ein Kunde klickt auf einen Affiliate-Verweis-Link
2. Ein Tracking-Cookie wird im Kundenbrowser gesetzt (wird für die konfigurierte Cookie-Laufzeit gespeichert)
3. Wenn der Kunde innerhalb der Cookie-Laufzeit eine Bestellung tätigt, wird diese Bestellung dem Affiliate-Mitglied zugeordnet
4. Eine Provision wird mit dem Status **Ausstehend** erstellt

### Provision-Statusse

| Status | Beschreibung |
|--------|-------------|
| **Ausstehend** | Provision erfasst, wartet auf Prüfung |
| **Genehmigt** | Bestätigt und bereit zur Auszahlung |
| **Abgelehnt** | Provision abgelehnt (z. B. betrügerische Bestellung oder Retourware) |
| **Ausgezahlt** | Provision in einer abgeschlossenen Auszahlung enthalten |

### Provisionen prüfen

Navigieren Sie zu **Marketing > Provisionen**, um ausstehende Provisionen zu prüfen:

1. Prüfen Sie die Bestelldetails, um sicherzustellen, dass der Verkauf legitim ist
2. Klicken Sie auf **Genehmigen**, um die Provision zu bestätigen, oder auf **Ablehnen** mit einem Grund
3. Genehmigte Provisionen sammeln sich zur Auszahlungsbilanz des Affiliate-Mitglieds

## Auszahlungen

Wenn die genehmigte Provisionenbilanz eines Affiliate-Mitglieds den Mindestauszahlungsschwellenwert erreicht, können Sie eine Auszahlung verarbeiten.

### Auszahlungen verarbeiten

1. Navigieren Sie zu **Marketing > Auszahlungen**
2. Wählen Sie Affiliate-Mitglieder mit verfügbaren Bilanzen aus
3. Wählen Sie die Zahlungsmethode:
   - **PayPal** — Gelder direkt an die PayPal-Email-Adresse des Affiliate-Mitglieds senden
   - **Banküberweisung** — Manuelle Banküberweisung aufzeichnen
4. Bestätigen und verarbeiten Sie die Auszahlung
5. Der Auszahlungsstatus wird auf **Abgeschlossen** aktualisiert und die Provisionen werden als **Ausgezahlt** markiert

### Auszahlungsanbieter

Spwig integriert sich mit Zahlungsanbietern für automatisierte Auszahlungen:
- **PayPal** — Automatisierte Massen-Auszahlungen über die PayPal-API
- **Airwallex** — Internationale Auszahlungen mit wettbewerbsfähigen Wechselkursen
- **Manuell** — Auszahlungen, die außerhalb von Spwig verarbeitet werden, aufzeichnen

## Verweis-Links

Jeder Verweis-Link eines Affiliate-Mitglieds folgt diesem Muster:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Affiliate-Mitglieder können auch Links zu bestimmten Produkten oder Kategorien erstellen:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

Der `ref`-Parameter funktioniert auf jeder Seite — der Tracking-Cookie wird gesetzt, unabhängig davon, auf welcher Startseite der Kunde landet.

## Programm-Statistiken

Das Affiliate-Programm-Dashboard zeigt an:
- **Gesamt-Klicks** — Wie oft Verweis-Links geklickt wurden
- **Gesamt-Orders** — Bestellungen, die Affiliate-Mitgliedern zugeordnet wurden
- **Gesamt-Provisionen** — Summe aller Provisionen (ausstehend, genehmigt und ausgezahlt)
- **Aktive Affiliate-Mitglieder** — Anzahl der genehmigten Affiliate-Mitglieder, die derzeit Verweis-Links erstellen

## Tipps

- Beginnen Sie mit einer **prozentualen Provision** (5–15 %) — sie passt sich natürlicherweise an den Bestellwert an und ist für Affiliate-Mitglieder leicht verständlich.
- Setzen Sie eine **Cookie-Laufzeit von 30 Tagen** als Standard — dies gibt Kunden die Möglichkeit, zurückzukommen und ihren Kauf abzuschließen, während die Verkaufsattribute noch dem Affiliate-Mitglied zugeordnet werden.
- Aktivieren Sie **automatische Genehmigung** für öffentliche Programme, um Reibungsverluste zu reduzieren, oder verwenden Sie manuelle Genehmigung für Einladungs-basierte Programme, bei denen Sie jeden Affiliate-Mitglied prüfen möchten.
- Setzen Sie eine vernünftige **Mindestauszahlung** (z. B. 25–50 $) um viele kleine Transaktionen zu vermeiden.
- Personalisieren Sie das **Affiliate-Portal**, um es mit Ihrer Marke abzugleichen — Affiliate-Mitglieder sind eher geneigt, Ihr Geschäft zu bewerben, wenn die Erfahrung professionell wirkt.
- Überwachen Sie regelmäßig Provisionen auf **betrügerische Muster** wie Selbstverweisungen, ungewöhnlich hohe Retourraten oder verdächtige Klickmengen.