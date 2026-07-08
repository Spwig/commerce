---
title: Produktattribute
---

Produktattribute definieren die Dimensionen, entlang derer ein Produkt variieren kann – beispielsweise Größe, Farbe oder Material. Sobald Sie ein Attribut und seine möglichen Werte erstellt haben, können Sie es jedem variablen Produkt zuweisen, und Spwig generiert den Variationsauswahl-Selector, den Kunden beim Checkout verwenden.

Navigieren Sie zu **Katalog > Produktattribute**, um Attribute und deren Werte zu verwalten.

## Wie Attribute funktionieren

Attribute sind über Ihr gesamtes Katalogsystem wiederverwendbar. Sie erstellen sie einmal und weisen sie so vielen Produkten zu, wie benötigt. Jedes Attribut hat:

- Ein **Name**, der es identifiziert (z. B. "Größe")
- Ein **Anzeigetyp**, der bestimmt, wie der Selector auf der Produktseite erscheint
- Einen oder mehrere **Werte**, die die verfügbaren Optionen darstellen (z. B. "Klein", "Mittel", "Groß")

Wenn Sie ein Attribut einem Produkt zuweisen, geben Sie auch an, welche seiner Werte für dieses spezifische Produkt verfügbar sind. Das bedeutet, dass ein "Größe"-Attribut Werte von S bis 3XL haben könnte, aber ein bestimmtes T-Shirt nur S, M und L anbietet.

## Attribut-Anzeigetypen

Das **Typ**-Feld eines Attributs bestimmt, wie der Auswahl-Widget auf der Produktseite Ihres Onlineshops erscheint:

| Typ | Erscheinungsbild | Bestens geeignet für |
|---|---|---|
| **Dropdown-Liste** | Ein Dropdown-Menü, das der Kunde öffnet, um einen Wert auszuwählen | Attribute mit vielen Werten (z. B. eine Größenreihe mit 10+ Größen) |
| **Farb-Vorschau** | Farbige Kreise oder Quadrate, die der Kunde anklickt | Farbattribute, bei denen visuelle Identifizierung hilfreich ist |
| **Schaltflächen-Gruppe** | Knöpfchen, die in einer Zeile angezeigt werden | Attribute mit einer geringen Anzahl an Werten (z. B. S, M, L, XL) |
| **Radiobuttons** | Traditionelle Liste von Radiobuttons | Jedes Attribut, bei dem Sie eine klare, zugängliche Layout-Liste wünschen |

Wählen Sie den Anzeigetyp aus, der am besten zu der Art entspricht, wie Ihre Kunden das Attribut wahrnehmen. Bei Farben sind Vorschau-Elemente fast immer besser als ein Dropdown. Bei Größen funktionieren Schaltflächen-Gruppen gut, wenn weniger als 8 Optionen vorhanden sind.

## Ein Attribut erstellen

1. Navigieren Sie zu **Katalog > Produktattribute**
2. Klicken Sie auf **+ Produktattribut hinzufügen**
3. Geben Sie den **Namen** ein (z. B. `Größe`, `Farbe`, `Material`)
4. Das **Slug** wird automatisch ausgefüllt – Sie können es so lassen, wie es ist
5. Wählen Sie den **Typ** (Dropdown, Farb-Vorschau, Schaltflächen-Gruppe oder Radiobuttons)
6. Aktivieren Sie **Pflichtfeld**, wenn Kunden dieses Attribut auswählen müssen, bevor sie das Produkt in den Warenkorb legen – dies ist für die meisten Größen- und Farbattribute geeignet
7. Legen Sie eine **Sortierreihenfolge** fest – Attribute mit niedrigeren Zahlen erscheinen zuerst im Variationsauswahl-Selector auf der Produktseite
8. Fügen Sie Attributwerte direkt im **Werte**-Abschnitt hinzu (siehe unten)
9. Klicken Sie auf **Speichern**

## Attribute-Werte hinzufügen

Attribute-Werte sind die einzelnen Optionen innerhalb eines Attributs. Sie können sie direkt beim Erstellen oder Bearbeiten eines Attributs hinzufügen, indem Sie das Inline-Werte-Formular am unteren Ende der Attribut-Detailsseite verwenden.

Für jeden Wert:

