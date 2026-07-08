---
title: Auszahlungsanbieter-Setup
---

Das Auszahlungsanbieter-Setup ermöglicht die Konfiguration von PayPal und Airwallex für automatisierte Affiliate-Auszahlungen. Dieser Leitfaden zeigt Ihnen, wie Sie Ihre Konten bei den Auszahlungsanbietern verbinden, Webhooks konfigurieren und Ihre Integration testen.

## Unterstützte Auszahlungsanbieter

Spwig integriert sich mit zwei Auszahlungsanbietern, um Affiliate-Auszahlungen zu automatisieren:

| Anbieter | Zahlungsmethode | Verarbeitung | Batch-Unterstützung | Bestens geeignet für |
|----------|----------------|------------|---------------|----------|
| **PayPal** | PayPal-Kontoumsätze | API-basiert | Ja (bis zu 15.000) | Die meisten Affiliates, globale Reichweite |
| **Airwallex** | Internationale Banküberweisungen | API-basiert | Nein (individuell) | Banküberweisungen, internationale Zahlungen |

### Wichtige Unterschiede

**PayPal-Auszahlungen**:
- Erfordert, dass der Affiliate ein PayPal-Konto (Zahlungsemail) besitzt
- Verarbeitet Batches von bis zu 15.000 Auszahlungen auf einmal
- Schnellere Verarbeitung (1-2 Geschäftstage)
- Geringere Einrichtungskomplexität
- Gebühren: ~2 % oder 0,25–1,00 USD pro Zahlung
- Einzelner Webhook für den gesamten Batch

**Airwallex**:
- Unterstützt direkte Banküberweisungen
- Verarbeitet individuelle Auszahlungen einzeln
- Längere Verarbeitung (2–5 Geschäftstage)
- Unterstützt mehrere Währungen und Länder
- Gebühren variieren je nach Ziel-Land
- Individueller Webhook pro Auszahlung

Sie können beide Anbieter konfigurieren und den Affiliates die von ihnen bevorzugte Zahlungsmethode überlassen.

## Warum Auszahlungsanbieter verwenden?

Die Integration von Zahlungsanbietern bietet erhebliche Vorteile gegenüber manuellen Zahlungen:

- **Automatisierte Verarbeitung** — Keine manuelle Dateneingabe oder Zahlungsausführung
- **Batch-Effizienz** — Verarbeiten Sie Dutzende oder Hunderte von Auszahlungen mit einem Klick
- **Webhook-Bestätigungen** — Automatische Statusaktualisierungen, wenn Zahlungen abgeschlossen sind
- **Geringere Fehler** — Das System validiert Kontodetails vor der Verarbeitung
- **Audit-Trail** — Vollständige Aufzeichnung von Transaktionen und Anbieterantworten
- **Schnellere Zahlungen** — Affiliates erhalten Geld schneller
- **Skalierbarkeit** — Verwalten Sie wachsende Affiliate-Programme ohne proportionalen Verwaltungsarbeit

Ohne Anbieterintegration müssen Sie jede Zahlung manuell über Ihr Bankkonto oder das PayPal-Dashboard verarbeiten und anschließend zu Spwig zurückkehren, um die Auszahlungen als abgeschlossen zu markieren.

## PayPal-Setup

Folgen Sie diesen Schritten, um PayPal-Auszahlungen für automatisierte Affiliate-Zahlungen zu konfigurieren.

### Voraussetzungen

Bevor Sie beginnen, benötigen Sie:
- Ein PayPal Business-Konto (persönliche Konten können die Auszahlungs-API nicht verwenden)
- Zugang zum PayPal Developer Dashboard
- Produktionsgenehmigung für die Auszahlungs-API (nach Sandboxed-Tests)

### Schritt 1: PayPal-App erstellen

