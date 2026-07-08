---
title: Kommunikationspräferenzen
---

Kommunikationspräferenzen ermöglichen es Kunden, zu bestimmen, welche E-Mails und SMS-Nachrichten sie von Ihrem Geschäft erhalten möchten. Dieses System stellt die Einhaltung der DSGVO sicher und hilft Ihnen dabei, die Kommunikationspräferenzen der Kunden über alle Kanäle hinweg zu respektieren.

Navigieren Sie zu **Kunden > Kommunikationspräferenzen** in der Seitenleiste des Admin-Bereichs, um die Kommunikationspräferenzen der Kunden zu verwalten.

## Kommunikationspräferenzen verstehen

Das Kommunikationspräferenzsystem gibt Kunden die feine Kontrolle über die Nachrichten, die sie erhalten. Dazu gehören:

- **Transaktionale E-Mails** — Wichtige Bestätigungen, Versandupdates, Sicherheits-E-Mails für Konten (immer aktiviert)
- **Marketing-E-Mails** — Newslettern, Promotionen, Produktvorschläge (erfordert Einwilligung)
- **App-spezifische Benachrichtigungen** — Blogbeiträge, Treuepunkte, Empfehlungsbelohnungen, Affiliate-Kommissionen
- **SMS-Benachrichtigungen** — Textnachrichten (erfordert explizite Einwilligung gemäß TCPA)

Alle Marketingkommunikation erfordert die Einwilligung des Kunden und eine E-Mail-Bestätigung, um die Einhaltung der DSGVO sicherzustellen.

## Erklärung der Präferenztypen

### Transaktionale Kommunikation (immer aktiviert)

Transaktionale Nachrichten sind für das Kundenkonto und Bestellungen unerlässlich. Diese **können nicht von Kunden deaktiviert werden**:

| Typ | Beschreibung | Beispiele |
|------|-------------|----------|
| **Bestätigungen für Bestellungen** | Bestätigung, wenn eine Bestellung aufgegeben wird | Bestellung #12345 wurde empfangen |
| **Versandupdates** | Benachrichtigungen, wenn sich der Bestellstatus ändert | Ihre Bestellung wurde versandt |
| **Zahlungsbestätigungen** | Zahlung erhalten, Rückerstattung verarbeitet | Zahlung von $49,99 bestätigt |
| **Konten-Sicherheit** | Passwort-Reset, E-Mail-Bestätigung | Passwort zurücksetzen |

### Marketingkommunikation (erforderliche Einwilligung)

Marketingnachrichten erfordern die Einwilligung des Kunden und eine E-Mail-Bestätigung:

| Typ | Beschreibung | Standard |
|------|-------------|---------|
| **Newsletter** | Allgemeine Newsletter und Updates | Abmeldung |
| **Promotionale Angebote** | Verkaufsangebote, Rabatte, Sonderangebote | Abmeldung |
| **Produktvorschläge** | Personalisierte Produktvorschläge | Abmeldung |
| **Wieder auf Lager** | Benachrichtigungen, wenn Produkte zurückkehren | Abmeldung |

Kunden müssen ihre **E-Mail-Adresse bestätigen**, bevor sie Marketing-E-Mails erhalten (DSGVO-Doppelbestätigung erforderlich).

### App-spezifische Präferenzen

Kunden können Benachrichtigungen von bestimmten Features steuern:

**Blog-Benachrichtigungen**
- Neuer Blogbeitrag veröffentlicht (sofortig, wöchentliche Zusammenfassung oder monatliche Zusammenfassung)
- Abonnements für spezifische Kategorien
- Frequenzpräferenzen

**Treueprogramm**
- Benachrichtigungen über erhaltene Punkte
- Stufenaufstiege
- Freigeschaltete Belohnungen
- Bald ablaufende Punkte
- Geburtstagsboni
- Kampagnenangebote

**Empfehlungsprogramm**
- Belohnung ausgestellt (für Empfehler und Empfänger)
- Erfolgreiche Registrierung durch Empfehlung
- Bald ablaufende Belohnung
- Empfehlungsaufforderungen

**Affiliate-Programm**
- Erhaltene Provisionen
- Genehmigte oder abgelehnte Provisionen
- Verarbeitete, abgeschlossene oder fehlgeschlagene Auszahlung
- Monatliche Leistungsberichte

### SMS-Benachrichtigungen (explizite Einwilligung erforderlich)

