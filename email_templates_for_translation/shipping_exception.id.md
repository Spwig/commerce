---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Pengecualian Pengiriman - Pesanan #{{ order_number }} Memerlukan Perhatian

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Pengecualian Pengiriman
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami menulis untuk memberi tahu Anda mengenai pengecualian pada pengiriman Anda. Kami sedang berusaha menyelesaikan masalah ini secepat mungkin.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Detail Pengecualian:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Jenis Pengecualian:</strong> {{ exception_type }}<br/>
              <strong>Deskripsi:</strong> {{ exception_description }}<br/>
              <strong>Terjadi:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informasi Pesanan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Nomor Pesanan:</strong> {{ order_number }}<br/>
              <strong>Nomor Pelacakan:</strong> {{ tracking_number }}<br/>
              <strong>Pengirim:</strong> {{ carrier_name }}<br/>
              <strong>Lokasi Saat Ini:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Terjadi Selanjutnya?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Tindakan Diperlukan:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lacak Pesanan Anda
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Hubungi Dukungan
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PENGECAULIAN PENGIRIMAN

Hi {{ customer_name }},

Kami menulis untuk memberi tahu Anda mengenai pengecualian pada pengiriman Anda. Kami sedang berusaha menyelesaikan masalah ini secepat mungkin.

DETAIL PENGECAULIAN:
- Jenis Pengecualian: {{ exception_type }}
- Deskripsi: {{ exception_description }}
- Terjadi: {{ exception_date }}

INFORMASI PESANAN:
- Nomor Pesanan: {{ order_number }}
- Nomor Pelacakan: {{ tracking_number }}
- Pengirim: {{ carrier_name }}
- Lokasi Saat Ini: {{ current_location }}

APA YANG TERJADI SELANJUTNYA?
{{ resolution_steps }}

{% if action_required %}
⚠️ TINDAKAN DIPERLUKAN:
{{ action_required_description }}
{% endif %}

Lacak pesanan Anda: {{ tracking_url }}
Hubungi dukungan: {{ support_url }}