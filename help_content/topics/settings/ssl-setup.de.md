---
title: SSL-Setup
---

SSL (Secure Sockets Layer) verschlüsselt die Verbindung zwischen den Browsern Ihrer Kunden und Ihrem Geschäft. Wenn SSL aktiv ist, beginnt die URL Ihres Geschäfts mit `https://` und Browser zeigen ein Schlosssymbol an. SSL ist für die Akzeptanz von Zahlungen, den Schutz von Kundendaten und eine gute Platzierung in Suchmaschinen unerlässlich.

Spwig unterstützt mehrere SSL-Modi, die verschiedenen Hosting-Setup-Anforderungen entsprechen. Dieser Leitfaden erklärt jeden Modus und hilft Ihnen, den richtigen auszuwählen.

## SSL-Modus auswählen

| Modus | Bestens geeignet für | Kosten des Zertifikats | Verlängerung |
|------|----------|-----------------|---------|
| **Let's Encrypt** | Die meisten Geschäfte | Kostenlos | Automatisch |
| **Cloudflare Origin CA** | Geschäfte, die Cloudflare-Proxy verwenden | Kostenlos | Manuel (bis zu 15 Jahre) |
| **Benutzerdefiniertes Zertifikat** | Geschäfte mit gekauften Zertifikaten | Variiert | Manuel |
| **Extern verwaltet** | Lastbalancer, Cloudflare Flexible | N/A | N/A |
| **Selbstsigniert** | Entwicklung und Test | Kostenlos | Manuel |
| **Kein (HTTP)** | Nur lokale Entwicklung | N/A | N/A |

Wenn Sie unsicher sind, welchen Modus Sie verwenden sollen, ist **Let's Encrypt** die beste Wahl für die meisten Geschäfte. Es ist kostenlos, automatisch und von allen Browsern vertraut.

## Let's Encrypt

Let's Encrypt bietet kostenlose, vertrauenswürdige SSL-Zertifikate, die sich alle 60-90 Tage automatisch erneuern. Dies ist die empfohlene Option für die meisten Händler.

**Voraussetzungen:**
- Ihre Domain muss auf Ihren Server zeigen (A-Record in DNS)
- Port 80 muss von Internet zugänglich sein (für Zertifikatsverifikation)
- Eine E-Mail-Adresse für Benachrichtigungen bei Ablauf des Zertifikats

**Einrichtungsschritte:**
1. Gehen Sie zu **Einstellungen > Site-Einstellungen** und öffnen Sie den Reiter **Domain & SSL**
2. Geben Sie Ihren Domain-Namen ein
3. Wählen Sie **Let's Encrypt**
4. Geben Sie Ihre Admin-E-Mail-Adresse ein
5. Klicken Sie auf **Konfiguration anwenden**

Spwig übernimmt den Rest automatisch: Ihre Domain wird überprüft, das Zertifikat wird abgerufen, NGINX wird konfiguriert und die automatische Erneuerung wird eingerichtet.

## Cloudflare Origin CA

Cloudflare Origin CA-Zertifikate verschlüsseln die Verbindung zwischen Cloudflare's Edge-Servern und Ihrem Geschäft. Diese Zertifikate sind kostenlos und können bis zu 15 Jahre gültig sein, aber sie werden **nur von Cloudflare vertraut** – Browser, die direkt auf Ihren Server zugreifen, erhalten eine Zertifikatwarnung.

Dieser Modus ist ideal, wenn Sie Cloudflare als Proxy (orangenes Cloud-Icon aktiviert) für Ihre Domain verwenden. Cloudflare zeigt Besuchern ihr eigenes vertrauenswürdiges Zertifikat, und das Origin CA-Zertifikat sichert die Verbindung zwischen Cloudflare und Ihrem Server.

**Voraussetzungen:**
- Ein Cloudflare-Konto mit Ihrer Domain hinzugefügt
- Ein Origin CA-Zertifikat und ein privater Schlüssel, die über das Cloudflare-Dashboard generiert wurden
- Cloudflare SSL/TLS-Modus auf **Full (Strict)** gesetzt

**Erstellen des Origin CA-Zertifikats:**
1. Melden Sie sich bei Ihrem Cloudflare-Dashboard an
2. Wählen Sie Ihre Domain aus
3. Gehen Sie zu **SSL/TLS > Origin Server**
4. Klicken Sie auf **Zertifikat erstellen**
5. Wählen Sie RSA oder ECC (RSA ist am kompatibelsten)
6. Fügen Sie Ihre Domain hinzu (z. B. `example.com` und `*.example.com`)
7. Wählen Sie eine Gültigkeitsdauer (15 Jahre wird empfohlen)
8. Klicken Sie auf **Erstellen** und kopieren Sie sowohl das Zertifikat als auch den privaten Schlüssel

**Einrichten in Spwig:**
1. Gehen Sie zu **Einstellungen > Site-Einstellungen** und öffnen Sie den Reiter **Domain & SSL**
2. Geben Sie Ihren Domain-Namen ein
3. Wählen Sie **Cloudflare Origin CA**
4. Fügen Sie das Zertifikat in das Feld **Zertifikat (PEM)** ein
5. Fügen Sie den privaten Schlüssel in das Feld **Privater Schlüssel (PEM)** ein
6. Klicken Sie auf **Konfiguration anwenden**

