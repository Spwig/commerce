---
title: Kundengruppen
---

Kundengruppen ermöglichen es Ihnen, Ihre Kunden automatisch in sinnvolle Gruppen einzuteilen, basierend auf ihrem Kaufverhalten. Sobald Kunden in Gruppen eingeteilt sind, können Sie diese Gruppen nutzen, um Ihre Marketingbemühungen zu fokussieren – beispielsweise, um Loyalitätsprämien an VIP-Kunden anzubieten oder Wiederherstellungskampagnen an Kunden zu senden, die seit geraumer Zeit nicht mehr gekauft haben.

Spwig bewertet die Kriterien der Kundengruppen anhand der Metriken jedes Kunden und weist sie der Gruppe mit der höchsten Priorität zu, für die sie qualifiziert sind. Dies geschieht automatisch, sobald sich Kundendaten aktualisieren.

## Verfügbare Kundengruppentypen

Spwig verfügt über eine Reihe eingebauter Kundengruppentypen. Jeder Kundengruppentyp hat einen festen internen Bezeichner, doch Sie können den Anzeigename, die Beschreibung, die Kriterien und die Farbe anpassen, um sie so darzustellen, wie Sie Ihre Kunden einstufen.

| Kundengruppentyp | Typische Verwendung |
|---|---|
| **Gastkunde** | Kunden, die ohne Erstellung eines Kontos ausgecheckt haben |
| **Neukunde** | Kunden, die kürzlich ihren ersten Kauf getätigt haben |
| **Regelmäßiger Kunde** | Kunden mit einer stabilen Kaufhistorie |
| **Häufiger Käufer** | Kunden, die häufig einkaufen (kurze Zeit zwischen Bestellungen) |
| **Hochwertiger Kunde** | Kunden mit hohem Gesamtausgaben |
| **VIP-Kunde** | Ihre wertvollsten und loyalsten Kunden |
| **Preisjäger** | Kunden, die tendenziell während Verkäufen einkaufen |
| **In Gefahr** | Kunden, die seit geraumer Zeit nicht mehr gekauft haben |
| **Inaktiv** | Kunden, die seit einer langen Zeit nicht mehr aktiv sind |

## Verständnis der Kundengruppenkriterien

Jede Kundengruppe wird durch eine Kombination von Kriterien definiert. Spwig prüft diese anhand der gespeicherten Metriken jedes Kunden. Alle Kriterien innerhalb einer Kundengruppe werden kombiniert – ein Kunde muss alle festgelegten Bedingungen erfüllen, um qualifiziert zu sein.

### Ausgabenkriterien

- **Mindestgesamtausgaben** – der Kunde muss mindestens diesen Betrag an allen abgeschlossenen Bestellungen ausgegeben haben
- **Maximaler Gesamtausgaben** – der Kunde darf nicht mehr als diesen Betrag ausgegeben haben

Verwenden Sie einen Ausgabenbereich, um eine bestimmte Stufe zu identifizieren. Zum Beispiel würde das Festlegen von Mindestwert auf 500 $ und Maximalwert auf 2.000 $ mittelständige Kunden adressieren.

### Bestellanzahlkriterien

- **Mindestbestellungen** – der Kunde muss mindestens diese Anzahl an abgeschlossenen Bestellungen haben
- **Maximalbestellungen** – der Kunde darf nicht mehr als diese Anzahl an abgeschlossenen Bestellungen haben

Die Kombination von Mindestbestellungen mit einem Ausgabenminimum ist eine zuverlässige Methode, um VIP-Kunden zu definieren: sie kaufen häufig *und* geben großzügig aus.

### Aktualitätskriterien

- **Mindesttage seit letztem Kauf** – die letzte Bestellung des Kunden muss mindestens so viele Tage zurückliegen
- **Maximaltage seit letztem Kauf** – die letzte Bestellung des Kunden muss innerhalb dieser Anzahl an Tagen liegen

Aktualitätskriterien sind für die Gruppen *In Gefahr* und *Inaktiv* entscheidend. Zum Beispiel würde das Festlegen von Mindesttagen auf 90 und Maximaltagen auf 365 Kunden identifizieren, die stillgelegt wurden, aber nicht vollständig verloren gegangen sind.

## Kundengruppenpriorität

Wenn ein Kunde für mehr als eine Kundengruppe qualifiziert ist, gewinnt die Kundengruppe mit dem **höchsten Prioritätswert**. Sie können die Priorität für jede Kundengruppe in der **Anzeige-Einstellungen**-Sektion des Kundengruppenformulars festlegen.

Die Kundengruppe **Gastkunde** wird immer zuerst bewertet, unabhängig von der Prioritätsreihenfolge, da der Gaststatus durch den Kontotyp und nicht durch Kaufkriterien bestimmt wird.

## Anzeigen und Verwalten von Kundengruppen

Navigieren Sie zu **Kunden > Kundengruppen**, um alle konfigurierten Kundengruppen anzuzeigen. Die Liste zeigt den Anzeigennamen, den internen Typ, die zugewiesene Farbe, die Priorität, die aktuelle Anzahl der passenden Kunden und ob die Kundengruppe aktiv ist.

