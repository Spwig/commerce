---
title: Form Builder Overview
---

Der Form Builder erstellt benutzerdefinierte Formulare zur Datensammlung – Kontaktformulare, Umfragen, Anträge, Registrierungen und mehr. Erstellen Sie visuell Formulare mit Drag-and-Drop-Feldern, konfigurieren Sie Validierungsregeln, aktivieren Sie mehrschrittige Workflows und sammeln Sie Antworten mit detaillierten Analysen. Formulare integrieren sich nahtlos in Elemente des Page Builders und können an beliebigen Stellen auf Ihrer Website eingebettet werden. Alle Einreichungen werden in der Datenbank gespeichert, einschließlich vollständiger Metadaten (IP-Adresse, Browser, Zeit bis zur Beendigung), um sie zur Analyse und Exportierung zu verwenden.

Verwenden Sie den Form Builder, wenn Sie strukturierte Daten von Kunden sammeln müssen, egal ob es sich um einfache Kontaktinformationen oder komplexe mehrseitige Anträge handelt.

## Was ist der Form Builder?

Der Form Builder ist ein visuelles Drag-and-Drop-Tool zur Erstellung benutzerdefinierter Formulare ohne Code:

**Unterstützte Formtypen**:
- Kontaktformulare (Name, E-Mail, Nachricht)
- Kundenumfragen (Bewertungen, Feedback, NPS)
- Produktregistrierungen (Garantie, Support)
- Stellenbewerbungen (Lebenslauf-Upload, mehrschrittig)
- Veranstaltungsregistrierungen (Teilnehmerinformationen, Präferenzen)
- Serviceanfragen (detaillierte Anforderungen)
- Newsletter-Abonnements (mit Häkchen für Präferenzen)

**Wichtige Funktionen**:
- **22 Feldtypen** - Text, E-Mail, Telefon, Dateiupload, Bewertungen, Produktauswahlfelder und mehr
- **Mehrschrittige Formulare** - Teilen Sie lange Formulare in logische Schritte mit Fortschrittsverfolgung auf
- **Bedingte Logik** - Zeigen Sie/verbergen Sie Felder basierend auf Benutzerantworten
- **Validierungsregeln** - Erforderliche Felder, Min/Max-Länge, benutzerdefinierte Regex-Muster
- **Spam-Schutz** - Honeypot-Felder oder Google reCAPTCHA v3
- **Antwortanalyse** - Verfolgen Sie die Bearbeitungszeit, die IP-Adresse, den Browser, den Verweis
- **CSV-Export** - Laden Sie alle Antworten herunter, um sie in Excel/Google Sheets zu analysieren
- **Mehrsprachigkeit** - Übersetzen Sie Formularbezeichnungen und Nachrichten in alle aktiven Sprachen

## Erstellen Sie Ihr erstes Formular

Navigieren Sie zu **Einstellungen > Seiten > Formulare**, um den Formular-Manager zu öffnen:

**Schritt 1: Neues Formular erstellen**
- Klicken Sie auf **+ Neues Formular erstellen**
- Geben Sie einen Formularnamen ein (interne Kennung, wird Kunden nicht angezeigt)
- Geben Sie einen Formulartitel ein (wird als Überschrift über dem Formular angezeigt)
- Optional: Fügen Sie eine Beschreibung hinzu (Hilfetext, der unter dem Titel angezeigt wird)

**Schritt 2: Felder hinzufügen**
- Klicken Sie auf **Formular-Design bearbeiten**, um den visuellen Builder zu öffnen
- Ziehen Sie Feldtypen aus der linken Seitenleiste auf das Canvas
- Klicken Sie auf ein Feld, um es in der rechten Panel zu konfigurieren
- Legen Sie Bezeichnung, Platzhalter, Hilfetext fest
- Schalten Sie den erforderlichen Status um
- Fügen Sie Validierungsregeln hinzu

**Schritt 3: Formular-Einstellungen konfigurieren**
- Legen Sie den Text für den Absenden-Button fest (Standard: "Absenden")
- Personalisieren Sie die Erfolgsnachricht (wird nach der Einreichung angezeigt)
- Wählen Sie Spam-Schutz (Honeypot empfohlen)
- Schalten Sie "Anmeldung erforderlich" um, wenn nötig
- Aktivieren Sie "Mehrschrittiges Formular" für komplexe Formulare

