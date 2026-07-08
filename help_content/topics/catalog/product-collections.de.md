---
title: Produktkollektionen
---

Kollektionen ermöglichen es Ihnen, Produkte zu gruppieren, um sie auf Ihrem Verkaufsstandort anzuzeigen. Im Gegensatz zu Kategorien – die Ihre gesamte Katalogstruktur in eine permanente Hierarchie organisieren – sind Kollektionen flexibel und kuriert, Gruppierungen, die Sie für einen bestimmten Zweck erstellen. Eine Kollektion könnte neue Artikel hervorheben, Produkte für eine saisonale Kampagne zeigen oder eine sorgfältig ausgewählte Auswahl an Bestsellern präsentieren.

Navigieren Sie zu **Katalog > Kollektionen**, um Ihre Kollektionen zu verwalten.

## Kollektionen vs. Kategorien

Sowohl Kategorien als auch Kollektionen gruppieren Produkte, aber sie dienen unterschiedlichen Zwecken:

|  | Kategorien | Kollektionen |
|---|---|---|
| **Zweck** | Permanente Katalogstruktur | Flexibel, kurierte Gruppierungen |
| **Hierarchie** | Ja – verschachtelte Eltern-/Kindstruktur | Nein – flache Gruppierungen |
| **Produkte pro Gruppe** | Jedes Produkt gehört zu einer Kategorie | Ein Produkt kann in vielen Kollektionen erscheinen |
| **Typische Verwendung** | Shop-Navigationsmenü, durch Abteilung suchen | Startseiten, Kampagnen, ausgewählte Sets |

Verwenden Sie Kategorien für "wie Ihr Shop organisiert ist" und Kollektionen für "was Sie jetzt hervorheben möchten".

## Kollektionstypen

Beim Erstellen einer Kollektion wählen Sie einen Typ, der dem entspricht, wie Sie die Produktliste verwalten möchten:

| Typ | Wie Produkte hinzugefügt werden |
|---|---|
| **Manuelle Auswahl** | Sie wählen genau die Produkte aus, die angezeigt werden, nacheinander |
| **Automatische Regeln** | Produkte werden automatisch basierend auf Kriterien, die Sie definieren, hinzugefügt |
| **Ausgewählte Produkte** | Eine kurierte redaktionelle Auswahl, die manuell verwaltet wird |
| **Saisonal** | Eine zeitbasierte Auswahl, typischerweise manuell für Kampagnen verwaltet |

Manuelle und ausgewählte Typen geben Ihnen präzise Kontrolle. Automatische Kollektionen können mit Ihrem Katalog wachsen, ohne dass eine laufende Wartung erforderlich ist.

## Eine Kollektion erstellen

1. Navigieren Sie zu **Katalog > Kollektionen**
2. Klicken Sie auf **+ Kollektion hinzufügen**
3. Füllen Sie den Abschnitt **Grundlegende Informationen** aus:
   - **Name** – der Name der Kollektion, wie er auf Ihrem Verkaufsstandort angezeigt wird
   - **Slug** – der URL-Pfad für die Kollektionsseite (automatisch aus dem Namen gefüllt; Sie können ihn anpassen)
   - **Beschreibung** – eine Beschreibung, die auf der Verkaufsstandortseite der Kollektion angezeigt wird
4. Wählen Sie einen **Kollektionstyp**
5. Fügen Sie Produkte hinzu:
   - Für **Manuelle Auswahl** und **Ausgewählte Produkte**-Typen: verwenden Sie das Feld **Produkte**, um nach und zu Produkten zu suchen
   - Für **Automatisch**-Typ: definieren Sie die Kriterien im Feld **Automatische Kriterien**
6. Laden Sie Bilder hoch:
   - **Bild** – das Hauptbild der Kollektion, das auf Listenseiten und Vorschaubildern verwendet wird
   - **Bannerbild** – ein breiteres Bannerbild, das oben auf der Kollektionsseite angezeigt wird
7. Konfigurieren Sie **SEO**-Felder (optional, aber empfohlen):
   - **Meta-Titel** – der Titel der Seite, der in Suchergebnissen angezeigt wird
   - **Meta-Beschreibung** – die Beschreibung, die unter dem Titel in Suchergebnissen angezeigt wird
