---
title: Produkte als Abonnements verkaufen
---

Jedes einfache, variable oder digitale Produkt kann nun auf abonnementbasiester Basis verkauft werden, neben — oder anstelle — eines Einzelkaufs. Dieser Leitfaden beschreibt, wie Sie das Abonnement für ein Produkt aktivieren, welche Pläne Kunden auswählen können, und was Ihre Kunden beim Kauf tatsächlich sehen.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: Das Bearbeitungsformular für Produkte mit aktiviertem Abonnement-Reiter, wobei
    das Kontrollkästchen "Abonnement aktivieren" markiert ist, eine oder mehrere Pläne in der
    Feldern "Abonnementpläne" ausgewählt wurden, und die Kontrollkästchen "Einzelkauf
    erlauben / Standard auf Abonnement setzen" sichtbar sind.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (storefront) Produkt-Detailseite für ein abonnementfähiges Produkt
  filename: subscribe-and-save-selector.webp
  description: Der Store-"Einzelkauf" vs. "Abonnieren & Sparen"-Auswahl-Modus,
    erweitert, wobei eine Lieferhäufigkeits-Tarifliste mit einem "X% sparen"-Etikett
    auf den Rabatt-Tarifen angezeigt wird.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Erfordert ein echtes abonnementfähiges Produkt mit mindestens einem
    aktiven öffentlichen Plan und Preistarifen, im Store (nicht im Admin) angesehen.
-->

## Welche Produkttypen können als Abonnements verkauft werden

Abonnements sind nur für diese Produkttypen verfügbar:

| Eignung | Nicht eignung |
|----------|---------------|
| Einfaches Produkt | Produktbündel |
| Variablen Produkt | Gutscheinkarte |
| Digitales Produkt | Anpassbares Produkt |
| | Konfigurierbares Produkt |
| | Buchungsprodukt |

Der Grund ist die Erfüllung, nicht der Preis: ein Abonnement erhebt dem Kunden in jedem Zyklus erneut und liefert das Produkt über einen neuen Auftrag. Spwig weiß, wie man ein einfaches oder variables Produkt erneut versendet und ein digitales Produkt bei jeder Erneuerung erneut gewährt — aber es kann ein Gutschein nicht sicher erneut ausstellen, ein mehrkomponentiges Bündel, eine angemeldete Anpassung des Kunden, einen Konfigurationsbau oder einen Buchungstermin nicht sicher auf einem wiederkehrenden Zeitplan erneut ausführen. Die Verkaufsart als Abonnement für diese Arten zu erlauben, würde das Risiko bedeuten, den Kunden im zweiten Zyklus das Geld zu nehmen, ohne etwas liefern zu können.

Das Kästchen **Abonnement aktivieren** ist für nicht eignungsfähige Arten nicht versteckt oder grau markiert — Sie können es theoretisch auf jedem Produkt markieren. Wenn Sie versuchen, ein Produkt mit Gutscheinkarte, Bündel, anpassbarem Produkt, konfigurierbarem Produkt oder Buchungsprodukt mit Abonnements zu speichern, lehrt Spwig den Speicher mit einer Validierungsfehlermeldung ab, dass dieser Produkttyp nicht als Abonnement verkauft werden kann. Ändern Sie zuerst die **Produktart** (Basic Info-Reiter), oder lassen Sie die Abonnements für dieses Produkt aus.

## Aktivieren von Abonnements auf einem Produkt

1. Navigieren Sie zu **Produkte > Alle Produkte** und öffnen Sie das Produkt, das Sie als Abonnement verkaufen möchten (oder erstellen Sie ein neues).
2. Stellen Sie sicher, dass die **Produktart** auf dem Basic Info-Reiter **Einfach**, **Variabel** oder **Digital** ist.
3. Klicken Sie auf den **Abonnements**-Tab.
4. Klicken Sie auf **Abonnement aktivieren**.
5. Wählen Sie in dem Feld **Abonnementpläne** einen oder mehrere Pläne aus, unter denen dieses Produkt angeboten werden soll. Sie können nur Pläne auswählen, die bereits existieren — wenn Sie noch keine erstellt haben, sehen Sie sich zunächst [Abonnementpläne](/help/subscription-plans) an.
6. Konfigurieren Sie die beiden Kaufmodus-Kontrollkästchen (unterhalb).
7. Klicken Sie auf **Speichern**.

## Anhängen von Abonnementplänen

Ein **Abonnementplan** ist eine wiederverwendbare Vorlage — Wiederkehrigkeitsoptionen, Probezeit, Einrichtungsgebühr, Kündigungsbedingungen — die Sie einmal erstellen und an jeden beliebigen Anzahl von eignungsfähigen Produkten anhängen können. Das Feld **Abonnementpläne** auf dem Abonnement-Reiter des Produkts ist der Ort, an dem Sie ein Produkt mit den Plänen verknüpfen, unter denen es verkauft werden soll.

Sie können mehr als einen Plan an dasselbe Produkt anhängen.

Das ist nützlich, wenn Sie beispielsweise für dasselbe Produkt eine "Standard"- und eine "Premium"-Wiederkehrend-Tarif anbieten möchten — jeder Plan kann seine eigenen Preisstufen, Probezeit und Kündigungsbedingungen tragen.

Behalten Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

Wenn ein Produkt mehrere Pläne hat, sehen Kunden auf der Produktseite vor der Wahl der Zahlungshäufigkeit einen Plan-Auswahllistensymbol.

## Steuern Sie Einmalkauf vs. Abonnements

