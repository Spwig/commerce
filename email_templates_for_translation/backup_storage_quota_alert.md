---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Backup Storage Quota Critical - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Storage Quota Critical
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENT:</strong> Your backup storage is critically low. Future backups may fail if storage space is not freed.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Storage Status:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Used:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>Utilization:</strong> {{ storage_percentage }}%<br/>
              <strong>Available:</strong> {{ storage_available }}<br/>
              <strong>Status:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Immediate Actions Required:
            </mj-text>
            <mj-text color="#92400e">
              1. Delete old backups no longer needed<br/>
              2. Archive backups to external storage<br/>
              3. Increase storage quota/capacity<br/>
              4. Review backup retention policy<br/>
              5. Monitor storage daily until resolved
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Manage Storage Now
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 STORAGE QUOTA CRITICAL

Hi {{ admin_name }},

URGENT: Your backup storage is critically low. Future backups may fail if storage space is not freed.

STORAGE STATUS:
- Used: {{ storage_used }} of {{ storage_total }}
- Utilization: {{ storage_percentage }}%
- Available: {{ storage_available }}
- Status: {{ storage_status }}

IMMEDIATE ACTIONS REQUIRED:
1. Delete old backups no longer needed
2. Archive backups to external storage
3. Increase storage quota/capacity
4. Review backup retention policy
5. Monitor storage daily until resolved

Manage storage now: {{ admin_backup_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| admin_name | Administrator name | Admin User |
| storage_used | Space consumed | 47.2 GB |
| storage_total | Total capacity | 50 GB |
| storage_percentage | Utilization % | 94 |
| storage_available | Free space | 2.8 GB |
| storage_status | Alert level | CRITICAL |
| admin_backup_url | Backup management | https://shop.com/en/admin/backups/ |

## Notes

- CRITICAL alert - sent when >90% full
- Risk of backup failure
- Requires immediate action
- Daily monitoring until resolved
