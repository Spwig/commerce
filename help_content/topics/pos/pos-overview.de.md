---
title: POS-Übersicht
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: pos-dashboard-overview.webp
  description: The POS dashboard landing page — full page at 1440x900
- url: /en/admin/
  filename: admin-sidebar-pos-group.webp
  description: Admin sidebar zoomed to the "Point of Sale" group, showing the expanded submenu with all items visible
-->

Spwig POS ist ein browserbasiertes Kassensystem, das es Ihrem Personal ermöglicht, Verkäufe im Geschäft über jedes Tablet oder Laptop abzurechnen — ohne spezielle Hardware oder Softwareinstallation. Da Spwig POS auf derselben Plattform läuft wie Ihr Online-Shop, sind Ihr Produktkatalog, Lagerbestände, Kundennachrichten und Bestellhistorie immer über alle Kanäle synchronisiert. Ein im Geschäft getätigter Verkauf reduziert sofort das Lagerbestand und erscheint in Ihren Bestellberichten neben Web-Verkäufen.

Spwig POS ist in jeder Edition enthalten — Community, Pro und Enterprise — ohne zusätzliche Kosten. Es gibt nichts zu entsperren oder zu upgraden.

![POS-Dashboard](/static/core/admin/img/help/pos/pos-dashboard-overview.webp)

## Wo sich POS im Admin-Bereich befindet

Im Seitenleistenmenü scrollen Sie zu der Gruppe **Point of Sale**. Klicken Sie auf **POS Dashboard**, um den POS-Verwaltungsbereich unter `/admin/pos/` zu öffnen. Von hier aus können Sie Ihre Terminals überwachen, kürzliche Schichten ansehen und über das Unter-Menü zu jedem POS-Konfigurationsbereich navigieren:

- **POS Dashboard** — Übersicht über den Terminalstatus, aktive Schichten und kürzliche POS-Verkäufe
- **Terminals** — Registrierte POS-Geräte und deren Einstellungen
- **Schichten** — Offene und geschlossene Schichtaufzeichnungen mit Bargeldabrechnungsdaten
- **Geschäftsgruppen** — Gruppen physischer Standorte, die regionale Einstellungen teilen
- **Belegvorlagen** — Individuelle Beleglayouts pro Geschäft oder Gruppe
- **Promo-Slides** — Werbebilder, die auf dem Kundenbildschirm angezeigt werden, wenn dieser leer ist
- **Terminal-Anbieter** — Zahlungsdienstleistungsverbindungen (z. B. Stripe Terminal, Square)
- **Kartenleser** — Physische Kartenlesergeräte, die mit Ihren Terminals verbunden sind
- **Open POS** — Öffnet die POS-Schnittstelle in einem neuen Tab

![Admin-Seitenleiste — Point of Sale-Gruppe](/static/core/admin/img/help/pos/admin-sidebar-pos-group.webp)

## Die POS-Terminal-App

Ihr Kassierer arbeitet in der POS-Schnittstelle, die als Progressive Web App (PWA) unter `/pos/` auf Ihrem Store-Domain läuft. Sie kann wie eine native App auf einem Tablet oder Laptop installiert werden — sie funktioniert vom Startbildschirm aus und arbeitet weiterhin im Offline-Modus, wenn die Internetverbindung vorübergehend ausfällt.

Die POS-Schnittstelle ist vom Admin-Backend getrennt. Ihr Personal meldet sich unter `/pos/` mit ihren Store-Anmeldeinformationen an, nicht auf den Haupt-Admin. Der Admin ist der Ort, an dem Sie alles konfigurieren und überwachen; die POS-App ist der Ort, an dem Verkäufe stattfinden.

Der Kundenfacing-Bildschirm läuft unter `/pos/display/` — ein zweiter Bildschirm oder ein Tablet, das dem Kunden zugewandt ist, um den aktuellen Warenkorb, die Preise und Werbebilder zwischen Transaktionen anzuzeigen.

## Schlüsselbegriffe

Das Verständnis dieser Begriffe macht den Rest der POS-Dokumentation leichter zu folgen.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Begriff | Bedeutung |
|------|---------------|
| **Geschäftsgruppe** | Ein benannter Sammelbegriff für physische Standorte, die regionale Einstellungen wie Währung, Sprache und Zeitzone teilen. Beispiel: "Neuseeland-Geschäfte" oder "Singapur-Region". |
| **Geschäftsstandort** | Ein einzelner Laden oder Zweig. In Spwig sind Geschäftsstandorte Lageraufzeichnungen, die als Verkaufsstandorte markiert sind. |
| **POS-Terminal** | Ein Gerät (Tablet, Laptop), das einem Geschäftsstandort zugeordnet ist. Jedes Terminal hat seinen eigenen Namen, ein Paarungscode und eine optionale Kartenleser-Zuordnung. |
| **Kartenleser** | Die Zahlungsterminal-Hardware, die an ein POS-Terminal angeschlossen ist – beispielsweise ein Stripe Reader S700 oder eine Adyen-Kartenmaschine. Es verarbeitet kontaktlose und Chip-and-PIN-Zahlungen. |
| **Zahlungsdienstleister** | Der Dienst hinter dem Kartenleser – Stripe Terminal, Square, Adyen und andere. Sie konfigurieren einen Zahlungsdienstleister pro Geschäft und verbinden Ihre Kartenleser über ihn. |
| **Schicht** | Ein Öffnungs- oder Schließzeitraum an einem Terminal. Ein Kassierer öffnet eine Schicht am Anfang seiner Sitzung (indem er den Anfangskassenbestand eingibt) und schließt sie am Ende, indem er den Geldbetrag in der Kasse zählt. Schichtberichte zeigen den Gesamtumsatz, Rückerstattungen und jede Gelddifferenz an. |
| **Kundenscreen** | Ein zweiter Bildschirm oder Tablet, das dem Kunden zugewandt ist und den aktuellen Warenkorb, den Gesamtbetrag und Werbeslides anzeigt, wenn das Terminal leer ist. Es wird über einen kurzen Paarungscode mit einem POS-Terminal verbunden. |
| **Paarungscode** | Ein 8-stelliger Code, der verwendet wird, um ein neues Gerät mit einem Terminal-Record im Admin zu verknüpfen. Wenn Sie ein Terminal registrieren, geben Sie dessen Paarungscode zum ersten Mal ein, wenn Sie `/pos/` auf diesem Gerät öffnen. |
| **Gesperrter Warenkorb** | Eine pausierte Transaktion, die gespeichert wird, damit der Kassierer einen anderen Kunden bedient und später zur ursprünglichen Verkaufsaktion zurückkehren kann. Gesperrte Warenkörbe werden pro Terminal gespeichert und verfallen nach 24 Stunden.

