---
title: Besucheranalytik
---

Besucheranalytik gibt Ihnen einen klaren Überblick darüber, wie Kunden durch Ihr Geschäft navigieren. Sie können sehen, welche Seiten die meisten Besuche anziehen, wie sich der Gesamtverkehr im Laufe der Zeit entwickelt, welche Geräte Ihre Kunden verwenden und wie sich neue Besucher im Vergleich zu wiederkehrenden Besuchern verhalten – alles ohne externe Analysetools zu benötigen.

## Übersicht der Analysebildschirme

Ihr Geschäft verfolgt Besucheraktivitäten automatisch, sobald das GeoIP-System aktiv ist. Die Daten sind in drei Ansichten organisiert, jede bietet Ihnen einen unterschiedlichen Grad an Detailtiefe.

### Tägliche Verkehrsübersicht

Navigieren Sie zu **Kunden > Tägliche Verkehrsstatistiken**, um den Gesamtverkehr Ihres Geschäfts für jeden Tag zu sehen. J Zeile stellt einen Kalendertag dar und zeigt:

| Spalte | Was es Ihnen sagt |
|--------|-------------------|
| **Datum** | Der Tag, an dem der Verkehr erfasst wurde |
| **Gesamtansichten** | Alle Seitenansichten, einschließlich von Bots |
| **Eindeutige Besucher** | Unterschiedliche Besucher (nach Sitzung) |
| **Bot-Ansichten** | Ansichten von Crawlern und automatisierten Tools |
| **Neue Besucher** | Sitzungen ohne vorherige Historie |
| **Wiederkehrende Besucher** | Sitzungen von Besuchern, die zuvor gesehen wurden |
| **Desktop-Ansichten** | Ansichten von Desktop-Browsern |
| **Mobile-Ansichten** | Ansichten von mobilen Geräten |
| **Tablet-Ansichten** | Ansichten von Tablet-Geräten |

Verwenden Sie die Datenhierarchie-Navigation oben in der Liste, um schnell zu einem bestimmten Monat oder Jahr zu springen. Die Gesamtwerte werden täglich durch einen automatisierten Hintergrundprozess aktualisiert, sodass die Zahlen für den aktuellen Tag am nächsten Morgen erscheinen.

### Statistiken pro Seite

Navigieren Sie zu **Kunden > Tägliche Seitenstatistiken**, um den Verkehr nach einzelnen Seiten aufgeteilt anzuzeigen. J Zeile zeigt einen URL-Pfad für einen Tag, sodass Sie die Leistung bestimmter Seiten im Laufe der Zeit vergleichen können.

| Spalte | Was es Ihnen sagt |
|--------|-------------------|
| **Datum** | Der Tag, zu dem diese Statistiken gehören |
| **URL-Pfad** | Der normalisierte Seitenpfad (z. B. `/products/blue-widget`) |
| **Ansichten** | Gesamtansichten für diese Seite an diesem Tag |
| **Eindeutige Besucher** | Unterschiedliche Besucher, die diese Seite angesehen haben |
| **Bot-Ansichten** | Ansichten von Bots auf dieser Seite |
| **Einträge** | Wie viele Sitzungen auf dieser Seite begonnen wurden (es war ihre Startseite) |

Verwenden Sie das **URL-Pfad**-Suchfeld, um Statistiken für eine bestimmte Seite zu finden. Zum Beispiel können Sie nach `/products/` suchen, um den Verkehr aller Produktseiten anzuzeigen, oder nach einem bestimmten Produkt-Slug suchen, um sich auf ein einzelnes Produkt zu konzentrieren.

### Einzelne Seitenansichtsereignisse

Navigieren Sie zu **Kunden > Seitenansichten**, um eine Rohprotokolldatei aller verfolgten Seitennavigationen anzuzeigen. Dies ist ein schreibgeschütztes Protokoll – Sie können keine Einträge hinzufügen oder bearbeiten. Verwenden Sie es, um bestimmte Sitzungen zu untersuchen oder sicherzustellen, dass die Verfolgung korrekt erfasst wird.

J Eintrag zeigt:
- **URL-Pfad** – die besuchte Seite
- **Sitzung** – eine kurze Identifikation der Besuchersitzung
- **Quelle** – ob der Besuch von der headless-Frontend- oder der Standardverkaufsfrontseite kam
- **Ist Bot** – ob der Besucher als automatisierter Verkehr identifiziert wurde
- **Ist Startseite** – ob dies die erste Seite in ihrer Sitzung war
- **Zeitstempel** – die genaue Zeit des Besuchs

Sie können nach **Ist Bot**, **Quelle** und **Ist Startseite** mit den Seitenleisten-Filtern filtern und nach Datum mit der Datenhierarchie oben navigieren.

