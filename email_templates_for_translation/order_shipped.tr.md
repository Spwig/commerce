---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Siparişiniz #{{ order_number }} kargonun yola çıktığına dair bilgi!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Sipariş Kargoya Verildi!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yolunda!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Harika haber! Siparişiniz kargoya verildi ve size ulaşmak üzere yola çıkmıştır.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Kargo Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş #:</strong> {{ order_number }}<br/>
              <strong>İzleme #:</strong> {{ tracking_number }}<br/>
              <strong>Taşıyıcı:</strong> {{ carrier_name }}<br/>
              <strong>Tahmini Teslimat:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Paketinizi Takip Et
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 SİPARİŞ KARGOLANDI!

Yolunda!

Merhaba {{ customer_name }},

Harika haber! Siparişiniz kargoya verildi ve size ulaşmak üzere yola çıkmıştır.

KARGO AYRINTILARI:
- Sipariş #: {{ order_number }}
- İzleme #: {{ tracking_number }}
- Taşıyıcı: {{ carrier_name }}
- Tahmini Teslimat: {{ estimated_delivery }}

Paketinizi takip et: {{ tracking_url }}