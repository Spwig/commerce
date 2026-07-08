---
title: Multi-Währungseinstellungen
---

Multi-Währung ermöglicht es Ihren Kunden, Produkte anzusehen und den Kaufvorgang in ihrer bevorzugten Währung abzuschließen. Preise werden automatisch aus Ihrer Basiswährung mithilfe von Wechselkursen eines verbundenen Anbieters oder manuell definierten Kursen konvertiert.

## Vor dem Beginn

Bevor Sie Multi-Währung aktivieren, benötigen Sie:

1. **Einen aktiven Wechselkursanbieter** - Gehen Sie zu **Einstellungen > Multi-Währung > Wechselkurs-Dashboard** und verbinden Sie mindestens einen Anbieter (z. B. Open Exchange Rates, Fixer.io oder ExchangeRate-API). Der Anbieter muss aktiv und synchronisiert sein.
2. **Mindestens zwei Währungen** - Ihre Basiswährung plus eine oder mehrere zusätzliche Währungen, die Sie unterstützen möchten.

## Aktivieren der Multi-Währung

Navigieren Sie zu **Einstellungen > Multi-Währung** und aktivieren Sie **Multi-Währung aktivieren**. Nachdem Sie Multi-Währung aktiviert haben, konfigurieren Sie die folgenden Optionen:

| Einstellung | Beschreibung |
|---------|-------------|
| **Währungsauswahlmodus** | Wie Kunden ihre Währung auswählen. *Automatisch* erkennt die Währung aus der Standortinformation, *Manuell* ermöglicht es Kunden, eine Währung über einen Wechsler auszuwählen, *Beide* kombiniert beide Ansätze. |
| **Währungswechsler anzeigen** | Zeigt einen Währungswechsler auf Ihrem Online-Shop an, damit Kunden die Währung manuell ändern können. |
| **Wechslerposition** | Wo der Währungswechsler angezeigt wird (Kopfzeile, Fußzeile oder Seitenleiste). |
| **Wechselkursinformationen anzeigen** | Zeigt Kunden eine Nachricht an, dass Preise ungefähre Konvertierungen aus Ihrer Basiswährung sind. |
| **Lokale Formatierung aktivieren** | Formatiert Zahlen und Währungssymbole entsprechend der Lokalisation jedes Kunden (z. B. 1.234,56 für europäische Formate). |

## Kaufmodus

Wählen Sie aus, wie Multi-Währung beim Kaufvorgang funktioniert:

| Modus | Beschreibung |
|------|-------------|
| **Vollständige Multi-Währung** | Kunden können Produkte ansehen, in den Warenkorb legen und in ihrer ausgewählten Währung bezahlen. Der Wechselkurs wird beim Kauf gesperrt und mit der Bestellung gespeichert. Dies ist die Standardoption. |
| **Nur Anzeige** | Preise werden in der Währung des Kunden angezeigt, um die Bequemlichkeit zu erhöhen, aber der Warenkorb und die Zahlung werden immer in Ihrer Basiswährung verarbeitet. Beim Kauf sehen Kunden eine Nachricht, die den ungefähren konvertierten Betrag neben dem tatsächlichen Betrag in Ihrer Basiswährung anzeigt. |

**Nur Anzeige** ist nützlich, wenn Ihr Zahlungsanbieter nur Ihre Basiswährung unterstützt, oder wenn Sie das Wechselkursrisiko vollständig vermeiden möchten. Kunden sehen dennoch lokalisierte Preise beim Durchstöbern, was ihnen ein Gefühl für den Preis in ihrer eigenen Währung gibt.

## Wechselkurs-Synchronisationsintervall

Steuern Sie fest, wie oft Ihr Shop frische Kurse von Ihrem verbundenen Anbieter abruft:

| Intervall | Beschreibung |
|----------|-------------|
| **Echtzeit** | Alle 15 Minuten. Bestens geeignet für Shops mit hohem internationalen Verkaufsvolumen. |
| **Stündlich** | Einmal pro Stunde. Gutes Gleichgewicht zwischen Aktualität und API-Nutzung. |
| **Täglich** | Einmal pro Tag. Geeignet für die meisten Shops. Dies ist die Standardoption. |
| **Wöchentlich** | Einmal pro Woche. Für Shops mit stabiler Preisgestaltung. |
| **Monatlich / Quartalsweise** | Weniger häufige Updates für Shops, die selten Kurse ändern. |
| **Nur manuell** | Kurse werden nie automatisch abgerufen. Sie verwalten alle Kurse manuell. |

