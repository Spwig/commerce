---
title: Bulk-Bestandshandlungen
---

Zusätzlich zu Einzelanpassungen bietet Spwig Ihnen drei Bulk-Aktionen auf der **Bestandselemente**-Liste für Arbeiten am Lagerbestand, die gleichzeitig für viele Produkte durchgeführt werden: Verschieben des Bestands zwischen Lagerhäusern, Schreiben von beschädigten oder verlorenen Einheiten ab und Abstimmung des Bestands nach einer physischen Zählung. Alle drei Aktionen stammen aus dem gleichen **Aktionen**-Dropdown, wenden Sie den gleichen Betrag auf jedes ausgewählte Bestandselement an und werden vollständig in der Audit-Trail für Bestandsbewegungen protokolliert.

Navigieren Sie zu **Produkte > Bestandselemente**, um sie zu verwenden.

## Ausführen einer Bulk-Bestandshandlung

1. Auf der **Bestandselemente**-Liste verwenden Sie die Filter oder die Suche, um die Elemente zu finden, die Sie aktualisieren möchten
2. Klicken Sie auf das Kästchen neben jedem Bestandselement, um es einzuschließen (oder verwenden Sie das Kästchen in der Überschrift, um alle Elemente auf der Seite auszuwählen)
3. Wählen Sie eine der drei Aktionen aus dem **Aktionen**-Dropdown:
   - **Bestand an Lagerhaus verschieben**
   - **Beschädigten/verlorenen Bestand protokollieren**
   - **Bestand neu zählen (physische Zählung)**
4. Auf **Los** klicken
5. Bestätigungsseite prüfen — sie listet jedes ausgewählte Bestandselement mit seinem aktuellen **vorhandenen**, **zugewiesenen** und **verfügbaren** Bestand auf, damit Sie überprüfen können, ob Sie die richtigen Elemente ausgewählt haben
6. Die Felder der Aktion ausfüllen (siehe unten) und auf den Absenden-Button klicken, um die Aktion anzuwenden

