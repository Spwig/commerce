---
title: Verwaiste Warenkörbe
---

Ein verwaister Warenkorb wird erstellt, wenn ein angemeldeter Kunde Artikel in seinen Warenkorb legt, aber den Kauf innerhalb von 24 Stunden nicht abschließt. Spwig verfolgt diese Warenkörbe automatisch, damit Sie verlorene Umsätze verstehen können, Muster erkennen können, warum Kunden abbrechen, und Maßnahmen ergreifen können, um Verkäufe zurückzugewinnen.

Navigieren Sie zu **Kunden > Verwaiste Warenkörbe**, um alle aufgezeichneten Verwasten anzuzeigen.

## Was Sie in der Liste verwaister Warenkörbe sehen können

Die Listenansicht zeigt jeden verwaisten Warenkorb mit folgenden Informationen im Überblick an:

| Spalte | Beschreibung |
|---|---|
| **Kunde** | Name und E-Mail-Adresse des Kunden |
| **Verwaist am** | Datum und Uhrzeit, zu der der Warenkorb als verwaist markiert wurde |
| **Gesamtwert** | Geldwert der Artikel im Warenkorb zum Zeitpunkt des Verwaisten |
| **Gesamtartikel** | Anzahl der Artikel im Warenkorb |
| **Schätzung für den Grund** | Spwigs beste Vermutung, warum der Warenkorb verwaist wurde |
| **Wiederherstellungszustand** | Ob dieser Warenkorb wiederhergestellt wurde (in einen abgeschlossenen Auftrag umgewandelt) |
| **Tage seit Verwaisten** | Wie lange der Warenkorb bereits verwaist ist |

### Filtern verwaister Warenkörbe

Verwenden Sie die Filter auf der rechten Seite, um die Liste zu verfeinern:

- **Schätzung für den Grund** — filtern Sie nach dem Grund des Verwaisten (z. B. zeigen Sie nur Warenkörbe an, bei denen der geschätzte Grund hohe Versandkosten war)
- **Wiederhergestellt** — filtern Sie, um nur wiederhergestellte oder nicht wiederhergestellte Warenkörbe anzuzeigen
- **Verwaist am** — filtern Sie nach einem Datumsbereich, um sich auf kürzliche Verwaisten oder einen bestimmten Kampagnenzeitraum zu konzentrieren

## Verständnis der Gründe für Verwaisten

Spwig protokolliert einen geschätzten Grund für jeden Verwaisten. Diese Gründe basieren auf Signalen, die während des Kaufvorgangs erfasst werden, und sind nicht garantiert exakt, aber sie bieten einen nützlichen Ausgangspunkt, um Muster für Abbrüche zu diagnostizieren.

| Grund | Was es möglicherweise anzeigen kann |
|---|---|
| **Unbekannt** | Kein spezifisches Signal wurde erfasst — der häufigste Grund |
| **Hohe Versandkosten** | Der Kunde wurde möglicherweise von den angezeigten Versandkosten abgeschreckt |
| **Gesamtbetrag zu hoch** | Der Gesamtbetrag des Auftrags war möglicherweise höher als erwartet |
| **Kaufprobleme** | Der Kunde hatte während des Kaufvorgangs ein Problem |
| **Zahlung fehlgeschlagen** | Es wurde ein Zahlungsversuch unternommen, der aber fehlgeschlagen ist |
| **Preisvergleich** | Der Kunde hat wahrscheinlich den Preis verglichen |
| **Für später gespeichert** | Der Kunde hat absichtlich Artikel für einen zukünftigen Besuch gespeichert |

Wenn Sie eine große Anzahl von Warenkörben mit demselben Grund sehen — z. B. eine signifikante Gruppe von „Hohe Versandkosten“-Verwaisten — ist das ein Signal, das Sie in Ihren Versandeinstellungen oder bei der Darstellung des Kaufvorgangs untersuchen sollten.

## Einzelnen verwaisten Warenkorb ansehen

Klicken Sie auf eine beliebige Zeile in der Liste, um die Detailansicht zu öffnen. Sie sehen:

