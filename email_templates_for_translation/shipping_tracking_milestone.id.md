---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Pemesanan Anda #{{ order_number }} sedang {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pembaruan Pengiriman: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! Pesanan Anda telah mencapai titik penting dalam perjalanan ke Anda.
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
              Detail Pesanan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Nomor Pesanan:</strong> {{ order_number }}<br/>
              <strong>Nomor Pelacakan:</strong> {{ tracking_number }}<br/>
              <strong>Pengirim:</strong> {{ carrier_name }}<br/>
              <strong>Lokasi Saat Ini:</strong> {{ current_location }}<br/>
              <strong>Pengiriman Diperkirakan:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lacak Paket Anda
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Pertanyaan tentang pengiriman Anda? <a href="{{ support_url }.ip">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembaruan Pengiriman: {{ milestone_status }}

Hai {{ customer_name }},

Berita baik! Pesanan Anda telah mencapai titik penting dalam perjalanan ke Anda.

📦 {{ milestone_status }}
{{ milestone_description }}

DETAIL PESANAN:
- Nomor Pesanan: {{ order_number }}
- Nomor Pelacakan: {{ tracking_number }}
- Pengirim: {{ carrier_name }}
- Lokasi Saat Ini: {{ current_location }}
- Pengiriman Diperkirakan: {{ estimated_delivery }}

Lacak paket Anda: {{ tracking_url }}

Pertanyaan tentang pengiriman Anda? Hubungi Dukungan: {{ support_url }}