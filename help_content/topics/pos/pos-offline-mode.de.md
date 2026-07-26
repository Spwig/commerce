---
title: POS-Offline-Modus & App-Installation
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA in Ruhezustand — Hauptansicht zur Auswahl des Anmelde-/Terminal-Modus mit Spwig POS-Branding
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Screenshots von "Zu Startbildschirm hinzufügen" (iPad Safari, Android Chrome) sind OS/browser-spezifisch
         annotierte Referenzbilder. Die Sitzung, die dies erfasst, sollte Geräteemulation
         oder Referenzbilder anstelle des Versuchs, den Browser-Install-Prompt auszulösen, verwenden.
-->

Die Spwig POS ist eine Progressive Web App (PWA). Sie läuft vollständig im Browser und kann wie eine native App auf das Startbildschirm eines Geräts installiert werden. Da die App, Ihr Produktkatalog und die kürzliche Bestellhistorie lokal auf dem Gerät zwischengespeichert werden, funktioniert Ihr Kassensystem weiterhin bei kurzen Netzwerkunterbrechungen und langsamen Verbindungen.

Dieses Thema erklärt genau, was funktioniert, wenn die Verbindung unterbrochen wird, wie abgeschlossene Verkäufe synchronisiert werden, wenn die Verbindung wiederhergestellt wird, wie Sie die POS auf das Startbildschirm eines Geräts installieren und wie Updates zu installierten Geräten gelangen.

## Wie der Offline-Modus funktioniert

Wenn Sie die POS zum ersten Mal auf einem Gerät öffnen, lädt der Browser die gesamte App herunter und speichert sie lokal — ihre Oberfläche, Bilder und alle unterstützenden Code. Ein Hintergrundkomponente namens Service Worker verwaltet diesen Cache. Ab diesem Zeitpunkt lädt die App aus dem lokalen Cache, auch wenn der Server nicht erreichbar ist.

Auf dem App-Cache basierend, verwaltet die POS eine lokale Datenbank auf dem Gerät (mithilfe der eingebauten IndexedDB-Speicherung des Browsers). Diese Datenbank enthält:

- **Produkte und Varianten** — synchronisiert aus Ihrem Katalog und alle 5 Minuten aktualisiert, wenn online
- **Kategorien** — synchronisiert beim Start und gemeinsam mit Produkten aktualisiert
- **Lagerbestände** — synchronisiert alle 2 Minuten, wenn online (mit einer Netzwerk-priorisierten Strategie, die auf den zwischengespeicherten Daten zurückgreift, wenn der Server innerhalb von drei Sekunden nicht antwortet)
- **Kundendaten** — bis zu 1.000 kürzliche Kunden
- **Bestellhistorie** — eine konfigurierbare Anzahl kürzlicher POS-Bestellungen (Standard: 500 Bestellungen über 14 Tage; pro Terminal in **POS > POS-Terminals** einstellbar)
- **Produktbilder** — lokal zwischengespeichert für bis zu 24 Stunden

Wenn die POS erkennt, dass das Gerät offline ist, erscheint ein Banner am oberen Bildschirmrand: **"Offline-Modus - Verkäufe werden synchronisiert, sobald die Verbindung wiederhergestellt ist."** Der Kassensystem weiterhin mit den lokal zwischengespeicherten Daten arbeitet.

## Was offline funktioniert

