---
title: A/B-Tests
---

Mit der **A/B-Test**-Funktion von Campaign Studio können Sie zwei bis vier **Varianten** – verschiedene Versionen derselben Kampagne – an einem Teil Ihrer Zielgruppe testen, bevor Sie die vollständige Sendung durchführen. Ändern Sie nur den Betreff oder gestalten Sie für jede Variante völlig unterschiedliche Inhalte. Spwig teilt eine Stichprobe Ihrer Liste gleichmäßig auf die Varianten auf, beobachtet die Leistung jeder Variante und sendet automatisch die am besten performende Variante an alle, die den Test nicht gesehen haben.

## Test einrichten

Erstellen Sie Ihre Kampagne zunächst wie gewohnt im visuellen Builder von Campaign Studio – schreiben Sie einen Betreff, gestalten Sie Ihre Inhalte und wählen Sie das **Segment**, das Sie erreichen möchten. Diese Kampagne wird zum **Container** des Tests. Sobald Sie einen A/B-Test daran anhängen, wird der Container selbst nie direkt gesendet – seine Aufgabe ist es, die Einstellungen zu halten, und die Zielgruppe, die er erreichen soll, ist genau der Pool, gegen den der Test läuft.

An zwei Stellen wird der A/B-Test-Assistent geöffnet:

- Der **A/B-Test**-Button in der Symbolleiste des visuellen Builders.
- Das **A/B-Test**-Symbol auf der Kampagnenkarte in **Campaign Studio > Kampagnen**.

Sobald ein Test auf einer Kampagne existiert, führt derselbe Button Sie direkt zu den Ergebnissen statt zum Assistenten, und die Kampagnenkarte erhält ein kleines **A/B**-Abzeichen, damit Sie sie in der Liste auf einen Blick erkennen können.

## Was testen?

Der erste Schritt des Assistenten fragt, was zwischen den Varianten unterschiedlich sein soll:

| Option | Was sich ändert | Gemessen durch |
|--------|--------------|-------------|
| **Betreffzeile** | Jede Variante sendet exakt denselben Inhalt – nur die Betreffzeile unterscheidet sich. Der häufigste Test. | Öffnungsrate |
| **Inhalt** | Jede Variante ist ein separates Design, das Sie selbst im visuellen Builder erstellen. | Klickrate |

