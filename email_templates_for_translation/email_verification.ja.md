---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
メールアドレスを確認してください

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          メールアドレスを確認してください
        </mj-text>
        <mj-text>
          以下のボタンをクリックしてメールアドレスを確認してください。
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          メールを確認する
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          このリンクは{{ expiry_hours }}時間後に無効になります。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
メールアドレスを確認してください

以下のリンクをクリックしてメールアドレスを確認してください。

{{ verification_url }}

このリンクは{{ expiry_hours }}時間後に無効になります。