**Schritt 4: Formular aktivieren**
- Schalten Sie den **Aktiv**-Status um
- Nur aktive Formulare akzeptieren Einreichungen
- Speichern Sie das Formular

**Schritt 5: In Page Builder verwenden**
- Fügen Sie das **Formular**-Element zu einer beliebigen Seite hinzu
- Wählen Sie Ihr Formular aus dem Dropdownmenü aus
- Das Formular erbt die Seitenstilvorlagen
- Einreichungen werden automatisch an den Backend gesendet

## Einseitige vs. Mehrschrittige Formulare

**Einseitige Formulare** (Standard):
- Alle Felder werden gleichzeitig angezeigt
- Scrollen Sie, um alle Felder zu sehen
- Absenden-Button am unteren Rand
- Bestens geeignet für: Kontaktformulare, kurze Umfragen, einfache Datensammlung

**Mehrschrittige Formulare**:
- Felder sind in nummerierte Schritte organisiert
- Fortschrittsleiste zeigt den aktuellen Schritt an
- Zurück/Weiter-Navigationsbuttons
- Absenden nur auf dem letzten Schritt
- Optional: Teilweise Antworten speichern (Entwurfmodus)
- Bestens geeignet für: Stellenbewerbungen, Registrierungen, komplexe Umfragen, Checkout-Flows

**Mehrschrittiges Formular aktivieren**:
1. Schalten Sie "Mehrschrittiges Formular" in den Formulareinstellungen um
2. Klicken Sie auf die Registerkarte **Schritte** in der rechten Panel
3. Fügen Sie einen Schritt hinzu (z. B. "Persönliche Daten", "Kontaktdetails", "Präferenzen")
4. Weisen Sie Felder Schritten zu, indem Sie beim Bearbeiten eines Felds das Schrittdropdown auswählen
5. Reihenfolge der Schritte durch Ziehen anpassen
6. Schritt-Eigenschaften festlegen: Titel, Beschreibung, überspringbar

**Vorteile von Mehrschrittformularen**:
- Reduziert das Abbrechen von Formularen (psychologisch: "Nur 3 Fragen auf dieser Seite")
- Logische Gruppierung verbessert die Benutzererfahrung
- Fortschrittsanzeige motiviert zur Beendigung
- Optionaler Entwurfsspeicher für lange Formulare

## Formulareinstellungen erläutert

**Grundlegende Einstellungen**:
- **Interne Bezeichnung** - Wie Sie das Formular im Admin-Panel identifizieren (nicht für Kunden sichtbar)
- **Slug** - URL-freundliche Bezeichnung (automatisch generiert, wird in API-Endpunkten verwendet)
- **Formulartitel** - Überschrift, die über dem Formular angezeigt wird
- **Beschreibung** - Optionaler Hilfetext, der unter dem Titel angezeigt wird
- **Text des Absenden-Buttons** - Personalisieren Sie die Schaltflächenbezeichnung (z. B. "Nachricht senden", "Jetzt bewerben")

**Nachrichten**:
- **Erfolgsnachricht** - Wird nach erfolgreicher Einreichung angezeigt (Standard: "Vielen Dank für Ihre Einreichung!")
- **Fehlermeldung** - Wird angezeigt, wenn die Einreichung fehlschlägt (Standard: "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.")

**Sicherheit & Zugriff**:
- **Aktiv** - Nur aktive Formulare akzeptieren Einreichungen (inaktive Formulare zeigen "Formular nicht verfügbar" an)
- **Anmeldung erforderlich** - Einschränkung auf authentifizierte Benutzer (anonyme Benutzer sehen einen Anmeldehinweis)

**Spam-Schutz**:
- **Keiner** - Keine Schutzmaßnahmen (nicht empfohlen, Bots werden spammen)
- **Honeypot-Feld** - Unsichtbares Feld, das Bots erwischt (empfohlen für die meisten Händler)
- **Google reCAPTCHA v3** - Erfordert Site-Schlüssel und Geheimen Schlüssel von Google (stärkster Schutz)

