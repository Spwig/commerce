---
title: Versand-Anbieterkonten
---

Versand-Anbieterkonten verbinden Ihren Store mit Anbieter-APIS (FedEx, UPS, DHL) zur Echtzeit-Berechnung von Versandkosten und zur automatisierten Etikettenkauf. Jedes Konto speichert verschlüsselte API-Anmeldeinformationen, überwacht den Verbindungsstatus und verknüpft sich mit Echtzeit-Versandmethoden. Anbieter holen Live-Raten beim Checkout basierend auf Paketabmessungen, Gewicht, Herkunft und Zielort – eliminieren manuelle Raten-Tabellen-Wartung und gewährleisten genaue Anbieterpreise.

Verwenden Sie Anbieterkonten, wenn Sie Versandkosten, die vom Anbieter berechnet werden, oder automatisierte Etiketten-Generierung anstelle der manuellen Versand-Erstellung benötigen.

## Unterstützte Versand-Anbieter

Spwig unterstützt große Anbieter über installierbare Anbieter-Komponenten:

### FedEx

**Dienste**: Ground, Express, International
**API**: FedEx Web Services
**Funktionen**: Echtzeit-Raten, Etikettenkauf, Nachverfolgung, internationale Zoll

### UPS

**Dienste**: Ground, Air, Worldwide
**API**: UPS Developer API
**Funktionen**: Echtzeit-Raten, Etiketten-Generierung, Nachverfolgung, Adressprüfung

### DHL

**Dienste**: Express, eCommerce, International
**API**: DHL Express API
**Funktionen**: Internationale Raten, Zolldokumente, Nachverfolgung

### Zusätzliche Anbieter

Installieren Sie sie bei Bedarf aus dem Komponenten-Marktplatz (USPS, Canada Post, Australia Post, etc.)

---

## Konfiguration der Anbieterkonten

Jede Anbieterkonto erfordert:

### Grundlegende Informationen

- **Anzeigename**: Wie das Konto im Admin-Panel erscheint (z. B. "FedEx Production Account")
- **Anbieter**: Wählen Sie die installierte Anbieterkomponente aus dem Dropdown-Menü aus
- **Aktiv**: Schalten Sie um, um das Konto zu aktivieren/deaktivieren, ohne die Anmeldeinformationen zu löschen
- **Standardkonto**: Legen Sie dieses Konto als Standardkonto für diesen Anbieter fest (nur ein Standardkonto pro Anbieter)

### API-Anmeldeinformationen (verschlüsselt)

**Variiert je nach Anbieter**, typischerweise umfassen:

**FedEx**:
- Kontonummer
- Meter-Nummer
- API-Schlüssel
- API-Geheimnis

**UPS**:
- Zugriffslizenznummer
- Benutzer-ID
- Passwort
- Kontonummer

**DHL**:
- Site-ID
- Passwort
- Kontonummer

**Alle Anmeldeinformationen sind im Ruhezustand verschlüsselt** und werden nur beim Durchführen von API-Aufrufen entschlüsselt.

### Ursprungsadresse

- **Standardversandadresse**: Lager-/Ursprungsadresse für die Ratenberechnung
- Einige Anbieter erfordern eine spezifische Ursprungsadresse in ihrem Dashboard

### Einstellungen

Anbieter-spezifische Optionen (variiert je nach Anbieter):

- **Testmodus**: Verwenden Sie die Sandbox-/Test-API-Endpunkte des Anbieters
- **Verhandelte Raten**: Verwenden Sie Ihre verhandelten Anbieter-Raten (wenn verfügbar)
- **Versicherung einbeziehen**: Versicherung automatisch in Raten einbeziehen
- **Wohnungsgebühr**: Wohnungsversandgebühren anwenden
- **Unterschrift erforderlich**: Standard-Unterschriftsbedingungen

---

## Anbieterkonto erstellen

**6-Schritt-Setup-Prozess**:

**Schritt 1: Erhalten Sie Zugang zur Anbieter-API**
1. Erstellen Sie ein Konto bei dem Anbieter (FedEx.com, UPS.com, DHL.com)
2. Beantragen Sie Zugang zur API/Entwickler-API
3. Führen Sie die Onboarding-Verfahren der Anbieter-API durch (kann 1-3 Geschäftstage dauern)
4. Empfangen Sie die API-Anmeldeinformationen per E-Mail oder über das Entwicklerportal

