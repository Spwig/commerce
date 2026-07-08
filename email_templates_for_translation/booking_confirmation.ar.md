---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
تم تأكيد الحجز - {{ product_name }} في {{ booking_date }}

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
          تم تأكيد الحجز!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          مرحبًا {{ customer_name }}, تم تأكيد حجزك.
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
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>الضيوف:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>المجموع:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>الدفعة المقدمة:</strong> {{ deposit_amount }}
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
          هل تحتاج إلى إجراء بعض التغييرات؟ يمكنك <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">إعادة جدولة</a> أو <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">إلغاء</a> حجزك من حسابك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم تأكيد الحجز!

مرحبًا {{ customer_name }}, تم تأكيد حجزك.

{{ product_name }}

التاريخ: {{ booking_date }}
الوقت: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}المورد: {{ resource_name }}{% endif %}
{% if persons_display %}الضيوف: {{ persons_display }}{% endif %}
{% if total_cost %}المجموع: {{ total_cost }}{% endif %}
{% if deposit_amount %}الدفعة المقدمة: {{ deposit_amount }}{% endif %}

{% if ical_url %}إضافة إلى التقويم: {{ ical_url }}{% endif %}

هل تحتاج إلى إجراء بعض التغييرات؟ قم بزيارة حسابك لإعادة جدولة أو إلغاء الحجز.
{{ reschedule_url }}
{{ cancel_url }}