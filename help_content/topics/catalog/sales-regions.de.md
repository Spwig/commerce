---
title: Verkaufsregionen
---

Verkaufsregionen ermöglichen es Ihnen, geografische Märkte für Ihren Shop zu definieren, und zu steuern, welche Produkte in jeder Region verfügbar sind. Dies ist nützlich, wenn Sie über mehrere Länder oder Gebiete verkaufen und unterschiedliche Produktkataloge, regionale Währungen oder Lagerverfügbarkeit pro Standort benötigen.

## Was ist eine Verkaufsregion?

Eine Verkaufsregion ist ein benanntes geografisches Gebiet, das aus einem oder mehreren Ländern besteht. Jede Region hat eine Standardwährung, eine Priorität und kann mit einem oder mehreren Lagerorten verknüpft sein. Wenn ein Kunde Ihren Shop besucht, ermittelt Spwig seine Region anhand seiner Lage und wendet die entsprechende Währung und Produktverfügbarkeitsregeln an.

Häufige Anwendungsfälle:
- Nur lokal verfügbare Produkte für Kunden in jedem Land anbieten
- Zuweisung von regionsspezifischen Standardwährungen (z. B. NZD für neuseeländische Kunden)
- Steuerung, welche Lager die Bestellungen für jede Region abwickeln
- Produkte verstecken, die in bestimmten Märkten noch nicht verfügbar sind

## Erstellen einer Verkaufsregion

1. Navigieren Sie zu **Lager > Verkaufsregionen**. Wenn Sie es nicht sehen, aktivieren Sie **Mehrfachlager aktivieren** unter **Einstellungen > Store-Einstellungen > E-Commerce**, um das Menü zu aktivieren - Sie müssen für diese Funktion nicht unbedingt mehrere Lager verwenden, es entsperrt nur den Link. Sie können auch direkt zu `/admin/catalog/salesregion/` gehen.
2. Klicken Sie auf **+ Verkaufsregion hinzufügen**
3. Geben Sie die Regiondetails ein:

| Feld | Beschreibung | Beispiel |
|-------|-------------|---------|
| **Regionenname** | Anzeigename für diese Region | `Asien-Pazifik` |
| **Regionencode** | Kurzer eindeutiger Bezeichner | `APAC` |
| **Länder** | ISO-Landcodes, die in dieser Region enthalten sind | `["NZ", "AU", "SG", "FJ"]` |
| **Standardwährung** | ISO-Währungscode für diese Region | `NZD` |
| **Priorität** | Höhere Priorität Regionen werden zuerst zugewiesen | `10` |
| **Aktiv** | Ob diese Region derzeit verwendet wird | Angekreuzt |

4. Klicken Sie auf **Speichern**

### Landescodes

Geben Sie Länder als JSON-Liste der zwei Buchstaben ISO-Codes ein. Zum Beispiel:
- Neuseeland und Australien: `["NZ", "AU"]`
- Nur Singapur: `["SG"]`
- Alle Länder Europas: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorität

Wenn das Land eines Kunden mit mehr als einer Region übereinstimmt, wird die Region mit der höchsten Prioritätsnummer verwendet. Legen Sie eine höhere Priorität für spezifischere Regionen fest (z. B. geben Sie `NZ` eine Priorität von 20 und `APAC` eine Priorität von 10, damit neuseeländische Kunden zuerst der NZ-Region zugeordnet werden).

## Steuern der Produktverfügbarkeit nach Region

Standardmäßig ist jedes Produkt in allen Regionen sichtbar. Um ein Produkt einzuschränkken, öffnen Sie es unter **Produkte > Alle Produkte** und setzen Sie das Feld **Regionenverfügbarkeit** (im Abschnitt Status) entweder, um es nur in bestimmten Regionen zuzulassen oder in allen Regionen außer bestimmten Regionen, und wählen Sie dann die Regionen in der Tabelle unter diesem Feld aus.

Dies bestimmt auch, was Käufer außerhalb der verfügbaren Regionen eines Produkts sehen - ob das Produkt in Listen ganz versteckt wird oder angezeigt wird mit einer "Wird nicht an [Region] versandt"-Meldung. Siehe das **Regionenverfügbarkeits**-Handbuch für den vollständigen Durchlauf, einschließlich dieser Anzeigeeinstellung und des Storefront-Ship-To-Selectors.

## Regionale Währung

Jede Region hat eine Standardwährung. Wenn Ihr Shop explizit mehr als eine Währung unterstützt (**Einstellungen > Mehrere Währungen**), wechselt die angezeigte Währung des Kunden zu der Standardwährung seiner Region, sobald sich seine Region ändert - ob das von der automatischen Regionen-Einladung oder dem Ship-To-Selector stammt. Stores mit nur einer Währung oder die, die bewusst keine Mehrfachwährung aktiviert haben, zeigen immer diese eine Währung unabhängig von der Region an.

Um Preise in mehreren Währungen einzurichten, konfigurieren Sie Wechselkurse unter **Einstellungen > Wechselkurse**. Preise können automatisch konvertiert oder pro Währung manuell festgelegt werden.

## Zuordnen von Lagerorten zu Regionen

Lager werden den Regionen zugeordnet, wenn Sie ein Lager unter **Katalog > Lager** erstellen oder bearbeiten. Jedes Lager gehört einer Region an, wodurch bestimmt wird, welche Lagerbestände für Bestellungen verwendet werden.

Weitere Details zu Lagerhäusern finden Sie im **Bestand und Lagerhäuser**-Hilfethema.

## Tipps

- Halten Sie Regionencodes kurz und beschreibend (NZ, APAC, EU, US) – sie werden intern und in Protokollen verwendet.
- Verwenden Sie höhere Prioritätsnummern für kleinere, spezifischere Regionen, damit sie breiteren Abdeckungsbereichen vorgehen.
- Falls Sie nur in einem Land verkaufen, müssen Sie keine Regionen konfigurieren – Spwig funktioniert mit einem einzigen globalen Katalog problemlos.
- Legen Sie die **Regionenverfügbarkeit** eines Produkts nur dann von **In allen Regionen verfügbar** ab, wenn Sie es tatsächlich einschränken müssen – der Standardwert hält Produkte universell verfügbar, ohne Wartung.
- Prüfen Sie bei jeder Hinzufügung einer neuen Verkaufsregion die Regionenregeln jedes Produkts, damit die Einschränkungen weiterhin mit Ihrem Ziel übereinstimmen.
- Fügen Sie den Ship-To-Selector in Ihre Kopfzeile hinzu (siehe die **Regionenverfügbarkeit**-Anleitung), damit Sie selbst Regionen wechseln und prüfen können, ob eingeschränkte Produkte wie erwartet funktionieren.