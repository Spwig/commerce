---
title: Übersetzungsdienst
---

Der Übersetzungsdienst bietet KI-gestützte Übersetzungen für Produktbeschreibungen, Seiteninhalte, Blogbeiträge, SEO-Felder und andere Händlerinhalte Ihres Geschäfts. Übersetzungen werden lokal auf Ihrem Server oder über externe Anbieter durchgeführt, sodass Ihr Inhalt privat bleibt und die Übersetzungen in Sekunden erfolgen.

![Sprachverwaltung](/static/core/admin/img/help/translation-service/language-management.webp)

## Wie es funktioniert

1. Sie **aktivieren Sprachen** für Ihr Geschäft (z. B. Englisch, Deutsch, Japanisch)
2. Wenn Sie Inhalt erstellen oder bearbeiten (Produkte, Seiten, Blogbeiträge), schreiben Sie in Ihrer Standard-Sprache
3. Klicken Sie auf **Übersetzen** in jedem übersetzbaren Feld, um KI-Übersetzungen in Ihre aktivierten Sprachen zu generieren
4. Übersetzungen werden zusammen mit dem Originalinhalt gespeichert und automatisch basierend auf der Sprache des Besuchers bereitgestellt

## Sprachen verwalten

Navigieren Sie zu **Einstellungen > Sprachen**, um die Sprachen Ihres Geschäfts zu verwalten.

### Sprachdashboard

Das Dashboard zeigt:
- **Gesamtzahl der Sprachen** — Alle verfügbaren Sprachen im System (100+)
- **Aktive Sprachen** — Sprachen, die derzeit für Ihr Geschäft aktiviert sind
- **Modellabdeckung** — Wie viele Sprachen das installierte Übersetzungsmodell unterstützt

### Sprachen aktivieren

1. Finden Sie die Sprache in der Spalte **Verfügbare Sprachen**
2. Klicken Sie auf die Sprache, um sie in die Spalte **Aktive Sprachen** zu verschieben
3. Die Sprache ist sofort für Übersetzungen verfügbar und erscheint im Sprachwechsler Ihres Geschäfts

### Standard-Sprache

Eine Sprache ist als **Standard** markiert. Dies ist:
- Die Sprache, in der Sie Inhalt erstellen
- Die Standard-Sprache, wenn keine Übersetzung vorhanden ist
- Die Sprache, die angezeigt wird, wenn Besucher keine Präferenz ausgewählt haben

## Übersetzungsmodule

Spwig enthält einen lokalen KI-Übersetzungsmotor, der vollständig auf Ihrem Server läuft — keine Daten werden an externe Dienste gesendet.

### Verfügbare Module

| Modell | Sprachen | Geschwindigkeit | Qualität |
|--------|----------|----------------|---------|
| **M2M100-418M** | 100 | Schnell | Gut für gängige Sprachpaare |
| **M2M100-1.2B** | 100 | Mittel | Bessere Qualität, höhere Ressourennutzung |
| **NLLB-200** | 200+ | Mittel | Beste Abdeckung, einschließlich seltener Sprachen |

### Modellauswahl

Die Sprachverwaltungsseite zeigt an, welches Modell installiert ist und seine Sprachabdeckung. Das Modell läuft als lokaler Dienst mit CTranslate2 für effiziente Inferenz.

## Externe Anbieter

Für Geschäfte, die Cloud-basierte Übersetzung bevorzugen oder eine spezifische Sprachqualität benötigen, unterstützt Spwig externe Übersetzungsdienste.

| Anbieter | Beschreibung |
|----------|-------------|
| **DeepL** | Premium-Übersetzung für europäische und asiatische Sprachen |
| **Google Translate** | Breite Sprachabdeckung mit neuronaler Maschinentranslation |
| **Azure Translator** | Microsofts neuronale Übersetzungsdienst |
| **AWS Translate** | Amazon-Maschinentranslation mit Unterstützung für benutzerdefinierte Terminologie |

### Anbieter verbinden

1. Navigieren Sie zu **Einstellungen > Übersetzungsdienste**
2. Wählen Sie den Anbieter und geben Sie Ihren API-Schlüssel ein
3. Setzen Sie den Anbieter als bevorzugten Übersetzungsdienst
4. Übersetzungen verwenden den externen Anbieter anstelle des lokalen Modells

Sie können externe Anbieter neben dem lokalen Modell verwenden — beispielsweise DeepL für europäische Sprachen und das lokale Modell für alles andere.

## Inhalt übersetzen

### Feldbezogene Übersetzung

Übersetzbare Felder (Produktbezeichnungen, Beschreibungen, SEO-Titel usw.) zeigen eine **Übersetzungsschaltfläche** neben dem Feld. Klicken Sie darauf, um:

1. **In alle aktiven Sprachen übersetzen** — Generiert Übersetzungen für jede aktive Sprache auf einmal
2. **In eine bestimmte Sprache übersetzen** — Wählen Sie einzelne Sprachen aus, um sie zu übersetzen

