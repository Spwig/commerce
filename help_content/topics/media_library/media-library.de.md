---
title: Medienbibliothek
---

Die Medienbibliothek ist das zentrale Zentrum zur Verwaltung aller Bilder, Videos, 3D-Modelle und Dateien, die in Ihrem Geschäft verwendet werden. Laden Sie Dateien hoch, indem Sie sie ziehen, organisieren Sie sie mit Ordnern und Tags und lassen Sie das System Bilder automatisch optimieren, damit sie schnell geladen werden.

![Medien Galerie](/static/core/admin/img/help/media-library/media-gallery.webp)

## Galerie Oberfläche

Navigieren Sie zu **Medienbibliothek** in der Seitenleiste, um die Galerie zu öffnen. Die Oberfläche hat drei Bereiche:

| Bereich | Ort | Zweck |
|--------|-----|------|
| **Hochladen Bereich** | Linksseitige Leiste, oben | Dateien per Drag & Drop hochladen (Bilder, Videos, 3D-Modelle bis zu 100 MB) |
| **Ordner & Tags** | Linksseitige Leiste, darunter | Ordner durchsuchen, nach Tags filtern, Zugriff auf den Papierkorb |
| **Medien Raster** | Hauptbereich | Durchsuchen, Filtern, Durchblättern und Verwalten aller Ihre Assets |

### Werkzeugleiste Steuerelemente

Die Werkzeugleiste über dem Medienraster bietet:

- **Suche** — Assets nach Titel, Alternativtext, Beschreibung oder Tag-Name finden
- **Typ-Filter** — Nur Bilder, Videos oder 3D-Modelle anzeigen
- **Größe-Filter** — Nach Dateigröße filtern (Klein, Mittel, Groß)
- **Massenaktionen** — Elemente auswählen, Details bearbeiten, ausgewählte löschen
- **Ansichtsmodi** — Raster (groß), kleiner Raster oder Listenansicht (wird über Sitzungen beibehalten)

## Dateien Hochladen

Ziehen Sie eine oder mehrere Dateien in den **Hochladen**-Bereich in der linken Seitenleiste, oder klicken Sie auf den Bereich, um einen Dateiauswahl-Dialog zu öffnen.

### Unterstützte Formate

| Typ | Formate |
|-----|--------|
| **Bilder** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Videos** | MP4, WebM, MOV, MKV, AVI |
| **3D-Modelle** | GLB, glTF |

### Hochladen Warteschlange

Wenn Sie mehrere Dateien hochladen, erscheint ein Warteschlangen-Manager, der zeigt:

- Den Namen jeder Datei und den Fortschrittsbalken für das Hochladen
- Konkurrierende Uploads (bis zu 2 gleichzeitig für Leistungsverbesserungen)
- Verarbeitungsstatus, während Dateien nach dem Hochladen optimiert werden
- Option, einzelne Uploads abzubrechen oder abgeschlossene Elemente zu löschen

Die Warteschlange ist ziehbar und kann minimiert werden, damit Sie weiterarbeiten können, während die Uploads abgeschlossen werden.

## Automatische Bildoptimierung

Jedes hochgeladene Bild wird automatisch optimiert:

- **WebP-Konvertierung** — eine WebP-Version wird neben der Originaldatei generiert (Qualität 85%) für schnelleres Laden
- **Vorschaugenerierung** — mehrere Größen werden basierend auf Ihren Bildvorlagen erstellt
- **EXIF-Orientierung** — Bilder werden automatisch auf die richtige Ausrichtung gedreht

### Systembildvorlagen

Die Plattform enthält 21 eingebaute Vorlagen, die gängige Anwendungsfälle abdecken:

| Vorlage | Abmessungen | Ausschneiden | Wofür verwendet |
|--------|-----------|----------|---------|
| **Vorschaubild** | 150 x 150 | Cover | Admin-Listen, schnelle Vorschau |
| **Klein** | 300 x 300 | Cover | Kleine Produktkarten |
| **Mittel** | 600 x 600 | Contain | Produktkarten, Blog-Vorschaubilder |
| **Groß** | 1200 x 1200 | Contain | Produkt-Detailseiten |
| **Galerie** | 800 x 800 | Contain | Bildgalerien |
| **Hero** | 1920 x 1080 | Cover | Hero-Bereiche, Seitenbannern |
| **Banner** | 1200 x 400 | Cover | Werbebannern |
| **Karte** | 400 x 300 | Cover | Merkblätter, Inhaltskarten |
| **Avatar** | 200 x 200 | Ausschneiden | Kunden- und Mitarbeiter-Avatare |
| **Produktliste** | 400 x 400 | Cover | Produktgitterkarten |
| **Produktdetail** | 1200 x 1200 | Cover | Vollständige Produktbilder |
| **Produktvorschau** | 100 x 100 | Cover | Variantenwähler, Mini-Warenkörbe |
| **Kategoriebanner** | 1920 x 480 | Cover | Kategorienkopfzeilen |
| **Kategorievorschau** | 300 x 200 | Cover | Kategorienkarten |
| **Logoheader** | 300 x 80 | Pad | Logo im Header |
| **Logofußzeile** | 200 x 60 | Pad | Logo im Fußzeile |
| **Logomail** | 400 x 100 | Pad | Logos in E-Mail-Vorlagen |
| **Logokreis** | 160 x 160 | Pad | Quadratische Logo-Platzierungen |
| **Markenlogo** | 200 x 100 | Pad | Marken-/Partnerlogos |
| **Ankündigungsbanner** | 800 x 300 | Cover | Ankündigungsbilder |
| **Ankündigungsgrund** | 1200 x 800 | Cover | Ankündigungsuntergründe |

Systemvorlagen können nicht umbenannt oder gelöscht werden. Sie können zusätzliche benutzerdefinierte Vorlagen unter **Medienbibliothek > Bildgrößenvorlagen** erstellen, wenn Sie Größen benötigen, die nicht von den Standardvorlagen abgedeckt werden.

### Ausschneide-Modi

| Modus | Verhalten |
|------|----------|
| **Cover** | Füllt den gesamten Bereich aus, schneidet bei Bedarf die Kanten ab — gut für Karten und Bannern |
| **Contain** | Fügt das gesamte Bild in den Bereich ein, fügt bei Bedarf transparenten Raum hinzu — gut für Produktbilder |
| **Ausschneiden** | Zentriert auf die genauen Abmessungen |
| **Pad** | Fügt das Bild ein und fügt Padding (transparent, weiß oder schwarz) hinzu — gut für Logos |

## Dateien organisieren

### Ordner

Erstellen Sie Ordner, um Ihre Medien in logische Gruppen zu organisieren. Ordner können beliebig tief verschachtelt werden. Klicken Sie auf einen Ordner in der linken Seitenleiste, um nur die Assets darin anzuzeigen. Der Link **Alle Dateien** zeigt alles an.

### Tags

Fügen Sie Tags zu Assets hinzu, um eine flexible Organisation über Ordner hinweg zu ermöglichen. Tags erscheinen in einer Wolke in der linken Seitenleiste. Klicken Sie auf einen Tag, um Assets nach diesem Tag zu filtern. Assets können mehrere Tags haben.

### Suche

Die Suchleiste findet Assets nach Titel, Alternativtext, Beschreibung oder Tag-Name. Kombinieren Sie die Suche mit Typ- und Größe-Filtern für präzise Ergebnisse.

## Asset Detail

Klicken Sie auf ein Asset, um seine Detailansicht mit einer großen Vorschau und vollständigen Metadaten zu öffnen.

![Asset Detail](/static/core/admin/img/help/media-library/media-detail.webp)

Die Detailansicht zeigt:

- **Vorschau** — große Bildvorschau mit den Originalabmessungen
- **Dateiinformationen** — Typ, Abmessungen, Dateigröße, Upload-Datum
- **Registerkarten** zum Bearbeiten:

| Registerkarte | Felder |
|--------------|--------|
| **Allgemein** | Titel, Alternativtext, Beschreibung (alle übersetzbar für mehrsprachige Geschäfte) |
| **Technisch** | MIME-Typ, Dateihash, Originaldateiname, WebP-Version-Status |
| **Organisation** | Ordnerzuordnung, Tags, öffentlich/privat-Schalter |
| **Erweitert** | Fokuspunkt-Koordinaten, externer ID, Metadaten JSON |

### Übersetzbare Felder

Titel, Alternativtext und Beschreibung unterstützen Übersetzungen. Klicken Sie auf das Übersetzen-Symbol neben jedem Feld, um Übersetzungen für Ihre aktivierten Sprachen hinzuzufügen. Dies stellt sicher, dass Bilder mit ordnungsgemäß lokalisierten Alternativtexten und Beschreibungen für SEO und Barrierefreiheit versehen sind.

### Nutzungsspur

