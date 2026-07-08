---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Tindakan diperlukan: Payout gagal

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ Payout Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          ID Payout: {{ payout_id }}
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
          Kami mengalami masalah dalam memproses payout Anda sebesar {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ini biasanya disebabkan oleh informasi pembayaran yang tidak benar atau masalah dengan penyedia pembayaran Anda.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Silakan perbarui informasi pembayaran Anda di dashboard afiliasi Anda dan hubungi tim dukungan kami untuk menyelesaikan masalah ini.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Perbarui Informasi Pembayaran
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Membutuhkan bantuan? <a href="mailto:{{ support_email }}" style="color: #007bff;">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tindakan diperlukan: Payout gagal

Hai {{ affiliate_name }},

Kami mengalami masalah dalam memproses payout Anda sebesar {{ payout_amount }} (ID Payout: {{ payout_id }}).

Ini biasanya disebabkan oleh informasi pembayaran yang tidak benar atau masalah dengan penyedia pembayaran Anda.

Silakan perbarui informasi pembayaran Anda di dashboard afiliasi Anda dan hubungi tim dukungan kami untuk menyelesaikan masalah ini.

Perbarui informasi pembayaran: {{ portal_url }}

{{ shop_name }}
Membutuhkan bantuan? Hubungi {{ support_email }}