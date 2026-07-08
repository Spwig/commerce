---
title: Verwaltung von Kartenlesern
---

Die Verwaltung von Kartenlesern verfolgt physische Zahlungshardware-Geräte, weist sie Terminalen für Kassensysteme zu und überwacht ihren Betriebsstatus. Jeder Kartenleser stellt eine tatsächliche Hardware (Stripe S700, WisePOS E oder P400) dar, die bei Ihrem Zahlungsdienstleister registriert ist. Leser haben eine Eins-zu-Eins-Beziehung zu Terminalen – jedes Register hat seinen eigenen dedizierten Kartenleser. Überwachen Sie den Status des Lesers (online, offline, beschäftigt) in Echtzeit, personalisieren Sie Startbildschirme mit Ihrer Markenidentität und beheben Sie Verbindungsprobleme, bevor sie den Zahlungsvorgang des Kunden beeinträchtigen.

Verwenden Sie die Kartenleser-Verwaltung, um sicherzustellen, dass die Zahlungshardware an allen Standorten richtig konfiguriert, zugewiesen und betriebsbereit ist.

![Liste der Kartenleser](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Verständnis von Kartenlesern

Kartenleser sind physische Hardware-Geräte, die Kredit- und Debitkartenzahlungen verarbeiten:

**Hardware-Komponenten**:
- EMV-Chipkarten-Slot
- NFC-Antenne (kontaktlos/Bezahlung per Tippen)
- Magnetstreifenleser (Legacy, selten verwendet)
- Bildschirm (zeigt Betrag, fordert PIN und Unterschrift an)
- Netzwerkverbindung (Wi-Fi oder Ethernet, je nach Modell)

**Software-Integration**:
- Leser verbinden sich mit der Stripe Terminal API (Cloud-basiert, keine direkte Verbindung zum Kassengerät)
- Kassenterminal sendet Zahlungsauftrag über die API
- Stripe leitet den Auftrag an den registrierten Leser weiter
- Leser verarbeitet die Karte und sendet das Ergebnis an das Kassengerät zurück
- Keine USB-/Bluetooth-Verbindung zwischen Kassengerät und Leser erforderlich

**Ein Leser pro Terminal**:
- Jedes Kassengerät sollte genau einen zugewiesenen Kartenleser haben
- Die Eins-zu-Eins-Beziehung gewährleistet klare Verantwortung und vereinfacht die Fehlerbehebung
- Mehrere Terminals können keinen gemeinsamen Leser verwenden (verursacht Konflikte)

## Typen von Kartenlesern

Spwig POS unterstützt Stripe Terminal-Kartenleser:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Alle-in-One Android-Terminal mit 5-Zoll-Farbbildschirm
- Optionales integrierter Drucker (Wärmebildkasse)
- Bestens geeignet für: Vollwertige Einzelhandelskasse, Restaurants (Tip-Anfragen auf Farbbildschirm)
- Verbindung: Nur Wi-Fi
- Startbildschirm: Vollfarbig 480×800 Porträt

**Stripe Reader S700** (`stripe_s700`):
- Schreibtischleser mit Monochrom-LCD
- Kompakte Bauweise, wasserfest
- Bestens geeignet für: Standard-Einzelhandel, kompakte Kassen
- Verbindung: Wi-Fi oder Ethernet
- Startbildschirm: Monochrom 480×800 Porträt

**Verifone P400** (`verifone_p400`):
- Legacy-Schreibtischleser (älteres Modell)
- Noch unterstützt, aber nicht für neue Implementierungen empfohlen
- Bestens geeignet für: Bestehende Implementierungen (ersetzen Sie keine funktionierende Hardware)
- Verbindung: Wi-Fi oder Ethernet
- Startbildschirm: Monochrom 480×800 Porträt

**Zukünftige Kompatibilität**:
- Weitere Lesermodelle können hinzugefügt werden, wenn Stripe Terminal die Hardwareangebote erweitert
- Das Dropdown-Menü für Lesertypen wird automatisch aus den Anbieterfunktionen befüllt

## Workflow zur Registrierung von Lesern

**Schritt 1: Kauf und Empfang der Hardware**
- Bestellen Sie den Leser bei Stripe (stripe.com/terminal) oder einem autorisierten Vertriebspartner
- Verpackung öffnen und Leser einschalten
- Verbinden Sie sich mit dem Wi-Fi-Netzwerk (folgen Sie dem auf dem Leser angezeigten Einrichtungsprozess)

**Schritt 2: Registrierung im Stripe Dashboard**
- Navigieren Sie zu **Stripe Dashboard > Terminal > Leser**
- Klicken Sie auf **Neuen Leser registrieren**
- Folgen Sie dem auf dem Bildschirm angezeigten Paarungsprozess (der Leser zeigt den Registrierungscode an)
- Weisen Sie den Leser einem Stripe-Standort zu (muss mit dem Standort in der Zahlungsdienstanbieter-Konfiguration übereinstimmen)
- Notieren Sie sich die **Leser-ID** (sieht aus wie `tmr_ABC123...`)

**Schritt 3: Synchronisierung mit Spwig (automatisch)**
- Spwig erkennt automatisch Leser, die Ihrem Stripe-Standort registriert sind
- Ein Hintergrundauftrag synchronisiert alle 30 Minuten
- Neue Leser erscheinen in der Liste **POS > Kartenleser** innerhalb von 30 Minuten

**Schritt 4: Zuordnung zu einem Terminal (manuell)**
- Navigieren Sie zu **POS > Kartenleser**
- Finden Sie den neu entdeckten Leser in der Liste
- Klicken Sie, um zu bearbeiten
- Wählen Sie **Terminal**, um dem Leser ein Terminal zuzuordnen
- Speichern

**Schritt 5: Testzahlung**
- Am Kassenterminal eine Testtransaktion verarbeiten
- Wählen Sie die Kartenzahlungsmethode
- Das POS-System sollte den zugewiesenen Leser erkennen
- Verwenden Sie die Stripe-Testkarte (4242 4242 4242 4242), um den Test abzuschließen
- Überprüfen Sie, ob die Zahlung erfolgreich abgeschlossen wurde

Wenn der Leser während des Tests nicht angezeigt wird, überprüfen Sie die Zuordnung zum Terminal und den Status des Lesers.

## Überwachung des Leserstatus

Leser melden ihren Status über die Stripe Terminal API, die Spwig alle 5 Minuten synchronisiert:

**Online** (grün) - Leser ist eingeschaltet, mit dem Netzwerk verbunden und bereit, Zahlungen zu empfangen

**Offline** (rot) - Leser ist ausgeschaltet, vom Netzwerk getrennt oder nicht erreichbar

**Beschäftigt** (gelb) - Leser verarbeitet derzeit eine Zahlungstransaktion

**Zuletzt gesehen** - Zeitstempel des letzten Check-ins des Lesers bei der Stripe API
- Wird alle ~2 Minuten aktualisiert, wenn der Leser online ist
- Nützlich für die Diagnose von Verbindungsproblemen („Leser war seit 3 Stunden offline“ = Strom- oder Netzwerkproblem während der Geschäftszeiten)

**Status-Anwendungsfälle**:
- **Vor der Öffnung prüfen**: Stellen Sie sicher, dass alle Ladenleser online sind, bevor Sie die Türen öffnen
- **Fehlerbehebung**: „Register 3 akzeptiert keine Karten“ → Prüfen Sie den Leserstatus → Zeigt offline → Prüfen Sie Strom/Netzwerk
- **Prüfung**: „Wurden Zahlungen am Terminal 5 gestern verarbeitet?“ → Prüfen Sie den Zeitstempel des letzten gesehenen Lesers

## Zuordnung zu einem Terminal

Kartenleser verwenden eine **Eins-zu-Eins-Beziehung** zu Terminalen:

**Warum die Zuordnung wichtig ist**:
- Während einer Zahlung muss das POS-System wissen, welcher Leser kommuniziert werden muss
- Mehrere Terminals, die einen Leser teilen, verursachen Konflikte (zwei Kassierer können denselben Leser nicht gleichzeitig verwenden)
- Nicht zugewiesene Leser werden nicht verwendet (verwaiste Hardware)

**Zuordnungsregeln**:
- Jedes Terminal kann **genau einen** Kartenleser zugewiesen haben
- Jeder Kartenleser kann **genau einem** Terminal zugewiesen werden
- Die Zuordnung eines Lesers zu Terminal A entfernt ihn automatisch von dem vorherigen Terminal

**Ändern der Zuordnung**:
- Bearbeiten Sie den Leser-Record
- Ändern Sie das Feld **Terminal** in das neue Terminal
- Speichern
- Das vorherige Terminal verliert die Zuordnung zum Kartenleser (zeigt während der Zahlung eine Fehlermeldung „Kein Leser zugewiesen“ an)

**Nicht zugewiesene Leser**:
- Neue entdeckte Leser starten nicht zugewiesen
- Nicht zugewiesene Leser erscheinen in der Liste, sind aber nicht nutzbar
- Zuordnen Sie sie zu einem Terminal, um sie zu aktivieren

## Anpassung des Startbildschirms

Startbildschirme der Leser zeigen Markenidentität auf dem Kundenbildschirm an, wenn dieser leer ist:

**Was ist ein Startbildschirm?**
- Bild, das auf dem Leserbildschirm angezeigt wird, wenn keine Zahlung verarbeitet wird
- Ersetzt das Standard-Stripe-Logo durch Ihre Markenidentität
- Sichtbar für Kunden, während sie am Kassenschalter warten

**Automatisch generiert vs. benutzerdefiniert**:

**Automatisch generiert** (Standard):
- Spwig generiert den Startbildschirm aus Ihrem Ladenlogo (wenn das Logo in den Laden-Einstellungen konfiguriert ist)
- Automatisch auf die Leserspezifikationen (480×800 Porträt) skaliert
- Monochrom für S700/P400, Farbe für WisePOS E
- Keine Konfiguration erforderlich

**Benutzerdefinierter Startbildschirm** (erweitert):
- Laden Sie Ihr eigenes benutzerdefiniertes Startbild hoch
- Vollständige Kontrolle über Design und Markenidentität
- Muss die Bildanforderungen erfüllen (siehe unten)

**Anforderungen für benutzerdefinierte Startbilder**:
- **Auflösung**: Genau 480×800 Pixel (Porträtorientierung)
- **Format**: PNG oder JPG
- **S700/P400**: Nur Monochrom (schwarz und weiß, keine Grautöne)
- **WisePOS E**: Vollfarbig unterstützt
- **Dateigröße**: <200KB

**Benutzerdefinierten Startbildschirm einstellen**:
1. Bearbeiten Sie den Kartenleser-Record
2. Laden Sie ein Bild in das Feld **Überschreiben des Startbildschirms** hoch (oder wählen Sie es aus der Medienbibliothek aus)
3. Speichern
4. Der Startbildschirm wird innerhalb von 5 Minuten zum Leser synchronisiert

**Benutzerdefinierten Startbildschirm entfernen**:
- Löschen Sie das Feld **Überschreiben des Startbildschirms**
- Speichern
- Der Leser kehrt zum automatisch generierten Startbildschirm zurück (oder zum Stripe-Standard, wenn kein Ladenlogo vorhanden ist)

**Testen des Startbildschirms**:
- Nach dem Hochladen warten Sie 5 Minuten auf die Synchronisation
- Besuchen Sie das Lesergerät
- Überprüfen Sie, ob der Startbildschirm auf dem leeren Bildschirm angezeigt wird
- Prüfen Sie die Bildqualität, Zentrierung und Kontrast

## Stripe Startbildschirm-Konfiguration

Hinter den Kulissen verwaltet Spwig die Konfiguration des Stripe Terminal-Startbildschirms:

**stripe_splash_file_id** - Interner Stripe-Bezeichner für die hochgeladene Startbild-Datei
- Wird automatisch gesetzt, wenn der Startbildschirm hochgeladen wird
- Wird verwendet, um den Startbildschirm in der Stripe API zu referenzieren

**stripe_splash_config_id** - Interner Stripe-Bezeichner für die Startbildschirm-Konfiguration
- Verknüpft die Startbild-Datei mit dem Leser
- Wird automatisch verwaltet, wenn der Startbildschirm dem Leser zugewiesen wird

Diese Felder sind schreibgeschützt und werden automatisch verwaltet – Sie müssen sie nicht direkt bearbeiten.

## Fehlerbehebung bei häufigen Problemen

**Problem 1: Leser zeigt offline an, ist aber eingeschaltet**
- **Ursachen**: Netzwerkverbindungsproblem, Wi-Fi-Passwort geändert, Leser außer Reichweite
- **Lösung**: Prüfen Sie die Netzwerk-Einstellungen des Lesers, verbinden Sie sich erneut mit Wi-Fi, überprüfen Sie, ob die Stripe API von Ihrem Netzwerk aus erreichbar ist

**Problem 2: POS meldet während der Zahlung „Kein Leser zugewiesen“**
- **Ursache**: Leser nicht dem Terminal zugewiesen oder die Zuordnung unvollständig
- **Lösung**: Bearbeiten Sie den Leser, weisen Sie ihn dem Terminal zu, speichern Sie und testen Sie die Zahlung erneut

**Problem 3: Leser bleibt unendlich beschäftigt (steckt fest auf dem Zahlungsbildschirm)**
- **Ursache**: Transaktion abgelaufen oder abgebrochen, Leserstatus nicht zurückgesetzt
- **Lösung**: Leser neu starten (Stromkreis schließen), kontaktieren Sie Stripe Support, wenn das Problem weiter besteht

**Problem 4: Benutzerdefinierter Startbildschirm wird nicht angezeigt**
- **Ursachen**: Bild falsche Auflösung, noch nicht synchronisiert, Monochrom-Anforderung nicht erfüllt (S700/P400)
- **Lösung**: Stellen Sie sicher, dass das Bild genau 480×800 Pixel beträgt, warten Sie 5 Minuten auf die Synchronisation, stellen Sie sicher, dass es monochrom ist für nicht-farbige Leser

**Problem 5: Leser ist in Stripe registriert, aber erscheint nicht in Spwig**
- **Ursache**: Leser ist einem anderen Stripe-Standort zugewiesen als der Anbieterkonfiguration
- **Lösung**: Im Stripe Dashboard prüfen, ob der Leserstandort mit der Anbieterstandort-ID übereinstimmt

## Tipps

- **Ein Leser pro Terminal** - Teilen Sie keine Leser zwischen Terminalen; verhindert Konflikte und vereinfacht die Verantwortung
- **Registrieren Sie Leser vor der Installation** - Vollenden Sie die Stripe-Registrierung und die Spwig-Zuordnung, bevor Sie den Leser an der Kasse platzieren
- **Testen Sie Startbildschirme vor Ort** - Der Kontrast variiert je nach Lesermodell und Beleuchtung; überprüfen Sie, ob der Startbildschirm in der tatsächlichen Umgebung gut aussieht
- **Überwachen Sie den Status vor der Öffnung** - Prüfen Sie täglich die Liste der Leser, um sicherzustellen, dass alle Leser online sind, bevor der Laden öffnet
- **Etikettieren Sie die Hardware physisch** - Verwenden Sie einen Etikettenhersteller, um den Leser mit dem Terminalnamen („Terminal 1 Leser“) zu kennzeichnen, um eine einfache Identifizierung während der Fehlerbehebung zu ermöglichen
- **Halten Sie Leser an einer ununterbrochenen Stromversorgung** - Stromausfälle während einer Transaktion können den Leserstatus beschädigen; ein UPS wird empfohlen
- **Dokumentieren Sie die Seriennummern der Leser** - Erstellen Sie ein Verzeichnis der Seriennummern für Garantie und Support (auf dem Leserhardware-Label zu finden)
- **Aktualisieren Sie die Firmware des Lesers** - Stripe sendet Firmware-Updates automatisch, aber prüfen Sie regelmäßig, ob die Leser auf der neuesten Version sind (prüfen Sie das Stripe Dashboard)