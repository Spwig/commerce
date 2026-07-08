---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Eylem Gerekiyor: Ödeme Başarısız

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
          ⚠️ Ödeme Başarısız
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
          {{ payout_amount }} ödeme işleme sırasında bir sorunla karşılaştık.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu genellikle yanlış ödeme bilgileri veya ödeme sağlayıcınızla ilgili bir sorun nedeniyle olur.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Lütfen affiliate panelinizdeki ödeme bilgilerinizi güncelleyin ve bu sorunu çözmek için destek ekibimize ulaşın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Ödeme Bilgilerini Güncelle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Yardıma mı ihtiyacınız var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Eylem Gerekiyor: Ödeme Başarısız

Merhaba {{ affiliate_name }},

{{ payout_amount }} ödeme işleme sırasında bir sorunla karşılaştık (Ödeme Kimliği: {{ payout_id }}).

Bu genellikle yanlış ödeme bilgileri veya ödeme sağlayıcınızla ilgili bir sorun nedeniyle olur.

Lütfen affiliate panelinizdeki ödeme bilgilerinizi güncelleyin ve bu sorunu çözmek için destek ekibimize ulaşın.

Ödeme bilgilerini güncelle: {{ portal_url }}

{{ shop_name }}
Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.