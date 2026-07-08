---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
이메일 주소 확인

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          이메일 확인
        </mj-text>
        <mj-text>
          아래의 버튼을 클릭하여 이메일 주소를 확인해 주세요.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          이메일 확인
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          이 링크는 {{ expiry_hours }} 시간 뒤에 만료됩니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
이메일 확인

아래의 링크를 클릭하여 이메일 주소를 확인해 주세요.

{{ verification_url }}

이 링크는 {{ expiry_hours }} 시간 뒤에 만료됩니다.