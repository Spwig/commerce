---
title: Kundentasche
---

Die Kundentasche ist ein Kredit-System für den Laden, das Kunden einen Saldo gewährt, den sie für zukünftige Bestellungen verwenden können. Ladenkredite können als Ergebnis von Rückgaben, Empfehlungsbelohnungen, Werbekampagnen oder manuellen Anpassungen, die Ihr Team vornimmt, hinzugefügt werden. Kunden können dann ihren Taschensaldo beim Checkout anwenden, um den Betrag, den sie zahlen, zu reduzieren.

Navigieren Sie zu **Kunden > Kundentaschen**, um Taschen anzuzeigen und zu verwalten.

## Verständnis von Taschensalden

Jede Kundentasche zeigt vier Saldo-Nummern an:

| Saldo | Beschreibung |
|---|---|
| **Verfügbares Saldo** | Der Betrag, den der Kunde jetzt beim Checkout ausgeben kann |
| **Ausstehendes Saldo** | Kredite, die noch nicht auszahlbar sind – beispielsweise eine Rückgabe, die noch in ihrer Bestätigungszeit liegt |
| **Lebenslanger Kredit** | Der Gesamtbetrag, der je nach Wallet je nach Zeitpunkt vergeben wurde, einschließlich aller früheren Kredite |
| **Lebenslanger Verbrauch** | Der Gesamtbetrag, den der Kunde aus seiner Tasche für alle Bestellungen ausgegeben hat |

Das verfügbare Saldo ist die einzige Zahl, die beim Checkout zählt. Ausstehende Kredite werden verfügbar, sobald die Ausstehenszeit abgelaufen ist.

## Kundentasche ansehen

1. Navigieren Sie zu **Kunden > Kundentaschen**
2. Verwenden Sie das Suchfeld, um den Kunden nach Namen oder E-Mail zu finden
3. Klicken Sie auf den Eintrag der Tasche, um die Detailansicht zu öffnen

Die Detailansicht zeigt die aktuellen Saldo-Nummern oben und eine vollständige Transaktionshistorie unten. Die Zeitstempel **Zuletzt vergeben** und **Zuletzt genutzt** zeigen an, wann die Tasche zuletzt aktiv war.

### Filtern der Taschenliste

Verwenden Sie den **Aktiv**-Filter, um aktive Taschen von gefrorenen zu trennen. Eine Tasche, die als inaktiv markiert ist, kann nicht beim Checkout verwendet werden, auch wenn sie einen positiven Saldo hat.

## Transaktionshistorie einsehen

Jede Änderung des Taschensaldos wird als einzelne Transaktion aufgezeichnet. Die Transaktionshistorie ist ein vollständiges, dauerhaftes Buch – Transaktionen werden niemals bearbeitet oder gelöscht. Wenn ein Fehler behoben werden muss, wird stattdessen eine neue Gegentransaktion hinzugefügt.

Jede Transaktion zeigt:

| Feld | Beschreibung |
|---|---|
| **Typ** | Kredit, Debit, Rückgabe, Anpassung oder Umkehrung |
| **Betrag** | Der Wert dieser Transaktion (immer als positiver Betrag angezeigt) |
| **Saldo nach** | Der Taschensaldo unmittelbar nach Anwendung dieser Transaktion |
| **Quelle** | Wo der Kredit oder Debit ursprünglich stammt |
| **Status** | Abgeschlossen, Ausstehend oder Umgekehrt |
| **Beschreibung** | Eine kurze Erklärung der Transaktion |
| **Referenz-ID** | Ein Link zur ursprünglichen Aufzeichnung (z. B. einer Bestellnummer oder Belohnungs-ID) |
| **Erstellt am** | Wann die Transaktion aufgezeichnet wurde |

### Erklärung der Transaktionstypen

- **Kredit** – Geld, das der Tasche hinzugefügt wird (aus einer Rückgabe, Promotion oder manueller Anpassung)
- **Debit** – Geld, das beim Checkout ausgegeben wird
- **Rückgabe** – Kredit, der speziell als Ergebnis einer zurückgegebenen oder abgebrochenen Bestellung hinzugefügt wird
- **Anpassung** – eine manuelle Korrektur, die von Ihrem Team vorgenommen wird
- **Umkehrung** – eine Transaktion, die eine frühere Eintragung aufhebt

### Erklärung der Transaktionsquellen

- **Bestellrückgabe** – Kredit, der vergeben wird, wenn eine Bestellung an die Tasche zurückgegeben wird
- **Empfehlungsbelohnung** – Kredit, der durch das Empfehlungsprogramm verdient wird
- **Promotion** – Kredit, der als Teil einer Marketingkampagne vergeben wird
- **Manuelle Anpassung** – Kredit, der direkt von einem Mitarbeiter hinzugefügt oder entfernt wird
- **Bestellzahlung** – Geld, das beim Checkout für eine Bestellung ausgegeben wird

