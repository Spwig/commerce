---
title: AI-SEO-Generator
---

Der AI-SEO-Generator erstellt automatisch Meta-Titel, Meta-Beschreibungen und andere SEO-Inhalte für Ihre Produkte mithilfe eines AI-Anbieters. Anstatt für jedes Produkt manuell SEO-Texte zu schreiben, können Sie präzise, optimierte Inhalte in Bulk mit einer einzigen Aktion generieren.

Ihr Geschäft verfügt über einen integrierten SEO-Generator, der sofort funktioniert. Sie können auch zusätzliche AI-Anbieter-Komponenten aus dem Spwig-Komponenten-Marktplatz installieren, um Zugang zu leistungsstärkeren Sprachmodellen zu erhalten.

## Wie der SEO-Generator funktioniert

Der SEO-Generator liest den Namen, die Beschreibung, die Kategorie und die Attribute Ihres Produkts und verwendet dann den konfigurierten AI-Anbieter, um SEO-Inhalte zu erstellen, die auf dieses Produkt zugeschnitten sind. Der generierte Inhalt wird direkt in die SEO-Felder des Produkts gespeichert.

Sie können SEO-Inhalte für einzelne Produkte von der Produktbearbeitungsseite generieren oder eine Bulk-Generierung über mehrere Produkte hinweg von der Produktliste aus durchführen.

## Einrichten eines SEO-Anbieters

### Verwenden des integrierten Anbieters

Ihr Geschäft verfügt über einen integrierten SEO-Anbieter, der SEO-Inhalte deterministisch aus Ihren Produktdaten generiert – keine externen API-Schlüssel sind erforderlich. Er wird automatisch als primärer Anbieter bei neuen Installationen festgelegt.

Um sicherzustellen, dass er aktiv ist:

1. Navigieren Sie zu **Marketing > SEO-Anbieter**
2. Überprüfen Sie, ob der integrierte Anbieter mit einem **PRIMÄR**-Abzeichen und einem **AKTIV**-Status angezeigt wird
3. Wenn keine Anbieter aufgelistet sind, klicken Sie auf **+ SEO-Anbieter-Konto hinzufügen** und legen Sie den **Anbieter-Schlüssel** auf `deterministic` fest

### Verknüpfen einer AI-Anbieter-Komponente

Für reichhaltigere, kontextuellere SEO-Inhalte können Sie eine AI-Anbieter-Komponente (z. B. eine auf OpenAI oder Claude basierende Komponente) aus dem Spwig-Komponenten-Marktplatz installieren.

1. Installieren Sie die Anbieterkomponente über das Komponenten-Update-System (fragen Sie Ihren Geschäftsinhaber)
2. Navigieren Sie zu **Marketing > SEO-Anbieter**
3. Klicken Sie auf **+ SEO-Anbieter-Konto hinzufügen**
4. Füllen Sie das Formular aus:

**Anbieterinformationen-Abteilung:**
- **Site** — wählen Sie Ihr Geschäft
- **Anbieterkomponente** — wählen Sie die installierte AI-Anbieterkomponente
- **Anbieter-Schlüssel** — lassen Sie dies leer, wenn Sie eine komponentenbasierte Anbieter verwenden
- **Kontoname** — ein beschreibender Name wie `OpenAI SEO-Anbieter`

**Konfigurationsabteilung:**
- **Aktiv** — aktivieren Sie dies, um diesen Anbieter zu verwenden
- **Primär** — aktivieren Sie dies, um diesen als Standardanbieter für alle SEO-Generierung zu verwenden
- **Priorität** — niedrigere Zahlen werden zuerst in der Fallback-Kette ausprobiert
- **Einstellungen** — anbieter-spezifische Einstellungen als JSON-Objekt (z. B. Modellname, Ton, Sprache)

5. Klicken Sie auf **Speichern**

Nur ein Anbieter kann als primär festgelegt werden. Wenn Sie einen neuen Anbieter als primär markieren, wird der vorherige primäre Anbieter automatisch abgestuft.

### Fallback-Kette des Anbieters

Wenn Ihr primärer Anbieter fehlschlägt (z. B. aufgrund eines API-Ausfalls), wechselt Ihr Geschäft automatisch zum nächsten aktiven Anbieter in der Prioritätsreihenfolge. Dies stellt sicher, dass die SEO-Generierung weiterhin funktioniert, auch wenn ein Anbieter vorübergehend nicht verfügbar ist.

## SEO-Inhalt für ein Produkt generieren

