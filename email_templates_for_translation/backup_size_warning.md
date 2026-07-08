---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Backup Size Warning - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Backup Size Warning
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your recent backup for {{ shop_name }} has exceeded the recommended size threshold. This may indicate growing data storage needs.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup Information:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current Size:</strong> {{ backup_size }}<br/>
              <strong>Warning Threshold:</strong> {{ size_threshold }}<br/>
              <strong>Growth Since Last Week:</strong> {{ size_increase }}<br/>
              <strong>Backup Date:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Review backup retention policy<br/>
          2. Consider archiving old backups<br/>
          3. Check for unnecessary large files in media library<br/>
          4. Evaluate storage capacity needs<br/>
          5. Monitor backup growth trend
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Manage Backups
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP SIZE WARNING

Hi {{ admin_name }},

Your recent backup for {{ shop_name }} has exceeded the recommended size threshold. This may indicate growing data storage needs.

BACKUP INFORMATION:
- Current Size: {{ backup_size }}
- Warning Threshold: {{ size_threshold }}
- Growth Since Last Week: {{ size_increase }}
- Backup Date: {{ backup_date }}

RECOMMENDED ACTIONS:
1. Review backup retention policy
2. Consider archiving old backups
3. Check for unnecessary large files in media library
4. Evaluate storage capacity needs
5. Monitor backup growth trend

Manage backups: {{ admin_backup_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| admin_name | Administrator name | Admin User |
| shop_name | Store name | Amazing Shop |
| backup_size | Current backup size | 12.4 GB |
| size_threshold | Warning threshold | 10 GB |
| size_increase | Growth amount | +1.8 GB (17%) |
| backup_date | Backup timestamp | 2026-02-15 02:00:00 UTC |
| admin_backup_url | Backup management | https://shop.com/en/admin/backups/ |

## Notes

- Warning alert - proactive notification
- Helps plan for storage capacity
- Threshold typically 80-90% of limit
- Monthly trend analysis recommended
