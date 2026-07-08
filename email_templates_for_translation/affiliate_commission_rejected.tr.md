---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Komisyon durumu güncelleme - Sipariş #{{ order_number }}

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
          Komisyon Durumu Güncellemesi
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
          Sipariş #{{ order_number }} ({{ commission_amount }}) için komisyonunuz onaylanmadığını bildirmek istedik.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu, genellikle komisyon dönemi bitmeden önce bir sipariş iptal edildiğinde veya iade edildiğinde olur.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu komisyon hakkında sorularınız varsa, lütfen destek ekibimize ulaşın.
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
          Sorularınız mı var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Komisyon durumu güncelleme - Sipariş #{{ order_number }}

Merhaba {{ affiliate_name }},

Sipariş #{{ order_number }} ({{ commission_amount }}) için komisyonunuz onaylanmadığını bildirmek istedik.

Bu, genellikle komisyon dönemi bitmeden önce bir sipariş iptal edildiğinde veya iade edildiğinde olur.

Bu komisyon hakkında sorularınız varsa, lütfen destek ekibimize ulaşın.

Affiliate panelini görüntüleyin: {{ portal_url }}

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin

