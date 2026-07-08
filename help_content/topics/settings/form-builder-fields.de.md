---
title: Formularbausteine und Validierung
---

Formularfelder sind die Grundbausteine Ihrer Formulare – jedes Feld sammelt einen Datenpunkt von Benutzern. Der Form Builder bietet 22 Feldtypen, die von einfachen Texteingaben bis hin zu fortgeschrittenen Bewertungsskalen und Produkt-Selektoren reichen. Konfigurieren Sie jedes Feld mit Beschriftungen, Validierungsregeln, Hilfetexten und bedingten Logiken, um dynamische Formulare zu erstellen, die sich basierend auf Benutzerantworten anpassen. Felder können erforderlich oder optional sein, mit Regex-Mustern validiert werden und mit benutzerdefinierten CSS-Klassen gestaltet werden.

Verwenden Sie diese Anleitung, um alle verfügbaren Feldtypen zu verstehen, wann Sie jedes verwenden sollten und wie Sie Validierung und bedingte Logik konfigurieren.

## Grundlagen der Feldkonfiguration

Jedes Feld teilt diese gemeinsamen Einstellungen:

**Identität**:
- **Feldname** - Maschinename für die Datenspeicherung (keine Leerzeichen, verwenden Sie Unterstriche: `email_address`)
- **Feldtyp** - Bestimmt das Eingabe-Verhalten und die Darstellung
- **Schrittzuordnung** - Zu welchem Schritt dieses Feld gehört (nur bei mehrschrittigen Formularen)

**Anzeige**:
- **Beschriftung** - Frage oder Prompt, der Benutzern angezeigt wird (z. B. "Was ist Ihre E-Mail-Adresse?")
- **Platzhalter** - Hinweistext innerhalb der Eingabe (z. B. "you@example.com")
- **Hilfetext** - Zusätzliche Anleitung unter dem Feld (z. B. "Wir teilen Ihre E-Mail niemals")
- **Standardwert** - Vorgegebener Wert (Benutzer können ihn ändern)

**Layout**:
- **Breite** - Voll (100%), Halb (50%) oder Drittel (33%) der Formularbreite
- **CSS-Klasse** - Zusätzliche Stilklasse für benutzerdefiniertes Design
- **Reihenfolge** - Position innerhalb des Schritts (ziehen Sie, um umzuordnen)

**Validierung**:
- **Erforderlich** - Schalter für erforderlich (ein rotes Asterisk erscheint neben der Beschriftung)
- **Min/Max Länge** - Zeichenbegrenzung (Textfelder)
- **Min/Max Wert** - Numerische Grenzen (Zahlenfelder)
- **Validierungsmuster** - Benutzerdefiniertes Regex für komplexe Validierung
- **Fehlermeldung** - Benutzerdefinierter Text, der angezeigt wird, wenn die Validierung fehlschlägt

## Texteingabefelder

**Einzeiliger Text** (`text`):
- Grundlegende Texteingabe für kurze Antworten
- Validierung: Min/Max Länge, Regex-Muster
- Verwendung: Namen, Adressen, Produktcodes, kurze Antworten
- Beispiel: "Vollständiger Name", "Straße", "Firma"

**Mehrzeiliger Text** (`textarea`):
- Erweiterbare Textfläche für längeren Inhalt (3-10 Zeilen)
- Validierung: Min/Max Länge
- Verwendung: Kommentare, Feedback, detaillierte Beschreibungen, Nachrichten
- Beispiel: "Erzählen Sie uns von Ihrer Erfahrung", "Zusätzliche Notizen"

**E-Mail-Adresse** (`email`):
- E-Mail-spezifische Validierung (erfordert @ und Domain)
- Mobiltelefone zeigen die @-Taste hervorragend an
- Verwendung: Kontakt-E-Mail, Newsletter-Anmeldung, Kontoerstellung
- Beispiel: "E-Mail-Adresse", "Arbeits-E-Mail"

**Telefonnummer** (`phone`):
- Formatiert Telefonnummern automatisch
- Mobiltelefone zeigen numerische Layout
- Validierung: konfigurierbares Muster (internationale Formate werden unterstützt)
- Verwendung: Kontakttelefon, Notrufkontakt, Terminbuchung
- Beispiel: "Telefonnummer", "Mobil", "Kontaktnummer"

