---
title: Produkte als Abonnements verkaufen
---

Jedes einfache, variable oder digitale Produkt kann nun als wiederkehrende Bestellung angeboten werden, neben — oder anstelle — einer Einzelbestellung. Dieser Leitfaden beschreibt, wie Sie die Abonnements für ein Produkt aktivieren, welche Pläne Kunden auswählen können, und was Ihre Kunden beim Kauf tatsächlich sehen.

## Welche Produkttypen können als Abonnements verkauft werden

Abonnements sind nur für diese Produkttypen verfügbar:

| Eignung | Nicht eignungsgemäß |
|----------|-------------------|
| Einfaches Produkt | Produktbündel |
| Variablers Produkt | Gutscheinkarte |
| Digitales Produkt | Anpassbares Produkt |
| | Konfigurierbares Produkt |
| | Buchungsprodukt |

Der Grund ist die Abholung, nicht der Preis: ein Abonnement erhebt dem Kunden in jedem Zyklus erneut und liefert das Produkt über eine neue Bestellung erneut. Spwig weiß, wie man ein einfaches oder variables Produkt erneut versendet und ein digitales Produkt bei jeder Erneuerung erneut herunterlädt oder lizenziert — aber es kann ein Gutscheinguthaben nicht sicher erneut ausstellen, ein mehrteiliges Bündel, eine gespeicherte Anpassung des Kunden, einen Konfigurationsbau oder einen Buchungstermin in einem wiederkehrenden Zeitraum nicht sicher erneut ausführen. Wenn diese Arten als Abonnements verkauft werden, besteht die Gefahr, dass der Kunde in Zyklus 2 Geld erhält, ohne etwas liefern zu können.

Das **Abonnement aktivieren**-Kontrollkästchen ist für nicht eignungsgemäße Typen nicht versteckt oder grau markiert — Sie können es theoretisch auf jedem Produkt aktivieren. Wenn Sie versuchen, eine Gutscheinkarte, ein Bündel, ein anpassbares, konfigurierbares oder ein Buchungsprodukt mit aktivierten Abonnements zu speichern, lehnt Spwig die Speicherung mit einer Validierungsfehlermeldung ab, die besagt, dass dieser Produkttyp nicht als Abonnement verkauft werden kann. Ändern Sie zuerst den **Produkttyp** (Registerkarte Grundlegende Informationen) oder lassen Sie die Abonnements für dieses Produkt deaktiviert.

## Aktivieren von Abonnements für ein Produkt

1. Navigieren Sie zu **Produkte > Alle Produkte** und öffnen Sie das Produkt, das Sie als Abonnement verkaufen möchten (oder erstellen Sie ein neues).
2. Stellen Sie sicher, dass der **Produkttyp** auf der Registerkarte Grundlegende Informationen ein einfaches, variables oder digitales Produkt ist.
3. Klicken Sie auf die Registerkarte **Abonnements**.
4. Klicken Sie auf **Abonnement aktivieren**.
5. Wählen Sie im Feld **Abonnementpläne** einen oder mehrere Pläne aus, unter denen dieser Produkttyp angeboten werden soll. Sie können nur Pläne auswählen, die bereits existieren — wenn Sie noch keine erstellt haben, sehen Sie sich zunächst [Abonnementpläne](/help/subscription-plans) an.
6. Konfigurieren Sie die beiden Kaufmodus-Kontrollkästchen (unterhalb).
7. Klicken Sie auf **Speichern**.

