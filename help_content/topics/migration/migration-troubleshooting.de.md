---
title: Fehlerbehebung bei Migrationen
---

Die meisten Migrationen verlaufen ohne Zwischenfälle, aber Verbindungen können fehlschlagen, Imports können ablaufen, und gelegentlich stoppt ein Lauf mitten im Prozess. Dieses Thema behandelt das Diagnostizieren einer fehlgeschlagenen Verbindung, das Lesen des Fortschrittslogs während eines Imports und – am wichtigsten – was Ihre Optionen wirklich sind, sobald etwas schiefgeht, einschließlich dessen, was Retry, Cancel und Rollback tatsächlich tun.

## Verbindungsfehler im Schritt 2

Das Kontrollkästchen **Testverbindung vor dem Fortfahren** ist standardmäßig aktiviert und ist Ihre erste Diagnose – es validiert die Anmeldeinformationen gegen die Quellplattform, bevor Sie den Rest des Assistenten bestätigen. Wenn es fehlschlägt, weist die Fehlermeldung normalerweise auf eines dieser Probleme hin:

- **WooCommerce** – Store-URL fehlt `https://` oder hat einen nachgestellten Pfadabschnitt; falsch geschriebener oder neu generierter Consumer Key/Secret; oder ein REST-API-Schlüssel, der ohne **Read**-Berechtigung unter **WooCommerce > Einstellungen > Erweitert > REST-API** erstellt wurde.
- **Shopify** – Store-Domain ist nicht im Format `yourstore.myshopify.com`; Client-ID/Secret aus der falschen App; oder am häufigsten eine App, die im Dev-Dashboard erstellt, aber nie tatsächlich **installiert** wurde – das Erstellen einer App-Version reicht nicht aus, Sie benötigen den benutzerdefinierten Verteilungslink und einen Klick auf **Install**. Spwig warnt auch, wenn `read_products`, `read_customers` oder `read_orders` nicht in den Berechtigungen der App enthalten waren.
- **Magento 2** – Store-URL, die auf das Frontend und nicht auf die API-Stammadresse zeigt, oder eine Integrationstoken, das erstellt, aber nie aktiviert wurde (**Speichern > Aktivieren > Erlauben**).
- **SSL-Probleme** – ein abgelaufenes, selbstsigniertes oder falsch konfiguriertes Zertifikat führt zur Verbindungsfehler, bevor die Anmeldeinformationen überprüft werden, und zeigt sich als allgemeiner Fehler anstatt als Authentifizierungsfehler. Wenn die Anmeldeinformationen korrekt aussehen, überprüfen Sie als nächstes das Zertifikat.

Führen Sie den Verbindungstest nach jedem Fehlerbehebung erneut aus, anstatt mehrere Anmeldeinformationen gleichzeitig zu ändern – das isoliert, welche falsch war.

## Lesen des Live-Logs im Schritt 5

Während ein Import läuft, zeigt Schritt 5 ein Protokoll der Aktivitäten in Echtzeit an. Klicken Sie auf **Details anzeigen**, um es in Einträge – Ebene und Nachricht – aufzuteilen, anstatt nur die Zusammenfassung des aktuellen Schritts anzuzeigen. Dies ist der schnellste Weg, um zu sehen, was passiert, wenn der Fortschritt scheinbar stillsteht: eine Wand von „übersprungenen“ Einträgen für einen Datentyp bedeutet normalerweise, dass „Vorhandene Elemente überspringen“ wie vorgesehen funktioniert, nicht dass etwas feststeckt.

Die Ansicht des Logs zeigt nur die **neuesten 500 Einträge** an, also bei einer großen Migration scrollen die frühesten Einträge aus dem Sichtbereich, während der Import noch läuft. Wenn Sie das vollständige Log nach Abschluss eines Datentyps benötigen, verwenden Sie stattdessen **Protokolle herunterladen** auf der Ergebnisseite – es hat keine solche Begrenzung.

