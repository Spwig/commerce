---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
이메일 주소를 확인하여 {{ blog_name }} 구독을 확인해 주세요

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          구독 확인
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ blog_name }}에 구독해 주셔서 감사합니다! 구독을 완료하고 업데이트를 받기 시작하려면 이메일 주소를 확인해 주세요.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          구독 확인
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              버튼을 클릭할 수 없으십니까? 이 링크를 브라우저에 복사하여 붙여넣으세요:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>확인이 필요한 이유</strong><br/>
          이메일 확인은 우리가 업데이트를 받고 싶은지 확인하고 스팸을 방지하는 데 도와줍니다. 귀하의 프라이버시와 이메일함은 우리에게 중요합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          구독하지 않았다면 이 이메일을 안전하게 무시할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
구독 확인

안녕하세요, {{ subscriber_name }},

{{ blog_name }}에 구독해 주셔서 감사합니다! 구독을 완료하고 업데이트를 받기 시작하려면 이메일 주소를 확인해 주세요.

구독 확인: {{ confirmation_url }}

확인이 필요한 이유
이메일 확인은 우리가 업데이트를 받고 싶은지 확인하고 스팸을 방지하는 데 도와줍니다. 귀하의 프라이버시와 이메일함은 우리에게 중요합니다.

구독하지 않았다면 이 이메일을 안전하게 무시할 수 있습니다.