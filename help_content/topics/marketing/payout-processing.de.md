---
title: Auszahlungsverarbeitung
---

Auszahlungsverarbeitung ermöglicht es Ihnen, Affiliate-Partner für ihre genehmigten Kommissionen zu bezahlen. Dieser Leitfaden zeigt Ihnen, wie Sie Auszahlungen über PayPal oder Banküberweisungen erstellen, verwalten und verarbeiten können.

![Auszahlungsliste](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Übersicht über Auszahlungen

Eine Auszahlung ist ein Zahlungsbatch, der mehrere genehmigte Kommissionen für einen einzelnen Affiliate zusammenfasst. Stellen Sie es sich wie einen Scheck für alle ausstehenden Einnahmen vor.

Wichtige Merkmale:
- **Enthält mehrere Kommissionen** — Eine Auszahlung kann Dutzende genehmigter Kommissionen abdecken
- **Erfordert Mindestschwellenwert** — Die meisten Programme haben Mindestauszahlungsbeträge ($50-$100 typisch)
- **Wird über Anbieter verarbeitet** — PayPal oder Airwallex übernehmen die tatsächliche Geldüberweisung
- **Hat Lebenszyklus** — Ausstehend → Verarbeitung → Abgeschlossen (oder Fehlgeschlagen)

## Auszahlungsworkflow

Der vollständige Auszahlungsprozess folgt sechs Schritten:

1. **Affiliate verdient Kommissionen** — Verkäufe werden Affiliate-Tracking-Links zugeordnet
2. **Händler genehmigt Kommissionen** — Genehmigen Sie ausstehende Kommissionen
3. **Kontostand erreicht Mindestwert** — Genehmigter Kontostand des Affiliates erreicht das Programmthreshold
4. **Affiliate beantragt Auszahlung** — Affiliate stellt Auszahlungsantrag in seinem Dashboard
5. **Händler verarbeitet Auszahlung** — Sie erstellen und verarbeiten die Auszahlung
6. **Zahlung abgeschlossen** — Anbieter sendet Gelder, Kommissionen werden als bezahlt markiert

## Auszahlungen ansehen

Navigieren Sie zu **Affiliate-Programm > Auszahlungen**, um das Auszahlungsverwaltungs-Dashboard zu öffnen.

Das Statistikpanel zeigt:
- **Ausstehend** — Erstellte Auszahlungen, die noch nicht verarbeitet wurden
- **Verarbeitung** — Wird derzeit an den Zahlungsdienstleister gesendet
- **Abgeschlossen** — Erfolgreich bezahlt
- **Fehlgeschlagen** — Zahlung fehlgeschlagen (erfordert Aufmerksamkeit)

Die Listenansicht zeigt:
- Affiliate-Name und -Code
- Auszahlungsbetrag
- Zahlungsmethode (PayPal oder Banküberweisung)
- Status-Abzeichen
- Erstellungs- und Abschlussdaten
- Aktionen-Buttons

Verwenden Sie Filter, um nach folgenden Kriterien zu suchen:
- Affiliate
- Zahlungsmethode
- Status
- Datumsbereich

## Auszahlung erstellen

Folgen Sie diesen Schritten, um eine neue Auszahlung zu erstellen:

1. **Navigieren Sie** zu **Affiliate-Programm > Auszahlungen**
2. **Klicken Sie** auf die Schaltfläche **+ Auszahlung hinzufügen**
3. **Wählen Sie Affiliate** aus dem Dropdown-Menü aus
4. **Überprüfen Sie genehmigte Kommissionen** — Das System zeigt alle unbezahlten, genehmigten Kommissionen für diesen Affiliate an
5. **Wählen Sie Kommissionen aus, die enthalten werden sollen** — Markieren Sie die Kästchen für die zu zahlenden Kommissionen (normalerweise alle)
6. **Überprüfen Sie den Gesamtbetrag** — Das System berechnet die Summe automatisch
7. **Wählen Sie Zahlungsmethode** — PayPal oder Banküberweisung (basierend auf der Präferenz des Affiliates)
8. **Wählen Sie Anbieterkonto** — Wählen Sie das zu verwendende PayPal/Airwallex-Konto aus
9. **Fügen Sie Notizen hinzu** (optional) — Interne Notizen für die Buchhaltung
10. **Klicken Sie auf Speichern** — Auszahlung wird mit dem Status "Ausstehend" erstellt

Die Auszahlung ist jetzt zur Verarbeitung bereit.

## Auszahlungen verarbeiten

Für die Verarbeitung von Auszahlungen haben Sie zwei Optionen: manuell oder anbieterbasiert.

### Manuelle Verarbeitung

Verwenden Sie die manuelle Verarbeitung, wenn Sie Zahlungen außerhalb des Systems verwalten (Schecks, Überweisungen usw.):

1. Wählen Sie die Auszahlung in der Liste aus
2. Klicken Sie auf die Aktion **Als Verarbeitung markieren**
3. Führen Sie die Zahlung über Ihre externe Methode ab
4. Gehen Sie zurück zur Auszahlung
5. Klicken Sie auf die Aktion **Als abgeschlossen markieren**
6. Die Kommissionen werden automatisch in den Status "Bezahlt" geändert

Die manuelle Verarbeitung bietet Flexibilität, erfordert jedoch mehr administrativen Aufwand.

### Anbieterbasierte Verarbeitung (Empfohlen)

Die Anbieterbasierte Verarbeitung automatisiert Zahlungen über PayPal oder Airwallex:

1. **Wählen Sie Auszahlung(en)** in der Liste aus (Sie können mehrere verarbeiten)
2. **Klicken Sie** auf die Aktion **Mit Anbieter verarbeiten**
3. **Bestätigen Sie** im Dialog
4. **Das System wartet auf die Aufgabe** — Celery-Worker verarbeitet die API-Anfrage
5. **Der Anbieter verarbeitet die Zahlung**:
   - **PayPal**: Bündelt bis zu 15.000 Auszahlungen pro Anfrage
   - **Airwallex**: Einzelne Banküberweisungen
6. **Webhook aktualisiert den Status** — Der Anbieter bestätigt die Abwicklung
7. **Kommissionen werden als bezahlt markiert** — Das System aktualisiert alle enthaltenen Kommissionen

Die Anbieterbasierte Verarbeitung ist schneller, zuverlässiger und erstellt eine automatische Prüfprotokollierung.

## Auszahlungsmethoden

Spwig unterstützt zwei Auszahlungsmethoden mit unterschiedlichen Anforderungen:

| Methode | Anbieter | Anforderungen | Verarbeitungszeit | Gebühren | Bestens geeignet für |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Auszahlungen | Affiliate muss eine gültige `payment_email` haben | 1-2 Geschäftstage | ~2% oder $0,25-$1,00 pro Zahlung | Die meisten Affiliates, globale Reichweite |
| **Banküberweisung** | Airwallex | Bankkontodetails (Kontonummer, Routing, SWIFT) | 2-5 Geschäftstage | Variiert je nach Land | Internationale Affiliates, große Beträge |

Affiliates konfigurieren ihre Zahlungsmethode und Details in ihrem Dashboard. Das System wählt automatisch den entsprechenden Anbieter basierend auf ihrer Präferenz.

### Logik zur Auswahl der Zahlungsmethode

Bei der Verarbeitung einer Auszahlung wählt Spwig den Anbieter wie folgt:

1. Prüfen Sie die bevorzugte Zahlungsmethode des Affiliates (PayPal oder Banküberweisung)
2. Zuordnen zu konfiguriertem Anbieterkonto (PayPal → PayPal, Bank → Airwallex)
3. Falls keine Präferenz vorhanden, zurückfallen auf den ersten verfügbaren Anbieter
4. Fehlermeldung anzeige, wenn keine Anbieter konfiguriert sind

## Auszahlungsstatusverlauf

Das Verständnis der Auszahlungsstatus hilft Ihnen, den Zahlungsfortschritt zu verfolgen:

| Status | Bedeutung | Nächste Aktion |
|--------|---------|-------------|
| **Ausstehend** | Erstellt, aber noch nicht an den Anbieter gesendet | Verarbeiten Sie mit Anbieter oder markieren Sie als verarbeitend |
| **Verarbeitung** | An Zahlungsdienstleister übermittelt, wartet auf Bestätigung | Warte auf Webhook oder prüfe Anbieter-Dashboard |
| **Abgeschlossen** | Zahlung erfolgreich, Gelder überwiesen | Keine — Kommissionen werden als bezahlt markiert |
| **Fehlgeschlagen** | Zahlung fehlgeschlagen (siehe Fehlerdetails) | Fehler überprüfen, Problem beheben, erneut versuchen oder abbrechen |
| **Abgebrochen** | Manuell vor Abschluss abgebrochen | Keine — Kommissionen bleiben unbezahlt |

### Erfolgsverlauf

Ausstehend → Verarbeitung → Abgeschlossen

Dies ist der glückliche Pfad. Webhooks des Anbieters aktualisieren automatisch den Status, während die Zahlung voranschreitet.

### Fehlverlauf

Ausstehend → Verarbeitung → Fehlgeschlagen

Wenn eine Zahlung fehlschlägt, ändert sich der Auszahlungsstatus in Fehlgeschlagen und Sie müssen dies untersuchen.

## Umgang mit fehlgeschlagenen Auszahlungen

Fehlgeschlagene Auszahlungen erfordern manuelle Intervention. Häufige Ursachen für Fehlschläge:

| Ursache | Anbieterfehler | Lösung |
|-------|----------------|----------|
| Ungültiges Konto | "Empfänger-Konto nicht gefunden" | Überprüfen Sie die Zahlungsemail oder Bankdetails des Affiliates |
| Unzureichender Kontostand | "Unzureichende Mittel" | Fügen Sie Mittel zu Ihrem Anbieterkonto hinzu |
| Bankdetailsfehler | "Ungültige Routing-Nummer" | Fordern Sie den Affiliate auf, seine Bankinformationen zu aktualisieren |
| Kontobeschränkung | "Empfänger kann keine Zahlungen empfangen" | Kontaktieren Sie den Affiliate, um seinen Kontostatus zu lösen |
| Anbieterproblem | "Dienst vorübergehend nicht verfügbar" | Warten Sie und versuchen Sie es nach einigen Stunden erneut |

### Wie man eine fehlgeschlagene Auszahlung erneut versucht

1. **Sehen Sie sich die fehlgeschlagene Auszahlung an** — Klicken Sie darauf in der Liste
2. **Lesen Sie die Fehlermeldung** — Prüfen Sie das Feld **Anbieterantwort** für Details
3. **Beheben Sie das zugrunde liegende Problem** — Aktualisieren Sie Affiliate-Details, fügen Sie Anbieter-Mittel hinzu usw.
4. **Setzen Sie den Status zurück** — Ändern Sie den Status zurück auf Ausstehend (Bearbeitungsformular)
5. **Verarbeiten Sie erneut** — Verwenden Sie die Aktion **Mit Anbieter verarbeiten**

### Wie man eine Auszahlung abbricht und neu erstellt

Wenn das erneute Versuchen nicht funktioniert:

1. **Öffnen Sie die fehlgeschlagene Auszahlung**
2. **Ändern Sie den Status in Abgebrochen**
3. **Speichern Sie die Auszahlung**
4. **Erstellen Sie eine neue Auszahlung** — Folgen Sie erneut den Erstellungsschritten
5. **Verarbeiten Sie die neue Auszahlung**

Abgebrochene Auszahlungen markieren keine Kommissionen als bezahlt, sodass sie für neue Auszahlungen weiterhin qualifiziert sind.

## Integration von Auszahlungsanbietern

Die Verarbeitung von Auszahlungen erfordert ein konfiguriertes Auszahlungsanbieterkonto. Spwig integriert sich mit:

- **PayPal Auszahlungen API** — Für PayPal-Zahlungen
- **Airwallex** — Für internationale Banküberweisungen

### Setup-Anforderungen

Bevor Sie Auszahlungen verarbeiten:
1. Konfigurieren Sie mindestens einen Anbieter in **Einstellungen > Auszahlungsanbieter**
2. Fügen Sie API-Anmeldeinformationen hinzu (Client-ID, Geheimnis, API-Schlüssel)
3. Setzen Sie auf Produktionsmodus (Sandbox für Tests)
4. Konfigurieren Sie die Webhook-URL im Anbieter-Dashboard
5. Überprüfen Sie die Verbindung mit einer Testauszahlung

Siehe den Leitfaden [Einrichtung von Auszahlungsanbietern](#) für detaillierte Konfigurationsanweisungen.

### Auswahl des Anbieters durch Affiliate

Affiliates wählen ihre bevorzugte Zahlungsmethode in ihrem Dashboard:
- PayPal: Geben Sie `payment_email` ein
- Banküberweisung: Geben Sie Bankkontodetails ein

Das System leitet Auszahlungen automatisch an den entsprechenden Anbieter weiter.

## Best Practices für Auszahlungsplanung

Erstellen Sie einen regelmäßigen Auszahlungsplan, um das Vertrauen der Affiliates zu stärken:

| Plan | Häufigkeit | Arbeitsaufwand | Affiliate-Zufriedenheit | Empfohlen für |
|----------|-----------|----------|------------------------|-----------------|
| Wöchentlich | Jeden Freitag | Hoch | Ausgezeichnet | Neue Programme, hoher Umsatz |
| Zweimal wöchentlich | 1. und 15. | Mittel | Gut | Programme mit mittlerem Umsatz |
| Monatlich | 1. des Monats | Niedrig | Akzeptabel | Etablierte Programme |
| Quartalsweise | Alle 3 Monate | Sehr niedrig | Schlecht | Nicht empfohlen |

Berücksichtigen Sie die Größe Ihres Programms und Ihre administrative Kapazität, wenn Sie einen Plan wählen.

## Best Practices für die Verarbeitung

Folgen Sie diesen Leitlinien für reibungslose Auszahlungsoperationen:

- **Verarbeiten Sie Auszahlungen nach Plan** — Verarbeiten Sie alle qualifizierten Auszahlungen am selben Tag jede Woche/monatlich
- **Überprüfen Sie die Details vor der Verarbeitung** — Doppelprüfen Sie die Zahlungsinformationen des Affiliates, insbesondere bei großen Beträgen
- **Überwachen Sie den Anbieterkontostand** — Stellen Sie sicher, dass genügend Mittel auf Ihrem PayPal/Airwallex-Konto vorhanden sind
- **Setzen Sie klare Mindestschwellen** — Kommunizieren Sie Mindestauszahlungsbeträge in den Programmbestimmungen ($50-$100 typisch)
- **Dokumentieren Sie Ihren Plan** — Fügen Sie den Auszahlungsplan in die Affiliate-Bestimmungen und Portal-Einstellungen hinzu
- **Verwenden Sie Anbieterverarbeitung** — Vermeiden Sie manuelle Verarbeitung, es sei denn, es ist unbedingt erforderlich
- **Überprüfen Sie fehlgeschlagene Auszahlungen sofort** — Beheben Sie Fehler innerhalb von 24 Stunden
- **Behalten Sie Webhooks des Anbieters konfiguriert** — Webhooks ermöglichen automatische Statusaktualisierungen
- **Exportieren Sie Auszahlungsberichte regelmäßig** — Laden Sie monatliche Berichte für die Buchhaltung herunter

## Auszahlungsverläufe und Berichte

Jede Auszahlung erstellt ein unveränderliches Verlauf mit:
- Affiliate-Informationen
- Enthaltene Kommissions-IDs
- Gesamtbetrag
- Zahlungsmethode und Anbieter
- Erstellungs- und Abschlusszeitenstempel
- Anbieter-Transaktions-ID (nach Verarbeitung)
- Anbieter-Antwortdaten (für Debugging)
- Interne Notizen

Sie können diese Daten durch Klicken auf jede Auszahlung in der Liste abrufen. Verwenden Sie die Exportfunktion des Admin-Interfaces, um Auszahlungsberichte für Buchhaltung oder Steuerzwecke herunterzuladen.

## Tipps

- Verarbeiten Sie Auszahlungen zu einem festen Zeitpunkt (z. B. jeden Freitag um 14:00 Uhr), damit die Affiliates wissen, wann sie mit der Zahlung rechnen können.
- Verwenden Sie immer die Anbieterverarbeitung anstelle der manuellen Verarbeitung — sie ist schneller, zuverlässiger und erstellt bessere Prüfprotokolle.
- Setzen Sie Mindestschwellen für Auszahlungen in Ihren Programmen, um den administrativen Aufwand zu reduzieren — $50 oder $100 sind Standard.
- Überwachen Sie den Kontostand Ihres Anbieterkontos vor der Verarbeitung großer Batches, um Fehlschläge zu vermeiden.
- Testen Sie Ihre Auszahlungsintegration im Sandbox-Modus, bevor Sie mit echten Zahlungen live gehen.
- Fügen Sie zu jeder Auszahlung eine Notiz hinzu, die erklärt, welchen Zeitraum sie abdeckt (z. B. "Kommissionen für Januar 2026").
- Prüfen Sie fehlgeschlagene Auszahlungen sofort — Verzögerungen frustrieren Affiliates und schädigen das Vertrauen.
- Kommunizieren Sie Verzögerungen proaktiv — wenn Sie nicht pünktlich verarbeiten können, benachrichtigen Sie betroffene Affiliates im Voraus.

