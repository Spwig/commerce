---
title: Einstellungen-Synchronisation
---

Die Einstellungen-Synchronisation ermöglicht es Ihnen, die Store-Konfiguration zwischen zwei Spwig-Installationen zu kopieren. Dies ist ideal, um Staging- und Produktionsumgebungen zu verwalten, bei denen Sie Änderungen auf dem Staging-Server konfigurieren und testen, bevor Sie sie auf Ihrem Live-Store bereitstellen.

## Wann Sie die Einstellungen-Synchronisation verwenden sollten

- **Staging zu Produktion**: Konfigurieren Sie Einstellungen auf Ihrem Staging-Store und推送 sie dann in die Produktion
- **Produktion zu Staging**: Ziehen Sie Produktionseinstellungen in das Staging, um mit einer übereinstimmenden Umgebung zu beginnen
- **Backup-Konfiguration**: Ziehen Sie Einstellungen aus der Produktion in eine Backup-Instanz als Schutzmaßnahme

Die Einstellungen-Synchronisation verarbeitet nur Konfigurationsdaten – sie überträgt keine Produkte, Kunden, Bestellungen oder Mediendateien. Für eine vollständige Datentransfer verwenden Sie stattdessen die Vollständige Systemmigration.

## Was synchronisiert werden kann

Die Einstellungen-Synchronisation unterstützt die folgenden Kategorien:

| Gruppe | Kategorien |
|-------|-----------|
| **Einstellungen** | Site-Einstellungen, Steuern & Währung, Steuersätze, Sprachen, Blog-Einstellungen, Soziale Teilen, Verkaufsregionen & Lager, Suchkonfiguration, Benutzerdefinierte Felder, Mitarbeiterrollen, Kundeanalyse |
| **Design** | Design & Theme, Kopf-/Fußzeilen/Navigation |
| **Anbieter** | E-Mail, SMS/WhatsApp, Zahlungsanbieter, Versand, SEO-Anbieter, Produktfeeds, Blog-Sozialverknüpfungen, POS-Konfiguration |
| **Inhalt** | Seiten & Vorlagen, Blogbeiträge, Bekanntmachungen, Formulare, Produktkollektionen |
| **Handel** | Handelregeln (Gutscheine, Promotionen, Treueprogramme, Abonnements), Affiliate-Programm, Webhooks & Integrationen |

> **Hinweis:** Kategorien, die Anmeldeinformationen enthalten (Zahlungsanbieter, Versandkonten usw.), sind mit einem Schlüsselicon markiert. API-Schlüssel und -geheimnisse werden sicher übertragen, können aber für OAuth-basierte Integrationen erneut eingegeben werden müssen.

## Schritt-für-Schritt-Anleitung

### Schritt 1: Eine Verbindung einrichten

1. Navigieren Sie im Admin- Seitenleiste zu **Datenmigration > Spwig-zu-Spwig-Synchronisation**
2. Klicken Sie auf **Einstellungen-Synchronisation starten**
3. Wählen Sie eine gespeicherte Verbindung aus oder erstellen Sie eine neue:
   - Geben Sie die URL des Remote-Stores ein (z. B. `https://staging.yourstore.com`)
   - Fügen Sie den auf dem Remote-Store generierten Sync-Token ein
   - Geben Sie der Verbindung einen beschreibenden Namen
   - Legen Sie die Rolle fest (Staging, Produktion, Backup oder Andere)
4. Klicken Sie auf **Verbindung testen**, um sicherzustellen, dass sie funktioniert
5. Klicken Sie auf **Weiter**, um fortzufahren

### Schritt 2: Kategorien und Richtung auswählen

**Richtung:**
- **Ziehen** – Kopiert Einstellungen von der verbundenen Store in diesen Store
- **Pushen** – Kopiert Einstellungen von diesem Store in die verbundene Store

**Synchronisationsmodus:**
- **Hinzufügen & Aktualisieren** – Fügt neue Elemente hinzu und aktualisiert vorhandene, löscht aber nichts. Dies ist die sicherste Option.
- **Exakter Kopie** – Macht das Ziel exakt dem Quell entsprechen, einschließlich der Entfernung von Elementen, die auf dem Ziel, aber nicht auf der Quelle vorhanden sind. Verwenden Sie dies vorsichtig.

Wählen Sie die Kategorien aus, die Sie einbeziehen möchten, und klicken Sie auf **Weiter**.

### Schritt 3: Änderungen vorab ansehen

Bevor Änderungen angewendet werden, sehen Sie eine detaillierte Vorschau, die genau zeigt, was für jede Kategorie hinzugefügt, geändert oder entfernt wird. Prüfen Sie dies sorgfältig.

Wenn Sie auf eine Produktion-Verbindung pushen, müssen Sie bestätigen, dass Sie verstehen, dass die Änderungen Ihren Live-Store beeinflussen werden.

Klicken Sie auf **Synchronisation starten**, wenn Sie bereit sind.

### Schritt 4: Fortschritt überwachen

Die Synchronisation läuft im Hintergrund. Sie können sicher von der Fortschrittsseite abweichen – die Synchronisation wird weiterlaufen.

Die Fortschrittsseite zeigt:
- Gesamtabschlussprozent mit geschätzter verbleibender Zeit
- Fortschritt pro Kategorie mit Erfolgs-/Fehlerzahlen
- Ein Live-Aktivitätsprotokoll, das Sie erweitern können, um detaillierte Ausgaben anzuzeigen

## Rückverfolgung

Nachdem eine Synchronisation abgeschlossen ist, haben Sie **24 Stunden**, um die Änderungen rückgängig zu machen. Eine Rückverfolgung stellt den vorherigen Zustand aller betroffenen Einstellungen wieder her.

Um eine Rückverfolgung durchzuführen:
1. Gehen Sie zu **Synchronisationsdashboard**
2. Finden Sie den abgeschlossenen Auftrag
3. Klicken Sie auf **Rückverfolgung** und bestätigen Sie

Nach 24 Stunden läuft die Rückverfolgungsoption ab und die Änderungen werden dauerhaft.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Auf der Staging-Umgebung testen**:

Stellen Sie sich zunächst auf eine Staging-Umgebung synchron, um die Ergebnisse zu überprüfen, bevor Sie sie in die Produktion übertragen.

- **Add & Update-Modus verwenden**:

Dies ist der sicherste Modus, da er keine bestehenden Daten löscht.

- **Die Vorschau sorgfältig prüfen**:

Die Diff-Vorschau zeigt Ihnen genau an, was sich ändern wird, bevor etwas angewendet wird.

- **Produktionsverbindungen zeigen Warnungen an**:

Wenn Sie auf eine Verbindung, die als Produktion markiert ist, übertragen, sind zusätzliche Sicherheitsbestätigungen erforderlich.