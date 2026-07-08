---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Yêu cầu đặt lại mật khẩu

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Yêu cầu đặt lại mật khẩu
        </mj-text>
        <mj-text>
          Chúng tôi đã nhận được yêu cầu đặt lại mật khẩu của bạn. Nhấn vào nút bên dưới để đặt lại.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Đặt lại mật khẩu
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Nếu bạn không yêu cầu điều này, bạn có thể an toàn bỏ qua email này.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Liên kết này sẽ hết hạn sau {{ expiry_hours }} giờ.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Yêu cầu đặt lại mật khẩu

Chúng tôi đã nhận được yêu cầu đặt lại mật khẩu của bạn. Nhấn vào liên kết bên dưới để đặt lại.

{{ reset_url }}

Nếu bạn không yêu cầu điều này, bạn có thể an toàn bỏ qua email này.
Liên kết này sẽ hết hạn sau {{ expiry_hours }} giờ.