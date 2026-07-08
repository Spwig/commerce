---
title: Anfertigung von benutzerdefinierten Produkten
---

Wenn ein Kunde ein Produkt gestaltet und eine Bestellung aufgibt, wird seine Gestaltung gesperrt und gemeinsam mit der Bestellung gespeichert. Dieser Leitfaden erklärt, wie benutzerdefinierte Gestaltungen durch den Bestellzyklus fließen und wie Sie die druckbereiten Dateien abrufen können, die Sie zur Abwicklung benötigen.

## Gestaltungszyklus

Eine Kunden-Gestaltung geht durch mehrere Phasen vom Erstellen bis zur Abwicklung:

### 1. Gestaltungserstellung

Der Kunde verwendet den visuellen Editor auf der Frontseite, um seine Gestaltung zu erstellen. Während sie arbeitet, wird ihr Fortschritt automatisch im Browser gespeichert. Registrierte Kunden können Gestaltungen auch in ihrem Konto speichern, um sie später zu bearbeiten.

### 2. Gestaltungsentwurf

Wenn der Kunde auf **In den Warenkorb** klickt, wird der aktuelle Gestaltungsstatus als **Gestaltungsentwurf** gespeichert. Der Entwurf enthält:

- Den vollständigen Canvas-Status für jede Oberfläche (Position der Elemente, Textinhalte, hochgeladene Bilder, Clipart, Styling)
- Eine Preisübersicht, die alle anwendbaren Gestaltungsgebühren anzeigt
- Vorschaubilder jeder Oberfläche

Der Entwurf wird über einen eindeutigen Token mit dem Warenkorb-Element verknüpft. Dies stellt sicher, dass die exakte Gestaltung, die der Kunde erstellt hat, auch dann erhalten bleibt, wenn er weiter einkauft, bevor er zur Kasse geht.

**Entwurfsgültigkeit:** Gestaltungsentwürfe verfallen automatisch nach 7 Tagen, wenn der Kunde die Bestellung nicht abschließt. Dies verhindert die Ansammlung von abgebrochenen Gestaltungen.

### 3. Gestaltungsabbild

Wenn der Kunde den Checkout abschließt und die Bestellung aufgibt, wird der Gestaltungsentwurf in ein **unveränderliches Gestaltungsabbild** umgewandelt. Dies ist der permanente Aufzeichnung der Gestaltung:

- Das Abbild kann vom Kunden nach dem Kauf nicht mehr geändert werden
- Es enthält die exakt gleichen Gestaltungsdaten wie der Entwurf
- Es ist dauerhaft mit dem spezifischen Bestellartikel verknüpft

Diese Unveränderlichkeit ist wichtig – sie stellt sicher, dass das, was der Kunde bestellt hat, exakt das ist, was Sie produzieren und versenden, mit keiner Möglichkeit zu Änderungen nach der Zahlung.

### 4. Erstellung der Abwicklungsdateien

Nachdem die Bestellung aufgegeben wurde, generiert das System automatisch **hochauflösende Abwicklungsdateien** für jede Oberfläche der Gestaltung. Dies sind Kombinationsbilder, die alle Gestaltungsbestandteile (Text, Bilder, Clipart) in eine einzelne druckbereite Datei kombinieren, die für jede Oberfläche konfiguriert wurde.

Die Erstellung erfolgt asynchron im Hintergrund. Bei den meisten Gestaltungen wird die Erstellung innerhalb weniger Sekunden abgeschlossen. Der Status **Gerendert** des Abbilds zeigt an, ob die Abwicklungsdateien bereit sind.

## Zugriff auf Gestaltungsdaten in Bestellungen

### Bestell-Detailsseite

Wenn Sie eine Bestellung ansehen, die benutzerdefinierte Produkte enthält, im Admin-Panel:

1. Navigieren Sie zu **Bestellungen > Alle Bestellungen**
2. Öffnen Sie die Bestellung mit dem benutzerdefinierten Produkt
3. Der Bestellartikel für das benutzerdefinierte Produkt zeigt die Gestaltungsinformationen, einschließlich Vorschauen der Oberflächen und einen Link zum Gestaltungsabbild

