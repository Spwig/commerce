---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Speicherplatzkontingent kritisch - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Speicherplatzkontingent kritisch
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>DRINGEND:</strong> Ihr Backup-Speicherplatz ist kritisch niedrig. Zukünftige Backups können fehlschlagen, wenn nicht genug Speicherplatz vorhanden ist.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Speicherstatus:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Verwendet:</strong> {{ storage_used }} von {{ storage_total }}<br/>
              <strong>Nutzung:</strong> {{ storage_percentage }}%<br/>
              <strong>Verfügbar:</strong> {{ storage_available }}<br/>
              <strong>Status:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Sofortige Maßnahmen erforderlich:
            </mj-text>
            <mj-text color="#92400e">
              1. Alte Backups löschen, die nicht mehr benötigt werden<br/>
              2. Backups in externe Speicher archivieren<br/>
              3. Speicherplatzkontingent/ -kapazität erhöhen<br/>
              4. Backup-Retentionsrichtlinie überprüfen<br/>
              5. Speicherplatz täglich überwachen, bis das Problem gelöst ist
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Speicher jetzt verwalten
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 SPEICHERPLATZKONTINGENT KRITISCH

Hi {{ admin_name }},

DRINGEND: Ihr Backup-Speicherplatz ist kritisch niedrig. Zukünftige Backups können fehlschlagen, wenn nicht genug Speicherplatz vorhanden ist.

SPEICHERSTATUS:
- Verwendet: {{ storage_used }} von {{ storage_total }}
- Nutzung: {{ storage_percentage }}%
- Verfügbar: {{ storage_available }}
- Status: {{ storage_status }}

SOFOORTIGE MAßNAHMEN ERFAORDERT:
1. Alte Backups löschen, die nicht mehr benötigt werden
2. Backups in externe Speicher archivieren
3. Speicherplatzkontingent/ -kapazität erhöhen
4. Backup-Retentionsrichtlinie überprüfen
5. Speicherplatz täglich überwachen, bis das Problem gelöst ist

Speicher jetzt verwalten: {{ admin_backup_url }}