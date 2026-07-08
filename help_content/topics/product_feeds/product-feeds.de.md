---
title: Produkt-Feeds
---

Produkt-Feeds ermöglichen es Ihnen, Ihren Katalog auf Einkaufsplattformen wie Google Shopping und Facebook Katalog zu exportieren. Sobald eine Verbindung hergestellt wurde, wird Ihre Produktinformation automatisch in einem Zeitplan synchronisiert, damit Ihre Werbung immer Ihre aktuellen Preise, Lagerbestände und Produktinformationen widerspiegelt.

Ihr Geschäft verwendet ein Komponentensystem für Anbieter, um Feeds bereitzustellen. Jeder Feed-Anbieter (Google, Facebook oder andere) wird als Komponente installiert und anschließend über ein Anbieterkonto verbunden. Sie können mehrere Feed-Anbieter gleichzeitig verwenden – beispielsweise einen Feed für Google Shopping und einen anderen für Facebook.

## Verbindung eines Feed-Anbieters

Bevor Sie Ihren Katalog synchronisieren können, müssen Sie mindestens eine Feed-Anbieterkomponente installieren und verbinden.

### Installation einer Anbieterkomponente

Anbieterkomponenten sind im Spwig-Komponentenmarkt erhältlich. Der Administrator Ihres Geschäfts installiert sie über das Komponentenaktualisierungssystem. Sobald eine Anbieterkomponente installiert ist, erscheint sie als Option beim Erstellen eines Feed-Anbieterkontos.

### Erstellen eines Feed-Anbieterkontos

1. Navigieren Sie zu **Marketing > Feed-Anbieter**
2. Klicken Sie auf **+ Feed-Anbieterkonto hinzufügen**
3. Füllen Sie das Formular aus:

**Anbieterinformationen-Abteilung:**
- **Site** — wählen Sie Ihr Geschäft (es gibt nur eines)
- **Anbieterkomponente** — wählen Sie den installierten Feed-Anbieter (z. B. Google Shopping, Facebook Katalog)
- **Kontoname** — ein beschreibender Name wie `Google Shopping — Haupt` oder `Facebook Katalog — US`

**Konfigurationsabteilung:**
- **Aktiv** — aktivieren Sie, um die Feed-Generierung und -Synchronisation zu ermöglichen
- **Primär** — aktivieren Sie, wenn dies Ihr Haupt-Feed-Anbieter für diese Plattformart ist
- **Priorität** — steuert die Sortierreihenfolge in der Liste (niedrigere Zahlen werden zuerst angezeigt)
- **Konfiguration** — anbieter-spezifische Einstellungen (siehe unten)

4. Klicken Sie auf **Speichern**

### Feed-Konfigurationsoptionen

Das Feld **Konfiguration** akzeptiert ein JSON-Objekt mit den folgenden Optionen:

| Option | Werte | Beschreibung |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Wie oft der Feed automatisch erneut generiert wird |
| `format_preference` | `xml`, `csv`, `json` | Ausgabeformat (die meisten Plattformen bevorzugen XML) |
| `include_variants` | `true` / `false` | Produktvarianten als separate Feed-Einträge einbeziehen |
| `target_country` | Ländercode z. B. `"US"` | Ziel-Land für den Feed |
| `content_language` | Sprachcode z. B. `"en"` | Sprache der Produktinformationen |

#### Beispielkonfiguration für einen täglichen XML-Feed mit Ziel USA:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtern, welche Produkte im Feed erscheinen

Sie können genau steuern, welche Produkte eingeschlossen werden, indem Sie eine `product_filter`-Sektion in die Konfiguration einfügen:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Filteroption | Beschreibung |
|---------------|-------------|
| `status` | Nur Produkte mit diesen Statuswerten einbeziehen. Verwenden Sie `["published"]`, um nur aktive Produkte einzubeziehen. |
| `in_stock_only` | Auf `true` setzen, um Produkte ohne Lagerbestand auszuschließen |
| `categories` | Auf bestimmte Kategorie-IDs beschränken |
| `brands` | Auf bestimmte Marken-IDs beschränken |

Sie können auch bestimmte Produkte durch ihre IDs mit `exclude_products` ausschließen:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Überwachen des Sync-Status

Die Liste der Feed-Anbieterkonten zeigt den Sync-Status jedes verbundenen Feeds im Überblick:

