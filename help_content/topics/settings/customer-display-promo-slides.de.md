---
title: Kundensichtbare Werbebilder
---

Werbebilder werden auf dem Kundenbildschirm angezeigt, wenn der POS-Terminal leer ist (keine aktive Transaktion). Erstellen Sie eine Bildschau, die saisonale Werbeaktionen, neue Produktstarts, Ladenpolitiken, bevorstehende Veranstaltungen und Vorteile des Treueprogramms zeigt. Werbebilder können mit der Zuordnung von Scopes an bestimmte Läden oder Gruppen gerichtet werden – führen Sie nur an US-Läden Weihnachtsaktionen durch oder zeigen Sie nur an relevanten Standorten lokale Veranstaltungsinformationen an. Aktive Werbebilder wechseln sich automatisch alle 5-10 Sekunden ab, wodurch ansprechende digitale Werbung entsteht, die Kunden während des Wartens informiert.

Verwenden Sie Werbebilder, um die Aufmerksamkeit auf aktuelle Werbeaktionen zu lenken, Kunden über Richtlinien zu informieren und die Teilnahme an Treueprogrammen und Veranstaltungen zu fördern.

![Liste der Werbebilder](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Kundenbildschirmverhalten

Wenn ein POS-Terminal leer ist (kein Kunde am Kassenschalter, keine laufende Transaktion), zeigt der Kundenbildschirm an:

**Karussellmodus**:
- Wechselt durch alle aktiven Werbebilder
- Jedes Werbebild wird 5-10 Sekunden angezeigt (konfigurierbar pro Terminal)
- Glatter Übergang zwischen den Werbebildern
- Wiederholt sich kontinuierlich, bis eine Transaktion gestartet wird

**Während einer Transaktion**:
- Das Karussell stoppt sofort
- Der Bildschirm wechselt in den Transaktionsansicht (Artikel, laufende Gesamtsumme, Zahlungsaufforderungen)
- Das Karussell startet erneut, wenn die Transaktion abgeschlossen ist und das Terminal erneut leer ist

**Keine konfigurierten Werbebilder**:
- Der Bildschirm zeigt eine „Willkommen“-Nachricht mit Ladenbranding an
- Statischer Bildschirm (kein Karussell)

**Technische Anforderungen**:
- Der Kundenbildschirm kann ein separates Monitor oder der gleiche Bildschirm wie der Kassierer sein (POS-App unterstützt Picture-in-Picture-Modus)
- Der Bildschirm synchronisiert sich über BroadcastChannel API (Kommunikation auf demselben Gerät) oder WebSocket (Bildschirme auf separaten Geräten)

## Zielgruppenorientierung

Wie bei Rezeptvorlagen unterstützt auch das Werbebild die Zielgruppenorientierung (von höchster Priorität zu niedrigster):

| Priorität | Zielgruppe | Beispiel | Anwendungsfall |
|-----------|------------|--------|----------------|
| **1** | Laden-spezifisch | Werbebilder für den Paris Store | Werbebild für ein Fest im Sommer in Paris |
| **2** | Gruppen-spezifisch | Werbebilder für europäische Stores | Werbebild für die DSGVO-Datenschutzrichtlinie nur für EU |
| **3** | Alle Stores | Globale Werbebilder | „Kostenlose Lieferung bei Bestellungen >$50“ (Firmenweite Werbeaktion) |

**Wie Zielgruppenfunktioniert**:
- Das Terminal zeigt Werbebilder an, die mit dem Store-Scope übereinstimmen (ladespezifische Werbebilder)
- Plus Werbebilder, die mit dem Gruppen-Scope übereinstimmen (wenn der Store in einer Gruppe ist)
- Plus Werbebilder ohne Scope-Zuordnung (globale Werbebilder)
- Ergebnis: Ein Laden kann 3-5 Werbebilder zeigen (Kombination aus Zielgruppen- und globalen Werbebildern)

**Beispiel**:
- Globales Werbebild: „Neues Treueprogramm – Jetzt beitreten!“ (kein Scope)
- Gruppenwerbebild: „Memorial Day Sale – 30% Rabatt“ (nur Gruppe US Stores)
- Ladenwerbebild: „Großöffnung – NYC Flagship“ (nur NYC Store)

**NYC Store Terminal** zeigt alle 3 Werbebilder an (Laden + Gruppe + global)
**London Store Terminal** zeigt nur das globale Werbebild an (nicht in der Gruppe US Stores, nicht NYC Store)

## Bildanforderungen

Werbebilder sind Vollbildbilder, die für Kundenbildschirm-Monitore optimiert sind:

**Seitenverhältnis**: 16:9 (breitbild)

**Empfohlene Auflösung**: 1920×1080 Pixel (Full HD)
- Skaliert sauber auf die meisten modernen Displays
- Dateigröße ausgewogen (Qualität vs. Ladezeit)

**Akzeptierte Auflösungen**:
- Mindestens: 1280×720 (HD)
- Optimal: 1920×1080 (Full HD)
- Maximal: 3840×2160 (4K) – nicht empfohlen (große Dateigröße, langsames Laden)

**Dateiformat**: JPG, PNG oder WebP
- JPG für Fotos
- PNG für Grafiken mit Transparenz (Hintergründe werden empfohlen)
- WebP für die kleinste Dateigröße

**Dateigröße**: <500 KB pro Werbebild
- Größere Dateien verlangsamen das Laden des Karussells
- Komprimieren Sie Bilder vor dem Hochladen (verwenden Sie die Optimierung der Medienbibliothek)

**Gestaltungsempfehlungen**:
- Hoher Kontrast für Lesbarkeit aus der Ferne (Kunden 2-6 Fuß vom Bildschirm entfernt)
- Große Schrift (mindestens 48pt für Textkörper, 72pt+ für Überschriften)
- Fette Schriften (dünne Schriften verschwinden auf einigen Bildschirmen)
- Vermeiden Sie kleine Details (werden vom Kunden nicht gesehen)
- Fügen Sie eine Aufforderung zur Handlung hinzu (was der Kunde tun sollte: „Frage den Kassierer nach Details“, „Jetzt anmelden“)

## Werbebild erstellen

Navigieren Sie zu **POS > Werbebilder** und klicken Sie auf **+ Werbebild hinzufügen**:

![Werbebild-Formular hinzufügen](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Bild** – Hochladen oder aus der Medienbibliothek auswählen:
- Klicken Sie auf **Medienbibliothek durchsuchen**, um ein vorhandenes Bild auszuwählen
- Oder laden Sie ein neues Bild hoch, das den oben genannten Anforderungen entspricht
- Vorschau zeigt an, wie das Bild auf dem Bildschirm angezeigt wird

**Titel** (optional) – Textüberlagerung oben auf dem Werbebild:
- Maximal 60 Zeichen (längere Texte werden abgeschnitten)
- Erscheint in einem halbtransparenten dunklen Balken oben auf dem Bild
- Verwenden Sie für den Titel des Werbebildes („Sommerverkauf“, „Neue Ankünfte“)
- Lassen Sie es leer, wenn das Bild bereits einen Titel enthält

**Untertitel** (optional) – Textüberlagerung unter dem Titel:
- Maximal 120 Zeichen
- Erscheint unter dem Titel im gleichen halbtransparenten Balken
- Verwenden Sie für ergänzende Details („Bis zu 50 % Rabatt“, „Gratis Geschenk mit Kauf“)
- Lassen Sie es leer, wenn das Bild selbstständig ist

**Aktiv** – Schalter zum Aktivieren/Deaktivieren des Werbebildes:
- Nur aktive Werbebilder erscheinen im Karussell
- Verwenden Sie zur saisonalen Aktivierung (deaktivieren Sie nach Ablauf der Werbeaktion)
- Deaktivieren Sie das Werbebild, um es für eine spätere Wiederaktivierung zu bewahren

**Sortierreihenfolge** – Steuert die Position des Werbebildes im Karussell:
- Niedrigere Zahlen erscheinen früher in der Rotation
- Verwenden Sie Vielfache von 10: 10, 20, 30 (erlaubt das Einfügen von Werbebildern zwischen bestehenden)
- Beispiel: Sommerverkauf (Sortierreihenfolge 10) wird vor dem allgemeinen Treueprogramm (Sortierreihenfolge 20) angezeigt

**Zielgruppenzuordnung** (optional):
- **Lager** – Wählen Sie, um das Werbebild nur an einem bestimmten Laden anzuzeigen
- **Ladengruppe** – Wählen Sie, um das Werbebild nur an Läden in der Gruppe anzuzeigen
- **Beide leer lassen** – Wird an allen Läden angezeigt (globales Werbebild)

## Sortierreihenfolge und Karussellablauf

**Beispiel Karussell** (Terminal in NYC Store):
- Werbebild 1 (Sortierreihenfolge 10): „Großöffnung – NYC Flagship“ (ladespezifisch)
- Werbebild 2 (Sortierreihenfolge 15): „Memorial Day Sale – 30% Rabatt“ (Gruppe US Stores)
- Werbebild 3 (Sortierreihenfolge 20): „Neues Treueprogramm – Jetzt beitreten!“ (global)
- Werbebild 4 (Sortierreihenfolge 30): „Folgen Sie uns @yourstore“ (global)

Karussellschleife: 1 → 2 → 3 → 4 → 1 → 2 → ...

**London Store Terminal** (nicht in der Gruppe US Stores, anderer Laden):
- Werbebild 1 (Sortierreihenfolge 20): „Neues Treueprogramm – Jetzt beitreten!“ (global)
- Werbebild 2 (Sortierreihenfolge 30): „Folgen Sie uns @yourstore“ (global)

Karussellschleife: 1 → 2 → 1 → 2 → ...

Verwenden Sie die Sortierreihenfolge, um den wichtigsten Inhalt zuerst in der Rotation zu priorisieren.

## Strategie für saisonale Aktivierung

**Problem**: Das Erstellen/Entfernen von Werbebildern für jede saisonale Werbeaktion ist mühsam.

**Lösung**: Werbebilder einmal erstellen, aktivieren/deaktivieren saisonal:

1. **Werbebilder für wichtige Ereignisse erstellen**:
   - „Sommerverkauf“ (Aktiv: Nein, erstellt im Voraus)
   - „Zurück zur Schule“ (Aktiv: Nein, erstellt im Voraus)
   - „Black Friday“ (Aktiv: Nein, erstellt im Voraus)
   - „Weihnachtsverkauf“ (Aktiv: Nein, erstellt im Voraus)

2. **Aktivieren, wenn relevant**:
   - 1. Juni: „Sommerverkauf“ → Aktiv: Ja
   - 15. August: „Sommerverkauf“ → Aktiv: Nein, „Zurück zur Schule“ → Aktiv: Ja
   - 20. November: „Black Friday“ → Aktiv: Ja
   - 1. Dezember: „Black Friday“ → Aktiv: Nein, „Weihnachtsverkauf“ → Aktiv: Ja

3. **Nach dem Ereignis deaktivieren**:
   - Hält die Werbebildbibliothek organisiert
   - Wiederverwenden Sie Werbebilder Jahr für Jahr (aktualisieren Sie das Bild bei Bedarf, behalten Sie die Konfiguration)

## Anwendungsfälle

**Anwendungsfall 1: Saisonale Werbeaktion**
- Bild: Rotes Hintergrund mit weißem Text „SUMMER SALE - UP TO 60% OFF"
- Titel: „Sommerverkauf"
- Untertitel: „50-60% Rabatt auf ausgewählte Artikel. Fragen Sie den Kassierer nach Details.“
- Zielgruppe: Alle Läden (global)
- Sortierreihenfolge: 10 (höchste Priorität während des Sommers)
- Aktiv: Nur im Juni-August

**Anwendungsfall 2: Ladenpolitik**
- Bild: Infografik, die die Schritte der Rückgabepolitik zeigt
- Titel: „Einfache Rückgaben"
- Untertitel: „30 Tage mit Kassenbon. Keine Fragen gestellt.“
- Zielgruppe: Alle Läden (global)
- Sortierreihenfolge: 40 (niedrigere Priorität als Werbeaktionen)
- Aktiv: Ganzjährig

**Anwendungsfall 3: Neues Produktstart**
- Bild: Hero-Bild des neuen Produkts
- Titel: „NEU: Wireless Earbuds Pro"
- Untertitel: „Jetzt im Geschäft und online erhältlich. $199,99"
- Zielgruppe: Alle Läden (global)
- Sortierreihenfolge: 5 (höchste Priorität während der Startwoche)
- Aktiv: Nur während der Startwoche, dann deaktivieren

**Anwendungsfall 4: Lokale Veranstaltung**
- Bild: Poster für eine lokale Charity-Lauf
- Titel: „Unterstützen Sie die lokale Gemeinschaft"
- Untertitel: „Treffen Sie uns beim Community 5K am 15. Juni!"
- Zielgruppe: Bestimmter Laden (nur NYC Store)
- Sortierreihenfolge: 8 (Priorität für diesen Laden)
- Aktiv: 2 Wochen vor der Veranstaltung

**Anwendungsfall 5: Treueprogramm**
- Bild: Visuelle Darstellung einer Treuekarte mit Beispielen für Punkte
- Titel: „Sammeln Sie Belohnungen"
- Untertitel: „Treten Sie unserem Treueprogramm bei und sammeln Sie 1 Punkt pro $1 Ausgaben"
- Zielgruppe: Alle Läden (global)
- Sortierreihenfolge: 30 (ewiger Inhalt)
- Aktiv: Ganzjährig

## Verwaltung von Werbebildern

**Liste der Werbebilder**:
- Zeigt alle Werbebilder mit Vorschau des Bildes, Titel, Zielgruppe und Status an
- Filtern Sie nach aktiv/inaktiv
- Filtern Sie nach Zielgruppe (ansicht alle globalen Werbebilder, alle Gruppenwerbebilder usw.)

**Massenaktivierung/Deaktivierung**:
- Wählen Sie mehrere Werbebilder in der Liste aus
- Verwenden Sie die Verwaltungsaktion, um alle gleichzeitig zu aktivieren oder deaktivieren
- Nützlich für saisonale Übergänge (deaktivieren Sie alle Sommerwerbebilder, aktivieren Sie alle Herbstwerbebilder)

**Testen von Werbebildern**:
- Nach dem Erstellen/Aktualisieren eines Werbebildes navigieren Sie zu einem POS-Terminal
- Lassen Sie das Terminal leer laufen (keine Transaktion)
- Überprüfen Sie, ob das Werbebild im Karussell angezeigt wird
- Prüfen Sie die Bildqualität, Lesbarkeit der Textüberlagerung und die Zeitspanne

**Aktualisieren aktiver Werbebilder**:
- Änderungen werden bei der nächsten Karussellaktualisierung wirksam (normalerweise <30 Sekunden)
- Es ist kein Neustart der Terminals erforderlich

## Tipps

- **Entwerfen Sie für die Distanz** – Kunden betrachten den Bildschirm von 2-6 Fuß Entfernung; verwenden Sie große Schrift und hohen Kontrast
- **Halten Sie die Nachricht einfach** – Das Werbebild wird weniger als 10 Sekunden angezeigt; eine klare Nachricht pro Werbebild
- **Verwenden Sie saisonale Deaktivierung** – Erstellen Sie einmal, schalten Sie jährlich ein/aus anstelle von Neuerstellung
- **Priorisieren Sie mit Sortierreihenfolge** – Wichtige Werbeaktionen sollten die niedrigste Sortierreihenfolge haben (erscheinen zuerst)
- **Testen Sie auf echter Hardware** – Farbkalibrierung des Bildschirms variiert; überprüfen Sie, ob die Werbebilder auf Ihren spezifischen Monitoren gut aussehen
- **Beschränken Sie die Anzahl aktiver Werbebilder** – 3-5 aktive Werbebilder pro Laden sind optimal; 10+ Werbebilder bedeuten, dass jedes nur selten angezeigt wird
- **Fügen Sie Aufforderungen zur Handlung hinzu** – Sagen Sie Kunden, was sie tun sollen („Frage den Kassierer“, „Besuchen Sie die Website“, „Scannen Sie den QR-Code auf dem Kassenbon“)
- **Aktualisieren Sie regelmäßig** – Veraltete Werbeaktionen (abgelaufene Verkaufsaktionen, vergangene Veranstaltungen) verringern das Vertrauen der Kunden
- **Verwenden Sie Zielgruppenstrategisch** – Regionale Werbeaktionen (Gruppenzielgruppe) und lokale Veranstaltungen (Ladenzielgruppe) fühlen sich relevanter an als ständige globale Inhalte

