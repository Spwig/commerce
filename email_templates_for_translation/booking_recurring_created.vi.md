---
template_type: booking_recurring_created
category: Bookings
---

# Email Template: booking_recurring_created

## Subject
Chuỗi đặt chỗ định kỳ đã được tạo - {{ product_name }}

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
          Chuỗi đặt chỗ định kỳ đã được tạo
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Chào {{ customer_name }}, chuỗi đặt chỗ định kỳ của bạn đã được thiết lập.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Series Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        {% if recurrence_description %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Lịch trình:</strong> {{ recurrence_description }}
        </mj-text>
        {% endif %}
        {% if first_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Lần đặt chỗ đầu tiên:</strong> {{ first_date }}
        </mj-text>
        {% endif %}
        {% if total_bookings %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tổng số đặt chỗ:</strong> {{ total_bookings }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tài nguyên:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Chi phí mỗi lần đặt chỗ:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Manage -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bạn có thể quản lý các lần đặt chỗ riêng lẻ trong chuỗi này từ tài khoản của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Chuỗi đặt chỗ định kỳ đã được tạo

Chào {{ customer_name }}, chuỗi đặt chỗ định kỳ của bạn đã được thiết lập.

{{ product_name }}

{% if recurrence_description %}Lịch trình: {{ recurrence_description }}{% endif %}
{% if first_date %}Lần đặt chỗ đầu tiên: {{ first_date }}{% endif %}
{% if total_bookings %}Tổng số đặt chỗ: {{ total_bookings }}{% endif %}
{% if resource_name %}Tài nguyên: {{ resource_name }}{% endif %}
{% if total_cost %}Chi phí mỗi lần đặt chỗ: {{ total_cost }}{% endif %}

Bạn có thể quản lý các lần đặt chỗ riêng lẻ trong chuỗi này từ tài khoản của bạn.