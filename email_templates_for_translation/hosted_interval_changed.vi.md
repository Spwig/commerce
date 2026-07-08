---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Cập nhật hóa đơn - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cập nhật hóa đơn
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
          Khoảng thời gian thanh toán cho gói <strong>{{ plan_name }}</strong> của bạn trên <strong>{{ store_name }}</strong> đã được cập nhật.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Chi tiết thanh toán
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Gói: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Khoảng thời gian thanh toán trước: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Khoảng thời gian thanh toán mới: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ngày thanh toán tiếp theo: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Gói đăng ký của bạn vẫn đang hoạt động. Bạn có thể quản lý các tùy chọn thanh toán bất kỳ lúc nào từ tài khoản của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Manage Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cập nhật hóa đơn - {{ store_name }}

Hi there,

Khoảng thời gian thanh toán cho gói {{ plan_name }} trên {{ store_name }} đã được cập nhật.

Chi tiết thanh toán:
- Gói: {{ plan_name }}
- Khoảng thời gian thanh toán trước: {{ old_interval }}
- Khoảng thời gian thanh toán mới: {{ new_interval }}
- Ngày thanh toán tiếp theo: {{ next_billing_date }}

Gói đăng ký của bạn vẫn đang hoạt động. Bạn có thể quản lý các tùy chọn thanh toán bất kỳ lúc nào từ tài khoản của bạn.

Quản lý gói đăng ký: https://spwig.com/account

Cần hỗ trợ? Liên hệ {{ support_email }}