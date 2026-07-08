---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Pembaruan untuk pesanan Anda #{{ order_number }} - Keterlambatan Pengiriman

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pembaruan untuk Pesanan Anda
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami ingin memberi tahu Anda tentang keterlambatan pesanan Anda. Kami memohon maaf atas ketidaknyamanan ini dan menghargai kesabaran Anda.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pesanan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Nomor Pesanan:</strong> {{ order_number }}<br/>
              <strong>ETA Awal:</strong> {{ original_delivery_date }}<br/>
              <strong>ETA Baru:</strong> {{ new_delivery_date }}<br/>
              <strong>Nomor Pelacakan:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alasan Keterlambatan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lacak Pesanan Anda
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Kami sedang bekerja keras untuk mengirimkan pesanan Anda secepat mungkin. Anda akan menerima pembaruan lain saat paket Anda dalam perjalanan.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Pertanyaan? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Hubungi tim layanan pelanggan kami</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembaruan untuk Pesanan Anda #{{ order_number }}

Hai {{ customer_name }},

Kami ingin memberi tahu Anda tentang keterlambatan pesanan Anda. Kami memohon maaf atas ketidaknyamanan ini dan menghargai kesabaran Anda.

DETAIL PESANAN:
- Nomor Pesanan: {{ order_number }}
- ETA Awal: {{ original_delivery_date }}
- ETA Baru: {{ new_delivery_date }}
- Nomor Pelacakan: {{ tracking_number }}

ALASAN KETERLAMBATAN:
{{ delay_reason }}

Lacak pesanan Anda: {{ tracking_url }}

Kami sedang bekerja keras untuk mengirimkan pesanan Anda secepat mungkin. Anda akan menerima pembaruan lain saat paket Anda dalam perjalanan.

Pertanyaan? Hubungi tim layanan pelanggan kami: {{ support_url }}

---

Pembaruan ini untuk pesanan #{{ order_number }} di {{ shop_name }}.