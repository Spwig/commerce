---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Pembayaran Dikonfirmasi - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pembayaran Dikonfirmasi
        </mj-text>
        <mj-text>
          Pembayaran Anda untuk pesanan #{{ order_number }} telah berhasil diproses.
        </mj-text>
        <mj-text>
          <strong>Jumlah yang Dibayar:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Cara Pembayaran:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembayaran Dikonfirmasi

Pembayaran Anda untuk pesanan #{{ order_number }} telah berhasil diproses.

Jumlah yang Dibayar: {{ amount_paid }}
Cara Pembayaran: {{ payment_method }}