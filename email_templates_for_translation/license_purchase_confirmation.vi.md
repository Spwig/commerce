---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Giấy phép Spwig của bạn - Đơn hàng #{{ order_number }}

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
          Cảm ơn bạn đã mua hàng!
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
          Việc mua hàng của bạn <strong>{{ product_name }}</strong> đã hoàn tất. Dưới đây là khóa giấy phép và mã cài đặt để bạn bắt đầu.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Tổng quan đơn hàng
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sản phẩm: {{ product_name }}{% if includes_pos %} (bao gồm POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số tiền: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Số đơn hàng: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          KHÓA GIẤY PHÉP CỦA BẠN
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Lưu lại khóa này - bạn sẽ cần nó để cài đặt lại
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          MÃ CÀI ĐẶT CỦA BẠN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Sử dụng mã này trong quá trình cài đặt để kích hoạt cửa hàng của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bắt đầu sử dụng
        </mj-text>
        <mj-text font-size="14px">
          1. Làm theo hướng dẫn cài đặt của chúng tôi để cài đặt Spwig trên máy chủ của bạn
        </mj-text>
        <mj-text font-size="14px">
          2. Nhập mã cài đặt của bạn khi được yêu cầu trong quá trình cài đặt
        </mj-text>
        <mj-text font-size="14px">
          3. Cửa hàng của bạn sẽ được kích hoạt tự động
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Tạo tài khoản của bạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Thiết lập mật khẩu để quản lý giấy phép của bạn, truy cập tải xuống và nhận các bản cập nhật.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Quan trọng:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Hãy giữ email này an toàn - nó chứa khóa giấy phép và mã cài đặt của bạn để tham khảo trong tương lai. Đừng chia sẻ các thông tin này với người khác.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cảm ơn bạn đã mua hàng!

Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Việc mua hàng của bạn {{ product_name }} đã hoàn tất. Dưới đây là khóa giấy phép và mã cài đặt để bạn bắt đầu.

Tổng quan đơn hàng:
- Sản phẩm: {{ product_name }}{% if includes_pos %} (bao gồm POS){% endif %}
- Số tiền: {{ price }}
- Số đơn hàng: {{ order_number }}

KHÓA GIẤY PHÉP CỦA BẠN:
{{ license_key }}
Lưu lại khóa này - bạn sẽ cần nó để cài đặt lại.

MÃ CÀI ĐẶT CỦA BẠN:
{{ setup_token }}
Sử dụng mã này trong quá trình cài đặt để kích hoạt cửa hàng của bạn.

Bắt đầu sử dụng:
1. Làm theo hướng dẫn cài đặt của chúng tôi để cài đặt Spwig trên máy chủ của bạn
2. Nhập mã cài đặt của bạn khi được yêu cầu trong quá trình cài đặt
3. Cửa hàng của bạn sẽ được kích hoạt tự động

Xem hướng dẫn cài đặt: {{ setup_url }}
{% if activation_url %}
Tạo tài khoản của bạn:
Thiết lập mật khẩu để quản lý giấy phép của bạn, truy cập tải xuống và nhận các bản cập nhật.
{{ activation_url }}
{% endif %}
QUAN TRỌNG:
Hãy giữ email này an toàn - nó chứa khóa giấy phép và mã cài đặt của bạn để tham khảo trong tương lai. Đừng chia sẻ các thông tin này với người khác.

Cần hỗ trợ? Liên hệ {{ support_email }}