---
template_type: booking_deposit_receipt
category: Bookings
---

# Email Template: booking_deposit_receipt

## Subject
押金已收到 - {{ product_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          押金已收到
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          你好 {{ customer_name }}，我们已收到你的押金。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>日期：</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>时间：</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px">
          <strong>已支付押金：</strong> {{ deposit_amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>总费用：</strong> {{ total_cost }}
        </mj-text>
        {% if remaining_balance %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>剩余余额：</strong> {{ remaining_balance }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
押金已收到

你好 {{ customer_name }}，我们已收到你的押金。

{{ product_name }}

日期：{{ booking_date }}
时间：{{ booking_time_start }} - {{ booking_time_end }}

已支付押金：{{ deposit_amount }}
总费用：{{ total_cost }}
{% if remaining_balance %}剩余余额：{{ remaining_balance }}{% endif %}