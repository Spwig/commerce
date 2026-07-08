---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Müşteri Görüşleri - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 MÜŞTERİ GÖRÜŞLERİ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Müşteri Analitiği
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Toplam Müşteriler:</strong> {{ total_customers }}<br/>
              <strong>Yeni Müşteriler:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Müşteri Bağlantılılık Oranı:</strong> {{ retention_rate }}%<br/>
              <strong>Ortalama CLV:</strong> {{ avg_clv }}<br/>
              <strong>Yinelenen Satın Alma Oranı:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Görüşler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Raporu Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 MÜŞTERİ GÖRÜŞLERİ

Müşteri Analitiği

METRICS:
- Toplam Müşteriler: {{ total_customers }}
- Yeni Müşteriler: {{ new_customers }} ({{ new_customer_rate }}%)
- Müşteri Bağlantılılık Oranı: {{ retention_rate }}%
- Ortalama CLV: {{ avg_clv }}
- Yinelenen Satın Alma Oranı: {{ repeat_purchase_rate }}%

GÖRÜŞLER:
{{ insights }}

Raporu Görüntüle: {{ full_report_url }}