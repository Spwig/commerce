---
title: Kommunikationseinstellungen
---

Mit den Kommunikationseinstellungen können Kunden steuern, welche E-Mails und SMS-Nachrichten sie von Ihrem Shop erhalten. Dieses System stellt die DSGVO-Konformität sicher und hilft Ihnen, die Kommunikationspräferenzen der Kunden über alle Kanäle hinweg zu respektieren.

Navigieren Sie in der Admin-Leiste zu **Kunden > Kommunikationseinstellungen**, um die Kommunikationspräferenzen der Kunden zu verwalten.

## Verständnis der Kommunikationseinstellungen

Das System für Kommunikationseinstellungen gibt Kunden eine detaillierte Kontrolle über die empfangenen Nachrichten. Dies umfasst:

- **Transaktionale E-Mails** — Wesentliche Bestellbestätigungen, Versandupdates, Kontosicherheits-E-Mails (immer aktiviert)
- **Marketing-E-Mails** — Newsletter, Aktionen, Produktempfehlungen (erfordert Opt-in)
- **App-spezifische Benachrichtigungen** — Blogbeiträge, Treuepunkte, Empfehlungsprämien, Affiliate-Provisionen
- **SMS-Benachrichtigungen** — Textnachrichten-Benachrichtigungen (erfordert explizites Opt-in gemäß TCPA)

Alle Marketing-Kommunikationen erfordern die Zustimmung des Kunden und die E-Mail-Verifizierung, um die DSGVO-Konformität sicherzustellen.

## Erklärung der Präferenztypen

### Transaktionale Kommunikation (Immer aktiviert)

Transaktionale Nachrichten sind für das Konto und die Bestellungen Ihrer Kunden unerlässlich. Diese **können von Kunden nicht deaktiviert** werden:

| Typ | Beschreibung | Beispiele |
|------|-------------|----------|
| **Bestellbestätigungen** | Bestätigung, wenn eine Bestellung aufgegeben wird | Bestellung #12345 wurde erhalten |
| **Versandupdates** | Benachrichtigungen bei Änderung des Bestellstatus | Ihre Bestellung wurde versendet |
| **Zahlungsbestätigungen** | Zahlung erhalten, Rückerstattung bearbeitet | Zahlung von 49,99 $ bestätigt |
| **Kontosicherheit** | Passwort-Reset, E-Mail-Verifizierung | Setzen Sie Ihr Passwort zurück |

### Marketing-Kommunikation (Opt-in erforderlich)

Marketing-Nachrichten erfordern die Zustimmung des Kunden und die E-Mail-Verifizierung:

| Typ | Beschreibung | Standard |
|------|-------------|---------|
| **Newsletter** | Allgemeine Newsletter und Updates | Opt-out |
| **Aktionen** | Sales, Rabatte, Sonderangebote | Opt-out |
| **Produktempfehlungen** | Personalisierte Produktempfehlungen | Opt-out |
| **Wieder verfügbar** | Benachrichtigungen, wenn Produkte wieder verfügbar sind | Opt-out |

Kunden müssen ihre **E-Mail-Adresse verifizieren**, bevor sie Marketing-E-Mails erhalten (DSGVO-Doppel-Opt-in-Anforderung).

### App-spezifische Einstellungen

Kunden können Benachrichtigungen von bestimmten Funktionen steuern:

**Blog-Benachrichtigungen**
- Neuer Blogbeitrag veröffentlicht (sofort, wöchentliches Digest oder monatliches Digest)
- Kategorie-spezifische Abonnements
- Frequenzeinstellungen

**Treueprogramm**
- Benachrichtigungen über erhaltene Punkte
- Stufen-Upgrades
- Freigeschaltete Belohnungen
- Bald ablaufende Punkte
- Geburtstagsboni
- Kampagnenangebote

**Empfehlungsprogramm**
- Ausgegebene Belohnung (Empfehler und Empfohlener)
- Erfolgreiche Registrierung durch Empfehlung
- Bald ablaufende Belohnung
- Empfehlungs-Einladungen

**Affiliate-Programm**
- Erzielte Provision
- Freigegebene oder abgelehnte Provision
- Auszahlung bearbeitet, abgeschlossen oder fehlgeschlagen
- Monatliche Leistungsberichte

### SMS-Benachrichtigungen (Explizites Opt-in erforderlich)

Alle SMS-Benachrichtigungen erfordern ein **explizites Opt-in** gemäß den TCPA-Regelungen. Kunden müssen das SMS-Opt-in-Kästchen aktiv ankreuzen:

- **Transaktionale SMS** — Bestellung versendet, zugestellt (Opt-in erforderlich)
- **Marketing-SMS** — Aktionen, Sonderangebote (separates Opt-in erforderlich)

Selbst transaktionale SMS erfordern ein Opt-in, da der Versand ungewollter Textnachrichten strenger reguliert ist als der Versand von E-Mails.

## Verwaltung der Kundeneinstellungen im Adminbereich

### Alle Einstellungen anzeigen

Navigieren Sie zu **Kunden > Kommunikationseinstellungen**, um alle Kundeneinstellungen anzuzeigen:

{
  "Table": {
    "Column": "Spaltenname",
    "Description": "Beschreibung"
  },
  "TableRows": {
    "User Email": "E-Mail-Adresse des Kunden (verknüpft mit dem Benutzer-Admin)",
    "Email Status": "Grün ✓, wenn E-Mails aktiviert sind, grau ○, wenn deaktiviert",
    "SMS Status": "Grün ✓, wenn SMS aktiviert sind, grau ○, wenn deaktiviert",
    "Marketing Status": "Schild 'Einhellig' oder 'Abgemeldet'",
    "Verification Status": "📧✓, wenn E-Mail verifiziert, 📱✓, wenn SMS verifiziert",
    "Consent Source": "Wo der Kunde seine Zustimmung gegeben hat (Registrierung, Checkout, Einstellungen-Bereich)",
    "Updated At": "Letzte Änderungszeit der Präferenzen"
  },
  "Filtering Preferences": {
    "Title": "Präferenzen filtern",
    "Description": "Verwenden Sie die Sidebar-Filter, um Kunden zu finden:"
  },
  "FilterOptions": {
    "Email Enabled": "Ja/Nein",
    "SMS Enabled": "Ja/Nein",
    "Email Marketing": "Ja/Nein (Marketing-Einwilligung)",
    "SMS Marketing": "Ja/Nein (Einwilligung für SMS-Marketing)",
    "Email Verified": "Ja/Nein (E-Mail-Adresse verifiziert)",
    "SMS Verified": "Ja/Nein (Handynummer verifiziert)",
    "Consent Source": "Registrierung, Checkout, Einstellungen-Bereich, API, Migration",
    "Language Code": "Bevorzugte Sprache für Kommunikationen"
  },
  "Searching Preferences": {
    "Title": "Präferenzen suchen",
    "Description": "Suche nach Kunden anhand von:"
  },
  "SearchOptions": {
    "User email": "Benutzer-E-Mail",
    "Username": "Benutzername",
    "First name": "Vorname",
    "Last name": "Nachname",
    "Unsubscribe token": "Unsubscribe-Token"
  },
  "Bulk Actions": {
    "Title": "Massenaktionen",
    "Description": "Wählen Sie mehrere Kunden aus und wenden Sie Massenaktionen an:"
  },
  "BulkActionOptions": {
    "✓ Mark Email as Verified": "E-Mail des Kunden manuell verifizieren\nNützlich, wenn Kunden aus einem anderen System importiert werden\nInvalidiert den Präferenz-Cache, um Änderungen sofort anzuwenden",
    "🚫 Unsubscribe from All Marketing": "Alle Marketingkommunikationen deaktivieren (E-Mail, SMS, alle Apps)\nBehält Transaktions-E-Mails bei\nVerwenden Sie dies für Kunden, die sich vollständig abmelden möchten\nRespektiert das GDPR-Recht, die Zustimmung zurückzuziehen",
    "📥 Export Preferences to CSV": "Präferenzen des Kunden in CSV-Datei exportieren\nEnthält alle Präferenzfelder und app-spezifische Einstellungen\nNützlich für Compliance-Prüfungen und Analyse\nFormat: CSV mit Kopfzeile"
  },
  "Customer Self-Service Preference Center": {
    "Title": "Kunden-Selbstbedienungs-Einstellungen-Bereich",
    "Description": "Kunden können ihre eigenen Einstellungen unter /accounts/preferences/ verwalten, wenn sie angemeldet sind."
  },
  "Preference Center Features": {
    "Title": "Einstellungen-Bereich-Funktionen",
    "Quick Actions": {
      "Subscribe to All Marketing": "Alle Marketingkommunikationen in einem Klick aktivieren",
      "Unsubscribe from All": "Alle Marketingkommunikationen deaktivieren (Transaktions-E-Mails sind weiterhin aktiv)"
    },
    "Preference Cards": {
      "Transactional Emails": "Nur zum Lesen (immer aktiv, als \"Erforderlich\" markiert)",
      "Marketing Communications": "Ein-/Ausschalten mit Verifizierungs-Schild",
      "Blog Preferences": "Ein-/Ausschalten, Frequenz auswählen (sofort, wöchentlich, monatlich)",
      "Loyalty Program": "Ein-/Ausschalten einzelner Benachrichtigungstypen",
      "Referral Program": "Ein-/Ausschalten Belohnungs-Benachrichtigungen",
      "Affiliate Program": "Ein-/Ausschalten Kommission- und Auszahlungs-Benachrichtigungen",
      "SMS Notifications": "Ein-/Ausschalten von SMS (zeigt Verifizierungsstatus an)"
    },
    "Real-Time Updates": {
      "Description": "Änderungen werden per AJAX sofort gespeichert\nKein Seiten-Reload erforderlich\nVisuelle Rückmeldung beim Speichern"
    }
  },
  "Email Verification Process": {
    "Title": "E-Mail-Verifizierungsprozess",
    "Description": "Wenn ein Kunde Marketing-E-Mails aktiviert:\n\n1. Kunde schaltet \"Marketing-E-Mails\" auf AN\n2. System sendet Verifizierungsemail mit eindeutigem Link\n3. Kunde klickt auf Verifizierungslin\n4. E-Mail wird als verifiziert markiert (Schild 📧✓ wird angezeigt)\n5. Marketing-E-Mails werden nun gesendet\n\n\nNicht verifizierte Kunden erhalten keine Marketing-E-Mails, auch wenn der Schalter auf AN steht. Dies stellt die Einhaltung der Doppel-Opt-in-Vorschriften der GDPR sicher."
  },
  "One-Click Unsubscribe": {
    "Title": "Einfache Abmeldung",
    "Description": "Alle Marketing-E-Mails enthalten einen Abmeldelink in der Fußzeile. Klicken Sie auf diesen Link:\n\n1. Leitet den Kunden zu /accounts/unsubscribe/<token>/ (keine Anmeldung erforderlich)\n2. Zeigt an, was sie abgemeldet haben\n3. Erlaubt optionale Rückmeldung (Grund für die Abmeldung)\n4. Deaktiviert Marketingkommunikation\n5. Behält Transaktions-E-Mails bei\n6. Bietet Link zu vollständigem Einstellungen-Bereich\n\nKunden können jederzeit erneut abonnieren, über den Einstellungen-Bereich."
  },
  "Compliance & Legal Requirements": {
    "Title": "Einhaltung und rechtliche Anforderungen",
    "GDPR Article 7 Compliance": {
      "Description": "Das System stellt die Einhaltung der GDPR Artikel 7 sicher:\n\nPreserve all markdown formatting, image paths, code blocks, and technical terms."
    }
  }
}