Das Synchronisationsintervall bestimmt, wie oft die Hintergrundaufgabe Kurse von Ihrem Anbieter abruft. Zwischen den Synchronisationen werden zwischengespeicherte Kurse verwendet. Wenn Sie eine sofortige Synchronisation erzwingen müssen, verwenden Sie die Schaltfläche **Jetzt synchronisieren** auf dem Wechselkurs-Dashboard oder **Vom Anbieter synchronisieren** auf der Seite für manuelle Wechselkurse.

## Manuelle Wechselkurse

Manuelle Wechselkurse ermöglichen es Ihnen, genaue Konvertierungskurse für bestimmte Währungspaare festzulegen. Sie haben Vorrang vor von Anbietern abgerufenen Kursen und geben Ihnen die volle Kontrolle über die Preise.

Navigieren Sie zu **Wechselkurse > Manuelle Wechselkurse**, um sie zu verwalten.

### Manuelle Kurse festlegen

Klicken Sie auf **Kurs hinzufügen**, um einen Kurs für ein Währungspaar zu erstellen. Geben Sie die Basiswährung, Zielwährung und den Kurs an. Zum Beispiel bedeutet das Festlegen von USD/EUR auf 0,92, dass 1 USD = 0,92 EUR.

### Von einem Anbieter synchronisieren

Klicken Sie auf **Vom Anbieter synchronisieren**, um manuelle Kurse automatisch aus den neuesten Kursen Ihres verbundenen Anbieters zu befüllen.

Dies erstellt manuelle Wechselkurse für alle unterstützten Währungen und gibt Ihnen einen Ausgangspunkt, um diese feiner abzustimmen.

Gesperrte Kurse werden während der Synchronisation übersprungen, sodass alle von Ihnen manuell angepassten Kurse nicht überschrieben werden.

### Kurse sperren

Klicken Sie auf das Schloss-Symbol neben einem Kurs, um sicherzustellen, dass dieser während der Synchronisation nicht überschrieben wird. Dies ist nützlich, wenn Sie einen spezifischen Kurs verhandelt haben oder einen festen Kurs unabhängig von Marktbewegungen beibehalten möchten.

- **Gesperrte** Kurse zeigen ein Schloss-Symbol an und werden nicht in die automatische Synchronisation einbezogen.
- **Nicht gesperrte** Kurse können aktualisiert werden, wenn Sie auf *Aus Provider synchronisieren* klicken.

### Vergleich der Anbieter

Jeder manuell festgelegte Kurs zeigt den aktuellen Kurs des Anbieters neben sich an, zusammen mit einem Prozentsatz Unterschied. Dies hilft Ihnen, auf einen Blick zu erkennen, wie sich Ihre manuell festgelegten Kurse zu den Marktkursen verhalten:

- Ein **grüner** Prozentsatz bedeutet, dass Ihr Kurs höher ist als der Anbieterkurs.
- Ein **roter** Prozentsatz bedeutet, dass Ihr Kurs niedriger ist als der Anbieterkurs.

## Wechselkurs-Zuschlag

Sie können einem Wechselkurs einen prozentualen Zuschlag hinzufügen, um Gebühren für Währungsumwandlungen zu decken und sich vor Kurschwankungen zu schützen, die zwischen dem Zeitpunkt des Bestellvorgangs eines Kunden und dem Zeitpunkt des Empfangs der Zahlung auftreten können.

Beispiel: Ein 2 %iger Zuschlag auf einen Wechselkurs von 1,18 USD/EUR würde diesen auf etwa 1,20 USD/EUR anpassen. Dieser kleine Puffer hilft dabei, sicherzustellen, dass Sie bei Währungsumwandlungen kein Geld verlieren.

## Strategie zur Auswahl von Kursen

Wenn Sie mehrere Wechselkurs-Anbieter verbunden haben, können Sie auswählen, wie Kurse ausgewählt werden:

- **Hauptanbieter** - Verwendet immer die Kurse Ihres festgelegten Hauptanbieters. Dies gewährleistet konsistente Preise in Ihrem Geschäft. Wenn der Hauptanbieter keine Daten für ein Währungspaar hat, wird stattdessen der neueste verfügbare Kurs von jedem Anbieter verwendet.
- **Neuester verfügbare Kurs** - Verwendet den neuesten synchronisierten Kurs von jedem aktiven Anbieter. Dies liefert Ihnen die aktuellsten Daten, allerdings können sich die Kurse leicht zwischen den Anbietern unterscheiden.

