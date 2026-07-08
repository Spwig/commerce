---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Chào lại! {{ store_name }} đã hoạt động trở lại

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
          Chào lại!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} đã hoạt động trở lại
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào bạn,
        </mj-text>
        <mj-text>
          Tin vui! Cửa hàng <strong>{{ store_name }}</strong> của bạn đã được kích hoạt lại. Gói đăng ký <strong>{{ plan_name }}</strong> của bạn hiện đang hoạt động và cửa hàng của bạn sẽ trở lại trực tuyến.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Chi tiết kích hoạt lại
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Gói: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số tiền đã thanh toán: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ngày thanh toán tiếp theo: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Cửa hàng của bạn đang trở lại trực tuyến. Có thể mất vài phút để mọi thứ được khôi phục hoàn toàn. Khi hoạt động, cửa hàng của bạn sẽ có thể truy cập tại {{ store_url }}.
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
Chào lại! {{ store_name }} đã hoạt động trở lại

Chào bạn,

Tin vui! Cửa hàng {{ store_name }} của bạn đã được kích hoạt lại. Gói đăng ký {{ plan_name }} của bạn hiện đang hoạt động và cửa hàng của bạn sẽ trở lại trực tuyến.

Chi tiết kích hoạt lại:
- Gói: {{ plan_name }}
- Số tiền đã thanh toán: {{ currency }}{{ amount }}
- Ngày thanh toán tiếp theo: {{ next_billing_date }}

Cửa hàng của bạn đang trở lại trực tuyến. Có thể mất vài phút để mọi thứ được khôi phục hoàn toàn. Khi hoạt động, cửa hàng của bạn sẽ có thể truy cập tại {{ store_url }}.

Đi đến cửa hàng của bạn: {{ admin_url }}

Cần hỗ trợ? Liên hệ {{ support_email }}