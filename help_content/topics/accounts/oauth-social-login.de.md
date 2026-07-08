---
title: OAuth & Social Login Setup
---

OAuth und soziale Anmeldung ermöglichen es Kunden, sich mit ihren bestehenden Google-, Apple- oder Microsoft-Konten in Ihrem Geschäft anzumelden — es ist keine weitere Passworterstellung erforderlich.

![OAuth-Einstellungen](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## Was ist OAuth / Soziale Anmeldung?

OAuth ist ein sicheres Authentifizierungsstandard, der es Kunden ermöglicht, sich mit Anmeldeinformationen von vertrauften Anbietern wie Google, Apple oder Microsoft anzumelden.

### Vorteile

- **Schnellerer Checkout** — Kunden überspringen das Registrierungsformular und melden sich mit einem Klick an
- **Verringerte Reibung** — Keine Passworterstellung, Bestätigungs-E-Mails oder vergessene Passwort-Flows
- **Bessere Umwandlung** — Studien zeigen, dass soziale Anmeldung die Umwandlungsrate um 20-40 % erhöhen kann
- **Erhöhte Sicherheit** — Anmeldeinformationen passieren nie durch Ihr Geschäft; die Authentifizierung wird vom Anbieter übernommen
- **Kundentrust** — Kunden vertrauen etablierten Anbietern mit ihren Anmeldeinformationen

### Wie es funktioniert

1. Kunde klickt auf „Mit Google anmelden“ (oder Apple/Microsoft) auf Ihrer Anmeldeseite
2. Sie werden zu der sicheren Anmeldeseite des Anbieters weitergeleitet
3. Kunde authentifiziert sich mit seinen Anmeldeinformationen des Anbieters
4. Der Anbieter sendet die überprüften Identitätsinformationen zurück zu Ihrem Geschäft
5. Kunde wird automatisch angemeldet

Bei der ersten Anmeldung wird ein neues Kundenkonto automatisch mit ihrer E-Mail-Adresse und Profilinformationen vom Anbieter erstellt.

## Unterstützte Anbieter

Spwig unterstützt drei große OAuth-Anbieter:

| Anbieter | Verwendungszweck | Anmeldeinformationen-Anforderungen |
|----------|----------------|------------------------|
| **Google** | Beliebtester Anbieter, einfachste Einrichtung | Client ID, Client Secret |
| **Apple** | Erforderlich für iOS-Apps, datenschutzorientiert | Client ID, Team ID, Key ID, Private Key |
| **Microsoft** | Unternehmenskunden, Office 365-Nutzer | Client ID, Client Secret, Tenant ID |

Sie können einen, zwei oder alle drei Anbieter aktivieren. Jeder funktioniert unabhängig.

## Einrichten von Google OAuth

Google OAuth ist die beliebteste Option und am einfachsten einzurichten.

### Voraussetzungen

- Ein Google-Konto
- Zugang zur Google Cloud Console

### Schritt-für-Schritt-Einrichtung

1. **Navigieren Sie zu den OAuth-Einstellungen**
   - Gehen Sie zu **Einstellungen > Geschäftseinstellungen** in Ihrem Admin-Panel
   - Scrollen Sie zu dem Abschnitt **OAuth-Anbieter**
   - Klicken Sie auf **Google konfigurieren**

2. **Erstellen Sie ein Google Cloud Projekt**
   - Besuchen Sie [Google Cloud Console](https://console.cloud.google.com/)
   - Klicken Sie auf **Projekt erstellen**
   - Geben Sie einen Projektnamen ein (z. B. "Mein Geschäft OAuth")
   - Klicken Sie auf **Erstellen**

3. **Aktivieren Sie die Google+ API**
   - In der linken Seitenleiste, gehen Sie zu **APIs & Services > Bibliothek**
   - Suchen Sie nach "Google+ API"
   - Klicken Sie auf **Aktivieren**

4. **Erstellen Sie OAuth-Anmeldeinformationen**
   - Gehen Sie zu **APIs & Services > Anmeldeinformationen**
   - Klicken Sie auf **Anmeldeinformationen erstellen > OAuth-Client-ID**
   - Wählen Sie Anwendungstyp: **Webanwendung**
   - Geben Sie einen Namen ein (z. B. "Geschäftsanmeldung")

5. **Konfigurieren Sie die Umleitungs-URI**
   - Unter **Erlaubte Umleitungs-URIs** fügen Sie hinzu:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Ersetzen Sie `yourdomain.com` mit Ihrem tatsächlichen Domain
   - Klicken Sie auf **Erstellen**

6. **Kopieren Sie die Anmeldeinformationen**
   - Kopieren Sie die **Client ID** und **Client Secret** aus dem Pop-up

7. **Geben Sie die Anmeldeinformationen in Spwig ein**
   - Gehen Sie zurück zu den OAuth-Einstellungen in Ihrem Spwig-Admin
   - Fügen Sie die Client ID und Client Secret ein
   - Klicken Sie auf **Speichern**
   - Schalten Sie **Google OAuth aktivieren** um, um es zu aktivieren

### Testen

- Besuchen Sie die Anmeldeseite Ihres Geschäftsgeschäfts
- Suchen Sie nach der Schaltfläche "Mit Google anmelden"
- Klicken Sie darauf und authentifizieren Sie sich mit Ihrem Google-Konto
- Sie sollten angemeldet und zur Kunden-Dashboard weitergeleitet werden

## Einrichten von Apple OAuth

Apple OAuth ist komplexer als Google aufgrund seines Schlüsselbasierten Authentifizierungssystems.

### Voraussetzungen

- Ein Apple Developer-Konto (bezahlte Mitgliedschaft erforderlich)
- Zugang zum Apple Developer-Portal

### Schritt-für-Schritt-Einrichtung

1. **Navigieren Sie zu den OAuth-Einstellungen**
   - Gehen Sie zu **Einstellungen > Geschäftseinstellungen > OAuth-Anbieter**
   - Klicken Sie auf **Apple konfigurieren**

2. **Erstellen Sie eine Service ID**
   - Melden Sie sich bei [Apple Developer](https://developer.apple.com/account/) an
   - Gehen Sie zu **Zertifikate, Identifiers & Profile**
   - Klicken Sie auf **Identifiers** und dann auf den **+**-Button
   - Wählen Sie **Service IDs** und klicken Sie auf **Weiter**
   - Geben Sie eine Beschreibung ein (z. B. "Geschäftsanmeldung")
   - Geben Sie eine Identifier ein (z. B., `com.yourstore.login`)
   - Klicken Sie auf **Weiter** und dann auf **Registrieren**

3. **Konfigurieren Sie die Service ID**
   - Klicken Sie auf Ihre neu erstellte Service ID
   - Aktivieren Sie **Mit Apple anmelden**
   - Klicken Sie auf **Konfigurieren**
   - Fügen Sie Ihre Domain und Rückgabeverknüpfung hinzu:
     - **Domains**: `yourdomain.com`
     - **Rückgabeverknüpfungen**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Klicken Sie auf **Speichern** und dann auf **Weiter** und **Speichern** nochmals

4. **Erstellen Sie einen Schlüssel**
   - In der linken Seitenleiste, klicken Sie auf **Keys** und dann auf den **+**-Button
   - Geben Sie einen Schlüsselnamen ein (z. B. "Geschäfts OAuth-Schlüssel")
   - Aktivieren Sie **Mit Apple anmelden**
   - Klicken Sie auf **Konfigurieren** und wählen Sie Ihre Primäre App ID aus
   - Klicken Sie auf **Speichern**, dann auf **Weiter** und **Registrieren**
   - **Laden Sie die Schlüsseldatei herunter** (.p8) — Sie können sie nicht erneut herunterladen

5. **Sammeln Sie die erforderlichen Informationen**
   Sie benötigen:
   - **Client ID** (Service ID): Die Identifier, die Sie erstellt haben (z. B., `com.yourstore.login`)
   - **Team ID**: In der oberen rechten Ecke des Apple Developer-Portals gefunden
   - **Key ID**: Angezeigt, wenn Sie den Schlüssel erstellt haben
   - **Private Key**: Der Inhalt der heruntergeladenen .p8-Datei

6. **Geben Sie die Anmeldeinformationen in Spwig ein**
   - Gehen Sie zurück zu den OAuth-Einstellungen in Ihrem Spwig-Admin
   - Fügen Sie die Client ID, Team ID und Key ID ein
   - Öffnen Sie die .p8-Datei in einem Texteditor und kopieren Sie deren Inhalt
   - Fügen Sie den gesamten Schlüssel (einschließlich Header) in das Feld Private Key ein
   - Klicken Sie auf **Speichern**
   - Schalten Sie **Apple OAuth aktivieren** um, um es zu aktivieren

### Testen

- Besuchen Sie die Anmeldeseite Ihres Geschäftsgeschäfts auf einem Gerät mit Apple ID
- Klicken Sie auf "Mit Apple anmelden"
- Authentifizieren Sie sich mit Ihrer Apple ID
- Sie sollten erfolgreich angemeldet werden

## Einrichten von Microsoft OAuth

Microsoft OAuth ist ideal für Geschäfte, die auf Geschäftsbenutzer abzielen, die Office 365 oder Azure AD verwenden.

### Voraussetzungen

- Ein Microsoft-Konto
- Zugang zum Azure-Portal

### Schritt-für-Schritt-Einrichtung

1. **Navigieren Sie zu den OAuth-Einstellungen**
   - Gehen Sie zu **Einstellungen > Geschäftseinstellungen > OAuth-Anbieter**
   - Klicken Sie auf **Microsoft konfigurieren**

2. **Registrieren Sie eine Anwendung in Azure**
   - Besuchen Sie [Azure-Portal](https://portal.azure.com/)
   - Gehen Sie zu **Azure Active Directory > App-Registrierungen**
   - Klicken Sie auf **Neue Registrierung**
   - Geben Sie einen Namen ein (z. B. "Geschäfts OAuth")
   - Wählen Sie **Konten in jedem organisatorischen Verzeichnis und persönliche Microsoft-Konten**
   - Unter **Umleitungs-URI** wählen Sie **Web** und geben Sie ein:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Klicken Sie auf **Registrieren**

3. **Kopieren Sie die Anwendungs-ID**
   - Auf der Übersichtsseite der Anwendung kopieren Sie die **Anwendungs-ID (Client-ID)**

4. **Erstellen Sie einen Client-Schlüssel**
   - In der linken Seitenleiste klicken Sie auf **Zertifikate & Geheimnisse**
   - Klicken Sie auf **Neues Client-Geheimnis**
   - Geben Sie eine Beschreibung ein (z. B. "OAuth-Geheimnis")
   - Wählen Sie eine Ablaufzeit (empfohlen: 24 Monate)
   - Klicken Sie auf **Hinzufügen**
   - **Kopieren Sie den Geheimniswert sofort** — er wird nicht erneut angezeigt

5. **Geben Sie die Anmeldeinformationen in Spwig ein**
   - Gehen Sie zurück zu den OAuth-Einstellungen in Ihrem Spwig-Admin
   - Fügen Sie die Anwendungs-ID (Client-ID) als Client-ID ein
   - Fügen Sie den Geheimniswert als Client-Secret ein
   - Geben Sie optional eine Tenant-ID ein (für Einzelmandant-Apps; lassen Sie sie leer für Multi-Mandant)
   - Klicken Sie auf **Speichern**
   - Schalten Sie **Microsoft OAuth aktivieren** um, um es zu aktivieren

### Testen

- Besuchen Sie die Anmeldeseite Ihres Geschäftsgeschäfts
- Klicken Sie auf "Mit Microsoft anmelden"
- Authentifizieren Sie sich mit Ihrem Microsoft-Konto
- Sie sollten erfolgreich angemeldet werden

## Verwalten von OAuth-Verbindungen

### Kundenansicht

Kunden können ihre verbundenen OAuth-Anbieter von ihrem Kontodashboard ansehen und verwalten:

- Navigieren Sie zu **Mein Konto > Verknüpfte Konten**
- Sehen Sie, welche Anbieter verbunden sind (Google, Apple, Microsoft)
- Trennen Sie einen Anbieter, indem Sie auf **Trennen** klicken
- Verbinden Sie ihn erneut, indem Sie sich mit diesem Anbieter erneut anmelden

### Mehrere Anbieter

Ein einzelnes Kundenkonto kann mit mehreren OAuth-Anbietern verbunden werden. Zum Beispiel kann ein Kunde sowohl Google als auch Apple mit demselben Konto verbinden.

Wenn ein Kunde versucht, sich mit einem anderen OAuth-Anbieter mit der gleichen E-Mail-Adresse anzumelden, verbindet Spwig es automatisch mit ihrem bestehenden Konto.

### Admin-Verwaltung

Als Administrator können Sie die OAuth-Verbindungen der Kunden einsehen:

- Gehen Sie zu **Kunden > Kunden**
- Öffnen Sie ein Kundenprofil
- Scrollen Sie zu dem Abschnitt **Verknüpfte Konten**
- Sehen Sie, welche Anbieter verbunden sind und wann sie verbunden wurden

Sie können keine Anbieter im Namen der Kunden trennen — sie müssen es selbst tun, aus Sicherheitsgründen.

## Problembehandlung

### Umleitungs-URI-Mismatch

**Fehler**: "Umleitungs-URI-Mismatch" oder "Ungültiger redirect_uri"

**Lösung**:
- Stellen Sie sicher, dass der Umleitungs-URI in Ihren Anbieter-Einstellungen exakt mit dem in Spwig übereinstimmt
- Prüfen Sie auf Schlussstriche — sie müssen übereinstimmen
- Stellen Sie sicher, dass Sie `https://` verwenden (nicht `http://`)
- Löschen Sie den Cache Ihres Browsers und versuchen Sie es erneut

### Ungültige Anmeldeinformationen

**Fehler**: "Ungültige Client ID" oder "Authentifizierung fehlgeschlagen"

**Lösung**:
- Stellen Sie sicher, dass Sie die Client ID und Client Secret korrekt kopiert haben
- Stellen Sie sicher, dass keine zusätzlichen Leerzeichen oder Zeilenumbrüche vorhanden sind
- Prüfen Sie, ob die Anmeldeinformationen aus dem richtigen Projekt/App stammen
- Für Apple stellen Sie sicher, dass der Private Key den vollständigen Inhalt der .p8-Datei enthält

### API des Anbieters nicht aktiviert

**Fehler**: "API nicht aktiviert" oder "Zugriff nicht konfiguriert"

**Lösung**:
- Für Google: Stellen Sie sicher, dass Sie die Google+ API in Ihrem Google Cloud Projekt aktiviert haben
- Für Microsoft: Prüfen Sie, ob Ihre App-Registrierung genehmigt und aktiv ist
- Für Apple: Prüfen Sie, ob "Mit Apple anmelden" für Ihre Service ID aktiviert ist

### SSL erforderlich

**Fehler**: "OAuth erfordert HTTPS" oder "Unsicherer Umleitungs-URI"

**Lösung**:
- OAuth-Anbieter erfordern SSL/TLS (HTTPS) für Sicherheit
- Stellen Sie sicher, dass Ihr Geschäft eine gültige SSL-Zertifikat installiert hat
- Aktualisieren Sie Ihre Umleitungs-URIs, um `https://` anstelle von `http://` zu verwenden
- Wenn Sie lokal testen, verwenden Sie einen Dienst wie ngrok, um einen HTTPS-Tunnel zu erstellen

### Schaltfläche erscheint nicht

**Problem**: Die Schaltfläche "Mit Google/Apple/Microsoft anmelden" erscheint nicht auf der Anmeldeseite

**Lösung**:
- Stellen Sie sicher, dass der Anbieter in den OAuth-Einstellungen aktiviert ist
- Löschen Sie den Cache Ihres Browsers und aktualisieren Sie die Seite
- Prüfen Sie, ob Ihr Theme die Vorlage für die soziale Anmeldung enthält
- Prüfen Sie den Browser-Konsolen-Log für JavaScript-Fehler

## Tipps und beste Praktiken

### Sicherheit

- **Drehen Sie Geheimnisse regelmäßig** — Aktualisieren Sie Client Secrets alle 12-24 Monate
- **Überwachen Sie fehlgeschlagene Anmeldeversuche** — Achten Sie auf ungewöhnliche Authentifizierungs-Muster
- **Verwenden Sie separate Anmeldeinformationen pro Umgebung** — Unterschiedliche Anmeldeinformationen für Test- und Produktionsumgebung
- **Einschränken Sie Umleitungs-URIs** — Fügen Sie nur die genauen URIs hinzu, die Sie benötigen

### Benutzererfahrung

- **Aktivieren Sie alle drei Anbieter** — Geben Sie Kunden die Wahl; verschiedene Demografien bevorzugen verschiedene Anbieter
- **Platzieren Sie die Schaltflächen auffällig** — Soziale Anmeldungsschaltflächen sollten über dem E-Mail/Passwort-Formular platziert werden
- **Verwenden Sie erkennbare Branding** — Behalten Sie die Standard-Schaltflächenstile von Google/Apple/Microsoft
- **Testen Sie auf Mobilgeräten** — OAuth-Flüsse funktionieren anders auf mobilen Browsern

### Einhaltung

- **Datenschutzrichtlinie** — Offenbaren Sie, dass Sie OAuth-Anbieter verwenden und welche Daten Sie erhalten
- **Nutzungsbedingungen** — Einhalten Sie die Anbieterbedingungen (Google, Apple, Microsoft haben jeweils Anforderungen)
- **Datenminimierung** — Fordern Sie nur die Profilinformationen an, die Sie tatsächlich benötigen

### Test-Checkliste

Bevor Sie online gehen, testen Sie:

- [ ] Anmeldung mit jedem Anbieter auf dem Desktop
- [ ] Anmeldung mit jedem Anbieter auf dem Mobilgerät
- [ ] Erstmalige Anmeldung (Kontenerstellung)
- [ ] Nachfolgende Anmeldungen (Kontoverknüpfung)
- [ ] Anmeldung mit derselben E-Mail-Adresse über verschiedene Anbieter
- [ ] Trennen und erneut Verknüpfen eines Anbieters
- [ ] Passwort-Reset-Fluss funktioniert weiterhin für Nicht-OAuth-Nutzer