1. **Navigieren Sie** zu [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. **Melden Sie sich** mit Ihrem PayPal Business-Konto an
3. **Klicken Sie** auf **My Apps & Credentials** in der linken Seitenleiste
4. **Wählen Sie** den **Live**-Reiter (oder Sandbox für Tests)
5. **Klicken Sie** auf **Create App**
6. **Geben Sie einen App-Namen** ein (z. B. "Spwig Affiliate Payouts")
7. **Wählen Sie den App-Typ**: Merchant
8. **Klicken Sie** auf **Create App**

PayPal generiert Ihre Anmeldeinformationen.

### Schritt 2: API-Anmeldeinformationen abrufen

Nachdem Sie die App erstellt haben:

1. **Kopieren Sie Client ID** — Langer alphanumerischer String
2. **Klicken Sie** auf **Show** unter Secret
3. **Kopieren Sie Client Secret** — Bewahren Sie dies vertraulich auf
4. **Notieren Sie den Modus** — Sandbox oder Live

### Schritt 3: Auszahlungsfunktion aktivieren

PayPal-Apps benötigen eine explizite Genehmigung, um Auszahlungen zu verwenden:

1. **Scrollen Sie** zu dem Abschnitt **Features** in Ihrer App
2. **Suchen Sie** nach der Funktion **Payouts**
3. **Klicken Sie** auf **Add**, wenn sie noch nicht aktiviert ist
4. **Einreichen zur Genehmigung**, wenn Sie den Live-Modus verwenden (Genehmigung dauert 1–2 Geschäftstage)

### Schritt 4: Anbieter in Spwig hinzufügen

Fügen Sie jetzt das PayPal-Konto in Spwig hinzu:

1. **Navigieren Sie** zu **Settings > Payout Providers**
2. **Klicken Sie** auf **+ Add PayPal Account**
3. **Füllen Sie das Formular** aus:
   - **Account Name**: Beschreibender Bezeichner (z. B. "Main PayPal Account")
   - **Client ID**: Fügen Sie aus dem PayPal Developer Dashboard ein
   - **Client Secret**: Fügen Sie aus dem PayPal Developer Dashboard ein
   - **Modus**: Wählen Sie Sandbox (Test) oder Production (Live)
   - **Is Active**: Ankreuzen, um zu aktivieren
4. **Klicken Sie auf Save**

Spwig validiert die Anmeldeinformationen, indem er einen Zugriffstoken anfordert. Wenn die Validierung fehlschlägt, überprüfen Sie nochmals Ihre Client ID und Secret.

### Schritt 5: Verbindung testen

Überprüfen Sie Ihre PayPal-Integration:

1. Erstellen Sie eine Testauszahlung in **Affiliate Program > Payouts**
2. Verwenden Sie Ihre eigene PayPal-E-Mail als Empfänger
3. Setzen Sie den Betrag auf $0,01 (wenn in Production) oder beliebigen Betrag (wenn Sandbox)
4. Verarbeiten Sie mit Anbieter
5. Überprüfen Sie das PayPal-Konto auf eingehende Zahlung
6. Bestätigen Sie, dass der Webhook den Auszahlungsstatus in Spwig aktualisiert

Wenn Sie den Sandbox-Modus verwenden, erstellen Sie ein Test-PayPal-Konto auf [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts), um Testauszahlungen zu empfangen.

## Airwallex-Setup

Airwallex unterstützt internationale Banküberweisungen für Affiliates, die direkte Einzahlung bevorzugen.

### Voraussetzungen

Bevor Sie beginnen, benötigen Sie:
- Ein Airwallex-Konto (erstellen Sie es auf [airwallex.com](https://www.airwallex.com))
- Bestätigte Geschäftsstatus
- Aktiviertes API-Zugriff (wenden Sie sich bei Bedarf an den Airwallex-Support)
- Ausreichendes Guthaben auf Ihrem Airwallex-Konto

### Schritt 1: API-Anmeldeinformationen generieren

1. **Melden Sie sich** bei [Airwallex Dashboard](https://www.airwallex.com/app/) an
2. **Navigieren Sie** zu **Settings > API Keys**
3. **Klicken Sie** auf **Create API Key**
4. **Geben Sie eine Beschreibung** ein: "Spwig Affiliate Payouts"
5. **Wählen Sie Berechtigungen**: Aktivieren Sie **Payouts** (Lesen und Schreiben)
6. **Klicken Sie** auf **Generate**
7. **Kopieren Sie API Key** — Wird nur einmal angezeigt
8. **Kopieren Sie Client ID** — Wird mit dem Schlüssel angezeigt

### Schritt 2: Ihr Umfeld notieren

Airwallex bietet zwei Umgebungen:

- **Demo**: Für Tests mit fiktiven Transaktionen
- **Production**: Für echte Geldüberweisungen

Stellen Sie sicher, dass Sie wissen, zu welcher Umgebung Ihr API-Schlüssel gehört.

### Schritt 3: Anbieter in Spwig hinzufügen

Fügen Sie das Airwallex-Konto in Spwig hinzu:

1. **Navigieren Sie** zu **Settings > Payout Providers**
2. **Klicken Sie** auf **+ Add Airwallex Account**
3. **Füllen Sie das Formular** aus:
   - **Account Name**: Beschreibender Bezeichner (z. B. "Airwallex EUR Account")
   - **API Key**: Fügen Sie aus dem Airwallex-Dashboard ein
   - **Client ID**: Fügen Sie aus dem Airwallex-Dashboard ein
   - **Umgebung**: Wählen Sie Demo oder Production
   - **Is Active**: Ankreuzen, um zu aktivieren
4. **Klicken Sie auf Save**

Spwig validiert die Anmeldeinformationen, indem er Ihre Kontostand abfragt.

### Schritt 4: Unterstützte Länder überprüfen

Airwallex unterstützt Überweisungen an viele Länder, aber nicht alle. Überprüfen Sie die Seite [Airwallex coverage](https://www.airwallex.com/global-business-account/global-transfers), um sicherzustellen, dass die Länder Ihrer Affiliates unterstützt werden.

Gemeinsam unterstützte Länder umfassen:
- Vereinigte Staaten
- Vereinigtes Königreich
- Länder der Europäischen Union
- Australien
- Kanada
- Singapur
- Hong Kong

### Schritt 5: Banküberweisung testen

Testen Sie Ihre Airwallex-Integration:

1. Erstellen Sie eine Testauszahlung für einen Affiliate mit Bankdaten
2. Verwenden Sie einen kleinen Betrag ($1–$5), wenn Sie sich im Production-Modus befinden
3. Verarbeiten Sie mit Anbieter
4. Überprüfen Sie das Airwallex-Dashboard auf die Transaktion
5. Warten Sie auf die Webhook-Bestätigung
6. Bestätigen Sie, dass die Auszahlung in Spwig abgeschlossen ist

Der Demo-Modus verarbeitet sofort. Der Production-Modus benötigt 2–5 Geschäftstage.

## Logik zur Anbieterauswahl

Wenn Sie eine Auszahlung verarbeiten, wählt Spwig automatisch den passenden Anbieter basierend auf der Zahlungsmethode des Affiliates.

### Auswahlablauf

1. **Überprüfen Sie die Zahlungsmethode des Affiliates**:
   - Wenn `payment_email` festgelegt ist → Affiliate bevorzugt PayPal
   - Wenn Bankdaten festgelegt sind → Affiliate bevorzugt Banküberweisung
2. **Zu Anbieter zuordnen**:
   - PayPal-E-Mail → Verwenden Sie das aktive PayPal-Anbieterkonto
   - Bankdaten → Verwenden Sie das aktive Airwallex-Anbieterkonto
3. **Zurückfallen auf den ersten verfügbaren Anbieter**, wenn der bevorzugte Anbieter nicht konfiguriert ist
4. **Fehler anzeigen**, wenn kein passender Anbieter vorhanden ist

### Mehrere Anbieterkonten

Sie können mehrere Konten für denselben Anbieter konfigurieren (z. B. zwei PayPal-Konten für verschiedene Regionen). Spwig wählt das erste aktive Konto, das der Zahlungsmethode entspricht. Um zu steuern, welches Konto verwendet wird, ordnen Sie sie in der Admin-Liste um oder setzen Sie nur eines als aktiv.

## Testen der Auszahlungsintegration

Testen Sie immer Ihre Anbieterintegration, bevor Sie Live-Zahlungen an Affiliates verarbeiten.

### Testen im Sandbox/Demo-Modus

1. **Setzen Sie den Anbieter auf Sandbox-Modus** (PayPal Sandbox oder Airwallex Demo)
2. **Erstellen Sie einen Test-Affiliate** mit Testzahlungsdetails
3. **Erstellen Sie Testkommissionen** und genehmigen Sie sie
4. **Erstellen Sie eine Testauszahlung**, die diese Kommissionen einschließt
5. **Verarbeiten Sie mit Anbieter** über das Aktionenmenü
6. **Überwachen Sie Celery-Protokolle** für API-Anfragen
7. **Überprüfen Sie das Anbieter-Dashboard** auf die Transaktion
8. **Warten Sie auf den Webhook**, um den Auszahlungsstatus zu aktualisieren
9. **Bestätigen Sie, dass die Kommissionen als bezahlt markiert sind**

### Produktions-Test

Bevor Sie live gehen:

1. **Wechseln Sie in den Produktionsmodus** in den Anbietereinstellungen
2. **Erstellen Sie eine kleine Testauszahlung** an sich selbst ($0,01–$1,00)
3. **Verarbeiten Sie sie** und warten Sie auf Abschluss
4. **Bestätigen Sie, dass das Geld auf Ihrem eigenen Konto empfangen wurde**
5. **Überprüfen Sie, ob der Webhook ausgelöst wurde** und den Status aktualisiert hat
6. **Überprüfen Sie die Gebühren des Anbietertransaktions**

### Häufige Testprobleme

| Problem | Ursache | Lösung |
|-------|-------|----------|
| "Ungültige Anmeldeinformationen" | Falscher API-Schlüssel oder Modusmismatch | Überprüfen Sie die Anmeldeinformationen, bestätigen Sie Sandbox vs. Production |
| Webhook wird nie ausgelöst | URL nicht im Anbieter konfiguriert | Fügen Sie Webhook-URL im Anbieter-Dashboard hinzu |
| Auszahlung bleibt in Verarbeitung | Webhook-Signatur fehlgeschlagen | Überprüfen Sie, ob Webhook-Secret übereinstimmt |
| Kein Anbieter verfügbar | Kein aktiver Anbieter für Zahlungsmethode | Aktivieren Sie mindestens ein Anbieterkonto |

## Batchverarbeitung (PayPal)

PayPal unterstützt Batchverarbeitung für Effizienz und Kosteneinsparungen.

### Wie Batchverarbeitung funktioniert

Wenn Sie mehrere Auszahlungen auswählen und auf **Mit Anbieter verarbeiten** klicken:

1. Spwig gruppiert alle PayPal-Auszahlungen in einen einzelnen Batch
2. Das System sendet eine einzelne API-Anfrage mit allen Auszahlungsdetails (bis zu 15.000)
3. PayPal verarbeitet den gesamten Batch als eine einzelne Transaktion
4. Der Webhook gibt mit Batch-Ergebnissen zurück
5. Spwig aktualisiert alle Auszahlungen basierend auf der Batch-Antwort

### Vorteile der Batchverarbeitung

- **Reduzierte API-Aufrufe** — Eine Anfrage für Hunderte von Auszahlungen
- **Geringere Gebühren** — Einige PayPal-Gebührenstruktur bevorzugen Batchverarbeitung
- **Schnellere Verarbeitung** — Parallele Ausführung für den gesamten Batch
- **Einzelner Webhook** — Einfacheres Monitoring und Logging

### Batchgrenzen

PayPal legt diese Grenzen fest:
- Maximal 15.000 Empfänger pro Batch
- Maximal $100.000 Gesamtsumme pro Batch
- Verarbeitung erfolgt in der Regel innerhalb von Minuten

Wenn Sie mehr als 15.000 Auszahlungen haben, teilt Spwig automatisch in mehrere Batches auf.

## Einzelverarbeitung (Airwallex)

Airwallex verarbeitet Auszahlungen einzeln, was andere Kompromisse bietet.

### Wie Einzelverarbeitung funktioniert

Wenn Sie Airwallex-Auszahlungen verarbeiten:

1. Das System sendet separate API-Anfrage für jede Auszahlung
2. Airwallex stellt Überweisungen einzeln in die Warteschlange
3. Jede Überweisung wird unabhängig abgeschlossen (2–5 Tage)
4. Einzelner Webhook wird ausgelöst, wenn jede Überweisung abgeschlossen ist
5. Spwig aktualisiert Auszahlungen, sobald Webhooks eintreffen

### Vorteile der Einzelverarbeitung

- **Bessere Fehlerisolation** — Ein Fehler blockiert keine anderen
- **Pro-Auszahlung-Tracking** — Individuelle Transaktions-IDs
- **Mehr Zahlungsdetails** — Bank-spezifische Informationen pro Überweisung
- **Flexiblerer Zeitplan** — Überweisungen werden zu unterschiedlichen Zeiten abgeschlossen

### Verarbeitungszeit

Im Gegensatz zur sofortigen Batchverarbeitung von PayPal benötigen Airwallex-Überweisungen länger:
- Nationale Überweisungen: 1–2 Geschäftstage
- Internationale Überweisungen: 3–5 Geschäftstage
- Einige Länder: Bis zu 7 Geschäftstage

Passen Sie die Erwartungen der Affiliates entsprechend in Ihre Programmbestimmungen an.

## Webhook-Konfiguration

Webhooks ermöglichen automatische Aktualisierungen des Auszahlungsstatus, wenn Anbieter Transaktionen abschließen.

### Webhook-URL-Format

Konfigurieren Sie diese URL in Ihrem Anbieter-Dashboard:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Ersetzen Sie `{provider}` mit:
- `paypal` für PayPal-Webhooks
- `airwallex` für Airwallex-Webhooks

Beispiele:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### PayPal-Webhook-Setup

1. **Navigieren Sie** zu [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. **Klicken Sie** auf Ihren App-Namen
3. **Scrollen Sie** zu dem Abschnitt **Webhooks**
4. **Klicken Sie** auf **Add Webhook**
5. **Geben Sie die Webhook-URL** ein (Format oben)
6. **Wählen Sie Ereignisse**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Klicken Sie auf Save**

PayPal stellt einen Webhook-Unterschriftsschlüssel bereit. Spwig verwendet diesen, um die Authentizität des Webhooks zu überprüfen.

### Airwallex-Webhook-Setup

1. **Navigieren Sie** zu [Airwallex Dashboard](https://www.airwallex.com/app/)
2. **Gehen Sie zu** **Settings > Webhooks**
3. **Klicken Sie** auf **Create Webhook**
4. **Geben Sie die Webhook-URL** ein (Format oben)
5. **Wählen Sie Ereignisse**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Klicken Sie auf Create**

Airwallex signiert Webhooks mit Ihrem API-Geheimnis.

### Webhook-Sicherheit

Webhooks werden mit diesen Mechanismen validiert:

- **Signaturüberprüfung** — Der Anbieter signiert den Webhook-Inhalt mit dem Geheimnischlüssel
- **Zeitstempelprüfung** — Alte Webhooks werden abgelehnt (verhindert Wiederholungsangriffe)
- **IP-Whitelist (optional)** — Einschränkung auf Anbieter-IP-Bereiche
- **HTTPS erforderlich** — Webhooks funktionieren nur über SSL

Deaktivieren Sie niemals die Signaturüberprüfung in der Produktion.

### Webhook-Testen

Die meisten Anbieter bieten Werkzeuge zum Testen von Webhooks an:

**PayPal**: Verwenden Sie den "Simulator" im Developer Dashboard, um Test-Webhooks auszulösen

**Airwallex**: Erstellen Sie eine Testüberweisung im Demo-Modus und beobachten Sie den Webhook

Sie können auch Webhook-Protokolle in Spwig unter **Settings > System Logs** überprüfen (wenn Logging aktiviert ist).

## Problembehandlung

### Fehler bei ungültigen Anmeldeinformationen

**Symptom**: "Authentifizierung fehlgeschlagen", wenn Sie das Anbieterkonto speichern

**Ursachen**:
- Falsche Client ID oder Secret
- Sandbox-Anmeldeinformationen werden in Production-Modus verwendet (oder umgekehrt)
- API-Schlüssel abgelaufen oder widerrufen
- Konto nicht bestätigt

**Lösungen**:
- Kopieren Sie die Anmeldeinformationen erneut aus dem Anbieter-Dashboard
- Bestätigen Sie, dass der Modus übereinstimmt (Sandbox vs. Production)
- Erstellen Sie neue API-Schlüssel
- Kontaktieren Sie den Anbieter-Support, um den Kontostatus zu bestätigen

### Webhook nicht empfangen

**Symptom**: Auszahlung bleibt im Status "Verarbeitung" unbegrenzt

**Ursachen**:
- Webhook-URL nicht in Anbieter-Dashboard konfiguriert
- Ungültiges SSL-Zertifikat
- Firewall blockiert Anbieter-IPs
- Webhook-Signaturvalidierung fehlgeschlagen

**Lösungen**:
- Überprüfen Sie die Webhook-URL in den Anbietereinstellungen erneut
- Bestätigen Sie, dass das SSL-Zertifikat gültig ist
- Whitelisten Sie Anbieter-IP-Bereiche in der Firewall
- Überprüfen Sie Celery-Protokolle auf Signaturfehler
- Testen Sie Webhook mit dem Simulator-Tool des Anbieters

### Auszahlung fehlgeschlagen

**Symptom**: Der Auszahlungsstatus ändert sich in "Fehlgeschlagen" mit einer Fehlermeldung

**Ursachen**:
- Ungültige Zahlungsdetails des Affiliates (falsche E-Mail oder Bankkontonummer)
- Unzureichendes Guthaben auf dem Anbieterkonto
- Empfänger-Konto kann keine Zahlungen empfangen
- Land nicht unterstützt (Airwallex)
- Auszahlung überschreitet Anbietergrenzen

**Lösungen**:
- Überprüfen Sie den Fehler im Feld **Anbieterantwort**
- Bestätigen Sie, dass die Zahlungsdetails des Affiliates korrekt sind
- Fügen Sie Guthaben auf dem Anbieterkonto hinzu
- Bitte den Affiliate, seinen Kontostatus zu überprüfen
- Überprüfen Sie die Länder- und Währungsunterstützung des Anbieters
- Teilen Sie große Auszahlungen, wenn sie die Grenzen überschreiten

### Modusmismatch

**Symptom**: Testauszahlungen funktionieren, aber Produktionsauszahlungen fehlschlagen

**Ursachen**:
- Anbieter ist auf Sandbox-Modus eingestellt, aber mit Produktionsaffiliate-Konten verwendet
- API-Anmeldeinformationen stammen aus falschem Umfeld

**Lösungen**:
- Wechseln Sie den Anbietermodus auf Production
- Erstellen Sie neue Produktions-API-Anmeldeinformationen
- Bestätigen Sie, dass die Webhook-URL auf Produktionsdomain verweist

## Sicherheitsbest Practices

Schützen Sie Ihre Auszahlungsintegration mit diesen Sicherheitsmaßnahmen:

### Anmeldeinformationenspeicherung

- **Kommitten Sie Anmeldeinformationen nie in die Versionskontrolle** — Verwenden Sie Umgebungsvariablen oder sicheren Speicher
- **Drehen Sie API-Schlüssel alle drei Monate** — Generieren Sie neue Schlüssel alle drei Monate
- **Verwenden Sie separate Schlüssel für Sandbox und Production** — Mischen Sie niemals Umgebungen
- **Beschränken Sie API-Berechtigungen** — Gewähren Sie nur Zugriff auf Auszahlungen, nicht auf vollständige Kontokontrolle

Spwig speichert Anbieteranmeldeinformationen im Datenbank verschlüsselt. Bewahren Sie Ihre Datenbank-Backups sicher auf.

### Webhook-Sicherheit

- **Überprüfen Sie immer Signaturen** — Vermeiden Sie niemals die Signaturvalidierung
- **Verwenden Sie ausschließlich HTTPS** — HTTP-Webhooks werden nicht unterstützt
- **Implementieren Sie IP-Whitelist** — Einschränkung auf Anbieter-IP-Bereiche
- **Protokollieren Sie alle Webhooks** — Überwachen Sie auf verdächtige Aktivitäten
- **Implementieren Sie Rate-Limiting für Webhook-Endpunkte** — Verhindern Sie Missbrauch

### Zugriffssteuerung

- **Beschränken Sie den Zugriff für Mitarbeiter** — Nur vertrauenswürdige Mitarbeiter sollten Auszahlungen verarbeiten
- **Verwenden Sie Zwei-Faktor-Authentifizierung** — Erfordern Sie 2FA für Mitarbeiterkonten
- **Überprüfen Sie Auszahlungsaktionen** — Überprüfen Sie, wer welche Auszahlungen verarbeitet hat
- **Trennen Sie Aufgaben** — Verschiedene Mitarbeiter für Genehmigung vs. Verarbeitung

### Überwachung

- **Überprüfen Sie täglich fehlgeschlagene Auszahlungen** — Beheben Sie Probleme schnell
- **Überwachen Sie die Kontostände des Anbieters** — Stellen Sie sicher, dass genügend Geld vorhanden ist
- **Überprüfen Sie Transaktionsprotokolle wöchentlich** — Erkennen Sie Anomalien frühzeitig
- **Richten Sie Benachrichtigungen ein** — E-Mail-Benachrichtigungen für große oder fehlgeschlagene Auszahlungen

## Tipps

- Testen Sie Ihre Integration gründlich im Sandbox-Modus, bevor Sie zu Production wechseln — erkennen Sie Probleme mit fiktivem Geld.
- Konfigurieren Sie sowohl PayPal als auch Airwallex, um Affiliates die Zahlungsmethode ihrer Wahl zu ermöglichen — verschiedene Affiliates bevorzugen verschiedene Methoden.
- Legen Sie Webhook-URLs während der ersten Einrichtung fest und bestätigen Sie, dass sie korrekt ausgelöst werden — Webhooks sind entscheidend für die Automatisierung.
- Halten Sie die Kontostände der Anbieter auf Vordermann, um fehlgeschlagene Auszahlungen während der Batchverarbeitung zu vermeiden.
- Verwenden Sie beschreibende Kontonamen, wenn Sie mehrere Anbieter konfigurieren (z. B. "PayPal USD", "PayPal EUR").
- Drehen Sie API-Anmeldeinformationen alle drei Monate als Sicherheitsbest Practice.
- Dokumentieren Sie Ihre Webhook-URLs und Anmeldeinformationen in einem sicheren Passwort-Manager, der mit Ihrem Team geteilt wird.
- Überwachen Sie fehlgeschlagene Auszahlungen sofort — Verzögerungen frustrieren Affiliates und schädigen das Programmimage.
- Verwenden Sie immer HTTPS für Ihre Spwig-Installation — Webhooks erfordern SSL-Zertifikate.
- Kontaktieren Sie den Anbieter-Support, wenn Sie anhaltende Fehler begegnen — sie können Ihren Kontostatus und Berechtigungen überprüfen.