### Einzelnes Produkt

1. Navigieren Sie zu **Produkte > Produkte** und öffnen Sie jedes Produkt
2. Scrollen Sie zu dem **SEO**-Abschnitt des Produktformulars
3. Klicken Sie auf die Schaltfläche **SEO generieren**
4. Der AI-Anbieter generiert einen Meta-Titel und eine Meta-Beschreibung basierend auf den Details des Produkts
5. Überprüfen Sie den generierten Inhalt und bearbeiten Sie ihn bei Bedarf
6. Klicken Sie auf **Speichern**, um die Änderungen anzuwenden

### Bulk-Generierung

Um SEO-Inhalte für mehrere Produkte gleichzeitig zu generieren oder zu aktualisieren:

1. Navigieren Sie zu **Produkte > Produkte**
2. Wählen Sie die Produkte aus, die Sie aktualisieren möchten, indem Sie ihre Kontrollkästchen auswählen, oder wählen Sie alle
3. Öffnen Sie das Dropdown **Aktion**
4. Wählen Sie **SEO-Inhalt generieren** (oder ähnlichen Aktionennamen – prüfen Sie das Dropdown für den genauen Bezeichnung)
5. Klicken Sie auf **Weiter**

Spwig stellt die Generierungsaufgaben in die Warteschlange und verarbeitet sie im Hintergrund. Aktualisieren Sie die Produktliste nach ein paar Minuten, um die aktualisierten SEO-Felder anzuzeigen.

## Überprüfen der SEO-Abdeckung

Der SEO-Generator verfolgt, welche Produkte bereits SEO-Inhalte haben. Um Produkte zu identifizieren, die immer noch SEO-Inhalte benötigen:

1.

Navigieren Sie zu **Produkte > Produkte**
2.


Verwenden Sie den **SEO-Status**-Filter (falls verfügbar), um Produkte anzuzeigen, bei denen Titel oder Beschreibungen fehlen
3.

Wählen Sie diese Produkte aus und führen Sie die Aktion zur Massenerstellung durch

## Provider-Einstellungen

Das **Einstellungen**-Feld eines SEO-Provider-Kontos akzeptiert ein JSON-Objekt mit provider-spezifischen Konfigurationen. Häufige Optionen sind:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Diese Einstellungen variieren je nach Provider-Komponente. Siehe die Dokumentation des Providers für die vollständige Liste der verfügbaren Optionen.

## Verwaltung mehrerer Provider

Wenn Sie mehr als ein SEO-Provider-Konto konfiguriert haben, zeigt die Provider-Liste ihren Status im Überblick an:

- **PRIMÄR-Abzeichen** — dieser Provider wird standardmäßig für alle SEO-Erstellungen verwendet
- **AKTIV-Abzeichen** — der Provider ist aktiviert
- **INAKTIV-Abzeichen** — der Provider ist deaktiviert und wird nicht verwendet

Um den primären Provider zu ändern, öffnen Sie das Konto des Providers, den Sie zum Primär-Provider machen möchten, aktivieren Sie das **Ist primär**-Kästchen und speichern Sie die Änderung. Das System stellt sicher, dass immer nur ein Provider das Primär-Abzeichen trägt.

## Tipps

- Erstellen Sie SEO-Inhalte für neue Produkte sofort nach deren Erstellung — es dauert nur Sekunden und gibt Suchmaschinen etwas Nützliches zum Indizieren
- Überprüfen Sie die von der KI generierten Metabeschreibungen vor der Veröffentlichung, wenn Ihre Produkte ungewöhnliche oder technische Namen haben; der Generator arbeitet am besten mit klaren, beschreibenden Produktbezeichnungen
- Legen Sie in den Provider-Einstellungen `"max_title_length": 60` und `"max_description_length": 160` fest, um den generierten Inhalt innerhalb der von Google empfohlenen Zeichenbegrenzung zu halten
- Führen Sie eine Massenerstellung von SEO-Inhalten durch, nachdem Sie einen großen Produktkatalog importiert haben, um alle SEO-Felder schnell zu füllen
- Wenn Sie die Beschreibung eines Produkts erheblich aktualisieren, erstellen Sie die SEO-Inhalte erneut, um die Metatags mit dem neuen Text abzugleichen
- Der integrierte deterministische Provider ist ein guter Ausgangspunkt; wechseln Sie zu einer KI-gestützten Komponente, sobald Ihr Katalog eingerichtet ist und Sie reichhaltigere, natürlicher klingende SEO-Texte wünschen