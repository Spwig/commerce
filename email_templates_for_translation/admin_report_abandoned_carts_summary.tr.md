---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Bırakılan Sepet Raporu - {{ abandoned_count }} sepet ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Bırakılan Sepet Raporu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sepet Bırakma Özeti
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Dönem:</strong> {{ report_period }}<br/>
              <strong>Bırakılan Sepetler:</strong> {{ abandoned_count }}<br/>
              <strong>Bırakılan Değer:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Bırakma Oranı:</strong> {{ abandonment_rate }}%<br/>
              <strong>Kurtarma Oranı:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En İyi Sebepler (izleniyorsa):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ayrıntıları Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 BIRAKILAN SEPET RAPORU

Sepet Bırakma Özeti

METRICS:
- Dönem: {{ report_period }}
- Bırakılan Sepetler: {{ abandoned_count }}
- Bırakılan Değer: {{ abandoned_value }}
- Bırakma Oranı: {{ abandonment_rate }}%
- Kurtarma Oranı: {{ recovery_rate }}%

EN İYİ SEBEPLER:
{{ top_reasons }}

Ayrıntıları Görüntüle: {{ full_report_url }}