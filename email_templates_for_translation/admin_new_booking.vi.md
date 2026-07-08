---
template_type: admin_new_booking
category: Bookings
---

# Email Template: admin_new_booking

## Subject
Đơn đặt mới - {{ product_name }}

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
          Đơn đặt mới đã nhận
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Một đơn đặt mới đã được đặt và cần sự chú ý của bạn.
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
          <strong>Khách hàng:</strong> {{ customer_name }} ({{ customer_email }})
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ngày:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Thời gian:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tài nguyên:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Khách:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Trạng thái:</strong> {{ status }}
        </mj-text>
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tổng cộng:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- View in Admin CTA -->
    {% if admin_booking_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_booking_url text="Xem trong Admin" %}
    {% endif %}
  </mj-body>
</mjml>

## Text Content
Đơn đặt mới đã nhận

Một đơn đặt mới đã được đặt và cần sự chú ý của bạn.

{{ product_name }}

Khách hàng: {{ customer_name }} ({{ customer_email }})
Ngày: {{ booking_date }}
Thời gian: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Tài nguyên: {{ resource_name }}{% endif %}
{% if persons_display %}Khách: {{ persons_display }}{% endif %}
Trạng thái: {{ status }}
{% if total_cost %}Tổng cộng: {{ total_cost }}{% endif %}

{% if admin_booking_url %}Xem trong Admin: {{ admin_booking_url }}{% endif %}