---
title: POS-Mitarbeiteranmeldung & biometrische Anmeldung
---

Jede Person, die Kunden an einem POS-Register bedient, benötigt ein Mitarbeiterkonto mit den richtigen Berechtigungen. Dieses Thema erklärt, wie Sie dieses Konto erstellen, den Mitarbeiter einem Terminal zuweisen und anschließend die biometrische Anmeldung einrichten, damit er das Register mit einem Fingerabdruck, Gesichtsscanner oder Hardware-Passwort entsperren kann, anstatt jedes Mal ein Passwort einzugeben.

Für PIN-Codes, Rabattgrenzen und Terminal-Sperreeinstellungen siehe [POS-Mitarbeiter-Rabatte & Terminal-Sicherheit](pos-staff-discounts).

## Was ein Mitarbeiter benötigt, um ein POS-Terminal zu verwenden

Um sich bei einem POS-Terminal anzumelden, benötigt eine Person:

1. Ein **Mitarbeiterkonto** — ein Spwig-Benutzer mit dem **Mitarbeiterstatus**-Flag aktiviert.
2. Eine **Rolle mit POS-Zugriff** — Rollen bestimmen, was ein Mitarbeiter im Admin-Bereich tun kann. Eine Rolle mit POS-Berechtigungen ist erforderlich, um auf das Register zuzugreifen.
3. **Zuordnung zum Terminal** — das Terminal muss sie als zugewiesenen Mitarbeiter auflisten, oder sie muss auf Ebene des Geschäftsorts zugewiesen werden.

## Erstellen eines für POS-Eligible-Mitarbeiterkonto

Navigieren Sie zu **Mitarbeiter & Konten > Mitarbeiter** (oder gehen Sie zu `/admin/accounts/staffmember/`).

1. Klicken Sie auf **+ Mitarbeiter hinzufügen**.
2. Geben Sie den **Vornamen**, **Nachnamen** und **E-Mail-Adresse** des Mitarbeiters ein.
3. Legen Sie ein temporäres Passwort fest und bitten Sie den Mitarbeiter, es bei der ersten Anmeldung zu ändern.
4. Stellen Sie sicher, dass **Mitarbeiterstatus** aktiviert ist — dies ermöglicht es ihnen, sich im Admin- und POS-Programm anzumelden.
5. Klicken Sie auf **Speichern**.

> **Hinweis:** Aktivieren Sie **Superuser-Status** nicht für gewöhnliche Kassierer oder Aufseher. Der Superuser-Status überspringt alle Berechtigungsprüfungen und sollte nur für den Geschäftsinhaber reserviert sein.

### Zuweisen einer Rolle mit POS-Zugriff

Mitarbeiterkonten haben an sich keine Berechtigungen — Rollen gewähren spezifische Fähigkeiten. Nachdem das Konto erstellt wurde, öffnen Sie das Mitarbeiterprofil und gehen Sie zu dem Abschnitt **Rollen**. Weisen Sie eine Rolle mit POS-Zugriff zu.

