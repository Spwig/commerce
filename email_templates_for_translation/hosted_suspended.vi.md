---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Cửa hàng bị tạm dừng - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Tài khoản bị tạm dừng
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
          Cửa hàng của bạn <strong>{{ store_name }}</strong> đã bị tạm dừng do chưa thanh toán hóa đơn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Điều này có nghĩa là gì
        </mj-text>
        <mj-text font-size="14px">
          Cửa hàng của bạn hiện đang ở chế độ chỉ đọc -- khách hàng có thể xem nhưng không thể đặt hàng. Dữ liệu của bạn an toàn và sẽ được lưu giữ trong 30 ngày.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Để khôi phục quyền truy cập đầy đủ, vui lòng cập nhật phương thức thanh toán và thanh toán số dư còn lại.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Khôi phục cửa hàng của bạn" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Tài khoản bị tạm dừng - {{ store_name }}

Chào {{ name|default:'there' }},

Cửa hàng của bạn {{ store_name }} đã bị tạm dừng do chưa thanh toán hóa đơn.

Điều này có nghĩa là gì:
Cửa hàng của bạn hiện đang ở chế độ chỉ đọc -- khách hàng có thể xem nhưng không thể đặt hàng. Dữ liệu của bạn an toàn và sẽ được lưu giữ trong 30 ngày.

Để khôi phục quyền truy cập đầy đủ, vui lòng cập nhật phương thức thanh toán và thanh toán số dư còn lại.

Khôi phục cửa hàng của bạn: https://spwig.com/account

Cần hỗ trợ? Liên hệ {{ support_email }}