---
title: Suchleistungs-Optimierung
---

Suchleistung beeinflusst direkt die Kundenerfahrung und Umwandlungsrate. Langsame Suchen frustrieren Kunden und erhöhen die Abbruchrate. Dieses umfassende Handbuch identifiziert häufige Leistungsengpässe im datenbankinternen Suchsystem von Spwig, bietet Optimierungsstrategien an und legt Leistungsziele fest. Nutzen Sie dieses Handbuch, wenn die Suchantwortzeiten die akzeptablen Schwellenwerte überschreiten oder Sie für das Katalogwachstum planen.

Zielantwortzeiten: <200ms für die Vervollständigung, <500ms für die Vollsuche. Folgen Sie dem untenstehenden Optimierungscheckliste, um diese Ziele zu erreichen.

## Verständnis von Leistungsindikatoren

Überwachen Sie diese Indikatoren in **Suche > Suchanalyse**:

**Antwortzeit** - Millisekunden, um eine Suchanfrage auszuführen (nur Serverseite, Netzwerklatenz ausgeschlossen)

**Cache-Trefferquote** - Prozentsatz der Suchen, die aus dem Cache abgerufen werden, im Vergleich zur Datenbank

**Anzahl der Abfragen** - Anzahl der Datenbankabfragen pro Suche (weniger ist besser)

**Datenbankabfragezeit** - Zeit, die in der Datenbank im Vergleich zur Anwendungscode verbracht wird

## Leistungsziele

| Abfragetyp | Ziel | Akzeptabel | Optimierung erforderlich |
|------------|--------|------------|----------------------|
| Vervollständigung | <200ms | 200-300ms | >300ms konsequent |
| Vollsuche | <500ms | 500-800ms | >800ms konsequent |
| Admin-Suche | <1000ms | 1000-1500ms | >1500ms konsequent |

Wenn Ihre Durchschnittsantwortzeiten die Schwellenwerte für "Optimierung erforderlich" überschreiten, implementieren Sie die untenstehenden Strategien.

## Leistungsüberwachung

**Durchschnittliche Antwortzeit des Analyse-Dashboards**

Navigieren Sie zu **Suche > Suchanalyse**, um die durchschnittliche Antwortzeit für alle Suchen anzuzeigen. Dies ist Ihr primärer Leistungsüberwachungsindikator.

**Wann untersuchen**: Durchschnittliche Antwortzeit >300ms für Vervollständigung oder >800ms für Vollsuche konsequent über mehrere Tage.

**Wöchentliche Überwachung**: Überprüfen Sie die Analyse jeden Montag, um eine frühe Erkennung von Leistungsabbau zu ermöglichen.

## Bekannte Leistungsengpässe

Die datenbankinterne Suche von Spwig hat mehrere dokumentierte Engpässe, die vermieden werden sollten:

### CTR-Berechnung N+1-Abfragen

**Was es ist**: Die CTR-Berechnung in AnalyticsService führt separate Abfragen für jedes aggregierte Ergebnisitem aus.

**Auswirkung**: Sehr stark bei Stores mit hohem Verkehr und vielen verfolgten Abfragen.

**Code-Position**: `search/services/analytics_service.py` - `get_click_through_rate()`-Methode

**Minderung**: Vermeiden Sie die Aufruf von CTR-Berechnungen in der Produktion. Dies ist hauptsächlich ein Admin-Analyse-Feature, das asynchron berechnet werden sollte, nicht während Kundenanfragen.

### Lageraggregation

**Was es ist**: `with_stock_totals()` berechnet die verfügbaren Mengen über alle Lager pro Produkt.

**Auswirkung**: Sehr teuer bei Katalogen >1.000 Produkte. Wird aufgerufen, wenn `in_stock`-Filter verwendet wird oder der Lagerstatus in der Vervollständigung angezeigt wird.

**Auslöser**: **Sucheinstellungen > Vervollständigung** - Option "Lagerstatus anzeigen"

**Empfehlung**: Aktivieren Sie den Lagerstatus in der Vervollständigung NIEMALS bei großen Katalogen. Fügt pro Anfrage 200-500ms hinzu.

### Varianten-Verknüpfungen

**Was es ist**: SKU-Suchen lösen eine JOIN-Operation auf der Variante-Tabelle aus, um Varianten-SKUs zu durchsuchen.

**Auswirkung**: 2-3x langsamer bei Produkten mit vielen Varianten (10+ Varianten pro Produkt).

