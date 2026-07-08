---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Komisyon geri alındı - Sipariş #{{ order_number }}

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
          Komisyon Geri Alındı
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
          Müşteri iadesi nedeniyle, sipariş #{{ order_number }} ({{ commission_amount }}) için komisyon geri alınmıştır.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Müşteriler iade talep ederse, ilişkili komisyonlar otomatik olarak geri alınır, böylece doğru muhasebe sağlanır.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu, afiliat prosesinin normal bir parçasıdır. {{ shop_name }}'i tanıtmayı sürdürün ve yeni komisyonlar kazanın!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Affiliate Panelini Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız var mı? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Komisyon geri alındı - Sipariş #{{ order_number }}

Merhaba {{ affiliate_name }},

Müşteri iadesi nedeniyle, sipariş #{{ order_number }} ({{ commission_amount }}) için komisyon geri alınmıştır.

Müşteriler iade talep ederse, ilişkili komisyonlar otomatik olarak geri alınır, böylece doğru muhasebe sağlanır.

Bu, afiliat prosesinin normal bir parçasıdır. {{ shop_name }}'i tanıtmayı sürdürün ve yeni komisyonlar kazanın!

Affiliate panelini görüntüleyin: {{ portal_url }}

{{ shop_name }}
Sorularınız var mı? {{ support_email }} ile iletişime geçin