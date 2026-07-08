---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Paket Anda #{{ order_number }} telah dikirim!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Pesanan Dikirim!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dalam Perjalanan!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! Pesanan Anda telah dikirim dan sedang dalam perjalanan ke Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pengiriman:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>No. Pesanan:</strong> {{ order_number }}<br/>
              <strong>No. Pelacakan:</strong> {{ tracking_number }}<br/>
              <strong>Pengirim:</strong> {{ carrier_name }}<br/>
              <strong>Est. Pengiriman:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lacak Paket Anda
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PESANAN DIKIRIM!

Dalam Perjalanan!

Hi {{ customer_name }},

Berita baik! Pesanan Anda telah dikirim dan sedang dalam perjalanan ke Anda.

DETAIL PENGIRIMAN:
- No. Pesanan: {{ order_number }}
- No. Pelacakan: {{ tracking_number }}
- Pengirim: {{ carrier_name }}
- Est. Pengiriman: {{ estimated_delivery }}

Lacak paket Anda: {{ tracking_url }}