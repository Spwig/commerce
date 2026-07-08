---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 URGENT: Backup Failed - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Backup Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A critical backup operation has failed for your {{ shop_name }} store. Immediate action is required to ensure data protection.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Backup Details:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Backup Type:</strong> {{ backup_type }}<br/>
              <strong>Started:</strong> {{ backup_started_at }}<br/>
              <strong>Failed:</strong> {{ backup_failed_at }}<br/>
              <strong>Duration:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error Details:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Check available disk space on your server<br/>
          2. Verify database connectivity<br/>
          3. Review error log for detailed stack trace<br/>
          4. Retry backup manually or wait for next scheduled run<br/>
          5. Contact support if the issue persists
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Backup Logs
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Retry Backup Now
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Last Successful Backup:</strong> {{ last_successful_backup }}<br/>
          <strong>Next Scheduled Backup:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 URGENT: BACKUP FAILED

Hi {{ admin_name }},

A critical backup operation has failed for your {{ shop_name }} store. Immediate action is required to ensure data protection.

BACKUP DETAILS:
- Backup Type: {{ backup_type }}
- Started: {{ backup_started_at }}
- Failed: {{ backup_failed_at }}
- Duration: {{ backup_duration }}

ERROR DETAILS:
{{ error_message }}

RECOMMENDED ACTIONS:
1. Check available disk space on your server
2. Verify database connectivity
3. Review error log for detailed stack trace
4. Retry backup manually or wait for next scheduled run
5. Contact support if the issue persists

View backup logs: {{ admin_backup_url }}
Retry backup now: {{ retry_backup_url }}

Last Successful Backup: {{ last_successful_backup }}
Next Scheduled Backup: {{ next_scheduled_backup }}

---
This is a critical system alert for {{ shop_name }} administrators.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| admin_name | Administrator's name | Admin User |
| shop_name | Store name | Amazing Shop |
| backup_type | Type of backup | Full Database Backup |
| backup_started_at | When backup began | 2026-02-15 02:00:00 UTC |
| backup_failed_at | When backup failed | 2026-02-15 02:15:30 UTC |
| backup_duration | How long backup ran before failing | 15 minutes 30 seconds |
| error_message | Technical error message | Disk quota exceeded: /var/backups |
| admin_backup_url | Link to backup admin page | https://shop.com/en/admin/backups/ |
| retry_backup_url | Link to retry backup | https://shop.com/en/admin/backups/retry/123 |
| last_successful_backup | Date/time of last success | 2026-02-14 02:00:00 UTC (1 day ago) |
| next_scheduled_backup | Next automatic backup time | 2026-02-16 02:00:00 UTC (in 22 hours) |
| theme.color.primary | Primary brand color | #2563eb |
| theme.color.text | Main text color | #1f2937 |
| theme.color.text_secondary | Secondary text color | #6b7280 |

## Notes

- CRITICAL PRIORITY - Always sent regardless of admin preferences
- Sent immediately when backup fails
- Red color scheme to indicate urgency
- Includes technical error details for troubleshooting
- Provides actionable steps for resolution
- Links to admin interface for immediate action
- Should trigger additional alerting (SMS, push notification) if configured
- Part of backup health monitoring system
- Follows up with backup_weekly_report to track resolution
