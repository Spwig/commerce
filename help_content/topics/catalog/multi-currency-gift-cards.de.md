---
title: Gutscheikarten mit mehreren Währungen
---

Wenn Sie Kunden in mehreren Ländern bedienen, können Sie Gutscheikarten in spezifischen Währungen ausgeben. Ein Beispiel: Ein Kunden aus Neuseeland kann eine 50 NZD-Gutscheikarte kaufen und der Empfänger kann sie in NZD einlösen — der Nennwert bleibt gleich, unabhängig von Wechselkurs-Schwankungen.

Diese Funktion erfordert, dass mehrere Währungen aktiviert sind und mindestens ein Wechselkurs-Anbieter konfiguriert ist.

## Wie es funktioniert

Wenn Sie eine **Gutscheikarten-Währung** für ein Gutscheikarten-Produkt festlegen, konvertiert das System den Produkt-Preis in die Zielwährung zum Zeitpunkt des Kaufs mit dem aktuellen Wechselkurs. Die entstehende Gutscheikarte ist in dieser Währung bezeichnet und kann nur von Kunden eingelöst werden, die in derselben Währung einkaufen.

| Schritt | Was passiert |
|--------|-------------|
| **Produkt einrichten** | Sie legen den Preis für die Gutscheikarte in Ihrer Grundwährung fest und wählen eine Zielwährung (z. B. NZD) |
| **Kauf** | Ein Kunde kauft die Gutscheikarte. Der Grundpreis wird in NZD mit dem aktuellen Wechselkurs konvertiert |
| **Gutscheikarte erstellt** | Die Gutscheikarte wird mit einem Wert in NZD ausgestellt (z. B. NZ$78,50) |
| **Einlösung** | Der Empfänger gibt den Code beim Checkout ein, während er in NZD einkauft. Der NZD-Bestand wird abgebucht |

## Voraussetzungen

Bevor Sie Gutscheikarten mit mehreren Währungen einrichten, stellen Sie sicher, dass Sie folgende Dinge haben:

1. **Mehrere Währungen aktiviert** — Gehen Sie zu **Einstellungen > Store-Einstellungen** und aktivieren Sie die Unterstützung für mehrere Währungen
2. **Unterstützte Währungen konfiguriert** — Fügen Sie die Währungen hinzu, die Sie anbieten möchten (z. B. NZD, SGD, EUR)
3. **Wechselkurs-Anbieter verbunden** — Gehen Sie zu **Einstellungen > Wechselkurse** und konfigurieren Sie einen Anbieter, damit aktuelle Kurse verfügbar sind

## Einrichten eines Gutscheikarten-Produkts mit mehreren Währungen

### Schritt 1: Erstellen oder bearbeiten Sie eine Gutscheikarte

1. Navigieren Sie zu **Produkte > Alle Produkte**
2. Klicken Sie auf **+ Produkt hinzufügen** oder öffnen Sie ein vorhandenes Gutscheikarten-Produkt
3. Legen Sie den **Produkttyp** auf **Gutscheikarte** fest

### Schritt 2: Währung der Gutscheikarte festlegen

1. Klicken Sie auf den Reiter **Gutscheikarte**
2. Konfigurieren Sie Ihre Bezeichnungs-Einstellungen wie gewohnt (feste Beträge, benutzerdefinierte Beträge oder beides)
3. Am unteren Ende des Gutscheikarten-Reiters finden Sie das Dropdown **Gutscheikarten-Währung**
4. Wählen Sie die Zielwährung (z. B. **NZD - Neuseeland-Dollar**)
5. Speichern Sie das Produkt

Das Dropdown zeigt alle Währungen an, die in Ihren Store-Einstellungen aktiviert sind. Das Wählen von **Store-Grundwährung (Standard)** bedeutet, dass Gutscheikarten in Ihrer Grundwährung ausgestellt werden — dies ist das Standardverhalten.

### Schritt 3: Preis festlegen

Legen Sie den Produkt-Preis in Ihrer Grundwährung wie gewohnt fest. Wenn ein Kunde diese Gutscheikarte kauft, wird der Preis automatisch in die Zielwährung konvertiert, basierend auf dem aktuellen Wechselkurs.

**Beispiel:** Ihre Grundwährung ist USD. Sie erstellen eine Gutscheikarte mit einem Preis von 50 USD und legen die Gutscheikarten-Währung auf NZD fest. Wenn der Wechselkurs 1 USD = 1,57 NZD ist, wird die entstehende Gutscheikarte einen Wert von NZ$78,50 haben.

## Währungsabgleich und Einlösung

Gutscheikarten mit mehreren Währungen verwenden **Einlösung in derselben Währung** — die aktive Währung des Kunden beim Einkaufen muss mit der Währung der Gutscheikarte übereinstimmen.

### Was Kunden erleben

- Ein Kunde, der in **NZD** einkauft, kann eine NZD-Gutscheikarte beim Checkout einlösen
- Ein Kunde, der in **USD** einkauft, kann keine NZD-Gutscheikarte einlösen — er sieht eine Nachricht, die die Währungsunterschiede erklärt
- Kunden können ihre Einkaufswährung mit dem Währungs-Selektor auf Ihrer Storefront ündern, bevor sie die Gutscheikarte einlösen

### Wie der Saldo funktioniert