**✅ Nachweis der Einwilligung**
- Zeitstempel, wann die Einwilligung erteilt wurde
- Quelle der Einwilligung (Registrierung, Kasse, Präferenzcenter)
- IP-Adresse der Einwilligung
- User-Agent (Browser-Informationen)

**✅ Getrennte Einwilligung**
- Marketing- und Transaktions-E-Mails sind separate Umschalter
- Jede App (Blog, Loyalität usw.) erfordert eine individuelle Einwilligung

**✅ Einfache Widerrufung**
- Abmeldung mit einem Klick in allen Marketing-E-Mails
- Präferenzcenter für alle angemeldeten Kunden verfügbar
- Abmeldung wird sofort wirksam

**✅ Freiwillig erteilte Einwilligung**
- Standard ist Opt-Out für Marketing (GDPR-Best-Practice)
- Keine vorausgewählten Kästchen (Kunden müssen aktiv opt-in)

**✅ Bestimmte und informierte Einwilligung**
- Klare Beschreibungen, was jede Präferenz steuert
- Granulare App-Ebene Präferenzen (nicht alles-oder-nichts)

**✅ Überprüfbare Einwilligung**
- Double Opt-In für Marketing-E-Mails
- Audit-Trail über die Statusverfolgung von EmailOutbox

### TCPA-Konformität (US-SMS-Regelungen)

Alle SMS-Benachrichtigungen erfordern eine **explizite Opt-In-Einwilligung**:

- Kunden müssen das SMS-Opt-In-Kästchen aktiv ankreuzen
- Vorausgewählte Kästchen sind nicht erlaubt
- Klare Beschreibung, worauf sie sich einlassen
- Einfache Opt-Out-Möglichkeit über das Präferenzcenter
- Alle SMS-Versende werden für Compliance-Audits protokolliert

