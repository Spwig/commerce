---
title: Übersicht zur Datenmigration
---

Wenn Ihre Produkte, Kunden und Bestellungen derzeit in WooCommerce, Shopify oder Magento – oder einfach in einigen CSV-Dateien – gespeichert sind, bringt das Migrationswerkzeug diese Daten in Ihre neue Spwig-Shop-Instanz, sodass Sie sie nicht manuell erneut eingeben müssen. Es verarbeitet Kategorien, Produkte, Kunden, Bestellungen, Bewertungen und Gutscheine. Bei WooCommerce kann es auch Bloginhalte übertragen und mit einer Brücke-Plug-in-Datei Ihr Affiliate-Programm übernehmen.

Sie finden es in der Admin- Seitenleiste unter **System Dashboard > Datenimport/Export** (sichtbar für Superuser bei selbstgehosteten Installationen; wenn Sie es nicht sehen, fragen Sie die Person, die Ihre Installation verwaltet). Die Seite, die **Datenimport & Export** heißt, listet jede gestartete Migration mit Statistikkarten für Gesamte Migrationen, Abgeschlossene, In Bearbeitung und Fehlgeschlagene auf, plus die Schaltflächen **Neue Migration starten**, **Protokolle ansehen** und **Feldzuordnungen**. Migrationen können nur über den Assistenten erstellt werden.

## Unterstützte Plattformen

Spwig verbindet sich direkt mit drei Plattformen, plus reinen CSV-Dateien:

- **WooCommerce** – der vollständigste Weg; Erweiterungsdaten (Abonnements, Bündel, Geschenkkarten, Buchungen) und Ihr Affiliate-Programm können ebenfalls übertragen werden.
- **Shopify** – verbindet sich über eine benutzerdefinierte App, die Sie in Ihrem Shopify-Entwickler-Dashboard erstellen.
- **Magento 2** – verbindet sich über eine Integrationstoken aus Ihrem Magento-Admin.
- **CSV-Dateien** – fünf separate Dateien (Produkte, Kategorien, Kunden, Bestellungen, Bewertungen), für andere Plattformen oder manuell vorbereitete Daten.

> **Hinweis:** BigCommerce, PrestaShop, Squarespace und Wix werden nicht als direkte Verbindungen unterstützt. Wenn Sie von einem dieser Anbieter migrieren, exportieren Sie Ihr Katalog- und Kundendaten in CSV und verwenden Sie den CSV-Import anstelle dessen – siehe [CSV-Dateien importieren](csv-import).

## Was pro Plattform übertragen wird

Die Abdeckung variiert je nach Plattform – prüfen Sie diese Tabelle vor der Veröffentlichung Ihres eigenen Shops.

| Daten | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Kategorien | Ja, mit Hierarchie | Ja, als Sammlungen (flach) | Ja | Ja |
| Produkte | Ja | Ja | Ja | Ja (erforderliche Datei) |
| Produktbilder | Ja | Ja | Ja | Nein |
| Varianten | Ja | Ja | Ja | Nein |
| Kunden + Adressen | Ja | Ja | Ja | Ja |
| Bestellungen | Ja | Ja, nur die letzten 60 Tage, es sei denn, der `read_all_orders`-Bereich wird hinzugefügt | Ja | Ja |
| Bewertungen | Ja | Nicht unterstützt | Normalerweise nicht verfügbar – Magento Community hat keinen REST-Endpunkt für Bewertungen | Ja |
| Gutscheine / Rabatte | Ja | Ja | Ja | Nein |
| Blog / CMS-Inhalt | Ja (Beiträge, Kategorien, Tags, Bilder) | Ja (Artikel) | Ja (CMS-Seiten) | Nein |
| Affiliate-Partner, Provisionen, Auszahlungen | Ja, erfordert das Spwig-Migration-Brücke-Plug-in | Nein | Nein | Nein |
| Erkennung benutzerdefinierter Felder | Ja | Nein – Shopify-Metadatenfelder werden nicht gelesen | Nein | n/a |

Shopify-Händler sollten planen, alle Metadatenfelder (benutzerdefinierte Produkt-Spezifikationen, zusätzliche Kundendaten) manuell nach dem Import erneut einzugeben, da sie nicht erkannt oder übertragen werden. Für alles andere siehe [Feldzuordnung der Migration](migration-field-mapping), um zu sehen, wie Quellfelder auf Spwig-Felder abgebildet werden.

