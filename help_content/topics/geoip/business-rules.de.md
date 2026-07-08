---
title: Ortsspezifische Geschäftsregeln
---

Ortsspezifische Geschäftsregeln ermöglichen es Ihnen, automatisch Aktionen auszuführen, wenn ein Besucher aus einem bestimmten Land, einer Region oder einem Geräte-Typ kommt. Sie können Regeln verwenden, um für Kunden aus einer bestimmten Region eine Währung festzulegen, Besucher auf eine lokalisierte Seite umzuleiten, einen Werbebanner anzuzeigen oder den Zugriff auf bestimmte Inhalte zu beschränken.

Die Regeln werden in Prioritätsreihenfolge jedes Mal bewertet, wenn eine Besucher-Sitzung hergestellt wird. Wenn eine Regel übereinstimmt, werden ihre konfigurierten Aktionen sofort ausgeführt.

## Wie Geschäftsregeln funktionieren

Jede Regel besteht aus zwei Teilen:

- **Bedingungen** — die Kriterien, die erfüllt sein müssen, damit die Regel ausgelöst wird (z. B. "Besucher kommt aus Deutschland")
- **Aktionen** — was geschieht, wenn alle Bedingungen erfüllt sind (z. B. "Währung auf EUR setzen")

Bedingungen und Aktionen werden als JSON-Objekte im Regel-Formular gespeichert. Spwig bewertet alle aktiven Regeln in Prioritätsreihenfolge (niedrigste Zahl zuerst) und wendet alle an, die übereinstimmen.

## Zum Navigieren zu Geschäftsregeln

Navigieren Sie zu **Customers > Business Rules**, um alle Ihre konfigurierten Regeln zu sehen. Die Liste zeigt den Namen jeder Regel, den Status, die Priorität, wie oft sie ausgelöst wurde und wann sie zuletzt ausgelöst wurde.

Klicken Sie auf eine Regel, um sie anzuzeigen oder zu bearbeiten, oder klicken Sie auf **+ Add Business Rule**, um eine neue Regel zu erstellen.

## Eine Geschäftsregel erstellen

### Schritt 1: Grundinformationen

Füllen Sie die Identifikationsdetails der Regel aus:

- **Name** — ein klarer, beschreibender Name (z. B. `Set EUR for Eurozone`)
- **Beschreibung** — optionale Notizen, die den Zweck der Regel erklären
- **Aktiv** — aktivieren Sie dies, um die Regel zu aktivieren; deaktivieren Sie es, um sie ohne zu löschen zu pausieren
- **Priorität** — niedrigere Zahlen werden zuerst ausgeführt; verwenden Sie `10`, `20`, `30`, um Raum für zukünftige Regeln zu lassen

### Schritt 2: Bedingungen definieren

Im Feld **Bedingungen** geben Sie ein JSON-Objekt ein, das beschreibt, wann die Regel ausgelöst werden soll. Alle Bedingungen im Objekt müssen wahr sein, damit die Regel übereinstimmt.

#### Verfügbare Bedingungsschlüssel

| Bedingung | Format | Beispiel |
|-----------|--------|---------|
| `country_in` | Array von ISO-Ländercodes | `["DE", "FR", "IT"]` |
| `country_not_in` | Array von ISO-Ländercodes | `["US", "CA"]` |
| `region_in` | Array von Regionennamen | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Array von Regionennamen | `["Quebec"]` |
| `is_mobile` | Boolean | `true` |
| `is_vpn` | Boolean | `false` |

#### Beispielbedingungen

Besucher aus Deutschland, Frankreich oder Italien:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Besucher aus den Vereinigten Staaten, die auf einem mobilen Gerät sind:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Besucher außerhalb der Europäischen Union:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Schritt 3: Aktionen definieren

Im Feld **Aktionen** geben Sie ein JSON-Objekt ein, das beschreibt, was geschehen soll, wenn die Regel ausgelöst wird.

#### Verfügbare Aktionsschlüssel

