---
title: Aus WooCommerce migrieren
---

Wenn Ihr Geschäft derzeit mit WooCommerce läuft, kann der Spwig-Migrationsassistent Ihre Produkte, Kunden, Bestellungen und Inhalte direkt über die REST-API von WooCommerce importieren. Dieser Leitfaden behandelt das Abrufen von API-Anmeldeinformationen, das Durchführen des Imports und zwei WooCommerce-spezifische Funktionen, die Sie zuerst kennen sollten: das optionale Migration Bridge-Plugin für Affiliate-Daten und die eingebaute Unterstützung für mehrere beliebte WooCommerce-Erweiterungen.

## Vor dem Beginn

WooCommerce hat die breiteste Unterstützung aller Quellplattformen im Migrationsassistenten. Der folgende Import erfolgt sauber: Kategorien (mit Hierarchie), Produkte, Bilder und Varianten, Kunden und Adressen, Bestellungen, Bewertungen, Gutscheine und Blogbeiträge mit ihren Kategorien, Tags und Bildern.

Affiliate-Profile, Kommissionsdaten und Auszahlungshistorien können ebenfalls importiert werden, jedoch nur, wenn Sie das Spwig Migration Bridge-Plugin zuerst installieren — siehe unten. Ohne dieses Plugin wird diese Daten einfach übersprungen.

Achten Sie auch darauf:

- Produkte aus bestimmten WooCommerce-Erweiterungen (Abonnements, Bündel, Buchungen, Geschenkkarten) landen in der entsprechenden Spwig-Funktion, aber nicht jedes Detail wird übernommen — siehe **WooCommerce-Erweiterungsunterstützung** unten.
- Benutzerdefinierte Felder auf Ihren Produkten, Kunden und Bestellungen werden automatisch erkannt und müssen in einem späteren Schritt abgebildet werden. Siehe [Migration Field Mapping](migration-field-mapping).
- Die Optionen **Import tax settings** und **Import shipping zones and methods** des Assistenten werden nicht auf die importierten Daten angewendet. Richten Sie Steuersätze und Versandoptionen in Spwig selbst ein — siehe [Nach Ihrer Migration](after-migration-review).
- Die Option **Price adjustment** auf demselben Schritt *wird* für WooCommerce-Imports angewendet und ändert den Grundpreis jedes Produkts, wenn es erstellt wird. Lassen Sie sie auf **None** gesetzt, es sei denn, Sie möchten absichtlich jeden Preis anpassen.

Halten Sie Ihre WordPress-Admin-Anmeldung bereit und wissen Sie ungefähr, wie viele Produkte, Kunden und Bestellungen Sie importieren, damit Sie die Zahlen, die der Assistent Ihnen zeigt, überprüfen können.

## REST API-Anmeldeinformationen erhalten

Spwig verbindet sich mit WooCommerce mithilfe eines REST-API-Schlüssels, der aus Ihrem WordPress-Admin erstellt wird. Dieser Schlüssel benötigt nur **Read**-Zugriff — Spwig liest nur aus Ihrem Geschäft während einer Migration, es schreibt nichts zurück.

1. In WordPress: Gehen Sie zu **WooCommerce > Einstellungen > Erweitert > REST API**
2. Klicken Sie auf **Schlüssel hinzufügen**
3. Geben Sie eine Beschreibung an (z. B. `Spwig Migration`) und setzen Sie **Berechtigungen** auf **Lesen**
4. Klicken Sie auf **API-Schlüssel generieren**
5. Kopieren Sie den **Consumer Key** (`ck_...`) und den **Consumer Secret** (`cs_...`) an einen sicheren Ort

> **Wichtig:** WooCommerce zeigt den Consumer Secret nur einmal an, zum Zeitpunkt seiner Erstellung. Wenn Sie sich von der Seite entfernen, bevor Sie ihn kopiert haben, müssen Sie einen neuen Schlüssel generieren.

## Ihr Geschäft verbinden

Gehen Sie in der Spwig-Verwaltung zu **Datenimport & -export > Neue Migration starten** und wählen Sie **WooCommerce** auf Schritt 1. Auf Schritt 2 geben Sie ein:

- **Store URL** — die vollständige Webadresse Ihres Geschäfts, z. B. `https://mystore.com`
- **Consumer Key** und **Consumer Secret** — die Werte, die Sie gerade kopiert haben

Lassen Sie **Verbindung testen, bevor Sie fortfahren** aktiv (standardmäßig aktiviert), damit Spwig bestätigt, dass es Ihr Geschäft erreichen und sich authentifizieren kann, bevor Sie fortfahren — dies erkennt Tippfehler und Berechtigungsprobleme sofort, anstatt sie erst während des Imports zu entdecken. Klicken Sie auf **Weiter**, sobald es erfolgreich ist.

