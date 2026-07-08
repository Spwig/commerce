---
title: 'SSO-Setup: Microsoft Entra ID'
---

Dieser Leitfaden führt Sie durch den Prozess, Spwig mit Microsoft Entra ID (früher Azure Active Directory) für die Einzelanmeldung (Single Sign-On) der Administratoren zu verbinden. Nach der Konfiguration können Ihre Mitarbeiter sich mit ihrem Microsoft-Arbeitskonto am Spwig-Administrationspanel anmelden.

**Hinweis:** Microsoft kann die Benutzeroberfläche des Entra-Administrationscenters im Laufe der Zeit aktualisieren. Diese Anweisungen wurden basierend auf der Oberfläche aus dem Jahr 2026 erstellt. Falls sich einige Schritte von dem unterscheiden, was Sie sehen, beziehen Sie sich auf die offizielle Microsoft-Dokumentation zu [der Registrierung einer Anwendung mit der Microsoft Identity-Plattform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Voraussetzungen

- Ein Azure-Abonnement mit Zugriff auf Microsoft Entra ID
- **Anwendungsadministrator**- oder **Globaler Administrator**-Rolle in Ihrem Entra ID-Mandanten
- Ihre Spwig-Store-URL (z. B. `https://your-store.com`)
- Mitarbeiter müssen in Spwig E-Mail-Adressen haben, die mit ihren Microsoft-Konten übereinstimmen

## Schritt 1: Anwendung registrieren

1. Melden Sie sich beim [Microsoft Entra-Administrationscenter](https://entra.microsoft.com) an
2. Navigieren Sie zu **Identität > Anwendungen > App-Registrierungen**
3. Klicken Sie auf **Neue Registrierung**
4. Konfigurieren Sie die Registrierung:

| Feld | Wert |
|-------|-------|
| **Name** | `Spwig Admin SSO` (oder einen beliebigen Namen Ihrer Wahl) |
| **Unterstützte Kontotypen** | **Nur Konten in diesem organisatorischen Verzeichnis** (Ein-Mandant) |
| **Umleitungs-URI** | Plattform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Klicken Sie auf **Registrieren**

**Wichtig:** Der Umleitungs-URI muss genau `https://your-store.com/oidc/callback/` entsprechen — einschließlich des Schlussstrichs. Ersetzen Sie `your-store.com` durch Ihre tatsächliche Store-Domain.

## Schritt 2: Anwendungs-IDs notieren

Nach der Registrierung sehen Sie die **Übersicht**-Seite der Anwendung. Notieren Sie diese beiden Werte — Sie benötigen sie später:

| Wert | Wo Sie ihn finden | Zweck |
|-------|-----------------|---------------|
| **Anwendung (Client)-ID** | Übersichtsseite, oberer Abschnitt | Geben Sie dies als **Client ID** in Spwig ein |
| **Verzeichnis (Mandant)-ID** | Übersichtsseite, oberer Abschnitt | Wird verwendet, um die Discovery-URL zu erstellen |

## Schritt 3: Client-Secret erstellen

1. In der Anwendungsregistrierung navigieren Sie zu **Zertifikate & Geheimnisse**
2. Klicken Sie auf **Neues Client-Geheimnis**
3. Geben Sie eine Beschreibung ein (z. B. `Spwig SSO`) und wählen Sie eine Ablaufzeit
4. Klicken Sie auf **Hinzufügen**
5. **Kopieren Sie den Wert sofort** — er wird nur einmal angezeigt. Dies ist das Client-Geheimnis, das Sie in Spwig eingeben.

**Kopieren Sie nicht die Geheimnis-ID** — Sie benötigen die **Wert**-Spalte, nicht die ID-Spalte.

**Erstellen Sie eine Erinnerung**, um das Geheimnis vor Ablauf zu rotieren. Wenn ein Geheimnis abgelaufen ist, funktioniert die SSO nicht mehr, bis Sie ein neues erstellen und es in Spwig aktualisieren.

## Schritt 4: API-Berechtigungen konfigurieren

1. Navigieren Sie zu **API-Berechtigungen**
2. Stellen Sie sicher, dass **Microsoft Graph > User.Read** (delegiert) aufgelistet ist. Dies wird standardmäßig hinzugefügt.
3. Wenn die Berechtigungen `openid`, `email` und `profile` nicht aufgelistet sind, klicken Sie auf **Berechtigung hinzufügen > Microsoft Graph > Delegierte Berechtigungen** und fügen Sie sie hinzu.
4. Klicken Sie auf **Admin-Berechtigung für [Ihre Organisation] erteilen**, wenn Sie dazu aufgefordert werden.

## Schritt 5: Discovery-URL erstellen

Die OIDC-Discovery-URL folgt diesem Format:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Ersetzen Sie `{tenant-id}` durch die **Verzeichnis (Mandant)-ID** aus Schritt 2.

Beispiel: Wenn Ihre Mandant-ID `a1b2c3d4-e5f6-7890-abcd-ef1234567890` ist, lautet die Discovery-URL:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Schritt 6: Gruppenansprüche konfigurieren (optional)

Wenn Sie möchten, dass Spwig Mitarbeiter- oder Superuser-Zustände basierend auf der Mitgliedschaft in Entra ID-Gruppen automatisch zuweist:

1. In der Anwendungsregistrierung navigieren Sie zu **Tokenkonfiguration**
2. Klicken Sie auf **Gruppenanspruch hinzufügen**
3. Wählen Sie die Gruppentypen aus, die Sie einbeziehen möchten (meist **Sicherheitsgruppen**)
4. Unter **Tokeneigenschaften nach Typ anpassen**, für den **ID**-Token, wählen Sie **Gruppen-ID**
5. Klicken Sie auf **Hinzufügen**

**Wichtig:** Entra ID sendet Gruppen-**Object IDs** (UUIDs wie `a1b2c3d4-...`), nicht Gruppen-Bezeichnungen.

Bei der Konfiguration der Rolle Zuordnung in Spwig müssen Sie diese Object IDs verwenden.

Um die Object ID einer Gruppe zu finden:
1. Im Entra-Verwaltungscenter navigieren Sie zu **Identity > Groups > All groups**
2. Klicken Sie auf die Gruppe
3. Kopieren Sie die **Object ID** von der Übersichtsseite der Gruppe

### Gruppenlimit

Microsoft Entra ID enthält maximal **200 Gruppen** im Token. Wenn ein Benutzer mehr als 200 Gruppen angehört, wird der Gruppenanspruch durch einen Link zur Microsoft Graph API ersetzt. Für Organisationen mit vielen Gruppen, erwägen Sie die Erstellung einer dedizierten Sicherheitsgruppe für den Spwig-Zugriff und die Verwendung von [Gruppenfilterung](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference), um festzulegen, welche Gruppen einbezogen werden.

## Schritt 7: In Spwig konfigurieren

1. In der Spwig-Verwaltung navigieren Sie zu **Enterprise SSO > SSO Provider Configuration**
2. Legen Sie **Provider Name** auf `Microsoft Entra ID` fest
3. Fügen Sie die Discovery-URL aus Schritt 5 in **OIDC Discovery URL** ein
4. Klicken Sie auf **Auto-Discover** – dies füllt alle Endpunkt-Felder automatisch aus
5. Geben Sie die **Client ID** aus Schritt 2 ein
6. Geben Sie den **Client Secret** (Wert) aus Schritt 3 ein
7. Wenn Sie Gruppenansprüche in Schritt 6 konfiguriert haben:
   - Legen Sie **Groups Claim** auf `groups` fest
   - Geben Sie in **Staff Groups** die Object IDs der Gruppen ein, deren Mitglieder als Mitarbeiter gelten sollen (kommagetrennt)
   - Geben Sie in **Superuser Groups** die Object IDs der Gruppen ein, deren Mitglieder als Superuser gelten sollen (kommagetrennt)
8. Klicken Sie auf **Save**

## Schritt 8: Aktivieren und Testen

1. Navigieren Sie zu **Site Settings > Security**-Registerkarte
2. Aktivieren Sie **Enable SSO for admin login**
3. Klicken Sie auf **Save**
4. Öffnen Sie die Admin-Anmeldeseite in einem **privaten/incognito-Fenster**
5. Sie sollten eine **Sign in with Microsoft Entra ID**-Schaltfläche sehen
6. Klicken Sie darauf – Sie sollten zur Microsoft-Anmeldeseite weitergeleitet werden
7. Melden Sie sich mit einem Microsoft-Konto an, dessen E-Mail-Adresse einer Mitarbeiterin oder einem Mitarbeiter in Spwig entspricht
8. Sie sollten zur Spwig-Admin-Startseite weitergeleitet werden

## Häufige Probleme

| Problem | Ursache | Lösung |
|---------|-------|----------|
| **AADSTS50011: Die Umleitungs-URI stimmt nicht überein** | Die Umleitungs-URI in Entra stimmt nicht exakt überein | Stellen Sie sicher, dass die Umleitungs-URI `https://your-store.com/oidc/callback/` mit dem Schlussstrich ist. Prüfen Sie auf einen Unterschied zwischen HTTP und HTTPS. |
| **AADSTS700016: Anwendung nicht gefunden** | Falsche Client ID oder Mandant | Überprüfen Sie die Client ID und stellen Sie sicher, dass die Discovery-URL die richtige Mandant-ID verwendet |
| **Anmeldung bei Microsoft ist erfolgreich, aber bei Spwig nicht** | Kein passender Benutzer in Spwig | Stellen Sie sicher, dass ein Mitarbeiterkonto in Spwig mit der gleichen E-Mail-Adresse wie das Microsoft-Konto vorhanden ist. Prüfen Sie, ob der Benutzer den Mitarbeiterstatus hat, wenn „Nur Mitarbeiter“ aktiviert ist. |
| **Gruppenanspruch ist leer** | Gruppenansprüche nicht konfiguriert | Folgen Sie Schritt 6, um einen Gruppenanspruch in der Token-Konfiguration hinzuzufügen |
| **Gruppenanspruch gibt eine URL anstelle von IDs zurück** | Benutzer ist in mehr als 200 Gruppen | Verwenden Sie Gruppenfilterung, um die Gruppen im Token zu begrenzen, oder weisen Sie spezifische Gruppen zu |
| **SSO funktioniert nach einigen Monaten nicht mehr** | Client Secret abgelaufen | Erstellen Sie ein neues Client Secret in Entra und aktualisieren Sie es in der SSO Provider Configuration von Spwig |

## Tipps

- **Verwenden Sie Sicherheitsgruppen** für die Rollenzuordnung, nicht Microsoft 365-Gruppen oder Verteilerlisten.

Sicherheitsgruppen sind für Zugriffssteuerung konzipiert und arbeiten am zuverlässigsten mit OIDC-Ansprüchen.
- **Einzelmandant ist empfohlen** – das Auswählen von „Konten in diesem organisatorischen Verzeichnis nur“ beschränkt SSO auf Ihre Organisationenbenutzer.

Mehrmmandant-Konfigurationen erfordern zusätzliche Validierung.
- **Setzen Sie eine lange Geheimnis-Ablaufzeit** – wählen Sie 24 Monate, wenn Sie das Client Secret erstellen, und setzen Sie einen Kalendererinnerung bei 22 Monaten, um es zu rotieren.
- **Bedingte Zugriff** – Sie können in Entra ID bedingte Zugriffspolitiken erstellen, die speziell für die App-Registrierung von Spwig gelten.

Zum Beispiel können Sie MFA erzwingen, Anmeldungen von unvertrauten Standorten blockieren oder die Verwendung komplizierter Geräte erzwingen.
- **Mit einem Nicht-Admin-Konto testen** — erstellen Sie ein Test-Staff-Konto in Spwig, um sicherzustellen, dass SSO funktioniert, bevor Sie es für Ihr gesamtes Team bereitstellen.