## Was ein fehlgeschlagene Migration tatsächlich bedeutet

Dies ist das Wichtigste zu verstehen, wenn eine Migration fehlschlägt.

Wenn eine Migration fehlschlägt, sagt die Abschlussseite Ihnen klar, was passiert ist: die Elemente, die vor dem Fehler importiert wurden, befinden sich immer noch in Ihrem Store, nichts wurde automatisch entfernt, und das Beheben des Problems und das erneute Ausführen des Imports überspringt, was bereits im ersten Mal importiert wurde. Nehmen Sie dies wörtlich. Kein Schritt im Import läuft innerhalb einer Datenbanktransaktion, die als Einheit zurückgerollt werden könnte – alles, was erfolgreich importiert wurde, bis zum Punkt des Fehlers, Produkte, Kategorien, Kunden, Bestellungen, was auch immer die Aufgabe durchgeführt hat, bleibt in Ihrem Store genau so, wie es erstellt wurde. Eine fehlgeschlagene Migration ist eine **partielle** Migration, nicht eine rückgängig gemachte.

Ein Fehler markiert auch die Aufgabe als nicht mehr rückgängig machbar, also wird der **Rollback**-Knopf auf einer fehlgeschlagenen **Import**-Aktion nicht verfügbar sein – er erscheint erst, wenn eine Migration abgeschlossen ist, oder wenn ein Rollback einer abgeschlossenen Migration selbst mitten im Prozess fehlschlägt, in diesem Fall bietet Spwig den Knopf erneut an, damit Sie den Vorgang erneut versuchen können. Die eine Situation, in der Sie am meisten eine automatische Rückgängigmachung wünschen würden – eine fehlgeschlagene Import – ist genau die Situation, in der der Knopf nicht angeboten wird.

Also, wenn eine Migration fehlschlägt:


1. **Überprüfen Sie, was tatsächlich importiert wurde**, mithilfe der Zahlen für Importiert/Übersprungen/Fehlgeschlagen und der heruntergeladenen Protokolle, um ein Bild davon zu erhalten, was sich in Ihrem Store befindet, und was nicht funktioniert hat.

2. **Entscheiden Sie, wie Sie die Daten bereinigen möchten.** Für eine kleine Menge an unvollständigen Daten überprüfen Sie diese manuell und löschen Sie das, was Sie nicht wollen, über die normalen Admin-Listenansichten.

Für eine größere oder unordentliche Teilimport ist es oft schneller, die importierten Daten selbst zu löschen, bevor Sie neu beginnen, als sie einzeln zu bereinigen.

3. **Führen Sie den Import erneut mit der Option „Vorhandene Elemente überspringen“ aktiviert durch**, unabhängig davon, welchen Bereinigungsweg Sie wählen – dies verhindert, dass die Daten, die überlebt haben, bei der nächsten Versuch dupliziert werden.

## Wiederholen

**Wiederholen** startet den Import vollständig von vorn. Es löscht die vorherigen Zähler und Protokolle des Jobs und importiert alles von Grund auf neu – es **fährt nicht** von dem Punkt fort, an dem der fehlgeschlagene Versuch abgebrochen wurde. Aktivieren Sie **Vorhandene Elemente überspringen**, damit Elemente, die bereits beim ersten Mal importiert wurden, nicht beim zweiten Durchlauf dupliziert werden.

Wenn eine Migration aufgrund des **4-Stunden**-Limits stoppt, ist die angezeigte Nachricht korrekt: das erneute Ausführen des Imports beginnt von vorn und überspringt Elemente, die bereits importiert wurden, und ist **kein** Fortsetzen vom Punkt, an dem der Import abgebrochen wurde. Für einen Store, der groß genug ist, um das Zeitlimit zu erreichen, ist das Wiederholen des gesamten Prozesses selten erfolgreich; stattdessen reduzieren Sie den Umfang jedes Durchlaufs, indem Sie in Schritt 3 weniger Datentypen auswählen (z. B. Produkte in einem Durchlauf, Bestellungen in einem anderen) und mehrere kleinere Durchläufe durchführen.

