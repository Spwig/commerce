---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Pemesanan Baru Diterima - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pemesanan Baru Diterima
        </mj-text>
        <mj-text>
          Sebuah pemesanan baru telah ditempatkan di toko Anda.
        </mj-text>
        <mj-text>
          <strong>Nomor Pesanan:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Nama Pelanggan:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Lihat di Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pemesanan Baru Diterima

Sebuah pemesanan baru telah ditempatkan di toko Anda.

Nomor Pesanan: {{ order_number }}
Nama Pelanggan: {{ customer_name }}
Total: {{ order_total }}

Lihat di admin: {{ admin_order_url }}
