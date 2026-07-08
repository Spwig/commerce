---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Anda mendapatkan komisi {{ commission_amount }}!

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
          💰 Komisi yang Diperoleh!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Berita baik dari {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Komisi Anda
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Dari Pesanan #{{ order_number }}
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
          Selamat! Anda telah mendapatkan komisi {{ commission_amount }} dari pesanan #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Teruslah mempromosikan {{ shop_name }} untuk mendapatkan lebih banyak komisi. Semakin banyak penjualan yang Anda hasilkan, semakin banyak pula yang Anda peroleh!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Nomor Pesanan:</strong> #{{ order_number }}<br/>
          <strong>Jumlah Komisi:</strong> {{ commission_amount }}<br/>
          <strong>Kadar Komisi:</strong> {{ commission_rate }}%
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
Anda mendapatkan komisi {{ commission_amount }}!

Halo {{ affiliate_name }},

Selamat! Anda telah mendapatkan komisi {{ commission_amount }} dari pesanan #{{ order_number }}.

Detail Komisi:
- Nomor Pesanan: #{{ order_number }}
- Jumlah Komisi: {{ commission_amount }}
- Kadar Komisi: {{ commission_rate }}%

Teruslah mempromosikan {{ shop_name }} untuk mendapatkan lebih banyak komisi.

Lihat dashboard Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}