---
title: Kundentasche
---

Die Kundentasche ist ein Kreditbuch, das den aktuellen Saldo für jeden Kunden verfolgt. Kredit kann durch Rückerstattungen, Empfehlungsbelohnungen, Werbekampagnen oder manuelle Anpassungen, die Ihr Team vornimmt, hinzugefügt werden.

> **Taschensalden können am Kasse verwendet werden.** Ein angemeldeter Kunde mit Kredit sieht diesen auf dem Zahlungsschritt und kann ihn mit einem Klick anwenden. Der Kredit wird vom Endbetrag abgezogen – nach Steuern und Lieferkosten – und der Rest wird wie gewohnt auf seine Karte belastet. Wenn der Kredit den gesamten Auftrag abdeckt, ist keine Karte erforderlich. Der Kredit wird reserviert, sobald er angewendet wird, und erst tatsächlich abgebucht, wenn die Zahlung bestätigt wird, sodass ein verlassener Kassenabschluss dem Kunden nichts kostet.

Navigieren Sie zu **Kunden > Kundentaschen**, um Taschen anzuzeigen und zu verwalten.

## Verständnis von Taschensalden

Jede Kundentasche zeigt vier Saldoangaben an:

| Saldo | Beschreibung |
|---|---|
| **Verfügbares Saldo** | Der aktuelle, verwendbare Kredit des Kunden – dies ist der Betrag, der am Kassenabschluss verwendet werden kann, sobald diese Funktion bereitsteht |
| **Ausstehendes Saldo** | Kredite, die noch nicht im verfügbaren Saldo enthalten sind – beispielsweise eine Rückerstattung, die noch in ihrer Bestätigungszeit liegt |
| **Lebenslanger Kredit** | Der Gesamtbetrag, der je nach Wallet je nach Zeitpunkt vergeben wurde, einschließlich aller früheren Kredite |
| **Lebenslanger Verbrauch** | Der Gesamtbetrag, der je nach Wallet je nach Zeitpunkt abgebucht wurde |

Das verfügbare Saldo ist die Zahl, die zählt, sobald der Kassenabschluss aktiv ist. Ausstehende Kredite werden in dieses Saldo übertragen, sobald die Ausstehenszeit abgelaufen ist.

## Anzeigen der Kundentasche

1. Navigieren Sie zu **Kunden > Kundentaschen**
2. Verwenden Sie das Suchfeld, um den Kunden nach Namen oder E-Mail zu finden
3. Klicken Sie auf den Eintrag der Tasche, um die Detailansicht zu öffnen

Die Detailansicht zeigt die aktuellen Saldoangaben oben und eine vollständige Transaktionshistorie unten. Die Zeitstempel **Zuletzt vergeben am** und **Zuletzt verwendet am** zeigen an, wann die Tasche zuletzt aktiv war.

### Filtern der Taschenliste

Verwenden Sie den **Aktiv**-Filter, um aktive Taschen von gefrorenen zu trennen. Eine als inaktiv markierte Tasche ist gefroren – keine Kredite oder Abbuchungen können gegen sie gebucht werden, obwohl sie ihren Saldo behält.

## Lesen der Transaktionshistorie

Jede Änderung des Taschensaldos wird als einzelne Transaktion aufgezeichnet. Die Transaktionshistorie ist ein vollständiges, dauerhaftes Buch – Transaktionen werden niemals bearbeitet oder gelöscht. Wenn ein Fehler behoben werden muss, wird stattdessen eine neue Gegentransaktion hinzugefügt.

Jede Transaktion zeigt an:

| Feld | Beschreibung |
|---|---|
| **Typ** | Kredit, Abbuchung, Rückerstattung, Anpassung oder Rückgängigmachung |
| **Betrag** | Der Wert dieser Transaktion (immer als positiver Betrag angezeigt) |
| **Saldo nach** | Der Taschensaldo unmittelbar nach Anwendung dieser Transaktion |
| **Quelle** | Wo der Kredit oder die Abbuchung stammt |
| **Status** | Abgeschlossen, Ausstehend oder Rückgängig |
| **Beschreibung** | Eine kurze Erklärung der Transaktion |
| **Referenz-ID** | Ein Link zur ursprünglichen Aufzeichnung (z. B. einer Bestellnummer oder Belohnungs-ID) |
| **Erstellt am** | Wann die Transaktion aufgezeichnet wurde |

### Erklärung der Transaktionstypen

- **Kredit** – Geld, das der Tasche hinzugefügt wird (aus einer Rückerstattung, Promotion oder manueller Anpassung)
- **Abbuchung** – Geld, das aus der Tasche abgebucht wird. Sobald der Kassenabschluss aktiv ist, bedeutet dies „auf einen Auftrag ausgegeben“ – derzeit ist die einzige Möglichkeit, eine Abbuchung vorzunehmen, eine manuelle Anpassung
- **Rückerstattung** – Kredit, der speziell als Ergebnis einer zurückgegebenen oder stornierten Bestellung hinzugefügt wird
- **Anpassung** – eine manuelle Korrektur, die von Ihrem Team vorgenommen wird
- **Rückgängigmachung** – eine Transaktion, die eine frühere Eintragung aufhebt