- **Wert** – das Anzeigelabel (z. B. `Klein`, `Rot`, `Baumwolle`)
- **Slug** – wird automatisch aus dem Wert gefüllt; wird in URLs und Variantenbezeichnungen verwendet
- **Farb-HEX** – nur für **Farb-Vorschau**-Typ-Attribute relevant. Geben Sie eine Hex-Farbcodierung ein (z. B. `#FF0000` für Rot), damit die Vorschau die richtige Farbe anzeigt.
- **Sortierreihenfolge** – bestimmt die Reihenfolge, in der die Werte im Selector angezeigt werden. Weisen Sie niedrigere Zahlen den Werten zu, die zuerst angezeigt werden sollen.

### Werte logisch sortieren

Für Größe-Attribute legen Sie die Sortierreihenfolge so fest, dass die Größen von klein nach groß laufen:

| Wert | Sortierreihenfolge |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Für Farbattribute können Sie alphabetisch sortieren oder ähnliche Farben zusammengruppen – was für Ihre Kunden am meisten Sinn ergibt.

## Attribute-Werte unabhängig verwalten

Sie können Attribute-Werte auch unabhängig verwalten, indem Sie zu **Katalog > Attribute-Werte** navigieren. Diese Liste ist nützlich, wenn Sie einen bestimmten Wert in Ihrem Katalog suchen oder aktualisieren müssen, ohne jedes Attribut einzeln zu öffnen. Die Liste kann nach Attributnamen gefiltert werden.

## Attribute zu Produkten zuweisen

Attribute werden auf der Produktstufe zugewiesen, nicht global.

Um ein Attribut einem Produkt hinzuzufügen:

1. Navigieren Sie zu **Katalog > Produkte** und öffnen Sie ein variierbares Produkt
2. Im Reiter **Variationen** finden Sie den Abschnitt **Attribute**
3. Wählen Sie das Attribut aus, das Sie hinzufügen möchten
4. Wählen Sie die Werte des Attributs aus, die für dieses Produkt verfügbar sein sollen
5. Speichern Sie das Produkt – Spwig generiert die entsprechenden Variantenkombinationen

Für detaillierte Anweisungen zur Einrichtung von Produktvarianten, siehe das Hilfethema **Produktvarianten**.

## Praktische Beispiele

### Beispiel: Attribut für Kleidungsgröße

| Feld | Wert |
|---|---|
| Name | Größe |
| Typ | Knopfgruppe |
| Erforderlich | Ja |
| Sortierreihenfolge | 1 |
| Werte | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Beispiel: Farbverlauf-Attribut

| Feld | Wert |
|---|---|
| Name | Farbe |
| Typ | Farbverlauf |
| Erforderlich | Ja |
| Sortierreihenfolge | 2 |
| Werte | Schwarz (#000000), Weiß (#FFFFFF), Marineblau (#001F5B), Rot (#CC0000) |

### Beispiel: Materialattribut

| Feld | Wert |
|---|---|
| Name | Material |
| Typ | Dropdown-Liste |
| Erforderlich | Nein |
| Sortierreihenfolge | 3 |
| Werte | 100 % Baumwolle, Baumwoll/Polyester-Mischung, Merinowolle, Leinen |

## Tipps

- Erstellen Sie Attribute, die echte Kaufentscheidungen der Kunden darstellen – wenn Kunden es nicht auswählen müssen, braucht es möglicherweise kein Attribut zu sein
- Verwenden Sie konsistente Benennung im gesamten Katalog: wenn einige Produkte „Farbe“ und andere „Colour“ verwenden, können Kunden und Ihr Team die Inkonsistenz verwirrend finden
- Die Sortierreihenfolge sowohl für Attribute als auch für Werte ist wichtig – setzen Sie das wichtigste Attribut an erster Stelle (meist Größe oder Farbe) und ordnen Sie die Werte in einer logischen Reihenfolge an
- Der Typ Farbverlauf erfordert genaue Hex-Code-Werte; testen Sie die Farben in einem Browser-Farbauswahlfeld, bevor Sie sie speichern, um sicherzustellen, dass der Farbverlauf der tatsächlichen Produktfarbe entspricht
- Wenn Sie ein Attribut umbenennen müssen (z. B. von „Color“ zu „Colour“), aktualisieren Sie das Feld **Name** anstelle eines neuen Attributs zu erstellen – das Ändern des Namens hat keinen Einfluss auf bestehende Produktzuordnungen