---
template_type: booking_reminder
category: Bookings
---

# Email Template: booking_reminder

## Subject
Напоминание: {{ product_name }} - {{ booking_date }}

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
          Напоминание о бронировании
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Здравствуйте {{ customer_name }}, это напоминание о вашем предстоящем бронировании.
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
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Гости:</strong> {{ persons_display }}
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
          Нужно внести изменения? Вы можете <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">переназначить</a> или <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">отменить</a> ваше бронирование через ваш аккаунт.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Напоминание о бронировании

Здравствуйте {{ customer_name }}, это напоминание о вашем предстоящем бронировании.

{{ product_name }}

Дата: {{ booking_date }}
Время: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Ресурс: {{ resource_name }}{% endif %}
{% if persons_display %}Гости: {{ persons_display }}{% endif %}

{% if ical_url %}Добавить в календарь: {{ ical_url }}{% endif %}

Нужно внести изменения? Перейдите в ваш аккаунт, чтобы переназначить или отменить.
{{ reschedule_url }}
{{ cancel_url }}