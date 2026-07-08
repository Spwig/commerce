---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Pengembalian Dana Selesai - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Pengembalian Dana Selesai
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Pengembalian untuk pesanan <strong>#{{ order_number }}</strong> telah diperiksa dan pengembalian dana Anda telah diproses.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Detail Pengembalian
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Jumlah Pengembalian:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Biaya Pengembalian:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Catatan:</strong> Pengembalian mungkin memakan waktu 5-10 hari kerja untuk muncul di akun Anda, tergantung pada penyedia pembayaran Anda.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Jika Anda memiliki pertanyaan tentang pengembalian dana Anda, silakan hubungi tim dukungan kami.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pengembalian Dana Selesai - Pesanan #{{ order_number }}

Hi {{ customer_name }},

Pengembalian untuk pesanan #{{ order_number }} telah diperiksa dan pengembalian dana Anda telah diproses.

Detail Pengembalian:
- Jumlah Pengembalian: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Biaya Pengembalian: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Catatan: Pengembalian mungkin memakan waktu 5-10 hari kerja untuk muncul di akun Anda, tergantung pada penyedia pembayaran Anda.

Jika Anda memiliki pertanyaan tentang pengembalian dana Anda, silakan hubungi tim dukungan kami.