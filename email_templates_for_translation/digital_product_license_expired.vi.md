---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
Chìa khóa cấp phép sắp hết hạn - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Chìa khóa cấp phép sắp hết hạn
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
          Chìa khóa cấp phép cho <strong>{{ product_name }}</strong> sẽ hết hạn sớm.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>Chìa khóa cấp phép:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Hết hạn:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Số ngày còn lại:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Gia hạn chìa khóa cấp phép
        </mj-text>
        <mj-text>
          Tiếp tục tận hưởng {{ product_name }} bằng cách gia hạn chìa khóa cấp phép của bạn ngay hôm nay.
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Gia hạn ngay
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Có câu hỏi về việc gia hạn? Liên hệ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Chìa khóa cấp phép sắp hết hạn

Chào {{ customer_name }},

Chìa khóa cấp phép cho {{ product_name }} sẽ hết hạn sớm.

Chi tiết chìa khóa:
• Chìa khóa cấp phép: {{ license_key }}
• Hết hạn: {{ expiration_date }}
• Số ngày còn lại: {{ days_remaining }}

Gia hạn chìa khóa cấp phép:
Tiếp tục tận hưởng {{ product_name }} bằng cách gia hạn chìa khóa cấp phép của bạn ngay hôm nay.

Gia hạn ngay: {{ renewal_url }}

Có câu hỏi về việc gia hạn? Liên hệ {{ support_email }}