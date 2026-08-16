---
title: Regionale Verfügbarkeit
---

Die regionale Verfügbarkeit steuert, in welchen Verkaufsregionen Ihres Produkts verkauft werden kann, und wie Käufer außerhalb dieser Regionen Ihr Katalogbild erleben. Sie verwenden dies, wenn ein Produkt nur für bestimmte Länder lizenziert ist, wenn Lagerbestände für den lokalen Markt reserviert sind oder wenn Sie ein neues Produkt schrittweise nach Regionen hin zurollen.

Dies baut auf **Verkaufsregionen** auf, die Länder in benannte Märkte gruppieren (siehe den Leitfaden zu den Verkaufsregionen für die Einrichtung). Sobald Ihre Regionen existieren, können Sie einzelnen Produkten diese zuweisen und entscheiden, wie eingeschränkte Produkte den Käufern angezeigt werden, die sie nicht kaufen können.

## Einschränken eines Produkts auf bestimmte Regionen

Jedes Produkt hat eine **Regionale Verfügbarkeit** auf seiner Bearbeitungsseite. Öffnen Sie **Produkte > Alle Produkte**, wählen Sie ein Produkt aus und finden Sie es im **Status**-Abschnitt neben **Status**, **Hervorgehoben** und **Vom Verkaufsort ausblenden**.

