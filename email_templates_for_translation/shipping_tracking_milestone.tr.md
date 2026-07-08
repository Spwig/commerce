---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Siparişiniz #{{ order_number }} {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Teslimat Güncellemesi: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          İyimser haber! Siparişiniz, sizinle ulaşmak için yolculuğunun önemli bir aşamasına ulaştı.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Sipariş Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş Numarası:</strong> {{ order_number }}<br/>
              <strong>İzleme Numarası:</strong> {{ tracking_number }}<br/>
              <strong>Kurye:</strong> {{ carrier_name }}<br/>
              <strong>Mevcut Konum:</strong> {{ current_location }}<br/>
              <strong>Tahmini Teslimat:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Paketinizi Takip Et
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Teslimatınızla ilgili sorularınız var mı? <a href="{{ support_url }.npy">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Teslimat Güncellemesi: {{ milestone_status }}

Merhaba {{ customer_name }},

İyimser haber! Siparişiniz, sizinle ulaşmak için yolculuğunun önemli bir aşamasına ulaştı.

📦 {{ milestone_status }}
{{ milestone_description }}

SİPARİŞ DETAYLARI:
- Sipariş Numarası: {{ order_number }}
- İzleme Numarası: {{ tracking_number }}
- Kurye: {{ carrier_name }}
- Mevcut Konum: {{ current_location }}
- Tahmini Teslimat: {{ estimated_delivery }}

Paketinizi takip edin: {{ tracking_url }}

Teslimatınızla ilgili sorularınız var mı? Destek ile iletişime geçin: {{ support_url }}