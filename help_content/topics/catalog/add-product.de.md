---
title: Produkt hinzufügen
---

Dies ist Teil 1 von 4 aus einem längeren Dokument.

<!-- screenshots-needed:
- url: /admin/catalog/product/<id>/change/
  filename: inventory-tab.webp
  description: Bestandsregister-Karte, nach unten gescrollt, um die physischen Attribute, Versand und Vorausverkaufskarten zusammen anzuzeigen (Versand erforderlich, ein bevorzugtes Versandpaket ausgewählt und Vorausverkauf aktiviert mit einem Veröffentlichungsdatum und einer Nachricht ausgefüllt, sodass alle neuen Felder in einem Schritt sichtbar sind).
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
  notes: Ersetzt die vorhandene inventory-tab.webp, die vor dem Vorhandensein der Versand- und Vorausverkaufskarten entstanden ist und nicht mehr mit dem Live-Formular übereinstimmt.
- url: /admin/catalog/product/<id>/change/
  filename: tags-card.webp
  description: Grundlegende Info-Karte, nach unten gescrollt, um die Tags-Karte anzuzeigen, mit ein paar Tags, die bereits dem Produkt im Tag-Auswahlfeld zugewiesen wurden.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: advanced-tab.webp
  description: Erweiterte Registerkarte mit der Produktseiten-Einstellungen-Karte (Dropdown-Menü für Seitenvorlage mit einer nicht standardmäßigen Option ausgewählt) und der technischen Details-Karte darunter.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
-->

Dieser Leitfaden führt Sie durch das Erstellen eines neuen Produkts in Ihrem Geschäft. Das Produktformular ist in Abschnitte unterteilt, die grundlegende Informationen, Medien, Preise, Bestand, SEO und vieles mehr abdecken — sodass Sie alles auf einen Schlag ausfüllen oder später zu den Abschnitten zurückkehren können.

## Einstieg

Gehen Sie über das Seitenmenü zu **Produkte > Alle Produkte**, um Ihren Produktkatalog anzuzeigen. Klicken Sie auf die Schaltfläche **+ Produkt hinzufügen** in der oberen rechten Ecke, um das Produktformular zu öffnen.

![Produktliste](/static/core/admin/img/help/add-product/product-list-page.webp)

## Grundlegende Informationen

Der Abschnitt **Grundlegende Informationen** ist der Ort, an dem Sie die Kernidentität Ihres Produkts definieren.

![Produktformular hinzufügen](/static/core/admin/img/help/add-product/add-product-form.webp)

### Pflichtfelder

- **Name** — Der dem Kunden angezeigte Produktname. Klicken Sie auf das Globus-Symbol, um Übersetzungen für andere Sprachen hinzuzufügen.
- **Slug** — URL-freundliche Version des Namens (automatisch generiert). Passen Sie ihn an, falls erforderlich.
- **SKU** — Ihre interne Artikelnummer.
- **Produkttyp** — Wählen Sie aus: Einfach, Variabel, Digital, Paket, Gutschein, Anpassbar, Konfigurierbar oder Buchung.
- **Kategorie** — Weisen Sie dem Produkt eine Kategorie zu, um es zu organisieren und für die Navigation im Geschäft zu verwenden.

### Status und Sichtbarkeit

Finden Sie dies im Abschnitt **Status** am Ende des Formulars:

- **Status** — Auf **Entwurf** setzen, während Sie arbeiten, **Veröffentlicht**, wenn es zum Verkauf bereit ist, oder **Nicht mehr erhältlich**, für Produkte, die Sie nicht mehr anbieten.
- **Als Highlight markieren** — Klicken Sie, um dieses Produkt auf Ihrem Geschäftshaus hervorzustellen.
- **Ist digitales Produkt** — Klicken Sie, wenn dieses Produkt digitale Downloads (Dateien, Lizenzen) enthält. Kann mit jedem Produkttyp kombiniert werden.
- **Vom Geschäftshaus ausblenden** — Blendet das Produkt von Katalogauflistungen ab, hält es aber als Konfigurierungs-Option oder Paketkomponente verfügbar.

### Optionale Felder

