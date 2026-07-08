---
title: Lagerbenachrichtigungen
---

Lagerbenachrichtigungen ermöglichen es Kunden, sich für eine E-Mail-Benachrichtigung anzumelden, sobald ein ausverkaufter Artikel wieder verfügbar ist. Die Einstellungen zur Lageranzeige steuern, was Kunden auf Produktseiten sehen – wie z. B. Lagerstatus-Labels, Warnungen bei geringem Lagerbestand und was geschieht, wenn ein Artikel ausverkauft ist.

## Einstellungen zur Lageranzeige

Die Einstellungen zur Lageranzeige sind Standardwerte für das gesamte Geschäft und gelten für alle Artikel, es sei denn, sie werden auf Kategorie- oder ArtikelEbene überschrieben.

Navigieren Sie zu **Katalog > Einstellungen zur Lageranzeige**, um diese Optionen zu konfigurieren. Es gibt eine Einstellungsdatei für Ihr Geschäft – klicken Sie darauf, um sie zu bearbeiten.

### Lagerstatusanzeige

| Einstellung | Beschreibung |
|---------|-------------|
| **Lagerstatus anzeigen** | Zeigt die Bezeichnungen "Auf Lager" oder "Ausverkauft" auf Produktseiten an |
| **Warnung bei geringem Lagerbestand anzeigen** | Zeigt eine Nachricht wie "Nur X übrig" an, wenn der Lagerbestand niedrig ist |
| **Schwellenwert für geringen Lagerbestand** | Die Menge, ab der die Warnung bei geringem Lagerbestand angezeigt wird (Standard: 5) |
| **Genauen Lagerbestand anzeigen** | Zeigt die genaue verbleibende Menge an (z. B. "Nur 3 übrig!") anstelle einer allgemeinen Warnung |

### Verhalten bei ausverkauften Artikeln

Die Einstellung **Aktion bei Ausverkauf** bestimmt, was Kunden sehen, wenn ein Artikel nicht mehr auf Lager ist:

| Aktion | Was Kunden sehen |
|--------|-------------------|
| **Aus der Liste entfernen** | Der Artikel wird von Kategorieseiten und Suchergebnissen entfernt |
| **Als nicht verfügbar anzeigen** | Der Artikel ist sichtbar, kann aber nicht in den Warenkorb gelegt werden |
| **Schaltfläche "Benachrichtigen Sie mich" anzeigen** | Kunden können ihre E-Mail-Adresse eingeben, um benachrichtigt zu werden, wenn der Artikel wieder verfügbar ist |
| **Zurückbestellungen erlauben** | Kunden können den Artikel auch dann kaufen, wenn der Lagerbestand null ist |

Legen Sie **Nachricht bei Ausverkauf** fest, um den Text anzupassen, der angezeigt wird, wenn ein Artikel nicht verfügbar ist (Standard: `Ausverkauft`).

Legen Sie **Zurückbestellungs-Nachricht** fest, um den Text anzupassen, der für zurückbestellbare Artikel angezeigt wird (Standard: `Auf Rückbestellung verfügbar`).

### Versand- und Lieferzeitanzeige

| Einstellung | Beschreibung |
|---------|-------------|
| **"Versand aus"-Standort anzeigen** | Zeigt den Lagername auf der Produktseite an |
| **Schätzung Lieferzeit anzeigen** | Zeigt geschätzte Lieferdaten an, die aus der Lagerstandort berechnet werden |

### Zurückbestellungen erlauben (Gesamtwebsite)

Aktivieren Sie **Zurückbestellungen erlauben**, um Kunden standardmäßig zu ermöglichen, ausverkaufte Artikel zu kaufen. Einzelne Artikel und Kategorien können diese Einstellung überschreiben.

## Benachrichtigungen bei Rückverfügbarkeit

Wenn Sie die Aktion bei Ausverkauf auf **Schaltfläche "Benachrichtigen Sie mich"** setzen, können Kunden auf der Produktseite ihre E-Mail-Adresse eingeben, um eine E-Mail zu erhalten, sobald der Artikel wieder verfügbar ist.

