---
title: Aus Shopify migrieren
---

Wenn Ihr Geschäft derzeit auf Shopify läuft, kann der Migrations-Assistent von Spwig Ihre Produkte, Kunden, Bestellungen und Inhalte importieren, indem er sich mit einer kleinen benutzerdefinierten App verbindet, die Sie im Shopify Partners-Dashboard erstellen. Die Plattform von Shopify ist im Vergleich zu den meisten anderen etwas eingeschränkter, daher konzentriert sich der größte Teil dieses Leitfadens darauf, diese App korrekt zu erstellen – die Verbindung selbst ist ein Schritt, der nur fünf Minuten dauert, sobald die App existiert.

## Vor dem Beginn

Zwei spezifische Shopify-Grenzen sind wichtig genug, um sie hier hervorzuheben, nicht nur weiter unten in einer Tabelle:

> **Wichtig:** Shopify hat keine Bewertungs-API, daher **werden Kundenbewertungen überhaupt nicht migriert**, unabhängig davon, welche App-Berechtigungen Sie erteilen. Wenn Sie Ihre Bewertungen benötigen, exportieren Sie sie separat aus der Bewertungs-App, die Sie verwenden (Judge.me, Yotpo, Loox usw.), und importieren Sie sie selbst in Spwig.

> **Wichtig:** Standardmäßig kann Spwig nur **Bestellungen der letzten 60 Tage** lesen. Um Ihre gesamte Bestellhistorie zu übernehmen, müssen Sie den Bereich `read_all_orders` hinzufügen, wenn Sie Ihre App erstellen – siehe die Liste der Bereiche unten. Dies ist leicht zu übersehen, da die App dennoch erfolgreich verbunden und importiert werden kann, ohne diesen Bereich; sie beschränkt nur stillschweigend, wie weit zurück Ihre Bestellhistorie geht.

Alles andere wird gut übertragen: Kategorien (als Sammlungen – siehe unten), Produkte, Bilder, Varianten, Kunden und Adressen, Rabatte und Bloginhalte. Benutzerdefinierte Felder sind der andere bemerkenswerte Lücke – siehe **Shopify-Metadatenfelder** am Ende dieses Leitfadens.

Achten Sie auch darauf:

- Die Optionen **Steuer-Importeinstellungen** und **Versandzonen und -methoden importieren** des Assistenten werden nicht auf die importierten Daten angewendet. Richten Sie Steuersätze und Versandoptionen in Spwig selbst ein – siehe [Nach Ihrer Migration](after-migration-review).
- Die Option **Preisanpassung** auf demselben Schritt *wird* für Shopify-Importe angewendet und ändert den Grundpreis jedes Produkts, wenn es erstellt wird. Setzen Sie sie auf **Keine**, es sei denn, Sie möchten absichtlich jeden Preis anpassen.
- Sie benötigen Zugriff auf ein Shopify Partners-Konto, um die App zu erstellen. Wenn Sie noch keines haben, können Sie eines kostenlos unter partners.shopify.com erstellen.

## Die Shopify-App erstellen

Spwig verbindet sich mit Shopify über eine benutzerdefinierte App, die Sie selbst auf Ihrem Geschäft erstellen und installieren. Dies spiegelt den in-App-**Shopify API Setup Guide**-Modal (über **Setup Guide öffnen** auf Schritt 2 des Assistenten) wider, daher entsprechen die Schritte unten exakt dem, was Sie dort sehen – Sie können entweder diesen oder den anderen folgen.

### Schritt 1: App erstellen

