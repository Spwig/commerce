---
title: Spwig Hosted Services
---

Spwig enthält drei optionale Cloud-Dienste, die Ihr Geschäft verwenden kann, ohne dass Sie etwas selbst konfigurieren oder hosten müssen: **GeoIP** ermittelt, wo sich Ihre Besucher befinden, **Geocoder** verwandelt Kundeadressen in Kartenkoordinaten, und **Push** sendet sofortige Benachrichtigungen an Ihre mobile Spwig-Admin-App. Bei der Community (kostenlos) Edition ist jedem Dienst eine großzügige monatliche Quote zugewiesen. Wenn ein Dienst seine Grenze erreicht, warnt Spwig Sie im Admin-Bereich, damit Sie entscheiden können, ob Sie vor dem Erreichen der Grenze upgraden möchten, bevor Ihre Kunden etwas bemerken.

## Die drei gehosteten Dienste

### GeoIP – Erkennung des Besucherlandes

GeoIP ermittelt das Land jedes Besuchers anhand seiner IP-Adresse. Ihr Geschäft verwendet diese Informationen, um automatisch die richtete Währung anzuzeigen, wenn ein Kunde kommt, und um das Land-Feld während des Checkouts vorzuvollständigen. Zum Beispiel sieht ein Besucher aus Deutschland Preise in Euro und ein Besucher aus Japan sieht Preise in Yen – ohne manuell auswählen zu müssen.

Jeder Seitenaufruf, bei dem GeoIP eine Abfrage durchführt, zählt gegen Ihre monatliche Quote. Wiederholte Besuche von der gleichen Browser-Sitzung verbrauchen keine Abfrage jeweils; das Ergebnis wird für die Sitzung zwischengespeichert. GeoIP-Abfragen finden nur auf dem Frontend statt, nicht in Ihrem Admin-Bereich.

### Geocoder – Adresse zu Koordinaten

Geocoder übersetzt von Kunden eingegebene Adressen in geografische Koordinaten (Breite und Länge). Ihr Geschäft verwendet diese Koordinaten zu zwei Zwecken: zur Berechnung von versandkostenbasierten Kosten, wenn Sie Abholstellen oder radiusbasierte Versandregeln haben, und zur Aktivierung der Adressvorschläge auf der Checkout-Seite, damit Kunden ihre Adresse schnell finden können.

Eine Geocoder-Abfrage wird ausgelöst, wenn ein Kunde eine Adresse auswählt oder bestätigt. Wie GeoIP werden die Ergebnisse zwischengespeichert, so dass die gleiche Adresse nur einmal pro Sitzung abgefragt wird.

### Push – Benachrichtigungen für die Admin-App

Push sendet Echtzeit-Benachrichtigungen an Ihre Spwig-Merchant-Mobil-App. Wenn eine neue Bestellung kommt, wenn der Lagerbestand unter einen Schwellenwert fällt oder wenn ein Kunde eine Nachricht sendet, sendet Push eine sofortige Benachrichtigung an Ihr Gerät, damit Sie darauf reagieren können, ohne die Admin-Oberfläche offen zu halten.

Jede Benachrichtigung, die an Ihr Gerät gesendet wird, zählt als eine Push-Anfrage gegen Ihre monatliche Quote.

## Die Community kostenlose Ausführung

Bei der Community-Ausführung von Spwig ist jeder Dienst kostenlos bis zu einer monatlichen Anfrageschranke. Die genauen Grenzen werden von Spwig festgelegt und können variieren; Ihr Admin-Dashboard zeigt immer die aktuellen Zahlen für Ihre Installation an. Bezahlte Pläne (Starter, Growth, Pro, Pro Plus) und selbstgehostete Installationen mit einer bezahlten Lizenz haben höhere Grenzen für jeden Dienst.

Wenn ein Dienst 100 % seiner Community-Quote erreicht, werden Anfragen zu diesem Dienst bis zum nächsten Kalendermonat, in dem der Zähler zurückgesetzt wird, gestoppt. Der Einfluss auf Ihr Geschäft hängt davon ab, welcher Dienst betroffen ist:

| Dienst | Was passiert bei 100 % |
|---------|----------------------|
| GeoIP | Die automatische Währungserkennung wechselt zur Standardwährung Ihres Geschäfts. Kunden können die Währung immer noch manuell ändern. |
| Geocoder | Die Adressvorschläge stoppen, Vorschläge werden nicht mehr angezeigt. Kunden können ihre Adresse immer noch manuell eingeben. Die Berechnung der Versandkosten erfolgt weiterhin mit den letzten bekannten Koordinaten. |
| Push | Neue Benachrichtigungen für die Admin-App werden in die Warteschlange gestellt, aber nicht bis zum nächsten Monat oder bis zu einem Upgrade gesendet. |

