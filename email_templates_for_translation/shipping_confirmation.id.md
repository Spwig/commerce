---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Pengiriman Pesanan Anda - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pengiriman Pesanan Anda!
        </mj-text>
        <mj-text>
          Berita baik! Pesanan Anda #{{ order_number }} telah dikirimkan.
        </mj-text>
        <mj-text>
          <strong>Nomor Pelacakan:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Pengirim:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Lacak Pengiriman
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pengiriman Pesanan Anda!

Berita baik! Pesanan Anda #{{ order_number }} telah dikirimkan.

Nomor Pelacakan: {{ tracking_number }}
Pengirim: {{ carrier }}

Lacak pengiriman Anda: {{ tracking_url }}
