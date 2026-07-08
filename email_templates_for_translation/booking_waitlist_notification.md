---
template_type: booking_waitlist_notification
category: Bookings
---

# Email Template: booking_waitlist_notification

## Subject
A Spot Opened Up - {{ product_name }}

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
          A Spot Just Opened Up!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hi {{ customer_name }}, a spot has become available for a booking you were waitlisted for.
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
          <strong>Available Date:</strong> {{ available_date }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Resource:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Urgency Notice -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Act quickly! This spot is available on a first-come, first-served basis.
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
A Spot Just Opened Up!

Hi {{ customer_name }}, a spot has become available for a booking you were waitlisted for.

{{ product_name }}
{% if available_date %}Available Date: {{ available_date }}{% endif %}
{% if resource_name %}Resource: {{ resource_name }}{% endif %}

Act quickly! This spot is available on a first-come, first-served basis.

{% if book_now_url %}Book Now: {{ book_now_url }}{% endif %}