![Die Liste der Bestandselemente mit geöffnetem Bulk-Aktionen-Dropdown, wobei die Optionen "Bestand an Lagerhaus verschieben", "Beschädigten/verlorenen Bestand protokollieren" und "Bestand neu zählen (physische Zählung)" neben den anderen Aktionen angezeigt werden](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Der gleiche Betrag, den Sie eingeben, wird auf **jedes** ausgewählte Element angewandt — dies ist dafür gedacht, die gleiche Anzahl von Einheiten über viele SKUs hinweg zu verschieben, zu schreiben oder neu zu zählen (z. B. das Verschieben von 10 Einheiten mehrerer Produkte in eine neue Ladenfiliale). Für ein einzelnes Element mit einem anderen Betrag führen Sie die Aktion erneut mit nur diesem Element aus oder verwenden Sie stattdessen **Bestandsebenen anpassen**.

## Bestand an Lagerhaus verschieben

Verwenden Sie dies, um verfügbaren Bestand aus jedem ausgewählten Elements Lagerhaus in ein anderes Lagerhaus zu verschieben — z. B. um ein neues Einzelhandelsstandort zu restocken, von Ihrem Hauptlager aus, oder um das Lager zwischen regionalen Fulfillment-Centern zu balancieren.

Auf der Bestätigungsseite füllen Sie Folgendes aus:

| Feld | Beschreibung |
|-------|-------------|
| **Ziel-Lagerhaus** | Wohin der Bestand verschoben werden soll. Nur aktive Lagerhäuser werden in dieser Liste angezeigt. |
| **Menge pro Artikel** | Einheiten, die aus dem aktuellen Lagerhaus jedes ausgewählten Elements herausgenommen werden. |
| **Grund** | Optionaler Hinweis, z. B. "Restocking neues Auckland-Lager". |

Auf **Bestand verschieben** klicken, um anzuwenden.

![Die Seite zur Bestätigungsseite für "Bestand verschieben": ein Karten-Widget mit drei Elementen, die ihre Angaben zu "vorhanden", "zugewiesen" und "verfügbar" aufweisen, und ein Formular "Verschiebungsdetails" mit einem Ziel-Lagerhaus, Menge und Grund, die ausgefüllt sind](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Nur unreservierter Bestand kann verschoben werden.** Spwig verschiebt von *verfügbarem* Bestand (vorhanden minus Einheiten, die für offene Bestellungen zugewiesen wurden) — Einheiten, die bereits einem Kundenbestellvorgang versprochen wurden, bleiben im Quell-Lager, damit dieser Bestellvorgang weiterhin erfüllt werden kann. Wenn ein ausgewähltes Element nicht genug verfügbaren Bestand hat, um die Menge zu decken, die Sie eingegeben haben, wird dieses Element übersprungen und eine Fehlermeldung erläutert, warum; der Rest der Auswahl wird dennoch übertragen.

Wenn ein ausgewähltes Element bereits im von Ihnen gewählten Ziel-Lagerhaus gelagert wird, wird es automatisch übersprungen (es ist nichts zu verschieben), und Sie erhalten eine Nachricht, die Ihnen mitteilt, wie viele Elemente aus diesem Grund übersprungen wurden.

Jeder Verschiebung wird ein Paar von Bewegungen in der Audit-Trail geschrieben — eine negative **Lagerhaus-Übertragung** im Quell-Lager und eine entsprechende positive im Ziel-Lager — sodass die vollständige Trail genau zeigt, wo der Bestand herkam und wohin er ging.

## Beschädigten/verlorenen Bestand protokollieren

Verwenden Sie dies, um Einheiten zu schreiben, die beschädigt, verdorben oder verloren gegangen sind — z. B. nachdem beschädigte Waren in einer Lieferung gefunden oder eine Diskrepanz untersucht wurden.

Auf der Bestätigungsseite füllen Sie Folgendes aus:

| Feld | Beschreibung |
|-------|-------------|
| **Abzuschreibende Menge (pro Artikel)** | Einheiten, die für jeden ausgewählten Artikel vom Lagerbestand entfernt werden. |
| **Grund** | Optionale Notiz, z. B. "Wasserschaden während der Lagerung". |

Klicken Sie auf **Abschreibung buchen**, um die Aktion anzuwenden.

**Reservierter Bestand kann nicht abgeschrieben werden.** Der Lagerbestand kann niemals unter die Menge fallen, die derzeit offenen Bestellungen zugewiesen ist – Spwig blockiert die Abschreibung für jeden Artikel, bei dem die eingegebene Menge in den zugewiesenen Bestand eingreifen würde, damit Sie versehentlich keine bezahlte Bestellung ohne den Bestand zur Erfüllung lassen. Falls dies bei einem Artikel der Fall ist, sehen Sie einen Fehler, der den Artikel benennt und wie viele nicht reservierte Einheiten tatsächlich für die Abschreibung verfügbar sind.

Jede Abschreibung wird als **Beschädigt/Verloren**-Bewegung für diesen Lagerartikel mit einer negativen Menge erfasst.

## Bestand neu zählen (physische Zählung)

Verwenden Sie dies nach einer physischen Bestandsaufnahme, um die Lagerbestandsmengen so zu korrigieren, dass sie mit dem übereinstimmen, was Sie tatsächlich gezählt haben – der schnellste Weg, um viele Artikel nach einer Lagerprüfung oder Zykluszählung abzugleichen.

Füllen Sie auf der Bestätigungsseite Folgendes aus:

| Feld | Beschreibung |
|-------|-------------|
| **Gezählter Lagerbestand (pro Artikel)** | Die Menge, die Sie physisch gezählt haben. Der Lagerbestand wird für jeden ausgewählten Artikel auf genau diese Zahl gesetzt – nicht addiert oder subtrahiert. |
| **Grund** | Optionale Notiz, z. B. "Q3-Lagerbestandsaufnahme". |

Klicken Sie auf **Neuzählung anwenden**, um die Aktion anzuwenden.

![Die Bestätigungsseite für die Bestandsneuzählung: die Karte "Ausgewählte Lagerartikel" und ein Formular "Neuzählungsdetails" mit der gezählten Lagerbestandsmenge und einem Grund ausgefüllt](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Im Gegensatz zu den anderen beiden Aktionen kann die Neuzählung den Bestand in beide Richtungen bewegen – nach oben, wenn Sie mehr gezählt haben als das System erwartet hat, nach unten, wenn Sie weniger gezählt haben. Wenn die eingegebene Zählung niedriger ist als die Menge, die derzeit offenen Bestellungen zugewiesen ist, wendet Spwig sie dennoch an (eine Zählung ist eine Tatsache, mit der man nicht streiten kann), aber die **Verfügbar**-Zahl für diesen Artikel wird in der Lagerliste als `0` angezeigt und sein Statussymbol wechselt zu "Ausverkauft" – betrachten Sie dies als Signal, zu prüfen, ob die betroffenen Bestellungen noch erfüllt werden können.

Jede Neuzählung wird als **Physische Neuzählung**-Bewegung erfasst, wobei die Menge die Korrektur (positiv oder negativ) zwischen den alten und neuen Lagerbestandszahlen zeigt.

## Überprüfung der Änderungen

Jede Übertragung, Abschreibung und Neuzählung wird auf dieselbe Weise protokolliert wie jede andere Lagerbewegung:

- Öffnen Sie einen Lagerartikel und scrollen Sie zum Abschnitt **Lagerbewegungen**, um die vollständige Historie anzuzeigen
- Oder navigieren Sie zu **Produkte > Lagerbewegungen**, um Bewegungen über alle Artikel hinweg zu durchsuchen, filterbar nach Typ

Jeder Eintrag erfasst den Bewegungstyp, die Mengenänderung, die vorherigen und neuen Lagerbestandszahlen, wer die Änderung vorgenommen hat und den Grund, den Sie eingegeben haben (falls vorhanden) – so ist eine Massenübertragung oder Abschreibung genauso nachvollziehbar wie eine einzelne manuelle Anpassung.

## Tipps

- Führen Sie **Bestand neu zählen** direkt nach einer physischen Bestandsaufnahme aus, während die gezählten Zahlen noch frisch sind – es ist einfacher, einen Tippfehler auf der Bestätigungsseite zu erkennen, als ihn später aus der Bewegungshistorie zu entwirren.
- Füllen Sie für Abschreibungen und Neuzählungen immer das Feld **Grund** aus. In sechs Monaten ist "Wasserschaden während der Lagerung" in der Audit-Trail deutlich nützlicher als ein leeres Feld.
- Prüfen Sie vor einer Bestandsübertragung die Spalte **Verfügbar** auf der Bestätigungsseite – sie berücksichtigt bereits die zugewiesenen Einheiten, sodass Sie sofort wissen, ob eine Menge für einen der ausgewählten Artikel zu hoch ist.

- Diese Aktionen wenden dieselbe Menge für jeden ausgewählten Artikel an. Gruppieren Sie Ihre Auswahl nach Artikeln, die tatsächlich dieselbe Menge bewegt, abgeschrieben oder neu gezählt werden müssen, und behandeln Sie Ausnahmen Artikel für Artikel.
- Wenn Sie an einem Einzelhandelsstandort POS verwenden, denken Sie daran, dass der Lagerpuffer des Lagers nicht Teil der "verfügbaren" Menge für Online-Bestellungen ist – aber Massenübertragungen und Abschreibungen funktionieren weiterhin gegen die tatsächliche Lagerbestandsmenge des Lagers.