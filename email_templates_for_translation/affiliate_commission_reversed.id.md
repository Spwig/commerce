---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Komisi dikembalikan - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          Komisi Dikembalikan
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Halo {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Komisi untuk pesanan #{{ order_number }} ({{ commission_amount }}) telah dikembalikan karena pengembalian dana oleh pelanggan.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ketika pelanggan meminta pengembalian dana, komisi yang terkait secara otomatis dikembalikan untuk memastikan akuntansi yang akurat.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ini adalah bagian normal dari proses afiliasi. Teruslah mempromosikan {{ shop_name }} untuk memperoleh komisi baru!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Lihat Dashboard Afiliasi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Pertanyaan? <a href="mailto:{{ support_email }}" style="color: #007bff;">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Komisi dikembalikan - Pesanan #{{ order_number }}

Halo {{ affiliate_name }},

Komisi untuk pesanan #{{ order_number }} ({{ commission_amount }}) telah dikembalikan karena pengembalian dana oleh pelanggan.

Ketika pelanggan meminta pengembalian dana, komisi yang terkait secara otomatis dikembalikan untuk memastikan akuntansi yang akurat.

Ini adalah bagian normal dari proses afiliasi. Teruslah mempromosikan {{ shop_name }} untuk memperoleh komisi baru!

Lihat dashboard Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}