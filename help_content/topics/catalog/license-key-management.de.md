---
title: Lizenzschlüssel-Management
---

Das Lizenzschlüssel-Management ermöglicht es Ihnen, zu steuern, wie Software-Lizenzschlüssel generiert, gespeichert und an Kunden weitergegeben werden, wenn sie digitale Produkte erwerben. Spwig unterstützt eingebaute Schlüsselgenerierung, vorgefertigte Schlüsselpools und Integrationen mit externen Lizenzverwaltungsdiensten.

## Übersicht

Es gibt drei Methoden, um Lizenzschlüssel in Spwig zu verwalten:

| Methode | Bestens geeignet für |
|--------|---------|
| **Lizenzvorlagen** | Automatisch eindeutige Schlüssel in einem benutzerdefinierten Format zum Zeitpunkt des Kaufs generieren |
| **Lizenzpools** | Vorgängig eine Schlüsselmenge generieren, um sie in Massen zu verteilen |
| **Externe Anbieter** | Die Schlüsselgenerierung und -verwaltung einem Drittanbieter wie Keygen.sh überlassen |

Diese Methoden können kombiniert werden – beispielsweise kann ein Pool eine benutzerdefinierte Vorlage verwenden, um das Schlüsselformat zu definieren, und kann optional generierte Schlüssel an einen externen Anbieter synchronisieren.

## Lizenzschlüsselvorlagen

Eine Lizenzschlüsselvorlage definiert das *Format* der generierten Schlüssel. Vorlagen verwenden ein Muster mit Platzhaltern, die Spwig zur Generierungszeit ausfüllt.

### Vorlage erstellen

1. Navigieren Sie zu **Katalog > Lizenzschlüsselvorlagen**
2. Klicken Sie auf **+ Lizenzschlüsselvorlage hinzufügen**
3. Geben Sie einen **Namen** an (z. B. `Standard App Lizenz`)
4. Konfigurieren Sie das **Muster** mithilfe von Platzhaltern (siehe unten)
5. Legen Sie bei Bedarf **Präfix** und **Suffix** fest (z. B. ein Präfix von `MYAPP` fügt `MYAPP-` zu jedem Schlüssel hinzu)
6. Wählen Sie das **Trennzeichen** (Standard: `-`)
7. Legen Sie den **Zeichensatz** fest – die Zeichen, die für zufällige Segmente verwendet werden. Der Standardwert enthält keine verwechslbaren Zeichen wie `0` und `O`, `1` und `I`
8. Legen Sie **Mindest-/Maximallänge** für die Validierung fest
9. Klicken Sie auf **Speichern**

### Platzhalter für Muster

| Platzhalter | Beschreibung | Beispiel-Ausgabe |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N zufällige Zeichen aus dem Zeichensatz | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N-stellige Prüfsumme für die Validierung | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Der Präfixwert der Vorlage | `MYAPP` |
| `{SUFFIX}` | Der Suffixwert der Vorlage | `PRO` |
| `{ORDER_ID}` | Die Bestellnummer | `10045` |
| `{PRODUCT_SKU}` | Die SKU des Produkts | `SOFTPRO` |
| `{DATE:FORMAT}` | Formatierter Datum | `{DATE:YYMMDD}` → `260318` |

**Beispiel-Muster**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Dies erzeugt Schlüssel wie: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Schlüsselvorschau

Nachdem Sie eine Vorlage gespeichert haben, steht eine Aktion **Beispiel-Schlüssel generieren** auf der Vorlagenliste zur Verfügung. Nutzen Sie dies, um sicherzustellen, dass Ihr Muster Schlüssel im erwarteten Format erzeugt, bevor Sie die Vorlage einem Produkt zuweisen.

## Lizenzpools

Ein Lizenzpool ist eine Gruppe vorgenerierter Schlüssel für ein Produkt. Pools sind nützlich, wenn:
- Sie Schlüssel für physische Verpackungen benötigen (Handelsverpackungen, gedruckte Karten)
- Sie mit Händlern arbeiten, die Batches von Schlüsseln benötigen
- Sie Schlüssel im Voraus generieren möchten, anstatt sie bei Bedarf zu generieren

### Lizenzpool erstellen

1. Navigieren Sie zu **Katalog > Lizenzpools**
2. Klicken Sie auf **+ Lizenzpool hinzufügen**
3. Füllen Sie die Pool-Details aus:

| Feld | Beschreibung |
|-------|-------------|
| **Name** | Beschreibender Name (z. B. `Retail Pack Q1 2026`) |
| **Produkt** | Das Produkt, für das diese Schlüssel bestimmt sind |
| **Lizenzvorlage** | Vorlage für das Schlüsselformat (Standard ist die Vorlage des Produkts) |
| **Gesamtanzahl Schlüssel** | Wie viele Schlüssel generiert werden sollen |
| **Schlüsseltyp** | Perpetuell, Abonnement oder Testversion |
| **Maximale Aktivierungen** | Wie viele Geräte jeder Schlüssel aktivieren kann |
| **Ablauf nach Tagen** | Tage, bis die Lizenz nach der ersten Aktivierung abläuft (leer lassen, um keinen Ablauf zu haben) |
| **Pool abläuft am** | Datum, ab dem Schlüssel aus diesem Pool, die nicht verwendet wurden, ungültig werden |
| **Zu Anbieter synchronisieren** | Optional: Generierte Schlüssel an einen externen Lizenzanbieter synchronisieren |

4. Klicken Sie auf **Speichern** – Spwig beginnt, die Schlüssel im Hintergrund zu generieren

### Pool-Status

