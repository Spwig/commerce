---
template_type: admin_report_weekly_digest
category: Admin Reports
---

# Email Template: admin_report_weekly_digest

## Subject
📈 Haftalık Özeti - {{ week_range }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 Haftalık Özeti
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ week_range }} Haftası
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gelir:</strong> <span style="font-size: 20px; color: #059669;">{{ total_revenue }}</span> ({{ revenue_change }})<br/>
              <strong>Siparişler:</strong> {{ total_orders }} ({{ orders_change }})<br/>
              <strong>Yeni Müşteriler:</strong> {{ new_customers }}<br/>
              <strong>Ortalama Sipariş Değeri:</strong> {{ avg_order_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Öne Çıkanlar:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ highlights }}
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
📈 HAFTALIK ÖZETİ

{{ week_range }} Haftası

PERFORMANS:
- Gelir: {{ total_revenue }} ({{ revenue_change }})
- Siparişler: {{ total_orders }} ({{ orders_change }})
- Yeni Müşteriler: {{ new_customers }}
- Ortalama Sipariş Değeri: {{ avg_order_value }}

ÖNE ÇIKANLAR:
{{ highlights }}

Raporu Görüntüle: {{ full_report_url }}