**Zahl** (`number`):
- Numerische Eingabe mit Steuerung zum Erhöhen/Verringern
- Validierung: Min/Max Wert, Schrittweite
- Gibt Zahl (nicht String) in Antworten zurück
- Verwendung: Mengen, Alters, Jahre Berufserfahrung, Budgetbeträge
- Beispiel: "Wie viele Mitarbeiter haben Sie?", "Ihr Alter", "Jahre in der Branche"

**URL** (`url`):
- URL-Validierung (erfordert http:// oder https://)
- Mobiltelefone zeigen .com-Taste an
- Verwendung: Website, LinkedIn-Profil, Portfolio-Link
- Beispiel: "Firmenwebsite", "Portfolio-URL"

## Auswahlfelder

**Dropdown-Liste** (`select`):
- Einzelne Option aus Dropdown-Liste auswählen
- Konfiguration: Array von {value, label} Optionen
- Unterstützt Standardauswahl
- Verwendung: Kategorien, Bundesländer/Länder, Statusauswahl
- Beispiel: "Wählen Sie Ihr Land", "Abteilung", "Wie haben Sie von uns erfahren?"
- Best Practice: Für 5+ Optionen (weniger Optionen verwenden Sie Radio-Buttons anstelle)

**Radio-Buttons** (`radio`):
- Einzelne Auswahl aus sichtbaren Optionen (alle Optionen werden angezeigt)
- Konfiguration: Array von {value, label} Optionen
- Bessere Benutzererfahrung als Dropdown für 2-4 Optionen
- Verwendung: Ja/Nein-Fragen, Geschlecht, Präferenzen mit wenigen Optionen
- Beispiel: "Würden Sie uns empfehlen?", "Bevorzugte Kontaktmethode"

**Checkbox** (`checkbox`):
- Einzelner Schalter (an/aus)
- Gibt true/false in Antworten zurück
- Verwendung: Zustimmung zu Bedingungen, Vereinbarungen, einzelne Präferenz
- Beispiel: "Ich stimme den Allgemeinen Geschäftsbedingungen zu", "Newsletter abonnieren"

**Checkbox-Gruppe** (`checkbox_group`):
- Mehrfachauswahl aus Optionen (Benutzer können 0, 1 oder viele auswählen)
- Konfiguration: Array von {value, label} Optionen
- Gibt Array der ausgewählten Werte zurück
- Verwendung: Mehrfachauswahl-Präferenzen, Interessen, benötigte Funktionen
- Beispiel: "Welche Themen interessieren Sie?", "Wählen Sie alle anwendbaren"

## Bewertungsfelder

**Sternbewertung** (`rating_stars`):
- Visuelle Sternbewertungsskala (typischerweise 1-5 Sterne)
- Konfiguration:
  - `max_stars`: 3-10 Sterne (Standard: 5)
  - `allow_half`: true/false für Halbsterne
  - `icon`: fa-star (Standard) oder fa-heart
  - `color`: Hex-Farbkodierung (Standard: #FFD700 gold)
- Verwendung: Produktbewertungen, Dienstleistungsqualität, Zufriedenheitsbewertungen
- Beispiel: "Bewerten Sie Ihre Erfahrung", "Wie war unser Service?"

**Likert-Skala** (`rating_likert`):
- Aussageskalen: stark nicht einverstanden → stark einverstanden
- Konfiguration:
  - `scale_type`: 5_point (1-5) oder 7_point (1-7)
  - `labels`: Endpunkte-Text anpassen (links: "Stark nicht einverstanden", rechts: "Stark einverstanden")
- Gibt numerischen Wert (1-5 oder 1-7) zurück
- Verwendung: Umfrageaussagen, Einvernehmenskalen, Sentimentmessung
- Beispiel: "Das Produkt erfüllt meine Bedürfnisse", "Der Kundenservice war hilfreich"

**Net Promoter Score (NPS)** (`rating_nps`):
- 0-10-Skala: "Nicht sehr wahrscheinlich" bis "Sehr wahrscheinlich"
- Konfiguration:
  - `low_label`: Linker Endpunkt-Text (Standard: "Nicht sehr wahrscheinlich")
  - `high_label`: Rechter Endpunkt-Text (Standard: "Sehr wahrscheinlich")
- Gibt 0-10-Wert zurück (0-6 = Abwehrer, 7-8 = Passiv, 9-10 = Förderer)
- Verwendung: NPS-Umfragen, Empfehlungswahrscheinlichkeit, Loyalitätsmessung
- Beispiel: "Wie wahrscheinlich sind Sie, uns einem Freund zu empfehlen?"

## Fortgeschrittene Felder

**Dateiupload** (`file`):
- Einzelner oder mehrere Dateiuploads
- Konfiguration:
  - `max_size_mb`: Dateigrößebegrenzung pro Datei (Standard: 5MB)
  - `allowed_types`: Array von Erweiterungen (z. B. ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: Maximale Anzahl an Dateien (1 für Einzel, 2+ für Mehrere)
- Gibt Dateipfad(e) in Antworten zurück
- Dateien werden in `/media/form_uploads/{form-slug}/` gespeichert
- Verwendung: Lebenslauf-Uploads, Dokumente, Fotoanhänge
- Beispiel: "Laden Sie Ihren Lebenslauf hoch", "Anhänge"

**Produkt-Selektor** (`product_select`):
- Mehrfachauswahl aus Ihrem Produktkatalog
- Konfiguration:
  - `category_filters`: Begrenzung auf bestimmte Kategorien (Array von Kategorie-IDs)
  - `max_selections`: 1 für Einzelprodukt, 2+ für Mehrere
  - `display_mode`: "list" (Standard) oder "grid" (mit Vorschaubildern)
- Gibt Produkt-IDs/SKUs in Antworten zurück
- Verwendung: Produktvorschläge, Wunschlisten, Feedbackumfragen, Bündel
- Beispiel: "Welche Produkte interessieren Sie?", "Wählen Sie Ihre Favoriten"

**Datum** (`date`):
- Datumsauswahl (Kalender-Belegung)
- Gibt ISO-Format (YYYY-MM-DD) zurück
- Validierung: Min/Max Datum
- Verwendung: Geburtsdatum, Veranstaltungsdatum, Terminbuchung, Fristen
- Beispiel: "Geburtsdatum", "Bevorzugtes Termin"

**Zeit** (`time`):
- Zeitauswahl (Stunden und Minuten)
- Gibt ISO-Zeitformat (HH:MM) zurück
- Verwendung: Terminzeiten, Verfügbarkeitsfenster
- Beispiel: "Bevorzugte Zeit", "Verfügbar nach"

**Datum & Zeit** (`datetime`):
- Kombinierte Datums- und Zeitauswahl
- Gibt vollständiges ISO-Datum und Zeit zurück
- Verwendung: Veranstaltungsplanung, Terminbuchung
- Beispiel: "Veranstaltungsbeginn", "Lieferfenster"

## Layoutfelder (keine Eingabe)

**Abschnittsüberschrift** (`heading`):
- Überschriftstext zur Organisation von Formularabschnitten
- Konfiguration: Überschriftslevel (h2, h3, h4)
- Keine Datensammlung
- Verwendung: Längere Formulare in logische Abschnitte unterteilen
- Beispiel: "Persönliche Informationen", "Kontaktdaten", "Präferenzen"

**Beschreibender Absatz** (`paragraph`):
- Reicher Textblock für Anweisungen oder Informationen
- Keine Datensammlung
- Unterstützt grundlegende Formatierung (Fett, Kursiv, Links)
- Verwendung: Schrittweisen Anweisungen, rechtliche Hinweise, Erklärungen
- Beispiel: Datenschutzrichtlinien, Erklärung zur Einwilligung nach GDPR

**Trennlinie** (`divider`):
- Visuelle horizontale Trennlinie
- Keine Datensammlung
- Verwendung: Visuelle Organisation zwischen Abschnitten

**Verstecktes Feld** (`hidden`):
- Unsichtbares Feld mit programmatischem Wert
- Konfiguration: `default_value` (erforderlich)
- Keine Beschriftung oder Hilfetext für Benutzer sichtbar
- Verwendung: UTM-Parameter, Trackingdaten, Sitzungsid, Verweiscodes
- Beispiel: Verstecktes Feld mit Wert aus URL-Parameter

## Feldvalidierungsregeln

**Erforderliche Felder**:
- Schalten Sie das "Erforderlich"-Kästchen in den Feldoptionen um
- Ein rotes Asterisk (*) erscheint neben der Beschriftung
- Das Formular kann nicht abgeschickt werden, wenn erforderliche Felder leer sind
- Benutzerdefinierte Fehlermeldung: "Dieses Feld ist erforderlich" (oder benutzerdefinierte Nachricht)

**Min/Max Länge** (Textfelder):
- Mindestzeichenanzahl festlegen: verhindert zu kurze Antworten
- Maximale Zeichenanzahl festlegen: verhindert übermäßige Eingabe
- Beispiel: Nachrichtenfeld erfordert mindestens 10 Zeichen (verhindert Antworten wie "ok")

**Min/Max Wert** (Zahlenfelder):
- Mindestwert festlegen: verhindert negative Alters, Mengen
- Maximalwert festlegen: begrenzt Eingabe auf vernünftigen Bereich
- Beispiel: Alter erfordert mindestens 18, maximal 120

**Validierungsmuster** (Regex):
- Benutzerdefiniertes reguläres Ausdruck für komplexe Validierung
- Häufige Muster:
  - ZIP-Code: `^×{5}(-×{4})?$` (US-Format)
  - Telefon: `^(×{3}) ×{3}-×{4}$` (US-Format)
  - Produktcode: `^[A-Z]{2}×{4}$` (2 Buchstaben, 4 Ziffern)
- Benutzerdefinierte Fehlermeldung erforderlich bei Verwendung von Mustern

**Datei-Validierung**:
- Maximaler Dateigröße: verhindert große Uploads (Standard 5MB)
- Erlaubte Typen: Whitelist spezifische Erweiterungen (Sicherheit)
- Beispiel: Lebenslauf-Feld erlaubt ["pdf", "doc", "docx"], max 2MB

## Bedingte Logik

Erstellen Sie dynamische Formulare, bei denen Felder basierend auf Benutzerantworten sichtbar oder unsichtbar werden:

**Wie bedingte Regeln funktionieren**:
1. Benutzer antwortet auf "Quellfeld" (Trigger)
2. Das System bewertet die Regel: Operator + Vergleichswert
3. Wenn die Bedingung wahr ist, wird die Aktion ausgeführt (Feld oder Schritt zeigen/verbergen/erzwingen)
4. Mehrere Regeln können sich aufeinander aufbauen (Regel A löst Regel B aus)

**Verfügbare Operatoren**:
- **Gleich** (`equals`): exakter Match (z. B. Land gleich "US")
- **Nicht gleich** (`not_equals`): alles außer Wert
- **Enthält** (`contains`): Text enthält Teilstring (Großschreibung nicht beachtet)
- **Größer als** (`greater_than`): numerische Vergleich (z. B. Alter > 18)
- **Kleiner als** (`less_than`): numerische Vergleich (z. B. Bewertung < 3)
- **Leer** (`is_empty`): Feld hat keinen Wert
- **Nicht leer** (`is_not_empty`): Feld hat einen Wert
- **In Liste** (`in_list`): Wert ist einer von ["Option1", "Option2"]

**Verfügbare Aktionen**:
- **Feld zeigen** - Verstecktes Feld anzeigen
- **Feld verbergen** - Feld verbergen (Wert wird gelöscht, wenn versteckt)
- **Feld erzwingen** - Feld verpflichtend machen
- **Feld nicht erzwingen** - Feld optional machen
- **Wert setzen** - Feld mit einem Wert füllen
- **Schritt zeigen** - Versteckten Schritt zeigen (nur bei mehrschrittigen Formularen)
- **Schritt verbergen** - Schritt verbergen (nur bei mehrschrittigen Formularen)
- **Zu Schritt springen** - Zu einem bestimmten Schritt springen (nur bei mehrschrittigen Formularen)

**Beispielregeln**:
- WENN `contact_method` GLEICH "phone" DANN `phone_number` zeigen
- WENN `rating` KLEINER ALS "3" DANN `improvement_feedback` erzwingen
- WENN `country` IN_LIST ["US", "CA"] DANN `shipping_details` zeigen
- WENN `budget` GRÖßER ALS "10000" DANN `enterprise_features` zeigen

**Erstellen von bedingten Regeln**:
1. Klicken Sie auf Registerkarte "Bedingte Regeln" im rechten Panel
2. Klicken Sie auf "Regel hinzufügen"
3. Wählen Sie Quellfeld (Trigger)
4. Wählen Sie Operator (Vergleichsart)
5. Geben Sie Vergleichswert ein (was verglichen werden soll)
6. Wählen Sie Aktion (was getan werden soll)
7. Wählen Sie Ziel (Feld oder Schritt, der beeinflusst wird)
8. Optional: Setzen Sie Priorität (Regeln mit höherer Priorität werden zuerst bewertet)
9. Speichern Sie die Regel

**Regelpriorität**:
- Höhere Zahlen werden zuerst bewertet (Priorität 100 vor Priorität 10)
- Verwenden Sie Priorität, wenn Regeln sich widersprechen oder aufeinander aufbauen
- Beispiel: Regel A (Priorität 100) zeigt Feld an, Regel B (Priorität 50) erzwingt es (A wird zuerst ausgeführt, dann B)

## Häufige Feldmuster

**Kontaktformular**:
- Vollständiger Name (text, erforderlich)
- E-Mail (email, erforderlich)
- Telefon (phone)
- Thema (select mit Optionen: "Verkauf", "Support", "Partnerschaft")
- Nachricht (textarea, erforderlich, min 10 Zeichen)

**Produktfeedback**:
- Produkt (product_select, Einzelwahl)
- Gesamtbewertung (rating_stars, 5 Sterne)
- Bedingung: WENN Bewertung < 3 DANN erzwingen "Was können wir verbessern?" (textarea)
- Empfehlung (rating_nps)

**Bewerbung**:
- Schritt 1: Persönliche Daten (Name, E-Mail, Telefon)
- Schritt 2: Lebenslauf (Dateiupload, erlaubt ["pdf", "doc"], max 2MB)
- Schritt 3: Verfügbarkeit (Datum für Start, checkbox_group für Arbeitstage)
- Bedingung: WENN "years_experience" > 5 DANN zeigen Feld "leadership_experience"

## Tipps

- **Verwenden Sie passende Feldtypen** - E-Mail-Feld für E-Mails (nicht text), bietet Validierung und bessere Mobiltelefone
- **Halten Sie Beschriftungen kurz** - Verwenden Sie Hilfetext für Details, nicht für Beschriftungen
- **Gruppieren Sie verwandte Felder** - Verwenden Sie Überschriften und Trennlinien für visuelle Organisation
- **Testen Sie Validierung** - Vorschau des Formulars und versuchen Sie, es mit ungültigen Daten abzusenden
- **Begrenzen Sie Dateiupload-Größe** - Max 5MB verhindert Serverüberlastung durch große Dateien
- **Verwenden Sie bedingte Logik sparsam** - Zu viele Regeln verwirren Benutzer; halten Sie Formulare einfach
- **Setzen Sie realistische Max-Werte** - Alter max 120, Menge max 100 (verhindert Tippfehler wie 1000)
- **Bieten Sie Musterbeispiele an** - Wenn Regex-Validierung verwendet wird, zeigen Sie Beispiel in Hilfetext an
- **Machen Sie offensichtliche Felder erforderlich** - Name und E-Mail für Kontaktformulare, immer erforderlich
- **Verwenden Sie Radio für 2-4 Optionen** - Dropdown für 5+ Optionen (verbessert UX)
- **Halbe Breite für kurze Eingaben** - Telefon und ZIP können halbe Breite haben, spart vertikalen Raum
- **Produkt-Selektoren für Wunschlisten** - Erlauben Kunden, mehrere Produkte für Empfehlungen auszuwählen

