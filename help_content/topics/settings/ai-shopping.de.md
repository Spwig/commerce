---
title: KI-Einkauf
---

KI-Einkauf ermöglicht es KI-Einkaufsassistenten, Ihre Produkte zu finden, und, wenn Sie es erlauben, von Ihrem Geschäft für den Kunden zu kaufen. Es ist **standardmäßig deaktiviert** – das Aktivieren ist eine bewusste Wahl, und solange Sie es nicht tun, gibt es nichts, was Ihr Geschäft diesen Assistenten gegenüber offenlegt.

## Aktivieren

Öffnen Sie **Einstellungen → KI-Einkauf** und schalten Sie **Agenterhandel aktiviert** ein. Ab diesem Zeitpunkt können Assistenten, die das Universal Commerce Protocol unterstützen, Ihr Geschäft entdecken und Ihre Katalogdatei lesen. Nichts an Ihrem normalen Geschäftsbereich ändert sich.

## Der Bereitschafts-Check

Oben auf der Seite KI-Einkauf beantwortet eine einzige Satz eine Frage: **Können KI-Assistenten Ihr Geschäft gerade direkt kaufen?**

- **"KI-Assistenten können bei Ihrem Geschäft einkaufen"** – alles, was für einen Kauf benötigt wird, ist vorhanden.
- **"KI-Assistenten können Ihr Geschäft durchsuchen, aber noch nicht kaufen"** – Ihr Geschäft ist entdeckbar, aber etwas fehlt, bevor ein Kauf abgeschlossen werden kann (meistens ein verbundener Zahlungsanbieter).
- **"Notstopp ist aktiviert"** oder **"Agenterhandel ist deaktiviert"** – nichts wird den Assistenten angeboten.

Unter dem Urteil sehen Sie eine kurze Prüfliste – Zahlungsanbieter angeschlossen, Versandkosten können berechnet werden, Produkte sind für Assistenten sichtbar – mit einem Hinweis neben allem, was noch Aufmerksamkeit benötigt. Die Zähler zeigen an, wie viele Produkte Assistenten verkaufen können, wie viele Sie von ihnen versteckt haben, wie viele Assistenten besucht haben und wie viele Sie blockiert haben.

Die Prüfliste spiegelt Ihre **Live-Einrichtung** wider: Verbinden Sie einen Zahlungsanbieter oder fügen Sie eine Versandmethode hinzu, und das Urteil aktualisiert sich beim nächsten Öffnen der Seite.

## Der Notstopp

Der **Notstopp** ist ein separater Schalter gegenüber dem Hauptschalter. Verwenden Sie ihn, um sofort alle Assistententätigkeiten zu stoppen – z. B. wenn etwas nicht stimmt –, ohne Ihre Konfiguration zu verändern. Heben Sie ihn auf, um fortzufahren. Stellen Sie sich den Hauptschalter als "ist diese Funktion konfiguriert" und den Notstopp als "Alles stoppen, sofort" vor.

## Was Assistenten können

Zwei Ebenen des Zugangs, die separat kontrolliert werden:

- **Lesen** (Entdeckung und Durchstöbern) ist risikoärmer. Ein Assistent kann Ihr Geschäft finden und Produktinformationen lesen.
- **Kasse** (echter Kauf) ist mit höheren Risiken verbunden und bleibt für nicht verifizierte Assistenten geschlossen, es sei denn, Sie erlauben es.

Ein Geschäft kann entdeckbar sein, ohne kaufbar zu sein – eine nützliche Möglichkeit, zu beginnen.

## Spezifische Produkte verstecken

Jedes Produkt hat einen **Sichtbarkeit für KI-Einkaufsagenten**-Einstellungsbutton (standardmäßig aktiviert). Schalten Sie ihn aus, um ein bestimmtes Produkt vor den Assistenten zu verstecken, während es auf Ihrem Geschäft bleibt – praktisch für Artikel, die Sie lieber nur über Ihre eigene Website verkaufen möchten.

## Einzelne Assistenten verwalten

Wenn ein Assistent erstmals kauft – oder es versucht –, protokolliert Spwig dies unter **KI-Einkauf → Agenten-Identitäten**. Jeder Eintrag zeigt die verifizierte Heimat des Assistenten (das Verzeichnis, mit dem er sich authentifiziert), sein Vertrauensniveau und die Anzahl der Anfragen an, die er gestellt hat. Der Name und das Logo, die ein Assistent präsentiert, werden nur als *behauptete* Details angezeigt – behandeln Sie sie als Etikett, nicht als Identitätsbeweis; der verifizierte Zuhause-Teil ist der Teil, der vertrauenswürdig ist.

Jeder Assistent hat eines der drei Vertrauensniveaus:

| Vertrauensniveau | Was es bedeutet |
|---|---|
| **Begrenzt (verifiziert, eingeschränkt)** | Der Standard für einen neuen Assistenten. Spwig hat seine Identität aufgezeichnet, und er trägt die Auftragswertbegrenzung, die Tagesausgabenbegrenzung und die Zahlungsbeschränkungen, die auf seiner Richtlinie festgelegt sind (siehe unten). |
| **Verifiziert (Grenzen entfernt)** | Eine bewusste Entscheidung von Ihnen, diesem Assistenten vollständig zu vertrauen. Seine Auftragswert- und Tagesausgabenbegrenzungen werden gelöscht. |
| **Blockiert** | Der Assistent kann Ihr Geschäft nicht mehr kaufen. Offene Käufe werden beendet, obwohl bereits genommene Zahlungen unangetastet bleiben. |

Um einen Assistenten zu stoppen, wählen Sie ihn in der Liste aus und wählen Sie **Ausgewählte Assistenten blockieren**. **Ausgewählte Assistenten entsperren** kehrt ihn immer in **Begrenzt** zurück – nie direkt in **Verifiziert** –, da das Aufheben von Grenzen ein separates, bewusstes Schritt ist.

Um die Grenzen eines Assistenten vollständig aufzuheben, wählen Sie ihn aus und wählen Sie **Zur Verifikation erhöhen (Grenzen entfernen)**.

Dies leert seinen Maximalbestellwert und den Tagesausgabegrenzwert und versetzt den Assistenten in den Zustand "Verifiziert".

Ein blockierter Assistent wird übersprungen - blockieren Sie ihn zunächst, und heben Sie ihn dann an.

Betrachten Sie dies als eine echte Vertrauensentscheidung: Heben Sie nur einen Assistenten an, von dem Sie überzeugt sind, da die Verifizierung die Schutzvorkehrungen entfernt, mit denen ein neuer Assistent beginnt.

## Festlegen der Grenzen eines Assistenten

Öffnen Sie die Detailseite eines Assistenten, und verwenden Sie den Abschnitt **Policy (Grenzen & erlaubte Angebote)**, um festzulegen, was er tun darf:

| Feld | Was es steuert |
|---|---|
| **Maximalbestellwert** | Der größte Einzelbestellwert, den dieser Assistent tätigen kann. Lassen Sie es leer, um keine Begrenzung vorzusehen. |
| **Tagesausgabegrenze** | Der maximale Betrag, den dieser Assistent an einem Tag über alle Bestellungen hinweg ausgeben kann. Lassen Sie es leer, um keine Begrenzung vorzusehen. |
| **Rabattcodes erlauben** | Ob der Assistent Rabattcodes beim Bezahlen anwenden kann. |
| **Geschenkkarten erlauben** | Ob der Assistent Geschenkkarten einlösen kann. |
| **Digitale Waren erlauben** | Ob der Assistent digitale Produkte kaufen kann. |
| **Rate Limit (pro Minute)** | Wie viele Anfragen der Assistent pro Minute an Ihren Shop senden kann. |

Ein neuer Assistent hat standardmäßig konkrete Bestellwerte und Ausgabengrenzen und hat Rabattcodes, Geschenkkarten und digitale Waren deaktiviert - den bewusst konservativen Standard. Ändern Sie eines dieser Felder und speichern Sie es; jede Änderung wird in **Agent Events** mit den vorherigen und nachfolgenden Werten geschrieben, sodass Sie stets eine Aufzeichnung davon haben, wer was geändert und wann geändert hat. Das Hochheben eines Assistenten auf "Verifiziert" löscht seinen Maximalbestellwert und die Tagesausgabengrenze für Sie - Sie müssen sie nicht manuell leeren.

## Der Aktivitätsverlauf

**AI Shopping → Agent Events** ist ein Beweismittel, das auf Manipulationen prüft, was Assistenten getan haben - jeden verifizierten Antrag, jeden blockierten Versuch, jede Änderung, die Sie vorgenommen haben. Es ist nur zum Anzeigen gedacht und kann nicht bearbeitet oder gelöscht werden, sodass es als Beweis für Sie steht, falls ein Kauf, den ein Assistent getätigt hat, jemals gestritten wird.

## Ein Hinweis zu den Assistenten-Plattformen

Die Unternehmen, die diese Assistenten betreiben (und die Regeln, um darin erscheinen zu können), sind neu und ändern sich oft. Einige erfordern, dass Sie sich bewerben oder regionale Bedingungen erfüllen, bevor Ihre Produkte durch sie gekauft werden können. Spwig bereitet Ihren Laden vor; ob ein bestimmter Assistent Sie auflistet, hängt von diesem Assistenten ab.

Beibehalten Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe.