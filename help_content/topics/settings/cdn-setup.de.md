---
title: CDN-Setup
---

Eine Content Delivery Network (CDN) speichert Kopien der Bilder, Stylesheets und Skripte Ihres Shops auf Servern weltweit. Wenn ein Kunde Ihren Shop besucht, werden diese Dateien vom Server abgerufen, der dem Kunden am nächsten ist, anstatt von Ihrem Haupt-Hosting-Server. Dies reduziert die Ladezeiten der Seite, insbesondere für Kunden, die weit entfernt von Ihrem Hosting-Server liegen.

Spwig optimiert die Auslieferung statischer Assets standardmäßig mit Brotli- und gzip-Vorverarbeitung, mit Fingerprinting von Asset-Caching und 1-Jahres-Immutable-Headers sowie korrekter Inhaltsverhandlung. Ein CDN hinzuzufügen ist optional, kann aber die Geschwindigkeit für Shops mit internationalen Kunden weiter verbessern.

## Braucht Ihr Shop ein CDN?

Nicht jeder Shop profitiert gleich stark von einem CDN. Verwenden Sie diese Leitlinien, um zu entscheiden:

**Ein CDN wird empfohlen, wenn**:
- Ihre Kunden sich über mehrere Länder oder Kontinente verteilen
- Ihr Shop viele Produktbilder oder medienreiche Seiten enthält
- Sie die schnellstmöglichen Ladezeiten weltweit möchten
- Sie in Regionen verkaufen, die weit von Ihrem Hosting-Server entfernt sind (z. B. Server in Europa, Kunden in Asien)

**Ein CDN ist wahrscheinlich unnötig, wenn**:
- Ihre Kunden hauptsächlich lokal oder im selben Land wie Ihr Server sind
- Ihr Shop einen kleinen Katalog mit wenigen Bildern hat
- Ihr Hosting-Anbieter bereits ein integriertes CDN enthält

Wenn Sie unsicher sind, schadet ein CDN der Leistung nicht. Dienste wie Cloudflare bieten kostenlose Tarife an, also gibt es keinen Kostenpunkt, um es auszuprobieren.

## Wie Spwig mit CDNs zusammenarbeitet

Spwig ist standardmäßig CDN-fähig. Sie müssen keine Code- oder Einstellungen in Ihrem Spwig-Admin-Panel ändern. Hier ist, was Spwig bereits für Sie tut:

- **Fingerprintierte statischen Dateien** -- Jede CSS-, JavaScript- und Bilddatei enthält eine eindeutige Versionshash in ihrem Dateinamen. Das bedeutet, dass CDNs diese Dateien sicher lange cachen können, ohne veraltete Inhalte auszuliefern.
- **Lange Cache-Header** -- Statische Assets werden mit 1-Jahres-Immutable-Cache-Header geliefert, die CDNs und Browser auffordern, sie aggressiv zu cachen.
- **Vorverarbeitete Dateien** -- Spwig verarbeitet Assets mit Brotli und gzip, sodass Ihr CDN kleinere Dateien liefern kann, ohne zusätzliche Verarbeitung.
- **Korrekte Inhaltsverhandlung** -- Spwig sendet die richtigen Content-Type- und Kodierungsheader, auf die CDNs für korrektes Caching angewiesen sind.

Alles, was Sie tun müssen, ist, die DNS-Einstellungen Ihres Domains auf den CDN-Anbieter zu verweisen, und alles funktioniert automatisch.

## Cloudflare einrichten

Cloudflare ist der beliebteste CDN und bietet einen kostenlosen Tarif, der für die meisten Shops gut funktioniert. Folgen Sie diesen Schritten:

**Schritt 1: Erstellen Sie ein Cloudflare-Konto**
- Besuchen Sie cloudflare.com und melden Sie sich für ein kostenloses Konto an

**Schritt 2: Fügen Sie Ihren Domain hinzu**
- Klicken Sie auf **Add a Site** und geben Sie den Namen Ihres Shops ein
- Wählen Sie den **Free**-Plan (ausreichend für die meisten Shops)

**Schritt 3: Aktualisieren Sie Ihre DNS-Nameserver**
- Cloudflare zeigt Ihnen zwei Nameserver an (z. B. `anna.ns.cloudflare.com`)
- Melden Sie sich bei Ihrem Domain-Registrierer (wo Sie Ihren Domain gekauft haben)
- Ersetzen Sie Ihre aktuellen Nameserver durch die Cloudflare-Nameserver
- DNS-Änderungen können bis zu 24 Stunden dauern, bis sie wirksam sind

