---
title: 3D-Produkt-Konfigurator
---

Der 3D-Konfigurator ermöglicht es Ihren Kunden, konfigurierbare Produkte in einem interaktiven 3D-Viewer direkt auf der Produktseite anzuzeigen. Wenn Kunden Optionen auswählen – wie Farben, Materialien oder Komponentenvariationen – aktualisiert sich das 3D-Modell in Echtzeit, um ihre Auswahl widerzuspiegeln. Auf unterstützten mobilen Geräten können Kunden das Produkt auch in der erweiterten Realität (AR) ansehen, wodurch es virtuell in ihrem eigenen Raum platziert wird, bevor sie es kaufen.

Der 3D-Konfigurator funktioniert mit konfigurierbaren Produkten. Jedes konfigurierbare Produkt kann eine 3D-Szenenkonfiguration haben, die eine GLB-Modelldatei mit den Konfigurationsoptionen des Produkts verknüpft.

## Vor dem Beginn

Um eine 3D-Szene einzurichten, benötigen Sie:

- Ein **konfigurierbares Produkt**, das bereits in Ihrem Katalog erstellt wurde
- Eine **Basis-3D-Modell**, die als GLB-Datei in Ihre Medienbibliothek hochgeladen wurde – dies ist das zusammengebauten Modell, das standardmäßig angezeigt wird
- Optional, zusätzliche GLB-Dateien für Geometrie-Wechsel (z. B. verschiedene Kragenformen) und Texturbilder für Materialvariationen

Wenn Sie das konfigurierbare Produkt und seine Konfigurationsoptionen noch nicht erstellt haben, tun Sie dies zunächst, bevor Sie die 3D-Szene einrichten.

## Erstellen einer Szenenkonfiguration

1. Navigieren Sie zu **Katalog > 3D-Szenenkonfigurationen**
2. Klicken Sie auf **+ 3D-Szenenkonfiguration hinzufügen**
3. Wählen Sie das **Produkt** aus, zu dem diese Szene gehört – nur konfigurierbare Produkte sind verfügbar
4. Wählen Sie die **Basis-3D-Modell** aus Ihrer Medienbibliothek aus – dies ist die GLB-Datei, die standardmäßig geladen wird
5. Konfigurieren Sie die Viewer-Einstellungen (siehe unten)
6. Speichern Sie den Eintrag

Nach dem Speichern wird das Feld **Node Tree** automatisch gefüllt. Dies ist der geparste Szenengraph, der aus Ihrer GLB-Datei extrahiert wird – es listet jeden benannten Knoten im Modell auf, den Sie bei der Hinzufügung von Knotenzuordnungen verwenden werden.

## Viewer-Einstellungen

Diese Einstellungen steuern, wie der 3D-Viewer auf Ihrer Produktseite angezeigt wird.

### Kamera und Beleuchtung

