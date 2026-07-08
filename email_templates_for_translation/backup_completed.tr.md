---
template_type: backup_completed
category: Backups
---

# Email Template: backup_completed

## Subject
✓ Backup Başarılı - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Backup Completed Successfully
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your scheduled backup for {{ shop_name }} has completed successfully.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Type:</strong> {{ backup_type }}<br/>
              <strong>Started:</strong> {{ backup_started_at }}<br/>
              <strong>Completed:</strong> {{ backup_completed_at }}<br/>
              <strong>Duration:</strong> {{ backup_duration }}<br/>
              <strong>Size:</strong> {{ backup_size }}<br/>
              <strong>Location:</strong> {{ backup_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          View Backup Details
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Next Scheduled Backup:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP COMPLETED SUCCESSFULLY

Hi {{ admin_name }},

Your scheduled backup for {{ shop_name }} has completed successfully.

BACKUP DETAILS:
- Type: {{ backup_type }}
- Started: {{ backup_started_at }}
- Completed: {{ backup_completed_at }}
- Duration: {{ backup_duration }}
- Size: {{ backup_size }}
- Location: {{ backup_location }}

View backup details: {{ admin_backup_url }}

Next Scheduled Backup: {{ next_scheduled_backup }}