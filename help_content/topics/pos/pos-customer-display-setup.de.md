---
title: POS-Kundendisplay-Setup
---

Ein Kundendisplay ist ein zweiter Bildschirm, der Ihrem Kunden während eines Verkaufs gegenüber steht. Während Sie die Transaktion verarbeiten, sieht der Kunde jedes erfasste Artikel, den laufenden Gesamtbetrag, die Preis- und Steuerzusammenstellung und – wenn keine Verkaufsaktivität stattfindet – eine rotierende Präsentation Ihrer Werbung."
    },
    {
      "type": "paragraph",
      "content": "Dieser Leitfaden behandelt die Hardware- und Paarungseite des Einrichtens Ihres Kundendisplays: das Aktivieren der Funktion auf einem Terminal, das Paaren eines separaten Geräts als Display-Bildschirm und das Verwalten von gängigen Einrichtungsszenarien. Für Informationen zu den Werbebilderfolien, die während der Ruhezeiten angezeigt werden, siehe [Kundendisplay-Werbefolien](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Was das Kundendisplay anzeigt"
    },
    {
      "type": "paragraph",
      "content": "Wenn ein Verkauf aktiv ist, zeigt das Kundendisplay Folgendes an:"
    },
    {
      "type": "list",
      "content": [
        "Jedes erfasste oder entfernte Artikel mit Menge und Preis",
        "Den Warenkorb-Teilbetrag, alle angewandten Rabatte und die Steuerzusammenstellung",
        "Den fälligen Gesamtbetrag und während der Zahlung den gezahlten Betrag und den Wechselgeld"
      ]
    },
    {
      "type": "paragraph",
      "content": "Wenn das Terminal ruht (keine aktive Transaktion), wechselt das Display in eine Werbebilderfolie. Sie steuern den Inhalt dieser Bilderfolie separat – siehe [Kundendisplay-Werbefolien](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Gängige Hardware-Setups"
    },
    {
      "type": "paragraph",
      "content": "Es gibt drei praktische Arten, einen Kundenfassenden Bildschirm einzurichten:"
    },
    {
      "type": "list",
      "content": [
        "**Separater Tablet oder Monitor auf einem Ständer** – das gängigste Setup für Kassentheke. Ein kleines Tablet, das auf einem Ständer gestellt ist, ist dem Kunden zugewandt, während Ihr Hauptterminal Ihnen zugewandt ist. Sie pairen die beiden Geräte mithilfe eines kurzlebigen Codes (wie unten beschrieben).",
        "**Zweiter Monitor im erweiterten Desktop-Modus** – wenn Ihr Hauptterminal ein Laptop oder Desktop ist, stecken Sie einen zweiten Monitor an, erweitern Sie Ihren Desktop darauf, ziehen Sie das Display-Fenster auf den zweiten Monitor und maximieren Sie es. Beide Bildschirme laufen auf demselben Gerät; kein Paarungscode ist erforderlich.",
        "**Dedizierter Stab-Display** – ein Hardware-Display-Gerät, das an einem Stab montiert ist, typischerweise über USB mit dem Kassen-Terminal verbunden oder auf der Kasse platziert. Öffnen Sie `/pos/display/` im Browser des Stab-Geräts und pairen Sie es mithilfe des Codes vom Hauptterminal."
      ]
    },
    {
      "type": "heading",
      "content": "Aktivieren des Kundendisplays auf einem Terminal"
    },
    {
      "type": "paragraph",
      "content": "Die Kundendisplay-Funktion wird pro Terminal über die Hardware-Konfiguration des Terminals aktiviert."
    },
    {
      "type": "list",
      "content": [
        "Navigieren Sie zu **POS > Terminals** und öffnen Sie das Terminal, das Sie konfigurieren möchten (oder klicken Sie auf **+ POS-Terminal hinzufügen**, um ein neues Terminal hinzuzufügen).",
        "Klicken Sie auf die Registerkarte **Gerät**.",
        "Scrollen Sie zu der Karte **Hardware-Konfiguration**. Sie sehen ein JSON-Feld.",
        "Fügen Sie `"customer_display": true` zum JSON-Objekt hinzu. Beispiel:"
      ]
    },
    {
      "type": "code-block",
      "content": "{'customer_display': true}"
    },
    {
      "type": "paragraph",
      "content": "Wenn das Feld bereits andere Hardware-Einstellungen enthält (z. B. Drucker- oder Scanner-Konfiguration), fügen Sie `"customer_display": true` neben diesen hinzu:"
    },
    {
      "type": "code-block",
      "content": "{'printer': 'HP LaserJet', 'scanner': 'Datalogic', 'customer_display': true}"
    },
    {
      "type": "list",
      "content": [
        "Klicken Sie auf **Speichern**."
      ]
    },
    {
      "type": "image",
      "content": "![Terminal-Hardware-Konfiguration mit aktiviertem customer_display](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
    },
    {
      "type": "paragraph",
      "content": "Nachdem die Funktion aktiviert wurde, öffnet die POS-App auf diesem Terminal das Kundendisplay-Ansicht in einem zweiten Browserfenster oder -tab, wenn eine Sitzung gestartet wird."
    },
    {
      "type": "heading",
      "content": "Ein separates Gerät als Display paaren"
    },
    {
      "type": "paragraph",
      "content": "Wenn Sie ein physisch separates Gerät für den Kundenbildschirm verwenden (ein Tablet, ein Smartphone oder ein zweiter Computer), paaren Sie es mit dem Terminal mithilfe eines kurzlebigen 6-stelligen Codes."
    },
    {
      "type": "heading",
      "content": "Schritt 1: Erstellen Sie einen Paarungscode auf dem Hauptterminal

Öffnen Sie die POS-App auf Ihrem Hauptterminal und navigieren Sie zu den Anzeige-Einstellungen oder dem Paarungsbereich der Terminal-Oberfläche.

Fordern Sie einen neuen Anzeigepaarungscode an.

Der Code ist eine 6-stellige Zahl und ist **5 Minuten** lang gültig.

Wenn Sie einen neuen Code generieren, werden automatisch alle vorherigen, nicht verwendeten Codes für dieses Terminal abgebrochen.

### Schritt 2: Öffnen Sie die Anzeige-URL auf dem Kunden-Gerät

Auf dem Kunden-Gerät öffnen Sie einen Webbrowser und navigieren Sie zu:

```
https://your-store-domain.com/pos/display/
```

Eine Anmeldung ist nicht erforderlich — die Anzeigenseite ist öffentlich zugänglich. Dies ist beabsichtigt: das Anzeigegerät benötigt keine Mitarbeiter-Anmeldeinformationen, und der Paarungscode stellt die Verbindung zwischen der Anzeige und dem richtigen Terminal her.

![Kundenanzeige im Ruhezustand](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Schritt 3: Geben Sie den Paarungscode ein

Auf dem Kunden-Gerät geben Sie den 6-stelligen Code vom Hauptterminal ein. Die Anzeige wird mit diesem Terminal gepaart und beginnt, die Live-Warenkorbdaten anzuzeigen.

Sobald der Code verwendet wurde, wird er sofort ungültig und kann nicht erneut verwendet werden.

## Neuer Paarungscode generieren

Wenn der Paarungscode abläuft, bevor Sie ihn eingeben können, oder wenn Sie das Anzeigegerät erneut paaren müssen (z. B. wenn ein Anzeigegerät ausgetauscht oder zurückgesetzt wird), generieren Sie einen neuen Code über die POS-App auf dem Hauptterminal.

Die Generierung eines neuen Codes bricht automatisch alle bestehenden, nicht verwendeten Codes für dieses Terminal ab. Der neue Code ist 5 Minuten lang gültig.

Sie müssen nichts im Admin-Panel ändern, um einen neuen Code zu generieren — dies erfolgt vollständig innerhalb der POS-App.

## Mehrere Monitore auf einem Gerät

Wenn Ihr Hauptterminal ein Laptop oder ein Desktop mit zwei Monitoren ist:

1. Schließen Sie den zweiten Monitor an und stellen Sie ihn im Anzeigemenü Ihres Betriebssystems auf **erweiterten Desktop**-Modus ein (nicht gespiegelt).
2. Öffnen Sie die POS-App wie gewohnt auf dem primären Bildschirm.
3. Die POS-App öffnet die Kundenanzeige in einem zweiten Fenster. Ziehen Sie dieses Fenster auf den zweiten Monitor.
4. Maximieren Sie oder schalten Sie den zweiten Monitor in den Vollbildmodus.

Ein Paarungscode ist nicht erforderlich, da beide Fenster auf demselben Gerät laufen und direkt miteinander kommunizieren.

## Verhalten im Ruhezustand

Wenn keine aktive Verkaufsaktion stattfindet, zeigt die Kundenanzeige eine rotierende Slideshow von Werbebildern. Sie erstellen und verwalten diese Slides separat unter **POS > Promo Slides**.

Für Details zur Erstellung von Slides, zum Zielsetzen auf bestimmte Geschäfte und zur Verwaltung von Saisoninhalten siehe [Kundenanzeige Promo Slides](customer-display-promo-slides).

Wenn keine Slides konfiguriert sind, zeigt die Anzeige eine einfache Willkommensseite mit dem Namen Ihres Geschäfts.

## Problembehandlung

**Die Anzeige ist leer oder hat aufgehört, sich zu aktualisieren**

Die Anzeige kommuniziert in Echtzeit mit dem Hauptterminal. Wenn die Verbindung unterbrochen wird, kann die Anzeige leer werden oder veraltete Daten anzeigen. Aktualisieren Sie den Browser auf dem Kunden-Gerät. Wenn dies nicht hilft, generieren Sie einen neuen Paarungscode und paaren Sie die Anzeige erneut.

**Die Anzeige zeigt den Warenkorb des falschen Terminals an**

Jede Anzeige ist einem bestimmten Terminal zugeordnet. Wenn Sie mehrere Terminals haben, stellen Sie sicher, dass Sie den Paarungscode auf dem richtigen Terminal generiert und ihn auf der Anzeige eingegeben haben. Um ein Missmatch zu beheben, generieren Sie einen neuen Code auf dem richtigen Terminal und paaren Sie das Anzeigegerät erneut.

**Der Paarungscode ist abgelaufen, bevor ich ihn eingeben konnte**

Die Codes sind 5 Minuten lang gültig. Generieren Sie einen neuen Code über die POS-App und geben Sie ihn auf dem Anzeigegerät schnell ein. Halten Sie die beiden Geräte während des Paarungsprozesses nahe beieinander.

**Der Paarungscode wurde eingegeben, aber die Anzeige hat sich nicht verbunden**

Stellen Sie sicher, dass das Kunden-Gerät auf Ihr Geschäfts-Domain zugreifen kann (es benötigt Netzwerkzugriff). Überprüfen Sie auch, ob `"customer_display": true` in der Hardwarekonfiguration des Terminals gesetzt ist, und dass das Terminal gespeichert wurde.

**Die Anzeige-URL gibt einen Fehler zurück**

Stellen Sie sicher, dass Sie zu `/pos/display/` auf Ihrer Geschäfts-Domain navigieren, nicht zur Admin-URL. Die Anzeigeanzeige erfordert keine Anmeldung — wenn Sie aufgefordert werden, sich anzumelden, überprüfen Sie die URL erneut.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Halten Sie die Paarungssitzung kurz** — stellen Sie sicher, dass das Kunden-Gerät bereit ist und der Browser auf `/pos/display/` geöffnet ist, bevor Sie den Paarungscode generieren.

Sie haben 5 Minuten, aber das Abschließen innerhalb weniger als einer Minute vermeidet das Auslaufen der Sitzung.

- **Testen Sie vor dem Öffnen** — führen Sie mit dem Display verbunden einen Testverkauf durch, um sicherzustellen, dass Kunden die richtigen Artikel und Gesamtbeträge sehen, bevor Sie Ihren ersten echten Verkauf durchführen.

- **Fügen Sie die Display-URL als Lesezeichen hinzu** — konfigurieren Sie den Browser des Kunden-Geräts so, dass er beim Start `/pos/display/` öffnet, damit das Gerät immer bereit ist.

- **Verwenden Sie den erweiterten Desktop für mehr Einfachheit** — wenn Ihr Terminal einen zusätzlichen HDMI-Anschluss und einen Monitor zur Verfügung stellt, erfordert der erweiterte Desktop-Ansatz keine laufende Paarung und läuft nie ab.

- **Fügen Sie Promo-Slides vor dem Öffnen hinzu** — ein leerer Willkommensbildschirm, der nur angezeigt wird, wenn das Display nicht in Gebrauch ist, ist eine verpasste Gelegenheit.

Richten Sie mindestens ein paar Promo-Slides ein, damit das Display auch dann nützlich ist, wenn kein Verkauf stattfindet.

Siehe [Customer Display Promo Slides](customer-display-promo-slides).

- **Sichern Sie das Display-Gerät** — die Display-URL ist per Design öffentlich zugänglich, zeigt aber nur Live-Warenkorb-Daten an, wenn sie mit einem aktiven Terminal gepaart ist.

Dennoch sollten Sie eine Kiosk-Browser-Modus auf dem Kunden-Gerät in Betracht ziehen, um Kunden davon abzuhalten, anderswo zu navigieren.