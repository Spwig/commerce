---
title: Lagerbenachrichtigungen
---

Mit Lagerbenachrichtigungen können sich Kunden anmelden, um per E-Mail benachrichtigt zu werden, wenn ein nicht verfügbares Produkt wieder vorrätig ist. Die Einstellungen für die Lageranzeige steuern, was Kunden auf den Produktseiten sehen – wie z. B. Lagerstatus-Labels, Warnungen bei geringem Bestand und was passiert, wenn ein Produkt ausverkauft ist.

## Einstellungen für die Lageranzeige

Die Einstellungen für die Lageranzeige sind store-weite Standardwerte, die für alle Produkte gelten, es sei denn, sie werden auf Kategorie- oder Produktebene überschrieben.

Navigieren Sie zu **Katalog > Einstellungen für die Lageranzeige**, um diese Optionen zu konfigurieren. Es gibt einen Einstellungsdatensatz für Ihren Store – klicken Sie darauf, um ihn zu bearbeiten.

### Anzeige des Lagerstatus

| Einstellung | Beschreibung |
|---------|-------------|
| **Lagerstatus anzeigen** | Zeigt die Labels "Auf Lager" oder "Nicht auf Lager" auf den Produktseiten an |
| **Warnung bei geringem Bestand anzeigen** | Zeigt die Meldung "Nur noch X übrig" an, wenn der Bestand niedrig ist |
| **Schwellenwert für geringen Bestand** | Die Menge, bei oder unter der die Warnung bei geringem Bestand angezeigt wird (Standard: 5) |
| **Exakte Menge anzeigen** | Zeigt die genaue verbleibende Anzahl an (z. B. "Nur noch 3 übrig!") anstelle einer allgemeinen Warnung |

### Verhalten bei Nichtverfügbarkeit

Die Einstellung **Aktion bei Nichtverfügbarkeit** bestimmt, was Kunden sehen, wenn ein Produkt keinen Bestand hat:

| Aktion | Was Kunden sehen |
|--------|-------------------|
| **Aus Listen ausblenden** | Das Produkt wird von den Kategorie-Seiten und Suchergebnissen entfernt |
| **Als nicht verfügbar anzeigen** | Das Produkt ist sichtbar, kann aber nicht in den Warenkorb gelegt werden |
| **"Benachrichtigen"-Button anzeigen** | Kunden können ihre E-Mail-Adresse registrieren, um benachrichtigt zu werden, wenn der Bestand wieder verfügbar ist |
| **Nachbestellungen erlauben** | Kunden können das Produkt kaufen, auch wenn der Bestand null ist |

Setzen Sie **Nachricht bei Nichtverfügbarkeit**, um den Text anzupassen, der angezeigt wird, wenn ein Produkt nicht verfügbar ist (Standard: `Out of Stock`).

Setzen Sie **Nachricht bei Nachbestellung**, um den Text anzupassen, der für nachbestellbare Produkte angezeigt wird (Standard: `Available on backorder`).

### Anzeige von Versand und Lieferung

| Einstellung | Beschreibung |
|---------|-------------|
| **"Versandort" anzeigen** | Zeigt den Lagerhausnamen auf der Produktseite an |
| **Geschätzte Lieferzeit anzeigen** | Zeigt geschätzte Lieferdaten an, die aus dem Standort des Lagerhauses berechnet werden |

### Nachbestellungen erlauben (store-weit)

Aktivieren Sie **Nachbestellungen erlauben**, um Kunden standardmäßig den Kauf jedes nicht verfügbaren Produkts zu ermöglichen. Einzelne Produkte und Kategorien können diese Einstellung überschreiben.

## Benachrichtigungen bei Wiederverfügbarkeit

Wenn Sie die Aktion bei Nichtverfügbarkeit auf **"Benachrichtigen"-Button anzeigen** setzen, können Kunden ihre E-Mail-Adresse auf der Produktseite eingeben, um eine E-Mail zu erhalten, wenn das Produkt wieder auf Lager ist.

### Anzeigen von Benachrichtigungsanfragen

