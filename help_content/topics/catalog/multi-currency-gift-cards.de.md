---
title: Gutscheine in mehreren Währungen
---

Wenn Sie Kunden in mehreren Ländern bedienen, können Sie Gutscheine in bestimmten Währungen ausstellen. Ein Beispiel: Ein Kunde aus Neuseeland kann einen 50 NZD-Gutschein kaufen, und der Empfänger kann diesen in NZD einlösen – der Nennwert bleibt unabhängig von Wechselkurschwankungen gleich.

Diese Funktion erfordert, dass mehrere Währungen aktiviert sind und mindestens ein Wechselkurs-Anbieter konfiguriert ist.

> **Gutscheinverkäufe sind vorübergehend pausiert**, während wir den automatisierten Lieferfluss abschließen – siehe den **Gutscheine**-Hilfethema für Details. Sie können dennoch jetzt eine **Gutscheinwährung** für ein Produkt konfigurieren, damit es bereit ist, sobald der Verkauf wieder aufgenommen wird, und Sie können heute manuell einen währungsspezifischen Gutschein ausstellen, genauso wie Sie jeden anderen Gutschein ausstellen würden (geben Sie den **Anfangswert** in der Währung an, in der der Gutschein bezeichnet ist).

## Wie es funktioniert

Wenn Sie eine **Gutscheinwährung** für ein Gutscheinprodukt festlegen, konvertiert das System den Produktpreis in die Zielwährung zum Zeitpunkt des Kaufs mithilfe des aktuellen Wechselkurses. Der resultierende Gutschein wird in dieser Währung bezeichnet und kann nur von Kunden eingelöst werden, die in derselben Währung einkaufen.

| Schritt | Was passiert |
|--------|-------------|
| **Produktkonfiguration** | Sie legen den Gutscheinprodukt-Preis in Ihrer Basiswährung fest und wählen eine Zielwährung (z. B. NZD) |
| **Kauf** | Ein Kunde kauft den Gutschein. Der Basispreis wird in NZD mit dem aktuellen Wechselkurs konvertiert |
| **Gutschein erstellt** | Der Gutschein wird mit einem Wert in NZD ausgestellt (z. B. NZ$78,50) |
| **Einlösung** | Der Empfänger gibt den Code beim Checkout ein, während er in NZD einkauft. Der NZD-Betrag wird abgebucht |

## Voraussetzungen

Bevor Sie Gutscheine in mehreren Währungen einrichten, stellen Sie sicher, dass Sie Folgendes haben:

1. **Mehrwährung aktiviert** – Gehen Sie zu **Einstellungen > Store-Einstellungen** und aktivieren Sie die Unterstützung für mehrere Währungen
2. **Unterstützte Währungen konfiguriert** – Fügen Sie die Währungen hinzu, die Sie anbieten möchten (z. B. NZD, SGD, EUR)
3. **Wechselkursanbieter verbunden** – Gehen Sie zu **Einstellungen > Wechselkurse** und konfigurieren Sie einen Anbieter, damit aktuelle Kurse verfügbar sind

## Einrichten eines Gutscheinprodukts mit mehreren Währungen

### Schritt 1: Erstellen oder bearbeiten Sie ein Gutscheinprodukt

1. Navigieren Sie zu **Produkte > Alle Produkte**
2. Klicken Sie auf **+ Produkt hinzufügen** oder öffnen Sie ein vorhandenes Gutscheinprodukt
3. Legen Sie den **Produkttyp** auf **Gutschein** fest

### Schritt 2: Wählen Sie die Gutscheinwährung

1. Klicken Sie auf den **Gutschein**-Reiter
2. Konfigurieren Sie Ihre Bezeichnungs-Einstellungen wie gewohnt (feste Beträge, benutzerdefinierte Beträge oder beides)
3. Am unteren Ende des Gutschein-Reiters finden Sie das Dropdown **Gutscheinwährung**
4. Wählen Sie die Zielwährung (z. B. **NZD - Neuseeland-Dollar**)
5. Speichern Sie das Produkt

Das Dropdown zeigt alle in Ihren Store-Einstellungen aktivierten Währungen an. Das Auswählen von **Store-Basiswährung (Standard)** bedeutet, dass Gutscheine in Ihrer Basiswährung ausgestellt werden – dies ist das Standardverhalten.

### Schritt 3: Preis festlegen

Legen Sie den Produktpreis in Ihrer Basiswährung wie gewohnt fest. Wenn ein Kunde diesen Gutschein kauft, wird der Preis automatisch in die Zielwährung konvertiert, basierend auf dem aktuellen Wechselkurs.

**Beispiel:** Ihre Basiswährung ist USD. Sie erstellen ein Gutscheinprodukt mit einem Preis von 50 USD und legen die Gutscheinwährung auf NZD fest. Wenn der Wechselkurs 1 USD = 1,57 NZD beträgt, wird der resultierende Gutschein einen Wert von NZ$78,50 haben.

## Währungsabgleich und Einlösung

Gutscheine in mehreren Währungen verwenden **gleichwertige Währungseinlösung** – die aktive Währung des Kunden muss mit der Währung des Gutscheins übereinstimmen.

### Was Kunden erleben

- Ein Kunde, der in **NZD** einkauft, kann einen NZD-Gutschein beim Checkout einlösen
- Ein Kunde, der in **USD** einkauft, kann keinen NZD-Gutschein einlösen – er sieht eine Nachricht, die die Währungsinkongruenz erklärt
- Kunden können ihre Einkaufswährung mithilfe des Währungs-Selektors auf Ihrem Storefront ändern, bevor sie den Gutschein einlösen

