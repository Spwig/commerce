---
title: Feldzuordnung bei der Migration
---

Jede Plattform benennt Dinge etwas anders – WooCommerce's `regular_price` ist nicht dasselbe wie Shopify's `price`, und eine CSV-Spalte namens `barcode` könnte genau dasselbe sein, was Spwig unter `sku` erwartet. Schritt 4 des Migrations-Assistenten, **Feldzuordnung konfigurieren**, ist der Ort, an dem Sie prüfen können, wie Ihre Quelldaten in Spwig landen, bevor die tatsächliche Importierung stattfindet. Dieses Thema behandelt jeden Block auf dieser Seite und gilt für WooCommerce, Shopify, Magento und CSV-Migrationen, wobei Unterschiede zwischen den Plattformen dort hervorgehoben werden, wo sie relevant sind. Für Anmeldeinformationen und die früheren Schritte des Assistenten siehe [Migrating from WooCommerce](migrate-from-woocommerce) oder den entsprechenden Leitfaden für Ihre Plattform.

## Automatische Zuordnungen

Dieser Block zeigt für jeden Datentyp, den Sie im Schritt 3 ausgewählt haben, eine schreibgeschützte Liste der Quellfelder und dem Spwig-Feld, auf das jedes Feld abgebildet wird – beispielsweise wird das Feld `name` eines Produkts auf den Produkttitel in Spwig abgebildet oder das Feld `email` eines Kunden auf die E-Mail-Adresse des Kontos. Nur die Datentypen, die Sie tatsächlich importieren, werden hier angezeigt; wenn Sie beispielsweise in Schritt 3 keine Bewertungen ausgewählt haben, gibt es auf dieser Seite keinen Abschnitt für Bewertungen.

Da diese Zeilen schreibgeschützt sind, gibt es nichts zu konfigurieren – sie existieren, damit Sie die Zuordnung vor der tatsächlichen Importierung überprüfen können. Wenn eine Zuordnung für Ihre Daten falsch aussieht, gibt es keine Möglichkeit, sie von diesem Bildschirm aus zu überschreiben; Ihre Optionen sind, die Quelldaten vor der Migration zu korrigieren oder die betroffenen Datensätze in Spwig nach Abschluss des Imports zu korrigieren.

## CSV-Spaltenzuordnung

Dieser Block erscheint nur bei CSV-Migrationen, mit einer Tabelle pro hochgeladenen Datei. Spwig erkennt automatisch wahrscheinliche Übereinstimmungen anhand der Spaltenüberschriften – beispielsweise erkennt eine Zuordnung von `sku` auch Überschriften wie `barcode`, `part_number` oder `item_number` – also in den meisten Fällen müssen Sie hier nichts anpassen.

Jede CSV-Spalte enthält ein Dropdown-Menü, das die Felder auflistet, die Spwig für diesen Dateityp erwartet:

- **products** – `id, name, slug, description, price, sku, stock_quantity, category`
- **categories** – `id, name, slug, description, parent_id`
- **customers** – `id, email, first_name, last_name, phone`
- **orders** – `id, customer_email, order_date, status, total, currency`
- **reviews** – `id, product_id, customer_email, rating, comment, date`

Jedes Dropdown-Menü enthält auch **— Diese Spalte überspringen —**, was diese Spalte vollständig vom Import ausschließt. Überschreiben Sie die automatisch erkannte Zuordnung, wenn Ihre Überschrift eine Namenskonvention verwendet, die Spwig nicht erkannt hat, oder wenn eine Spalte tatsächlich nichts mit den Feldern zu tun hat, die Spwig importiert (z. B. ein interner Notizfeld) – wählen Sie „Überspringen“ anstelle davon, sie dem nächsten verfügbaren Feld zuzuordnen.

## Benutzerdefinierte Felder

Dieser Block ist nur für WooCommerce verfügbar. Spwig nimmt 10 Produkte, Kunden und Bestellungen aus Ihrem Geschäft und listet alle benutzerdefinierten Metadatenfelder auf, die es außerhalb der Standard-WooCommerce-Felder findet, zusammen mit dem erkannten Typ und einem Beispielwert.

Für jedes Feld wählen Sie, wohin es abgebildet werden soll:

- **Zuordnen zu** – Benutzerdefiniertes Feld 1, 2 oder 3 für Produkte (Benutzerdefiniertes Feld 1 oder 2 für Kunden und Bestellungen), oder **Metadaten (JSON)** als Allzweckoption, wenn Sie mehr benutzerdefinierte Felder haben als die nummerierten Slots, oder lassen Sie es als **— Dieses Feld überspringen —**.
- **Transformieren** – wie der Wert auf dem Weg in Spwig konvertiert werden soll: Als Text, Als Zahl (Ganzzahl), Als Dezimalzahl, Als Wahr/Falsch (Boolesch), Als JSON, Als Datum, Als URL oder Als E-Mail.

> **Hinweis:** Metafelder von Shopify werden von dieser Funktion überhaupt nicht erkannt – bei Shopify-Migrationen wird niemals ein Block für benutzerdefinierte Felder angezeigt, egal wie viel Metafeld-Daten Ihr Geschäft hat. Wenn Sie auf Shopify-Metafelder angewiesen sind, um Produkt-Spezifikationen, Kundenattribute oder ähnliches zu speichern, planen Sie, diese Daten nach Abschluss des Imports manuell in Spwig einzugeben.