## Migration planen

- **Migrieren Sie, bevor Sie online gehen**, mit einer Spwig-Installation, die noch keine echten Besucher verarbeitet, bevor Sie den DNS-Server Ihres Domains darauf verweisen – so können Sie Dinge überprüfen und beheben, ohne dass Kunden einen halbfertigen Katalog sehen.
- **Lassen Sie Ihren alten Shop weiterlaufen, nur lesbar**, bis Sie sicher sind, dass die Spwig-Kopie korrekt ist.
- **Planen Sie Zeit für die Steuern- und Versandkonfiguration danach** – die Einstellungen des Assistenten für diese Aspekte sehen so aus, als würden sie Ihre Steuersätze und Zonen importieren, aber sie werden nicht angewendet (siehe [Feldzuordnung der Migration](migration-field-mapping)). Konfigurieren Sie **Einstellungen > Steuern & Währung** und **Einstellungen > Versand** selbst.
- **Prüfen Sie gezielt statt nur oberflächlich** – Erweiterungsdaten werden auf Best-Effort-Basis importiert; ein Produkt, dessen Erweiterungsdaten nicht gelesen werden können, wird dennoch erstellt, nur ohne diese Daten. Siehe [Nach Ihrer Migration](after-migration-review), bevor Sie etwas an Kunden ankündigen.

## Voraussetzungen

- **Admin-Zugriff auf Ihre Quellplattform**, um API-Anmeldeinformationen zu erstellen – einen REST-API-Schlüssel in WooCommerce, eine benutzerdefinierte App in Shopify oder eine Integrationstoken in Magento.

Nicht erforderlich für CSV.
- **Nur-Lese-Bereiche**, wo die Quellplattform sie anbietet – Spwig liest nur von Ihrem alten Geschäft aus, schreibt nie zurück.
- **Zeitbudget** – jeder Durchlauf hat eine harte 4-Stunden-Grenze.

Für ein großes Geschäft planen Sie einen schrittweisen Ansatz (Kategorien und Produkte zuerst, Bestellungen später) anstelle eines einzigen Durchlaufs.

> **Wichtig:** Spwig verschlüsselt nicht die API-Anmeldeinformationen, die Sie im Assistenten eingeben. Nachdem die Migration als abgeschlossen bestätigt wurde, widerrufen Sie oder löschen Sie die Anmeldeinformationen auf der Quellplattform.

## Der Migration-Assistent, Schritt für Schritt

Der Assistent besteht aus sechs Schritten, wobei der Fortschritt zwischen den Schritten gespeichert wird:

1. **Plattform** – Wählen Sie WooCommerce, Shopify, Magento oder CSV-Import aus.
2. **Verbindung** – Geben Sie die Anmeldeinformationen ein, mit einer Option (standardmäßig aktiviert), die Verbindung zunächst zu testen. Die plattformspezifischen Anleitungen beschreiben genau, was generiert werden muss.
3. **Vorschau** – Live-Zahlen aus Ihrem Quellgeschäft, eine Stichprobe der ersten 5 Produkte, sowie Kontrollkästchen für die einzubeziehenden Datentypen und Optionen wie Batch-Größe.
4. **Zuordnung** – Wie Quellfelder auf Spwig-Felder abgebildet werden, alle benutzerdefinierten WooCommerce-Felder und Kategorien ohne offensichtliche Übereinstimmung. Vollständige Details in [Migration Field Mapping](migration-field-mapping).
5. **Import** – Läuft im Hintergrund; Sie können den Tab schließen, und es geht weiter, mit einem Live-Protokoll.
6. **Abgeschlossen** – Eine Ergebniszusammenfassung, ein Link-Überarbeitungstool für Inhalte, die auf Ihr altes Domain-Name verweisen, und Downloads von PDF/CSV-Berichten.

## Nach Ihrer Migration

Ein erfolgreicher Import ist nicht das Ziel – siehe [After Your Migration](after-migration-review) für eine vollständige Checkliste, die Datenüberprüfung, das Beheben interner Links, die immer noch auf Ihr altes Domain-Name verweisen, und die Steuer- und Versandkonfiguration, die der Assistent nicht für Sie verarbeitet.

## Rollback ist kein Sicherheitsnetz

Verstehen Sie dies, bevor Sie beginnen, nicht erst, nachdem etwas schiefgelaufen ist. Ein Rollback existiert, ist aber nicht die Rückgängig-Taste, die man erwarten könnte:

