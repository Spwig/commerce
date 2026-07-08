---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Pembayaran selesai: {{ payout_amount }}

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
          🎉 Pembayaran Selesai!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Pembayaran Berhasil
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID Pembayaran: {{ payout_id }}
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
          Pembayaran Anda sebesar {{ payout_amount }} telah selesai dengan sukses!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dana telah dikirim ke metode pembayaran Anda. Tergantung pada bank atau pemroses pembayaran Anda, mungkin memerlukan 1-2 hari kerja untuk muncul di akun Anda.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Terima kasih telah mempromosikan {{ shop_name }}. Pertahankan pekerjaan yang hebat!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Lihat Detail Pembayaran
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
✓ Pembayaran selesai: {{ payout_amount }}

Hai {{ affiliate_name }},

Pembayaran Anda sebesar {{ payout_amount }} telah selesai dengan sukses!

Detail Pembayaran:
- ID Pembayaran: {{ payout_id }}
- Jumlah: {{ payout_amount }}
- Metode Pembayaran: {{ payout_method }}

Dana telah dikirim ke metode pembayaran Anda. Tergantung pada bank atau pemroses pembayaran Anda, mungkin memerlukan 1-2 hari kerja untuk muncul di akun Anda.

Terima kasih telah mempromosikan {{ shop_name }}. Pertahankan pekerjaan yang hebat!

Lihat detail pembayaran: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}