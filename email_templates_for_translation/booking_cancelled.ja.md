---
template_type: booking_cancelled
category: Bookings
---

# Email Template: booking_cancelled

## Subject
予約がキャンセルされました - {{ product_name }}

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
          予約がキャンセルされました
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          こんにちは {{ customer_name }}、あなたの予約がキャンセルされました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Details -->
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
        {% if cancellation_reason %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>理由:</strong> {{ cancellation_reason }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Rebook CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          再度予約したい場合は、弊社のウェブサイトをご覧ください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
予約がキャンセルされました

こんにちは {{ customer_name }}、あなたの予約がキャンセルされました。

{{ product_name }}

日付: {{ booking_date }}
時間: {{ booking_time_start }} - {{ booking_time_end }}
{% if cancellation_reason %}理由: {{ cancellation_reason }}{% endif %}

再度予約したい場合は、弊社のウェブサイトをご覧ください。