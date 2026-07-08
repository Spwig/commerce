---
title: Blogverwaltung
---

Der Blog ermöglicht es Ihnen, Artikel, Leitfäden und Nachrichten zu veröffentlichen, um den Traffic zu steigern und Ihr Publikum zu begeistern. Der Blog von Spwig umfasst einen reichen Text-Editor, geplante Veröffentlichungen, Benachrichtigungen für Abonnenten, automatische Teilen auf sozialen Medien und SEO-Tools.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Erstellen eines Blogbeitrags

Navigieren Sie zu **Marketing > Blogbeiträge** und klicken Sie auf **Beitrag hinzufügen**.

### Beitraginhalt

Schreiben Sie Ihren Beitrag mit dem **CKEditor 5**-Text-Editor, der folgende Funktionen unterstützt:
- Textformatierung (Überschriften, fett, kursiv, Listen, Blockzitate)
- Bilder und Medien (über die Medienbibliothek hochgeladen)
- Einbettete Videos (YouTube, Vimeo)
- Tabellen und Codeblöcke
- Links zu Produkten, Kategorien und externen URLs

Für komplexere Layouts aktivieren Sie den **Seiten-Builder**-Schalter, um den drag-and-drop-Seiten-Builder anstelle des Text-Editors zu verwenden.

### Beitragseinstellungen

| Einstellung | Beschreibung |
|---------|-------------|
| **Titel** | Die Überschrift, die im Blog und in den Suchergebnissen angezeigt wird |
| **Slug** | URL-freundliche Identifikation (automatisch aus dem Titel generiert, bearbeitbar) |
| **Excerpt** | Kurze Zusammenfassung, die in den Blog-Karten und RSS-Feeds angezeigt wird |
| **Featured Image** | Hauptbild, das oben im Beitrag und in den Karten angezeigt wird |
| **Kategorie** | Hauptkategorie des Beitrags |
| **Tags** | Schlüsselwörter zur Filterung und zum Verknüpfung von Inhalten |
| **Autor** | Mitarbeiter, der als Autor zugeschrieben wird |
| **Status** | Entwurf, Geplant, Veröffentlicht oder Archiviert |
| **Featured** | Beitragskarte an die Spitze der Blog-Liste anheften |

### SEO-Einstellungen

Jeder Beitrag enthält SEO-Felder:
- **Meta-Titel** — benutzerdefinierter Titel für Suchmaschinenergebnisse (Standard ist der Beitragstitel)
- **Meta-Beschreibung** — Zusammenfassung, die in Suchmaschinenergebnissen angezeigt wird
- **Open Graph-Bild** — Bild, das verwendet wird, wenn der Beitrag auf sozialen Medien geteilt wird

## Beitragstatusse

| Status | Beschreibung |
|--------|-------------|
| **Entwurf** | Arbeit in Arbeit, nicht für die Öffentlichkeit sichtbar |
| **Geplant** | Wird automatisch an einem festgelegten Datum und Uhrzeit veröffentlicht |
| **Veröffentlicht** | Live und für Besucher sichtbar |
| **Archiviert** | Aus der Blog-Liste versteckt, aber weiterhin über direkten URL zugänglich |

### Beiträge planen

Um einen Beitrag für eine zukünftige Veröffentlichung zu planen:
1. Setzen Sie den Status auf **Geplant**
2. Wählen Sie das **Veröffentlichungsdatum und -zeit**
3. Speichern Sie den Beitrag

Eine Hintergrundaufgabe veröffentlicht den Beitrag automatisch zur geplanten Zeit und löst Benachrichtigungen für Abonnenten aus.

## Kategorien

Navigieren Sie zu **Marketing > Blogkategorien**, um Ihren Inhalt zu organisieren.

Kategorien unterstützen:
- **Hierarchie** — Erstellen Sie Eltern- und Kindkategorien (z. B. "Leitfäden" > "Einführung")
- **Benutzerdefinierte URLs** — Jede Kategorie hat ihre eigene Slug für saubere URLs
- **Beschreibungen** — Fügen Sie Kategorienbeschreibungen hinzu, die auf der Kategoriearchivseite angezeigt werden
- **Sortierung** — Steuern Sie die Anzeige-Reihenfolge der Kategorien in der Navigation

## Tags

Tags bieten eine zweite Möglichkeit, den Inhalt zu klassifizieren. Im Gegensatz zu Kategorien (die hierarchisch sind), sind Tags flache Bezeichnungen. Besucher können auf einen Tag klicken, um alle Beiträge mit diesem Tag anzuzeigen.

## Abonnenten

Navigieren Sie zu **Marketing > Blogabonnenten**, um Ihre Liste der Abonnenten zu verwalten.

### Wie Abonnements funktionieren

