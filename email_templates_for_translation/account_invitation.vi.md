---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Tạo Tài Khoản Tại {{ site_name }}

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
          Bạn Được Mời!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tạo tài khoản tại {{ site_name }}
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
          Chúng tôi nhận thấy bạn đã mua sắm với chúng tôi dưới tư cách là khách. Tạo tài khoản đầy đủ để mở khóa các lợi ích như theo dõi đơn hàng, thanh toán nhanh hơn và các ưu đãi đặc biệt.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Lịch Sử Mua Sắm Của Bạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tổng Số Đơn Hàng: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tổng Số Tiền Chi: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Tại Sao Nên Tạo Tài Khoản?
        </mj-text>
        <mj-text font-size="14px">
          - Theo dõi đơn hàng và xem lịch sử đơn hàng
        </mj-text>
        <mj-text font-size="14px">
          - Thanh toán nhanh hơn với thông tin đã lưu
        </mj-text>
        <mj-text font-size="14px">
          - Quản lý địa chỉ và sở thích của bạn
        </mj-text>
        <mj-text font-size="14px">
          - Truy cập các ưu đãi và khuyến mãi đặc biệt
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Tạo Tài Khoản" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Liên kết này sẽ cho phép bạn thiết lập mật khẩu cho tài khoản của bạn. Lịch sử đơn hàng hiện tại của bạn sẽ được giữ nguyên.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bạn Được Mời Tạo Tài Khoản!

Chào {{ customer_name }},

Chúng tôi nhận thấy bạn đã mua sắm với chúng tôi dưới tư cách là khách. Tạo tài khoản đầy đủ để mở khóa các lợi ích như theo dõi đơn hàng, thanh toán nhanh hơn và các ưu đãi đặc biệt.

Lịch Sử Mua Sắm Của Bạn:
- Tổng Số Đơn Hàng: {{ total_orders }}
- Tổng Số Tiền Chi: {{ total_spent }}

Tại Sao Nên Tạo Tài Khoản?
- Theo dõi đơn hàng và xem lịch sử đơn hàng
- Thanh toán nhanh hơn với thông tin đã lưu
- Quản lý địa chỉ và sở thích của bạn
- Truy cập các ưu đãi và khuyến mãi đặc biệt

Tạo Tài Khoản: {{ activation_url }}

Liên kết này sẽ cho phép bạn thiết lập mật khẩu cho tài khoản của bạn. Lịch sử đơn hàng hiện tại của bạn sẽ được giữ nguyên.

Cần hỗ trợ? Liên hệ {{ support_email }}