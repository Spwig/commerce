---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
驗證您的電子郵件地址

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          驗證您的電子郵件
        </mj-text>
        <mj-text>
          請點擊下方按鈕以驗證您的電子郵件地址。
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          驗證電子郵件
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          這個連結將在 {{ expiry_hours }} 小時後過期。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
驗證您的電子郵件

請點擊下方連結以驗證您的電子郵件地址。

{{ verification_url }}

這個連結將在 {{ expiry_hours }} 小時後過期。