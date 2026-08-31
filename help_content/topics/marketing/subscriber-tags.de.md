---
title: Abonnententags
---

Tags sind Ihre eigenen Bezeichnungen, um Ihre Zielgruppe im Campaign Studio zu organisieren – kurze Markierungen wie `VIP`, `Großhandel` oder `Ereignis-2026`, die Sie definieren und auf diejenigen anwenden, die passen. Sobald ein Tag existiert, können Sie Ihre Liste der Abonnenten danach filtern, es auf beliebig viele Personen gleichzeitig anwenden oder entfernen und – am nützlichsten – es als Bedingung verwenden, wenn Sie einen Segment erstellen, damit Ihre Kampagnen und Journeys genau die Personen ansprechen können, die Sie markiert haben.

## Was sind Tags?

Ein Tag ist nichts anderes als ein Name, den Sie wählen. Spwig verfügt nicht über vordefinierte Tags, und er wendet einen Tag niemals automatisch an – Sie entscheiden, wie sie heißen und wer einen bekommt. Das macht sie zu einer guten Ergänzung für alles, was spezifisch für Ihr eigenes Unternehmen ist und nicht zu einem Status passt, den Spwig bereits verfolgt: eine Treuestufe, ein Großhandelskonto, alle, die an einer Messe angemeldet wurden, oder eine Einzelveranstaltungsliste wie `Ereignis-2026`.

Jeder Tag erhält auch ein **Slug** – eine vereinfachte, URL-freundliche Version seines Namens – das automatisch generiert wird, sobald Sie ihn erstellen. Segmente und Filter verwenden den Slug intern; als Händler werden Sie fast nie das Bedürfnis haben, ihn anzusehen.

## Ein Tag erstellen

Tags haben einen eigenen Admin-Bereich. Öffnen Sie **Campaign Studio > Abonnenten** und klicken Sie oben auf der Seite auf **Campaign Studio**, um die vollständige Liste der Campaign-Studio-Bereiche anzuzeigen, und wählen Sie **Abonnententags**.

1. Klicken Sie auf **Neues Abonnententag hinzufügen**.
2. Geben Sie einen **Namen** ein – kürzere und spezifischere Namen sind am besten, z. B. `VIP`, `Großhandel` oder `Ereignis 2026`.
3. Spwig füllt ein passendes **Slug** aus, während Sie tippen. Sie können es so lassen, wie es generiert wurde.
4. Ein optionales **Farbfeld** ist ebenfalls verfügbar, falls Sie eine Hexadezimalfarbe (z. B. `#2563eb`) gegen den Tag aufzeichnen möchten, für Ihre eigene Referenz.
5. Klicken Sie auf **Speichern**.

Sie müssen nicht auf das aufhören, was Sie gerade tun, um eines zu erstellen – ein grünes **+** neben dem **Tags**-Feld auf der Bearbeitungsseite eines Abonnenten öffnet das gleiche "Tag hinzufügen"-Formular in einem Popup. Und wenn Sie versuchen, Abonnenten vor der Erstellung eines Tags überhaupt zu taggen, bietet der Tag-Auswahlfeld einen **Tag erstellen**-Shortcut, der Sie direkt dorthin bringt.

## Abonnenten taggen

Die gängigste Methode, um einen Tag anzuwenden, ist in der Massenverarbeitung, aus der Liste der Abonnenten:

1. Öffnen Sie **Campaign Studio > Abonnenten**.
2. Klicken Sie auf das Kontrollkästchen neben jedem Abonnenten, den Sie markieren möchten (oder **Alle auf dieser Seite auswählen**).
3. Wählen Sie aus dem **Massenaktionen**-Dropdown **Tag zu ausgewählten hinzufügen** (oder **Tag von ausgewählten entfernen**, um Leute zu enttaggen).
4. Klicken Sie auf **Go**.
5. Wählen Sie den Tag aus der Liste aus und klicken Sie auf **Tag hinzufügen** (oder **Tag entfernen**).