- **Marke** — Weisen Sie eine Marke zu, falls zutreffend.
- **Tags** — Weisen Sie einem oder mehreren Tags in der **Tags**-Karte weiter unten dieses Tabs zu. Tags sind von Sammlungen getrennt — sie sind schnelle, freie Bezeichnungen zur Organisation und Filterung von Produkten, anstatt eine Merchandising-Gruppierung zu sein. Geben Sie etwas ein, um nach einem vorhandenen Tag zu suchen, oder geben Sie einen neuen Namen ein, um einen On-the-Fly-Tag zu erstellen. Siehe das Hilfethema **Produkt-Tags**, um Tags direkt zu erstellen, zu benennen und in Massen zu löschen.

### Produktbeschreibungen

- **Kurzbeschreibung** — Erscheint in Produktlisten und Karten. Halten Sie sie kurz und überzeugend.
- **Vollständige Beschreibung** — Detaillierte Produktbeschreibung, die auf der Produktseitenansicht angezeigt wird. Verwenden Sie den Rich-Text-Editor, um Formatierung, Bilder, Videos und Tabellen hinzufügen.

Beide Beschreibungsfelder unterstützen das Übersetzungsfeature — klicken Sie auf das Globus-Symbol, um Inhalt in anderen Sprachen bereitzustellen.

### Merkmale und Spezifikationen

Bewahren Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

Der **Produktdetails-Bereich** enthält zwei strukturierte Datenfelder:

- **Eigenschaften** — Schlüssel-Wert-Paare für Produktmerkmale (z. B. "Akku-Laufzeit: 20 Stunden").
- **Spezifikationen** — Technische Details für den Spezifikationsreiter auf der Produktseite (z. B. "Prozessor: Intel i7").

## Medien

Der **Medien-Bereich** ermöglicht die Verwaltung von Produktbildern mit der integrierten Medienbibliothek.

![Reiter "Medien"](/static/core/admin/img/help/add-product/media-tab.webp)

1. Klicken Sie auf **+ Bilder aus der Medienbibliothek hinzufügen**, um den Medien-Editor zu öffnen.
2. Wählen Sie vorhandene Bilder aus oder laden Sie direkt neue Bilder hoch.
3. Ziehen Sie Bilder, um sie zu sortieren — das **erste Bild** wird zum Hauptproduktbild, das in Listen und Karten angezeigt wird.

Das Feld **Galerietyp**, in der Karte **Galerieeinstellungen** unter der Bildliste, steuert, wie Bilder im Shop angezeigt werden: Standardgalerie, Carousel, Rasterlayout, Zoomgalerie oder 360°-Ansicht.

## Preise

Legen Sie den Preis Ihres Produkts fest und richten Sie Rabatte ein.

