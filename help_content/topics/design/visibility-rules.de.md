---
title: Sichtbarkeitsregeln
---

# Sichtbarkeitsregeln

Sichtbarkeitsregeln ermöglichen es Ihnen, Teile Ihres Ladens zu zeigen oder zu verstecken, je nachdem, wer besucht und wo sie sich befinden. Sie können **Seitenelemente**, **Menüpunkte** und **Header-/Footer-Widgets** anhand derselben Bedingungen sperren — den Markt oder die Region des Kunden, die Sprache oder Währung, in der sie angezeigt werden, die Uhrzeit des Tages oder pro-Besucher-Signale wie die Anmeldung.

Alles wird aus **Regelgruppen** aufgebaut: einem benannten, wiederverwendbaren Satz aus einer oder mehreren Bedingungen. Sie erstellen eine Regelgruppe einmal (z. B. "Neuseeland-Markt" oder "angemeldete Mitglieder") und heften sie an jedes Element, jeden Menüpunkt oder jedes Widget, das Sie steuern möchten. Ein Element ohne angeschlossene Regelgruppe ist immer sichtbar.

## Wie die Sichtbarkeit entschieden wird

Wenn mehr als eine Regelgruppe an ein Element angehängt ist, wird das Element angezeigt, wenn **irgendeine** angehängte Gruppe übereinstimmt (sie kombinieren sich mit OR). Innerhalb einer einzelnen Gruppe wählen Sie, ob **alle** oder **irgendeine** der Bedingungen übereinstimmen müssen.

Regeln fallen in zwei Familien, und Spwig behandelt sie unterschiedlich, damit Ihr Geschäft schnell bleibt und suchmaschinenfreundlich ist:

- **Marktregeln** — Bedingungen zu Region/Markt, Sprache, Währung und Zeit. Diese werden auf dem Server für jede Markt-URL entschieden, sodass dieselbe Seite jedem Besucher (und jedem Suchmaschinenindex) an dieser Adresse identisch geliefert wird. Dies hält Seiten cachebar und SEO-sicher.
- **Pro-Besucher-Regeln** — Anmeldestatus, Warenkorbinhalt, Gerät und genaue Lage. Diese hängen vom individuellen Besucher ab, sodass Spwig sie privat für jeden Menschen nach dem Laden der Seite auflöst. Sie werden niemals in eine gemeinsame, gecachte Seite eingebaut.

Wenn Sie eine Regelgruppe deaktivieren, hört sie einfach auf, anzuwenden — das Element, an das sie angehängt war, kehrt zu seiner Sichtbarkeit zurück. Das Deaktivieren einer Gruppe ist kein Weg, etwas zu verstecken.

## Erstellen und Anhängen von Regeln

Es gibt zwei Arten, mit Regelgruppen zu arbeiten.

### Hängen Sie sie an, wo Sie entwerfen

Überall, wo Sie Inhalt sperren können, sehen Sie eine **Sichtbarkeitssteuerung** (das Auge-Symbol):

- **Page Builder** — wählen Sie ein Element aus, öffnen Sie dessen Eigenschaften, und verwenden Sie die Sichtbarkeitssteuerung.
- **Menu Builder** — wählen Sie einen Menüpunkt aus und öffnen Sie den **Sichtbarkeitsreiter**. Dies funktioniert bei **jedem** Element, einschließlich eines Untermenü (Dropdown)-Elements, das unter einem anderen eingebettet ist — eine Regel auf einem Kind versteckt nur dieses Kind, wobei der Rest des Menüs intakt bleibt.
- **Header & Footer Builder** — wählen Sie ein Widget aus und öffnen Sie den **Sichtbarkeitsregelgruppen-Bereich** in dessen Einstellungen.

Regeln, die sich auf den individuellen Besucher beziehen — ob sie angemeldet sind, was in ihrem Warenkorb ist, oder ihr Gerät — werden für jeden Kunden gelöst, ohne Ihren Laden zu verlangsamen oder Suchmaschinen zu beeinflussen. Ihr Ladensystem bleibt schnell und cachebar, und jeder Besucher sieht nur die Navigation an, die für ihn bestimmt ist.

Im Sichtbarkeits-Editor können Sie Folgendes tun:

- **Anhängen** Sie jede Ihrer vorhandenen Regelgruppen, indem Sie sie markieren.
- **Schnellregel** — erstellen Sie eine einfache Regelgruppe vor Ort (z. B. "nur Mitglieder", einen einzelnen Markt, eine Währung, ein Gerät oder einen Mindestwarenkorbwert) und hängen Sie sie in einem Schritt an.
- **Regelgruppen verwalten** — springen Sie zum vollständigen Builder für erweiterte Regeln.

Klicken Sie auf **Anwenden**, und das Element ist sofort gesperrt.

### Erstellen Sie erweiterte Regeln

Für alles, was anspruchsvoller ist — mehrere Bedingungen kombinieren, Gruppen verschachteln oder feine Operatoren — gehen Sie zu **Design → Sichtbarkeitsregeln** (Regelgruppen). Dort können Sie Regeln mit UND/ODER-Logik zusammenstellen und sie über den gesamten Laden wiederverwenden.

## Häufige Bedingungen

Bleiben Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe erhalten.

| Bedingung | Verwenden Sie es, um… |
|-----------|----------------------|
| **Region / Markt** | Zeigen Sie einen Block nur für Besucher in einem bestimmten Markt an (z. B. Neuseeland) |
| **Ausgewählte Währung** | Zeigen Sie Preisnotizen oder Angebote nur an, wenn eine bestimmte Währung aktiv ist |
| **Ausgewählte Sprache** | Zeigen Sie den Inhalt nur in einer bestimmten Sprache an |
| **Datum / Uhrzeit / Tag / Geschäftszeiten** | Führen Sie eine Werbebanner während eines Verkaufsfensters durch oder nur während der Öffnungszeiten |
| **Anmeldestatus** | Zeigen Sie „Nur für Mitglieder“-Inhalt oder eine Anmeldeaufforderung für Gäste an |
| **Gerätetyp** | Zeigen oder verstecken Sie etwas auf Mobilgeräten, Tablets oder Desktop-PCs |
| **Wert des Warenkorbs / Artikel** | Zeigen Sie eine Aufforderung zur kostenlosen Lieferung an, sobald der Warenkorb einen Schwellenwert überschreitet |

## Vorschau

In der Vorschau des Page Builders können Sie **als Markt** und **als Besucher** (angemeldet oder Gast, mit einem Beispiel-Warenkorb) prüfen, was jeder Benutzer sehen würde — einschließlich der pro-Benutzer-Regeln, die normalerweise privat gelöst werden.

## Tipps

- Erstellen Sie eine kleine Gruppe gut benannter Regeln („Neuseeland-Markt“, „Mitglieder“, „Nur Mobilgeräte“) und verwenden Sie sie überall – es ist einfacher zu verwalten als Einzelregeln.
- Markenregeln sind die sichere Wahl für alles, was Sie in Suchmaschinen indiziert werden soll, weil das Ergebnis für jeden bei einer bestimmten Marken-URL gleich ist.
- Wenn ein Artikel unerwartet verschwindet, prüfen Sie seine zugeordneten Regelsätze – ein Artikel wird nur dann versteckt, wenn ein aktiver Satz vorhanden ist und keiner seiner Sätze mit dem aktuellen Besucher übereinstimmt.