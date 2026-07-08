---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Müdür {{ payout_amount }} ödemesi işleniyor

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
          💸 Ödeme İşleniyor
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Ödemenizin İşlenmesi
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
          İyimser haber! {{ payout_amount }} tutarındaki ödemeniz artık işlenmekte.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Para 3-5 iş günü içinde hesabınıza ulaşmalıdır. Ödeme tamamlandığında size başka bir e-posta göndereceğiz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Ödeme Kimliği:</strong> {{ payout_id }}<br/>
          <strong>Tutar:</strong> {{ payout_amount }}<br/>
          <strong>Ödeme Yöntemi:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ödeme Geçmişi Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız varsa <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Müdür {{ payout_amount }} ödemesi işleniyor

Merhaba {{ affiliate_name }},

İyimser haber! {{ payout_amount }} tutarındaki ödemeniz artık işlenmekte.

Ödeme Detayları:
- Ödeme Kimliği: {{ payout_id }}
- Tutar: {{ payout_amount }}
- Ödeme Yöntemi: {{ payout_method }}

Para 3-5 iş günü içinde hesabınıza ulaşmalıdır. Ödeme tamamlandığında size başka bir e-posta göndereceğiz.

Ödeme geçmişi görüntüle: {{ portal_url }}

{{ shop_name }}
Sorularınız varsa: {{ support_email }}