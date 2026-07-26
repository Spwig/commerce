---
title: Gutscheinkarten
---

Gutscheinkarten sind Einzahlungen, die Kunden für jemand anderen – oder für sich selbst – per E-Mail als eindeutigen Gutscheincode übermitteln können. Sie können eine Gutscheinkarte auch direkt aus dem Admin-Panel ohne Kundenkauf ausstellen.

Der Verkauf von Gutscheinkarten ist aktiv. Wenn ein Kunde eine Karte kauft, wird diese automatisch erstellt und per E-Mail gesendet, sobald die Zahlung abgeschlossen ist – niemals vorher, damit niemand einen Code für eine später fehlgeschlagene Zahlung erhält.

Ein paar Dinge, die Sie wissen sollten, bevor Sie ein Gutscheinkartenprodukt aktivieren:

- **Eine Gutscheinkarte ist Geld, nicht ein Rabatt.** Sie wird vom Endbetrag nach Steuern und Versand abgezogen und verringert nicht die Steuern, die Sie zahlen müssen. Das ist das Gegenteil eines Gutscheins, der den Preis der Waren reduziert.
- **Karten sind in einer einzigen Währung.** Eine in Euro gekaufte Karte kann nur für einen Euro-Bestellung verwendet werden. Wenn Sie in mehreren Währungen verkaufen, erstellen Sie bitte ein separates Gutscheinkartenprodukt für jede Währung. Das schützt Sie vor Wechselkursbewegungen auf einem Saldo, das möglicherweise ein Jahr lang nicht ausgegeben wird.
- **Gutscheinkarten können nicht vergünstigt werden.** Ein Gutschein gilt nicht für eine Gutscheinkartenposition, da der Verkauf von 100 £ Kredit für 80 £ Sie jedes Mal 20 £ kostet.
- **Eine Gutscheinkarte kann keine andere Gutscheinkarte kaufen.** Das schließt einen Weg, den Menschen nutzen, um gestohlene Karteninformationen zu waschen.
- **Das Kaufen einer Gutscheinkarte bringt keine Treuepunkte.** Die Punkte werden erzielt, wenn die Karte für Waren verwendet wird, also erhält niemand zweimal für das gleiche Geld.

