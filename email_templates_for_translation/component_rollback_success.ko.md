---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }}을(를) 이전 버전 v{{ previous_version }}으로 롤백했습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ 롤백 완료
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          구성 요소 복원
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }}은(는) 이전 버전으로 성공적으로 롤백되었습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              롤백 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>구성 요소:</strong> {{ component_name }}<br/>
              <strong>롤백 전:</strong> v{{ failed_version }}<br/>
              <strong>복원된 버전:</strong> v{{ previous_version }}<br/>
              <strong>완료 시간:</strong> {{ completed_at }}<br/>
              <strong>기간:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          롤백 원인:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ 가게 상태
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              가게는 이제 안정적인 버전 {{ previous_version }}에서 실행되고 있습니다. 모든 기능이 복원되어야 합니다.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>데이터 복원:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음 단계:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          구성 요소 세부 정보 보기
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          사고 보고서 보기
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          문제가 계속 발생하는 경우 지원팀에 문의해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ 롤백 완료

구성 요소 복원

{{ component_name }}은(는) 이전 버전으로 성공적으로 롤백되었습니다.

롤백 세부 정보:
- 구성 요소: {{ component_name }}
- 롤백 전: v{{ failed_version }}
- 복원된 버전: v{{ previous_version }}
- 완료 시간: {{ completed_at }}
- 기간: {{ rollback_duration }}

{% if rollback_reason %}
롤백 원인:
{{ rollback_reason }}
{% endif %}

✓ 가게 상태:
가게는 이제 안정적인 버전 {{ previous_version }}에서 실행되고 있습니다. 모든 기능이 복원되어야 합니다.

{% if data_restored %}
데이터 복원: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
다음 단계:
{{ next_steps }}
{% endif %}

구성 요소 세부 정보 보기: {{ component_url }}
{% if incident_report_url %}사고 보고서 보기: {{ incident_report_url }}{% endif %}

문제가 계속 발생하는 경우 지원팀에 문의해 주세요.