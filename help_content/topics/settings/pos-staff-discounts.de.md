---
title: POS-Mitarbeiter-Rabatte und Terminal-Sicherheit
---

Die Einstellungen für POS-Mitarbeiter-Rabatte ermöglichen es Ihnen, zu steuern, wie viel Rabatt jeder Mitarbeiter am Verkaufspunkt anwenden kann. Ereignisse zum Sperren des Terminals geben eine Überprüfungsprotokoll für jedes Mal, wenn ein Terminal gesperrt oder entsperrt wurde – helfen Sie dabei, zu verfolgen, wer auf das Terminal zugegriffen hat und ob es Versuche zum Fehlversuch des Anmeldeversuchs gab.

## Mitarbeiter-Rabattgrenzen

Jeder Mitarbeiter, der den POS verwendet, kann individuelle Rabattberechtigungen haben. Standardmäßig können Mitarbeiter bis zu 10 % Rabatt auf Artikel oder den gesamten Warenkorb anwenden. Sie können diese Grenze pro Person erhöhen oder verringern oder Mitarbeiter als Manager bezeichnen, die Rabatte genehmigen können, die die Standardgrenzen überschreiten.

### Konfigurieren der Rabattgrenze eines Mitarbeiters

1. Navigieren Sie zu **POS > Mitarbeiter-Rabatte**
2. Klicken Sie auf **+ Mitarbeiter-Rabatt hinzufügen** oder klicken Sie auf einen vorhandenen Mitarbeiter, um ihn zu bearbeiten
3. Wählen Sie den **Mitarbeiter** aus der Liste aus
4. Legen Sie die Rabattgrenzen fest:

| Feld | Beschreibung |
|-------|-------------|
| **Maximaler Rabatt %** | Maximale Prozentsatz-Rabatt, den diese Person anwenden kann (z. B. `10` für 10 %) |
| **Maximaler Rabattbetrag** | Maximale feste Geldsumme pro Transaktion (leer lassen, um keine feste Obergrenze festzulegen) |
| **Kann Artikel-Rabatte anwenden** | Erlaubt das Anwenden von Rabatten auf einzelne Zeilen |
| **Kann Warenkorb-Rabatte anwenden** | Erlaubt das Anwenden von Rabatten auf den gesamten Warenkorb |
| **Benötigt Grund** | Wenn aktiviert, muss der Mitarbeiter einen Grund eingeben, bevor er einen Rabatt anwendet |

5. Klicken Sie auf **Speichern**

### Wie Rabattgrenzen am POS funktionieren

Wenn ein Kassierer versucht, einen Rabatt anzuwenden:
- Wenn der Rabatt innerhalb seiner Grenze liegt, wird er sofort angewendet
- Wenn der Rabatt seine Grenze überschreitet, fragt das Terminal nach **Manager-Genehmigung**
- Ein Manager gibt sein PIN ein, um die Ûernahme zu genehmigen, und der Rabatt wird angewendet

Dieser Workflow verhindert nicht autorisierte hohe Rabatte, während er Flexibilität gewährt, wenn echte Rabatte gerechtfertigt sind.

## Manager-Rollen

Mitarbeiter mit dem **Ist Manager**-Flag können Rabatte genehmigen, die andere Mitarbeitergrenzen überschreiten. Manager werden am Terminal durch ein PIN identifiziert, das sie eingeben müssen, wenn eine Genehmigung erforderlich ist.

### Einrichten eines Managers

1. Öffnen Sie das Rabatt-Protokoll eines Mitarbeiters
2. Aktivieren Sie **Ist Manager**
3. Geben Sie ein **Manager-PIN** (4-6 Ziffern) ein – dies wird sicher gehasht, wenn es gespeichert wird
4. Klicken Sie auf **Speichern**

Das Manager-PIN ist von dem Kassierer-PIN getrennt, der für das Sperren/Entsperren des Terminals verwendet wird. Ein Manager kann sowohl ein Manager-PIN (für Rabattgenehmigungen) als auch ein Kassierer-PIN (für Terminalzugriff) haben.

### Sicherheit des Manager-PIN

Wenn Sie ein PIN im Admin-Formular eingeben und speichern, hash Spwig es automatisch – das Klartext-PIN wird nie gespeichert. Das Klartext-PIN-Feld wird nach dem Speichern geleert, was ein erwartetes Verhalten ist.

## Kassierer-PINs und Kartenzugriff

Jeder Mitarbeiter kann auch ein **Kassierer-PIN** für das Sperren und Entsperren des Terminals haben:

- **Kassierer-PIN** – 4-6 Ziffern PIN, der zum Entsperren des Terminals nach dem automatischen Sperren oder manuellen Sperren verwendet wird
- **Karten-Identifikator** – Eine registrierte Karte (Schwipkkarte oder NFC) kann auch zum Entsperren des Terminals verwendet werden

