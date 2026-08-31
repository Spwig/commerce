---
title: E-Mail-Konfiguration
---

Die E-Mail-Konfiguration steuert, wie Ihr Geschäft transaktionsbezogene E-Mails versendet – Bestätigungen zu Bestellungen, Versandbenachrichtigungen, Passwortwiederherstellung und vieles mehr. Spwig verfügt über einen integrierten SMTP-Server und unterstützt externe E-Mail-Anbieter für eine höhere Zustellbarkeit.

![E-Mail-Konten](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Verfügbare Anbieter

| Anbieter | Beschreibung |
|----------|-------------|
| **Integrierter SMTP** | Kostenlos, selbst gehosteter E-Mail-Server, der mit Spwig geliefert wird. Automatische DKIM-Signatur. |
| **Gmail API** | Senden über Ihr Gmail- oder Google Workspace-Konto mit OAuth-Authentifizierung. |
| **Allgemeiner SMTP** | Verbinden Sie jeden SMTP-Server (SendGrid, Mailgun, Amazon SES oder Ihren eigenen Mailserver). |

## E-Mail-Richtlinie einrichten

Navigieren Sie zu **Einstellungen > E-Mail-Konten** und klicken Sie auf **E-Mail-Konto hinzufügen**, um den Einrichtungswizard zu starten.

### Schritt 1: Anbieter auswählen

Wählen Sie Ihren E-Mail-Anbieter. Der integrierte SMTP-Server ist die einfachste Option, um loszulegen – er benötigt keine externen Konten.

### Schritt 2: Anmeldeinformationen konfigurieren

Geben Sie die Anmeldeinformationen für Ihren gewählten Anbieter ein:

- **Integrierter SMTP** – Es sind keine Anmeldeinformationen erforderlich. Der Server läuft auf Ihrer Spwig-Installation.
- **Gmail API** – Authentifizieren Sie sich über Google OAuth. Sie werden zur Anmeldung mit Ihrem Google-Konto weitergeleitet.
- **Allgemeiner SMTP** – Geben Sie die SMTP-Server-Adresse, den Port, den Benutzernamen und das Passwort ein.

### Schritt 3: Absender-Konfiguration

Legen Sie die Absenderidentität für ausgehende E-Mails fest:

- **Absender-E-Mail** – Die E-Mail-Adresse, die im Feld "Von" erscheint (z. B. orders@yourstore.com)
- **Absender-Name** – Der Anzeigename neben der E-Mail-Adresse (z. B. "Ihr Geschäftsnamen")
- **Antwort-E-Mail** – Dorthin, wohin Kunden antworten (kann sich von der Absender-E-Mail unterscheiden)

### Schritt 4: DNS-Prüfung

Überprüfen Sie die E-Mail-Authentifizierungsprotokolle Ihres Domänen. Der Wizard prüft drei DNS-Protokolle:

| Protokoll | Zweck |
|--------|---------|
| **SPF** | Autorisiert Ihren Server, E-Mails im Namen Ihrer Domain zu versenden |
| **DKIM** | Digitale Signatur von E-Mails, um zu beweisen, dass sie nicht manipuliert wurden |
| **DMARC** | Teilt empfangenden Servern mit, was mit E-Mails geschehen soll, die SPF/DKIM-Prüfungen nicht bestanden haben |

Für jedes Protokoll zeigt der Wizard:
- **Aktueller Status** – Ob das Protokoll korrekt konfiguriert ist
- **Erforderter Wert** – Das genaue DNS-Protokoll, das Sie bei Ihrem Domain-Registrar hinzufügen müssen
- **Verbreitungszustand** – Ob kürzliche Änderungen wirksam geworden sind (DNS-Änderungen können bis zu 48 Stunden dauern)

Der integrierte SMTP-Server generiert automatisch DKIM-Schlüssel für Ihre Domain.

### Schritt 5: Test-E-Mail senden

Senden Sie eine Test-E-Mail, um zu prüfen, ob alles funktioniert:
1. Geben Sie eine Empfänger-E-Mail-Adresse ein
2. Klicken Sie auf **Test senden**
3. Prüfen Sie Ihre Postfach auf die Testnachricht
4. Stellen Sie sicher, dass die E-Mail ohne Spam-Warnungen ankommt

### Schritt 6: Speichern und Aktivieren

Speichern Sie die Konfiguration und setzen Sie das Konto als aktiv. Markieren Sie es als **Standard**, falls es das primäre E-Mail-Konto sein soll.

## E-Mail-Vorlagen

Spwig verfügt über 30+ E-Mail-Vorlagen für jeden transaktionsbezogenen Ereignis. Navigieren Sie zu **Einstellungen > E-Mail-Vorlagen**, um sie zu verwalten.

### Vorlagen-Typen

Vorlagen umfassen alle Geschäftsevents, einschließlich:
- **Bestellverlauf** – Bestätigung, Verarbeitung, Versand, Lieferung, Stornierung
- **Zahlung** – Quittung, Bestätigung der Erstattung, fehlerhafte Zahlung
- **Kundenkonto** – Willkommensnachricht, Passwortwiederherstellung, E-Mail-Bestätigung
- **Geschenkkarten** – Lieferung, Kontostandsbenachrichtigung
- **Versand** – Tracking-Updates, Lieferbestätigung
- **Digitale Produkte** – Download-Links, Lizenzschlüssel
- **Marketing** – Wiederherstellung des Warenkorbs, Anfragen zu Bewertungen

### Anpassen von Vorlagen

1. Navigieren Sie zur Liste der Vorlagen
2. Klicken Sie auf eine Vorlage, um sie zu bearbeiten
3. Ändern Sie Betreffzeile, Kopfzeile, Textinhalt und Fußzeile
4. Verwenden Sie Vorlagen-Variablen (z. B. `{{ bestellnummer }}`, `{{ kundenname }}`), um dynamischen Inhalt zu erstellen
5. Zeigen Sie die E-Mail vor dem Speichern an

### Mehrsprachige Unterstützung

Bewahren Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

E-Mail-Vorlagen unterstützen mehrere Sprachen:
- Jede Vorlage kann Übersetzungen für alle aktiven Sprachen Ihres Shops enthalten
- Das System sendet E-Mails in der bevorzugten Sprache des Kunden
- **Sprach-Fallback-Kette** — Wenn keine Übersetzung verfügbar ist, fällt das System auf die Standardsprache des Shops zurück
- Verwenden Sie die Funktion **KI-Übersetzung**, um Vorlagen automatisch in andere Sprachen zu übersetzen

### Vorlagen klonen

Um eine angepasste Version einer Systemvorlage zu erstellen:
1. Öffnen Sie die Vorlage, die Sie ändern möchten
2. Klicken Sie auf **Vorlage klonen**
3. Bearbeiten Sie die geklonte Version
4. Der Klon hat Vorrang vor der ursprünglichen Systemvorlage

## E-Mail-Warteschlange

Überwachen Sie ausgehende E-Mails unter **Einstellungen > E-Mail-Warteschlange**:

- **In Warteschlange** — E-Mails, die auf den Versand warten
- **Wird gesendet** — Derzeit wird übertragen
- **Gesendet** — Erfolgreich zugestellt
- **Fehlgeschlagen** — Konnte nicht zugestellt werden (mit Fehlerdetails)
- **Zurückgeprallt** — Vom E-Mail-Server des Empfängers abgelehnt

Klicken Sie auf eine beliebige E-Mail, um alle Details einschließlich Empfänger, Betreff, Versandzeit und Zustellstatus anzuzeigen.

## Zustellungsverfolgung

Verfolgen Sie das Engagement der E-Mails:
- **Öffnungen** — Wie viele Empfänger die E-Mail geöffnet haben
- **Klicks** — Link-Klicks innerhalb der E-Mail
- **Zurückgeprallt** — Verfolgung von harten und weichen Bounces
- **Beschwerden** — Spam-Meldungen von Empfängern

## Mehrere Konten

Sie können mehrere E-Mail-Konten konfigurieren:
- **Standardkonto** — Wird für alle ausgehenden E-Mails verwendet, es sei denn, es wird überschrieben
- **Fallback** — Wenn das Standardkonto fehlschlägt, werden E-Mails in die Warteschlange für einen erneuten Versuch gestellt
- Verwenden Sie verschiedene Konten für verschiedene Zwecke (z. B. eines für transaktionale E-Mails, ein anderes für Marketing)

## E-Mail-Zustellmodus

Navigieren Sie zu **Einstellungen > Shop-Einstellungen**, um zu steuern, wie Ihr Shop ausgehende E-Mails verarbeitet. Diese Einstellungen sind während der Entwicklung und Testphase nützlich.

| Modus | Beschreibung |
|------|-------------|
| **Live** | E-Mails werden normal an echte Empfänger zugestellt |
| **Pausiert** | E-Mails werden in der Warteschlange gehalten und nicht gesendet, bis Sie wieder auf Live umschalten |
| **Nur protokollieren** | E-Mails werden im Postausgang protokolliert, aber nie zugestellt |

### Test-Weiterleitungse-Mail

Geben Sie eine **Test-Weiterleitungse-Mail**-Adresse an, um alle ausgehenden E-Mails abzufangen und an eine einzelne Adresse weiterzuleiten. Wenn dies festgelegt ist, gehen alle E-Mails — unabhängig vom tatsächlichen Empfänger — an diese Adresse. Dies ist nützlich, um E-Mail-Vorlagen zu testen, ohne versehentlich an echte Kunden zu senden. Lassen Sie das Feld leer, um E-Mails an die tatsächlichen Empfänger zu senden.

### Sandbox-E-Mail-Whitelist

Im Sandbox- oder Entwicklungsmodus können Sie die E-Mail-Zustellung auf eine Whitelist genehmigter Adressen beschränken. Nur E-Mails an Adressen auf der Whitelist werden zugestellt. Alle anderen E-Mails werden protokolliert, aber nie gesendet. Die Admin-E-Mail wird immer automatisch einbezogen. Sie können bis zu 10 Adressen hinzufügen.

## Tipps

- Beginnen Sie mit dem **integrierten SMTP**-Server für eine schnelle Einrichtung und wechseln Sie dann zu einem externen Anbieter, wenn Sie höhere Versandmengen oder eine bessere Zustellbarkeit benötigen.
- Konfigurieren Sie immer **SPF-, DKIM- und DMARC**-Einträge — ohne diese landen E-Mails viel häufiger in Spam-Ordner.
- Senden Sie nach jeder Konfigurationsänderung eine **Test-E-Mail**, um zu überprüfen, ob die Zustellung funktioniert.
- Überwachen Sie die E-Mail-Warteschlange regelmäßig auf **fehlgeschlagene** oder **zurückgeprallte** E-Mails — diese deuten auf Zustellungsprobleme hin.
- Verwenden Sie eine **professionelle Absenderadresse** (z. B. bestellungen@ihreshop.com) anstelle einer kostenlosen E-Mail-Adresse für mehr Vertrauen und bessere Zustellbarkeit.
- Halten Sie Ihre Vorlagen knapp — transaktionale E-Mails sollten Informationen schnell liefern, keine Marketing-Newsletter sein.