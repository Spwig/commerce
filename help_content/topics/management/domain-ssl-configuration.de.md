---
title: Domain & SSL-Konfiguration
---

Dieser Leitfaden erklärt, wie Sie einen benutzerdefinierten Domain-Namen mit Ihrem Spwig-Shop verbinden und SSL-Zertifikate für sicheren HTTPS-Zugriff einrichten. Sie können eine Domain während der Installation konfigurieren oder sie später hinzufügen.

## Domain nach der Installation hinzufügen

Wenn Sie Spwig ohne Domain (mithilfe der Server-IP-Adresse) installiert haben, können Sie eine Domain jederzeit hinzufügen.

### Schritt 1: DNS einrichten

Mit Ihrem Domain-Registrierer oder DNS-Anbieter:

1. Erstellen Sie einen **A-Record**, der Ihren Domain-Namen (oder Subdomain) auf die IP-Adresse Ihres Servers verweist
2. Wenn Sie eine Subdomain wie `shop.example.com` verwenden, erstellen Sie den A-Record für `shop`
3. Warten Sie auf die DNS-Verbreitung — dies dauert in der Regel 5–60 Minuten

Überprüfen Sie, ob der DNS-Record funktioniert:

```bash
 dig +short shop.example.com
```

Dies sollte die IP-Adresse Ihres Servers zurückgeben.

### Schritt 2: Domain-Konfigurations-Skript ausführen

SSH-Verbindung zu Ihrem Server herstellen und in das Verzeichnis Ihrer Spwig-Installation wechseln:

```bash
 ./configure-domain.sh
```

Das Skript führt Folgendes aus:

1. Fragt nach Ihrem Domain-Namen
2. Überprüft, ob der DNS-Record auf Ihren Server verweist
3. Aktualisiert die Konfiguration des Shops
4. Holt ein kostenloses SSL-Zertifikat von Let's Encrypt
5. Konfiguriert den Webserver, um HTTPS zu verwenden
6. Startet die relevanten Dienste neu

Ihr Shop ist nun unter `https://yourdomain.com` erreichbar.

### Schritt 3: Shop-Einstellungen aktualisieren

Nachdem Sie eine Domain hinzugefügt haben, melden Sie sich in Ihrem Admin-Panel an und navigieren Sie zu **Store Settings**. Stellen Sie sicher, dass der **Store URL** mit Ihrer neuen Domain übereinstimmt. Dies stellt sicher, dass E-Mails, Rechnungen und Links die richtige Adresse verwenden.

## SSL-Zertifikate

### Automatisches SSL (Let's Encrypt)

In **standalone-Modus** ruft der Installer automatisch ein kostenloses SSL-Zertifikat von Let's Encrypt ab. Diese Zertifikate:

- Werden von allen großen Browsern als vertrauenswürdig angesehen
- Sind für 90 Tage gültig
- Werden automatisch erneuert — eine Erneuerungsprüfung wird täglich durchgeführt, und Zertifikate werden erneuert, wenn sie weniger als 30 Tage gültig sind
- Decken Ihren genauen Domain-Namen ab (z. B. `shop.example.com`)

Sie müssen keine Erneuerung manuell verwalten.

### Selbstsignierte Zertifikate

In einigen Situationen verwendet Spwig ein selbstsigniertes Zertifikat stattdessen:

- **Local-Modus**-Installationen (Entwicklungstest)
- Wenn Let's Encrypt Ihren Server nicht erreichen kann (Port 80 durch Firewall blockiert, DNS noch nicht verbreitet)
- Wenn keine Domain konfiguriert ist (nur IP-Zugriff)

Selbstsignierte Zertifikate verschlüsseln den Datenverkehr, werden aber von Browsern nicht als vertrauenswürdig angesehen — Besucher erhalten eine Sicherheitswarnung. Dies ist für Tests akzeptabel, sollte aber nicht in der Produktion verwendet werden.

### SSL im Sidecar-Modus

In **Sidecar-Modus** übernimmt Ihr bestehender Webserver (Apache, Nginx, Caddy usw.) die SSL-Verarbeitung. Spwig läuft auf einem HTTP-Port hinter Ihrem Proxy. Konfigurieren Sie SSL auf Ihrem Hauptwebserver wie gewohnt.

Der Installer generiert einen Proxy-Konfigurationsblock, den Sie Ihrem Webserver hinzufügen können. Für Nginx sieht das ungefähr so aus:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Domain wechseln

Um zu einer anderen Domain zu wechseln:

1. Richten Sie die DNS-Einstellungen für die neue Domain ein (A-Record, der auf Ihren Server verweist)
2. Führen Sie `./configure-domain.sh` erneut mit der neuen Domain aus
3. Das Skript aktualisiert alle Konfigurationen, holt ein neues Zertifikat und startet die Dienste neu
4. Aktualisieren Sie die **Store Settings** im Admin-Panel mit der neuen URL

Ihre alte Domain wird nicht mehr funktionieren, sobald die Konfiguration aktualisiert wurde.

## Problembehandlung

### „DNS-Validierung fehlgeschlagen“

Das Skript `configure-domain` überprüft, ob Ihre Domain auf Ihren Server verweist, bevor es ein Zertifikat anfordert. Wenn diese Überprüfung fehlschlägt:

- Stellen Sie sicher, dass der A-Record korrekt ist, indem Sie `dig +short yourdomain.com` verwenden
- Warten Sie noch einige Minuten auf die DNS-Verbreitung
- Überprüfen Sie, ob Sie den genauen Domain-Namen oder die Subdomain konfigurieren (nicht eine Wildcard)

### „Let's Encrypt Rate-Limit erreicht“

Let's Encrypt begrenzt die Anzahl der Zertifikat-Anfragen auf 5 pro Domain pro Woche. Wenn Sie diese Grenze erreichen:



- Warte 7 Tage, bevor du es erneut versuchst
- Verwende in der Zwischenzeit eine andere Unterdomäne
- Der Store bleibt währenddessen über HTTP oder mit einem selbstsignierten Zertifikat zugänglich

### "Port 80 ist nicht erreichbar"

Let's Encrypt muss sich über Port 80 mit deinem Server verbinden, um die Domaineigenschaft zu überprüfen. Stelle sicher:

- Dein Firewall erlaubt eingehenden TCP-Verkehr auf Port 80
- Keine andere Anwendung blockiert Port 80
- Der Sicherheitsgruppe oder Netzwerkfirewall deines Cloud-Anbieters erlaubt Port 80

### Zertifikatsverlängerung fehlgeschlagen

Falls die automatische Verlängerung fehlschlägt, läuft das Zertifikat nach 90 Tagen ab. Um es manuell zu verlängern:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Überprüfe den Verlängerungsprotokoll, falls dies fehlschlägt. Die häufigste Ursache ist, dass Port 80 durch eine Firewalländerung nach der ursprünglichen Installation blockiert wird.