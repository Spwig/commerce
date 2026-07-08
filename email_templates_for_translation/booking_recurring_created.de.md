---
template_type: booking_recurring_created
category: Bookings
---

# Email Template: booking_recurring_created

## Subject
Wiederkehrende Buchungsserie erstellt - {{ product_name }}

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
          Wiederkehrende Buchung erstellt
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hallo {{ customer_name }}, Ihre wiederkehrende Buchungsserie wurde eingerichtet.
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
          <strong>Zeitplan:</strong> {{ recurrence_description }}
        </mj-text>
        {% endif %}
        {% if first_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Erste Buchung:</strong> {{ first_date }}
        </mj-text>
        {% endif %}
        {% if total_bookings %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Gesamtzahl der Buchungen:</strong> {{ total_bookings }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ressource:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Kosten pro Buchung:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Manage -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Sie können einzelne Buchungen in dieser Serie über Ihr Konto verwalten.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Wiederkehrende Buchung erstellt

Hallo {{ customer_name }}, Ihre wiederkehrende Buchungsserie wurde eingerichtet.

{{ product_name }}

{% if recurrence_description %}Zeitplan: {{ recurrence_description }}{% endif %}
{% if first_date %}Erste Buchung: {{ first_date }}{% endif %}
{% if total_bookings %}Gesamtzahl der Buchungen: {{ total_bookings }}{% endif %}
{% if resource_name %}Ressource: {{ resource_name }}{% endif %}
{% if total_cost %}Kosten pro Buchung: {{ total_cost }}{% endif %}

Sie können einzelne Buchungen in dieser Serie über Ihr Konto verwalten.