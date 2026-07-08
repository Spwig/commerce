---
title: Digitale Produkte
---

Digitale Produkte ermoeglichen es Ihnen, herunterladbare Dateien, Softwarelizenzen und andere nicht-physische Gueter zu verkaufen. Spwig unterstuetzt eigenstaendige digitale Produkte sowie hybride Produkte, die physische und digitale Lieferung kombinieren.

![Lizenzanbieter](/static/core/admin/img/help/digital-products/license-providers.webp)

## Arten von Digitalen Produkten

### Eigenstaendiges Digitales Produkt

Setzen Sie den **Produkttyp** auf **Digitales Produkt** fuer rein digitale Artikel:
- Softwareanwendungen
- E-Books und PDFs
- Musik und Audiodateien
- Digitale Kunst und Vorlagen

### Hybride Produkte

Jeder Produkttyp kann eine digitale Lieferung beinhalten, indem Sie **Ist Digitales Produkt** auf dem Tab Basisinformationen aktivieren. Dies ist nuetzlich fuer:
- **Variable digitale Produkte** — Software mit Basis-/Pro-/Enterprise-Editionen
- **Anpassbare digitale Produkte** — Individuell gestaltete digitale Inhalte
- **Physische + digitale Pakete** — Ein Buch, das einen digitalen Download beinhaltet

## Ein Digitales Produkt einrichten

### Schritt 1: Das Produkt erstellen

1. Navigieren Sie zu **Produkte > Alle Produkte** und klicken Sie auf **+ Produkt hinzufuegen**
2. Setzen Sie den **Produkttyp** auf **Digitales Produkt** (oder aktivieren Sie **Ist Digitales Produkt** bei einem anderen Produkttyp)
3. Fuellen Sie die Produktdetails aus (Name, Beschreibung, Preis)
4. Speichern Sie das Produkt

### Schritt 2: Herunterladbare Dateien hinzufuegen

1. Gehen Sie zum Tab **Inventar** des Produkts
2. Laden Sie im Bereich **Digitale Dateien** die Dateien hoch, die Kunden nach dem Kauf erhalten
3. Fuer jede Datei koennen Sie festlegen:
   - **Dateiname** — Anzeigename, der den Kunden angezeigt wird
   - **Download-Limit** — Maximale Anzahl der Downloads (0 = unbegrenzt)
   - **Ablauftage** — Anzahl der Tage, die der Download-Link aktiv bleibt

### Schritt 3: Lizenzlieferung konfigurieren (Optional)

Wenn Ihr digitales Produkt Lizenzschluessel erfordert:

1. Navigieren Sie zu **Einstellungen > Lizenzverwaltung**
2. Verbinden Sie einen Lizenzanbieter (siehe unten)
3. Weisen Sie im Produktbearbeitungsformular den Lizenzanbieter zu

## Lizenzanbieter

Lizenzanbieter sind externe Dienste, die automatisch Softwarelizenzschluessel generieren und verwalten, wenn ein Kunde Ihr Produkt kauft.

### Verfuegbare Anbietertypen

| Anbieter | Beschreibung |
|----------|-------------|
| **Spwig Integrierter Lizenzserver** | Einfache Lizenzschluesselgenerierung, in die Plattform integriert |
| **Keygen.sh** | Umfassende API zur Lizenzverwaltung |
| **LicenseSpring** | Enterprise-Lizenzverwaltung |
| **Cryptlex** | Softwarelizenzierung mit Offline-Unterstuetzung |
| **Benutzerdefinierte API** | Verbinden Sie jedes Lizenzsystem ueber REST API |

### Einen Lizenzanbieter verbinden

1. Navigieren Sie zu **Einstellungen > Lizenzverwaltung**
2. Klicken Sie auf **Anbieter verbinden**
3. Folgen Sie dem Einrichtungsassistenten:
   - **Schritt 1** — Waehlen Sie den Anbietertyp
   - **Schritt 2** — Konfigurieren Sie die allgemeinen Einstellungen
   - **Schritt 3** — Geben Sie die API-Zugangsdaten ein
4. Testen Sie die Verbindung, um die Funktionsfaehigkeit zu ueberpruefen
5. Speichern Sie die Konfiguration

### Anbieterkarte

Jeder verbundene Anbieter zeigt:
- **Status-Badges** — Aktiv/Inaktiv und Verbindungsstatus
- **API-Endpunkt** — Die konfigurierte Server-URL
- **Synchronisierungsfaehigkeiten** — Unterstuetzung fuer Bestell-, Aktivierungs- und Deaktivierungssynchronisierung
- **Aktionsschaltflaechen** — Konfigurieren, Testen und Jetzt Synchronisieren

### Synchronisierungsfaehigkeiten

Lizenzanbieter koennen bei drei Ereignissen synchronisieren:

- **Bestellung** — Automatische Generierung eines Lizenzschluessels, wenn ein Kunde einen Kauf abschliesst
- **Aktivierung** — Erfassung, wann ein Kunde seine Lizenz aktiviert
- **Deaktivierung** — Verwaltung der Lizenzdeaktivierung fuer Erstattungen oder Uebertragungen

## Kundenerlebnis

### Nach dem Kauf

Wenn ein Kunde ein digitales Produkt kauft:

1. **Bestellbestaetigung** — Zeigt an, dass die digitale Lieferung enthalten ist
2. **E-Mail-Zustellung** — Download-Links und/oder Lizenzschluessel werden automatisch gesendet
3. **Kontoseite** — Kunden koennen ueber ihr Konto-Dashboard auf ihre Downloads zugreifen
4. **Download-Seite** — Sichere, zeitlich begrenzte Download-Links

### Download-Sicherheit

Downloads digitaler Dateien sind geschuetzt durch:
- Einzigartige, zeitlich begrenzte Download-Tokens
- Optionale Begrenzung der Download-Anzahl
- Ablaufdaten, nach denen Links inaktiv werden
- Anmeldepflicht (fuer registrierte Kunden)

## Tipps

- Setzen Sie angemessene Download-Limits (3-5 Downloads), um Missbrauch zu verhindern und gleichzeitig erneute Downloads zu ermoeglichen.
- Verwenden Sie Ablauftage, die Ihrem Support-Zeitraum entsprechen (z. B. 365 Tage fuer ein Jahr Zugang).
- Testen Sie den gesamten Kaufablauf mit einer Testbestellung, um sicherzustellen, dass Download-Links und Lizenzschluessel korrekt zugestellt werden.
- Verbinden Sie fuer Softwareprodukte einen Lizenzanbieter, um die Schluesselgenerierung zu automatisieren, anstatt Schluessel manuell zu verwalten.
- Nutzen Sie die Hybridprodukt-Funktion, wenn Sie physische Waren mit digitalen Extras verkaufen (z. B. gedrucktes Buch + PDF).
