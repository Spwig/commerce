---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
Komisyon onaylandı: {{ commission_amount }}

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
          ✓ Komisyon Onaylandı!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Ödeme için onaylandı
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
          {{ commission_amount }} tutarındaki komisyonunuz, #{{ order_number }} siparişinden onaylandı ve bir sonraki ödeme işlemlerinizde dahil edilecektir.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ödemeler, ödeme planınıza göre işlenir. Ödemenin işlendiği zaman, başka bir e-posta alacaksınız.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Komisyonları Görüntüle
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
Komisyon onaylandı: {{ commission_amount }}

Merhaba {{ affiliate_name }},

{{ commission_amount }} tutarındaki komisyonunuz, #{{ order_number }} siparişinden onaylandı ve bir sonraki ödeme işlemlerinizde dahil edilecektir.

Ödemeler, ödeme planınıza göre işlenir. Ödemenin işlendiği zaman, başka bir e-posta alacaksınız.

Komisyonlarınızı görüntüleyin: {{ portal_url }}

{{ shop_name }}
Sorularınız var mı? {{ support_email }} ile iletişime geçin