---
template_type: admin_report_top_products
category: Admin Reports
---

# Email Template: admin_report_top_products

## Subject
🏆 Báo cáo Sản phẩm Hàng đầu - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🏆 Báo cáo Sản phẩm Hàng đầu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sản phẩm bán chạy nhất - {{ report_period }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Theo doanh thu:
        </mj-text>

        {% for product in top_by_revenue %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              Doanh thu: {{ product.revenue }} | Doanh số: {{ product.units }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Theo số lượng bán:
        </mj-text>

        {% for product in top_by_units %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong><br/>
              Số lượng: {{ product.units }} | Doanh thu: {{ product.revenue }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem báo cáo đầy đủ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🏆 BÁO CÁO SẢN PHẨM HÀNG ĐẦU

Sản phẩm bán chạy nhất - {{ report_period }}

THEO DOANH THU:
{% for product in top_by_revenue %}
{{ product.rank }}. {{ product.name }}
Doanh thu: {{ product.revenue }} | Doanh số: {{ product.units }}
{% endfor %}

THEO SỐ LƯỢNG BÁN:
{% for product in top_by_units %}
{{ product.rank }}. {{ product.name }}
Số lượng: {{ product.units }} | Doanh thu: {{ product.revenue }}
{% endfor %}

Xem báo cáo đầy đủ: {{ full_report_url }}