- Es gibt keinen automatischen Rollback, wenn ein Import mittendrin fehlschlägt. Alles, was vor dem Fehler importiert wurde, bleibt in Ihrem Shop, und ein fehlgeschlagener Import kann nicht über den Admin-Bereich zurückgerollt werden — Sie müssen die unvollständigen Daten manuell überprüfen und bereinigen.
- Eine abgeschlossene Migration kann zurückgerollt werden, und der Rollback entfernt nur das, was der Import selbst erstellt hat — nie mehr. Ein migrierter Kunde, der seit dem Import eine echte Bestellung aufgegeben hat, behält sein Konto, seine Adressen, seine Treuepunkte-Historie und sein Guthaben, und diese echte Bestellung bleibt unangetastet; entfernt werden nur die Bestellungen, die der Import selbst erstellt hat. Ein migriertes Produkt, das noch von einer Bestellung, einem Bundle, einer Geschenkkarte oder einem Konfigurator-Slot referenziert wird, bleibt ebenfalls erhalten, und Bestellungen anderer Kunden werden nie verändert.
- Partner, Provisionen und Auszahlungen, die der Import erstellt hat, werden entfernt, ebenso wie jedes Partnerkonto, das der Import erstellt hat — ein Partner, der mit einem bereits vorher existierenden Kunden verknüpft ist, behält sein Kundenkonto, nur der Partnerdatensatz wird gelöscht. Abonnement-Pläne, Preisstufen und Buchungsressourcen, die von Shop-Erweiterungen erstellt wurden, werden weiterhin nicht entfernt — bereinigen Sie diese manuell.
- Bevor Sie bestätigen, zeigt Spwig eine Vorschau, was genau entfernt und was behalten wird, mit Namen, Anzahl und Begründung — berechnet anhand Ihrer Live-Daten. Lesen Sie sie, bevor Sie bestätigen. Der Rollback läuft anschließend im Hintergrund, sodass Sie den Tab schließen können; die Zusammenfassung der Migration zeigt den Bericht, sobald er abgeschlossen ist.
- Ein Rollback ist für die Zeilen, die er tatsächlich entfernt, weiterhin eine dauerhafte, zerstörerische Aktion — verwenden Sie ihn bewusst und bereinigen Sie manuell alles, was Spwig behält und das Sie eigentlich nicht möchten. Da er aber nicht mehr über das hinausgreift, was der Import erstellt hat, ist er nicht länger nur am selben Tag sicher nutzbar, wie es früher der Fall war.
- Die Schaltfläche „Rollback" bleibt auf der Zusammenfassung einer abgeschlossenen Migration verfügbar, solange der Auftragseintrag besteht, und sie wird erneut angeboten, wenn ein Rollback-Versuch selbst mittendrin fehlschlägt, damit Sie ihn wiederholen können. Einträge werden nach keinem festen Zeitplan gelöscht, sodass dies von selbst nicht abläuft.

Wenn Sie auf eine fehlgeschlagene oder blockierte Migration stoßen, behandelt [Migration Troubleshooting](migration-troubleshooting) das Wiederholen, Abbrechen und Lesen der Protokolle.

## Tipps

- **Beginnen Sie mit einem kleinen Testlauf** – Kategorien plus ein paar Produkte bestätigen, dass die Feldzuordnung richtig aussieht, bevor Sie den gesamten Katalog importieren.
- **Lesen Sie zunächst das plattformspezifische Handbuch** – [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify) und [Migrating from Magento](migrate-from-magento) behandeln genau, welche Anmeldeinformationen und Berechtigungen Sie benötigen.
- **Verpassen Sie die Fähigkeitsmatrix oben nicht** – das Wissen über Shopify-Bewertungen oder CSV-Varianten wird Ihnen helfen, Überraschungen zu vermeiden, nachdem Sie den DNS-Wechsel vorgenommen haben.
- **Halten Sie das Admin-Panel Ihrer Quellplattform in einem anderen Tab offen** zum Generieren oder Kopieren von Anmeldeinformationen während des Vorgangs.
- **Behandeln Sie die Kontrollkästchen des Assistenten wörtlich** – wenn eine Einstellung nicht als funktionierend hier beschrieben wird, konfigurieren Sie sie direkt in Spwig, anstatt dem Assistenten zu vertrauen.