## Daten überprüfen und auswählen

Schritt 3 zieht aktuelle Zahlen von Ihrem Geschäft heran — Kategorien, Produkte, Kunden, Bestellungen, Bewertungen und Gutscheine — plus eine Stichprobe der ersten fünf Produkte, damit Sie sicherstellen können, dass es die richtige Website liest. Das Häkchen für jeden Datentyp wird automatisch aktiviert, wenn die Anzahl größer als null ist, und deaktiviert, wenn die Anzahl null ist.

**Import-Optionen:**

- **Vorhandene Elemente überspringen** (aktiviert) — vergleicht eingehende Datensätze mit dem, was bereits in Spwig vorhanden ist (SKU für Produkte, E-Mail-Adresse für Kunden) und überspringt Duplikate.

Lassen Sie es aktiviert, es sei denn, Sie starten von einem leeren Store.
- **Produktbilder importieren** (aktiviert) — langsamer, aber lohnenswert.
- **Ursprüngliche IDs so weit wie möglich beibehalten** (deaktiviert) — das Assistenten-Tool selbst bezeichnet dies als "nicht empfohlen". Deaktivieren Sie es, es sei denn, Sie haben einen spezifischen technischen Grund, WooCommerce's numerischen IDs beizubehalten.
- **Batch-Größe** — 10, 25 (Standard), 50 oder 100 Datensätze auf einmal.

Kleinere Batches eignen sich für unzuverlässige Verbindungen; größere Batches sind bei stabiler Verbindung schneller.

## Der Spwig Migration Bridge Plugin

WooCommerce hat keine eingebaute Konzeption für ein Affiliate-Programm, also wenn Sie eines über eine WooCommerce Affiliate-Erweiterung betreiben, dann liegt diese Daten in Tabellen, die die Standard REST API nicht sieht. Der **Spwig Migration Bridge** ist ein kleines Begleit-Plugin, das Sie auf Ihrem WordPress-Server installieren, um dies sichtbar zu machen.

Das Bridge-Plugin ermöglicht:

- **Affiliate-Profile** — Details zu Ihren Affiliates und ihre Referral-Codes
- **Kommissionsdaten** — Kommissionshistorie, die jedem Affiliate zugeordnet ist
- **Auszahlungshistorie** — vergangene Auszahlungen an Affiliates

Es ist vollständig optional — überspringen Sie es, wenn Sie kein Affiliate-Programm betreiben oder diese Historie in Spwig nicht benötigen.

> **Hinweis:** Affiliate-Daten können nur importiert werden, wenn Bestellungen und Kunden auch im gleichen Migrationsschritt importiert werden, da Kommissionen und Auszahlungen an bestimmte Bestellungen und Kunden gebunden sind.

Um es zu installieren:

1. Auf Schritt 3, wenn das Plugin noch nicht auf Ihrem Server erkannt wird, sehen Sie einen **Download Bridge Plugin**-Button mit Installationsanweisungen
2. Laden Sie das Plugin ZIP herunter
3. In WordPress, gehen Sie zu **Plugins > Neu hinzufügen > Plugin hochladen**, wählen Sie das ZIP, klicken Sie auf **Jetzt installieren**, dann auf **Aktivieren**
4. Gehen Sie zurück zum Spwig-Assistenten und aktualisieren Sie die Seite — ein **Affiliates**-Kontrollkästchen und ein **Affiliate Program Data**-Block erscheinen, die die gefundenen Zahlen anzeigt

Sie können das Bridge-Plugin nach Abschluss der Migration deaktivieren und aus WordPress entfernen.

## WooCommerce-Erweiterungsunterstützung

Wenn Ihr Store bestimmte beliebte Erweiterungen verwendet, werden die Produkte, die sie erstellen, während des Imports erkannt und in das entsprechende Spwig-Feature abgebildet, anstatt als einfache Produkte importiert zu werden:

| WooCommerce-Erweiterung | Wird in | 
|---|---|
| Abonnements | Spwig-Abonnements |
| Produkt-Ergänzungen | Spwig-Produkt-Ergänzungen |
| Produkt-Pakete | Spwig-Produkt-Pakete |
| Geschenkkarten (WooCommerce, YITH und PW-Varianten) | Spwig-Geschenkkarten |
| Komposite-Produkte | Spwig-Komposite-Produkte |
| Buchungen und Unterkunftsbuchungen | Spwig-Buchungen |

