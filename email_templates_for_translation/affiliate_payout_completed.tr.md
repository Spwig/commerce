---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Ödeme tamamlandı: {{ payout_amount }}

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
          🎉 Ödeme Tamamlandı!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Başarıyla Ödendi
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Ödeme Kimliği: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Merhaba {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ payout_amount }} ödeme başarıyla tamamlandı!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Para, ödeme yönteminize gönderildi. Bankanız veya ödeme işlemciniz tarafından, hesabınızda görünmesi için 1-2 iş günü sürebilir.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }}'i tanıtım için teşekkür ederiz. Harikasını yapmaya devam edin!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ödeme Detaylarını Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız var mı? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Ödeme tamamlandı: {{ payout_amount }}

Merhaba {{ affiliate_name }},

{{ payout_amount }} ödeme başarıyla tamamlandı!

Ödeme Detayları:
- Ödeme Kimliği: {{ payout_id }}
- Tutar: {{ payout_amount }}
- Ödeme Yöntemi: {{ payout_method }}

Para, ödeme yönteminize gönderildi. Bankanız veya ödeme işlemciniz tarafından, hesabınızda görünmesi için 1-2 iş günü sürebilir.

{{ shop_name }}'i tanıtım için teşekkür ederiz. Harikasını yapmaya devam edin!

Ödeme detaylarını görüntüle: {{ portal_url }}

{{ shop_name }}
Sorularınız var mı? {{ support_email }} ile iletişime geçin