| Feld | Beschreibung | Standard |
|-------|-------------|---------|
| **Kamera-Orbit** | Anfangsposition der Kamera im Format `Winkel Höhe Entfernung` (z. B. `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Kamera-Ziel** | Der Punkt, auf den die Kamera blickt, in Metern vom Modellzentrum (z. B. `0m 0m 0m`) | `0m 0m 0m` |
| **Umgebungsimage** | Ein HDR-Bild aus Ihrer Medienbibliothek, das für die Bildbasierte Beleuchtung verwendet wird – gibt realistischere Reflexionen und Schatten | Keines |
| **Belichtung** | Gesamte Helligkeit der Szene – niedrigere Werte sind dunkler, höhere Werte sind heller | `1.0` |

### Schatten

| Feld | Beschreibung | Standard |
|-------|-------------|---------|
| **Schattenintensität** | Wie stark der Schatten unter dem Modell erscheint – `0` bedeutet keinen Schatten, `1` bedeutet volle Intensität | `0.5` |
| **Schattenweichheit** | Wie verschwommen die Schattenränder sind – `0` ist scharf, `1` ist sehr weich | `0.5` |

### Farbgebung

| Feld | Beschreibung |
|-------|-------------|
| **Tonmapping** | Der Farbgebungsalgorithmus, der auf die Szene angewendet wird. **Commerce** erzeugt lebendige, produktfreundliche Farben. **Neutral** ist farbgenau. **ACES** gibt einen filmischen Kinoblick. |
| **Bloom-Stärke** | Fügt einem emissiven (selbstbeleuchteten) Teil des Modells ein Leuchteffekt hinzu. `0` deaktiviert Bloom. Werte zwischen `1` und `5` erzeugen subtile bis dramatische Leuchteffekte. |

### Verhalten und Hintergrund

| Feld | Beschreibung | Standard |
|-------|-------------|---------|
| **Automatische Drehung** | Ob das Modell beim Laden langsam rotiert, um die Aufmerksamkeit des Kunden zu erregen | An |
| **AR aktiviert** | Ob Kunden auf unterstützten Geräten eine **In AR ansehen**-Schaltfläche sehen | An |
| **Hintergrund** | Die Hintergrundfarbe oder CSS-Gradient des Viewers – geben Sie eine Hex-Farbe (z. B. `#f5f5f5`) oder einen CSS-Gradient-Wert ein | `#ffffff` |

### Vorschaubild

Das Feld **Vorschaubild** enthält ein Vorschaubild des 3D-Viewers, das vor dem Laden des Viewers angezeigt wird. Sie können ein Screenshot aus der Live-Produktseite erstellen und es in Ihre Medienbibliothek hochladen, und dann hier einen Link erstellen, um eine glättere Ladeerfahrung zu ermöglichen.

## Aktivieren und Deaktivieren des 3D-Viewers

Der **Aktiviert**-Schalter steuert, ob der 3D-Viewer auf der Produktseite angezeigt wird.

Wenn diese Funktion deaktiviert ist, wechselt das Produkt automatisch zum Standard-2D-Bild-Konfigurator.

Damit können Sie eine Szenenkonfiguration vorbereiten, bevor sie Kunden sichtbar gemacht wird.

## Verknüpfen von Konfigurationsoptionen mit 3D-Aktionen

Sobald die Grundszene konfiguriert ist, können Sie jede Konfigurationsoption mit einer visuellen Änderung im 3D-Modell verknüpfen. Diese Verknüpfungen werden **Node Mappings** genannt und werden im Abschnitt **Node Mappings** am unteren Ende des Szenenkonfigurationsformulars hinzugefügt.

### Felder für Node-Mapping

| Feld | Beschreibung |
|-------|-------------|
| **Slot-Option** | Die Konfigurationsoption, die diese Änderung auslöst (z. B. "Rote Leder") |
| **Aktionstyp** | Welche visuelle Änderung stattfindet (siehe Aktionstypen unten) |
| **Zielknoten** | Der Name des Knotens im Szenengraphen, der sich ändert – wählen Sie aus den Namen, die in Ihrem **Node Tree** aufgelistet sind |
| **Aktionendaten** | Aktionsspezifische Daten wie eine Farbhex-Code, Textur-URL oder GLB-Datei-URL |
| **Sortierreihenfolge** | Steuert die Reihenfolge, in der mehrere Zuordnungen für dieselbe Option angewendet werden |

### Aktionstypen

| Aktion | Was sie tut |
|--------|-------------|
| **Materialfarbe** | Ändert die Farbe eines Materials am Zielknoten – geben Sie eine Hex-Farbe in **Aktionendaten** an |
| **Materialtextur** | Ersetzt die Textur, die einem Material angewendet wird – verknüpfen Sie eine Texturbildressource in **Aktionendaten** |
| **Geometrieaustausch** | Ersetzt einen Teil des Modells durch eine andere GLB-Datei – nützlich für strukturelle Änderungen wie eine andere Griffform |
| **Sichtbarkeit** | Zeigt oder versteckt einen Knoten in der Szene – setzen Sie `visible: true` oder `visible: false` in **Aktionendaten** |

Für eine einzelne Slot-Option können mehrere Zuordnungen hinzugefügt werden. Zum Beispiel könnte das Auswählen von "Blauer Denim" die Materialfarbe *und* einen Lederkantenknoten gleichzeitig ausblenden.

## Geometrie-Assets

Wenn Ihre Konfiguration **Geometrieaustausch**-Aktionen enthält, müssen Sie die Ersatz-GLB-Dateien als Geometrie-Assets registrieren. Diese werden im Abschnitt **Geometrie-Assets** des Szenenkonfigurationsformulars hinzugefügt.

| Feld | Beschreibung |
|-------|-------------|
| **Bezeichnung** | Beschreibender Name für dieses Geometrie-Asset, z. B. "V-Ausschnitt-Kragen" |
| **GLB-Datei** | Die Ersatz-GLB-Datei aus Ihrer Medienbibliothek |
| **Zielknoten** | Welcher Knoten im Grundmodell dieses Geometrie-Asset ersetzt |

Nachdem Sie ein Geometrie-Asset gespeichert haben, werden die Knotennamen aus der GLB-Datei analysiert und in **Node Data** gespeichert, wodurch sie als Zielknoten in Ihren Zuordnungen zur Verfügung stehen.

## Textur-Assets

Texturbilder, die in **Materialtextur**-Zuordnungen verwendet werden, können als Textur-Assets registriert werden, um sie leichter zu referenzieren. Diese werden im Abschnitt **Textur-Assets** hinzugefügt.

| Feld | Beschreibung |
|-------|-------------|
| **Bezeichnung** | Beschreibender Name, z. B. "Rotes Leder" |
| **Textur-Bild** | Das Textur-Bild aus Ihrer Medienbibliothek |
| **Textur-Typ** | Der PBR-Kanal, auf den diese Textur angewendet wird – Grundfarbe, Normalmap, Rauheitsmap, Metallmap, Umgebungsbeleuchtung oder Emissionmap |

## Beispiel: konfigurierbare Jacke mit Farboptionen

**Szenario:** Eine Jacke, die in Schwarz, Marineblau oder Burgunder bestellt werden kann, wobei jede Farbe auf das Jacken-Mesh angewendet wird.

**Einrichtung:**

1. Erstellen Sie eine Szenenkonfiguration für das Jackenprodukt mit der zusammengebauten Jacken-GLB-Datei als Grundmodell
2. Stellen Sie **Tone Mapping** auf Commerce und **Auto Rotate** auf aktiv ein
3. Fügen Sie im Abschnitt Node Mappings drei Einträge hinzu – einen pro Farboption:

| Slot-Option | Aktionstyp | Zielknoten | Aktionendaten |
|-------------|-------------|-------------|-------------|
| Schwarz | Materialfarbe | JacketBody | `{"color": "#1a1a1a"}` |
| Marineblau | Materialfarbe | JacketBody | `{"color": "#1b2a4a"}` |
| Burgunder | Materialfarbe | JacketBody | `{"color": "#6b2737"}` |

Wenn ein Kunde auf der Produktseite Marineblau auswählt, aktualisiert der Viewer das Material von JacketBody sofort auf die Marineblau-Farbe.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Benennen Sie Ihre GLB-Knoten klar, wenn Sie Ihr 3D-Modell erstellen — Knotennamen wie "JacketBody" oder "CollarMesh" sind viel einfacher zu bearbeiten als automatisch generierte Namen wie "Mesh_023"
- Verwenden Sie die **Commerce**-Tonalitätskarte für die meisten Produkte — sie ist für eine lebendige und ansprechende Produktpräsentation optimiert
- Deaktivieren Sie **Auto Rotate** für Produkte, bei denen der Standardkamerawinkel bereits die wichtigsten Merkmale zeigt, um den Kunden beim Laden nicht zu verwirren
- Testen Sie die AR-Schaltfläche auf einem echten mobilen Gerät, bevor Sie sie bewerben — die AR-Verfügbarkeit hängt vom Gerät und Browser des Kunden ab (iOS Safari und Android Chrome mit WebXR-Unterstützung sind am zuverlässigsten)
- Laden Sie ein **Thumbnail**-Bild für jede Szeneinstellung hoch — dies verhindert, dass ein leerer weißer Kasten während des Ladens des 3D-Ansichtsprogramms erscheint
- Wenn der 3D-Ansichtsprogramm noch nicht bereit ist, deaktivieren Sie es mit dem **Enabled**-Schalter, damit die Kunden stattdessen das Standardbildkonfiguratoren sehen