### Wie der Saldo funktioniert

Der Gutscheinsaldo wird immer in seiner ursprünglichen Währung verfolgt:

- Eine Geschenkkarte im Wert von NZ$78,50 beginnt mit einem Saldo von NZ$78,50
- Wenn ein Kunde einen Kauf im Wert von NZ$30 tätigt, beträgt der verbleibende Saldo NZ$48,50
- Der Saldo ändert sich nicht mit Wechselkursen – der Nennwert ist fest

Wenn die Geschenkkarte am Checkout angewendet wird, konvertiert das System den Rabatt intern in Ihre Basiswährung für die Bestellberechnung, aber der Saldo der Geschenkkarte wird immer in ihrer ursprünglichen Währung abgebucht.

## Verwaltung von Geschenkkarten in mehreren Währungen

Navigieren Sie zu **Produkte > Geschenkkarten**, um alle ausgestellten Geschenkkarten anzuzeigen. Mehrwertwährungsgeschenkkarten werden mit ihrer ursprünglichen Währung angezeigt:

- **Saldo** wird in der Währung der Geschenkkarte angezeigt (z. B. NZ$48,50)
- **Transaktionen** werden in der Währung der Geschenkkarte erfasst
- **Anfangswert** zeigt den konvertierten Betrag zum Zeitpunkt des Kaufs an

### Prüfen von Wechselkursdetails

Jede Geschenkkarten-Transaktion protokolliert den Wechselkurs, der zum Zeitpunkt der Transaktion verwendet wurde. Dies ermöglicht eine vollständige Buchung für Buchhaltungszwecke.

## Beispiele

### Beispiel 1: Regionale Geschenkkarte für Neuseeland

**Szenario:** Sie betreiben ein Geschäft aus den USA, haben aber Kunden in Neuseeland. Sie möchten Geschenkkarten in NZD verkaufen.

| Einstellung | Wert |
|-----------|------|
| Produktname | NZ Geschenkkarte |
| Produkttyp | Geschenkkarte |
| Preis | $50,00 (USD – Ihre Basiswährung) |
| Nennwerttyp | Fixe Nennwerte |
| Fixe Nennwerte | 25, 50, 100, 200 |
| Geschenkkartenwährung | NZD - Neuseeland-Dollar |
| Ablaufdatum | 365 Tage |

Wenn ein Kunde den Nennwert von $50 auswählt:
- Das System konvertiert $50 USD in NZD mit dem aktuellen Wechselkurs
- Es wird eine Geschenkkarte mit dem entsprechenden NZD-Betrag erstellt (z. B. NZ$78,50)
- Der Empfänger kann sie beim Einkaufen in NZD einlösen

### Beispiel 2: Geschenkkarten in mehreren Währungen

**Szenario:** Sie verkaufen an Kunden in Singapur, Australien und dem Vereinigten Königreich. Erstellen Sie drei Geschenkkartenprodukte:

1. **SG Geschenkkarte** – Geschenkkartenwährung: SGD
2. **AU Geschenkkarte** – Geschenkkartenwährung: AUD
3. **UK Geschenkkarte** – Geschenkkartenwährung: GBP

Jedes Produkt konvertiert Ihren Basispreis in die Zielwährung zum Zeitpunkt des Kaufs. Kunden in jedem Gebiet können die Geschenkkarte in ihrer lokalen Währung einlösen.

### Beispiel 3: Kombinierte Geschenkkartenangebote

**Szenario:** Sie möchten sowohl Geschenkkarten in der Basiswährung als auch regionale Geschenkkarten anbieten.

- **Store Geschenkkarte** – Geschenkkartenwährung: *Store Basiswährung (Standard)* – einlösbar in Ihrer Basiswährung
- **NZ Geschenkkarte** – Geschenkkartenwährung: NZD – einlösbar nur in NZD

Beide Produkte können gleichzeitig in Ihrem Katalog existieren. Kunden sehen, in welcher Währung eine Geschenkkarte bezeichnet ist, wenn sie den Saldo prüfen.

## Tipps

- Beginnen Sie mit einer regionalen Währung und testen Sie den gesamten Ablauf (Kauf, Lieferung, Einlösung), bevor Sie weitere Währungen hinzufügen.
- Der Wechselkurs zum Zeitpunkt des Kaufs bestimmt den Wert der Geschenkkarte. Wenn sich die Kurse erheblich ändern, bleibt der Wert der Geschenkkarte fest – dies schützt sowohl Sie als auch Ihre Kunden.
- Machen Sie die Währung im Produktname klar (z. B. „NZ Geschenkkarte“ oder „Geschenkkarte (NZD)“), damit Kunden wissen, was sie kaufen.
- Geschenkkarten ohne festgelegte Währung funktionieren weiterhin genau wie zuvor in Ihrer Basiswährung – bestehende Produkte werden nicht beeinflusst.
- Überwachen Sie Ihren Wechselkursanbieter, um sicherzustellen, dass die Kurse aktuell sind. Veraltete Kurse können zu über- oder unterbewerteten Geschenkkarten führen.
- Überlegen Sie sich Ihre Nennwerte sorgfältig. Ein Nennwert von $25 USD konvertiert sich auf etwa NZ$39 – runde Nennwerte in der Zielwährung können besser aussehen. Sie können separate Produkte mit Nennwerten erstellen, die in der Zielwährung runde Zahlen sind.