Ihr Geschäft funktioniert weiterhin normal in allen Fällen – keine Bestellungen gehen verloren und Kunden können sich weiterhin auschecken. Die Auswirkungen beschränken sich auf Bequemlichkeitsfunktionen.

## Lesen des Dashboard-Blocks

Der **Spwig-Dienstnutzungs**-Block erscheint auf der Startseite Ihres Admin-Dashboards. Er zeigt eine Fortschrittsleiste für jeden der drei Dienste an.

Jede Zeile im Block folgt dem gleichen Layout:

- **Dienstname** (links) – GeoIP, Adresssuche (Geocoder) oder Push-Benachrichtigungen.
- **Fortschrittsleiste** (Mitte) – füllt sich von links nach rechts, je mehr Nutzung.

Die Farbe der Leiste ändert sich, wenn Grenzen näher kommen:
  - **Grün** – Nutzung ist unter 80 %.

Alles läuft normal.

  - **Amber** — der Verbrauch liegt zwischen 80 % und 99 %.

Der Dienst läuft weiter, ist aber nahe am Limit.

  - **Red** — der Verbrauch hat 100 % erreicht.

Der Dienst ist jetzt für diesen Monat begrenzt.

- **Verbrauchszahlen** (rechts) — die genaue Anzahl der verwendeten Anfragen aus dem insgesamt erlaubten Umfang, z. B. `3.241 / 10.000`.

Die Bezeichnung in Klammern zeigt das Zeitfenster an, typischerweise `(dieser Monat)`.

Wenn das Kachel-Element den Spwig-Update-Server nicht erreichen kann, um Ihren aktuellen Verbrauch abzurufen (z. B. wenn Ihr Server keinen Ausgangs-Internetzugang hat), zeigt die Spalte "Verbrauch" ein Bindestrichzeichen (`—`) für diesen Dienst an. Dies bedeutet nicht, dass der Dienst defekt ist; es bedeutet nur, dass die Anzeige des Verbrauchs vorübergehend nicht verfügbar ist.

### Der Upgrade-Button

Wenn ein beliebiger Dienst 80 % oder mehr erreicht, erscheint ein **Upgrade**-Button in der rechten oberen Ecke der Kachel. Durch Klicken darauf öffnet sich die Spwig-Upgrade-Seite, auf der Sie Pläne vergleichen und Ihre Dienstgrenzen erhöhen können. Der Button verschwindet, sobald der Verbrauch unter 80 % fällt, sobald der nächste Monat beginnt.

## Der Quotenwarnbanner

Neben der Kachel auf dem Dashboard erscheint ein Banner oben auf jeder Admin-Seite, sobald ein beliebiger Dienst die 80 %-Schwelle überschreitet. Der Banner erscheint nur bei Community-Installationen.

**Amber-Banner — Grenze nähert sich (80–99 %)**

> **Grenze der gehosteten Dienste nähert sich:** Einer Ihrer Spwig-Dienste überschreitet die Community-Tier-Quota um mehr als 80 %. Upgrade, um die Grenze vor dem Erreichen zu erhöhen.

Dieser Banner ist eine Frühwarnung. Ihre Dienste laufen weiter, und Sie haben noch Zeit, zu entscheiden, ob Sie vor Ablauf des Monats ein Upgrade durchführen möchten.

**Roter Banner — Grenze erreicht (100 %)**

> **Grenze der Spwig-Dienste erreicht:** Einer Ihrer gehosteten Dienste hat die Community-Tier-Quota erreicht. Upgrade, um sie ohne Unterbrechung weiter laufen zu lassen.

Dieser Banner erscheint, sobald mindestens ein Dienst 100 % erreicht und jetzt begrenzt ist. Durch Klicken auf **Upgrade** auf einem der Banner öffnet sich dieselbe Upgrade-Seite wie durch den Button auf der Kachel.

Der Banner verschwindet automatisch am Beginn des nächsten Kalendermonats, wenn die Zähler zurückgesetzt werden, oder sofort nachdem Sie zu einem bezahlten Plan upgegradet haben.

## E-Mail-Benachrichtigung bei 90 %

Wenn ein beliebiger Dienst 90 % seiner Quote überschreitet, sendet Spwig auch eine einmalige Warn-E-Mail an die in Ihren Store-Einstellungen konfigurierte E-Mail-Adresse (**Einstellungen > Store-Einstellungen > Kontakt > Admin-E-Mail**). Die E-Mail wird pro Dienst pro Kalendermonat maximal einmal gesendet, sodass Sie nicht mit Nachrichten überflutet werden. Bei 100 % wird keine E-Mail gesendet, da der Banner im Admin-Bereich die Situation bereits klar macht.

