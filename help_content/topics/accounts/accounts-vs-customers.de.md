---
title: Konten vs. Kunden
---

Händler fragen häufig: "Was ist der Unterschied zwischen einem Konto und einem Kunden?" Dieses Verwirrung ist üblich, da jeder Kunde ein Konto ist, aber nicht jedes Konto ein Kunde. Dieser Leitfaden klärt die Unterschiede und erklärt, wann Sie jede Admin-Oberfläche verwenden sollten.

![Benutzerliste](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Was ist ein Konto?

Ein **Konto** ist das zentrale Authentifizierungsobjekt in Spwig. Jeder, der sich in Ihre Plattform einloggen kann – Mitarbeiter oder Kunde – hat ein Konto. Konten werden im Spwig-Authentifizierungssystem verwaltet und sind im `User`-Modell gespeichert.

Alle Konten haben:
- **E-Mail-Adresse** – Die primäre Identifikation und Anmeldeinformation
- **Benutzername** – Ein eindeutiger Benutzername (standardmäßig automatisch aus der E-Mail generiert)
- **Passwort** – Hashiert und sicher gespeichert
- **is_staff-Flag** – Bestimmt, ob das Konto auf das Admin-Backend zugreifen kann

Konten können sich auch über OAuth-Anbieter (Google, Facebook usw.) authentifizieren, die unter **Einstellungen > Authentifizierung** konfiguriert sind.

## Was ist ein Kunde?

Ein **Kunde** ist ein spezieller Typ von Konto mit `is_staff=False`. Kunden shoppen auf Ihrem Laden, geben Bestellungen auf und verwalten ihre Profile. Jedes Kundenkonto wird automatisch erweitert mit:

- **CustomerProfile** – Speichert Präferenzen, Newsletter-Abonnements und benutzerdefinierte Feldwerte
- **CustomerMetrics** – Verfolgt Lebenszeitwert (LTV), RFM-Scores, Bestellhistorie und Segmentdaten
- **OrderHistory** – Verknüpft mit allen Bestellungen, die dieser Kunde getätigt hat

Kunden können sein:
- **Registrierte Kunden** – Erstellt über Ladenregistrierung oder Admin
- **Gastbenutzer** – Temporäre Konten, die während des Gastcheckouts erstellt werden (Benutzername beginnt mit `guest_`)
- **Importierte Kunden** – Migriert von anderen Plattformen über CSV-Import

## Der Hauptunterschied

| Attribut | Konto | Kunde |
|-----------|---------|----------|
| **Zweck** | Authentifizierung und Autorisierung | Einkaufen, Bestellungen und Analysen |
| **Umfang** | Mitarbeiter und Kunden | Nur Kunden |
| **is_staff-Flag** | Wahr oder Falsch | Immer Falsch |
| **Erweiterte Daten** | Keine (nur Kernfelder) | CustomerProfile + CustomerMetrics |
| **Admin-Position** | Einstellungen > Benutzer | Kunden > Kundenprofile |
| **Kann sich anmelden** | Ja | Ja |
| **Kann Bestellungen aufgeben** | Nur wenn CustomerProfile vorhanden ist | Ja |
| **Kann Admin zugreifen** | Nur wenn is_staff=True | Nein |

Kurz gesagt:
- Ein **Konto** ist jeder, der sich anmelden kann
- Ein **Kunde** ist ein Konto, das einkauft und Bestellungen aufgibt

## Mitarbeiter sind auch Konten

Mitarbeiter sind Konten mit `is_staff=True`. Sie können sich in das Admin-Backend einloggen und Aktionen basierend auf ihren zugewiesenen **StaffRole**-Berechtigungen durchführen.

Mitarbeiter können optional ein **CustomerProfile** haben, wenn sie auch im Laden einkaufen. Zum Beispiel, wenn Sie (der Händler) eine Testbestellung auf Ihrem eigenen Store tätigen, wird für Ihr Mitarbeiterkonto ein CustomerProfile erstellt. Dies hat **keinen** Einfluss auf Ihre Admin-Zugriffsrechte.

Mitarbeiterberechtigungen werden gesteuert durch:
- **StaffRole** – Definiert, welche Admin-Abteilungen und Aktionen der Mitarbeiter zugreifen kann
- **is_superuser-Flag** – Gewährt vollen, eingeschränkten Zugriff (sparsam verwenden)

Verwalten Sie Mitarbeiter unter **Einstellungen > Mitarbeiterverwaltung**.

## Gastbenutzer

Gastcheckout erstellt temporäre Konten mit automatisch generierten Benutzernamen, die mit `guest_` beginnen. Diese Konten:
- Haben `is_staff=False` (sie sind Kunden)
- Haben ein CustomerProfile (für Bestellzuordnung)
- Haben ein zufälliges Passwort (Gast kann sich nicht anmelden, es sei denn, sie werden zu registrierten Benutzern konvertiert)
- Werden standardmäßig von Kundenanalysen ausgeschlossen

Gäste können zu registrierten Kunden werden, indem sie:
1. Ein Konto auf dem Laden mit der gleichen E-Mail erstellen
2. Ihre E-Mail-Adresse verifizieren
3. Das System merge die Gastbestellhistorie in das neue registrierte Konto

Verwalten Sie Gastkonvertierungseinstellungen unter **Einstellungen > Checkout > Gastcheckout**.

## Wo Sie jede finden

| Admin-Position | Was Sie verwalten | Schlüsselverwendungsfälle |
|----------------|-----------------|---------------|
| **Einstellungen > Benutzer** | Alle Konten (Mitarbeiter + Kunden) | Passwörter zurücksetzen, Konten aktivieren/deaktivieren, Mitarbeiterberechtigungen zuweisen |
| **Einstellungen > Mitarbeiterverwaltung** | Nur Mitarbeiterkonten (is_staff=True) | Rollen zuweisen, Teammitgliederzugang verwalten, Berechtigungen konfigurieren |
| **Kunden > Kundenprofile** | Nur Kundenkonten (is_staff=False) | Kundenpräferenzen ansehen, Bestellhistorie, LTV, RFM-Scores, Segmente |
| **Kunden > Analysen** | Kundenmetriken und Segmente | Kundenverhalten analysieren, Marketingsegrmente erstellen, Retention verfolgen |

![Kundenprofilliste](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Wann Sie jede Oberfläche verwenden sollten

Verwenden Sie **Einstellungen > Benutzer**, wenn Sie:
- Ein Kundenpasswort zurücksetzen müssen
- Ein kompromittiertes Konto deaktivieren
- Ein Kundenkonto manuell erstellen
- OAuth-Anmeldeverbindungen ansehen
- Alle Konten (Mitarbeiter + Kunden) in einer Liste sehen

Verwenden Sie **Einstellungen > Mitarbeiterverwaltung**, wenn Sie:
- Einen neuen Teammitglied hinzufügen
- Eine Rolle für einen Mitarbeiter zuweisen oder ändern
- Feine Berechtigungen konfigurieren
- Mitarbeiteraktivitätsprotokolle überprüfen

Verwenden Sie **Kunden > Kundenprofile**, wenn Sie:
- Eine Kundenbestellhistorie ansehen
- Kundenpräferenzen und benutzerdefinierte Feldwerte sehen
- Newsletter-Abonnementsstatus prüfen
- Kunden LTV und RFM-Scores überprüfen
- Kundensegmente verwalten

Verwenden Sie **Kunden > Analysen**, wenn Sie:
- Hochwertige Kunden identifizieren
- Marketingsegmente erstellen (z. B. "Kunden, die in 90 Tagen nicht bestellt haben")
- Kundenlebenszykluswerttrends analysieren
- Kundenlisten für Kampagnen exportieren

## Tipps

- **Kundenprofile werden automatisch erstellt** – Wenn ein Kunde seine erste Bestellung (Gast oder registriert) tätigt, erstellt Spwig ein CustomerProfile und eine CustomerMetrics-Record für Analysen.
- **Mitarbeiter können auch Kunden sein** – Wenn ein Mitarbeiter eine Bestellung im Laden tätigt, erhält er ein CustomerProfile. Dies ist normal und hat keinen Einfluss auf seine Admin-Zugriffsrechte.
- **Gastkonten verunreinigen die Benutzerliste** – Verwenden Sie die Kundenprofil-Oberfläche, um sich auf echte, engagierte Kunden zu konzentrieren. Die Benutzerliste enthält alle Gastkonten.
- **Segmentieren Sie nach is_staff=False** – Wenn Sie Kundenlisten für E-Mail-Kampagnen exportieren, filtern Sie immer nach `is_staff=False`, um Teammitglieder auszuschließen.
- **OAuth-Konten sind auch Konten** – Wenn ein Kunde sich über Google oder Facebook anmeldet, erstellt Spwig ein Konto und verknüpft es mit ihrem OAuth-Profil. Das E-Mail-Feld wird aus dem OAuth-Anbieter befüllt.