**Minderung**: Verwendet `.distinct()` zur Vermeidung von Duplikaten, was Overhead hinzufügt. Notwendig für SKU-Funktionalität - deaktivieren Sie es nicht, es sei denn, SKUs werden nicht verwendet.

### Produktzahlen in der Vervollständigung

**Was es ist**: Ergebnisse der Vervollständigung von Kategorien/Marken zeigen Produktzahlen an ("Elektronik (234)")

**Auswirkung**: Jeder Inhaltstyp mit aktivierten Zahlen fügt 2 zusätzliche Abfragen hinzu. Abfragen beinhalten Verknüpfungen und Aggregationen.

**Auslöser**: **Sucheinstellungen > Vervollständigung** - "Produktzahlen anzeigen" für Kategorien/Marken

**Empfehlung**: Deaktivieren Sie Produktzahlen. Spart 2-4 Abfragen pro Vervollständigungsanfrage. Größte Optimierung für Vervollständigung.

### Dokumentindexierung

**Was es ist**: Textextraktion aus PDF/DOCX/XLSX-Dateien während Suchanfragen.

**Auswirkung**: Sehr teuer (Datei-I/O + Textextraktion). Synchron blockierende Operationen.

**Auslöser**: **Sucheinstellungen > Tief indexing** - "Dokumente indexieren"

**Empfehlung**: Fast nie lohnt sich der Leistungsverlust. AKTIVIEREN SIE ES NUR FÜR KLEINE DIGITALE PRODUKTKATALOGS (<500 Produkte) nach gründlichen Tests.

## Cache-Konfiguration

Caching ist die effektivste Leistungsoptimierung.

**Vervollständigungs-Cache** - Standard: 60s
- **Empfohlener Bereich**: 45-90s
- **Höherer TTL (90-120s)**: Bessere Leistung, wenn Lageränderungen selten sind
- **Niedrigerer TTL (30-45s)**: Aktuellerer Ergebnisse, wenn Sie Produkte stündlich hinzufügen

**Ergebnis-Cache** - Standard: 300s (5 Minuten)
- **Empfohlener Bereich**: 180-600s
- **Höherer TTL (600s/10min)**: Signifikante Leistungsverbesserung für statische Kataloge
- **Niedrigerer TTL (180s)**: Aktuellerer, wenn Produktinformationen häufig aktualisiert werden

**Optimierungsstrategie**: Wenn Suchen langsam sind, verdoppeln Sie die Cache-TTL, bevor Sie Features deaktivieren. Das Verdoppeln des Vervollständigungs-Cache von 60s auf 120s reduziert die Datenbanklast um die Hälfte.

## Vervollständigungs-Optimierungscheckliste

Wenden Sie diese Änderungen an den Vervollständigungs-Einstellungen an, um maximale Leistung zu erzielen:

**1. Erhöhen Sie Debounce auf 300-400ms**
- Ort: **Sucheinstellungen > Vervollständigung** - "Debounce Delay"
- Auswirkung: Reduziert API-Aufrufe, indem länger gewartet wird zwischen Tastatureingaben
- Kompromiss: Weniger reaktiv (für die meisten Benutzer unmerklich)

**2. Reduzieren Sie Max Results von 8 auf 5-6**
- Ort: **Sucheinstellungen > Vervollständigung** - "Max Results Per Type"
- Auswirkung: Kleinere Ergebnismengen = schnellere Abfragen und kleinere JSON-Payloads
- Kompromiss: Weniger Optionen angezeigt (normalerweise ausreichend)

**3. Deaktivieren Sie Produktzahlen (GRÖßTE GEWINN)**
- Ort: **Sucheinstellungen > Vervollständigung** - "Show Product Count" für Kategorien/Marken abwählen
- Auswirkung: Spart 2-4 Abfragen pro Vervollständigungsanfrage
- Kompromiss: Keine Produktzahlen im Dropdown (selten benötigt)

**4. Deaktivieren Sie Lagerstatus**
- Ort: **Sucheinstellungen > Vervollständigung** - "Show Stock Status" abwählen
- Auswirkung: Eliminiert teure Lageraggregation
- Kompromiss: Keine Lager-Emojis (nicht kritisch im Vervollständigungs-Kontext)

