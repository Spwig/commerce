---
title: GeoIP-Setup
---

GeoIP ermöglicht es Ihrem Store, automatisch zu erkennen, woher jeder Besucher kommt, basierend auf seiner IP-Adresse. Dies ermöglicht Funktionen, die auf der Standortbasis basieren, in Ihrem gesamten Store – von der automatischen Anzeige der richtigen Währung bis hin zur Ausführung geografischer Geschäftsregeln und zur Anzeige von Landebrechungen in Ihren Analysen.

Ihr Store ist standardmäßig mit dem Spwig GeoIP-Dienst konfiguriert, sodass die geografische Erkennung sofort funktioniert. Sie können auch zusätzliche Anbieter für eine höhere Genauigkeit verbinden, eine selbst heruntergeladene Datenbank verwenden oder sich auf Header von einem CDN verlassen, um Lookup ohne Latenzzeit durchzuführen.

## Wie Anbieter funktionieren

Navigieren Sie zu **Kunden > GeoIP-Anbieter**, um die für Ihren Store konfigurierten Anbieter anzuzeigen. Jeder Anbieter führt IP-zu-Ort-Abfragen mit einer anderen Methode durch. Wenn ein Besucher kommt, fragt Ihr Store die aktiven Anbieter in Prioritätsreihenfolge ab und verwendet das erste erfolgreiche Ergebnis.

Mehrere Anbieter können gleichzeitig aktiv sein – Anbieter mit niedrigerer Prioritätszahl werden zuerst ausprobiert. Wenn der Anbieter mit der höchsten Priorität fehlschlägt oder keine Daten zurückgibt, wird der nächste automatisch ausprobiert.

### Verfügbare Anbieter-Typen

| Anbieter | Beschreibung |
|----------|-------------|
| **Spwig GeoIP** | Standard-Cloud-basierte Abfrage über den Spwig-Dienst. Keine Einrichtung erforderlich. |
| **MaxMind GeoLite2** | Offline-Datenbank von MaxMind. Hohe Genauigkeit. Erfordert einen kostenlosen Lizenzschlüssel. |
| **DB-IP Lite** | Offline-Datenbank von DB-IP. Herunterladen von ihrer Website. |
| **IP2Location LITE** | Offline-Datenbank von IP2Location. Erfordert eine kostenlose Registrierung. |
| **CDN Edge Headers** | Liest Standort-Header, die von Ihrem CDN injiziert werden (z. B. Cloudflare). Null Latenz. |
| **Browser Hints** | Verwendet die vom Browser bereitgestellte Zeitzone/Sprache als weiche Standortsignal. |
| **Custom Provider** | Ein Anbieterkomponente, die aus dem Spwig-Komponenten-Marktplatz installiert wird. |

## Einen Anbieter hinzufügen

### Spwig GeoIP-Dienst verwenden (Standard)

Der Spwig GeoIP-Anbieter wird bei neuen Installationen automatisch hinzugefügt. Stellen Sie sicher, dass er in der Liste erscheint und dass **Aktiv** markiert ist. Keine zusätzliche Konfiguration ist erforderlich.

### MaxMind GeoLite2-Datenbank hinzufügen

MaxMind bietet eine kostenlose Offline-Datenbank an, die genaue Ergebnisse liefert, ohne Abfragen an einen externen Dienst zu senden.

1. Registrieren Sie sich für ein kostenloses Konto auf maxmind.com und generieren Sie einen Lizenzschlüssel
2. Navigieren Sie zu **Kunden > GeoIP-Anbieter** und klicken Sie auf **+ GeoIP-Anbieter hinzufügen**
3. Füllen Sie das Formular aus:
   - **Name**: `MaxMind GeoLite2` (oder beliebiger beschreibender Name)
   - **Anbieter-Typ**: MaxMind GeoLite2
   - **Aktiv**: markiert
   - **Priorität**: `1` (niedriger als der Spwig-Standard, um ihn zuerst zu testen, oder höher, um ihn als Ersatz zu verwenden)
   - **Lizenzschlüssel**: Fügen Sie Ihren MaxMind-Lizenzschlüssel ein
   - **Datenbank-URL**: Die Download-URL aus Ihrem MaxMind-Konto-Dashboard
4. Klicken Sie auf **Speichern**

Nachdem Sie gespeichert haben, wählen Sie den Anbieter in der Liste aus und verwenden Sie die Aktion **Ausgewählte Anbieterdatenbanken aktualisieren**, um sicherzustellen, dass die Datenbank-URL erreichbar ist.

### CDN-Edge-Header hinzufügen