![Liste der Kundengruppen](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Erstellen oder Bearbeiten einer Kundengruppe

1.

Navigieren Sie zu **Kunden > Kundengruppen**
2.

Klicken Sie auf eine vorhandene Kundengruppe, um sie zu bearbeiten, oder klicken Sie auf **+ Kundengruppe hinzufügen**, um eine neue zu erstellen
3.

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

Füllen Sie den Reiter **Segmentinformationen** aus:
   - **Name** — wählen Sie den internen Segmenttyp aus dem Dropdown-Menü aus
   - **Anzeigename** — der für Menschen lesbare Name, der im Admin-Panel angezeigt wird (z. B. "VIP-Kunden")
   - **Beschreibung** — eine kurze interne Notiz, die erklärt, was dieses Segment darstellt
4.

Legen Sie Kriterien in den relevanten Reitern fest:
   - **Kriterien - Ausgaben** — Mindest- und Höchstwert der Gesamtausgaben
   - **Kriterien - Bestellungen** — Mindest- und Höchstwert der Bestellanzahl
   - **Kriterien - Aktualität** — Mindest- und Höchstwert der Tage seit dem letzten Kauf
5.

Konfigurieren Sie **Anzeigestellungen**:
   - **Farbe** — eine Hex-Farbe, die verwendet wird, um dieses Segment in Listen visuell zu identifizieren
   - **Priorität** — eine höhere Zahl bedeutet, dass dieses Segment zuerst bewertet wird
   - **Aktiv** — deaktivieren Sie das Segment, um es zu deaktivieren, ohne es zu löschen
6.

Klicken Sie auf **Speichern**, um die Änderungen anzuwenden

### Beispiel: Konfigurieren eines VIP-Segments

Hier ist ein realistisches Beispiel für ein hochwertiges VIP-Segment:

| Feld | Wert |
|---|---|
| Name | `vip` |
| Anzeigename | VIP-Kunden |
| Mindestgesamtausgaben | $1.000 |
| Mindestbestellungen | 5 |
| Maximaler Tage seit letztem Kauf | 180 |
| Priorität | 90 |
| Farbe | `#FFD700` |

Das bedeutet: Ein Kunde qualifiziert sich als VIP, wenn er mindestens $1.000 ausgegeben hat, mindestens 5 Bestellungen aufgegeben hat und innerhalb der letzten 6 Monate einen Kauf getätigt hat.

### Beispiel: Konfigurieren eines Risikosegments

| Feld | Wert |
|---|---|
| Name | `at_risk` |
| Anzeigename | Risikosegment |
| Mindesttage seit letztem Kauf | 60 |
| Höchsttage seit letztem Kauf | 180 |
| Priorität | 30 |
| Farbe | `#FF6B35` |

## Verwenden von Segmenten für gezielte Marketingkampagnen

Segments werden auf Kundenprofilen im gesamten Admin-Panel angezeigt, sodass Ihr Team sofort weiß, zu welcher Kategorie jeder Kunde gehört. Nutzen Sie diese Informationen, um:

- **Gezielte Gutschein-Kampagnen** durchzuführen — erstellen Sie Gutscheine, die nur für Kunden in einem bestimmten Segment gelten, und verwenden Sie Ihr E-Mail-System, um sie nur an diese Gruppe zu senden
- **Unterstützung priorisieren** — markieren Sie VIP- oder hochwertige Kunden, damit Ihr Team priorisierte Unterstützung anbieten kann
- **Wiederherstellung planen** — überprüfen Sie regelmäßig die Segmente Risikosegment und Inaktive Kunden, um Kunden zu identifizieren, die eine Wiederherstellungsmail oder ein besonderes Angebot benötigen
- **Marketingausgaben anpassen** — konzentrieren Sie den Akquise-Budget auf Kanäle, die hochwertige Kunden anziehen, indem Sie analysieren, welche Kohorten in diese Segmente konvertieren

## Tipps

- Beginnen Sie mit den integrierten Segmenttypen, bevor Sie benutzerdefinierte Kriterien erstellen — sie decken die häufigsten Segmentierungsbedürfnisse ab
- Überprüfen Sie regelmäßig die Anzahl der Kunden in jedem Segment; ein VIP-Segment mit null Kunden oder ein Risikosegment, das sich schnell vergrößert, sind beide wert, untersucht zu werden
- Verwenden Sie das Feld **Priorität** bewusst — wenn sich Ihre Kriterien zwischen Segmenten überschneiden (z. B. ein Kunde qualifiziert sich für beide Stammkunden und Hochwertige), gewinnt das Segment mit der höheren Priorität
- Deaktivieren Sie Segmente, die Sie derzeit nicht verwenden, anstatt sie zu löschen — Sie können sie später ohne erneute Konfiguration der Kriterien wieder aktivieren
- Segmentkriterien werden gegen gespeicherte Kundendaten geprüft, die automatisch neu berechnet werden. Wenn die Segmentzahlen veraltet wirken, können die Metriken aus dem Abschnitt Kundendaten im Admin-Panel neu berechnet werden