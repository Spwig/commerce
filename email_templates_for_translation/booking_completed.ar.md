---
template_type: booking_completed
category: Bookings
---

# Email Template: booking_completed

## Subject
شكرًا - {{ product_name }}

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
          شكرًا!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          أهلاً {{ customer_name }}, نتمنى أنك استمتعت بتجربتك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Summary -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>التاريخ:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>الوقت:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Book Again -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          نتمنى أن نراك مرة أخرى! قم بزيارة موقعنا لحجز موعدك القادم.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
شكرًا!

أهلاً {{ customer_name }}, نتمنى أنك استمتعت بتجربتك.

{{ product_name }}

التاريخ: {{ booking_date }}
الوقت: {{ booking_time_start }} - {{ booking_time_end }}

نتمنى أن نراك مرة أخرى! قم بزيارة موقعنا لحجز موعدك القادم.