![Gutscheinkarten-Verwaltung](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Nennungstypen

Diese Einstellungen steuern, wie ein Kunde den Betrag wählt, wenn er eine Gutscheinkarte kauft:

| Typ | Beschreibung |
|------|-------------|
| **Feste Nennungen** | Kunden wählen aus vordefinierten Beträgen (z. B. 25 $, 50 $, 100 $) |
| **Benutzerdefinierter Betrag** | Kunden können einen beliebigen Betrag innerhalb eines Min-/Max-Bereichs eingeben |
| **Beide** | Bieten Sie feste Nennungen an und fügen Sie eine Option für einen benutzerdefinierten Betrag hinzu |

## Erstellen eines Gutscheinkartenprodukts

Jede Gutscheinkarte – ob sie letztendlich verkauft wird oder heute manuell ausgestellt wird – benötigt zuerst ein Gutscheinkartenprodukt.

### Schritt 1: Produkt einrichten

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt hinzufügen**
2. Wählen Sie **Produkttyp** auf **Gutscheinkarte**
3. Geben Sie den Produktname und die Beschreibung ein
4. Konfigurieren Sie die Nennungseinstellungen:
   - Wählen Sie einen **Nennungstyp** (Fest, Benutzerdefiniert oder Beide)
   - Für Fest: legen Sie die verfügbaren Nennungsbeträge fest
   - Für Benutzerdefiniert: setzen Sie den **Mindest-** und **Höchstbetrag**
5. Setzen Sie **Ablauf in Tagen** (0 = nie abläuft) – dies bestimmt, wie lange Gutscheinkarten nach dem Kauf gültig sind
6. Speichern und veröffentlichen Sie das Produkt

### Schritt 2: Veröffentlichen

Veröffentlichen Sie das Produkt, wenn Sie bereit sind, es zu verkaufen. Kunden können es sofort aus Ihrem Onlineshop kaufen, und die Karte wird automatisch per E-Mail gesendet, sobald ihre Zahlung abgeschlossen ist.

Das Produkt ist auch das, das Sie auswählen, wenn Sie eine Karte manuell ausstellen – also lohnt es sich, eines zu erstellen, auch wenn Sie nur vorhaben, Karten zu verschenken.

## Gutscheinkarte manuell erstellen

Dies ist der einzige Weg, eine finanzierte Gutscheinkarte jetzt zu erstellen, und es funktioniert vollständig heute.

1. Navigieren Sie zu **Produkte > Gutscheinkarten** und klicken Sie auf **+ Gutscheinkarte hinzufügen**
2. Wählen Sie das **Produkt** – dies muss ein bestehendes Gutscheinkartenprodukt sein (siehe oben)
3. Geben Sie den **Anfangswert** ein – der Startguthabenbetrag, in beliebigen Beträgen, die Sie wählen. Im Gegensatz zu einem Kundenkauf ist dies nicht auf die Nennungseinstellungen des Produkts beschränkt
4. Setzen Sie optional ein **Ablaufdatum** und lassen Sie **Aktiv** aktiviert, damit die Karte eingelöst werden kann
5. Füllen Sie den **Empfänger**-Abschnitt weiter unten auf der gleichen Seite aus:
   - **Empfänger-E-Mail** – erforderlich; Ort, an den die Liefer-E-Mail gesendet wird
   - **Empfängername**, **Absendername** und **Persönliche Nachricht** – alle optional
   - **Geplantes Sendedatum** – optional; lassen Sie es leer und senden Sie es, sobald Sie bereit sind, oder setzen Sie ein zukünftiges Datum/Uhrzeit (z. B. ein Geburtstag)
6. Klicken Sie auf **Speichern**

Der Einlösungscodewird automatisch generiert und der Startguthabenbetrag wird aus dem Anfangswert gesetzt – Sie füllen weder von diesen beiden Feldern selbst ein.

**Das Speichern der Karte sendet keine E-Mail.** Um sie zu versenden, kehren Sie zur Geschenkkartenliste zurück, aktivieren Sie das Häkchen der Karte, wählen Sie **Geschenkkarten-E-Mails senden** im Aktionen-Dropdown aus und klicken Sie auf **Weiter**.

Die gleiche Aktion sendet die E-Mail erneut, wenn Sie sie später erneut senden müssen.

## Verwaltung von Geschenkkarten im Admin

Navigieren Sie zu **Produkte > Geschenkkarten**, um alle Geschenkkarten zu verwalten:

### Statistik-Dashboard

Oben auf der Seite zeigen vier Karten die wichtigsten Kennzahlen an:

- **Gesamtzahl der Geschenkkarten** — Gesamtzahl der ausgestellten Geschenkkarten
- **Aktiv** — Aktuelle Karten mit verfügbarem Saldo
- **Gesamtsaldo** — Gesamtes verbleibendes Saldo über alle Karten
- **Teilweise genutzt** — Karten, die teilweise eingelöst wurden

### Filter

Filtern Sie Geschenkkarten nach:

- **Suche** — Nach Code, E-Mail oder Empfängername suchen
- **Status** — Aktiv, Inaktiv, Abgelaufen, Vollständig eingelöst oder Teilweise genutzt
- **Saldo** — Mit Saldo oder Nullsaldo
- **Erstellt** — Zeitraum (Heute, Diese Woche, Dieser Monat, Dieses Jahr)

### Geschenkkarten-Details

Jede Geschenkkarte zeigt an:

- **Code** — Der eindeutige Einlösungscode (z. B. GC-XXXX-XXXX-XXXX)
- **Empfänger** — E-Mail und Name
- **Status-Abzeichen** — Aktueller Status mit Farbcodierung
- **Saldo / Anfangsbetrag / Einlösung** — Finanzübersicht mit Prozent genutzt
- **Wichtige Daten** — Erstellt, ausgestellt, erster Gebrauch
- **Absender** — Wer die Geschenkkarte gekauft (oder ausgestellt) hat

### Aktionen

- Klicken Sie auf eine Geschenkkarte, um ihre **Details zu bearbeiten** und ihre vollständige **Transaktionshistorie** anzuzeigen, die inline auf derselben Seite angezeigt wird
- Wählen Sie eine oder mehrere Karten aus und verwenden Sie das **Aktionen**-Dropdown, um **Geschenkkarten-E-Mails zu senden** (liefert oder sendet die Liefer-E-Mail erneut) oder **Ausgewählte Geschenkkarten als inaktiv markieren** (deaktiviert — das Saldo bleibt erhalten, aber die Karte kann nicht mehr eingelöst werden)

## Einlösung heute

**Im Geschäft**, an Ihrem Kassenterminal:

1. Der Kassierer nimmt den Code im Zahlungsschritt entgegen
2. Der Code wird validiert — aktiv, nicht abgelaufen, mit Saldo und in derselben Währung wie der Verkauf
3. Das Saldo wird auf den gesamten fälligen Betrag angewendet, einschließlich Steuern und Lieferkosten
4. Wenn das Saldo den gesamten Verkauf nicht abdeckt, zahlt der Kunde den Rest auf andere Weise
5. Das Saldo wird abgebucht und die Transaktion wird protokolliert

Beachten Sie, dass der Kassierer den Code am **Zahlungsschritt** entgegennimmt, nicht beim Zusammenstellen des Warenkorbs. Eine Geschenkkarte ist Geld, das der Kunde bereits übergeben hat, daher begleicht sie die Rechnung, anstatt die Waren zu vergünstigen.

**Online** hat der Checkout-Schritt ein Feld für Geschenkkarten am Zahlungsschritt. Der Kunde gibt seinen Code ein, das Saldo wird vom fälligen Betrag abgezogen — nach Steuern und Lieferkosten — und der Rest wird wie gewohnt auf seine Karte belastet. Wenn die Karte den gesamten Auftrag abdeckt, ist keine weitere Zahlung erforderlich. Das Saldo wird erst tatsächlich abgebucht, wenn die Zahlung bestätigt wird, daher berührt ein abgebrochener Checkout die Karte nie.

Empfänger können auch jederzeit den verbleibenden Saldo anhand des Links in ihrer Liefer-E-Mail überprüfen.

## Rückerstattung

Bei Rückerstattungen von Bestellungen oder Verkäufen, die eine Geschenkkarte verwendet haben:

- **Eine von dem Kunden gekaufte Geschenkkarte, die noch nicht verwendet wurde** — die Karte wird deaktiviert und ihr Saldo auf Null gesetzt, sodass der Kredit mit der Rückerstattung verschwindet.
- **Eine von dem Kunden gekaufte Geschenkkarte, die teilweise genutzt wurde** — dies erfordert Ihre Einschätzung. Die Deaktivierung würde den Kredit zurücknehmen, den der Kunde bereits genutzt hat, daher bleibt das Saldo unverändert und wird für Sie markiert, um es manuell anzupassen.
- **Eine Geschenkkarte, die zur Bezahlung der rückzuerstattenden Bestellung verwendet wurde** — die Rückerstattung geht zuerst auf die Karte zurück, bevor jede Karte oder Bankzahlung erfolgt. Das Zurückgeben von Geld an eine Bank, von der der Händler nie tatsächlich Geld erhalten hat, ist der größere Fehler, und das Zurückgeben von Wert an den ursprünglichen Ort schließt einen bekannten Betrugsweg ab. Wenn die ursprüngliche Karte seitdem abgelaufen oder deaktiviert wurde, wird eine Ersatzkarte ohne Ablaufdatum an denselben Empfänger ausgestellt.
- **Vollständige Rückerstattung** — Kreditieren Sie den Betrag über die Geschenkkarten-Saldo über eine Rückerstattungstransaktion

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Verwenden Sie manuelle Ausstellung für Goodwill-Gutschriften, Kundendienstlösungen oder in jedem Fall, in dem Sie einem Kunden ohne Kauf im Onlineshop ein Guthaben gewähren möchten.
- Legen Sie realistische Ablaufzeiten fest (z. B. 365 Tage), um den lokalen Geschenkkartenregelungen zu entsprechen – einige Jurisdiktionen verlangen Mindestgültigkeitszeiträume.
- Verwenden Sie den Bezeichnungstyp "Beide", um Bequemlichkeit (vordefinierte Beträge) und Flexibilität (einen individuellen Betrag) anzubieten.
- Überwachen Sie regelmäßig das Metric "Gesamtbetrag" – es stellt eine offene Verbindlichkeit auf Ihren Büchern dar.
- Eine Karte wird online und vor Ort gleichartig ausgegeben – bei der Web-Bezahlung im Zahlungsschritt oder am Kassentisch.

Die Liefer-E-Mail enthält einen Link zur Kontrolle des Kontostands, den die Empfänger jederzeit verwenden können.
- Wenn Sie Kunden in mehreren Ländern bedienen, können Sie Geschenkkarten in bestimmten Währungen ausstellen – siehe den Hilfethema **Multi-Currency Gift Cards** für Details.