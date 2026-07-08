---
title: Übersetzungsaufträge
---

Übersetzungsaufträge automatisieren die Masseübersetzung großer Mengen an Inhalten. Anstatt Produkte einzeln manuell zu übersetzen, erstellen Sie einen Auftrag, der Ihren gesamten Katalog – oder spezifische Teilmengen – im Hintergrund übersetzt. Aufträge laufen asynchron, sodass Sie während der automatischen Übersetzung von hunderten oder tausenden Feldern weiterarbeiten können.

Verwenden Sie Übersetzungsaufträge, wenn Sie eine neue Sprache aktivieren, neue Produkte importieren oder Lücken in nicht übersetzten Inhalten schließen.

## Was sind Übersetzungsaufträge?

Ein Übersetzungsauftrag ist eine Hintergrundaufgabe, die:

1. **Inhalte durchsucht**, um übersetzbare Felder (Produkte, Seiten, Blogbeiträge usw.) zu identifizieren
2. **Unübersetzte oder veraltete Felder** basierend auf dem Auftragsumfang erkennt
3. **Felder an die Übersetzungsmaschine** sendet (lokales AI-Modell oder externer Anbieter)
4. **Übersetzungen speichert**, zurück in Ihren Inhalt
5. **Vollständigkeit meldet**, mit Statistiken zu übersetzten Feldern

Aufträge laufen über die Celery-Auftragswarteschlange ab, sodass sie Ihr Admin-Interface nicht blockieren.

## Wann Übersetzungsaufträge verwenden

**Neue Sprache starten**:
- Aktivieren Sie Deutsch als neue Sprache
- Erstellen Sie einen Auftrag: Übersetzen Sie alle Produkte von Englisch auf Deutsch
- Ergebnis: Der gesamte Katalog ist innerhalb von Minuten/Stunden in Deutsch verfügbar (abhängig von der Größe)

**Neue Produktimporte**:
- Importieren Sie 500 neue Produkte auf Englisch
- Erstellen Sie einen Auftrag: Übersetzen Sie neue Produkte in alle aktiven Sprachen
- Ergebnis: Das neue Sortiment ist sofort in allen Märkten verfügbar

**Lücken schließen**:
- Bericht über die Abdeckung zeigt, dass Produkte nur zu 60 % auf Französisch übersetzt sind
- Erstellen Sie einen Auftrag: Übersetzen Sie nur die fehlenden französischen Produktfelder
- Ergebnis: Die Französisch-Abdeckung steigt auf ~100 %

**Veraltete Übersetzungen aktualisieren**:
- Das Übersetzungsmodell wurde verbessert oder ein neuer Anbieter ist verfügbar
- Erstellen Sie einen Auftrag: Übersetzen Sie alle Produkte erneut ins Spanische
- Ergebnis: Höhere Qualität der spanischen Übersetzungen im gesamten Katalog

## Übersetzungsauftrag erstellen

Navigieren Sie zu **Einstellungen > Übersetzungsaufträge** und klicken Sie auf **+ Auftrag erstellen**.

### Auftragskonfiguration

**Auftragsname** - Beschreibender Bezeichner (z. B. "Produkte ins Deutsche übersetzen", "Neue Blogbeiträge - alle Sprachen")

**Inhaltstyp** - Was übersetzt werden soll:
- Produkte
- Produktkategorien
- Seiten
- Blogbeiträge
- SEO-Metadaten
- E-Mail-Vorlagen
- Alle Inhaltstypen

**Quellsprache** - Die Sprache, aus der Sie übersetzen (meist Ihre Standardsprache)

**Zielsprache(n)** - Eine oder mehrere Sprachen, in die Sie übersetzen sollen (mehrere auswählen für parallele Übersetzung)

**Umfang** - Welcher Teilmenge von Inhalten:
- **Alle Elemente** - Übersetzen Sie alles, unabhängig von bestehenden Übersetzungen
- **Nur unübersetzte** - Überspringen Sie Felder, die bereits Übersetzungen haben
- **Erstellt/aktualisiert seit Datum** - Nur neue oder kürzlich geänderte Inhalte
- **Spezifische Elemente** - Wählen Sie einzelne Produkte/Seiten aus (erweiterte Filterung)

