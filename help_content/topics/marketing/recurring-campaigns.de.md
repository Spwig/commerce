---
title: Wiederkehrende Kampagnen
---

Die **wiederkehrenden Kampagnen** von Campaign Studio ermöglichen es Ihnen, eine Newsletter-Kampagne einmal zu erstellen – eine wöchentliche Produktzusammenfassung, ein monatlicher Blog-Überblick – und sie dann automatisch nach einem wiederverwendbaren Zeitplan senden zu lassen, anstatt bei jeder Gelegenheit manuell eine neue Kampagne zu erstellen und zu senden.

## Broadcast vs. wiederkehrend

Jede Kampagne in Campaign Studio hat einen **Kampagnentyp**:

| Typ | Verhalten |
|------|-----------|
| **Broadcast** | Wird einmal gesendet – sofort oder an einem bestimmten geplanten Datum und Uhrzeit. Verwenden Sie dies für eine Einzelankündigung, einen Verkauf oder eine Produktveröffentlichung per E-Mail. |
| **Wiederkehrend** | Funktioniert als Vorlage, die nach einem wiederverwendbaren Zeitplan gesendet wird. Jeder Sendevorgang ist eine frische, datierte Kopie, die als **Vorkommnis** bezeichnet wird – die Vorlage sendet sich selbst niemals direkt. |

Um eine Kampagne in eine wiederkehrende zu verwandeln, öffnen Sie sie in **Campaign Studio > Kampagnen** und setzen Sie den **Kampagnentyp** auf **Wiederkehrend**, und speichern Sie dann. Sobald Sie die Kampagne erneut öffnen, erscheint eine **Zeitplan-Sektion** – sie wird nur für wiederkehrende Kampagnen angezeigt.

