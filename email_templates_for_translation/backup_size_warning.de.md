---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Backup-Größenwarnung - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Backup-Größenwarnung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre kürzliche Sicherung für {{ shop_name }} hat den empfohlenen Größengrenzwert überschritten. Dies kann wachsende Speicherbedarf an Daten bedeuten.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup-Informationen:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Aktuelle Größe:</strong> {{ backup_size }}<br/>
              <strong>Warnschwellenwert:</strong> {{ size_threshold }}<br/>
              <strong>Wachstum seit letzter Woche:</strong> {{ size_increase }}<br/>
              <strong>Sicherungsdatum:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Maßnahmen:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Sicherungs-Retentionsrichtlinie überprüfen<br/>
          2. Überlegen Sie, alte Sicherungen zu archivieren<br/>
          3. Prüfen Sie auf unnötige große Dateien in der Medienbibliothek<br/>
          4. Beurteilen Sie die Speicherkapazitätsbedarf<br/>
          5. Verfolgen Sie den Sicherungswachstumstrend
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Sicherungen verwalten
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP-GRÖßENWARNUNG

Hi {{ admin_name }},

Ihre kürzliche Sicherung für {{ shop_name }} hat den empfohlenen Größengrenzwert überschritten. Dies kann wachsende Speicherbedarf an Daten bedeuten.

BACKUP-INFO:
- Aktuelle Größe: {{ backup_size }}
- Warnschwellenwert: {{ size_threshold }}
- Wachstum seit letzter Woche: {{ size_increase }}
- Sicherungsdatum: {{ backup_date }}

EMPFOHLENE MAßnahmen:
1. Sicherungs-Retentionsrichtlinie überprüfen
2. Überlegen Sie, alte Sicherungen zu archivieren
3. Prüfen Sie auf unnötige große Dateien in der Medienbibliothek
4. Beurteilen Sie die Speicherkapazitätsbedarf
5. Verfolgen Sie den Sicherungswachstumstrend

Sicherungen verwalten: {{ admin_backup_url }}