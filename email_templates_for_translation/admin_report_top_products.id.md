---
template_type: admin_report_top_products
category: Admin Reports
---

# Email Template: admin_report_top_products

## Subject
🏆 Laporan Produk Terbaik - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🏆 Laporan Produk Terbaik
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produk Terlaris - {{ report_period }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Berdasarkan Pendapatan:
        </mj-text>

        {% for product in top_by_revenue %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              Pendapatan: {{ product.revenue }} | Penjualan: {{ product.units }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Berdasarkan Unit Terjual:
        </mj-text>

        {% for product in top_by_units %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              Unit: {{ product.units }} | Pendapatan: {{ product.revenue }}
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
🏆 LAPORAN PRODUK TERBAIK

Produk Terlaris - {{ report_period }}

Berdasarkan Pendapatan:
{% for product in top_by_revenue %}
{{ product.rank }}. {{ product.name }}
Pendapatan: {{ product.revenue }} | Penjualan: {{ product.units }}
{% endfor %}

Berdasarkan Unit Terjual:
{% for product in top_by_units %}
{{ product.rank }}. {{ product.name }}
Unit: {{ product.units }} | Pendapatan: {{ product.revenue }}
{% endfor %}

Lihat laporan lengkap: {{ full_report_url }}