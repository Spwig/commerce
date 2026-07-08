---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Sipariş #{{ order_number }} - Durum Güncellemesi: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sipariş Durumu Güncellemesi
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
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
          Siparişiniz <strong>#{{ order_number }}</strong> durumu güncellenmiştir.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Önceki Durum:</strong> {{ old_status_display }}<br/>
              <strong>Yeni Durum:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sipariş Detaylarını Görüntüle
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sipariş Durumu Güncellemesi - Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Siparişiniz #{{ order_number }} durumu güncellenmiştir.

Önceki Durum: {{ old_status_display }}
Yeni Durum: {{ new_status_display }}

{% if order_url %}Sipariş detaylarını görüntüleyin: {{ order_url }}{% endif %}