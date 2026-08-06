---
title: Regionale Verf眉gbarkeit
---

Die regionale Verf眉gbarkeit steuert, in welchen Verkaufsregionen Ihres Produkts verkauft werden kann, und wie K盲ufer au脽erhalb dieser Regionen Ihr Katalogerlebnis wahrnehmen. Nutzen Sie dies, wenn ein Produkt nur f眉r bestimmte L盲nder lizenziert ist, wenn Lagerbest盲nde f眉r den lokalen Markt reserviert sind oder wenn Sie ein neues Produkt schrittweise in einzelnen Regionen einf眉hren.

Dies baut auf **Verkaufsregionen** auf, die L盲nder zu benannten M盲rkten gruppieren (siehe den Leitfaden zu den Verkaufsregionen, um diese einzurichten). Sobald Ihre Regionen existieren, k枚nnen Sie einzelnen Produkten diese zuweisen und entscheiden, wie eingeschr盲nkte Produkte f眉r K盲ufer aussehen, die sie nicht kaufen k枚nnen.

## Einschr盲nkung eines Produkts auf bestimmte Regionen

Jedes Produkt hat eine **Regionale Verf眉gbarkeit** auf seiner Bearbeitungsseite. Öffnen Sie **Produkte > Alle Produkte**, w盲hlen Sie ein Produkt aus und suchen Sie es im Abschnitt **Status** neben **Status**, **Hervorgehoben** und **Vom Storefront verstecken**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Produkt-Bearbeitungsseite, in den Status-Bereich gescrollt, mit sichtbarem und auf "Nur in ausgew盲hlten Regionen" eingestelltem Dropdown-Liste f眉r die regionale Verf眉gbarkeit
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Verwenden Sie ein Produkt mit mindestens 2 bereits ausgew盲hlten Regionen darunter, falls m枚glich, damit die Inline-Tabelle in dem zweiten Screenshot sichtbare Zeilen hat.
-->

| Option | Was es bedeutet |
|--------|-----------------|
| **In allen Regionen verf眉gbar** | Keine Einschr盲nkung. Das Produkt wird überall verkauft. Dies ist die Standardeinstellung f眉r jedes Produkt. |
| **Nur in ausgew盲hlten Regionen** | Eine Erlaubnisliste. Das Produkt wird nur in den Regionen verkauft, die Sie unten ausw盲hlen - 眉berall sonst wird es als nicht verf眉gbar betrachtet. |
| **Alle Regionen au脽er ausgew盲hlten** | Eine Sperrliste. Das Produkt wird in allen Regionen vertrieben, *au脽er* den Regionen, die Sie unten ausw盲hlen. |

### Regionen ausw盲hlen

Unter dem Status-Bereich wird eine Tabelle mit dem Titel **Regionale Verf眉gbarkeit (ausgew盲hlte Regionen)** angezeigt, die die Regionen auflistet, auf die sich der obige Modus bezieht.

1. Legen Sie die **Regionale Verf眉gbarkeit** auf **Nur in ausgew盲hlten Regionen** oder **Alle Regionen au脽er ausgew盲hlten** fest.
2. In der Tabelle **Regionale Verf眉gbarkeit (ausgew盲hlte Regionen)** klicken Sie auf **Weitere Region hinzuf眉gen** und w盲hlen Sie eine Verkaufsregion.
3. Wiederholen Sie diesen Vorgang f眉r jede Region, die Sie hinzuf眉gen m枚chten.
4. Klicken Sie auf **Speichern**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: Die Tabelle "Regionale Verf眉gbarkeit (ausgew盲hlte Regionen)" mit zwei oder drei hinzugef眉gten Regionen
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Wenn **Regionale Verf眉gbarkeit** auf **In allen Regionen verf眉gbar** eingestellt ist, wird alles in dieser Tabelle ignoriert - l枚schen Sie zuerst den Modus-Downlopend, wenn Sie eine Einschr盲nkung aufheben und die Zeilen nicht l枚schen m枚chten.

F眉r eine Katalog-übergreifende Ansicht der regionenspezifischen Regeln jedes Produkts in einer Liste (n眉tzlich, wenn Sie viele Produkte gleichzeitig auditieren), gehen Sie zu **Produkt-Regionensichtbarkeit** unter `/admin/catalog/productregionvisibility/`.

## Anzeigen, in welchen Regionen ein Produkt nicht geliefert wird

