---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Pembayaran {{ payout_amount }} Anda sedang diproses

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
          💸 Pemrosesan Pembayaran
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Pemrosesan Pembayaran Anda
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
          Berita baik! Pembayaran Anda sebesar {{ payout_amount }} sekarang sedang diproses.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dana tersebut seharusnya tiba di akun Anda dalam 3-5 hari kerja. Anda akan menerima email lain saat pembayaran selesai.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID Pembayaran:</strong> {{ payout_id }}<br/>
          <strong>Jumlah:</strong> {{ payout_amount }}<br/>
          <strong>Cara Pembayaran:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Lihat Riwayat Pembayaran
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
Pembayaran {{ payout_amount }} Anda sedang diproses

Hai {{ affiliate_name }},

Berita baik! Pembayaran Anda sebesar {{ payout_amount }} sekarang sedang diproses.

Dana tersebut seharusnya tiba di akun Anda dalam 3-5 hari kerja. Anda akan menerima email lain saat pembayaran selesai.

Detail Pembayaran:
- ID Pembayaran: {{ payout_id }}
- Jumlah: {{ payout_amount }}
- Cara Pembayaran: {{ payout_method }}

Lihat riwayat pembayaran: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}