**5. Deaktivieren Sie Produktbeschreibungen**
- Ort: **Sucheinstellungen > Vervollständigung** - "Show Description" abwählen
- Auswirkung: Reduziert Textverarbeitung und Payloadgröße
- Kompromiss: Weniger Vorschau-Text (Produktname ist normalerweise ausreichend)

**6. Erhöhen Sie Cache-TTL auf 90s**
- Ort: **Sucheinstellungen > Caching** - "Autocomplete Cache TTL"
- Auswirkung: Mehr Anfragen werden aus dem Cache abgerufen
- Kompromiss: Ergebnisse können bis zu 90 Sekunden veraltet sein (für die meisten Geschäfte akzeptabel)

**Erwartete Verbesserung**: Die Anwendung aller 6 Optimierungen reduziert normalerweise die Antwortzeit der Vervollständigung um 50-70%.

## Tief indexing-Optimierung

Jede Option für tiefes Indexing fügt Overhead hinzu. Deaktivieren Sie sie basierend auf der Kataloggröße:

| Kataloggröße | Empfohlene Tief indexing-Optionen |
|--------------|---------------------------|
| **<1.000 Produkte** | Alle AN (minimaler Einfluss) |
| **1.000-10.000** | Behalten Sie SKUs, Attribute, benutzerdefinierte Felder AN; Deaktivieren Sie Bewertungen |
| **10.000-20.000** | Behalten Sie SKUs, Attribute AN; Deaktivieren Sie benutzerdefinierte Felder, Bewertungen |
| **20.000-50.000** | Behalten Sie SKUs AN nur; Deaktivieren Sie alles andere |
| **>50.000** | Behalten Sie SKUs AN; Überlegen Sie sich eine Migration zu Elasticsearch |

**Dokumentindexierung**: IMMER AUS, es sei denn, es ist kritisch (digitale Produkte mit durchsuchbaren Dokumenten UND <500 Produkte insgesamt).

## Optimierung von Inhaltstypen

Deaktivieren Sie nicht verwendete Inhaltstypen in **Sucheinstellungen > Inhaltstypen**:

- **Kein Blog?** Deaktivieren Sie "Blogbeiträge" - spart Abfragen
- **Keine Markenfilterung?** Deaktivieren Sie "Marken" - spart Abfragen
- **Nur-Shop-Store?** Deaktivieren Sie "Kategorien" und "Blogbeiträge"

Jeder deaktivierte Inhaltstyp entfernt Datenbankabfragen aus jeder Suche.

## Datenbankoptimierung

Spwig erstellt notwendige Indizes über Migrationen. Vertrauen Sie darauf - erstellen Sie keine zusätzlichen Indizes, ohne Profiling.

**PostgreSQL-Wartung** (wenn PostgreSQL verwendet wird):
- Führen Sie `VACUUM ANALYZE` wöchentlich, um die Statistiken des Abfrageplaners zu aktualisieren
- Große Kataloge profitieren von monatlichem `VACUUM FULL` (erfordert Ausfallzeit)

**Überwachen Sie die Datenbankabfragzeit**: Während der Entwicklung, identifizieren Sie langsame Abfragen mithilfe von Profiling-Tools. Die meisten Abfrageoptimierungen sind bereits implementiert:
- `.select_related('brand', 'category')` auf Produkten
- `.prefetch_related('images')` für Vorschaubilder
- `.distinct()` für Variantensuchen

## Leistungsverhalten von Fuzzy-Matching

Levenshtein-Abstand ist rechenintensiv (O(m*n) Komplexität):

**Schwellenwertoptimierung**:
- **Höherer Schwellenwert (0,85 vs 0,80)**: Schneller, aber weniger Tippfehler erfasst
- **Niedrigerer Schwellenwert (0,75 vs 0,80)**: Langsamer, aber verzeihender

**Max-Edits-Optimierung**:
- **Niedrigerer Max-Edits (1 vs 2)**: Schneller, aber mehr Tippfehler verpasst
- **Höherer Max-Edits (2 vs 3)**: Langsamer, aber mehr Tippfehler erfasst

**Bibliotheksleistung**: Spwig verwendet `rapidfuzz`, wenn verfügbar (10x schneller als reiner Python). Stellen Sie sicher, dass es installiert ist: `pip install rapidfuzz`

## Leistung von Synonymen und Umleitungen

**Synonym-Abfrageerweiterung**: Jedes Synonym fügt OR-Klauseln zur Suchabfrage hinzu. Begrenzen Sie auf maximal 10-20 Synonyme pro Begriff.

