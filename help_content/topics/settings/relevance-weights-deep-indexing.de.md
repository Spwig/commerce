---
title: Relevanzgewichte und Tiefenindexierung
---

Relevanzgewichte und Tiefenindexierung steuern, wie Suchergebnisse bewertet werden und welche Produktinformationen in die Suche einbezogen werden. Gewichte sind Multiplikatoren der Wichtigkeit - ein Gewicht von 2,0 bedeutet, dass Übereinstimmungen in diesem Feld doppelt so wichtig sind wie ein Gewicht von 1,0. Tiefenindexierung bestimmt, ob die Suche über grundlegende Produktbezeichnungen hinaus in SKUs, Attribute, Bewertungen und sogar Dokumentinhalte sucht. Dieser Leitfaden erläutert beide Systeme, wann Sie sie anpassen sollten und welche kritischen Leistungsfolgen dies hat.

Die Standardwerte funktionieren für die meisten E-Commerce-Shops gut. Ändern Sie sie nur, wenn Sie spezifische Sortier- oder Indexierungsanforderungen haben.

![Weights Tab](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Gewichtung verstehen

Gewichte sind Multiplikatoren (Skala 0,0-2,0), die angewendet werden, wenn Textübereinstimmungen in verschiedenen Feldern gefunden werden. Höhere Gewichte bedeuten, dass Übereinstimmungen in diesem Feld in den Suchergebnissen höher rangieren.

**Beispiel**: Wenn ein Produkt sowohl im Namen (Gewicht 1,50) als auch in der Beschreibung (Gewicht 0,80) den Begriff "laptop" enthält:
- Übereinstimmung im Namen trägt 1,50 zur Relevanzbewertung bei
- Übereinstimmung in der Beschreibung trägt 0,80 bei
- Die kombinierte Bewertung bestimmt die Rangfolge gegenüber anderen Produkten

Gewichte ermöglichen es Ihnen, bei der Sortierung von Suchergebnissen bestimmte Felder gegenüber anderen zu priorisieren.

## Gewichtskategorien und Standardwerte

Navigieren Sie zu **Sucheinstellungen > Gewichtung** um alle Gewichtungseinstellungen anzuzeigen:

| Feld | Standardgewicht | Begründung |
|-------|---------------|-----------|
| **weight_name** | 1,50 | Produktbezeichnungen sind am wichtigsten - Kunden erwarten, dass exakte Bezeichnungen in den Suchergebnissen oben stehen |
| **weight_sku** | 1,20 | SKUs sind spezifische Identifikatoren - wichtig für B2B und zurückkehrende Kunden |
| **weight_description** | 0,80 | Beschreibungen liefern Kontext, sind aber weniger wichtig als exakte Bezeichnungen |
| **weight_categories** | 0,80 | Kategorienübereinstimmungen sind für das Durchsuchen nützlich, aber nicht so spezifisch wie Name/Artikelnummer |
| **weight_attributes** | 0,70 | Farbe, Größe, Materialsuche - nützlich, aber unterstützende Informationen |
| **weight_brands** | 0,70 | Markenfilterung ist wichtig, aber für die meisten Shops ist sie nicht der primäre Suchkriterium |
| **weight_blog_posts** | 0,60 | Bloginhalte sind bei Suchvorgängen mit Fokus auf E-Commerce weniger wichtig (niedrigste Priorität) |
| **weight_reviews** | 0,50 | Benutzererzeugte Inhalte sind am wenigsten kontrolliert - niedrigstes Gewicht |

Diese Standardwerte setzen voraus, dass ein typischer E-Commerce-Shop vorliegt, bei dem die Produktentdeckung das primäre Suchziel ist.

## Wann Gewichte anpassen

Ändern Sie Gewichte, wenn die Prioritäten Ihres Shops von den typischen E-Commerce-Mustern abweichen:

**SKU-orientierte Shops (B2B, Großhandel)** - Erhöhen Sie `weight_sku` auf 1,8-2,0, damit Suchvorgänge nach Produktcodes die Ergebnisse dominieren. B2B-Kunden suchen oft nach exakten SKUs.

**Markenorientierte Shops** - Erhöhen Sie `weight_brands` auf 1,2-1,5, wenn Kunden hauptsächlich nach Marken einkaufen (Designerkleidung, Luxuswaren).

**Inhaltsschwerpunkte Shops** - Erhöhen Sie `weight_blog_posts` auf 0,9-1,2, wenn Sie ein Inhaltshersteller oder Bildungshändler sind, bei dem Blogbeiträge genauso wichtig sind wie Produkte.

**Attribut-orientierte Shops (Mode)** - Erhöhen Sie `weight_attributes` auf 1,0-1,2, wenn Kunden häufig nach Farbe, Größe, Stilattributen suchen.

## Beispiele für Gewichtsanpassungen

| Shop-Typ | Empfohlene Anpassungen |
|-----------|------------------------|
| **B2B-Großhandel** | weight_sku: 2,0, weight_name: 1,3, weight_description: 0,6 - Produktcodes priorisieren |
| **Modeboutique** | weight_attributes: 1,2, weight_brands: 1,2, weight_name: 1,4 - Farbe/Stil/Marken sind wichtig |
| **Inhaltshersteller** | weight_blog_posts: 1,2, weight_name: 1,3, weight_reviews: 0,7 - Inhalt ist genauso wichtig wie Produkte |
| **Allgemeiner E-Commerce** | Standardwerte verwenden - Ausgewogen für typische Online-Shops |

Ändern Sie ein Gewicht zur Zeit und testen Sie es, bevor Sie weitere Änderungen vornehmen.

## Übersicht über Tiefenindexierung

⚠️ **LEISTUNGSWARNUNG** - Jede Option der Tiefenindexierung erhöht die Abfragekomplexität und die Auslastung.

Tiefenindexierung erweitert die Suche über die grundlegenden Produktbezeichnungen und -beschreibungen hinaus in zusätzliche Daten:

![Tiefenindexierungstabelle](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Navigieren Sie zu **Sucheinstellungen > Tiefenindexierung** um sie zu konfigurieren.

## SKUs indexieren

**Standard**: AN, **Leistungsbeeinträchtigung**: Gering

Enthält Produkt- und Varianten-SKUs im Suchindex. Löst eine Variante JOIN (geringe Kosten) aus.

**Wann AN lassen**: Wichtig für B2B-Shops, bei denen Kunden Produktcodes kennen. Auch nützlich für zurückkehrende Kunden, die SKU aus früheren Bestellungen kennen.

**Wann deaktivieren**: Nie, es sei denn, Sie haben tatsächlich keine SKUs zugewiesen. Die Leistungsbeeinträchtigung ist vernachlässigbar.

## Attribute indexieren

**Standard**: AN, **Leistungsbeeinträchtigung**: Mittel

Enthält Produktattribute (Farbe, Größe, Material, benutzerdefinierte Attribute) im Suchindex. Verknüpft mit der Attribute-Tabelle.

**Wann AN lassen**: Wichtig für Mode, konfigurierbare Produkte oder für jeden Shop, bei dem Kunden nach Produktmerkmalen suchen ("roter Rock", "großer T-Shirt").

**Wann deaktivieren**: Kataloge mit mehr als 20.000 Produkten und vielen Attributen pro Produkt können eine Overhead von 50-100 ms haben. Deaktivieren Sie nur, wenn die Leistung kritisch ist und Kunden nicht nach Attributen suchen.

## Benutzerdefinierte Felder indexieren

**Standard**: AN, **Leistungsbeeinträchtigung**: Mittel

Enthält benutzerdefinierte Felder aus JSONField im Suchindex. Erfordert JSONField-Traversal.

**Wann AN lassen**: Wenn Sie benutzerdefinierte Felder für suchbare Produktinformationen verwenden (Garantieinformationen, Spezifikationen, Kompatibilitätsdetails).

**Wann deaktivieren**: Wenn Sie keine benutzerdefinierten Felder verwenden oder benutzerdefinierte Felder nicht suchbare Daten enthalten (interne Notizen, Buchhaltungscodes). Deaktivieren Sie, um JSONField-Verarbeitungsauslastung zu sparen.

## Bewertungen indexieren

**Standard**: AN, **Leistungsbeeinträchtigung**: Mittel-Hoch

Enthält genehmigte Bewertungstitel und Kommentare in der Suche. Verknüpft mit der Bewertungstabelle und fügt Textsuche-Auslastung hinzu.

**Wann AN lassen**: Bei Katalogen mit vielen Bewertungen, bei denen Kunden nach Produkten basierend auf Bewertungsinhalten suchen ("wasserdichter Laptopbeutel" könnte in Bewertungstexten auftauchen).

**Wann deaktivieren**: Bei Katalogen mit mehr als 20.000 Produkten oder bei Shops mit vielen Bewertungen pro Produkt. Fügt 100-200 ms Overhead bei großen Katalogen hinzu.

## Dokumente indexieren

**Standard**: AUS, **Leistungsbeeinträchtigung**: SEHR HOH 🚨

**NIEMALS LAUFGELASSEN** - Teuerster Suchfunktion.

Dokumentindexierung extrahiert Text aus PDF-, DOCX- und XLSX-Dateien, die an digitale Produkte angehängt sind, und macht den Inhalt der Dateien suchbar.

**Technische Details**:
- Verwendet Bibliotheken PyPDF2, python-docx und openpyxl
- Synchrones Datei-I/O und Textextraktion bei der Suche
- Verfolgt Dateien über MD5-Prüfsumme (nur bei Änderungen der Datei wird ein Neuanlage durchgeführt)
- Potenzielle Timeout bei großen Dateien (>10 MB PDFs)

**Leistungsbeeinträchtigung**:
- Sehr teure Anfangsindexierung (Minuten bis Stunden für große Bibliotheken)
- Signifikante Abfrage-Auslastung (100-500 ms zusätzliche Latenz)
- Speicherintensiv bei großen Dokumenten

**Nur aktivieren, wenn**:
- Sie digitale Produkte mit suchbaren Dokumenten verkaufen (E-Books, Berichte, Handbücher)
- Katalog ist klein (<500 digitale Produkte)
- Server hat ausreichende Ressourcen
- Sie haben den Einfluss gründlich getestet

**Für digitale Produktshops**: Überlegen Sie, ob Kunden wirklich den Inhalt von Dokumenten suchen müssen, oder ob die Suche nach Produktbezeichnungen und -beschreibungen ausreicht.

## Tabelle zur Leistungsbeeinträchtigung

| Funktion | Standard | Auswirkung | Verwenden, wenn |
|---------|---------|--------|----------|
| SKUs indexieren | AN | Gering | Immer (wichtig für B2B) |
| Attribute indexieren | AN | Mittel | Konfigurierbare Produkte |
| Benutzerdefinierte Felder indexieren | AN | Mittel | Benutzerdefinierte Felder verwenden |
| Bewertungen indexieren | AN | Mittel-Hoch | Bewertungsschwerpunkt-Shop |
| Dokumente indexieren | AUS | Sehr hoch | Nur für digitale Produkte (zuerst testen) |

Die Auswirkungen beziehen sich auf typische Kataloge. Bei großen Katalogen (>50.000 Produkte) treten proportionell höhere Auslastungen auf.

## Testen von Gewichtsänderungen

Wenn Sie Gewichte anpassen, befolgen Sie diesen Testablauf:

1. **Ändern Sie ein Gewicht zur Zeit** - Ändern Sie nicht mehrere Gewichte gleichzeitig; Sie werden nicht wissen, welche Änderung die Ergebnisse verursacht hat
2. **Kleine Schritte** - Ändern Sie Gewichte um ±0,2 (z. B. 1,0 → 1,2, nicht 1,0 → 1,8)
3. **Testen Sie mit echten Abfragen** - Verwenden Sie tatsächliche Suchbegriffe aus der Analyse, nicht zufällige Tests
4. **Überwachen Sie die Analyse** - Vergleichen Sie die Relevanz der Ergebnisse vor und nach der Verwendung der wichtigsten Abfragen
5. **Wartezeit von 1-2 Wochen** - Geben Sie Kunden Zeit, sich mit den neuen Rangfolgen zu beschäftigen
6. **Messung der Klickdurchschnittsrate** - Klicken Kunden auf die Ergebnisse mehr oder weniger als zuvor?

## Leistungs- vs. Genauigkeitskompromisse

Mehr Indexierung = bessere Suchergebnisse, aber langsamerer Leistung:

**Szenario: Kleiner Katalog (<1.000 Produkte)**
- Aktivieren Sie alle Indexierungsoptionen (SKUs, Attribute, benutzerdefinierte Felder, Bewertungen)
- Leistungsbeeinträchtigung ist minimal
- Umfassende Suchfunktionen

**Szenario: Mittlerer Katalog (1.000-10.000 Produkte)**
- Behalten Sie SKUs, Attribute, benutzerdefinierte Felder AN
- Überlegen Sie, Bewertungen zu deaktivieren, wenn der Durchschnitt mehr als 10 Bewertungen pro Produkt beträgt
- Überwachen Sie die Antwortzeiten

**Szenario: Großer Katalog (>10.000 Produkte)**
- Behalten Sie SKUs AN (geringe Auswirkung)
- Deaktivieren Sie Bewertungssuche (hohe Auswirkung)
- Deaktivieren Sie benutzerdefinierte Felder, wenn sie nicht genutzt werden
- AKTIVIEREN SIE NIEMALS Dokumentindexierung
- Überlegen Sie Elasticsearch bei mehr als 50.000 Produkten

Gleichgewicht basierend auf der Größe Ihres Katalogs und den Serverressourcen.

## Gewichtsoverrides für spezifische Suchmaschinen

Wenn Sie eine Suchmaschine über den Assistenten erstellen (Schritt 3), können Sie die globalen Gewichte für diese spezifische Suchmaschine überschreiben.

**Verwendungsfall**: Suchmaschine mit Fokus auf Blog
- Erstellen Sie eine "blog"-Suchmaschine
- Überschreiben Sie `weight_blog_posts` auf 1,5 (gegenüber globalem 0,60)
- Bloginhalte rangieren jetzt höher in Blog-Suchmaschinen

Die meisten Suchmaschinen sollten KEINE Gewichte überschreiben - lassen Sie sie leer, um globale Einstellungen zu erben.

## Tipps

- **Aktivieren Sie niemals Dokumentindexierung, es sei denn, es ist absolut notwendig** - Höchste Leistungsbeeinträchtigung aller Suchfunktionen
- **B2B-Shops: Erhöhen Sie weight_sku auf 2,0** - Produktcodes sind die primäre Suchmethode
- **Testen Sie Gewichtsänderungen während der Nebenzeit** - Beobachten Sie die Leistungsbeeinträchtigung vor dem Hochzeit
- **Überwachen Sie Antwortzeiten nach Aktivierung der Indexierung** - Prüfen Sie das Analysetool für Verlangsamungen
- **Deaktivieren Sie Bewertungssuche bei Katalogen >20K Produkte** - Signifikante Leistungsbeeinträchtigung
- **Ändern Sie ein Gewicht zur Zeit für Tests** - Mit gleichzeitigen Änderungen können Sie keine Ursache/Wirkung bestimmen
- **Dokumentextraktion erfordert PyPDF2/docx/openpyxl** - Stellen Sie sicher, dass diese Bibliotheken installiert sind, bevor Sie Dokumentindexierung aktivieren

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bilddateipfade, Codeblöcke und technischen Begriffe genau wie in den Erhaltungsvorschriften gezeigt auf.