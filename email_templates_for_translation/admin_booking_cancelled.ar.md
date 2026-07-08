---
template_type: admin_booking_cancelled
category: Bookings
---

# Email Template: admin_booking_cancelled

## Subject
الغاء الحجز من قبل العميل - {{ product_name }}

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
          الغاء الحجز
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          قام عميل بยกالغاء حجزه.
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
          <strong>العميل:</strong> {{ customer_name }} ({{ customer_email }})
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>التاريخ:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>الوقت:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        {% if cancellation_reason %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>السبب:</strong> {{ cancellation_reason }}
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
الغاء الحجز

قام عميل بยกالغاء حجزه.

{{ product_name }}

العميل: {{ customer_name }} ({{ customer_email }})
التاريخ: {{ booking_date }}
الوقت: {{ booking_time_start }} - {{ booking_time_end }}
{% if cancellation_reason %}السبب: {{ cancellation_reason }}{% endif %}

{% if admin_booking_url %}View in Admin: {{ admin_booking_url }}{% endif %}