**Regex-Match-Typ**: Regex-Umleitungen sind langsamer als exakt/enthält/Beginnt mit. Vermeiden Sie komplexe Muster.

**Empfehlung**: Verwenden Sie so weit wie möglich einfache Match-Typen. Reservieren Sie Regex für Fälle, in denen andere Match-Typen nicht funktionieren.

## Optimierung für große Kataloge (>10.000 Produkte)

Spezifische Strategien für große Kataloge:

**1. Aggressives Caching**
- Vervollständigung: 90-120s TTL
- Ergebnisse: 600s (10min) TTL
- Akzeptieren Sie Veraltetheit für Leistung

**2. Minimales Tief indexing**
- Nur SKUs (Attribute, benutzerdefinierte Felder, Bewertungen deaktivieren)
- Testen Sie die Leistung mit/ohne Attribute

**3. Reduzierte Vervollständigungs-Ergebnisse**
- Maximal 5 Ergebnisse pro Typ (von 8 herabgesetzt)
- Reduziert Abfrage-Overhead

**4. Deaktivieren Sie Lagerstatus überall**
- In der Vervollständigung
- In den Suchergebnissen, wenn sie angezeigt werden

**5. Überlegen Sie sich Elasticsearch bei >50K Produkten**
- Datenbankinterne Suche ist bis zu ~50.000 Produkte geeignet
- Danach wird Elasticsearch empfohlen für:
  - Komplexe facettierte Suche
  - Hohe parallele Suchlast (>100 Suchen/sec)
  - Konsistent >500ms Antwortzeiten trotz Optimierung

## Leistungsverhalten bei mehreren Sprachen

JSONField JSONB-Indexierung (PostgreSQL) macht mehrsprachige Suche effizient:

- **1-3 Sprachen**: Minimaler Overhead (5-10ms)
- **5+ Sprachen**: Geringfügige Erhöhung der Abfragekomplexität (20-40ms)
- **10+ Sprachen**: Merkbarer Overhead (50-100ms)

Der Overhead steigt linear mit der Anzahl der Sprachen.

## Notfallleistungsverbesserungen

Wenn Suchen kritisch langsam sind (>2s Antwortzeiten), wenden Sie diese sofortigen Korrekturen in der Reihenfolge an:

**Sofort** (jetzt anwenden):
1. Deaktivieren Sie Dokumentindexierung
2. Deaktivieren Sie Produktzahlen in der Vervollständigung
3. Erhöhen Sie Cache-TTLs auf 120s Vervollständigung / 600s Ergebnisse

**Schnell** (innerhalb von 24 Stunden anwenden):
4. Deaktivieren Sie Lagerstatus in der Vervollständigung
5. Reduzieren Sie die maximale Anzahl der Vervollständigungs-Ergebnisse auf 5
6. Deaktivieren Sie Produktbeschreibungen in der Vervollständigung

**Mittel** (innerhalb einer Woche anwenden):
7. Deaktivieren Sie Bewertungsindexierung, wenn >20K Produkte vorhanden sind
8. Überprüfen und deaktivieren Sie nicht verwendete Inhaltstypen
9. Erhöhen Sie Debounce auf 400ms

**Erwartete Verbesserung**: Diese 9 Korrekturen reduzieren normalerweise die Antwortzeiten um 60-80% bei großen Katalogen.

## Tipps

- **Überwachen Sie Antwortzeiten wöchentlich** - Erkennen Sie frühzeitig Leistungsabbau
- **Cache-erhöhung ist die erste Optimierung** - Verdoppeln Sie die Cache-TTL, das ist der einfachste Gewinn
- **Produktzahlen in der Vervollständigung = teuer** - Größte Leistungskiller für Vervollständigung
- **Dokumentindexierung fast nie lohnt sich** - Leistungsverlust selten gerechtfertigt
- **Testen Sie eine Änderung zur Zeit** - Kausalität kann nicht erkannt werden, wenn Änderungen gleichzeitig vorgenommen werden
- **Benchmarken Sie mit realistischen Datenvolumina** - Testen Sie mit Katalogen der Produktionsgröße
- **Lageraggregation zerstört Leistung bei großen Katalogen** - Vermeiden Sie das Anzeigen von Lagerstatus in der Vervollständigung
- **Überlegen Sie sich Elasticsearch bei 50K+ Produkten** - Datenbankinterne Suche hat Grenzen

