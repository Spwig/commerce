---
template_type: booking_deposit_receipt
category: Bookings
---

# Email Template: booking_deposit_receipt

## Subject
Depósito recibido - {{ product_name }}

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
          Depósito recibido
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hola {{ customer_name }}, hemos recibido tu pago de depósito.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Fecha:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Hora:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px">
          <strong>Depósito pagado:</strong> {{ deposit_amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Costo total:</strong> {{ total_cost }}
        </mj-text>
        {% if remaining_balance %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Saldo restante:</strong> {{ remaining_balance }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Depósito recibido

Hola {{ customer_name }}, hemos recibido tu pago de depósito.

{{ product_name }}

Fecha: {{ booking_date }}
Hora: {{ booking_time_start }} - {{ booking_time_end }}

Depósito pagado: {{ deposit_amount }}
Costo total: {{ total_cost }}
{% if remaining_balance %}Saldo restante: {{ remaining_balance }}{% endif %}