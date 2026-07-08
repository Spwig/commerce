---
title: Preis-Charm-Regeln
---

Preis-Charm (auch als psychologische Preisgestaltung bezeichnet) passt die Produktpreise automatisch so an, dass sie auf bestimmte Ziffern enden, die für Kunden attraktiver wirken. Zum Beispiel wird anstelle eines Preises von 20,00 $ ein Preis von 19,99 $ angezeigt – eine weit verbreitete Technik, die den Eindruck vermittelt, dass die Preise auf einen Blick niedriger sind.

Spwig wendet Preis-Charm-Regeln automatisch in Ihrem Geschäft an, pro Währung, sodass Sie jede Regel nur einmal einstellen müssen.

## Wie Preis-Charm funktioniert

Wenn ein Produktpreis berechnet wird (einschließlich nach Rabatten oder Angeboten), überprüft Spwig, ob eine aktive Preis-Charm-Regel für diese Währung vorhanden ist. Wenn dies der Fall ist, wird der Preis vor der Anzeige für Kunden angepasst. Die Anpassung gilt für Preise über Ihrem festgelegten Mindestschwellenwert.

Sie können separate Regeln für jede Währung einrichten, die Ihr Geschäft akzeptiert. Zum Beispiel könnten Sie für USD Endungen mit .99 verwenden, aber für JPY auf die nächste 10 Yen runden.

## Erstellen einer Preis-Charm-Regel

1. Navigieren Sie zu **Katalog > Preis-Charm-Regeln**
2. Klicken Sie auf **+ Preis-Charm-Regel hinzufügen**
3. Wählen Sie die **Währung** aus, für die diese Regel gilt (z. B. `USD`, `EUR`, `NZD`)
4. Wählen Sie eine **Regelart** (siehe die Tabelle unten)
5. Optional können Sie einen **Mindestpreisschwellenwert** festlegen, um sehr niedrige Preise auszuschließen
6. Aktivieren Sie **Auf Verkaufspreise anwenden**, wenn Sie auch bei Angeboten Preis-Charm verwenden möchten
7. Stellen Sie sicher, dass **Aktiv** aktiviert ist
8. Klicken Sie auf **Speichern**

Nur eine Regel kann pro Währung existieren. Wenn Sie eine Regel ändern möchten, bearbeiten Sie die vorhandene Regel.

## Regeltypen

| Regeltyp | Beispiel | Bestens geeignet für |
|-----------|---------|----------|
| **.99-Endung charmieren** | 20,50 $ → 19,99 $ | Die meisten Einzelhandelsgüter – der klassische psychologische Preis |
| **.95-Endung charmieren** | 20,50 $ → 19,95 $ | Eine etwas sanftere Alternative zu .99 |
| **.90-Endung charmieren** | 20,50 $ → 19,90 $ | Rund, aber immer noch unter dem nächsten Dollar |
| **Abrunden** | 19,50 $ → 19,00 $ | Geschäfte, die ganze Zahlen bevorzugen |
| **Aufrunden** | 19,50 $ → 20,00 $ | Leichtes Aufrunden für saubere Anzeigen |
| **Auf die nächste 5 runden** | 23,00 $ → 25,00 $ | Hochfrequente Einzelhandelsgeschäfte und Märkte |
| **Auf die nächste 10 runden** | 23,00 $ → 20,00 $ | Höherwertige Artikel wie Haushaltsgeräte |
| **Auf die nächste 100 runden** | 1.234 $ → 1.200 $ | Hochwertige Artikel wie Möbel oder Elektronik |
| **Benutzerdefinierte Endung** | Beliebig – unten angeben | Wenn Ihre Marke eine spezifische Endung wie `.88` verwendet |

### Benutzerdefinierte Endungen

Wenn Sie **Benutzerdefinierte Endung** auswählen, geben Sie den Endwert im Feld **Benutzerdefinierte Endung** ein. Zum Beispiel können Sie `0,88` eingeben, um alle Preise so zu gestalten, dass sie auf `.88` enden (häufig in einigen asiatischen Märkten).

## Mindestpreisschwellenwert

Verwenden Sie das Feld **Mindestpreisschwellenwert**, um Preis-Charm für sehr günstige Artikel zu überspringen, bei denen die Anpassung ungewöhnlich wirken würde. Zum Beispiel bedeutet ein Schwellenwert von `5,00`, dass Artikel unter 5 $ mit ihrem tatsächlichen berechneten Preis ohne Preis-Charm angezeigt werden.

Lassen Sie es bei `0` stehen, um Preis-Charm auf alle Preise anzuwenden.

## Verkaufspreise

Standardmäßig wird Preis-Charm sowohl auf reguläre als auch auf Verkaufspreise angewendet. Wenn Sie möchten, dass Ihre Verkaufspreise ihre exakten berechneten Werte anzeigen (nützlich für zeitlich begrenzte Werbeaktionen, bei denen genaue Zahlen wichtig sind), deaktivieren Sie **Auf Verkaufspreise anwenden**.

## Deaktivieren einer Regel

Um Preis-Charm vorübergehend zu stoppen, ohne die Regel zu löschen, deaktivieren Sie **Aktiv** und speichern Sie die Änderung. Die Regel wird beibehalten und kann jederzeit erneut aktiviert werden.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Beginnen Sie mit Endungen wie .99, wenn Sie unsicher sind – dies ist die am weitesten verbreitete psychologische Preistaktik und funktioniert gut für die meisten Produkttypen.
- Legen Sie ein Minimum fest, wenn Sie günstige Artikel (unter $5) verkaufen, damit ein Artikel zum Preis von 3,50 $ nicht auf 2,99 $ abgerundet wird.
- Überprüfen Sie Ihre Preise nach der Aktivierung einer neuen Regel, indem Sie ein Produkt auf der Verkaufsseite ansehen – abgerundete Preise werden in Echtzeit angezeigt.
- Japanische Yen und ähnliche Währungen mit ganzzahligen Beträgen funktionieren am besten mit **Auf Rundung auf die nächste 10** oder **Auf Rundung auf die nächste 100**, da Dezimalendungen ungewöhnlich wirken.
- Die Preiserkennung wird nach allen Rabatten und Promotionen angewendet, daher werden auch Ihre Verkaufspreise ebenfalls abgerundet, es sei denn, Sie deaktivieren **Auf Verkaufspreise anwenden**.
- Sie können für verschiedene Währungen unterschiedliche Regeltypen haben, was nützlich ist, wenn Sie in mehrere Märkte mit unterschiedlichen Preiskonventionen verkaufen.