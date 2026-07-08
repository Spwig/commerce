---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Ihre Bestellung ist versandt worden - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Ihre Bestellung ist versandt worden!
        </mj-text>
        <mj-text>
          Große Neuigkeit! Ihre Bestellung #{{ order_number }} ist versandt worden.
        </mj-text>
        <mj-text>
          <strong>Tracking-Nummer:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Transporteur:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Sendung verfolgen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ihre Bestellung ist versandt worden!

Große Neuigkeit! Ihre Bestellung #{{ order_number }} ist versandt worden.

Tracking-Nummer: {{ tracking_number }}
Transporteur: {{ carrier }}

Sendung verfolgen: {{ tracking_url }}