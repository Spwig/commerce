---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Anda telah mencapai ambang batas pembayaran!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Ambang Batas Pembayaran Tercapai!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Berita Baik!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Selamat! Saldo afiliasi Anda telah mencapai ambang batas pembayaran minimum. Anda sekarang dapat meminta pembayaran.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Saldo Anda:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Saldo Tersedia:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Ambang Batas Minimum:</strong> {{ minimum_payout }}<br/>
              <strong>Komisi Tertunda:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa Selanjutnya:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Ajukan permohonan pembayaran dari dashboard afiliasi Anda<br/>
          • Pembayaran diproses {{ payout_schedule }}<br/>
          • Dana akan dikirimkan melalui {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ajukan Pembayaran
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 AMBANG BATAS PEMBAYARAN TERCAPAI!

Berita Baik!

Hi {{ affiliate_name }},

Selamat! Saldo afiliasi Anda telah mencapai ambang batas pembayaran minimum. Anda sekarang dapat meminta pembayaran.

SALDO ANDA:
- Saldo Tersedia: {{ available_balance }}
- Ambang Batas Minimum: {{ minimum_payout }}
- Komisi Tertunda: {{ pending_balance }}

APA SELANJUTNYA:
• Ajukan permohonan pembayaran dari dashboard afiliasi Anda
• Pembayaran diproses {{ payout_schedule }}
• Dana akan dikirimkan melalui {{ payment_method }}

Ajukan pembayaran: {{ request_payout_url }}
Lihat dashboard: {{ portal_url }}