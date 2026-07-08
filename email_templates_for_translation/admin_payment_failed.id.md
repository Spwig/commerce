---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Pembayaran Gagal - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Pembayaran Gagal
        </mj-text>
        <mj-text>
          Upaya pembayaran gagal untuk pesanan #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Pelanggan:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Jumlah:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Kesalahan:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Lihat di Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembayaran Gagal

Upaya pembayaran gagal untuk pesanan #{{ order_number }}.

Pelanggan: {{ customer_name }}
Jumlah: {{ order_total }}
Kesalahan: {{ error_message }}

Lihat di admin: {{ admin_order_url }}