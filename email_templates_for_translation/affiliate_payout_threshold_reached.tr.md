---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Ödeme Seviyesine Ulaştınız!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Ödeme Seviyesine Ulaştınız!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Harika Haber!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tebrikler! İş ortağınızın bakiyesi en düşük ödeme seviyesine ulaştı. Şimdi ödeme talep edebilirsiniz.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bakiyeniz:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Kullanılabilir Bakiye:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Minimum Ödeme:</strong> {{ minimum_payout }}<br/>
              <strong>Bekleyen Komisyonlar:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ne Sıradaki:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • İş ortağı panelinizden ödeme talep edin<br/>
          • Ödemeler {{ payout_schedule }} işlenir<br/>
          • Para {{ payment_method }} yoluyla gönderilecek
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ödeme Talep Et
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Paneli Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 ÖDENE SEVİYESİ ERİŞİLDİ!

Harika Haber!

Merhaba {{ affiliate_name }},

Tebrikler! İş ortağınızın bakiyesi en düşük ödeme seviyesine ulaştı. Şimdi ödeme talep edebilirsiniz.

BAKİYENİZ:
- Kullanılabilir Bakiye: {{ available_balance }}
- Minimum Ödeme: {{ minimum_payout }}
- Bekleyen Komisyonlar: {{ pending_balance }}

NE SIRADA:
• İş ortağı panelinizden ödeme talep edin
• Ödemeler {{ payout_schedule }} işlenir
• Para {{ payment_method }} yoluyla gönderilecek

Ödeme talep et: {{ request_payout_url }}
Paneli görüntüle: {{ portal_url }}