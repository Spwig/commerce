---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Siparişiniz #{{ order_number }} - Teslimat Gecikmesi

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Siparişinizin Güncellemesi
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinizle ilgili bir gecikme olduğunu bildirmek istedik. Bu olumsuzluğu için özür dileriz ve sabrınız için teşekkür ederiz.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Sipariş Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş Numarası:</strong> {{ order_number }}<br/>
              <strong>Asıl Teslimat Tarihi:</strong> {{ original_delivery_date }}<br/>
              <strong>Yeni Teslimat Tarihi:</strong> {{ new_delivery_date }}<br/>
              <strong>İzleme Numarası:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gecikmenin Nedeni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Siparişinizi Takip Et
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Siparişinizi mümkün olduğu kadar çabuk size ulaştırmak için çalışıyoruz. Paketiniz yola çıktıktan sonra başka bir güncelleme alacaksınız.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorularınız varsa <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">müşteri hizmetlerimizle iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Siparişinizin Güncellemesi #{{ order_number }}

Merhaba {{ customer_name }},

Siparişinizle ilgili bir gecikme olduğunu bildirmek istedik. Bu olumsuzluğu için özür dileriz ve sabrınız için teşekkür ederiz.

SİPARİŞ DETAYLARI:
- Sipariş Numarası: {{ order_number }}
- Asıl Teslimat Tarihi: {{ original_delivery_date }}
- Yeni Teslimat Tarihi: {{ new_delivery_date }}
- İzleme Numarası: {{ tracking_number }}

GEÇİKMENİN NEDENİ:
{{ delay_reason }}

Siparişinizi takip edin: {{ tracking_url }}

Siparişinizi mümkün olduğu kadar çabuk size ulaştırmak için çalışıyoruz. Paketiniz yola çıktıktan sonra başka bir güncelleme alacaksınız.

Sorularınız varsa müşteri hizmetlerimizle iletişime geçin: {{ support_url }}

---
Bu güncelleme, {{ shop_name }}'da #{{ order_number }} siparişi için yapılmıştır.