Alle SMS-Benachrichtigungen erfordern **explizite Einwilligung** gemäß TCPA-Regelungen. Kunden müssen aktiv das SMS-Einwilligungsfeld ankreuzen:

- **Transaktionale SMS** — Bestellung versandt, geliefert (Einwilligung erforderlich)
- **Marketing-SMS** — Promotionen, Sonderangebote (separate Einwilligung erforderlich)

Auch transaktionale SMS erfordert Einwilligung, da das Versenden unerwünschter Textnachrichten strenger reguliert ist als E-Mails.

## Verwalten von Kundenpräferenzen im Admin-Bereich

### Alle Präferenzen ansehen

Navigieren Sie zu **Kunden > Kommunikationspräferenzen**, um alle Kundenpräferenzen anzuzeigen:

| Spalte | Beschreibung |
|--------|-------------|
| **E-Mail-Adresse des Benutzers** | E-Mail-Adresse des Kunden (Link zum Benutzer-Admin) |
| **E-Mail-Status** | Grün ✓, wenn E-Mails aktiviert sind, Grau ○, wenn deaktiviert |
| **SMS-Status** | Grün ✓, wenn SMS aktiviert sind, Grau ○, wenn deaktiviert |
| **Marketing-Status** | Abzeichen "Opted In" oder "Opted Out" |
| **Bestätigungsstatus** | 📧✓, wenn E-Mail bestätigt ist, 📱✓, wenn SMS bestätigt ist |
| **Einwilligungsquelle** | Wo der Kunde seine Einwilligung erteilt hat (Registrierung, Checkout, Präferenzcenter) |
| **Aktualisiert am** | Letzter Zeitpunkt, zu dem die Präferenzen geändert wurden |

### Präferenzen filtern

Verwenden Sie die Filterseitenleiste, um Kunden zu finden:

- **E-Mail aktiviert** — Ja/Nein
- **SMS aktiviert** — Ja/Nein
- **E-Mail-Marketing** — Ja/Nein (für Marketing eingerichtet)
- **SMS-Marketing** — Ja/Nein (für SMS-Marketing eingerichtet)
- **E-Mail bestätigt** — Ja/Nein (E-Mail-Adresse bestätigt)
- **SMS bestätigt** — Ja/Nein (Telefonnummer bestätigt)
- **Einwilligungsquelle** — Registrierung, Checkout, Präferenzcenter, API, Migration
- **Sprachcode** — bevorzugte Sprache für Kommunikation

### Präferenzen durchsuchen

Suchen Sie nach Kunden anhand von:
- E-Mail-Adresse des Benutzers
- Benutzername
- Vorname
- Nachname
- Abmelde-Token

### Massenaktionen

Wählen Sie mehrere Kunden aus und wenden Sie Massenaktionen an:

**✓ E-Mail als bestätigt markieren**
- Bestätige manuell die E-Mail-Adressen der Kunden
- Nützlich, wenn Kunden aus einem anderen System importiert werden
- Überprüft den Präferenz-Cache, um Änderungen sofort anzuwenden

**🚫 Von allen Marketing-Präferenzen abmelden**
- Deaktiviert alle Marketingkommunikation (E-Mail, SMS, alle Apps)
- Behält transaktionale E-Mails aktiviert
- Verwenden Sie dies für Kunden, die sich vollständig abmelden möchten
- Respektiert das DSGVO-Recht auf Widerruf der Einwilligung

**📥 Präferenzen als CSV exportieren**
- Exportieren Sie Kundenpräferenzen in eine Tabellenkalkulation
- Enthält alle Präferenzfelder und App-spezifische Einstellungen
- Nützlich für Compliance-Prüfungen und Analysen
- Format: CSV mit Überschriften

## Kunden-Selbstbedienungs-Präferenzcenter

Kunden können ihre eigenen Präferenzen bei `/accounts/preferences/` verwalten, wenn sie angemeldet sind.

### Merkmale des Präferenzcenters

**Schnelle Aktionen**
- **Alle Marketing-E-Mails abonnieren** — Aktiviert alle Marketingkommunikation mit einem Klick
- **Von allem abmelden** — Deaktiviert alle Marketingkommunikation (transaktionale E-Mails bleiben aktiviert)

