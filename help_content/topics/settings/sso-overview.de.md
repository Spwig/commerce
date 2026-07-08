---
title: Einzelner Anmelde-Identitätsprovider (SSO)
---

Single Sign-On (SSO) ermöglicht es Ihrem Personal, sich mit Ihrem Organisations-Identitätsanbieter anzumelden, anstatt einen separaten Benutzernamen und Passwort zu verwenden. Spwig unterstützt jeden Identitätsanbieter, der das OpenID Connect (OIDC)-Protokoll verwendet, einschließlich Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak und anderer.

## Was ist Enterprise SSO?

Enterprise SSO unterscheidet sich von sozialer Anmeldung (Anmeldung mit einem persönlichen Google- oder Facebook-Konto). Mit Enterprise SSO:

- Das Personal authentifiziert sich über den **Identitätsanbieter Ihrer Organisation** – denselben System, den sie für E-Mail, interne Tools und andere Geschäftsanwendungen verwenden
- Ihr IT-Team kontrolliert den Zugriff zentral – wenn jemand die Organisation verlässt, wird das Deaktivieren seines Kontos beim Identitätsanbieter sofort den Zugriff auf Spwig entziehen
- Mehrfaktor-Authentifizierung (MFA) wird vom Identitätsanbieter erzwungen, was Ihnen eine konsistente Sicherheitsrichtlinie für alle Anwendungen bietet
- Das Personal muss kein separates Passwort für Spwig merken

## Wie funktioniert es

Wenn SSO aktiviert ist, zeigt die Admin-Anmeldeseite eine **Mit [Anbieter] anmelden**-Schaltfläche an. Der Authentifizierungsfluss funktioniert wie folgt:

1. Der Mitarbeiter klickt auf die SSO-Schaltfläche auf der Spwig-Anmeldeseite
2. Sie werden zur Anmeldeseite Ihres Identitätsanbieters weitergeleitet (z. B. Microsoft-Anmeldung)
3. Sie authentifizieren sich beim Identitätsanbieter (einschließlich jeder MFA, die der Anbieter erfordert)
4. Der Identitätsanbieter leitet sie zurück zu Spwig mit einem sicheren Autorisierungscode
5. Spwig tauscht den Code gegen Benutzerinformationen und erstellt eine Sitzung
6. Der Mitarbeiter landet in der Admin-Übersicht, vollständig authentifiziert

Dies verwendet das branchenübliche **OpenID Connect (OIDC)**-Protokoll, das von fast allen Enterprise-Identitätsanbietern unterstützt wird.

## SSO aktivieren

SSO wird an zwei Stellen konfiguriert:

1. **Site-Einstellungen > Sicherheit** – SSO aktivieren oder deaktivieren und die Sichtbarkeit der Passwortanmeldung steuern
2. **SSO-Anbieterkonfiguration** – Geben Sie die OIDC-Daten Ihres Identitätsanbieters ein

### Schritt 1: Konfigurieren Sie Ihren Identitätsanbieter

Bevor Sie SSO in Spwig aktivieren, müssen Sie Spwig als Anwendung in Ihrem Identitätsanbieter registrieren. Siehe die anbieter-spezifischen Anleitungen:

- **Microsoft Entra ID** – siehe den Microsoft Entra ID-Setup-Leitfaden
- **Google Workspace** – siehe den Google Workspace-Setup-Leitfaden
- **Okta** – siehe den Okta-Setup-Leitfaden
- **Andere Anbieter** – Jeder OIDC-konforme Anbieter funktioniert. Registrieren Sie eine Webanwendung mit Umleitungs-URI `https://your-store.com/oidc/callback/` und konsultieren Sie die Dokumentation Ihres Anbieters für die OIDC-Entdeckungs-URL, Client-ID und Client-Secret.

### Schritt 2: Konfigurieren Sie den SSO-Anbieter in Spwig

Navigieren Sie zur **SSO-Anbieterkonfiguration**-Seite (von der Sicherheitstabelle verlinkt oder über **Enterprise SSO > SSO-Anbieterkonfiguration** im Admin-Seitennavigation). Geben Sie ein:

1. **Anbietername** – wird auf der Anmelde-Schaltfläche angezeigt (z. B. „Microsoft Entra ID“)
2. **OIDC-Entdeckungs-URL** – die `.well-known/openid-configuration`-URL Ihres Anbieters. Klicken Sie auf **Automatisch entdecken**, um die Endpunkt-Felder automatisch zu füllen.
3. **Client-ID** und **Client-Secret** – aus der Anwendungregistrierung Ihres Identitätsanbieters

Das Client-Secret wird verschlüsselt gespeichert und wird nach dem Speichern nie wieder angezeigt.

### Schritt 3: SSO in den Site-Einstellungen aktivieren

