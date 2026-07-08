---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Xác nhận địa chỉ email của bạn

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Xác nhận email
        </mj-text>
        <mj-text>
          Vui lòng xác nhận địa chỉ email của bạn bằng cách nhấp vào nút bên dưới.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Xác nhận email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Liên kết này sẽ hết hạn sau {{ expiry_hours }} giờ.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Xác nhận email

Vui lòng xác nhận địa chỉ email của bạn bằng cách nhấp vào liên kết bên dưới.

{{ verification_url }}

Liên kết này sẽ hết hạn sau {{ expiry_hours }} giờ.