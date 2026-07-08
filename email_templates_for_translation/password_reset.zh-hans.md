---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
密码重置请求

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          密码重置请求
        </mj-text>
        <mj-text>
          我们收到了重置您密码的请求。点击下方按钮重置密码。
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          重置密码
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          如果您没有请求此操作，可以安全地忽略此邮件。
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          此链接将在 {{ expiry_hours }} 小时后过期。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
密码重置请求

我们收到了重置您密码的请求。点击下方链接重置密码。

{{ reset_url }}

如果您没有请求此操作，可以安全地忽略此邮件。此链接将在 {{ expiry_hours }} 小时后过期。