- **Verwaistensdetails** — der Kunde, die Warenkorbreferenz, wann der Warenkorb verwaist wurde und der geschätzte Grund
- **Warenkorbzusammenfassung** — die Anzahl der Artikel und der Gesamtwert zum Zeitpunkt des Verwaisten
- **Wiederherstellungsspur** — ob der Warenkorb wiederhergestellt wurde, wann er wiederhergestellt wurde und in welchen Auftrag er umgewandelt wurde

Das Feld **Warenkorb** verlinkt direkt auf den zugrunde liegenden Warenkorb, sodass Sie genau sehen können, welche Produkte sich im Warenkorb befanden.

## Wiederherstellungsworkflow

Spwig verfolgt, ob jeder verwaiste Warenkorb schließlich in einen abgeschlossenen Auftrag umgewandelt wird. Wenn ein Kunde zurückkehrt und einen Kauf aus einem verwaisten Warenkorb abschließt, wird der Eintrag automatisch als **Wiederhergestellt** markiert und der resultierende Auftrag wird verknüpft.

Der Zähler **Wiederherstellungsmails gesendet** zeigt an, wie viele automatisierte Wiederherstellungsmails an den Kunden für diesen Warenkorb gesendet wurden. Dies hilft Ihnen dabei, zu verstehen, ob Ihre E-Mail-Kampagnen Kunden dazu bewegen, zurückzukehren.

### Manuelle Wiederherstellungsaktionen

Die Ansicht verwaister Warenkörbe ist schreibgeschützt — es ist ein Protokoll über das, was geschehen ist, und kein Werkzeug zum Bearbeiten des Warenkorbinhalts. Um verwaiste Warenkörbe zu bearbeiten:

1.

Notieren Sie die E-Mail-Adresse des Kunden aus dem Verwaisten-Warenkorb-Protokoll
2.

Verwenden Sie Ihr E-Mail-System oder Ihre Marketingtools, um eine personalisierte Nachricht zu senden
3.

Überlegen Sie, einen Gutscheincode anzuhängen, um dem Kunden einen Anreiz zu geben, den Kauf abzuschließen
4.

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

Verfolgen Sie den **Recovered**-Status über die nächsten Tage, um festzustellen, ob die Outreach-Maßnahme Erfolg hatte

## Analysieren von Warenkorb-Abbruchtrends

Überprüfen Sie die Liste der abgebrochenen Warenkörbe regelmäßig, um den Zustand Ihres Kaufvorgangs zu beurteilen:

- Ein plötzlicher Anstieg der Abbrüche kann auf ein technisches Problem beim Checkout oder bei der Zahlung hinweisen
- Konsistent hohe Warenkorbwerte in nicht wiederhergestellten Warenkörben stellen den Segement mit den höchsten Wiederherstellungschancen dar
- Vergleichen Sie den Verhältnis von wiederhergestellten zu nicht wiederhergestellten Warenkörben im Laufe der Zeit, um die Effektivität Ihrer Wiederherstellungsmails zu messen

Der Abschnitt **Customer Analytics** im Kundenprofil zeigt auch die persönliche Abbruchrate des Warenkorbs an, sodass Sie Kunden identifizieren können, die häufig Waren in den Warenkorb legen, aber selten einen Kauf abschließen.

## Tipps

- Sortieren Sie nach **Total Value** (absteigend), um die Warenkörbe mit dem höchsten Wert zu identifizieren, die Priorität für persönliche Outreach-Maßnahmen verdienen
- Nutzen Sie den **Abandoned At**-Datumsfilter, um Abbrüche aus einem bestimmten Kampagnen- oder Werbephase zu überprüfen – ein Anstieg während eines Flash-Sales kann bedeuten, dass Ihre Werbung Besucher anzieht, die nicht unbedingt Käufer sind
- Kombinieren Sie die Daten zu abgebrochenen Warenkörben mit Gutschein-Kampagnen: Senden Sie einen zeitlich begrenzten Rabattcode an Kunden mit hochwertigen, nicht wiederhergestellten Warenkörben, um Dringlichkeit zu erzeugen
- Ein Warenkorb, der länger als 7 Tage abgebrochen wurde, wird wahrscheinlich nicht von selbst wiederhergestellt – wenn Wiederherstellungsmails aktiviert sind, sind dies die Warenkörbe, die die meisten Aufmerksamkeit benötigen
- Gastkunden erscheinen nicht in abgebrochenen Warenkörben – diese Nachverfolgung gilt nur für Kunden mit registrierten Konten