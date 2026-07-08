---
title: Kundennachverfolgung verwalten
---

Der Abschnitt Kundennachverfolgung gibt Ihnen einen vollständigen Überblick über alle aktiven, pausierten und abgebrochenen wiederkehrenden Abonnements in Ihrem Geschäft. Von hier aus können Sie den Zahlungsstatus überwachen, detaillierte Informationen zu einzelnen Abonnements einsehen und Maßnahmen ergreifen, wenn Probleme auftreten.

## Kundennachverfolgung ansehen

Navigieren Sie zu **Abonnements > Kundennachverfolgung**, um die vollständige Liste aller Abonnements aller Kunden anzuzeigen.

![Liste der Kundennachverfolgungen](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Die Liste zeigt für jedes Abonnement den Kunden, den Plan-Namen, den aktuellen Status, das nächste Zahlungsdatum und die Anzahl der abgeschlossenen Zahlungszyklen an.

### Filtern und Suchen

Verwenden Sie das Filterpanel auf der rechten Seite, um Abonnements nach folgenden Kriterien zu filtern:

- **Status** — Filtern Sie nach Aktiv, Testphase, Überfällig, Pausiert, Abgebrochen oder Abgelaufen
- **Plan** — Zeigen Sie Abonnements für einen bestimmten Plan an
- **Provider-Modus** — Native (Stripe/PayPal-gesteuert) oder Fallback (interne Abrechnung)

Verwenden Sie die Suchleiste, um Abonnements nach E-Mail-Adresse des Kunden zu finden.

## Abonnementsstatus

Das Verständnis jedes Status hilft Ihnen dabei, Abonnements zu identifizieren, die Aufmerksamkeit erfordern:

| Status | Was es bedeutet |
|--------|---------------|
| **Testphase** | Der Kunde ist in der kostenlosen oder reduzierten Testphase |
| **Aktiv** | Das Abonnement ist gesund — die Zahlung ist aktuell und der Zugriff ist aktiv |
| **Überfällig** | Ein Zahlungsversuch ist fehlgeschlagen — das System versucht erneut. Der Kunde behält während der Verjährungsfrist den Zugriff |
| **Pausiert** | Das Abonnement ist vorübergehend ausgesetzt — keine Zahlung, kein Zugriff |
| **Abgebrochen** | Die Kündigung wurde beantragt. Der Kunde kann bis zum Enddatum des Abonnements weiterhin Zugriff haben |
| **Abgelaufen** | Das Abonnement ist vollständig beendet — Testphase abgelaufen, maximale Zahlungszyklen erreicht oder Kündigungsfrist abgelaufen |

Abonnements, die **überfällig** sind, benötigen die größte Aufmerksamkeit — wenn die Zahlung weiterhin fehlschlägt und die Verjährungsfrist abgelaufen ist, wird das Abonnement ausgesetzt.

## Details eines Abonnements ansehen

Klicken Sie auf ein beliebiges Abonnement, um die Detailansicht zu öffnen. Dies zeigt:

### Aktueller Zahlungszyklus

- **Aktueller Zyklusbeginn / -ende** — Die Daten des aktiven Zahlungszeitraums
- **Nächster Zahlungsdatum** — Wann der nächste Zahlungsversuch stattfinden wird
- **Letztes Zahlungsdatum** und **Letzter Zahlungsstatus** — Ergebnis des letzten Zahlungsversuchs
- **Zahlungszyklusanzahl** — Wie viele erfolgreiche Zahlungszyklen abgeschlossen wurden

### Abonnementinformationen

- **Plan** und **Preistufe** — Welchen Plan und Zahlungshäufigkeit der Kunde nutzt
- **Produkt / Variante** — Das Katalogprodukt, das mit diesem Abonnement verknüpft ist (falls zutreffend)
- **Menge** — Anzahl der Sitzplätze oder Einheiten (für mengenbasierte Pläne)
- **Zahlungstoken** — Der gespeicherte Zahlungsmethode, der für wiederkehrende Zahlungen verwendet wird

### Testphase-Details

Wenn das Abonnement in der Testphase ist, zeigt das **Enddatum der Testphase** an, wann die Testphase des Kunden endet und die volle Abrechnung beginnt.

### Kündigungsdetails

Für abgebrochene Abonnements können Sie folgende Informationen einsehen:

- **Kündigungsart** — Ob die Kündigung sofort, zum Enddatum des Abonnements oder geplant war
- **Abgebrochen am** — Wann die Kündigung beantragt wurde
- **Kündigungsgrund** — Notizen, warum der Kunde das Abonnement abgebrochen hat (falls aufgezeichnet)
- **Wiederherstellungstermin** — Letzter Tag, an dem der Kunde das Abonnement ohne erneutes Abonnement von Grund auf wiederherstellen kann

### Verjährungsfrist und Verpflichtungen

- **Enddatum der Verjährungsfrist** — Wenn eine Zahlung fehlschlägt, zeigt dies das Deadline an, bevor der Zugriff ausgesetzt wird
- **Enddatum der Mindestverpflichtung** — Für Pläne mit Mindestverpflichtungen ist dies das früheste Kündigungsdatum

## Ein Abonnement pausieren

Ein pausiertes Abonnement stoppt vorübergehend die Abrechnung und suspendiert den Zugriff. Dies ist nützlich für Kunden, die eine Pause machen möchten, ohne das Abonnement vollständig zu kündigen.

Um pausierte Abonnements anzuzeigen, filtern Sie nach **Status: Pausiert**. Die Detailansicht zeigt an:

- **Pausiert am** — Wann die Pausierung begonnen hat
- **Pausierungsgrund** — Notizen, warum es pausiert wurde
- **Automatischer Wiederstartdatum** — Wenn festgelegt, ist dies das Datum, an dem das Abonnement automatisch wieder abgerechnet und der Zugriff wiederhergestellt wird

Abonnements werden entweder am automatischen Wiederholungsdatum oder wenn der Kunde sie manuell reaktiviert, wieder aufgenommen.

## Abrechnungszyklus-Protokolle

Jeder Abrechnungsversuch — erfolgreich oder fehlgeschlagen — wird im Abrechnungszyklus-Protokoll gespeichert. Navigieren Sie zu **Abonnements > Abrechnungszyklus-Protokolle**, um diese Historie anzuzeigen.

![Liste der Abrechnungszyklus-Protokolle](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Eintrag im Abrechnungszyklus-Protokoll einsehen

Jeder Protokolleintrag dokumentiert:

- **Abonnement** — Welches Kundenabonnement dieser Abrechnungsversuch gehört
- **Zyklusnummer** — Sequenzieller Abrechnungszyklus (Zyklus 1 = erste Gebühr nach der Testphase)
- **Abrechnungsdatum** — Wann die Gebühr versucht wurde
- **Status** — Ausstehend, In Bearbeitung, Erfolgreich, Fehlgeschlagen oder Wiederholung
- **Gebührenbreakdown**:
  - **Grundgebühr** — Der Planpreis vor jeder Anpassung
  - **Mengengebühr** — Zusätzliche Gebühr für die Anzahl der Sitzplätze/Einheiten
  - **Zusatzgebühren** — Gesamtkosten aktiver Zusatzleistungen
  - **Rabattgebühr** — Gesamte Rabatte, die angewendet wurden
  - **Gesamtgebühr** — Der endgültige Betrag, der abgebucht wurde (oder versucht wurde)
- **Zahlungsmethode** — Die Karte oder Zahlungsmethode, die verwendet wurde
- **Transaktions-ID des Anbieters** — Die Referenznummer des Zahlungsanbieters (nützlich für Rückzahlungsabfragen)
- **Fehlergrund** — Wenn die Abrechnung fehlgeschlagen ist, warum sie fehlgeschlagen ist (z. B. Karte abgelehnt, nicht genügend Guthaben)

### Diagnose von Zahlungsfehlern

Wenn ein Kunde Sie wegen eines Abrechnungsproblems kontaktiert, suchen Sie nach seinem Abonnement und prüfen Sie die Abrechnungszyklus-Protokolle. Das Feld **Fehlergrund** erklärt, was schiefgelaufen ist. Häufige Fehlergründe sind:

- **Karte abgelehnt** — Die Karte des Kunden wurde von ihrer Bank abgelehnt
- **Nicht genügend Guthaben** — Der Kontostand war zu niedrig zum Zeitpunkt der Abrechnung
- **Karte abgelaufen** — Die gespeicherte Zahlungsmethode ist abgelaufen
- **Netzwerkfehler** — Ein vorübergehender Verbindungsfehler mit dem Zahlungsanbieter — löst sich in der Regel bei einer Wiederholung

Bei anhaltenden Fehlern bitten Sie den Kunden, seine Zahlungsmethode in seinen Kontoeinstellungen zu aktualisieren.

## Tipps

- Prüfen Sie den Filter **Überfällig** wöchentlich, um Abonnements zu erkennen, die das Risiko eines Abfalls bergen. Eine schnelle E-Mail an den Kunden löst oft Zahlungsprobleme, bevor die Verjährungsfrist abläuft.
- Abrechnungszyklus-Protokolle sind schreibgeschützt — sie werden automatisch erstellt und können nicht geändert werden. Dies stellt eine zuverlässige Prüfprotokollierung sicher.
- Wenn ein Kundenabonnement **Überfällig** anzeigt, aber der Kunde bereits seine Zahlungsmethode aktualisiert hat, wird der nächste automatische Wiederholungsversuch die neue Karte verwenden. Wiederholungen folgen dem Verjährungsplan, der im Plan konfiguriert ist.
- **Abgelaufene** Abonnements werden nicht gelöscht — sie bleiben für Berichte sichtbar. Verwenden Sie die Datumsfilter, um sich auf aktuelle Abonnements zu konzentrieren.
- Für Abonnements in der **Testphase** prüfen Sie das **Enddatum der Testphase**, um bevorstehende erste Gebühren vorherzusehen und Probleme mit der Zahlungsmethode proaktiv zu beheben.