---
title: Store-Einstellungen konfigurieren
---

Store-Einstellungen ist der zentrale Ort, um die Identität, Lokalisierung, Branding und Betriebsvorlieben Ihres Geschäfts zu konfigurieren. Navigieren Sie zu **Einstellungen > Store-Einstellungen**, um zu beginnen.

![Allgemeine Registerkarte der Store-Einstellungen](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Allgemeine Registerkarte

Die **Allgemeine** Registerkarte enthält die Kernidentitätseinstellungen Ihres Geschäfts.

### Geschäftsidentität

- **Geschäftsname** — Der Anzeigename, der in Seitentiteln, E-Mails und dem Admin-Header angezeigt wird.
- **Untertitel** — Eine kurze Beschreibung Ihres Geschäfts, die in der Suchmaschinenoptimierung und sozialen Mediengeteilten verwendet wird.
- **Webadresse** — Die öffentliche Webadresse Ihres Geschäfts. Wird in E-Mails, der Generierung von Sitemaps und dem Linkbau verwendet.

### Kontaktinformationen

- **Kontakt-E-Mail** — Empfängt Bestellbenachrichtigungen und wird in Kundenkommunikation angezeigt.
- **Telefonnummer** — Optionaler Support-Telefonnummer, die im Fußbereich und E-Mails angezeigt wird.

### Geschäftsadresse

Geben Sie Ihre vollständige Adresse (Straße, Stadt, Bundesland, Postleitzahl, Land) ein. Wird verwendet für:
- Berechnung des Versandherkunftsorts
- Steuerberechnung
- Rechtliche Anforderungen und Rechnungen

## Branding

### Logo

Laden Sie das Logo Ihres Geschäfts hoch (PNG oder SVG empfohlen, ~200x50px mit transparentem Hintergrund). Das Logo wird angezeigt in:
- Der Storefront-Überschrift
- E-Mail-Vorlagen
- Dem Admin-Panel

### Favicon

Laden Sie ein quadratisches Favicon hoch (ICO oder PNG, 32x32px). Es wird angezeigt als:
- Icon im Browser-Tab
- Lesezeichen-Icon
- Icon auf dem Mobil-Startbildschirm

## Lokalisierung

### Standard-Sprache

Wählen Sie die primäre Sprache Ihres Geschäfts aus 10 unterstützten Optionen:

| Sprache | Code |
|----------|------|
| Englisch | en |
| Spanisch | es |
| Französisch | fr |
| Deutsch | de |
| Portugiesisch | pt |
| Japanisch | ja |
| Chinesisch Vereinfacht | zh-hans |
| Chinesisch Traditionell | zh-hant |
| Russisch | ru |
| Arabisch | ar |

Die Standard-Sprache steuert die Sprache des Admin-Interfaces und die Ausfallsicherung für Storefront-Inhalte.

### Zeitzone

Wählen Sie die Zeitzone Ihres Geschäfts aus, um genaue Bestellzeitzüge, geplante Promotionen und Berichte zu erhalten.

### Währung

- **Standardwährung** — Die primäre Währung für Preise und Buchhaltung.
- **Mehrwährung** — Aktivieren Sie dies, um Kunden zu ermöglichen, Preise in ihrer bevorzugten Währung anzuzeigen, mit automatischer Umrechnung mithilfe von Echtzeit-Austauschkursen.

Konfigurieren Sie zusätzliche Währungen in **Einstellungen > Store-Einstellungen > Währung**.

## E-Commerce-Einstellungen

### Gastbestellung

Erlauben Sie den Kauf ohne Erstellung eines Kontos:
- Schnellerer Bestellvorgang
- Weniger Reibung für erste Käufer
- Erfasst weniger Kundendaten

### Bestellnummernformat

Anpassen, wie Bestellnummern angezeigt werden:
- **Präfix** — z. B. "ORD-"
- **Startnummer** — Die erste Bestellnummer
- **Auffüllung** — z. B. 00001

### Lagerbestandsstandardwerte

- **Lagerbestand verfolgen** — Aktivieren Sie die globale Lagerverfolgung
- **Unterstützung bei geringem Lagerbestand** — Warnschwelle (Standard: 5 Einheiten)
- **Bestellungen bei geringem Lagerbestand akzeptieren** — Akzeptieren Sie Bestellungen, wenn der Lagerbestand erschöpft ist

## E-Mail-Einstellungen

### Absenderinformationen

- **Absendername** — Wird als E-Mail-Absender angezeigt (meist der Geschäftsname)
- **Absender-E-Mail** — Muss von einem verifizierten Domain stammen
- **Antwort-E-Mail** — Ort, an den Kundenantworten weitergeleitet werden

### E-Mail-Provider

Konfigurieren Sie Ihren E-Mail-Versanddienst in **Einstellungen > E-Mail-Konfiguration**. Unterstützte Anbieter umfassen SMTP, SendGrid, Mailgun und Amazon SES.

## Rechtliche & Einhaltung

Fügen Sie Ihre Geschäftsrichtlinien hinzu, um rechtliche Anforderungen zu erfüllen:

- **Allgemeine Geschäftsbedingungen** — Erforderlich für den Kauf; Kunden müssen sie akzeptieren, bevor sie kaufen
- **Datenschutzrichtlinie** — Einhaltung von GDPR/CCPA; im Fußbereich verknüpft
- **Rückgaberecht** — Definieren Sie Ihren Rückgabetermin, Bedingungen und Erstattungsprozess

## Wartungsmodus

Aktivieren Sie den Wartungsmodus, um Ihr Geschäft vorübergehend offline zu nehmen:
- Zeigt eine benutzerdefinierte Wartungsnachricht an Besuchern an
- Einschränkung des Zugangs auf Admin-Benutzer
- Nützlich während großer Updates oder Migrationen

## Steuer-Einstellungen

Konfigurieren Sie die Steuererhebung unter **Einstellungen > Steuer-Einstellungen**:

1. **Berechnungsmethode** — Nach Versandadresse, Rechnungsadresse oder Geschäftsstandort
2. **Steuersätze** — Definieren Sie Sätze nach Region und Produktsteuerklasse
3. **Steueranzeige** — Zeigen Sie Preise mit Steuer, ohne Steuer oder beides an

## Tipps

- Stellen Sie sicher, dass Ihre Zeitzone korrekt eingestellt ist, bevor Sie Bestellungen verarbeiten — es beeinflusst alle Zeitstempel und Berichte.
- Aktivieren Sie den Gastbestellmodus, um die Umwandlungsrate zu verbessern.
- Geben Sie Ihre Geschäftsadresse an, um genaue Versand- und Steuerberechnungen zu ermöglichen.
- Laden Sie sowohl ein Logo als auch ein Favicon hoch, um eine professionelle, markenbasierte Erfahrung zu gewährleisten.
- Prüfen Sie Ihre rechtlichen Seiten regelmäßig, um die Einhaltung der lokalen Vorschriften sicherzustellen.

## Problembehandlung

**Änderungen werden nicht auf der Storefront angezeigt:**
- Löschen Sie den Cache Ihres Browsers
- Führen Sie eine Cache-Löschen aus dem Admin-Panel durch
- Prüfen Sie, ob der Wartungsmodus versehentlich aktiviert ist

**E-Mails werden nicht gesendet:**
- Überprüfen Sie Ihre E-Mail-Provider-Einstellungen in der E-Mail-Konfiguration
- Prüfen Sie, ob der Domain des "Absender-E-Mail"-Feldes verifiziert ist
- Testen Sie die Verbindung von der Anbieterkonfigurationsseite

**Währungsumrechnung funktioniert nicht:**
- Überprüfen Sie, ob Ihr Wechselkursanbieter verbunden ist
- Prüfen Sie die API-Anmeldeinformationen in den Wechselkurs-Einstellungen
- Versuchen Sie, die Kurse manuell zu aktualisieren