## Wie Lager und Bestellungen verbunden sind

Jedes Produkt, das Sie über den POS verkaufen, stammt aus Ihrem Hauptkatalog. Das Lager wird vom gleichen Lager abgezogen, das dem Terminal zugewiesen ist, sodass die Verfügbarkeit online und im Geschäft weiterhin korrekt bleibt. POS-Bestellungen erscheinen in **Bestellungen** neben Ihren Web-Bestellungen mit einem POS-Abzeichen, um sie zu unterscheiden. Kundenkonten, die am Kassentresen erstellt werden, werden auch auf Ihrem Online-Shop verwendet – wenn ein Kunde bereits online eingekauft hat, kann der Kassierer ihn nach Namen oder E-Mail suchen und die In-Store-Bestellung seinem Konto zuordnen.

## Einstellungshierarchie

POS-Einstellungen fließen von allgemein zu spezifisch, sodass Sie nur die Einstellungen konfigurieren müssen, die sich auf jeder Ebene unterscheiden:

1. **Standard der Website** – Die allgemeine Währung, Sprache und Zeitzone Ihres Geschäfts aus **Einstellungen > Geschäftseinstellungen**
2. **Geschäftsgruppe** – Überschreibt Währung, Sprache oder Zeitzone für alle Standorte in der Gruppe
3. **Geschäftsstandort** – Weitere Überschreibungen für einen bestimmten Zweig (in seiner Lageraufzeichnung festgelegt)
4. **Terminal** – Geräteebene für Währung oder Hardware-Überschreibungen für einen einzelnen Kassentresen

Wenn Sie ein Einzelstandort-Geschäft betreiben, können Sie Geschäftsgruppen vollständig überspringen und alles von Ihren Standard-Einstellungen der Website erben.

## Was Sie im POS-Admin tun können

| Aufgabe | Wo |
|------|-------|
| Registrieren Sie ein neues POS-Gerät | **Verkaufsplatz > Terminals** |
| Verbinden Sie einen Zahlungsdienstleister (Stripe, Square usw.) | **Verkaufsplatz > Terminal-Anbieter** |
| Verknüpfen Sie einen physischen Kartenleser mit einem Terminal | **Verkaufsplatz > Kartenleser** |
| Überprüfen oder schließen Sie eine offene Schicht | **Verkaufsplatz > Schichten** |
| Anpassen Sie das Layout Ihrer Quittung | **Verkaufsplatz > Quittungsvorlagen** |
| Fügen Sie Werbebilder für den Kundenscreen hinzu | **Verkaufsplatz > Werbeslides** |
| Organisieren Sie Zweige nach Region | **Verkaufsplatz > Geschäftsgruppen** |
| Starten Sie die Kassierer-Oberfläche | **Verkaufsplatz > POS öffnen** (öffnet sich in einem neuen Tab)

## Tipps

- Sie benötigen keine Geschäftsgruppe, wenn Sie nur einen Standort betreiben.

# Store groups

Store groups sind nützlich, wenn Sie mehrere Filialen mit unterschiedlichen regionalen Einstellungen haben — beispielsweise Geschäfte in verschiedenen Ländern, die unterschiedliche Währungen verwenden.
- Geben Sie jedem Terminal einen eindeutigen, beschreibenden Namen (z. B. "Vorderbereich" oder "Café-Kasse"), damit Schichtberichte und Quittungen leicht zu lesen sind.
- Richten Sie Ihre Quittungsvorlage vor Ihrem ersten Schichtbeginn ein — Sie können das Logo, die Geschäftsadresse, die Fußzeile und sogar einen QR-Code hinzufügen, der auf eine Bewertungsseite oder ein Loyalitätsprogramm verlinkt.
- Der Kundendisplay unter `/pos/display/` funktioniert auf jedem Gerät mit einem Browser.

Ein zusätzlicher Tablet- oder Monitor reicht aus — es ist keine zusätzliche Hardware erforderlich.
- Wenn ein Kartenleser während einer beschäftigten Zeit offline geht, kann der POS Bargeld- und manuell eingegebene Kartenzahlungen als Notfalllösung akzeptieren, damit Verkäufe ununterbrochen weiterlaufen können.
- POS-Schichtberichte sind mit dem Kassierer verknüpft, der sie geöffnet hat, wodurch es am Ende jeder Sitzung einfach ist, den Bargeldbestand abzugleichen.