Der Gutscheikarten-Saldo wird immer in der ursprünglichen Währung verfolgt:

- Eine Gutscheikarte mit NZ$78,50 startet mit einem Saldo von NZ$78,50
- Wenn ein Kunde einen Kauf im Wert von NZ$30 tätigt, beträgt der verbleibende Saldo NZ$48,50
- Der Saldo schwankt nicht mit Wechselkursen — der Nennwert ist fest

Wenn die Gutscheikarte beim Checkout angewendet wird, konvertiert das System den Rabatt intern in Ihre Grundwährung für die Bestellberechnung, aber der Gutscheikarten-Saldo wird immer in der ursprünglichen Währung abgebucht.

## Verwaltung von Gutscheikarten mit mehreren Währungen

Navigieren Sie zu **Produkte > Gutscheikarten**, um alle ausgestellten Gutscheikarten anzuzeigen. Gutscheikarten mit mehreren Währungen werden mit ihrer ursprünglichen Währung angezeigt:

- **Saldo** wird in der Währung der Gutscheikarte angezeigt (z. B. NZ$48,50)
- **Transaktionen** protokollieren Beträge in der Währung der Gutscheikarte
- **Anfangswert** zeigt den konvertierten Betrag zum Zeitpunkt des Kaufs an

### Überprüfen von Wechselkurs-Details

Jede Gutscheikarten-Transaktion protokolliert den Wechselkurs, der zum Zeitpunkt der Transaktion verwendet wurde. Dies ermöglicht eine vollständige Prüfung für Buchhaltungszwecke.

## Beispiele

### Beispiel 1: Regionale Gutscheikarte für Neuseeland

**Szenario:** Sie betreiben einen Store aus den USA, haben aber Kunden in Neuseeland. Sie möchten Gutscheikarten in NZD ausgeben.

| Einstellung | Wert |
|-----------|-----|
| Produktname | NZ Gutscheikarte |
| Produkttyp | Gutscheikarte |
| Preis | 50,00 $ (USD — Ihre Grundwährung) |
| Bezeichnungstyp | Feste Bezeichnungen |
| Feste Bezeichnungen | 25, 50, 100, 200 |
| Gutscheikarten-Währung | NZD - Neuseeland-Dollar |
| Ablaufdatum | 365 Tage |

Wenn ein Kunde die 50 $ Bezeichnung auswählt:
- Das System konvertiert 50 USD in NZD mit dem aktuellen Wechselkurs
- Eine Gutscheikarte wird mit dem NZD-Äquivalent erstellt (z. B. NZ$78,50)
- Der Empfänger kann sie einlösen, wenn er in NZD einkauft

### Beispiel 2: Gutscheikarten in mehreren Währungen

**Szenario:** Sie verkaufen an Kunden in Singapur, Australien und dem Vereinigten Königreich. Erstellen Sie drei Gutscheikarten-Produkte:

1. **SG Gutscheikarte** — Gutscheikarten-Währung: SGD
2. **AU Gutscheikarte** — Gutscheikarten-Währung: AUD
3. **UK Gutscheikarte** — Gutscheikarten-Währung: GBP

Jedes Produkt konvertiert Ihren Grundpreis in die Zielwährung zum Zeitpunkt des Kaufs. Kunden in jedem Gebiet können die Gutscheikarte in ihrer lokalen Währung einlösen.

### Beispiel 3: Mischung aus Gutscheikarten

**Szenario:** Sie möchten sowohl Gutscheikarten in der Grundwährung als auch regionale Gutscheikarten anbieten.

- **Store Gutscheikarte** — Gutscheikarten-Währung: *Store-Grundwährung (Standard)* — einlösbar in Ihrer Grundwährung
- **NZ Gutscheikarte** — Gutscheikarten-Währung: NZD — einlösbar nur in NZD

Beide Produkte können in Ihrem Katalog nebeneinander existieren. Kunden sehen, in welcher Währung eine Gutscheikarte bezeichnet ist, wenn sie den Saldo prüfen.

## Tipps

- Beginnen Sie mit einer regionalen Währung und testen Sie den gesamten Ablauf (Kauf, Lieferung, Einlösung), bevor Sie weitere Währungen hinzufügen.
- Der Wechselkurs zum Zeitpunkt des Kaufs bestimmt den Wert der Gutscheikarte. Wenn sich die Kurse stark ändern, bleibt der Wert der Gutscheikarte fest — dies schüzt sowohl Sie als auch Ihre Kunden.
- Machen Sie die Währung im Produkt-Namen klar (z. B. "NZ Gutscheikarte" oder "Gutscheikarte (NZD)") damit Kunden wissen, was sie kaufen.
- Gutscheikarten ohne festgelegte Währung funktionieren weiterhin wie zuvor in Ihrer Grundwährung — bestehende Produkte werden nicht beeinflusst.
- Üben Sie Ihre Wechselkurs-Anbieter, um sicherzustellen, dass die Kurse aktuell sind. Veraltete Kurse können zu über- oder unterbewerteten Gutscheikarten führen.
- Üben Sie Ihre Bezeichnungen sorgfältig. Eine Bezeichnung von 25 USD konvertiert zu etwa NZ$39 — runde Bezeichnungen in der Zielwährung können besser aussehen. Sie können separate Produkte mit Bezeichnungen erstellen, die in der Zielwährung runde Zahlen sind.