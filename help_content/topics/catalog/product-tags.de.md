---
title: Produkt-Labels
---

Produkt-Labels sind kurze, freie Etiketten, die Sie Produkten anhängen können, um diese flexibel zu organisieren und zu filtern. Im Vergleich zu Kategorien sind Labels leichtgewichtig – sie haben keine Hierarchie oder dedizierte Seiten, sind aber schnell zu erstellen und einfach auf viele Produkte gleichzeitig anzuwenden.

Häufige Verwendungen von Labels:
- Produkte nach Thema gruppieren (`summer`, `gift-idea`, `clearance`)
- Produkte für interne Zwecke markieren (`staff-pick`, `new-arrival`, `bundle-candidate`)
- Filterbare Sammlungen in Promotionen und Kampagnen erstellen
- Schnell verwandte Produkte in verschiedenen Kategorien finden

## Ein Label erstellen

Labels werden automatisch erstellt, wenn Sie sie einem Produkt hinzufügen, Sie können sie aber auch direkt verwalten:
1. Navigieren Sie zu **Catalog > Product Tags**
2. Klicken Sie auf **+ Add Product Tag**
3. Geben Sie den Label-**Name** ein (z. B. `New Arrival`)
4. Der **Slug** wird automatisch aus dem Namen generiert (`new-arrival`) – Sie können ihn bei Bedarf bearbeiten
5. Klicken Sie auf **Save**

Label-Slugs müssen eindeutig sein. Der Slug wird intern und in URLs verwendet, wenn Labels für die Filterung im Frontend genutzt werden.

## Ein Label einem Produkt hinzufügen

1. Navigieren Sie zu **Products > All Products**
2. Öffnen Sie das Produkt, dem Sie ein Label hinzufügen möchten
3. Finden Sie das Feld **Tags** im Produkt-Edit-Formular
4. Geben Sie einen bestehenden Tag ein, um ihn zu suchen, oder geben Sie den Namen eines neuen Tags ein, um ihn sofort zu erstellen
5. Wählen Sie oder erstellen Sie so viele Tags wie benötigt
6. Speichern Sie das Produkt

## Bestehende Labels verwalten

### Alle Labels ansehen

Die Liste der Labels unter **Catalog > Product Tags** zeigt alle Labels in alphabetischer Reihenfolge an. Klicken Sie auf ein Label, um dessen Namen oder Slug zu bearbeiten.

### Ein Label umbenennen

1. Navigieren Sie zu **Catalog > Product Tags**
2. Klicken Sie auf das Label, das Sie umbenennen möchten
3. Aktualisieren Sie das Feld **Name**
4. Der Slug aktualisiert sich nicht automatisch, wenn Sie das Label umbenennen – aktualisieren Sie ihn manuell, wenn nötig, um Konsistenz zu gewährleisten
5. Klicken Sie auf **Save**

Hinweis: Das Umbenennen eines Labels aktualisiert es an allen Stellen, an denen es verwendet wird, da Produkte auf das gleiche Label-Objekt verweisen.

### Ein Label löschen

1. Navigieren Sie zu **Catalog > Product Tags**
2. Markieren Sie das Kästchen neben dem/den Label(s), das/der Sie löschen möchten
3. Wählen Sie **Delete selected product tags** aus dem Dropdown **Action** aus
4. Bestätigen Sie die Löschung

Das Löschen eines Labels entfernt es von allen Produkten, zu denen es zugewiesen war. Die Produkte werden nicht gelöscht – nur das Label-Label wird entfernt.

## Tipps

- Halten Sie die Namen der Labels kurz und konsistent – verwenden Sie Kleinbuchstaben oder Title Case und wählen Sie eine Konvention und verwenden Sie diese konsistent in Ihrem Katalog.
- Vermeiden Sie, Kategorielogik in Labels zu duplizieren. Labels sind am besten geeignet, um überquerende Themen (wie `new-arrival` oder `staff-pick`) zu behandeln, die nicht sauber in Ihre Kategoriestruktur passen.
- Verwenden Sie ein Label `clearance` oder `sale`, um Produkte für zeitlich begrenzte Promotionen zu markieren – das macht es leichter, diese Produkte später zu finden und zu aktualisieren.
- Labels sind standardmäßig für Kunden nicht sichtbar. Ihr primäres Ziel ist es, Ihnen bei der Organisation und Filterung von Produkten im Admin-Panel zu helfen.
- Wenn Sie sich dabei ertappen, viele Labels zu erstellen, die sich mit Ihren Kategorien überschneiden, könnte es sinnvoll sein, Ihre Kategoriestruktur erneut zu überprüfen.