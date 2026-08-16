---
title: Store-Einstellungen konfigurieren
---

Store Settings ist der zentrale Ort, um die Identität, Lokalisierung, Markenbildung und betrieblichen Einstellungen Ihres Ladens zu konfigurieren. Navigieren Sie zu **Einstellungen > Store-Einstellungen**, um zu beginnen.

![Store-Einstellungen-Registerkarte "Allgemein"](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Allgemeine Registerkarte

Der **Allgemeine**-Tab enthält die Kerneinstellungen für die Identität Ihres Ladens.

### Store-Identität

- **Ladens Name** — Der Anzeigename, der in Titeln von Webseiten, E-Mails und dem Admin-Header angezeigt wird.
- **Slogan** — Eine kurze Beschreibung Ihres Ladens, die für SEO und soziale Medien verwendet wird.
- **Web-URL** — Die öffentliche Webadresse Ihres Ladens. Wird in E-Mails, der Generierung von Sitemaps und dem Aufbau von Links verwendet.

### Kontaktinformationen

- **Kontakt-E-Mail** — Empfängt Bestellbenachrichtigungen und wird in Kundenkommunikationen angezeigt.
- **Telefonnummer** — Optionale Support-Telefonnummer, die im Footer und in E-Mails angezeigt wird.

### Geschäftsadresse

Geben Sie Ihre vollständige Adresse (Straße, Stadt, Bundesland, Postleitzahl, Land) ein. Dies wird für folgende Zwecke verwendet:
- Berechnung des Versandstandorts
- Steuerberechnungen
- Rechtliche Anforderungen und Rechnungen

## Markenbildung

### Logo

Laden Sie Ihr Ladenlogo hoch (PNG oder SVG wird empfohlen, ~200x50px mit transparentem Hintergrund). Das Logo wird angezeigt in:
- Dem Laden-Header
- E-Mail-Vorlagen
- Dem Admin-Bereich

### Favicon

Laden Sie ein quadratisches Favicon hoch (ICO oder PNG, 32x32px). Es wird angezeigt als:
- Das Symbol des Browser-Tabs
- Das Lesezeichen-Symbol
- Das Symbol des mobilen Startbildschirms

## Lokalisierung

### Standard-Sprache

Wählen Sie die primäre Sprache Ihres Ladens aus 10 unterstützten Optionen:

| Sprache | Code |
|----------|------|
| Englisch | en |
| Spanisch | es |
| Französisch | fr |
| Deutsch | de |
| Portugiesisch | pt |
| Japanisch | ja |
| Vereinfachtes Chinesisch | zh-hans |
| Traditionelles Chinesisch | zh-hant |
| Russisch | ru |
| Arabisch | ar |

Die Standard-Sprache steuert die Sprache der Admin-Oberfläche und den Rückgriff für Ladeninhalte.

### Zeitzone

Wählen Sie die Zeitzone Ihres Ladens für genaue Bestellzeitenstempel, geplante Werbeaktionen und Berichte.

### Währung

- **Standard-Währung** — Die primäre Währung für Preise und Buchhaltung.
- **Mehrfache Währung** — Aktivieren Sie diese Option, damit Kunden Preise in ihrer bevorzugten Währung mit automatischer Umrechnung unter Verwendung von Echtzeit-Wechselkursen ansehen können.

Konfigurieren Sie zusätzliche Währungen in **Einstellungen > Store-Einstellungen > Währung**.

## E-Commerce-Einstellungen

### Gast-Bestellung

Erlauben Sie Käufe ohne Anmeldung:
- Schnellerer Checkout-Fluss
- Geringere Hürde für Erstkunden
- Erfasst weniger Kundendaten

### Kontoerstellungszeitpunkt

Steuern Sie, wann Kunden aufgefordert werden, ein Konto zu erstellen:

| Option | Beschreibung |
|--------|-------------|
| **Nach Kauf (Empfohlen)** | Aufforderung zur Kontoerstellung nach einem erfolgreichen Kauf — nutzt den Post-Purchase-Goodwill für die beste Konversion |
| **Während des Checkout** | Ein Konto vor der Bearbeitung der Zahlung erstellen |
| **Vor dem Checkout** | Ein Konto vor dem Einkaufen erfordern (nicht empfohlen - verringert die Konversion) |

Sie können auch eine benutzerdefinierte **Nachricht zur Kontoerstellung** festlegen, um die Vorteile der Registrierung zu erläutern.

### Lagerbestandsstandardwerte

- **Lagerbestand überwachen** — Aktivieren Sie die globale Überwachung des Lagerbestands
- **Schwellenwert für niedrigen Lagerbestand** — Lagerbestand, bei dem Benachrichtigungen für niedrigen Lagerbestand an die Admin-E-Mail gesendet werden (Standard: 10 Einheiten)

## Lagerbestandsintelligenz

![Karten-Intelligenz-Karte mit Feldern "Standard-Wiederbeschaffungszeit" und "Sicherheitsbestand-Multiplikator"](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Diese Einstellungen passen die automatischen Nachbestellung, Sicherheitsbestand und Verkaufsgeschwindigkeit an und steuern, wie mit Lagerbestands- und niedrigen Lagerbestands-Situationen umgegangen wird.

- **Standard-Wiederbeschaffungszeit (Tage)** — Wie viele Tage es im Allgemeinen dauert, bis die Nachschublieferung von Ihrem Lieferanten eintrifft, sobald Sie eine Bestellung aufgeben (Standard: 14).

Die Prognose verwendet dies, um Produkte zu kennzeichnen, die *jetzt* nachbestellt werden müssen, um einen Lagerout vor dem Eintreffen des neuen Lagerbestands zu vermeiden.
- **Sicherheitsbestand-Multiplikator** — Ein Puffer, der auf die erwartete Nachfrage aufgeschlagen wird, um Verkaufsspitzen oder Lieferverzögerungen zu absorbieren.

Beispielsweise wird bei einem Multiplikator von `1,5` ein 50 %iger Puffer über dem berechneten Sicherheitsbestand eingebaut; `2,0` verdoppelt ihn.

Erhöhen Sie diesen Wert für Produkte, bei denen das Ausverkaufen kostbar ist (Bestseller, saisonale Artikel); verringern Sie ihn für langsam verkaufte Artikel, die Sie nicht überbestellen möchten.
- **Geschwindigkeitsberechnungsfenster (Tage)** — Das Rückwärtsfenster, das Spwig verwendet, um die Verkaufsgeschwindigkeit jedes Produkts zu berechnen, was wiederum die Wiederverkaufsvorschläge und die Tage des Vorrats beeinflusst (Standard: 30).

Ein kürzeres Fenster reagiert schneller auf aktuelle Nachfrageveränderungen; ein längeres Fenster glättet saisonale Spitzen, sodass eine einzelne beschäftigte Woche die Vorhersage nicht verfälscht.
- **Standardmäßig Rücklagen erlauben** — Der ursprüngliche Rücklagen-Status, der für neu erstellte Produkte angewandt wird (Standardmäßig ausgeschaltet).

Jedes Produkt kann diesen Wert individuell auf seiner eigenen Produktseite überschreiben, und bestehende Produkte behalten den Wert, den sie bereits haben – das Ändern dieses Werts ändert nur den Standard, mit dem neue Produkte beginnen, es retroaktiviert nicht Ihren Katalog.
- **Häufigkeit der Benachrichtigung bei niedrigem Lagerbestand** — Wie oft Ihre Spwig-Mobile-App über niedrigen Lagerbestand benachrichtigt wird: **Echtzeit** sendet eine Push-Benachrichtigung, sobald ein Produkt seinen Schwelle für niedrigen Lagerbestand überschreitet; **Täglicher Überblick** und **Wöchentliche Zusammenfassung** senden stattdessen eine einzelne Push-Benachrichtigung, die alle derzeit niedrigen Lagerbestand auf dieser Liste zusammenfasst.

Dieser Einstellungsparameter tritt nur in Kraft, während **Benachrichtigungen bei niedrigem Lagerbestand** (E-Mail-Einstellungen, unten) aktiviert ist – bei deaktivierten Benachrichtigungen werden keine Benachrichtigungen auf irgendeine Weise gesendet.

### Dokumente & Rechnungen

![Dokumente & Rechnungen Karte mit in Beispielwerten gefüllten Feldern für Steuer-Identifikationsnummer / Umsatzsteuer-Nummer, Rechnungsfußzeilentext und Packzettel-Fußzeilentext](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Diese Felder füllen die Rechnungen und Packzettel, die Spwig für Bestellungen generiert – beispielsweise wenn ein Händler eine PDF-Rechnung herunterlädt oder per E-Mail versendet, oder einen Packzettel für eine Lieferung ausdruckt.

- **Steuer-Identifikationsnummer / Umsatzsteuer-Nummer** — Ihre Geschäftsteuer-Identifikationsnummer. Auf generierten Rechnungen gedruckt, damit sie lokale Steuerdokumentationsanforderungen erfüllen.
- **Fußzeilentext der Rechnung** — Freier Text, der am Ende jeder generierten Rechnung angezeigt wird. Häufige Anwendung: Zahlungsbedingungen ("Zahlung innerhalb von 30 Tagen"); ein Dankeschön-Mitteilung oder Banküberweisungsdetails.
- **Fußzeilentext des Packzettels** — Freier Text, der am Ende jeder generierten Packzettel angezeigt wird. Häufige Anwendung: Rückgabeanweisungen oder eine Nachricht an das Lager/Verarbeitungsteam.
- **Breite des Dokumentenlogos (px)** — Die Breite Ihres Geschäftlogos, wie es auf generierten PDF-Rechnungen und Packzetteln erscheint (Standard: 200 px). Die Höhe skaliert automatisch, um zu passen, sodass die Proportionen Ihres Logos erhalten bleiben. Das Logo-Bild stammt aus Ihrem **Logo** (Markenbildung, oben) – SVG-Logos werden auf PDF-Dokumenten nicht gezeichnet, also laden Sie eine PNG- oder JPG-Version Ihres Logos hoch, wenn Sie Vektorgrafiken im Geschäft verwenden.

## E-Mail-Einstellungen

Konfigurieren Sie E-Mail-Versand-Einstellungen in **Einstellungen > E-Mail-Konten** und **Einstellungen > E-Mail-Vorlagen**. Siehe [E-Mail-Konfiguration](/help/email-configuration) für detaillierte Informationen.

Wichtige E-Mail-Einstellungen, die in den Store-Einstellungen verfügbar sind:

- **Bestellbestätigungs-E-Mails** — Schalten Sie automatische Bestätigungs-E-Mails ein oder aus
- **Versandbenachrichtigungs-E-Mails** — Schalten Sie Versand-Benachrichtigungen ein oder aus
- **Benachrichtigungen bei niedrigem Lagerbestand** — Senden Sie Benachrichtigungen an die Admin-E-Mail, wenn der Lagerbestand unter die Schwelle fällt
- **E-Mail-Versandmodus** — Live (normaler Versand), Pause (alle E-Mails anhalten) oder Nur Protokoll (Protokoll aufzeichnen, aber niemals senden)
- **Test-E-Mail-Umleitung** — Leiten Sie alle ausgehenden E-Mails an eine Adresse um, um sie zu testen

## Sicherheitseinstellungen

### Zwei-Faktor-Authentifizierung (2FA)

Steuern Sie, ob Mitarbeiter zwei-Faktor-Authentifizierung verwenden müssen:

| Einstellung | Beschreibung |
|---------|-------------|
| **Optional** | Mitarbeiter können sich entscheiden, 2FA zu aktivieren, aber es ist nicht erforderlich |
| **Empfohlen** | Mitarbeiter sehen eine Aufforderung, die sie auffordert, 2FA einzurichten |
| **Erforderlich** | Mitarbeiter können sich nicht in den Admin-Bereich einloggen, bis 2FA aktiviert ist |

Alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Grace Period (Tage)** — Wie viele Tage Mitarbeiter haben, um die 2FA nach der Aktivierung der Durchsetzung einzurichten
- **Vertraute Geräte erlauben** — Ermöglichen Sie es Mitarbeitern, die 2FA-Prüfung auf erkannten Geräten für eine festgelegte Anzahl von Tagen zu umgehen

## Cookie-Einwilligung

Konfigurieren Sie die Cookie-Einwilligungsbanner, die Kunden im Geschäftsbereich sehen:

- **Cookie-Einwilligung aktiviert** — Cookie-Banner anzeigen oder ausblenden
- **Banner-Position** — Wo das Banner auf dem Bildschirm erscheint (untere Leiste, Ecke Popup usw.)
- **Einwilligungsmodus** — Einfache Mitteilung, Opt-in oder Opt-out
- **Banner-Titel und Text** — Anpassbare Überschrift und Beschreibung, die den Besuchern angezeigt werden
- **Kategoriedescription** — Separate Beschreibungen für Analyse-, Marketing- und Funktions-Cookies

Alle Banner-Textfelder unterstützen Übersetzungen für mehrsprachige Stores.

## Kommunikation

Der **Kommunikations**-Tab steuert, wie Ihr Geschäft Kunden bei der Einwilligung in Marketing-E-Mails und SMS erhält, bestätigt und Kunden diese verwalten können. Diese Einstellungen prägen Ihren rechtlichen Compliance-Status (GDPR für E-Mails, TCPA für SMS), weshalb Sie sie vor dem Launch mit Ihrem eigenen Rechtsberater überprüfen sollten – Spwig stellt die Steuerungsmöglichkeiten bereit, nicht den Rat.

![Kommunikationsreiter mit E-Mail-Marketing-Einwilligung, Einstellungen und Abmeldung sowie SMS-Einwilligungskarten](/static/core/admin/img/help/store-settings/communications-tab.webp)

### E-Mail-Marketing-Einwilligung

- **Doppelte Opt-In für Marketing-E-Mails aktivieren** — Wenn aktiviert, erhält ein Kunde, der sich für Marketing-E-Mails einträgt, eine Bestätigungs-E-Mail und muss den Link darin anklicken, bevor Spwig ihm eine Marketingnachricht sendet. Wenn deaktiviert, ist das Abhaken des Marketing-Einwilligungs-Kastens allein ausreichend. Standardmäßig ist dies aktiviert, gemäß den besten Praktiken des GDPR.
- **Standardmäßiger Marketing-Einwilligungsstatus** — Der ursprüngliche Marketing-Einwilligungsstatus, der neu erstellten Kund:innen-Konten zugewiesen wird. Standardmäßig deaktiviert (GDPR-Opt-Out), sodass neue Kunden ursprünglich nicht an Marketing-E-Mails teilnehmen, bis sie aktiv einwilligen.

Wenn die doppelte Opt-In-Funktion aktiviert ist, löst das Einwilligen eine Bestätigungs-E-Mail mit einem Verifizierungslink aus. Bis der Kunde den Link anklickt, wird er als eingerichtet, aber nicht bestätigt aufgezeichnet, und Marketing-Benachrichtigungen werden übersprungen – transaktionale E-Mails (Bestätigungen der Bestellung, Versandupdates, Passwortzurücksetzung) werden durch diese Einstellung nie beeinflusst.

### Einstellungen und Abmeldung

- **Kunden-Einstellungscenter aktivieren** — Wenn aktiviert, können Kunden ihre E-Mail- und SMS-Einstellungen über eine selbstbedienende Seite verwalten, die aus ihrem Kontodashboard verknüpft ist. Wenn deaktiviert, wird diese Seite und ihre unterstützende API unerreichbar angezeigt und der Dashboard-Link wird ausgeblendet. Ein-Klick-Abmelde-Links in Ihren E-Mails funktionieren weiterhin – dieser Notfall ist für die Einhaltung erforderlich und wird durch diesen Schalter nicht beeinflusst.
- **Abmeldegründe sammeln** — Wenn aktiviert, fragt die Ein-Klick-Abmelde-Seite den Kunden nach einem kurzen Grund, bevor die Bestätigung erfolgt: *Ich erhalte zu viele E-Mails*, *Der Inhalt ist nicht für mich relevant*, *Ich habe mich nie dafür angemeldet*, *Ich bin nicht mehr interessiert* oder *Anderer*. Der Grund, den ein Kunde wählt, wird in den Einwilligungs-Prüfprotokoll aufgezeichnet, damit Sie sich über Abmelde-Muster im Zeitverlauf ein Bild machen können.

### SMS-Einwilligung

- **SMS-Verifikation erfordern** — Wenn aktiviert (Standard), muss ein Kunde seine Handynummer mit einem Einmalcode verifizieren, bevor Spwig ihm eine SMS sendet, einschließlich Marketing-Nachrichten. Wenn deaktiviert, ist das Abhaken des SMS-Einwilligungs-Kastens allein ausreichend, um zu beginnen. Dieser Standard wurde aus Sicherheitsgründen für TCPA auf **aktiv** geändert – deaktivieren Sie ihn nur, wenn Sie in Ihrem Anmeldeprozess eine andere Verifizierungsschritt haben.

## Wartungsmodus

Aktivieren Sie den Wartungsmodus, um Ihren Laden vorübergehend offline zu schalten:
- Zeigt eine benutzerdefinierte Wartungsnachricht für Besucher an
- Sie können eine **Wartungsseite** einbinden, die im Page Builder erstellt wurde, für eine vollständig markenbezogene Wartungserfahrung
- Beschränkt den Zugriff auf Admin-Benutzer
- Nützlich bei großen Updates oder Migrationen

## Soziale Medien

Verknüpfen Sie die sozialen Medien-Profil-URLs Ihres Ladens. Diese werden im Footer und in E-Mail-Vorlagen angezeigt:

- **Facebook-URL**
- **Twitter-URL**
- **Instagram-URL**
- **LinkedIn-URL**

## SEO-Standardwerte

Alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

Setzen Sie Standard-Meta-Tags fest, die verwendet werden, wenn Seiten keine eigenen SEO-Einstellungen haben:

- **Meta-Titel** — Standardseitentitel (max. 60 Zeichen)
- **Meta-Beschreibung** — Standardbeschreibung, die in Suchergebnissen angezeigt wird (max. 160 Zeichen)
- **Meta-Schlüsselwörter** — Standardkomma-getrennte Schlüsselwörter

## Steuer-Einstellungen

Konfigurieren Sie die Steuererhebung unter **Einstellungen > Steuer-Einstellungen**:

1. **Berechnungsmethode** — Nach Versandadresse, Rechnungsadresse oder Geschäftsort
2. **Steuersätze** — Steuersätze nach Region und Produktsteuerklasse definieren
3. **Steueranzeige** — Preise mit Steuer, ohne Steuer oder beides anzeigen

## Tipps

- Richten Sie Ihre Zeitzone korrekt ein, bevor Sie Bestellungen verarbeiten — dies wirkt sich auf alle Zeitschichten und Berichte aus.
- Aktivieren Sie die Bezahlung ohne Konto, um die Umwandlungsrate zu erhöhen.
- Füllen Sie Ihre Geschäftadresse aus, um genaue Versand- und Steuerberechnungen zu gewährleisten.
- Laden Sie sowohl ein Logo als auch ein Favicon hoch, um ein professionelles, markenbezogenes Erlebnis zu gewährleisten.
- Verwenden Sie den **Nach dem Kauf**-Zeitpunkt für die Kontenerstellung, um die besten Registrierungsraten zu erzielen.
- Aktivieren Sie die Durchsetzung der Zwei-Faktor-Authentifizierung für Mitarbeiter, um den Store-Admin zu schützen.
- Testen Sie E-Mail-Flüsse mit der **Test-Weiterleitungs-E-Mail**-Einstellung, bevor Sie live gehen.
- Legen Sie die **Standard-Wiederbeschaffungs-Vorlaufzeit** so fest, dass sie Ihrem langsamsten regulären Lieferanten entspricht — die Wiederbeschaffungsprognose wendet diesen einzelnen Wert über Ihr gesamtes Sortiment an, also achten Sie darauf, dass Sie den längsten Vorlaufzeitprodukt-Wert wählen.
- Füllen Sie Ihre **Steuer-ID / Umsatzsteuer-Nummer** und Fußzeilentext vor dem Versand der ersten echten Rechnung an einen Kunden aus — beide Felder sind standardmäßig leer.
- Lassen Sie **Doppelte Opt-In-Einwilligung für Marketing-E-Mails** aktiviert, es sei denn, Sie haben einen spezifischen Grund, sie abzuschalten — dies ist die sicherere Standard-Einstellung für die DSGVO, und sie schützt Ihre Absenderreputation, indem sie unverifizierte Adressen aus den Marketing-Versand-Listen hält.
- Lassen Sie die **Standard-Marketing-Einwilligungseinstellung** aus. Die vorangestellte Einwilligung für Marketing-Einwilligungen untergräbt die DSGVO-Anforderung der Einwilligung, auch wenn ein Kunde theoretisch die Kästchen abwählen könnte.
- Schalten Sie **Kundenpräferenz-Center aktivieren** nicht einfach aus, um Ihr Kontodashboard zu vereinfachen — ohne es können Kunden weiterhin eine einzelne Nachrichtentyp-Abmeldung vornehmen, aber sie verlieren die Fähigkeit, Präferenzen detailliert zu verwalten (z. B. Versand-Updates beibehalten, aber die Newsletter abbestellen).
- Halten Sie **SMS-Verifizierung erforderlich** aktiviert, es sei denn, Ihr Anmeldeprozess bestätigt die Telefonnummer bereits auf andere Weise (z. B. ein SMS-basiertes Login) — diese Einstellung dient speziell dazu, dass Sie innerhalb der TCPA-Regeln bleiben.

## Problembehandlung

**Änderungen sind auf dem Store nicht sichtbar:**
- Löschen Sie den Browser-Cache
- Führen Sie einen Cache-Löschvorgang über das Admin-Panel durch
- Prüfen Sie, ob der Wartungsmodus versehentlich aktiviert ist

**E-Mails werden nicht gesendet:**
- Prüfen Sie Ihre E-Mail-Provider-Einstellungen in der E-Mail-Konfiguration
- Stellen Sie sicher, dass die **E-Mail-Versandmodus**-Einstellung auf **Live** gesetzt ist
- Stellen Sie sicher, dass die **Test-Weiterleitungs-E-Mail** leer ist, wenn Sie E-Mails an echte Empfänger senden möchten

**Währungsumrechnung funktioniert nicht:**
- Prüfen Sie, ob Ihr Wechselkursanbieter verbunden ist
- Prüfen Sie die API-Anmeldeinformationen in den Wechselkurs-Einstellungen
- Versuchen Sie, die Raten manuell zu aktualisieren

**Marketing-E-Mails erreichen Kunden, die sich angemeldet haben, nicht:**
- Prüfen Sie, ob **Doppelte Opt-In-Einwilligung für Marketing-E-Mails** aktiviert ist — falls ja, muss der Kunde den Bestätigungslink in der Verifizierungsemail anklicken, bevor der Marketing-Versand fortgesetzt wird
- Bitten Sie den Kunden, im Spam/Junk-Ordner nach der Bestätigungsemail zu suchen
- Bestätigen Sie, dass die Einwilligung des Kunden für Marketing-E-Mails in seinen Präferenzen noch aktiviert ist — ein Abbestellklick schaltet sie zurück

**Kunden sagen, dass sie das Präferenzcenter nicht finden können:**
- Prüfen Sie, ob **Kundenpräferenz-Center aktivieren** aktiviert ist — wenn es deaktiviert ist, wird der Dashboard-Link ausgeblendet und die Seite ist ausdrücklich nicht verfügbar
- Der Abmeldelink in jeder Marketing-E-Mail funktioniert immer, unabhängig von dieser Einstellung, also weisen Sie Kunden darauf hin, falls nötig

Bleiben Sie alle Markdown-Formatierungen, Bildpfade, Codeblöcke und technischen Begriffe erhalten.