### Liste der Gestaltungsabbilder

Sie können auch alle Gestaltungsabbilder direkt durchsuchen:

1. Navigieren Sie zu **Benutzerdefinierte Produkte > Gestaltungsabbilder**
2. Die Liste zeigt alle Abbilder, die mit Bestellartikeln verknüpft sind
3. Klicken Sie auf ein Abbild, um die vollständigen Gestaltungsdaten, gerenderte Bilder und Abwicklungsdateien anzuzeigen

Jedes Abbild zeigt:

| Feld | Beschreibung |
|-------|-------------|
| **Bestellartikel** | Link zum zugehörigen Bestellartikel |
| **Gestaltungsdaten** | Der vollständige Canvas-Status (JSON) |
| **Gerenderte Bilder** | Vorschauvorschaubilder pro Oberfläche |
| **Abwicklungsdateien** | Hochauflösende Kombinationsdateien für den Druck |
| **Gerendert** | Ob die Erstellung abgeschlossen ist |
| **Erstellt um** | Zeitstempel, zu dem die Dateien generiert wurden |

## Herunterladen der Abwicklungsdateien

Die Abwicklungsdateien sind die Dateien, die Sie an Ihren Druckdienstleister senden oder in Ihrem Produktionsprozess verwenden.

**Für eine benutzerdefinierte T-Shirt-Bestellung:**
- Laden Sie die Datei der **Vorderseite** herunter (z. B. 300 DPI Kombinations-PNG)
- Laden Sie die Datei der **Rückseite** herunter
- Laden Sie die Datei der **Ärmel** herunter (wenn gestaltet)
- Senden Sie alle Dateien an Ihren Druckdienstleister oder DTG (direct-to-garment)-Drucker


**Für eine benutzerdefinierte Posterbestellung:**
- Laden Sie die einzelne **Vorderseite**-Datei in Druckauflösung herunter
- Die Datei enthält einen Bleed-Bereich, wenn dieser für die Oberfläche konfiguriert wurde
- Senden Sie diese an Ihren Poster-/Karten-Drucker

Jede Datei ist ein einzelnes Kompositbild, das alle Designelemente zusammengefasst und in der von Ihnen für diese Oberfläche konfigurierten DPI gerendert enthält.

## Gespeicherte Designs

Angemeldete Kunden können ihre Designs in ihrem Konto speichern, um sie später zu bearbeiten. Als Händler können Sie diese gespeicherten Designs in einer schreibgeschützten Liste einsehen:

1. Navigieren Sie zu **Benutzerdefinierten Produkten > Gespeicherte Designs**
2. Die Liste zeigt alle vom Kunden gespeicherten Designs mit dem Namen des Kunden, dem Produkt, dem Designnamen und dem Datum an

Gespeicherte Designs sind:
- **Kundenbesitz** — Sie gehören zum Kundenkonto
- **Schreibgeschützt für Händler** — Sie können sie einsehen, aber nicht bearbeiten
- **Trennt sich von Bestellungen** — Ein gespeichertes Design wird erst zu einer Bestellung, wenn der Kunde es in den Warenkorb legt und den Kauf abschließt
- **Wiederverwendbar** — Kunden können ein gespeichertes Design laden, es bearbeiten und mehrmals bestellen

## Erfüllungsworkflow

### Standardworkflow

1. **Bestellung empfangen** — Die Bestellung erscheint in Ihrer Bestellliste mit den benutzerdefinierten Artikeln
2. **Rendern überprüfen** — Prüfen Sie, ob der Design-Preview **Gerendert: Ja** anzeigt. Wenn das Rendern noch nicht abgeschlossen ist, warten Sie einige Minuten und aktualisieren Sie die Seite
3. **Dateien herunterladen** — Laden Sie die Erfüllungsdatei für jede gestaltete Oberfläche herunter
4. **Qualität prüfen** — Öffnen Sie die Dateien und überprüfen Sie, ob das Design Ihre Druckqualitätsstandards erfüllt (prüfen Sie DPI, Positionierung der Elemente und Lesbarkeit des Textes)
5. **An Produktion weiterleiten** — Weiterleiten Sie die Dateien an Ihren Druckdienstleister oder Ihre Produktionsabteilung
6. **Versenden und abschließen** — Nach der Produktion versenden Sie das Produkt und markieren Sie die Bestellung als erfüllt

