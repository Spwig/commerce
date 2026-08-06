---
title: Kundennutzung verwalten
---

Der Bereich Kundennutzungen bietet Ihnen einen vollständigen Überblick über alle aktiven, pausierten und stornierten Wiederkehrauszahlungen in Ihrem Geschäft. Hier können Sie die Gesundheit der Rechnungsstellung überwachen, Einzelheiten zu jeder Nutzungsvereinbarung ansehen und Maßnahmen ergreifen, wenn Probleme auftreten.

## Kunden-Nutzungen ansehen

Gehen Sie zu **Nutzungen > Kundennutzungen**, um die vollständige Liste der Nutzungen aller Kunden anzuzeigen.

![Liste der Kundennutzungen](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Die Liste zeigt für jede Nutzungsvereinbarung den Kunden, den Namen des Plans, den aktuellen Status, das nächste Fälligkeitsdatum und die Anzahl der abgeschlossenen Abrechnungszyklen an.

### Filtern und suchen

Verwenden Sie das Filterpanel rechts, um Nutzungen nach folgenden Kriterien einzugrenzen:

- **Status** — Filtern Sie nach aktiv, Probezeit, Überfällig, pausiert, storniert oder abgelaufen
- **Plan** — Zeigen Sie Nutzungen für einen bestimmten Plan an
- **Anbietermodus** — Native (Stripe/PayPal-verwaltete) oder Fallback (interner Abrechnungsmodus)

Verwenden Sie die Suchleiste, um Nutzungen anhand der E-Mail-Adresse des Kunden zu finden.

## Nutzungsstatus

Das Verständnis jedes Status hilft Ihnen, Nutzungen zu identifizieren, die Aufmerksamkeit erfordern:

| Status | Was es bedeutet |
|--------|----------------|
| **Probezeit** | Der Kunde befindet sich in der kostenlosen oder reduzierten Preis-Probezeit |
| **Aktiv** | Die Nutzungsvereinbarung ist gesund – die Abrechnung ist aktuell und der Zugang ist aktiv |
| **Überfällig** | Ein Zahlungsversuch ist fehlgeschlagen – das System versucht, erneut zu zahlen. Der Kunde hat während der Frist noch Zugang |
| **Pausiert** | Die Nutzungsvereinbarung ist vorübergehend unterbrochen – keine Abrechnung, kein Zugang |
| **Storniert** | Die Stornierung wurde beantragt. Der Kunde kann möglicherweise noch Zugang bis zum Enddatum des Zeitraums haben |
| **Abgelaufen** | Die Nutzungsvereinbarung ist vollständig beendet – die Probezeit ist abgelaufen, die maximale Anzahl von Abrechnungszyklen erreicht oder die Stornierungsfrist ist abgelaufen |

Nutzungen, die **Überfällig** sind, erfordern die meiste Aufmerksamkeit – wenn die Zahlung weiterhin fehlschlägt und die Frist abgelaufen ist, wird die Nutzungsvereinbarung unterbrochen.

## Details einer Nutzungsvereinbarung ansehen

Klicken Sie auf eine beliebige Nutzungsvereinbarung, um die Detailansicht zu öffnen. Dies zeigt Folgendes an:

### Aktueller Abrechnungszeitraum

- **Aktueller Zeitraum Anfang / Ende** — Die Daten des aktiven Abrechnungszeitraums
- **Nächstes Fälligkeitsdatum** — Wann der nächste Zahlungsversuch unternommen wird
- **Letztes Fälligkeitsdatum** und **Letzter Abrechnungsstatus** — Das Ergebnis des letzten Abrechnungsversuchs
- **Anzahl der Abrechnungszyklen** — Wie viele erfolgreiche Abrechnungszyklen abgeschlossen wurden

### Nutzungsinformationen

- **Plan** und **Preisstufe** — Welcher Plan und welches Abrechnungsfrequenz der Kunde verwendet
- **Produkt / Variante** — Das Katalogprodukt, das mit dieser Nutzungsvereinbarung verknüpft ist (sofern zutreffend)
- **Menge** — Anzahl der Plätze oder Einheiten (für plangestützte Pläne)
- **Zahlungstoken** — Die gespeicherte Zahlungsmethode, die für die wiederkehrende Abrechnung verwendet wird

### Probephase Details

Wenn die Nutzungsvereinbarung sich in der Probezeit befindet, zeigt das **Enddatum der Probezeit** an, wann die Probezeit des Kunden abläuft und die vollständige Abrechnung beginnt.

### Stornierungsdetails

Bei stornierten Nutzungsvereinbarungen können Sie Folgendes sehen:

- **Stornierungstyp** — Ob die Stornierung sofort, am Ende des Zeitraums oder geplant war
- **Stornierungsdatum** — Wann die Stornierung beantragt wurde
- **Stornierungsgrund** — Bemerkungen dazu, warum der Kunde die Stornierung vorgenommen hat (sofern aufgezeichnetet)
- **Wiederherstellungstermin** — Der letzte Tag, an dem der Kunde die Wiederherstellung ohne Neuanmeldung durchführen kann

### Frist und Verpflichtungen

- **Fristende** — Falls eine Zahlung fehlgeschlagen ist, zeigt dies das Ablaufdatum an, bevor der Zugang unterbrochen wird
- **Mindestverpflichtungsdatum** — Für Pläne mit Mindestverpflichtungen das früheste Stornierungsdatum

## Pausieren einer Nutzungsvereinbarung

Eine pausierte Nutzungsvereinbarung unterbricht die Abrechnung vorübergehend und unterbricht auch den Zugang. Dies ist nützlich für Kunden, die eine Pause einlegen möchten, ohne vollständig zu stornieren.

Um pausierte Nutzungsvereinbarungen anzuzeigen, filtern Sie nach **Status: Pausiert**. Die Detailansicht zeigt Folgendes an:

- **Pausierungsdatum** — Wann die Pause begonnen hat
- **Pausierungsgrund** — Bemerkungen dazu, warum sie pausiert wurde
- **Automatisches Wiederaufnahme-Datum** — Falls festgelegt, das Datum, an dem die Nutzungsvereinbarung automatisch wieder abgerechnet und der Zugang wiederhergestellt wird

Abonnements werden entweder am Auto-Resume-Datum wieder aufgenommen oder wenn der Kunde sie manuell erneut aktiviert.

## Gebührenzyklus-Protokolle

Jeder Gebührenversuch — erfolgreich oder fehlgeschlagen — wird im Gebührenzyklus-Protokoll protokolliert. Navigieren Sie zu **Abonnements > Gebührenzyklus-Protokolle**, um diese Historie anzuzeigen.

![Liste des Gebührenzyklus-Protokolls](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Eintrag des Gebührenzyklus-Protokolls lesen

Jeder Protokolleintrag enthält folgende Informationen:

- **Abonnement** — Zu welchem Kundensubskription dieser Gebührenversuch gehört
- **Zyklusnummer** — Sekundärer Gebührenzyklus (Zyklus 1 = erste Gebühr nach dem Testzeitraum)
- **Gebührendatum** — Wann die Gebühr versucht wurde
- **Status** — Ausstehend, Verarbeitung, Erfolgreich, Fehlgeschlagen oder Wiederholung
- **Betragsspalte**:
  - **Grundbetrag** — Der Planpreis vor allen Anpassungen
  - **Mengenbetrag** — Zusätzliche Gebühr für die Anzahl der Plätze/Einheiten
  - **Zusatzleistungen-Betrag** — Gesamtkosten aktiver Zusatzleistungen
  - **Rabatt-Betrag** — Gesamtrabatte angewandt
  - **Gesamtbetrag** — Der endgültige Gebetrag (oder versuchter Betrag)
- **Zahlungsmethode** — Die Karte oder Zahlungsmethode, die verwendet wurde
- **Provider-Transaktions-ID** — Die Referenznummer des Zahlungsanbieters (nützlich für Rückerstattungsanfragen)
- **Fehlerschlussfolgerung** — Falls die Gebühr fehlgeschlagen ist, warum sie fehlgeschlagen ist (z. B. Karte abgelehnt, unzureichende Mittel)

### Diagnose von Zahlungsfehlern

Wenn ein Kunde sich bei Ihnen wegen eines Gebührenproblems meldet, finden Sie ihr Abonnement und prüfen Sie das Gebührenzyklus-Protokoll. Das Feld **Fehlerschlussfolgerung** erklärt, was schiefgelaufen ist. Häufige Fehlerschlussfolgerungen sind:

- **Karte abgelehnt** — Die Karte des Kunden wurde von der Bank abgelehnt
- **Unzureichende Mittel** — Das Kontoguthaben war zum Zeitpunkt der Gebühr zu niedrig
- **Karte abgelaufen** — Die gespeicherte Zahlungsmethode ist abgelaufen
- **Netzwerkfehler** — Ein temporäres Verbindungsproblem mit dem Zahlungsanbieter — wird in der Regel bei erneuter Versuch gelöst

Bei anhaltenden Fehlern leiten Sie den Kunden dazu an, ihre Zahlungsmethode in den Kontoeinstellungen zu aktualisieren.

## Wie Erneuerungen erfüllt werden

Jeder erfolgreiche Erneuerungsgebührenversuch erstellt ein brandneues bezahltes Auftrag für diesen Gebührenzyklus — es handelt sich nicht nur um einen Zahlungsverlauf. Dieser Auftrag durchläuft Ihren normalen Erfüllungsprozess genau so wie ein bei der Kasse platziertes Auftrag:

- **Physische Produkte** — Der Erneuerungsauftrag gelangt in die reguläre Erfüllungswarteschlange für das Auswählen, Verpacken und Versenden. Er wird nicht automatisch anhand des Lagerbestands zugewiesen, sobald die Karte belastet wird, sodass ein vorübergehender Lagerbestandsmangel niemals einen bereits erfolgreich abgeschlossenen Gebührenversuch blockiert — Sie sehen den Auftrag immer noch und können ihn entsprechend dem Lagerbestand erfüllen.
- **Digitale Produkte** — Der Zugang (Download-Links, Lizenzschlüssel) wird automatisch erneut erteilt, sobald der Erneuerungsauftrag erstellt wird, genau so wie bei einem Erstkauf.

Erneuerungsaufträge kopieren die Versand- und Rechnungsdaten des Auftrags, der das Abonnement gestartet hat, sodass Sie nichts erneut eingeben müssen. Sie tragen kein besonderes Abzeichen in Ihrem **Bestellungen**-Liste, aber Sie können immer einen bestimmten Zykl direkt zurück zu seinem Auftrag verfolgen: öffnen Sie **Abonnements > Gebührenzyklus-Protokolle**, klicken Sie auf den Protokolleintrag für diesen Zykl, und das Feld **Bestellung** verweist direkt darauf.

## Automatische Abonnement-E-Mails

Spwig sendet automatisch E-Mails zum Abonnement-Lifecycle — Sie müssen diese manuell nicht auslösen. Die, die Händler am häufigsten fragen:

| E-Mail | Wann wird sie gesendet |
|-------|------------------|
| **Erinnerung zur Erneuerung** | Vor einer bevorstehenden Erneuerungsgutschrift |
| **Testzeitraum endet** | Vor dem Übergang eines kostenlosen oder reduzierten Testzeitraums in die vollständige Gebühr |
| **Zahlung fehlgeschlagen** | Sofort nach dem Fehlschlagen einer Erneuerungsgutschrift und erneut als letzte Mitteilung, wenn die Frist abgelaufen ist (Dunning) |
| **Bestätigung der Kündigung** | Wenn ein Abonnement gekündigt wird |

Spwig sendet außerdem Willkommens-, Zahlungserfolgs-, Pause/Erneuerung, Ablauf, Wiederaktivierung, Planaenderung und E-Mail zur Ablauf des Zahlungsmethode bei den relevanten Punkten in einem Abonnement-Lifecycle.

Alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

Alle diese sind gewöhnliche E-Mail-Vorlagen — siehe [E-Mail-Vorlagen](/help/email-templates), um deren Inhalt zu überprüfen oder anzupassen und sicherzustellen, dass sie aktiviert sind.

## Kunden-Selbstbedienung

Kunden müssen Sie nicht für gewöhnliche Abonnementsänderungen kontaktieren — sie können ihre eigenen Abonnements über ihr Konto verwalten: Details und Rechnungsverlauf ansehen, das Abonnement pausieren, fortsetzen, kündigen und die auf der Karte hinterlegte Zahlungsmethode aktualisieren. Dies deckt den Großteil ab, was andernfalls in Ihrem Support-Queue landen würde. Wenn ein Kunde sich wegen ihres Abonnements an Sie wendet, lohnt es sich, zuerst zu prüfen, ob sie bereits ihre Kontoseite genutzt haben, bevor Sie die Änderung für sie im Admin vornehmen.

## Tipps

- Prüfen Sie wöchentlich den **Überfällig**-Filter, um Abonnements zu ermitteln, die das Austrittsrisiko haben. Eine schnelle E-Mail an den Kunden löst die Zahlungsprobleme oft vor Ablauf der Frist auf.
- Die Protokolle der Abrechnungszyklen sind schreibgeschützt — sie werden automatisch erstellt und können nicht geändert werden. Dies stellt sicher, dass ein zuverlässiger Audit-Verlauf gewährleistet ist.
- Falls das Abonnement eines Kunden **Überfällig** ist, aber sie bereits ihre Zahlungsmethode aktualisiert haben, erfasst der nächste automatische Versuch die neue Karte. Wiederholungsversuche folgen dem im Plan konfigurierten Fristenplan.
- **Abgelaufene** Abonnements werden nicht gelöscht — sie bleiben für Berichte sichtbar. Verwenden Sie die Datumsfilter, um sich auf aktuelle Abonnements zu konzentrieren.
- Bei Abonnements im **Probemonat** prüfen Sie das **Datum des Probemonatsende**, um auf kommende erste Gebühren vorbereitet zu sein, und lösen Sie proaktiv mögliche Probleme mit der Zahlungsmethode.
- Falls ein Kunde sagt, dass ein physisches Erneuerungsprodukt "noch nicht versandt wurde", prüfen Sie Ihren regulären Versand-Queue anstelle des Abonnement-Records — Erneuerungsaufträge werden auf die gleiche Weise abgewickelt wie andere Aufträge und springen nicht in der Warteschlange.

Alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.