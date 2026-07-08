---
title: Affiliate-Programm-Übersicht
---

Das Spwig-Affiliate-Programm ermöglicht es Ihnen, Partner zu gewinnen, die Ihre Produkte bewerben und dafür Provisionen erhalten. Dieses Marketingkanal erweitert Ihren Einfluss durch Influencer, Blogger, Content-Ersteller und Markenbotschafter, die eindeutige Tracking-Links mit ihren Followern teilen. Wenn jemand auf einen Affiliate-Link klickt und einen Kauf tätigt, erhält der Affiliate eine Provision und Sie gewinnen einen Kunden.

Diese Übersicht erklärt, was das Affiliate-Programm ist, für wen es geeignet ist und wie Händler es nutzen, um ein Partner-Netzwerk zu erstellen, das Verkäufe steigert.

![Händler-Dashboard](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Schlüsselkonzepte

Das Verständnis dieser Kernbegriffe hilft Ihnen dabei, Ihr Affiliate-Programm zu konfigurieren und zu verwalten:

| Begriff | Definition |
|--------|-----------|
| **Affiliate** | Ein Partner, der Ihre Produkte bewirbt und für vermittelte Verkäufe Provisionen erhält |
| **Programm** | Eine Provisionenstruktur mit Sätzen, Regeln und Einstellungen (Sie können mehrere Programme erstellen) |
| **Tracking-Link** | Ein eindeutiger URL, der den Affiliate-Code enthält (z. B. `yourstore.com/?ref=CODE`) |
| **Provision** | Die Zahlung, die ein Affiliate für einen vermittelten Verkauf erhält, die basierend auf den Programmroutinen berechnet wird |
| **Cookie-Laufzeit** | Wie lange (in Tagen) der Tracking-Cookie besteht, nachdem ein Kunde auf einen Affiliate-Link geklickt hat |
| **Auszahlung** | Eine Massenzahlung, die mehrere genehmigte Provisionen auf einmal abwickelt |
| **Händler-Dashboard** | Ihr Verwaltungsinterface für die Verwaltung von Programmen, Affiliates, Provisionen und Auszahlungen |
| **Affiliate-Portal** | Das öffentlich zugängliche Dashboard, in dem Affiliates ihre Einnahmen einsehen, Tracking-Links erhalten und Auszahlungen anfordern |

## Wie es funktioniert

Der Affiliate-Ablauf folgt vier Hauptphasen:

### 1. Bewerben
Affiliates entdecken Ihr Programm und senden ihre Bewerbung über das öffentliche Affiliate-Portal unter `/affiliate/` auf Ihrem Store. Sie können **automatische Freigabe** für offene Programme aktivieren oder **manuelle Prüfung** für Einladungs-Only-Partnerschaften.

### 2. Freigeben
Sie prüfen Bewerbungen in **Marketing > Affiliates**. Überprüfen Sie die Website, das soziale Medienprofil und die Zielgruppe jedes Bewerbers, bevor Sie die Freigabe erteilen. Nach der Freigabe erhält der Affiliate Zugangsdaten und kann auf ihr Dashboard zugreifen.

### 3. Bewerben
Genehmigte Affiliates erhalten eindeutige Verweislinks über ihr Portal. Sie teilen diese Links in Blogbeiträgen, sozialen Medien, E-Mail-Newslettern oder wo immer sie mit ihrer Zielgruppe in Kontakt treten. Spwig setzt einen Tracking-Cookie, wenn jemand auf den Link klickt.

### 4. Verdienen
Wenn ein verworbener Kunde innerhalb der Cookie-Laufzeit einen Kauf abschließt, erstellt Spwig einen Eintrag für die Provision. Sie prüfen und genehmigen die Provisionen in **Marketing > Provisionen**, und verarbeiten die Auszahlungen, wenn Affiliates den Mindestauszahlungsschwellenwert erreichen.

## Übersicht über den Händler-Ablauf

Als Händler verwalten Sie den gesamten Programmlebenszyklus über Ihr Admin-Panel:

### Erstellen von Programmen
Beginnen Sie damit, ein oder mehrere Affiliate-Programme unter **Marketing > Affiliate-Programme** zu erstellen. Jedes Programm hat seine eigene Provisionenstruktur, Cookie-Laufzeit und Freigabeeinstellungen. Sie könnten separate Programme für Influencer (höhere Provision) erstellen, im Vergleich zu allgemeinen Partnern (niedrigere Provision).

### Prüfen von Bewerbungen
Neue Affiliate-Bewerbungen erscheinen unter **Marketing > Affiliates** mit dem Status **Ausstehend**. Prüfen Sie jede Bewerbung, um sicherzustellen, dass der Partner zu Ihrer Marke passt. Genehmigen Sie, um das Konto zu aktivieren, oder ablehnen Sie mit einem Grund.

### Genehmigen von Provisionen
Wenn Affiliates Verkäufe generieren, erscheinen die Provisionen unter **Marketing > Provisionen** mit dem Status **Ausstehend**. Prüfen Sie den verknüpften Auftrag, um sicherzustellen, dass er legitim ist (kein Selbstverweis, keine Retouren), und genehmigen Sie oder ablehnen Sie entsprechend.

### Verarbeiten von Auszahlungen
Sobald Affiliates genehmigte Provisionen über Ihren Mindestauszahlungsschwellenwert haben, verarbeiten Sie Massen-Auszahlungen unter **Marketing > Auszahlungen**. Spwig integriert sich mit PayPal und Airwallex für automatisierte Auszahlungen, oder Sie können manuelle Banküberweisungen aufzeichnen.

## Übersicht über den Affiliate-Ablauf

Das Verständnis davon, wie Affiliates Ihr Programm erleben, hilft Ihnen dabei, bessere Onboarding- und Support-Strategien zu entwerfen:

### Bewerben
Affiliates besuchen Ihr Affiliate-Portal, lesen die Programmdetails (Provisionsrate, Cookie-Laufzeit, Auszahlungsbedingungen) und senden eine Bewerbung mit ihren Kontaktdaten und Promotionskanälen.

### Links erstellen
Nach der Freigabe loggen sich Affiliates in ihr Dashboard ein, um Tracking-Links zu erstellen. Sie können allgemeine Store-Links erstellen oder Links zu bestimmten Produkten/Kategorien, die sie bewerben möchten.

### Bewerben
Affiliates teilen ihre Tracking-Links überall dort, wo sie potenzielle Kunden erreichen – Blogbeiträge, YouTube-Videos, Instagram-Stories, E-Mail-Newslettern oder Vergleichsseiten.

### Auszahlung anfordern
Affiliates verfolgen ihre Einnahmen in Echtzeit über das Affiliate-Portal-Dashboard. Wenn ihr genehmigter Saldo den Mindestauszahlungsschwellenwert erreicht, können sie eine Auszahlung anfordern.

## Wo Sie jede Funktion finden

| Funktion | Admin-Position | Beschreibung |
|--------|----------------|-------------|
| **Programme** | Marketing > Affiliate-Programme | Erstellen und konfigurieren Sie Provisionenstruktur |
| **Affiliates** | Marketing > Affiliates | Prüfen Sie Bewerbungen, verwalten Sie Affiliate-Konten |
| **Provisionen** | Marketing > Provisionen | Prüfen und genehmigen Sie ausstehende Provisionen |
| **Auszahlungen** | Marketing > Auszahlungen | Verarbeiten Sie Massenzahlungen an Affiliates |
| **Einstellungen** | Marketing > Affiliate-Einstellungen | Globale Einstellungen, Auszahlungsanbieter, Portal-Anpassungen |
| **Dashboard** | Marketing > Affiliate-Dashboard | Analyseübersicht mit Klicks, Bestellungen und Gesamtprovisionen |

Das Affiliate-Portal ist automatisch unter `/affiliate/` auf der öffentlichen URL Ihres Stores verfügbar.

## Typische Anwendungsfälle

Hier sind vier bewährte Methoden, wie Händler das Spwig-Affiliate-Programm nutzen, um ihr Geschäft zu wachsen:

### Influencer-Partnerschaften
Partner mit sozialen Medien-Influencern, die in Ihrem Nischenbereich engagierte Zielgruppen haben. Bieten Sie höhere Provisionssätze (15–20%) an, um qualitativ hochwertige Influencer anzuziehen, die viel Traffic generieren können. Nutzen Sie Tracking-Links, um den ROI für jede Partnerschaft zu messen.

### Markenbotschafter
Erstellen Sie ein Netzwerk aus treuen Kunden, die zu Markenvertretern werden. Bieten Sie diesen Wiederholungskunden Affiliate-Konten an, damit sie Provisionen verdienen, wenn sie Freunde und Familie vermitteln. Dies funktioniert besonders gut für Nischenprodukte mit begeisterten Communities.

### Content-Ersteller
Rekrutieren Sie Blogger, YouTuber und Podcast-Hosts, die Kaufleitfäden, Rezensionen oder Vergleichsinhalte erstellen. Affiliates mit evergreen-Inhalten können monatlich konsistente Verweisungen generieren.

### Verweisnetzwerke
Ermöglichen Sie bestehenden Kunden, Ihr Programm beizutreten und Provisionen zu verdienen, indem sie Produkte teilen, die sie lieben. Dies erzeugt einen viralen Effekt, bei dem zufriedene Kunden zu Werbenden werden und neue Kunden einbringen, die möglicherweise selbst zu Affiliates werden.

## Tipps

- **Beginnen Sie mit einem Programm** – Erstellen Sie ein allgemeines Partnerprogramm mit einer 10 % Provision und einer Cookie-Laufzeit von 30 Tagen. Sie können später spezialisierte Programme hinzufügen, sobald Sie verstehen, welche Partner am besten abschneiden.
- **Setzen Sie klare Erwartungen** – Dokumentieren Sie Ihren Genehmigungsprozess, Provisionstermine und Auszahlungsplan im Affiliate-Portal. Transparenz baut Vertrauen und reduziert Support-Anfragen.
- **Überwachen Sie auf Betrug** – Prüfen Sie Provisionen sorgfältig auf rote Flaggen wie Selbstverweise (Affiliates, die über ihre eigenen Links einkaufen), ungewöhnlich hohe Rückgaberate oder verdächtige Klickmuster. Verweigern Sie sofort betrügerische Provisionen.
- **Kommunizieren Sie regelmäßig** – Senden Sie monatliche Updates an Ihre Affiliates mit Programm-News, Highlights des Promotionskalenders und Anerkennung für Top-Performern. Aktive Kommunikation hält Affiliates engagiert und fördert ihre Werbung.
- **Optimieren Sie für mobile Geräte** – Die meisten Affiliates teilen Links auf sozialen Medien, wo die Mehrheit der Klicks von mobilen Geräten kommt. Testen Sie Ihren Checkout-Flow auf Smartphones, um sicherzustellen, dass der Erlebnis für verworbene Kunden reibungslos ist.
- **Bieten Sie kreative Materialien an** – Machen Sie es Affiliates leicht, Ihre Produkte zu bewerben, indem Sie Bannerbilder, Produktfotos und vorgefertigte Textvorlagen bereitstellen, die sie in ihrem Inhalt verwenden können.