---
template_type: admin_booking_cancelled
category: Bookings
---

# Email Template: admin_booking_cancelled

## Subject
顧客による予約のキャンセル - {{ product_name }}

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
          予約のキャンセル
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          顧客が予約をキャンセルしました。
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
          <strong>顧客:</strong> {{ customer_name }} ({{ customer_email }})
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

    <!-- View in Admin CTA -->
    {% if admin_booking_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_booking_url text="View in Admin" %}
    {% endif %}
  </mj-body>
</mjml>

## Text Content
予約のキャンセル

顧客が予約をキャンセルしました。

{{ product_name }}

顧客: {{ customer_name }} ({{ customer_email }})
日付: {{ booking_date }}
時間: {{ booking_time_start }} - {{ booking_time_end }}
{% if cancellation_reason %}理由: {{ cancellation_reason }}{% endif %}

{% if admin_booking_url %}View in Admin: {{ admin_booking_url }}{% endif %}