1. Besucher abonnieren über ein Formular auf dem Blog (E-Mail-Adresse erforderlich)
2. Eine **Doppelbestätigung**-Bestätigungsmail wird gesendet
3. Nach Bestätigung erhält der Abonnent Benachrichtigungen, wenn neue Beiträge veröffentlicht werden

### Benachrichtigungshäufigkeit

Abonnenten wählen, wie oft sie Benachrichtigungen erhalten:

| Häufigkeit | Beschreibung |
|-----------|-------------|
| **Sofortig** | E-Mail wird gesendet, sobald ein neuer Beitrag veröffentlicht wird |
| **Wöchentliche Zusammenfassung** | Eine wöchentliche Zusammenfassung aller neuen Beiträge |
| **Monatliche Zusammenfassung** | Eine monatliche Zusammenfassung aller neuen Beiträge |

Hintergrundaufgaben verwalten die Zusammenfassung und die Auslieferung automatisch.

### Abonnenten verwalten

- Anzahl der Abonnenten, Bestätigungsstatus und Registrierungsdatum ansehen
- Exportieren Sie Listen von Abonnenten für die Verwendung in externen E-Mail-Marketing-Tools
- Entfernen oder abonnieren Sie einzelne E-Mail-Adressen
- Jede Benachrichtigungsemail enthält einen **Einmal-Abmelde-Link**

## Automatisches Teilen auf sozialen Medien

Spwig kann neue Beiträge automatisch auf Ihre sozialen Medienkonten teilen, wenn sie veröffentlicht werden.

### Soziale Konten verbinden

Navigieren Sie zu **Marketing > Soziale Verknüpfungen**, um Ihre Konten zu verbinden:

| Plattform | Authentifizierung |
|----------|---------------|
| **Facebook** | OAuth — Verbinden Sie Ihre Facebook-Seite |
| **Instagram** | OAuth — Verbinden Sie Ihr Geschäftsprofil |
| **LinkedIn** | OAuth — Verbinden Sie Ihre Firmenseite |

### Wie das automatische Teilen funktioniert

1. Verbinden Sie eine oder mehrere soziale Konten
2. Beim Erstellen eines Beitrags aktivieren Sie **Automatisch teilen** für jede verbundene Konten
3. Passen Sie die Teilemeldung an (Standard ist der Beitragstitel und der Excerpt)
4. Wenn der Beitrag veröffentlicht wird (oder die geplante Zeit erreicht), wird er automatisch geteilt

Das automatische Teilen funktioniert auch mit geplanten Beiträgen — die soziale Freigabe wird zur gleichen Zeit gesendet, zu der der Beitrag online geht.

## RSS-Feed

Der Blog generiert automatisch einen RSS-Feed unter `/blog/feed/`. Dies ermöglicht Besuchern und Aggregatoren, sich für Ihren Inhalt zu abonnieren. Der Feed enthält:
- Beitragstitel und Excerpt
- Veröffentlichungsdatum
- Autoreninformationen
- Direkter Link zum vollständigen Beitrag

## Blogeinstellungen

Navigieren Sie zu **Marketing > Blogeinstellungen**, um globale Blogoptionen zu konfigurieren:

- **Beiträge pro Seite** — Anzahl der Beiträge, die pro Seite in der Liste angezeigt werden
- **Kommentare erlauben** — Kommentare für Beiträge aktivieren oder deaktivieren
- **Standardkategorie** — Standardkategorie für Beiträge ohne zugewiesene Kategorie
- **Sozialteilen-Buttons** — Zeigen Sie Teilen-Buttons auf den einzelnen Beitragseiten an

## Tipps

- Schreiben Sie Beiträge mit **SEO im Hinterkopf** — verwenden Sie beschreibende Titel, füllen Sie Meta-Beschreibungen aus und integrieren Sie relevante Schlüsselwörter natürlicherweise in den Inhalt.
- Verwenden Sie **geplante Veröffentlichungen**, um eine konsistente Veröffentlichungshäufigkeit ohne manuelle Arbeit zu gewährleisten.
- Aktivieren Sie **automatisches Teilen**, um den Reichweitenmaximierung — Beiträge, die auf sozialen Medien kurz nach der Veröffentlichung geteilt werden, erhalten die meisten Interaktionen.
- Fordern Sie Besucher an, **sich abzubonnieren**, indem Sie das Abonnementsformular auffällig auf Ihrem Blog platzieren und eine überzeugende Call-to-Action verwenden.
- Verwenden Sie **Kategorien** für breite Inhaltsgruppierungen und **Tags** für spezifische Themen — dies hilft Besuchern, verwandte Inhalte zu finden.
- Fügen Sie einem **Featured-Bild** zu jedem Beitrag hinzu — Beiträge mit Bildern erzielen bessere Ergebnisse in Suchmaschinenergebnissen und sozialen Medien-Teilen.
- Verwenden Sie die **wöchentliche oder monatliche Zusammenfassung**-Option für Abonnenten, die keine häufigen E-Mails möchten — dies verringert die Abmeldequote.