**Präferenzkarten**
- **Transaktionale E-Mails** — Nur Lesen (immer aktiviert, als "Erforderlich" markiert)
- **Marketingkommunikation** — Ein/Aus-Schalter mit Bestätigungsabzeichen
- **Blog-Präferenzen** — Aktivieren/Deaktivieren, Frequenz auswählen (sofortig, wöchentlich, monatlich)
- **Treueprogramm** — Individuelle Benachrichtigungen aktivieren/deaktivieren
- **Empfehlungsprogramm** — Belohnungsbenachrichtigungen aktivieren/deaktivieren
- **Affiliate-Programm** — Provision und Auszahlungsbenachrichtigungen aktivieren/deaktivieren
- **SMS-Benachrichtigungen** — Ein/Aus für SMS (zeigt Bestätigungsstatus an)

**Echtzeit-Updates**
- Änderungen werden sofort über AJAX gespeichert
- Keine Seitenneuladung erforderlich
- Visuelle Rückmeldung beim Speichern

### E-Mail-Bestätigungsprozess

Wenn ein Kunde Marketing-E-Mails aktiviert:

1. Der Kunde schaltet "Marketing-E-Mails" auf AN
2. Das System sendet eine Bestätigungs-E-Mail mit einem eindeutigen Link
3. Der Kunde klickt auf den Bestätigungslink
4. Die E-Mail wird als bestätigt markiert (das Abzeichen 📧✓ erscheint)
5. Marketing-E-Mails werden nun gesendet

**Unbestätigte Kunden erhalten KEINE Marketing-E-Mails**, auch wenn der Schalter auf AN steht. Dies stellt die DSGVO-Doppelbestätigung einher ein.

## Ein-Klick-Abmeldung

Alle Marketing-E-Mails enthalten einen Link zur Abmeldung im Fußbereich. Das Klicken auf diesen Link:

1. Leitet den Kunden zu `/accounts/unsubscribe/<token>/` (keine Anmeldung erforderlich)
2. Zeigt an, von was der Kunde sich abmeldet
3. Ermöglicht optionalen Rückmeldung (Grund für die Abmeldung)
4. Deaktiviert Marketingkommunikation
5. Behält transaktionale E-Mails aktiviert
6. Bietet einen Link zum vollständigen Präferenzcenter

Kunden können sich jederzeit über das Präferenzcenter erneut anmelden.

## Compliance und rechtliche Vorgaben

### Einhaltung von Artikel 7 der DSGVO

Das System stellt die volle Einhaltung von Artikel 7 der DSGVO sicher:

**✅ Nachweis der Einwilligung**
- Zeitstempel, zu dem die Einwilligung erteilt wurde
- Quelle der Einwilligung (Registrierung, Checkout, Präferenzcenter)
- IP-Adresse der Einwilligung
- User-Agent (Browserinformationen)

**✅ Separate Einwilligung**
- Marketing- und transaktionale E-Mails sind separate Schalter
- Jede App (Blog, Treueprogramm usw.) erfordert individuelle Einwilligung

**✅ Einfacher Widerruf**
- Ein-Klick-Abmeldung in allen Marketing-E-Mails
- Präferenzcenter ist für alle angemeldeten Kunden verfügbar
- Die Abmeldung wirkt sofort

**✅ Freiwillige Einwilligung**
- Standard ist Abmeldung für Marketing (DSGVO-Best Practice)
- Keine vorab markierten Felder (Kunden müssen aktiv einwilligen)

**✅ Spezifische und informierte Einwilligung**
- Klare Beschreibungen dafür, was jede Präferenz steuert
- Feine Einstellungen auf App-Ebene (nicht alles oder nichts)

**✅ Verifizierbare Einwilligung**
- Doppelbestätigung für Marketing-E-Mails
- Audit-Trail über den EmailOutbox-Statusverfolgung

### Einhaltung der TCPA-Vorschriften (US-amerikanische SMS-Regelungen)

Alle SMS-Benachrichtigungen erfordern **explizite Einwilligung**:

- Kunden müssen aktiv das SMS-Einwilligungsfeld ankreuzen
- Keine vorab markierten Felder erlaubt
- Klare Beschreibung dafür, was sie einwilligen
- Einfache Abmeldung über das Präferenzcenter
- Alle SMS-Versand werden für die Einhaltungsprüfung protokolliert

### Einhaltung der CAN-SPAM-Vorschriften (US-amerikanische E-Mail-Regelungen)

Das System stellt die Einhaltung von CAN-SPAM sicher:

- Abmelde-Link in jeder Marketing-E-Mail
- Abmeldung wird sofort verarbeitet (innerhalb von 10 Geschäftstagen erforderlich, wir tun es sofort)
- Klare "Von"-Name (Ihr Shop-Name)
- Physische Adresse im E-Mail-Fußbereich
- Keine täuschenden Betreffzeilen

