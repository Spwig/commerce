---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ การสำรองข้อมูลตามกำหนดเวลาไม่ได้ดำเนินการ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Scheduled Backup Missed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A scheduled backup for {{ shop_name }} did not run as expected. Your data may not be fully protected.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup Schedule Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Scheduled Time:</strong> {{ scheduled_time }}<br/>
              <strong>Backup Type:</strong> {{ backup_type }}<br/>
              <strong>Last Successful Backup:</strong> {{ last_successful_backup }}<br/>
              <strong>Time Since Last Backup:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Possible Causes:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Server was offline or unreachable<br/>
          • Scheduled task service not running<br/>
          • Insufficient permissions<br/>
          • Storage space full<br/>
          • Database connectivity issues
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Run Backup Manually
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View System Logs
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SCHEDULED BACKUP MISSED

Hi {{ admin_name }},

A scheduled backup for {{ shop_name }} did not run as expected. Your data may not be fully protected.

BACKUP SCHEDULE DETAILS:
- Scheduled Time: {{ scheduled_time }}
- Backup Type: {{ backup_type }}
- Last Successful Backup: {{ last_successful_backup }}
- Time Since Last Backup: {{ time_since_last }}

POSSIBLE CAUSES:
• Server was offline or unreachable
• Scheduled task service not running
• Insufficient permissions
• Storage space full
• Database connectivity issues

Run backup manually: {{ admin_backup_url }}
View system logs: {{ admin_logs_url }}