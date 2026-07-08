---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Pembayaran Dibatalkan - {{ payout_amount }}

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
          Pembayaran Dibatalkan
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
          Pembayaran Anda sebesar {{ payout_amount }} (ID Pembayaran: {{ payout_id }}) telah dibatalkan.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Jika Anda memiliki pertanyaan mengenai alasan pembatalan pembayaran ini, mohon hubungi tim dukungan kami.
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
          Pertanyaan? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            Hubungi Dukungan
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembayaran Dibatalkan - {{ payout_amount }}

Halo {{ affiliate_name }},

Pembayaran Anda sebesar {{ payout_amount }} (ID Pembayaran: {{ payout_id }}) telah dibatalkan.

Jika Anda memiliki pertanyaan mengenai alasan pembatalan pembayaran ini, mohon hubungi tim dukungan kami.

Lihat dashboard Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}