**Nach der Konfiguration:**
- In Cloudflare den SSL/TLS-Modus auf **Full (Strict)** setzen
- Cloudflare-Proxy (orangenes Cloud-Icon) für den DNS-Record Ihrer Domain aktivieren
- Ihr Geschäft wird über HTTPS mit Cloudflare's vertrauenswürdigem Zertifikat zugänglich sein

## Benutzerdefiniertes Zertifikat

Verwenden Sie diesen Modus, wenn Sie ein SSL-Zertifikat von einem Zertifizierungsstellen (CA) wie DigiCert, Sectigo oder GoDaddy gekauft haben, oder wenn Ihr Hosting-Anbieter eines für Sie ausgestellt hat.

**Einrichtungsschritte:**
1.

Gehen Sie zu **Einstellungen > Site-Einstellungen** und öffnen Sie den Reiter **Domain & SSL**
2.

Geben Sie Ihren Domain-Namen ein
3.

Wählen Sie **Benutzerdefiniertes Zertifikat**
4.

Beachten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe.

Fügen Sie Ihre Zertifikatskette (einschließlich Zwischenzertifikaten) in das Feld **Zertifikat (PEM)** ein
5.

Fügen Sie Ihren privaten Schlüssel in das Feld **Privater Schlüssel (PEM)** ein
6.

Klicken Sie auf **Konfiguration anwenden**

Ihr Zertifikat sollte die vollständige Kette enthalten: Ihr Domain-Zertifikat gefolgt von allen Zwischenzertifikaten. Der private Schlüssel sollte im PEM-Format vorliegen (mit `-----BEGIN PRIVATE KEY-----` oder `-----BEGIN RSA PRIVATE KEY-----` beginnen).

## Extern verwaltet

Wählen Sie diesen Modus aus, wenn das SSL-Verkehrsaufbau durch einen externen Dienst vor dem Erreichen Ihres Servers beendet wird. In dieser Konfiguration erhält Ihr Server nur unverschlüsselten HTTP-Verkehr – auf dem Server selbst ist kein Zertifikat installiert.

**Typische Szenarien:**
- **Cloudflare Flexible SSL** – Cloudflare verschlüsselt den Verkehr von Browser zu Cloudflare, sendet aber HTTP an Ihren Server
- **Cloud-Lastausgleich** – AWS ALB, Google Cloud Load Balancer oder DigitalOcean Load Balancer beendet SSL und leitet HTTP weiter
- **Reverse-Proxy** – Ein weiterer Server vor Spwig verwaltet SSL

**Einrichtungsschritte:**
1. Gehen Sie zu **Einstellungen > Site-Einstellungen** und öffnen Sie den Reiter **Domain & SSL**
2. Geben Sie Ihren Domain-Namen ein
3. Wählen Sie **Extern verwaltet**
4. Klicken Sie auf **Konfiguration anwenden**

Spwig konfiguriert NGINX, um nur HTTP zu bereitstellen und vertraut auf den `X-Forwarded-Proto`-Header von Ihrem Proxy, um Besucher mit HTTPS korrekt zu erkennen.

## Selbstsigniertes Zertifikat

Selbstsignierte Zertifikate verschlüsseln die Verbindung, werden aber von Browsern nicht als vertrauenswürdig angesehen. Besucher erhalten eine Sicherheitswarnung, die sie manuell umgehen müssen. Dieser Modus ist nur für Entwicklungsserver und interne Tests geeignet.

**Einrichtungsschritte:**
1. Gehen Sie zu **Einstellungen > Site-Einstellungen** und öffnen Sie den Reiter **Domain & SSL**
2. Geben Sie Ihren Domain-Namen ein
3. Wählen Sie **Selbstsigniert**
4. Klicken Sie auf **Konfiguration anwenden**

Spwig generiert ein selbstsigniertes Zertifikat automatisch. Verwenden Sie diesen Modus nicht für einen Produktions-Shop.

## Problembehandlung

**Zertifikat funktioniert nicht nach der Konfiguration:**
- Stellen Sie sicher, dass der A-Record Ihres Domains auf die IP-Adresse Ihres Servers zeigt
- Stellen Sie sicher, dass die Ports 80 und 443 in Ihrem Firewall-Regelwerk geöffnet sind
- Warten Sie einige Minuten, bis DNS-Änderungen wirksam werden

**Let's Encrypt kann kein Zertifikat ausstellen:**
- Stellen Sie sicher, dass Ihr Domain auf die IP-Adresse dieses Servers verweist
- Stellen Sie sicher, dass Port 80 nicht durch einen Firewall blockiert ist
- Wenn Sie hinter Cloudflare sind, setzen Sie temporär die DNS-Einstellungen auf "DNS only" (grauer Cloud) während der Zertifikatsausstellung

**Cloudflare zeigt "Fehler 526" (Ungültiges SSL-Zertifikat):**
- Stellen Sie sicher, dass Sie den Modus **Cloudflare Origin CA** ausgewählt haben (nicht "Extern verwaltet")
- Stellen Sie sicher, dass der SSL/TLS-Modus in Cloudflare auf **Full (Strict)** gesetzt ist
- Stellen Sie sicher, dass das Origin CA-Zertifikat nicht abgelaufen ist

**Browser zeigt "Nicht sicher" an, obwohl SSL vorhanden ist:**
- Einige Seiten laden Bilder oder Skripte über HTTP (gemischter Inhalt). Prüfen Sie die Entwicklerkonsole Ihres Browsers auf Warnungen zu gemischtem Inhalt.
- Stellen Sie sicher, dass die Site-URL in den Einstellungen `https://` verwendet