**Übersetzungsmaschine** - Welcher Dienst verwendet werden soll:
- Lokales AI-Modell (Standard, keine API-Kosten)
- Spezifischer externer Anbieter (DeepL, Google, Azure, AWS)
- Automatisch auswählen (verwendet die konfigurierte Präferenz)

**Übersetzungen sperren** - Ob übersetzte Felder vor zukünftigen automatischen Überschreibungen gesperrt werden sollen (nützlich für überprüfte Übersetzungen)

### Erweiterte Optionen

**Gesperrte Felder überspringen** - Wenn aktiviert, werden bestehende gesperrte Übersetzungen berücksichtigt (empfohlen)

**Bestehende überschreiben** - Übersetzen Sie erneut, auch wenn Übersetzungen vorhanden sind (verwenden Sie dies für Qualitätserhöhung)

**Feldfilter** - Übersetzen Sie nur bestimmte Felder (z. B. Produktbezeichnungen und Beschreibungen, Attribute überspringen)

**Batch-Größe** - Wie viele Elemente gleichzeitig verarbeitet werden sollen (Standard: 50, erhöhen Sie dies für schnellere Verarbeitung, wenn der Server dies unterstützt)

**Priorität** - Aufträge mit hoher Priorität werden vor normalen Aufträgen verarbeitet (verwenden Sie dies sparsam)

## Auftragslebenszyklus und Status

Aufträge durchlaufen diese Zustände:

**In Warteschlange** - Auftrag erstellt, wartet darauf, dass ein Worker ihn abruft

**Wird verarbeitet** - Worker übersetzt aktuell den Inhalt

**Abgeschlossen** - Alle Übersetzungen wurden erfolgreich abgeschlossen

**Fehlgeschlagen** - Der Auftrag ist auf Fehler gestoßen (prüfen Sie den Fehlerprotokoll)

**Abgebrochen** - Wurde manuell vom Admin gestoppt

**Pausiert** - Temporär unterbrochen (kann fortgesetzt werden)

## Auftragsfortschritt überwachen

Die Auftragsdetailseite zeigt:

**Fortschrittsleiste** - Prozentualer Fortschritt

**Statistiken**:
- Gesamtanzahl der zu übersetzenden Elemente
- Abgeschlossene Elemente
- Verbleibende Elemente
- Schätzung der verbleibenden Zeit

**Echtzeit-Protokoll** - Stream der Übersetzungstätigkeiten (hilfreich bei der Fehlerbehebung)

**Fehleranzahl** - Wie viele Felder die Übersetzung nicht geschafft haben (mit Gründen)

## Auftragsergebnisse und Statistiken

Wenn ein Auftrag abgeschlossen ist, zeigt die Ergebnisseite:

**Zusammenfassung**:
- Gesamtzahl der verarbeiteten Felder
- Erfolgreich übersetzte Felder
- Fehlgeschlagene Übersetzungen
- Übersprungene Felder (bereits übersetzt, gesperrt oder ausgeschlossen durch Filter)

**Einzelnen Auftrag analysieren**:
- Welche Produkte/Seiten übersetzt wurden
- Wie viele Felder pro Element
- Eventuelle auftretende Fehler

**Leistungsmaße**:
- Gesamte Zeitdauer
- Durchschnittliche Übersetzungen pro Sekunde
- Verwendete Übersetzungsmaschine

## Fehlgeschlagene Übersetzungen behandeln

Wenn einige Übersetzungen fehlschlagen:

**Überprüfen Sie das Fehlerprotokoll** - Identifiziert, welche Felder fehlgeschlagen sind und warum

**Häufige Ursachen für Fehlschläge**:
- API-Rate-Limit erreicht (externer Anbieter)
- Übersetzungsmaschine Timeout (sehr langer Text)
- Ungültiges Feldformat (JSON-Parsing-Fehler)
- Modell unterstützt keine Sprachpaare

**Wiederholungsoptionen**:
- Beheben Sie das zugrunde liegende Problem
- Erstellen Sie einen neuen Auftrag nur für die fehlgeschlagenen Elemente
- Verwenden Sie eine andere Übersetzungsmaschine

## Aufträge abbrechen und pausieren

