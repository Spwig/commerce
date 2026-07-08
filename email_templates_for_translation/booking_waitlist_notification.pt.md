---
template_type: booking_waitlist_notification
category: Bookings
---

# Email Template: booking_waitlist_notification

## Subject
Um Lugar Abriu - {{ product_name }}

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
          Um Lugar Acabou de Abrir!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Olá {{ customer_name }}, um lugar ficou disponível para uma reserva para a qual você estava na lista de espera.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        {% if available_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Data Disponível:</strong> {{ available_date }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Recurso:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Urgency Notice -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Aja rapidamente! Esse lugar está disponível sob o princípio de primeiro a chegar, primeiro a ser atendido.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Book Now CTA -->
    {% if book_now_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=book_now_url text="Book Now" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Um Lugar Acabou de Abrir!

Olá {{ customer_name }}, um lugar ficou disponível para uma reserva para a qual você estava na lista de espera.

{{ product_name }}
{% if available_date %}Data Disponível: {{ available_date }}{% endif %}
{% if resource_name %}Recurso: {{ resource_name }}{% endif %}

Aja rapidamente! Esse lugar está disponível sob o princípio de primeiro a chegar, primeiro a ser atendido.

{% if book_now_url %}Reserve Agora: {{ book_now_url }}{% endif %}