Übersetzungen erscheinen in den Sprachregisterkarten des Bearbeiters. Sie können Übersetzungen überprüfen und bei Bedarf manuell bearbeiten.

### Massen-Übersetzungsaufträge

Für große Mengen an Inhalt verwenden Sie **Übersetzungsaufträge**:

1. Navigieren Sie zu **Einstellungen > Übersetzungsaufträge**
2. Erstellen Sie einen neuen Auftrag, indem Sie auswählen:
   - **Inhaltstyp** — Produkte, Seiten, Blogbeiträge, Kategorien usw.
   - **Quellsprache** — Die Sprache, aus der übersetzt werden soll
   - **Zielsprachen** — Eine oder mehrere Sprachen, in die übersetzt werden soll
   - **Umfang** — Alle Inhalte oder nur nicht übersetzte Felder
3. Senden Sie den Auftrag — er wird im Hintergrund über eine Aufgabenwarteschlange verarbeitet
4. Überwachen Sie den Fortschritt in der Auftragsliste (in Warteschlange → Verarbeitung → Abgeschlossen)

Massen-Aufträge sind nützlich, wenn Sie eine neue Sprache aktivieren und Ihren gesamten Katalog auf einmal übersetzen möchten.

## Übersetzungsbewirtschaftung

### Übersetzungen überprüfen

Jedes übersetzte Feld verfolgt:
- **Übersetzungszustand** — Ob das Feld maschinell übersetzt, manuell bearbeitet oder fehlt
- **Sperrezustand** — Gesperrte Übersetzungen werden nicht durch zukünftige Maschinenübersetzungen überschrieben
- **Zuletzt übersetzt** — Wann die Übersetzung zuletzt generiert oder bearbeitet wurde

### Übersetzungen sperren

Wenn Sie eine maschinell generierte Übersetzung manuell bearbeiten, um sie zu verbessern, **sperren** Sie das Feld, um zu verhindern, dass es beim nächsten Mal durch eine Massenübersetzung überschrieben wird. Gesperrte Felder werden bei automatischen Übersetzungen übergangen.

### Übersetzungsumfang

Der Umfangsverfolger zeigt an, welcher Prozentsatz Ihres Inhalts für jede Sprache übersetzt ist. Navigieren Sie zu **Einstellungen > Sprachen**, um anzuzeigen:
- Prozentsätze der Übersetzungserledigung pro Sprache
- Welche Inhaltstypen Lücken aufweisen
- Felder, die immer noch eine Übersetzung benötigen

## UI-Übersetzungsoverrides

Neben Produkt- und Seiteninhalten können Sie auch die Übersetzungen von **Frontend-Schnittstellenzeichenfolgen** anpassen — Schaltflächen, Beschriftungen, Nachrichten und andere UI-Texte, die Besuchern angezeigt werden.

Navigieren Sie zu **Einstellungen > UI-Überschreibungen**, um:
1. Eine bestimmte Zeichenfolge suchen (z. B. "Add to Cart")
2. Für jede Sprache Ihre bevorzugte Übersetzung eingeben
3. Speichern — die Überschreibung wird sofort wirksam

Es sind etwa 300 Frontend-Zeichenfolgen für die Anpassung verfügbar. Überschreibungen haben Vorrang vor den Standard-Übersetzungen.

## Tipps

- Beginnen Sie damit, nur die Sprachen zu aktivieren, die Ihre Kunden tatsächlich verwenden — Sie können immer weitere Sprachen später hinzufügen.
- Verwenden Sie das **lokale KI-Modell** für alltägliche Übersetzungen — es ist schnell, privat und hat keine Kosten pro Übersetzung.
- Überlegen Sie sich **DeepL**, wenn Sie die höchste Qualität für wichtige europäische Sprachen benötigen — es erzeugt konsistent natürlichere Übersetzungen als generische Modelle.
- Überprüfen Sie immer **maschinell generierte Übersetzungen** für Produktbezeichnungen, Markenbegriffe und Marketingtexte — KI verarbeitet technischen Inhalt gut, kann aber Nuancen in kreativem Text verfehlen.
- **Sperren** Sie jede Übersetzung, die Sie manuell verfeinert haben, um sie vor dem Überschreiben während Massenübersetzungen zu schützen.
- Verwenden Sie **Massenübersetzungsaufträge**, wenn Sie eine neue Sprache aktivieren, um Ihren gesamten Katalog in einem Durchgang zu übersetzen, anstatt jedes Produkt einzeln zu übersetzen.
- Anpassen Sie **UI-Überschreibungen**, um Ihre Markenstimme zu spiegeln — zum Beispiel, ändern Sie "Add to Cart" in "Buy Now", wenn das besser zu Ihrem Geschäft passt.

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bilddateipfade, Codeblöcke und technischen Begriffe genau so wie in den Erhaltungsvorgaben gezeigt auf.