Das System verfolgt, wo jedes Asset in der Plattform verwendet wird. Der Abschnitt **Mediennutzungen** am unteren Ende zeigt jedes Modell und Feld an, das dieses Asset referenziert, was Ihnen hilft, den Einfluss zu verstehen, bevor Sie Änderungen vornehmen oder es löschen.

## Video Unterstützung

Videos, die in die Medienbibliothek hochgeladen werden, werden automatisch analysiert:

- **Metadatenextraktion** — Dauer, Auflösung, Bildrate, Bitrate und Codecs werden erfasst
- **Posterbild** — ein Vorschaubild wird aus dem Video generiert
- **Streaming** — Videos unterstützen Range-Anfragen für das Suchen ohne das vollständige Datei herunterzuladen
- **Optionale Konvertierung** — Videos können in optimierte WebM/AV1-Formate konvertiert werden, um eine schnellere Lieferung zu ermöglichen

## Papierkorb

Das Löschen eines Assets verschiebt es in den **Papierkorb** anstatt es dauerhaft zu entfernen. Dies schützt vor versehentlichem Löschen.

| Aktion | Was es tut |
|--------|-----------|
| **Löschen** | Verschiebt das Asset in den Papierkorb (weiche Löschen) |
| **Wiederherstellen** | Gibt ein gelöschtes Asset an seinen ursprünglichen Ort zurück |
| **Dauerhaft löschen** | Entfernt das Asset und alle seine Vorschaubilder dauerhaft aus dem Speicher |
| **Papierkorb leeren** | Löscht alle Elemente im Papierkorb dauerhaft |

Klicken Sie auf **Papierkorb** in der linken Seitenleiste, um gelöschte Assets anzuzeigen und zu verwalten.

## Wo wird die Medienbibliothek verwendet

Die Medienbibliothek ist über die gesamte Plattform integriert:

| Funktion | Wie wird Medien verwendet |
|--------|----------------------|
| **Produktkatalog** | Produktbilder, Variantenbilder, Kategoriebannern |
| **Blog** | Merkblätter, inhaltliche Bilder über CKEditor |
| **Seitenbaukasten** | Bildelemente, Hintergründe für Hero-Bereiche, Galeriekomponenten |
| **Header/Footer-Baukasten** | Logobilder, Hintergrundbilder |
| **Site-Einstellungen** | Site-Logo und Favicon |
| **Ankündigungen** | Ankündigungsbilder und Hintergründe |
| **CKEditor** | Alle reichhaltigen Textbilduploads werden über die Medienbibliothek geroutet |
| **Loyalitätsprogramm** | Belohnungs- und Stufenbilder |

Wenn Sie ein Bild in einer dieser Funktionen auswählen, öffnet sich die Medienbibliothek als Modal für eine einfache Durchsuchung und Auswahl.

## Tipps

- **Verwenden Sie beschreibende Titel und Alternativtexte** — gute Metadaten verbessern SEO und Barrierefreiheit. Das System verwendet den Alternativtext in Bildetiketten über die gesamte Frontend-Shop-Website.
- **Organisieren Sie mit Ordnern frühzeitig** — erstellen Sie eine Ordnerstruktur (z. B. Produkte, Blog, Bannern, Logos) vor dem Hochladen vieler Dateien. Es ist viel einfacher, während Sie gehen zu organisieren, als später neu zu organisieren.
- **Verwenden Sie Tags für Querschnittskategorien** — Tags wie "saisonal", "Verkauf" oder "Lebensstil" helfen Ihnen, Assets zu finden, die mehrere Ordner überschreiten.
- **Überprüfen Sie die Nutzung vor dem Löschen** — der Abschnitt zur Nutzungsspur zeigt an, wo ein Asset referenziert wird. Das Löschen eines genutzten Assets kann zu beschädigten Bildern auf Ihrer Frontend-Shop-Website führen.
- **Lassen Sie WebP die Arbeit machen** — die automatische WebP-Konvertierung reduziert typischerweise die Dateigröße um 25-35% im Vergleich zu JPEG mit keiner sichtbaren Qualitätseinbuße. Sie müssen keine Bilder vor dem Hochladen manuell konvertieren.
- **Erstellen Sie benutzerdefinierte Vorlagen** — wenn Sie ein einzigartiges Layout benötigen, das eine bestimmte Bildgröße erfordert, erstellen Sie eine benutzerdefinierte Vorlage anstatt Bilder manuell zu skalieren.