| Funktion | Offline-Verfügbarkeit |
|---------|---------------------|
| Produkt-Suche und -Durchsuchung | Verfügbar — verwendet den lokal zwischengespeicherten Katalog |
| Barcode-Scanning | Verfügbar — Scans suchen nach Produkten im lokalen Cache |
| Artikel zum Warenkorb hinzufügen | Verfügbar |
| Manuelle Rabatte anwenden | Verfügbar |
| Gutschein-Code anwenden | Nicht verfügbar — Kontrolle des Kontostands erfordert eine aktive Verbindung |
| Bargeldzahlungen | Verfügbar — lokal gespeichert und für die Synchronisation in die Warteschlange gestellt |
| Kartenzahlungen (manuelle Eingabe) | Verfügbar — Kassierer verarbeitet auf einem separaten Terminal und gibt die Referenz ein; lokal gespeichert und für die Synchronisation in die Warteschlange gestellt |
| Kartenzahlungen (integrierter Leser — Stripe Terminal usw.) | Nicht verfügbar — integrierte Kartenleser kommunizieren in Echtzeit mit dem Zahlungssystem |
| Geschenkkartenzahlungen | Nicht verfügbar — Kontrolle des Kontostands erfordert eine aktive Verbindung |
| Zahlungen teilen, die Bargeld und manuelle Karte kombinieren | Verfügbar |
| Rechnungsausdruck an ein Netzwerkdrucker | Verfügbar, wenn der Drucker auf demselben lokalen Netzwerk wie das Gerät ist — Drucken erfordert keine Internetverbindung, nur lokale Netzwerkverbindung |
| Digitale Rechnungen (E-Mail/SMS/WhatsApp) | Nicht verfügbar — Versenden erfordert eine aktive Verbindung |
| Durchsuchen der Bestellhistorie | Verfügbar — zeigt zwischengespeicherte Bestellungen mit einem Banner an, der anzeigt, dass Sie offline-Daten ansehen |
| Erstattungen und Stornierungen | Nicht verfügbar — diese erfordern eine aktive Verbindung |
| Kundentreuepunkte-Abfrage | Nicht verfügbar |
| Öffnen und Schließen von Schichten | Verfügbar — Schichtstatus wird lokal gespeichert |

## Abgeschlossene Verkäufe und Synchronisation, wenn die Verbindung wiederhergestellt wird

Offline-Verkäufe gehen nicht verloren.

Wenn der Registrierungsterminal den Server nicht erreichen kann, werden alle abgeschlossenen Verkäufe in eine lokale Warteschlange (den `pendingTransactions`-Speicher in der lokalen Datenbank des Geräts) geschrieben.

Der Verkauf umfasst alle Warenkorbartikel, Mengen, Preise, Zahlungsmethode und die Zeit, zu der er abgeschlossen wurde.

Wenn die Internetverbindung wiederhergestellt wird, führt der POS automatisch Folgendes durch:

1. Er erkennt die Wiederherstellung der Verbindung über das `online`-Ereignis des Browsers
2. Zeigt eine Benachrichtigung an: **"N ausstehende Transaktion(en) werden synchronisiert..."**
3. Sendet die in der Warteschlange befindlichen Verkäufe in Reihenfolge an den Backend-Server. Falls die erste Versuch fehlschlägt, wird ein exponentieller Back-off-Wiederholungsplan verwendet (bis zu 10 Wiederholungen innerhalb eines maximalen Zeitfensters von fünf Minuten pro Versuch)
4. Markiert jeden Verkauf als synchronisiert, sobald der Backend-Server dies bestätigt

**Schutz vor Doppelverkäufen** — jedem in der Warteschlange befindlichen Verkauf wird vor dem Verlassen des Geräts eine eindeutige lokale ID zugewiesen. Der Backend-Server prüft diese ID, bevor ein Bestellung erstellt wird. Falls derselbe Verkauf zweimal abgesendet wird (z. B. weil eine Wiederholung mit einem erfolgreichen ersten Versuch überschneidet), ignoriert der Backend-Server den Duplikat. Sie werden nie doppelt gezählt.

**Konflikt erkennung** — in seltenen Fällen kann der Backend-Server einen in der Warteschlange befindlichen Verkauf als Konflikt markieren (z. B. wenn ein Produkt serverseitig gelöscht wurde, während das Gerät offline war). Konfliktverkäufe werden unter **POS > Einstellungen > Ausstehende Transaktionen** angezeigt, damit Sie sie manuell überprüfen und beheben können.

