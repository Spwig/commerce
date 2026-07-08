---
title: Steuerkonfiguration
---

Konfigurieren Sie Steuervorschriften für Ihr Geschäft, damit die richtigen Steuern automatisch auf Bestellungen basierend auf der Kundenstandort angewendet werden. Sie können regionale Voreinstellungen mit einem Klick laden oder benutzerdefinierte Regeln für jedes Land, Bundesland, Stadt oder Postleitzahl erstellen.

![Steuer Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Steuer Dashboard

Navigieren Sie zu **Bestellungen > Versand > Steuersätze**, um das Steuerdashboard zu öffnen. Die Seite zeigt:

- **Statistik-Panel** — vier Karten, die Gesamtregeln, aktive Regeln, abgedeckte Länder und verwendete Steuertypen anzeigt
- **Filter** — suchen Sie nach Namen, Land oder Bundesland und filtern Sie nach Land, Steuertyp (Sales Tax, VAT, GST, Custom) oder Status (Aktiv/Inaktiv)
- **Steuervorschriftskarten** — jede Karte zeigt das Landflagge, Regelname, Standort, Steuersatz in Prozent, Steuertyp-Abzeichen, Status-Abzeichen, Priorität und Ausnahmenanzahl

## Steuervoreinstellungen laden

Klicken Sie auf **Voreinstellungen laden**, um das Voreinstellungen-Modal zu öffnen. Voreinstellungen sind Sammlungen von Standardsteuersätzen für eine Region, die mit einem Klick in Ihr Geschäft geladen werden können.

![Voreinstellungen laden](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Voreinstellungen sind nach Weltregionen organisiert:

| Region | Voreinstellung Gruppen |
|--------|--------------|
| **Afrika** | Afrika MwSt (25 Sätze) |
| **Asien-Pazifik** | Asien-Pazifik MwSt/UMSt (24 Sätze), Zentralasien MwSt (6 Sätze) |
| **Europa** | EU MwSt-Sätze, UK MwSt, andere europäische MwSt |
| **Lateinamerika** | Lateinamerika MwSt |
| **Naher Osten** | Naher Osten MwSt |
| **Nordamerika** | US-Bundesstaatliche Umsatzsteuer, kanadische MwSt/HST |
| **Ozeanien** | Ozeanien MwSt/VAT |

### Wie Voreinstellungen funktionieren

1. Klicken Sie auf **Laden** für die Voreinstellunggruppe, die Sie möchten
2. Das System erstellt Steuervorschriften für jedes Land oder Bundesland in dieser Gruppe
3. Bestehende Regeln mit demselben Land, Bundesland und Steuertyp werden automatisch übersprungen, um Duplikate zu vermeiden
4. Nach dem Laden ist jede Regel vollständig bearbeitbar — passen Sie die Sätze an, fügen Sie Ausnahmen hinzu oder deaktivieren Sie Regeln, die Sie nicht benötigen

Sie können mehrere Voreinstellunggruppen laden. Zum Beispiel laden Sie sowohl EU MwSt als auch UK MwSt, wenn Sie Kunden in ganz Europa bedienen.

## Steuervorschriften manuell erstellen

Klicken Sie auf **Steuersatz hinzufügen**, um eine benutzerdefinierte Regel zu erstellen. Das Formular hat vier Abschnitte:

![Steuersatz Formular](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Grundlegende Informationen

| Feld | Beschreibung |
|-------|-------------|
| **Name** | Anzeigename für die Regel (z. B. "Kalifornische Umsatzsteuer") |
| **Aktiv** | Schalter, um die Regel zu aktivieren oder zu deaktivieren |
| **Steuertyp** | Umsatzsteuer, MwSt, Umsatzsteuer oder benutzerdefinierte Steuer |
| **Satz (%)** | Der Steuersatz als Prozent (z. B. geben Sie 8,25 für 8,25% ein) |
| **Priorität** | Höhere Zahlen haben Vorrang, wenn mehrere Regeln denselben Standort übereinstimmen |

### Geografischer Umfang

| Feld | Beschreibung |
|-------|-------------|
| **Land** | ISO 3166-1 alpha-2-Code (z. B. US, GB, DE) |
| **Bundesland** | Bundesland oder Provinz (leer lassen, um das gesamte Land anzuwenden) |
| **Stadt** | Stadtnamen (optional, für stadtbezogene Steuervorschriften) |
| **Postleitzahlen** | Liste spezifischer Postleitzahlen (optional, für postleitzahlenbezogene Steuervorschriften) |

Regeln werden von der spezifischsten zur am wenigsten spezifischen abgeglichen. Eine Regel für eine spezifische Postleitzahl hat Vorrang vor einer Regel für dasselbe Bundesland, die wiederum Vorrang vor einer Regel für das gesamte Land hat.

### Anwendungsvorschriften

| Feld | Beschreibung |
|-------|-------------|
| **Auf Versand anwenden** | Wenn aktiviert, wird diese Steuer auch auf Versandkosten angewendet |
| **Zusammengesetzte Steuer** | Wenn aktiviert, wird diese Steuer zusätzlich zu anderen Steuern berechnet (die Grundsumme plus bereits angewendete Steuern) |

### Produkt-Ausnahmen

| Feld | Beschreibung |
|-------|-------------|
| **Ausgenommene Produkttypen** | Produkttypen, die von dieser Steuer ausgenommen sind (z. B. digitale Produkte, Dienstleistungen) |
| **Ausgenommene Kategorien** | Spezifische Produktkategorien, die von dieser Steuer ausgenommen sind |

## Steuertypen

| Typ | Verwendet für | Beispiele |
|------|----------|---------|
| **Umsatzsteuer** | USA, Kanada | Bundes- und Provinzumsatzsteuer |
| **MwSt** | Europa, UK, viel von Asien und Afrika | Mehrwertsteuer |
| **Umsatzsteuer** | Australien, Neuseeland, Indien, Singapur | Umsatzsteuer auf Waren und Dienstleistungen |
| **Benutzerdefinierte Steuer** | Besondere Fälle | Lokale Zusatzgebühren, Umweltsteuern, Luxussteuern |

## Wie die Steuerberechnung funktioniert

Wenn ein Kunde zur Kasse geht, berechnet das System automatisch Steuern basierend auf seiner Versandadresse:

1. **Geografische Übereinstimmung** — findet alle aktiven Regeln, die dem Kundenland entsprechen, und verengt dann nach Bundesland, Stadt und Postleitzahl
2. **Spezifizitätsbewertung** — spezifischere Regeln (Postleitzahl > Stadt > Bundesland > Land) werden höher bewertet
3. **Prioritätsreihenfolge** — innerhalb derselben Spezifizitätsstufe haben Regeln mit höherer Priorität Vorrang
4. **Produkt-Ausnahmen** — ausgenommene Produkte werden aus jeder anwendbaren Regel ausgeschlossen
5. **Nicht-zusammengesetzte Steuern** — werden zuerst auf den Grundpreis jedes Artikels berechnet
6. **Zusammengesetzte Steuern** — werden auf den Grundpreis plus alle bereits angewendeten nicht-zusammengesetzten Steuern berechnet
7. **Versandsteuer** — wenn eine Regel "Auf Versand anwenden" aktiviert ist, wird der Versandkostenbetrag in den steuerpflichtigen Betrag einbezogen

Die Steuerzusammenbruch wird mit der Bestellung gespeichert, damit Sie genau sehen können, welche Regeln angewendet wurden und wie viel jede beigetragen hat.

## Typische Konfigurationen

### EU-Geschäft

1. Klicken Sie auf **Voreinstellungen laden** und laden Sie die Gruppe **EU MwSt-Sätze**
2. Dies erstellt MwSt-Regeln für alle EU-Mitgliedstaaten mit ihren aktuellen Standard-Sätzen
3. Laden Sie optional **UK MwSt** herunter, wenn Sie auch in das Vereinigte Königreich verkaufen

### US-Geschäft

1. Klicken Sie auf **Voreinstellungen laden** und laden Sie die Gruppe **US-Bundesstaatliche Umsatzsteuer**
2. Dies erstellt Umsatzsteuerregeln für alle US-Bundesstaaten, die Umsatzsteuer erheben
3. Für stadtbezogene Steuern fügen Sie manuell Regeln hinzu, bei denen das Feld Stadt ausgefüllt ist und eine höhere Priorität hat

### Mehrregionales Geschäft

1. Laden Sie mehrere Voreinstellunggruppen für jeden Markt, in dem Sie verkaufen
2. Das System wendet die richtige Steuer basierend auf der Lage jedes Kunden an
3. Passen Sie bei Bedarf einzelne Regeln entsprechend Ihren spezifischen Geschäftsanforderungen an

## Tipps

- **Beginnen Sie mit Voreinstellungen** — laden Sie die Voreinstellunggruppen für Ihre Zielmärkte, und passen Sie dann einzelne Sätze an, anstatt alle Regeln von Grund auf neu zu erstellen.
- **Verwenden Sie Prioritäten sorgfältig** — setzen Sie höhere Prioritätswerte für lokale Regeln, die spezifischer sind, damit sie die breiteren regionalen Regeln richtig überschreiben.
- **Überprüfen Sie zusammengesetzte Steuern sorgfältig** — zusammengesetzte Steuern sind selten. Die meisten Jurisdiktionen verwenden einfache (nicht zusammengesetzte) Steuern. Aktivieren Sie zusammengesetzte Steuern nur, wenn Ihre lokalen Vorschriften explizit die Berechnung von Steuern auf Steuern erfordern.
- **Aktivieren/Deaktivieren Sie Regeln** — anstatt Steuervorschriften für saisonale oder vorübergehende Änderungen zu löschen, schalten Sie sie einfach deaktiviert und aktivieren Sie sie erneut, wenn sie benötigt werden.
- **Testen Sie vor der Veröffentlichung** — nachdem Sie Ihre Steuervorschriften eingerichtet haben, erstellen Sie eine Testbestellung von verschiedenen Adressen, um sicherzustellen, dass die richtigen Steuern angewendet werden.