**Schritt 4: Konfigurieren Sie SSL/TLS**
- Im Cloudflare-Dashboard navigieren Sie zu **SSL/TLS**
- Stellen Sie den Verschlüsselungsmodus auf **Full (strict)**
- Dies stellt sicher, dass alle Daten zwischen Cloudflare und Ihrem Server verschlüsselt bleiben

**Schritt 5: Überprüfen Sie, ob es funktioniert**
- Sobald die DNS-Änderungen propagiert sind, besuchen Sie Ihren Shop und prüfen Sie den `cf-cache-status`-Header in Ihrem Browser (siehe unten: Ihr CDN überprüfen)

## AWS CloudFront einrichten

Wenn Sie bereits Amazon Web Services verwenden, integriert sich CloudFront natürlich in Ihre Infrastruktur:

1. Öffnen Sie die **CloudFront**-Konsole in Ihrem AWS-Konto
2. Erstellen Sie eine neue **Distribution** mit dem Domain Ihres Shops als Ursprung
3. Stellen Sie die **Origin Protocol Policy** auf "HTTPS Only"
4. Unter **Cache Behavior** setzen Sie die **Cache Policy** auf "CachingOptimized" für statische Assets
5. Fügen Sie den Domain Ihres Shops als **Alternate Domain Name (CNAME)** hinzu
6. Fügen Sie ein SSL-Zertifikat aus AWS Certificate Manager an
7. Aktualisieren Sie die DNS-Einstellungen Ihres Domains, um auf die CloudFront-Distribution-URL zu verweisen


Die CloudFront-Preise sind nutzungsabhängig.

Für die meisten Stores sind die Kosten minimal, da die von Spwig abgezeichneten Assets über lange Zeiträume im Cache gespeichert werden.

## Empfohlene CDN-Einstellungen

Für die besten Ergebnisse konfigurieren Sie Ihr CDN so, dass es den richtigen Inhalt caches und den Rest überspringt.