## Verständnis des E-Mail-Status in EmailOutbox

Wenn Sie **E-Mail-System > E-Mail-Abgang** ansehen, sehen Sie, wie Präferenzen den E-Mail-Versand beeinflussen:

| Status | Bedeutung | Grund |
|--------|---------|--------|
| **Ausstehend** | E-Mail in der Warteschlange für den Versand | Präferenzen erlauben diesen E-Mail-Versand |
| **In Warteschlange** | In der Versandwarteschlange | Präferenzen erlauben diesen E-Mail-Versand |
| **Übersprungen** | E-Mail nicht gesendet | Kundenpräferenzen deaktiviert |
| **Gesendet** | Erfolgreich zugestellt | E-Mail wurde normal gesendet |

Wenn eine E-Mail **übersprungen** wird, zeigt das Feld `skip_reason` an, warum:

- **user_preference_disabled** — Der Kunde hat diesen E-Mail-Typ in den Präferenzen deaktiviert
- **email_not_verified** — Der Kunde hat seine E-Mail-Adresse noch nicht bestätigt
- **email_disabled** — Der Kunde hat alle E-Mails deaktiviert (Master-Schalter)

Dieser Audit-Trail ist wichtig für die DSGVO-Einhaltung — Sie können beweisen, dass Sie die Präferenzen der Kunden beachtet haben.

## Einstellungen für Präferenzen auf der Website

Navigieren Sie zu **Einstellungen > Website-Einstellungen**, um globale Präferenzstandardwerte zu konfigurieren:

**Doppelbestätigung für Marketing-E-Mails aktivieren** (Standard: Ja)
- Erfordert E-Mail-Bestätigung vor dem Versand von Marketing-E-Mails
- DSGVO-Best Practice
- Empfohlen: Lassen Sie dies aktiviert

**Standardzustand für Marketing-Einwilligung** (Standard: Nein - Abmeldung)
- Standardzustand, wenn neue Kunden sich registrieren
- DSGVO erfordert Abmeldung als Standard
- Empfohlen: Lassen Sie dies als Abmeldung (Falsch) bestehen

**Präferenzcenter aktivieren** (Standard: Ja)
- Ermöglicht Kunden, ihre eigenen Präferenzen zu verwalten
- Erforderlich für das DSGVO-Recht auf Widerruf der Einwilligung
- Empfohlen: Lassen Sie dies aktiviert

**SMS-Bestätigung erforderlich** (Standard: Nein)
- Erfordert Bestätigung der Telefonnummer für SMS-Benachrichtigungen
- Optional, aber empfohlen für Anbieter mit hohem SMS-Volumen
- Kann aktiviert werden, wenn Sie eine Doppelbestätigung für SMS wünschen

**Gründe für Abmeldung anzeigen** (Standard: Ja)
- Sammelt optionalen Feedback, wenn Kunden sich abmelden
- Hilft dabei, zu verstehen, warum Kunden sich abmelden
- Empfohlen: Lassen Sie dies aktiviert, um Erkenntnisse zu gewinnen

## Best Practices

### 1. Standardmäßig auf Abmeldung für Marketing setzen

Setzen Sie Marketingkommunikation immer auf **Abmeldung** (nicht aktiviert):
- Einhaltung der DSGVO
- Baut Vertrauen mit Kunden auf
- Reduziert Beschwerden über Spam
- Senden Sie nur an engagierte Kunden

### 2. E-Mail-Bestätigung erforderlich

Behalten Sie **Doppelbestätigung** aktiviert:
- Stellt sicher, dass E-Mail-Adressen gültig sind
- Bestätigt, dass der Kunde tatsächlich Marketing-E-Mails erhalten möchte
- Reduziert den Rücklauf
- Erforderlich für die Einhaltung der DSGVO

### 3. Präferenzen sofort beachten

Wenn ein Kunde Präferenzen ändert:
- Änderungen wirken sofort
- Präferenz-Cache wird ungültig
- Als nächstes werden die aktualisierten Präferenzen überprüft
- Keine Verzögerung bei der Einhaltung von Abmeldungen

### 4. Übersprungene E-Mails überwachen

Überprüfen Sie regelmäßig den **E-Mail-Abgang**, um übersprungene E-Mails zu finden:
- Hoher Übersprungswert deutet darauf hin, dass Kunden sich abmelden
- Vielleicht signalisiert es, dass der Inhalt der E-Mails verbessert werden muss
- Hilft bei der Identifizierung von Präferenzproblemen

