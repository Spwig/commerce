---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Pembaruan status komisi - Pesanan #{{ order_number }}

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
          Pembaruan Status Komisi
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hai {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Kami ingin memberi tahu Anda bahwa komisi untuk pesanan #{{ order_number }} ({{ commission_amount }}) tidak disetujui.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Hal ini biasanya terjadi saat pesanan dibatalkan atau dikembalikan sebelum periode komisi berakhir.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Jika Anda memiliki pertanyaan tentang komisi ini, mohon hubungi tim dukungan kami.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
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
Pembaruan status komisi - Pesanan #{{ order_number }}

Hai {{ affiliate_name }},

Kami ingin memberi tahu Anda bahwa komisi untuk pesanan #{{ order_number }} ({{ commission_amount }}) tidak disetujui.

Hal ini biasanya terjadi saat pesanan dibatalkan atau dikembalikan sebelum periode komisi berakhir.

Jika Anda memiliki pertanyaan tentang komisi ini, mohon hubungi tim dukungan kami.

Lihat dashboard Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}

