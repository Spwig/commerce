---
title: Autocomplete konfigurieren
---

Autocomplete, auch prädiktive Suche oder Suche-while-typen genannt, zeigt Ergebnisse an, während Kunden ihre Abfragen eingeben. Dies verbessert erheblich die Benutzererfahrung, indem Kunden schneller Produkte finden und Null-Ergebnis-Suchen reduziert werden. Dieser Leitfaden erklärt, wie Sie das Verhalten von Autocomplete, Anzeigestellungen und Leistungsabwägungen konfigurieren.

Autocomplete ist standardmäßig mit sinnvollen Einstellungen aktiviert. Ändern Sie diese nur, wenn Sie spezifische Leistungsprobleme oder Anzeigepräferenzen haben.

![Autocomplete Einstellungen](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Autocomplete aktivieren

Navigieren Sie zu **Suche > Sucheinstellungen** und klicken Sie auf den Reiter **Autocomplete**.

**Autocomplete aktivieren** - Master-Schalter für die prädiktive Suche. Wenn aktiviert, zeigen Sucheingaben ein Dropdown mit Ergebnissen an, während Kunden tippen.

**Maximale Ergebnisse pro Typ** - Standard: 8 Elemente. Wie viele Ergebnisse pro Inhaltstyp (Produkte, Kategorien, Marken, Blogbeiträge) angezeigt werden sollen. Niedrigere Werte (5-6) reduzieren die Größe der API-Payload und beschleunigen die Darstellung. Höhere Werte (10-12) bieten Kunden mehr Optionen, verlangsamen aber die Antwort.

## Debounce-Zeit

⚠️ **LEISTUNGSWARNUNG** - Die Debounce-Zeit beeinflusst erheblich die Serverlast.

**Debounce-Verzögerung** - Standard: 300ms. Wie lange nach dem letzten Tastendruck gewartet werden soll, bevor eine Autocomplete-Anfrage ausgelöst wird.

Diese Einstellung balanciert Reaktivität mit Serverlast:

| Verzögerung | Benutzererfahrung | Server-Auswirkung |
|-------------|------------------|------------------|
| **100ms** | Sehr reaktiv | 3x mehr API-Aufrufe als bei 300ms - hohe Last |
| **200ms** | Reaktiv | 1,5x mehr API-Aufrufe als bei 300ms |
| **300ms** | Gutes Gleichgewicht (empfohlen) | Baseline |
| **400ms** | Leicht verlangsamt | Weniger API-Aufrufe - geringere Last |
| **500ms** | Merkbar verzögert | 50 % weniger Aufrufe, fühlt sich aber langsam an |

**Empfehlung**: Halten Sie sich zwischen 250-350ms. Erhöhen Sie nur über 350ms, wenn Ihr Server Schwierigkeiten mit der Autocomplete-Last hat. Gehen Sie nie unter 200ms, es sei denn, Sie haben einen sehr schnellen Server und einen kleinen Katalog.

## Anzeigestellungen für Produkte

Diese Schalter steuern, welche Informationen in den Autocomplete-Ergebnissen für Produkte angezeigt werden:

**Vorschaubild anzeigen** - Standard: AN. Zeigt das Produktbild neben dem Ergebnis an. **Leistungsbeeinträchtigung**: Fügt eine Bildabfrage hinzu und erhöht die Größe der JSON-Payload. Deaktivieren Sie dies für eine schnellere Autocomplete bei langsamen Verbindungen.

**Beschreibung anzeigen** - Standard: AUS. Zeigt die kurze Produktbeschreibung an. **Leistungsbeeinträchtigung**: Fügt Textverarbeitung hinzu und erhöht die Payload-Größe erheblich. Behalten Sie dies deaktiviert, es sei denn, Beschreibungen sind für die Produktwahl entscheidend.

**Preis anzeigen** - Standard: AN. Zeigt den Produktpreis an. **Leistungsbeeinträchtigung**: Gering - Preisdaten werden bereits mit dem Produkt geladen. Es ist sicher, dies aktiviert zu lassen.

**SKU anzeigen** - Standard: AN. Zeigt die Produkt-SKU an. **Leistungsbeeinträchtigung**: Gering - SKU ist bereits indiziert. Wichtig für B2B-Geschäfte.

**Lagerstatus anzeigen** - Standard: AUS. ⚠️ **MAßGEBLICHE LEISTUNGSWARNUNG**

Zeigt Abzeichen wie „Auf Lager“, „Niedriges Lager“ oder „Ausverkauft“ an. **Aktivieren Sie dies NIEMALS bei großen Katalogen**.

Der Lagerstatus erfordert die Aggregation `with_stock_totals()` - die Berechnung der Lagerbestände in allen Lagerhäusern für jedes Produkt in den Autocomplete-Ergebnissen. Dies führt zu:
- Erheblicher Datenbanklast (Aggregationsabfragen)
- 200-500ms zusätzlicher Latenz bei Katalogen mit mehr als 1.000 Produkten
- Potenzielle Timeout bei Katalogen mit mehr als 10.000 Produkten

Aktivieren Sie dies nur, wenn es absolut kritisch ist und Sie weniger als 500 Produkte haben.

## Anzeigestellungen für Blogbeiträge

**Vorschaubild anzeigen** - Standard: AN. Vorschaubild des Blogbeitrags in den Autocomplete-Ergebnissen.

**Excerpt anzeigen** - Standard: AN. Kurze Vorschau aus dem Beitragstext.

**Excerpt-Länge** - Standard: 60 Zeichen. Wie viel Vorschau-Text angezeigt werden soll.

Diese Einstellungen haben minimale Leistungsbeeinträchtigung, da Blogbeiträge im Vergleich zu Produkten typischerweise wenige sind.

## Anzeigestellungen für Kategorien und Marken

**Vorschaubild/Logo anzeigen** - Standard: AN. Kategorie- oder Markenbild in den Ergebnissen.

**Anzahl der Produkte anzeigen** - Standard: AUS. ⚠️ **LEISTUNGSWARNUNG**

Zeigt an, wie viele Produkte in jeder Kategorie oder Marke vorhanden sind (z. B. „Elektronik (234)“).

**Aktivieren Sie dies NIEMALS bei großen Katalogen**. Produktzahlen werden bei jedem Autocomplete-Ansuchen neu berechnet:
- Jeder Inhaltstyp mit aktivierten Zahlen fügt 2 zusätzliche Abfragen hinzu
- Abfragen beinhalten Joins und Aggregationen
- Typische zusätzliche Latenz von 100-300ms
- Steigt linear mit der Anzahl der Kategorien/Marken

Aktivieren Sie dies nur, wenn Sie weniger als 50 Kategorien/Marken und insgesamt weniger als 1.000 Produkte haben.

## Caching

**Autocomplete-Cache-TTL** - Standard: 60 Sekunden (im Caching-Reiter festgelegt).

Autocomplete-Ergebnisse werden im Cache gespeichert, um die Leistung zu verbessern. Die 60-Sekunden-TTL bedeutet:
- Der erste Kunde, der nach „Laptop“ sucht, löst eine Datenbankabfrage aus
- In den nächsten 59 Sekunden geben alle „Laptop“-Suchen die im Cache gespeicherten Ergebnisse zurück
- Nach 60 Sekunden läuft der Cache ab und die nächste Suche aktualisiert die Daten

**Empfehlung für TTL**:
- **45-60s**: Gutes Gleichgewicht für die meisten Geschäfte (Standard)
- **90-120s**: Bessere Leistung, wenn das Produktbestand selten geändert wird
- **30s**: Aktuellere Ergebnisse, wenn Sie häufig Produkte hinzufügen

Die Erhöhung der Cache-TTL ist die einfachste Möglichkeit, die Leistung von Autocomplete zu verbessern.

## Multilingual Autocomplete

Wenn Sie mehrere Sprachen konfiguriert haben, sucht Autocomplete automatisch nach übersetztem Inhalt, der in JSONField-Übersetzungen gespeichert ist.

**Funktionsweise**:
- Kunde sucht auf Spanisch: „zapatos“
- System sucht nach spanischen Produktbezeichnungen
- Ergebnisse zeigen spanische Produktbezeichnungen aus JSONField-Daten an
- Fällt zurück auf die Basissprache, wenn die spanische Übersetzung fehlt

**Leistung**: Minimale Overhead für 1-3 Sprachen. Mit 5+ Sprachen steigt die Abfragekomplexität leicht.

## Autocomplete testen

Nach der Konfiguration der Einstellungen testen Sie die Autocomplete-Erfahrung:

1. **Öffnen Sie die Startseite Ihres Geschäfts** in einem Incognito-Fenster
2. **Klicken Sie auf das Suchfeld**, um es zu fokussieren
3. **Geben Sie einen häufigen Produktnamen langsam ein** (z. B. „Laptop“)
4. **Beobachten Sie**:
   - Wie schnell die Ergebnisse nach dem Stoppen des Tipps erscheinen (funktioniert Debounce?)
   - Welche Informationen angezeigt werden (Vorschaubilder, Preise, SKUs wie konfiguriert)
   - Ob die Ergebnisse relevant sind (prüfen Sie die Relevanzgewichte, wenn nicht)
5. **Testen Sie auf Mobilgeräten** - Stellen Sie sicher, dass das Dropdown für Touch-Bedienung und Lesbarkeit geeignet ist

## Tipps

- **Beschreibungen für Produkte deaktivieren, um Geschwindigkeit zu erhöhen** - Beschreibungen erhöhen die Payload-Größe erheblich, bieten aber in Autocomplete-Kontext kaum Wert
- **Aktivieren Sie NIEMALS den Lagerstatus bei großen Katalogen** - Lageraggregation zerstört die Autocomplete-Leistung
- **Testen Sie auf Mobilgeräten mit Touch-Zielen** - Autocomplete-Ergebnisse müssen auf Handys leicht zu tippen sein
- **Überwachen Sie wöchentlich die Antwortzeiten** - Ziel: <200ms für Autocomplete-Anfragen
- **Erhöhen Sie den Cache-TTL, wenn es langsam ist** - Einfachste Leistungsoptimierung
- **Produktzahlen sind teuer - deaktivieren Sie sie, es sei denn, sie sind kritisch** - Jede Kategorie/Marken-Zahl fügt 2 Abfragen zu jedem Autocomplete-Ansuchen hinzu