**Was zu cache** (statische Assets):
- `/static/` -- Alle Stylesheets, Skripte, Schriften und Theme-Assets
- `/media/` -- Produktbilder und hochgeladene Mediendateien
- Bilddateien (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Schriftdateien (`.woff`, `.woff2`)

**Was nicht zu cache** (dynamische Seiten):
- `/admin/` -- Der Admin-Bereich muss immer frischen Inhalt liefern
- `/cart/` -- Warenkorbseiten enthalten sessionspezifische Daten
- `/checkout/` -- Checkout-Seiten dürfen niemals gecacht werden, aus Sicherheitsgründen
- `/accounts/` -- Kundenseiten enthalten private Daten
- Jede Seite, die eine Anmeldung erfordert oder personalisierten Inhalt anzeigt

**Allgemeine Caching-Regeln**:
- **Respect origin cache headers** -- Spwig sendet die richtigen cache-control-Header für jeden Inhaltstyp. Konfigurieren Sie Ihr CDN, um diese Header zu beachten, anstatt sie zu überschreiben.
- **Enable Brotli compression** -- Sowohl Cloudflare als auch CloudFront unterstützen Brotli. Aktivieren Sie es, um von Spwig vorab komprimierten Assets zu profitieren.
- **Set Browser Cache TTL to "Respect Existing Headers"** -- Dies ermöglicht es der eingebauten Cachepolitik von Spwig, das Verhalten zu steuern.

## Verifying Your CDN

Nach der Einrichtung bestätigen Sie, dass das CDN Ihren Inhalt korrekt bereitstellt:

**Step 1: Open Browser Developer Tools**
- In Chrome oder Firefox drücken Sie **F12**, um die Entwicklertools zu öffnen
- Klicken Sie auf den **Network**-Tab

**Step 2: Load Your Store**
- Besuchen Sie die Startseite Ihres Stores mit den Entwicklertools geöffnet
- Klicken Sie auf eine Anfrage zu einer statischen Datei (z. B. eine `.css`- oder `.js`-Datei)

**Step 3: Check the Response Headers**
- **Cloudflare**: Suchen Sie nach dem Header `cf-cache-status`. Ein Wert von `HIT` bedeutet, dass die Datei vom CDN-Cache bereitgestellt wurde. `MISS` bedeutet, dass sie von Ihrem Server abgerufen wurde (nur bei der ersten Anfrage).
- **CloudFront**: Suchen Sie nach dem Header `x-cache`. Ein Wert von `Hit from cloudfront` bestätigt die Lieferung über das CDN.

**Step 4: Test from Another Location**
- Verwenden Sie ein kostenloses Tool wie gtmetrix.com oder webpagetest.org, um Ihren Store von verschiedenen geografischen Standorten zu testen
- Vergleichen Sie die Ladezeiten vor und nach der Einrichtung des CDN

## Common Issues

### Stale Content After Theme Changes

**Problem**: Nachdem Sie Ihr Theme aktualisiert oder Designänderungen vorgenommen haben, sehen Kunden weiterhin die alte Version.

**Solution**: Löschen Sie den CDN-Cache. In Cloudflare gehen Sie zu **Caching > Configuration > Purge Everything**. In CloudFront erstellen Sie eine **Invalidation** für `/*`. Beachten Sie, dass Spwig's abgezeichnete Assets normalerweise dieses Problem verhindern, da aktualisierte Dateien automatisch neue Dateinamen erhalten. Dieses Problem betrifft am häufigsten nicht-abgezeichnete Assets wie benutzerdefinierte Uploads.

---

### Mixed Content Warnings

**Problem**: Ihr Browser zeigt nach Aktivierung des CDN eine Sicherheitswarnung zu "mixed content" an.

**Solution**: Stellen Sie sicher, dass der SSL-Modus Ihres CDN auf **Full (strict)** gesetzt ist, nicht auf "Flexible". Der Flexible-Modus kann dazu führen, dass Ihr Server HTTP-Anfragen anstelle von HTTPS empfängt, was zu Warnungen vor gemischtem Inhalt führt. In Cloudflare prüfen Sie **SSL/TLS > Overview** und bestätigen Sie den Modus.

---

### Admin Panel Running Slowly

**Problem**: Der Admin-Bereich fühlt sich nach Hinzufügen eines CDN langsamer an.

**Solution**: CDNs sollten Admin-Seiten nicht cachen. Erstellen Sie eine **Page Rule** (Cloudflare) oder **Cache Behavior** (CloudFront), die das Caching auf "Bypass" setzt, für jede URL, die `/admin/*` entspricht. Dies stellt sicher, dass Admin-Anfragen direkt an Ihren Server weitergeleitet werden, ohne CDN-Überhead.

---

### Images Not Loading

**Problem**: Produktbilder oder Mediendateien geben nach Einrichtung des CDN Fehler zurück.

**Solution**: Stellen Sie sicher, dass der Ursprung Ihres CDN mit dem richtigen Protokoll (HTTPS) und Port konfiguriert ist. Prüfen Sie auch, ob Ihre Serverfeuerwall Verbindungen von den IP-Adressbereichen des CDN erlaubt.

## Tips

Behalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe bei.

- **Beginnen Sie mit dem kostenlosen Tarif von Cloudflare** -- Er deckt die Anforderungen der meisten Geschäfte ab und benötigt nur Minuten zur Einrichtung
- **Verwenden Sie immer den vollständigen (strengen) SSL-Modus** -- Der flexible Modus erzeugt Sicherheitslücken und kann den Kaufablauf unterbrechen
- **Löschen Sie Ihren CDN-Cache nach großen Theme-Updates** -- Obwohl die von Spwig mit Fingerprint versehenen Dateien die meisten Fälle abdecken, stellt ein vollständiges Cache-Verzeichnis sicher, dass keine veralteten Inhalte übrig bleiben
- **Cachen Sie keine Checkout- oder Warenkorbseiten** -- Das Cachen dieser Seiten kann die Daten eines Kunden einem anderen Kunden ausliefern
- **Testen Sie aus der Perspektive Ihrer Kunden** -- Verwenden Sie kostenlose Tools wie webpagetest.org, um die tatsächliche Leistung aus den Regionen zu messen, in denen Ihre Kunden einkaufen
- **Überwachen Sie Ihre CDN-Analysen** -- Sowohl Cloudflare als auch CloudFront bieten Dashboards an, die Cache-Trefferquoten, gespeicherte Bandbreite und den Verkehr nach Land anzeigen
- **Halten Sie die DNS-TTL während der Einrichtung niedrig** -- Stellen Sie die DNS-TTL auf 300 Sekunden (5 Minuten) ein, während Sie zu einem CDN wechseln, und erhöhen Sie sie anschließend, sobald alles bestätigt ist
- **Ein CDN ersetzt keine gute Webhosting-Plattform** -- Ihr Ursprungsserver ist dennoch wichtig für dynamische Seiten wie Checkout, Warenkorb und Admin.

Wählen Sie eine qualitativ hochwertige Webhosting-Plattform neben einem CDN