---
template_type: admin_new_booking
category: Bookings
---

# Email Template: admin_new_booking

## Subject
Nuova Prenotazione - {{ product_name }}

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
          Nuova Prenotazione Ricevuta
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          &Egrave; stata effettuata una nuova prenotazione e richiede la tua attenzione.
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
          <strong>Cliente:</strong> {{ customer_name }} ({{ customer_email }})
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Data:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ora:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Risorsa:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ospiti:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Stato:</strong> {{ status }}
        </mj-text>
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Totale:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- View in Admin CTA -->
    {% if admin_booking_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_booking_url text="Visualizza nell'Amministrazione" %}
    {% endif %}
  </mj-body>
</mjml>

## Text Content
Nuova Prenotazione Ricevuta

&Egrave; stata effettuata una nuova prenotazione e richiede la tua attenzione.

{{ product_name }}
Cliente: {{ customer_name }} ({{ customer_email }})
Data: {{ booking_date }}
Ora: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Risorsa: {{ resource_name }}{% endif %}
{% if persons_display %}Ospiti: {{ persons_display }}{% endif %}
Stato: {{ status }}
{% if total_cost %}Totale: {{ total_cost }}{% endif %}

{% if admin_booking_url %}Visualizza nell'Amministrazione: {{ admin_booking_url }}{% endif %}