## Abbrechen

**Abbrechen** ist während eines laufenden Migrationsvorgangs verfügbar und markiert den Job sofort als fehlgeschlagen. Es **stoppt nicht** den Hintergrundimportauftrag, der weiterläuft und Daten schreibt, bis er zu einem natürlichen Endpunkt kommt. Erwarten Sie, dass die importierten Zahlen weiter ansteigen, nachdem Sie abgebrochen haben – lassen Sie sie sich erst beruhigen, bevor Sie entscheiden, was Sie bereinigen möchten, anstatt auf die Zahlen zu reagieren, die Sie beim Klicken auf **Abbrechen** erfasst haben.

## Es gibt keine Pause oder Fortsetzung

Spwig unterstützt das Anhalten eines laufenden Migrationsvorgangs und das später Wiederaufnehmen nicht. Die **Fortsetzen**-Schaltfläche auf dem Dashboard ist für einen anderen Fall vorgesehen: eine Migration, die über den Assistenten konfiguriert, aber noch nie gestartet wurde. Sie öffnet den Assistenten erneut, an dem Sie ihn verlassen haben – unabhängig von einem bereits laufenden Durchlauf.

## Rollback

> **Warnung:** Rollback ist eine dauerhafte, zerstörerische Aktion. Lesen Sie diesen Abschnitt vollständig, bevor Sie ihn verwenden.

Rollback wird für eine **abgeschlossene** Migration angeboten, und erneut für eine, bei der der Rollback zuvor teilweise fehlgeschlagen ist (Status **Rollback fehlgeschlagen**), sodass ein gestoppter Rollback erneut versucht werden kann. Es entfernt nur das, was der Import selbst erstellt hat, und behält alles bei, auf das Ihr Store jetzt angewiesen ist:

- Ein migrierter Kunde, der seit dem Import eine echte Bestellung platziert hat, wird **behalten** – sein Konto, Adressen, Treuehistorie und Store-Guthaben bleiben bei ihm, und diese echte Bestellung bleibt unverändert. Nur die Bestellungen, die der Import erstellt hat, werden entfernt.
- Ein migrierter Produkt, das immer noch von einer Bestellung, einem Bundle, einer Geschenkkarte oder einem Konfiguratoren-Slot referenziert wird, wird **behalten**. Bestellungen anderer Kunden werden niemals geändert – ein Rollback kann keine Zeilen aus einer unabhängigen Bestellung entfernen oder sie mit dem falschen Gesamtbetrag lassen.
- Was auch immer behalten wird, wird Ihnen mit Namen und Anzahl gemeldet, zusammen mit dem Grund – zum Beispiel „1 Produkt behalten, immer noch von einer Bestellposition referenziert“ – damit Sie genau wissen, was noch vorhanden ist und warum.
- Affiliate-Beziehungen, Kommissionen und Auszahlungen, die der Import erstellt hat, **werden entfernt**, zusammen mit jedem Affiliate-Konto, das der Import erstellt hat. Ein Affiliate, der einem Kunden zugeordnet ist, der bereits existiert, behält sein Konto; nur der Affiliate-Record wird entfernt.
- Treuehistorie und Store-Guthaben folgen dem Kunden: entfernt, wenn der Kunde entfernt wird, behalten, wenn der Kunde behalten wird.

Es entfernt immer noch **keine** Abonnement-Pläne, Preisstufen oder Buchungsressourcen, die von Store-Erweiterungen erstellt wurden – diese überstehen einen Rollback und müssen manuell bereinigt werden, wenn Sie sie nicht haben möchten.

