---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ {{ metric_name }}이 정상으로 복구되었습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 문제 해결 완료
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          시스템 건강 상태 복구
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          좋은 소식입니다! {{ metric_name }}의 시스템 건강 상태 문제는 해결되었습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              복구 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>지표:</strong> {{ metric_name }}<br/>
              <strong>현재 값:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>정상 임계값:</strong> {{ normal_threshold }}<br/>
              <strong>문제 감지 시간:</strong> {{ issue_detected_at }}<br/>
              <strong>복구 완료 시간:</strong> {{ recovered_at }}<br/>
              <strong>지속 시간:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ 시스템 상태: 정상
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }}은 정상 수준으로 복구되어 허용 가능한 범위 내에서 작동하고 있습니다.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          해결 요약:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          수행된 조치:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          예방 조치:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          시스템 대시보드 보기
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          사고 보고서 보기
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 문제 해결 완료

시스템 건강 상태 복구

좋은 소식입니다! {{ metric_name }}의 시스템 건강 상태 문제는 해결되었습니다.

복구 세부 정보:
- 지표: {{ metric_name }}
- 현재 값: {{ current_value }}
- 정상 임계값: {{ normal_threshold }}
- 문제 감지 시간: {{ issue_detected_at }}
- 복구 완료 시간: {{ recovered_at }}
- 지속 시간: {{ issue_duration }}

✓ 시스템 상태: 정상
{{ metric_name }}은 정상 수준으로 복구되어 허용 가능한 범위 내에서 작동하고 있습니다.

{% if resolution_summary %}
해결 요약:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
수행된 조치:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
예방 조치:
{{ preventive_measures }}
{% endif %}

시스템 대시보드 보기: {{ dashboard_url }}
{% if incident_report_url %}사고 보고서 보기: {{ incident_report_url }}{% endif %}