## Manuelle Taschenanpassungen

Sie können Geld nicht direkt aus der Detailansicht der Tasche hinzufügen oder entfernen – Taschentransaktionen werden durch die relevanten Prozesse (Rückgaben, Belohnungen, Promotionen) erstellt. Allerdings können Mitarbeiter mit den entsprechenden Berechtigungen manuelle Anpassungstransaktionen über den Abschnitt **Taschentransaktionen** erstellen.

Navigieren Sie zu **Kunden > Taschentransaktionen** und verwenden Sie **+ Taschentransaktion hinzufügen**, wenn Sie einen Kredit anwenden müssen, der nicht zu einer anderen Quelle passt – beispielsweise einen Goodwill-Kredit nach einer Beschwerde über den Service.

Bei der Erstellung einer manuellen Anpassung:

1.

Wählen Sie die **Tasche** aus, die Sie anpassen (suchen Sie nach der E-Mail-Adresse des Kunden)
2.


Setze **Transaktionsart** auf `Anpassung`
3.

Setze **Quelle** auf `Manuelle Anpassung`
4.

Gib den **Betrag** ein – immer eine positive Zahl, unabhängig von der Richtung
5.

Setze den **Status** auf `Abgeschlossen`, um einen sofortigen Gutschrift zu vergeben
6.

Füge eine klare **Beschreibung** hinzu, die den Grund erklärt – dies ist im Transaktionsverlauf sichtbar
7.

Klicke auf **Speichern**

> **Hinweis:** Da Wallet-Transaktionen unveränderlich sind, überprüfe den Betrag und das Wallet noch einmal, bevor du speicherst. Falls du einen Fehler machst, musst du eine Gegenbuchung erstellen, um dies zu korrigieren.

## Das Wallet sperren

Wenn du einen Kunden davon abhalten möchtest, sein Wallet-Guthaben zu verwenden – beispielsweise während einer Betrugsuntersuchung – kannst du es deaktivieren, ohne es zu löschen oder das Guthaben zu entfernen.

1. Öffne den Detailansicht des Kunden-Wallets
2. Deaktiviere den **Aktiv**-Schalter
3. Klicke auf **Speichern**

Das Guthaben bleibt erhalten und das Wallet kann jederzeit wieder aktiviert werden. Während es inaktiv ist, kann der Kunde das Wallet-Guthaben beim Checkout nicht verwenden.

## Alle Transaktionen ansehen

Für eine Gesamtansicht der Wallet-Aktivitäten navigiere zu **Kunden > Wallet-Transaktionen**. Diese Liste zeigt jede Transaktion in allen Kunden-Wallets, mit Filtern für:

- **Transaktionsart** – filtere nach Gutschrift, Abbuchung, Anpassung usw.
- **Quelle** – filtere nach dem Ursprung der Transaktionen
- **Status** – filtere nach abgeschlossen, ausstehend oder rückgängig gemacht
- **Datum** – nutze die Datenhierarchie oben, um in ein bestimmtes Tag, Monat oder Jahr einzusteigen

Die Transaktionsliste ist schreibgeschützt – Transaktionen können nicht bearbeitet oder gelöscht werden.

## Tipps

- Überprüfe **Lebenslange Gutschriften** versus **Lebenslange Nutzung**, um zu verstehen, wie aktiv ein Kunde sein Store-Guthaben verwendet – ein großes, nicht genutztes Guthaben kann darauf hindeuten, dass der Kunde es vergessen hat
- Wenn ein Kunde meldet, dass sein Guthaben falsch aussieht, überprüfe die vollständige Transaktionshistorie, um genau zu verfolgen, wie sich das Guthaben im Laufe der Zeit verändert hat; die Spalte **Guthaben nach** auf jedem Eintrag macht dies einfach
- Nutze Wallet-Guthaben als Kundenbindungsinstrument – eine Gutschrift als Goodwill nach einem schwierigen Bestell-Erlebnis kann günstiger sein als eine Erstattung, während der Kunde weiterhin in deinem Store ausgibt
- Gefrorene Wallets behalten ihr Guthaben dauerhaft; es gibt keine Ablaufdatum – wenn du ein Wallet vorübergehend deaktivierst, erinnere dich daran, es wieder zu aktivieren, sobald das Problem gelöst ist
- Die **Referenz-ID** auf jeder Transaktion verweist auf den ursprünglichen Eintrag, wodurch es einfach ist, zu überprüfen, warum eine Gutschrift oder Abbuchung angewendet wurde, ohne anderswo suchen zu müssen