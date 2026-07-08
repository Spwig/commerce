---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Weekly Backup Summary - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Weekly Backup Summary
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup Statistics:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Backups:</strong> {{ total_backups }}<br/>
              <strong>Successful:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Failed:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Average Size:</strong> {{ average_size }}<br/>
              <strong>Total Storage Used:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Issues Detected:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} backup(s) failed this week. Please review and take corrective action.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Latest Backups:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Size: {{ backup.size }} | Duration: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Success</span>
              {% else %}
              <span style="color: #dc2626;">✗ Failed</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          View All Backups
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
WEEKLY BACKUP SUMMARY
{{ week_start }} - {{ week_end }}

BACKUP STATISTICS:
- Total Backups: {{ total_backups }}
- Successful: {{ successful_backups }}
- Failed: {{ failed_backups }}
- Average Size: {{ average_size }}
- Total Storage Used: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ ISSUES DETECTED:
{{ failed_backups }} backup(s) failed this week. Please review and take corrective action.
{% endif %}

LATEST BACKUPS:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Size: {{ backup.size }} | Duration: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

View all backups: {{ admin_backup_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| week_start | Week start date | February 8, 2026 |
| week_end | Week end date | February 14, 2026 |
| total_backups | Total backup count | 7 |
| successful_backups | Success count | 6 |
| failed_backups | Failure count | 1 |
| average_size | Avg backup size | 2.3 GB |
| total_storage | Storage consumed | 16.1 GB |
| recent_backups | List of backups | [{date, type, size, duration, status}] |
| admin_backup_url | Backup admin | https://shop.com/en/admin/backups/ |

## Notes

- Sent weekly (e.g., Monday morning)
- Summary of backup health
- Opt-in for admins who want digest instead of individual notifications
- Highlights issues for review
