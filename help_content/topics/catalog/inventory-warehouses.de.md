---
title: Lagerbestand & Lager
---

Das Lager-System ermöglicht die Verwaltung des Lagerbestands über mehrere Standorte, die Festlegung von Erfüllungs-Prioritäten und die Echtzeit-Überwachung des Lagerbestands. Navigieren Sie zu **Produkte > Lager** im Admin-Seitenleistenmenü, um Ihre Lagerstandorte zu verwalten.

![Lagerliste](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Lager

### Lagerliste

Die Lagerseite zeigt alle Ihre Lagerstandorte als Karten mit:

- **Name und Code** — Lager-Identifikator (z. B. "Hauptlager", Code "Haupt-LS")
- **Verkaufsregion** — Zuordnung der geografischen Region
- **Status-Badges** — Aktiv/inaktiv, Einzelhandelsstandort
- **Statistiken** — Gelagerte Produkte, Erfüllungspriorität, Lagerpuffer-Prozentsatz
- **Lage** — Stadt und Land
- **Zuletzt aktualisiert** — Zeitpunkt der letzten Änderung des Lagerbestands

### Ein Lager erstellen

1. Klicken Sie auf **+ Lager hinzufügen**
2. Füllen Sie die **Grundinformationen** aus:
   - **Name** — Beschreibender Bezeichner (z. B. "US-East-Lager")
   - **Code** — Kurze eindeutige Kennung (z. B. "US-EAST") — muss eindeutig in allen Lagern sein
   - **Verkaufsregion** — Zuordnung einer geografischen Region für die Erfüllungsrouting
   - **Aktiv** — Aktivieren, um es in die Erfüllung einzubeziehen
3. Füllen Sie den **Adressbereich** mit der vollständigen Lageradresse aus
4. Konfigurieren Sie **Erfüllungseinstellungen**:
   - **Erfüllungspriorität** — Höhere Zahlen = höhere Priorität für die Bestellabwicklung
   - **Lagerpuffer-Prozentsatz** — Prozentsatz des Lagerbestands, der als Sicherheitspuffer reserviert wird (0–100)
   - **Versandort** — Optionalen Link zu einem Abholort hinzufügen, falls dieses Lager Kundenabholung unterstützt
5. Konfigurieren Sie **Kundenansicht** (optional):
   - **Anzeigename** — Kundenansichts-Bezeichnung (z. B. "Versendet aus Australien"). Leer lassen, um den Lagernamen zu verwenden.
   - **Im Frontend anzeigen** — Diesen Lagerstandort auf Produktseiten Kunden anzeigen
6. Konfigurieren Sie **POS / Einzelhandelsspeicher** (optional):
   - **Einzelhandelsspeicher** — Prüfen, ob dieses Lager auch als physischer Laden mit POS-Terminals dient
   - **POS-Anzeigename** — Kurzer Name, der im POS-Interface angezeigt wird
   - **Lagengruppe** — einer POS-Lagengruppe zuordnen für Einstellungen Erbschaft
7. Fügen Sie **Kontaktdaten** hinzu, falls erforderlich (Name, E-Mail, Telefon)
8. Auf **Speichern** klicken

### Erfüllungspriorität

Wenn eine Bestellung eingeht, wählt das System das beste Lager basierend auf:

1. **Prioritätswert** — Höhere Prioritätslager werden bevorzugt
2. **Lagerbestand** — Muss ausreichend vorhanden sein
3. **Regionenübereinstimmung** — Lager in der Region des Kunden werden bevorzugt

Zum Beispiel: Wenn Sie ein US-Lager (Priorität 100) und ein EU-Lager (Priorität 60) haben, werden US-Bestellungen zuerst aus dem US-Lager abgewickelt.

### Lagerpuffer

Der Lagerpuffer reserviert einen Prozentsatz des Lagerbestands, der nicht online verkauft wird. Dies ist nützlich für:

- Physische Einzelhandelsgeschäfte, die Bodenbestand benötigen
- Sicherheitsbestand, um Überverkäufe zu vermeiden
- Reservierter Bestand für Großhandelsbestellungen

Ein 10 %iger Puffer auf 100 Einheiten bedeutet, dass nur 90 Einheiten für Online-Bestellungen verfügbar sind.

## Lagerartikel

Lagerartikel repräsentieren den tatsächlichen Lagerbestand eines bestimmten Produkts an einem bestimmten Lager.

### Anzeige des Lagerbestands

1. Klicken Sie auf das **Lager-Symbol** auf jedem Lagerkarten, um seine Lagerartikel anzuzeigen
2. Oder navigieren Sie zu dem **Lager**-Tab eines Produkts, um den Bestand in allen Lagern anzuzeigen

Jeder Lagerartikel zeigt an:

- **Produktname** und Variante (falls zutreffend)
- **Vorrat** — Gesamtbestand physisch
- **Zugewiesen** — Menge, die für ausstehende Bestellungen reserviert ist
- **Verfügbar** — Vorrat minus zugewiesen (was verkauft werden kann)

### Lagerbestand hinzufügen

1. Navigieren Sie zu **Produkte > Lagerartikel** und klicken Sie auf **+ Lagerartikel hinzufügen**, oder
2. Öffnen Sie das Bearbeitungsformular eines Produkts und verwenden Sie den **Lagerartikel**-Inline-Bereich unten
3. Wählen Sie das **Produkt** und das **Lager** (und optional eine **Variante** für variable Produkte)
4. Geben Sie die **Vorratsmenge** ein
5. Legen Sie den **Niedrigbestands-Schwellenwert** fest — dieser pro-Artikel-Schwellenwert löst eine Warnung bei niedrigem Bestand aus
6. Speichern

### Lagerbewegungen

Jede Änderung des Lagerbestands wird als **Lagerbewegung** protokolliert:

| Bewegungstyp | Beschreibung |
|--------------|-------------|
| **Eingang** | Neues Lagergut vom Lieferanten erhalten |
| **Verkauf** | Lagergut für einen abgeschlossenen Auftrag abgezogen |
| **Rückgabe** | Lagergut von einem Kunden zurückgegeben |
| **Anpassung** | Manuelle Korrektur (Zählungsdifferenz) |
| **Transfer** | Zwischen Lagerhäusern verschoben |
| **Reservierung** | Temporär für einen aktiven Warenkorb gesperrt |
| **Beschädigung** | Als beschädigt oder verloren angesehen |
| **Neuzählung** | Korrigiert, um einer physischen Lagerzählung zu entsprechen |

Lagerbewegungen bieten einen vollständigen Audit-Trail für Lagerveränderungen. Neben der Aktion **Lagerbestände anpassen** bietet Spwig auch Massenaktionen auf der Liste der Lagerartikel, um Lagerbestände in vielen Artikeln gleichzeitig zu transferieren, abzuschreiben und neu zu zählen — siehe [Massenlageraktionen](/help/stock-bulk-actions).

## Lagerbestandsverfolgung bei Produkten

### Lagerbestandsverfolgung aktivieren

Im **Lager**-Abschnitt eines Produkts:

1. Schalten Sie **Lagerbestand verfolgen** ein, um die Lagerverwaltung für dieses Produkt zu aktivieren
2. Legen Sie den **Niedrigbestands-Schwellenwert** fest — löst Warnungen im Dashboard aus, wenn der Lagerbestand in einem Lager unter diesen Wert fällt
3. Konfigurieren Sie **Zurückhaltungen zulassen**, falls Sie Bestellungen akzeptieren möchten, wenn der Artikel nicht auf Lager ist
4. Legen Sie optional eine **Nicht-lagernd-Aktion** fest, um das Verhalten der Website oder Kategorie für dieses spezifische Produkt zu überschreiben

Nach Aktivierung der Verfolgung können Sie die tatsächlichen Lagerbestände über die **Lagerartikel**-Inline-Sektion am Ende des Produktformulars verwalten oder über **Produkte > Lagerartikel**.

### Lagerbestand über mehrere Lagerhäuser

Wenn die Lagerverfolgung aktiviert ist, zeigt der Lager-Tab die Lagerbestände über alle Lagerhäuser in einer Zusammenfassungstabelle an:

- Gesamtbestand an allen Standorten
- Aufschlüsselung pro Lagerhaus
- Verfügbare Mengen nach Reservierungen und Zuordnungen

## Niedrigbestands-Warnungen

Das System überwacht automatisch die Lagerbestände und warnt Sie, wenn:
- Ein Produkt unter seinen **Niedrigbestands-Schwellenwert** fällt
- Ein Produkt **keine verfügbaren Lagerbestände** mehr hat

Niedrigbestands-Warnungen erscheinen auf:
- Der **Shop-Dashboard**-Seite im Abschnitt "Aktionen erforderlich"
- Der Produktliste mit einer visuellen Kennzeichnung

## Tipps

- Beginnen Sie mit einem Lagerhaus und fügen Sie weitere hinzu, wenn sich Ihr Geschäft weiterentwickelt.
- Legen Sie Fulfillment-Prioritäten basierend auf der Versandgeschwindigkeit und -kosten für jedes Gebiet fest.
- Verwenden Sie Lagerpuffer für Einzelhandelsstandorte, um die Lagerverfügbarkeit am Regal sicherzustellen.
- Prüfen Sie regelmäßig Lagerbewegungen, um Beschädigungen oder Diskrepanzen zu identifizieren.
- Legen Sie Niedrigbestands-Schwellenwerte basierend auf Ihrem Nachschub-Zeithorizont fest – wenn es 2 Wochen dauert, um nachzubestellen, setzen Sie den Schwellenwert auf 2 Wochen Verkauf.
- Aktivieren Sie die Lagerverfolgung, bevor Sie live gehen, um Überverkäufe zu vermeiden.