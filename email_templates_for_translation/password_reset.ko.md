---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
비밀번호 재설정 요청

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          비밀번호 재설정 요청
        </mj-text>
        <mj-text>
          비밀번호 재설정 요청을 받았습니다. 아래의 버튼을 클릭하여 비밀번호를 재설정하세요.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          비밀번호 재설정
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          이 요청을 하지 않았다면 이 이메일을 무시해도 안전합니다.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          이 링크는 {{ expiry_hours }} 시간 내에 만료됩니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
비밀번호 재설정 요청

비밀번호 재설정 요청을 받았습니다. 아래의 링크를 클릭하여 비밀번호를 재설정하세요.

{{ reset_url }}

이 요청을 하지 않았다면 이 이메일을 무시해도 안전합니다.
이 링크는 {{ expiry_hours }} 시간 내에 만료됩니다.