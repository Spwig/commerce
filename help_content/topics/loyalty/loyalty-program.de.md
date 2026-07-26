---
title: Loyalitätsprogramm
---

Das Loyalitätsprogramm ermöglicht es Ihnen, Kunden für Einkäufe und Engagement mit einem Punktesystem zu belohnen. Kunden sammeln Punkte, steigen in Stufen auf und können Belohnungen einlösen. Navigieren Sie zu **Marketing > Loyalitätsprogramm** in der Admin-Seitenleiste.

![Loyalitätsdashboard](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Loyalitätsdashboard

Das Dashboard bietet einen umfassenden Überblick über Ihr Loyalitätsprogramm:

### Schlüsselmetriken

- **Gesamtmitglieder** — Gesamtzahl der angemeldeten Kunden
- **Aktive Mitglieder (30d)** — Mitglieder, die in den letzten 30 Tagen Punkte gesammelt oder eingelöst haben
- **Punkte in Höhe** — Gesamtzahl der noch nicht eingelösten Punkte aller Mitglieder
- **Einlösungsrate** — Prozentsatz der gesammelten Punkte, die eingelöst wurden
- **Punkte gesammelt (30d)** — Punkte, die in den letzten 30 Tagen gesammelt wurden
- **Punkte eingelöst (30d)** — Punkte, die in den letzten 30 Tagen eingelöst wurden
- **Durchschnittliche Punkte/Member** — Durchschnittlicher Punktestand pro Mitglied
- **Aktive Regeln** — Anzahl der aktuell aktiven Sammelregeln

### Schnellaktionen

Das Dashboard enthält Karten mit Kurzweg-Links, um alle Aspekte des Programms zu verwalten:
- **Mitglieder** — Mitglieder des Loyalitätsprogramms ansehen und verwalten
- **Stufen** — Mitgliedsstufen konfigurieren
- **Belohnungen** — Katalog der Belohnungen einrichten
- **Einlösungen** — Einlösungsverlauf ansehen
- **Regeln** — Konfigurieren, wie Punkte gesammelt werden
- **Abzeichen** — Erfolgsabzeichen verwalten
- **Kampagnen** — Besondere Loyalitätskampagnen durchführen
- **Segmentierung** — Mitgliedersegmente für Zielgruppen erstellen

### Diagramme und Analysen

- **Mitgliederregistrierungstrend** — Neuanmeldungen im Laufe der Zeit
- **Punkte gesammelt vs. eingelöst** — Verlauf des Punktestands verfolgen
- **Stufenverteilung** — Sehen Sie, wie Mitglieder sich über die Stufen verteilen

## Einrichten des Programms

### Schritt 1: Stufen erstellen

Stufen definieren Mitgliedslevels mit zunehmenden Vorteilen:

1. Navigieren Sie zu **Loyalität > Stufen**
2. Erstellen Sie Stufen wie Bronze, Silber, Gold, Platinum
3. Für jede Stufe legen Sie fest:
   - **Name** — Anzeigename der Stufe
   - **Rang** — Sortierreihenfolge (niedrigerer Rang = niedrigere Stufe, z. B. Bronze = 1, Silber = 2)
   - **Farbe** — Visuelle Akzentfarbe, die auf den Mitgliedsabzeichen angezeigt wird
   - **Mindestpunkte** — Gesamtpunkte, die erforderlich sind, um für diese Stufe qualifiziert zu sein
   - **Mindestumsatz** — Gesamtbetrag, der erforderlich ist, um für diese Stufe qualifiziert zu sein
   - **Mindestbestellungen** — Anzahl der Bestellungen, die erforderlich sind, um für diese Stufe qualifiziert zu sein
   - **Punktevervielfachung** — Bonus-Sammelrate für Mitglieder in dieser Stufe (z. B. 2,0 = 2x Punkte)

Ein Mitglied qualifiziert sich für eine Stufe, wenn **irgendeine** der drei Schwellenwerte erreicht wird. Sie können nur eine Schwellenwert verwenden oder alle drei kombinieren.

### Schritt 2: Sammelregeln konfigurieren

Regeln definieren, wie Kunden Punkte sammeln:

1. Navigieren Sie zu **Loyalität > Regeln**
2. Erstellen Sie Regeln mithilfe einer der vier Regeltypen:

| Regeltyp | Beschreibung | Beispiel |
|-----------|-------------|---------|
| **Kauf** | Punkte pro Ausgabenbetrag | 1 Punkt pro $1 |
| **Artikel** | Punkte pro gekauftem Artikel | 50 Punkte pro Produkt in einer bestimmten Kategorie |
| **Aktion** | Punkte für eine bestimmte Aktion | 200 Punkte für die Registrierung |
| **Ereignis** | Punkte für ein Kalenderereignis | Geburtstagsbonuspunkte |

3. Konfigurieren Sie zusätzliche Regeloptionen:
   - **Bereich / Bereichsfilter** — Die Regel auf bestimmte Produkte, Kategorien oder Kundenstufen beschränken
   - **Mindestbestellwert** — Mindestwert des Warenkorbs, um die Regel anzuwenden
   - **Erlaubte Stufen** — Die Regel auf bestimmte Mitgliedsstufen beschränken
   - **Exklusiv** — Wenn aktiviert, kann diese Regel nicht mit anderen Regeln叠加
   - **Punkteverzögerung in Tagen** — Anzahl der Tage, bis gesammelte Punkte zur Verfügung stehen (hilfreich, um Rückgabetermine zu berücksichtigen)
   - **Punkteablauf in Tagen** — Anzahl der Tage nach der Sammlung, bis die Punkte ablaufen (leer lassen, um keinen Ablauf zu ermöglichen)
   - **Start-/Enddatum** — Die Regel auf einen Datumsbereich beschränken

### Schritt 3: Belohnungen einrichten

Belohnungen sind das, was Kunden mit ihren Punkten einlösen können:

1. Navigieren Sie zu **Loyalität > Belohnungen**
2. Erstellen Sie Belohnungen wie:
   - **$5 Gutschein** — 500 Punkte
   - **Kostenlose Lieferung** — 300 Punkte
   - **10 % Rabatt** — 1000 Punkte

> **Gutscheincodes können derzeit nicht eingelöst werden.** Eine Belohnung mit **Belohnungstyp** auf **Gutscheincode** — wie der $5-Gutschein oder der 10%-Rabatt oben genannten Beispiele — kann derzeit nicht eingelöst werden.

Der Mitglied sieht eine klare Fehlermeldung und seine Punkte werden automatisch an sein Guthaben zur\xfcckgegeben, sodass nichts verloren geht, aber die Belohnung noch nicht verwendbar ist.

Dies ist eine bewusste Korrektur: Die Einlösung meldete fr\xfcher Erfolg an, w\xe4hrend sie heimlich Punkte abzog und nichts ausgab.

Wenn Mitglieder erw\xe4hnen, dass eine Einlösung „nicht funktioniert“, dann ist dies dies — kein neues Problem.

Gutscheine werden in einer bevorstehenden Ver\xf6ffentlichung wieder funktionieren.

Dies betrifft nicht die Freiversand-, Freeprodukt- oder Erlebnis/Vorteilsbelohnungen.

### Schritt 4: Abzeichen erstellen (optional)

Abzeichen erkennen Kundenleistungen:

1. Navigieren Sie zu **Loyalit\xe4t > Abzeichen**
2. Erstellen Sie Abzeichen f\xfcr Meilensteine:
   - **Erster Kauf** — Verliehen nach dem ersten Bestellung
   - **Gro\xdfspender** — Verliehen nach Ausgaben von $500+
   - **Treuer Kunde** — Verliehen nach 10 Bestellungen

Abzeichen k\xf6nnen Bonuspunkte vergeben, wenn sie erlangt werden.

## Mitglieder verwalten

### Mitgliederliste

Sehen Sie sich alle Loyalit\xe4tsmitglieder mit:
- Aktueller Stufe und Status
- Punkteguthaben
- Registrierungsdatum
- K\xfcrzlich Aktivit\xe4t

### Top Punkteverdiener

Das Dashboard hebt Ihre aktivsten Mitglieder hervor, mit einer Rangliste, die Rang, Name, Stufe und in dem Zeitraum verdiente Punkte anzeigt.

### K\xfcrzliche Transaktionen

Ein Transaktionsprotokoll zeigt alle k\xfcrzlichen Punkteaktivit\xe4ten an. Transaktionsarten umfassen:

| Typ | Bedeutung |
|------|---------|
| **Erwerben** | Punkte, die durch eine qualifizierende Kauf oder Regel gutgeschrieben werden |
| **Einl\xf6sen** | Punkte, die f\xfcr eine Belohnung ausgegeben werden |
| **Bonus** | Zusatzpunkte von einem Abzeichen, Kampagne oder manueller Verleihung |
| **Anpassung** | Manuelle Punktekorrektur durch ein Mitglied des Personals |
| **Entziehen** | Punkte, die entfernt werden (z. B. nach Bestellstornierung) |
| **Ablauf** | Punkte, die ihren Ablaufdatum \xfcberschritten haben |

### Manuelle Punkteanpassungen

Sie k\xf6nnen Punkte f\xfcr jedes Mitglied manuell hinzuf\xfcgen oder abziehen:

1. \xd6ffnen Sie die Detailseite des Mitglieds
2. Klicken Sie auf **Punkte anpassen**
3. Geben Sie die Punkteanzahl ein (positiv, um Punkte hinzuzuf\xfcgen, negativ, um Punkte abzuziehen)
4. Geben Sie den Grund f\xfcr die Anpassung ein
5. Klicken Sie auf **Speichern**

Die Anpassung wird als Transaktion aufgezeichnet und ist im Transaktionsverlauf des Mitglieds sichtbar.

## Kampagnen

Loyalit\xe4tskampagnen erm\xf6glichen Ihnen, besondere Promotionen durchzuf\xfchren:
- **Doppelte Punkte am Wochenende** — Tempor\xe4res Erh\xf6hen der Erwerbsrate
- **Bonuspunkteveranstaltungen** — Zusatzpunkte f\xfcr bestimmte Aktionen vergeben
- **Stufenupgrade-Kampagnen** — Das Schwellenwert f\xfcr Stufenwechsel senken

## Tipps

- Beginnen Sie mit einfachen Erwerbsregeln (1 Punkt pro $1 ausgegeben) und erweitern Sie im Laufe der Zeit.
- Setzen Sie erreichbare Belohnungsschwellen, um Mitglieder engagiert zu halten — wenn Belohnungen unerreichbar wirken, verlieren Mitglieder das Interesse.
- Nutzen Sie Abzeichen, um das Erlebnis zu gamifizieren und bestimmte Verhaltensweisen zu f\xf6rdern.
- \xdcberwachen Sie die Einl\xf6sungsrate — ein gesundes Programm hat eine Einl\xf6sungsrate von 10-30 %.
- F\xfchren Sie Kampagnen in Zeiten geringer Aktivit\xe4t durch, um die Teilnahme zu erh\xf6hen.
- Nutzen Sie den Diagramm „Verdiente Punkte vs. Einl\xf6ste Punkte“, um sicherzustellen, dass Ihr Programm nachhaltig ist.