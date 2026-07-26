---
title: Nach Ihrer Migration
---

Eine abgeschlossene Migration ist der Beginn Ihrer Prüfung, nicht das Ende. Schritt 6 des Assistenten gibt Ihnen eine Zusammenfassung dessen, was übertragen wurde, ein Werkzeug zur Behebung von Links, die immer noch auf Ihre alte Website zeigen, und einen Bericht, den Sie herunterladen können, um ihn für Ihre Unterlagen zu speichern. Dieses Thema führt Sie durch die Prüfung, die Sie vornehmen sollten, bevor Sie den Umzug als abgeschlossen betrachten, einschließlich der Steuer-, Versand- und Go-Live-Arbeiten, die der Assistent selbst nicht für Sie erledigt.

## Ihre Ergebnisse einsehen

Oben auf der Abschlussseite sehen Sie eine Reihe von Statistik-Karten – eine pro Datentyp (Produkte, Kategorien, Kunden, Bestellungen und so weiter) – gefolgt von einer **Importzusammenfassung**-Tabelle mit den Spalten *Importiert*, *Übersprungen*, *Fehlgeschlagen* und *Gesamt* für jeden Schritt, der ausgeführt wurde.

- **Importiert** – Elemente, die erfolgreich in Spwig erstellt wurden.
- **Übersprungen** – Elemente, die Ihre Quellplattform hatte, aber Spwig nicht erstellt hat. Dies ist fast immer erwartet: mit **Bestehende Elemente überspringen** aktiviert in Schritt 3, wird alles, was mit einem Element übereinstimmt, das bereits in Spwig existierte (nach SKU, E-Mail usw.), nicht dupliziert, sondern einfach ignoriert. Ein hoher Übersprungsanzahl nach einem erneuten Versuch bedeutet in der Regel nur, dass der erste Versuch diese Einträge bereits erstellt hat.
- **Fehlgeschlagen** – Elemente, die Spwig versucht hat, aber nicht erstellen konnte, aufgrund eines Datenproblems, eines fehlenden Abhängigkeiten oder eines Fehlers auf der Quellseite. Ein nicht-null Fehlgeschlagen-Zähler ist wertvoll, um zu untersuchen; siehe [Migration-Problembehebung](migration-troubleshooting), um zu erfahren, wie Sie die Protokolle einsehen und welche Ihre Optionen zur Bereinigung sind.

> **Hinweis:** Wenn ein Schritt Fehler anzeigt, nehmen Sie nicht an, dass der Store etwas rückgängig gemacht hat, um dies zu kompensieren – das tut er nicht. Alles, was vor dem Fehlschlag importiert wurde, befindet sich in Ihrem Store neben allem, was erfolgreich war. Überprüfen Sie es auf die gleiche Weise, wie Sie eine normale teilweise Ergebnis überprüfen würden.

## Link-Umstellung

Produkte, Seiten und Blogbeiträge, die von Ihrer alten Plattform importiert wurden, enthalten oft Links zurück zu ihrem ursprünglichen Domain – ein Bild-URL, ein Link zu einem „verwandten Produkt“, eine interne Querverweisung. Wenn Spwig in dem gerade importierten Inhalt solche Links erkennt, erscheint ein **Link-Umstellung**-Panel auf der Abschlussseite.

Jeder erkannte Link wird nach der Seite oder dem Produkt, von dem er stammt, gruppiert und mit folgendem angezeigt:

- **Originaler URL** – der Link genau so, wie er im importierten Inhalt erschien.
- **Vorgeschlagener URL** – Spwigs beste Vermutung für die entsprechende Seite auf Ihrem neuen Store, wenn eine gefunden wurde.
- **Übereinstimmung** – ein Vertrauenswert in Prozent für diese Vorschlag. Links, die keine vernünftige Übereinstimmung haben, werden als **Keine** angezeigt und haben keinen vorgeschlagenen URL, den Sie genehmigen können.

Für jeden Link können Sie den Vorschlag **Genehmigen** oder ihn **Überspringen**, einen nach dem anderen. **Automatisch genehmigen, wenn Vertrauenswert hoch ist** genehmigt alle Vorschläge mit 85 % oder mehr mit einem Klick – eine Zeitersparnis, aber dennoch wert, danach einige manuelle Kontrollen durchzuführen. Vorschläge unter diesem Schwellenwert sind diejenigen, die Sie manuell öffnen sollten: eine Übereinstimmung von 50–70 % könnte das richtige Produkt unter einem falschen Namen sein, oder es könnte weit davon entfernt sein, und nur ein menschlicher Blick kann das erkennen.