### CAN-SPAM-Konformität (US-E-Mail-Regelungen)

Das System stellt die CAN-SPAM-Konformität sicher:

- Abmeldelink in jeder Marketing-E-Mail
- Abmeldung wird sofort verarbeitet (innerhalb von 10 Arbeitstagen erforderlich, wir machen es sofort)
- Klare "Von"-Bezeichnung (Ihr Shopname)
- Physische Adresse im E-Mail-Fußzeile
- Keine irreführenden Betreffzeilen

## Verständnis der E-Mail-Status in EmailOutbox

Wenn Sie **E-Mail-System > E-Mail-Outbox** anzeigen, sehen Sie, wie Präferenzen die E-Mail-Zustellung beeinflussen:

| Status | Bedeutung | Grund |
|--------|-----------|-------|
| **Ausstehend** | E-Mail in der Warteschlange zum Versand | Präferenzen erlauben diese E-Mail |
| **In Warteschlange** | In der Versand-Warteschlange | Präferenzen erlauben diese E-Mail |
| **Übersprungen** | E-Mail nicht gesendet | Kundenpräferenz deaktiviert |
| **Gesendet** | Erfolgreich zugestellt | E-Mail normal gesendet |

Wenn eine E-Mail **übersprungen** wird, zeigt das Feld `skip_reason` den Grund an:

- **user_preference_disabled** — Kunde hat diesen E-Mail-Typ in den Präferenzen deaktiviert
- **email_not_verified** — Kunde hat seine E-Mail-Adresse nicht verifiziert
- **email_disabled** — Kunde hat alle E-Mails deaktiviert (Hauptumschalter)

Dieser Audit-Trail ist wichtig für die GDPR-Konformität — Sie können nachweisen, dass Sie die Kundenpräferenzen respektiert haben.

## Seiteneinstellungen für Präferenzen

Navigieren Sie zu **Einstellungen > Seiteneinstellungen**, um globale Standardpräferenzen zu konfigurieren:

**Double Opt-In für Marketing-E-Mails aktivieren** (Standard: Ja)
- Erfordert E-Mail-Verifizierung vor dem Versand von Marketing-E-Mails
- GDPR-Best-Practice
- Empfehlung: Aktiviert lassen

**Standard-Marketing-Opt-In-Zustand** (Standard: Nein - Opt-Out)
- Standardzustand, wenn neue Kunden sich registrieren
- GDPR erfordert standardmäßig Opt-Out
- Empfehlung: Als Opt-Out (False) belassen

**Präferenzcenter aktiviert** (Standard: Ja)
- Ermöglicht es Kunden, ihre eigenen Präferenzen zu verwalten
- Erforderlich für das GDPR-Recht auf Widerruf der Einwilligung
- Empfehlung: Aktiviert lassen

**SMS-Verifizierung erforderlich** (Standard: Nein)
- Erfordert die Verifizierung der Telefonnummer für SMS-Benachrichtigungen
- Optional, aber für Hochvolumen-SMS-Versender empfohlen
- Kann aktiviert werden, wenn Sie Double Opt-In für SMS wünschen

**Abmeldegründe anzeigen** (Standard: Ja)
- Sammelt optionales Feedback, wenn Kunden sich abmelden
- Hilft zu verstehen, warum Kunden sich abmelden
- Empfehlung: Aktiviert lassen für Einblicke

## Best Practices

### 1. Standardmäßig Opt-Out für Marketing

Setzen Sie Marketing-Kommunikation immer standardmäßig auf **Opt-Out** (nicht angekreuzt):
- Erfüllt die GDPR
- Baut Vertrauen bei Kunden auf
- Reduziert Spam-Beschwerden
- Senden Sie nur an engagierte Kunden

### 2. E-Mail-Verifizierung erforderlich

Halten Sie **Double Opt-In** aktiviert:
- Stellt sicher, dass E-Mail-Adressen gültig sind
- Bestätigt, dass der Kunde tatsächlich Marketing-E-Mails möchte
- Reduziert die Bounce-Rate
- Erforderlich für die GDPR-Konformität

### 3. Präferenzen sofort respektieren

Bewahren Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe bei.

Wenn ein Kunde seine Einstellungen ändert:
- Änderungen werden sofort wirksam
- Der Einstellungscache wird ungültig gemacht
- Beim nächsten E-Mail-Versand werden die aktualisierten Einstellungen überprüft
- Keine Verzögerung bei der Berücksichtigung von Abmeldewünschen

### 4. Überwachte übersprungene E-Mails

