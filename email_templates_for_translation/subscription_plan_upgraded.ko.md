---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ 구독 플랜이 업그레이드되었습니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 플랜 업그레이드됨!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ new_plan_name }}에 오신 것을 환영합니다
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          구독 플랜이 성공적으로 업그레이드되었습니다. 이제 {{ new_plan_name }}의 모든 혜택을 누릴 수 있습니다!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              플랜 변경 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>이전 플랜:</strong> {{ old_plan_name }}<br/>
              <strong>새로운 플랜:</strong> {{ new_plan_name }}<br/>
              <strong>업그레이드 날짜:</strong> {{ upgrade_date }}<br/>
              <strong>즉시 적용</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          새롭게 추가된 기능:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          요금 정보:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>새로운 가격:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>다음 결제 날짜:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>현재 주기의 잔여 기간에 대한 일할 계산 요금:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 오늘, 현재 결제 주기의 잔여 기간에 대해 {{ prorated_charge }}의 요금이 부과되었습니다.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          구독 보기
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          질문이 있으시면? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 플랜 업그레이드됨!

{{ new_plan_name }}에 오신 것을 환영합니다

안녕하세요, {{ customer_name }}님,

구독 플랜이 성공적으로 업그레이드되었습니다. 이제 {{ new_plan_name }}의 모든 혜택을 누릴 수 있습니다!

플랜 변경 세부 정보:
- 이전 플랜: {{ old_plan_name }}
- 새로운 플랜: {{ new_plan_name }}
- 업그레이드 날짜: {{ upgrade_date }}
- 즉시 적용

새롭게 추가된 기능:
{{ new_features }}

요금 정보:
- 새로운 가격: {{ new_price }} / {{ billing_period }}
- 다음 결제 날짜: {{ next_billing_date }}
{% if prorated_charge %}- 현재 주기의 잔여 기간에 대한 일할 계산 요금: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 오늘, 현재 결제 주기의 잔여 기간에 대해 {{ prorated_charge }}의 요금이 부과되었습니다.
{% endif %}

구독 보기: {{ account_url }}
질문이 있으시면? 지원팀에 문의: {{ support_url }}