---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
Phương thức thanh toán đã được cập nhật - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Phương thức thanh toán đã được cập nhật
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi there,
        </mj-text>
        <mj-text>
          Phương thức thanh toán cho gói <strong>{{ plan_name }}</strong> của bạn trên <strong>{{ store_name }}</strong> đã được cập nhật thành công.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bạn không thực hiện thay đổi này?
        </mj-text>
        <mj-text font-size="14px">
          Nếu bạn không cập nhật phương thức thanh toán, vui lòng liên hệ ngay với nhóm hỗ trợ của chúng tôi để chúng tôi có thể bảo vệ tài khoản của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Phương thức thanh toán đã được cập nhật - {{ store_name }}

Hi there,

Phương thức thanh toán cho gói {{ plan_name }} của bạn trên {{ store_name }} đã được cập nhật thành công.

Bạn không thực hiện thay đổi này?
Nếu bạn không cập nhật phương thức thanh toán, vui lòng liên hệ ngay với nhóm hỗ trợ của chúng tôi để chúng tôi có thể bảo vệ tài khoản của bạn.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}