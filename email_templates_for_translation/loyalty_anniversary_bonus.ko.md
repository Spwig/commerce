---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }}년 동안 {{ shop_name }}과 함께 - 감사합니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Year{{ years_as_member|pluralize }} Together!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Today marks {{ years_as_member }} year{{ years_as_member|pluralize }} since you joined our loyalty program. Thank you for being such a valued member!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Anniversary Bonus
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Added to celebrate {{ years_as_member }} year{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your {{ years_as_member }}-Year Journey:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Your Loyalty Dashboard
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Thank you for {{ years_as_member }} amazing year{{ years_as_member|pluralize }}!<br/>
          Here's to many more 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }}년 동안 함께!

안녕하세요, {{ customer_name }}!

오늘은 당신이 충성도 프로그램에 가입한 지 {{ years_as_member }}년이 지났습니다. 귀하의 소중한 고객이 되어 주셔서 감사합니다!

생일 보너스:
{{ bonus_points }} 포인트
{{ years_as_member }}년 동안 기념하기 위해 추가되었습니다!

{{ years_as_member }}년간 여정:
- 가입일: {{ member_since }}
- 총 주문 수: {{ total_orders }}
- 쌓은 포인트: {{ lifetime_points }} 포인트
- 현재 등급: {{ loyalty_tier }}
- 총 절약 금액: {{ total_savings }}

충성도 대시보드 확인: {{ loyalty_dashboard_url }}

{{ years_as_member }}년의 훌륭한 시간 감사합니다!
앞으로도 더 많은 시간을 보내길 바랍니다 🥂