Wenn Spwig in Ihrem Beispiel keine benutzerdefinierten Felder erkennt, sehen Sie stattdessen eine Bestätigungsmitteilung und es gibt nichts weiteres zu konfigurieren.

Wenn einige Ihrer Quellkategorien in Spwig keine offensichtliche Übereinstimmung haben, bietet dieser Block drei Optionen: **Neue Kategorien erstellen**, **Zu Standardkategorie zuweisen** (eine "Unkategorisiert"-Zielkategorie) oder **Elemente mit nicht zugeordneten Kategorien überspringen**.

> **Hinweis:** Egal welche Option Sie hier auswählen, erstellt Spwig derzeit automatisch eine passende Kategorie für jedes Produkt, das Quellkategoriedaten hat, und greift nur auf "Unkategorisiert" zurück, wenn ein Produkt überhaupt keine Kategorieninformationen hat. Sie müssen sich nicht den Kopf darüber zerbrechen – wenn Sie später Kategorien haben, die Sie nicht wollen, ist es schneller, sie im **Katalog > Kategorien** nach dem Import zu mergen oder zu löschen, als auf diese Einstellung zu vertrauen.

## Steuern, Versand und Preis-Einstellungen

Der letzte Block, **Steuern & Versandseinstellungen**, hat drei Steuerelemente: **Steuereinstellungen importieren**, **Versandzonen und -methoden importieren** und einen **Preisanpassungstyp** und einen Wert.

Die beiden Häkchen beeinflussen derzeit den Import nicht – Steuersätze oder Versandzonen werden unabhängig davon, wie sie auf Ihrer alten Plattform festgelegt sind, nicht von Ihrem alten System übertragen. Konfigurieren Sie beide direkt in Spwig nach Abschluss des Imports: Steuersätze unter **Einstellungen > Steuern & Währung**, Versandzonen und -methoden unter **Einstellungen > Versand**.

**Preisanpassung** verhält sich je nach Quellplattform unterschiedlich:

- **WooCommerce, CSV und Shopify-Migrationen** – dieses Steuerelement funktioniert wie beschrieben. Wählen Sie **Prozent** oder **Fixer Betrag**, geben Sie einen Wert ein (z. B. `10` für eine 10 % Erhöhung oder `-5` für eine 5 $ Reduzierung), und der Grundpreis jedes Produkts wird während des Imports um diesen Betrag angepasst. Es gilt nur für den Grundpreis – Verkaufs-/Vergleichspreise werden unverändert übertragen.
- **Magento-Migrationen** – das gleiche Steuerelement erscheint auf der Seite, hat aber keine Auswirkung; Magento-Preise werden unverändert importiert, unabhängig davon, was Sie eingeben. Wenn Sie bei einer Magento-Migration eine allgemeine Preisanpassung benötigen, wenden Sie sie nach dem Import mithilfe der Massenpreis-Tools im Katalog von Spwig an, nicht über dieses Feld.

> **Warnung:** Wenn Sie sich von WooCommerce, CSV oder Shopify migrieren und keine Preisanpassung möchten, lassen Sie **Preisanpassung** auf **Keine** stehen. Es ist das einzige Steuerelement auf dieser Seite, das Ihre Daten tatsächlich verändert, und es ist leicht, fälschlicherweise anzunehmen, dass es sich genauso verhält wie die Steuer- und Versand-Häkchen direkt darüber.

## Abbildungen werden für das nächste Mal gespeichert

Egal, was Sie auf dieser Seite konfigurieren, wird mit dem Migrationstask gespeichert, und Spwig verwendet es als Ausgangspunkt für zukünftige Migrationen von der gleichen Plattform – nützlich, wenn Sie eine schrittweise Migration durchführen (zuerst Kategorien und Produkte, später Bestellungen) oder nach der Behebung eines Datenproblems erneut importieren müssen. Sie können auch gespeicherte Abbildungen nach Abschluss einer Migration über die Schaltfläche **Feldabbildungen** auf dem Migrationsdashboard ansehen und anpassen, ohne den gesamten Assistenten erneut durchlaufen zu müssen.

## Tipps

- **Überprüfen Sie den Block Automatische Abbildungen, auch wenn Sie ihn nicht bearbeiten können** – das Erkennen eines falschen Abbildungsversuchs, bevor Sie auf Start Import klicken, ist viel günstiger als das Korrigieren von Hunderten importierter Datensätze danach.
- **Benennen Sie unsichere CSV-Überschriften vor dem Hochladen um**, wenn die automatische Erkennung sie nicht erkannt hat, anstatt versuchen, ein nicht passendes Feld über das Dropdown zu zwingen.
- **Verwenden Sie Metadaten (JSON) als Überlauf für benutzerdefinierte Felder** – es ist das einzige Abbildungsziel, das nicht nach zwei oder drei Feldern ausläuft.
- **Verlassen Sie sich nicht auf diese Seite für Steuern, Versand oder (bei Magento) Preise** – behandeln Sie diese als manuelle Einrichtungsaufgabe direkt nach dem Import, nicht als etwas, das der Assistent für Sie erledigt.
- **Lassen Sie Preisanpassung bei Ihrer ersten Ausführung einer neuen Migration auf Keine**, dann verwenden Sie eine kleine Testbatch, um die Mathematik zu bestätigen, bevor Sie sie auf Ihren gesamten Katalog anwenden.