---
title: Benutzerdefinierte Felder
---

Benutzerdefinierte Felder ermöglichen es Ihnen, zusätzliche Daten zu Produkten, Kategorien, Bestellungen und Kundenprofilen hinzuzufügen, ohne den Code zu ändern. Verwenden Sie sie, um geschäftsbezogene Informationen wie externe API-IDs, Lagerorten, Konformitätsdaten oder beliebige Attribute zu speichern, die Ihr Geschäft benötigt.

## Zugang zu benutzerdefinierten Feldern

Navigieren Sie zu **Einstellungen > Benutzerdefinierte Felder** in der Admin-Seitenleiste.

![Seite benutzerdefinierte Felder](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Schlüsselkonzepte

### Feldgruppen

Felder sind in **Gruppen** organisiert – logische Sammlungen, die als Abschnitt zusammen angezeigt werden. Ein Beispiel für eine "Versandinformationen"-Gruppe könnte Felder für Lagerort, Paketmaße und Gefahrgutklassifizierung enthalten.

### Felddefinitionen

Jede Felddefinition steuert:
- **Name**: Das Label, das in Formularen angezeigt wird
- **Slug**: Der maschinenlesbare Schlüssel, der in JSON-Speicher und API-Antworten verwendet wird
- **Feldtyp**: Welche Art von Eingabe gerendert wird (Text, Zahl, Dropdown usw.)
- **Validierung**: Regeln wie Min/Max, Maximallänge, Regex oder erlaubte Optionen
- **Sichtbarkeit**: Ob das Feld auf dem Frontend angezeigt wird

### Unterstützte Feldtypen

| Typ | Beschreibung | Beispielverwendung |
|------|-------------|-------------|
| **Text** | Einzeilige Texteingabe | Externe API-ID, Markencode |
| **Textbereich** | Mehrzeiliger Text | Besondere Behandlungsnotizen |
| **Zahl** | Ganzzahlwerte | Mindestbestellmenge |
| **Dezimalzahl** | Dezimalwerte | Gewichtsübernahme, benutzerdefinierte Dimension |
| **Ja/Nein** | Kontrollkästchen | Ist zerbrechlich, benötigt Unterschrift |
| **Datum** | Datumsauswahl | Veröffentlichungsdatum, Ablaufdatum |
| **Datum und Uhrzeit** | Datums- und Uhrzeitauswahl | Geplante Verfügbarkeit |
| **URL** | Webadresse | Lieferantenslink, Spezifikationsblatt-URL |
| **E-Mail** | E-Mail-Adresse | Herstellerkontakt |
| **Dropdown** | Einzelwahlliste | Materialtyp, Ursprungsland |
| **Mehrfachauswahl** | Mehrfachauswahlliste | Zertifizierungen, Tags |
| **Farbe** | Farbauswahl | Markenfarbe, Etikettfarbe |

## Verwaltung benutzerdefinierter Felder

### Erstellen einer Feldgruppe

1. Öffnen Sie **Einstellungen > Benutzerdefinierte Felder**
2. Wählen Sie den Modultab (Produkte, Kategorien, Bestellungen oder Kundenprofile) aus
3. Klicken Sie auf **Gruppe hinzufügen**
4. Geben Sie einen **Gruppennamen** ein (z. B. "Externe Integrationen")
5. Aktivieren Sie optional **Auf Frontend anzeigen**, wenn Kunden diese Felder sehen sollen
6. Klicken Sie auf **Gruppe speichern**

### Feld zu einer Gruppe hinzufügen

1. Auf der Gruppenkarte klicken Sie auf **Feld hinzufügen**
2. Geben Sie einen **Feldnamen** ein – der Slug wird automatisch generiert
3. Wählen Sie den **Feldtyp** aus
4. Geben Sie optional eine **Hilfetext** und einen **Standardwert** ein
5. Konfigurieren Sie Validierungsoptionen (variiert je nach Feldtyp):
   - Text: Maximallänge, Regex-Muster
   - Zahl/Dezimalzahl: Mindest- und Höchstwert
   - Dropdown: Definieren Sie die Liste der Optionen
6. Setzen Sie Feldoptionen:
   - **Erforderlich**: Händler müssen dieses Feld ausfüllen, wenn sie es speichern
   - **Auf Frontend anzeigen**: Wert auf der Kundenfassungseite anzuzeigen
   - **Übersetzbar**: Ermöglicht die Übersetzung des Werts (nur Text/Textbereich)
7. Klicken Sie auf **Feld speichern**

### Bearbeiten und Sortieren

- Klicken Sie auf das **Stiftsymbol** für eine Gruppe oder ein Feld, um es zu bearbeiten
- Ziehen Sie das **Greifsymbol** zum Sortieren von Gruppen oder Feldern innerhalb einer Gruppe
- Änderungen wirken sich sofort auf alle relevanten Formulare aus

### Löschen von Gruppen und Feldern

- Klicken Sie auf das **Müllsymbol** einer Gruppe oder eines Felds, um es zu löschen
- Löschen ist ein **weiches Löschen** – die Daten werden im Datenbank beibehalten, aber aus Formularen verborgen
- Dies schützt bestehende Daten vor versehentlichem Verlust

## Verwenden von benutzerdefinierten Feldern in Formularen

Sobald Sie benutzerdefinierte Felder für ein Modell definiert haben, erscheint automatisch eine **Benutzerdefinierte Felder**-Registerkarte auf dem entsprechenden Bearbeitungsformular.

### Produkte und Kategorien

1. Öffnen Sie ein beliebiges Produkt oder eine Kategorie zum Bearbeiten
2. Klicken Sie auf die Registerkarte **Benutzerdefinierte Felder**
3. Füllen Sie die Felder entsprechend aus
4. Klicken Sie auf **Speichern** – die Werte werden zusammen mit dem Datensatz gespeichert

### Bestellungen

Benutzerdefinierte Feldwerte für Bestellungen werden als **nur-lesbarer Abschnitt** auf der Bestelldetailseite angezeigt. Benutzerdefinierte Felder für Bestellungen werden in der Regel über die API oder am Checkout gesetzt.

### Kundenprofile

1. Öffnen Sie ein Kundenprofil
2. Klicken Sie auf die Registerkarte **Benutzerdefinierte Felder**
3. Füllen Sie die Felder aus und speichern Sie sie

## API-Zugriff

### Auflisten von Felddefinitionen

Alle benutzerdefinierten Felddefinitionen für ein Modell abrufen:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Antwort:**
```json
[
  {
    "id": 1,
    "name": "Externe API-ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "Externe Integrationen" }
  }
]
```

### Lesen von benutzerdefinierten Feldwerten

Benutzerdefinierte Feldwerte sind in dem `custom_fields` JSON-Objekt in API-Antworten enthalten:

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Schreiben von benutzerdefinierten Feldwerten

Fügen Sie `custom_fields` hinzu, wenn Sie über die API einen Datensatz erstellen oder aktualisieren:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Werte werden gegen die Felddefinitionen validiert. Ungültige Werte geben einen `400` Fehler mit Details zurück.

### Abfragen über benutzerdefinierte Felder

Benutzerdefinierte Felder sind für schnelle Datenbankabfragen indiziert. Filtern Sie Datensätze mithilfe von Datenbankabfrage-Filtern:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Frontend-Anzeige

### Für Theme-Entwickler

Verwenden Sie den `render_custom_fields` Template-Tag, um benutzerdefinierte Felder auf dem Frontend anzuzeigen:

```python
{% load custom_fields_tags %}

{# Rendern aller auf dem Frontend sichtbaren Felder #}
{% render_custom_fields product %}

{# Einen bestimmten Feldwert abrufen #}
{% get_custom_field product "warehouse_location" as location %}
<p>Versand von: {{ location }}</p>
```

Nur Felder, bei denen **Auf Frontend anzeigen** auf Gruppen- und Feld Ebene aktiviert ist, werden gerendert.

## Best Practices

- **Verwenden Sie beschreibende Namen** – Feldnamen werden in Formularen und auf dem Frontend angezeigt
- **Setzen Sie Hilfetexte** – leiten Sie Händler an, was in jedem Feld eingegeben werden soll
- **Gruppieren Sie verwandte Felder** – halten Sie Formulare organisiert und intuitiv
- **Verwenden Sie Standardwerte** – setzen Sie sinnvolle Standardwerte, um die Dateneingabe zu reduzieren
- **Seien Sie selektiv mit der Frontend-Sichtbarkeit** – zeigen Sie nur Felder an, die für Kunden relevant sind
- **Verwenden Sie Slugs in Integrationen** – Slugs sind stabile Identifikatoren; Feldnamen können sich ändern

## Problembehandlung

**Benutzerdefinierte Felder-Registerkarte wird nicht angezeigt:**
- Stellen Sie sicher, dass mindestens eine aktive Feldgruppe für dieses Modell vorhanden ist
- Prüfen Sie, ob die Admin-Klasse den `CustomFieldsAdminMixin` enthält
- Löschen Sie den Cache und aktualisieren Sie die Seite

**Feldwerte werden nicht gespeichert:**
- Stellen Sie sicher, dass erforderliche Felder ausgefüllt sind
- Prüfen Sie die Validierungsregeln (Min/Max, Regex-Muster, erlaubte Optionen)
- Stellen Sie sicher, dass das Feld aktiv und nicht weichgelöscht ist

**API gibt leere custom_fields zurück:**
- Bestätigen Sie, dass das Modell den `CustomFieldsMixin` enthält
- Prüfen Sie, ob Felddefinitionen für den richtigen Inhaltstyp vorhanden sind
- Stellen Sie sicher, dass der Serializer `CustomFieldsSerializerMixin` enthält

## Verwandte Themen

- [Produkte hinzufügen](#)
- [Store Einstellungen](#)