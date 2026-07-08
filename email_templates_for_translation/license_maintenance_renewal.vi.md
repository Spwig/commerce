---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Bảo trì được gia hạn - Đơn hàng #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bảo trì được gia hạn!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Đơn hàng #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào {{ customer_name }},
        </mj-text>
        <mj-text>
          Gói bảo trì Spwig của bạn đã được gia hạn thành công. Bạn sẽ tiếp tục nhận được các bản cập nhật nền tảng, vá lỗi bảo mật và tính năng mới.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Tổng quan gia hạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          License Key: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bảo trì còn hiệu lực đến: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số đơn hàng: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Những gì được bao gồm
        </mj-text>
        <mj-text font-size="14px">
          Gói bảo trì đang hoạt động của bạn cho phép bạn truy cập:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Cập nhật và cải tiến tính năng nền tảng
        </mj-text>
        <mj-text font-size="14px">
          - Vá lỗi bảo mật và sửa lỗi
        </mj-text>
        <mj-text font-size="14px">
          - Phát hành thành phần mới qua máy chủ nâng cấp
        </mj-text>
        <mj-text font-size="14px">
          - Hỗ trợ kỹ thuật
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Không cần hành động từ phía bạn. Các bản cập nhật sẽ tiếp tục được cung cấp thông qua hệ thống cập nhật thành phần trong bảng điều khiển quản trị của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bảo trì được gia hạn!

Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Gói bảo trì Spwig của bạn đã được gia hạn thành công. Bạn sẽ tiếp tục nhận được các bản cập nhật nền tảng, vá lỗi bảo mật và tính năng mới.

Tổng quan gia hạn:
- License Key: {{ license_key }}
- Bảo trì còn hiệu lực đến: {{ renewal_expires_at }}
- Số đơn hàng: {{ order_number }}

Những gì được bao gồm:
- Cập nhật và cải tiến tính năng nền tảng
- Vá lỗi bảo mật và sửa lỗi
- Phát hành thành phần mới qua máy chủ nâng cấp
- Hỗ trợ kỹ thuật

Không cần hành động từ phía bạn. Các bản cập nhật sẽ tiếp tục được cung cấp thông qua hệ thống cập nhật thành phần trong bảng điều khiển quản trị của bạn.

Cần hỗ trợ? Liên hệ {{ support_email }}