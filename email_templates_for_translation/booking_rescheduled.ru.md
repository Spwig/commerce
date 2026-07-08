---
template_type: booking_rescheduled
category: Bookings
---

# Email Template: booking_rescheduled

## Subject
Бронирование перенесено - {{ product_name }}

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
          Бронирование перенесено
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Здравствуйте {{ customer_name }}, ваше бронирование было перенесено.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- New Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="10px">
          Новая дата и время
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Дата:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Время:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ресурс:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if old_date %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="15px">
          <em>Ранее: {{ old_date }} в {{ old_time_start }} - {{ old_time_end }}</em>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Add to Calendar -->
    {% if ical_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=ical_url text="Update Calendar" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Бронирование перенесено

Здравствуйте {{ customer_name }}, ваше бронирование было перенесено.

{{ product_name }}

Новая дата и время:
Дата: {{ booking_date }}
Время: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Ресурс: {{ resource_name }}{% endif %}
{% if old_date %}Ранее: {{ old_date }} в {{ old_time_start }} - {{ old_time_end }}{% endif %}

{% if ical_url %}Обновить календарь: {{ ical_url }}{% endif %}