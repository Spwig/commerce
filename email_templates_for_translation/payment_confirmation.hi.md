---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
भुगतान स्वीकृत - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          भुगतान स्वीकृत
        </mj-text>
        <mj-text>
          आदेश #{{ order_number }} के लिए आपका भुगतान सफलता पूर्वक प्रक्रिया में रखा गया है।
        </mj-text>
        <mj-text>
          <strong>भुगतान की राशि:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>भुगतान विधि:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
भुगतान स्वीकृत

आदेश #{{ order_number }} के लिए आपका भुगतान सफलता पूर्वक प्रक्रिया में रखा गया है।

भुगतान की राशि: {{ amount_paid }}
भुगतान विधि: {{ payment_method }}