**Schritt 2: Installieren Sie die Anbieterkomponente** (wenn nicht bereits vorinstalliert)
1. Gehen Sie zu Einstellungen > Komponenten > Marktplatz
2. Suchen Sie nach dem Namen des Anbieters (z. B. "FedEx")
3. Installieren Sie die Versand-Anbieterkomponente
4. Warten Sie, bis die Installation abgeschlossen ist

**Schritt 3: Erstellen Sie ein Anbieterkonto in Spwig**
1. Navigieren Sie zu Einstellungen > Versand > Anbieterkonten
2. Klicken Sie auf "Anbieterkonto hinzufügen"
3. Wählen Sie den Anbieter aus dem Dropdown-Menü aus
4. Geben Sie den Anzeigename ein

**Schritt 4: Geben Sie die API-Anmeldeinformationen ein**
1. Füllen Sie die Felder für die Anmeldeinformationen aus (variiert je nach Anbieter)
2. Die Anmeldeinformationen werden automatisch verschlüsselt, wenn Sie sie speichern
3. Optional: Aktivieren Sie den Testmodus für die erste Testphase

**Schritt 5: Verbindung testen**
1. Klicken Sie auf den Schaltflächen "Verbindung testen"
2. Das System versucht, eine API-Anfrage an den Anbieter zu senden
3. Überprüfen Sie, ob der Status "Verbunden" erscheint
4. Prüfen Sie den Zeitstempel von last_tested_at

**Schritt 6: Verknüpfen mit einer Versandmethode**
1. Erstellen Sie oder bearbeiten Sie eine Versandmethode (Einstellungen > Warenkorb > Versandmethoden)
2. Setzen Sie method_type = "Echtzeit"
3. Wählen Sie das Anbieterkonto aus dem Dropdown-Menü aus
4. Speichern Sie die Methode

---

## Überwachung des Verbindungsstatus

Anbieterkonten überwachen den Verbindungsstatus:

### Statuswerte

**Unbekannt** (grau): Nie getestet oder noch nicht verbunden

**Verbunden** (grün): Letzter API-Aufruf erfolgreich, Anmeldeinformationen gültig

**Fehler** (rot): Letzter API-Aufruf fehlgeschlagen, Anmeldeinformationen können ungültig sein

### Letzter Test

- **Zeitstempel**: Wann die Verbindung zuletzt überprüft wurde
- **Automatische Aktualisierung**: Jedes Mal, wenn der Anbieter verwendet wird (Ratenabfrage, Etikettenkauf)
- **Manueller Test**: Klicken Sie jederzeit auf den Schaltflächen "Verbindung testen"

### Fehlerbehebung bei fehlgeschlagenen Verbindungen

**Häufige Ursachen**:
- Falsche API-Anmeldeinformationen (Tippfehler, kopiert mit zusätzlichem Leerzeichen)
- API-Schlüssel des Anbieters abgelaufen oder widerrufen
- Testmodus aktiviert, aber Produktions-Anmeldeinformationen verwendet (oder umgekehrt)
- IP-Adresse nicht mit dem Anbieter genehmigt
- Ausfall der Anbieter-API

**Lösungsschritte**:
1. Stellen Sie sicher, dass die Anmeldeinformationen exakt mit dem Anbieter-Dashboard übereinstimmen
2. Prüfen Sie, ob der Testmodus-Einstellung mit dem Anmeldeinformationstyp übereinstimmt
3. Prüfen Sie die Ausfallseite der Anbieter-API für Ausfälle
4. Kontaktieren Sie den Anbieter-Support für die Kontenüberprüfung

---

## Arbeitsablauf für Ratenabfrage

Wie Echtzeit-Raten beim Checkout funktionieren:

**1. Kunde gibt Adresse ein**
- Versandadresse eingegeben
- Warenkorb berechnet Gesamtgewicht + Abmessungen

**2. System bereitet Ratenanfrage vor**
- Holt Anbieterkonto-Anmeldeinformationen (entschlüsselt)
- Berechnet Paketabmessungen aus Warenkorbartikeln (verwendet Versandpakete, wenn definiert)
- Vorbereitet API-Anfrage mit Ursprung, Zielort, Paketen

**3. Anbieter-API aufgerufen**
- Anfrage an Anbieter-API mit Auth-Anmeldeinformationen gesendet
- Anbieter berechnet Rate basierend auf Zone, Gewicht, Abmessungen
- Antwort umfasst Dienstoptionen (Ground, Express, etc.)

