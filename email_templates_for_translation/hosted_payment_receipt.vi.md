---
template_type: hosted_payment_receipt
category: License
---

# Email Template: hosted_payment_receipt

## Subject
Phiếu thanh toán - {{ store_name }}

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
          Phiếu thanh toán
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
          Chào {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Thanh toán của bạn đã được xác nhận. Dưới đây là chi tiết để bạn lưu lại.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Receipt Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Chi tiết phiếu thanh toán
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số tiền: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Gói: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Khoảng thời gian: {{ period_start }} - {{ period_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ngày thanh toán tiếp theo: {{ next_billing_date }}
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
Phiếu thanh toán - {{ store_name }}

Chào {{ name|default:'there' }},

Thanh toán của bạn đã được xác nhận. Dưới đây là chi tiết để bạn lưu lại.

Chi tiết phiếu thanh toán:
- Số tiền: {{ currency }}{{ amount }}
- Gói: {{ plan_name }}
- Khoảng thời gian: {{ period_start }} - {{ period_end }}
- Ngày thanh toán tiếp theo: {{ next_billing_date }}

Đi đến Cửa hàng của bạn: {{ admin_url }}

Cần hỗ trợ? Liên hệ {{ support_email }}