1. Gehen Sie zu Ihrem [Shopify Partners Entwickler-Dashboard](https://dev.shopify.com/dashboard) und öffnen Sie **Apps**
2. Klicken Sie auf **App erstellen**
3. Wählen Sie **Von Dev Dashboard starten**
4. Geben Sie den App-Namen ein: `Spwig Migration`
5. Klicken Sie auf **Erstellen**

![Die Spwig-Migration-App im Shopify-Entwickler-Dashboard erstellen](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Schritt 2: App-URL und Bereiche festlegen

Auf der Konfigurationsseite der neuen App unter **Versionen** legen Sie fest:

- **App-URL**: `https://shopify.dev/apps/default-app-home`
- **Bereiche**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![App-URL und erforderliche Bereiche festlegen](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Bereich | Gibt Spwig Zugriff auf |
|---|---|
| `read_products` | Produkte, Varianten, Bilder, Sammlungen |
| `read_customers` | Kundennamen, E-Mails, Adressen |
| `read_orders` | Bestellungen der letzten 60 Tage |
| `read_content` | Blogbeiträge und Seiten |
| `read_discounts` | Rabattcodes und Regeln |
| `read_files` | Hochgeladene Mediendateien |

> **Hinweis:** Möchten Sie Ihre gesamte Bestellhistorie anstelle nur der letzten 60 Tage? Fügen Sie `read_all_orders` zur Bereichsliste oben hinzu.

### Schritt 3: Client-ID und Geheimnis kopieren

Gehen Sie zu **Einstellungen > Anmeldeinformationen** und kopieren Sie die dort angezeigte **Client-ID** und **Geheimnis** – Sie werden diese gleich in den Spwig-Assistenten einfügen.

![Client-ID und Geheimnis von der App-Einstellungsseite kopieren](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Schritt 4: Ein benutzerdefinierten Verteilungslink generieren

1.

Gehe zu **Distribution** und wähle **Custom distribution** aus
2.

Gib deinen Store-Domain ein (z. B. `yourstore.myshopify.com`)
3.

Klicke auf **Generate link**, dann **Copy**, um den Installationslink zu kopieren

![Kopieren des generierten custom-distribution-Installationslinks](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Schritt 5: Die App auf deinem Store installieren

Öffne den gerade kopierten Installationslink in deinem Browser (stelle sicher, dass du bei deinem Shopify-Store-Admin angemeldet bist), überprüfe die von der App geforderten Berechtigungen und klicke auf **Install**.

![App auf dem Shopify-Store installieren](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Wichtig:** Dieser letzte Schritt ist leicht zu übersehen. Das Generieren des Installationslinks installiert die App nicht — du musst den Link tatsächlich öffnen und auf Install klicken, sonst kann Spwig keine Verbindung herstellen. Falls der Verbindungstest im nächsten Abschnitt fehlschlägt, ist dies die erste Sache, die du überprüfen solltest.

## Deine Anmeldeinformationen in Spwig kopieren

In der Spwig-Verwaltung gehst du zu **Data Import & Export > Start New Migration**, wähle auf Schritt 1 **Shopify** aus, und gib auf Schritt 2 ein:

- **Store Domain** — `yourstore.myshopify.com`
- **Client ID** — aus Einstellungen > Anmeldeinformationen
- **Client Secret** — aus Einstellungen > Anmeldeinformationen

Wenn du lieber die Schritt-für-Schritt-Anleitung im Produkt folgen möchtest, als diese Anleitung, klicke auf **Open Setup Guide** in diesem Schritt — sie behandelt die gleichen fünf Schritte wie oben mit den gleichen Screenshots und dauert insgesamt etwa 10 Minuten.

Lass **Test connection before proceeding** aktiviert. Wenn `read_products`, `read_customers` oder `read_orders` nicht in den Berechtigungen deiner App enthalten sind, warnt Spwig dich vor der Fortsetzung — geh zurück zur Versionsseite der App im Shopify-Dashboard, füge die fehlende Berechtigung hinzu, speichere eine neue Version und versuche es erneut.

## Daten überprüfen und auswählen

Schritt 3 zieht aktuelle Zahlen von deinem Store und zeigt eine Vorschau der ersten fünf Produkte an. Ein paar Dinge sehen anders aus als bei anderen Plattformen:

- **Sammlungen, nicht Kategorien** — Shopify organisiert Produkte in Sammlungen anstelle von Kategorien, und Sammlungen unterstützen keine Verschachtelung, wodurch die Hierarchie flach importiert wird. Wenn dein Shopify-Store Sammlungen zur Darstellung eines Kategorienbaums verwendet hat, plane, diese Struktur nach dem Import im Kategorien-Manager von Spwig neu aufzubauen.
- **Rabatte, nicht Gutscheine** — Die Rabattcodes und Regeln von Shopify werden als Spwig-Rabatte importiert.
- **Keine Bewertungszeile** — da Shopify keine Bewertungs-API hat, erscheint dieser Datentyp auf diesem Schritt überhaupt nicht, im Gegensatz zu WooCommerce oder CSV-Imports.

Die **Import-Optionen** funktionieren auf anderen Plattformen gleich: **Bestehende Elemente überspringen** (aktiviert) vergleicht SKU und E-Mail, um Duplikate zu vermeiden; **Produktbilder importieren** (aktiviert) ist langsamer, aber empfohlen; **Ursprüngliche IDs so weit wie möglich beibehalten** (deaktiviert) sollte deaktiviert bleiben, es sei denn, du hast einen spezifischen Grund, dies zu ändern; **Batch-Größe** ist standardmäßig auf 25 eingestellt.

## Shopify-Metadatenfelder

Wenn du Shopify-Metadatenfelder verwendest, um zusätzliche Daten zu Produkten, Kunden oder Bestellungen zu speichern, beachte, dass Spwig sie nicht erkennt oder liest — anders als bei WooCommerce gibt es keinen Schritt zur Zuordnung von benutzerdefinierten Feldern bei Shopify-Imports. Jegliche Daten, die du in Metadatenfeldern gespeichert hast, müssen nach dem Import manuell in Spwig über [benutzerdefinierte Felder](migration-field-mapping) eingegeben werden, also lohnt es sich, eine Liste deiner Metadatenfelder und deren Werte aus Shopify vor dem Start zu exportieren.

## Import ausführen

Sobald du Schritt 3 überprüft hast, starte den Import. Er läuft im Hintergrund — du kannst das Browserfenster schließen, und er läuft weiter. Schritt 5 zeigt den Live-Fortschritt mit einer Zeile pro Datentyp und einem erweiterbaren Aktivitätsprotokoll.

Schritt 6 zeigt deine Ergebnisse: was importiert, übersprungen oder fehlgeschlagen ist, plus ein **Link-Umwidmungstool**, wenn interne Links zu deinem alten `myshopify.com`-Domain in importiertem Inhalt gefunden wurden.

Überprüfen Sie die Zusammenfassung sorgfältig, und arbeiten Sie anschließend durch die Checkliste in [Nach Ihrer Migration](after-migration-review) — sie umfasst die Überprüfung Ihrer Daten, das Neuaufbauen jeder Sammlungshierarchie, das Einrichten von Steuersätzen und Versandkosten (die der Assistent nicht für Sie konfiguriert), sowie das erneute Eingeben von Daten, die in Metafeldern gespeichert waren.

## Löschen Sie die App von Shopify

Sobald Sie bestätigt haben, dass die Migration erfolgreich abgeschlossen wurde, kehren Sie zu der **Apps**-Seite in Ihrem Shopify-Admin-Bereich oder zum Partner-Dashboard zurück und löschen Sie die Spwig-Migration-App (oder mindestens deinstallieren Sie sie von Ihrem Store). Es gibt keinen Grund, den Lesezugriff auf Ihre Store-Daten aktiv zu lassen, sobald die Migration abgeschlossen ist.

## Tipps

- **Bestellhistorie ist standardmäßig eingeschränkt** — wenn Sie mehr als die letzten 60 Tage Bestellungen benötigen, fügen Sie `read_all_orders` der Scope-Liste vor dem Generieren Ihres Installationslinks hinzu, nicht nachher.
- **Bewertungen benötigen eine separate Exportdatei** — planen Sie dies vor der Migration, da es keine Möglichkeit gibt, Bewertungen über den Assistenten zu übertragen.
- **Das Generieren des Links ist nicht dasselbe wie das Installieren der App** — führen Sie immer Schritt 5 ab und klicken Sie auf Installieren, andernfalls wird der Verbindungstest in Spwig fehlschlagen.
- **Sammlungen werden flach importiert** — wenn Ihre Kategorienstruktur für Navigation oder SEO wichtig war, planen Sie Zeit ein, um die Hierarchie in Spwig nach dem Import neu aufzubauen.
- **Exportieren Sie Ihre Metafelder zuerst** — Spwig kann sie nicht lesen, also sichern Sie diese Daten aus Shopify, bevor Sie mit dem Import beginnen, falls Sie sie später benötigen.
- **Löschen Sie die App, sobald Sie bestätigt haben, dass alles funktioniert** — lassen Sie keine aktive Integration auf Ihrem alten Store bestehen, nachdem Sie bereits weitergezogen sind.