**Erweiterte Funktionen**:
- **Mehrschrittiges Formular** - Aktivieren Sie einen Schritt-für-Schritt-Workflow
- **Teilweise Antworten speichern** - Ermöglicht Benutzern, den Fortschritt zu speichern und später fortzusetzen (nur bei mehrschrittigen Formularen)

## Spam-Schutz-Optionen

**Honeypot-Feld (Empfohlen)**:
- Unsichtbares Feld wird dem Formular hinzugefügt
- Bots füllen es aus (Menschen können es nicht sehen)
- Einreichungen mit ausgefülltem Honeypot werden abgelehnt
- Keine Konfiguration erforderlich
- Keine CAPTCHA-Frust für Benutzer
- Wirksam gegen 95 % + der Spam-Bots

**Google reCAPTCHA v3**:
- Unsichtbarer Hintergrundscore (0,0-1,0)
- Kein "Verkehrszeichen klicken"-Challenge
- Erfordert Einrichtung:
  1. Erstellen Sie ein Konto bei google.com/recaptcha/admin
  2. Generieren Sie Site-Schlüssel und Geheimen Schlüssel
  3. Geben Sie die Schlüssel in den Formular-Builder-Einstellungen ein
- Robuster als Honeypot
- Verwenden Sie es, wenn Honeypot unzureichend ist

**Keiner**:
- Kein Spam-Schutz
- Nur für interne Formulare oder Tests verwenden
- Öffentliche Formulare werden stark gespammt

## Verwalten von Formularantworten

Alle Einreichungen können unter **Einstellungen > Seiten > Formulare > [Formularname] > Antworten** angesehen werden:

**Antwortlisteansicht**:
- Status: Entwurf, eingereicht, abgeschlossen
- Einreicher: E-Mail (wenn angemeldet) oder "Anonym"
- IP-Adresse und Standort (wenn GeoIP aktiviert ist)
- Datum/Zeit der Einreichung
- Zeit bis zur Beendigung (Sekunden)

**Antwortdetail**:
- Alle Feldwerte mit Bezeichnungen
- Metadaten: Browser, Verweis, Sprache
- Fortschrittsverfolgung (mehrschrittig): aktueller Schritt, abgeschlossene Schritte
- Aktionsergebnisse (wenn das Formular Aktionen auslöst)

**Antwortfilterung**:
- Filtern Sie nach Formular, Status, Datumsbereich
- Suchen Sie nach Einreichere-Mail oder IP-Adresse
- Sortieren Sie nach Einreichungsdatum, Bearbeitungszeit

**Antwortexport**:
- Klicken Sie auf die Schaltfläche **Als CSV exportieren**
- Herunterladen von `{form-slug}_responses_{date}.csv`
- Kopfzeile: Submitted At, User, IP, Status, [Feldbezeichnungen]
- Eine Antwort pro Zeile
- Öffnen Sie in Excel, Google Sheets oder Datenanalysetools

## Verwenden von Formularen in Seiten

**Einbetten von Formularen**:
1. Öffnen Sie die Seite im Page Builder
2. Fügen Sie das **Formular**-Element aus dem Elemente-Panel hinzu
3. Wählen Sie ein Formular aus dem Dropdownmenü aus
4. Personalisieren Sie den Formular-Container-Stil (Hintergrund, Abstand, Rand)
5. Speichern und veröffentlichen Sie die Seite

**Das Formular wird mit**:
- Formulartitel und Beschreibung (aus den Formulareinstellungen)
- Alle Felder in Reihenfolge (einseitig) oder aktuellen Schritt (mehrschrittig)
- Absenden-Button mit benutzerdefiniertem Text
- Erfolgs-/Fehlermeldungen nach der Einreichung

**Stilübernahme**:
- Formulare erben die Seitenstilvorlagen
- Schaltflächen verwenden die Themen-Schaltflächenstile
- Eingabefelder verwenden die Themen-Eingabestile
- Ein benutzerdefinierter CSS-Klassenname kann für Felder hinzugefügt werden, um spezifische Stile anzuwenden

## Form Builder Oberfläche

**Linken Seitenleiste - Feldbibliothek**:
- Kategorisiert nach Kategorie (Text, Auswahl, Bewertung, Erweitert)
- Feld auf das Canvas ziehen oder klicken, um es hinzuzufügen
- Suchen Sie, um Feldtypen schnell zu finden

