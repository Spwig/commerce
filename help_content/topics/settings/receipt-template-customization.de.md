---
title: Belegvorlagen anpassen
---

Belegvorlagen steuern das Erscheinungsbild und den Inhalt der gedruckten Wärmebelege an Ihren POS-Terminals. Passen Sie Kopf- und Fußzeile an, fügen Sie Ihr Logo hinzu, konfigurieren Sie Compliance-Felder (Steuer-IDs, Geschäftsregistrierungsnummern) und fügen Sie Werbe-QR-Codes hinzu. Vorlagen unterstützen das Zielen auf einen Umfang – erstellen Sie eine Standardvorlage für alle Geschäfte, gruppenbezogene Vorlagen für Regionen oder geschäftsbezogene Vorlagen für einzelne Standorte. Das System verwendet Regeln zur Umfangs-Vorrangigkeit, um zu bestimmen, welche Vorlage beim Drucken eines Belegs angewendet wird.

Verwenden Sie Belegvorlagen, um Markenkonstanz zu gewährleisten, regionale Compliance-Anforderungen zu erfüllen und durch werbliche Elemente die Kundenbindung zu erhöhen.

![Belegvorlagenliste](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Grundlagen der Belegvorlagen

Belegvorlagen definieren die Struktur und den Inhalt der gedruckten Belege von ESC/POS-Wärmebelegdruckern. Jede Vorlage legt fest:

**Physikalische Konfiguration**:
- Papierbreite (58 mm oder 80 mm)
- Logo-Bild (Schwarz-Weiß für Wärmebelege)
- Schriftgröße und Zeilenabstand

**Inhaltabschnitte**:
- Kopftext (Geschäftsname, Adresse, Kontaktinformationen)
- Dynamische Transaktionsdaten (Artikel, Preise, Gesamtbeträge, Zahlungsmethoden)
- Fußzeile (Rückgaberecht, Dankesnachricht, soziale Medien)
- Compliance-Felder (Steuer-IDs, Geschäftsregistrierungsnummern)
- Werbe-QR-Code mit Beschriftung

**Zielung auf einen Umfang**:
- Standardvorlage (gilt für alle Geschäfte, es sei denn, sie wird überschrieben)
- Gruppenvorlage (gilt für alle Geschäfte in einer Gruppe)
- Geschäftsvorlage (gilt für ein bestimmtes Geschäft/Lager)

## Regeln zur Umfangs-Vorrangigkeit

Wenn ein Terminal einen Beleg druckt, wählt das System eine Vorlage mithilfe dieser Hierarchie (höchste Priorität zu niedrigster):

| Priorität | Umfang | Beispiel | Anwendungsfall |
|-----------|--------|---------|----------------|
| **1** | Geschäftsspezifisch | Vorlage für Paris-Geschäft | Eindeutige Steuerkonformitätsanforderungen in Frankreich |
| **2** | Gruppenspezifisch | Vorlage für europäische Geschäfte | Mehrwertsteueranzeige für alle EU-Standorte |
| **3** | Standard | Globale Vorlage | Standard für alle nicht konfigurierten Geschäfte |

**Funktionsweise**:
1. Prüfen, ob das Geschäft eine eigene Vorlage (spezifisch für das Lager) hat
2. Wenn nicht, prüfen, ob die Gruppe des Geschäfts eine Gruppenvorlage hat
3. Wenn nicht, verwenden Sie die Standardvorlage

**Beispiel**:
- Standardvorlage: "Standardbeleg" (keine Umfangsbelegung)
- Gruppenvorlage: "EU-Beleg" (zugeordnet zur Gruppe europäische Geschäfte) – enthält Mehrwertsteuerregistrierung
- Geschäftsvorlage: "Paris-Beleg" (zugeordnet zum Lager Paris) – enthält französischen SIRET-Nummer

**Ergebnis**:
- Terminal für Paris-Geschäft: Verwendet "Paris-Beleg" (spezifisch für das Geschäft)
- Terminal für Berlin-Geschäft (in der Gruppe europäische Geschäfte, keine Geschäftsvorlage): Verwendet "EU-Beleg" (Gruppenstufe)
- Terminal für New York-Geschäft (keine Gruppe, keine Geschäftsvorlage): Verwendet "Standardbeleg" (Standardzurückfall)

## Papierbreitenkonfiguration

Wärmebelegdrucker verwenden entweder 58 mm oder 80 mm Papierbreite. Wählen Sie basierend auf Ihrer Druckhardware:

| Papierbreite | Zeichen pro Zeile | Bestens geeignet für | Typische Verwendung |
|--------------|------------------|----------------------|---------------------|
| **58 mm** | ~32 Zeichen | Kleiner Platzbedarf, tragbar | Food Trucks, mobile POS, Kioske |
| **80 mm** | ~48 Zeichen | Standard Einzelhandel | Die meisten Einzelhandelsgeschäfte, Restaurants |

**Keine Mischung von Breiten**: Alle Terminals, die dieselbe Vorlage verwenden, müssen denselben Papierbreiten-Drucker haben. Wenn Sie verschiedene Druckertypen haben, erstellen Sie separate Vorlagen für jede Breite.

**Logo-Größenbeschränkungen**:
- **58 mm**: Maximalbreite 384 Pixel (empfohlen: 350 px)
- **80 mm**: Maximalbreite 576 Pixel (empfohlen: 550 px)

Logos, die die maximale Breite überschreiten, werden automatisch verkleinert, was die Qualität reduzieren kann.

## Logo-Konfiguration

Beleglogos müssen **schwarz-weiß** (nur Schwarz und Weiß) sein, um mit Wärmebelegdruckern kompatibel zu sein:

**Logo-Anforderungen**:
- Dateiformat: PNG, JPG oder WebP
- Farbmodus: Schwarz-Weiß (Schwarz auf weißem Hintergrund)
- Empfohlene Abmessungen:
  - 58 mm Papier: 350 px Breite × 100-150 px Höhe
  - 80 mm Papier: 550 px Breite × 150-200 px Höhe
- Dateigröße: <100 KB (Wärmebelegdrucker haben begrenzten Speicher)

**Erstellen von Schwarz-Weiß-Logos**:
1. Starten Sie mit Ihrem regulären Logo (Farbe oder Graustufen)
2. Verwenden Sie ein Bildbearbeitungsprogramm, um es in reines Schwarz und Weiß umzuwandeln (keine Graustufen)
3. Erhöhen Sie den Kontrast, um sicherzustellen, dass die schwarzen Elemente fest sind
4. Exportieren Sie als PNG mit transparentem oder weißem Hintergrund

**Logo-Positionierung**:
- Immer horizontal zentriert
- Wird oben auf dem Beleg gedruckt (über dem Kopftext)
- Gefolgt von automatischer Zeilenabstand (verhindert Überfüllung mit Inhalt)

**Logo-Auswahl**:
- Klicken Sie auf **Medienbibliothek durchsuchen** im Vorlagenformular
- Wählen Sie ein schwarz-weißes Logo-Asset aus
- Der Vorschau wird angezeigt, wie das Logo auf dem Beleg erscheint

**Kein Logo**: Lassen Sie das Logo-Feld leer, wenn Sie eine Textmarke (Kopftext kann den Geschäftsname enthalten) bevorzugen.

## Kopftext

Der Kopftext erscheint unmittelbar nach dem Logo (oder oben, wenn kein Logo vorhanden ist). Typischer Inhalt:

**Geschäftsname und Adresse**:
```
Ihr Geschäftsname
123 Main Street
City, State 12345
Telefon: (555) 123-4567
```

**Geschäftszeiten**:
```
Montag-Freitag: 9 Uhr bis 21 Uhr
Samstag-Sonntag: 10 Uhr bis 18 Uhr
```

**Slogan oder Leitmotiv**:
```
Qualitativ hochwertige Produkte, exzellenter Service
```

**Formatierung**:
- Verwenden Sie Zeilenumbrüche, um Informationen zu trennen
- Automatisch zentriert
- Halten Sie Zeilen unter dem Zeichenlimit für die Papierbreite (32 Zeichen für 58 mm, 48 für 80 mm)

**Verfügbare Variablen** (optional):
- `{store_name}` – Wird durch den Lagername ersetzt
- `{order_date}` – Wird durch das Transaktionsdatum ersetzt
- `{order_number}` – Wird durch die Bestellnummer ersetzt

Die meisten Händler verwenden statischen Text anstelle von Variablen für die Konsistenz des Kopftextes.

## Fußzeile

Der Fußzeile erscheint nach den Transaktionsdetails (Artikel, Gesamtbeträge, Zahlung). Typischer Inhalt:

**Rückgaberecht**:
```
Rückgaben innerhalb von 30 Tagen mit Beleg
Nur Gutschrift oder Austausch
```

**Dankesnachricht**:
```
Vielen Dank, dass Sie bei uns einkaufen!
Folgen Sie uns @yourstore
```

**Kundenservice**:
```
Fragen? Rufen Sie an (555) 123-4567
oder senden Sie eine E-Mail an support@yourstore.com
```

**Formatierungstipps**:
- Halten Sie die wichtigsten Informationen zuerst (Rückgaberecht, Kontakt)
- Verwenden Sie Zeilenumbrüche für Lesbarkeit
- Überlegen Sie, eine Trennlinie (`---`) zwischen Abschnitten hinzuzufügen

## Compliance-Felder

Viele Jurisdiktionen verlangen spezifische Informationen auf Belegen:

**Steuer-ID-Bezeichnung** – Anpassbare Bezeichnung für die Steueridentifikationsnummer:
- USA: "Steuer-ID" oder "EIN"
- EU: "Mehrwertsteuer-Nummer" oder "Mehrwertsteuer-Registrierungsnummer"
- Kanada: "GST/HST-Nummer"
- Australien: "ABN"

**Steuer-ID-Wert** – Die tatsächliche Identifikationsnummer:
- Wird einmal in der Vorlage eingegeben und erscheint auf allen Belegen
- Beispiel: "Mehrwertsteuer-Nummer: GB123456789"

**Geschäftsregistrierungsbezeichnung** – Anpassbare Bezeichnung für die Geschäftsregistrierung:
- Frankreich: "SIRET"
- Deutschland: "Handelsregister"
- Vereinigtes Königreich: "Company Registration Number"

**Geschäftsregistrierungs-Wert** – Die tatsächliche Registrierungsnummer:
- Beispiel: "SIRET: 123 456 789 00010"

**Powered by Spwig anzeigen** – Schalter zum Anzeigen oder Verbergen der Marke "Powered by Spwig":
- Standardmäßig aktiviert (unterstützt Plattformentwicklung)
- Deaktivieren Sie es für White-Label-Betriebe

**Compliance-Beispiele nach Region**:

**Europäische Union**:
- Steuer-ID-Bezeichnung: "Mehrwertsteuer-Nummer"
- Steuer-ID-Wert: "GB123456789"
- Zeigen Sie die Geschäftsregistrierungsnummer an, wenn sie in Ihrem Land erforderlich ist

**Vereinigte Staaten**:
- Allgemein keine Steuer-ID-Anforderung auf Belegen (variiert nach Bundesstaat)
- Kann EIN für B2B-Transaktionen enthalten

**Frankreich (spezifisch)**:
- Pflicht SIRET auf allen Belegen
- Geschäftsregistrierungsbezeichnung: "SIRET"
- Geschäftsregistrierungs-Wert: "123 456 789 00010"

**Australien**:
- Empfohlene ABN (australische Geschäftsnummer) für GST-registrierte Unternehmen
- Steuer-ID-Bezeichnung: "ABN"

Prüfen Sie die Beleganforderungen Ihrer lokalen Jurisdiktion, bevor Sie live gehen.

## QR-Code-Werbung

Fügen Sie einen QR-Code am unteren Ende der Belege hinzu, um die Kundenbindung zu fördern:

**QR-Code-URL** – Zielort beim Scannen:
- Bewertung anfordern: `https://yourstore.com/reviews/leave-review`
- Treueprogramm: `https://yourstore.com/loyalty/join`
- Rabatt für nächsten Kauf: `https://yourstore.com/discount/THANKYOU`
- Soziale Medien: `https://instagram.com/yourstore`
- Startseite des Webs: `https://yourstore.com`

**QR-Code-Bezeichnung** – Text, der über dem QR-Code angezeigt wird:
- "Scan, um eine Bewertung abzugeben und 10 % Rabatt auf Ihren nächsten Kauf zu erhalten"
- "Treten Sie unserem Treueprogramm bei – Scannen Sie hier"
- "Folgen Sie uns auf Instagram – Scannen Sie, um sich zu verbinden"
- "Bewerten Sie Ihre Erfahrung"

**QR-Code-Best Practices**:
- Verwenden Sie kurze URLs (lange URLs erzeugen dichte, schwer lesbare Codes)
- Testen Sie den QR-Code mit mehreren Handynummern, bevor Sie ihn bereitstellen
- Fügen Sie einen klaren Wert in der Bezeichnung hinzu (was der Kunde für das Scannen erhält)
- Verfolgen Sie QR-Code-Scans, um die Effektivität zu messen (verwenden Sie eine URL mit Tracking-Parameter)

**Dynamische QR-Codes** (Erweitert):
- Verwenden Sie einen QR-Weiterleitungs-Dienst (bit.ly, tinyurl), um eine kurze URL zu erstellen
- Leiten Sie die Weiterleitung zu unterschiedlichen Zielen je nach Saison, ohne die Belege erneut zu drucken
- Beispiel: `https://bit.ly/yourstoreqr` → leitet zu aktuellen Promotion

## Vorlagen für unterschiedliche Umfänge erstellen

**Standardvorlage** (empfohlener Ausgangspunkt):
1. Navigieren Sie zu **POS > Belegvorlagen**
2. Klicken Sie auf **+ Belegvorlage hinzufügen**
3. Lassen Sie die Felder **Lager** und **Geschäftsgruppe** leer (dies macht es zur Standardvorlage)
4. Konfigurieren Sie die Papierbreite, die mit Ihrem häufigsten Druckertyp übereinstimmt
5. Fügen Sie Logo, Kopf- und Fußzeile hinzu
6. Konfigurieren Sie Compliance-Felder für Ihr primäres Marktgebiet
7. Speichern Sie

Diese Vorlage gilt für alle Geschäfte, es sei denn, sie wird überschrieben.

**Gruppenvorlage** (für regionale Unterschiede):
1. Erstellen Sie eine neue Vorlage
2. Wählen Sie **Geschäftsgruppe** aus (z. B. "europäische Geschäfte")
3. Lassen Sie **Lager** leer
4. Anpassen Sie Compliance-Felder für die Region (z. B. Mehrwertsteuerformatierung)
5. Anpassen Sie den Kopftext (z. B. regionale Adresse)
6. Speichern Sie

Diese Vorlage gilt für alle Geschäfte in der Gruppe.

**Geschäftsvorlage** (für Standort-spezifische Bedürfnisse):
1. Erstellen Sie eine neue Vorlage
2. Wählen Sie **Lager** aus (z. B. "Paris-Geschäft")
3. Anpassen Sie alle Felder für diesen spezifischen Standort
4. Speichern Sie

Diese Vorlage gilt nur für dieses eine Geschäft.

**Testen von Vorlagen**:
- Verarbeiten Sie eine Testtransaktion am Terminal
- Drucken Sie den Beleg
- Überprüfen Sie die Klarheit des Logos, die Textausrichtung, die Compliance-Felder und die Scannbarkeit des QR-Codes
- Passen Sie die Vorlage an und testen Sie erneut, wenn nötig

## Typische Beleglayouts

**Minimaler Beleg** (Food Trucks, Pop-ups):
- Kein Logo (Speicherersparnis)
- Kopfzeile: Nur Geschäftsname und Telefonnummer
- Fußzeile: Dankesnachricht
- Kein QR-Code

**Standard-Einzelhandelsbeleg**:
- Logo (schwarz-weißes Markenlogo)
- Kopfzeile: Vollständiger Geschäftsname, Adresse, Öffnungszeiten
- Compliance: Steuer-ID
- Fußzeile: Rückgaberecht, Dankesnachricht
- QR-Code: Bewertung anfordern

**Premium-Einzelhandelsbeleg**:
- Logo (vollständiges Markenwortlogo)
- Kopfzeile: Leitmotiv, Adresse, Kontakt
- Compliance: Steuer-ID, Geschäftsregistrierung
- Fußzeile: Rückgaberecht, Kundenservice, soziale Medien
- QR-Code: Treueprogramm-Registrierung

**Mehrlager-Kette**:
- Standardvorlage: Unternehmensmarken, Standardrichtlinien
- Gruppenvorlagen: Regionale Compliance (Mehrwertsteuer für EU, GST für Kanada)
- Geschäftsvorlagen: Standort-spezifische Adresse und Telefonnummer

## Verwaltung mehrerer Vorlagen

**Namenskonvention für Vorlagen**:
- Verwenden Sie den Umfang im Namen: "Standardbeleg", "EU-Gruppenbeleg", "Paris-Geschäftsbeleg"
- Hilft dabei, zu erkennen, welche Vorlage wo gilt, wenn Sie die Liste überprüfen

**Vorlagenänderungen**:
- Änderungen gelten sofort für zukünftige Belege
- Bereits gedruckte Belege (bereits gedruckte) sind nicht betroffen
- Testen Sie Änderungen an einem Terminal mit geringem Verkehr, bevor Sie sie allen Geschäften bereitstellen

**Vorlagen duplizieren**:
- Wenn Sie eine neue Vorlage erstellen, die einer vorhandenen ähnelt, duplizieren Sie die vorhandene Vorlage und bearbeiten Sie sie
- Verhindert, dass Sie von Grund auf neu beginnen müssen

**Vorlagen löschen**:
- Sie können die Standardvorlage nicht löschen, solange Terminals existieren (muss eine Rückfallvorlage vorhanden sein)
- Sie können Gruppen- oder Geschäftsvorlagen löschen (Terminals fallen zurück auf die nächste Ebene in der Hierarchie)
- Bestätigen Sie, dass keine Terminals aktiv die Vorlage verwenden, bevor Sie sie löschen

## Tipps

- **Beginnen Sie mit 80 mm, wenn Sie unsicher sind** – Die Standardpapierbreite eignet sich für die meisten Einzelhandelsgeschäfte; 58 mm ist spezialisiert
- **Testen Sie das Logo in einem echten Drucker** – Was auf dem Bildschirm gut aussieht, kann schlecht drucken; testen Sie früh
- **Halten Sie Compliance-Felder aktuell** – Ablaufende Steuerregistrierungen auf Belegen führen zu rechtlichen Problemen
- **QR-Codes mit Wertvorschlag scannen besser** – "Scan for 10% off" übertrifft "Scan here" um das 10-fache
- **Überprüfen Sie Zeichenbegrenzungen** – Textumbrüche ruinieren die Formatierung; zählen Sie die Zeichen pro Zeile, bevor Sie bereitstellen
- **Eine Vorlage pro Papierbreite** – Weisen Sie keine 80 mm-Vorlage einem Terminal mit 58 mm-Drucker zu (Logo passt nicht)
- **Drucken Sie Testbelege monatlich** – Drucker verschlechtern sich im Laufe der Zeit; überprüfen Sie, ob die Qualität akzeptabel bleibt
- **Verwenden Sie Variablen sparsam** – Statischer Text ist zuverlässiger als dynamische Variablen (weniger Fehlerpunkte)
- **Sichern Sie die Vorlagenkonfiguration** – Machen Sie einen Screenshot oder exportieren Sie die Vorlagenkonfiguration, bevor Sie große Änderungen vornehmen (leichter Rückgang)
- **Regionale Compliance variiert** – Forschen Sie nach lokalen Beleganforderungen, bevor Sie bereitstellen; Geldstrafen für Nichtkonformität können schwerwiegend sein

