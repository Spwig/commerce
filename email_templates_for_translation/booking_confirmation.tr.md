---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
Rezervasyon Onaylandı - {{ product_name }} - {{ booking_date }}

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
          Rezervasyon Onaylandı!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Merhaba {{ customer_name }}, rezervasyonunuz onaylandı.
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
          <strong>Tarih:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Saat:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Kaynak:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ziyaretçiler:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Toplam:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ödendi:</strong> {{ deposit_amount }}
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
          Değişiklik yapmanız gerekiyor mu? Hesabınızdan <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">tekrar planlayabilirsiniz</a> veya <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">rezervasyonu iptal</a> edebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Rezervasyon Onaylandı!

Merhaba {{ customer_name }}, rezervasyonunuz onaylandı.

{{ product_name }}

Tarih: {{ booking_date }}
Saat: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Kaynak: {{ resource_name }}{% endif %}
{% if persons_display %}Ziyaretçiler: {{ persons_display }}{% endif %}
{% if total_cost %}Toplam: {{ total_cost }}{% endif %}
{% if deposit_amount %}Ödendi: {{ deposit_amount }}{% endif %}

{% if ical_url %}Takvime Ekle: {{ ical_url }}{% endif %}

Değişiklik yapmanız gerekiyor mu? Hesabınıza girerek rezervasyonu iptal edebilir veya tekrar planlayabilirsiniz.
{{ reschedule_url }}
{{ cancel_url }}