> **Hinweis:** Der Import von Erweiterungsdaten blockiert nie den Grundprodukt-Import. Wenn die spezifischen Daten einer Erweiterung nicht gelesen werden können, wird das Produkt dennoch importiert — nur als reguläres Produkt, ohne seine Abonnement-, Paket-, Buchungs- oder Geschenkkarten-Konfiguration.

Überprüfen Sie Ihre Abonnement-, Paket-, Buchungs- und Geschenkkartenprodukte nach dem Import, um sicherzustellen, dass ihre spezifischen Einstellungen der Erweiterung korrekt übertragen wurden, anstatt einfach davon auszugehen, dass ein erfolgreicher Import alle Details übernommen hat.

## Benutzerdefinierte Felder

Wenn Sie benutzerdefinierte Metadatenfelder zu Ihren WooCommerce-Produkten, Kunden oder Bestellungen hinzugefügt haben, erfasst Spwig etwa zehn Datensätze pro Typ, um zu erkennen, welche Felder vorhanden sind. Sie werden jedes Feld auf Schritt 4 einem benutzerdefinierten Feldslot in Spwig oder einem allgemeinen Metadatenfeld zuordnen. Siehe [Migration Field Mapping](migration-field-mapping) für den vollständigen Schritt-für-Schritt-Leitfaden, einschließlich der Erklärung, wie Zuordnungen für zukünftige Migrationen gespeichert werden.

## Import ausführen

Sobald Sie Schritt 3 überprüft und Ihre Zuordnungen in Schritt 4 bestätigt haben, starten Sie den Import. Er läuft im Hintergrund — Sie können das Browserfenster schließen, und er läuft weiter. Schritt 5 zeigt den Live-Fortschritt mit einer Zeile pro Datentyp (Kategorien, Produkte, Kunden, Bestellungen, Bewertungen, Gutscheine, Blogbeiträge und Affiliates/Kommissionen/Auszahlungen, wenn das Bridge-Plugin verwendet wurde) plus eine erweiterbare Aktivitätsprotokoll.

Schritt 6 zeigt Ihre Ergebnisse: was importiert, übersprungen oder fehlgeschlagen ist, plus ein **Link-Umleitungstool**, wenn interne Links zu Ihrem alten WooCommerce-Domain in importiertem Inhalt gefunden wurden.

Überprüfen Sie die Zusammenfassung sorgfältig, dann arbeiten Sie Schritt für Schritt durch die Checkliste in [Nach Ihrer Migration](after-migration-review) – sie behandelt die Überprüfung Ihrer Daten, die Einrichtung von Steuersätzen und Versand (die der Assistent nicht für Sie konfiguriert), sowie das Neuschreiben interner Links.

## Deaktivieren Sie Ihren API-Schlüssel

Sobald Sie bestätigt haben, dass die Migration erfolgreich abgeschlossen wurde, kehren Sie zu **WooCommerce > Einstellungen > Erweitert > REST API** in WordPress zurück und deaktivieren oder löschen Sie den Schlüssel, den Sie für Spwig erstellt haben. Es gibt keinen Grund, einen aktiven API-Schlüssel auf Ihrem alten Store zu lassen, sobald Sie damit fertig sind.

## Tipps

- **Erstellen Sie den API-Schlüssel direkt vor dem benötigen** – da der Consumer Secret nur einmal angezeigt wird, erstellen Sie ihn unmittelbar vor dem Start von Schritt 2, anstatt ihn im Voraus zu erstellen.
- **Nur Lesezugriff ist wirklich ausreichend** – gewähren Sie niemals Schreib- oder Lesen/Schreiben-Berechtigungen; Spwig liest nur von Ihrem WooCommerce-Store.
- **Installieren Sie das Bridge-Plugin, bevor Sie mit dem Import beginnen** – Sie müssen es hinzufügen und den Assistenten aktualisieren, bevor Sie den Import starten, also überprüfen Sie es bereits im Voraus, anstatt es während des Prozesses zu tun.
- **Überprüfen Sie Produkte, die von Erweiterungen abhängen** – Abonnements, Bündel, Buchungen und Geschenkkarten sind die Produkte, die am wahrscheinlichsten nach dem Import manuell überprüft werden müssen.
- **Ein teilweiser Import wird nicht automatisch bereinigt** – sehen Sie sich [Migration Troubleshooting](migration-troubleshooting) an, bevor Sie einen fehlgeschlagenen Import erneut versuchen.
- **Deaktivieren Sie den API-Schlüssel, sobald Sie fertig sind** – lassen Sie keine alten Integrationen auf einem Store aktiv, den Sie migriert haben.