---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ {{ current_tier }} 등급 상태가 곧 만료됩니다 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 등급 상태 만료 예정
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          등급 상태를 잃지 마세요!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ expiry_date }} 이전에 활동 수준을 유지하지 않으면 {{ current_tier }} 등급 상태가 만료됩니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              현재 상태:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>현재 등급:</strong> {{ current_tier }}<br/>
              <strong>만료일:</strong> {{ expiry_date }} ({{ days_remaining }} 일)<br/>
              <strong>다음 등급:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ current_tier }} 등급 상태를 유지하는 방법:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ expiry_date }} 이전에 {{ requirement_type }}을 수행해야 합니다:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              현재: {{ current_progress }} | 필요: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          잃게 될 혜택:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          지금 쇼핑하고 상태 유지
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ shop_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          상세 정보 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 등급 상태 만료 예정

등급 상태를 잃지 마세요!

안녕하세요 {{ customer_name }},

{{ expiry_date }} 이전에 활동 수준을 유지하지 않으면 {{ current_tier }} 등급 상태가 만료됩니다.

현재 상태:
- 현재 등급: {{ current_tier }}
- 만료일: {{ expiry_date }} ({{ days_remaining }} 일)
- 다음 등급: {{ next_tier }}

{{ current_tier }} 등급 상태를 유지하는 방법:
{{ expiry_date }} 이전에 {{ requirement_type }}을 수행해야 합니다:

{{ requirement_description }}
현재: {{ current_progress }} | 필요: {{ required_amount }}

잃게 될 혜택:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

쇼핑하고 상태 유지: {{ shop_url }}
상세 정보 보기: {{ loyalty_dashboard_url }}