---
title: E-Mail-Konfiguration
---

E-Mail-Konfiguration steuert, wie Ihr Geschäft transaktionale E-Mails sendet – Bestätigungen, Versandbenachrichtigungen, Passwortzurücksetzungen und mehr. Spwig enthält einen eingebauten SMTP-Server und unterstützt externe E-Mail-Anbieter für eine höhere Zustellbarkeit.

![E-Mail-Konten](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Verfügbare Anbieter

| Anbieter | Beschreibung |
|----------|-------------|
| **Eingebauter SMTP** | Kostengenauer, selbstgehosteter E-Mail-Server, der mit Spwig geliefert wird. Automatische DKIM-Unterschrift. |
| **Gmail API** | Senden Sie über Ihr Gmail- oder Google Workspace-Konto mit OAuth-Authentifizierung. |
| **Allgemeiner SMTP** | Verbinden Sie jeden SMTP-Server (SendGrid, Mailgun, Amazon SES oder Ihren eigenen E-Mail-Server). |

## E-Mail einrichten

Navigieren Sie zu **Einstellungen > E-Mail-Konten** und klicken Sie auf **E-Mail-Konto hinzufügen**, um den Einrichtungsführer zu starten.

### Schritt 1: Anbieter auswählen

Wählen Sie Ihren E-Mail-Anbieter. Der eingebaute SMTP-Server ist die einfachste Option, um zu beginnen – er erfordert keine externen Konten.

### Schritt 2: Anmeldeinformationen konfigurieren

Geben Sie die Anmeldeinformationen für Ihren ausgewählten Anbieter ein:

- **Eingebauter SMTP** – Keine Anmeldeinformationen erforderlich. Der Server läuft auf Ihrer Spwig-Installation.
- **Gmail API** – Authentifizieren Sie sich über Google OAuth. Sie werden zur Anmeldung mit Ihrem Google-Konto umgeleitet.
- **Allgemeiner SMTP** – Geben Sie die SMTP-Server-Adresse, den Port, den Benutzernamen und das Passwort ein.

### Schritt 3: Absenderkonfiguration

Legen Sie die Absenderidentität für ausgehende E-Mails fest:

- **Von-E-Mail** – Die E-Mail-Adresse, die im Feld "Von" angezeigt wird (z. B. orders@yourstore.com)
- **Von-Name** – Der Anzeigename neben der E-Mail-Adresse (z. B. "Ihr Geschäftsnamen")
- **Antworten an E-Mail** – Wo Kundenantworten weitergeleitet werden (kann von der Absenderadresse abweichen)

### Schritt 4: DNS-Validierung

Überprüfen Sie die E-Mail-Authentifizierungsdatensätze Ihres Domains. Der Assistent prüft drei DNS-Datensätze:

| Datensatz | Zweck |
|--------|---------|
| **SPF** | Ermächtigt Ihren Server, E-Mails im Namen Ihres Domains zu senden |
| **DKIM** | Digitale Signatur von E-Mails, um zu beweisen, dass sie nicht manipuliert wurden |
| **DMARC** | Gibt Empfangsserver an, was mit E-Mails geschehen soll, die SPF/DKIM-Prüfungen nicht bestanden haben |

Für jeden Datensatz zeigt der Assistent an:
- **Aktueller Status** – Ob der Datensatz richtig konfiguriert ist
- **Erforderlicher Wert** – Der genaue DNS-Datensatz, den Sie bei Ihrem Domain-Registrierer hinzufügen müssen
- **Verbreitungsstatus** – Ob kürzliche Änderungen wirksam wurden (DNS-Änderungen können bis zu 48 Stunden dauern)

Der eingebaute SMTP-Server generiert automatisch DKIM-Schlüssel für Ihr Domain.

### Schritt 5: Test-E-Mail senden

Senden Sie eine Test-E-Mail, um sicherzustellen, dass alles funktioniert:
1. Geben Sie eine E-Mail-Adresse des Empfängers ein
2. Klicken Sie auf **Test-E-Mail senden**
3. Prüfen Sie Ihren Posteingang auf die Testnachricht
4. Bestätigen Sie, dass die E-Mail ohne Spam-Alarme ankommt

### Schritt 6: Speichern und aktivieren

Speichern Sie die Konfiguration und legen Sie das Konto als aktiv fest. Markieren Sie es als **Standard**, wenn es der primäre E-Mail-Konto sein soll.

## E-Mail-Vorlagen

Spwig enthält über 30 E-Mail-Vorlagen für jedes transaktionale Ereignis. Navigieren Sie zu **Einstellungen > E-Mail-Vorlagen**, um sie zu verwalten.

### Vorlagen-Typen

Vorlagen umfassen alle Geschäftsevents, einschließlich:
- **Bestellzyklus** – Bestätigung, Verarbeitung, versandt, geliefert, abgebrochen
- **Zahlung** – Quittung, Rückerstattungsbestätigung, fehlgeschlagene Zahlung
- **Kundenkonto** – Willkommensnachricht, Passwortzurücksetzung, E-Mail-Bestätigung
- **Gutschein-Karten** – Lieferung, Benachrichtigung über den Kontostand
- **Versand** – Tracking-Updates, Lieferbestätigung
- **Digitale Produkte** – Download-Links, Lizenzschlüssel
- **Marketing** – Wiederherstellung von verwaisten Warenkörben, Bewertungsanfragen

### Vorlagen anpassen

1. Navigieren Sie zur Vorlagenliste
2. Klicken Sie auf eine Vorlage, um sie zu bearbeiten
3. Ändern Sie die Betreffzeile, den Header, den Inhalt und den Footer
4. Verwenden Sie Vorlagenvariablen (z. B. `{{ order.number }}`, `{{ customer.name }}`) für dynamischen Inhalt
5. Vorschau der E-Mail vor dem Speichern

### Mehrsprachige Unterstützung

E-Mail-Vorlagen unterstützen mehrere Sprachen:
- Jede Vorlage kann Übersetzungen für alle aktiven Sprachen Ihres Geschäfts haben
- Das System sendet E-Mails in der bevorzugten Sprache des Kunden
- **Sprachfallbackkette** – Wenn eine Übersetzung nicht verfügbar ist, wechselt das System zur Standard-Sprache Ihres Geschäfts
- Verwenden Sie die **KI-Übersetzung**-Funktion, um Vorlagen automatisch in andere Sprachen zu übersetzen

### Vorlagen klonen

Um eine benutzerdefinierte Version eines Systemvorlagen zu erstellen:
1. Öffnen Sie die Vorlage, die Sie bearbeiten möchten
2. Klicken Sie auf **Vorlage klonen**
3. Bearbeiten Sie die geklonte Version
4. Die Kopie hat Vorrang vor der ursprünglichen Systemvorlage

## E-Mail-Warteschlange

Überwachen Sie ausgehende E-Mails unter **Einstellungen > E-Mail-Warteschlange**:

- **In Warteschlange** – E-Mails, die zum Senden warten
- **Wird gesendet** – Wird derzeit übertragen
- **Gesendet** – Erfolgreich zugestellt
- **Fehlgeschlagen** – Konnte nicht zugestellt werden (mit Fehlerinformationen)
- **Zurückgewiesen** – Von der Empfänger-Email-Server abgelehnt

Klicken Sie auf eine E-Mail, um deren vollständige Details anzuzeigen, einschließlich Empfänger, Betreff, Sendezzeit und Zustellstatus.

## Zustellverfolgung

Verfolgen Sie E-Mail-Engagement:
- **Öffnungen** – Wie viele Empfänger die E-Mail geöffnet haben
- **Klicks** – Linkklicks innerhalb der E-Mail
- **Zurückgewiesen** – Verfolgung von harten und weichen Zurückweisungen
- **Beschwerden** – Spam-Berichte von Empfängern

## Mehrere Konten

Sie können mehrere E-Mail-Konten konfigurieren:
- **Standardkonto** – Wird für alle ausgehenden E-Mails verwendet, es sei denn, es wird überschrieben
- **Zurückfall** – Wenn das Standardkonto fehlschlägt, werden E-Mails in die Warteschlange gestellt, um erneut versendet zu werden
- Verwenden Sie verschiedene Konten für verschiedene Zwecke (z. B. eines für transaktionale E-Mails, ein anderes für Marketing)

## Tipps

- Beginnen Sie mit dem **eingebauten SMTP**-Server für eine schnelle Einrichtung, wechseln Sie dann zu einem externen Anbieter, wenn Sie höhere Versandvolumina oder bessere Zustellbarkeit benötigen.
- Konfigurieren Sie immer **SPF, DKIM und DMARC**-Datensätze – ohne sie landen E-Mails viel wahrscheinlicher in Spam-Ordner.
- Senden Sie eine **Test-E-Mail** nach jeder Konfigurationsänderung, um sicherzustellen, dass die Zustellung funktioniert.
- Überwachen Sie regelmäßig die E-Mail-Warteschlange auf **fehlgeschlagene** oder **zurückgewiesene** E-Mails – diese deuten auf Zustellprobleme hin.
- Verwenden Sie eine **professionelle Absenderadresse** (z. B. orders@yourstore.com) anstelle einer kostenlosen E-Mail-Adresse für bessere Vertrauenswürdigkeit und Zustellbarkeit.
- Halten Sie Ihre Vorlagen kurz – transaktionale E-Mails sollten Informationen schnell liefern, nicht als Marketing-Newsletter dienen.