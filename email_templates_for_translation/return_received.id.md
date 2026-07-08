---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Kami Telah Menerima Pengembalian Anda - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Pengembalian Diterima
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami telah menerima barang pengembalian untuk pesanan <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Apa yang terjadi selanjutnya:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Tim kami akan memeriksa barang pengembalian dalam 2-3 hari kerja<br/>
          2. Kami akan memverifikasi bahwa barang dalam kondisi aslinya<br/>
          3. Setelah pemeriksaan selesai, kami akan memproses pengembalian dana Anda<br/>
          4. Anda akan menerima email konfirmasi setelah pengembalian dana selesai diproses
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Pengembalian dana akan dikreditkan ke metode pembayaran asli Anda dan mungkin memakan waktu 5-10 hari kerja untuk muncul di akun Anda.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Terima kasih atas kesabaran Anda!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pengembalian Diterima - Pesanan #{{ order_number }}

Hai {{ customer_name }},

Kami telah menerima barang pengembalian untuk pesanan #{{ order_number }}.

Apa yang terjadi selanjutnya:
1. Tim kami akan memeriksa barang pengembalian dalam 2-3 hari kerja
2. Kami akan memverifikasi bahwa barang dalam kondisi aslinya
3. Setelah pemeriksaan selesai, kami akan memproses pengembalian dana Anda
4. Anda akan menerima email konfirmasi setelah pengembalian dana selesai diproses

Pengembalian dana akan dikreditkan ke metode pembayaran asli Anda dan mungkin memakan waktu 5-10 hari kerja untuk muncul di akun Anda.

Terima kasih atas kesabaran Anda!