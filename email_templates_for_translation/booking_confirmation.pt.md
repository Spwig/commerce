---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
Reserva Confirmada - {{ product_name }} em {{ booking_date }}

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
          Reserva Confirmada!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Olá {{ customer_name }}, sua reserva foi confirmada.
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
          <strong>Data:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Hora:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Recurso:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Hóspedes:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Total:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Depósito Pago:</strong> {{ deposit_amount }}
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
          Precisa fazer alterações? Você pode <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">reagendar</a> ou <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">cancelar</a> sua reserva a partir da sua conta.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Reserva Confirmada!

Olá {{ customer_name }}, sua reserva foi confirmada.

{{ product_name }}

Data: {{ booking_date }}
Hora: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Recurso: {{ resource_name }}{% endif %}
{% if persons_display %}Hóspedes: {{ persons_display }}{% endif %}
{% if total_cost %}Total: {{ total_cost }}{% endif %}
{% if deposit_amount %}Depósito Pago: {{ deposit_amount }}{% endif %}

{% if ical_url %}Adicionar ao calendário: {{ ical_url }}{% endif %}

Precisa fazer alterações? Acesse sua conta para reagendar ou cancelar.
{{ reschedule_url }}
{{ cancel_url }}