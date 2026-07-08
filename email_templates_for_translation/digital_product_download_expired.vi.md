---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Liên kết tải xuống đã hết hạn - Đơn hàng #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Liên kết tải xuống đã hết hạn
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
          Liên kết tải xuống cho <strong>{{ product_name }}</strong> từ đơn hàng #{{ order_number }} đã hết hạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Liên kết tải xuống hết hạn sau {{ expiration_days }} ngày kể từ khi mua hàng vì lý do bảo mật.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Cần liên kết tải xuống mới?
        </mj-text>
        <mj-text>
          Bạn có thể yêu cầu liên kết tải xuống mới bằng cách đăng nhập vào tài khoản của bạn hoặc liên hệ với nhóm hỗ trợ của chúng tôi.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Đến Tài Khoản Của Tôi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Có câu hỏi? Liên hệ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Liên kết tải xuống đã hết hạn

Chào {{ customer_name }},

Liên kết tải xuống cho {{ product_name }} từ đơn hàng #{{ order_number }} đã hết hạn.

Liên kết tải xuống hết hạn sau {{ expiration_days }} ngày kể từ khi mua hàng vì lý do bảo mật.

Cần liên kết tải xuống mới?
Bạn có thể yêu cầu liên kết tải xuống mới bằng cách đăng nhập vào tài khoản của bạn hoặc liên hệ với nhóm hỗ trợ của chúng tôi.

Đến Tài Khoản Của Tôi: {{ account_url }}

Có câu hỏi? Liên hệ {{ support_email }}