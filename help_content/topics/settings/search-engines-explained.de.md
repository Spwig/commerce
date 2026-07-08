---
title: Suchmaschinen erläutert
---

Suchmaschinen in Spwig sind keine externen Dienste wie Elasticsearch oder Algolia - sie sind Konfigurationskontexte innerhalb Ihres Stores Suchsystem. Jede Maschine definiert, welche Inhaltstypen gesucht werden sollen, was ausgeschlossen werden soll und wie Ergebnisse priorisiert werden sollen. Dieser Leitfaden erläutert, was Suchmaschinen sind, wann Sie mehrere Maschinen erstellen sollten und wie Sie sie konfigurieren.

Die meisten Händler verwenden eine einzelne Standard-"Shop"-Maschine. Erstellen Sie mehrere Maschinen nur, wenn Sie für verschiedene Anwendungsfälle unterschiedliche Inhaltsmischungen oder Ausschlüsse benötigen.

![Suchmaschinenliste](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## Was sind Suchmaschinen?

Eine Suchmaschine in Spwig ist eine benannte Konfiguration, die festlegt:

- **Welche Inhaltstypen gesucht werden sollen** (Produkte, Kategorien, Marken, Blogbeiträge)
- **Was ausgeschlossen werden soll** (spezifische Kategorien oder Marken, die aus der Suche verborgen werden sollen)
- **Benutzerdefinierte Relevanzgewichte** (optional pro-Maschine Gewichtsübernahme)
- **Aktivstatus** (Suchmaschinen können vorübergehend deaktiviert werden)

Jede Maschine hat einen eindeutigen Slug, der in API-Aufrufen und Frontend-Code verwendet wird, um festzulegen, welche Maschine eine Suchanfrage verarbeiten soll.

## Wann mehrere Suchmaschinen erstellen?

Die meisten Geschäfte benötigen nur eine Maschine. Erstellen Sie zusätzliche Suchmaschinen für diese Szenarien:

| Anwendungsfall | Beispiel |
|----------------|----------|
| **Unterschiedliche Inhaltsmischungen** | Shop-Maschine sucht nur nach Produkten; Blog-Maschine sucht nur nach Blogbeiträgen |
| **Ausgewählte Ausschlüsse** | Haupt-Shop-Maschine verbirgt Kategorie "Clearance"; Clearance-Maschine zeigt nur Clearance-Artikel an |
| **Kategorie-spezifische Suche** | Elektronik-Maschine schließt Kleidungskategorien aus; Kleidung-Maschine schließt Elektronik aus |
| **Trennung zwischen B2B und B2C** | Großhandels-Maschine zeigt nur Großverkaufsprodukte an; Einzelhandels-Maschine zeigt Verbraucherprodukte an |

Wenn Sie sich nicht sicher sind, ob Sie mehrere Suchmaschinen benötigen, bleiben Sie bei einer. Das Hinzufügen von Maschinen erzeugt Komplexität ohne Vorteile, es sei denn, Sie haben einen spezifischen Anwendungsfall.

## Der 4-Schritt-Assistent

![Schritt 1 des Assistenten - Grundinformationen](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Navigieren Sie zu **Suche > Einrichtungsassistent**, um eine neue Maschine über einen geführten 4-Schritt-Prozess zu erstellen:

### Schritt 1: Grundinformationen

**Maschinenname** - Freundlicher Anzeigename (z. B. "Shop-Suche", "Blog-Suche"). Wird nur im Admin-Interface verwendet.

**Slug** - URL-sicherer Bezeichner (z. B. "shop-search", "blog-search"). Wird in API-Aufrufen und Frontend-Code verwendet. Wird automatisch aus dem Namen generiert, wenn leer gelassen.

**Aktiv** - Ob diese Maschine für Suchvorgänge verfügbar ist. Inaktive Maschinen liefern keine Ergebnisse.

### Schritt 2: Inhaltstypen

Wählen Sie aus, welche Arten von Inhalten diese Maschine durchsuchen soll:

- Produkte (beinhaltet alle Produkttypen: physisch, digital, Abonnements)
- Kategorien
- Marken
- Blogbeiträge

**Tipp**: Wählen Sie nur die Inhaltstypen aus, die für den Zweck dieser Maschine relevant sind. Eine auf Blogs fokussierte Maschine benötigt keine Produkte.

### Schritt 3: Gewichte (optional)

![Schritt 3 des Assistenten - Gewichte](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Optional können Sie die Relevanzgewichte für diese spezifische Maschine anpassen. Wenn Sie diesen Schritt überspringen, erbt die Maschine die globalen Gewichte aus SearchSettings.

Die meisten Maschinen sollten diesen Schritt überspringen und die globalen Standardwerte verwenden. Passen Sie die Gewichte nur an, wenn diese Maschine spezifische Rangierbedürfnisse hat (z. B. könnte eine Blog-Maschine das Gewicht_blog_posts auf 1,2 erhöhen).

### Schritt 4: Überprüfen und erstellen

Überprüfen Sie Ihre Konfiguration und klicken Sie auf **Maschine erstellen**, um sie zu speichern.

## Konfigurationsfelder der Maschine

Wenn Sie eine Maschine direkt bearbeiten (den Assistenten umgehen), sehen Sie diese Felder:

**Name und Slug** - Anzeigename und URL-Bezeichner

**Aktivstatus** - Schalter zum Aktivieren/Deaktivieren

**Inhaltstypen** - JSON-Array wie `['product', 'category']`

**Gewichtsübernahme** - JSON-Objekt wie `{'weight_name': 1.8}` (leer, wenn globale Gewichte verwendet werden)

**Ausgeschlossene Kategorien** - M2M-Beziehung zum Category-Modell. Produkte in diesen Kategorien werden in Suchergebnissen nicht angezeigt.

**Ausgeschlossene Marken** - M2M-Beziehung zum Brand-Modell. Produkte mit diesen Marken werden in Suchergebnissen nicht angezeigt.

## Ausschlüsse verwenden

Ausschlüsse verbergen bestimmte Inhalte in Suchergebnissen für diese Maschine:

**Beispiel: Clearance-Artikel ausblenden**

1. Erstellen Sie eine "Haupt-Shop"-Maschine
2. Im Feld "Ausgeschlossene Kategorien" wählen Sie Ihre "Clearance"-Kategorie aus
3. Im Feld "Ausgeschlossene Marken" wählen Sie jede Budget-Marke aus, die Sie verbergen möchten
4. Speichern Sie die Einstellungen

Jetzt werden Suchvorgänge über die "Haupt-Shop"-Maschine keine Clearance-Produkte zurückgeben, obwohl sie auf Ihrer Website sichtbar sind. Sie könnten eine separate "Clearance"-Maschine erstellen, die NUR Clearance-Artikel durchsucht.

## Verwendung von Maschinen im Frontend

Ihr Frontend-Code legt fest, welche Maschine über API-Aufrufe verwendet werden soll:

```javascript
// Verwenden Sie die "shop"-Maschine (meistens)
fetch('/api/search/?q=laptop&engine=shop')

// Verwenden Sie die "blog"-Maschine
fetch('/api/search/?q=ecommerce tips&engine=blog')

// Standardmaschine, wenn kein engine-Parameter angegeben ist
fetch('/api/search/?q=laptop')
```

Der Slug der Maschine wird als Abfrageparameter verwendet. Wenn keine Maschine angegeben ist, verwendet Spwig die erste aktiviertete Maschine alphabetisch.

## Synonyme und Umleitungen, die auf Maschinen spezifisch sind

Sowohl das Synonym- als auch das SearchRedirect-Modell haben eine optionale Fremdschlüsselbeziehung zu `engine`. Wenn festgelegt, gilt dieses Synonym oder diese Umleitung NUR für Suchvorgänge über diese spezifische Maschine.

**Beispiel**: Eine Blog-Maschine könnte Synonyme wie "tutorial" → "guide" haben, die nicht für Produkt-Suchen gelten.

Die meisten Synonyme und Umleitungen sollten NICHT auf Maschinen spezifisch sein - lassen Sie das Feld engine leer, um sie global anzuwenden.

## Tipps

- **Beginnen Sie mit einer Maschine** - Erstellen Sie die Standard-"Shop"-Maschine und verwenden Sie sie für alles, bis Sie einen klaren Bedarf für mehrere Maschinen haben
- **Verwenden Sie beschreibende Slugs** - Wählen Sie Slugs wie "shop", "blog", "wholesale", die den Zweck der Maschine klar zeigen
- **Testen Sie Maschinen vor der Aktivierung** - Erstellen Sie Maschinen in inaktiver Zustand, testen Sie sie über die API, dann aktivieren Sie sie
- **Erstellen Sie keine Maschinen, es sei denn, es ist notwendig** - Mehr Maschinen = mehr Konfigurationskomplexität, ohne Vorteile, wenn sie alle dasselbe tun
- **Überprüfen Sie Analysen pro Maschine** - Das Suchanalytik-Dashboard kann nach Maschine filtern, um zu sehen, welche Maschinen am häufigsten verwendet werden