**Lageränderungen offline** werden auf die gleiche Weise behandelt: Lageränderungen, die während der Offlinezeit vorgenommen wurden, werden in eine Warteschlange gestellt und werden wiederholt, sobald die Verbindung wiederhergestellt wird. Die lokalen Lagerzahlen auf dem Gerät werden sofort aktualisiert, damit der Kassierer eine genaue (geschätzte) Anzahl sieht.

## Installation des POS auf das Startbildschirm des Geräts

Die Installation des POS auf das Startbildschirm bietet Ihnen eine Vollbild-Erfahrung ohne Browser-Adressleiste, ein Symbol auf dem Gerät und schnellere Startzeiten.

### iPad (Safari)

1. Öffnen Sie Safari und navigieren Sie zu der POS-URL Ihres Geschäfts: `https://yourstore.com/pos/`
2. Melden Sie sich an und vervollständigen Sie die erste Paarung, wenn dies ein neues Gerät ist.
3. Tippen Sie auf den **Teilen**-Button (das Quadrat mit Pfeil nach oben) in der Safari-Toolbar.
4. Scrollen Sie nach unten im Teilen-Blatt und tippen Sie auf **Zu Startbildschirm hinzufügen**.
5. Bearbeiten Sie den Namen, wenn Sie möchten (der Standardname lautet "Spwig POS") und tippen Sie auf **Hinzufügen**.

Das POS-Symbol erscheint jetzt auf Ihrem iPad-Startbildschirm. Wenn Sie darauf tippen, öffnet sich die Anwendung im Vollbildmodus ohne die Browser-Elemente von Safari.

> **Hinweis:** Für die Option "Zu Startbildschirm hinzufügen" ist Safari auf dem iPad erforderlich. Drittanbieter-Browser auf iOS (Chrome, Firefox) unterstützen die Installation von PWAs bis Mitte 2025 nicht.

### Android (Chrome)

1. Öffnen Sie Chrome und navigieren Sie zu der POS-URL Ihres Geschäfts: `https://yourstore.com/pos/`
2. Melden Sie sich an und vervollständigen Sie die Paarung, wenn nötig.
3. Tippen Sie auf den **Drei-Punkte-Menü** (oben rechts) und tippen Sie auf **App installieren** (oder **Zu Startbildschirm hinzufügen** bei älteren Chrome-Versionen).
4. Bestätigen Sie durch Tippen auf **Installieren**.

Das POS-Symbol erscheint auf dem Startbildschirm und im App-Ordner. Das Starten über das Symbol öffnet die Anwendung im standalone-Modus.

### Desktop (Chrome oder Edge)

1. Navigieren Sie zu der POS-URL Ihres Geschäfts in Chrome oder Edge.
2. Suchen Sie nach dem **Installations-Icon** in der Adressleiste des Browsers (ein Computerbildschirm mit Pfeil nach unten oder ein "+"-Icon, je nach Version).
3. Alternativ öffnen Sie das **Drei-Punkte-Menü** und wählen Sie **Spwig POS installieren** (Chrome) oder **Apps > Diese Seite als App installieren** (Edge).
4. Bestätigen Sie die Installation.

Der POS öffnet sich als eigenständiges Fenster ohne Browser-Registerkarten oder Adressleiste. Er erscheint in Ihrer System-App-Liste und kann an die Taskleiste angeheftet werden.

## Wie die App aktualisiert wird

Der POS verwaltet seine eigenen Updates über den Service Worker. Sie müssen keine App-Store besuchen oder etwas manuell herunterladen.

**Aktualisierungszyklus:**

1.

Jedes Mal, wenn Sie den POS öffnen (oder der Tab nach einer Hintergrundaktivität aktiv wird), prüft der Service Worker den Server auf eine neue Version.
2.

Wenn eine neue Version vorhanden ist, lädt der Service Worker diese im Hintergrund herunter, während Sie weiterarbeiten — Ihre aktuelle Sitzung wird nicht unterbrochen.
3.

Die Aktualisierung tritt beim nächsten Öffnen des POS in Kraft.