### Anzeigen von Benachrichtigungsanfragen

Navigieren Sie zu **Katalog > Lagerbenachrichtigungen**, um alle Kundenbenachrichtigungsanfragen anzuzeigen. Jeder Eintrag zeigt:
- Kunden-E-Mail-Adresse
- Produkt und Variante (falls zutreffend)
- Präferierte Lagerstätte (falls der Kunde eine regionale Präferenz ausgewählt hat)
- Wann die Anfrage erstellt wurde
- Wann die Benachrichtigung gesendet wurde (leer, wenn noch nicht gesendet)

### Wann Benachrichtigungen gesendet werden

Spwig sendet automatisch E-Mails bei Rückverfügbarkeit, wenn der Lagerbestand eines Artikels über null ansteigt. Das Feld **Benachrichtigt um** protokolliert, wann die E-Mail gesendet wurde.

Kunden erhalten eine Benachrichtigung per E-Mail. Nach der Benachrichtigung müssen sie sich erneut anmelden, wenn der Artikel erneut ausverkauft ist.

### Filtern von Benachrichtigungsanfragen

Verwenden Sie die Admin-Filter, um Folgendes zu finden:
- Anfragen für ein bestimmtes Produkt
- Anfragen, die bereits benachrichtigt wurden (um zu sehen, wer kontaktiert wurde)
- Anfragen, die noch ausstehen (Kunden, die auf eine Rückverfügbarkeit warten)

## Überschreibungen auf ArtikelEbene

Die gesamtwebsite-weiten Lageranzeige-Einstellungen können pro Artikel oder Kategorie überschrieben werden. Auf dem Artikelbearbeitungsformular suchen Sie nach dem Abschnitt **Lager**, in dem Sie eine artikelbezogene Einstellung **Aktion bei Ausverkauf** festlegen können, die sich von der globalen Standard-Einstellung unterscheidet.

Dies ist nützlich, wenn Sie die meisten Artikel standardmäßig für Rückbestellungen freigeben möchten, aber einige Artikel auf "Benachrichtigen Sie mich" setzen – oder wenn ein bestimmter Artikel ausverkauft sein sollte, verborgen werden sollte.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Legen Sie den **Niedrigen Lagerbestandsschwellenwert** auf den Neubestellpunkt fest, den Sie typischerweise verwenden, damit Kunden vor dem Ausverkauf gewarnt werden.
- Nutzen Sie stattdessen die Option **„Benachrichtige mich“-Schaltfläche anzeigen**, um ausverkaufte Produkte nicht zu verbergen – Kunden, die sich anmelden, stellen eine reale Nachfrage dar, die eine Neubestellung rechtfertigen kann.
- Aktivieren Sie **Genauere Menge anzeigen** nur selten.

Für die meisten Geschäfte ist es besser, „Nur 3 übrig!“ anzuzeigen, als die genaue Zahl, da dies Dringlichkeit erzeugt, ohne das vollständige Lagerbild preiszugeben.
- Prüfen Sie die Liste der Lagerbestandsbenachrichtigungen, bevor Sie eine neue Bestellung aufgeben – die Anzahl der wartenden Benachrichtigungsanfragen zeigt Ihnen an, wie groß die Nachfrage nach diesem Produkt ist.
- Wenn Sie Rückbestellungen verwenden, aktualisieren Sie Ihre **Rückbestellungsmitteilung**, um realistische Erwartungen zu setzen (z. B. „Lieferzeit: 2–3 Wochen – bestellen Sie jetzt, um Ihren Platz zu sichern“).
- Kombinieren Sie Benachrichtigungen über ausverkaufte Produkte mit E-Mail-Marketing: Wenn Sie ein beliebtes Produkt wieder auf Lager haben, senden Sie eine Kampagne an alle, die sich angemeldet haben, nicht nur an die automatische Benachrichtigungse-Mail.