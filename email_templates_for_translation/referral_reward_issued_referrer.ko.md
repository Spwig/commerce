---
template_type: referral_reward_issued_referrer
category: Referral Program
---

# Email Template: referral_reward_issued_referrer

## Subject
당신은 {{ reward_amount }} 보상이 지급되었습니다!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 보상이 지급되었습니다!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referee_name }}을(를) 추천해 주셔서 감사합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 당신의 보상
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          만료일: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요, {{ customer_name }}!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          축하합니다! {{ referee_name }}이(가) 당신의 추천 링크를 통해 처음으로 구매를 하셨고, 당신은 {{ reward_amount }} 보상을 받으셨습니다!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          추천 링크를 계속 공유하여 더 많은 보상을 얻으세요. 추천하는 친구가 많을수록 더 많이 얻을 수 있습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Referral Stats -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          당신의 추천 통계
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-group>
        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" line-height="1">
            {{ total_referrals }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            성공적인 추천
          </mj-text>
        </mj-column>

        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center" line-height="1">
            {{ total_rewards_earned }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            총 보상
          </mj-text>
        </mj-column>
      </mj-group>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          추천 목록 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          계속 공유하고 계속 얻으세요!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background|default:'#ffffff' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          친구들과 이 링크를 공유하여 더 많은 보상을 얻으세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          문의사항이 있으시면 <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">고객 지원팀에 문의해 주세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
당신은 {{ reward_amount }} 보상이 지급되었습니다!

안녕하세요, {{ customer_name }}!

축하합니다! {{ referee_name }}이(가) 당신의 추천 링크를 통해 처음으로 구매를 하셨고, 당신은 {{ reward_amount }} 보상을 받으셨습니다!

보상: {{ reward_amount }}
유형: {{ reward_type_display }}
{% if expires_at %}만료일: {{ expires_at }}{% endif %}

당신의 추천 통계:
- 성공적인 추천: {{ total_referrals }}
- 총 보상: {{ total_rewards_earned }}

추천 링크를 계속 공유하여 더 많은 보상을 얻으세요:
{{ referral_link }}

추천 목록 보기: {{ referral_dashboard_url }}

{{ shop_name }}
문의사항이 있으시면 {{ support_email }}에 문의해 주세요