---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 당신의 친구 {{ referee_name }}이 방금 가입했습니다!

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
          🎉 추천 성공!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ referee_name }} 가입!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          당신의 추천이 이제 회원이 되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          기쁜 소식입니다! {{ referee_name }}이 당신의 추천 링크를 사용하여 방금 가입했습니다.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          그들이 첫 구매를 하면, 당신과 모두 보상이 자동으로 지급됩니다! 그 일이 발생할 때 다시 이메일을 보내드릴 예정입니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          다음으로 무엇이 일어날까요?
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }}이 첫 구매를 합니다<br/>
          2. 당신과 모두 보상이 자동으로 지급됩니다<br/>
          3. 미래의 구매에 보상을 사용할 수 있습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          더 많이 벌기 위해 계속 공유하세요!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
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
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          내 추천 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 당신의 친구 {{ referee_name }}이 방금 가입했습니다!

안녕하세요 {{ customer_name }},

기쁜 소식입니다! {{ referee_name }}이 당신의 추천 링크를 사용하여 방금 가입했습니다.

그들이 첫 구매를 하면, 당신과 모두 보상이 자동으로 지급됩니다! 그 일이 발생할 때 다시 이메일을 보내드릴 예정입니다.

다음으로 무엇이 일어날까요?
1. {{ referee_name }}이 첫 구매를 합니다
2. 당신과 모두 보상이 자동으로 지급됩니다
3. 미래의 구매에 보상을 사용할 수 있습니다

더 많이 벌기 위해 계속 공유하세요:
{{ referral_link }}

추천 보기: {{ referral_dashboard_url }}

{{ shop_name }}