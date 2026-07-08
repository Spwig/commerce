---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Siparişiniz Gönderildi - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Siparişiniz Gönderildi!
        </mj-text>
        <mj-text>
          Harika haber! Siparişiniz #{{ order_number }} gönderildi.
        </mj-text>
        <mj-text>
          <strong>İzleme Numarası:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Kurye:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Gönderiyi Takip Et
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Siparişiniz Gönderildi!

Harika haber! Siparişiniz #{{ order_number }} gönderildi.

İzleme Numarası: {{ tracking_number }}
Kurye: {{ carrier }}

Gönderiyi takip et: {{ tracking_url }}