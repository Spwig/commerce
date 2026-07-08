---
title: 'SSO-Setup: Google Workspace'
---

Dieser Leitfaden führt Sie durch den Prozess, Spwig mit Google Workspace für die Einzelanmeldung (Single Sign-On) für Administratoren zu verbinden. Nach der Konfiguration können Ihre Mitarbeiter sich mit ihrem Google Workspace-Konto am Spwig-Admin-Panel anmelden.

**Hinweis:** Google kann die Oberfläche des Cloud Console im Laufe der Zeit aktualisieren. Diese Anweisungen wurden basierend auf der Oberfläche aus dem Jahr 2026 erstellt. Falls sich einige Schritte von dem unterscheiden, was Sie sehen, beziehen Sie sich auf die offizielle Dokumentation von Google zu [OAuth 2.0 einrichten](https://support.google.com/cloud/answer/6158849).

## Voraussetzungen

- Eine Google Workspace-Abonnement (Google Workspace Business, Enterprise oder Education)
- Administratorzugriff auf die [Google Cloud Console](https://console.cloud.google.com)
- Ihre Spwig-Store-URL (z. B. `https://your-store.com`)
- Mitarbeiter müssen E-Mail-Adressen in Spwig haben, die mit ihren Google Workspace-Konten übereinstimmen

## Schritt 1: Erstellen oder Auswählen eines Google Cloud-Projekts

1. Gehen Sie zu der [Google Cloud Console](https://console.cloud.google.com)
2. Klicken Sie auf den Projektauswahl-Button in der oberen Leiste
3. Klicken Sie auf **Neues Projekt** (oder wählen Sie ein bestehendes Projekt, wenn Sie möchten)
4. Geben Sie einen Projektnamen ein (z. B. `Spwig SSO`)
5. Wählen Sie Ihre Organisation aus
6. Klicken Sie auf **Erstellen**

## Schritt 2: Konfigurieren des OAuth-Zustimmungsscreens

1. In der Cloud Console navigieren Sie zu **APIs & Services > OAuth-Zustimmungsscreen**
2. Wählen Sie **Intern** als Benutzertyp – dies beschränkt die Anmeldung auf Benutzer innerhalb Ihrer Google Workspace-Organisation
3. Klicken Sie auf **Erstellen**
4. Füllen Sie die erforderlichen Felder aus:

| Feld | Wert |
|-------|-------|
| **App-Name** | `Spwig Admin` (oder der Name Ihres Stores) |
| **Support-E-Mail für Benutzer** | Ihre Administrator-E-Mail-Adresse |
| **Erlaubte Domänen** | `your-store.com` (Ihr Stores-Domäne, ohne `https://`) |
| **Entwicklerkontakt-E-Mail** | Ihre Administrator-E-Mail-Adresse |

5. Klicken Sie auf **Speichern und Weiter**
6. Auf der Seite **Bereiche** klicken Sie auf **Bereiche hinzufügen oder entfernen** und fügen Sie hinzu:
   - `openid`
   - `email`
   - `profile`
7. Klicken Sie auf **Speichern und Weiter**
8. Überprüfen Sie die Zusammenfassung und klicken Sie auf **Zurück zur Dashboard**

## Schritt 3: Erstellen von OAuth-Anmeldeinformationen

1. Navigieren Sie zu **APIs & Services > Anmeldeinformationen**
2. Klicken Sie auf **Erstellen von Anmeldeinformationen > OAuth-Client-ID**
3. Konfigurieren Sie den Client:

| Feld | Wert |
|-------|-------|
| **Anwendungstyp** | Webanwendung |
| **Name** | `Spwig SSO` |
| **Erlaubte Umleitungs-URIs** | `https://your-store.com/oidc/callback/` |

4. Klicken Sie auf **Erstellen**
5. Ein Dialogfenster zeigt Ihre **Client-ID** und **Client-Secret** an – kopieren Sie beide Werte. Sie können sie auch als JSON herunterladen, um sie sicher aufzubewahren.

**Wichtig:** Die Umleitungs-URI muss exakt `https://your-store.com/oidc/callback/` entsprechen – einschließlich des Schlussstrichs und des `https://`-Schemas. Ersetzen Sie `your-store.com` durch Ihre tatsächliche Store-Domäne.

## Schritt 4: Erhalten der Discovery-URL

Google verwendet eine einzelne, standardisierte Discovery-URL für alle Workspace-Mietverhältnisse:

```
https://accounts.google.com/.well-known/openid-configuration
```

Diese URL ist für jede Google Workspace-Organisation gleich – Sie müssen sie nicht mit einem Mietverhältnis oder einer Domäne anpassen.

## Schritt 5: Konfigurieren in Spwig

1. In der Spwig-Administration navigieren Sie zu **Enterprise SSO > SSO-Provider-Konfiguration**
2. Setzen Sie **Provider-Name** auf `Google Workspace`
3. Geben Sie die Discovery-URL ein: `https://accounts.google.com/.well-known/openid-configuration`
4. Klicken Sie auf **Automatisch entdecken** – dies füllt alle Endpunkt-Felder automatisch aus
5. Geben Sie die **Client-ID** aus Schritt 3 ein
6. Geben Sie das **Client-Secret** aus Schritt 3 ein
7. Klicken Sie auf **Speichern**

### Zuordnung von Ansprüchen

Google verwendet standardisierte OIDC-Anspruchsnamen, daher funktioniert die Standardkonfiguration in Spwig sofort:

| Spwig-Einstellung | Google-Anspruch | Standardwert |
|---------------|-------------|---------------|
| E-Mail-Anspruch | `email` | `email` |
| Vorname-Anspruch | `given_name` | `given_name` |
| Nachname-Anspruch | `family_name` | `family_name` |

Es sind keine Änderungen der Anspruchszuordnung erforderlich.

## Schritt 6: Aktivieren und Testen

1.

Navigieren Sie zu **Site Settings > Security**-Registerkarte
2.

Aktivieren Sie **SSO für Admin-Anmeldung**
3.

Klicken Sie auf **Speichern**
4.



Öffnen Sie die Admin-Anmeldeseite in einem **privaten/incognito-Fenster**
5.

Sie sollten eine **Mit Google Workspace anmelden**-Schaltfläche sehen
6.

Klicken Sie darauf – Sie sollten zur Google-Anmeldeseite weitergeleitet werden
7.

Melden Sie sich mit einem Google Workspace-Konto an, dessen E-Mail-Adresse einer Mitarbeiterin oder einem Mitarbeiter in Spwig entspricht
8.

Sie sollten zur Spwig-Admin-Übersicht weitergeleitet werden

## Gruppenbasierte Rollenzuordnung

Im Gegensatz zu Microsoft Entra ID oder Okta enthält Google standardmäßig keine Gruppenmitgliedschaft in den OIDC-Token. Die Implementierung von Gruppenansprüchen mit Google erfordert die Google Workspace Directory API und eine zusätzliche Konfiguration jenseits der grundlegenden OIDC-Einstellungen.

Für die meisten Google Workspace-Bereitstellungen empfehlen wir, die Mitarbeiter- und Superuser-Berechtigungen direkt in Spwig zu verwalten, anstatt sie über eine automatische Rollenzuordnung vorzunehmen:

1. Erstellen Sie Mitarbeiterkonten in Spwig mit den entsprechenden Berechtigungen
2. Verwenden Sie das Spwig-System für Mitarbeiterrollen, um Zugriffslevels zu steuern
3. Mitarbeiter melden sich über SSO an, und Spwig verwendet ihre bestehenden Berechtigungen

Wenn Sie eine automatische, gruppenbasierte Rollenzuordnung benötigen, konsultieren Sie die [Google Workspace Admin SDK Directory API-Dokumentation](https://developers.google.com/admin-sdk/directory), um benutzerdefinierte Ansprüche zu konfigurieren.

## Häufige Probleme

| Problem | Ursache | Lösung |
|---------|-------|----------|
| **Fehler 400: redirect_uri_mismatch** | Die Umleitungs-URI in Google Cloud stimmt nicht exakt überein | Stellen Sie sicher, dass die Umleitungs-URI `https://your-store.com/oidc/callback/` mit dem Schlussstrich ist. Prüfen Sie HTTP vs HTTPS. |
| **Fehler 403: access_denied** | Der Benutzer gehört nicht zur Google Workspace-Organisation | Mit dem Benutzertyp "Internal" können nur Benutzer aus Ihrer Organisation sich anmelden. Stellen Sie sicher, dass das Benutzerkonto Teil Ihres Workspace-Domains ist. |
| **OAuth-Bestätigungsbildschirm zeigt "Diese App ist nicht verifiziert" an** | Normal für interne Apps | Dieser Hinweis ist für interne Apps erwartet und beeinflusst die Funktionalität nicht. Benutzer in Ihrer Organisation können sich dennoch anmelden. |
| **Anmeldung bei Google ist erfolgreich, aber bei Spwig fehlschlägt** | Kein passender Benutzer in Spwig | Stellen Sie sicher, dass ein Mitarbeiterkonto in Spwig mit der gleichen E-Mail-Adresse wie das Google Workspace-Konto vorhanden ist. Prüfen Sie, ob "Auf Mitarbeiter beschränken" richtig konfiguriert ist. |
| **"Zugriff blockiert: Diese Anfrage der App ist ungültig"** | Scopes nicht ordnungsgemäß konfiguriert | Stellen Sie sicher, dass die Scopes `openid`, `email` und `profile` zur OAuth-Bestätigungsbildschirm hinzugefügt wurden. |

## Tipps

- **Benutzen Sie den Benutzertyp "Internal"** – dies beschränkt die Anmeldung auf Ihre Google Workspace-Organisation und erfordert nicht den Verifikationsprozess von Googles App.
- **Google-Client-Schlüssel verlieren nicht ihre Gültigkeit** – im Gegensatz zu Microsoft Entra ID haben Google OAuth-Client-Schlüssel keine Ablaufdatum. Sie können sie jedoch jederzeit von der Credentials-Seite rotieren.
- **Ein Projekt für mehrere Apps** – Sie können mehrere OAuth-Client-IDs innerhalb des gleichen Google Cloud-Projekts erstellen, wenn Sie mehrere Spwig-Installationen haben.
- **Testen Sie mit einem Nicht-Admin-Konto** – erstellen Sie ein Test-Mitarbeiterkonto in Spwig und verwenden Sie einen regulären Google Workspace-Benutzer (nicht einen Superadmin), um sicherzustellen, dass SSO wie erwartet funktioniert.