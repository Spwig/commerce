---
title: Bulk-Bestandshandlungen
---

Zusätzlich zu Einzelanpassungen bietet Spwig Ihnen drei Bulk-Aktionen auf der **Bestandselemente**-Liste für die Lagerverwaltungsarbeiten, die gleichzeitig für viele Produkte durchgeführt werden: Verschieben von Lagerbestand zwischen Lagerhallen, Schreiben von beschädigten oder verlorenen Einheiten ab und Abstimmung des Lagerbestands nach einer physischen Zählung. Alle drei Aktionen laufen über dasselbe **Aktionen**-Dropdown-Menü, wenden dieselbe Menge auf jedes ausgewählte Bestandselement an und werden vollständig in der Audit-Liste für Lagerbewegungen protokolliert.

Gehen Sie zu **Produkte > Bestandselemente**, um sie zu verwenden.

## Ausführen einer Bulk-Bestandshandlung

1. Auf der **Bestandselemente**-Liste verwenden Sie die Filter oder die Suche, um die Artikel zu finden, die Sie aktualisieren möchten
2. Klicken Sie das Kästchen neben jedem Bestandselement an, um es einzuschließen (oder verwenden Sie das Kästchen in der Kopfzeile, um alle Elemente auf der Seite auszuwählen)
3. Wählen Sie eine der drei Aktionen aus dem **Aktionen**-Dropdown-Menü:
   - **Lagerbestand in Lagerhaus verschieben**
   - **Beschädigten/verlorenen Lagerbestand protokollieren**
   - **Lagerbestand neu zählen (physische Zählung)**
4. Auf **Los** klicken
5. Bestätigungsseite prüfen — sie listet jedes ausgewählte Bestandselement mit seinen aktuellen **vorhandenen**, **zugeordneten** und **verfügbaren** Mengen auf, damit Sie überprüfen können, ob Sie die richtigen Elemente ausgewählt haben
6. Die Felder der Aktion ausfüllen (siehe unten) und auf den Absenden-Button klicken, um die Aktion anzuwenden

