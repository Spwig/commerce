---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
週次バックアップの要約 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          週次バックアップの要約
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              バックアップ統計:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>総バックアップ数:</strong> {{ total_backups }}<br/>
              <strong>成功:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>失敗:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>平均サイズ:</strong> {{ average_size }}<br/>
              <strong>使用された総ストレージ:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 問題が検出されました:
            </mj-text>
            <mj-text color="#7f1d1d">
              今週、{{ failed_backups }} 件のバックアップが失敗しました。確認し、修正措置を講じてください。
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最新のバックアップ:
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
          すべてのバックアップを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
週次バックアップの要約
{{ week_start }} - {{ week_end }}

バックアップ統計:
- 総バックアップ数: {{ total_backups }}
- 成功: {{ successful_backups }}
- 失敗: {{ failed_backups }}
- 平均サイズ: {{ average_size }}
- 使用された総ストレージ: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ 問題が検出されました:
{{ failed_backups }} 件のバックアップが今週失敗しました。確認し、修正措置を講じてください。
{% endif %}

最新のバックアップ:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Size: {{ backup.size }} | Duration: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

すべてのバックアップを表示: {{ admin_backup_url }}