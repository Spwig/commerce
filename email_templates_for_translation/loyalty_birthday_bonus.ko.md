---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 {{ customer_name }}님의 생일 축하! {{ shop_name }}에서 특별한 선물이 있어요

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Happy Birthday!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Happy Birthday, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          To celebrate your special day, we've added {{ bonus_points }} bonus points to your loyalty account!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Your Birthday Gift
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Added to your account!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Loyalty Account:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points Balance:</strong> {{ total_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Birthday Bonus:</strong> +{{ bonus_points }} points
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Start Shopping & Use Your Points
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Have an amazing birthday! 🎉<br/>
          - The {{ shop_name }} Team
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 HAPPY BIRTHDAY!

{{ customer_name }}님 생일 축하합니다!

{{ customer_name }}님의 특별한 날을 기념하여 충성도 계정에 {{ bonus_points }} 포인트를 추가했습니다!

생일 선물:
{{ bonus_points }} 포인트
계정에 추가됨!

충성도 계정:
- 포인트 잔액: {{ total_points }} 포인트
- 현재 등급: {{ loyalty_tier }}
- 생일 보너스: +{{ bonus_points }} 포인트

포인트 사용하여 쇼핑 시작: {{ shop_url }}

기념할 만한 생일 보내세요! 🎉
- {{ shop_name }} 팀