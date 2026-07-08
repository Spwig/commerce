---
title: Sucheinstellungen verstehen
---

Die SearchSettings-Schnittstelle steuert das globale Suchverhalten in Ihrem Spwig-Shop. Diese einzelne Konfigurationsseite verwendet eine 8-Registerkarten-Schnittstelle, um Suchoptionen von der grundlegenden Aktivierung bis hin zu fortgeschrittenen Leistungsanpassungen zu organisieren. Änderungen hier gelten für alle Suchmaschinen, es sei denn, sie werden auf Ebene der Suchmaschine überschrieben.

Dieser Leitfaden führt Sie durch jedes Registerkarte und erklärt, was jede Einstellung tut und wann Sie sie anpassen sollten.

![Sucheinstellungen Allgemein-Registerkarte](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## Die 8-Registerkarten-Schnittstelle

SearchSettings ist ein Singleton-Modell - nur eine Konfigurationsdatensatz existiert (pk=1) für Ihren gesamten Shop. Die Schnittstelle ist in acht Registerkarten unterteilt:

| Registerkarte | Zweck |
|---------------|-------|
| **Allgemein** | Suche aktivieren/deaktivieren, grundlegende Parameter festlegen |
| **Autocomplete** | Verhalten des prädiktiven Suchdropdowns konfigurieren |
| **Inhaltstypen** | Wählen Sie die Typen von Inhalten, die durchsuchbar sind |
| **Tiefe der Indexierung** | Steuern Sie, welche Produktinformationen in die Suche einbezogen werden (Leistungsbeeinträchtigung) |
| **Unschärfe-Matching** | Toleranz für Tippfehler und Ähnlichkeitsgrenzwerte |
| **Gewichte** | Relevanzmultiplikatoren für die Ergebnisbewertung |
| **Caching** | Abwägung zwischen Antwortzeit und Aktualität |
| **Analysen** | Abfrageverfolgung und Datenschutz-Einstellungen |

Jede Registerkarte konzentriert sich auf einen bestimmten Aspekt der Suchkonfiguration.

## Allgemein-Registerkarte

Die Allgemein-Registerkarte enthält Kern-Einstellungen, die alle Suchen beeinflussen:

**Suche aktivieren** - Master-Schalter für das Suchsystem. Wenn diese deaktiviert ist, sind alle Suchfunktionen in Ihrem Shop inaktiv, einschließlich Autocomplete und der Suchergebnisseite.

**Mindestlänge der Abfrage** - Standard: 2 Zeichen. Suchen kürzer als dies werden abgelehnt. Die Einstellung auf 1 erlaubt Suchen mit einem Zeichen (z. B. "A"), erhöht aber die Serverlast.

**Ergebnisse pro Seite** - Standard: 20 Elemente. Steuert die Paginierung für Suchergebnisseiten. Höhere Werte (30-50) reduzieren Klicks auf die Paginierung, erhöhen aber die Ladezeit der Seite.

## Inhaltstypen-Registerkarte

![Einstellungen für Inhaltstypen](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Schalten Sie die Inhaltstypen ein, die in den Suchergebnissen angezeigt werden:

- **Produkte** - Physische, digitale und Abonnementprodukte
- **Kategorien** - Produktkategorien
- **Marken** - Produktmarken
- **Blogbeiträge** - Bloginhalte

**Leistungsmerkmal**: Weniger Inhaltstypen = schnellere Suchen. Jeder aktiviert Typ fügt zusätzliche Datenbankabfragen hinzu. Wenn Sie keinen Blog haben, deaktivieren Sie Blogbeiträge, um die Reaktionszeiten zu verbessern.

## Tiefe der Indexierung-Registerkarte

⚠️ **LEISTUNGSWARNUNG** - Diese Einstellungen haben erhebliche Leistungsfolgen.

![Einstellungen für Tiefe der Indexierung](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Die Tiefe der Indexierung steuert, welche produktbezogenen Daten in die Suche einbezogen werden:

**SKUs indizieren** - Standard: AN, geringer Einfluss. Fügt SKUs von Produkten und Varianten in die Suche ein. Wichtig für B2B-Shops, bei denen Kunden nach Produktcodes suchen.

**Attribute indizieren** - Standard: AN, mittlerer Einfluss. Fügt Produktattribute (Farbe, Größe, Material) in die Suche ein. Fügt eine JOIN-Operation zur Attributtabelle hinzu. Wichtig für Mode und konfigurierbare Produkte.

**Benutzerdefinierte Felder indizieren** - Standard: AN, mittlerer Einfluss. Fügt benutzerdefinierte Felder, die vom Händler definiert wurden, in die Suchergebnisse ein. Erfordert JSONField-Traversal.

**Bewertungen indizieren** - Standard: AN, mittlerer-hoher Einfluss ⚠️

Die Indizierung von Dokumenten extrahiert Text aus PDF-, DOCX- und XLSX-Dateien, die an digitale Produkte angehängt sind. Dieses Feature:

- Erfordert eine sehr teure erste Indizierung
- Fügt erhebliche Abfrageüberhead auf jede Suche hinzu
- Kann zu Timeout bei großen Dateien führen
- **Sollte nur für digitale Produktshops mit durchsuchbaren Dokumenten aktiviert werden**
- **Aktivieren Sie es nie willkürlich** - testen Sie die Leistungsfolgen gründlich

## Unschärfe-Matching-Registerkarte

![Einstellungen für Unschärfe-Matching](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

Unschärfe-Matching verwendet den Levenshtein-Abstand, um Tippfehler zu behandeln:

**Unschärfe-Matching aktivieren** - Ermöglicht Suchen, die ähnliche Begriffe abgleichen (z. B. "Laptop" passt zu "Labtop")

**Ähnlichkeitsgrenzwert** - Standard: 0,80 (80 % Ähnlichkeit). Bereich: 0,0-1,0. Höhere Werte erfordern genauere Übereinstimmungen und laufen schneller. Niedrigere Werte erfassen mehr Tippfehler, können aber irrelevanten Ergebnissen führen.

**Maximaler Edit-Abstand** - Standard: 2 Zeichenänderungen. Maximale Anzahl von Einfügungen, Löschen oder Substitutionen, die erlaubt sind. Niedrigere Werte (1) verbessern die Leistung, erfassen aber weniger Tippfehler.

## Gewichte-Registerkarte

Gewichte steuern die Relevanzbewertung - wie Ergebnisse rangiert werden. Die Gewichte-Registerkarte zeigt die Standardmultiplikatoren für jedes durchsuchbaren Feld an:

- weight_name: 1,50 (Produktname ist am wichtigsten)
- weight_sku: 1,20
- weight_description: 0,80
- weight_categories: 0,80
- weight_attributes: 0,70
- weight_brands: 0,70
- weight_blog_posts: 0,60
- weight_reviews: 0,50

Diese Standardwerte funktionieren gut für die meisten E-Commerce-Shops. Für detaillierte Informationen zur Anpassung von Gewichten und zum Verständnis ihrer Auswirkungen, siehe das Thema [Relevanz-Gewichte und Tiefe der Indexierung](/en/admin/help/relevance-weights-deep-indexing/).

## Caching-Registerkarte

![Caching-Einstellungen](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Caching verbessert die Suchleistung erheblich, indem es kürzlich Ergebnisse speichert:

**Autocomplete-Cache-TTL** - Standard: 60 Sekunden. Wie lange Autocomplete-Ergebnisse im Cache gespeichert werden. Kürzere TTL (30-45s) = frischere Ergebnisse, aber mehr Datenbankabfragen. Längere TTL (90-120s) = schneller, aber möglicherweise veraltete Ergebnisse.

**Ergebnis-Cache-TTL** - Standard: 300 Sekunden (5 Minuten). Dauer des Caches für die vollständige Suchergebnisseite. Längere TTL verbessert die Leistung erheblich, verzögert aber die Sichtbarkeit neuer Produkte.

**Abwägungen**: Caching ist die effektivste Leistungsoptimierung. Wenn Suchen langsam sind, erhöhen Sie diese Werte, bevor Sie Funktionen deaktivieren.

## Analytics-Registerkarte

![Analytics-Einstellungen](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Suchabfragen verfolgen** - Aktiviert das Suchanalytik-Dashboard. Protokolliert den Abfragetext, die Ergebnisanzahl, die Antwortzeit und den Zeitstempel.

**Nutzereinformationen verfolgen** - Verknüpft Suchen mit angemeldeten Nutzern. Deaktivieren Sie dies für die Einhaltung von Datenschutzvorschriften (GDPR, CCPA).

**Sitzungsinformationen verfolgen** - Verwendet Sitzungsid's, um anonyme Nutzersuchen zu verfolgen. Nützlich für die Identifizierung von Suchmustern ohne personenbezogene Daten.

## Singleton-Muster

SearchSettings verwendet ein Singleton-Muster - nur ein Einstellungsdatensatz existiert in Ihrer Datenbank (pk=1). Wenn Sie sich in der Admin-UI zu Search Settings navigieren, bearbeiten Sie immer den gleichen Datensatz.

Es gibt keine "Hinzufügen" oder "Löschen"-Option - nur "Ändern". Alle Suchmaschinen erben diese Einstellungen, es sei denn, sie geben pro-Suchmaschine-Überschreibungen an (selten).

## Tipps

- **Halten Sie die Standardwerte, es sei denn, Sie haben einen spezifischen Bedarf** - Die Standard-Einstellungen sind für typische E-Commerce-Shops optimiert
- **Aktivieren Sie die Dokumentindizierung nie willkürlich** - Nur für digitale Produktshops mit durchsuchbaren Dokumenten, und testen Sie die Leistungsfolgen zuerst
- **Überwachen Sie die Antwortzeiten in den Analysen** - Ziel: <200ms für Autocomplete, <500ms für vollständige Suche
- **Erhöhen Sie die Cache-TTL, wenn die Leistung langsam ist** - Caching ist der einfachste Leistungsverbesserung
- **Überprüfen Sie wöchentlich Abfragen mit Null-Ergebnissen** - Sie zeigen fehlende Produkte oder benötigte Synonyme
- **Deaktivieren Sie nicht verwendete Inhaltstypen** - Wenn Sie keinen Blog haben, schalten Sie Blogbeiträge aus, um Suchen zu beschleunigen

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bilddateipfade, Codeblöcke und technischen Begriffe genau wie in den Erhaltungsvorgaben an.