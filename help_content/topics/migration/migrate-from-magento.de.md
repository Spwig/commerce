---
title: Aus Magento migrieren
---

Spwig kann Katalog, Kunden, Bestellungen, Gutscheine und CMS-Seiten direkt aus einer laufenden Magento 2- oder Adobe Commerce-Shop-Instanz über die REST-API von Magento importieren. Dieser Leitfaden beschreibt, wie Sie die Integrationserlaubnis generieren, die Magento benötigt, den Migrations-Assistenten ausführen und die eine bedeutende Lücke, mit der Händler, die von Magento kommen, rechnen müssen: Produktbewertungen.

Nur **Magento 2 und Adobe Commerce** werden unterstützt. Magento 1 ist seit Jahren aus dem Support ausgeschieden und stellt nicht die REST-API bereit, auf der diese Migration basiert – wenn Sie noch immer auf Magento 1 sind, verwenden Sie stattdessen [Import aus CSV-Dateien](csv-import).

## Vor der Migration

Überprüfen Sie [Übersicht zur Datenmigration](migration-overview) für allgemeine Planungshinweise. Für Magento spezifisch:

- **Kategorien** – werden mit ihrer Hierarchie importiert.
- **Produkte** – werden importiert, einschließlich Bilder.
- **Kunden und Adressen** – werden importiert.
- **Bestellungen** – werden importiert.
- **Gutscheine** – werden als Spwig-Gutscheine importiert, basierend auf den Verkaufsregeln von Magento.
- **CMS-Seiten** – werden als Spwig-Seiten importiert.
- **Bewertungen** – werden **normalerweise nicht** importiert. Sehen Sie sich den nächsten Abschnitt an, bevor Sie sich darauf verlassen.
- Varianten werden für konfigurierbare Produkte unterstützt.

> **Hinweis:** Migrationen von Magento übertragen keine Affiliate-Programme, Provisionen oder Auszahlungen – die Affiliate-Brücke-Integration von Spwig ist nur für WooCommerce-Shops verfügbar.

### Die Bewertungseinschränkung

Magento Community Edition stellt keinen REST-Endpunkt für Produktbewertungen bereit – der Pfad `/reviews` existiert einfach nicht in einer Standard-Community-Installation. Spwig prüft diesen vor dem Import und, wenn er nicht vorhanden ist, protokolliert eine Nachricht und setzt die restliche Migration fort, anstatt den gesamten Vorgang zu beenden. Ihre Kategorien, Produkte, Kunden, Bestellungen, Gutscheine und Seiten werden dennoch übertragen; nur Bewertungen werden übersprungen.

Bewertungen **werden** importiert, wenn Ihr Shop **Adobe Commerce** verwendet (was diesen Endpunkt bereitstellt) oder wenn Ihre Magento-Installation ein benutzerdefiniertes Modul hat, das einen kompatiblen Bewertungs-Pfad hinzufügt.

Wenn Sie Magento Community verwenden und Ihre Bewertungen in Spwig benötigen, exportieren Sie sie separat (die meisten Bewertungserweiterungen bieten eine CSV-Exportfunktion) und laden Sie sie anschließend über die Bewertungsdatei in [Import aus CSV-Dateien](csv-import) hoch, wobei sie anhand von `product_id` mit Ihren Produkten verknüpft werden.

## Schritt 1: Magento auswählen

Auf dem Migration-Dashboard unter **Datenimport & -export** klicken Sie auf **Neue Migration starten** und wählen Sie **Magento** als Ihre Plattform aus.

## Schritt 2: Zu Ihrem Shop verbinden

Sie benötigen die URL Ihres Magento-Shops und einen Zugriffstoken für die Integration. Im Magento-Admin wird keine einfache API-Schlüssel wie bei einigen Plattformen bereitgestellt – Sie erstellen eine **Integration**, die ein begrenztes Zugriffsrecht darstellt, das Magento wie eine verbundene Anwendung behandelt.

