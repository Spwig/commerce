---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Komisyon Kazandınız: {{ commission_amount }}!

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
          💰 Komisyon Kazandınız!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ shop_name }} dan müjde!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Komisyonunuz
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          #{{ order_number }} Siparişinden
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
          TEBRİKLER! #{{ order_number }} siparişinden {{ commission_amount }} komisyon kazandınız.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }}'i daha fazla tanıtın ve daha fazla komisyon kazanın. Ne kadar satış yaparsanız kazançınız da o kadar artar!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Sipariş Numarası:</strong> #{{ order_number }}<br/>
          <strong>Komisyon Tutarı:</strong> {{ commission_amount }}<br/>
          <strong>Komisyon Oranı:</strong> {{ commission_rate }}%
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
          Sorularınız mı var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ commission_amount }} komisyon kazandınız!

Merhaba {{ affiliate_name }},

Tebrikler! #{{ order_number }} siparişinden {{ commission_amount }} komisyon kazandınız.

Komisyon Detayı:
- Sipariş Numarası: #{{ order_number }}
- Komisyon Tutarı: {{ commission_amount }}
- Komisyon Oranı: {{ commission_rate }}%

{{ shop_name }}'i daha fazla tanıtın ve daha fazla komisyon kazanın.

Panelinizi görüntüleyin: {{ portal_url }}

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin