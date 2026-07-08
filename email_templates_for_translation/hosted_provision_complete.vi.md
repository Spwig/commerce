---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Cửa hàng của bạn đã sẵn sàng - {{ store_name }}

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
          Cửa hàng của bạn đã hoạt động!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} đã sẵn sàng cho bạn
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
          Tin vui! Cửa hàng Spwig của bạn <strong>{{ store_name }}</strong> đã được thiết lập và hiện đang hoạt động. Bạn có thể bắt đầu thiết lập sản phẩm, thương hiệu và phương thức thanh toán ngay lập tức.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Chi tiết cửa hàng của bạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL cửa hàng: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Panel quản trị: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Khu vực: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bắt đầu nhanh chóng
        </mj-text>
        <mj-text font-size="14px">
          1. Đăng nhập vào panel quản trị bằng email và mật khẩu bạn đã thiết lập khi thanh toán
        </mj-text>
        <mj-text font-size="14px">
          2. Thêm logo và thương hiệu cửa hàng của bạn dưới mục Thiết kế > Cài đặt chủ đề
        </mj-text>
        <mj-text font-size="14px">
          3. Thêm sản phẩm đầu tiên của bạn dưới mục Danh mục > Sản phẩm
        </mj-text>
        <mj-text font-size="14px">
          4. Thiết lập nhà cung cấp thanh toán dưới mục Cài đặt > Nhà cung cấp thanh toán
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Đi đến Panel Quản trị" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cửa hàng của bạn đã hoạt động!

{{ store_name }} đã sẵn sàng cho bạn.

Chào {{ name|default:'there' }},

Tin vui! Cửa hàng Spwig của bạn {{ store_name }} đã được thiết lập và hiện đang hoạt động. Bạn có thể bắt đầu thiết lập sản phẩm, thương hiệu và phương thức thanh toán ngay lập tức.

Chi tiết cửa hàng của bạn:
- URL cửa hàng: {{ store_url }}
- Panel quản trị: {{ admin_url }}
- Khu vực: {{ region }}

Bắt đầu nhanh chóng:
1. Đăng nhập vào panel quản trị bằng email và mật khẩu bạn đã thiết lập khi thanh toán
2. Thêm logo và thương hiệu cửa hàng của bạn dưới mục Thiết kế > Cài đặt chủ đề
3. Thêm sản phẩm đầu tiên của bạn dưới mục Danh mục > Sản phẩm
4. Thiết lập nhà cung cấp thanh toán dưới mục Cài đặt > Nhà cung cấp thanh toán

Đi đến Panel Quản trị: {{ admin_url }}

Cần hỗ trợ? Liên hệ {{ support_email }}