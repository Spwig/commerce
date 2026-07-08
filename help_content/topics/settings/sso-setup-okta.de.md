---
title: 'SSO-Setup: Okta'
---

Dieser Leitfaden führt Sie durch den Prozess, Spwig mit Okta für die Einzelanmeldung (Single Sign-On) für Admins zu verbinden. Nach der Konfiguration können Ihre Mitarbeiter sich mit ihrem Okta-Konto in das Spwig-Admin-Panel anmelden.

**Hinweis:** Okta kann ihre Admin-Konsolen-Schnittstelle im Laufe der Zeit aktualisieren. Diese Anweisungen wurden basierend auf der Okta-Admin-Konsolen-Schnittstelle bis Anfang 2026 verfasst. Falls sich einige Schritte von dem unterscheiden, was Sie sehen, beziehen Sie sich auf die offizielle Dokumentation von Okta zu [Erstellen einer OIDC-App-Integration](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Voraussetzungen

- Eine Okta-Organisation (beliebiger Tarif – kostenlose Entwicklerkonten eignen sich für Tests)
- **Super Administrator** oder **Application Administrator**-Rolle in Okta
- Ihre Spwig-Store-URL (z. B. `https://your-store.com`)
- Mitarbeiter müssen in Spwig E-Mail-Adressen haben, die mit ihren Okta-Konten übereinstimmen

## Schritt 1: Anwendung erstellen

1. Melden Sie sich bei der [Okta Admin-Konsolen](https://your-org-admin.okta.com) an
2. Navigieren Sie zu **Applications > Applications**
3. Klicken Sie auf **Create App Integration**
4. Wählen Sie:

| Feld | Wert |
|-------|-------|
| **Anmeldeart** | OIDC - OpenID Connect |
| **Anwendungstyp** | Web Application |

5. Klicken Sie auf **Next**

## Schritt 2: Anwendung konfigurieren

Füllen Sie die Anwendungseinstellungen aus:

| Feld | Wert |
|-------|-------|
| **App-Integration-Name** | `Spwig Admin SSO` (oder einen beliebigen Namen Ihrer Wahl) |
| **Erlaubnistyp** | Authorization Code (wird standardmäßig ausgewählt) |
| **Anmelde-Redirect-URIs** | `https://your-store.com/oidc/callback/` |
| **Abmelde-Redirect-URIs** | `https://your-store.com/en/admin/login/` |
| **Kontrollierte Zugriffsberechtigung** | Wählen Sie basierend auf Ihren Bedürfnissen (siehe unten) |

Für **Kontrollierte Zugriffsberechtigung** wählen Sie eine der folgenden Optionen:

- **Alle Benutzer in Ihrer Organisation zulassen** – alle Okta-Benutzer können sich anmelden (Sie können den Zugriff auf Spwig weiterhin mit der Einstellung *Nur für Mitarbeiter einschränken* kontrollieren)
- **Zugriff auf ausgewählte Gruppen beschränken** – nur Benutzer in bestimmten Okta-Gruppen können sich anmelden
- **Zuweisen von Gruppen vorerst überspringen** – Sie weisen Benutzer oder Gruppen später manuell zu

Klicken Sie auf **Save**.

**Wichtig:** Die Anmelde-Redirect-URI muss exakt `https://your-store.com/oidc/callback/` entsprechen – einschließlich des Schlussstrichs.

## Schritt 3: Client-Anmeldeinformationen abrufen

Nachdem Sie gespeichert haben, zeigt der **General**-Reiter der Anwendung Ihre Anmeldeinformationen an:

| Wert | Wo Sie es finden können |
|-------|-----------------|
| **Client ID** | General-Reiter, Abschnitt Client Credentials |
| **Client Secret** | General-Reiter, Abschnitt Client Credentials (klicken Sie auf das Auge-Symbol, um es anzuzeigen) |

Kopieren Sie beide Werte – Sie benötigen sie für Spwig.

## Schritt 4: Discovery-URL erstellen

Die Discovery-URL hängt von Ihrer Okta-Organisation und Ihrem Autorisierungsserver ab:

**Standard-Autorisierungsserver (meistens):**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**Benutzerdefinierter Autorisierungsserver (falls konfiguriert):**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

Ersetzen Sie `your-org.okta.com` mit Ihrer tatsächlichen Okta-Domäne. Sie können Ihre Okta-Domäne in der Adressleiste der Admin-Konsolen-URL oder unter **Settings > Account** finden.

**Tipp:** Die meisten Organisationen verwenden den Org-Autorisierungsserver (Standard). Nutzen Sie nur eine benutzerdefinierte Autorisierungsserver-URL, wenn Ihr Okta-Administrator eine speziell eingerichtet hat.

## Schritt 5: Benutzer oder Gruppen zuweisen

Wenn Sie in Schritt 2 **Zuweisen von Gruppen vorerst überspringen** ausgewählt haben, müssen Sie Benutzer zuweisen, bevor sie sich anmelden können:

1. Klicken Sie im **Assignments**-Reiter der Anwendung auf **Assign**
2. Wählen Sie **Assign to People** oder **Assign to Groups**
3. Wählen Sie die Benutzer oder Gruppen aus und klicken Sie auf **Assign**
4. Klicken Sie auf **Done**

Benutzer, die nicht der Anwendung zugewiesen wurden, erhalten bei der Versuche zur Einzelanmeldung eine Fehlermeldung.

## Schritt 6: Gruppenansprüche konfigurieren (optional)

Wenn Sie möchten, dass Spwig automatisch den Mitarbeiter- oder Superuser-Status basierend auf der Gruppenmitgliedschaft in Okta festlegt:

1.

Navigieren Sie zu **Security > API** in der Admin-Konsolen
2.

Wählen Sie Ihren **Autorisierungsserver** aus (verwenden Sie "default", wenn Sie keinen benutzerdefinierten erstellt haben, oder den Org-Autorisierungsserver)
3.

Gehen Sie zum **Claims**-Reiter
4.



Klicken Sie auf **Behauptung hinzufügen**
5.

Konfigurieren Sie die Behauptung:

| Feld | Wert |
|-------|-------|
| **Name** | `groups` |
| **In Token-Typ einbeziehen** | ID Token, Always |
| **Werttyp** | Gruppen |
| **Filter** | Übereinstimmung mit Regex: `.*` (um alle Gruppen einzubeziehen) |
| **In einbeziehen** | Jeder Bereich (oder `openid`, wenn Sie es einschränken möchten) |

6. Klicken Sie auf **Erstellen**

**Tipp:** Im Gegensatz zu Microsoft Entra ID, die Object IDs sendet, sendet Okta standardmäßig **Gruppennamen**. Dies macht die Zuordnung von Rollen intuitiver – Sie können die Anzeigennamen Ihrer Okta-Gruppen direkt in den Feldern *Mitarbeitergruppen* und *Superuser-Gruppen* von Spwig verwenden.

### Gruppenfiltern

Wenn Ihre Benutzer zu vielen Okta-Gruppen gehören und Sie nur bestimmte in den Token einbeziehen möchten:

- Ändern Sie den Filter von `.*` in einen spezifischeren Regex, z. B. `^Spwig.*`, um nur Gruppen einzubeziehen, die mit "Spwig" beginnen
- Oder verwenden Sie stattdessen Filter wie **Beginnt mit**, **Gleich** oder **Enthält**

## Schritt 7: In Spwig konfigurieren

1. Navigieren Sie im Spwig-Admin-Bereich zu **Enterprise SSO > SSO-Provider-Konfiguration**
2. Legen Sie den **Provider-Namen** auf `Okta` fest
3. Geben Sie die Entdeckungs-URL aus Schritt 4 ein
4. Klicken Sie auf **Automatisch entdecken** – dies füllt alle Endpunkt-Felder automatisch aus
5. Geben Sie die **Client-ID** aus Schritt 3 ein
6. Geben Sie den **Client-Secret** aus Schritt 3 ein
7. Wenn Sie in Schritt 6 Gruppenbehauptungen konfiguriert haben:
   - Legen Sie **Gruppenbehauptung** auf `groups` fest
   - Geben Sie in **Mitarbeitergruppen** die Namen der Okta-Gruppen ein, deren Mitglieder Mitarbeiter sein sollen (kommagetrennt)
   - Geben Sie in **Superuser-Gruppen** die Namen der Okta-Gruppen ein, deren Mitglieder Superuser sein sollen (kommagetrennt)
8. Klicken Sie auf **Speichern**

## Schritt 8: Aktivieren und Testen

1. Navigieren Sie zu **Site-Einstellungen > Sicherheit**-Registerkarte
2. Aktivieren Sie **SSO für Admin-Anmeldung**
3. Klicken Sie auf **Speichern**
4. Öffnen Sie die Admin-Anmeldeseite in einem **privaten/inkognito Fenster**
5. Sie sollten eine **Mit Okta anmelden**-Schaltfläche sehen
6. Klicken Sie darauf – Sie sollten zur Okta-Anmeldeseite weitergeleitet werden
7. Melden Sie sich mit einem Okta-Konto an, das der Anwendung zugewiesen ist, und dessen E-Mail einer Mitarbeiterin oder einem Mitarbeiter in Spwig entspricht
8. Sie sollten zur Spwig-Admin-Dashboard-Website weitergeleitet werden

## Häufige Probleme

| Problem | Ursache | Lösung |
|---------|-------|----------|
| **Die Umleitungs-URI ist nicht erlaubt** | Die Umleitungs-URI stimmt nicht mit der Anwendungs-Konfiguration überein | Stellen Sie sicher, dass die Umleitungs-URI für die Anmeldung exakt `https://your-store.com/oidc/callback/` lautet, einschließlich des Schlussstrichs |
| **Der Benutzer ist nicht der Client-Anwendung zugewiesen** | Der Benutzer ist nicht der Okta-Anwendung zugewiesen | Weisen Sie den Benutzer oder seine Gruppe der Anwendung im Registerkarte *Zuordnungen* zu |
| **Anmeldung bei Okta ist erfolgreich, aber bei Spwig fehlschlägt** | Kein passender Benutzer in Spwig | Stellen Sie sicher, dass ein Mitarbeiterkonto in Spwig mit der gleichen E-Mail vorhanden ist. Prüfen Sie die Einstellung *Nur für Mitarbeiter beschränken*. |
| **Gruppenbehauptung ist leer** | Gruppenbehauptung nicht auf dem Autorisierungsserver konfiguriert | Folgen Sie Schritt 6, um eine Gruppenbehauptung hinzuzufügen. Stellen Sie sicher, dass Sie sie dem richtigen Autorisierungsserver hinzufügen. |
| **Falscher Autorisierungsserver** | Die Entdeckungs-URL verwendet einen anderen Auth-Server als den, auf dem die Gruppenbehauptung konfiguriert ist | Stellen Sie sicher, dass die Entdeckungs-URL dem Autorisierungsserver entspricht, auf dem Sie die Gruppenbehauptung konfiguriert haben |
| **„Der bereitgestellte Client-ID ist ungültig“** | Client-ID stimmt nicht überein oder Anwendung ist inaktiv | Prüfen Sie, ob die Client-ID korrekt ist und der Anwendungsstatus in Okta als *Aktiv* festgelegt ist |

## Tipps

- **Okta sendet Gruppennamen, nicht IDs** – dies macht die Rollenzuordnung einfach.

Geben Sie den exakten Anzeigennamen der Gruppe (z. B. `Spwig Admins`) in die Felder *Mitarbeitergruppen* oder *Superuser-Gruppen* in Spwig ein.
- **Verwenden Sie Gruppenzuordnung für Zugriffssteuerung** – weisen Sie bestimmte Okta-Gruppen der Spwig-Anwendung zu, anstatt allen Benutzern Zugriff zu gewähren.

# Sicherheitseinstellungen für SSO mit Okta

So können nur die beabsichtigten Mitarbeiter sich anmelden.
- **Okta-Client-Geheimnisse verlieren nicht automatisch ihre Gültigkeit** — Sie können sie jedoch jederzeit im Allgemein-Tab der Anwendung für beste Sicherheitspraktiken rotieren.
- **Testen Sie mit einem Nicht-Admin-Konto** — verwenden Sie einen regulären Okta-Benutzer (nicht Super-Admin), der der Anwendung zugewiesen ist, um sicherzustellen, dass SSO wie erwartet funktioniert.
- **MFA in Okta** — konfigurieren Sie die globale Sitzungspolitik oder Authentifizierungspolitiken in Okta, um MFA zu erzwingen.

Dies gilt für alle SSO-Anmeldungen bei Spwig, ohne dass eine separate MFA-Konfiguration in Spwig erforderlich ist.