### 5. Regelmäßige Compliance-Prüfungen

Exportieren Sie Präferenzen regelmäßig für die Einhaltung:
1. Navigieren Sie zu **Kommunikationspräferenzen**
2. Wählen Sie alle Kunden aus
3. Wählen Sie **Präferenzen als CSV exportieren** aus
4. Speichern Sie es für den DSGVO-Audit-Trail

Speichern Sie die Exporte **mindestens 3 Jahre** lang, um die DSGVO-Datenspeicherungsvorgaben zu erfüllen.

### 6. Klare Kommunikation

Bei der Erfassung der Einwilligung:
- Verwenden Sie klare Sprache, nicht rechtliche Fachbegriffe
- Erklären Sie, was Kunden erhalten werden
- Zeigen Sie die Frequenz an (täglich, wöchentlich, monatlich)
- Machen Sie die Einwilligungsfelder sichtbar, aber nicht vorausgewählt

### 7. Segmentierung nach Präferenzen

Bei der Sendung von Marketingkampagnen:
- Senden Sie nur an bestätigte, eingerichtete Kunden
- Respektieren Sie App-spezifische Präferenzen (senden Sie keine Blog-E-Mails an Kunden, die Blog-Präferenzen deaktiviert haben)
- Verwenden Sie Frequenzpräferenzen (senden Sie keine sofortigen E-Mails an Kunden, die wöchentliche Zusammenfassungen erhalten)

## Tipps

**💡 Präferenzen vor dem Senden prüfen**

Das System prüft automatisch die Präferenzen, wenn Sie E-Mails mit `EmailSendingService.send_template_email()` senden. Stellen Sie sicher, dass alle E-Mail-Versand über diesen Dienst erfolgen und nicht über direkte SMTP-Aufrufe.

**💡 Übersprungener Status ist normal**

Seien Sie nicht alarmiert, wenn E-Mails im Ausgangsstatus übersprungen werden — dies bedeutet, dass das System richtig funktioniert und die Präferenzen der Kunden beachtet. Es ist besser, unerwünschte E-Mails zu überspringen, als das Risiko von DSGVO-Strafen oder Spam-Beschwerden einzugehen.

**💡 Präferenz-Cache beträgt 5 Minuten**

Präferenz-Prüfungen werden für 5 Minuten zwischengespeichert, um die Leistung zu optimieren. Wenn Kunden Präferenzen über das Präferenzcenter oder Admin-Aktionen ändern, wird der Cache sofort ungültig, damit Änderungen sofort wirksam werden.

**💡 Gastkunden überspringen Prüfungen**

Kunden, die über den Gast-Checkout einkaufen (kein Konto) erhalten alle E-Mails normal, da sie keine Präferenzdaten haben. Dies ist beabsichtigt — sie haben durch die Angabe ihrer E-Mail-Adresse beim Checkout eingewilligt.

**💡 Transaktionale E-Mails werden immer gesendet**

Bestätigungen für Bestellungen, Versandupdates und Sicherheits-E-Mails für Konten **werden immer gesendet**, unabhängig von den Präferenzen. Dies stellt sicher, dass Kunden wichtige Informationen über ihre Bestellungen und Konten erhalten.

**💡 Massenaktionen sorgfältig verwenden**

Die Massenaktion "Von allem Marketing abmelden" wirkt sich auf **alle Apps** (Blog, Treueprogramm, Empfehlungen, Affiliate) aus. Verwenden Sie dies nur für Kunden, die explizit um eine vollständige Abmeldung gebeten haben. Für spezifische Präferenzen bearbeiten Sie die Einzelkundenakten.

**💡 Audit-Trail für Einhaltung**

Das System protokolliert:
- Zeitstempel und Quelle der Einwilligung
- IP-Adresse und User-Agent
- Zeitstempel der E-Mail-Bestätigung
- Jede Präferenzänderung über den Status der übersprungenen E-Mails in EmailOutbox

Dieser Audit-Trail beweist die DSGVO-Einhaltung, wenn Behörden nach Nachweisen der Einwilligung fragen.

## Verwandte Themen

- [Kundenkonten verwalten](/help/managing-customer-accounts) — Kundenprofilverwaltung
- [E-Mail-Konfiguration](/help/email-configuration) — SMTP-Setup und E-Mail-Vorlagen

