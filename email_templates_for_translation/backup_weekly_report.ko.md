---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
주간 백업 요약 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주간 백업 요약
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              백업 통계:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>총 백업 수:</strong> {{ total_backups }}<br/>
              <strong>성공:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>실패:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>평균 크기:</strong> {{ average_size }}<br/>
              <strong>사용된 총 저장 공간:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 문제 감지:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }}개의 백업이 이번 주에 실패했습니다. 검토하고 수정 조치를 취해 주세요.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          최신 백업:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              크기: {{ backup.size }} | 기간: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ 성공</span>
              {% else %}
              <span style="color: #dc2626;">✗ 실패</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          모든 백업 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주간 백업 요약
{{ week_start }} - {{ week_end }}

백업 통계:
- 총 백업 수: {{ total_backups }}
- 성공: {{ successful_backups }}
- 실패: {{ failed_backups }}
- 평균 크기: {{ average_size }}
- 사용된 총 저장 공간: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ 문제 감지:
{{ failed_backups }}개의 백업이 이번 주에 실패했습니다. 검토하고 수정 조치를 취해 주세요.
{% endif %}

최신 백업:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  크기: {{ backup.size }} | 기간: {{ backup.duration }} | 상태: {{ backup.status }}
{% endfor %}

모든 백업 보기: {{ admin_backup_url }}