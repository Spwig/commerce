---
template_type: admin_report_top_products
category: Admin Reports
---

# Email Template: admin_report_top_products

## Subject
🏆 최상위 제품 보고서 - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🏆 최상위 제품 보고서
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          최고 판매 상품 - {{ report_period }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          매출 기준:
        </mj-text>

        {% for product in top_by_revenue %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              매출: {{ product.revenue }} | 판매량: {{ product.units }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          판매량 기준:
        </mj-text>

        {% for product in top_by_units %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              판매량: {{ product.units }} | 매출: {{ product.revenue }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          보고서 전체 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🏆 최상위 제품 보고서

최고 판매 상품 - {{ report_period }}

매출 기준:
{% for product in top_by_revenue %}
{{ product.rank }}. {{ product.name }}
매출: {{ product.revenue }} | 판매량: {{ product.units }}
{% endfor %}

판매량 기준:
{% for product in top_by_units %}
{{ product.rank }}. {{ product.name }}
판매량: {{ product.units }} | 매출: {{ product.revenue }}
{% endfor %}

보고서 전체 보기: {{ full_report_url }}