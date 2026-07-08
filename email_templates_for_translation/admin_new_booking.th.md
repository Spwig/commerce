---
template_type: admin_new_booking
category: Bookings
---

# Email Template: admin_new_booking

## Subject
การจองใหม่ - {{ product_name }}

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
          การจองใหม่ได้รับแล้ว
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          มีการจองใหม่ที่ถูกส่งมาแล้วและต้องการให้คุณตรวจสอบ
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
          <strong>ลูกค้า:</strong> {{ customer_name }} ({{ customer_email }})
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>วันที่:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>เวลา:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ทรัพยากร:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ผู้เข้าพัก:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>สถานะ:</strong> {{ status }}
        </mj-text>
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>รวม:</strong> {{ total_cost }}
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
การจองใหม่ได้รับแล้ว

มีการจองใหม่ที่ถูกส่งมาแล้วและต้องการให้คุณตรวจสอบ

{{ product_name }}
ลูกค้า: {{ customer_name }} ({{ customer_email }})
วันที่: {{ booking_date }}
เวลา: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}ทรัพยากร: {{ resource_name }}{% endif %}
{% if persons_display %}ผู้เข้าพัก: {{ persons_display }}{% endif %}
สถานะ: {{ status }}
{% if total_cost %}รวม: {{ total_cost }}{% endif %}

{% if admin_booking_url %}ดูใน Admin: {{ admin_booking_url }}{% endif %}