![Der Schritt "Was möchten Sie testen?", mit ausgewählter Betreffzeile](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Varianten auswählen

Was Sie als Nächstes eingeben, hängt davon ab, was Sie ausgewählt haben:

- **Betreffzeile** – Geben Sie für jede Variante (2–4) einen Betreff ein. Es werden zunächst zwei Zeilen angezeigt; klicken Sie auf **Weitere Betreffzeile hinzufügen** für eine dritte oder vierte.
- **Inhalt** – Wählen Sie einfach, wie viele Varianten Sie möchten (2–4). Jede Variante beginnt als exakte Kopie des aktuellen Designs Ihres Containers, sodass Sie nur das ändern müssen, was Sie testen.

In beiden Fällen beschriftet Spwig die Varianten in der Reihenfolge, in der Sie sie eingeben, mit **A**, **B**, **C** und **D** – Sie sehen sie ab hier als "Variante A", "Variante B" usw.

![Der Varianten-Schritt mit drei Betreffzeilen für die Varianten A, B und C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Für einen Inhaltstest gestalten Sie die Varianten nicht im Assistenten selbst – nachdem Sie den Test erstellt haben, erhält die Karte jeder Variante im Ergebnis-Hub ein kleines Stift-Symbol, das sie im selben visuellen Builder öffnet, den Sie für den Container verwendet haben. Dies ist nur verfügbar, während der Test noch im **Entwurf** ist; sobald Sie den Test starten, sind die Designs gesperrt, damit sich das, was Sie messen, während des Tests nicht ändert.

## Testeinstellungen

Der letzte Schritt des Assistenten behandelt, wie der Test durchgeführt und entschieden wird:

| Einstellung | Was sie bewirkt |
|---------|--------------|
| **Teststichprobe** | Der Anteil Ihrer Zielgruppe, der für den Test verwendet wird, gleichmäßig auf die Varianten aufgeteilt: 20 %, 30 %, 50 % oder 100 %. Der Rest – die **Haltegruppe** – erhält anschließend den Gewinner. Die Auswahl von 100 % testet Ihre gesamte Liste auf einmal, sodass keine Haltegruppe übrig ist, an die ein Gewinner gesendet werden kann. |
| **Gewinner bestimmt durch** | **Öffnungsrate** oder **Klickrate**. Standardmäßig Öffnungsrate für einen Betreffzeilentest und Klickrate für einen Inhaltstest, da dies das ist, was jeweils tatsächlich gemessen wird – aber Sie können es in beide Richtungen ändern. |
| **Testzeitraum (Stunden)** | Wie lange Öffnungen und Klicks gesammelt werden, bevor ein Gewinner ausgewählt wird, von 1 bis 168 Stunden (eine volle Woche). |
| **Gewinner automatisch an den Rest der Zielgruppe senden** | Standardmäßig aktiviert. Wenn aktiviert, sendet Spwig die gewinnende Variante an die Haltegruppe, sobald der Zeitraum endet, ohne weitere Aktion von Ihnen. |

Eine kurze Übersichtskarte am unteren Rand fasst Ihre Auswahl zusammen, bevor Sie bestätigen.

![Der Einstellungsschritt mit festgelegten Optionen für Stichprobe, Metrik, Zeitfenster und automatisches Senden sowie einer Übersichtskarte](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Test starten

Klicken Sie auf **Test erstellen**, um die Einrichtung zu speichern – es wird noch nichts gesendet. Sie gelangen zum Ergebnis-Hub des Tests im Status **Entwurf**, in dem jede Variante mit bisher null Empfängern angezeigt wird sowie zwei Schaltflächen: **Test starten** und **Test abbrechen**.

![Ein gerade erstellter Test im Status Entwurf, der drei Varianten zum Start zeigt](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Klicken Sie auf **Test starten**, wenn Sie bereit sind. Spwig verteilt Ihre Teststichprobe gleichmäßig auf die Varianten und sendet jede sofort per E-Mail – Sie müssen nichts weiter tun; ein Hintergrundjob prüft nach Ablauf des Testzeitfensters und bestimmt den Gewinner automatisch. Der Status der Container-Kampagne bleibt währenddessen **Entwurf** – das ist erwartet, da die Varianten (und später der Gewinner) tatsächlich versendet werden, nie der Container.

Ihr Publikum muss groß genug sein, damit jede Variante eine sinnvolle Anzahl von Empfängern erhält. Spwig blockiert das Starten eines Tests, wenn eine Variante auf null Personen käme, aber ein wirklich aussagekräftiger Test braucht mehr als das Mindestmaß – zielen Sie auf einige hundert Empfänger oder mehr, bevor Sie sich auf das Ergebnis verlassen.

## Während des Testlaufs

Sobald gestartet, wechselt der Hub in den Status **Testlauf** und zeigt „Test läuft – der Gewinner wird automatisch um“ Datum und Uhrzeit des Fenstersendes bestimmt. Empfängerzahlen und Live-Öffnungs-/Klickraten aktualisieren sich bei jedem Besuch, zusammen mit einem Balkendiagramm, das die Öffnungs- und Klickrate jeder Variante nebeneinander vergleicht – nicht nur die Metrik, die Sie zur Gewinnerbestimmung gewählt haben.

![Ein laufender Test mit Live-Empfängerzahlen, Öffnungs-/Klickraten und einem Vergleichsdiagramm](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Sie können auch jeden Test vom **Kampagnen-Studio-Dashboard** aus im Auge behalten: Das Panel *Letzte A/B-Tests* listet Ihre laufenden und kürzlich entschiedenen Tests auf – jeweils mit einem Blick auf das Konfidenzniveau – und verlinkt direkt zu den Ergebnissen, neben Karten, die anzeigen, wie viele Tests laufen und wie viele in den letzten 30 Tagen entschieden wurden.

## Ergebnisse lesen

Wenn das Testzeitfenster endet, wählt Spwig die Variante mit der höchsten Rate auf Ihrer gewählten Metrik, markiert den Test als **Abgeschlossen** und – wenn **Gewinner automatisch senden** aktiviert war und es eine Haltegruppe zum Senden gibt – sendet diese Variante an alle, die nicht Teil des Tests waren. Die Karte der Gewinnervariante ist umrandet und trägt ein **Gewinner**-Abzeichen; das Vergleichsdiagramm bleibt an Ort und Stelle, damit Sie sehen können, wie sich die Varianten verglichen haben.

![Ein abgeschlossener Test mit hervorgehobener Gewinnervariante und Gewinner-Abzeichen](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Beachten Sie, dass die Zahlen auf dieser Seite immer für die Teststichprobe gelten, nicht für Ihre gesamte Liste – bei einer 20%-Stichprobe lesen Sie, wie ein Fünftel Ihres Publikums reagiert hat, nicht alle.

## Wie sicher ist das Ergebnis?

Eine höhere Öffnungs- oder Klickrate bedeutet nicht immer, dass eine Variante tatsächlich besser ist – bei einem kleinen Publikum kann eine Variante rein zufällig vorne liegen. Deshalb zeigt Spwig neben dem Gewinner an, **wie sicher es ist, dass das Ergebnis real ist**, basierend auf der Größe des Unterschieds und der Anzahl der Empfänger. Sie sehen eine von drei Bewertungen:

- **Ein klares Ergebnis** – Spwig ist zu mindestens 95 % sicher, dass die führende Variante die anderen tatsächlich schlägt. Dies ist ein Ergebnis, auf das Sie handeln können.
- **Zu knapp, um zu sagen** – es gibt einen Führenden, aber der Unterschied ist klein genug, dass es Zufall sein könnte. Der angezeigte Prozentsatz gibt an, wie sicher Spwig ist, unter der 95%-Marke. Erwägen Sie, mit einem größeren Publikum oder einem längeren Testzeitfenster erneut durchzuführen, bevor Sie Schlussfolgerungen ziehen.
- **Noch nicht genug Daten** – zu wenige Empfänger (oder zu wenige Öffnungen und Klicks), um die Varianten überhaupt unterscheiden zu können. Dies ist bei kleinen Listen üblich; vergrößern Sie das Publikum oder lassen Sie den Test länger laufen.

![Ein abgeschlossener Test mit einem klaren Ergebnis — die siegreiche Variante trägt ein Konfidenzbadge und die Zusammenfassung lautet "statistisch klar"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

Dieselbe Anzeige erscheint auch, während ein Test noch läuft, sodass Sie beobachten können, wie sich ein Ergebnis festigt — oder auch nicht — bevor das Zeitfenster schließt. Da die Konfidenz stark von der Größe des Publikums abhängt, ist dies der praktische Grund, pro Test auf einige hundert oder mehr Empfänger zu zielen: Auf einer sehr kleinen Liste wird selbst ein großer Unterschied in der Regel als "zu knapp, um zu entscheiden" eingeordnet.

Beachten Sie, dass Spwig bei aktiviertem automatischem Versand die Variante mit der höchsten Rate an den Rest Ihres Publikums sendet, selbst wenn das Ergebnis unentschieden ist — die Konfidenzanzeige dient dazu, Ihnen mitzuteilen, wie viel Sie dem Ergebnis vertrauen können, und nicht dazu, den Versand aufzuhalten.

## Test abbrechen

**Test abbrechen** ist verfügbar, während ein Test im Status **Entwurf** oder **Testlauf** ist, und stoppt ihn, ohne dass jemals ein Gewinner versendet wird. Diese Option ist für Fälle vorgesehen, in denen Sie Ihre Meinung geändert oder einen Fehler bei der Einrichtung gemacht haben — sie sollte nicht leichtfertig verwendet werden, da es nach dem Abbrechen eines Tests (oder nach dessen normalem Abschluss) keinen Button gibt, um auf derselben Kampagne einen neuen Test einzurichten. Wenn Sie später einen weiteren Vergleich durchführen möchten, erstellen Sie dafür eine neue Kampagne.

## Tipps

- Beginnen Sie mit einem **Betreffzeile**-Test — er ist am einfachsten einzurichten und der häufigste Grund, überhaupt einen A/B-Test durchzuführen.
- Verwenden Sie einen **Inhalt**-Test, wenn Sie grundlegend unterschiedliche Designs oder Angebote vergleichen möchten, nicht nur die Wortwahl im Betreff.
- Beenden Sie das Designen jeder Variante eines Inhalts-Tests — mit dem Stift-Symbol auf jeder Karte — bevor Sie auf **Test starten** klicken. Sie können das Design einer Variante nicht mehr bearbeiten, sobald der Test läuft.
- Lassen Sie die **Teststichprobe** unter 100 %, wenn Sie möchten, dass Spwig den Gewinner anschließend automatisch an den Rest Ihrer Liste per E-Mail versendet — bei 100 % bleibt kein Rückhalt zurück, an den er gesendet werden könnte.

- Stellen Sie sicher, dass das Testzeitfenster genug Zeit hat, um die normalen Lesezeiten Ihrer Abonnenten abzudecken (24 Stunden decken bequem einen vollen Tag über verschiedene Zeitzonen und Postfächer ab), anstatt einen Gewinner nur anhand der ersten ein oder zwei Stunden zu bestimmen.