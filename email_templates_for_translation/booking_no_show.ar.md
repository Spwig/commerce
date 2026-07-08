---
template_type: booking_no_show
category: Bookings
---

# Email Template: booking_no_show

## Subject
الحجز المفقود - {{ product_name }}

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
          لقد غابنا عنك
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          أهلاً {{ customer_name }}, يبدو أنك غابت عن حجزك.
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
          <strong>الوقت:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Rebook -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          هل ترغب في إعادة الحجز؟ قم بزيارة موقعنا لحجز موعد جديد في وقت يناسبك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
لقد غابنا عنك

أهلاً {{ customer_name }}, يبدو أنك غابت عن حجزك.

{{ product_name }}

التاريخ: {{ booking_date }}
الوقت: {{ booking_time_start }} - {{ booking_time_end }}

هل ترغب في إعادة الحجز؟ قم بزيارة موقعنا لحجز موعد جديد في وقت يناسبك.