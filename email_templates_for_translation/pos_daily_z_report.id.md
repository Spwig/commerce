---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Laporan Z Harian - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Laporan Z Harian
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Laporan Penyelesaian Akhir Hari
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ringkasan harian untuk {{ location_name }} pada {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Penjualan:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Penjualan:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Transaksi:</strong> {{ transaction_count }}<br/>
              <strong>Barang Terjual:</strong> {{ items_sold }}<br/>
              <strong>Rata-rata Penjualan:</strong> {{ average_sale }}<br/>
              <strong>Pajak yang Dikumpulkan:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Metode Pembayaran:
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
          Ringkasan Shift:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Shift:</strong> {{ shift_count }}<br/>
              <strong>Terminal yang Digunakan:</strong> {{ terminal_count }}<br/>
              <strong>Kasir Aktif:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Penjualan: {{ terminal.sales }} | Transaksi: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penyesuaian & Diskon:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Diskon yang Diberikan:</strong> {{ discounts_total }}<br/>
              <strong>Pengembalian Dana yang Dikeluarkan:</strong> {{ refunds_total }}<br/>
              <strong>Pembatalan:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Total Variasi Uang Tunai: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produk Terlaris:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} terjual ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Laporan Lengkap
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 LAPORAN Z HARIAN

Laporan Penyelesaian Akhir Hari

Ringkasan harian untuk {{ location_name }} pada {{ report_date }}.

RINGKASAN PENJUALAN:
- Total Penjualan: {{ total_sales }}
- Transaksi: {{ transaction_count }}
- Barang Terjual: {{ items_sold }}
- Rata-rata Penjualan: {{ average_sale }}
- Pajak yang Dikumpulkan: {{ tax_collected }}

METODE PEMBAYARAN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transaksi)
{% endfor %}

RINGKASAN SHIFT:
- Total Shift: {{ shift_count }}
- Terminal yang Digunakan: {{ terminal_count }}
- Kasir Aktif: {{ cashier_count }}

PECAHAN TERMINAL:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} transaksi
{% endfor %}

PENYESUAIAN & DISKON:
- Diskon yang Diberikan: {{ discounts_total }}
- Pengembalian Dana yang Dikeluarkan: {{ refunds_total }}
- Pembatalan: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ TOTAL VARIASI UANG TUNAI: {{ cash_variance }}
{{ variance_note }}
{% endif %}

PRODUK TERLARIS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} terjual ({{ product.revenue }})
{% endfor %}

Lihat laporan lengkap: {{ full_report_url }}