### Beispiel für T-Shirt-Erfüllung

1. Bestellung erhalten: „Benutzerdefiniertes Team-T-Shirt“ mit Designs auf Vorder- und Rückseite
2. Bestellung öffnen → Design-Preview ansehen
3. Laden Sie `front.png` (300 DPI, 300x400mm) und `back.png` (300 DPI, 300x400mm) herunter
4. Senden Sie beide Dateien an Ihren DTG-Drucker mit der Kleidungsfarbe und Größe aus der Variante der Bestellung
5. Nach dem Drucken und der Qualitätssicherung versenden Sie das Produkt an den Kunden

### Beispiel für Poster-Erfüllung

1. Bestellung erhalten: „Benutzerdefiniertes A4-Poster“ mit einer einzigen gestalteten Oberfläche
2. Bestellung öffnen → Design-Preview ansehen
3. Laden Sie `front.png` (300 DPI, 210x297mm mit 3mm Bleed) herunter
4. Senden Sie diese an Ihren Poster-Druckdienstleister
5. Nach dem Drucken und Schneiden versenden Sie das Produkt an den Kunden

## Problembehandlung

**Problem:** Der Design-Preview zeigt „Gerendert: Nein“ an und das Rendern ist noch nicht abgeschlossen

- **Ursache:** Die Hintergrund-Rendertask ist möglicherweise fehlgeschlagen oder wird noch verarbeitet
- **Lösung:** Warten Sie einige Minuten. Wenn das Rendern nicht abgeschlossen wird, prüfen Sie die Protokolle der Hintergrundtasks. Sie können auch den Designdaten direkt im Preview ansehen, um sicherzustellen, dass das Design des Kunden erhalten bleibt

**Problem:** Die Erfüllungsdatei wirkt schlechter als erwartet

- **Ursache:** Der Kunde hat möglicherweise niedrigauflösende Bilder hochgeladen
- **Lösung:** Prüfen Sie die DPI-Einstellungen der Oberfläche. Wenn Warnungen für die Mindest-DPI konfiguriert wurden, hätte der Kunde während des Designprozesses gewarnt werden. Für zukünftige Produkte können Sie die Mindest-DPI-Anforderung erhöhen

**Problem:** Der Kunde bittet um eine Änderung seines Designs nach der Bestellung

- **Lösung:** Design-Previews sind per Design unveränderlich. Wenn der Kunde Änderungen benötigt, sollte er eine neue Bestellung mit dem aktualisierten Design aufgeben. Wenn Sie eine Ausnahme zulassen, kann der Kunde sein gespeichertes Design (wenn er eines gespeichert hat) als Ausgangspunkt für eine neue Bestellung verwenden

## Tipps

- Überprüfen Sie immer, ob das Rendern abgeschlossen ist, bevor Sie mit der Produktion beginnen.

Prüfen Sie das Feld **Gerendert** im Design-Preview.
- Halten Sie die DPI-Einstellungen entsprechend Ihrem Druckverfahren.

Eine höhere DPI erzeugt eine bessere Qualität, aber größere Dateigrößen. 300 DPI ist die Standardauflösung für die meisten professionellen Druckprodukte.
- Ermutigen Sie Kunden, ihre Designs vor der Bestellung zu speichern.

Behalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe bei.

# Wenn es zu einem Produktionsproblem kommt und die Bestellung neu erstellt werden muss, macht das gespeicherte Design das Neubestellen einfacher.
- Bauen Sie einen Puffer in Ihren Produktionszeitplan für anpassbare Produkte ein.

Im Gegensatz zu Standardprodukten erfordert jedes Einzelteil individuelle Dateibehandlung.
- Wenn Sie hohe Mengen an anpassbaren Bestellungen verarbeiten, sollten Sie den Schritt zur Dateiherunterladung automatisieren, indem Sie sich mit der API Ihres Druckanbieters integrieren.