---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Laporan Pergantian: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Shift Ditutup
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Laporan Ringkasan Shift
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Shift ditutup di {{ terminal_name }} oleh {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Shift:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasir:</strong> {{ cashier_name }}<br/>
              <strong>Dibuka:</strong> {{ shift_started }}<br/>
              <strong>Ditutup:</strong> {{ shift_ended }}<br/>
              <strong>Durasi:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Penjualan:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Penjualan:</strong> {{ total_sales }}<br/>
              <strong>Transaksi:</strong> {{ transaction_count }}<br/>
              <strong>Barang Terjual:</strong> {{ items_sold }}<br/>
              <strong>Rata-rata Penjualan:</strong> {{ average_sale }}<br/>
              <strong>Pajak Terkumpul:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pemecahan Pembayaran:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transaksi)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Rekonsiliasi Kas:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Kas Awal:</strong> {{ opening_cash }}<br/>
              <strong>Jual Kas:</strong> {{ cash_sales }}<br/>
              <strong>Kas yang Diharapkan:</strong> {{ expected_cash }}<br/>
              <strong>Kas yang Dihitung:</strong> {{ counted_cash }}<br/>
              <strong>Perbedaan:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Ketidaksesuaian Kas: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Catatan: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Laporan Lengkap
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 SHIFT DITUTUP

Laporan Ringkasan Shift

Shift ditutup di {{ terminal_name }} oleh {{ cashier_name }}.

DETAIL SHIFT:
- Terminal: {{ terminal_name }}
- Kasir: {{ cashier_name }}
- Dibuka: {{ shift_started }}
- Ditutup: {{ shift_ended }}
- Durasi: {{ shift_duration }}

RINGKASAN PENJUALAN:
- Total Penjualan: {{ total_sales }}
- Transaksi: {{ transaction_count }}
- Barang Terjual: {{ items_sold }}
- Rata-rata Penjualan: {{ average_sale }}
- Pajak Terkumpul: {{ tax_collected }}

PEMECAHAN PEMBAYARAN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transaksi)
{% endfor %}

REKONSILIASI KAS:
- Kas Awal: {{ opening_cash }}
- Penjualan Kas: {{ cash_sales }}
- Kas yang Diharapkan: {{ expected_cash }}
- Kas yang Dihitung: {{ counted_cash }}
- Perbedaan: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ KETIDAKSESUAIAN KAS: {{ discrepancy_amount }}
{% if discrepancy_note %}Catatan: {{ discrepancy_note }}{% endif %}
{% endif %}

Lihat laporan lengkap: {{ shift_report_url }}