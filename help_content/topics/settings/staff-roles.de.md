---
title: Mitarbeiterrollen & Berechtigungen
---

Mitarbeiterrollen ermöglichen es Ihnen, exakt zu steuern, was jeder Teammitglied in beiden Admin-Panel und POS-Terminal sehen und tun kann. Definieren Sie Rollen mit spezifischen Berechtigungen und weisen Sie diese dann Mitarbeitern zu. Ein Benutzer kann mehrere Rollen haben, und ihre effektiven Berechtigungen sind die Kombination aller zugewiesenen Rollen.

![Mitarbeiterrollen](/static/core/admin/img/help/staff-roles/role-list.webp)

## Wie es funktioniert

1. Sie erstellen **Rollen**, die eine Menge von Berechtigungen definieren (z. B. "Bestellmanager", "Kassierer")
2. Jede Rolle steuert zwei Arten von Zugriff: **Admin-Panel-Berechtigungen** und **POS-Berechtigungen**
3. Sie **weisen Rollen** Mitarbeitern zu, von ihrer Profilseite aus
4. Die effektiven Berechtigungen eines Mitarbeiters sind die **Vereinigung** aller ihrer Rollen — wenn eine Rolle Zugriff gewährt, hat der Benutzer ihn
5. Berechtigungen werden **gecacht** für Leistung und automatisch aktualisiert, wenn Rollen geändert werden

## Vorgefertigte Rollen

Spwig enthält 7 eingebaute Rollen, die die häufigsten Teamstrukturen abdecken. Diese können nicht gelöscht werden, aber Sie können benutzerdefinierte Rollen für spezifischere Anforderungen erstellen.

| Rolle | Zugriff | Beschreibung |
|------|--------|-------------|
| **Geschäftsinhaber** | Admin + POS | Vollzugriff auf alles. Für den primären Geschäftsinhaber. |
| **Geschäftsführer** | Admin + POS | Tägliche Betriebsabläufe — voller Zugriff auf Produkte, Bestellungen, Kunden, Marketing und Suche. Nur Lesen für Design, E-Mail, Zahlungen und Einstellungen. |
| **Inhalt-Editor** | Admin | Verwaltet Seiten, Blogbeiträge, Design und Medien. Nur Lesen für Produkte. |
| **Bestellmanager** | Admin | Verwaltet Bestellungen, Versand, Rückgaben und Kundenservice. Nur Lesen für Produkte. |
| **Marketingmanager** | Admin | Verwaltet Promotionen, Gutscheine, Affiliate, Treueprogramme und Empfehlungsprogramme. Nur Lesen für Produkte, Kunden und Medien. |
| **Kassierer** | Nur POS | Frontlinie POS-Mitarbeiter. Kann Verkäufe verarbeiten und Gutscheinkonten prüfen. Keine Rabatte, Rückerstattungen oder Bargeldverwaltung. |
| **Erfahrener Kassierer** | Nur POS | Erfahrener POS-Mitarbeiter. Kann Rückerstattungen verarbeiten, Rabatte anwenden (bis zu 25 %), Bargeld verwalten und Schichten schließen. |

## Erstellen einer benutzerdefinierten Rolle

Navigieren Sie zu **Einstellungen > Mitarbeiterrollen** und klicken Sie auf **Rolle hinzufügen**.

### Allgemeine Einstellungen

| Einstellung | Beschreibung |
|---------|-------------|
| **Anzeigename** | Der Rolle Name, der im Admin gezeigt wird (z. B. "Lagerpersonal") |
| **Beschreibung** | Eine kurze Erklärung, wofür diese Rolle ist |
| **Sortierreihenfolge** | Steuert die Anzeigereihenfolge in der Rollenliste |
| **Symbol** | Wählen Sie aus 20 Symbolen, um die Rolle visuell zu identifizieren |
| **Badge-Farbe** | Farbe, die für Rollen-Badge verwendet wird (Blau, Grün, Orange, Rot, Teal, Grau) |
| **Admin-Panel** | Schalten Sie um, ob diese Rolle Zugriff auf das Admin-Backend gewährt |
| **POS-Terminals** | Schalten Sie um, ob diese Rolle Zugriff auf POS-Terminals gewährt |

### Admin-Berechtigungs-Kategorien

Der Admin-Berechtigungen-Tab organisiert alle Plattformfunktionen in 13 Kategorien. Für jede Kategorie legen Sie einen der drei Zugriffsstufen fest:

- **Kein Zugriff** — Kein Zugriff auf diesen Bereich (Menüelemente sind ausgeblendet)
- **Anschauen** — Nur-Leserecht (kann Daten sehen, aber nicht ändern)
- **Vollständig** — Vollzugriff (kann Daten ansehen, erstellen, bearbeiten und löschen)

