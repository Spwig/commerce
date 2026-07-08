---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
Komisi disetujui: {{ commission_amount }}

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
          ✓ Komisi Disetujui!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Disetujui untuk pembayaran
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
          Komisi Anda sebesar {{ commission_amount }} dari pesanan #{{ order_number }} telah disetujui dan akan termasuk dalam pembayaran berikutnya Anda.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Pembayaran diproses sesuai jadwal pembayaran Anda. Anda akan menerima email lain saat pembayaran diproses.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Lihat Komisi
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
Komisi disetujui: {{ commission_amount }}

Halo {{ affiliate_name }},

Komisi Anda sebesar {{ commission_amount }} dari pesanan #{{ order_number }} telah disetujui dan akan termasuk dalam pembayaran berikutnya Anda.

Pembayaran diproses sesuai jadwal pembayaran Anda. Anda akan menerima email lain saat pembayaran diproses.

Lihat komisi Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}