- **PENDING** — kein Sync wurde noch durchgeführt, oder der Feed wartet auf die Generierung
- **SYNCING** — ein Sync wird derzeit durchgeführt
- **SUCCESS** — der letzte Sync wurde ohne Fehler abgeschlossen
- **ERROR** — der letzte Sync ist fehlgeschlagen; die Fehlermeldung wird auf der Detailseite des Kontos angezeigt

Die Liste zeigt auch die Anzahl der Produkte im aktuellen Feed und den Zeitpunkt des letzten Syncs an.

## Anzeigen der generierten Feeds

Navigieren Sie zu **Marketing > Produkt-Feeds**, um die generierten Feed-Dateien anzuzeigen. Jeder Eintrag stellt einen generierten Feed-Snapshot dar und zeigt:


- **Provider-Konto** — zu dem dieses Feed gehört
- **Format** — XML, CSV oder JSON
- **Produktanzahl** — Anzahl der enthaltenen Produkte
- **Größe** — Dateigröße des generierten Feeds
- **Erstellt um** — wann er erstellt wurde
- **Ablauf um** — wann diese zwischengespeicherte Version abläuft
- **Status** — ob der Feed immer noch gültig ist oder abgelaufen ist
- **Herunterladen** — wie oft dieser Feed heruntergeladen wurde

Feeds sind im Admin-Panel schreibgeschützt — sie werden automatisch vom Sync-Prozess generiert.

## Sync-Historie ansehen

Navigieren Sie zu **Marketing > Feed Sync Logs**, um eine vollständige Historie aller Sync-Versuche für alle Ihre Feed-Konten zu sehen. Jeder Eintrag im Log protokolliert:

- Das Provider-Konto, das synchronisiert wurde
- Der Sync-Typ (Vollständig, Inkrementell, Manuel, oder Geplant)
- Status (Erfolgreich, Teilweise erfolgreich, Fehlgeschlagen, usw.)
- Synchronisierte, fehlgeschlagene und übersprungene Produkte
- Dauer der Synchronisation
- Eventuelle Fehlermeldungen

Das Sync-Log-Dashboard oben auf der Seite zeigt Gesamtstatistiken an: Gesamtzahl der Syncs, Erfolgsquote und Durchschnittsdauer der Syncs. Verwenden Sie die Filter **Konto** und **Sync-Typ**, um sich auf einen bestimmten Feed zu beschränken.

### Was tun, wenn eine Synchronisation fehlschlägt

1. Navigieren Sie zu **Marketing > Feed Sync Logs** und suchen Sie den fehlgeschlagenen Eintrag
2. Klicken Sie auf den Log-Eintrag, um die vollständige **Fehlermeldung** und **Fehlerdetails** anzuzeigen
3. Häufige Ursachen sind:
   - Fehlende erforderliche Produktfelder (Titel, Preis, Bild)
   - Ungültige oder abgelaufene API-Anmeldeinformationen — installieren Sie das Provider-Modul erneut, um die Anmeldeinformationen zu aktualisieren
   - Netzwerkfehler bei der Verbindung mit der API des Providers
4. Sobald das Problem behoben ist, wird die nächste geplante Synchronisation automatisch laufen, oder Sie können eine manuelle Synchronisation vom Provider-Konto aus auslösen

## Tipps

- Setzen Sie `"sync_interval": "daily"` für die meisten Anwendungsfälle — Google und Facebook benötigen keine häufigeren Updates, es sei denn, Sie haben eine sehr hohe Preisschwankung
- Schließen Sie immer `"in_stock_only": true` in Ihre Produktfilter ein, um das Werben für Produkte zu vermeiden, die Kunden nicht kaufen können
- Verwenden Sie einen beschreibenden Kontonamen, der die Plattform und das Zielmarkt beinhaltet (z. B. `Google Shopping — UK`), damit es einfach ist, mehrere Feeds zu verwalten
- Die Anzahl der **Produkte im Feed** auf dem Provider-Konto zeigt Ihnen sofort an, ob weniger Produkte als erwartet enthalten sind — prüfen Sie Ihre Produktfiltereinstellungen, wenn die Anzahl niedrig erscheint
- Kennzeichnen Sie ein Konto als **Primäres Feed** für jeden Provider-Typ; einige Berichterstattungstools verwenden dies, um Ihr Hauptfeed zu identifizieren
- Überprüfen Sie den Sync-Log nach jeder Massenänderung in Ihrem Produktkatalog, um sicherzustellen, dass die aktualisierten Daten korrekt erfasst wurden