![Berechtigungs-Kategorien](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Kategorie | Was es steuert |
|----------|-----------------|
| **Produktkatalog** | Produkte, Kategorien, Marken, Attribute, Lagerbestand, Lager, digitale Assets |
| **Bestellungen & Erfüllung** | Bestellungen, Rückerstattungen, Rückgaben, Versand, Versandkonfiguration |
| **Kunden** | Kundenprofile, Segmente, Analysen |
| **Inhalt & Seiten** | Seiten, Blogbeiträge, Ankündigungen, Formulare |
| **Design & Theme** | Themes, Header/Footer-Vorlagen, Menüs, Design-Token, benutzerdefinierte CSS |
| **Marketing & Promotionen** | Promotionen, Gutscheine, Affiliate, Treueprogramme, Empfehlungen, Produktfeeds |
| **Medienbibliothek** | Bilder, Videos, Ordner, Tags |
| **E-Mail-System** | E-Mail-Konten, Vorlagen, Lieferwarteschlange |
| **Zahlungen & Abrechnung** | Zahlungsdienstleister, Transaktionen, Webhooks, Abonnements, Wechselkurse |
| **Suche** | Sucheinstellungen, Synonyme, Umleitungen, Analysen |
| **Geschäfts-Einstellungen** | Site-Einstellungen, Geolokalisierung, Länderzuordnungen, Geschäftsregeln |
| **POS-Verwaltung** | POS-Terminals, Schichten, Bargeldbewegungen, Rechnungsvorlagen |
| **Benutzer & Rollen** | Mitarbeiterkonten, Rollen, API-Token |

Wenn ein Benutzer mehrere Rollen hat, gewinnt die **höchste** Zugriffsstufe. Zum Beispiel, wenn Rolle A "Anschauen" für Produkte gewährt und Rolle B "Vollständig" gewährt, hat der Benutzer "Vollständig" Zugriff.

### POS-Berechtigungs-Flags

Wenn die Rolle POS-Zugriff gewährt, ermöglicht der POS-Berechtigungen-Tab, genau zu definieren, was ein POS-Bediensteter tun kann. Diese sind getrennt von Admin-Berechtigungen und werden am POS-Terminal geprüft.

![POS-Berechtigungen](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Gruppe | Berechtigung | Beschreibung |
|-------|-----------|-------------|
| **Allgemein** | POS-Zugriff | Kann das POS-System verwenden |
| **Verkäufe & Rabatte** | Manuelle Rabatte | Kann manuelle Zeilen- oder Warenkorb-Rabatte anwenden |
| | Höchster Rabatt % | Der höchste erlaubte Rabattprozentsatz (0–100) |
| | Preisüberschreibung | Kann Produktpreise am Kassensystem überschreiben |
| **Rückerstattungen & Stornos** | Rückerstattungen verarbeiten | Kann Rückerstattungen für POS-Bestellungen verarbeiten |
| | Bestellungen stornieren | Kann POS-Bestellungen aus der aktuellen Schicht stornieren |
| **Geschenkkarten** | Geschenkkarten ausstellen | Kann neue Geschenkkarten am Kassensystem ausstellen |
| | Geschenkkarten-Balance prüfen | Kann Geschenkkarten-Balancen prüfen |
| **Bargeldverwaltung** | Bargeldverwaltung | Kann Bargeld-Ein- und -Auszahlungen durchführen |
| | Kassenschubladen öffnen | Kann die Kassenschublade ohne Verkauf öffnen |
| | Schichten schließen | Kann Schichten schließen und Bargeldabrechnung durchführen |
| **Berichte** | POS-Berichte ansehen | Kann Schichtberichte und Verkaufszusammenfassungen ansehen |
| **Lager** | Lagerbestandsanpassungen | Kann Lagerbestände anpassen (Empfang, Schäden, Neuzählung, Rückgabe) |

Für boolesche Berechtigungen, wenn **irgendeine** der Rollen eines Benutzers sie aktiviert, hat der Benutzer sie. Für den Höchsten Rabatt %, gilt der **höchste** Wert über alle Rollen.

## Mitarbeiter verwalten

Navigieren Sie zu **Einstellungen > Mitarbeiterverwaltung**, um Ihr Team anzuzeigen und zu verwalten.

### Mitarbeiterliste

Die Mitarbeiterliste zeigt alle Benutzer mit Mitarbeiterzugriff an. Für jedes Mitglied können Sie sehen:
- **Name und E-Mail**
- **Zugewiesene Rollen** (als farbige Badges angezeigt)
- **Zugriffstyp** — Nur Admin, Nur POS oder Beides
- **2FA-Status** — Ob die zweistufige Authentifizierung aktiviert ist
- **Aktiv/Inaktiv**-Status

Verwenden Sie die Filter, um nach Rolle, Zugriffstyp oder 2FA-Status zu filtern.

### Rollen zuweisen

1. Klicken Sie auf einen Mitarbeiter, um deren Profil zu öffnen
2. In der **Rollen**-Sektion sehen Sie Karten für jede verfügbare Rolle
3. Klicken Sie auf das Schalter auf jeder Rollenkarte, um sie zuzuweisen oder zu entfernen
4. Änderungen treten sofort in Kraft — kein Speichern-Button erforderlich
5. Die **Effektive Berechtigungen** Zusammenfassung unten zeigt das kombinierte Ergebnis aller zugewiesenen Rollen

### Neuen Mitarbeiter hinzufügen

1. Navigieren Sie zu **Einstellungen > Mitarbeiterverwaltung** und klicken Sie auf **Mitarbeiter hinzufügen**
2. Geben Sie die E-Mail, den Vornamen und Nachnamen des Benutzers ein
3. Legen Sie ein temporäres Passwort fest
4. Weisen Sie eine oder mehrere Rollen zu
5. Der Benutzer kann jetzt mit dem Zugriff, den seine Rollen gewähren, anmelden

## Rollen klonen

Um eine neue Rolle basierend auf einer vorhandenen zu erstellen:

1. Öffnen Sie die Rolle, die Sie kopieren möchten
2. Klicken Sie auf **Rolle klonen** am unteren Rand der Seite
3. Eine neue Rolle wird erstellt, mit allen gleichen Berechtigungen
4. Benennen Sie sie um und passen Sie Berechtigungen an, wenn nötig
5. Speichern Sie die neue Rolle

Dies ist nützlich, wenn Sie eine Rolle benötigen, die einer vorhandenen sehr ähnlich ist, aber mit geringfügigen Unterschieden — zum Beispiel, eine "Junior Manager"-Rolle basierend auf "Geschäftsführer", aber mit weniger Berechtigungen.

## Wie Berechtigungen angewendet werden

### Admin-Panel

- **Menü-Sichtbarkeit** — Seitenleistenabschnitte sind für Kategorien ausgeblendet, in denen der Benutzer "Kein Zugriff" hat
- **Seitenzugriff** — Versuchen, eine eingeschränkte Seite zu besuchen, zeigt einen Berechtigungsfehler an
- **Aktionseinschränkungen** — Mit "Anschauen"-Zugriff sind Bearbeiten- und Löschen-Buttons ausgeblendet und Speichern-Aktionen blockiert
- **Superuser-Überschreibung** — Superuser-Konten haben immer Vollzugriff, unabhängig von Rollenzuordnungen

### POS-Terminal

- **Anmelde-Schranke** — Nur Benutzer mit mindestens einer Rolle, die "POS-Terminals" aktiviert hat, können sich am POS anmelden
- **Funktionsschalter** — POS-Schaltflächen und Aktionen (Rückerstattung, Rabatt, Stornierung usw.) werden basierend auf den zusammengeführten POS-Berechtigungen des Benutzers angezeigt oder ausgeblendet
- **Rabattgrenze** — Der Höchste Rabatt % erzwingt eine harte Grenze, wie groß ein Rabatt ein POS-Bediensteter anwenden kann
- **API-Enforcement** — Alle POS-Berechtigungen werden am API-Schicht serverseitig geprüft, nicht nur in der Benutzeroberfläche

## Tipps

- **Beginnen Sie mit vorgefertigten Rollen** — Die 7 eingebauten Rollen decken die meisten Teamstrukturen ab. Erstellen Sie benutzerdefinierte Rollen nur, wenn Sie spezifischere Zugriffssteuerungen benötigen.
- **Verwenden Sie das Klonen** — Wenn Sie eine Rolle benötigen, die einer vorhandenen sehr ähnlich ist, klonen Sie sie und passen Sie sie an, anstatt sie von Grund auf neu zu erstellen.
- **Weisen Sie mehrere Rollen zu, wenn nötig** — Ein Mitarbeiter, der sowohl Bestellungen als auch Marketing bearbeitet, kann sowohl die Rolle "Bestellmanager" als auch "Marketingmanager" zugewiesen bekommen. Berechtigungen kombinieren sich automatisch.
- **Trennen Sie Admin- und POS-Zugriff** — Kassierer benötigen in der Regel keinen Admin-Zugriff, und Büroangestellte benötigen keinen POS-Zugriff. Verwenden Sie die Zugriffsschalter, um Dinge sauber zu halten.
- **Setzen Sie Rabattgrenzen für POS-Mitarbeiter** — Der Höchste Rabatt % verhindert, dass Kassierer zu große Rabatte anwenden. Setzen Sie es auf 0, um keine Rabatte zu erlauben, oder auf einen vernünftigen Grenzwert wie 10–25 % für erfahrene Mitarbeiter.
- **Überprüfen Sie Rollen regelmäßig** — Wenn Ihr Team wächst, überprüfen Sie die Rollenzuordnungen, um sicherzustellen, dass Mitarbeiter nur den minimalen Zugriff haben, der für ihre Arbeit erforderlich ist. Entfernen Sie Rollen, wenn sich die Positionen von Mitarbeitern ändern.
- **Aktivieren Sie 2FA für sensible Rollen** — Mitarbeiter mit Zugriff auf Zahlungen, Einstellungen oder Benutzerverwaltung sollten zwei-Faktor-Authentifizierung aktiviert haben, um Sicherheit zu gewährleisten.