Für die meisten Geschäfte ist **Hauptanbieter** die empfohlene Wahl, da dieser die vorhersehbaresten Preise bietet.

## Unterstützte Währungen

Verwenden Sie den Drag-and-Drop-Währungs-Manager, um auszuwählen, welche Währungen Ihr Geschäft unterstützt:

1. **Verfügbare Währungen** (linker Spalte) zeigt alle Währungen an, die Sie aktivieren können.
2. **Aktive Währungen** (rechte Spalte) zeigt die Währungen an, die derzeit in Ihrem Geschäft aktiviert sind.
3. Ziehen Sie Währungen zwischen den Spalten, um sie zu aktivieren oder zu deaktivieren.
4. Ziehen Sie innerhalb der Aktiven-Spalte, um die Reihenfolge anzuzeigen, in der Währungen im Wechsler erscheinen.
5. Klicken Sie auf **Währungskonfiguration speichern**, um Ihre Änderungen anzuwenden.

Ihre Basewährung ist immer aktiv und kann nicht entfernt werden.

## Wie Wechselkurse gelöst werden

Wenn ein Preis in eine andere Währung umgerechnet werden muss, überprüft das System die Kurse in dieser Reihenfolge:

1. **Manueller Wechselkurs** - Wenn ein aktiver manueller Kurs für das Währungspaar vorhanden ist, wird dieser immer zuerst verwendet.
2. **Anbieterkurs** - Wenn kein manueller Kurs vorhanden ist, wird der neueste Kurs von Ihrem verbundenen Anbieter verwendet.

Das bedeutet, dass Sie Anbieter für die meisten Währungen verwenden können und bestimmte Paare mit manuellen Kursen überschreiben können, wenn Sie präzise Kontrolle benötigen.

## Wichtig: Diese Einstellung ist dauerhaft

Sobald die Mehrwährungsfunktion aktiviert ist und Kunden Bestellungen in fremden Währungen tätigen, kann diese Einstellung **nicht mehr deaktiviert** werden. Der Grund dafür ist:

- Bestellungen speichern dauerhaft die von dem Kunden gewählte Währung und den Wechselkurs, der zum Zeitpunkt des Kaufs verwendet wurde.
- Finanzberichte und Rückerstattungsberechnungen hängen von dieser historischen Währungsdaten ab.
- Die Deaktivierung der Mehrwährungsfunktion würde bestehende Bestellungen in fremden Währungen in einen inkonsistenten Zustand versetzen.

Wenn keine Bestellungen in fremden Währungen getätigt wurden, können Sie die Mehrwährungsfunktion immer noch deaktivieren.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Zuerst mit einer kleinen Bestellung testen** - Eine Testbestellung in einer fremden Währung aufgeben, um den Checkout-Flow zu überprüfen und sicherzustellen, dass Wechselkurse korrekt angewendet werden.
- **Wechselkurse regelmäßig überwachen** - Das Wechselkurse-Dashboard regelmäßig prüfen, um sicherzustellen, dass Ihr Anbieter die Kurse synchronisiert und diese sinnvoll erscheinen.
- **Aufwertung für volatilere Währungen berücksichtigen** - Wenn Sie Währungen mit hoher Volatilität unterstützen, kann eine leicht höhere Aufwertung (2-3 %) Ihre Gewinnmargen schützen.
- **Mit den wichtigsten Währungen beginnen** - Mit weit verbreiteten Währungen (EUR, GBP, JPY, CAD, AUD) beginnen und je nach Kundennachfrage erweitern.
- **Kompatibilität mit Zahlungsanbietern prüfen** - Nicht alle Zahlungsanbieter unterstützen alle Währungen.

Prüfen Sie die Dokumentation Ihres Zahlungsanbieters, um zu bestätigen, welche Währungen er verarbeitet.
- **Display Only-Modus verwenden, wenn unsicher** - Wenn Sie unsicher sind, ob Ihr Zahlungsanbieter den Mehrwährung-Checkout unterstützt, beginnen Sie mit dem Display Only-Modus.

Sie können später zu Full Multi-Currency wechseln.
- **Wechselkurse vor Werbeaktionen sperren** - Wenn Sie eine Aktion durchführen, sperren Sie die Wechselkurse im Voraus, um eine konsistente Preisgestaltung während der Werbeaktion sicherzustellen.