8. Setzen Sie **Anzeigeoptionen**:
   - **Aktiv** – steuert, ob die Kollektion auf Ihrem Verkaufsstandort sichtbar ist
   - **Als ausgewählt markieren** – markiert die Kollektion für eine ausgewählte Platzierung in Ihrem Theme
   - **Sortierreihenfolge** – steuert die Reihenfolge, in der Kollektionen auf Listenseiten angezeigt werden (niedrigere Zahlen werden zuerst angezeigt)
9. Klicken Sie auf **Speichern**

## Produkte zu einer Kollektion hinzufügen

Für manuelle Kollektionen verwenden Sie das Feld **Produkte** mit automatischer Vervollständigung, um in Ihrem Katalog zu suchen und Artikel auszuwählen. Sie können so viele Produkte hinzufügen, wie Sie benötigen – es gibt keine Grenze.

Produkte können gleichzeitig zu mehreren Kollektionen gehören. Zum Beispiel könnte ein Produkt sowohl in Ihrer Kollektion "Sommerverkauf" als auch in Ihrer Kollektion "Bestseller" enthalten sein, ohne dass dies zu einem Konflikt führt.

## Kollektionen auf Ihrem Verkaufsstandort anzeigen

Jede Kollektion erhält automatisch ihre eigene Seite unter `/collection/{slug}/`. Sie können Links zu Kollektionsseiten von Ihrem Navigationsmenü, dem Seitenbuilder oder Werbebanner ausgeben.

Das Flag **Als ausgewählt markieren** wird von Ihrem Theme verwendet, um zu bestimmen, welche Kollektionen in ausgewählten Bereichen angezeigt werden – beispielsweise ein Raster aus hervorgehobenen Kollektionen auf der Startseite. Prüfen Sie die Dokumentation Ihres Themes, um zu verstehen, wie ausgewählte Kollektionen genau angezeigt werden.

## Verwaltung der Sichtbarkeit von Kollektionen

- **Aktiv** bestimmt, ob die Sammlungsseite für die Öffentlichkeit zugänglich ist.

Eine inaktive Sammlung ist Kunden nicht sichtbar, bleibt aber im Admin-Panel gespeichert, damit Sie sie später erneut aktivieren können.
- **Sortierreihenfolge** bestimmt, in welcher Reihenfolge Sammlungen auf Listen-Seiten angezeigt werden.

Weisen Sie niedrigere Zahlen den Sammlungen zu, die zuerst angezeigt werden sollen.

## SEO für Sammlungen

Jede Sammlung hat eigene Felder für **Meta-Titel** und **Meta-Beschreibung**. Diese bestimmen, was in den Suchergebnissen der Suchmaschinen angezeigt wird, wenn jemand Ihre Sammlungsseite findet. Wenn Sie diese Felder leer lassen, greift Ihr Theme in der Regel auf den Sammlungsnamen und die Beschreibung zurück.

Gute SEO-Titel für Sammlungen sind beschreibend und spezifisch:
- "Sommerkleider 2026 — Blumendruck und leichte Stile" ist besser als "Sommerkollektion"
- "Herren-Laufschuhe — Leicht und atmungsaktiv" ist besser als "Laufschuhe"

## Tipps

- Halten Sie Sammlungsnamen kurz und klar — sie erscheinen als Seitentitel und Linktext in der Navigation Ihres Online-Shops
- Nutzen Sie saisonale oder kampagnenbasierte Sammlungen mit einem Start- und Endplan: Erstellen Sie die Sammlung, aktivieren Sie sie, wenn die Kampagne beginnt, und deaktivieren Sie sie (statt sie zu löschen), wenn sie endet, damit Sie sie später noch einmal verwenden können
- Das Feld **Sortierreihenfolge** ist es wert, bewusst festgelegt zu werden — der Standardwert ist 0 für alle Sammlungen, was bedeutet, dass sie alphabetisch sortiert werden. Weisen Sie spezifische Zahlen zu, um zu steuern, welche Sammlungen am auffälligsten angezeigt werden
- Eine Sammlung ohne Produkte zeigt Kunden eine leere Seite — entweder fügen Sie Produkte hinzu, bevor Sie die Sammlung aktivieren, oder lassen Sie die Sammlung inaktiv, bis sie bereit ist
- Prüfen Sie das Flag **Als Highlight markieren** nur für Sammlungen, die Sie wirklich hervorheben möchten; die meisten Themes reservieren die Highlight-Plätze für eine kleine Anzahl an Sammlungen und die Darstellung kann überladen wirken, wenn zu viele als hervorgehoben gekennzeichnet sind