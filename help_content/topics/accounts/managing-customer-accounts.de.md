---
title: Verwaltung von Kundenkonten
---

Kundenkonten ermöglichen Händlern, Kundendaten, Bestellhistorie und Präferenzen zu verfolgen. Navigieren Sie zu **Kunden > Alle Kunden** in der Admin- Seitenleiste, um Kundenkonten zu verwalten.

![Kunden hinzufügen](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Verständnis von Kundenkonten vs. Kundendaten

**Kundenkonten** sind die Anmeldeinformationen (E-Mail/Passwort), die im Nutzermodell gespeichert werden. **Kundendaten** speichern zusätzliche Kundendaten wie Telefonnummer, Geburtsdatum, Präferenzen und Analysen. Jedes Kundenkonto hat ein entsprechendes Profil, das diese erweiterten Daten speichert.

Wenn Sie Kunden in der Admin- Oberfläche verwalten, arbeiten Sie mit Kundendaten, die hinter den Kulissen mit Nutzerkonten verknüpft sind.

## Alle Kunden ansehen

Die Kundensliste zeigt alle registrierten Kunden mit Schlüsselmetriken:

| Spalten | Beschreibung |
|--------|-------------|
| **Nutzer** | Kundename und E-Mail-Adresse |
| **Affiliate-Status** | Ob der Kunde auch ein Affiliate-Partner ist |
| **Kundennutzwert** | Gesamtbetrag, den der Kunde ausgegeben hat (farbkodiert) |
| **Kundensegment** | RFM-Segment (Champion, Loyal, In Gefahr, etc.) |
| **Gesamtbestellungen** | Anzahl der abgeschlossenen Bestellungen |
| **Tage seit letzter Bestellung** | Aktualität der letzten Kauf |
| **VIP-Kunde** | Abzeichen, wenn der Kunde als VIP gekennzeichnet ist |

### Kunden filtern

Verwenden Sie die Filterseitenleiste, um die Liste einzuschränken:

- **Affiliate-Status** — Ist Affiliate, Kein Affiliate, Affiliate in Bearbeitung, Aktiv, Suspendiert, Abgelehnt
- **Dashboard-Layout** — Präferiertes Dashboard-Layout des Kunden
- **Newsletter aboniert** — Ob der Kunde Newsletter aboniert hat
- **Marketing-E-Mails** — Ob der Kunde Marketing-E-Mails aboniert hat
- **Erstellt am** — Filtern nach Registrierungsdatum

### Kunden suchen

Verwenden Sie die Suchleiste, um Kunden nach folgenden Kriterien zu finden:
- Benutzername
- E-Mail-Adresse
- Vorname
- Nachname
- Telefonnummer

## Kundendetails ansehen

Klicken Sie auf den Namen eines Kunden, um deren vollständiges Profil anzuzeigen. Die Kundendetailseite zeigt:

![Kundendetails](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Kundendaten-Abschnitt

Grundlegende Kontaktinformationen und Kontostatus:
- **Nutzer** — Link zum zugrunde liegenden Nutzerkonto
- **Telefon** — Kundentelefonnummer
- **Geburtsdatum** — Für Altersverifikation und Geburtstagskampagnen

### Dashboard-Einstellungen

Wie der Kunde sein Konto-Dashboard angepasst hat:
- **Dashboard-Layout** — Raster, Liste oder kompakte Ansicht
- **Bestellhistorie anzeigen** — Ob die Bestellhistorie auf dem Dashboard angezeigt wird
- **Wunschliste anzeigen** — Ob die Wunschliste auf dem Dashboard angezeigt wird
- **Letzte Produkte anzeigen** — Ob kürzlich angesehene Produkte angezeigt werden
- **Produktvorschläge anzeigen** — Ob Produktvorschläge angezeigt werden

### Kommunikationsvorlieben

Status des Kunden für verschiedene Kommunikationsformen:
- **Newsletter aboniert** — In Newsletter aboniert
- **Marketing-E-Mails** — In Marketing-E-Mails aboniert
- **Bestellbenachrichtigungen** — In Bestellstatus-Updates aboniert

### Kundeanalysen

Nur lesbare Zusammenfassungen des Kundengestaltungs- und Nutzwerts:
- **Kundeanalysen-Zusammenfassung** — RFM-Bewertungen, Segment, Lebenszeitwert
- **Kaufverhalten-Zusammenfassung** — Bestellhäufigkeit, durchschnittlicher Bestellwert, bevorzugte Kategorien
- **Engagement-Zusammenfassung** — Letzte Anmeldung, E-Mail-Öffnungsrate, Website-Aktivität

Diese Analysenfelder werden automatisch berechnet und können nicht manuell bearbeitet werden. Siehe [Verständnis von Kundeanalysen](customer-analytics.md) für Details.

## Kundenkonto erstellen

Händler können Kundenkonten manuell für telefonische Bestellungen, In-Store-Abholungen oder zur Vorbereitung von Großhandelskunden erstellen.

1. Klicken Sie auf **+ Kundoprofil hinzufügen** in der oberen rechten Ecke
2. Füllen Sie die erforderlichen und optionalen Felder aus:

| Feld | Erforderlich | Beschreibung |
|-------|----------|-------------|
| **Nutzer** | Ja | Wählen Sie ein bestehendes Nutzerkonto aus oder erstellen Sie ein neues |
| **Telefon** | Nein | Kundentelefonnummer |
| **Geburtsdatum** | Nein | Für Altersverifikation und Geburtstagskampagnen |
| **Newsletter aboniert** | Nein | Kunde in Newsletter abonnieren |
| **Marketing-E-Mails** | Nein | Kunde in Marketing-E-Mails abonnieren |

### Nutzerkonto erstellen, während ein Profil hinzugefügt wird

Wenn der Kunde noch kein Nutzerkonto hat:
1. Klicken Sie auf das **+**-Symbol neben dem Nutzerfeld
2. Geben Sie die E-Mail-Adresse des Kunden ein (dies wird ihr Benutzername)
3. Geben Sie optional **Vorname** und **Nachname** ein
4. Geben Sie optional ein **Passwort** ein
5. Aktivieren Sie **Passwort-Reset-E-Mail senden**, wenn Sie kein Passwort festgelegt haben
6. Speichern Sie das Nutzerkonto
7. Füllen Sie die Kundendatenfelder aus
8. Klicken Sie auf **Speichern**

### Willkommens-E-Mails

Nachdem Sie ein Kundenkonto erstellt haben:
- Wenn Sie ein Passwort festgelegt haben, kann der Kunde sofort mit diesem Passwort anmelden
- Wenn Sie kein Passwort festgelegt haben, sendet das System eine Passwort-Reset-E-Mail, damit der Kunde sein eigenes Passwort festlegen kann
- Sie können manuell eine Willkommens-E-Mail über das E-Mail-System unter **Marketing > E-Mail-Kampagnen** auslösen

## Kundendaten bearbeiten

Um Kundendaten zu aktualisieren:
1. Navigieren Sie zu **Kunden > Alle Kunden**
2. Klicken Sie auf den Namen des Kunden
3. Ändern Sie die Felder, die Sie aktualisieren möchten
4. Klicken Sie auf **Speichern**

### Was Sie bearbeiten können

**Kontaktdaten:**
- Name (über das Nutzerkonto)
- E-Mail-Adresse (über das Nutzerkonto)
- Telefonnummer
- Geburtsdatum

**Vorlieben:**
- Newsletter-Abonnement-Status
- Marketing-E-Mail-Abmeldung
- Bestellbenachrichtigungsvorlieben
- Dashboard-Layout und Sichtbarkeitseinstellungen

### Was Sie nicht bearbeiten können

Diese Felder werden basierend auf Kundengestaltungsverhalten automatisch berechnet:
- Gesamtausgaben / Kundennutzwert
- Bestellanzahl
- Kundensegment (Champion, Loyal, In Gefahr, etc.)
- RFM-Bewertungen
- Lebenszeitwertvorhersagen
- Letzte Bestelldatum
- Analyse-Zusammenfassungen

Wenn diese Felder falsch erscheinen, prüfen Sie die zugrunde liegenden Bestelldaten oder lösen Sie manuell eine Neuberechnung unter **Kunden > Analysen** → **Metriken neu berechnen**.

## Kundennachrichten

Fügen Sie interne Notizen zu Kunden hinzu, um Support-Probleme, VIP-Anfragen oder Nachfolgeaufgaben zu verfolgen.

### Notiz hinzufügen

1. Öffnen Sie das Kundeprofil
2. Scrollen Sie zu dem Abschnitt **Kundennachrichten** (kann ein separates Tab sein)
3. Klicken Sie auf **+ Notiz hinzufügen**
4. Füllen Sie die Notizdetails aus:

| Feld | Beschreibung |
|-------|-------------|
| **Notiztyp** | Allgemein, Support-Problem, Beschwerde, Lob, VIP-Dienst, Nachfolge erforderlich, Zahlungsproblem, Versandproblem |
| **Titel** | Kurze Zusammenfassung der Notiz |
| **Inhalt** | Detaillierte Notizinhalte |
| **Nachfolge erforderlich** | Markieren Sie dies, wenn eine Aktion erforderlich ist |
| **Nachfolgedatum** | Datum, bis zu dem eine Nachfolge erfolgen muss |
| **Erledigt** | Markieren Sie dies, wenn die Nachfolge abgeschlossen ist |

### Notiztypen

| Typ | Anwendungsfall |
|------|----------|
| **Allgemeine Notiz** | Jede allgemeine Beobachtung über den Kunden |
| **Support-Problem** | Aufzeichnung eines Support-Tickets oder Problems |
| **Beschwerde** | Kundenschwerde für Nachverfolgung und Lösung |
| **Lob** | Positives Feedback über den Kunden oder deren Feedback über Sie |
| **VIP-Dienst** | Sonderbehandlungsanfragen für VIP-Kunden |
| **Nachfolge erforderlich** | Aufgaben, die bis zu einem bestimmten Datum bearbeitet werden müssen |
| **Zahlungsproblem** | Notizen über Zahlungsprobleme oder Streitigkeiten |
| **Versandproblem** | Notizen über Versandprobleme oder besondere Lieferanfragen |

### Notizhistorie ansehen

Alle Notizen erscheinen in chronologischer Reihenfolge auf dem Kundeprofil. Jede Notiz zeigt:
- Erstellungsdatum und -zeit
- Erstellt von (Name des Mitarbeiter)
- Notiztyp-Abzeichen
- Titel und Inhalt
- Nachfolgestatus, wenn zutreffend

### Interne vs. für Kunden sichtbare Notizen

Alle Kundennachrichten sind standardmäßig **intern** – Kunden sehen diese Notizen nie. Sie dienen nur zur Kommunikation innerhalb des Händler-Teams.

Wenn Sie mit dem Kunden kommunizieren möchten, verwenden Sie das E-Mail-System unter **Marketing > E-Mail-Kampagnen** oder fügen Sie eine Bestellkommentar auf der spezifischen Bestellung hinzu.

## Gastkunden in registrierte Kunden umwandeln

Gastkunden werden automatisch erstellt, wenn jemand die Kasse abschließt, ohne ein Konto zu erstellen. Ihr Benutzername folgt dem Muster `guest_10374`, wobei die Zahl eine eindeutige ID ist.

Um einen Gast in einen registrierten Kunden umzuwandeln:

1. Navigieren Sie zu **Kunden > Alle Kunden**
2. Suchen Sie den Gast über ihre Bestell-E-Mail-Adresse
3. Klicken Sie auf das Gastkundenprofil
4. Klicken Sie auf den **Nutzer**-Link, um das zugrunde liegende Nutzerkonto zu bearbeiten
5. Ändern Sie den **Benutzernamen** von `guest_10374` in die echte E-Mail-Adresse des Kunden
6. Ändern Sie die **E-Mail** entsprechend
7. Geben Sie optional **Vorname** und **Nachname** ein
8. Aktivieren Sie **Passwort-Reset-E-Mail senden**, damit der Kunde ein Passwort festlegen kann
9. Klicken Sie auf **Speichern**

Der Kunde kann jetzt mit seiner E-Mail-Adresse anmelden und sieht seine früheren Gastbestellungen in seiner Bestellhistorie.

### Warum Gastkunden umwandeln?

- Gastbestellungen zählen nicht zu Kundeanalysen oder Segmente
- Gäste können keine Bestellungen verfolgen oder auf Bestellhistorie zugreifen
- Das Umwandeln von Gästen erhöht die Anzahl der registrierten Kunden und verbessert die Genauigkeit der Analysen
- Registrierte Kunden sind eher geneigt, wiederkehrende Käufe zu tätigen

## Deaktivieren vs. Löschen von Konten

### Kundenkonto deaktivieren

Deaktivierung verhindert die Anmeldung, während alle Daten erhalten bleiben:

1. Öffnen Sie das Kundeprofil
2. Klicken Sie auf den **Nutzer**-Link, um das Nutzerkonto zu bearbeiten
3. **Deaktivieren Sie "Aktiv"**
4. Klicken Sie auf **Speichern**

**Was passiert:**
- Der Kunde kann sich nicht anmelden
- Die Bestellhistorie bleibt erhalten
- Der Kunde kann später erneut aktiviert werden, indem "Aktiv" erneut aktiviert wird
- Analysen und Metriken bleiben unverändert

**Deaktivierung verwenden für:**
- Temporäre Sperren aufgrund von Zahlungsstreitigkeiten
- Blockieren von missbräuchlichen Kunden
- Kunden, die die Empfang von Zugang anfordern, aber keine Daten löschen möchten

### Kundenkonto löschen

Löschen entfernt das Konto und kann Bestellhistorie verwaisten lassen:

1. Öffnen Sie das Kundeprofil
2. Scrollen Sie zum Ende und klicken Sie auf **Löschen**
3. Bestätigen Sie das Löschen

**Was passiert:**
- Das Kundenkonto wird dauerhaft entfernt
- Das Kundeprofil wird gelöscht
- Die Bestellhistorie kann verwaist sein (Bestellungen existieren, sind aber nicht mit einem Kunden verknüpft)
- Kann nicht rückgängig gemacht werden

**Löschen verwenden für:**
- GDPR/CCPA-Datensparsanfragen (Daten zuerst exportieren)
- Testkonten, die nie existieren sollten
- Versehentlich erstellte Duplikatkonten

### GDPR-Konformität

Bevor Sie ein Kundenkonto in Reaktion auf eine GDPR-Anfrage löschen:

1. Navigieren Sie zu **Kunden > Alle Kunden**
2. Wählen Sie den Kunden aus
3. Verwenden Sie die Aktion **Daten exportieren**, um einen vollständigen Datendownload zu generieren
4. Senden Sie den Download dem Kunden, wenn er dies verlangt
5. Gehen Sie dann zum Löschen über

Der Download enthält: Kundendaten, Bestellhistorie, Adressen, Notizen und Analyse-Daten.

## Tipps

- **Verwenden Sie Filter, um hochwertige Kunden zu identifizieren** — Filtern Sie nach Kundennutzwert, um Ihre Champions und VIPs zu finden
- **Prüfen Sie Kundennachrichten regelmäßig** — Prüfen Sie mindestens wöchentlich offene Nachfolgeaufgaben
- **Bearbeiten Sie keine Analysen manuell** — Lassen Sie das System RFM-Bewertungen und Segmente automatisch berechnen
- **Wandeln Sie Gäste proaktiv um** — Nachdem ein Gast eine zweite Bestellung getätigt hat, kontaktieren Sie ihn und bieten Sie an, ein ordnungsgemäßes Konto zu erstellen
- **Verwenden Sie Deaktivierung anstelle von Löschen** — Deaktivierung bewahrt Daten und kann bei Bedarf rückgängig gemacht werden
- **Fügen Sie während Support-Telefonaten Notizen hinzu** — Dokumentieren Sie Support-Interaktionen, damit andere Teammitglieder den Kontext haben
- **Setzen Sie Nachfolgedaten** — Verwenden Sie das Nachfolgeaufgaben-System in Notizen, um sicherzustellen, dass nichts in den Hintergrund gerät
- **Respektieren Sie Kommunikationsvorlieben** — Senden Sie keine Marketing-E-Mails an Kunden, die sich abgemeldet haben