### Erstellen eines Zugriffstokens für die Integration

1. Gehen Sie im Magento-Admin zu **System > Integration**.
2. Klicken Sie auf **Neue Integration hinzufügen**.
3. Legen Sie den Namen auf `Spwig Migration` fest, damit Sie ihn später leicht erkennen können.
4. Öffnen Sie den **API**-Reiter und setzen Sie **Ressourcenzugriff** auf **Alle**.
5. Klicken Sie auf **Speichern**, dann auf **Aktivieren**.
6. Bestätigen Sie, indem Sie auf **Erlauben** im Popup klicken, das die gewährten Berechtigungen auflistet.
7. Kopieren Sie den Zugriffstoken, der nach der Aktivierung angezeigt wird – Magento zeigt ihn nur einmal an.

> **Hinweis:** Der Ressourcenzugriff wird auf **Alle** gesetzt, da der Ressourcenbaum von Magento sehr feingranular ist – Hunderte individueller Berechtigungen für Katalog, Verkauf, Kunden und CMS – mit keiner einzigen „Alles lesen“-Schalter, außer wenn Sie alle auswählen. Die Migration liest nur von Ihrem Shop; sie schreibt nie zurück, und Sie können die Integration nach Bestätigung Ihrer Migration widerrufen (am Ende dieses Leitfadens behandelt).

Zurück im Spwig-Assistenten geben Sie Ihre **Shop-URL** und den **Zugriffstoken** ein, den Sie kopiert haben. Lassen Sie **Verbindung testen, bevor Sie fortfahren** aktiviert (standardmäßig aktiviert), damit Spwig überprüft, ob sie Ihre Shop erreichen und sich anmelden kann, bevor Sie fortfahren. Wenn der Test fehlschlägt, überprüfen Sie die URL und stellen Sie sicher, dass die Integration in Magento immer noch aktiv ist. Klicken Sie auf **Weiter**.

comment

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: magento-connection-step.webp
  description: Step 2 of the wizard with Magento selected, showing the Store URL and Access Token fields and the Test connection checkbox
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

heading

## Schritt 3: Überprüfen, was importiert wird

paragraph

Spwig fragt Ihre Magento-Shop ab und zeigt Live-Zähler für jeden Datentyp an, den er gefunden hat: Kategorien, Produkte, Kunden, Bestellungen, Gutscheine (aus Verkaufsregeln) und CMS-Seiten. Jeder Typ hat ein Häkchenfeld, das automatisch aktiviert wird, wenn Spwig Elemente zum Import gefunden hat, und deaktiviert wird, wenn die Anzahl null ist.

paragraph

Sie werden auch eine Vorschau der ersten fünf Produkte sehen, damit Sie sicherstellen können, dass Titel, Preise und Bilder korrekt aussehen, bevor Sie den vollständigen Import durchführen.

paragraph

Unterhalb der Zähler ermöglichen **Import-Optionen**, wie sich der Import verhält:

list

paragraph

Wenn Sie wissen möchten, wie bestimmte Felder abgebildet werden sollen — benutzerdefinierte Attribute, Kategorien, Steuern oder Versandbehandlung — geschieht das im Schritt 4, wie in [Migration Field Mapping](migration-field-mapping) beschrieben. Klicken Sie auf **Weiter**, um zur Abbildung zu gelangen, und dann auf **Migration starten**, sobald Sie dies überprüft haben.

heading

## Import ausführen

paragraph

Der Import wird im Hintergrund ausgeführt — Sie können das Fenster schließen, und er wird weiterlaufen. Die Fortschrittsseite zeigt den Live-Status für jeden Datentyp (Kategorien, Produkte, Kunden, Bestellungen, Bewertungen, Gutscheine) mit einem Log, das Sie erweitern können, um Details anzuzeigen.

paragraph