Wenn Ihr Store hinter einem CDN steht, das geografische Header injiziert (z. B. Cloudflares `CF-IPCountry`), können Sie diese Header für sofortige, latenzfreie Ländererkennung verwenden.

1. Navigieren Sie zu **Kunden > GeoIP-Anbieter** und klicken Sie auf **+ GeoIP-Anbieter hinzufügen**
2. Setzen Sie **Anbieter-Typ** auf **CDN Edge Headers**
3. Setzen Sie **Priorität** auf `0` (höchste Priorität, da Header die schnellste Quelle sind)
4. Geben Sie im Feld **Konfiguration** an, welchen Header Ihr CDN verwendet:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Klicken Sie auf **Speichern**

## Einen Anbieter testen

Nachdem Sie einen Anbieter hinzugefügt haben, können Sie überprüfen, ob er korrekt funktioniert:

1. In der GeoIP-Anbieter-Liste wählen Sie den Anbieter mit dem Häkchen
2. Öffnen Sie das Dropdown **Aktion** und wählen Sie **Ausgewählte Anbieter testen**
3. Klicken Sie auf **Los**

Spwig sendet eine Testabfrage für eine bekannte IP-Adresse (Googles öffentliche DNS, `8.8.8.8`) und zeigt Ihnen das Ergebnis an. Ein erfolgreicher Test zeigt das zurückgegebene Land und die Antwortzeit in Millisekunden an.

## Anbieterpriorität festlegen

Wenn mehrere Anbieter aktiv sind, steuert das Feld **Priorität**, welcher zuerst versucht wird.

Niedrigere Zahlen bedeuten höhere Priorität.

Zum Beispiel, um zuerst CDN-Header (schnellster) und dann auf Spwig GeoIP zurückzugreifen:

| Anbieter | Priorität |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Sie können die Priorität direkt in der Listenansicht bearbeiten — die Spalte **Priorität** ist inline bearbeitbar.

## Monitoring der Anbieterleistung

Jeder Anbieter-Record verfolgt seine eigenen Genauigkeitsstatistiken:

- **Gesamte Lookups** — Gesamtzahl der versuchten IP-Lookups
- **Erfolgreiche Lookups** — Lookups, die ein Ergebnis zurückgaben
- **Fehlgeschlagene Lookups** — Lookups, die keine Daten oder einen Fehler zurückgaben
- **Durchschnittliche Antwortzeit (ms)** — Durchschnittliche Antwortzeit in Millisekunden
- **Genauigkeit** — Prozentsatz der erfolgreichen Lookups

Wenn ein Anbieter eine niedrige Genauigkeitsrate oder hohe Antwortzeiten aufweist, überlegen Sie, seine Priorität anzupassen oder ihn zugunsten einer besseren Leistung zu deaktivieren.

## Länderzuordnungen

Navigieren Sie zu **Kunden > Länderzuordnungen**, um Standardwerte pro Land für Währung, Sprache, Steuern und Versand zu konfigurieren. Jeder Ländereintrag steuert:

- **Standardwährung** — die Währung, die für Besucher aus diesem Land vorausgewählt wird
- **Standardsprache** — die Sprache, die Besuchern aus diesem Land angezeigt wird
- **Steuersatz** — der Standardsteuersatz, der für dieses Land angewendet wird
- **EU-Mitglied** / **Umsatzsteuer erforderlich** — wird für die Steuerkonformität in der EU verwendet
- **Versandzone** — verknüpft das Land mit einer Versandzone
- **COD unterstützt** — aktiviert Barzahlung bei Lieferung für dieses Land

Sie können die Felder **Aktiv**, **Standardwährung** und **Standardsprache** direkt in der Liste bearbeiten, ohne jeden Eintrag zu öffnen.

## Tipps

- Der Spwig GeoIP-Anbieter funktioniert sofort ohne Konfiguration — fügen Sie zusätzliche Anbieter nur hinzu, wenn Sie eine höhere Genauigkeit oder eine Offline-Betriebsweise benötigen
- Wenn Sie Cloudflare verwenden, ist der Anbieter CDN Edge Headers die beste Wahl: Er fügt keine Latenz hinzu und zählt nicht gegen eine API-Kontingent
- Aktivieren Sie nur die Anbieter, die Sie tatsächlich benötigen — das Aktivieren vieler Anbieter verbessert die Genauigkeit nicht, wenn der erste bereits erfolgreich ist
- Prüfen Sie die Genauigkeitsstatistiken wöchentlich und deaktivieren Sie jeden Anbieter, dessen Erfolgsquote unter 80 % liegt
- Länderzuordnungen werden als Standardwerte verwendet; Kunden können immer ihre Währung und Sprache manuell im Frontend ändern