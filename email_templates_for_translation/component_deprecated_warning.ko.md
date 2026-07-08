---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ {{ component_name }}은 {{ deprecation_date }}에 사용이 중단될 예정입니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 사용 중단 공지
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          사용 중단 예정 구성 요소
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }}은 사용 중단될 예정이며, 더 이상 권장되지 않습니다. 대체 솔루션으로 마이그레이션하는 것을 계획하세요.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              사용 중단 일정:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>구성 요소:</strong> {{ component_name }}<br/>
              <strong>현재 버전:</strong> {{ current_version }}<br/>
              <strong>사용 중단일:</strong> {{ deprecation_date }}<br/>
              <strong>지원 종료일:</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          사용 중단의 이유:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          이 의미하는 바는:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 구성 요소는 {{ end_of_support_date }}까지 계속 작동할 예정입니다<br/>
          • 새로운 기능은 추가되지 않을 예정입니다<br/>
          • 지원 종료일까지 보안 업데이트가 제공될 예정입니다<br/>
          • {{ end_of_support_date }} 이후 구성 요소는 더 이상 업데이트를 받지 못할 예정입니다
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 대체 구성 요소:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">마이그레이션 가이드 보기</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          대체 구성 요소 보기
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          지원 담당자 연락
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 사용 중단 공지

사용 중단 예정 구성 요소

{{ component_name }}은 사용 중단될 예정이며, 더 이상 권장되지 않습니다. 대체 솔루션으로 마이그레이션하는 것을 계획하세요.

사용 중단 일정:
- 구성 요소: {{ component_name }}
- 현재 버전: {{ current_version }}
- 사용 중단일: {{ deprecation_date }}
- 지원 종료일: {{ end_of_support_date }}

사용 중단의 이유:
{{ deprecation_reason }}

이 의미하는 바는:
• 구성 요소는 {{ end_of_support_date }}까지 계속 작동할 예정입니다
• 새로운 기능은 추가되지 않을 예정입니다
• 지원 종료일까지 보안 업데이트가 제공될 예정입니다
• {{ end_of_support_date }} 이후 구성 요소는 더 이상 업데이트를 받지 못할 예정입니다

{% if recommended_alternative %}권장 대체 구성 요소:
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}마이그레이션 가이드 보기: {{ migration_guide }}{% endif %}
{% if alternative_url %}대체 구성 요소 보기: {{ alternative_url }}{% endif %}
지원 담당자 연락: {{ support_url }}