Bevor Sie bestätigen, zeigt die Bestätigungsseite eine Vorschau davon, was genau entfernt und was beibehalten wird, berechnet anhand Ihrer Live-Daten – lesen Sie sie vor dem Klicken auf **Ja, Migration rückgängig machen**.

Die Rückgängigmachung wird dann im Hintergrund und nicht in Ihrem Browser durchgeführt, sodass es sicher ist, den Tab zu schließen; prüfen Sie den Status der Migration, um den Bericht darüber zu erhalten, was tatsächlich entfernt und beibehalten wurde, sobald sie abgeschlossen ist.

Da die Rückgängigmachung nicht weiter geht als das, was die Importierung erstellt hat, ist sie nicht mehr ein Tool, das nur am selben Tag verwendet werden kann – die echten Bestellungen eines migrierten Kunden und die echten Verkäufe eines migrierten Produkts sind geschützt, unabhängig davon, wie viel Zeit seit der Migration vergangen ist. Es handelt sich dennoch um eine dauerhafte, zerstörerische Aktion für die Zeilen, die sie tatsächlich entfernt, also verwenden Sie sie bewusst und nicht leichtsinnig, und entfernen Sie manuell alles, was Spwig beibehält, das Sie tatsächlich nicht wollen.

Bei der Verfügbarkeit: Der Rückgängig-Migration-Button bleibt auf der Zusammenfassung einer abgeschlossenen Migration so lange aktiv, wie der Job-Record existiert – bei den meisten Plattformen gibt es keinen festen Deadline. Magento ist die Ausnahme und verliert die Rückgängig-Möglichkeit nach einem festgelegten Zeitraum, also entscheiden Sie sich schnell, wenn Sie Magento verwenden. Job-Records werden nicht nach einem Zeitplan entfernt, sodass eine Migration theoretisch immer rückgängig gemacht werden kann, es sei denn, Sie löschen den Record selbst.

## Strategie für große Stores und langsame Imports

Für einen Store, der groß genug ist, dass eine einzelne Ausführung das 4-Stunden-Limit riskiert:

- **Erhöhen Sie die Batch-Größe** im Schritt 3 (bis zu 100) – größere Batches bedeuten in der Regel weniger Roundtrips und eine schnellere Durchsatzrate.
- **Teilen Sie die Migration in mehrere Ausführungen nach Datentyp auf** – Kategorien und Produkte in einer Ausführung, Kunden und Bestellungen in einer Folgeausführung, anstatt alles auf einmal.
- **Behalten Sie Skip existing items aktiviert** für jede Ausführung nach der ersten, damit wiederholte Ausführungen nichts duplizieren, was bereits erfolgreich war.
- **Deaktivieren Sie Import product images.** Das Herunterladen und Verarbeiten jedes Bildes ist in der Regel der größte Faktor für eine langsame Ausführung. Sie können Bilder zu Produkten einzeln hinzufügen oder über einen separaten CSV-Import, sobald der Rest der Daten vorhanden ist.

## Tipps

- **Testen Sie die Verbindung nach jeder Änderung der Anmeldeinformationen**, nicht nur einmal am Ende – das isoliert den Wert, der falsch ist.
- **Nehmen Sie nie an, dass ein fehlgeschlagener Job sich selbst bereinigt hat** – prüfen Sie, was tatsächlich in Ihrem Store vorhanden ist, bevor Sie eine Bereinigung oder einen erneuten Versuch planen.
- **Skip existing items sollte aktiviert bleiben für jeden erneuten Versuch** – es ist das einzige, was Duplikate bei einem zweiten Durchlauf verhindert.
- **Kämpfen Sie nicht gegen das 4-Stunden-Limit mit mehreren erneuten Versuchen** – teilen Sie stattdessen nach Datentyp auf.
- **Lesen Sie die Rückgängig-Vorschau vor der Bestätigung** – sie nennt genau, was entfernt und was beibehalten wird, berechnet anhand Ihrer Live-Daten, sodass es keine Überraschungen gibt.