| Aktion | Format | Beschreibung |
|--------|--------|-------------|
| `set_currency` | Währungscode-String | Wählen Sie eine Währung für den Besucher vorab aus |
| `set_language` | Sprachcode-String | Legen Sie die Anzeigesprache fest |
| `show_banner` | Boolean | Auslösen eines Werbebanners |
| `redirect_to` | URL-Pfad-String | Leiten Sie den Besucher zu einer anderen URL um |

#### Beispielaktionen

Währung auf Euro setzen:
```json
{
  "set_currency": "EUR"
}
```

Zu einer lokalisierten Startseite umleiten:
```json
{
  "redirect_to": "/de/"
}
```

Währung und Sprache gleichzeitig setzen:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Praktische Beispiele

### Beispiel: Währungsregel für die Eurozone

**Szenario:** Zeigen Sie automatisch Euro-Preise an, wenn Besucher aus Ländern der Eurozone kommen.

| Feld | Wert |
|-------|-------|
| Name | `Eurozone — Set EUR` |
| Priorität | `10` |
| Ist aktiv | Angekreuzt |
| Bedingungen | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Aktionen | `{"set_currency": "EUR"}` |

### Beispiel: Währungsregel für das Vereinigte Königreich

**Szenario:** Zeigen Sie GBP-Preise an, wenn Besucher aus dem Vereinigten Königreich kommen.

| Feld | Wert |
|-------|-------|
| Name | `UK — Set GBP` |
| Priorität | `20` |
| Aktiv | Angekreuzt |
| Bedingungen | `"{\"country_in\": [\"GB\"]}"` |
| Aktionen | `"{\"set_currency\": \"GBP\"}"` |

### Beispiel: Umleiten zu einem lokalisierten Bereich

**Szenario:** Besucher aus Australien an eine dedizierte australische Seite weiterleiten.

| Feld | Wert |
|-------|-------|
| Name | `Australia — Redirect` |
| Priorität | `30` |
| Aktiv | Angekreuzt |
| Bedingungen | `"{\"country_in\": [\"AU\"]}"` |
| Aktionen | `"{\"redirect_to\": \/au\/}"` |

## Regeln testen

Sie können überprüfen, ob eine Regel dem erwarteten Besucherprofil entspricht, ohne auf echten Traffic zu warten:

1. In der Liste der Geschäftsregeln die Regel mit dem Häkchen auswählen
2. Öffnen Sie das **Aktion**-Dropdown und wählen Sie **Test ausgewählte Regeln**
3. Klicken Sie auf **Weiter**

Spwig bewertet die Regel anhand eines Beispielprofils eines Besuchers aus den USA und meldet, ob sie übereinstimmt und welche Aktionen ausgelöst worden wären.

## Überwachung der Regelaktivität

Die Spalte **Ausgelöst** in der Regel-Liste zeigt an, wie oft jede Regel ausgelöst wurde. Klicken Sie auf eine Regel, um den **Letzten Auslösezeitpunkt** im Statistikabschnitt anzuzeigen.

Verwenden Sie die Aktion **Statistik zurücksetzen**, um die Auslösezählung zu null zu setzen, wenn Sie nach Änderungen an einer Regel ab einem bestimmten Datum neu messen möchten.

## Tipps

- Legen Sie Prioritäten mit Lücken (10, 20, 30) anstelle von sequenziellen Zahlen (1, 2, 3) fest, damit Sie später neue Regeln einfügen können, ohne alles neu zu nummerieren
- Regeln werden in Prioritätsreihenfolge ausgelöst und alle übereinstimmenden Regeln werden angewendet – wenn zwei Regeln beide die Währung festlegen, wird die Aktion der Regel mit niedrigerer Priorität (höherer Zahl) zuletzt angewendet
- Verwenden Sie den **Aktiv**-Schalter, um eine Regel vorübergehend zu pausieren, während Sie keine Promotion durchführen, ohne die Konfiguration zu löschen
- Testen Sie immer eine neue Regel, bevor Sie sie in der Live-Umgebung aktivieren, um sicherzustellen, dass die Bedingungen korrekt sind
- Die Erkennung von VPNs (`"is_vpn": true`) ist verfügbar, wenn Sie unterschiedliche Behandlung für Besucher mit versteckter Standort verwenden möchten, beachten Sie jedoch, dass einige legitime Kunden VPNs für den Datenschutz verwenden