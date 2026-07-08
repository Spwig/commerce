---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Laporan Penjualan Harian - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Laporan Penjualan Harian
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Penjualan - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Pendapatan:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Pesanan:</strong> {{ order_count }}<br/>
              <strong>Nilai Pesanan Rata-rata:</strong> {{ avg_order_value }}<br/>
              <strong>Rate Konversi:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Pengunjung:</strong> {{ visitor_count }}<br/>
              <strong>Pelanggan Baru:</strong> {{ new_customers }}<br/>
              <strong>Pelanggan Kembali:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produk Teratas:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} penjualan ({{ product.revenue }})
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
📊 LAPORAN PENJUALAN HARIAN

Ringkasan Penjualan - {{ report_date }}

PERFORMA:
- Total Pendapatan: {{ total_revenue }}
- Pesanan: {{ order_count }}
- Nilai Pesanan Rata-rata: {{ avg_order_value }}
- Rate Konversi: {{ conversion_rate }}%

TRAFFIC:
- Pengunjung: {{ visitor_count }}
- Pelanggan Baru: {{ new_customers }}
- Pelanggan Kembali: {{ returning_customers }}

PRODUK TERATAS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} penjualan ({{ product.revenue }})
{% endfor %}

Lihat laporan lengkap: {{ full_report_url }}