![Die Liste der Bestandselemente mit dem geoeffneten Bulk-Aktionen-Dropdown, wobei "Lagerbestand in Lagerhaus verschieben", "Beschädigten/verlorenen Lagerbestand protokollieren" und "Lagerbestand neu zählen (physische Zählung)" neben den anderen Aktionen angezeigt werden](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Der gleiche Wert, den Sie eingeben, wird auf **jedes** ausgewählte Element angewandt — dies ist für das Verschieben, Schreiben ab oder Neu-zählen derselben Anzahl von Einheiten für viele SKUs gleichzeitig gedacht (z. B. Verschieben von 10 Einheiten mehrerer Produkte in eine neue Ladenfiliale). Für ein einzelnes Element mit einer anderen Menge führen Sie die Aktion erneut mit nur diesem Element ausgewählt, oder verwenden Sie stattdessen **Bestandsebenen anpassen**.

## Lagerbestand in Lagerhaus verschieben

Verwenden Sie dies, um verfügbaren Bestand aus jedem ausgewählten Elements Lagerhaus in ein anderes Lagerhaus zu verschieben — z. B. Restocken einer neuen Einzelhandelsfiliale aus Ihrem Hauptlager oder Umverteilung des Lagerbestands zwischen regionalen Fulfillment-Centern.

Auf der Bestätigungsseite füllen Sie folgende Felder aus:

| Feld | Beschreibung |
|-------|-------------|
| **Ziel-Lagerhaus** | Wo der Bestand hingehen sollte. Nur aktive Lagerhäuser werden in dieser Liste angezeigt. |
| **Menge pro Artikel** | Einheiten, die aus dem aktuellen Lagerhaus jedes ausgewählten Elements herausgenommen werden. |
| **Grund** | Optionaler Hinweis, z. B. "Restocken der neuen Auckland-Filiale". |

Auf **Lagerbestand verschieben** klicken, um anzuwenden.

![Die Seite zur Bestätigung des Lagerbestandsverschiebens: ein Karten-Widget für ausgewählte Lagerbestandselemente mit ihren Werten für "vorhanden", "zugeordnet" und "verfügbar", und ein Formular für die Verschiebungsdaten mit einem Ziel-Lagerhaus, Menge und Grund, der ausgefüllt ist](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Nur unreservierter Bestand kann verschoben werden.** Spwig verschiebt von *verfügbarem* Bestand (vorhanden minus Einheiten, die auf offene Bestellungen zugewiesen wurden) — Einheiten, die bereits einem Kundenbestellvorgang zugeordnet sind, bleiben im Quell-Lagerhaus, damit dieser Bestellvorgang weiterhin erledigt werden kann. Wenn ein ausgewähltes Element nicht genug verfügbaren Bestand hat, um die Menge zu decken, die Sie eingegeben haben, wird dieses Element ausgelassen und ein Fehler erklärt, warum; der Rest der Auswahl wird dennoch übertragen.

Wenn ein ausgewähltes Element bereits im Ziel-Lagerhaus, das Sie gewählt haben, gelagert wird, wird es automatisch ausgelassen (es ist nichts zu übertragen, um sich selbst), und Sie sehen eine Nachricht, die Ihnen mitteilt, wie viele Elemente aus diesem Grund ausgelassen wurden.

Jeder Verschiebung wird ein Paar von Bewegungen in der Audit-Liste geschrieben — eine negative **Lagerhaus-Transfer**-Eintragung am Ursprung und eine entsprechende positive Eintragung am Ziel — sodass die vollständige Liste genau angibt, wo der Bestand herkam und wohin er ging.

## Beschädigten/verlorenen Lagerbestand protokollieren

Verwenden Sie dies, um Einheiten zu schreiben, die beschädigt, verdorben oder verloren gegangen sind — z. B. nachdem beschädigte Waren in einer Lieferung gefunden oder eine Diskrepanz untersucht wurden.

Auf der Bestätigungsseite füllen Sie folgende Felder aus:

| Field | Description |
|-------|-------------|
| **Quantity to write off (per item)** | Units to remove from on-hand stock for each selected item. |
| **Reason** | Optional note, e.g. "Water damage during storage". |

Click **Record Write-off** to apply.

**Reserved stock can't be written off.** On-hand stock can never drop below the quantity currently allocated to open orders — Spwig blocks the write-off for any item where the quantity you entered would eat into allocated stock, so you can't accidentally leave a paid order without the stock to fulfill it. If that happens for an item, you'll see an error naming the item and how many unreserved units it actually has available to write off.

Each write-off is recorded as a **Damaged/Lost** movement on that stock item, with a negative quantity.

## Recount stock (physical count)

Use this after a physical stock take to correct on-hand quantities to match what you actually counted — the fastest way to reconcile many items after a warehouse audit or cycle count.

On the confirmation page, fill in:

| Field | Description |
|-------|-------------|
| **Counted on-hand quantity (per item)** | The quantity you physically counted. On-hand is set to this exact number for every selected item — not added or subtracted. |
| **Reason** | Optional note, e.g. "Q3 warehouse stock take". |

Click **Apply Recount** to apply.

![The Recount Stock confirmation page: the Selected Stock Items card and a Recount Details form with the counted on-hand quantity and a reason filled in](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Unlike the other two actions, recount can move stock in either direction — up if you counted more than the system expected, down if you counted less. If the count you enter is lower than the quantity currently allocated to open orders, Spwig still applies it (a count is a fact, not something to argue with), but that item's **Available** figure will show as `0` on the stock list and its status icon will flip to Out of Stock — treat that as a signal to check whether the affected orders can still be fulfilled.

Each recount is recorded as a **Physical Recount** movement, with the quantity showing the correction (positive or negative) between the old and new on-hand figures.

## Reviewing what changed

Every transfer, write-off, and recount is logged the same way as any other stock change:

- Open a stock item and scroll to the **Stock Movements** section to see its full history
- Or navigate to **Products > Stock Movements** to browse movements across all items, filterable by type

Each entry records the movement type, the quantity change, the previous and new on-hand figures, who made the change, and the reason you entered (if any) — so a bulk transfer or write-off is just as traceable as a single manual adjustment.

## Tips

- Run **Recount stock** right after a physical stock take while the counted numbers are fresh — it's easier to catch a typo in the confirmation page than to untangle it later from the movement history.
- Always fill in **Reason** for write-offs and recounts. Six months from now, "Water damage during storage" is far more useful in the audit trail than a blank field.
- Before transferring stock, check the **Available** column on the confirmation page — it already accounts for allocated units, so you'll know immediately if a quantity is too high for one of the items you selected.
- These actions apply the same quantity to every selected item. Group your selection by items that genuinely need the same quantity moved, written off, or recounted, and handle exceptions one item at a time.
- If you use POS at a retail location, remember that warehouse's stock buffer isn't part of "available" for online orders — but bulk transfers and write-offs still work against the warehouse's real on-hand total.