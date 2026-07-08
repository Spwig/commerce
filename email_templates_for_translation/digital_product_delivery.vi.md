---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Sản phẩm số của bạn đã sẵn sàng - Đơn hàng #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Sản phẩm số của bạn đã sẵn sàng!
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
          Cảm ơn bạn đã mua hàng! Sản phẩm số của bạn hiện đã sẵn sàng để tải về.
        </mj-text>
        <mj-text font-weight="bold">
          Đơn hàng #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Phiên bản: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Kích thước tệp: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Tải xuống ngay
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Thông tin quan trọng:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Bạn có thể tải xuống sản phẩm này {{ download_limit }} lần
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Liên kết tải xuống sẽ hết hạn sau {{ expiration_days }} ngày
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Hãy giữ email này để tham khảo sau này
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Cần hỗ trợ? Liên hệ với nhóm hỗ trợ của chúng tôi tại {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sản phẩm số của bạn đã sẵn sàng!

Chào {{ customer_name }},

Cảm ơn bạn đã mua hàng! Sản phẩm số của bạn hiện đã sẵn sàng để tải về.

Đơn hàng #{{ order_number }}

Sản phẩm: {{ product_name }}
Phiên bản: {{ product_version }}
Kích thước tệp: {{ file_size }}

Tải sản phẩm của bạn tại đây:
{{ download_url }}

Thông tin quan trọng:
{% if download_limit %}• Bạn có thể tải xuống sản phẩm này {{ download_limit }} lần
{% endif %}{% if expiration_days %}• Liên kết tải xuống sẽ hết hạn sau {{ expiration_days }} ngày
{% endif %}• Hãy giữ email này để tham khảo sau này

Cần hỗ trợ? Liên hệ với nhóm hỗ trợ của chúng tôi tại {{ support_email }}