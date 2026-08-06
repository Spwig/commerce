---
title: Plattform-Updates
---

Ihre Spwig-Installation besteht aus einer Sammlung von Komponenten – Themes, Widgets, Integrationen, Elementen des Seitenbauers und Verbindungen zu Anbietern – jede mit ihrer eigenen Version, die unabhängig aktualisiert werden kann. Das Komponenten-Register bietet Ihnen eine zentrale Übersicht über alles Installierte, zeigt an, welche Komponenten Updates warten, und ermöglicht es Ihnen, Updates jederzeit zu installieren oder zurückzusetzen.

![Übersicht des Komponenten-Registers](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Verständnis des Komponenten-Registers

Navigieren Sie zu **System Dashboard > Komponenten-Updates**, um jede installierte Komponente in Ihrem Geschäft zu sehen. Jede Zeile zeigt:

- **Name** – der Anzeigename der Komponente
- **Typ** – was für eine Komponente es ist (Theme, Widget, Integration usw.)
- **Aktuelle Version** – die Version, die derzeit in Ihrem Geschäft läuft
- **Update-Status** – ob ein Update verfügbar ist
- **Kanal** – welchem Update-Kanal die Komponente folgt
- **Automatisches Update** – ob Updates automatisch installiert werden
- **Gesperrt** – ob die Komponente auf ihrer aktuellen Version gefroren ist

Das Dashboard oben auf der Seite zeigt Zusammenfassungszahlen an: Gesamtzahl der installierten Komponenten, wie viele Updates verfügbar sind und wie viele aktuell sind.

### Komponententypen

| Typ | Was es ist |
|-----|------------|
| Theme | Das visuelle Design Ihres Geschäfts |
| Widget | Wiederverwendbare Blöcke des Seitenbauers |
| Element des Seitenbauers | Benutzerdefinierte Elemente für den Seitenbauer |
| Hilfsmittel des Seitenbauers | Editor-Tools und Hilfsmittel |
| Kopf-/Fußleiste-Vorlage | Layouts für Kopf- und Fußleiste |
| Versand-Anbieter | Integrationen zu Versanddiensten (FedEx, UPS usw.) |
| E-Mail-Anbieter | E-Mail-Versanddienste |
| Zahlung-Anbieter | Integrationen zu Zahlungsgattern |
| Wechselkurs-Anbieter | Quellen für Wechselkursdaten |
| Übersetzung-Anbieter | KI-Übersetzungsdienste |
| Sprachpaket | Übersetzungsdateien für die Oberfläche |

## Update-Kanäle

Jede Komponente folgt einem Update-Kanal, der bestimmt, welche Releases sie erhält. Sie können jede Komponente basierend auf dem Risikopotenzial, mit dem Sie sich wohlfühlen, einem anderen Kanal zuweisen.

| Kanal | Beschreibung | Bestens geeignet für |
|-------|-------------|---------------------|
| **Stabil** | Für Produktion bereit, gründlich getestete Releases | Alle Komponenten auf Live-Geschäften |
| **Beta** | Vorab-Builds für das Testen neuer Funktionen, bevor sie stabil werden | Nicht-kritische Komponenten, die Sie vorab testen möchten |
| **Entwicklung** | Neueste Funktionen, möglicherweise instabil | Nur Testumgebungen |
| **Sicherheit** | Nur kritische Sicherheitspatches, mit höchster Priorität geliefert | Komponenten, bei denen Stabilität von höchster Priorität ist |

Um den Kanal einer Komponente zu ändern, klicken Sie auf ihren Namen, um die Detailansicht zu öffnen, wählen Sie dann einen neuen Wert im Feld **Update-Kanal** aus und speichern Sie die Änderung.

## Nach Updates suchen

Spwig prüft automatisch auf Updates im Intervall, das in Ihren Update-Server-Einstellungen konfiguriert ist (Standard: alle 24 Stunden). Um sofort zu prüfen:

1. Navigieren Sie zu **System Dashboard > Komponenten-Updates**
2. Klicken Sie auf die Schaltfläche **Nach Updates suchen**, die oben auf der Seite steht
3. Das System kontaktiert den Spwig-Update-Server und aktualisiert den Update-Status für alle Komponenten
4. Komponenten mit verfügbaren Updates werden hervorgehoben, und die Anzahl **Verfügbare Updates** wird aktualisiert

Sie können auch eine Update-Prüfung für einzelne Komponenten mithilfe der Aktion **Nach Updates suchen** aus dem Aktionen-Menü der Liste auslösen.

## Updates installieren

### Einzelne Komponente aktualisieren

1. Navigieren Sie zu **System Dashboard > Komponenten-Updates**
2. Finden Sie die Komponente, die Sie aktualisieren möchten – Komponenten mit verfügbaren Updates zeigen einen Update-Indikator neben ihrer Version an
3. Klicken Sie auf die Schaltfläche **Update installieren**, die in der Zeile der Komponente steht
4. Bestätigen Sie das Update, wenn Sie aufgefordert werden
5. Das Update wird heruntergeladen, überprüft und installiert – ein Fortschrittsindikator zeigt jeden Schritt an
6. Nach Abschluss wird die **Aktuelle Version** der Komponente auf die neue Versionsnummer aktualisiert

### Mehrere Komponenten aktualisieren

1.

Markieren Sie die Kontrollkästchen neben den Komponenten, die Sie aktualisieren möchten
2.



Wählen Sie **Aktualisierungen installieren** im **Aktion**-Dropdownmenü aus
3.

Klicken Sie auf **Weiter**, um fortzufahren
4.

Aktualisierungen werden in Abhängigkeitsreihenfolge installiert — Komponenten, auf die andere Komponenten angewiesen sind, werden zuerst aktualisiert

### Was während einer Aktualisierung passiert

Der Aktualisierungsprozess durchläuft diese Phasen:

1. **Überprüfen** — bestätigt, dass die Aktualisierung verfügbar ist und Ihr Lizenzschlüssel gültig ist
2. **Herunterladen** — lädt das Paket vom Spwig-Aktualisierungsserver herunter
3. **Überprüfen** — prüft die Integrität des Pakets anhand eines SHA-256-Prüfsummenwerts
4. **Entpacken** — entpackt die neuen Dateien
5. **Bereitstellen** — aktiviert die neue Version
6. **Gesundheitsprüfung** — überprüft, ob die Komponente nach der Aktualisierung funktioniert

Falls eine Phase fehlschlägt, versucht das System automatisch, die vorherige Version wiederherzustellen.

## Plattformweite Aktualisierungen

Zusätzlich zu einzelnen Komponenten kann Spwig auch plattformweite Aktualisierungen empfangen, die den Kernspeicher selbst aktualisieren. Diese Aktualisierungen durchlaufen einen umfassenderen Prozess, einschließlich Datenbankmigrationen und einer kurzen Wartungszeit.

Navigieren Sie zu **System Dashboard > Plattformaktualisierungen**, um plattformweite Aktualisierungen separat von einzelnen Komponenten anzuzeigen und zu verwalten.

### Überprüfen Sie, was neu ist, bevor Sie eine Installation durchführen

Klicken Sie auf **Auf Aktualisierungen prüfen**, um zu sehen, ob eine neue Plattformversion verfügbar ist. Wenn eine gefunden wird, zeigt die Karte **Aktualisierung verfügbar** die Versionänderung (z. B. `v1.7.0 → v1.7.1`), die **Paketgröße**, die **Schätzzeit** und den **Kanal** der Aktualisierung — sowie einen **Was ist neu**-Vorschau, damit Sie sehen können, was sich geändert hat, bevor Sie entscheiden, die Aktualisierung zu installieren:

- Eine kurze Zusammenfassung, die die Veröffentlichung beschreibt
- Eine Aufzählung der wichtigsten Änderungen in dieser Version (bis zu fünf, mit einer Notiz, wenn es mehr gibt)

Wenn die Aktualisierung Ihre Datenbankstruktur ändert, erscheint eine Meldung **Datenbankmigration erforderlich** mit einer geschätzten Zeit. Sicherheitsaktualisierungen zeigen ein **Sicherheitsaktualisierung**-Abzeichen, das empfiehlt, sie sofort zu installieren. Lesen Sie den Vorschau von **Was ist neu** vor der Installation — es ist der schnellste Weg, um zu sehen, ob eine Veröffentlichung besondere Aufmerksamkeit erfordert, wie z. B. Schritte, die nach der Upgrade-Vollendung durchgeführt werden müssen.

Die Historie der Plattformaktualisierungen ist weiter unten auf der Seite sichtbar. Jeder Eintrag zeigt die Versionsumschaltung (z. B. `v1.3.2 → v1.3.3`), den Status und die Dauer des Aktualisierungsprozesses.

Sicherheitsaktualisierungen werden separat markiert und, wenn **Automatische Installation von Sicherheitsaktualisierungen** in Ihrer Aktualisierungsserver-Konfiguration aktiviert ist, werden sie automatisch installiert, ohne manuelle Aktion zu erfordern.

## Anzeigen der Versionsgeschichte

Um alle zuvor installierten Versionen einer Komponente anzuzeigen:

1. Klicken Sie auf den Namen der Komponente, um ihre Detailansicht zu öffnen
2. Scrollen Sie zu dem Abschnitt **Komponentenversionen** am unteren Ende der Seite
3. Jeder Versionseintrag zeigt die Versionsnummer, wann sie installiert wurde, die Installationsmethode und ihren Gesundheitsstatus

Das System behält die letzten drei installierten Versionen für eine Rückverfolgung bereit. Versionen darüber hinaus werden automatisch entfernt.

## Eine Komponente zurückrollen

Wenn eine Aktualisierung Probleme verursacht, können Sie zu einer früheren Version zurückkehren:

1. Öffnen Sie die Detailansicht der Komponente
2. Scrollen Sie zu dem Abschnitt **Zurückrollen**
3. Wählen Sie die Version aus, die Sie wiederherstellen möchten
4. Klicken Sie auf **Zurückrollen zu dieser Version**

Nur Versionen, die mit **Zurückrollen möglich** markiert sind, können wiederhergestellt werden. Der Eintrag im Rückroll-Protokoll dokumentiert, wer das Zurückrollen initiiert hat und wann.

## Komponenten sperren

Das Sperren einer Komponente verhindert, dass beliebige Aktualisierungen installiert werden, einschließlich automatischer. Dies ist nützlich, wenn Sie Anpassungen oder Integrationen haben, die auf einer bestimmten Version basieren.

1. Öffnen Sie die Detailansicht der Komponente
2. Aktivieren Sie das **Gesperrt**-Kästchen im Abschnitt **Sperren und Einfrieren**
3. Geben Sie einen Grund in **Sperfgrund** ein, damit Ihr Team weiß, warum sie gesperrt ist
4. Speichern Sie den Eintrag

Gesperrte Komponenten werden in der Registrierungsliste mit einem Schloss-Indikator angezeigt. Um sie zu entsperren, deaktivieren Sie **Gesperrt** und speichern Sie die Änderung.

## Aktualisierungsprotokolle einsehen

Das Aktualisierungsprotokoll protokolliert jede Installation, Aktualisierung, Rückverfolgung und Gesundheitsprüfung:

1.

Öffnen Sie die Detailansicht einer Komponente
2.

Die **Aktualisierungsprotokolle** sind am unteren Ende der Seite inline sichtbar
3.



Jeder Eintrag zeigt an: die durchgeführte Aktion, Start- und Endzeiten, alte und neue Versionen, ob es sich um eine automatische oder manuelle Aktion handelte, und ggf. Fehlermeldungen, wenn die Operation fehlgeschlagen ist

Log-Einträge mit dem Status **Failed** enthalten die vollständige Fehlermeldung, um bei der Problembehebung zu helfen.

## Aktivieren der automatischen Updates

Sie können Spwig erlauben, Updates automatisch zu installieren, sobald sie verfügbar sind:

1. Öffnen Sie die Detailansicht des Komponenten
2. Aktivieren Sie **Auto Update** im Abschnitt **Version & Update Status**
3. Speichern Sie den Eintrag

Wenn automatische Updates aktiviert sind, installiert das System die Updates während des nächsten geplanten Prüfzyklus. Sicherheitsupdates folgen der globalen Einstellung **Auto Install Security Updates**, unabhängig von den Einstellungen einzelner Komponenten.

## Tipps

- Aktualisieren Sie immer über den **Stable**-Kanal für Themes und Zahlungsdienstleister – dies sind die am häufigsten genutzten Komponenten, und Stabilität ist am wichtigsten
- Schließen Sie eine Komponente ab, bevor Sie eigene Änderungen an ihr vornehmen, und notieren Sie den Grund klar, damit zukünftige Teammitglieder wissen, dass sie nicht aktualisiert werden soll
- Prüfen Sie die **Release Notes** im Versionseintrag der Komponente, bevor Sie eine große Versionserhöhung installieren – Breaking Changes werden dort markiert
- Bevor Sie eine Plattformaktualisierung installieren, lesen Sie die **What's New**-Vorschau auf der Seite **Platform Updates** – für einen vollständigen Blick in die Release Notes, einschließlich zusätzlicher Schritte, die Sie möglicherweise durchführen müssen, wechseln Sie zur Seite **System Upgrade**
- Nach einem Update navigieren Sie zu dem betroffenen Bereich Ihres Shops, um sicherzustellen, dass alles wie erwartet aussieht und funktioniert, bevor Sie das Update als abgeschlossen erklären
- Wenn automatische Updates für eine Komponente aktiviert sind, überprüfen Sie die **Update Logs** regelmäßig, um sicherzustellen, dass die automatischen Updates erfolgreich abgeschlossen werden