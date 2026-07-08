---
title: Synonyme und Umleitungen verwalten
---

Synonyme und Umleitungen machen Ihre Suche intelligenter, indem sie gleichwertige Begriffe verwalten und bestimmte Abfragen an Zielseiten weiterleiten. Synonyme erweitern die Suche, um verwandte Begriffe einzubeziehen („Laptop“ findet auch „Notebook“), während Umleitungen Abfragen wie „Sale“ direkt zu Ihrer Verkaufsseite weiterleiten. Dieser Leitfaden erklärt, wie Sie beide Funktionen erstellen und verwalten, um die Suchrelevanz und den Kundenerlebnis zu verbessern.

Verwenden Sie Synonyme für Begriffsequivalenzen und Umleitungen für Navigationsschnellwege.

![Synonyme Liste](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Verständnis von Synonymen

Synonyme teilen dem Suchsystem mit, dass bestimmte Begriffe als gleichwertig behandelt werden. Wenn ein Kunde nach einem Begriff sucht, werden automatisch Ergebnisse angezeigt, die mit den Synonymbegriffen übereinstimmen.

**Beispiel**: Erstellen Sie eine Synonymzuordnung „Laptop“ → „Notebook“, „portable computer“. Jetzt, wenn jemand nach „Laptop“ sucht, erhält er auch Ergebnisse für Produkte, die „Notebook“ oder „portable computer“ in ihren Namen oder Beschreibungen enthalten.

Synonyme sind besonders wertvoll für:
- Britisches vs. Amerikanisches Englisch (jumper/sweater, trainers/sneakers)
- Markennamen vs. generische Begriffe (tissues/Kleenex)
- Häufige Rechtschreibfehler (accommodate/accomodate)
- Branchensprache vs. Alltagssprache (CPU/processor)

## Synonyme erstellen

Navigieren Sie zu **Search > Synonyms** und klicken Sie auf **+ Add Synonym**.

![Add Synonym Form](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - Der ursprüngliche Suchbegriff, der die Synonymerweiterung auslöst

**Synonyms** - JSON-Array von gleichwertigen Begriffen, z. B. `['sweater', 'pullover', 'jumper']`

**Bidirectional** - Standardmäßig: Angekreuzt. Wenn aktiviert, funktionieren die Synonymbeziehungen in beide Richtungen:
- Suche nach „Laptop“ findet „Notebook“-Produkte
- Suche nach „Notebook“ findet „Laptop“-Produkte

Deaktivieren Sie dies für einseitige Zuordnungen (siehe unten).

**Language** - Optional. Beschränken Sie dieses Synonym auf Suchen in einer bestimmten Sprache. Leer lassen, um es für alle Sprachen anzuwenden.

**Engine** - Optional. Beschränken Sie dieses Synonym auf eine bestimmte Suchmaschine. Leer lassen, um es global anzuwenden.

**Active** - Ob dieses Synonym derzeit verwendet wird. Deaktivieren Sie es, um es vorübergehend zu deaktivieren, ohne es zu löschen.

## Bidirektionale Beispiele

Die meisten Synonyme sollten bidirektional sein - wahre Äquivalente, die in beide Richtungen funktionieren:

| Term | Synonyme | Anwendungsfälle |
|------|----------|----------|
| laptop | notebook, portable computer | Amerikanisches/Britisches Englisch + generische Begriffe |
| sofa | couch, settee | Regionale Unterschiede |
| trainers | sneakers, running shoes | UK/US-Englisch |
| mobile | cell phone, cellular | Internationale Unterschiede |

Mit aktiviertem Bidirektionalen finden alle diese Begriffe die gleichen Produkte, unabhängig davon, welchen Begriff der Kunde verwendet.

## Einseitige Beispiele

Deaktivieren Sie „Bidirektional“ für einseitige Beziehungen:

**Häufige Anwendungsfälle**:
- **Rechtschreibfehler**: Begriff: „acco

mmodate“ → Synonyme: `['accommodate']` (einseitig, sodass die korrekte Schreibweise den Rechtschreibfehler nicht findet)
- **Spezifisch → Generisch**: Begriff: „MacBook“ → Synonyme: `['laptop']` (MacBooks sind Laptops, aber nicht alle Laptops sind MacBooks)
- **Abkürzungen**: Begriff: „CPU“ → Synonyme: `['processor']` (CPU findet Verarbeitungsprodukte, aber Suchanfragen nach Verarbeitung sollten nicht immer CPU enthalten)

## Sprachspezifische Synonyme

Verwenden Sie das Feld Sprache, um regionale Synonyme zu erstellen:

**Beispiel**: Britisches Englisch-Shop
- Begriff: „jumper“, Synonyme: `['sweater', 'pullover']`, Sprache: Englisch (UK)
- Begriff: „trainers“, Synonyme: `['sneakers']`, Sprache: Englisch (UK)

**Beispiel**: Mehrsprachiger Shop
- Begriff: „ordinateur portable“, Synonyme: `['laptop', 'notebook']`, Sprache: Französisch
- Begriff: „zapatos“, Synonyme: `['shoes']`, Sprache: Spanisch

Sprachspezifische Synonyme gelten nur, wenn ein Kunde in dieser Sprache navigiert.

## Engine-spezifische Synonyme

Die meisten Synonyme sollten global gelten (das Feld Engine leer lassen). Verwenden Sie nur engine-spezifische Synonyme, wenn unterschiedliche Suchkontexte unterschiedliche Begriffszuordnungen benötigen:

**Beispiel**: Sie haben separate „shop“- und „blog“-Engines
- Blogsynonym: Begriff: „tutorial“ → Synonyme: `['guide', 'how-to']`, Engine: blog
- Dieses Synonym gilt nur für Blog-Suchen, nicht für Produkt-Suchen

## Verständnis von Umleitungen

Suchumleitungen senden bestimmte Abfragen direkt zu bestimmten Seiten, um die normalen Suchergebnisse zu überspringen. Verwenden Sie Umleitungen, wenn Sie genau wissen, wohin ein Kunde gehen sollte.

**Beispiel**: Erstellen Sie eine Umleitung für „sale“ → `/products/sale/`. Jetzt, wenn jemand nach „sale“ sucht, überspringt er die Suchergebnisse und landet direkt auf Ihrer Verkaufsseite.

Umleitungen sind ideal für:
- Häufige Navigationsschnellwege („returns“ → Verkaufsbedingungenseite)
- Saisonale Promotionen („summer sale“ → Sommerkollektion)
- Beliebte Kategorien („laptops“ → Laptop-Kategorieseite)
- Richtlinienseiten („shipping“ → Versandinformationen)

![Umleitungen Liste](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Übereinstimmungstypen

Umleitungen unterstützen vier Übereinstimmungstypen, die steuern, wie streng die Suchabfrage mit dem Begriff übereinstimmen muss:

**Exact** - Großschreibung ignorierende exakte Übereinstimmung. Die Abfrage muss den Begriff exakt übereinstimmen (Großschreibung ignorieren).
- Begriff: „sale“
- Übereinstimmungen: „sale“, „SALE“, „Sale“
- Übereinstimmungen nicht: „summer sale“, „on sale“

**Contains** - Die Abfrage enthält den Begriff an irgendeiner Stelle.
- Begriff: „sizing“
- Übereinstimmungen: „sizing guide“, „help with sizing“, „what sizing“
- Übereinstimmungen nicht: „size chart“ (anderes Wort)

**Starts With** - Die Abfrage beginnt mit dem Begriff.
- Begriff: „return“
- Übereinstimmungen: „returns“, „return policy“, „returning items“
- Übereinstimmungen nicht: „how to return“ (beginnt nicht mit dem Begriff)

**Regex** - Mustererkennung mithilfe regulärer Ausdrücke. **⚠️ Leistungsbedenken** - komplexe reguläre Ausdrücke verlangsamen die Suche. Verwenden Sie sie nur, wenn andere Übereinstimmungstypen nicht funktionieren.
- Muster: `^(laptop|notebook)s?$`
- Übereinstimmungen: „laptop“, „laptops“, „notebook“, „notebooks“
- Verwenden Sie nur, wenn andere Übereinstimmungstypen nicht funktionieren

## Umleitungen erstellen

Navigieren Sie zu **Search > Redirects** und klicken Sie auf **+ Add Redirect**.

![Add Redirect Form](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - Die Suchabfrage, die übereinstimmen soll

**Match Type** - Exact, Contains, Starts With oder Regex (siehe oben)

**Redirect URL** - Wohin der Kunde weitergeleitet werden soll. Kann relativ (`/products/sale/`) oder absolut (`https://example.com/page/`) sein

**Redirect Type** - HTTP-Statuscode:
- **302 (Vorübergehend)**: Empfohlen. Der Browser cache nicht, Sie können den Zielort später ändern
- **301 (Permanent)**: Browser und Suchmaschinen cache. Nur für permanente Umleitungen verwenden

**Engine** - Optional. Beschränken Sie auf eine bestimmte Suchmaschine

**Hit Count** - Wird automatisch erhöht, wenn diese Umleitung verwendet wird. Hilft, beliebte Schnellwege zu identifizieren.

**Active** - Aktivieren/Deaktivieren Sie diese Umleitung

## Umleitungsbeispiele

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | `/products/sale/` | Direkte „sale“-Suche zu Verkaufsseite |
| clearance | Exact | `/clearance/` | Überspringen Sie die Suche für Clearance-Artikel |
| sizing | Contains | `/pages/size-guide/` | Jede Abfrage zu Größeninformationen geht zum Guide |
| return | Starts With | `/pages/returns/` | Rückgabeverwandte Abfragen gehen zur Richtlinie |

Alle verwenden 302 (vorübergehende) Umleitungen für Flexibilität.

## Umleitungsart: 302 vs 301

**302 (Vorübergehend)** - Empfohlen für die meisten Umleitungen
- Der Browser erstellt bei jedem Aufruf eine neue Anfrage
- Sie können den Ziel-URL jederzeit ändern
- Sicherere Wahl, wenn Sie sich nicht sicher sind

**301 (Permanent)** - Nur sparsam verwenden
- Der Browser cache die Umleitung
- Suchmaschinen aktualisieren ihre Indizes
- Schwieriger zu ändern, wenn Sie später nochmal müssen

**Empfehlung**: Verwenden Sie 302, es sei denn, Sie sind sich absolut sicher, dass die Umleitung sich nie ändern wird.

## Hit Count Analytics

Das Feld Hit Count wird jedes Mal automatisch erhöht, wenn eine Umleitung ausgelöst wird. Verwenden Sie dies, um:
- Die am häufigsten verwendeten Navigationsschnellwege zu identifizieren
- Umleitungen zu finden, die nie verwendet werden (überlegen Sie, sie zu entfernen)
- Beliebte Suchmuster zu entdecken

Überprüfen Sie die Hit-Zahlen monatlich, um Ihre Umleitungsstrategie zu optimieren.

## Synonymchancen finden

**Verwenden Sie Abfragen mit Null-Ergebnissen**: Navigieren Sie zu **Search > Search Analytics** und filtern Sie nach Abfragen mit Null-Ergebnissen. Diese zeigen:
- Begriffe, die Kunden verwenden, die nicht mit Ihren Produktbeschreibungen übereinstimmen
- Regionale Unterschiede, die Sie nicht berücksichtigt haben
- Häufige Rechtschreibfehler

**Workflow**:
1. Überprüfen Sie wöchentlich Abfragen mit Null-Ergebnissen
2. Identifizieren Sie Muster (gleiche Begriffe, die sich wiederholen)
3. Fügen Sie Synonyme hinzu, um Kundenbegriffe mit Ihren Produktbezeichnungen zu verknüpfen
4. Überwachen Sie, ob die Anzahl der Null-Ergebnisse abnimmt

## Tipps

- **Überprüfen Sie wöchentlich Abfragen mit Null-Ergebnissen, um Synonymideen zu finden** - Sie zeigen Lücken zwischen dem Kundenbegriff und Ihren Produktbeschreibungen
- **Beginnen Sie mit häufigen Synonymen, erweitern Sie basierend auf Daten** - Beginnen Sie mit offensichtlichen regionalen Unterschieden, fügen Sie basierend auf tatsächlichen Suchverhalten hinzu
- **Verwenden Sie bidirektionale für wahre Äquivalente** - Die meisten Synonyme sollten in beide Richtungen funktionieren (Laptop ↔ Notebook)
- **Vermeiden Sie komplexe reguläre Ausdrücke** - Reguläre Ausdrücke sind langsamer als andere Übereinstimmungstypen; verwenden Sie sie nur, wenn nötig
- **Verwenden Sie standardmäßig 302-Redirects (vorübergehend)** - Gibt Ihnen Flexibilität, Zielorte später zu ändern
- **Testen Sie Synonyme mit echten Abfragen** - Suchen Sie nach Synonymbegriffen, um sicherzustellen, dass sie die erwarteten Ergebnisse zurückgeben
- **Sprachspezifische Synonyme für mehrsprachige Shops** - Erstellen Sie regionale Begriffszuordnungen für jede unterstützte Sprache