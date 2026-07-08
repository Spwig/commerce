---
title: UI-Übersetzungsverwaltung
---

Die UI-Übersetzungsseite ermöglicht es Ihnen, zu bestimmen, wie Frontend-Schnittstellenzeichenketten – Schaltflächen, Beschriftungen, Fehlermeldungen und andere UI-Texte – in jeder Sprache angezeigt werden. Im Gegensatz zu Produkt- oder Seiteninhaltsübersetzungen sind dies die festen Schnittstellenelemente, die Kunden in Ihrem Geschäft sehen. Passen Sie sie an, um Ihre Markenstimme zu widerspiegeln oder die Klarheit für Ihr spezifisches Publikum zu verbessern.

Diese Seite zeigt alle übersetzbaren UI-Zeichenketten an und ermöglicht es Ihnen, die Standardübersetzungen, die von Spwig bereitgestellt werden, zu überschreiben.

## Verständnis von UI-Übersetzungen

UI-Übersetzungen sind die Textzeichenketten, die Ihre Geschäfts-Schnittstelle bilden:

**Beispiele für UI-Zeichenketten**:
- Schaltflächen: "Add to Cart", "Checkout", "Search"
- Beschriftungen: "Price", "Quantity", "Shipping Address"
- Nachrichten: "Item added to cart", "Order confirmed", "Invalid email address"
- Navigation: "Home", "Shop", "Contact Us"
- Formularfelder: "Email", "Password", "First Name"

Spwig enthält Standardübersetzungen für etwa 300 UI-Zeichenketten in allen unterstützten Sprachen. Die UI-Übersetzungsseite ermöglicht es Ihnen, jede dieser Standardwerte durch eigene benutzerdefinierte Übersetzungen zu ersetzen.

## Warum UI-Übersetzungen anpassen?

**Markenstimme**: Ändern Sie "Add to Cart" in "Buy Now" oder "Get Yours", um Ihre Markenpersönlichkeit widerzuspiegeln

**Regionale Unterschiede**: Anpassen Sie Übersetzungen für spezifische Märkte (britisches Englisch vs. amerikanisches Englisch, europäisches Spanisch vs. lateinamerikanisches Spanisch)

**Klarheit**: Wenn die Standardübersetzung für Ihre Produkte oder Ihr Publikum nicht sinnvoll ist, ersetzen Sie sie durch klareren Text

**Branchenspezifische Begriffe**: Verwenden Sie Terminologie, die Ihre Kunden erwarten (z. B. "Book Appointment" anstelle von "Add to Cart" für Dienstleistungs-Geschäfte)

## Nach Zeichenketten suchen

Verwenden Sie das Suchfeld, um spezifische UI-Zeichenketten zu finden:

**Nach englischem Text suchen**: Geben Sie "add to cart" ein, um die Übersetzungen für diese Schaltfläche zu finden

**Nach Übersetzung suchen**: Geben Sie Text in jeder Sprache ein, um passende Übersetzungen zu finden

**Nach Schlüssel suchen**: Wenn Sie den Übersetzungsschlüssel kennen (z. B. `cart.add_item`), suchen Sie ihn direkt

Die Seite aktualisiert sich sofort, während Sie tippen, und zeigt nur übereinstimmende Zeichenketten an.

## Übersetzungsdetails ansehen

Jede UI-Zeichenkette zeigt:

**Englischer Quelltext** - Die Standardversion auf Englisch (Ihr Referenzpunkt)

**Übersetzungsschlüssel** - Der interne Bezeichner, der im Code verwendet wird (z. B. `cart.add_to_cart`)

**Sprachspalten** - Aktuelle Übersetzung für jede aktive Sprache

**Überschreibungsstatus** - Ob Sie die Übersetzung angepasst haben (hervorgehoben, wenn überschrieben)

## Überschreibungen für Übersetzungen erstellen

Um eine UI-Zeichenkette zu überschreiben:

1. **Finden Sie die Zeichenkette** mithilfe der Suche (z. B. suchen Sie nach "add to cart")
2. **Klicken Sie auf die Sprachzelle**, die Sie anpassen möchten
3. **Geben Sie Ihre benutzerdefinierte Übersetzung** in den Pop-up-Editor ein
4. **Speichern** - Ihre Überschreibung wird sofort wirksam

Die ursprüngliche Standardübersetzung wird beibehalten – Sie erstellen eine Überschreibung, die Vorrang hat.

## Zurückkehren zu den Standardwerten

Um eine benutzerdefinierte Überschreibung zu entfernen und die Standardübersetzung wiederherzustellen:

1. **Klicken Sie auf die überschriebene Übersetzung** (diese sind hervorgehoben)
2. **Klicken Sie auf "Zurückkehren zu Standard"** im Editor
3. **Bestätigen** - Die Standardübersetzung wird sofort wiederhergestellt

Sie können einzelne Sprachüberschreibungen zurücknehmen, ohne Ihre Überschreibungen in anderen Sprachen zu beeinflussen.

## Filtern nach Überschreibungsstatus

Verwenden Sie den Filter-Abwärtsmenü, um anzuzeigen:

**Alle Zeichenketten** - Jede UI-Zeichenkette im System (~300 insgesamt)

**Nur überschrieben** - Zeichenketten, für die Sie benutzerdefinierte Übersetzungen erstellt haben

**Nur Standardwerte** - Zeichenketten, die immer noch die Standardübersetzungen von Spwig verwenden

Dies hilft Ihnen, zu überprüfen, welche Zeichenketten Sie angepasst haben und Lücken zu identifizieren.

## Häufige Anpassungsbeispiele

| Englische Standardübersetzung | Benutzerdefinierte Überschreibung | Anwendungsfall |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Direkterer Aufruf zur Aktion |
| Checkout | Secure Checkout | Sicherheit betonen |
| Search | Find Products | Spezifischer für E-Commerce |
| Contact Us | Get in Touch | Freundlicherer Ton |
| Subscribe | Join Our Newsletter | Klare Wertepositionierung |

## Übersetzungssicherheit

Bei der Eingabe benutzerdefinierter Übersetzungen stellen Sie sicher, dass:

**Länge passt zur UI-Bereich** - Übersetzungen können länger oder kürzer als Englisch sein (deutsche Wörter sind oft länger, beispielsweise)

**Bedeutung bleibt erhalten** - Ändern Sie keine Funktionalität in der Übersetzung (eine "Cancel"-Schaltfläche sollte nicht "Delete" heißen)

**Konsistente Terminologie** - Verwenden Sie die gleiche Übersetzung für wiederkehrende Begriffe in der gesamten Schnittstelle

**Angemessene Formalität** - Passen Sie den Ton Ihres Zielmarktes an (formell vs. locker)

## Konsistenz in mehreren Sprachen

Wenn Sie eine Zeichenkette für mehrere Sprachen anpassen:

1. **Beginnen Sie mit Ihrer Standard-Sprache** - Legen Sie die Grundlage fest
2. **Anpassen Sie andere Sprachen**, um den gleichen Zweck zu erfüllen
3. **Testen Sie in jeder Sprache**, um Layout und Bedeutung zu überprüfen
4. **Verwenden Sie bei Bedarf Muttersprachler**, um nicht-englische Anpassungen zu überprüfen

Unkonsistente Anpassungen in verschiedenen Sprachen führen zu einem verwirrenden Kunden-Erlebnis.

## Massenexport/Import

Für umfangreiche Anpassungen verwenden Sie den Export/Import-Workflow:

1. **Exportieren** Sie die aktuellen Übersetzungen als JSON oder CSV
2. **Bearbeiten Sie in einer Tabellenkalkulation** oder einem Texteditor (einfacher für Massenänderungen)
3. **Importieren** Sie die aktualisierten Übersetzungen zurück in das System

Dieser Workflow ist über die Übersetzungsaufgabenseite verfügbar, um umfangreiche Übersetzungsvorhaben zu verwalten.

## Tipps

- **Suchen Sie vor der Anpassung** - Stellen Sie sicher, dass Sie die richtige Zeichenkette bearbeiten; einige ähnliche Zeichenketten dienen unterschiedlichen Zwecken
- **Testen Sie auf dem Frontend nach dem Speichern** - Überprüfen Sie, ob Ihre benutzerdefinierte Übersetzung korrekt in der tatsächlichen UI angezeigt wird
- **Halten Sie Übersetzungen kurz** - Kürzere Texte sind in der Regel besser für Schaltflächen und Beschriftungen
- **Dokumentieren Sie Ihre Überschreibungen** - Notieren Sie, warum Sie bestimmte Zeichenketten angepasst haben, um dies für die Zukunft zu referenzieren
- **Verwenden Sie konsistente Terminologie** - Wenn Sie "Cart" in "Basket" ändern, tun Sie dies konsistent über alle verwandten Zeichenketten hinweg
- **Berücksichtigen Sie mobile Layouts** - Längere Übersetzungen können auf kleineren Bildschirmen umgebrochen oder abgeschnitten werden
- **Überprüfen Sie nach Sprachupdates** - Wenn Spwig neue Standardübersetzungen hinzufügt, überprüfen und anpassen Sie diese, um Konsistenz zu gewährleisten

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe genau so wie in den Preservation Rules gezeigt auf.