Navigieren Sie zu **Site-Einstellungen > Sicherheit**-Tab und aktivieren Sie **SSO für Admin-Anmeldung**. Die SSO-Schaltfläche wird sofort auf der Admin-Anmeldeseite angezeigt.

## SSO-Einstellungen

| Einstellung | Beschreibung |
|---------|-------------|
| **SSO für Admin-Anmeldung aktivieren** | Zeigt die SSO-Schaltfläche auf der Admin-Anmeldeseite an. Beeinflusst die normale Passwortanmeldung nicht, es sei denn, Sie deaktivieren sie auch. |
| **Passwortanmeldung auf der Admin-Seite erlauben** | Wenn nicht aktiviert, wird das Passwortformular hinter einem zusammenklappbaren Schalter versteckt. Das Personal sieht standardmäßig nur die SSO-Schaltfläche. Das Passwortformular kann immer noch über Klicken auf „Mit lokalem Konto anmelden“ oder durch Anhängen von `?password=1` an die Anmelde-URL aufgerufen werden. |

### Verhalten der Anmelde-Seite

| SSO aktiviert | Passwortanmeldung | Ergebnis |
|-------------|---------------|--------|
| Aus | An | Standard-Anmeldeseite mit nur dem Benutzernamen-/Passwort-Formular |
| An | An | SSO-Button oben, Trenner "oder", dann Passwort-Formular darunter |
| An | Aus | Nur SSO-Button. Das Passwort-Formular ist hinter einem Schalter "Mit lokalem Konto anmelden" versteckt |
| Aus | Aus | Nicht möglich — Passwortanmeldung wird automatisch wieder aktiviert, wenn SSO deaktiviert oder nicht konfiguriert ist |

## Benutzerzuordnung

Wenn ein Mitarbeiter sich über SSO anmeldet, ordnet Spwig ihn einem bestehenden Benutzerkonto zu, indem es die **E-Mail-Adresse** (fallunterscheidend) verwendet. Die E-Mail aus den Ansprüchen des Identitätsanbieters muss mit der E-Mail des Mitarbeiters auf dem Spwig-Konto übereinstimmen.

Wenn kein passender Benutzer gefunden wird:

- **Automatische Benutzererstellung deaktiviert** (Standard) — die Anmeldung wird abgelehnt. Sie müssen zuerst ein Mitarbeiterkonto in Spwig mit einer passenden E-Mail-Adresse erstellen.
- **Automatische Benutzererstellung aktiviert** — ein neues Benutzerkonto wird automatisch mit dem Namen und der E-Mail aus den Ansprüchen des Identitätsanbieters erstellt.

Die Einstellung **Nur für Mitarbeiter beschränken** (standardmäßig aktiviert) fügt eine zusätzliche Prüfung hinzu: selbst wenn ein Benutzerkonto vorhanden ist, wird die Anmeldung abgelehnt, es sei denn, der Benutzer hat Mitarbeiterstatus. Dies verhindert, dass Nicht-Mitarbeiterkonten über SSO auf das Admin-Panel zugreifen.

## Rollenzuordnung

Wenn Ihr Identitätsanbieter Gruppenmitgliedschaftsinformationen in den OIDC-Ansprüchen sendet, kann Spwig die Mitarbeiter- und Superuserstatus automatisch basierend auf der Gruppenmitgliedschaft festlegen.

Um Rollenzuordnung zu konfigurieren:

1. In der SSO-Anbieterkonfiguration legen Sie das Feld **Gruppenanspruch** auf den Namen des Anspruchs fest, den Ihr Anbieter verwendet (Standard: `groups`)
2. In **Mitarbeitergruppen** geben Sie kommagetrennte Gruppennamen oder -ids ein. Benutzer in einer dieser Gruppen erhalten Mitarbeiterstatus.
3. In **Superuser-Gruppen** geben Sie kommagetrennte Gruppennamen oder -ids ein. Benutzer in einer dieser Gruppen erhalten Superuserstatus.

Die Rollenzuordnung wird jedes Mal bewertet, wenn ein Benutzer sich über SSO anmeldet. Wenn ein Benutzer aus einer Gruppe im Identitätsanbieter entfernt wird, wird sein Mitarbeiter- oder Superuserstatus bei seiner nächsten SSO-Anmeldung aktualisiert.

**Wichtig:** Microsoft Entra ID sendet standardmäßig **Objekt-IDs** (UUIDs) für Gruppen, nicht Gruppennamen. Kopieren Sie die Objekt-ID aus dem Azure-Portal, wenn Sie die Rollenzuordnung konfigurieren. Andere Anbieter wie Okta senden in der Regel Gruppennamen.

## Anspruchszuordnung

Spwig liest Benutzerinformationen aus standardmäßigen OIDC-Ansprüchen. Die Standardwerte funktionieren mit den meisten Anbietern, aber Sie können die Anspruchsfeldnamen in der SSO-Anbieterkonfiguration anpassen:

| Einstellung | Standard | Beschreibung |
|---------|---------|-------------|
| **E-Mail-Anspruch** | `email` | Der Anspruch, der die E-Mail-Adresse des Benutzers enthält |
| **Vorname-Anspruch** | `given_name` | Der Anspruch, der den Vornamen des Benutzers enthält |
| **Nachname-Anspruch** | `family_name` | Der Anspruch, der den Nachnamen des Benutzers enthält |
| **Gruppenanspruch** | `groups` | Der Anspruch, der Gruppenmitgliedschaften enthält (leer lassen, um Rollenzuordnung zu deaktivieren) |

## MFA-Verhalten

Wenn ein Mitarbeiter sich über SSO anmeldet, wird die eingebaute Zwei-Faktor-Authentifizierung (2FA) von Spwig automatisch umgangen. Dies liegt daran, dass der Identitätsanbieter für die Durchführung von MFA als Teil des SSO-Anmeldeverlaufs verantwortlich ist.

Wenn Ihre Organisation MFA erfordert, konfigurieren Sie es in den bedingten Zugriffsrichtlinien Ihres Identitätsanbieters, nicht in den 2FA-Einstellungen von Spwig. Dies ermöglicht Ihnen eine zentrale MFA-Verwaltung für alle Ihre Anwendungen.

## Wiederherstellungszugriff

Wenn Ihr Identitätsanbieter einen Ausfall oder eine Fehlkonfiguration hat, können Sie dennoch auf das Admin-Anmeldeformular zugreifen:

- **Klicken Sie auf den Schalter** — Wenn die Passwortanmeldung deaktiviert ist, klicken Sie auf "Mit lokalem Konto anmelden" auf der Anmeldeseite, um das Passwortformular anzuzeigen
- **URL-Parameter** — Fügen Sie `?password=1` zur Admin-Anmelde-URL hinzu (z. B. `https://your-store.com/en/admin/login/?password=1`), um das Passwortformular direkt anzuzeigen
- **Passwortanmeldung ist immer verfügbar** — Selbst wenn sie im UI versteckt ist, bleibt der Passwort-Authentifizierungsbackend aktiv. Nur die Sichtbarkeit des Formulars wird beeinflusst.

Spwig verhindert auch, dass Sie den Passwort-Login deaktivieren, es sei denn, SSO ist sowohl aktiviert als auch ordnungsgemäß konfiguriert – Sie können sich nicht versehentlich ausloggen.

## Unterstützte Anbieter

Spwig funktioniert mit jedem Identitätsanbieter, der das OpenID Connect (OIDC)-Protokoll unterstützt. Detaillierte Einrichtungsanleitungen sind für folgende Anbieter verfügbar:

- **Microsoft Entra ID** (früher Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Für andere OIDC-konforme Anbieter (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud usw.) sind die Spwig-Konfigurationsschritte identisch – Sie benötigen die OIDC-Discovery-URL des Anbieters, die Client-ID und den Client-Secret. Konsultieren Sie die Dokumentation Ihres Anbieters, um zu erfahren, wie Sie eine Webanwendung registrieren und diese Anmeldeinformationen erhalten. Die Umleitungs-URL, die Sie verwenden müssen, ist immer `https://your-store.com/oidc/callback/`.

## Tipps

- **Beginnen Sie mit aktiviertem Passwort-Login** – Aktivieren Sie SSO zusammen mit dem Passwort-Login. Sobald Sie bestätigt haben, dass SSO für Ihr Team funktioniert, können Sie optional den Passwort-Login deaktivieren.
- **Testen Sie in einem Incognito-Fenster** – Verwenden Sie ein privates/Incognito-Browserfenster, um SSO zu testen, ohne von Ihrer aktuellen Admin-Sitzung beeinflusst zu werden.
- **Erstellen Sie Mitarbeiterkonten zuerst** – Sofern Sie Auto-Create Users nicht aktivieren, benötigen Mitarbeiter ein bestehendes Spwig-Konto mit einer übereinstimmenden E-Mail-Adresse, bevor sie sich über SSO anmelden können.
- **Verwenden Sie den Auto-Discover-Button** – Geben Sie die OIDC-Discovery-URL Ihres Anbieters ein und klicken Sie auf Auto-Discover, um alle Endpunkt-Felder automatisch auszufüllen. Dies ist schneller und weniger fehleranfällig als die manuelle Eingabe der Endpunkte.
- **Behalten Sie ein lokales Admin-Konto bei** – Halten Sie immer mindestens ein lokales Admin-Konto mit einem Passwort als Wiederherstellungsoption bereit, falls Probleme mit dem Identitätsanbieter auftreten.
- **Überwachen Sie die Ablaufdatum des Client-Secrets** – Einige Anbieter (insbesondere Microsoft Entra ID) stellen Client-Secrets mit Ablaufdaten bereit. Stellen Sie einen Kalendererinnerung ein, um das Secret vor Ablauf zu rotieren.