---
title: Suchanalytik-Dashboard
---

Das Suchanalytik-Dashboard verfolgt jede Suchanfrage auf Ihrem Store und gibt Einblicke in das, wonach Kunden suchen, welche Suchanfragen erfolgreich oder nicht sind und wie schnell Ihr Suchsystem reagiert. Nutzen Sie diese Daten, um beliebte Produkte zu identifizieren, fehlende Lagerbestände zu entdecken, Synonyme zu erstellen und die Suchleistung zu optimieren.

Die Analyse muss in **Sucheinstellungen > Analytik-Registerkarte** aktiviert werden, damit Daten angezeigt werden.

![Analytics Dashboard](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Dashboard-Übersicht

Navigieren Sie zu **Suche > Suchanalytik**, um das Dashboard zu öffnen. Die Seite zeigt:

**Statistik-Karten** - Schnelle Metriken für heute und die vergangene Woche:
- Gesamt-Suchanfragen heute
- Gesamt-Suchanfragen diese Woche
- Suchanfragen mit Null-Ergebnissen (Suchanfragen, die keine Produkte zurückgeben)
- Durchschnittliche Reaktionszeit in Millisekunden

**Top-Abfragen-Tabelle** - Häufigste Suchbegriffe mit Ergebniszahlen

**Null-Ergebnis-Abfragen** - Suchanfragen, die keine Ergebnisse zurückgaben (kritisch für Verbesserungen)

**Abfragen-Liste** - Alle individuellen Suchaufzeichnungen mit Filtern

## Heutige Statistiken

**Gesamt-Suchanfragen heute** - Anzahl aller Suchanfragen seit Mitternacht in der Zeitzone Ihres Stores. Enthält sowohl Autocomplete- als auch vollständige Suchseitenanfragen.

**Eindeutige Abfragen heute** - Anzahl der unterschiedlichen Suchbegriffe, die heute genutzt wurden. Wenn 5 Kunden alle nach "Laptop" suchen, zählt das als 1 eindeutige Abfrage, obwohl es 5 Gesamt-Suchanfragen gibt.

**Null-Ergebnisse heute** - Suchanfragen heute, die keine Produkte zurückgaben. Hohe Zahlen von Null-Ergebnissen deuten auf fehlende Produkte oder eine unzureichende Synonymabdeckung hin.

Die Daten werden in Echtzeit aktualisiert, sobald Suchanfragen stattfinden.

## Wöchentliche Statistiken

**Wöchentlicher Gesamtbestand** - Gesamtzahl der Suchanfragen in den letzten 7 Tagen

**Einzigartige Abfragen** - Unterschiedliche Suchbegriffe, die diese Woche genutzt wurden

**Wöchentliche Wachstumsrate** - Prozentsatzänderung im Vergleich zur vorherigen Woche (wenn angezeigt)

Nutzen Sie die wöchentlichen Daten, um Trends zu erkennen: Ein Anstieg der Suchvolumina korreliert oft mit einem Anstieg des Traffics oder Marketingkampagnen.

## Durchschnittliche Reaktionszeit

⚠️ **LEISTUNGSÜBERWACHUNG**

Durchschnittliche Zeit (in Millisekunden), um Suchanfragen auszuführen. Zielreaktionszeiten:

| Abfragetyp | Ziel | Warnschwellenwert |
|------------|--------|-------------------|
| Autocomplete | < 200ms | > 300ms konsistent |
| Vollständige Suche | < 500ms | > 800ms konsistent |

Wenn die durchschnittliche Reaktionszeit die Warnschwellenwerte überschreitet:
1. Prüfen Sie **Sucheinstellungen > Caching-Registerkarte** - erhöhen Sie die Cache-TTLs
2. Überprüfen Sie **Tiefe Indexierung** - deaktivieren Sie kostspielige Funktionen (Dokumentindexierung, Bewertungsindexierung bei großen Katalogen)
3. Siehe [Suchleistungs-Optimierung](/en/admin/help/search-performance-optimization/)-Leitfaden

## Top-Abfragen

Die Tabelle der Top-Abfragen zeigt die häufigsten Suchbegriffe:

**Nutzen Sie diese Daten, um**:
- **Beliebte Produkte hervorzuheben** - Wenn "drahtlose Kopfhörer" eine Top-Suche ist, heben Sie diese Produkte auf Ihrer Startseite hervor
- **Lagerentscheidungen** - Ein hoher Suchvolumen für eine Kategorie deutet auf Nachfrage hin
- **Trends erkennen** - Saisonale Suchen zeigen, was derzeit beliebt ist
- **Inhaltserstellung** - Schreiben Sie Blogbeiträge oder Leitfäden zu häufig gesuchten Themen

Überprüfen Sie die Top-Abfragen monatlich, um Ihre Merchandising-Strategie mit den Interessen der Kunden abzugleichen.

## Null-Ergebnis-Abfragen

**KRITISCH FÜR VERBESSERUNGEN** - Null-Ergebnis-Abfragen sind ein Goldgrube für die Optimierung Ihres Stores.

Null-Ergebnis-Abfragen treten aus drei Hauptgründen auf:

### 1. Fehlende Produkte

Kunden suchen nach Produkten, die Sie nicht verkaufen.

**Beispiel**: Wiederholte Suchen nach "Yogamatten", aber Sie verkaufen nur Fitnessausrüstung, nicht Yoga-Zubehör.

**Aktion**: Überlegen Sie, diese Produkte Ihrem Katalog hinzuzufügen, wenn die Suchen häufig sind.

### 2. Fehlende Synonyme

Kunden verwenden Begriffe, die nicht mit Ihren Produktbeschreibungen übereinstimmen.

**Beispiel**: Kunden suchen nach "Laptop", aber Ihre Produkte sagen alle "Notebook-Computer".

**Aktion**: Erstellen Sie Synonyme, die Kundenbegriffe auf Ihre Produktbezeichnung abbilden. Siehe [Verwaltung von Synonymen und Umleitungen](/en/admin/help/managing-synonyms-redirects/).

### 3. Schlechte Fuzzy-Matching

Tippfehler oder Rechtschreibfehler stimmen nicht überein, auch wenn die Fuzzy-Suche aktiviert ist.

**Beispiel**: Suche nach "accomodate" findet keine Produkte mit "accommodate".

**Aktion**:
- Verringern Sie den Ähnlichkeits-Schwellenwert in **Sucheinstellungen > Fuzzy-Matching-Registerkarte** (von 0,80 auf 0,75)
- Fügen Sie einseitige Synonyme für häufige Rechtschreibfehler hinzu

**Wöchentliche Arbeitsabläufe**:
1. Überprüfen Sie die Null-Ergebnis-Abfragen jeden Montag
2. Kategorisieren Sie: Fehlende Produkte, fehlende Synonyme oder Rechtschreibfehler
3. Fügen Sie Synonyme für häufig gesuchte Begriffe hinzu
4. Notieren Sie Produktlücken für die Lagerplanung

## Abfrage-Details

Klicken Sie auf eine beliebige Abfrage in der Liste, um die vollständigen Details anzuzeigen:

**Verfolgte Felder**:
- **Abfragetext** - Was der Kunde gesucht hat
- **Zeitstempel** - Wann die Suche stattfand
- **Ergebnisanzahl** - Wie viele Ergebnisse zurückgegeben wurden
- **Reaktionszeit** - Millisekunden zur Ausführung (Leistungsüberwachung)
- **Benutzer** - Angemeldeter Kunde (wenn die Benutzerverfolgung aktiviert ist)
- **Sitzungsid** - Anonyme Sitzungsid
- **Sprache** - Store-Sprache während der Suche
- **Engine** - Welcher Suchmaschine die Abfrage verarbeitet wurde

## Filtern und Suche

Verwenden Sie Filter, um bestimmte Segmente zu analysieren:

**Datumshierarchie** - Filtern Sie nach Datum, Monat oder Jahr

**Sprachfilter** - Sehen Sie sich Suchen nach Sprache an (wichtig für mehrsprachige Stores)

**Engine-Filter** - Vergleichen Sie Suchverhalten über verschiedene Engine

**Null-Ergebnis-Schalter** - Zeigen Sie nur Abfragen an, die keine Ergebnisse zurückgaben

**Suchfeld** - Finden Sie spezifischen Abfragetext

## Datenexportieren

Klicken Sie auf **Exportieren**, um die Abfragendaten als CSV herunterzuladen, um eine tiefere Analyse in Excel oder Daten-Tools durchzuführen.

**CSV enthält**:
- Alle Abfragetexte
- Zeitstempel
- Ergebnisanzahlen
- Reaktionszeiten
- Sprach- und Engine-Daten

Verwenden Sie Exporte für:
- Trendanalyse im Laufe der Zeit
- Identifizierung saisonaler Suchmuster
- Leistungsüberprüfung
- Präsentation an Stakeholder

## Datenschutzaspekte

Suchanalytik-Tracking respektiert den Datenschutz:

**Benutzertracking** (optional) - Verknüpft Suchen mit angemeldeten Kundenkonten. Deaktivieren Sie dies für GDPR/CCPA-Konformität in **Sucheinstellungen > Analytik-Registerkarte**.

**Sitzungstracking** (Standard) - Verwendet anonyme Sitzungsid, um Suchmuster zu verfolgen, ohne Kunden zu identifizieren. Datenschutzfreundlich.

**Datenhaltung** - Suchanfragen bleiben unendlich im Datenbank. Implementieren Sie eine benutzerdefinierte Datenhaltungspolitik, wenn dies für die Konformität erforderlich ist.

## Nutzung von Analytik zur Verbesserung der Suche

Handlungsfähige Einblicke aus der Suchanalytik:

**Wöchentliche Aufgaben**:
- Überprüfen Sie Null-Ergebnisse und fügen Sie Synonyme für häufige Begriffe hinzu
- Überwachen Sie Reaktionszeiten und optimieren Sie, wenn diese konsistent langsam sind
- Identifizieren Sie Top-Suchen und stellen Sie sicher, dass diese Produkte gut bestückt sind

**Monatliche Aufgaben**:
- Analysieren Sie Top-Abfragen, um die Produktwahl zu beeinflussen
- Exportieren Sie Daten, um saisonale Trends zu identifizieren
- Überprüfen Sie sprachspezifische Suchmuster
- Verfolgen Sie Umleitungs-Hits, um Navigationsschnellwege zu optimieren

**Quartalsaufgaben**:
- Prüfen Sie die Effektivität von Synonymen (haben sich die Null-Ergebnisse verringert?)
- Vergleichen Sie das Wachstum der Suchvolumina mit dem Gesamttraffic
- Durchführen von A/B-Tests für Gewichtungsänderungen und messen Sie die Relevanz der Ergebnisse
- Überprüfen Sie, ob neue Produktkategorien basierend auf der Suchnachfrage hinzugefügt werden sollten

## Tipps

- **Null-Ergebnis-Abfragen sind Goldgruben für Verbesserungen** - Sie sagen Ihnen direkt, wonach Kunden suchen, was Sie nicht anbieten
- **Überprüfen Sie die Analytik am Montagmorgen** - Starten Sie Ihre Woche mit der Optimierung basierend auf den Daten der vorherigen Woche
- **Reaktionszeit >300ms konsistent = untersuchen** - Prüfen Sie zunächst die Caching-Einstellungen, dann die Tiefe-Indexierungsfunktionen
- **Exportieren Sie CSV für Trendanalyse** - Tabellenkalkulationsanalysen zeigen Muster, die im Admin-Interface nicht offensichtlich sind
- **Erstellen Sie Synonyme, bevor Sie Produkte hinzufügen** - Wenn Kunden nach "Tablet-Beuteln" suchen, aber Sie sie "Schutzbeutel" nennen, fügen Sie Synonyme zuerst hinzu
- **Verfolgen Sie saisonale Suchmuster** - "Winterstiefel" im Oktober, "Badeanzüge" im März - lagern Sie entsprechend