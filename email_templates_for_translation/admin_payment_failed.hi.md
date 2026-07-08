---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
भुगतान विफल - आर्डर #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          भुगतान विफल
        </mj-text>
        <mj-text>
          आर्डर #{{ order_number }} के लिए भुगतान प्रयास विफल रहा।
        </mj-text>
        <mj-text>
          <strong>ग्राहक:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>राशि:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>त्रुटि:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          प्रशासन में देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
भुगतान विफल

आर्डर #{{ order_number }} के लिए भुगतान प्रयास विफल रहा।

ग्राहक: {{ customer_name }}
राशि: {{ order_total }}
त्रुटि: {{ error_message }}

प्रशासन में देखें: {{ admin_order_url }}
