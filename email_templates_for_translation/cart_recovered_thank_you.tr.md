---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Siparişiniz için teşekkür ederiz #{{ order_number }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Siparişiniz için teşekkür ederiz!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinizi tamamlamış olduğunuz için çok mutluyuz! Siparişiniz onaylandı ve kargonuza hazırlanıyor.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Sipariş Özeti
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş Numarası:</strong> {{ order_number }}<br/>
              <strong>Sipariş Tarihi:</strong> {{ order_date }}<br/>
              <strong>Toplam:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Siparişinizi Takip Et
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adımlar Nedir?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Siparişiniz hazırlanacak (genellikle 1-2 iş günü içinde)<br/>
          2. Kargo onayı ve takip bilgileri alacaksınız<br/>
          3. Siparişiniz şu adrese teslim edilecek: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Bilir misiniz?</strong><br/>
              Hesap panelinizde her zaman siparişinizi takip edebilirsiniz.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorularınız varsa, <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">destek ekibimize ulaşın</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 SİPARİŞİNİZ İÇİN TEŞEKKÜR EDERİZ!

Merhaba {{ customer_name }},

Siparişinizi tamamlamış olduğunuz için çok mutluyuz! Siparişiniz onaylandı ve kargonuza hazırlanıyor.

SİPARİŞ ÖZETİ:
- Sipariş Numarası: {{ order_number }}
- Sipariş Tarihi: {{ order_date }}
- Toplam: {{ order_total }}

Siparişinizi takip edin: {{ order_tracking_url }}

SONRAKİ ADIMLAR NEDİR?
1. Siparişiniz hazırlanacak (genellikle 1-2 iş günü içinde)
2. Kargo onayı ve takip bilgileri alacaksınız
3. Siparişiniz şu adrese teslim edilecek: {{ shipping_address }}

💡 BİLİYORDU MU?
Hesap panelinizde her zaman siparişinizi takip edebilirsiniz.

Sorularınız varsa, lütfen destek ekibimize ulaşın: {{ support_url }}

---
{{ shop_name }}'da #{{ order_number }} siparişi