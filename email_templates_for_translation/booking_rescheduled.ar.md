---
template_type: booking_rescheduled
category: Bookings
---

# Email Template: booking_rescheduled

## Subject
تم إعادة جدولة الحجز - {{ product_name }}

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
          تم إعادة جدولة الحجز
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          مرحبًا {{ customer_name }}, تم إعادة جدولة حجزك.
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
          التاريخ والوقت الجدد
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>التاريخ:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>الوقت:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>المورد:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if old_date %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="15px">
          <em>سابقًا: {{ old_date }} في {{ old_time_start }} - {{ old_time_end }}</em>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Add to Calendar -->
    {% if ical_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=ical_url text="تحديث التقويم" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم إعادة جدولة الحجز

مرحبًا {{ customer_name }}, تم إعادة جدولة حجزك.

{{ product_name }}

التاريخ والوقت الجدد:
التاريخ: {{ booking_date }}
الوقت: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}المورد: {{ resource_name }}{% endif %}
{% if old_date %}سابقًا: {{ old_date }} في {{ old_time_start }} - {{ old_time_end }}{% endif %}

{% if ical_url %}تحديث التقويم: {{ ical_url }}{% endif %}