Wenn die App bereits geöffnet ist und eine Synchronisation aussteht, wartet der POS darauf, dass die Warteschlange leer ist, bevor er signalisiert, dass eine Neuladung bereit ist, um eine aktive Schicht mit nicht synchronisierten Verkäufen nicht zu unterbrechen.

**Was "Neuladen" bedeutet, wenn Verkäufe ausstehen** – wenn Sie einen Hinweis zum Neuladen für eine Aktualisierung sehen und Sie haben ausstehende Offline-Verkäufe, schließen Sie die aktuelle Schicht sauber ab (oder warten Sie, bis das Synchronisierungsbanner verschwindet), bevor Sie neu laden. Das Neuladen während wartender Verkäufe löscht sie nicht – sie bleiben in der lokalen Datenbank – aber es ist sicherer, zuerst zu synchronisieren, um sicherzustellen, dass sie empfangen wurden.

**Überprüfen der installierten Version** – öffnen Sie den POS, tippen Sie auf das **Menüsymbol** (drei horizontale Linien), und navigieren Sie zu **Einstellungen**. Die aktuelle Build-Version wird am unteren Rand des Einstellungspanels angezeigt.

## Speicher und Löschen der Installation

Der POS speichert mehrere Arten von Daten lokal:

| Was | Typischer Speicherbedarf |
|-----|------------------------|
| App-Shell (HTML, CSS, JS, Icons) | ~3–5 MB |
| Produktkatalog (Text und Metadaten) | 1–10 MB, abhängig von der Kataloggröße |
| Produktbilder (gespeichert) | 5–50 MB, abhängig von der Kataloggröße |
| Bestellhistorie | 1–5 MB (500 Bestellungen) |
| Kundendaten | 1–3 MB (1.000 Kunden) |
| Warteschlange für ausstehende Transaktionen | Minimal; wird bei Synchronisation gelöscht |

**Wenn das Gerät Speicherplatz knapp hat** – Browser setzen den gespeicherten Speicher unter Druck, wenn das Gerät voll ist. Der POS setzt seine Caches so weit wie möglich als persistent, wo der Browser es erlaubt, aber auf sehr vollen Geräten kann der Browser zuerst Produktbilder löschen. Wenn Bilder nicht mehr geladen werden, wird der POS sie bei der nächsten Synchronisation erneut in den Cache laden. Gesynchronisierte Verkäufe und die App-Shell sind davon nicht betroffen.

**Zurücksetzen der Installation** – wenn der POS unerwartet funktioniert (festgefahren auf einer alten Version, Katalog wird nicht aktualisiert, Synchronisation ist dauerhaft blockiert), können Sie eine saubere Neustart durchführen:

1. **Entfernen Sie die App** – auf Mobilgeräten halten Sie das POS-Symbol und wählen Sie **Entfernen** oder **Deinstallieren**. Auf dem Desktop klicken Sie mit der rechten Maustaste auf die Titelleiste des App-Fensters und wählen Sie **Deinstallieren**.
2. Öffnen Sie die POS-URL direkt im Browser und melden Sie sich erneut an.
3. Das Gerät wird erneut nach dem 8-Zeichen-Paarkode des Terminals gefragt. Sie können diesen Code in der Verwaltung unter **POS > POS-Terminals** finden oder erneut generieren – öffnen Sie den Terminal und klicken Sie auf **Paarkode erneut generieren**.
4. Ein frischer Paarcode zwingt eine vollständige Neusynchronisation aller gespeicherten Daten.

> **Nach dem Zurücksetzen**: alle Offline-Verkäufe, die vor dem Zurücksetzen in der Warteschlange standen, aber noch nicht synchronisiert wurden, gehen verloren, da die lokale Datenbank gelöscht wird. Stellen Sie immer sicher, dass die Verbindung wiederhergestellt und das Synchronisierungsbanner verschwunden ist, bevor Sie eine Installation zurücksetzen.

## Problembehandlung