### Erklärung der Transaktionsquellen

- **Bestellrückerstattung** – Kredit, der vergeben wird, wenn eine Bestellung an die Tasche zurückerstattet wird
- **Empfehlungsbelohnung** – Kredit, der durch das Empfehlungsprogramm verdient wird
- **Promotion** – Kredit, der als Teil einer Marketingkampagne vergeben wird
- **Manuelle Anpassung** – Kredit, der direkt von einem Mitarbeiter hinzugefügt oder abgebucht wird
- **Bestellzahlung** – Geld, das am Kassenabschluss für eine Bestellung ausgegeben wird. Nicht noch in Verwendung – reserviert für den Kassenabschluss der Tasche

## Manuelle Wallet-Anpassungen

Sie können keine Mittel über das Admin-Panel hinzufügen oder entfernen — Wallet-Transaktionen werden nur von den Prozessen erstellt, die sie besitzen: Rückgaben von Bestellungen, Treueprämien und Empfehlungsprämien. Dies ist bewusst so gestaltet. Jeder Bewegung liegt eine Referenz zur Ursache zugrunde, und eine tägliche Prüfung vergleicht den Saldo jedes Wallets mit seiner eigenen Historie; manuell eingegebene Zeilen brechen diese Kette. 

Für eine Gutschrift aus gutem Willen — bei einer Dienstleistungsklage, einem Gestus nach einem Problem — geben Sie stattdessen manuell eine **Gutschein-Karte** aus (siehe das Hilfethema **Gutschein-Karten**). Eine Gutschein-Karte ist genau dafür konzipiert: Sie kontrollieren den Wert, der Kunde erhält einen Code per E-Mail und kann ihn beim Checkout genauso wie Store-Guthaben ausgeben.

## Wallet sperren

Wenn Sie einen Kunden daran hindern müssen, sein Wallet-Guthaben zu verwenden — beispielsweise während einer Betrugsuntersuchung — können Sie es deaktivieren, ohne es zu löschen oder das Guthaben zu entfernen.

1. Öffnen Sie die Detailansicht des Kunden-Wallets
2. Deaktivieren Sie den **Aktiv**-Schalter
3. Klicken Sie auf **Speichern**

Das Guthaben bleibt erhalten und das Wallet kann jederzeit wieder aktiviert werden. Während es inaktiv ist, können keine neuen Guthaben- oder Lastschriftvorgänge — manuell oder anderweitig — im Wallet gebucht werden.

## Alle Transaktionen ansehen

Für eine Gesamtansicht der Wallet-Aktivitäten navigieren Sie zu **Kunden > Wallet-Transaktionen**. Diese Liste zeigt jede Transaktion in allen Kunden-Wallets an, mit Filtern für:

- **Transaktionsart** — filtern Sie nach Guthaben, Lastschrift, Anpassung usw.
- **Quelle** — filtern Sie nach dem Ursprung der Transaktionen
- **Status** — filtern Sie nach abgeschlossen, ausstehend oder rückgängig gemacht
- **Datum** — verwenden Sie die Datenhierarchie oben, um sich in ein bestimmtes Tag, Monat oder Jahr einzuklicken

Die Transaktionsliste ist schreibgeschützt — Transaktionen können nicht in dieser Ansicht bearbeitet oder gelöscht werden.

## Tipps

- Prüfen Sie **Lebenslänglich gutgeschrieben** versus **Lebenslänglich genutzt**, um zu verstehen, wie aktiv ein Kunde sein Store-Guthaben verwendet — ein großes, nicht genutztes Guthaben kann darauf hindeuten, dass der Kunde es vergessen hat
- Wenn ein Kunde meldet, dass sein Guthaben falsch aussieht, überprüfen Sie die vollständige Transaktionshistorie, um genau zu verfolgen, wie sich das Guthaben im Laufe der Zeit verändert hat; die Spalte **Guthaben nach** in jedem Eintrag macht dies einfach
- Ein großes, nicht genutztes Guthaben lohnt sich, darauf hinzuweisen — Kunden sehen ihr Store-Guthaben auf dem Kontodashboard und beim Zahlungsschritt beim Checkout, aber eine kurze E-Mail, die darauf hinweist, verwandelt es oft in einen Auftrag
- Gefrorene Wallets behalten ihr Guthaben dauerhaft; es gibt keine Ablaufdatum — wenn Sie ein Wallet vorübergehend deaktivieren, erinnern Sie sich, es wieder zu aktivieren, sobald das Problem gelöst ist
- Die **Referenz-ID** auf jeder Transaktion verweist auf den ursprünglichen Eintrag, wodurch es einfach ist, zu überprüfen, warum eine Guthaben- oder Lastschrift angewendet wurde, ohne anderswo zu suchen