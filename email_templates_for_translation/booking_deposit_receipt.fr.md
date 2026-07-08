---
template_type: booking_deposit_receipt
category: Bookings
---

# Email Template: booking_deposit_receipt

## Subject
Dépôt reçu - {{ product_name }}

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
          Dépôt reçu
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Bonjour {{ customer_name }}, nous avons reçu votre paiement de dépôt.
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
          <strong>Date :</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Heure :</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px">
          <strong>Dépôt payé :</strong> {{ deposit_amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Coût total :</strong> {{ total_cost }}
        </mj-text>
        {% if remaining_balance %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Solde restant :</strong> {{ remaining_balance }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Dépôt reçu

Bonjour {{ customer_name }}, nous avons reçu votre paiement de dépôt.

{{ product_name }}

Date : {{ booking_date }}
Heure : {{ booking_time_start }} - {{ booking_time_end }}

Dépôt payé : {{ deposit_amount }}
Coût total : {{ total_cost }}
{% if remaining_balance %}Solde restant : {{ remaining_balance }}{% endif %}