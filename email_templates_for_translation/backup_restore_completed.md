---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Backup Restore Completed - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Backup Restore Completed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your backup restore operation has completed successfully. Your store data has been restored.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Restore Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Backup File:</strong> {{ backup_filename }}<br/>
              <strong>Backup Date:</strong> {{ backup_date }}<br/>
              <strong>Started:</strong> {{ restore_started_at }}<br/>
              <strong>Completed:</strong> {{ restore_completed_at }}<br/>
              <strong>Duration:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Important Next Steps:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Verify your store is functioning correctly<br/>
              2. Check key data (products, orders, customers)<br/>
              3. Clear cache if needed<br/>
              4. Test critical workflows (checkout, admin access)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Go to Admin Dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP RESTORE COMPLETED

Hi {{ admin_name }},

Your backup restore operation has completed successfully. Your store data has been restored.

RESTORE DETAILS:
- Backup File: {{ backup_filename }}
- Backup Date: {{ backup_date }}
- Started: {{ restore_started_at }}
- Completed: {{ restore_completed_at }}
- Duration: {{ restore_duration }}

⚠️ IMPORTANT NEXT STEPS:
1. Verify your store is functioning correctly
2. Check key data (products, orders, customers)
3. Clear cache if needed
4. Test critical workflows (checkout, admin access)

Go to admin dashboard: {{ admin_dashboard_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| admin_name | Administrator name | Admin User |
| backup_filename | Restored backup file | 2026-02-14_full.sql.gz |
| backup_date | When backup was created | 2026-02-14 02:00:00 UTC |
| restore_started_at | Restore start time | 2026-02-15 10:00:00 UTC |
| restore_completed_at | Restore completion | 2026-02-15 10:15:45 UTC |
| restore_duration | Time taken | 15 minutes 45 seconds |
| admin_dashboard_url | Admin dashboard | https://shop.com/en/admin/ |

## Notes

- CRITICAL - Sent after restore completes
- Requires admin verification steps
- Should trigger additional monitoring
- Follow up with manual checks
