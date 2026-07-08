---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Khóa giấy phép phần mềm của bạn - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Khóa giấy phép của bạn đã sẵn sàng
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào {{ customer_name }},
        </mj-text>
        <mj-text>
          Cảm ơn bạn đã mua {{ product_name }}! Dưới đây là khóa giấy phép của bạn để kích hoạt.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          KHÓA GIẤY PHÉP CỦA BẠN
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Nhấp để sao chép hoặc ghi lại cẩn thận
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Chi tiết giấy phép:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Sản phẩm: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Phiên bản: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Loại giấy phép: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Số lần kích hoạt tối đa: {{ max_activations }} thiết bị
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Hạn sử dụng: Giấy phép trọn đời
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Hết hạn vào: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Cách kích hoạt:
        </mj-text>
        <mj-text font-size="14px">
          1. Tải xuống và cài đặt phần mềm
        </mj-text>
        <mj-text font-size="14px">
          2. Mở ứng dụng
        </mj-text>
        <mj-text font-size="14px">
          3. Nhập khóa giấy phép khi được yêu cầu
        </mj-text>
        <mj-text font-size="14px">
          4. Nhấp vào "Kích hoạt" để hoàn tất quy trình
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Tải xuống phần mềm
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Quan trọng:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Hãy giữ email này an toàn - bạn sẽ cần khóa giấy phép để cài đặt lại
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Đừng chia sẻ khóa giấy phép với người khác
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Bạn có thể hủy kích hoạt thiết bị từ bảng điều khiển tài khoản của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Cần hỗ trợ kích hoạt? Liên hệ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Khóa giấy phép của bạn đã sẵn sàng

Chào {{ customer_name }},

Cảm ơn bạn đã mua {{ product_name }}! Dưới đây là khóa giấy phép của bạn để kích hoạt.

KHÓA GIẤY PHÉP CỦA BẠN:
{{ license_key }}

Chi tiết giấy phép:
• Sản phẩm: {{ product_name }}
• Phiên bản: {{ product_version }}
• Loại giấy phép: {{ license_type }}
• Số lần kích hoạt tối đa: {{ max_activations }} thiết bị
{% if is_lifetime %}• Hạn sử dụng: Giấy phép trọn đời{% else %}• Hết hạn vào: {{ expiration_date }}{% endif %}

Cách kích hoạt:
1. Tải xuống và cài đặt phần mềm
2. Mở ứng dụng
3. Nhập khóa giấy phép khi được yêu cầu
4. Nhấp vào "Kích hoạt" để hoàn tất quy trình

{% if download_url %}Tải xuống phần mềm: {{ download_url }}

{% endif %}QUAN TRỌNG:
• Hãy giữ email này an toàn - bạn sẽ cần khóa giấy phép để cài đặt lại
• Đừng chia sẻ khóa giấy phép với người khác
• Bạn có thể hủy kích hoạt thiết bị từ bảng điều khiển tài khoản của bạn

Cần hỗ trợ kích hoạt? Liên hệ {{ support_email }}