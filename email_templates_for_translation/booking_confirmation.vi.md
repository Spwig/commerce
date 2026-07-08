---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
Đặt chỗ đã xác nhận - {{ product_name }} vào {{ booking_date }}

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
          Đặt chỗ đã xác nhận!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Chào {{ customer_name }}, đặt chỗ của bạn đã được xác nhận.
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
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Tổng cộng:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Đặt cọc:</strong> {{ deposit_amount }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Add to Calendar -->
    {% if ical_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=ical_url text="Add to Calendar" %}
    {% endif %}

    <!-- Manage Booking -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Cần thay đổi? Bạn có thể <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">điều chỉnh lịch</a> hoặc <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">hủy</a> đặt chỗ của bạn từ tài khoản của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Đặt chỗ đã xác nhận!

Chào {{ customer_name }}, đặt chỗ của bạn đã được xác nhận.

{{ product_name }}

Ngày: {{ booking_date }}
Thời gian: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Tài nguyên: {{ resource_name }}{% endif %}
{% if persons_display %}Khách: {{ persons_display }}{% endif %}
{% if total_cost %}Tổng cộng: {{ total_cost }}{% endif %}
{% if deposit_amount %}Đặt cọc: {{ deposit_amount }}{% endif %}

{% if ical_url %}Thêm vào lịch: {{ ical_url }}{% endif %}

Cần thay đổi? Truy cập tài khoản của bạn để điều chỉnh lịch hoặc hủy.
{{ reschedule_url }}
{{ cancel_url }}