![Reiter "Preise"](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Standardpreis

- **Standardpreis** — Der Standard-Retailpreis, den Kunden sehen werden. Die Währung wird neben dem Preisbetrag festgelegt.
- **Kosten** — Ihre Kosten für Waren, die für die Gewinnberechnung verwendet werden. Dies wird den Kunden nie angezeigt.

### Rabatt-Einstellungen

Richten Sie zeitweise Rabatte ein:

- **Rabatt-Typ** — Wählen Sie aus: Kein Rabatt, Fixer Rabattpreis, Betrag abziehen oder Prozentsatz abziehen.
- **Rabatt-Betrag** — Der Rabattbetrag oder der Prozentsatz.
- **Rabatt-Startdatum / Rabatt-Enddatum** — Legen Sie fest, wann der Rabatt aktiviert und abgelaufen ist. Lassen Sie dies leer, um sofortigen Start oder kein Enddatum zu haben.

### Mehrsprachige Preise

Wenn die Mehrfachwährungsfunktion in Ihrem Geschäft aktiviert ist, erscheint ein Feld **Preisstrategie**:

- **Dynamische Preise** — Preise in anderen Währungen werden automatisch mit den konfigurierten Wechselkursen berechnet.
- **Festpreis** — Legen Sie für jede Währung unabhängig einen spezifischen Preis fest, indem Sie den **Mehrfachwährungspreis**-Bereich verwenden, der danach erscheint.

## Lagerbestand

Verwalten Sie Lagerbestände, Versandverhalten und physische Produktmerkmale.

![Reiter "Lager"](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Lagerverwaltung

- **Lagerbestand überwachen** — Aktivieren Sie dies, um Lagerbestände zu überwachen (standardmäßig aktiviert).
- **Lagerbestandsschwelle** — Melden Sie, wenn der Bestand unter diese Zahl fällt (Standard: 5).
- **Rücklagen erlauben** — Aktivieren Sie dies, um Bestellungen zu akzeptieren, auch wenn das Produkt nicht auf Lager ist.
- **Lagerbestandsaktion** — Überschreiben Sie das site-weite oder Kategorien-Verhalten, wenn dieses Produkt ausverkauft ist: es verstecken, als nicht verfügbar anzeigen, eine "Benachrichtige mich"-Schaltfläche anbieten oder Rücklagen erlauben.

Lagerbestände werden pro Lager verwalten. Nachdem Sie das Produkt gespeichert haben, verwenden Sie den **Lagerbestand-Bereich** am Ende des Formulars (oder navigieren Sie zu **Produkte > Lagerbestände**), um Mengen an jedem Lagerort festzulegen.

### Physische Merkmale

Geben Sie das Gewicht des Produkts (kg) und die Maße (Länge, Breite, Höhe in cm) ein, um genaue Versandberechnungen durchzuführen.

### Versand

- **Benötigt Versand** — Ob dieses Produkt an den Kunden versandt werden muss. Standardmäßig aktiviert für physische Produkte; Ihr Shop und Checkout verwenden es, um zu entscheiden, ob ein Versandadresse gesammelt und der Versandkostenzuschlag für die Bestellung berechnet werden soll. Spwig schaltet es automatisch aus für digitale, Buchungs- und Gutscheinkarten-Produkte, da diese niemals versendet werden — Sie müssen es für diese Produkttypen nicht (und können es nicht) erneut aktivieren. Lassen Sie es aktiviert, für ein physisches Produkt, das beispielsweise wie eine digitale Gutscheinkarte aussieht, wie ein gedrucktes Gutscheinkarten-Produkt, das in einer Box versendet wird.
- **Vorgezogenes Versandpaket** — Wählen Sie optional eines Ihrer konfigurierten Versandpakete. Wenn festgelegt, werden die eigenen Maße des Pakets für die Versandkostenberechnung verwendet, anstatt das Gewicht und die Maße des Produkts oben anzugeben — nützlich, wenn ein Produkt immer in derselben Standardbox oder einem Umschlag versendet wird. Lassen Sie es leer, um das physische Gewicht und die Maße des Produkts zu verwenden. Verwalten Sie verfügbare Pakete unter **Versand > Pakete**.

### Vorbestellung

Use the **Vorbestellkarte** to sell a product before it has any stock — useful for upcoming releases you want to start taking orders for ahead of launch:

- **Ist Vorbestellung** — Aktivieren, damit Kunden dieses Produkt auch dann kaufen können, wenn es nicht auf Lager ist.
- **Vorbestellungsdatum** — Das erwartete Verkaufsdatum, das den Kunden angezeigt wird.
- **Vorbestellungsnachricht** — Eine kurze benutzerdefinierte Nachricht, die den Kunden angezeigt wird, bis zu 200 Zeichen (z. B. "Versand März 2026").

### Produktidentifikatoren

Standardproduktcodes für Marktplatzlisten und Lagerverwaltungssysteme:

- **GTIN** — Globaler Handelsartikelnr.
- **EAN** — Europäische Artikelnummer
- **UPC** — Universal Product Code (US)
- **ISBN** — Für Bücher
- **ASIN** — Amazon-Identifikator
- **MPN** — Hersteller-Teilenummer

### Internationale Lieferung / Zoll

Erforderlich für internationale Sendungen (Abschnitt **Internationale Lieferung / Zoll** erweitern):

- **HS-Code** — Harmonisierte System-Klassifizierungscode
- **Herkunftsland** — In welchem Land das Produkt hergestellt wird
- **Zoll-Einzelwert** — Angegebener Wert pro Einheit für Zollzwecke
- **Exportlizenznummer** — Nur für kontrollierte oder eingeschränkte Artikel erforderlich
- **Ablaufdatum der Exportlizenz** — Ablaufdatum der Exportlizenz

## SEO

Optimieren Sie die Sichtbarkeit Ihres Produkts in Suchmaschinen.

![SEO-Reiter](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta-Titel** — Der Titel, der in Suchmaschinenresultaten angezeigt wird. Klicken Sie auf das Globus-Symbol, um zu übersetzen.
- **Meta-Beschreibung** — Eine kurze Beschreibung für Suchmaschinenresultate (max. 160 Zeichen). Klicken Sie auf das Globus-Symbol, um zu übersetzen.
- **SEO automatisch generieren** — Klicken Sie, um SEO-Inhalt automatisch zu generieren, wenn das Produkt gespeichert wird.

Eine Live-**Suchergebnisvorschau** zeigt an, wie Ihr Produkt in Google-Suchmaschinenresultaten aussehen wird.

## Produktseiteneinstellungen

Auf dem **Erweitert**-Tab ermöglicht die **Produktseiteneinstellungen** -Karte, die Darstellung der Produktseite im Store zu steuern:

- **Seitenvorlage** — Überschreiben Sie das Standardlayout der Site für dieses Produkt: Classic, Vollbreite, Galeriefokus oder Digital. Lassen Sie es auf **Standard-Site verwenden**, um das Layout zu erben, das Ihre Designeinstellungen angeben. Die meisten Produkte sollten auf dem Standardverfahren bleiben, damit Vorlagenänderungen dort automatisch angewandt werden.
- **Verwandte Produkte anzeigen** — Verwandte Produkte am Ende der Seite anzeigenn.
- **Bewertungen anzeigen** — Kundenbewertungen anzeigenn.
- **Spezifikationen anzeigen** — Spezifikationen-Reiter anzeigenn.

Das Feld **Galerietyp** – das die Anzeige der Produktbilder steuert (Standardgalerie, Carousel, Rasterlayout, Zoomgalerie oder 360°-Ansicht) – wird separat auf dem **Medien**-Tab festgelegt.

## Verkaufskanal

Das Feld **Verkaufskanal** (in der Status-Sektion) steuert, wo das Produkt verkauft werden kann:

- **Alle Kanäle** — Online und im Geschäft (POS) verfügbar.
- **Nur Online** — Nicht über POS-Terminals verfügbar.
- **Nur im Geschäft** — Nicht online gelistet; nur in Ihrem physischen Geschäft verfügbar.

Ein **Barcode** -Feld ist auch für die POS-Barcodescans verfügbar.

## Produkt speichern

Wenn Sie bereit sind, verwenden Sie die Speicherbuttons in der oberen rechten Ecke. Ihr Produkt ist auf dem Store sichtbar, sobald der Status auf **Veröffentlicht** gesetzt wird.

## Tipps

Alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Beginnen Sie mit dem Status **Entwurf**, damit Sie das Produkt vor dem Erscheinen bei den Kunden perfektionieren können.
- Laden Sie mehrere Bilder hoch – Produkte mit mehreren Fotos konvertieren besser.
- Füllen Sie die **SEO**-Felder aus, um die Erreichbarkeit in Suchmaschinen zu verbessern.
- Verwenden Sie **Kategorien**, **Marken** und **Stichwörter**, um den Kunden bei der Navigation durch Ihr Katalog zu helfen.
- Bei variablen Produkten (z. B. verschiedenen Größen oder Farben) wählen Sie den **Variablen Produkttyp** und fügen Sie nach dem Speichern Varianten hinzu.
- Verwenden Sie **Eigenschaften** und **Spezifikationen**, um strukturierte Produktinformationen hinzuzufügen, die auf separaten Tabs auf der Produktseite angezeigt werden.
- Falls **Braucht Versand** nicht aktiviert bleibt, prüfen Sie **Produkttyp** – Spwig schaltet den Versand automatisch ab für digitale, Buchungs- und Gutscheingegenstände, da diese nicht physisch versendet werden.
- Legen Sie ein **Bevorzugtes Versandpaket** fest für Produkte, die immer in derselben Box versendet werden – es spart Ihnen die Mühe, das Gewicht und die Maße dieses Produkts mit dem zu synchronisieren, das Sie tatsächlich verwenden.