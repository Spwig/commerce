---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
İade İşlemi Tamamlandı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          İade İşlemi Tamamlandı
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Sipariş #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinize <strong>#{{ order_number }}</strong> ait iade talebiniz incelenmiş ve iade işleminiz tamamlanmıştır.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              İade Detayları
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>İade Tutarı:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>İade Ücreti:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Not:</strong> İade işleminizin hesabınıza yansıması, ödeme sağlayıcınıza bağlı olarak 5-10 iş günü sürebilir.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          İade ile ilgili sorularınız varsa lütfen destek ekibimize ulaşın.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade İşlemi Tamamlandı - Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Sipariş #{{ order_number }} ait iade talebiniz incelenmiş ve iade işleminiz tamamlanmıştır.

İade Detayları:
- İade Tutarı: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- İade Ücreti: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Not: İade işleminizin hesabınıza yansıması, ödeme sağlayıcınıza bağlı olarak 5-10 iş günü sürebilir.

İade ile ilgili sorularınız varsa lütfen destek ekibimize ulaşın.