Wenn Sie die E-Mail nicht erhalten, überprüfen Sie, ob die Admin-E-Mail-Adresse unter **Einstellungen > Store-Einstellungen** korrekt eingestellt ist.

## Ihr Plan upgraden

Wenn Sie von Community zu einem beliebigen bezahlten Plan upgraden, treten die höheren Grenzen sofort in Kraft — es ist kein Neustart des Stores oder eine Änderung der Konfiguration erforderlich. Die Dashboard-Kachel zeigt die neue, höhere Grenze beim nächsten Aktualisieren an (innerhalb von fünf Minuten).

Um zu upgraden, klicken Sie auf den **Upgrade**-Button auf der Dashboard-Kachel oder dem Quotenbanner, oder besuchen Sie die Spwig-Upgrade-Seite direkt. Bezahlte Pläne beinhalten dieselben drei gehosteten Dienste (GeoIP, Geocoder, Push) mit erhöhten monatlichen Grenzen sowie Zugriff auf die von Spwig gehostete E-Mail-Übermittlung und Prioritätsunterstützung.

## Selbsthosting und Pro-Lizenzen

Wenn Sie eine selbstgehostete Spwig-Installation mit einer bezahlten Lizenz betreiben, bestimmt Ihre Lizenzstufe Ihre Dienstgrenzen, genauso wie bei dem entsprechenden gehosteten Plan. Ihr Store benötigt weiterhin Ausgangs-Internetzugang, um `updates.spwig.com` zu erreichen, damit die Plattform Ihre Stufenkonfiguration abrufen und überprüfen kann. Die in der Dashboard-Kachel angezeigten Verbrauchszähler werden von den Endpunkten der gehosteten Dienste unter `geoip.spwig.com`, `geocoder.spwig.com` und `push.spwig.com` abgerufen.

Derzeit gibt es keine Option, GeoIP, Geocoder oder Push durch selbstgehostete Alternativen zu ersetzen — diese Dienste werden ausschließlich von der Infrastruktur von Spwig bereitgestellt und sind in allen Editionen enthalten.

## Tipps

Alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- **Prüfen Sie das Tile regelmäßig am Ende beschäftigter Monate** — ein Verkaufsevent oder eine Promotion kann die GeoIP- und Geocoder-Abfragen erheblich erhöhen.

Das Tile gibt Ihnen eine Vorbereitung, bevor Kunden beeinträchtigt werden.
- **Währungsfallback ist für die meisten Kunden unsichtbar** — wenn GeoIP seine Grenze erreicht, sehen Kunden die Standardwährung Ihres Geschäfts.

Dies ist selten ein ernstes Problem für Geschäfte, die hauptsächlich einen Markt bedienen; es spielt eher für wirklich internationale Geschäfte eine Rolle.
- **Adressvervollständigung ist eine Bequemlichkeit, nicht ein Hindernis** — wenn der Geocoder gedrosselt wird, können Kunden ihre Adresse dennoch normal eingeben und senden.

Wenn Sie häufige Promotionen durchführen, die viel Checkout-Verkehr erzeugen, erwägen Sie ein Upgrade vor beschäftigten Zeiten.
- **Drosselung verhindert nicht dauerhafte Benachrichtigungen** — gespeicherte Benachrichtigungen aus der Drosselungsperiode werden nicht rückwirkend geliefert, wenn der Monat zurücksetzt oder nach einem Upgrade erfolgt.

Wenn Sie stark auf Push-Benachrichtigungen für zeitkritische Bestellalarme angewiesen sind, sorgen Sie dafür, dass Sie vor Erreichen der Grenze ein Upgrade durchführen, um nichts zu verpassen.
- **Der 5-Minuten-Cache bedeutet, dass das Tile nicht perfekt in Echtzeit ist** — die Nutzungsdaten werden im Hintergrund ungefähr alle fünf Minuten aktualisiert.

Während ungewöhnlich hoher Verkehrszeiten kann die tatsächliche Nutzung leicht vor dem auf dem Tile angezeigten Stand liegen.
- **Legen Sie Ihre Admin-E-Mail-Adresse fest** — die 90%-Warn-E-Mail funktioniert nur, wenn **Einstellungen > Geschäftseinstellungen > Admin-E-Mail** ausgefüllt ist.

Es lohnt sich, sicherzustellen, dass dies korrekt eingestellt ist, damit Sie vor Problemen gewarnt werden.