### Der POS ist auf einer alten Version festgefahren

Der Service Worker hat möglicherweise die neue Version noch nicht aktiviert. Versuchen Sie, alle Browser-Registerkarten zu schließen, die den POS geöffnet haben, und öffnen Sie ihn erneut. Wenn das Problem besteht, setzen Sie die Installation wie oben beschrieben zurück.

### Das Banner "Keine Verbindung" verschwindet nicht

Überprüfen Sie, ob das Gerät außerhalb des POS-Apps Internetzugang hat (versuchen Sie, eine andere Seite zu laden). Wenn das Gerät online ist, aber das Banner weiterhin besteht:

- Der POS-Server könnte vorübergehend nicht erreichbar sein – warten Sie eine Minute, und der POS versucht automatisch erneut.
- Wenn Sie sich in einem Netzwerk befinden, das eine Anmeldeseite erfordert (captive portal), öffnen Sie ein neues Browser-Tab, vervollständigen Sie die Anmeldung und kehren Sie dann zum POS zurück.

### Ein Produkt fehlt im POS, das im Admin vorhanden ist

Der POS synchronisiert Produkte alle fünf Minuten, solange er online ist. Wenn Sie ein Produkt kürzlich im Admin hinzugefügt haben, tippen Sie auf das **Menüsymbol** und navigieren Sie zu **Einstellungen > Jetzt synchronisieren**, um eine sofortige Synchronisation auszulösen. Wenn das Produkt immer noch nicht erscheint, überprüfen Sie, ob es als **Aktiv** markiert ist und nicht in den POS-Einstellungen für die Verfügbarkeit im POS ausgeschlossen wurde.

### Ausstehende Transaktionen sind in Status "Konflikt" festgefahren

Gehen Sie zu **POS > Einstellungen** (im POS-App selbst) und überprüfen Sie das Panel **Ausstehende Transaktionen**.

Konflikttransaktionen entstehen in der Regel durch ein Produkt oder eine Preisänderung, die zwischen dem Zeitpunkt des Offline-Verkaufs und der Synchronisation stattfand.


Sie können die Verkaufsdetails ansehen und, wenn der Verkauf korrekt empfangen wurde, ihn als geprüft markieren.

## Tipps

- Führen Sie den POS auf einem dedizierten Gerät durch, das über Ihr lokales Wi-Fi-Netzwerk verbunden bleibt. Kurze Unterbrechungen des Wi-Fi-Netzwerks werden automatisch behandelt, aber ein Gerät, das lange Zeit offline ist, benötigt mehr Zeit, um sich bei der Wiederherstellung der Verbindung zu synchronisieren.
- Synchronisationsintervalle sind pro Gerät. Wenn Sie mehrere Terminals haben, synchronisiert sich jedes unabhängig. Ein Verkauf an einem Terminal erscheint sofort im Admin bei der Synchronisation, aber der lokale Bestell-Cache des anderen Terminals aktualisiert sich erst bei dessen eigenen Synchronisationszyklus.
- Vor geplanter Internetunterbrechung (z. B. bei der Bewegung zu einem Ereignis ohne Wi-Fi) öffnen Sie den POS noch, während Sie online sind, damit Katalog- und Lagerdaten vollständig aktuell sind. Bargeldverkäufe werden zuverlässig in der Warteschlange stehen; vermeiden Sie einfach integrierte Kartenzahlungen, bis Sie wieder online sind.
- Wenn Sie bei einem Ereignis nur Bargeldverkäufe benötigen, funktioniert die manuelle Kartenzahlungsmethode (Kassierer verarbeitet auf einem eigenständigen Terminal und gibt eine Referenz ein) auch offline für Kartentransaktionen.
- Halten Sie das Gerät während eines langen Schichts angeschlossen – die lokale Datenbank und der Synchronisierungsprozess beeinflussen die Batterie nicht signifikant im Vergleich zum Bildschirm, aber ein geladenes Gerät ist immer sicherer für den Handel.