Das Genehmigen oder Überspringen markiert nur den Link – nichts in Ihrem Inhalt ändert sich, bis Sie auf **Genehmigte Links anwenden** klicken, was alle genehmigten Links gleichzeitig neu schreibt. Das bedeutet, dass es sicher ist, die Liste über mehrere Sitzungen hinweg zu bearbeiten, bevor Sie sich verpflichten.

> **Tipp:** Lassen Sie jeden Link, den Sie nicht sicher sind, als **Überspringen** stehen, anstatt einen Vorschlag zu genehmigen. Sie können immer einen alten-Domain-Link manuell später beheben; eine falsche Umstellung, die auf Dutzende von Produkten angewendet wird, ist mehr Arbeit, um sie rückgängig zu machen.

## Ihre Daten überprüfen

Behandeln Sie die Statistik-Karten als Ausgangspunkt, nicht als Beweis dafür, dass alles korrekt ist. Verbringen Sie ein paar Minuten, um einige Stichproben zu überprüfen:

- **Produkte** – Öffnen Sie ein paar Produkte, insbesondere solche mit Varianten (Größe, Farbe usw.), und bestätigen Sie, dass die Variantenoptionen und Preise korrekt übertragen wurden, und dass die Bilder angehängt und auf der Frontseite angezeigt werden, nicht nur im Admin.
- **Kategorien** – Bestätigen Sie, dass die Kategorienhierarchie richtig aussieht, insbesondere wenn Sie von Shopify migriert haben, bei der Sammlungen als flache Liste und nicht als verschachtelten Baum importiert werden.
- **Kundennachweise** – Überprüfen Sie E-Mails und Adressen auf ein paar Einträgen.


Migrierte Kunden bringen ihr altes Passwort nicht mit — Spwig kann es nicht von der Quellplattform auslesen — daher **müssen Kunden ihr Passwort beim ersten Anmeldeversuch zurücksetzen**.

Überlege dir eine Vorbereitungsmail, sobald du online gehst.
- **Bestellungen** — Stelle sicher, dass Gesamtbeträge, Status und Zeilenartikel einer Stichprobe von Bestellungen mit dem, was du auf der alten Plattform gesehen hast, übereinstimmen.
- **Erweiterungs-basierte Produkte** — Wenn du von WooCommerce migriert hast und Erweiterungen wie Subscriptions, Bundles, Geschenkkarten, Komposite-Produkte oder Buchungen verwendet hast, überprüfe Produkte, die diese genutzt haben.

Erweiterungsdaten, die nicht gelesen werden können, blockieren nicht die Importierung des Produkts — es wird dennoch importiert, nur ohne diese zusätzliche Konfiguration — daher sind diese Produkte am wahrscheinlichsten eine manuelle Nachbearbeitung zu benötigen.

## Steuern und Versand konfigurieren

Die Optionen des Assistenten im Schritt 4 zur Importierung von Steuereinstellungen und Versandzonen protokollieren deine Präferenzen, werden aber nicht auf den Import angewendet — keine Steuersätze oder Versandzonen werden daraus erstellt. Das ist erwartet: **Die Einrichtung von Steuern und Versand ist ein normaler, separater Schritt, den du direkt in Spwig nach Abschluss des Datenimports durchführst**, genauso wie du es bei der Einrichtung eines neuen Geschäfts tun würdest.

Die **Preisanpassung**-Steuerung auf demselben Schritt ist die Ausnahme — sie hat bei WooCommerce-, CSV- und Shopify-Imports Auswirkung und verschiebt den Grundpreis jedes Produkts, während es erstellt wird. Wenn du eine festgelegt hast und deine Preise falsch aussehen, ist das der Ursprung des Problems. Siehe [Migration Field Mapping](migration-field-mapping) für die Details.

Bevor du online gehst, konfiguriere:

- Deine Steuersätze — siehe [Tax Configuration](tax-configuration), um Sätze nach Land, Bundesland oder Region einzurichten, einschließlich jeder Steuerbefreiung, die deine Produkte benötigen.
- Deine Versandzonen und -methoden — siehe [Setting Up Shipping](setup-shipping), um die Versandoptionen zu reproduzieren, die deine Kunden auf deiner alten Plattform hatten.

Tue dies vor dem Testen des Checkouts, damit dein Testauftrag die tatsächlichen Gesamtbeträge widerspiegelt.

## Dein Bericht herunterladen

Die Abschlussseite bietet drei Downloads an:

- **PDF herunterladen** — ein formatierter Zusammenfassung mit Job-Metadaten, Zählungen pro Schritt und einer Liste von Fehlern, begrenzt auf die **ersten 20 Fehler**.
- **CSV herunterladen** — dieselbe Zusammenfassung in Tabellenform, begrenzt auf die **ersten 50 Fehler**.
- **Protokolle herunterladen** — alle Protokolldaten für den Job, ohne Begrenzung.

Wenn die Anzahl der Fehle nicht groß ist, reichen PDF oder CSV aus. Bei einer Migration mit einer großen Anzahl an Fehlern lade stattdessen die Protokolle herunter — dies ist die einzige der drei mit dem vollständigen Protokoll anstelle einer abgeschnittenen Stichprobe.

> **Tipp:** Migration-Job-Protokolle — einschließlich ihrer Protokolle und Berichte — bleiben in Spwig unbegrenzt; nichts entfernt sie nach einem Zeitplan. Lade dennoch eine Kopie herunter, wenn du sie für Offline-Protokolle oder um sie mit jemandem zu teilen, der keinen Admin-Zugriff hat, benötigst. Es gibt jedoch keine Countdown-Zwang, dies heute zu tun.

## Online gehen

Sobald du mit deinen Daten, Steuern und Versandkonfiguration zufrieden bist:

1. **Teste den Checkout vollständig.** Füge ein Produkt zum Warenkorb hinzu, vollende den Checkout und bestätige, dass Steuern, Versand und Zahlung korrekt berechnet und verarbeitet werden, idealerweise mit einer echten Zahlungsmethode im Testmodus.
2. **Aktualisiere deine DNS-Einstellungen**, um deinen Domain-Namen nur dann auf Spwig zu verweisen, wenn dieser Test erfolgreich war. Schalte die DNS nicht zuerst um und debugge danach — Kunden könnten währenddessen auf einen defekten Checkout stoßen.
3. **Behalte deine alte Plattform in einem schreibgeschützten oder „geschlossenen“ Zustand**, bis du sicher bist, dass die neue Plattform Bestellungen korrekt verarbeitet. Dies gibt dir eine Ausweichmöglichkeit, ohne das Risiko, dass Bestellungen auf der alten Plattform nach dem Wechsel platziert werden.

## Zugriffsrechte auf der Quellplattform widerrufen

Sobald du die Migration als abgeschlossen bestätigt hast und keine erneute Ausführung erwartest, kehre zu deiner Quellplattform zurück und widerrufe oder lösche den API-Schlüssel, die App oder die Integration, die du für sie erstellt hast (siehe [Migrating from WooCommerce](migrate-from-woocommerce) oder den entsprechenden Plattformleitfaden, um zu erfahren, wo sich diese Zugriffsrechte befinden).


Spwig benötigt keinen ständigen Zugriff auf Ihren alten Store, nachdem der Import abgeschlossen ist, daher ist das Entfernen davon eine gute Idee, um ein nicht mehr verwendeter Zugangsdaten zu schließen.

## Tips

- **Übersprungen ist in der Regel in Ordnung, fehlgeschlagen ist nicht** — eine große Anzahl an übersprungenen Elementen nach einem Neuerprobung mit "Überspringen bestehender Elemente" aktiviert ist erwartet; eine nicht-null Anzahl an fehlgeschlagenen Elementen verdient einen Blick in die Protokolle.
- **Gehen Sie nicht zu schnell mit "Anwenden genehmigter Links"** — Genehmigungen und Überspringen können bis kurz vor dem Klicken auf "Anwenden" geändert werden, also nehmen Sie sich die Zeit bei den Links mit geringer Zuverlässigkeit.
- **Richten Sie Steuern und Versand vor Ihrem ersten Live-Verkauf ein**, nicht danach — der Import tut dies nicht für Sie, und eine nicht konfigurierte Steuer ist leicht zu übersehen, bis ein Kunde beschwert.
- **Warnen Sie Ihre Kunden vor Passwort-Reset**, wenn Sie Ihre Kundenliste per E-Mail über den Umzug informieren, damit die erste Anmeldung keine Überraschung ist.
- **Laden Sie Ihren Bericht vor dem 90-Tage-Mark herunter**, wenn Sie ihn für Buchhaltung oder Compliance-Dokumentation benötigen.
- **Behalten Sie den alten Store für eine Weile bei, nur zum Lesen**, — es kostet wenig und gibt Ihnen ein Sicherheitsnetz während Ihrer ersten Tage auf Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Migration completion page showing the stat cards and Imported/Skipped/Failed/Total summary table
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Link Rewriting panel with grouped suggestions, confidence percentages, and the Approve/Skip/Apply Approved Links controls
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->