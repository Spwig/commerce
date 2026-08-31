---
title: Konfigurieren der Shop-Einstellungen
---

Shop-Einstellungen ist der zentrale Ort, um die Identität, Lokalisierung, das Branding und die betrieblichen Einstellungen Ihres Shops zu konfigurieren. Navigieren Sie zu **Einstellungen > Shop-Einstellungen**, um zu beginnen.

![Allgemeiner Tab der Shop-Einstellungen](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Allgemeiner Tab

Der Tab **Allgemein** enthält die grundlegenden Identitätseinstellungen Ihres Shops.

### Shop-Identität

- **Shop-Name** — Der Anzeigename, der in Seitentiteln, E-Mails und der Admin-Kopfzeile angezeigt wird.
- **Slogan** — Eine kurze Beschreibung Ihres Shops, die in SEO und beim Teilen in sozialen Medien verwendet wird.
- **Site-URL** — Die öffentliche Webadresse Ihres Shops. Dies wird in E-Mails, bei der Sitemap-Erstellung und beim Linkaufbau verwendet.

### Kontaktinformationen

- **Kontakt-E-Mail** — Empfängt Bestellbenachrichtigungen und wird in Kundenkommunikation angezeigt.
- **Telefonnummer** — Optionale Support-Telefonnummer, die im Footer und in E-Mails angezeigt wird.

### Geschäftsadresse

Geben Sie Ihre vollständige Adresse (Straße, Stadt, Bundesland, Postleitzahl, Land) ein. Dies wird für Folgendes verwendet:
- Berechnung des Versandorts
- Steuerberechnungen
- Rechtliche Anforderungen und Rechnungen

## Branding

### Logo

Laden Sie Ihr Shop-Logo hoch (PNG oder SVG empfohlen, ca. 200x50px mit transparentem Hintergrund). Das Logo erscheint in:
- Der Shop-Kopfzeile
- E-Mail-Vorlagen
- Dem Admin-Panel

### Favicon

Laden Sie ein quadratisches Favicon (ICO oder PNG, 32x32px) hoch. Es erscheint als:
- Browser-Tab-Symbol
- Lesezeichen-Symbol
- Symbol auf dem mobilen Startbildschirm

## Lokalisierung

### Standardsprache

Wählen Sie die Primärsprache Ihres Shops aus 10 unterstützten Optionen:

| Sprache | Code |
|----------|------|
| Englisch | en |
| Spanisch | es |
| Französisch | fr |
| Deutsch | de |
| Portugiesisch | pt |
| Japanisch | ja |
| Chinesisch (vereinfacht) | zh-hans |
| Chinesisch (traditionell) | zh-hant |
| Russisch | ru |
| Arabisch | ar |

Die Standardsprache steuert die Sprache der Admin-Oberfläche und den Fallback für Shop-Inhalte.

### Zeitzone

Wählen Sie die Zeitzone Ihres Shops für genaue Bestellzeitstempel, geplante Aktionen und Berichte.

### Währung

- **Standardwährung** — Die primäre Währung für Preise und Buchhaltung.
- **Mehrwährung** — Aktivieren Sie diese Option, um Kunden die Anzeige von Preisen in ihrer bevorzugten Währung mit automatischer Umrechnung anhand aktueller Wechselkurse zu ermöglichen.

Konfigurieren Sie zusätzliche Währungen unter **Einstellungen > Shop-Einstellungen > Währung**.

## E-Commerce-Einstellungen

### Gast-Kasse

Erlaubt Käufe ohne Erstellung eines Kontos:
- Schnellere Kassenabwicklung
- Geringere Hürden für Erstkaufende
- Erfasst weniger Kundendaten

### Zeitpunkt der Kontoerstellung

Steuern Sie, wann Kunden zur Erstellung eines Kontos aufgefordert werden:

| Option | Beschreibung |
|--------|-------------|
| **Nach dem Kauf (Empfohlen)** | Aufforderung zur Kontoerstellung nach einer erfolgreichen Bestellung — nutzt die positive Stimmung nach dem Kauf für die beste Conversion |
| **Während der Kasse** | Konto erstellen, bevor die Zahlung verarbeitet wird |
| **Vor der Kasse** | Konto erforderlich, bevor eingekauft wird (nicht empfohlen — reduziert die Conversion) |

Sie können auch eine benutzerdefinierte **Kontoerstellungs-Nachricht** festlegen, um die Vorteile der Registrierung zu erklären.

### Lagerbestands-Standardwerte

- **Lagerbestand verfolgen** — Globale Bestandsverfolgung aktivieren
- **Schwellerwert für niedrigen Bestand** — Bestandsniveau, bei dem Warnungen vor niedrigem Bestand an die Admin-E-Mail gesendet werden (Standard: 10 Einheiten)

### Lagerintelligenz

![Karte der Lagerintelligenz mit den Feldern Standard-Nachschub-Laufzeit, Sicherheitsbestand-Multiplikator, Umsatzgeschwindigkeits-Berechnungsfenster, Standardmäßig Nachbestellungen erlauben und Häufigkeit der Warnungen vor niedrigem Bestand](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Diese Einstellungen passen die automatischen Berechnungen für Nachschub, Sicherheitsbestand und Umsatzgeschwindigkeit an und steuern, wie Situationen mit fehlendem oder niedrigem Bestand behandelt werden.

- **Standard-Nachschub-Laufzeit (Tage)** — Wie viele Tage es in der Regel dauert, den Nachschub vom Lieferanten zu erhalten, nachdem eine Bestellung aufgegeben wurde (Standard: 14).

Die Prognosefunktion verwendet dies, um Produkte zu kennzeichnen, die *jetzt* nachbestellt werden müssen, um einen Lagerbestand von null zu vermeiden, bevor der neue Bestand eintrifft.
- **Sicherheitsbestand-Multiplikator** — Ein Puffer, der über die erwartete Nachfrage hinaus angewendet wird, um Verkaufsspitzen oder Lieferverzögerungen abzufedern.

Zum Beispiel baut ein Multiplikator von `1,5` einen 50 %igen Puffer über den berechneten Sicherheitsbestand ein; `2,0` verdoppelt ihn.

Erhöhen Sie diesen Wert für Produkte, bei denen ein Ausfall kostspielig ist (Bestseller, saisonale Artikel); senken Sie ihn für langsam verkaufte Ware, die Sie nicht überbestellen möchten.
- **Berechnungszeitraum für die Absatzgeschwindigkeit (Tage)** — Der Rückblick-Zeitraum, den Spwig verwendet, um die Absatzgeschwindigkeit jedes Produkts zu berechnen, was wiederum die Nachbestellvorschläge und die Vorratstage beeinflusst (Standard: 30).

Ein kürzerer Zeitraum reagiert schneller auf aktuelle Nachfrageänderungen; ein längerer Zeitraum glättet saisonale Spitzen, sodass eine einzelne geschäftige Woche die Prognose nicht verfälscht.
- **Rückbestellungen standardmäßig erlauben** — Die anfängliche Einstellung für Rückbestellungen, die neu erstellten Produkten zugewiesen wird (standardmäßig deaktiviert).

Jedes Produkt kann dies auf seiner eigenen Produktseite individuell überschreiben, und bestehende Produkte behalten ihre bereits vorhandenen Einstellungen bei — die Änderung dieser Einstellung ändert nur den Standardwert, mit dem neue Produkte starten, und aktualisiert Ihren Katalog nicht rückwirkend.
- **Häufigkeit der Warnungen bei niedrigem Bestand** — Wie oft Ihre Spwig-App über niedrigen Bestand benachrichtigt wird: **Echtzeit** sendet eine Push-Benachrichtigung, sobald ein Produkt seinen Schwellenwert für niedrigen Bestand unterschreitet; **Tägliche Zusammenfassung** und **Wöchentliche Übersicht** senden stattdessen eine einzelne Push-Benachrichtigung, die alle aktuell lagernden Produkte mit niedrigem Bestand auf diesem Zeitplan zusammenfasst.

Diese Einstellung wirkt sich nur aus, wenn **Warnungen bei niedrigem Bestand** (E-Mail-Einstellungen, unten) aktiviert ist — bei deaktivierten Warnungen werden keine Benachrichtigungen auf irgendeiner Frequenz gesendet.

### Dokumente & Rechnungen

![Karte für Dokumente & Rechnungen mit ausgefüllten Feldern für Steuernummer / USt-IdNr., Fußzeilentext der Rechnung, Fußzeilentext des Lieferscheins und Logo-Breite der Dokumente mit Beispielwerten](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Diese Felder füllen die Rechnungen und Lieferscheine aus, die Spwig für Bestellungen erstellt — beispielsweise, wenn ein Händler eine PDF-Rechnung herunterlädt oder per E-Mail versendet, oder einen Lieferschein für eine Sendung druckt.

- **Steuernummer / USt-IdNr.** — Ihre geschäftliche Steueridentifikationsnummer. Wird auf generierten Rechnungen gedruckt, damit diese den lokalen steuerlichen Dokumentationsanforderungen entsprechen.
- **Fußzeilentext der Rechnung** — Freitext, der am unteren Rand jeder generierten Rechnung angezeigt wird. Häufige Verwendungszwecke: Zahlungsbedingungen ("Zahlung innerhalb von 30 Tagen fällig"), eine Dankesnachricht oder Bankverbindungsdetails.
- **Fußzeilentext des Lieferscheins** — Freitext, der am unteren Rand jedes generierten Lieferscheins angezeigt wird. Häufige Verwendungszwecke: Rücksendeanweisungen oder eine Notiz für das Lager-/Versandteam.
- **Logo-Breite der Dokumente (px)** — Die Breite Ihres Store-Logos, wie es auf generierten PDF-Rechnungen und Lieferscheinen erscheint (Standard: 200px). Die Höhe skaliert automatisch entsprechend, sodass die Proportionen Ihres Logos erhalten bleiben. Das Logobild selbst stammt aus Ihrem **Logo** (Branding, oben) — SVG-Logos werden nicht auf PDF-Dokumenten gezeichnet, daher laden Sie eine PNG- oder JPG-Version Ihres Logos hoch, wenn Sie Vektorgrafiken im Store verwenden.

## E-Mail-Einstellungen

Konfigurieren Sie die E-Mail-Versand-Einstellungen unter **Einstellungen > E-Mail-Konten** und **Einstellungen > E-Mail-Vorlagen**. Weitere Details finden Sie unter [E-Mail-Konfiguration](/help/email-configuration).

Wichtige E-Mail-Einstellungen, die in den Store-Einstellungen verfügbar sind:

- **Bestätigungs-E-Mails** — Automatische Bestätigungs-E-Mails ein- oder ausschalten
- **Versandbenachrichtigungs-E-Mails** — Versand-Update-Benachrichtigungen ein- oder ausschalten
- **Warnungen bei niedrigem Bestand** — Sendet Warnungen an die Admin-E-Mail, wenn der Bestand unter den Schwellenwert fällt
- **E-Mail-Versandmodus** — Live (normaler Versand), Pausiert (alle E-Mails zurückhalten) oder Nur protokollieren (aufzeichnen, aber nie senden)
- **Test-Umleitungse-Mail** — Leitet alle ausgehenden E-Mails an eine einzelne Adresse zum Testen um

## Sicherheitseinstellungen

### Zwei-Faktor-Authentifizierung (2FA)

Steuern Sie, ob Mitarbeiter die Zwei-Faktor-Authentifizierung verwenden müssen:


| Einstellung | Beschreibung |
|---------|-------------|
| **Optional** | Mitarbeiter können die 2FA aktivieren, es ist jedoch nicht erforderlich |
| **Empfohlen** | Mitarbeiter sehen einen Hinweis, der sie ermutigt, die 2FA einzurichten |
| **Erforderlich** | Mitarbeiter können den Adminbereich nicht aufrufen, bis die 2FA aktiviert ist |

- **Gnadenfrist (Tage)** — Wie viele Tage Mitarbeiter haben, um die 2FA nach der Aktivierung der Durchsetzung einzurichten
- **Vertrauenswürdige Geräte zulassen** — Ermöglicht es Mitarbeitern, die 2FA-Verifizierung auf erkannten Geräten für eine festgelegte Anzahl von Tage zu überspringen

## Cookie-Einwilligung

Konfigurieren Sie die Cookie-Einwilligungsbanner, die Storefront-Besuchern angezeigt werden:

- **Cookie-Einwilligung aktiviert** — Zeigt oder blendet das Cookie-Banner aus
- **Banner-Position** — Wo das Banner auf dem Bildschirm erscheint (untere Leiste, Eck-Popup usw.)
- **Einwilligungsmodus** — Einfache Benachrichtigung, Opt-in oder Opt-out
- **Banner-Titel und Text** — Anpassbarer Titel und Beschreibung, die Besuchern angezeigt werden
- **Kategorie-Beschreibungen** — Separate Beschreibungen für Analyse-, Marketing- und Funktions-Cookies

Alle Banner-Textfelder unterstützen Übersetzungen für mehrsprachige Stores.

## Kommunikation

Der Reiter **Kommunikation** steuert, wie Ihr Store die Einwilligung für Marketing-E-Mails und SMS einholt, bestätigt und es Kunden ermöglicht, diese Einwilligung zu verwalten. Diese Einstellungen bestimmen Ihre rechtliche Compliance-Position (GDPR für E-Mails, TCPA für SMS), daher sollten Sie sie vor dem Launch mit Ihrem eigenen Rechtsbeistand überprüfen — Spwig stellt die Steuerungselemente bereit, aber keine Rechtsberatung.

![Kommunikationsreiter mit Karten für E-Mail-Marketing-Einwilligung, Einstellungen & Abmeldung und SMS-Einwilligung](/static/core/admin/img/help/store-settings/communications-tab.webp)

### E-Mail-Marketing-Einwilligung

- **Doppelte Opt-in für Marketing-E-Mails aktivieren** — Wenn aktiviert, erhält ein Kunde, der sich für Marketing-E-Mails anmeldet, eine Bestätigungs-E-Mail und muss den darin enthaltenen Link klicken, bevor Spwig ihm eine Marketing-Nachricht sendet. Wenn deaktiviert, reicht das Ankreuzen des Marketing-Opt-in-Kastens allein aus. Standardmäßig aktiviert, im Einklang mit den GDPR-Best Practices.
- **Standard-Marketing-Opt-in-Zustand** — Der anfängliche Marketing-Opt-in-Zustand, der neu erstellten Kundenkonten zugewiesen wird. Standardmäßig deaktiviert (GDPR Opt-out), sodass neue Kunden zunächst von Marketing-E-Mails abgemeldet sind, bis sie sich aktiv anmelden.

Wenn die doppelte Opt-in aktiviert ist, löst die Anmeldung eine Bestätigungs-E-Mail mit einem Verifizierungslink aus. Bis der Kunde darauf klickt, wird er als angemeldet, aber nicht bestätigt erfasst, und Marketing-Sendungen werden übersprungen — transaktionale E-Mails (Bestellbestätigungen, Versandupdates, Passwort-Resets) werden von dieser Einstellung nie beeinflusst.

### Einstellungen & Abmeldung

- **Kundeneinstellungszentrum aktivieren** — Wenn aktiviert, können Kunden ihre E-Mail- und SMS-Einstellungen über eine Selbstbedienungsseite verwalten, die von ihrem Kontodashboard verlinkt ist. Wenn deaktiviert, ist diese Seite und ihre unterstützende API nicht verfügbar und der Dashboard-Link wird ausgeblendet. Ein-Klick-Abmelde-Links in Ihren E-Mails funktionieren in beiden Fällen weiterhin — dieser Ausweg ist für die Compliance erforderlich und wird von diesem Schalter nicht beeinflusst.
- **Abmeldegründe erfassen** — Wenn aktiviert, fragt die Ein-Klick-Abmelde-Seite den Kunden vor der Bestätigung nach einem kurzen Grund: *Ich erhalte zu viele E-Mails*, *Der Inhalt ist für mich nicht relevant*, *Ich habe mich nie dafür angemeldet*, *Ich habe kein Interesse mehr* oder *Sonstiges*. Der von einem Kunden ausgewählte Grund wird im Einwilligungs-Audit-Trail erfasst, sodass Sie Abmelde-Muster im Laufe der Zeit überprüfen können.

### SMS-Einwilligung

- **SMS-Verifizierung erforderlich** — Wenn aktiviert (Standard), muss ein Kunde seine Telefonnummer mit einem Einmal-Code verifizieren, bevor Spwig ihm eine SMS sendet, einschließlich Marketing-SMS. Wenn deaktiviert, reicht das Ankreuzen des SMS-Opt-in-Kastens allein aus, um mit dem Senden zu beginnen. Dieser Standard wurde aus TCPA-Sicherheitsgründen auf **aktiviert** geändert — deaktivieren Sie ihn nur, wenn Sie einen anderen Verifizierungsschritt in Ihrem Anmeldeprozess haben.

## Wartungsmodus

Aktivieren Sie den Wartungsmodus, um Ihren Store vorübergehend offline zu nehmen:
- Zeigt Besuchern eine benutzerdefinierte Wartungsnachricht an
- Sie können eine **Wartungsseite** verlinken, die im Page Builder erstellt wurde, für ein vollständig markenkonformes Wartungserlebnis
- Beschränkt den Zugriff auf Admin-Benutzer
- Nützlich während großer Updates oder Migrationen

## Soziale Medien

Verknüpfen Sie die sozialen Medien des Ladens. Diese werden im Footer und in E-Mail-Vorlagen angezeigt:

- **Facebook-URL**
- **Twitter-URL**
- **Instagram-URL**
- **LinkedIn-URL**

## SEO-Standardwerte

Legen Sie Standard-Meta-Tags fest, die verwendet werden, wenn Seiten keine eigenen SEO-Einstellungen haben:

- **Meta-Titel** — Standardseitentitel (max. 60 Zeichen)
- **Meta-Beschreibung** — Standardbeschreibung, die in Suchergebnissen angezeigt wird (max. 160 Zeichen)
- **Meta-Schlüsselwörter** — Standard-komma-getrennte Schlüsselwörter

## Steuer-Einstellungen

Richten Sie die Steuererhebung unter **Einstellungen > Steuer-Einstellungen** ein:

1. **Berechnungsmethode** — Nach Versandadresse, Rechnungsadresse oder Geschäftsort
2. **Steuersätze** — Legen Sie Sätze nach Region und Produktsteuerklasse fest
3. **Steueranzeige** — Preise mit Steuer, ohne Steuer oder beides anzeigen

## Tipps

- Stellen Sie sicher, dass Ihre Zeitzone korrekt eingestellt ist, bevor Sie Bestellungen verarbeiten — dies beeinflusst alle Zeitenstempel und Berichte.
- Aktivieren Sie den Gastkauf, um die Konversionsrate zu verbessern.
- Füllen Sie Ihre Geschäftadresse aus, um genaue Versand- und Steuerberechnungen zu gewährleisten.
- Laden Sie ein Logo und ein Favicon hoch, um ein professionelles, markenbezogenes Erlebnis zu gewährleisten.
- Verwenden Sie den **Nach Kauf**-Zeitpunkt für die Konton creation, um die besten Registrierungsraten zu erzielen.
- Aktivieren Sie die Durchsetzung der Zwei-Faktor-Authentifizierung für Mitarbeiter, um den Ladenadmin zu schützen.
- Testen Sie E-Mail-Flüsse mit der **Testumleitungsemail**-Einstellung, bevor Sie live gehen.
- Legen Sie die **Standard-Wiederbeschaffungs-Vorlaufzeit** so fest, dass sie Ihrem langsamsten regulären Lieferanten entspricht — die Wiederbeschaffungsprognose wendet diesen einzelnen Wert über Ihr gesamtes Sortiment an, also achten Sie darauf, dass Sie sich bei der längsten Vorlaufzeit entscheiden.
- Verkürzen Sie das **Geschwindigkeitsberechnungsfenster**, wenn Sie häufige Werbeaktionen oder Nachschub durchführen und die Prognose schnell auf die letzten Tage des Verkaufs reagieren möchte; verlängern Sie es, um eine stabilere, weniger starken Schwankungen unterliegende Sicht auf die Nachfrage zu erhalten.
- Wenn Sie **Standardmäßig Rückbestellungen erlauben** aktivieren, beachten Sie, dass dies nur den Ausgangspunkt für Produkte darstellt, die *nach* der Änderung erstellt werden — besuchen Sie bei Bedarf einzelne Produkte erneut, wenn Sie Rückbestellungen für Ihr aktuelles Sortiment aktivieren möchten.
- Passen Sie die **Benachrichtigungshäufigkeit bei niedrigem Lagerbestand** an, wie aktiv Sie den Lagerbestand verwalten: **Echtzeit** für schnelle Kataloge, bei denen jede Lagerauslastung sofort beachtet werden muss, **Täglicher Überblick** oder **Wöchentliche Zusammenfassung**, um bei einem größeren Katalog Alert-Fatigue zu vermeiden.
- Füllen Sie Ihre **Steuer-ID / Umsatzsteuer-Nummer** und Fußzeilentext vor dem ersten echten Rechnungsausgang an einen Kunden aus — beide Felder sind standardmäßig leer.
- Wenn Ihr **Logo** ein SVG ist, laden Sie auch eine PNG- oder JPG-Version hoch — die **Dokument-Breite des Logos** hat keinen Einfluss auf PDFs, da Spwig keine SVG-Kunstwerke auf generierten Rechnungen und Versandbelegen zeichnen kann.
- Lassen Sie **Doppelter Opt-In für Marketing-E-Mails** aktiviert, es sei denn, Sie haben einen spezifischen Grund, es auszuschalten — es ist die sicherere Standardoption für die DSGVO, und es schützt Ihre Absenderreputation, indem es unverifizierte Adressen aus Ihren Marketing-Versand-Listen hält.
- Lassen Sie **Standardmäßige Marketing-Zustimmung** aus. Das vorab markierte Einverständnis für Marketing-Anliegen untergräbt die DSGVO-Anforderung zur Zustimmung, auch wenn ein Kunde die Zustimmung theoretisch deaktivieren könnte.
- Schalten Sie **Kundenpräferenzcenter erforderlich** nicht einfach aus, um Ihr Kontodashboard zu vereinfachen — ohne es können Kunden weiterhin eine einzelne Nachrichtentypen abmelden, aber sie verlieren die Fähigkeit, Präferenzen detailliert zu verwalten (z. B. Versandupdates beibehalten, aber den Newsletter abmelden).
- Halten Sie **SMS-Verifizierung erforderlich** aktiviert, es sei denn, Ihr Anmeldefluss bestätigt die Mobilnummer bereits auf andere Weise (z. B. ein SMS-basiertes Anmeldeverfahren) — die Einstellung dient speziell dazu, Sie in den TCPA-Regeln zu halten.

**Währungsumrechnung funktioniert nicht:**
- Stellen Sie sicher, dass Ihr Wechselkursanbieter verbunden ist
- Prüfen Sie die API-Anmeldeinformationen in den Einstellungen für Wechselkurse
- Versuchen Sie, die Wechselkurse manuell zu aktualisieren

**Marketing-E-Mails erreichen Kunden, die sich angemeldet haben:**
- Prüfen Sie, ob **Doppelter Opt-In für Marketing-E-Mails aktiviert ist** – falls ja, muss der Kunde auf den Bestätigungslink in der Verifizierungsemail klicken, bevor das Marketing fortgesetzt wird
- Bitten Sie den Kunden, die Spam-/Junk-E-Mails zu prüfen, auf die Bestätigungs-E-Mail
- Bestätigen Sie, dass der Marketing-Opt-In des Kunden in seinen Einstellungen aktiviert ist – ein Abmelden-Link schaltet ihn wieder aus

**Kunden sagen, sie können das Einstellungszentrum nicht finden:**
- Prüfen Sie, ob **Kunden-Einstellungszentrum aktiviert ist** – wenn es deaktiviert ist, wird der Dashboard-Link ausgeblendet und die Seite ist ausdrücklich nicht verfügbar
- Der Abmeldelink in jeder Marketing-E-Mail funktioniert immer, unabhängig von diesem Einstellung, also weisen Sie Kunden darauf hin, als Fallback zu verwenden