Wenn sich die Region des K盲ufers nicht mit den Verf眉gbarkeitsregeln des Produkts deckt, kontrollieren Sie, was sie in **Stock-Display-Einstellungen** unter dem Abschnitt **Regionale Verf眉gbarkeit** sehen. Diese Seite hat noch keinen Sidebar-Kurzbefehl - 鰂fnen Sie sie direkt unter `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: "Stock Display Settings" -Bearbeitungsformular, gescrollt zum "Regionale Verf眉gbarkeit"-Feld, mit sichtbarem Dropdown-Liste f眉r "Regionen-eingeschr盲nkte Anzeige"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Alle Markdown-Formatierungen, Bildpfade, Codebl枚cke und technischen Begriffe beibehalten.

| Option | Was Kunden sehen |
|--------|-------------------|
| **Anzeigen, als nicht lieferbar markiert** (Standard) | Das Produkt wird weiterhin in Listen angezeigt, mit einem "Nicht lieferbar"-Stichwort und einer "Wird nicht nach [Region] geliefert"-Meldung anstelle des "Zum Warenkorb hinzufügen"-Buttons. Zudem wird eine Banner-Anzeige oben auf Listenseiten angezeigt ("Einige Produkte werden nicht nach [Zielort] geliefert") mit einem Link, um nur die Artikel anzuzeigen, die dort geliefert werden. |
| **Aus Listen entfernen** | Das Produkt wird für Kunden in dieser Region vollständig aus Listen und Suchergebnissen entfernt. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Storefront-Produktliste mit dem Regionen-Banner oben und mindestens einem Produktkarten-Element mit dem "Nicht lieferbar"-Stichwort und der "Wird nicht nach [Region] geliefert"-Meldung
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Erfordert eine Live-Ship-To-Auswahl (oder GeoIP-Erkennung), die auf eine Region außerhalb der Demo-Produkte abzielt.
-->

Ein eingeschränktes Produkt zeigt immer eine "Dieses Produkt wird nicht nach [Region] geliefert"-Meldung an, wenn ein Kunde direkt darauf zugreift (z. B. von einem geteilten Link oder Suchmaschinenergebnis) — dies gilt unabhängig davon, welche Listenoption Sie oben ausgewählt haben, da ein direkter Link die Liste vollständig umgeht.

## Ermöglichen, dass Kunden ihre Region auswählen oder entdecken

Spwig kann die Region eines Kunden automatisch erkennen und ein Wechseloption anbieten, und Sie können einen Selektor hinzufügen, damit Kunden diese selbst jederzeit ändern können.

### Vor dem Beginn

Sie benötigen zwei Dinge, um die Regionserkennung und -wechsel korrekt zu konfigurieren:

1. **Verkaufsregionen** — die Länder in jeder Region und die Standardwährung jeder Region. Wenn Sie unter **Bestand** im Seitenleistenmenü **Verkaufsregionen** nicht sehen, aktivieren Sie **Mehrfachlager aktivieren** unter **Einstellungen > Store-Einstellungen > E-Commerce**, um das Menüeintrag zu aktivieren (Sie müssen nicht unbedingt mehrere Lager verwenden — dieser Einstellung dient nur dazu, das Menüelement zu entsperren). Sie können auch direkt zu `/admin/catalog/salesregion/` gehen.
2. **Versandländer** — die Länder, in die Ihr Geschäft tatsächlich versendet. Diese sind in der Regel bereits vorhanden: Jedes Land, das Sie zu einem Versandgebiet hinzufügen, wird automatisch hier hinzugefügt. Um die Liste zu überprüfen oder manuell anzupassen, öffnen Sie direkt `/admin/shipping/shippingcountry/` (es verfügt zudem noch nicht über einen Seitenleistenlink).

### Die automatische Regionbestätigung

Spwig erkennt die Region des Kunden anhand ihres Standorts und wendet sie automatisch an. Wenn dies sie in eine Region *anders als* den Standardmarktplatz Ihres Geschäfts bringt — und Sie zwei oder mehr aktive Verkaufsregionen haben — zeigt Spwig eine Bestätigung bei ihrem ersten Besuch an, damit sie wissen, in welcher Region sie sich befinden, und sie diese ändern können:

> **Wir haben Ihre Region auf [Region] gesetzt**
> Wir haben dies aus Ihrem Standort gewählt, damit Sie die richtigen Produkte und Preise sehen. Falsch? Wählen Sie Ihr Land aus.
> Liefern unter: [Landauswahl]  **[Weiterstöbern]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: Das "Wir haben Ihre Region auf [Region] gesetzt"-Bestätigungsmodul auf der Startseite des Storefronts, mit der Landauswahl und dem "Weiterstöbern"-Button
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Erfordert GeoIP-Auflösung in einer nicht-standardmäßigen Region und mindestens 2 aktive Verkaufsregionen, um ausgelöst zu werden. Lokal können Sie einen "geo_country"-Cookie auf ein nicht-standardmäßiges Land setzen, um es zu simulieren.
-->

Die Auswahl eines anderen Landes in der Auswahlliste wechselt sie sofort. Das Verwerfen oder Klicken auf **Weiterstöbern** behält ihre aktuelle Region bei, und sie werden auf diesem Browser nicht erneut gefragt. Besucher, die bereits in der Standardregion Ihres Geschäfts sind, erhalten die Bestätigung überhaupt nicht.

### Hinzufügen eines Lieferort-Selektors zu Ihrem Header oder Footer

Wenn Sie lieber möchten, dass Kunden ihre Region selbst jederzeit ändern können (anstelle sich nur auf den automatischen Hinweis zu verlassen), fügen Sie das **Lieferort-Selektor**-Widget zu Ihrem Header oder Footer hinzu.

1.

Gehe zu **Design > Header-Builder** (oder **Footer-Builder**).
2.

Ziehe das **Ship-To-Selector**-Widget aus der Widget-Bibliothek in eine Zeile.
3.

Klicke auf **Speichern**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Header-Builder mit geöffneter Widget-Bibliothek und sichtbarem/ausgewähltem Ship-To-Selector-Widget
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Das Widget benötigt keine Einrichtung – es listet Ihre aktiven Versandländer automatisch auf und zeigt die aktuelle Auswahl des Kunden an (oder den über GeoIP erkannten Land, falls der Kunde noch keinen ausgewählt hat). Das Auswählen eines anderen Landes aktualisiert sofort deren Region und lädt die Produktverfügbarkeit und Preise der Seite neu.

Der Ship-To-Selector verfügt noch nicht über ein eigenes Einstellungsformular. Wenn Sie den Button-Stil (outline, solid oder ghost) ändern oder das „Ship to“-Label verstecken möchten, öffnen Sie die Einstellungen des Widgets im Builder und bearbeiten Sie das **Benutzerdefinierte Konfigurations (JSON)**-Feld direkt, indem Sie `button_style` und `show_label` verwenden.

### Währung folgt der Region

Wenn Ihr Shop mehr als eine Währung unterstützt (unter **Einstellungen > Mehrere Währungen** festgelegt), ändert sich mit dem Wechsel der Region – ob über die Aufforderung oder den Ship-To-Selector – auch die angezeigte Währung auf die Standardwährung dieser Region. Wenn Ihr Shop nur eine Währung hat oder keine zweite explizit aktiviert hat, bleibt die Währung unverändert, wenn ein Kunde die Region wechselt.

## Tipps

- Lassen Sie **Regionenverfügbarkeit** auf **In allen Regionen verfügbar** stehen, es sei denn, Sie haben einen spezifischen Grund, eine Produktverfügbarkeit einzuschränken – es ist die einfachste Option und benötigt keinen Wartungsaufwand, wenn Sie später weitere Regionen hinzufügen.
- Verwenden Sie **Nur in ausgewählten Regionen**, für eine kleine Zulassungsliste (z. B. ein Produkt, das zunächst in einem Land veröffentlicht wird) und **Alle Regionen außer ausgewählten**, für eine kleine Blockliste (z. B. überall außer einem Land, in dem das Produkt nicht lizenziert ist) – wählen Sie, welches weniger Zeilen zum Einrichten benötigt.
- Wenn Kunden berichten, dass ein Produkt fehlt, das sichtbar sein sollte, prüfen Sie sowohl die Einstellung **Regionenverfügbarkeit** des Produkts als auch, ob ihr Land von einer aktiven **Verkaufsregion** und einem aktiven **Versandland** abgedeckt wird.
- **Aus der Liste ausblenden** hält Ihr Katalogbild sauber für Kunden, die bestimmte Artikel nicht kaufen können, aber bedeutet auch, dass die Sortimente und Suche in diesen Regionen dünner aussehen – **Anzeigen, als wäre es nicht verfügbar**, ist in der Regel besser, wenn Sie den vollen Katalog dennoch durchsuchen möchten, auch in Regionen, in denen sie nicht auschecken können.
- Testen Sie das Regionenverhalten, indem Sie den Ship-To-Selector in Ihren Header aufnehmen und selbst zwischen Ländern wechseln, bevor Sie sich auf die GeoIP-Erkennung während eines Releases verlassen.
- Legen Sie die Prioritätswerte Ihrer Regionen (auf der Seite der Verkaufsregionen) bewusst fest – die am höchsten priorisierte aktive Region ist die Rückfalloption für Kunden, deren Land nicht erkannt werden kann oder nicht mit einer Region übereinstimmt.