Prüfen Sie regelmäßig den **E-Mail-Versand** auf übersprungene E-Mails:
- Eine hohe Überspringrate deutet darauf hin, dass sich Kunden abmelden
- Kann ein Hinweis darauf sein, dass der E-Mail-Inhalt verbessert werden muss
- Hilft bei der Identifizierung von Einstellungskonflikten

### 5. Regelmäßige Compliance-Audits

Exportieren Sie Einstellungen regelmäßig zu Compliance-Zwecken:
1. Navigieren Sie zu **Kommunikationseinstellungen**
2. Wählen Sie alle Kunden aus
3. Wählen Sie **Einstellungen als CSV exportieren**
4. Speichern Sie für die DSGVO-Audit-Trail

Bewahren Sie Exporte **mindestens 3 Jahre** auf, um die DSGVO-Datenaufbewahrungsvorgaben einzuhalten.

### 6. Klare Kommunikation

Bei der Einholung der Einwilligung:
- Verwenden Sie einfache Sprache, keine juristische Fachsprache
- Erklären Sie, was die Kunden erhalten werden
- Zeigen Sie die Frequenz an (täglich, wöchentlich, monatlich)
- Machen Sie die Opt-in-Boxen prominent, aber nicht vorausgewählt

### 7. Segmentierung nach Einstellungen

Beim Versand von Marketing-Kampagnen:
- Senden Sie nur an verifizierte, eingetragene Kunden
- Beachten Sie app-spezifische Einstellungen (keine Blog-E-Mails an Kunden, die den Blog deaktiviert haben)
- Verwenden Sie Frequenzeinstellungen (keine sofortigen E-Mails an Abonnenten des wöchentlichen Digests)

## Tipps

**💡 Einstellungen vor dem Versand prüfen**

Das System überprüft automatisch die Einstellungen, wenn Sie E-Mails mit `EmailSendingService.send_template_email()` senden. Stellen Sie sicher, dass alle E-Mail-Versände diesen Dienst verwenden und keine direkten SMTP-Aufrufe.

**💡 Übersprungener Status ist normal**

Seien Sie nicht beunruhigt von übersprungenen E-Mails im Versand – dies bedeutet, dass das System korrekt funktioniert und die Kundeneinstellungen respektiert. Es ist besser, unerwünschte E-Mails zu überspringen, als das Risiko von DSGVO-Geldstrafen oder Spam-Beschwerden einzugehen.

**💡 Einstellungscache beträgt 5 Minuten**

Einstellungsprüfungen werden aus Leistungsgründen für 5 Minuten gecacht. Wenn Kunden ihre Einstellungen über das Einstellungszentrum oder Administratoraktionen ändern, wird der Cache sofort ungültig gemacht, damit die Änderungen sofort wirksam werden.

**💡 Gastkunden umgehen Prüfungen**

Gastbesteller (ohne Konto) erhalten alle E-Mails wie gewöhnlich, da sie keinen Einstellungseintrag haben. Dies ist beabsichtigt – sie haben sich durch die Angabe ihrer E-Mail-Adresse beim Checkout eingetragen.

**💡 Transaktionale E-Mails werden immer gesendet**

Bestätigungen, Versandupdates und Kontosicherheitse-Mails werden **immer gesendet**, unabhängig von den Einstellungen. Dies stellt sicher, dass Kunden wichtige Informationen über ihre Bestellungen und Konten erhalten.

**💡 Bulk-Aktionen vorsichtig verwenden**

Die Bulk-Aktion "Von allen Marketing-E-Mails abmelden" betrifft **alle Apps** (Blog, Loyalität, Empfehlungen, Affiliate). Verwenden Sie dies nur für Kunden, die ausdrücklich eine vollständige Abmeldung angefordert haben. Für spezifische Einstellungen bearbeiten Sie einzelne Kundendatensätze.

**💡 Audit-Trail für Compliance**

Das System erfasst:
- Zeitstempel und Quelle der Einwilligung
- IP-Adresse und User-Agent
- Zeitstempel der E-Mail-Verifizierung
- Jede Einstellungsänderung über den übersprungenen Status der EmailOutbox

Dieser Audit-Trail beweist die DSGVO-Compliance, falls Behörden jemals Beweise für die Einwilligung anfordern.

## Verwandte Themen

- [Verwaltung von Kundenkonten](/help/managing-customer-accounts) — Verwaltung von Kundenprofilen
- [E-Mail-Konfiguration](/help/email-configuration) — SMTP-Einrichtung und E-Mail-Vorlagen