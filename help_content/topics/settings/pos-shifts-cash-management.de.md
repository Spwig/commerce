---
title: POS-Schichtwechsel und Kassenverwaltung
---

POS-Schichtwechsel verfolgen die Arbeitszeiten der Kassierer und gewährleisten eine genaue Kassenbuchhaltung. Jede Schicht stellt die Zeit eines Kassierers an einem Terminal dar – von der Öffnung der Kasse mit einem Startgeldbetrag bis zur Schließung der Schicht mit einem Endbetrag und Abstimmung. Das System berechnet automatisch den erwarteten Bargeldbestand anhand der tatsächlichen Bargeldverkäufe und vergleicht ihn mit dem physischen Bestand, wodurch Abweichungen für die Untersuchung hervorgehoben werden. Bargeldbewegungen während der Schicht (Zuschüsse zum Wechselgeld, Auszahlungen aus der Kasse) werden mit Gründen verfolgt, um vollständige Prüfprotokolle zu ermöglichen.

Navigieren Sie zu **POS > Schichtwechsel**, um alle Schichtwechsel anzuzeigen, aktive Schichtwechsel zu überwachen, Bargeldabstimmungsberichte zu überprüfen und historische Aktivitäten zu prüfen.

![Schichtliste](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Verständnis von POS-Schichtwechseln

Eine Schicht ist eine Arbeitszeit, während der ein Kassierer ein Terminal bedient. Schichtwechsel gewährleisten die Bargeldverantwortung – jeder Kassierer ist für das Bargeld in seiner Kasse während seiner Schicht verantwortlich.

**Schichtlebenszyklus**:
1. **Öffnen** - Kassierer startet die Schicht, zählt das Startgeld, notiert den Betrag
2. **Während der Schicht** - Verkäufe verarbeiten, Zahlungen annehmen, Rückerstattungen ausstellen
3. **Schließen** - Kassierer zählt das Bargeld, notiert den Endbetrag, das System berechnet die Abweichung
4. **Abgestimmt** - Schicht wird finalisiert und für die Prüfung gesperrt

**Wichtige Metriken, die verfolgt werden**:
- **Startgeld** - Anfangsbetrag in der Kasse zum Schichtbeginn
- **Endgeld** - Physisches Bargeld in der Kasse am Schichtende
- **Erwartetes Bargeld** - Berechnet: Startgeld + Bargeldverkäufe - Bargeldrückerstattungen + Bargeldbewegungen
- **Bargeldabweichung** - Abweichung: Endgeld - erwartetes Bargeld (positiv = Überschuss, negativ = Mangel)
- **Gesamte Verkäufe** - Summe aller Verkaufstransaktionen während der Schicht
- **Gesamte Rückerstattungen** - Summe aller Rückerstattungstransaktionen während der Schicht
- **Transaktionsanzahl** - Anzahl der bearbeiteten Bestellungen

## Ansicht der Schichtliste

Die Schichtliste zeigt alle Schichtwechsel mit wichtigen Informationen an:

**Schichtstatus**:
- **Offen** (grüner Badge) - Aktiv offene Schicht
- **Geschlossen** (grauer Badge) - Abgeschlossene Schicht
- **Abgestimmt** (blauer Badge) - Finalisiert und für die Prüfung gesperrt

**Terminal** - Welches POS-Terminal die Schicht verwendet hat

**Kassierer** - Mitarbeiter, der die Schicht bearbeitet hat

**Startgeld** - Anfangsbetrag

**Endgeld** - Endbetrag (leer, wenn Schicht noch offen ist)

**Erwartetes Bargeld** - Systemberechneter erwarteter Betrag basierend auf Transaktionen

**Bargeldabweichung** - Abweichung (in Rot hervorgehoben, wenn negativ, Grün, wenn positiv, Schwarz, wenn null)

**Dauer** - Schichtlänge (von Startzeit bis Endzeit)

**Gesamte Verkäufe** - Umsatz während der Schicht

Verwenden Sie Filter, um anzuzeigen:
- Nur offene Schichten (aktive Terminals überwachen)
- Schichten mit Abweichungen (Bargeldabweichung ≠ 0)
- Schichten nach Datumsbereich (tägliche Abstimmungsberichte)
- Schichten nach Kassierer (Leistungsprüfung)

## Schicht öffnen

Kassierer öffnen Schichten direkt vom POS-Terminal aus (nicht aus dem Admin). Der Workflow am Terminal:

1. **Mitarbeiter meldet sich an** - Gibt Anmeldeinformationen ein, um auf das Terminal zuzugreifen

2. **Startgeld zählen** - Zählt physisch alle Bargeld in der Kasse (Banknoten und Münzen)

3. **Startbetrag eingeben** - Notiert den gezählten Betrag in der POS-App

4. **Schicht starten** - Terminal ist bereit, Verkäufe zu verarbeiten

**Startgeld-Richtlinien**:
- Standard-Startgeld (Wechselgeld) beträgt in der Regel $100-$300, abhängig von der Größe des Geschäfts
- Zählen Sie zweimal, um Genauigkeit sicherzustellen – Fehler beim Start führen zu Abweichungen beim Schließen
- Wenn die Kasse leer ist, beträgt das Startgeld $0,00 (Wechselgeld wird über Bargeldbewegungen hinzugefügt)
- Dokumentieren Sie große Banknoten (>$50) separat, um ihre Bewegung zu verfolgen

![Schicht hinzufügen](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Während der Schicht

Während die Schicht offen ist, verfolgt das System automatisch:

**Bargeldverkäufe** - Jede Transaktion, bei der der Kunde mit physischem Bargeld zahlt (erhöht das erwartete Bargeld)

**Bargeldrückerstattungen** - Jede Rückerstattung in Bargeld (verringert das erwartete Bargeld)

**Kartenverkäufe** - Kredit-/Debitkartentransaktionen (kein Einfluss auf Bargeld)

**Teilzahlung** - Teilweise Bargeld + Teilweise Karte (nur der Bargeldanteil beeinflusst das erwartete Bargeld)

**Geschenkkarten & Gutscheine** - Nicht-Bargeld-Zahlungsmethoden (kein Einfluss auf Bargeld)

Kassierer verarbeiten weiterhin Verkäufe normal. Das System führt eine laufende Berechnung des erwarteten Bargelds im Hintergrund durch.

## Bargeldbewegungen

Bargeldbewegungen sind Anpassungen der Kasse während einer Schicht:

**Wechselgeldzuschüsse** - Bargeld in die Kasse hinzufügen:
- Grund: "Wechselgeld hinzufügen für große Banknoten"
- Betrag: +$100,00
- Erwartetes Bargeld erhöht sich um $100,00

**Kleingeldabhebungen** - Bargeld für Ausgaben entfernen:
- Grund: "Kauf von Bürobedarf"
- Betrag: -$25,00
- Erwartetes Bargeld verringert sich um $25,00

**Bankablieferungen** - Überschüssiges Bargeld für Sicherheit entfernen:
- Grund: "Sicherheitsablieferung – mehr als $500 in der Kasse"
- Betrag: -$300,00
- Erwartetes Bargeld verringert sich um $300,00

**Bargeldbewegungen am Terminal aufzeichnen**:
1. Tippen Sie auf **Menü** > **Bargeldbewegung**
2. Wählen Sie den Typ: Hinzufügen oder Entfernen
3. Geben Sie den Betrag ein
4. Geben Sie den Grund an (erforderlich für die Prüfung)
5. Bestätigen Sie

Alle Bargeldbewegungen erscheinen im Schichtdetailbericht mit Zeitstempeln, Beträgen und Gründen.

## Schicht schließen

Wenn ein Kassierer seine Arbeitszeit beendet hat, schließt er die Schicht:

1. **Schicht schließen tippen** - Im Terminalmenü

2. **Verbleibende Transaktionen verarbeiten** - Beenden Sie alle geparkten Wagen oder ausstehenden Verkäufe

3. **Endgeld zählen** - Zählen Sie physisch alle Bargeld in der Kasse
   - Zählen Sie Banknoten nach Nennwert ($100s, $50s, $20s, $10s, $5s, $1s)
   - Zählen Sie Münzen nach Typ (25-Cent-Stücke, 10-Cent-Stücke, 5-Cent-Stücke, 1-Cent-Stücke)
   - Gesamt = Endgeldbetrag

4. **Endbetrag eingeben** - Notieren Sie den gezählten Gesamtbetrag

5. **System berechnet Abweichung**:
   - Erwartetes Bargeld = Startgeld + Bargeldverkäufe - Bargeldrückerstattungen + Bargeldzuschüsse (Bewegungen)
   - Bargeldabweichung = Endgeld - erwartetes Bargeld
   - Beispiel: Endgeld $485,00 - Erwartetes $480,00 = +$5,00 Überschuss

6. **Abweichung überprüfen** - Das Terminal zeigt die Abweichung an:
   - **Genau ($0,00)** - Perfekte Abstimmung
   - **Kleiner Überschuss (+$1 bis +$5)** - Akzeptable Rundung oder Kundschaftstipp
   - **Kleiner Mangel (-$1 bis -$5)** - Kleinere Zählfehler, akzeptabel
   - **Große Abweichung (>$5)** - Neues Zählen erforderlich

7. **Wenn nötig, erneut zählen** - Wenn die Abweichung groß (>$10) ist, sollte der Kassierer das Endgeld erneut zählen, bevor er die Schicht abschließt

8. **Schicht abschließen** - Bestätigen Sie den Endbetrag, der Schichtstatus ändert sich in "Geschlossen"

9. **Schichtbericht drucken** - Das Terminal druckt einen Bargeldabstimmungsbeleg für die Aufzeichnungen des Kassierers

![Schichtdetails](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Bargeldabstimmungsformel

Das System berechnet das erwartete Bargeld mit dieser Formel:

```
Erwartetes Bargeld = Startgeld
                + Bargeldverkäufe
                - Bargeldrückerstattungen
                + Bargeldzuschüsse (Bewegungen)
                - Bargeldentfernungen (Bewegungen)
```

**Beispiel**:
- Startgeld: $200,00
- Bargeldverkäufe: $450,00 (aus 15 Transaktionen)
- Bargeldrückerstattungen: -$30,00 (1 Rückgabe)
- Bargeldzuschuss: +$100,00 (Wechselgeld während der Schicht hinzugefügt)
- Bargeldentnahme: -$50,00 (Kleingeldabhebung)
- **Erwartetes Bargeld: $200 + $450 - $30 + $100 - $50 = $670,00**

Wenn der Kassierer $675,00 am Ende zählt:
- Bargeldabweichung: $675,00 - $670,00 = **+$5,00 Überschuss**

## Schichtberichte und Prüfung

Schichtberichte liefern detaillierte Abstimmungsinformationen:

**Zusammenfassungsabschnitt**:
- Start- und Endgeld
- Erwartetes Bargeldberechnung
- Bargeldabweichung (Überschuss/Mangel)
- Gesamte Verkäufe und Rückerstattungen
- Transaktionsanzahl
- Schichtdauer

**Transaktionsdetails**:
- Alle Verkäufe während der Schicht (Bestell-IDs, Beträge, Zahlungsmethoden)
- Alle Rückerstattungen
- Zeitstempel jeder Transaktion

**Bargeldbewegungsprotokoll**:
- Alle Hinzufügungen und Entfernungen
- Angegebene Gründe
- Zeitstempel

**Anwendungsfälle**:
- **Tägliche Abstimmung** - Alle Schichten am Ende des Geschäftstages überprüfen
- **Kassiererleistung** - Muster von Abweichungen nach Mitarbeiter identifizieren
- **Diebstahlerkennung** - Große, konsistente Mangeln deuten auf Diebstahl hin
- **Schulungsbedarf** - Häufige kleine Abweichungen zeigen Probleme mit der Zählgenauigkeit an
- **Prüfprotokoll** - Vollständige Aufzeichnung für Buchhaltung und Steuerzwecke

## Mehr-Terminal-Bargeldverwaltung

Für Geschäfte mit mehreren Terminals, die gleichzeitig Schichten abwickeln:

**Separate Kassen** – Jeder Terminal hat seine eigene Kasse – Schichten sind unabhängig. Kassierer A am Terminal 1 und Kassierer B am Terminal 2 führen separate Schichten mit separater Abstimmung durch.

**Gemeinsame Kasse** – Einige Geschäfte teilen eine Kasse über mehrere Terminals (nicht empfohlen). Wenn dies der Fall ist:
- Nur eine Schicht kann pro gemeinsamer Kasse offen sein
- Kassierer müssen die Schicht schließen, wenn sie an den nächsten Kassierer übergeben
- Bargeldbewegungen verfolgen alle Hinzufügungen/Entfernungen während der Übergabe
- Abweichungen sind schwerer auf bestimmte Kassierer zuzuordnen

**Best Practices**: Eine Kasse pro Terminal, eine Schicht pro Kassierer pro Sitzung. Dies gewährleistet klare Verantwortung und vereinfachte Abstimmung.

## Umgang mit Abweichungen

Wenn das geschlossene Bargeld nicht mit dem erwarteten Bargeld übereinstimmt:

**Kleine Abweichungen (<$5)**:
- Akzeptabel aufgrund von Rundung, Zählfehlern oder Kunden-Tipps
- Dokumentieren Sie dies in den Schichtnotizen
- Keine weitere Maßnahmen erforderlich, es sei denn, ein Muster entsteht

**Mittlere Abweichungen ($5-$20)**:
- Zählen Sie das Bargeld erneut, bevor Sie die Schicht abschließen
- Prüfen Sie den Transaktionsprotokoll auf Fehler (falsches Wechselgeld gegeben, nicht verarbeitete Stornotransaktion)
- Dokumentieren Sie die Umstände in den Schichtnotizen
- Empfohlene Prüfung durch den Manager

**Große Abweichungen (>$20)**:
- Erneutes Zählen ist obligatorisch
- Managerzustimmung erforderlich, um die Schicht zu schließen
- Prüfen Sie alle Transaktionen und Bargeldbewegungen
- Untersuchen Sie mögliche Ursachen (Diebstahl, Kassenkarte, falsches Startgeld)
- Je nach Umständen kann eine disziplinarische Maßnahme erforderlich sein

**Konsistente Mangel**:
- Muster von negativen Abweichungen vom gleichen Kassierer = Schulungsproblem oder Diebstahl
- Implementieren Sie zusätzliche Aufsicht (Manager-Prüfung während der Schicht)
- Prüfen Sie die POS-Schulungsverfahren
- Überlegen Sie sich eine Aktualisierung der Bargeldverwaltungsrichtlinien

## Tipps

- **Startgeld zweimal zählen** – Fehler beim Start führen zu Abweichungen beim Schließen; Genauigkeit am Anfang verhindert Probleme am Ende
- **Bargeldbewegungen sofort dokumentieren** – Warten Sie nicht bis zum Schließen, um Zuschüsse zum Wechselgeld oder Kleingeldabhebungen zu dokumentieren
- **Gründe für Bewegungen immer angeben** – "$100 hinzugefügt" ist für die Prüfung nutzlos; "$100 hinzugefügt für Wechselgeld (zu wenige $5-Banknoten)" ist handlungsorientiert
- **Wenn Abweichung >$10, erneut zählen** – Schließen Sie keine Schicht mit einer großen Abweichung ohne erneutes Zählen
- **Schichtberichte täglich drucken** – Anhängen an tägliche Abstimmungsdokumente für die Buchhaltung
- **Muster überprüfen, nicht einzelne Abweichungen** – Ein -$3,00 Mangel ist in Ordnung; fünf aufeinanderfolgende -$3,00 Mangel sind ein Problem
- **Schichten am Ende des Tages schließen** – Schichten nicht über Nacht offen lassen; Abweichungen sind einfacher zu untersuchen, wenn sie kürzlich sind
- **Kassierer in der Zählung nach Nennwert trainieren** – Die meisten Fehler entstehen durch falsches Zählen von Banknoten (z. B. eine $5-Banknote als $10-Banknote zu erkennen)
- **Münfenster verwenden** – Vorgewickelte Münzen reduzieren Zählfehler und beschleunigen die Abstimmung