![Der Status-Abschnitt des Produktbearbeitungsformulars mit der Dropdown-Liste für die regionale Verfügbarkeit, die auf "Nur in ausgewählten Regionen" eingestellt ist, neben Hervorgehoben und Vom Verkaufsort ausblenden](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Option | Was es bedeutet |
|--------|-----------------|
| **In allen Regionen verfügbar** | Keine Einschränkung. Das Produkt wird überall verkauft. Dies ist die Standardeinstellung für jedes Produkt. |
| **Nur in ausgewählten Regionen** | Eine Erlaubnisliste. Das Produkt wird nur in den Regionen verkauft, die Sie unten auswählen - überall sonst wird es als nicht verfügbar betrachtet. |
| **Alle Regionen außer ausgewählten** | Eine Sperrliste. Das Produkt wird überall verkauft, *außer* den Regionen, die Sie unten auswählen. |

### Regionen auswählen

Unter dem Status-Abschnitt wird eine Tabelle mit dem Titel **Regionale Verfügbarkeit (ausgewählte Regionen)** angezeigt, die die Regionen auflistet, auf die sich der obige Modus bezieht.

1. Legen Sie die **Regionale Verfügbarkeit** auf **Nur in ausgewählten Regionen** oder **Alle Regionen außer ausgewählten** fest.
2. In der Tabelle **Regionale Verfügbarkeit (ausgewählte Regionen)** klicken Sie auf **Another Region hinzufügen** und wählen Sie eine Verkaufsregion.
3. Wiederholen Sie dies für jede Region, die Sie hinzufügen möchten.
4. Klicken Sie auf **Speichern**.

![Die Inline-Tabelle "Regionale Verfügbarkeit (ausgewählte Regionen)" mit den Zeilen Nordamerika und Europa](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Wenn die **Regionale Verfügbarkeit** auf **In allen Regionen verfügbar** eingestellt ist, wird alles in dieser Tabelle ignoriert – löschen Sie zuerst den Modus-Dialog, wenn Sie eine Einschränkung aufheben möchten, ohne die Zeilen zu löschen.

Für eine Katalog-übergreifende Ansicht aller Produktspezifikationen in einer Liste (hilfreich, wenn Sie viele Produkte gleichzeitig auditieren), gehen Sie zu **Produktregionen-Sichtbarkeit** unter `/admin/catalog/productregionvisibility/`.

## Anzeigen, in welchen Regionen ein Produkt nicht versandt wird

Wenn sich die Region des Kunden nicht mit den Verkaufsregeln des Produkts übereinstimmt, kontrollieren Sie, was sie in **Stock Display Settings**, unter dem **Regionale Verfügbarkeit**-Abschnitt sehen. Diese Seite hat noch keinen Sidebar-Kurzbefehl – öffnen Sie sie direkt unter `/admin/catalog/stockdisplaysettings/`.

![Stock Display Settings, Regionale Verfügbarkeit-Abschnitt – die Dropdown-Liste für die regionale Einschränkung, auf "Anzeigen, als nicht verfügbar markiert" eingestellt](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Option | Was Käufer sehen |
|--------|------------------|
| **Anzeigen, als nicht verfügbar markiert** (Standard) | Das Produkt wird weiterhin in Listen angezeigt, mit einem "Nicht verfügbar"-Stichwort und einer "Wird nicht an [Region] versandt"-Meldung anstelle des "Zum Warenkorb hinzufügen"-Buttons. Ein Banner erscheint zudem oben auf Listen-Seiten ("Einige Produkte werden nicht an [Zielort] versandt") mit einem Link, um nur die Artikel anzuzeigen, die dort versandt werden. |
| **Von Listen ausblenden** | Das Produkt wird für Käufer in dieser Region vollständig aus Listen und Suchergebnissen entfernt. |

![Storefront-Produktliste, Versand nach Europa – das "Einige Produkte werden nicht an Europa versandt"-Banner über dem Gitter und ein Produktkarten-Element mit "Nicht verfügbar" und einer "Wird nicht an Europa versandt"-Meldung](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

Eine eingeschränkte Produktseite zeigt immer eine Meldung an: „Dieses Produkt wird nicht in [Region] geliefert“, wenn ein Kunde sie direkt besucht (z. B. über einen geteilten Link oder Suchmaschinenergebnis) — dies gilt unabhängig davon, welche Listenoption Sie oben auswählen, da ein direkter Link die Liste vollständig umgeht.

## Den Kunden ermöglichen, ihre Region auszuwählen oder zu entdecken

Spwig kann die Region des Kunden automatisch erkennen und eine Auswahl anbieten, und Sie können einen Selektor hinzufügen, damit Kunden diese jederzeit selbst ändern können.

### Vorab

Sie benötigen zwei Dinge, um die Regionserkennung und -umschaltung korrekt zu konfigurieren:

1. **Verkaufsregionen** — die Länder in jeder Region und die Standardwährung jeder Region. Wenn Sie unter **Bestand** im Seitenleistenmenü **Verkaufsregionen** nicht sehen, aktivieren Sie **Mehrfachlager aktivieren** unter **Einstellungen > Store-Einstellungen > E-Commerce**, um das Menüeintrag zu aktivieren (Sie müssen nicht unbedingt mehrere Lager verwenden — dieser Einstellung dient nur dazu, das Menüelement zu entsperren). Sie können auch direkt zu `/admin/catalog/salesregion/` gehen.
2. **Versandländer** — die Länder, in die Ihr Geschäft tatsächlich versendet. Diese sind in der Regel bereits vorhanden: jedes Land, das Sie zu einem Versandgebiet hinzufügen, wird automatisch auch hier hinzugefügt. Um die Liste zu überprüfen oder manuell anzupassen, öffnen Sie direkt `/admin/shipping/shippingcountry/` (es verfügt derzeit noch nicht über einen Seitenleistenlink).

### Die automatische Regionbestätigung

Spwig erkennt die Region des Kunden anhand ihres Standorts und wendet sie automatisch an. Wenn dies sie in eine Region bringt, die *nicht* Ihr Geschäftsmarkt (primäre Region) ist — und Sie zwei oder mehr aktive Verkaufsregionen haben — zeigt Spwig bei ihrem ersten Besuch eine Bestätigung an, damit sie wissen, in welcher Region sie sich befinden, und sie diese ändern können:

> **Wir haben Ihre Region auf [Region] gesetzt**
> Wir haben dies anhand Ihres Standorts gewählt, damit Sie die richtigen Produkte und Preise sehen. Falsch? Wählen Sie Ihr Land aus.
> Liefern an: [Landewahl]  **[Weiterstöbern]**

![Die Bestätigungsmeldung "Wir haben Ihre Region auf Nordamerika gesetzt" auf dem Storefront, mit einem "Liefern an"-Landewahl-Widget und einem "Weiterstöbern"-Button](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Die Auswahl eines anderen Landes in der Auswahl ändert sie sofort. Das Verwerfen oder Klicken auf **Weiterstöbern** behält ihre aktuelle Region bei, und sie werden auf diesem Browser nicht erneut gefragt. Besucher, die bereits in ihrer Standardregion sind, erhalten die Bestätigung überhaupt nicht.

### Hinzufügen eines Lieferort-Selektors zu Ihrem Header oder Footer

Wenn Sie lieber möchten, dass Kunden ihre Region jederzeit selbst ändern können (anstelle sich nur auf den automatischen Hinweis zu verlassen), fügen Sie das **Lieferort-Selektor-Widget** Ihrem Header oder Footer hinzu.

1. Navigieren Sie zu **Design > Header Builder** (oder **Footer Builder**).
2. Ziehen Sie das **Lieferort-Selektor-Widget** aus der Widget-Bibliothek in eine Zeile.
3. Klicken Sie auf **Speichern**.

![Die Widget-Bibliothek des Header Builders mit dem Gruppe "Shop" hervorgehoben, wobei das Lieferort-Selektor-Widget neben dem Einkaufswagen, dem Kontomenu und dem Sprachauswahlfeld angezeigt wird](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Das Widget benötigt keine Einrichtung — es listet Ihre aktiven Versandländer automatisch auf, und es zeigt die aktuelle Auswahl des Kunden an (oder das GeoIP-erkannte Land, falls der Kunde noch kein Land ausgewählt hat). Das Auswählen eines anderen Landes aktualisiert sofort deren Region und lädt die Produktverfügbarkeit und Preise der Seite neu.

Das Lieferort-Selektor-Widget verfügt derzeit noch nicht über eine eigene Einstellungsformular. Wenn Sie das Aussehen des Buttons (Outline, Solid oder Ghost) ändern oder das „Liefern an“-Label verstecken möchten, öffnen Sie die Einstellungen des Widgets im Builder und bearbeiten Sie das Feld **Benutzerdefinierte Konfiguration (JSON)** direkt, und verwenden Sie `button_style` und `show_label`.

### Währung folgt der Region

Wenn Ihr Geschäft mehr als eine Währung unterstützt (unter **Einstellungen > Mehrere Währungen** festgelegt), ändert sich mit dem Wechsel der Region — sei es über den Hinweis oder den Lieferort-Selektor — auch die angezeigte Währung auf die Standardwährung dieser Region.

Wenn Ihr Geschäft nur eine Währung hat oder keine explizite Aktivierung einer zweiten Währung vorgenommen hat, wird die Währung beibehalten, wenn ein Kunde die Region wechselt.

## Tipps

- Lassen Sie die **Regionenverfügbarkeit** auf **In allen Regionen verfügbar** stehen, es sei denn, Sie haben einen spezifischen Grund, ein Produkt einzuschränken – dies ist die einfachste Option und benötigt keinen Wartungsaufwand, wenn Sie später weitere Regionen hinzufügen.
- Verwenden Sie **Nur in ausgewählten Regionen** für eine kleine Whitelist (z. B. ein Produkt, das zunächst in einem Land lanciert wird), und **Alle Regionen außer ausgewählten** für eine kleine Blacklist (z. B. überall außer einem Land, in dem das Produkt nicht lizenziert ist) – wählen Sie, welche weniger Zeilen zum Einrichten benötigt.
- Wenn Kunden berichten, dass ein Produkt fehlt, das sichtbar sein sollte, prüfen Sie sowohl die Einstellung **Regionenverfügbarkeit** des Produkts als auch, ob ihr Land von einer aktiven **Verkaufsregion** und einer aktiven **Versandland**-Einstellung abgedeckt wird.
- **Aus der Liste ausblenden** hält Ihr Katalogbild sauber für Kunden, die bestimmte Artikel nicht kaufen können, aber es bedeutet auch, dass die Werbung und Suche in diesen Regionen dünner aussehen werden – **Anzeigen, als wäre es nicht verfügbar** ist in der Regel besser, wenn Sie möchten, dass Kunden auch in Regionen, in denen sie nicht bezahlen können, Ihren gesamten Katalog durchsuchen.
- Testen Sie das Verhalten von Regionen, indem Sie den Ship-To-Selector in Ihre Kopfzeile aufnehmen und selbst zwischen Ländern wechseln, bevor Sie sich auf die GeoIP-Erkennung während eines Launches verlassen.
- Legen Sie die Prioritätswerte Ihrer Regionen (auf der Seite Verkaufsregionen) bewusst fest – die hochpriorige aktive Region ist der Rückfalloption für Kunden, deren Land nicht erkannt werden kann oder nicht mit einer Region übereinstimmt.