Sobald er abgeschlossen ist, landen Sie auf der Ergebnisseübersicht. Gehen Sie durch [Nach Ihrer Migration](after-migration-review), um zu überprüfen, was übertragen wurde, eventuelle Links für Inhalte, die Ihre alten Magento-URLs referenzierten, zu bearbeiten, und kümmern Sie sich um die Steuer- und Versandkonfiguration, die der Assistent sammelt, aber nicht automatisch anwendet.

comment

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step5/
  filename: magento-import-progress.webp
  description: Import progress page showing per-step status rows during a Magento migration
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

heading

## Rückrollungsfrist

paragraph

Magento ist die einzige Plattform, bei der eine Rückrollung eine Frist hat. Sobald Ihre Migration abgeschlossen ist, erscheint die Schaltfläche **Rückrollen** auf der Zusammenfassungsseite des Jobs — aber bei Magento speziell kann diese Schaltfläche nach einer gewissen Zeit nach Abschluss nicht mehr angeboten werden. Andere Migrationstypen (WooCommerce, Shopify, CSV) haben diese Frist nicht, aber Magento hat sie, also verzögern Sie die Überprüfung nicht.

blockquote

**Warnung:** Die Rückrollung löscht mehr als nur das, was die Migration erstellt hat — einschließlich Bestellungen, die von migrierten Kunden *nach* der Migration platziert wurden, und Bestellpositionen, die migrierte Produkte referenzieren, sogar bei Bestellungen von Kunden, die Sie nicht migriert haben. Es ist nur sicher, sie unmittelbar nach einer Migration zu verwenden, bevor auf dem Shop echte Handelsvorgänge stattfinden. Siehe [Migration Troubleshooting](migration-troubleshooting) für den vollständigen Überblick darüber, was die Rückrollung wirklich und nicht rückgängig macht.

paragraph

Überprüfen Sie Ihre importierten Daten so schnell wie möglich, solange die Rückrollung noch möglich ist, falls Sie sie benötigen.

heading

## Integration widerrufen

paragraph

Sobald Sie Ihre Daten in Spwig überprüft haben — Produkte, Preise, Bilder, Kunden, Bestellungen, Gutscheine und Seiten sehen alles richtig aus — kehren Sie zu **System > Integrationen** in Magento zurück, suchen Sie nach `Spwig Migration` und deaktivieren Sie oder löschen Sie sie.

Der Token ist nicht nochmal benötigt, es sei denn, Sie planen, die Migration erneut durchzuführen. Das Entfernen des Tokens schließt eine bestehende Lesezugriffs-Zugangsidentität, die Sie nicht mehr benötigen, ab.

## Tips

- **Bewertungen sind die größte Überraschung für Magento-Händler** — planen Sie bei der Community Edition einen separaten Export/Import, wenn Bewertungen für Ihr Geschäft wichtig sind.
- **Kopieren Sie den Zugriffstoken sofort** — Magento zeigt ihn nur einmal an, wenn Sie die Integration aktivieren; sollten Sie ihn verlieren, müssen Sie die Integration deaktivieren und neu erstellen.
- **Verzögern Sie die Verifizierung nicht** — die Verfügbarkeit des Rollback-Buttons ist bei Magento zeitlich begrenzt, im Gegensatz zu anderen Plattformen.
- **Verwenden Sie die Vorschau im Schritt 3**, um offensichtliche Zuordnungsprobleme (falsche Preise, fehlende Bilder) vor dem Durchführung des vollständigen Imports zu erkennen.
- **Gutscheine stammen aus Verkaufsregeln** — wenn ein Magento-Gutschein auf komplexe Bedingungen angewiesen ist, prüfen Sie ihn anschließend in Spwig, da nicht jeder Regeln-Typ eine direkte Äquivalenz hat.
- **Konfigurieren Sie Steuersätze und Versandzonen in Spwig nach dem Import** — die Steuer- und Versandoptionen des Assistenten werden gespeichert, werden aber nicht automatisch auf Ihr Geschäft angewendet.