![Der Massen-Tag-Auswahlfeld nach der Auswahl von "Tag zu ausgewählten hinzufügen" für vier Abonnenten](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Sobald angewandt, wird ein Tag als kleines Chip-Element auf dem Karten-Abonnenten in der Liste neben ihrem Status und Quellensymbol angezeigt. Ein **Tag**-Filter erscheint auch im Filterpanel der Abonnentenliste, sobald Sie mindestens einen Tag haben, damit Sie die Liste auf alle Abonnenten mit einem bestimmten Tag eingrenzen können – praktisch, um zu prüfen, wer in einer Zielgruppe ist, bevor Sie eine Kampagne darum herum aufbauen.

![Die Abonnentenliste, gefiltert auf den VIP-Tag, mit dem Import-CSV-Button und Tag-Chips sichtbar](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Sie können auch direkt von der Bearbeitungsseite eines einzelnen Abonnenten Tags hinzufügen oder entfernen, indem Sie dasselbe **Tags**-Feld verwenden, das die Massenaktion verwaltet.

## Tags in Segmenten verwenden

Segmente sind die gespeicherten, regelbasierten Zielgruppen, auf die Sie Kampagnen und Journeys ausrichten. Sobald Sie mindestens einen Tag erstellt haben, wird eine **Hat Tag**-Bedingung im Segment-Regel-Builder verfügbar – sie erscheint nicht bei einer frischen Installation ohne definierte Tags, also werden Sie keine tote Option sehen, bevor sie für Sie nützlich ist.

Um sie zu verwenden, öffnen Sie **Campaign Studio > Segmente**, fügen Sie (oder bearbeiten Sie) ein dynamisches Segment hinzu, und klicken Sie auf **+ Bedingung hinzufügen**:

1. Richten Sie die Feldbedingung auf **Hat Tag** ein.
2. Wählen Sie einen Operator – **ist** für einen einzelnen Tag oder **ist einer von** , wenn Sie es auf diese Weise formulieren möchten.
3. Wählen Sie den Tag aus dem Dropdown-Menü aus.

![A "Has tag" condition set to VIP, showing a live count of matching subscribers](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

Die Anzahl in der oberen rechten Ecke wird aktualisiert, während Sie die Regel erstellen, sodass Sie genau sehen können, wie viele Abonnenten derzeit qualifizieren, bevor Sie sie speichern. Jede **Has tag**-Bedingung passt sich derzeit jeweils einem Tag zu - wenn Sie eine Zielgruppe wünschen, die *einen* der folgenden Tags trifft (z. B. `VIP` oder `Wholesale`), fügen Sie einfach eine **Has tag**-Bedingung pro Tag hinzu und setzen Sie **Match** auf **any**.

Das ist es, was Tags jenseits der Organisation nützlich macht: Eine auf **Has tag** basierende Segmentierung wird zu einer Zielgruppe, die Sie bei einer Broadcast- oder Wiederholkampagne als **Segment** auswählen können, oder als **Only for segment**-Einstellung in einem Weges, also "alle, die den Tag `VIP` haben", kann eine eigene Willkommensreihe, ein eigenes wiederkehrendes Newsletter-Abonnement haben oder einfach nur die Personen sein, die Sie das nächste Mal auswählen, wenn Sie eine Einzelkampagne senden.

## Tipps

- Halten Sie die Tag-Namen kurz und spezifisch - sie werden als kleine Chips auf den Abonnentenkarten angezeigt, daher liest sich `VIP` besser als `Very Important Person - Tier 1`.
- Verwenden Sie den **Tag**-Filter, um vor dem Erstellen eines Segments oder dem Versenden einer Kampagne zu prüfen, wer tatsächlich getaggt ist.
- Das Zuweisen von Tags ist additiv - das Entfernen eines Tags von einem Abonnenten wirkt sich nie auf einen anderen Tag, den sie haben, und berührt nie deren Status, Quelle oder Einwilligung.
- Kombinieren Sie Tags mit anderen Regel-Builder-Bedingungen (wie **Opted into marketing** oder **Total spent**) auf demselben Segment, um eine präzisere Zielgruppe zu erhalten, nicht nur einen Tag alleine.
- Ein Abonnent kann so viele Tags tragen, wie Sie mögen - es gibt kein Limit, also ist es in Ordnung, sie für mehrere sich überschneidende Zwecke zu verwenden (ein Treueprogramm *und* eine Eventliste *und* eine Quellennotiz).
- Wenn ein Tag nicht mehr nützlich ist, löschen Sie ihn aus **Subscriber tags**, entfernt er ihn von jedem Abonnenten, auf den er angewandt wurde, und von jedem Segment, das ihn referenziert hat - Segmente, die ihn verwenden, passen sich einfach nicht mehr auf diese Bedingung an.