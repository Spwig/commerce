---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
{{ store_name }} 구독 확인 요청

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          구독 확인
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ store_name }} 소식에 관심을 가져주셔서 감사합니다! 업데이트와 혜택을 받으려면 이메일 주소를 확인해 주세요.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          구독 확인
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              버튼을 클릭할 수 없나요? 브라우저에 이 링크를 복사하여 붙여넣으세요:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>왜 확인해야 하나요?</strong><br/>
          이메일을 확인하면 업데이트를 원하시는 분인지 확인하고, 스팸 메일을 방지할 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          가입하지 않으셨다면, 이 이메일을 무시하셔도 됩니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ store_name }} 구독 확인 요청

{{ store_name }} 소식에 관심을 가져주셔서 감사합니다! 업데이트와 혜택을 받으려면 이메일 주소를 확인해 주세요:

{{ confirmation_url }}

이메일을 확인하면 업데이트를 원하시는 분인지 확인하고, 스팸 메일을 방지할 수 있습니다.

가입하지 않으셨다면, 이 이메일을 무시하셔도 됩니다.