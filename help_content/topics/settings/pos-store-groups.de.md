---
title: POS-Store-Gruppen
---

Store-Gruppen organisieren mehrere Einzelhandelsstandorte mit gemeinsamen Konfigurationen. Anstatt jeden Terminal einzeln zu konfigurieren, gruppieren Sie Terminals nach Region, Franchise oder Standorttyp und wenden Sie Einstellungen auf Gruppenebene an. Gruppen unterstützen die Vererbung von Einstellungen – Währung, Sprache, Zeitzone, Belegvorlagen und Werbematerialien werden von der Gruppe auf einzelne Stores weitergeleitet. Dies vereinfacht die Verwaltung für Händler mit mehreren Standorten, während Flexibilität für spezifische Überschreibungen im Store behalten bleibt.

Verwenden Sie Store-Gruppen, wenn Sie mehrere Einzelhandelsstandorte, Franchises oder regionale Märkte mit unterschiedlichen operativen Anforderungen betreiben.

![Store Group List](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Was sind Store-Gruppen?

Store-Gruppen sind organisatorische Container für Lager und Terminals, die gemeinsame Merkmale teilen:

**Gängige Gruppierungsstrategien**:
- **Geografisch**: Nordregion, Südregion, Westküste, Ostküste
- **Franchise**: Franchisee A Stores, Franchisee B Stores, Unternehmensstores
- **Format**: Einkaufszentrum-Orte, Einzelhandelsstandorte, Pop-up-Shops
- **Markt**: Inlandsgeschäfte, europäische Geschäfte, asiatisch-pazifische Geschäfte

Gruppen ändern nicht die physische Betriebsweise von Terminals – sie bieten eine Konfigurationsschicht, die die Verwaltung im großen Stil vereinfacht.

## Wann Store-Gruppen verwenden

**Einzelner Standort** - Gruppen sind nicht erforderlich. Konfigurieren Sie Terminals direkt.

**2-3 Standorte mit identischen Einstellungen** - Gruppen sind optional. Es kann einfacher sein, Terminals direkt zu konfigurieren.

**4+ Standorte** - Gruppen werden stark empfohlen. Zentralisierte Konfiguration spart Zeit.

**Multinationaler Betrieb** - Gruppen sind unerlässlich. Unterschiedliche Währungen, Sprachen und Zeitzone erfordern Überschreibungen auf Gruppenebene.

**Franchise-Betrieb** - Gruppen sind entscheidend. Jeder Franchisee benötigt unabhängige Einstellungen, während Markenkonstanz gewahrt bleibt.

## Einstellungshierarchie der Vererbung

Spwig POS verwendet eine 4-stufige Einstellungskaskade (höchste Priorität zu niedrigster):

| Ebene | Priorität | Beispiel | Anwendungsfall |
|-------|----------|---------|----------|
| **Terminal** | 1 (Höchste) | Terminal 5 überschreibt die Papierbreite auf 58mm | Ein einzelner Terminal hat einzigartige Druckhardware |
| **Store** | 2 | Store 2 überschreibt die Währung auf GBP | UK-Standort unterwiegend US-Store |
| **Gruppe** | 3 | Europäische Gruppe legt die Zeitzone auf CET fest | Regionale Konsistenz über mehrere Stores hinweg |
| **Site** | 4 (Niedrigste) | Globale Standardwerte: USD, Englisch, UTC | Standardwert für alle nicht konfigurierten Einstellungen |

**Funktionsweise**:
- Das System prüft zuerst die Terminal-Einstellungen
- Wenn nicht festgelegt, prüft das System die Store-Einstellungen
- Wenn nicht festgelegt, prüft das System die Gruppeneinstellungen
- Wenn nicht festgelegt, werden die Site-Standardwerte verwendet

**Beispiel**:
- Site-Standard: Währung = USD, Sprache = Englisch
- Gruppe "European Stores": Währung = EUR, Sprache = nicht festgelegt
- Store "Paris Flagship": Währung = nicht festgelegt, Sprache = Französisch
- Terminal "Paris Register 1": Währung = nicht festgelegt, Sprache = nicht festgelegt

**Ergebnis für Paris Register 1**:
- Währung: EUR (erbt von Gruppe)
- Sprache: Französisch (erbt von Store)

Diese Kaskade ermöglicht umfassende Standardwerte mit gezielten Überschreibungen, wo nötig.

## Erstellen einer Store-Gruppe

Navigieren Sie zu **POS > Store Groups** und klicken Sie auf **+ Store Group hinzufügen**:

![Store Group Add Form](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Grundkonfiguration

**Gruppenname** - Beschreibender Bezeichner (z. B. "West Coast Stores", "European Franchises", "Mall Locations")

**Code** - Kurzer eindeutiger Bezeichner (z. B. "WEST", "EUR", "MALL"):
- Wird intern für Referenzen verwendet
- Muss in allen Gruppen eindeutig sein
- 2-10 Zeichen, alphanumerisch
- Großbuchstaben werden zur Konsistenz empfohlen

**Sortierreihenfolge** - Steuert die Anzeigereihenfolge in Verwaltungslisten (niedrigere Zahlen werden zuerst angezeigt):
- Verwenden Sie Vielfache von 10: 10, 20, 30 (erlaubt das Einfügen neuer Gruppen zwischen bestehenden)
- Hilft bei der logischen Organisation von Gruppen (geografische Reihenfolge, Größenreihenfolge usw.)

### Regionale Überschreibungen

**Währungsüberschreibung** - Legen Sie die Gruppenwährung anders als die Site-Standardwährung fest:
- Beispiel: Europäische Gruppe verwendet EUR, asiatisch-pazifische Gruppe verwendet JPY
- Terminals in dieser Gruppe verwenden standardmäßig diese Währung
- Beeinflusst die Preisanzeige, die Bargeldabrechnung und Berichte

**Sprachüberschreibung** - Legen Sie die Gruppensprache anders als die Site-Standardwährung fest:
- Beispiel: Französische Stores verwenden Französisch, deutsche Stores verwenden Deutsch
- Beeinflusst die Sprache der POS-Oberfläche, die Belegsprache (wenn das Template dies unterstützt)
- Mitarbeiter sehen die POS-Oberfläche in dieser Sprache, wenn sie sich bei Gruppenterminals anmelden

**Zeitzonenüberschreibung** - Legen Sie die Gruppenzeitzone anders als die Site-Standardzeitzone fest:
- Beispiel: Westküstenstores verwenden America/Los_Angeles, europäische Stores verwenden Europe/Paris
- Beeinflusst die Schichtzeitenstempel, Berichtsplanung und Werbeauftragsplanung
- Stellt sicher, dass Schichtberichte mit lokalen Geschäftszeiten übereinstimmen

**Wann Überschreibungen vornehmen**:
- **Währung**: Überschreiben Sie immer für internationale Standorte (unterschiedliche Zahlungswährungen)
- **Sprache**: Überschreiben Sie für Märkte, die nicht englischsprachig sind (kundennahes Inhalt)
- **Zeitzone**: Überschreiben Sie für Standorte, die mehr als 2 Stunden von der Site-Standardzeitzone entfernt sind (genaue lokale Zeitstempel)

## Zuordnen von Lagerhäusern zu Gruppen

Nachdem Sie eine Gruppe erstellt haben, weisen Sie Lagerhäuser ihr zu:

1. Navigieren Sie zu **Katalog > Lagerhäuser**
2. Bearbeiten Sie das Lagerhaus, das einen Store-Standort darstellt
3. Legen Sie das Feld **Store Group** auf Ihre erstellte Gruppe fest
4. Speichern Sie

Alle Terminals, die diesem Lagerhaus zugewiesen sind, erben nun die Einstellungen der Gruppe.

**Beispielkonfiguration**:
- Gruppe erstellen: "European Stores" (Währung: EUR, Sprache: nicht festgelegt, Zeitzone: CET)
- Lagerhäuser erstellen: "Paris Store", "Berlin Store", "Rome Store"
- Weisen Sie alle 3 Lagerhäuser der Gruppe "European Stores" zu
- Erstellen Sie Terminals: "Paris Register 1", "Berlin Register 1", "Rome Register 1"
- Jeder Terminal erbt die Währung EUR und die Zeitzone CET von der Gruppe
- Überschreiben Sie die Sprache auf Store-Ebene: Paris=Französisch, Berlin=Deutsch, Rom=Italienisch

## Einstellungen, die von Gruppen gesteuert werden

Gruppen können diese Einstellungen überschreiben:

**Betriebs-einstellungen**:
- Währung (beeinflusst Preisanzeige und Bargeldabrechnung)
- Sprache (beeinflusst die Sprache der POS-Oberfläche)
- Zeitzone (beeinflusst Zeitstempel und Planung)

**Inhaltseinstellungen** (über gebietsspezifische Modelle):
- Belegvorlagen (erstellen Sie gruppenbezogene Belegdesigns)
- Werbeaufträge (zielgerichtete Werbung für bestimmte Gruppen)

**Nicht von Gruppen gesteuert**:
- Terminal-Hardwarekonfiguration (wird pro Terminal konfiguriert)
- Personalzuordnungen (wird pro Terminal konfiguriert)
- Lagerbestandsmengen (wird pro Lager konfiguriert)
- Zahlungsdienstanbieterkonten (wird site-weit oder pro Anbieter konfiguriert)

## Real-World-Beispiele

### Beispiel 1: Internationale Modekette

**Einrichtung**:
- 50 Stores in 5 Ländern
- Jedes Land hat unterschiedliche Währung, Sprache und Steueranforderungen

**Gruppenstruktur**:
- Gruppe: "US Stores" (USD, Englisch, America/New_York)
  - 20 Lagerhäuser (NY, LA, Chicago usw.)
  - 60 Terminals
- Gruppe: "UK Stores" (GBP, Englisch, Europe/London)
  - 10 Lagerhäuser (London, Manchester usw.)
  - 30 Terminals
- Gruppe: "EU Stores" (EUR, nicht festgelegt, Europe/Paris)
  - 15 Lagerhäuser (Paris, Berlin, Rom usw.)
  - 45 Terminals
  - Sprache wird auf Store-Ebene überschrieben (Paris=Französisch, Berlin=Deutsch, Rom=Italienisch)
- Gruppe: "Japan Stores" (JPY, Japanisch, Asia/Tokyo)
  - 5 Lagerhäuser (Tokyo, Osaka usw.)
  - 15 Terminals

**Vorteile**:
- Eine Gruppenkonfiguration gilt für alle Stores in jedem Markt
- Belegvorlagen, die auf Gruppen beschränkt sind (Mehrwertsteuerformat für EU, Umsatzsteuer für US)
- Werbeaufträge, die regional abgestimmt sind (US: Memorial Day Sale, EU: Sommerurlaubssale)

### Beispiel 2: Kaffee-Kette

**Einrichtung**:
- 30 Standorte, alle im gleichen Land, aber unterschiedliche Formate

**Gruppenstruktur**:
- Gruppe: "Mall Locations" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 10 mall-basierte Stores
  - Werbeaufträge mit erweiterten Öffnungszeiten (bis 21 Uhr geöffnet)
  - Belegvorlage mit QR-Code für Parkplatzvalidierung im Einkaufszentrum
- Gruppe: "Standalone Stores" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 15 Stores mit Frontverkauf
  - Standardwerbeaufträge
  - Standardbelegvorlage
- Gruppe: "Airport Locations" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 5 Airport-Stores
  - 24-Stunden-Werbeaufträge
  - Belegvorlage mit Integration von Fluginformationen QR-Code

**Vorteile**:
- Unterschiedliche Werbeinhalte für verschiedene Formate
- Standort-spezifische Beleganpassungen
- Vereinfachte Verwaltung (eine Gruppe aktualisieren anstelle von 10 Einzelstores)

### Beispiel 3: Franchise-Betrieb

**Einrichtung**:
- 100 Stores, 20 verschiedene Franchisee

**Gruppenstruktur**:
- Gruppe: "Franchisee A" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 10 Stores, die von Franchisee A betrieben werden
  - Kontaktinformationen von Franchisee A auf Belegen (über Gruppenbelegvorlage)
  - Werbematerialien von Franchisee A (lokale Veranstaltungen, Angebote)
- Gruppe: "Franchisee B" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 8 Stores, die von Franchisee B betrieben werden
  - Kontaktinformationen von Franchisee B auf Belegen
  - Werbematerialien von Franchisee B
- (Wiederholen Sie dies für alle Franchisee)
- Gruppe: "Corporate Stores" (nicht festgelegt, nicht festgelegt, nicht festgelegt)
  - 5 von der Unternehmensseite betriebene Stores
  - Unternehmensbranding und Werbematerialien

**Vorteile**:
- Jeder Franchisee verwaltet seine eigenen Gruppeneinstellungen
- Markenkonstanz wird über Site-Standardwerte gewahrt
- Unabhängigkeit der Franchisee über Gruppenüberschreibungen

## Verwalten von Gruppeneinstellungen

**Ändern von Gruppeneinstellungen** beeinflusst alle Terminals in dieser Gruppe:
- Währungswechsel: Alle Gruppenterminals wechseln auf die neue Währung bei der nächsten Synchronisation
- Sprachwechsel: Alle Gruppenterminals wechseln auf die neue Sprache bei der nächsten Synchronisation
- Zeitzonenumstellung: Alle Gruppenterminals berechnen die Zeitstempel erneut bei der nächsten Synchronisation

**Überlegungen zur Auswirkung**:
- Testen Sie Änderungen an einem einzelnen Terminal, bevor Sie sie auf die gesamte Gruppe anwenden
- Informieren Sie das Personal über bevorstehende Änderungen (z. B. Sprachwechsel)
- Planen Sie Änderungen während der Nebenzeit, um Störungen zu minimieren

**Entfernen einer Gruppe**:
- Weisen Sie alle Lagerhäuser einer anderen Gruppe zu oder entfernen Sie die Gruppenzuordnung
- Terminals verlieren die Gruppeneinstellungen und fallen zurück auf Site-Standardwerte
- Gruppen können nicht gelöscht werden, solange Lagerhäuser ihr zugewiesen sind

## Tipps

- **Verwenden Sie bedeutsame Codes** - "WEST" ist klarer als "GRP1", wenn Sie Konfigurationen überprüfen
- **Planen Sie die Hierarchie vor der Erstellung von Gruppen** - Denken Sie zunächst über Ihre Organisationsstruktur nach; eine Neustrukturierung später ist mühsam
- **Testen Sie Gruppeneinstellungen mit einem Terminal** - Bevor Sie 50 Lagerhäuser einer Gruppe zuweisen, testen Sie die Gruppeneinstellungen mit einem Terminal
- **Überschreiben Sie sparsam auf Store-Ebene** - Zu viele Store-Ebene-Überschreibungen entziehen den Gruppen ihren Zweck
- **Dokumentieren Sie den Zweck der Gruppen** - Notieren Sie im Gruppennamen, was diese Gruppe ausmacht (Geografie, Format, Franchisee)
- **Verwenden Sie die Sortierreihenfolge strategisch** - Ordnen Sie Gruppen nach Bedeutung (Corporate Stores zuerst) oder Geografie (West nach Ost) für eine einfachere Navigation
- **Halten Sie die Anzahl der Gruppen angemessen** - 20+ Gruppen deuten auf Übersegmentierung hin; überlegen Sie, ob Sie sie konsolidieren können
- **Währungsüberschreibungen sind dauerhaft** - Das Wechseln der Währung einer Gruppe während des Betriebs kompliziert die Buchhaltung; planen Sie sorgfältig

