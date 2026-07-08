---
title: Plattform-Updates
---

Ihre Spwig-Installation besteht aus einer Sammlung von Komponenten — Themes, Widgets, Integrationen, Elementen des Seitenbauers und Verbindungen zu Anbietern — jede mit ihrer eigenen Version, die unabhängig aktualisiert werden kann. Das Komponenten-Register bietet Ihnen eine zentrale Übersicht über alles Installierte, zeigt an, welche Komponenten Updates warten, und ermöglicht es Ihnen, Updates jederzeit zu installieren oder zurückzusetzen.

![Übersicht des Komponenten-Registers](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Verständnis des Komponenten-Registers

Navigieren Sie zu **Erweiterungen > Komponenten-Register**, um jede installierte Komponente auf Ihrem Store anzuzeigen. Jede Zeile zeigt:

- **Name** — der Anzeigename der Komponente
- **Typ** — welcher Typ von Komponente es ist (Theme, Widget, Integration usw.)
- **Aktuelle Version** — die Version, die derzeit auf Ihrem Store läuft
- **Update-Status** — ob ein Update verfügbar ist
- **Kanal** — welchem Update-Kanal die Komponente folgt
- **Automatisches Update** — ob Updates automatisch installiert werden
- **Gesperrt** — ob die Komponente auf ihrer aktuellen Version gefroren ist

Das Dashboard oben auf der Seite zeigt Zusammenfassungszahlen an: Gesamtzahl der installierten Komponenten, wie viele Updates verfügbar sind und wie viele aktuell sind.

### Komponententypen

| Typ | Was es ist |
|------|------------|
| Theme | Das visuelle Design Ihres Stores |
| Widget | Wiederverwendbare Blöcke des Seitenbauers |
| Element des Seitenbauers | Benutzerdefinierte Elemente für den Seitenbauer |
| Hilfsmittel des Seitenbauers | Editor-Tools und Hilfsmittel |
| Header-/Footer-Vorlage | Layouts für Header und Footer |
| Versand-Anbieter | Integrationen zu Versanddiensten (FedEx, UPS usw.) |
| E-Mail-Anbieter | E-Mail-Versanddienste |
| Zahlung-Anbieter | Integrationen zu Zahlungsgattern |
| Wechselkurs-Anbieter | Quellen für Wechselkursdaten |
| Übersetzung-Anbieter | KI-basierte Übersetzungsdienste |
| Sprachpaket | Übersetzungsdateien für die Oberfläche |

## Update-Kanäle

Jede Komponente folgt einem Update-Kanal, der bestimmt, welche Releases sie erhält. Sie können jede Komponente basierend auf dem Risikopotenzial, mit dem Sie sich wohlfühlen, einem anderen Kanal zuweisen.

| Kanal | Beschreibung | Bestens geeignet für |
|---------|-------------|----------|
| **Stabil** | Fertige, gründlich getestete Releases | Alle Komponenten auf Live-Stores |
| **Beta** | Vorab-Builds zur Testung neuer Funktionen, bevor sie stabil werden | Nicht-kritische Komponenten, die Sie vorab testen möchten |
| **Entwicklung** | Neueste Funktionen, möglicherweise instabil | Nur Testumgebungen |
| **Sicherheit** | Nur kritische Sicherheitspatches, mit höchster Priorität geliefert | Komponenten, bei denen Stabilität von höchster Priorität ist |

Um den Kanal einer Komponente zu ändern, klicken Sie auf ihren Namen, um die Detailansicht zu öffnen, wählen Sie dann einen neuen Wert im Feld **Update-Kanal** aus und speichern Sie die Änderung.

## Nach Updates suchen

Spwig prüft automatisch auf Updates im Intervall, das in Ihren Update-Server-Einstellungen konfiguriert ist (Standard: alle 24 Stunden). Um sofort zu prüfen:

1. Navigieren Sie zu **Erweiterungen > Komponenten-Register**
2. Klicken Sie auf die Schaltfläche **Auf Updates prüfen**, die oben auf der Seite steht
3. Das System kontaktiert den Spwig-Update-Server und aktualisiert den Update-Status aller Komponenten
4. Komponenten mit verfügbaren Updates werden hervorgehoben, und die Anzahl **Verfügbare Updates** wird aktualisiert

Sie können auch eine Update-Prüfung für einzelne Komponenten mithilfe der Aktion **Auf Updates prüfen** aus dem Aktionen-Menü der Liste auslösen.

## Updates installieren

### Einzelne Komponente aktualisieren

1. Navigieren Sie zu **Erweiterungen > Komponenten-Register**
2. Finden Sie die Komponente, die Sie aktualisieren möchten — Komponenten mit verfügbaren Updates zeigen einen Update-Indikator neben ihrer Version an
3. Klicken Sie auf die Schaltfläche **Update installieren** in der Zeile dieser Komponente
4. Bestätigen Sie das Update, wenn Sie aufgefordert werden
5. Das Update wird heruntergeladen, überprüft und installiert — ein Fortschrittsindikator zeigt jeden Schritt an
6. Nach Abschluss wird die **Aktuelle Version** der Komponente auf die neue Versionsnummer aktualisiert

### Mehrere Komponenten aktualisieren

1.

Markieren Sie die Kontrollkästchen neben den Komponenten, die Sie aktualisieren möchten
2.



Wählen Sie **Updates installieren** im **Aktion**-Dropdownmenü aus
3.

Klicken Sie auf **Weiter**, um fortzufahren
4.

Updates werden in Abhängigkeitsreihenfolge installiert — Komponenten, auf die andere Komponenten angewiesen sind, werden zuerst aktualisiert

### Was während eines Updates passiert

Der Updatevorgang läuft in folgenden Schritten ab:

1. **Überprüfen** — bestätigt, dass das Update verfügbar ist und Ihre Lizenz gültig ist
2. **Herunterladen** — lädt das Paket vom Spwig-Update-Server herunter
3. **Überprüfen** — prüft die Integrität des Pakets anhand eines SHA-256-Prüfsummenwerts
4. **Entpacken** — entpackt die neuen Dateien
5. **Bereitstellen** — aktiviert die neue Version
6. **Gesundheitsprüfung** — überprüft, ob die Komponente nach dem Update funktioniert

Falls ein Schritt fehlschlägt, versucht das System automatisch, die vorherige Version wiederherzustellen.

## Plattformweite Updates

Zusätzlich zu einzelnen Komponenten kann Spwig auch plattformweite Updates empfangen, die den Kern des Shops aktualisieren. Diese Updates durchlaufen einen umfassenderen Prozess, einschließlich Datenbankmigrationen und einer kurzen Wartungszeit.

Die Historie der Plattformupdates ist im Abschnitt **Plattformupdates** im Registry sichtbar. Jeder Eintrag zeigt die Versionsumschaltung (z. B. `v1.3.2 → v1.3.3`), den Status und die Dauer des Updatevorgangs an.

Sicherheitsupdates werden separat markiert und werden, wenn **Automatische Installation von Sicherheitsupdates** in der Update-Server-Konfiguration aktiviert ist, automatisch installiert, ohne manuelle Aktion zu erfordern.

## Versionshistorie ansehen

Um alle zuvor installierten Versionen einer Komponente anzuzeigen:

1. Klicken Sie auf den Namen der Komponente, um ihre Detailansicht zu öffnen
2. Scrollen Sie zu dem Abschnitt **Komponentenversionen** am unteren Ende der Seite
3. Jeder Versionseintrag zeigt die Versionsnummer, den Installationszeitpunkt, die Installationsmethode und den Gesundheitsstatus an

Das System behält die letzten drei installierten Versionen für eine Rückverfolgung bereit. Versionen darüber hinaus werden automatisch gelöscht.

## Eine Komponente zurückrollen

Falls ein Update Probleme verursacht, können Sie zu einer früheren Version zurückkehren:

1. Öffnen Sie die Detailansicht der Komponente
2. Scrollen Sie zu dem Abschnitt **Zurückrollen**
3. Wählen Sie die Version aus, die Sie wiederherstellen möchten
4. Klicken Sie auf **Zurückrollen zu dieser Version**

Nur Versionen, die mit **Zurückrollen möglich** markiert sind, können wiederhergestellt werden. Der Eintrag im Rückroll-Log protokolliert, wer die Rückverfolgung initiiert hat und wann.

## Komponenten sperren

Das Sperren einer Komponente verhindert, dass Updates installiert werden, einschließlich automatischer Updates. Dies ist nützlich, wenn Sie Anpassungen oder Integrationen haben, die von einer bestimmten Version abhängen.

1. Öffnen Sie die Detailansicht der Komponente
2. Aktivieren Sie das **Gesperrt**-Kästchen im Abschnitt **Sperren und Einfrieren**
3. Geben Sie einen Grund in **Sperfgrund** ein, damit Ihr Team weiß, warum sie gesperrt ist
4. Speichern Sie den Eintrag

Gesperrte Komponenten werden im Registry-Liste mit einem Schloss-Indikator angezeigt. Um sie zu entsperren, deaktivieren Sie **Gesperrt** und speichern Sie den Eintrag.

## Update-Protokolle einsehen

Das Update-Protokoll protokolliert jede Installation, Aktualisierung, Rückverfolgung und Gesundheitsprüfung:

1. Öffnen Sie die Detailansicht einer Komponente
2. Die **Update-Protokolle** sind inline am unteren Ende der Seite sichtbar
3. Jeder Eintrag zeigt an: die durchgeführte Aktion, Start- und Endzeit, alte und neue Versionen, ob es automatisch oder manuell war, und ggf. Fehlermeldungen, wenn der Vorgang fehlgeschlagen ist

Protokolleinträge mit dem Status **Fehlgeschlagen** enthalten die vollständige Fehlermeldung, um bei der Problembehebung zu helfen.

## Automatische Updates aktivieren

Sie können Spwig erlauben, Updates automatisch zu installieren, sobald sie verfügbar sind:

1. Öffnen Sie die Detailansicht der Komponente
2. Aktivieren Sie **Automatische Aktualisierung** im Abschnitt **Version und Update-Status**
3. Speichern Sie den Eintrag

Wenn automatische Aktualisierung aktiviert ist, installiert das System Updates während des nächsten geplanten Prüfzyklus. Sicherheitsupdates folgen der globalen Einstellung **Automatische Installation von Sicherheitsupdates**, unabhängig von den Einstellungen einzelner Komponenten.

## Tipps

Behalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe bei.

- Aktualisieren Sie sich immer über den **Stabilen** Kanal für Themes und Zahlungsdienstleister — dies sind die am häufigsten genutzten Komponenten, und Stabilität ist am wichtigsten
- Schließen Sie eine Komponente vor der Durchführung von benutzerdefinierten Änderungen ab, und dokumentieren Sie den Grund klar, damit zukünftige Teammitglieder wissen, warum sie nicht aktualisiert werden sollte
- Prüfen Sie die **Release Notes** im Versionsverzeichnis der Komponente, bevor Sie eine große Versionserhöhung installieren — dort werden Bruchänderungen markiert
- Nach einer Aktualisierung navigieren Sie zu dem betroffenen Bereich Ihres Shops, um sicherzustellen, dass alles wie erwartet aussieht und funktioniert, bevor Sie die Aktualisierung als abgeschlossen erklären
- Wenn bei einer Komponente die automatische Aktualisierung aktiviert ist, überprüfen Sie die **Update Logs** regelmäßig, um sicherzustellen, dass die automatischen Updates erfolgreich abgeschlossen werden