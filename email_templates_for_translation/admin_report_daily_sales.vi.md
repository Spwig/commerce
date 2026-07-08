---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Báo cáo doanh số hàng ngày - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Báo cáo doanh số hàng ngày
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng kết doanh số - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tổng doanh thu:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Đơn hàng:</strong> {{ order_count }}<br/>
              <strong>Giá trị trung bình đơn hàng:</strong> {{ avg_order_value }}<br/>
              <strong>Tỷ lệ chuyển đổi:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số lượt truy cập:</strong> {{ visitor_count }}<br/>
              <strong>Khách hàng mới:</strong> {{ new_customers }}<br/>
              <strong>Khách hàng quay lại:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sản phẩm nổi bật:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} đơn hàng ({{ product.revenue }})
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
📊 BÁO CÁO DOANH SỐ HÀNG NGÀY

Tổng kết doanh số - {{ report_date }}

HIỆN THẢI:
- Tổng doanh thu: {{ total_revenue }}
- Đơn hàng: {{ order_count }}
- Giá trị trung bình đơn hàng: {{ avg_order_value }}
- Tỷ lệ chuyển đổi: {{ conversion_rate }}%

LUỒNG TRUY CẬP:
- Số lượt truy cập: {{ visitor_count }}
- Khách hàng mới: {{ new_customers }}
- Khách hàng quay lại: {{ returning_customers }}

SẢN PHẨM NỔI BẬT:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} đơn hàng ({{ product.revenue }})
{% endfor %}

Xem báo cáo đầy đủ: {{ full_report_url }}