---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 CRITICAL: Backup Restore Failed - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 CRITICAL: Backup Restore Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Ciao {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un'operazione di ripristino del backup critica è fallita. Il tuo negozio potrebbe essere in uno stato inconsistente e richiede un'attenzione immediata.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Restore Details:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Backup File:</strong> {{ backup_filename }}<br/>
              <strong>Started:</strong> {{ restore_started_at }}<br/>
              <strong>Failed:</strong> {{ restore_failed_at }}<br/>
              <strong>Duration:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 IMMEDIATE ACTION REQUIRED:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>DO NOT</strong> make any changes to the store<br/>
              2. Check database connectivity and integrity<br/>
              3. Review error logs for detailed stack trace<br/>
              4. Contact technical support immediately<br/>
              4. Consider rolling back to last known good state
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Restore Logs
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Contact Emergency Support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CRITICAL: BACKUP RESTORE FAILED

Hi {{ admin_name }},

A critical backup restore operation has failed. Your store may be in an inconsistent state and requires immediate attention.

RESTORE DETAILS:
- Backup File: {{ backup_filename }}
- Started: {{ restore_started_at }}
- Failed: {{ restore_failed_at }}
- Duration: {{ restore_duration }}

ERROR DETAILS:
{{ error_message }}

🚨 IMMEDIATE ACTION REQUIRED:
1. DO NOT make any changes to the store
2. Check database connectivity and integrity
3. Review error logs for detailed stack trace
4. Contact technical support immediately
5. Consider rolling back to last known good state

View restore logs: {{ admin_backup_url }}
Contact emergency support: {{ support_url }}