---
template_type: booking_no_show
category: Bookings
---

# Email Template: booking_no_show

## Subject
बुकिंग छूट गई - {{ product_name }}

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
          हमने आपको छोड़ दिया
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          हेलो {{ customer_name }}, आपकी बुकिंग छूट गई लगता है।
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
          <strong>तारीख:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>समय:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Rebook -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          क्या आप फिर से बुक करना चाहते हैं? हमारे वेबसाइट पर जाएं और आपके लिए एक अच्छा समय चुनें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
हमने आपको छोड़ दिया

हेलो {{ customer_name }}, आपकी बुकिंग छूट गई लगता है।

{{ product_name }}

तारीख: {{ booking_date }}
समय: {{ booking_time_start }} - {{ booking_time_end }}

क्या आप फिर से बुक करना चाहते हैं? हमारे वेबसाइट पर जाएं और आपके लिए एक अच्छा समय चुनें।