| Status | Bedeutung |
|--------|---------|
| **Erzeugung** | Schlüssel werden im Hintergrund erstellt |
| **Bereit** | Alle Schlüssel wurden generiert und sind für die Verteilung verfügbar |
| **Aufgebraucht** | Alle Schlüssel wurden Bestellungen zugewiesen |
| **Abgelaufen** | Der Ablaufdatum des Pools ist vergangen |

### Pool überwachen

Die Pool-Liste zeigt an, wie viele Schlüssel verteilt wurden, im Vergleich zur Gesamtzahl der generierten Schlüssel. Öffnen Sie einen Pool, um die vollständige Liste der Schlüssel und deren individuelle Status anzuzeigen.

## Externe Lizenzbereitsteller

Externe Bereitsteller sind Drittanbieter-Lizenzbereitstellungsdienste, die die Schlüsselerstellung und -aktivierung verwalten. Wenn ein Kunde einen Kauf abschließt, kommuniziert Spwig mit dem Bereitsteller, um den Schlüssel zu generieren und zu registrieren.

### Unterstützte Bereitsteller

| Bereitsteller | Typ |
|----------|------|
| **Spwig eingebauter Lizenzservers** | Eingebaut – kein externes Konto erforderlich |
| **Keygen.sh** | Cloud-basierte Lizenzbereitstellung API |
| **LicenseSpring** | Unternehmenslizenzbereitstellung |
| **Cryptlex** | Lizenzbereitstellung mit Offline-Unterstützung |
| **Benutzerdefinierte API** | Jeder REST-basierte Lizenzsysteem |

### Verbindung mit einem Bereitsteller

1. Navigieren Sie zu **Katalog > Lizenzbereitsteller**
2. Klicken Sie auf **+ Lizenzbereitsteller hinzufügen**
3. Füllen Sie die Bereitstellerdetails aus:

| Feld | Beschreibung |
|-------|-------------|
| **Name** | Eine Bezeichnung für diese Verbindung (z. B. `Keygen Production`) |
| **Bereitstellertyp** | Wählen Sie aus den unterstützten Bereitstellern aus |
| **API-Endpunkt** | Die Basis-URL der API des Bereitstellers |
| **API-Schlüssel** | Authentifizierungsschlüssel für den Bereitsteller |
| **API-Geheimnis** | Wenn dies vom Bereitsteller erforderlich ist |

4. Konfigurieren Sie das Sync-Verhalten:
   - **Auf Bestellung synchronisieren** – Automatisch synchronisieren, wenn ein Kunde einen Kauf abschließt
   - **Auf Aktivierung synchronisieren** – Aktivierungen von Geräten an den Bereitsteller melden
   - **Auf Deaktivierung synchronisieren** – Deaktivierungen melden (nützlich für Lizenstransfers und Erstattungen)
   - **Bidirektionale Synchronisation** – Ermöglicht es dem Bereitsteller, Spwig-Records über Webhooks zu aktualisieren

5. Klicken Sie auf **Speichern**, dann auf **Verbindung testen**, um sicherzustellen, dass die Anmeldeinformationen funktionieren

### Verbindungsstatus

Jeder Bereitsteller zeigt einen von drei Verbindungsstatus an:

| Status | Bedeutung |
|--------|---------|
| **Nicht getestet** | Die Verbindung wurde noch nicht überprüft |
| **Verbunden** | Letzter Test war erfolgreich |
| **Fehler** | Verbindungstest fehlgeschlagen – prüfen Sie die Fehlermeldung |

### Bestehende Lizenzen synchronisieren

Um vorhandene Lizenzschlüssel manuell an einen Bereitsteller zu senden (für die erste Einrichtung oder nach einem fehlgeschlagenen Sync), verwenden Sie die Aktion **Jetzt synchronisieren** aus der Liste der Bereitsteller.

## Sync-Aktivitäten überwachen

Navigieren Sie zu **Katalog > Externe Lizenzsynchronisationen**, um den Sync-Protokoll zu überprüfen. Jeder Eintrag zeigt an:
- Den Lizenzschlüssel, der synchronisiert wurde
- Den Bereitsteller, an den er gesendet wurde
- Richtung (Spwig → Bereitsteller oder Bereitsteller → Spwig)
- Status (Ausstehend, Erfolgreich, Fehlgeschlagen)
- Fehlerdetails für fehlgeschlagene Synchronisationen

Fehlgeschlagene Synchronisationen werden automatisch erneut versucht. Sie können auch eine erneute Versuche erzwingen, indem Sie den Eintrag bearbeiten und den Fehler löschen.

## Tipps

- Verwenden Sie das Standardzeichenmenge (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`), um verwirrende Zeichen zu vermeiden, die Kunden oft falsch lesen – es enthält `0`, `O`, `1` und `I` nicht.
- Fügen Sie einen `{CHECKSUM}`-Segment in Ihr Vorlagenmuster hinzu, damit Kunden und Ihr Support-Team fehlgeschriebene Schlüssel schnell erkennen können.
- Für Produkte mit hohem Umfang verwenden Sie einen Pool anstelle der auf Anfrage generierten Schlüssel, um sicherzustellen, dass Schlüssel sofort beim Checkout geliefert werden.
- Legen Sie **Pool Ablaufdatum** für saisonale oder zeitlich begrenzte Schlüsselbatches fest, damit alte, nicht verwendete Schlüssel automatisch ungültig werden.
- Testen Sie immer die Verbindung zum Bereitsteller nach der Einrichtung und nach jeder Änderung der Anmeldeinformationen – eine defekte Verbindung bedeutet, dass Kunden ihre Schlüssel nicht erhalten.
- Wenn Sie bidirektionale Synchronisation verwenden, konfigurieren Sie die Webhook-URL Ihres Bereitstellers, um auf den Lizenzzugangspunkt Ihres Geschäfts zu verweisen.