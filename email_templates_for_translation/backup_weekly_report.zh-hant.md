---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
週末備份摘要 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          週末備份摘要
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              備份統計數據：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>總備份數：</strong> {{ total_backups }}<br/>
              <strong>成功：</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>失敗：</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>平均大小：</strong> {{ average_size }}<br/>
              <strong>總共使用儲存空間：</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 發現問題：
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} 個備份失敗。請檢閱並採取糾正措施。
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最新備份：
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
              <span style="color: #059669;">✓ 成功</span>
              {% else %}
              <span style="color: #dc2626;">✗ 失敗</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          查看所有備份
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
週末備份摘要
{{ week_start }} - {{ week_end }}

備份統計數據：
- 總備份數：{{ total_backups }}
- 成功：{{ successful_backups }}
- 失敗：{{ failed_backups }}
- 平均大小：{{ average_size }}
- 總共使用儲存空間：{{ total_storage }}

{% if failed_backups > 0 %}
⚠️ 發現問題：
{{ failed_backups }} 個備份失敗。請檢閱並採取糾正措施。
{% endif %}

最新備份：
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Size: {{ backup.size }} | Duration: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

查看所有備份：{{ admin_backup_url }}