---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Transaksi Berharga Tinggi: {{ transaction_amount }} di {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Transaksi Berharga Tinggi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Transaksi Besar Telah Diproses
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah transaksi sebesar {{ transaction_amount }} telah diproses di {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Transaksi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Jumlah:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasir:</strong> {{ cashier_name }}<br/>
              <strong>Waktu:</strong> {{ transaction_time }}<br/>
              <strong>ID Transaksi:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informasi Pembayaran:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Barang:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Jumlah Total Barang:</strong> {{ item_count }}<br/>
              <strong>Subtotal:</strong> {{ subtotal }}<br/>
              <strong>Pajak:</strong> {{ tax_amount }}<br/>
              <strong>Total:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informasi Pelanggan:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Pemberitahuan ini dikirim untuk semua transaksi yang melebihi {{ threshold_amount }} dengan tujuan pencegahan penipuan dan pemantauan.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Transaksi
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Struk
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 TRANSAKSI BERHARGA TINGGI

Transaksi Besar Telah Diproses

Sebuah transaksi sebesar {{ transaction_amount }} telah diproses di {{ terminal_name }}.

DETAIL TRANSAKSI:
- Jumlah: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Kasir: {{ cashier_name }}
- Waktu: {{ transaction_time }}
- ID Transaksi: {{ transaction_id }}

INFORMASI PEMBAYARAN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

RINGKASAN BARANG:
- Jumlah Total Barang: {{ item_count }}
- Subtotal: {{ subtotal }}
- Pajak: {{ tax_amount }}
- Total: {{ transaction_amount }}

{% if customer_info %}
INFORMASI PELANGGAN:
{{ customer_info }}
{% endif %}

Pemberitahuan ini dikirim untuk semua transaksi yang melebihi {{ threshold_amount }} dengan tujuan pencegahan penipuan dan pemantauan.

Lihat transaksi: {{ transaction_url }}
Lihat struk: {{ receipt_url }}