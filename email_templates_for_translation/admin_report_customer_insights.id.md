---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Insights Pelanggan - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Insights Pelanggan
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analitik Pelanggan
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Pelanggan:</strong> {{ total_customers }}<br/>
              <strong>Pelanggan Baru:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Rate Retensi:</strong> {{ retention_rate }}%<br/>
              <strong>Rata-rata CLV:</strong> {{ avg_clv }}<br/>
              <strong>Rate Pembelian Ulang:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Insights:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Laporan Lengkap
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 INSIGHTS PELANGGAN

Analitik Pelanggan

METRICS:
- Total Pelanggan: {{ total_customers }}
- Pelanggan Baru: {{ new_customers }} ({{ new_customer_rate }}%)
- Rate Retensi: {{ retention_rate }}%
- Rata-rata CLV: {{ avg_clv }}
- Rate Pembelian Ulang: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

Lihat laporan lengkap: {{ full_report_url }}