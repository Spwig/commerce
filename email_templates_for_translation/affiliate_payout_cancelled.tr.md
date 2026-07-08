---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Ödeme iptal edildi - {{ payout_amount }}

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
          Ödeme İptal Edildi
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
          {{ payout_amount }} (Ödeme Kimliği: {{ payout_id }}) ödemeniz iptal edildi.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu ödeme nedeniyle sorularınız varsa, lütfen destek ekibimizle iletişime geçin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Affiliate Panelini Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız varsa? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ödeme iptal edildi - {{ payout_amount }}

Merhaba {{ affiliate_name }},

{{ payout_amount }} (Ödeme Kimliği: {{ payout_id }}) ödemeniz iptal edildi.

Bu ödeme nedeniyle sorularınız varsa, lütfen destek ekibimizle iletişime geçin.

Affiliate Panelini Görüntüle: {{ portal_url }}

{{ shop_name }}
Sorularınız varsa? {{ support_email }} ile iletişime geçin