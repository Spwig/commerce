---
title: Verkaufsregionen
---

Verkaufsregionen ermöglichen es Ihnen, geografische Märkte für Ihr Geschäft zu definieren und zu steuern, welche Produkte in jeder Region verfügbar sind. Dies ist nützlich, wenn Sie in mehreren Ländern oder Gebieten tätig sind und unterschiedliche Produktkataloge, regionale Währungen oder Lagerverfügbarkeiten pro Standort benötigen.

## Was ist eine Verkaufsregion?

Eine Verkaufsregion ist ein benannter geografischer Bereich, der aus einem oder mehreren Ländern besteht. Jede Region hat eine Standardwährung, eine Priorität und kann mit einem oder mehreren Lagerhäusern verknüpft werden. Wenn ein Kunde in Ihrem Geschäft stöbert, bestimmt Spwig seine Region anhand seiner Standortdaten und wendet die entsprechenden Währungs- und Produkt-Sichtbarkeitsregeln an.

Häufige Anwendungsfälle:
- Nur lokal verfügbare Produkte für Kunden in jedem Land anzeigen
- Regionenspezifische Standardwährungen zuweisen (z. B. NZD für Kunden aus Neuseeland)
- Steuern, welche Lagerhäuser Bestellungen für jede Region erfüllen
- Produkte ausblenden, die in bestimmten Märkten noch nicht verfügbar sind

## Erstellen einer Verkaufsregion

1. Navigieren Sie zu **Katalog > Verkaufsregionen**
2. Klicken Sie auf **+ Verkaufsregion hinzufügen**
3. Füllen Sie die Region-Details aus:

| Feld | Beschreibung | Beispiel |
|-------|-------------|---------|
| **Regionenname** | Anzeigename für diese Region | `Asia-Pacific` |
| **Regionencode** | Kurze eindeutige Kennung | `APAC` |
| **Länder** | ISO-Ländercodes, die in dieser Region enthalten sind | `["NZ", "AU", "SG", "FJ"]` |
| **Standardwährung** | ISO-Währungscode für diese Region | `NZD` |
| **Priorität** | Regionen mit höherer Priorität werden zuerst abgeglichen | `10` |
| **Aktiv** | Ob diese Region derzeit in Gebrauch ist | Angekreuzt |

4. Klicken Sie auf **Speichern**

### Ländercodes

Geben Sie Länder als JSON-Liste aus zwei Buchstaben ISO-Codes an. Beispiel:
- Neuseeland und Australien: `["NZ", "AU"]`
- Nur Singapur: `["SG"]`
- Alle Europäischen Länder: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorität

Wenn ein Kundenland mehreren Regionen entspricht, wird die Region mit der höchsten Prioritätsnummer verwendet. Setzen Sie eine höhere Priorität für spezifischere Regionen (z. B. geben Sie `NZ` eine Priorität von 20 und `APAC` eine Priorität von 10, damit Kunden aus Neuseeland zuerst der NZ-Region zugeordnet werden).

## Produkt-Sichtbarkeit nach Region steuern

Standardmäßig ist jedes Produkt in allen Regionen sichtbar. Um ein Produkt auf bestimmte Regionen zu beschränken, verwenden Sie **Produkt-Region-Sichtbarkeit**-Einträge.

### Ein Produkt auf bestimmte Regionen beschränken

1. Navigieren Sie zu **Katalog > Produkt-Region-Sichtbarkeit**
2. Klicken Sie auf **+ Produkt-Region-Sichtbarkeit hinzufügen**
3. Wählen Sie das **Produkt** aus
4. Wählen Sie die **Region** aus
5. Setzen Sie **Sichtbar** auf an oder aus, je nach Bedarf
6. Klicken Sie auf **Speichern**

Sobald für ein Produkt eine Sichtbarkeitseintrag vorhanden ist, wendet Spwig die Regeln an. Produkte ohne Sichtbarkeitseinträge bleiben überall sichtbar.

### Häufige Muster

**Nur eine Region zulassen**

Fügen Sie einen Sichtbarkeitseintrag pro Region hinzu, für die Sie Unterstützung wünschen, und setzen Sie **Sichtbar** auf `Ja` für die erlaubten Regionen. Kunden aus anderen Regionen werden das Produkt nicht sehen.

**Aus einer Region ausschließen**

Fügen Sie einen einzelnen Sichtbarkeitseintrag für die Region hinzu, die Sie ausschließen möchten, und setzen Sie **Sichtbar** auf `Nein`. Das Produkt bleibt in allen anderen Regionen sichtbar.

### Sichtbarkeit von der Produktseite bearbeiten

Sie können auch die Regionensichtbarkeit direkt von der Produktbearbeitungsformular aus verwalten. Auf dem **Regionensichtbarkeit**-Abschnitt des Produkts finden Sie eine Inline-Tabelle, die alle Regionen und deren Sichtbarkeitseinstellungen für dieses Produkt anzeigt.

## Regionale Währung

Jede Region hat eine Standardwährung. Kunden, die aus dieser Region stammen, sehen Preise in der Währung der Region angezeigt. Die verwendete Währung wird zur Kasse bestimmt.

Um Preise in mehreren Währungen einzurichten, konfigurieren Sie Wechselkurse unter **Einstellungen > Wechselkurse**. Preise können automatisch konvertiert werden oder manuell pro Währung festgelegt werden.

## Lagerhäuser mit Regionen verknüpfen

Lagerhäuser werden mit Regionen verknüpft, wenn Sie ein Lagerhaus erstellen oder bearbeiten, unter **Katalog > Lagerhäuser**. Jedes Lagerhaus gehört zu einer Region, die bestimmt, welche Lagerbestände zur Erfüllung von Bestellungen verwendet werden.

Für weitere Details zu Lagerhäusern siehe das **Hilfethema zu Lagerbeständen und Lagerhäusern**.

## Tipps

- Halten Sie Regionscodes kurz und beschreibend (`NZ`, `APAC`, `EU`, `US`) — sie werden intern und in Protokollen verwendet.
- Verwenden Sie höhere Prioritätszahlen für kleinere, spezifischere Regionen, damit sie Vorrang vor breiteren Allzweckregionen haben.
- Wenn Sie nur in einem Land verkaufen, müssen Sie Regionen überhaupt nicht konfigurieren — Spwig funktioniert gut mit einem einzigen globalen Katalog.
- Testen Sie die regionenbasierte Sichtbarkeit, indem Sie Ihr Geschäft vorab ansehen, während Sie im Admin eine bestimmte Region filtern.
- Produkt-Sichtbarkeitsdatensätze müssen nur erstellt werden, wenn Sie Produkte einschränken möchten. Ein Produkt ohne Sichtbarkeitsdatensätze ist universell verfügbar.
- Überprüfen Sie Ihre Sichtbarkeitsregeln immer, wenn Sie eine neue Region hinzufügen, um sicherzustellen, dass bestehende Produktbeschränkungen korrekt sind.