**Abbrechen** - Stoppt den Auftrag sofort, verworfen alle laufenden Übersetzungen (bereits abgeschlossene Übersetzungen werden gespeichert)

**Pausieren** - Temporär stoppt den Auftrag, kann später von dem Punkt fortgesetzt werden, an dem er aufgehört hat

**Fortsetzen** - Fortsetzen eines pausierten Auftrags

Verwenden Sie pausieren/fortsetzen, wenn Sie temporär Serverressourcen freigeben müssen.

## Strategien für Massenaufträge

**Strategie 1: Sprache für Sprache**:
- Erstellen Sie separate Aufträge für jede Zielsprache
- Einfacherer Fortschrittsverfolgung pro Sprache
- Wichtige Sprachen können priorisiert werden
- Last wird über die Zeit verteilt

**Strategie 2: Alles auf einmal**:
- Einmaliger Auftrag, der in alle aktiven Sprachen übersetzt
- Schnellerer Gesamtabschluss
- Höhere Serverlast während der Verarbeitung
- Einfachere Auftragsverwaltung

**Strategie 3: Inhaltstyp für Inhaltstyp**:
- Übersetzen Sie zuerst Produkte (höchste Priorität)
- Danach Kategorien, Seiten, Blogbeiträge
- Ermöglicht schrittweise Umsetzung
- Einfacheres Testen und Verifizieren der Übersetzungen

Wählen Sie basierend auf Ihrer Serverkapazität, Dringlichkeit und Kataloggröße.

## Auftragsplanung

Planen Sie wiederkehrende Aufträge, um neuen Inhalt automatisch zu verarbeiten:

**Tägliche Aufträge** - Übersetzen Sie alle Produkte, die in den letzten 24 Stunden erstellt oder aktualisiert wurden

**Wöchentliche Aufträge** - Schließen Sie wöchentlich Lücken in der Übersetzung

**Nach Import** - Trigger Auftrag automatisch nach Massenproduktimport

**Bei Aktivierung einer Sprache** - Erstellen Sie automatisch einen Auftrag, wenn Sie eine neue Sprache aktivieren

Geplante Aufträge halten Übersetzungen aktuell, ohne manuelle Eingriffe.

## Leistungsüberlegungen

**Lokales AI-Modell**:
- ~100-500 Übersetzungen pro Sekunde (abhängig vom Server)
- CPU-intensiv während der Verarbeitung
- Keine API-Rate-Limits
- Kostenlos (keine Kosten pro Übersetzung)

**Externe Anbieter**:
- Rate-Limits variieren (DeepL: 500k Zeichen pro Monat auf der kostenlosen Ebene)
- API-Latenz erhöht die Overhead
- Bessere Qualität, aber Kosten entstehen
- Begrenzung der parallelen Anfragen

**Große Aufträge** (>10.000 Felder):
- Führen Sie sie während der Nebenzeit durch
- Überwachen Sie Serverressourcen
- Bedenken Sie, sie in kleinere Batches aufzuteilen
- Testen Sie zuerst mit einer Teilmenge

## Tipps

- **Beginnen Sie klein** - Testen Sie Aufträge mit einer Teilmenge (z. B. 10 Produkte) vor dem Start der vollständigen Katalogübersetzung
- **Verwenden Sie den Umfang 'Nur unübersetzte'** - Schneller und vermeidet erneutes Übersetzen bereits guter Inhalte
- **Überwachen Sie den ersten Auftrag genau** - Achten Sie auf Fehler oder Qualitätsschwächen, bevor Sie größere Aufträge starten
- **Planen Sie Aufträge während der Zeit mit geringem Verkehr** - Übersetzung ist CPU/API-intensiv
- **Sperren Sie überprüfte Übersetzungen** - Verhindert, dass Massenaufträge Ihre manuellen Änderungen überschreiben
- **Behalten Sie Aufträge fokussiert** - Kleinere, gezielte Aufträge sind einfacher zu beheben als riesige "Alles übersetzen"-Aufträge
- **Überprüfen Sie Beispiele nach Abschluss** - Prüfen Sie zufällige Übersetzungen auf Qualität, bevor Sie den Auftrag als erfolgreich betrachten
- **Exportieren/Sichern Sie vor großen Aufträgen** - Falls Sie Massenänderungen rückgängig machen müssen