**4. Raten werden angezeigt**
- System analysiert Anbieterantwort
- Normalisiert auf Standardformat
- Optionaler Aufschlag angewendet (wenn konfiguriert)
- Raten werden Kunden beim Checkout angezeigt

**5. Kunde wählt Dienst aus**
- Kunde wählt bevorzugte Option aus
- Ausgewählte Rate wird zur Bestellung gespeichert

**Beispiel API-Fluss**:
```
Anfrage an FedEx API:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // Gramm
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

FedEx Antwort:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Etikettenkauf (optional)

Wenn der Anbieter Etiketten-Generierung unterstützt:

**Arbeitsablauf**:
1. Kunde vervollständigt Bestellung
2. Händler erstellt Versand (Bestellungen > Bestell-Details > Versand erstellen)
3. Wählen Sie Anbieterkonto + Dienst aus
4. System ruft Anbieter-Etiketten-API auf
5. Etiketten-PDF generiert und an Versand angehängt
6. Nachverfolgungsnummer automatisch ausgefüllt
7. Etiketten bereit für Druck

**Vorteile**:
- Kein manuelles Anmelden auf Anbieter-Website
- Nachverfolgung automatisch synchronisiert
- Zollformulare automatisch generiert (international)
- Batch-Etiketten-Generierung möglich

---

## Raten-Aufschlag

Fügen Sie Händler-Aufschlag zu Anbieter-Raten hinzu:

**Konfiguration** (in Versandmethode, nicht in Anbieterkonto):
- **Aufschlag-Typ**: Prozent oder Fix
- **Aufschlag-Betrag**: z. B. 15 % oder $2,50

**Beispiel**:
```
Anbieter-Rate: $12,50
Aufschlag: 15 %
Kunde zahlt: $14,38

ODER

Anbieter-Rate: $12,50
Aufschlag: $2,50 (Fix)
Kunde zahlt: $15,00
```

**Anwendungsfälle**:
- Verpackung/Verarbeitungskosten abdecken
- Gewinnmarge für Versand hinzufügen
- Kartenkosten für Versand ausgleichen

---

## Mehrere Anbieterkonten

Sie können mehrere Konten für denselben Anbieter erstellen:

**Anwendungsfälle**:
1. **Test vs. Produktion**
   - Testkonto: Anbieter-Sandbox-Anmeldeinformationen
   - Produktionskonto: Live-Anmeldeinformationen

2. **Mehrere Lagerhäuser**
   - Lagerhaus A-Konto: Ursprung = Los Angeles
   - Lagerhaus B-Konto: Ursprung = New York

3. **Verschiedene verhandelte Raten**
   - Konto A: Standardraten
   - Konto B: Mengenrabatt-Raten

**Jedes Konto kann mit verschiedenen Versandmethoden verknüpft werden** für eine flexible Konfiguration.

---

## Tipps

- **Testen Sie zuerst in der Sandbox** – Verwenden Sie Anbieter-Test-Anmeldeinformationen, bevor Sie live gehen
- **Überwachen Sie den Verbindungsstatus** – Prüfen Sie regelmäßig das Dashboard auf Fehlerstatus
- **Definieren Sie Versandpakete** – Genauere Abmessungen verbessern Ratenangebote
- **Verwenden Sie verhandelte Raten** – Aktivieren Sie diese, wenn Sie Mengenrabatte mit dem Anbieter haben
- **Setzen Sie eine realistische Ursprung** – Verwenden Sie die tatsächliche Versandadresse für genaue Zonen
- **Halten Sie Anmeldeinformationen sicher** – Teilen Sie niemals API-Schlüssel, aktualisieren Sie sie regelmäßig
- **Halten Sie eine Backup-Methode bereit** – Behalten Sie eine Flachrate-Methode aktiv, wenn die Anbieter-API fehlschlägt
- **Überwachen Sie Anbieter-API-Limits** – Einige Anbieter begrenzen API-Aufrufe pro Tag
- **Aktualisieren Sie Anmeldeinformationen sofort** – Wenn der Anbieter Schlüssel rotiert, aktualisieren Sie sie sofort
- **Verwenden Sie beschreibende Namen** – "FedEx LA Lagerhaus" ist besser als "FedEx 1"