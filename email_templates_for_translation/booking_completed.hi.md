---
template_type: booking_completed
category: Bookings
---

# Email Template: booking_completed

## Subject
धन्यवाद - {{ product_name }}

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
          धन्यवाद!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          हेलो {{ customer_name }}, हम उम्मीत करते हैं कि आपने अपना अनुभव आनंदित किया।
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
          <strong>तारीख:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>समय:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Book Again -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          हम आपको फिर से देखना चाहते हैं! हमारे वेबसाइट पर जाएं और अपना अगला अपॉइंटमेंट बुक करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
धन्यवाद!

हेलो {{ customer_name }}, हम उम्मीत करते हैं कि आपने अपना अनुभव आनंदित किया।

{{ product_name }}

तारीख: {{ booking_date }}
समय: {{ booking_time_start }} - {{ booking_time_end }}

हम आपको फिर से देखना चाहते हैं! हमारे वेबसाइट पर जाएं और अपना अगला अपॉइंटमेंट बुक करें।