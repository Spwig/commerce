---
template_type: booking_deposit_receipt
category: Bookings
---

# Email Template: booking_deposit_receipt

## Subject
預金を受け取りました - {{ product_name }}

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
          預金を受け取りました
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          こんにちは {{ customer_name }}、ご予約の預金が入金されました。
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
          <strong>日付:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>時間:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px">
          <strong>支払った預金:</strong> {{ deposit_amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>総費用:</strong> {{ total_cost }}
        </mj-text>
        {% if remaining_balance %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>残額:</strong> {{ remaining_balance }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
預金を受け取りました

こんにちは {{ customer_name }}、ご予約の預金が入金されました。

{{ product_name }}

日付: {{ booking_date }}
時間: {{ booking_time_start }} - {{ booking_time_end }}

支払った預金: {{ deposit_amount }}
総費用: {{ total_cost }}
{% if remaining_balance %}残額: {{ remaining_balance }}{% endif %}