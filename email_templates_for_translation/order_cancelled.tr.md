---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Siparişiniz #{{ order_number }} İptal Edildi

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sipariş İptal Edildi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişiniz <strong>#{{ order_number }}</strong> iptal edildi.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Neden:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Eğer ödeme yapıldıysa, iade işlemi orijinal ödeme yöntemi üzerinden yapılacaktır.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sipariş Detayı Görüntüle
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sipariş İptal Edildi

Merhaba {{ customer_name }},

Siparişiniz #{{ order_number }} iptal edildi.

{% if cancellation_reason %}Neden: {{ cancellation_reason }}{% endif %}

Eğer ödeme yapıldıysa, iade işlemi orijinal ödeme yöntemi üzerinden yapılacaktır.

{% if order_url %}Sipariş detaylarını görüntüleyin: {{ order_url }}{% endif %}

Bu iptal hakkında sorularınız var mı?
E-posta: {{ support_email }}
Telefon: {{ support_phone }}