Zwei Kontrollkästchen auf dem Tab "Abonnements" steuern, wie Kunden das Produkt kaufen können:

- **Einfache Einmalzahlung erlauben** — Standardmäßig aktiviert. Wenn dieses Kästchen aktiviert ist, wählen Kunden zwischen einem regulären Einzelkauf und einem Abonnement. Deaktivieren Sie es, um das Produkt zu Abonnement-Only zu machen - jeder Kauf wird zu einem wiederkehrenden Auftrag, und es wird überhaupt keine Einzelkauf-Option angezeigt.
- **Standardmäßig zu Abonnement wechseln** — Wählt die Abonnement-Option (und deren Standardplan/Tarif) beim Laden der Produktseite vor, anstatt Kunden aktiv wählen zu lassen. Dies hat nur Auswirkungen, wenn **Einfache Einmalzahlung erlauben** ebenfalls aktiviert ist - wenn Einzelkauf deaktiviert ist, ist das Produkt abonnementspezifisch, unabhängig von diesem Einstellung.

Verwenden Sie **Standardmäßig zu Abonnement wechseln** für Produkte, bei denen die wiederkehrende Lieferung die natürliche Erwartung ist (Kaffee, Nahrungsergänzungsmittel, Verbrauchsgüter) - es entfernt einen Klick und lenkt Kunden in die Richtung, die sie zurückkehren lässt, ohne ihre Fähigkeit zu entfernen, einfach einmal zu kaufen.

## Was Kunden sehen

### Auf der Produktseite

Wenn ein Produkt Abonnements aktiviert hat und mindestens einen aktiven, öffentlichen Plan hat, erscheint auf der Produktseite ein Kaufmodus-Selector:

- Wenn Einzelkauf erlaubt ist, sehen Kunden eine **"Einzelkauf"** vs. **"Abonnieren & sparen"**-Auswahl, wobei der Standardmodus die von Ihnen konfigurierte Option ist.
- Wenn das Produkt mehr als einen Plan hat, erscheint ein Plan-Auswahllistensymbol, sobald **"Abonnieren & sparen"** ausgewählt wird.
- Für den ausgewählten Plan sehen Kunden eine **Lieferhäufigkeit**-Liste, die aus den Preistarifen dieses Plans besteht (z. B. Monatlich, Quartalsweise, Jahresweise), wobei jeder Tarif seinen Preis und ein **"Sparen X%"**-Abzeichen zeigt, wenn der Tarif einen Rabatt hat.
- Die Dauer des Probetests, Gebühr für die Einrichtung und die Kündigungsbedingungen des Plans (z. B. "Jederzeit kündbar") werden neben der Tarifliste angezeigt, sowie eine Notiz, dass bei der Kasse eine Zahlungsmethode hinzugefügt wird.

### In dem Warenkorb und bei der Kasse

Abonnementzeilen im Warenkorb tragen ein **Abonnement**-Abzeichen, die Zahlungshäufigkeit (z. B. "Alle Monate") und eine Probetestsnotiz, falls eine zutrifft, damit klar ist, welche Zeilen wiederverwendbar sind. Bei der Kasse wählt der Kunde einen Zahlungsanbieter wie üblich - dies ist die Zahlungsmethode, die bei zukünftigen Erneuerungen belastet wird.

> **Bekannte Einschränkung:** Das automatische Speichern einer Karte des Kunden für zukünftige Abonnementerneuerungen bei der Kasse wird bei einigen Zahlungsanbietern noch verbunden. Bis ein spezifischer Anbieter dies unterstützt, können Abonnements, die durch ihn platziert werden, möglicherweise zusätzliche Nachverfolgung benötigen (z. B. Kontaktaufnahme mit dem Kunden für aktualisierte Zahlungsdetails vor einer Erneuerung), anstatt von Anfang an vollständig problemlos zu sein. Prüfen Sie bei Bedarf Ihre Zahlungsanbieter-Einrichtung, wenn Sie bemerken, dass bei einem Abonnement keine automatische Erneuerung stattfindet.

## Tipps

- Legen Sie zuerst den Abonnementplan an und testen Sie ihn (Preistarife, Probetests, Kündigungsbedingungen), und heften Sie ihn dann an Produkte - es ist einfacher, den Plan richtig zu machen, als ihn später an mehreren Produkten zu korrigieren.
- Lassen Sie **Einfache Einmalzahlung erlauben** für die meisten Produkte aktiviert. Reservieren Sie Abonnement-only-Produkte für Fälle, in denen ein Einzelkauf für Ihr Unternehmen tatsächlich keinen Sinn macht.
- Wenn Sie ein bestehendes Bestseller-Produkt in eine Abonnementoption umwandeln, lassen Sie **Standardmäßig zu Abonnement wechseln** zunächst deaktiviert, damit Sie Kunden nicht stören, die es gewohnt sind, es einmal zu kaufen - Schalten Sie es später ein, sobald Sie gesehen haben, wie sich Abonnenten verhalten.
- Digitale Produkte sind hervorragend für Abonnements geeignet (Software-Lizenzen, Inhaltsmitgliedschaften), da die Erneuerung den Zugriff automatisch erneut gewährt, ohne dass Versand beteiligt ist.
- Wenn Sie eine Produktart benötigen, die nicht für die wiederkehrende Verkaufsform geeignet ist (z. B. ein Paket oder ein anpassbares Produkt), überlegen Sie, ob eine vereinfachte Simple- oder Digitalequivalent-Version den Abonnement-Verkauf tragen könnte.