Navigieren Sie zu **Katalog > Lagerbenachrichtigungen**, um alle Kundenbenachrichtigungsanfragen zu sehen. Jeder Datensatz zeigt:
- Kunden-E-Mail-Adresse
- Produkt und Variante (falls zutreffend)
- Bevorzugtes Lagerhaus (falls der Kunde eine regionale Präferenz ausgewählt hat)
- Wann die Anfrage erstellt wurde
- Wann die Benachrichtigung gesendet wurde (leer, wenn noch nicht gesendet)

### Wann Benachrichtigungen gesendet werden

Spwig sendet E-Mails zur Wiederverfügbarkeit automatisch, wenn der Lagerbestand eines Produkts über null steigt. Das Feld **Benachrichtigt am** protokolliert, wann die E-Mail gesendet wurde.

Kunden erhalten eine Benachrichtigungs-E-Mail. Sobald sie benachrichtigt wurden, müssen sie sich erneut anmelden, wenn das Produkt ein zweites Mal ausverkauft ist.

Wenn Sie lieber mehr als eine einzelne einfache Warnung senden möchten – zum Beispiel das wieder verfügbare Produkt mit einem **Featured Product**-Inhaltsblock anzeigen oder einen Tag später nachfassen – erstellen Sie eine **Produkt wieder auf Lager**-Reise in **Campaign Studio > Journeys** und setzen Sie sie auf **Aktiv**. Sobald diese Reise existiert, werden wartende Kunden darin registriert, anstatt die einfache Einmal-E-Mail zu erhalten; ohne aktive Reise wird diese Einmal-E-Mail genau wie oben beschrieben weiterhin gesendet. Siehe [Triggered Journeys](/help/triggered-journeys) für das Verhalten des Triggers.

### Filtern von Benachrichtigungsanfragen

Verwenden Sie die Admin-Filter, um Folgendes zu finden:
- Anfragen für ein bestimmtes Produkt
- Anfragen, die bereits benachrichtigt wurden (um zu sehen, wer kontaktiert wurde)
- Anfragen, die noch ausstehen (Kunden, die auf eine Wiederauffüllung warten)

## Produktbezogene Überschreibungen

Die Einstellungen für das Lagerbestandsanzeige auf der gesamten Website können pro Produkt oder Kategorie überschrieben werden. Auf dem Bearbeitungsformular für Produkte finden Sie den **Lagerbestand**-Bereich, in dem Sie eine produktbezogene **Aktion bei Ausverkauf** festlegen können, die sich von der globalen Standardeinstellung unterscheidet.

Dies ist nützlich, wenn Sie möchten, dass die meisten Produkte auf Rückbestellungen setzen, aber einige Produkte auf "Benachrichtigen Sie mich" gesetzt werden sollen – oder wenn ein bestimmtes Produkt bei Ausverkauf versteckt werden soll.

## Tipps

- Setzen Sie den **Schwellenwert für niedrigen Lagerbestand** auf den Wiederbestellpunkt, den Sie normalerweise verwenden, damit Kunden vor dem vollständigen Ausverkauf gewarnt werden.
- Verwenden Sie die Option **"Benachrichtigen Sie mich"-Schaltfläche anzeigen**, anstatt Produkte bei Ausverkauf zu verstecken – Kunden, die sich anmelden, repräsentieren echtes Verlangen, das eine Wiederbestellung rechtfertigen kann.
- Aktivieren Sie **Genaue Menge anzeigen** sparsam. Für die meisten Geschäfte funktioniert "Nur noch 3 da!" besser als die Anzeige der exakten Zahl, da sie Dringlichkeit erzeugt, ohne Ihr gesamtes Lagerbild zu offenbaren.
- Prüfen Sie die Liste der Lagerbenachrichtigungen, bevor Sie eine neue Bestellung aufgeben – die Anzahl der ausstehenden Benachrichtigungsanfragen gibt Ihnen ein Bild davon, wie viel Nachfrage für dieses Produkt besteht.
- Falls Sie Rückbestellungen verwenden, aktualisieren Sie Ihre **Rückbestellmeldung**, um genaue Erwartungen zu setzen (z. B. "Sende in 2-3 Wochen ab – bestellen Sie jetzt, um Ihren Platz zu sichern").
- Kombinieren Sie Lagerbenachrichtigungen mit E-Mail-Marketing: Wenn Sie ein beliebtes Produkt wieder auf Lager haben, senden Sie eine Kampagne an alle, die sich angemeldet haben, und nicht nur die automatische Benachrichtigungsemail.