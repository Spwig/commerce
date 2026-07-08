---
template_type: account_welcome
category: Enhanced E-commerce
---

# Email Template: account_welcome

## Subject
Chào mừng bạn đến với {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Chào mừng! 👋
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Chúng tôi rất vui được đón bạn vào cộng đồng của chúng tôi
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personalized Greeting -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Chào {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Tài khoản của bạn đã được tạo thành công. Bạn đã sẵn sàng để bắt đầu mua sắm!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          Lợi ích thành viên
        </mj-text>

        {% for benefit in shop_benefits %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 0">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px;">✓</span> {{ benefit }}
        </mj-text>
        {% endfor %}
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-button
          href="{{ browse_products_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="16px"
          font-weight="600"
          border-radius="6px"
          padding="14px 32px"
        >
          Bắt đầu mua sắm
        </mj-button>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button
          href="{{ account_url }}"
          background-color="{{ theme.color.text_muted|default:'#6b7280' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="14px"
          border-radius="6px"
          padding="12px 24px"
        >
          Quản lý tài khoản của tôi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Chào mừng! 👋

Chào {{ customer_name }},

Tài khoản của bạn đã được tạo thành công. Bạn đã sẵn sàng để bắt đầu mua sắm!

Lợi ích thành viên:
{% for benefit in shop_benefits %}
✓ {{ benefit }}
{% endfor %}

Bắt đầu mua sắm: {{ browse_products_url }}
Quản lý tài khoản: {{ account_url }}

Cần giúp đỡ?
Email: {{ support_email }}
Điện thoại: {{ support_phone }}