![Die Registerkarte "Abonnements" des Produktbearbeitungsformulars: "Abonnement aktivieren" ist aktiviert, ein Plan in der Liste der Abonnementpläne ausgewählt und die Kontrollkästchen "Einzelkauf erlauben" und "Standardmäßig zu Abonnement wechseln"](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Anhängen von Abonnementplänen

Ein **Abonnementplan** ist eine wiederverwendbare Vorlage — Zahlungszyklus-Optionen, Probezeit, Einrichtungsgebühr, Kündigungsbedingungen — die Sie einmal erstellen und an jeden beliebigen geeigneten Produkttyp anhängen können. Das Feld **Abonnementpläne** auf der Registerkarte **Abonnements** des Produkts ist der Ort, an dem Sie das Produkt mit den Plänen verknüpfen, unter denen es verkauft werden soll.

Sie können mehr als einen Plan an dasselbe Produkt anhängen. Dies ist nützlich, wenn Sie beispielsweise für dasselbe Produkt eine "Standard"- und eine "Premium"-Wiederkehrend-Tarif anbieten möchten — jeder Plan kann seine eigenen Preisstufen, Probezeit und Kündigungsbedingungen tragen. Wenn ein Produkt mehr als einen Plan anhängt, sehen Kunden auf der Produktseite vor dem Auswählen des Zahlungsintervalls einen Planwähler.

## Steuern von Einzelkauf vs. Abonnementkauf

Zwei Kontrollkästchen auf der Registerkarte **Abonnements** steuern, wie Kunden das Produkt kaufen können:

- **Einzelkauf erlauben** — Standardmäßig aktiviert.

Wenn dieses Kontrollkästchen aktiviert ist, wählen Kunden zwischen einem regulären Einzelkauf und einem Abonnement.

Deaktivieren Sie es, um das Produkt ausschließlich als Abonnement zu machen — jeder Kauf wird zu einer Wiederkehrend-Bestellung, und es wird überhaupt kein Einzelkaufoption angezeigt.
- **Standardmäßig zu Abonnement wechseln** — wählt die Abonnementoption (und ihren Standardplan/Tarif) beim Laden der Produktseite vor, anstatt Kunden, aktiv dafür zu wählen.

Dies hat nur dann Auswirkungen, wenn auch **Einzelkauf erlauben** aktiviert ist — wenn der Einzelkauf deaktiviert ist, ist das Produkt unabhängig von dieser Einstellung ausschließlich als Abonnement erhältlich.

Verwenden Sie **Standardmäßig Abonnement** für Produkte, bei denen die wiederkehrende Lieferung die natürliche Erwartung ist (Kaffee, Nahrungsergänzungsmittel, Verbrauchsgüter) — dadurch wird ein Klick eingespart und Kunden werden in Richtung der Option gedrängt, die sie wiederkehrend kommen lässt, ohne ihre Fähigkeit zu entfernen, einfach nur einmal zu kaufen.

## Was Kunden sehen

### Auf der Produktseite

Wenn ein Produkt Abonnements unterstützt und mindestens ein aktives, öffentliches Abonnement angehängt ist, erscheint auf der Produktseite ein Kaufmodus-Selector:

![Der Store- Kauf-Selector mit "Abonnieren & sparen" ausgewählt: ein Einzelkauf vs. Abonnieren & sparen-Weiche über einer Lieferhäufigkeitsliste mit jährlichen (20 % sparen), monatlichen und vierteljährlichen (10 % sparen) Stufen mit Preisen sowie Probephase, Kündigung und Zahlungshinweisen](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Wenn Einzelkauf erlaubt ist, sehen Kunden eine **"Einzelkauf"** vs. **"Abonnieren & sparen"** Wahl, wobei der Standardmodus die von Ihnen konfigurierte Einstellung ist.
- Wenn dem Produkt mehrere Pläne zugeordnet sind, erscheint ein Planwähler, sobald "Abonnieren & sparen" ausgewählt wird.
- Für den ausgewählten Plan sehen Kunden eine **Lieferhäufigkeit**-Liste, die aus den Preistufen dieses Plans besteht (z. B. Monatlich, Vierteljährlich, Jährlich), wobei jede Stufe ihren Preis und ein **"Sparen Sie X%"**-Abzeichen zeigt, wenn die Stufe einen Rabatt hat.
- Probelaufdauer, Einrichtungsgebühr und der Kündigungsbedingungen des Plans (z. B. "Jederzeit kündbar") werden neben der Stufenliste angezeigt, sowie eine Notiz, dass bei der Kasse eine Zahlungsmethode hinzugefügt wird.

### In dem Warenkorb und bei der Kasse

Abonnementzeilen im Warenkorb tragen ein **Abonnement**-Abzeichen, die Abrechnungshäufigkeit (z. B. "Alle Monate") und bei Anwendung ein Probephase, damit klar ist, welche Zeilen wiederverkauft werden. Bei der Kasse wählt der Kunde einen Zahlungsanbieter wie üblich — dies ist die Zahlungsmethode, die bei zukünftigen Erneuerungen belastet wird.

> **Bekannte Einschränkung:** Das automatische Speichern der Karte eines Kunden für zukünftige Abonnementerneuerungen bei der Kasse ist bei einigen Zahlungsanbietern noch nicht verbunden. Bis ein bestimmter Anbieter dies unterstützt, können Abonnements, die über ihn platziert werden, möglicherweise zusätzliche Nachverfolgung benötigen (z. B. Kontaktaufnahme mit dem Kunden für aktualisierte Zahlungsdetails vor einer Erneuerung), anstatt von Anfang an vollständig problemlos zu sein. Prüfen Sie bei Anomalien bei Erneuerungen, ob die automatische Belastung für ein Abonnement nicht funktioniert, bei Ihrem Zahlungsanbieter nach.

## Tipps

- Legen Sie zuerst das Abonnementplan an (Preistufen, Probephase, Kündigungsbedingungen) und heften Sie es dann an Produkte an — es ist einfacher, den Plan richtig zu bekommen, als ihn später über mehrere Produkte hinweg zu korrigieren.
- Lassen Sie **Einzelfallkauf erlauben** bei den meisten Produkten aktiviert. Reservieren Sie Abonnement-exklusive Produkte für Fälle, in denen ein Einzelkauf für Ihr Unternehmen tatsächlich keinen Sinn macht.
- Wenn Sie ein bestehendes Bestseller-Produkt in eine Abonnementoption umwandeln, halten Sie **Standardmäßig Abonnement** zunächst aus, damit Sie Kunden nicht stören, die es normalerweise einmal kaufen — schalten Sie es später ein, sobald Sie gesehen haben, wie sich Abonnenten verhalten.
- Digitale Produkte sind hervorragend für Abonnements geeignet (Software-Lizenzen, Inhaltsmitgliedschaften), da die Erneuerung automatisch den Zugriff erneut gewährt, ohne dass Versand beteiligt ist.
- Wenn Sie eine Produktart benötigen, die nicht für wiederkehrende Verkäufe geeignet ist (z. B. ein Paket oder ein anpassbares Produkt), überlegen Sie, ob eine vereinfachte Version oder ein digitales Äquivalent das Abonnement tragen könnte.