**Hauptcanvas - Feld-Editor**:
- Ziehen Sie den Handle (≡) zum Umordnen der Felder
- Klicken Sie auf ein Feld, um es auszuwählen und zu bearbeiten
- Löschen-Button (×) für jedes Feld
- Visuelle Vorschau des konfigurierten Felds
- Leere Zustand mit Drop-Zone-Anweisungen

**Rechte Seitenleiste - Eigenschaften-Panel**:
- **Formulareinstellungen-Registerkarte** - Grundlegende Informationen, Nachrichten, Spam-Schutz
- **Feld-Einstellungen-Registerkarte** - Konfigurieren Sie das ausgewählte Feld (Bezeichnung, Validierung usw.)
- **Schritte-Registerkarte** - Verwalten Sie Schritte (nur bei mehrschrittigen Formularen)
- **Bedingte Regeln-Registerkarte** - Fügen Sie Show/Hide-Logik basierend auf Antworten hinzu

**Werkzeugleiste-Funktionen**:
- **Undo/Redo** - Vollständige Bearbeitungsgeschichte
- **Vorschau** - Testen Sie die Funktionalität des Formulars
- **Speichern** - Automatisch alle 3 Sekunden während der Bearbeitung
- **Übersetzungen** - Übersetzen Sie Formulartexte in andere Sprachen

## Häufige Formularbeispiele

**Kontaktformular**:
- Felder: Vollständiger Name (erforderlich), E-Mail (erforderlich), Telefon, Nachricht (erforderlich)
- Absenden-Button: "Nachricht senden"
- Erfolg: "Vielen Dank, dass Sie sich bei uns gemeldet haben! Wir antworten innerhalb von 24 Stunden." 

**Produktfeedbackumfrage**:
- Schritt 1: Sternebewertung, Likert-Skala Zustimmung
- Schritt 2: NPS-Score, Verbesserungsvorschläge
- Bedingung: Wenn Bewertung < 3, erforderliche Verbesserungsvorschläge

**Stellenbewerbung**:
- Schritt 1: Persönliche Informationen (Name, E-Mail, Telefon)
- Schritt 2: Erfahrung (Lebenslauf-Upload, Jahre Erfahrung, Referenzen)
- Schritt 3: Verfügbarkeit (Startdatum, Gehaltserwartungen)
- Teilweise Speicherung aktiviert (Bewerber können später fortfahren)

**Newsletter-Abonnement mit Präferenzen**:
- E-Mail (erforderlich)
- Häkchengruppe: Interessen (Produkte, Verkaufsangebote, Blog-Updates)
- reCAPTCHA aktiviert (verhindert gefälschte Abonnements)

## Tipps

- **Beginnen Sie mit einseitigen Formularen** - Fügen Sie mehrschrittige Formulare nur hinzu, wenn das Formular mehr als 10 Felder hat
- **Verwenden Sie Honeypot zuerst** - Upgraden Sie nur zu reCAPTCHA, wenn Spam weiterhin besteht
- **Testen Sie vor der Veröffentlichung** - Verwenden Sie den Vorschau-Modus, um Validierung und Fluss zu überprüfen
- **Exportieren Sie regelmäßig** - Laden Sie die CSV-Datei der Antwort wöchentlich herunter, um eine Sicherung zu erstellen
- **Überwachen Sie die Bearbeitungszeit** - Wenn der Durchschnitt >5 Minuten beträgt, ist das Formular möglicherweise zu lang
- **Verwenden Sie bedingte Logik** - Verbergen Sie irrelevante Felder, um die Wahrnehmung der Formularlänge zu reduzieren
- **Aktivieren Sie teilweise Speicherung für lange Formulare** - Reduziert das Abbrechen bei mehrschrittigen Anträgen
- **Übersetzen Sie Formularbezeichnungen** - Verwenden Sie das integrierte Übersetzungssystem für mehrsprachige Websites
- **Erfordern Sie Anmeldung für sensible Daten** - Verhindert anonyme Spam, verknüpft Einreichungen mit Benutzerkonten
- **Halten Sie Erfolgsnachrichten spezifisch** - "Wir antworten innerhalb von 24 Stunden" ist besser als "Vielen Dank"