## Verkehrsverläufe erkennen

Die tägliche Verkehrsübersicht ist Ihr bestes Werkzeug, um Trends zu erkennen. Achten Sie auf Muster wie:

- **Verkehrsspitzen** nach dem Durchführen einer Promotion oder dem Versenden eines Marketing-E-Mails
- **Schrittweise Wachstum** über Wochen und Monate, während Ihr Geschäft organische Sichtbarkeit gewinnt
- **Wochenend- vs. Wochentagsmuster**, um zu verstehen, wann Ihre Kunden am aktivsten sind
- **Mobile vs. Desktop-Aufteilung**, um zu entscheiden, ob Sie Priorität für mobile optimierte Designänderungen setzen sollen

Die Spalten **Neue Besucher** und **Wiederkehrende Besucher** zusammen zeigen Ihnen, wie gut Sie Kunden beibehalten. Ein gesundes Geschäft sieht in der Regel eine Mischung aus beiden – ein hoher Anteil an neuen Besuchern deutet auf starke Akquise hin, während ein höherer Anteil an wiederkehrenden Besuchern darauf hindeutet, dass Kundenbindung aufgebaut wird.

Die pro-Seiten-Statistikansicht, sortiert nach Ansichten in absteigender Reihenfolge (Standard), zeigt Ihnen sofort, welche Seiten den meisten Traffic an einem bestimmten Tag generieren.

Achten Sie auf:

- **Seiten mit hohem Eintritt, aber geringen Ansichten** — Seiten, die Besucher aus Suchmaschinen oder Werbung anziehen, aber nicht die Aufmerksamkeit halten
- **Seiten mit hohen Ansichten und vielen eindeutigen Besuchern** — beliebte Zielseiten, die aktuell gehalten werden sollten
- **Produktseiten mit steigender Ansichtszahl** — Produkte, die möglicherweise eine bessere Suchmaschinen-Sichtbarkeit erlangen

### Beispiel: Traffic für ein Produkt finden

Um zu prüfen, wie viel Traffic Ihr bestverkauftes Produkt letzte Woche erhielt:

1. Navigieren Sie zu **Customers > Daily Page Stats**
2. Verwenden Sie die Datenhierarchie, um die relevante Woche auszuwählen
3. Geben Sie im Suchfeld die URL-Slug des Produkts ein (z. B. `/blue-widget`)
4. Überprüfen Sie die **Ansichten**, **Eindeutigen Besucher** und **Eintritte** über die angezeigten Tage

## Besucherstandortdaten

Navigieren Sie zu **Customers > Visitor Locations**, um eine Sitzungsebene-Ansicht davon zu erhalten, wo sich Ihre Besucher befinden. Jeder Eintrag stellt eine Besuchersitzung dar und enthält:

- Land und Stadt (automatisch durch das GeoIP-System ermittelt)
- Gerätetyp (Desktop, Mobil, Tablet)
- Währungs- und Sprachpräferenzen, die der Besucher ausgewählt hat
- UTM-Kampagnenzuordnung (Quelle, Medium, Kampagnenname)
- Flags für Bot- und Admin-Traffic

Sie können Besucher nach Land, Gerätetyp, UTM-Quelle und ob sie Bots oder Admin-Mitarbeiter waren, filtern. Verwenden Sie den Filter **Is Bot** auf false, um sich auf echten Kundenverkehr zu konzentrieren, und den Filter **Is Admin Traffic**, um Ihre eigenen Test-Sitzungen aus der Analyse auszuschließen.

## Tipps

- Bot-Ansichten werden separat verfolgt und automatisch aus der Anzahl der eindeutigen Besucher ausgeschlossen — Ihre Traffic-Zahlen spiegeln echte Kundenaktivitäten wider
- Die Spalte **Eintritte** in den pro-Seiten-Statistiken zeigt Ihnen, welche Seiten als Eingangstor Ihres Shops aus Suchmaschinen und Werbung dienen; die Optimierung dieser Seiten hat den größten Einfluss
- Filtern Sie Besucherstandorte nach **UTM Source**, um zu messen, wie viel Traffic ein bestimmter Marketingkanal (z. B. ein E-Mail-Newsletter oder eine Google-Werbung) tatsächlich sendet
- Tägliche Statistiken werden über Nacht aggregiert — wenn Sie denselben Tag Traffic prüfen müssen, verwenden Sie direkt das Protokoll der Seitenansichten
- Die Geräteaufschlüsselung in der täglichen Zusammenfassung hilft Ihnen, Designarbeiten zu priorisieren; wenn mehr als die Hälfte Ihrer Besuche mobil sind, stellen Sie sicher, dass Ihre Produktseiten und der Checkout auf kleinem Bildschirm gut aussehen