---
title: Zahlungseinstellungen
---

Zahlungsdienstanbieter verbinden Ihr Geschäft mit Zahlungsabwicklern, damit Sie Kreditkarten, digitale Geldbörsen und andere Zahlungsmethoden am Kasse akzeptieren können. Spwig unterstützt mehrere Anbieter gleichzeitig und bietet Ihren Kunden flexible Zahlungsoptionen.

![Zahlungsdienstanbieter](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Verfügbare Anbieter

| Anbieter | Beschreibung |
|----------|-------------|
| **Stripe** | Kreditkarten, Apple Pay, Google Pay und 135+ Währungen |
| **PayPal** | PayPal-Konto, Kredit-/Debitkarten und Optionen zur späteren Zahlung |
| **Airwallex** | Mehrwährungszahlungen, optimiert für den internationalen Handel |
| **Adyen** | Unternehmensklasse-Zahlungen mit 250+ Zahlungsmethoden weltweit |
| **Square** | Kassenzahlungen und Onlinezahlungen mit integrierter Kassensystem-Unterstützung |
| **Revolut** | Schnelle europäische Zahlungen mit wettbewerbsfähigen Wechselkursen |

## Verbindung eines Anbieters

Navigieren Sie zu **Einstellungen > Zahlungsdienstanbieter** und klicken Sie auf **Verbinden Sie einen Anbieter**, um den Einrichtungsführer zu starten.

### Schritt 1: Anbieter auswählen

Wählen Sie einen der verfügbaren Zahlungsdienstanbieter aus. Jede Karte zeigt die unterstützten Funktionen und Regionen des Anbieters.

### Schritt 2: Einrichtungsanweisungen

Überprüfen Sie den spezifischen Einrichtungsführer des Anbieters. Dies umfasst:
- Wie Sie ein Konto bei dem Anbieter erstellen (falls Sie noch keines haben)
- Wo Sie Ihre API-Anmeldeinformationen im Dashboard des Anbieters finden
- Jede Voraussetzung (z. B. Geschäftsverifikation)

### Schritt 3: Anmeldeinformationen eingeben

Geben Sie Ihre API-Anmeldeinformationen ein:
- **API-Schlüssel / Geheimnis-Schlüssel** — Ihre Authentifizierungsanmeldeinformationen aus dem Dashboard des Anbieters
- **Zahlungsmodus** — Wählen Sie, wie Kunden mit dem Zahlungsformular interagieren:

| Modus | Beschreibung |
|------|-------------|
| **Hosted** | Kunden werden zur Zahlungsseite des Anbieters weitergeleitet (z. B. Stripe Checkout). Einfachste Einrichtung, PCI-Konformität wird vom Anbieter übernommen. |
| **Integrated** | Das Zahlungsformular wird direkt in Ihre Kasse integriert. Nahtlose Erfahrung, erfordert jedoch das JavaScript-SDK des Anbieters. |

- **Sandbox / Live-Modus** — Beginnen Sie im Sandbox-Modus für Tests, wechseln Sie dann in den Live-Modus, wenn Sie bereit sind

### Schritt 4: Verbindung testen

Klicken Sie auf **Verbindung testen**, um zu überprüfen, ob Ihre Anmeldeinformationen gültig sind. Der Assistent überprüft:
- API-Schlüssel-Authentifizierung
- Kontoberechtigungen
- Zugänglichkeit des Webhook-Endpunkts

### Schritt 5: Konfigurieren und Speichern

Finalisieren Sie die Einstellungen des Anbieters:
- **Aktiv** — Aktivieren oder Deaktivieren Sie den Anbieter
- **Standard-Anbieter** — Legen Sie ihn als primäre Zahlungsmethode am Kasse fest
- **Anzeigename** — Der Name, der während des Zahlungsvorgangs den Kunden angezeigt wird
- **Sortierreihenfolge** — Steuert die Reihenfolge, in der Anbieter am Kasse angezeigt werden (niedrigere Zahlen werden zuerst angezeigt)

## Zahlungs-Dashboard

Navigieren Sie zu **Einstellungen > Zahlungs-Dashboard**, um einen Überblick über Ihre Zahlungstätigkeit zu erhalten:

### Aktionen erforderlich

Warnkarten oben weisen Probleme, die Aufmerksamkeit erfordern, hervor:
- **Gescheiterte Transaktionen** — Zahlungen, die nicht verarbeitet werden konnten
- **Ausstehende Erfassungen** — Genehmigte Zahlungen, die auf Erfassung warten
- **Verbindungsfehler** — Anbieter mit Verbindungsproblemen

### Umsatzanalyse

- **Umsatzdiagramm** — Visuelle Aufschlüsselung des Zahlungsvolumens im Laufe der Zeit, gruppiert nach Tag, Woche oder Monat
- **Leistungsindikatoren** — Gesamtumsatz, Erfolgsquote, Durchschnittswert einer Transaktion und Rückerstattungsquote
- **Anbietervergleich** — Nebeneinanderliegende Leistungsanzeigen für jeden verbundenen Anbieter

### Transaktionsaufschlüsselung

- **Statusverteilung** — Anzahl der abgeschlossenen, ausstehenden, gescheiterten und zurückerstatteten Transaktionen
- **Zahlungsmethodenmix** — Welche Zahlungsmethoden Kunden am häufigsten verwenden (Kreditkarte, PayPal, digitale Geldbörsen)

## Verwaltung von Zahlungsmethoden

Jeder Anbieter unterstützt unterschiedliche Zahlungsmethoden. Sie können bestimmte Methoden pro Land aktivieren oder deaktivieren:

1. Navigieren Sie zu der Konfigurationsseite eines Anbieters
2. Scrollen Sie zu dem Abschnitt **Zahlungsmethoden**
3. Schalten Sie einzelne Methoden an oder aus
4. Verwenden Sie Steuerelemente auf Landesebene, um Methoden auf bestimmte Märkte zu beschränken

Dies ist nützlich, wenn eine Zahlungsmethode in einem Gebiet beliebt ist, aber in einem anderen nicht (z. B. iDEAL in den Niederlanden, Bancontact in Belgien).

## Webhooks

Webhooks halten Ihr Geschäft in Echtzeit mit dem Zahlungsdienstanbieter synchron. Sie verarbeiten Ereignisse wie:
- Zahlung abgeschlossen oder gescheitert
- Rückerstattungen verarbeitet
- Streitigkeiten und Rückbuchungen geöffnet
- Abonnementverlängerungen

### Automatische Einrichtung

Wenn Sie einen Anbieter verbinden, registriert Spwig automatisch einen Webhook-Endpunkt bei dem Anbieter. Die Webhook-URL wird auf der Konfigurationsseite des Anbieters angezeigt, um sich als Referenz zu dienen.

### Webhook-Überwachung

Jeder eingehende Webhook wird mit protokolliert:
- **Ereignistyp** (z. B. payment_intent.succeeded)
- **Zeitstempel** und Verarbeitungsstatus
- **Nutzlast** für Debugging

Wenn ein Webhook nicht verarbeitet werden kann, wird er als Fehler protokolliert, damit Sie ihn untersuchen können.

## Mehrere Anbieter verwenden

Sie können mehrere Zahlungsdienstanbieter gleichzeitig verbinden:

- **Standard-Anbieter** — Der Anbieter, der standardmäßig am Kasse ausgewählt ist. Markieren Sie einen Anbieter als Standard in seiner Konfiguration.
- **Sortierreihenfolge** — Steuert die Anzeigereihenfolge am Kasse. Kunden sehen alle aktiven Anbieter und können ihre bevorzugte Methode auswählen.
- **Ausfallsicherung** — Wenn ein Anbieter Ausfallzeiten hat, können Kunden immer noch mit einem alternativen Anbieter zahlen.

## Tipps

- Beginnen Sie mit **Stripe** oder **PayPal** — sie decken den breitesten Zahlungsmethoden- und Regionenbereich ab.
- Verwenden Sie **Sandbox/Test-Modus**, um Testtransaktionen zu verarbeiten, bevor Sie live gehen. Jeder Anbieter hat in seiner Dokumentation Testkartennummern.
- Aktivieren Sie **mehrere Anbieter**, damit Kunden eine Backup-Zahlungsoption haben, wenn ein Anbieter Probleme hat.
- Legen Sie eine **niedrige Sortierreihenfolge** für Ihren bevorzugten Anbieter fest, damit er am Kasse zuerst angezeigt wird.
- Überprüfen Sie das Zahlungs-Dashboard wöchentlich, um gescheiterte Transaktionen und Verbindungsprobleme frühzeitig zu erkennen.
- Bewahren Sie Ihre API-Anmeldeinformationen sicher auf — sie werden im Datenbank verschlüsselt gespeichert, sollten aber niemals geteilt werden.