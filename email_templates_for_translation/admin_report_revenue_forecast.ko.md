---
template_type: admin_report_revenue_forecast
category: Admin Reports
---

# Email Template: admin_report_revenue_forecast

## Subject
📈 수익 전망 - {{ forecast_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 수익 전망
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          예상 성과
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Forecast Period:</strong> {{ forecast_period }}<br/>
              <strong>Projected Revenue:</strong> <span style="font-size: 20px; color: #059669;">{{ projected_revenue }}</span><br/>
              <strong>Current Trend:</strong> {{ trend_direction }}<br/>
              <strong>Confidence:</strong> {{ confidence_level }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          분석:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ analysis }}
        </mj-text>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 사항:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          상세 전망 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 수익 전망

예상 성과

FORECAST:
- Forecast Period: {{ forecast_period }}
- Projected Revenue: {{ projected_revenue }}
- Current Trend: {{ trend_direction }}
- Confidence: {{ confidence_level }}%

ANALYSIS:
{{ analysis }}

{% if recommendations %}
RECOMMENDATIONS:
{{ recommendations }}
{% endif %}

상세 전망 보기: {{ full_report_url }}