![Kampagnentyp auf Wiederkehrend eingestellt](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Einrichten eines Zeitplans

Sobald eine Kampagne wiederkehrend ist, steuert ihre **Zeitplan-Sektion**, wann sie ausgelöst wird:

| Feld | Beschreibung |
|-------|-------------|
| **Aktiv** | Schaltet die Wiederholung ein oder aus, ohne den Zeitplan zu löschen. |
| **Intervall** | **Täglich**, **Wöchentlich** oder **Monatlich**. |
| **Abstand** | Sendet alle N Intervalleinheiten – z. B. ein Abstand von `2` bei wöchentlichem Intervall bedeutet alle 2 Wochen. |
| **Wochentag** | Welcher Tag zum Senden bei wöchentlichem Intervall (0 = Montag … 6 = Sonntag). |
| **Tag des Monats** | Welcher Tag zum Senden bei monatlichem Intervall (1–28, damit jeder Monat diesen Tag hat). |
| **Sendezeit** | Die Uhrzeit, zu der die Kampagne versendet wird. |
| **Zeitzone** | Ein IANA-Zeitzonennamen, z. B. `Europe/London` oder `America/New_York` – die Sendezeit wird in dieser Zone interpretiert, nicht in der des Servers. |

![Wöchentlicher Zeitplan in einer wiederkehrenden Kampagne](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Sobald Sie einen aktiven Zeitplan speichern, **aktiviert er sich selbst** – Spwig berechnet den nächsten Auslösezeitpunkt und zeigt ihn in **Nächster Lauf um** an. Sie müssen nichts manuell auslösen; eine Hintergrundaufgabe prüft, ob Zeitpläne fällig sind, und sendet das Vorkommnis, sobald die Zeit gekommen ist. **Letzter Lauf um** und **Vorkommnisse gesendet** werden automatisch aktualisiert, damit Sie sehen können, dass der Zeitplan aktiv ist.

## Das Kein-Neue-Inhalte-Richtlinie

Wiederkehrende Newsletter enthalten oft dynamische Inhalte – am häufigsten ein **Blog-Beiträge**-Block (oder ein **Produktgitter**), der im visuellen Editor auf **Neu seit letztem Senden** eingestellt ist, der nur Beiträge anzeigt, die seit der letzten Sendung des Kampagnenverlaufs veröffentlicht wurden – oder Produkte hinzugefügt wurden. Das wirft eine offensichtliche Frage auf: Was passiert, wenn ein geplanter Durchlauf eintrifft und es nichts Neues zu präsentieren gibt?

Spwig beantwortet diese Frage mit der **Kein-Neue-Inhalte-Richtlinie** des Zeitplans:

| Richtlinie | Was passiert | Am besten geeignet für |
|--------|---------------|----------|
| **Diesen Versand überspringen** *(Standard)* | Der Lauf wird vollständig übersprungen — es wird nichts versendet. Der Zeitplan geht direkt zum nächsten geplanten Lauf über. | Ein Blog- oder Produkt-Newsletter, damit Abonnenten nie eine E-Mail erhalten, die nur das wiederholt, was sie bereits gesehen haben. |
| **Trotzdem senden (leere Blöcke weglassen)** | Die E-Mail wird planmäßig gesendet, unabhängig von den Umständen. Jeder Block, der nichts Neues enthält — wie ein leerer „Neu seit letztem Versand“-Blog-Beiträge-Block — rendert an dieser Stelle einfach nichts. | Newsletter, die immer andere Inhalte zum Senden haben (eine Willkommensnachricht, Evergreen-Bereiche oder mehrere dynamische Blöcke), selbst wenn ein Block leer bleibt. |
| **Zurückhalten und verspätet senden** | Der Versand wird verschoben. Spwig prüft täglich erneut auf neue Inhalte, bis zum **Haltefenster (Tage)**. Wenn innerhalb dieses Fensters neue Inhalte erscheinen, wird der Lauf verspätet gesendet; wenn das Fenster ohne neue Inhalte abläuft, wird dieser Lauf aufgegeben und der Zeitplan geht zum nächsten Slot über. | Ein Rhythmus, den Sie schützen möchten (z. B. immer *etwas* irgendwann senden), ohne eine leere Ausgabe auszulösen, nur weil in dieser Woche nichts Neues veröffentlicht wurde. |

Nur Kampagnen mit delta-bewussten Inhalten — ein Blog-Beiträge-Block oder ein Produkt-Raster, das auf **Neu seit letztem Versand** eingestellt ist — lösen diese Prüfung aus. Eine wiederkehrende Kampagne ohne solche Blöcke wird immer als frisch betrachtet und planmäßig normal gesendet.

**Haltefenster (Tage)** gilt nur für die **Zurückhalten und verspätet senden**-Richtlinie — es legt fest, wie viele Tage Spwig erneut versucht, bevor es diesen Lauf aufgibt.

## A/B-Testierung jedes Laufs

Ein wiederkehrender Newsletter ist ein natürlicher Ort, um Ihre **Betreffzeilen** A/B zu testen — Sie senden in einem regelmäßigen Rhythmus an dasselbe Publikum, sodass Sie weiterhin lernen können, welche Formulierung mehr Öffnungen erzielt. Spwig kann automatisch einen neuen Betreffzeilen-A/B-Test für **jeden Lauf** durchführen.

Richten Sie dies im Bereich **Zeitplan** ein:

1. Geben Sie unter **A/B-Betreffzeilen** **zwei bis vier** Betreffzeilen ein, eine pro Zeile. Lassen Sie das Feld leer, um die Läufe normal mit dem eigenen Betreff der Vorlage zu senden.
2. Stellen Sie den **A/B-Test-Stichprobenanteil (%)** ein — den Anteil des Publikums jedes Laufs, der zum Testen verwendet wird, gleichmäßig auf die Betreffzeilen aufgeteilt. Der Rest ist die Haltegruppe, die den Gewinner erhält.
3. Wählen Sie die **A/B-Gewinner-Metrik** (Öffnungs- oder Klickrate), das **A/B-Testfenster (Stunden)**, um Ergebnisse zu sammeln, bevor entschieden wird, und ob der **Gewinner automatisch an die Haltegruppe gesendet** werden soll.

Ab dann teilt jeder Lauf, wenn der Zeitplan ausgelöst wird, sein Publikum auf, sendet jede Betreffzeile an einen Ausschnitt, wartet das Testfenster ab und wählt dann die gewinnende Betreffzeile aus und sendet sie an alle anderen — ohne weitere Aktion von Ihnen. Jeder Lauf ist ein eigenständiger Test, sodass Sie bei jedem Versand eine neue Einschätzung erhalten und beobachten können, welche Betreffzeilen über die Wochen gewinnen. Das Ergebnis jedes Laufs wird unter **Laufverlauf** unten angezeigt und verlinkt direkt zu seiner Ergebnisseite mit den Raten pro Variante, dem Gewinner und wie sicher Spwig ist (siehe [A/B-Testierung](ab-testing), um zu erfahren, wie man diese Ergebnisse liest).

Zwei Dinge, die es zu wissen gilt:

- **A/B-Testierung hier betrifft nur Betreffzeilen.** Um völlig unterschiedliche Designs zu vergleichen, verwenden Sie einen einmaligen Broadcast-A/B-Test — der vollständige Assistent, der Inhaltsvarianten unterstützt, ist für Broadcast-Kampagnen.
- Wenn das Publikum eines Laufs **zu klein zum Aufteilen** auf die Varianten ist, sendet Spwig diesen Lauf stattdessen still als normalen Newsletter — eine schmale Woche bedeutet nie einen verpassten Versand.

## Laufverlauf

Jedes Mal, wenn eine wiederkehrende Kampagne tatsächlich sendet, erstellt Spwig einen datierten **Lauf** — einen echten, unabhängigen Kampagnenaufzeichnung mit eigenem Betreff, Empfängern und Versandstatistiken (gesendet, fehlgeschlagen, übersprungen, Öffnungen, Klicks). Der Lauf wird nach der Vorlage benannt, mit dem Versanddatum angehängt, z. B. „Wöchentlicher Blog-Newsletter — 2026-08-19“.

Die Bearbeitungsseite der wiederkehrenden Kampagne listet den **Vorkommensverlauf** auf — die jüngsten Vorkommnisse, von denen jedes zu dem eigenen Kampagneneintrag dieses Vorkommnisses verlinkt, sodass Sie genau überprüfen können, was gesendet wurde und wie es abgeschnitten hat.

![Vorkommensverlauf in einer wiederkehrenden Kampagne](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Tipps

- Kombinieren Sie eine wiederkehrende Kampagne mit einem **Blog-Beiträge**-Block, der auf **Neu seit letztem Versand** eingestellt ist, für einen selbstverwalteten „Neue Beiträge diese Woche“-Newsletter — Sie schreiben die Beiträge, Spwig übernimmt das Versenden der E-Mails.
- Beginnen Sie bei Inhalts-Newslettern mit **Diesen Versand überspringen**. Dies ist die sicherste Standardeinstellung: Abonnenten erhalten nie eine Wiederholung des Inhalts vom letzten Mal.
- Wechseln Sie nur zu **Trotzdem senden**, wenn Ihre Vorlage andere Inhalte enthält, die für sich allein einen Versand wert sind, selbst wenn der dynamische Block leer ist.
- Verwenden Sie **Zurückhalten und verspätet senden**, wenn es in Ordnung ist, den Rhythmus gelegentlich zu verfehlen, aber nicht, wenn Sie ihn wochenlang in Folge verfehlen — stellen Sie das Haltefenster so ein, wie lange eine Lücke für Sie akzeptabel ist.
- Prüfen Sie **Nächster Lauf am** nach dem Speichern eines Zeitplans, um sicherzustellen, dass er auf den erwarteten Tag und die erwartete Uhrzeit fällt, insbesondere bei der Arbeit über Zeitzonen hinweg.
- Prüfen Sie den **Vorkommensverlauf** regelmäßig — eine Vorlage, die ständig übersprungen wird, ist ein Zeichen dafür, dass Ihre dynamische Inhaltsquelle (z. B. der Blog) still ist.