Um ein Kassierer-PIN einzurichten, geben Sie es in das Feld **Kassierer-PIN** ein und speichern Sie es. Wie das Manager-PIN wird es automatisch gehasht, wenn es gespeichert wird.

## Terminal-Sperre-Ereignisse

Jedes Mal, wenn ein Terminal gesperrt oder entsperrt wird, protokolliert Spwig ein Terminal-Sperre-Ereignis. Dies erstellt ein vollständiges Sicherheitsprotokoll.

### Anzeigen von Sperre-Ereignissen

Navigieren Sie zu **POS > Terminal-Sperre-Ereignisse**, um die vollständige Historie anzuzeigen. Sie können Ereignisse nach folgenden Kriterien filtern:
- Terminal
- Ereignistyp
- Datumsbereich

### Ereignistypen

| Ereignis | Bedeutung |
|-------|---------|
| **Manueller Sperrvorgang** | Ein Mitarbeiter hat absichtlich den Terminal gesperrt |
| **Automatische Sperre (Inaktivitätszeitlimit)** | Der Terminal wurde automatisch aufgrund von Inaktivität gesperrt |
| **Entsperrung durch Kassierer** | Der Kassierer hat sich authentifiziert und den Terminal entsperrt |
| **Entsperrung durch Manager** | Ein Manager hat seine Anmeldeinformationen verwendet, um den Terminal zu entsperren |
| **Entsperrung durch Karte** | Der Terminal wurde mit einer registrierten Swipe-Karte entsperrt |
| **Entsperrung durch Biometrie** | Der Terminal wurde mit Fingerabdruck oder Gesichtserkennung entsperrt |
| **Fehlgeschlagene Entsperrversuche** | Ein Entsperrversuch wurde mit falschen Anmeldeinformationen durchgeführt |
| **Sperrung (3+ Fehlschläge)** | Der Terminal wurde nach mehreren fehlgeschlagenen Versuchen gesperrt |

### Was Sperrereignisprotokolle enthalten

Jedes Ereignis protokolliert:
- Den betroffenen **Terminal**
- Den **Ereignistyp**
- Wer die Aktion durchgeführt hat (**Durchgeführt von**) und wer bei der Sperrung angemeldet war (**Gesperrt von**)
- Ob eine **Manager-Übernahme** verwendet wurde
- Die **Entsperrmethode** (PIN, Karte oder biometrisch)
- **Fehlversuche** vor diesem Ereignis (hilfreich bei der Erkennung von Brute-Force-Mustern)
- Den **Warenkorb-Gesamtbetrag** und die Artikelanzahl zum Zeitpunkt des Ereignisses
- Die IP-Adresse der Anfrage

### Sicherheitsbedenken untersuchen

Wenn Sie unerlaubten Zugriff auf einen Terminal vermuten:

1. Navigieren Sie zu **POS > Terminal-Sperrereignisse**
2. Filtern Sie nach dem betreffenden Terminal
3. Suchen Sie nach Ereignissen des Typs **Fehlgeschlagene Entsperrversuche** oder **Sperrung** – diese deuten auf wiederholte fehlgeschlagene Zugriffe hin
4. Prüfen Sie das Feld **Durchgeführt von** bei erfolgreichen Entsperrungen, um zu sehen, wer Zugriff erhielt
5. Vergleichen Sie dies mit den Schichtprotokollen (**POS > Schichten**), um den Kassierer zu überprüfen, der theoretisch im Dienst sein sollte

## Tipps

- Legen Sie Rabattgrenzen basierend auf der Mitarbeitererfahrung fest – neue Mitarbeiter könnten mit 5 % beginnen, erfahrene Mitarbeiter mit 10–15 %, und Manager können alles Höhere genehmigen.
- Aktivieren Sie **Benötigt Grund** für Mitarbeiter mit höheren Rabattgrenzen. Ein Grund im Protokoll hilft Ihnen, Rabattmuster zu analysieren und mögliche Missbrauchsfälle zu erkennen.
- Überprüfen Sie Terminal-Sperrereignisse wöchentlich, wenn Ihr Geschäft mehrere Mitarbeiter oder einen hohen Mitarbeiterwechsel hat – unregelmäßige Zugriffsereignisse sind leichter zu erkennen, bevor sie ein Problem werden.
- Wenn ein Mitarbeiter das Unternehmen verlässt, entfernen Sie sofort seine Kassierer-PIN und Kartenidentifikation, um den Terminal-Zugriff zu verhindern.
- Nutzen Sie das Sperrereignis, um Terminals zu identifizieren, bei denen das automatische Zeitlimit für die Sperre angepasst werden muss – wenn Kunden häufig versehentlich gesperrt werden, könnte das Inaktivitätszeitlimit zu kurz eingestellt sein.
- Manager-PINs sollten regelmäßig geändert werden. Aktualisieren Sie sie im Mitarbeiter-Rabatt-Protokoll – die neue PIN wird beim Speichern gehasht.