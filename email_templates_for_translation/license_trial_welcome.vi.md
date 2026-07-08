---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Chào mừng bạn đến với Spwig - Thử nghiệm miễn phí {{ trial_days }} ngày của bạn

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Chào mừng bạn đến với Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Thử nghiệm miễn phí {{ trial_days }} ngày của bạn đã sẵn sàng
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
          Cảm ơn bạn đã thử nghiệm <strong>{{ product_name }}</strong>! Thử nghiệm của bạn đã được kích hoạt và bạn có <strong>{{ trial_days }} ngày</strong> để khám phá mọi thứ mà Spwig có thể cung cấp{% if includes_pos %}, bao gồm hệ thống Bán hàng tại chỗ (POS) của chúng tôi{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          TOKEN CẤP CÔNG THỨC CỦA BẠN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Sử dụng token này trong quá trình cài đặt để kích hoạt cửa hàng thử nghiệm của bạn
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
          1. Theo dõi hướng dẫn cài đặt của chúng tôi để cài đặt Spwig trên máy chủ của bạn
        </mj-text>
        <mj-text font-size="14px">
          2. Nhập token cài đặt của bạn khi được yêu cầu trong quá trình cài đặt
        </mj-text>
        <mj-text font-size="14px">
          3. Bắt đầu xây dựng cửa hàng trực tuyến của bạn!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Những gì được bao gồm trong thử nghiệm của bạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Truy cập đầy đủ vào tất cả các tính năng cốt lõi trong {{ trial_days }} ngày
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Danh mục sản phẩm, đơn hàng và quản lý khách hàng
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tùy chỉnh giao diện và công cụ xây dựng trang
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tích hợp nhà cung cấp thanh toán và vận chuyển
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Hệ thống Bán hàng tại chỗ (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Thử nghiệm của bạn sẽ hết hạn sau {{ trial_days }} ngày. Khi bạn sẵn sàng, nâng cấp lên giấy phép đầy đủ để tiếp tục vận hành cửa hàng của bạn mà không có bất kỳ tổn thất dữ liệu nào.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Chào mừng bạn đến với Spwig!
Thử nghiệm miễn phí {{ trial_days }} ngày của bạn đã sẵn sàng.

Chào {{ customer_name }},

Cảm ơn bạn đã thử nghiệm {{ product_name }}! Thử nghiệm của bạn đã được kích hoạt và bạn có {{ trial_days }} ngày để khám phá mọi thứ mà Spwig có thể cung cấp{% if includes_pos %}, bao gồm hệ thống Bán hàng tại chỗ (POS) của chúng tôi{% endif %}.

TOKEN CẤP CÔNG THỨC CỦA BẠN:
{{ setup_token }}
Sử dụng token này trong quá trình cài đặt để kích hoạt cửa hàng thử nghiệm của bạn.

Bắt đầu sử dụng:
1. Theo dõi hướng dẫn cài đặt của chúng tôi để cài đặt Spwig trên máy chủ của bạn
2. Nhập token cài đặt của bạn khi được yêu cầu trong quá trình cài đặt
3. Bắt đầu xây dựng cửa hàng trực tuyến của bạn!

Xem Hướng dẫn Cài đặt: {{ setup_url }}

Những gì được bao gồm trong thử nghiệm của bạn:
- Truy cập đầy đủ vào tất cả các tính năng cốt lõi trong {{ trial_days }} ngày
- Danh mục sản phẩm, đơn hàng và quản lý khách hàng
- Tùy chỉnh giao diện và công cụ xây dựng trang
- Tích hợp nhà cung cấp thanh toán và vận chuyển
{% if includes_pos %}- Hệ thống Bán hàng tại chỗ (POS){% endif %}

Thử nghiệm của bạn sẽ hết hạn sau {{ trial_days }} ngày. Khi bạn sẵn sàng, nâng cấp lên giấy phép đầy đủ để tiếp tục vận hành cửa hàng của bạn mà không có bất kỳ tổn thất dữ liệu nào.

Cần hỗ trợ? Liên hệ {{ support_email }}