---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Đăng ký thành công - {{ store_name }}

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
          Đăng ký thành công!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Chào mừng bạn đến với Spwig
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
          Cảm ơn bạn đã đăng ký! Kế hoạch <strong>{{ plan_name }}</strong> của bạn cho <strong>{{ store_name }}</strong> đã được xác nhận.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Chi tiết kế hoạch
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Kế hoạch: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Khoảng thời gian thanh toán: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số tiền: {{ currency }}{{ amount }}{% if intro_period %} (giá khởi đầu){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Giá khởi đầu của bạn áp dụng trong {{ intro_period }}. Sau đó, kế hoạch của bạn sẽ được gia hạn với giá {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Cửa hàng của bạn đang được thiết lập và bạn sẽ nhận được một email khác khi sẵn sàng.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Ngày thanh toán tiếp theo: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Đăng ký thành công!

Chào {{ name|default:'there' }},

Cảm ơn bạn đã đăng ký! Kế hoạch {{ plan_name }} của bạn cho {{ store_name }} đã được xác nhận.

Chi tiết kế hoạch:
- Kế hoạch: {{ plan_name }}
- Khoảng thời gian thanh toán: {{ billing_interval }}
- Số tiền: {{ currency }}{{ amount }}{% if intro_period %} (giá khởi đầu){% endif %}
{% if intro_period %}
Đây là giá khởi đầu của bạn trong {{ intro_period }}. Sau đó, kế hoạch của bạn sẽ được gia hạn với giá {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Cửa hàng của bạn đang được thiết lập và bạn sẽ nhận được một email khác khi sẵn sàng.

Ngày thanh toán tiếp theo: {{ next_billing_date }}

Cần hỗ trợ? Liên hệ {{ support_email }}