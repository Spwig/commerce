---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 {{ referee_name }}을(를) 추천하여 보너스 포인트를 얻으셨습니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 추천 보너스 획득!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          공유해 주셔서 감사합니다, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          훌륭한 소식입니다! {{ referee_name }}이(가) 귀하의 추천을 통해 저희 충성도 프로그램에 가입했으며, 보너스 포인트를 얻으셨습니다!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              획득한 포인트
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} 포인트
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ referee_name }} 추천
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          업데이트된 잔액:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>포인트 잔액:</strong> {{ total_points }} 포인트<br/>
          <strong>추천 보너스:</strong> +{{ bonus_points }} 포인트<br/>
          <strong>추천한 친구:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              계속 공유하고 계속 획득하세요!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              친구가 가입할 때마다 {{ points_per_referral }} 포인트를 얻을 수 있습니다. 제한이 없습니다!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              추천 링크 공유
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          쇼핑 시작
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 추천 보너스 획득!

공유해 주셔서 감사합니다, {{ customer_name }}!

훌륭한 소식입니다! {{ referee_name }}이(가) 귀하의 추천을 통해 저희 충성도 프로그램에 가입했으며, 보너스 포인트를 얻으셨습니다!

획득한 포인트:
+{{ bonus_points }} 포인트
{{ referee_name }} 추천

업데이트된 잔액:
- 포인트 잔액: {{ total_points }} 포인트
- 추천 보너스: +{{ bonus_points }} 포인트
- 추천한 친구: {{ total_referrals }}

계속 공유하고 계속 획득하세요!
친구가 가입할 때마다 {{ points_per_referral }} 포인트를 얻을 수 있습니다. 제한이 없습니다!

추천 링크 공유: {{ referral_url }}
쇼핑 시작: {{ shop_url }}