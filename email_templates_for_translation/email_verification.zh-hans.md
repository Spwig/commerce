---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
验证您的电子邮件地址

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          验证您的电子邮件
        </mj-text>
        <mj-text>
          请通过点击下方按钮来验证您的电子邮件地址。
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          验证电子邮件
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          此链接将在 {{ expiry_hours }} 小时后过期。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
验证您的电子邮件

请通过点击下方链接来验证您的电子邮件地址。

{{ verification_url }}

此链接将在 {{ expiry_hours }} 小时后过期。