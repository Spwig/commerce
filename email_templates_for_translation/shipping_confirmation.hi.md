---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
आपका ऑर्डर शिप कर दिया गया है - ऑर्डर #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          आपका ऑर्डर शिप कर दिया गया है!
        </mj-text>
        <mj-text>
          अच्छ खबर! आपका ऑर्डर #{{ order_number }} शिप कर दिया गया है।
        </mj-text>
        <mj-text>
          <strong>ट्रैकिंग नंबर:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>वाहक:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          शिपमेंट ट्रैक करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपका ऑर्डर शिप कर दिया गया है!

अच्छ खबर! आपका ऑर्डर #{{ order_number }} शिप कर दिया गया है।

ट्रैकिंग नंबर: {{ tracking_number }}
वाहक: {{ carrier }}

अपने शिपमेंट को ट्रैक करें: {{ tracking_url }}