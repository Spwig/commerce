---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Pengembalian Dana Selesai - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pengembalian Dana Selesai
        </mj-text>
        <mj-text>
          Pengembalian dana telah diproses untuk pesanan #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Jumlah Pengembalian:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          Pengembalian dana akan muncul di akun Anda dalam {{ refund_days }} hari kerja.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pengembalian Dana Selesai

Pengembalian dana telah diproses untuk pesanan #{{ order_number }}.

Jumlah Pengembalian: {{ refund_amount }}

Pengembalian dana akan muncul di akun Anda dalam {{ refund_days }} hari kerja.