Für eine vollständige Erklärung, wie Rollen funktionieren und welche Berechtigungen einzubeziehen sind, siehe [Mitarbeiterrollen](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Mitarbeiterliste, die einen für POS-Eligible-Nutzer mit ihrer Rollenabzeichen zeigt
-->

![Mitarbeiterliste](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Mitarbeiter einem Terminal zuweisen

Einstellungen folgen einer Kaskade: **Standard für das Site → Store-Gruppe → Store-Location → Einzelner Terminal**. Für die meisten Geschäfte ist der richtige Ort, um Mitarbeiter zuzuweisen, auf Ebene des Terminals.

1. Navigieren Sie zu **POS > Terminals** (oder gehen Sie zu `/admin/pos_app/posterminal/`).
2. Öffnen Sie das Terminal, das Sie konfigurieren möchten.
3. Gehen Sie zum Tab **Mitarbeiterzuweisung**.
4. In das Feld **Zugewiesene Mitarbeiter**, suchen Sie und fügen Sie den Mitarbeiter hinzu.
5. Klicken Sie auf **Speichern**.

Mitarbeiter, die in der **Zugewiesenen Mitarbeiter**-Liste eines Terminals erscheinen, können ihren Namen auf dem Anmeldebildschirm dieses Terminals auswählen. Mitarbeiter, die keinem Terminal zugewiesen sind, können sich dennoch anmelden, indem sie ihre E-Mail direkt eingeben.

> **Tipp:** Wenn Ihr Geschäft viele Mitarbeiter hat, die zwischen Terminals wechseln, weisen Sie sie auf Ebene des Geschäftsorts (Lager) zu, anstatt Terminal für Terminal. Jeder Mitarbeiter, der dem Standort zugewiesen ist, hat automatisch Zugriff auf alle Terminals an diesem Standort.

## Anmeldung am POS-Register

Wenn ein Kassier das POS-Programm (`/pos/`) auf einem Terminal öffnet, sieht er einen Mitarbeiterauswahlscreen. Der Anmeldevorgang funktioniert wie folgt:

1. Der Kassier tippt oder klickt auf seinen Namen in der Liste (oder tippt seine E-Mail, wenn er nicht aufgelistet ist).
2. Er gibt sein Passwort ein.
3. Er ist angemeldet und das Register öffnet sich für seine Schicht.

Für die PIN-basierte Entsperrung (nachdem das Terminal während einer Schicht gesperrt wurde), siehe [POS-Mitarbeiter-Rabatte & Terminal-Sicherheit](pos-staff-discounts).

## Biometrische Anmeldung

Die biometrische Anmeldung ermöglicht es einem Kassier, einen Fingerabdrucksensor zu berühren, in eine Gesichtskamera zu blicken oder einen Hardware-Schlüssel zu tippen, anstatt ein Passwort einzugeben. Auf einem beschäftigten Register spart dies mehrere Sekunden pro Schicht und vermeidet Fehler während der Stoßzeiten.

Spwig verwendet den **WebAuthn**-Browserstandard für die biometrische Anmeldung.

Ein "WebAuthn-Zertifikat" ist ein Gerätegebundenes Schlüsselpaar: der private Schlüssel wird in der sicheren Hardware des Geräts gespeichert und verlässt dieses nie.

Die POS-Anwendung kommuniziert mit dieser Hardware über den Browser.

### Geräte und Browser, die biometrische Anmeldung unterstützen

WebAuthn wird von allen modernen Browsern — Chrome, Edge, Firefox und Safari — auf Geräten unterstützt, die kompatible Hardware haben. Typische Konfigurationen, die gut funktionieren:

| Gerät | Authenticator |
|--------|---------------|
| iPad (Touch ID) | Fingerabdruck über Safari oder Chrome |
| Android-Tablet | Fingerabdruck oder Gesicht über Chrome |
| Windows-Tablet oder PC | Windows Hello (Fingerabdruck, Gesicht oder PIN) |
| Jedes Gerät + Sicherheitsschlüssel | USB, NFC oder Bluetooth FIDO2-Schlüssel (z. B. YubiKey) |
| iPhone (Face ID) | Gesicht über Safari |

Die POS-Anwendung zeigt die Option für die biometrische Anmeldung nur an, wenn der Browser bestätigt hat, dass ein Zertifikat für den aktuellen Benutzer auf diesem Gerät eingerichtet wurde.

### Wie die Registrierung funktioniert

Die Registrierung erfolgt am POS-Terminal, nicht im Admin-Bereich. Der Mitarbeiter muss zunächst eine normale Passwortanmeldung durchführen und dann innerhalb der POS-Anwendung die Einrichtung der biometrischen Anmeldung auswählen. Der Browser fragt anschließend nach, um die Identität des Benutzers mithilfe des biometrischen Sensors des Geräts (oder eines Passkeys, der in ihrem Konto auf iOS/macOS/Windows gespeichert ist) zu bestätigen. Nach Bestätigung wird das Zertifikat gespeichert und die biometrische Anmeldung ist für zukünftige Schichten auf diesem Gerät verfügbar.

Ein einzelner Mitarbeiter kann sich auf mehreren Geräten registrieren — beispielsweise auf einem privaten Tablet und einem gemeinsam genutzten Kasse-Register — und jedes Gerät speichert sein eigenes Zertifikat.

> **Hinweis:** Der genaue Text der Registrierungsaufforderung ("Biometrisch registrieren", "Fingerabdruck-Anmeldung einrichten" usw.) stammt von der POS-Anwendung und kann je nach Browser und Gerät variieren.

### Mit biometrischer Anmeldung anmelden

Nach der Registrierung wird auf dem Anmeldebildschirm der Name des Kassiers durch einen biometrischen Anmeldebutton (Fingerabdruck-Icon oder ähnliches) ersetzt. Der Kassier:

1. Tippt auf seinen Namen auf dem Anmeldebildschirm des Terminals.
2. Tippt auf **Mit Fingerabdruck anmelden** (oder Äquivalent).
3. Berührt den Sensor oder blickt in die Kamera.
4. Das Terminal wird sofort entsperrt.

Falls die biometrische Verifizierung fehlschlägt (Finger nicht erkannt, Gesicht verdeckt), wechselt der Kassier zur Eingabe seines Passworts.

### Ein Zertifikat widerrufen

Wenn ein Gerät verloren geht, gestohlen wird oder ein Mitarbeiter das Unternehmen verlässt, sollten Sie seine biometrischen Zertifikate sofort entfernen.

1. Navigieren Sie zu **Mitarbeiter & Konten > Mitarbeiter**.
2. Öffnen Sie das Profil des Mitarbeiters.
3. Scrollen Sie zu dem Abschnitt **POS-Einstellungen**.
4. In der Zeile **Biometrische Entsperrung**, klicken Sie auf **Alle entfernen**.
5. Bestätigen Sie die Aktion.

Dies entfernt alle eingerichteten WebAuthn-Zertifikate für diesen Mitarbeiter auf allen Geräten. Das nächste Mal, wenn er versucht, sich mit biometrischer Anmeldung auf einem beliebigen Terminal anzumelden, muss er stattdessen mit seinem Passwort anmelden.

> **Wichtig:** Das Entfernen der Zertifikate hier blockiert den Mitarbeiter nicht daran, sich mit seinem Passwort anzumelden. Um den Zugang vollständig zu widerrufen, deaktivieren Sie auch sein Mitarbeiterkonto oder entfernen Sie ihn aus der Liste der zugewiesenen Mitarbeiter am Terminal.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Mitarbeiter-Formular, das den POS-Einstellungen-Abschnitt mit der Anzahl der biometrischen Zertifikate und dem Knopf "Alle entfernen" zeigt
-->

## Sicherheitshinweise

- **Zertifikate sind hardwaregebunden.** Der private Schlüssel verlässt nie das sichere Element des Geräts.

Wenn ein Tablet gestohlen wird, kann ein Angreifer den biometrischen Schlüssel nicht extrahieren — dazu müsste er zuerst den eigenen Sperrbildschirm des Geräts umgehen, bevor der Browser den Schlüssel freigibt.
- **Das Verlieren eines Geräts führt nicht zur Preisgabe eines Passworts.** WebAuthn ersetzt das Passwort für dieses Gerät; das Passwort des Mitarbeiters ist separat und bleibt unbeeinflusst.
- **Revokation sofort durchführen, wenn Mitarbeiter das Unternehmen verlassen.** Entfernen Sie die biometrischen Anmeldeinformationen und deaktivieren Sie das Mitarbeiterkonto im selben Vorgang, wenn ein Mitarbeiter abgebaut wird.
- **Die biometrischen Daten selbst werden nie übertragen.** Der Fingerabdruck oder das Gesichtsscan wird vollständig von der Hardware des Geräts verarbeitet.

Spwig erhält nur eine signierte Antwort auf die Herausforderung, keine biometrischen Daten.

## Problembehandlung

### Der Knopf "Mit Fingerabdruck anmelden" wird nicht angezeigt

Die biometrische Option erscheint nur, wenn:
- Der Mitarbeiter eine Anmeldeinformation auf diesem spezifischen Gerät eingerichtet hat.
- Der Browser WebAuthn unterstützt (alle modernen Browser tun das — aktualisieren Sie, wenn Sie eine ältere Version verwenden).

Wenn der Knopf fehlt, hat der Mitarbeiter noch nicht auf diesem Gerät angemeldet. Er sollte sich mit seinem Passwort anmelden und die biometrische Anmeldung über die POS-App einrichten.

### Registrierung fehlgeschlagen

Häufige Ursachen:
- **Browser-Berechtigung abgelehnt.** Der Browser fragte nach der Berechtigung, um den Authenticator zu nutzen, und der Mitarbeiter lehnte ab. Der Mitarbeiter muss es erneut versuchen und auf **Erlauben** klicken, wenn dies gefragt wird.
- **Kein kompatibler Authenticator gefunden.** Das Gerät hat keinen Fingerabdrucksensor, keine Gesichtskamera oder keinen Sicherheitsschlüssel angeschlossen. Prüfen Sie die Hardware des Geräts.
- **Doppelte Anmeldeinformation.** Der Mitarbeiter hat möglicherweise bereits auf diesem Gerät angemeldet. Bestehende Anmeldeinformationen werden während der Neuregistrierung ausgeschlossen, um Duplikate zu vermeiden.

### Biometrische Anmeldung funktioniert auf einem Gerät, aber nicht auf einem anderen

Jedes Gerät speichert seine eigenen Anmeldeinformationen. Die Registrierung auf einem iPad funktioniert nicht automatisch auf einem zweiten iPad. Der Mitarbeiter muss die Registrierung separat auf jedem Gerät abschließen, das er verwenden wird.

### Cross-device-Passkeys

Einige Betriebssysteme (iOS 16+, macOS Ventura+, Windows 11 mit Microsoft-Konto) können Passkeys über Geräte hinweg synchronisieren, über iCloud Keychain oder Windows Hello. Wenn der Mitarbeiter sich mit einem synchronisierten Passkey angemeldet hat, kann es automatisch auf mehreren Geräten funktionieren. Das Verhalten hängt vom Betriebssystem und Browser ab, nicht von Spwig.

## Tipps

- Richten Sie die biometrische Anmeldung auf gemeinsam genutzten Kassen vor dem Eintreffen der Mitarbeiter für ihre Schicht ein — der zweiminütige Registrierungsprozess ist viel reibungsloser, wenn keine Kunden warten müssen.
- Weisen Sie Mitarbeitern eine Rolle mit eingeschränkten POS-Berechtigungen zu und eine separate Manager-Rolle für Aufsichtspersonen. Halten Sie ihre Konten von dem Konten des Ladeninhabers getrennt.
- Wenn ein Mitarbeiter ein neues Gerät (neues Tablet, neues Telefon) verwendet, lassen Sie ihn sich zuerst auf dem neuen Gerät registrieren und entfernen Sie dann die alte Anmeldeinformation über die Admin-UI, wenn das Gerät nicht mehr in Gebrauch ist.
- Für Läden mit hohem Mitarbeiterwechsel prüfen Sie regelmäßig die Liste **Zugewiesene Mitarbeiter** auf jedem Terminal und entfernen Sie Mitarbeiter, die nicht mehr an diesem Standort arbeiten.
- Wenn Sie Hardware-Sicherheitsschlüssel (YubiKey oder ähnliche) verwenden, kann ein Schlüssel auf mehrere Terminals eingerichtet werden, ohne Änderungen in der Admin-Oberfläche vorzunehmen — stecken Sie einfach den Schlüssel ein und vervollständigen Sie die Registrierung auf jedem Terminal.