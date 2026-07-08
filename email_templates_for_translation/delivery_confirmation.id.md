---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Pesanan Terkirim - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pesanan Terkirim
        </mj-text>
        <mj-text>
          Pesanan Anda #{{ order_number }} telah terkirim!
        </mj-text>
        <mj-text>
          Kami berharap Anda menikmati pembelian Anda. Jika Anda memiliki pertanyaan atau kekhawatiran, jangan ragu untuk menghubungi kami.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Lihat Pesanan
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pesanan Terkirim

Pesanan Anda #{{ order_number }} telah terkirim!

Kami berharap Anda menikmati pembelian Anda. Jika Anda memiliki pertanyaan atau kekhawatiran, jangan ragu untuk menghubungi kami.

Lihat pesanan: {{ order_url }}